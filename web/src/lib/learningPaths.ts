import type { GuideSlug } from "./guides";

export type LearningPathId = "ai-engineer" | "agent-builder" | "cloud-ai" | "interview-prep";

export type LearningPath = {
  id: LearningPathId;
  title: string;
  description: string;
  guideSlugs: GuideSlug[];
  /** Accent key — drives the path card color band. Matches design tokens. */
  accent: "teal" | "lavender" | "cobalt" | "amber";
};

export const LEARNING_PATHS: LearningPath[] = [
  {
    id: "ai-engineer",
    title: "AI Engineer",
    description:
      "Build, evaluate, and ship production AI systems end-to-end. From data and training to serving and ops.",
    guideSlugs: [
      "ai-engineering",
      "llm-inference",
      "ai-system-design",
      "python",
      "dsa",
    ],
    accent: "teal",
  },
  {
    id: "agent-builder",
    title: "Agent Builder",
    description:
      "Design tool-using agents, planning loops, MCP, memory, and multi-agent orchestration patterns.",
    guideSlugs: [
      "agentic-ai",
      "ai-system-design",
      "llm-inference",
      "ai-engineering",
    ],
    accent: "cobalt",
  },
  {
    id: "cloud-ai",
    title: "Cloud AI",
    description:
      "Compare and use the managed AI/ML platforms across AWS, Azure, and GCP for inference and training workloads.",
    guideSlugs: [
      "aws",
      "azure",
      "gcp",
      "cloud-ai-comparison",
    ],
    accent: "cobalt",
  },
  {
    id: "interview-prep",
    title: "Interview Prep",
    description:
      "Frameworks, patterns, and walkthroughs for AI/ML and software engineering interviews.",
    guideSlugs: [
      "interview-prep",
      "ai-system-design",
      "dsa",
      "system-design",
    ],
    accent: "amber",
  },
];

export const LEARNING_PATH_BY_ID: Record<LearningPathId, LearningPath> = LEARNING_PATHS.reduce(
  (acc, p) => ({ ...acc, [p.id]: p }),
  {} as Record<LearningPathId, LearningPath>,
);
