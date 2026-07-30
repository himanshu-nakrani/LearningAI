"use client";
import { useEffect, useRef } from "react";
import { Sidebar } from "./Sidebar";
import { IconButton } from "./IconButton";
import styles from "./MobileNavDrawer.module.css";

type Props = {
  open: boolean;
  onClose: () => void;
};

function getFocusable(root: HTMLElement): HTMLElement[] {
  const sel =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"]), input:not([disabled])';
  return Array.from(root.querySelectorAll<HTMLElement>(sel));
}

export function MobileNavDrawer({ open, onClose }: Props) {
  const panelRef = useRef<HTMLDivElement>(null);
  const closeBtnRef = useRef<HTMLButtonElement>(null);
  const previouslyFocused = useRef<HTMLElement | null>(null);

  // Lock body scroll while open
  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [open]);

  // ESC closes + Tab trap + focus management
  useEffect(() => {
    if (!open) return;
    previouslyFocused.current = document.activeElement as HTMLElement | null;
    // Defer focus to the next frame so the panel is mounted.
    const focusTimer = setTimeout(() => closeBtnRef.current?.focus(), 0);

    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
        return;
      }
      if (e.key !== "Tab" || !panelRef.current) return;
      const focusables = getFocusable(panelRef.current);
      if (focusables.length === 0) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement as HTMLElement | null;
      if (e.shiftKey) {
        if (active === first || !panelRef.current.contains(active)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last || !panelRef.current.contains(active)) {
          e.preventDefault();
          first.focus();
        }
      }
    }
    document.addEventListener("keydown", onKey);
    return () => {
      clearTimeout(focusTimer);
      document.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  // Restore focus on close.
  useEffect(() => {
    if (open) return;
    const prev = previouslyFocused.current;
    if (prev && typeof prev.focus === "function") {
      setTimeout(() => prev.focus(), 0);
    }
  }, [open]);

  if (!open) return null;

  return (
    <div className={styles.root} role="dialog" aria-modal="true" aria-label="Navigation">
      <button
        type="button"
        className={styles.backdrop}
        onClick={onClose}
        aria-label="Close navigation"
        tabIndex={-1}
      />
      <div className={styles.panel} ref={panelRef}>
        <div className={styles.head}>
          <span className={styles.headTitle}>All guides</span>
          <IconButton aria-label="Close" onClick={onClose} ref={closeBtnRef}>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden>
              <path d="M3 3l8 8M11 3l-8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </IconButton>
        </div>
        <Sidebar onNavigate={onClose} />
      </div>
    </div>
  );
}
