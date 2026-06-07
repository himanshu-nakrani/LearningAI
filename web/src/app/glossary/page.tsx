import { GuideShell } from "@/components/GuideShell";
import Mdx from "@/content/glossary.mdx";

export const metadata = {
  title: "Glossary",
  description:
    "Brief definitions of the key concepts and acronyms used across the Learning AI guides.",
};

// Use a green accent for the glossary, distinct from the guide colors.
const glossaryGuide = {
  slug: "glossary",
  title: "Glossary",
  shortTitle: "Glossary",
  description: "",
  accent: "#6b8e2e",
  accentDark: "#a8c476",
  accentSoft: "#eef2e0",
  accentSoftDark: "#232818",
  group: "fundamentals" as const,
} as const;

export default function GlossaryPage() {
  return (
    <GuideShell guide={glossaryGuide as any}>
      <Mdx />
    </GuideShell>
  );
}
