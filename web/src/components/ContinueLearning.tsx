"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Card } from "./Card";
import { Chip } from "./Chip";
import type { GuideMeta } from "@/lib/guides";
import styles from "./ContinueLearning.module.css";

const STORAGE_KEY = "learningai.recent";

type Recent = {
  slug: string;
  href: string;
  title: string;
  shortTitle: string;
  accent: string;
  accentDark: string;
  accentSoft: string;
  difficulty?: string;
  readMinutes?: number;
  lastReadAt: string;
};

function readRecent(): Recent | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Recent;
    if (!parsed?.slug) return null;
    return parsed;
  } catch {
    return null;
  }
}

function relativeTime(iso: string): string {
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "recently";
  const diff = Date.now() - then;
  const min = Math.floor(diff / 60000);
  if (min < 1) return "just now";
  if (min < 60) return `${min}m ago`;
  const h = Math.floor(min / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  if (d < 30) return `${d}d ago`;
  return "a while ago";
}

export function ContinueLearning() {
  const [recent, setRecent] = useState<Recent | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setRecent(readRecent());
  }, []);

  return (
    <Card className={styles.card}>
      <div className={styles.eyebrow}>Continue learning</div>
      {!mounted ? (
        <div className={styles.placeholder} aria-hidden>&nbsp;</div>
      ) : !recent ? (
        <div className={styles.empty}>
          Start a guide to see your progress here.
        </div>
      ) : (
        <Link
          href={recent.href}
          className={styles.recent}
          style={
            {
              "--accent": recent.accent,
              "--accent-soft": recent.accentSoft,
            } as React.CSSProperties
          }
        >
          <div className={styles.recentHead}>
            <div className={styles.recentTitle}>{recent.shortTitle}</div>
            <div className={styles.recentTime}>{relativeTime(recent.lastReadAt)}</div>
          </div>
          <div className={styles.recentMeta}>
            {recent.difficulty && <Chip size="sm" intent="neutral">{recent.difficulty}</Chip>}
            {typeof recent.readMinutes === "number" && (
              <Chip size="sm" intent="neutral">{recent.readMinutes} min</Chip>
            )}
          </div>
          <div className={styles.recentCta}>
            Resume <span aria-hidden>→</span>
          </div>
        </Link>
      )}
    </Card>
  );
}

/** Public helper for guide pages — records the most recent visit. */
export function recordRecentVisit(guide: GuideMeta) {
  try {
    const payload: Recent = {
      slug: guide.slug,
      href: `/guides/${guide.slug}`,
      title: guide.title,
      shortTitle: guide.shortTitle,
      accent: guide.accent,
      accentDark: guide.accentDark,
      accentSoft: guide.accentSoft,
      difficulty: guide.difficulty,
      readMinutes: guide.readMinutes,
      lastReadAt: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // ignore — private mode / quota
  }
}
