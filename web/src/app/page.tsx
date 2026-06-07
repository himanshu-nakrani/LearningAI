import Link from "next/link";
import { GUIDES } from "@/lib/guides";
import styles from "./page.module.css";

const groupOrder: Array<{ key: "ai" | "cloud" | "fundamentals"; title: string }> = [
  { key: "ai", title: "AI & Machine Learning" },
  { key: "cloud", title: "Cloud Platforms" },
  { key: "fundamentals", title: "Software Engineering Fundamentals" },
];

export default function HomePage() {
  return (
    <main className={styles.main}>
      <h1 className={styles.h1}>Learning AI — Guides</h1>
      <p className={styles.tagline}>
        A consolidated index of long-form study notes covering AI engineering, cloud
        platforms, and core software fundamentals.
      </p>

      {groupOrder.map((group) => (
        <section key={group.key}>
          <h2 className={styles.h2}>{group.title}</h2>
          <div className={styles.grid}>
            {GUIDES.filter((g) => g.group === group.key).map((g) => (
              <Link
                key={g.slug}
                href={`/guides/${g.slug}`}
                className={styles.card}
                style={
                  {
                    "--card-accent": g.accent,
                    "--card-accent-dark": g.accentDark,
                  } as React.CSSProperties
                }
              >
                <div className={styles.cardTitle}>{g.shortTitle}</div>
                <div className={styles.cardDesc}>{g.description}</div>
              </Link>
            ))}
          </div>
        </section>
      ))}

      <section>
        <h2 className={styles.h2}>Reference</h2>
        <div className={styles.grid}>
          <Link
            href="/glossary"
            className={styles.card}
            style={{ "--card-accent": "#6b8e2e", "--card-accent-dark": "#a8c476" } as React.CSSProperties}
          >
            <div className={styles.cardTitle}>Glossary</div>
            <div className={styles.cardDesc}>
              Brief definitions of the key concepts and acronyms used across the guides —
              AI/ML, agents, inference, cloud, hardware, system design, Python, DSA.
            </div>
          </Link>
        </div>
      </section>

      <footer className={styles.footer}>
        Part of the <a href="https://github.com/himanshu-nakrani/LearningAI">LearningAI</a>{" "}
        repository.
      </footer>
    </main>
  );
}
