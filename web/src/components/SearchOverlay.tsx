"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearch } from "./SearchContext";
import styles from "./SearchOverlay.module.css";

type Section = { l: string; i: string; t: string; x: string };
type GuideIndex = { f: string; g: string; s: Section[] };
type Index = GuideIndex[];

type Hit = { guide: GuideIndex; sec: Section; score: number };

function escapeRE(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function highlight(s: string, terms: string[]) {
  let html = s.replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" })[c]!);
  for (const t of terms) {
    if (!t) continue;
    html = html.replace(new RegExp(`(${escapeRE(t)})`, "gi"), "<mark>$1</mark>");
  }
  return html;
}
function score(sec: Section, terms: string[]) {
  let s = 0;
  const title = sec.t.toLowerCase();
  const text = sec.x.toLowerCase();
  for (const t of terms) {
    if (title === t) s += 50;
    if (title.includes(t)) s += 10;
    if (title.startsWith(t)) s += 5;
    if (text.includes(t)) s += 1;
  }
  return s;
}

export function SearchOverlay() {
  const { isOpen, close } = useSearch();
  const [query, setQuery] = useState("");
  const [idx, setIdx] = useState<Index | null>(null);
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    inputRef.current?.focus();
    if (!idx) {
      // basePath is baked into asset URLs by Next, but JSON in /public is served
      // at `${basePath}/search-index.json`. Derive at runtime from a known asset path.
      const base =
        typeof window !== "undefined" && window.location.pathname.startsWith("/LearningAI")
          ? "/LearningAI"
          : "";
      fetch(`${base}/search-index.json`)
        .then((r) => r.json())
        .then((data: Index) => setIdx(data))
        .catch(() => setIdx([]));
    }
  }, [isOpen, idx]);

  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  const hits: Hit[] = [];
  if (idx && terms.length) {
    for (const g of idx) {
      for (const s of g.s) {
        const sc = score(s, terms);
        if (sc > 0) hits.push({ guide: g, sec: s, score: sc });
      }
    }
    hits.sort((a, b) => b.score - a.score);
    hits.splice(20);
  }

  function pickHref(h: Hit) {
    return `${h.guide.f}#${h.sec.i}`;
  }

  function onKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((v) => (hits.length ? (v + 1) % hits.length : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((v) => (hits.length ? (v - 1 + hits.length) % hits.length : 0));
    } else if (e.key === "Enter") {
      if (hits[active]) {
        const href = pickHref(hits[active]);
        window.location.href = href;
        close();
      }
    }
  }

  if (!isOpen) return null;

  return (
    <div
      className={`${styles.overlay} ${styles.open}`}
      role="dialog"
      aria-modal="true"
      aria-label="Search"
      onClick={(e) => {
        if (e.target === e.currentTarget) close();
      }}
    >
      <div className={styles.modal}>
        <input
          ref={inputRef}
          type="text"
          className={styles.input}
          placeholder="Search all guides…  (Esc to close, ↑↓ to navigate, Enter to open)"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setActive(0);
          }}
          onKeyDown={onKey}
          autoComplete="off"
          spellCheck={false}
        />
        <div className={styles.results}>
          {!terms.length && <div className={styles.empty}>Type to search across all guides.</div>}
          {terms.length > 0 && !hits.length && <div className={styles.empty}>No matches.</div>}
          {hits.map((h, i) => (
            <Link
              key={`${h.guide.f}-${h.sec.i}-${i}`}
              href={pickHref(h)}
              className={`${styles.result} ${i === active ? styles.active : ""}`}
              onClick={close}
            >
              <div
                className={styles.title}
                dangerouslySetInnerHTML={{ __html: highlight(h.sec.t, terms) }}
              />
              <div className={styles.meta}>
                {h.guide.g} · {h.sec.l}
              </div>
              <div
                className={styles.text}
                dangerouslySetInnerHTML={{ __html: highlight(h.sec.x.slice(0, 200), terms) }}
              />
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
