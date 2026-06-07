/**
 * HTML → MDX converter.
 *
 * For each /pages/<slug>-guide.html (or special-named file) extracts the
 * <main> body, strips per-page chrome (booknav, scripts, ascii copy buttons,
 * meta wrappers), and rewrites bespoke elements into our component library.
 */
import { promises as fs } from "fs";
import path from "path";
import { JSDOM } from "jsdom";

const ROOT = path.resolve(__dirname, "..");
const PAGES_DIR = path.resolve(ROOT, "../pages");
const OUT_DIR = path.resolve(ROOT, "src/content");

type FileMap = { source: string; slug: string; route: "guide" | "glossary" };

const FILES: FileMap[] = [
  { source: "ai-engineering-guide.html", slug: "ai-engineering", route: "guide" },
  { source: "agentic-ai-guide.html", slug: "agentic-ai", route: "guide" },
  { source: "llm-inference-guide.html", slug: "llm-inference", route: "guide" },
  { source: "aws-guide.html", slug: "aws", route: "guide" },
  { source: "azure-guide.html", slug: "azure", route: "guide" },
  { source: "gcp-guide.html", slug: "gcp", route: "guide" },
  { source: "cloud-ai-comparison.html", slug: "cloud-ai-comparison", route: "guide" },
  { source: "python-guide.html", slug: "python", route: "guide" },
  { source: "dsa-guide.html", slug: "dsa", route: "guide" },
  { source: "system-design-guide.html", slug: "system-design", route: "guide" },
  { source: "interview-prep.html", slug: "interview-prep", route: "guide" },
  { source: "glossary.html", slug: "glossary", route: "glossary" },
];

function rewriteHrefs(html: string): string {
  // /pages/*.html cross-guide links → /guides/<slug>
  const map: Record<string, string> = {
    "ai-engineering-guide.html": "/guides/ai-engineering",
    "agentic-ai-guide.html": "/guides/agentic-ai",
    "llm-inference-guide.html": "/guides/llm-inference",
    "aws-guide.html": "/guides/aws",
    "azure-guide.html": "/guides/azure",
    "gcp-guide.html": "/guides/gcp",
    "cloud-ai-comparison.html": "/guides/cloud-ai-comparison",
    "python-guide.html": "/guides/python",
    "dsa-guide.html": "/guides/dsa",
    "system-design-guide.html": "/guides/system-design",
    "interview-prep.html": "/guides/interview-prep",
    "glossary.html": "/glossary",
    "index.html": "/",
  };
  for (const [k, v] of Object.entries(map)) {
    // both `href="x.html"` and `href="x.html#anchor"`
    html = html.replace(new RegExp(`href="${k}"`, "g"), `href="${v}"`);
    html = html.replace(new RegExp(`href="${k}#`, "g"), `href="${v}#`);
  }
  return html;
}

function transformDom(scope: Element, doc: Document) {
  scope.querySelectorAll(".booknav, .reading-progress, .scroll-top, .skip-link, .search-overlay, script").forEach((n) => n.remove());
  scope.querySelectorAll('[id="theme-toggle"], [id="search-trigger"]').forEach((n) => n.remove());

  scope.querySelectorAll("div.ascii").forEach((el) => {
    const replacement = doc.createElement("Ascii");
    while (el.firstChild) replacement.appendChild(el.firstChild);
    el.replaceWith(replacement);
  });

  scope.querySelectorAll("div.callout").forEach((el) => {
    let variant: "tip" | "warn" | "gap" = "tip";
    if (el.classList.contains("callout-warn")) variant = "warn";
    else if (el.classList.contains("callout-gap")) variant = "gap";
    const repl = doc.createElement("Callout");
    repl.setAttribute("variant", variant);
    const strong = el.querySelector(":scope > strong");
    if (strong) {
      repl.setAttribute("title", strong.textContent?.trim() ?? "");
      strong.remove();
    }
    while (el.firstChild) repl.appendChild(el.firstChild);
    el.replaceWith(repl);
  });

  scope.querySelectorAll("span.tag").forEach((el) => {
    let kind: "core" | "concept" | "prod" | "gap" | "neutral" = "neutral";
    if (el.classList.contains("tag-core")) kind = "core";
    else if (el.classList.contains("tag-concept")) kind = "concept";
    else if (el.classList.contains("tag-prod")) kind = "prod";
    else if (el.classList.contains("tag-gap")) kind = "gap";
    const repl = doc.createElement("Tag");
    repl.setAttribute("kind", kind);
    while (el.firstChild) repl.appendChild(el.firstChild);
    el.replaceWith(repl);
  });

  scope.querySelectorAll(".copy-btn").forEach((n) => n.remove());

  scope.querySelectorAll("[class]").forEach((el) => {
    const keep = ["callout", "ascii", "tag", "meta", "toc", "glossary", "ref"];
    const original = (el.getAttribute("class") ?? "").split(/\s+/);
    const kept = original.filter((c) => keep.some((k) => c.startsWith(k)));
    if (kept.length === 0) el.removeAttribute("class");
    else el.setAttribute("class", kept.join(" "));
  });
}

function decodeEntities(s: string): string {
  return s
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ");
}

