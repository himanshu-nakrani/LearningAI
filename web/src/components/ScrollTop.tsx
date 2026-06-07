"use client";
import { useEffect, useState } from "react";

export function ScrollTop() {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    function update() {
      setVisible((window.pageYOffset || document.documentElement.scrollTop) > 300);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, []);
  return (
    <button
      type="button"
      className={`scroll-top ${visible ? "visible" : ""}`}
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      aria-label="Scroll to top"
    >
      ↑
    </button>
  );
}
