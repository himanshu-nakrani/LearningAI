"use client";
import { useEffect, useState } from "react";

/**
 * Reading progress bar — fixed at the top of the viewport.
 * Tracks the .prose article element specifically so the bar fills as the user
 * scrolls through the article (not the whole page).
 */
export function ReadingProgress() {
  const [pct, setPct] = useState(0);
  useEffect(() => {
    function update() {
      const article = document.querySelector<HTMLElement>(".prose");
      if (!article) {
        const top = window.pageYOffset || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - window.innerHeight;
        setPct(height > 0 ? (top / height) * 100 : 0);
        return;
      }
      const rect = article.getBoundingClientRect();
      const articleTopAbs = window.pageYOffset + rect.top;
      const articleHeight = article.offsetHeight;
      const viewportTop = window.pageYOffset;
      const viewportBottom = viewportTop + window.innerHeight;
      const articleBottomAbs = articleTopAbs + articleHeight;
      const readBottom = viewportBottom - articleTopAbs;
      const total = articleHeight;
      if (total <= 0) {
        setPct(viewportBottom >= articleBottomAbs ? 100 : 0);
        return;
      }
      const progress = Math.max(0, Math.min(100, (readBottom / total) * 100));
      setPct(progress);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);
  return <div className="reading-progress" style={{ width: `${pct}%` }} aria-hidden />;
}
