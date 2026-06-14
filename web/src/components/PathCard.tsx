import Link from "next/link";
import type { ReactNode } from "react";
import { Card } from "./Card";
import { MetadataRow } from "./MetadataRow";
import styles from "./PathCard.module.css";

type Accent = "teal" | "lavender" | "cobalt" | "amber" | "green";

type Props = {
  title: string;
  description: string;
  href: string;
  guideCount: number;
  totalReadMinutes: number;
  icon: ReactNode;
  accent?: Accent;
};

export function PathCard({ title, description, href, guideCount, totalReadMinutes, icon, accent = "teal" }: Props) {
  return (
    <Link href={href} className={`${styles.link} ${styles[accent]}`}>
      <Card interactive className={styles.card}>
        <div className={styles.head}>
          <div className={styles.icon} aria-hidden>{icon}</div>
          <span className={styles.eyebrow}>Learning path</span>
        </div>
        <h3 className={styles.title}>{title}</h3>
        <p className={styles.desc}>{description}</p>
        <div className={styles.foot}>
          <MetadataRow
            size="md"
            items={[
              { label: `${guideCount} guide${guideCount === 1 ? "" : "s"}` },
              { label: `~${totalReadMinutes} min` },
            ]}
          />
          <span className={styles.cta}>
            Start <span aria-hidden>→</span>
          </span>
        </div>
      </Card>
    </Link>
  );
}
