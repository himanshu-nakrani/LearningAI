"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSearch } from "./SearchContext";
import { GUIDES } from "@/lib/guides";
import { Kbd } from "./Kbd";
import styles from "./CommandSearch.module.css";

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

/** Items inside the palette that can receive focus (for Tab trapping). */
function getFocusable(root: HTMLElement): HTMLElement[] {
  const sel = 'a[href], button:not([disabled]), input:not([disabled])';
  return Array.from(root.querySelectorAll<HTMLElement>(sel)).filter(
    (el) => !el.hasAttribute("data-focus-skip"),
  );
}

export function CommandSearch() {
  const { isOpen, close } = useSearch();
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [idx, setIdx] = useState<Index | null>(null);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [fetchAttempt, setFetchAttempt] = useState(0);
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  // Open: focus the input on mount (layout effect = before paint, before
  // other useEffects so document.activeElement at the time of focus is the
  // trigger button, which we capture via the input's onFocus).
  useLayoutEffect(() => {
    if (!isOpen) return;
    // Reset the captured trigger each time we open so we always restore to
    // the element that opened *this* palette session.
    previouslyFocused.current = null;
    inputRef.current?.focus();
  }, [isOpen]);

  // Open: fetch the index.
  useEffect(() => {
    if (!isOpen) return;
    setFetchError(null);
    if (idx) return;
    const base =
      typeof window !== "undefined" && window.location.pathname.startsWith("/LearningAI")
        ? "/LearningAI"
        : "";
    fetch(`${base}/search-index.json`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data: Index) => setIdx(data))
      .catch((err) => {
        setIdx(null);
        setFetchError(err instanceof Error ? err.message : "Search index unavailable");
      });
  }, [isOpen, idx, fetchAttempt]);

  // Close: restore focus, reset state.
  useEffect(() => {
    if (isOpen) return;
    setQuery("");
    setActive(0);
    const prev = previouslyFocused.current;
    if (prev && typeof prev.focus === "function") {
      setTimeout(() => prev.focus(), 0);
    }
  }, [isOpen]);

  function retry() {
    setIdx(null);
    setFetchError(null);
    setFetchAttempt((n) => n + 1);
  }

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

  const fallback: { href: string; title: string; meta: string }[] =
    !terms.length
      ? GUIDES.map((g) => ({ href: `/guides/${g.slug}`, title: g.title, meta: g.shortTitle }))
      : [];

  const totalRows = terms.length ? hits.length : fallback.length;

  function pickHref(h: Hit) {
    return `${h.guide.f}#${h.sec.i}`;
  }

  function navigate(href: string) {
    close();
    // Use client-side routing so we don't trigger a full reload.
    if (href.startsWith("#")) {
      // Hash-only navigation: scroll to the anchor on the current page.
      const el = document.getElementById(href.slice(1));
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        history.replaceState(null, "", href);
      }
      return;
    }
    const hashIdx = href.indexOf("#");
    if (hashIdx >= 0) {
      const path = href.slice(0, hashIdx);
      const hash = href.slice(hashIdx);
      router.push(path + hash);
    } else {
      router.push(href);
    }
  }

  function onKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((v) => (totalRows ? (v + 1) % totalRows : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((v) => (totalRows ? (v - 1 + totalRows) % totalRows : 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (terms.length && hits[active]) {
        navigate(pickHref(hits[active]));
      } else if (!terms.length && fallback[active]) {
        navigate(fallback[active].href);
      }
    } else if (e.key === "Escape") {
      e.preventDefault();
      close();
    } else if (e.key === "Tab") {
      // Trap Tab inside the modal between input and last focusable.
      const focusables = modalRef.current ? getFocusable(modalRef.current) : [];
      if (focusables.length === 0) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement as HTMLElement | null;
      if (e.shiftKey) {
        if (active === first || !modalRef.current?.contains(active)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last || !modalRef.current?.contains(active)) {
          e.preventDefault();
          first.focus();
        }
      }
    }
  }

  // Keep the active row in view
  useEffect(() => {
    const el = listRef.current?.querySelector<HTMLElement>(`[data-row="${active}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [active]);

  if (!isOpen) return null;

  return (
    <div
      className={styles.overlay}
      role="dialog"
      aria-modal="true"
      aria-label="Search"
      onClick={(e) => {
        if (e.target === e.currentTarget) close();
      }}
    >
      <div className={styles.modal} role="document" ref={modalRef} onKeyDown={(e) => {
        // Tab trap also fires when focus is outside the input (e.g. on a result link).
        if (e.key === "Tab") onKey(e as unknown as React.KeyboardEvent<HTMLInputElement>);
      }}>
        <div className={styles.head}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden className={styles.searchIcon}>
            <circle cx="6" cy="6" r="4.5" stroke="currentColor" strokeWidth="1.4" />
            <path d="M9.5 9.5l3 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className={styles.input}
            placeholder="Search guides…"
            value={query}
            onFocus={(e) => {
              // Capture the trigger at the moment the input gains focus —
              // it happens to be the element we want to restore to.
              if (!previouslyFocused.current) {
                previouslyFocused.current = e.relatedTarget as HTMLElement | null;
                if (!previouslyFocused.current) {
                  // Fallback: walk back through the activeElement chain.
                  previouslyFocused.current = document.activeElement as HTMLElement | null;
                }
              }
            }}
            onChange={(e) => {
              setQuery(e.target.value);
              setActive(0);
            }}
            onKeyDown={onKey}
            autoComplete="off"
            spellCheck={false}
            aria-label="Search query"
          />
          <span className={styles.kbdRow}>
            <Kbd>esc</Kbd>
          </span>
        </div>

        <div className={styles.results} ref={listRef}>
          {fetchError && (
            <div className={styles.empty}>
              <div>Search index unavailable ({fetchError}).</div>
              <button type="button" className={styles.retry} onClick={retry}>
                Retry
              </button>
            </div>
          )}

          {!fetchError && !terms.length && (
            <>
              <div className={styles.eyebrow}>Jump to a guide</div>
              {fallback.map((f, i) => (
                <Link
                  key={f.href}
                  href={f.href}
                  data-row={i}
                  className={`${styles.result} ${i === active ? styles.active : ""}`}
                  onClick={(e) => { e.preventDefault(); navigate(f.href); }}
                >
                  <div className={styles.title}>{f.title}</div>
                  <div className={styles.meta}>Guide</div>
                </Link>
              ))}
            </>
          )}

          {!fetchError && terms.length > 0 && !hits.length && (
            <div className={styles.empty}>
              No matches for <span className={styles.emptyQuery}>“{query}”</span>.
            </div>
          )}

          {!fetchError && terms.length > 0 && hits.length > 0 && (
            <>
              <div className={styles.eyebrow}>{hits.length} match{hits.length === 1 ? "" : "es"}</div>
              {hits.map((h, i) => (
                <Link
                  key={`${h.guide.f}-${h.sec.i}-${i}`}
                  href={pickHref(h)}
                  data-row={i}
                  className={`${styles.result} ${i === active ? styles.active : ""}`}
                  onClick={(e) => { e.preventDefault(); navigate(pickHref(h)); }}
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
            </>
          )}
        </div>

        <div className={styles.foot}>
          <span className={styles.hint}>
            <Kbd>↑</Kbd><Kbd>↓</Kbd> navigate
          </span>
          <span className={styles.hint}>
            <Kbd>↵</Kbd> open
          </span>
          <span className={styles.hint}>
            <Kbd>esc</Kbd> close
          </span>
        </div>
      </div>
    </div>
  );
}
