export type GuideSlug =
  | "ai-engineering"
  | "agentic-ai"
  | "llm-inference"
  | "aws"
  | "azure"
  | "gcp"
  | "cloud-ai-comparison"
  | "python"
  | "dsa"
  | "system-design"
  | "ai-system-design"
  | "interview-prep";

/** Top-level nav groupings used in the sidebar / command palette. */
export type NavGroup = "ai" | "agents" | "cloud" | "fundamentals" | "interview" | "reference";

export type Difficulty = "Beginner" | "Intermediate" | "Advanced" | "Reference";
export type GuideStatus = "Core" | "Advanced" | "Reference";

export type GuideMeta = {
  slug: GuideSlug;
  title: string;
  shortTitle: string;
  description: string;
  accent: string;
  accentDark: string;
  accentSoft: string;
  accentSoftDark: string;
  /** Coarse grouping used in the legacy home page (kept for back-compat). */
  group: "ai" | "cloud" | "fundamentals";
  /** Sidebar nav group. Drives the Study OS sidebar taxonomy. */
  navGroup: NavGroup;
  /** Difficulty bucket. Defaults to Intermediate. */
  difficulty?: Difficulty;
  /** Optional status chip (Core / Advanced / Reference). */
  status?: GuideStatus;
  /** Estimated read time in minutes. */
  readMinutes?: number;
};

