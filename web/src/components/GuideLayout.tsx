import type { ReactNode } from "react";
import { GuideShell } from "./GuideShell";
import { ReadingProgress } from "./ReadingProgress";
import type { GuideMeta } from "@/lib/guides";
import styles from "./GuideLayout.module.css";

type Props = {
  guide: GuideMeta;
  /** Kept for API compatibility; sibling nav lives in the main sidebar. */
  siblings?: GuideMeta[];
  currentSlug?: string;
  /** @deprecated Left guide-nav rail removed for a cleaner reading layout. */
  compact?: boolean;
  children: ReactNode;
  /** Optional footer below the article (e.g. related guides). */
  footer?: ReactNode;
};

/**
 * Reading-first guide layout (inside AppShell content).
 * Single centered article column — no left guide rail.
 * Right TOC is provided by AppShell as rightRail.
 */
export function GuideLayout({ guide, children, footer }: Props) {
  return (
    <div className={styles.layout}>
      <ReadingProgress />
      <div className={styles.article}>
        <GuideShell guide={guide}>
          {children}
        </GuideShell>
        {footer && <div className={styles.footer}>{footer}</div>}
      </div>
    </div>
  );
}
