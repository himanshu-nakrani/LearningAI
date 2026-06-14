"use client";
import { useSearch } from "./SearchContext";
import { ThemeToggle } from "./ThemeToggle";
import { IconButton } from "./IconButton";
import { Kbd } from "./Kbd";
import styles from "./TopBar.module.css";
import Link from "next/link";

export type BreadcrumbItem = { label: string; href?: string };

type Props = {
  breadcrumb?: BreadcrumbItem[];
  /** When set, shows a hamburger that opens the mobile nav drawer. */
  onOpenMobileNav?: () => void;
};

export function TopBar({ breadcrumb, onOpenMobileNav }: Props) {
  const { open } = useSearch();

  return (
    <header className={styles.topbar}>
      <div className={styles.left}>
        {onOpenMobileNav && (
          <IconButton
            className={styles.menuBtn}
            aria-label="Open navigation"
            onClick={onOpenMobileNav}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
              <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </IconButton>
        )}
        <Link href="/" className={styles.brand}>
          <span className={styles.brandMark} aria-hidden>◆</span>
          <span>LearningAI</span>
        </Link>
        {breadcrumb && breadcrumb.length > 0 && (
          <nav className={styles.crumbs} aria-label="Breadcrumb">
            {breadcrumb.map((c, i) => (
              <span key={i} className={styles.crumb}>
                {i > 0 && <span className={styles.crumbSep} aria-hidden>/</span>}
                {c.href ? <Link href={c.href} className={styles.crumbLink}>{c.label}</Link> : <span className={styles.crumbCurrent}>{c.label}</span>}
              </span>
            ))}
          </nav>
        )}
      </div>

      <div className={styles.right}>
        <button
          type="button"
          className={styles.searchTrigger}
          onClick={open}
          aria-label="Search guides"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden>
            <circle cx="6" cy="6" r="4.5" stroke="currentColor" strokeWidth="1.4" />
            <path d="M9.5 9.5l3 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
          </svg>
          <span className={styles.searchLabel}>Search guides</span>
          <span className={styles.searchKbd}>
            <Kbd>⌘</Kbd>
            <Kbd>K</Kbd>
          </span>
        </button>
        <ThemeToggle />
      </div>
    </header>
  );
}
