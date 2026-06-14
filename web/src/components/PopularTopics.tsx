import Link from "next/link";
import { Card } from "./Card";
import styles from "./PopularTopics.module.css";

/** Curated popular topics. Hardcoded per brief — can become a build-time list later. */
const TOPICS: { label: string; href: string; count?: number }[] = [
  { label: "Transformers", href: "/guides/ai-engineering/#transformers" },
  { label: "RAG patterns", href: "/guides/agentic-ai/#retrieval-augmented-generation" },
  { label: "KV cache", href: "/guides/llm-inference/#kv-cache" },
  { label: "Quantization", href: "/guides/llm-inference/#quantization" },
  { label: "MCP", href: "/guides/agentic-ai/#model-context-protocol-mcp" },
  { label: "Multi-agent", href: "/guides/agentic-ai/#multi-agent-orchestration" },
  { label: "Vector databases", href: "/guides/ai-engineering/#vector-search" },
  { label: "RLHF / DPO", href: "/guides/ai-engineering/#rlhf-preference-fine-tuning" },
  { label: "System design basics", href: "/guides/system-design/" },
  { label: "DSA walkthroughs", href: "/guides/dsa/" },
  { label: "AWS Bedrock", href: "/guides/aws/#ai-ml-services" },
  { label: "Vertex AI", href: "/guides/gcp/#vertex-ai" },
];

export function PopularTopics() {
  return (
    <Card className={styles.card}>
      <div className={styles.eyebrow}>Popular topics</div>
      <ul className={styles.list}>
        {TOPICS.map((t) => (
          <li key={t.href}>
            <Link href={t.href} className={styles.item}>
              <span>{t.label}</span>
              <span className={styles.arrow} aria-hidden>→</span>
            </Link>
          </li>
        ))}
      </ul>
    </Card>
  );
}
