import { AppShell } from "@/components/AppShell";
import { PathCard } from "@/components/PathCard";
import { GuideCard, fromGuide, type GuideCardData } from "@/components/GuideCard";
import { ContinueLearning } from "@/components/ContinueLearning";
import { RecommendedNext } from "@/components/RecommendedNext";
import { PopularTopics } from "@/components/PopularTopics";
import { GUIDES, GLOSSARY_META } from "@/lib/guides";
import { LEARNING_PATHS } from "@/lib/learningPaths";
import styles from "./page.module.css";

/** Throws if a path references a guide slug that doesn't exist. Runs at module
 *  load so drift between the two data files is caught immediately. */
function resolvePath(path: (typeof LEARNING_PATHS)[number]) {
  const guides = path.guideSlugs.map((slug) => {
    const g = GUIDES.find((x) => x.slug === slug);
    if (!g) {
      throw new Error(
        `LearningPath "${path.id}" references unknown guide slug "${slug}". ` +
          `Update learningPaths.ts to match GUIDES.`,
      );
    }
    return g;
  });
  const total = guides.reduce((sum, g) => sum + (g.readMinutes ?? 30), 0);
  return { ...path, guides, totalReadMinutes: total };
}

export default function HomePage() {
  const paths = LEARNING_PATHS.map(resolvePath);

  const glossaryCard: GuideCardData = {
    href: GLOSSARY_META.href,
    title: GLOSSARY_META.shortTitle,
    description: GLOSSARY_META.description,
    category: "Glossary",
    navGroup: "reference",
    status: "Reference",
    difficulty: "Reference",
    readMinutes: GLOSSARY_META.readMinutes,
  };

  const allCards: GuideCardData[] = [
    ...GUIDES.map((g) => fromGuide(g)),
    glossaryCard,
  ];

  const totalMinutes = allCards.reduce((s, c) => s + (c.readMinutes ?? 0), 0);

  return (
    <AppShell
      rightRail={
        <>
          <ContinueLearning />
          <RecommendedNext />
          <PopularTopics />
        </>
      }
    >
      <div className={styles.home}>
        <header className={styles.hero}>
          <div className={styles.heroBadge}>
            <span className={styles.heroBadgeDot} aria-hidden />
            Study OS
          </div>
          <h1 className={styles.h1}>
            Learn AI engineering,{" "}
            <span className={styles.h1Accent}>end to end</span>
          </h1>
          <p className={styles.subhead}>
            A focused library of long-form study guides for AI engineers, agent builders,
            and cloud practitioners. Pick a path — or browse by topic.
          </p>
          <div className={styles.heroMeta}>
            <span className={styles.heroMetaItem}>
              <strong>{allCards.length}</strong> guides
            </span>
            <span className={styles.heroMetaSep} aria-hidden />
            <span className={styles.heroMetaItem}>
              <strong>{paths.length}</strong> learning paths
            </span>
            <span className={styles.heroMetaSep} aria-hidden />
            <span className={styles.heroMetaItem}>
              <strong>~{totalMinutes}</strong> min of reading
            </span>
          </div>
        </header>

        <section className={styles.section} aria-labelledby="paths-heading">
          <div className={styles.sectionHead}>
            <h2 id="paths-heading" className={styles.h2}>Learning paths</h2>
            <span className={styles.sectionMeta}>{paths.length} curated tracks</span>
          </div>
          <div className={styles.pathGrid}>
            {paths.map((p) => (
              <PathCard
                key={p.id}
                title={p.title}
                description={p.description}
                href={`/guides/${p.guides[0].slug}`}
                guideCount={p.guides.length}
                totalReadMinutes={p.totalReadMinutes}
                accent={p.accent}
                icon={pathIcon(p.id)}
              />
            ))}
          </div>
        </section>

        <section className={styles.section} aria-labelledby="guides-heading">
          <div className={styles.sectionHead}>
            <h2 id="guides-heading" className={styles.h2}>All guides</h2>
            <span className={styles.sectionMeta}>{allCards.length} guides</span>
          </div>
          <div className={styles.guideGrid}>
            {allCards.map((c) => (
              <GuideCard key={c.href} data={c} />
            ))}
          </div>
        </section>

        <footer className={styles.footer}>
          <span>
            Part of the{" "}
            <a
              href="https://github.com/himanshu-nakrani/LearningAI"
              target="_blank"
              rel="noreferrer"
              className={styles.footerLink}
            >
              LearningAI
            </a>{" "}
            repository.
          </span>
          <span className={styles.footerNote}>Open source · self-paced</span>
        </footer>
      </div>
    </AppShell>
  );
}

function pathIcon(id: string): React.ReactNode {
  switch (id) {
    case "ai-engineer":
      return <>◆</>;
    case "agent-builder":
      return <>◇</>;
    case "cloud-ai":
      return <>▲</>;
    case "interview-prep":
      return <>◎</>;
    default:
      return <>·</>;
  }
}
