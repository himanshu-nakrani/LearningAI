import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { BookNav } from "@/components/BookNav";
import { SearchProvider } from "@/components/SearchContext";
import { SearchOverlay } from "@/components/SearchOverlay";

export const metadata: Metadata = {
  title: {
    default: "Learning AI",
    template: "%s — Learning AI",
  },
  description:
    "Long-form study notes covering AI engineering, agentic AI, LLM inference, cloud AI platforms, and core software fundamentals.",
};

const noFlashScript = `
(function() {
  try {
    var t = localStorage.getItem('theme');
    if (!t && window.matchMedia('(prefers-color-scheme: dark)').matches) t = 'dark';
    if (t === 'dark') document.documentElement.classList.add('dark');
  } catch(e) {}
})();
`;

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script dangerouslySetInnerHTML={{ __html: noFlashScript }} />
      </head>
      <body>
        <SearchProvider>
          <BookNav />
          {children}
          <SearchOverlay />
        </SearchProvider>
      </body>
    </html>
  );
}
