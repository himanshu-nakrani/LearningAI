"use client";
import { useSearch } from "./SearchContext";
import styles from "./SearchTrigger.module.css";

export function SearchTrigger() {
  const { open } = useSearch();
  return (
    <button type="button" className={styles.btn} onClick={open} aria-label="Search guides">
      Search <kbd className={styles.kbd}>⌘K</kbd>
    </button>
  );
}
