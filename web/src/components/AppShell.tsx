"use client";
import { useState, type ReactNode } from "react";
import { TopBar, type BreadcrumbItem } from "./TopBar";
import { MobileNavDrawer } from "./MobileNavDrawer";
import styles from "./AppShell.module.css";

type Props = {
  children: ReactNode;
  /** Optional right rail (TOC on guide pages). */
  rightRail?: ReactNode;
  /** Optional breadcrumb shown on guide / glossary pages. */
  breadcrumb?: BreadcrumbItem[];
  /** @deprecated Folio layout has no desktop sidebar. */
  sidebarExtras?: ReactNode;
  /** @deprecated Folio layout has no desktop sidebar. */
  defaultCollapsed?: boolean;
  /** Wider magazine frame for the home page. */
  wide?: boolean;
};

/**
 * Paper Folio shell — top navigation frame, no permanent left sidebar.
 * Guide list lives in the mobile/menu drawer. Reading stays centered.
 */
export function AppShell({
  children,
  rightRail,
  breadcrumb,
  wide,
}: Props) {
  const [navOpen, setNavOpen] = useState(false);

  return (
    <div className={`${styles.shell} ${wide ? styles.wide : ""}`}>
      <TopBar
        breadcrumb={breadcrumb}
        onOpenMobileNav={() => setNavOpen(true)}
      />

      <div className={styles.frame}>
        <div className={`${styles.body} ${rightRail ? styles.withRail : ""}`}>
          <div className={styles.content}>{children}</div>
          {rightRail && (
            <aside className={styles.rail} aria-label="On this page">
              {rightRail}
            </aside>
          )}
        </div>
      </div>

      <MobileNavDrawer open={navOpen} onClose={() => setNavOpen(false)} />
    </div>
  );
}
