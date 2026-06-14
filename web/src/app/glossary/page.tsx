import { AppShell } from "@/components/AppShell";
import { GuideLayout } from "@/components/GuideLayout";
import { GuideTOC } from "@/components/GuideTOC";
import Mdx from "@/content/glossary.mdx";
import type { GuideMeta } from "@/lib/guides";

export const metadata = {
  title: "Glossary",
  description:
    "Brief definitions of the key concepts and acronyms used across the Learning AI guides.",
};

// Use a green accent for the glossary, distinct from the guide colors.
const glossaryGuide: GuideMeta = {
  slug: "glossary" as GuideMeta["slug"],
  title: "Glossary",
  shortTitle: "Glossary",
  description: "",
  accent: "#6b8e2e",
  accentDark: "#a8c476",
  accentSoft: "#eef2e0",
  accentSoftDark: "#232818",
  group: "fundamentals",
  navGroup: "reference",
  status: "Reference",
  readMinutes: 15,
};

const breadcrumb = [
  { label: "Home", href: "/" },
  { label: "Reference", href: "/" },
  { label: "Glossary" },
];

export default function GlossaryPage() {
  return (
    <AppShell breadcrumb={breadcrumb} rightRail={<GuideTOC />}>
      <GuideLayout guide={glossaryGuide} siblings={[]} currentSlug="glossary" compact>
        <Mdx />
      </GuideLayout>
    </AppShell>
  );
}
