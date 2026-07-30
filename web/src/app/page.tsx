import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { fromGuide, type GuideCardData } from "@/components/GuideCard";
import { GUIDES, GLOSSARY_META } from "@/lib/guides";
import { LEARNING_PATHS } from "@/lib/learningPaths";
import styles from "./page.module.css";

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

  const featured = allCards[0];
  const rest = allCards.slice(1);

  return (
    <AppShell wide>
      <div className={styles.home}>
        <header className={styles.masthead}>
          <div className={styles.mastLeft}>
            <div className={styles.kicker}>Study folio · Vol. 02</div>
            <h1 className={styles.h1}>Learn AI like a craft</h1>
          </div>
          <div className={styles.mastRight}>
            <strong className={styles.statNum}>{allCards.length} guides</strong>
            <p className={styles.statCopy}>
              Long-form notes for engineers who prefer depth over dashboards.
              Paths for builders, agents, cloud, and interviews.
            </p>
          </div>
        </header>

        <section className={styles.section} aria-labelledby="paths-heading">
          <div className={styles.sectionHead}>
            <h2 id="paths-heading" className={styles.h2}>Learning paths</h2>
            <span className={styles.sectionMeta}>{paths.length} tracks</span>
          </div>
          <div className={styles.pathStrip}>
            {paths.map((p, i) => (
              <Link
                key={p.id}
                href={`/guides/${p.guides[0].slug}`}
                className={styles.pathCell}
              >
                <span className={styles.pathNum}>{String(i + 1).padStart(2, "0")}</span>
                <h3 className={styles.pathTitle}>{p.title}</h3>
                <p className={styles.pathDesc}>{p.description}</p>
                <span className={styles.pathMeta}>
                  {p.guides.length} guides · {p.totalReadMinutes} min
                </span>
              </Link>
            ))}
          </div>
        </section>

        <section className={styles.section} aria-labelledby="guides-heading">
          <div className={styles.sectionHead}>
            <h2 id="guides-heading" className={styles.h2}>From the library</h2>
            <span className={styles.sectionMeta}>{allCards.length} guides</span>
          </div>
          <div className={styles.library}>
            {featured && (
              <Link href={featured.href} className={`${styles.card} ${styles.featured}`}>
                <span className={styles.cat}>
                  Lead · {featured.category}
                  {featured.status ? ` · ${featured.status}` : ""}
                </span>
                <h3 className={styles.cardTitle}>{featured.title}</h3>
                <p className={styles.cardDesc}>{featured.description}</p>
                <span className={styles.cardMeta}>
                  {featured.difficulty} · {featured.readMinutes ?? 30} min read
                </span>
              </Link>
            )}
            {rest.map((c) => (
              <Link key={c.href} href={c.href} className={styles.card}>
                <span className={styles.cat}>
                  {c.category}
                  {c.status ? ` · ${c.status}` : ""}
                </span>
                <h3 className={styles.cardTitle}>{c.title}</h3>
                <p className={styles.cardDesc}>{c.description}</p>
                <span className={styles.cardMeta}>
                  {c.difficulty ?? "Intermediate"} · {c.readMinutes ?? 30} min
                </span>
              </Link>
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
