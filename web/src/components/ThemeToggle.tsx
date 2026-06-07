"use client";
import { useEffect, useState } from "react";
import styles from "./ThemeToggle.module.css";

const KEY = "theme";

export function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  useEffect(() => {
    const stored = (localStorage.getItem(KEY) as "light" | "dark" | null) ??
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    setTheme(stored);
    document.documentElement.classList.toggle("dark", stored === "dark");
  }, []);
  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    document.documentElement.classList.toggle("dark", next === "dark");
    localStorage.setItem(KEY, next);
  }
  return (
    <button
      type="button"
      className={styles.btn}
      onClick={toggle}
      aria-label={theme === "dark" ? "Toggle light mode" : "Toggle dark mode"}
    >
      {theme === "dark" ? "☀️" : "🌙"}
    </button>
  );
}