export const GUIDES: GuideMeta[] = [
  {
    slug: "ai-engineering",
    title: "AI Engineering",
    shortTitle: "AI Engineering",
    description:
      "End-to-end overview of building production AI systems — data, training, evaluation, deployment.",
    accent: "#0f7b8a",
    accentDark: "#6fb0b9",
    accentSoft: "#e3f1f3",
    accentSoftDark: "#1f1f1f",
    group: "ai",
    navGroup: "ai",
    difficulty: "Intermediate",
    status: "Core",
    readMinutes: 55,
  },
  {
    slug: "agentic-ai",
    title: "Agentic AI — Complete Engineering Guide",
    shortTitle: "Agentic AI",
    description:
      "Agents, tool use, planning loops, MCP, memory, multi-agent orchestration.",
    accent: "#4338ca",
    accentDark: "#a5a0f0",
    accentSoft: "#e7e6fb",
    accentSoftDark: "#22214a",
    group: "ai",
    navGroup: "agents",
    difficulty: "Advanced",
    status: "Core",
    readMinutes: 70,
  },
  {
    slug: "llm-inference",
    title: "LLM Inference & Serving",
    shortTitle: "LLM Inference",
    description:
      "Batching, KV cache, quantization, speculative decoding, serving engines.",
    accent: "#b8453a",
    accentDark: "#e08a82",
    accentSoft: "#fbe8e6",
    accentSoftDark: "#3a2826",
    group: "ai",
    navGroup: "ai",
    difficulty: "Advanced",
    readMinutes: 60,
  },
  {
    slug: "ai-system-design",
    title: "AI System Design (High Level)",
    shortTitle: "AI System Design",
    description:
      "High-level AI interview architectures for RAG, agents, recommendations, ranking, and voice systems.",
    accent: "#7c3aed",
    accentDark: "#b79af5",
    accentSoft: "#efe7ff",
    accentSoftDark: "#261a3a",
    group: "ai",
    navGroup: "ai",
    difficulty: "Advanced",
    status: "Core",
    readMinutes: 80,
  },
  {
    slug: "aws",
    title: "Amazon Web Services",
    shortTitle: "AWS",
    description: "Core AWS services, compute, storage, networking, AI/ML offerings.",
    accent: "#d97300",
    accentDark: "#f0a050",
    accentSoft: "#fbeede",
    accentSoftDark: "#3a2c1a",
    group: "cloud",
    navGroup: "cloud",
    difficulty: "Intermediate",
    readMinutes: 50,
  },
  {
    slug: "azure",
    title: "Microsoft Azure",
    shortTitle: "Azure",
    description: "Azure fundamentals with a focus on enterprise and AI workloads.",
    accent: "#0078d4",
    accentDark: "#6cb8f0",
    accentSoft: "#e3f0fb",
    accentSoftDark: "#1a2a3a",
    group: "cloud",
    navGroup: "cloud",
    difficulty: "Intermediate",
    readMinutes: 50,
  },
  {
    slug: "gcp",
    title: "Google Cloud Platform",
    shortTitle: "GCP",
    description: "GCP services, Vertex AI, BigQuery, Gemini, TPUs.",
    accent: "#1a73e8",
    accentDark: "#7ab0f0",
    accentSoft: "#e8f0fe",
    accentSoftDark: "#1a2a3a",
    group: "cloud",
    navGroup: "cloud",
    difficulty: "Intermediate",
    readMinutes: 50,
  },
  {
    slug: "cloud-ai-comparison",
    title: "Cloud AI Comparison",
    shortTitle: "Cloud AI",
    description: "Side-by-side comparison of AWS, Azure, and GCP AI/ML services.",
    accent: "#6a4c93",
    accentDark: "#a78cc8",
    accentSoft: "#efe9f6",
    accentSoftDark: "#241f33",
    group: "cloud",
    navGroup: "cloud",
    difficulty: "Intermediate",
    readMinutes: 35,
  },
  {
    slug: "python",
    title: "Python",
    shortTitle: "Python",
    description: "From basics to advanced — idioms, async, typing, performance, tooling.",
    accent: "#306998",
    accentDark: "#7fa9d4",
    accentSoft: "#e4eef7",
    accentSoftDark: "#1a2530",
    group: "fundamentals",
    navGroup: "fundamentals",
    difficulty: "Beginner",
    status: "Core",
    readMinutes: 60,
  },
  {
    slug: "dsa",
    title: "Data Structures & Algorithms",
    shortTitle: "DSA",
    description: "Interview-oriented walkthrough from basic to medium problems.",
    accent: "#8b5e34",
    accentDark: "#c89870",
    accentSoft: "#f5ecde",
    accentSoftDark: "#2c2218",
    group: "fundamentals",
    navGroup: "fundamentals",
    difficulty: "Beginner",
    readMinutes: 70,
  },
  {
    slug: "system-design",
    title: "System Design",
    shortTitle: "System Design",
    description: "Architectural patterns, scalability, reliability, trade-offs.",
    accent: "#2c6e49",
    accentDark: "#80b598",
    accentSoft: "#e0eee6",
    accentSoftDark: "#1a2a20",
    group: "fundamentals",
    navGroup: "fundamentals",
    difficulty: "Intermediate",
    status: "Core",
    readMinutes: 80,
  },
  {
    slug: "interview-prep",
    title: "Interview Prep",
    shortTitle: "Interview Prep",
    description: "Strategies, frameworks, and practical tips for AI/ML & software interviews.",
    accent: "#a5374a",
    accentDark: "#d88090",
    accentSoft: "#f7e4e7",
    accentSoftDark: "#33181d",
    group: "fundamentals",
    navGroup: "interview",
    difficulty: "Advanced",
    readMinutes: 120,
  },
];

export const GUIDE_BY_SLUG: Record<GuideSlug, GuideMeta> = Object.fromEntries(
  GUIDES.map((g) => [g.slug, g]),
) as Record<GuideSlug, GuideMeta>;

/** Apply safe defaults to a guide record (used by new Study OS components). */
export function withDefaults(g: GuideMeta): Required<Pick<GuideMeta, "difficulty" | "readMinutes">> & GuideMeta {
  return {
    ...g,
    difficulty: g.difficulty ?? "Intermediate",
    readMinutes: g.readMinutes ?? 30,
  };
}

/** Guides in a given nav group, preserving the canonical GUIDES order. */
export function guidesByNavGroup(group: NavGroup): GuideMeta[] {
  return GUIDES.filter((g) => g.navGroup === group);
}

/** Glossary entry — not a real guide, lives at /glossary. Used in sidebar / cards. */
export const GLOSSARY_META = {
  slug: "glossary" as const,
  title: "Glossary",
  shortTitle: "Glossary",
  description:
    "Brief definitions of the key concepts and acronyms used across the guides — AI/ML, agents, inference, cloud, hardware, system design, Python, DSA.",
  href: "/glossary",
  difficulty: "Reference" as const,
  readMinutes: 15,
};
