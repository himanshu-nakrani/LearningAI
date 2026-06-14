import type { ReactNode } from "react";
import type { GuideMeta } from "@/lib/guides";
import { ScrollTop } from "./ScrollTop";
import { CopyButton } from "./CopyButton";

/**
 * Article shell — wraps the MDX content in .prose and applies the per-guide
 * accent via the data-accent attribute. The reading progress bar lives in
 * GuideLayout (which owns the guide reading chrome).
 */
export function GuideShell({
  guide,
  children,
}: {
  guide?: GuideMeta;
  children: ReactNode;
}) {
  return (
    <div
      data-accent={guide?.slug}
      className="guide-shell-root"
    >
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <main id="main" className="prose" tabIndex={-1}>
        {children}
      </main>
      <ScrollTop />
      <CopyButton />
    </div>
  );
}
