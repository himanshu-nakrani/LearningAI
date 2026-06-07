import { notFound } from "next/navigation";
import { GUIDES, GUIDE_BY_SLUG, type GuideSlug } from "@/lib/guides";
import { GuideShell } from "@/components/GuideShell";

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

  return (
    <GuideShell guide={guide}>
      <Mdx />
    </GuideShell>
  );
}
