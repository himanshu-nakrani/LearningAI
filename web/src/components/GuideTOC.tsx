"use client";
import { useEffect, useState } from "react";
import { useArticleHeadings, type ArticleHeading } from "@/lib/useArticleHeadings";
import styles from "./GuideTOC.module.css";

/** Pixels from the top of the viewport that count as "passed". */
const SCROLL_OFFSET = 120;

export function GuideTOC() {
  const headings = useArticleHeadings();
  const [activeId, setActiveId] = useState<string | null>(null);

  // Proper scroll-spy: on each scroll, find the last heading whose top is
  // above `viewport.top + SCROLL_OFFSET`. Whichever heading has most recently
  // passed that line is the active one — this matches how readers
  // conceptualize "what section am I in" and avoids sticking to whichever
  // heading happens to render first at the top of the viewport.
  useEffect(() => {
    if (!headings.length) return;

    let raf = 0;
    function recompute() {
      raf = 0;
      const article = document.querySelector(".prose");
      if (!article) return;

      const targets: { id: string; top: number }[] = [];
      for (const h of headings) {
        const el = document.getElementById(h.id);
        if (el) targets.push({ id: h.id, top: el.getBoundingClientRect().top });
      }
      if (!targets.length) return;

      // Walk in document order (headings are already in doc order) and
      // pick the last one whose top is above the SCROLL_OFFSET line.
      let active: string | null = null;
      for (const t of targets) {
        if (t.top - SCROLL_OFFSET <= 0) {
          active = t.id;
        } else {
          break;
        }
      }
      // Edge case: if the user is scrolled past the very last heading,
      // keep the last heading active.
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
  }, [headings]);

  if (!headings.length) {
    return (
      <div className={styles.toc}>
        <div className={styles.eyebrow}>On this page</div>
        <div className={styles.placeholder}>&nbsp;</div>
      </div>
    );
  }

  return (
    <nav className={styles.toc} aria-label="Table of contents">
      <div className={styles.eyebrow}>On this page</div>
      <ul className={styles.list}>
        {headings.map((h) => {
          const isActive = activeId === h.id;
          return (
            <li
              key={h.id}
              className={`${h.level === 3 ? styles.nested : ""} ${isActive ? styles.activeItem : ""}`}
            >
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
