"use client";
import { useEffect, useState } from "react";
import { IconButton } from "./IconButton";

const KEY = "theme";

export function ThemeToggle() {
  // Start with the "off" state on both server and the first client render so
  // the markup matches exactly (no hydration mismatch on the label/icon).
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    setMounted(true);
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

  // Render nothing on the server / first client paint so the markup matches
  // exactly. After mount, the no-flash script has already applied the dark
  // class if appropriate, so the icon rendered here will match the visible
  // theme.
  if (!mounted) {
    return (
      <IconButton aria-label="Toggle theme" title="Toggle theme">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path
            d="M13 9.5A5.5 5.5 0 0 1 6.5 3a.5.5 0 0 0-.7-.5A7 7 0 1 0 13.5 10.2a.5.5 0 0 0-.5-.7z"
            stroke="currentColor"
            strokeWidth="1.4"
            strokeLinejoin="round"
          />
        </svg>
      </IconButton>
    );
  }

  return (
    <IconButton
      onClick={toggle}
      aria-label={theme === "dark" ? "Switch to light theme" : "Switch to dark theme"}
      title={theme === "dark" ? "Light theme" : "Dark theme"}
    >
      {theme === "dark" ? (
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
          <circle cx="8" cy="8" r="3" stroke="currentColor" strokeWidth="1.4" />
          <path d="M8 1.5v1.4M8 13.1v1.4M14.5 8h-1.4M2.9 8H1.5M12.6 3.4l-1 .1M4.4 11.6l-1 1M12.6 12.6l-1-1M4.4 4.4l-1-1" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
      ) : (
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path
            d="M13 9.5A5.5 5.5 0 0 1 6.5 3a.5.5 0 0 0-.7-.5A7 7 0 1 0 13.5 10.2a.5.5 0 0 0-.5-.7z"
            stroke="currentColor"
            strokeWidth="1.4"
            strokeLinejoin="round"
          />
        </svg>
      )}
    </IconButton>
  );
}
