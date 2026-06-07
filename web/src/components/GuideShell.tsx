import type { ReactNode } from "react";
import type { GuideMeta } from "@/lib/guides";
import { ReadingProgress } from "./ReadingProgress";
import { ScrollTop } from "./ScrollTop";
import { CopyButton } from "./CopyButton";

export function GuideShell({
  guide,
  children,
}: {
  guide?: GuideMeta;
  children: ReactNode;
}) {
  const style = guide
    ? ({
        "--accent": guide.accent,
        "--accent-soft": guide.accentSoft,
      } as React.CSSProperties)
    : undefined;

  return (
    <div style={style}>
      <ReadingProgress />
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <main id="main" className="prose" tabIndex={-1}>
        {children}
      </main>
      <ScrollTop />
      <CopyButton />
      {guide && (
        <style
          // per-guide accent for dark mode too
          dangerouslySetInnerHTML={{
            __html: `html.dark { --accent: ${guide.accentDark}; --accent-soft: ${guide.accentSoftDark}; }`,
          }}
        />
      )}
    </div>
  );
}
