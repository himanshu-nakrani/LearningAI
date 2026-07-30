"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { buildSidebarSections, type NavItem, type NavSection } from "@/lib/nav";
import styles from "./Sidebar.module.css";

type Props = {
  collapsed?: boolean;
  onNavigate?: () => void;
};

export function Sidebar({ collapsed, onNavigate }: Props) {
  const pathname = usePathname();
  const sections: NavSection[] = buildSidebarSections();

  function isActive(item: NavItem): boolean {
    if (item.kind === "home") return pathname === "/";
    if (item.kind === "reference") return pathname?.startsWith("/glossary") ?? false;
    if (item.slug) return pathname === `/guides/${item.slug}` || pathname === `/guides/${item.slug}/`;
    return false;
  }

  return (
    <aside
      className={`${styles.sidebar} ${collapsed ? styles.collapsed : ""}`}
      aria-label="Primary navigation"
    >
      <Link href="/" className={styles.brand} onClick={onNavigate}>
        <span className={styles.brandMark} aria-hidden>
          AI
        </span>
        <span className={styles.brandText}>LearningAI</span>
      </Link>

      <nav className={styles.nav}>
        {sections.map((section) => (
          <div key={section.id} className={styles.section}>
            {!collapsed && <div className={styles.sectionLabel}>{section.label}</div>}
            <ul className={styles.list}>
              {section.items.map((item) => {
                const active = isActive(item);
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`${styles.item} ${active ? styles.active : ""}`}
                      onClick={onNavigate}
                      title={collapsed ? item.label : undefined}
                      aria-current={active ? "page" : undefined}
                    >
                      {item.icon && <span className={styles.icon} aria-hidden>{item.icon}</span>}
                      <span className={styles.label}>{item.label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      <div className={styles.footer}>
        {!collapsed && (
          <span className={styles.version}>Study OS · v2</span>
        )}
      </div>
    </aside>
  );
}
