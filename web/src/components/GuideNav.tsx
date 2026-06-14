"use client";
import Link from "next/link";
import { useArticleHeadings } from "@/lib/useArticleHeadings";
import type { GuideMeta } from "@/lib/guides";
import styles from "./GuideNav.module.css";

type Props = {
  guide: GuideMeta;
  /** Other guides in the same navGroup. */
  siblings: GuideMeta[];
  /** Current slug, highlighted in the siblings list. */
  currentSlug: string;
};

export function GuideNav({ guide, siblings, currentSlug }: Props) {
  const headings = useArticleHeadings();

  // The left nav only shows top-level (H2) sections — the right rail TOC
  // is where H3 sub-sections live.
  const topHeadings = headings.filter((h) => h.level === 2);

  return (
    <aside className={styles.nav} aria-label={`Sections in ${guide.shortTitle}`}>
      <div className={styles.section}>
        <div className={styles.eyebrow}>In this guide</div>
        {topHeadings.length === 0 ? (
          <div className={styles.placeholder}>&nbsp;</div>
        ) : (
          <ul className={styles.list}>
            {topHeadings.map((h) => (
              <li key={h.id}>
                <a href={`#${h.id}`} className={styles.link}>{h.text}</a>
              </li>
            ))}
          </ul>
        )}
      </div>

      {siblings.length > 0 && (
        <div className={styles.section}>
          <div className={styles.eyebrow}>Related guides</div>
          <ul className={styles.list}>
            {siblings.map((g) => {
              const active = g.slug === currentSlug;
              return (
                <li key={g.slug}>
                  <Link
                    href={`/guides/${g.slug}`}
                    className={`${styles.sibling} ${active ? styles.siblingActive : ""}`}
                    style={
                      {
                        "--accent": g.accent,
                      } as React.CSSProperties
                    }
                  >
                    <span className={styles.siblingTitle}>{g.shortTitle}</span>
                    <span className={styles.siblingMeta}>
                      {g.readMinutes ?? 30} min
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </aside>
  );
}
