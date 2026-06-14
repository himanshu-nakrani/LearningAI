import { notFound } from "next/navigation";
import { GUIDES, GUIDE_BY_SLUG, guidesByNavGroup, type GuideSlug, type GuideMeta } from "@/lib/guides";
import { AppShell } from "@/components/AppShell";
import { GuideLayout } from "@/components/GuideLayout";
import { GuideTOC } from "@/components/GuideTOC";
import { RelatedGuides } from "@/components/RelatedGuides";
import { RecordRecentVisit } from "@/components/RecordRecentVisit";

export function generateStaticParams() {
  return GUIDES.map((g) => ({ slug: g.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const guide = GUIDE_BY_SLUG[slug as GuideSlug];
  if (!guide) return {};
  return {
    title: guide.title,
    description: guide.description,
  };
}

export default async function GuidePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const guide = GUIDE_BY_SLUG[slug as GuideSlug];
  if (!guide) notFound();

  const mod = await import(`@/content/guides/${slug}.mdx`);
  const Mdx = mod.default;

  // Sibling guides = same navGroup, excluding the current one.
  const siblings = guidesByNavGroup(guide.navGroup).filter((g) => g.slug !== guide.slug);

  // Related guides = same-group first, then cross-group, prefer "Core" status, capped at 3.
  const others = GUIDES.filter((g) => g.slug !== guide.slug);
  const ranked = [
    ...others.filter((g) => g.navGroup === guide.navGroup),
    ...others.filter((g) => g.navGroup !== guide.navGroup && g.status === "Core"),
    ...others.filter((g) => g.navGroup !== guide.navGroup),
  ];
  const related = ranked.slice(0, 3);

  const groupLabel =
    guide.navGroup === "agents" ? "Agents"
    : guide.navGroup === "ai" ? "AI"
    : guide.navGroup === "cloud" ? "Cloud"
    : guide.navGroup === "fundamentals" ? "Fundamentals"
    : guide.navGroup === "interview" ? "Interview Prep"
    : "Reference";

  const breadcrumb = [
    { label: "Home", href: "/" },
    { label: groupLabel, href: "/" },
    { label: guide.shortTitle },
  ];

  return (
    <AppShell
      breadcrumb={breadcrumb}
      rightRail={
        <>
          <GuideTOC />
          <RelatedGuides guides={related} />
        </>
      }
      defaultCollapsed
    >
      <RecordRecentVisit guide={guide} />
      <GuideLayout guide={guide} siblings={siblings} currentSlug={guide.slug}>
        <Mdx />
      </GuideLayout>
    </AppShell>
  );
}
