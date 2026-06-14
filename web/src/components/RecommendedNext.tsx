import Link from "next/link";
import { Card } from "./Card";
import { GUIDES } from "@/lib/guides";
import styles from "./RecommendedNext.module.css";

type Props = {
  /** Optional current guide slug — recommendations avoid this one. */
  currentSlug?: string;
  /** Optional current nav group — recommendations will prefer same group. */
  currentGroup?: string;
  limit?: number;
};

export function RecommendedNext({ currentSlug, currentGroup, limit = 4 }: Props) {
  // Heuristic: same navGroup first (excluding current), then advanced/interview, then anything else.
  const sameGroup = GUIDES.filter(
    (g) => g.navGroup === currentGroup && g.slug !== currentSlug,
  );
  const advanced = GUIDES.filter(
    (g) => g.status === "Core" && g.slug !== currentSlug && !sameGroup.includes(g),
  );
  const rest = GUIDES.filter((g) => g.slug !== currentSlug && !sameGroup.includes(g) && !advanced.includes(g));

  const ordered = [...sameGroup, ...advanced, ...rest].slice(0, limit);

  return (
    <Card className={styles.card}>
      <div className={styles.eyebrow}>Recommended next</div>
      <ul className={styles.list}>
        {ordered.map((g) => (
          <li key={g.slug}>
            <Link
              href={`/guides/${g.slug}`}
              className={styles.item}
              style={
                {
                  "--accent": g.accent,
                } as React.CSSProperties
              }
            >
              <div className={styles.itemTitle}>{g.shortTitle}</div>
              <div className={styles.itemMeta}>
                {g.difficulty ?? "Intermediate"} · {g.readMinutes ?? 30} min
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </Card>
  );
}
