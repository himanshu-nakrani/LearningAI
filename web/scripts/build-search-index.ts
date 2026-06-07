/**
 * Build search-index.json from the prerendered HTML in out/.
 * Runs after `next build` so it sees the final hydrated content.
 */
import { promises as fs } from "fs";
import path from "path";
import { JSDOM } from "jsdom";
import { GUIDES } from "../src/lib/guides";

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.resolve(ROOT, "out");
const PUBLIC_DIR = path.resolve(ROOT, "public");
const BASE_PATH = "/LearningAI"; // matches next.config.mjs

type Section = { l: "h2" | "h3" | "term"; i: string; t: string; x: string };
type FileIndex = { f: string; g: string; s: Section[] };

function strip(s: string) {
  return s.replace(/\s+/g, " ").trim();
}

async function indexFile(htmlPath: string, label: string, route: string): Promise<FileIndex> {
  const html = await fs.readFile(htmlPath, "utf8");
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const main = doc.querySelector("main");
  const root = main ?? doc.body;

  const sections: Section[] = [];

  // h2/h3 with id
  const headings = Array.from(root.querySelectorAll("h2[id], h3[id]"));
  for (let i = 0; i < headings.length; i++) {
    const h = headings[i] as HTMLElement;
    const tag = h.tagName.toLowerCase() as "h2" | "h3";
    const id = h.id;
    const title = strip(h.textContent ?? "");
    if (!title) continue;
    // collect text up to next heading
    const nextH = headings[i + 1];
    let cur: Node | null = h.nextSibling;
    let text = "";
    while (cur && cur !== nextH) {
      text += " " + (cur.textContent ?? "");
      cur = cur.nextSibling;
    }
    sections.push({ l: tag, i: id, t: title, x: strip(text).slice(0, 280) });
  }

  // glossary <dt> entries
  if (route.endsWith("/glossary/")) {
    const dts = root.querySelectorAll("dt[id]");
    dts.forEach((dt) => {
      const id = (dt as HTMLElement).id;
      const title = strip(dt.textContent ?? "");
      const dd = dt.nextElementSibling;
      const body = dd && dd.tagName.toLowerCase() === "dd" ? strip(dd.textContent ?? "") : "";
      sections.push({ l: "term", i: id, t: title, x: body.slice(0, 220) });
    });
  }

  return { f: route, g: label, s: sections };
}

async function main() {
  const targets: Array<{ html: string; label: string; route: string }> = [];

  // each guide
  for (const g of GUIDES) {
    targets.push({
      html: path.join(OUT_DIR, "guides", g.slug, "index.html"),
      label: g.shortTitle,
      route: `${BASE_PATH}/guides/${g.slug}/`,
    });
  }
  // glossary
  targets.push({
    html: path.join(OUT_DIR, "glossary", "index.html"),
    label: "Glossary",
    route: `${BASE_PATH}/glossary/`,
  });

  const index: FileIndex[] = [];
  let total = 0;
  for (const t of targets) {
    try {
      const fi = await indexFile(t.html, t.label, t.route);
      index.push(fi);
      total += fi.s.length;
      console.log(`  ${t.label}: ${fi.s.length} sections`);
    } catch (e) {
      console.warn(`  ${t.label}: SKIP (${(e as Error).message})`);
    }
  }

  await fs.mkdir(PUBLIC_DIR, { recursive: true });
  const outFile = path.join(PUBLIC_DIR, "search-index.json");
  await fs.writeFile(outFile, JSON.stringify(index));
  // Also write to out/ since `next build` already copied public/ before we ran.
  const outDirFile = path.join(OUT_DIR, "search-index.json");
  await fs.writeFile(outDirFile, JSON.stringify(index));
  console.log(`\n${total} sections across ${index.length} pages → public/search-index.json (+ out/)`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
