"use client";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

type Ctx = {
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
};

const SearchCtx = createContext<Ctx | null>(null);

export function SearchProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((v) => !v), []);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const meta = e.metaKey || e.ctrlKey;
      if (meta && e.key.toLowerCase() === "k") {
        e.preventDefault();
        toggle();
      } else if (e.key === "/" && !isOpen) {
        const target = e.target as HTMLElement | null;
        if (target && ["INPUT", "TEXTAREA"].includes(target.tagName)) return;
        if (target?.isContentEditable) return;
        e.preventDefault();
        open();
      } else if (e.key === "Escape" && isOpen) {
        close();
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, close, toggle, isOpen]);

  const value = useMemo(() => ({ isOpen, open, close, toggle }), [isOpen, open, close, toggle]);
  return <SearchCtx.Provider value={value}>{children}</SearchCtx.Provider>;
}

export function useSearch() {
  const ctx = useContext(SearchCtx);
  if (!ctx) throw new Error("useSearch must be used within SearchProvider");
  return ctx;
}
