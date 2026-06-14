import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { SearchProvider } from "@/components/SearchContext";
import { CommandSearch } from "@/components/CommandSearch";

export const metadata: Metadata = {
  title: {
    default: "LearningAI Study OS",
    template: "%s — LearningAI",
  },
  description:
    "Long-form study notes for AI engineering, agents, cloud AI, and software engineering fundamentals.",
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
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: noFlashScript }} />
      </head>
      <body>
        <SearchProvider>
          {children}
          <CommandSearch />
        </SearchProvider>
      </body>
    </html>
  );
}
