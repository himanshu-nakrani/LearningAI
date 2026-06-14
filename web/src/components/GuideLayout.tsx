import type { ReactNode } from "react";
import { GuideNav } from "./GuideNav";
import { GuideShell } from "./GuideShell";
import { ReadingProgress } from "./ReadingProgress";
import type { GuideMeta } from "@/lib/guides";
import styles from "./GuideLayout.module.css";

type Props = {
  guide: GuideMeta;
  siblings: GuideMeta[];
  currentSlug: string;
  /** True when the user is at a viewport where the in-guide left nav should be hidden. */
  compact?: boolean;
  children: ReactNode;
};

/**
 * Three-zone guide page layout (lives inside the AppShell's content slot).
 * Left  = GuideNav (sections + sibling guides)
 * Center = article (.prose)
 * Right  = provided by AppShell as rightRail (TOC + Related)
 */
export function GuideLayout({ guide, siblings, currentSlug, compact, children }: Props) {
  return (
    <div className={`${styles.layout} ${compact ? styles.compact : ""}`}>
      <ReadingProgress />
      {!compact && (
        <aside className={styles.guideNav} aria-label="Guide navigation">
          <GuideNav guide={guide} siblings={siblings} currentSlug={currentSlug} />
        </aside>
      )}
      <div className={styles.article}>
        <GuideShell guide={guide}>
          {children}
        </GuideShell>
      </div>
    </div>
  );
}
