"use client";
import { useState, type ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { TopBar, type BreadcrumbItem } from "./TopBar";
import { MobileNavDrawer } from "./MobileNavDrawer";
import styles from "./AppShell.module.css";

type Props = {
  children: ReactNode;
  /** Page-specific right rail (ContinueLearning, RecommendedNext, etc.). */
  rightRail?: ReactNode;
  /** Optional breadcrumb shown on guide / glossary pages. */
  breadcrumb?: BreadcrumbItem[];
  /** Optional content rendered inside the sidebar, below the main nav. */
  sidebarExtras?: ReactNode;
  /** Start with the sidebar collapsed (icons-only). Useful on guide pages where
   *  the article has its own left rail. The user can still expand. */
  defaultCollapsed?: boolean;
};

export function AppShell({
  children,
  rightRail,
  breadcrumb,
  sidebarExtras,
  defaultCollapsed = false,
}: Props) {
  const [navOpen, setNavOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(defaultCollapsed);

  return (
    <div className={`${styles.shell} ${collapsed ? styles.shellCollapsed : ""}`}>
      <div className={styles.sidebarHost}>
        <Sidebar collapsed={collapsed} />
        {sidebarExtras && !collapsed && (
          <div className={styles.sidebarExtras}>{sidebarExtras}</div>
        )}
      </div>

      <div className={styles.main}>
        <TopBar
          breadcrumb={breadcrumb}
          onOpenMobileNav={() => setNavOpen(true)}
        />

        <div className={styles.body}>
          <div className={styles.content}>{children}</div>
          {rightRail && (
            <aside className={styles.rail} aria-label="Page sidebar">
              {rightRail}
            </aside>
          )}
        </div>
      </div>

      <button
        type="button"
        className={`${styles.collapseToggle} ${collapsed ? styles.collapseToggleCollapsed : ""}`}
        onClick={() => setCollapsed((v) => !v)}
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden>
          {collapsed ? (
            <path d="M5 3l4 4-4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          ) : (
            <path d="M9 3l-4 4 4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          )}
        </svg>
      </button>

      <MobileNavDrawer open={navOpen} onClose={() => setNavOpen(false)} />
    </div>
  );
}
