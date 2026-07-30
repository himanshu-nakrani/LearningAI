"use client";
import Link from "next/link";
import type { GuideMeta } from "@/lib/guides";
import styles from "./RelatedGuides.module.css";

type Props = { guides: GuideMeta[] };

export function RelatedGuides({ guides }: Props) {
  if (!guides.length) return null;
  return (
    <div className={styles.card}>
      <div className={styles.eyebrow}>Continue with</div>
      <ul className={styles.list}>
        {guides.slice(0, 3).map((g) => (
          <li key={g.slug}>
            <Link href={`/guides/${g.slug}`} className={styles.item}>
              <div className={styles.title}>{g.shortTitle}</div>
              <div className={styles.meta}>
                {g.difficulty ?? "Intermediate"} · {g.readMinutes ?? 30} min
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
