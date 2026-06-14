import type { GuideMeta, NavGroup } from "./guides";
import { GUIDES, guidesByNavGroup } from "./guides";
import { LEARNING_PATHS } from "./learningPaths";

/** One entry in the sidebar nav. */
export type NavItem = {
  label: string;
  href: string;
  icon?: string; // emoji or short string — keeps zero-dependency icons
  /** Marks the Home / Glossary entries. */
  kind?: "home" | "reference";
  /** Slug of a guide, used for active-state matching. */
  slug?: string;
};

export type NavSection = {
  id: NavGroup | "home" | "reference";
  label: string;
  items: NavItem[];
};

/** Build the canonical sidebar sections from the GUIDES data. */
export function buildSidebarSections(): NavSection[] {
  const sections: NavSection[] = [
    { id: "home", label: "Overview", items: [{ label: "Home", href: "/", icon: "⌂", kind: "home" }] },
  ];

  const groupLabels: Record<NavGroup, string> = {
    ai: "AI",
    agents: "Agents",
    cloud: "Cloud",
    fundamentals: "Fundamentals",
    interview: "Interview Prep",
    reference: "Reference",
  };

  const groupOrder: NavGroup[] = ["ai", "agents", "cloud", "fundamentals", "interview"];

  for (const g of groupOrder) {
    const items: NavItem[] = guidesByNavGroup(g).map((guide) => ({
      label: guide.shortTitle,
      href: `/guides/${guide.slug}`,
      slug: guide.slug,
    }));
    if (items.length) {
      sections.push({ id: g, label: groupLabels[g], items });
    }
  }

  sections.push({
    id: "reference",
    label: "Reference",
    items: [{ label: "Glossary", href: "/glossary", icon: "§", kind: "reference" }],
  });

  return sections;
}

/** Returns the nav group that contains a given guide slug, or null. */
export function navGroupForSlug(slug: string): NavGroup | null {
  const g: GuideMeta | undefined = GUIDES.find((x) => x.slug === slug);
  return g ? g.navGroup : null;
}

export { GUIDES, LEARNING_PATHS };
