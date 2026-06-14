"use client";
import Link from "next/link";
import type { GuideMeta, NavGroup } from "@/lib/guides";
import styles from "./GuideNav.module.css";

type Props = {
  guide: GuideMeta;
  /** Other guides in the same navGroup. */
  siblings: GuideMeta[];
  /** Current slug, highlighted in the siblings list. */
  currentSlug: string;
};

const groupLabels: Record<NavGroup, string> = {
  ai: "AI guides",
  agents: "Agent guides",
  cloud: "Cloud guides",
  fundamentals: "Fundamentals",
  interview: "Interview prep",
  reference: "Reference",
};

export function GuideNav({ guide, siblings, currentSlug }: Props) {
  if (siblings.length === 0) return null;

  return (
    <aside className={styles.nav} aria-label={`More in ${groupLabels[guide.navGroup]}`}>
      <div className={styles.section}>
        <div className={styles.eyebrow}>{groupLabels[guide.navGroup]}</div>
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
    </aside>
  );
}