function bodyToMdx(html: string): string {
  // 1. <pre><code> → MDX fenced code (avoids JSX expression parsing inside code).
  html = html.replace(/<pre><code[^>]*>([\s\S]*?)<\/code><\/pre>/g, (_m, inner) => {
    const code = decodeEntities(inner);
    return "\n\n```\n" + code + "\n```\n\n";
  });

  // 2. <Ascii>...</Ascii> → wrap inner as a JS template literal so anything goes inside.
  html = html.replace(/<Ascii>([\s\S]*?)<\/Ascii>/g, (_m, inner) => {
    const raw = decodeEntities(inner);
    const escaped = raw.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$\{/g, "\\${");
    return "\n\n<Ascii>{`" + escaped + "`}</Ascii>\n\n";
  });

  // 3. Inline <code>...</code> — escape `{`, `}`, `<` so MDX doesn't try to parse them
  //    as JSX expressions / tags. Convert to HTML entities since they're rendered raw.
  html = html.replace(/<code(\b[^>]*)>([\s\S]*?)<\/code>/g, (_m, attrs, inner) => {
    const safe = inner
      .replace(/\{/g, "&#123;")
      .replace(/\}/g, "&#125;");
    return `<code${attrs}>${safe}</code>`;
  });

  // 4. Strip jsdom-added <tbody> (MDX adjacency rules don't like the auto-inserted form).
  html = html.replace(/<tbody>/g, "").replace(/<\/tbody>/g, "");

  // 5. Convert inline style="key: value; ..." strings to JSX style={{ ... }} objects.
  html = html.replace(/\bstyle="([^"]+)"/g, (_m, css: string) => {
    const obj = css
      .split(";")
      .map((d) => d.trim())
      .filter(Boolean)
      .map((d) => {
        const [k, ...rest] = d.split(":");
        const v = rest.join(":").trim();
        const camel = k.trim().replace(/-([a-z])/g, (_x, c: string) => c.toUpperCase());
        // numeric? leave bare; else quote.
        const value = /^-?\d+(\.\d+)?$/.test(v) ? v : JSON.stringify(v);
        return `"${camel}": ${value}`;
      })
      .join(", ");
    return `style={{${obj}}}`;
  });

  // 6. HTML attrs to JSX form
  html = html
    .replace(/\bclass=/g, "className=")
    .replace(/<br>/g, "<br />")
    .replace(/<hr>/g, "<hr />")
    .replace(/<img([^>]*?)>/g, "<img$1 />");

  // 6. MDX is picky about lists. Two known gotchas:
  //    (a) blank lines inside <li> close the JSX element early
  //    (b) indented JSX (4+ spaces) inside <li> is parsed as markdown code
  //    Solution: re-serialize each top-level <ul>/<ol> as a single line of HTML
  //    (no blank lines, no leading indentation per line).
  html = html.replace(/<(ul|ol)>([\s\S]*?)<\/\1>/g, (match) => {
    return match.replace(/\n\s*/g, "");
  });

  return html;
}

function escapeForFrontmatter(s: string): string {
  return s.replace(/"/g, '\\"');
}

async function processFile(map: FileMap) {
  const src = await fs.readFile(path.join(PAGES_DIR, map.source), "utf8");
  const dom = new JSDOM(src);
  const doc = dom.window.document;

  const titleTag = doc.querySelector("title")?.textContent ?? map.slug;
  const desc =
    doc.querySelector('meta[name="description"]')?.getAttribute("content") ?? "";

  const main = doc.querySelector("main");
  if (!main) throw new Error(`No <main> in ${map.source}`);

  transformDom(main as unknown as Element, doc);

  // strip the first <h1> (we will derive from frontmatter for layout titles)
  // ...actually, leaving it in keeps page intent intact. We just suppress generation in layout.

  let html = main.innerHTML;
  html = rewriteHrefs(html);
  // jsdom serializes custom element names lowercased; restore PascalCase BEFORE MDX transforms.
  html = html
    .replace(/<ascii(\b[^>]*)>/g, "<Ascii$1>")
    .replace(/<\/ascii>/g, "</Ascii>")
    .replace(/<callout(\b[^>]*)>/g, "<Callout$1>")
    .replace(/<\/callout>/g, "</Callout>")
    .replace(/<tag(\b[^>]*)>/g, "<Tag$1>")
    .replace(/<\/tag>/g, "</Tag>");
  html = bodyToMdx(html);

  const frontmatter = [
    "---",
    `title: "${escapeForFrontmatter(titleTag)}"`,
    `description: "${escapeForFrontmatter(desc)}"`,
    `slug: "${map.slug}"`,
    "---",
    "",
  ].join("\n");

  const outRel =
    map.route === "guide"
      ? `guides/${map.slug}.mdx`
      : map.route === "glossary"
        ? `glossary.mdx`
        : `${map.slug}.mdx`;
  const out = path.join(OUT_DIR, outRel);
  await fs.mkdir(path.dirname(out), { recursive: true });
  await fs.writeFile(out, frontmatter + html + "\n");
  return out;
}

async function main() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  const results = await Promise.all(FILES.map((f) => processFile(f)));
  console.log(`Wrote ${results.length} MDX files:`);
  for (const r of results) console.log(`  ${path.relative(ROOT, r)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
