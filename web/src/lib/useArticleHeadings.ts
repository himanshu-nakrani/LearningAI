"use client";
import { useEffect, useState } from "react";

export type ArticleHeading = { id: string; text: string; level: 2 | 3 };

/** Walks the .prose article to extract h2/h3 headings. Returns empty until mount. */
export function useArticleHeadings(articleSelector = ".prose"): ArticleHeading[] {
  const [headings, setHeadings] = useState<ArticleHeading[]>([]);

  useEffect(() => {
    const article = document.querySelector(articleSelector);
    if (!article) return;
    const els = Array.from(article.querySelectorAll<HTMLElement>("h2, h3"));
    const out: ArticleHeading[] = [];
    for (const el of els) {
      if (!el.id) continue;
      const level = el.tagName === "H2" ? 2 : 3;
      if (level !== 2 && level !== 3) continue;
      out.push({ id: el.id, text: el.textContent ?? "", level });
    }
    setHeadings(out);
  }, [articleSelector]);

  return headings;
}
