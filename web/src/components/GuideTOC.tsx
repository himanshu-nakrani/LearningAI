"use client";
import { useEffect, useMemo, useState } from "react";
import { useArticleHeadings } from "@/lib/useArticleHeadings";
import styles from "./GuideTOC.module.css";

/** Pixels from the top of the viewport that count as "passed". */
const SCROLL_OFFSET = 120;

/**
 * Quiet sticky outline of top-level (h2) sections only.
 * Nested h3s are omitted so the rail stays short and scannable.
 */
export function GuideTOC() {
  const headings = useArticleHeadings();
  const topLevel = useMemo(
    () => headings.filter((h) => h.level === 2),
    [headings],
  );
  const [activeId, setActiveId] = useState<string | null>(null);

  useEffect(() => {
    if (!topLevel.length) return;

    let raf = 0;
    function recompute() {
      raf = 0;
      const targets: { id: string; top: number }[] = [];
      for (const h of topLevel) {
        const el = document.getElementById(h.id);
        if (el) targets.push({ id: h.id, top: el.getBoundingClientRect().top });
      }
      if (!targets.length) return;

      let active: string | null = null;
      for (const t of targets) {
        if (t.top - SCROLL_OFFSET <= 0) {
          active = t.id;
        } else {
          break;
        }
      }
      if (!active && targets.length) active = targets[0].id;
      setActiveId(active);
    }

    function onScroll() {
      if (raf) return;
      raf = requestAnimationFrame(recompute);
    }

    recompute();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      if (raf) cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, [topLevel]);

  if (!topLevel.length) {
    return null;
  }

  return (
    <nav className={styles.toc} aria-label="Table of contents">
      <div className={styles.eyebrow}>On this page</div>
      <ul className={styles.list}>
        {topLevel.map((h) => {
          const isActive = activeId === h.id;
          return (
            <li key={h.id}>
              <a
                href={`#${h.id}`}
                className={`${styles.link} ${isActive ? styles.active : ""}`}
              >
                {h.text}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
