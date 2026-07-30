import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Fraunces, Manrope, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { SearchProvider } from "@/components/SearchContext";
import { CommandSearch } from "@/components/CommandSearch";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
  weight: ["500", "600", "700"],
});

const sans = Manrope({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
  weight: ["400", "500", "600", "700", "800"],
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
  weight: ["400", "500", "600"],
});

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
    <html
      lang="en"
      suppressHydrationWarning
      className={`${display.variable} ${sans.variable} ${mono.variable}`}
    >
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
