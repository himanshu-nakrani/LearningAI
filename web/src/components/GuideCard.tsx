import Link from "next/link";
import { Card } from "./Card";
import { Chip } from "./Chip";
import { MetadataRow } from "./MetadataRow";
import type { GuideMeta, NavGroup, GuideStatus, Difficulty } from "@/lib/guides";
import styles from "./GuideCard.module.css";

/** Minimal card shape — accepts both a real GuideMeta and ad-hoc card data
 *  (e.g. the glossary, which isn't a guide in the data sense). */
export type GuideCardData = {
  href: string;
  title: string;
  description: string;
  category: string; // short label shown on the chip (e.g. "AI", "Glossary")
  navGroup?: NavGroup; // drives the chip color
  status?: GuideStatus;
  difficulty?: Difficulty;
  readMinutes?: number;
};

type Props = {
  data: GuideCardData;
};

const navGroupLabel: Record<NavGroup, string> = {
  ai: "AI",
  agents: "Agents",
  cloud: "Cloud",
  fundamentals: "Fundamentals",
  interview: "Interview",
  reference: "Glossary",
};

const categoryToChipIntent: Record<string, "neutral" | "core" | "advanced" | "lavender" | "cobalt" | "warning" | "success"> = {
  ai: "core",
  agents: "lavender",
  cloud: "cobalt",
  fundamentals: "neutral",
  interview: "warning",
  reference: "neutral",
};

const statusToIntent: Record<GuideStatus, "core" | "advanced" | "neutral"> = {
  Core: "core",
  Advanced: "advanced",
  Reference: "neutral",
};

/** Construct card data from a real GuideMeta. */
export function fromGuide(g: GuideMeta): GuideCardData {
  return {
    href: `/guides/${g.slug}`,
    title: g.shortTitle,
    description: g.description,
    category: navGroupLabel[g.navGroup] ?? "Guide",
    navGroup: g.navGroup,
    status: g.status,
    difficulty: g.difficulty,
    readMinutes: g.readMinutes,
  };
}

export function GuideCard({ data }: Props) {
  const intent = (data.navGroup && categoryToChipIntent[data.navGroup]) ?? "neutral";
  const statusIntent = data.status ? statusToIntent[data.status] : undefined;
  const difficultyLabel = data.difficulty ?? "Intermediate";

  return (
    <Link href={data.href} className={styles.link}>
      <Card interactive className={styles.card}>
        <div className={styles.top}>
          <Chip intent={intent} size="sm">{data.category}</Chip>
          {statusIntent && data.status && <Chip intent={statusIntent} size="sm">{data.status}</Chip>}
        </div>
        <h3 className={styles.title}>{data.title}</h3>
        <p className={styles.desc}>{data.description}</p>
        <div className={styles.foot}>
          <MetadataRow
            size="sm"
            items={[
              { label: difficultyLabel },
              { label: `${data.readMinutes ?? 30} min` },
            ]}
          />
        </div>
      </Card>
    </Link>
  );
}
