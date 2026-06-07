"use client";
import { useEffect } from "react";

/** Attaches a "Copy" button to every `pre` rendered inside the prose article. */
export function CopyButton() {
  useEffect(() => {
    const article = document.querySelector(".prose");
    if (!article) return;
    const pres = Array.from(article.querySelectorAll("pre"));
    const cleanup: Array<() => void> = [];
    for (const pre of pres) {
      if (pre.querySelector(".copy-btn")) continue;
      if (pre.parentElement?.classList.contains("ascii")) continue;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy code to clipboard");
      Object.assign(btn.style, {
        position: "absolute",
        top: "8px",
        right: "8px",
        background: "var(--bg)",
        border: "1px solid var(--border)",
        color: "var(--muted)",
        fontFamily: "-apple-system, sans-serif",
        fontSize: "0.7em",
        padding: "3px 9px",
        borderRadius: "4px",
        cursor: "pointer",
        opacity: "0",
        transition: "opacity 0.15s ease, color 0.15s ease, border-color 0.15s ease",
        letterSpacing: "0.02em",
      });
      const code = pre.querySelector("code");
      const text = code?.innerText ?? pre.innerText;
      const onEnter = () => (btn.style.opacity = "1");
      const onLeave = () => (btn.style.opacity = "0");
      pre.addEventListener("mouseenter", onEnter);
      pre.addEventListener("mouseleave", onLeave);
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(text);
          btn.textContent = "Copied";
          btn.style.color = "var(--tip-bd)";
          btn.style.borderColor = "var(--tip-bd)";
          setTimeout(() => {
            btn.textContent = "Copy";
            btn.style.color = "var(--muted)";
            btn.style.borderColor = "var(--border)";
          }, 1400);
        } catch {
          btn.textContent = "Err";
        }
      });
      pre.appendChild(btn);
      cleanup.push(() => {
        pre.removeEventListener("mouseenter", onEnter);
        pre.removeEventListener("mouseleave", onLeave);
        btn.remove();
      });
    }
    return () => cleanup.forEach((f) => f());
  }, []);
  return null;
}
