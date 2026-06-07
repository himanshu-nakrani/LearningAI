"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { GUIDES } from "@/lib/guides";
import { ThemeToggle } from "./ThemeToggle";
import { SearchTrigger } from "./SearchTrigger";
import styles from "./BookNav.module.css";

export function BookNav() {
  const pathname = usePathname();
  const isCurrent = (href: string) =>
    pathname === href || pathname.startsWith(href + "/");

  return (
    <nav className={styles.root} aria-label="Guides navigation">
      <Link href="/" className={styles.home}>
        Home
      </Link>
      {GUIDES.map((g) => {
        const href = `/guides/${g.slug}`;
        return (
          <Link
            key={g.slug}
            href={href}
            className={isCurrent(href) ? `${styles.link} ${styles.current}` : styles.link}
          >
            {g.shortTitle}
          </Link>
        );
      })}
      <Link
        href="/glossary"
        className={
          isCurrent("/glossary") ? `${styles.link} ${styles.current}` : styles.link
        }
      >
        Glossary
      </Link>
      <SearchTrigger />
      <ThemeToggle />
    </nav>
  );
}
