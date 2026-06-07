# Learning AI — web

Next.js 15 + MDX rebuild of the long-form study guides in `../pages/*.html`.
Static export, deploys to GitHub Pages.

## Dev

```bash
cd web
npm install
npm run convert    # one-shot: read ../pages/*.html → src/content/*.mdx
npm run dev        # localhost:3000
```

You'll generally re-run `convert` whenever you touch `../pages/*.html`.

## Production build

```bash
npm run build      # convert → next build → search-index
npx serve out      # preview the static export
```

`out/` is the deployable directory.

## What lives where

```
web/
├── scripts/
│   ├── convert.ts              ← HTML → MDX with PascalCase components
│   └── build-search-index.ts   ← scans out/*.html → public/search-index.json
├── src/
│   ├── app/
│   │   ├── page.tsx            ← /                (guides index)
│   │   ├── guides/[slug]/      ← /guides/:slug    (11 long-form guides)
│   │   ├── glossary/           ← /glossary
│   │   ├── globals.css         ← design tokens + prose typography
│   │   └── layout.tsx          ← BookNav + SearchProvider + SearchOverlay
│   ├── components/             ← Callout, Ascii, Tag, BookNav, SearchOverlay,
│   │                              ThemeToggle, ReadingProgress, ScrollTop,
│   │                              CopyButton, GuideShell, SearchContext
│   ├── content/                ← GENERATED — do not edit; run `convert` instead
│   └── lib/guides.ts           ← per-guide metadata: title, accent palette
├── public/
│   └── search-index.json       ← GENERATED — produced by build-search-index
└── next.config.mjs             ← MDX pipeline (Shiki, slug, autolink, gfm)
```

## Design system at a glance

- **Charter serif** body, **system sans** for h1-h4 and chrome
- **Per-guide accent** color, light/dark variants (see `src/lib/guides.ts`)
- **h2** uses a 36px accent bar above the heading instead of a bottom rule
- **`<hr>`** renders as a centered `· · ·` ornament
- **Tables** drop vertical rules; hairline horizontal rules only
- **Callouts** with three variants: `tip` (green), `warn` (amber), `gap` (red)
- **`<Ascii>`** for monospace whitespace-preserving diagrams
- **Shiki** highlights all fenced code blocks at build time (zero runtime cost)
- **Copy** button fades in on `pre:hover`
- **Search** overlay (`⌘K` / `/`) fetches a static JSON index
- **Reading progress** bar + **scroll-to-top** button
- **Dark mode** via `localStorage`; respects `prefers-color-scheme` on first load

## Coexistence with `../pages/`

The legacy `../pages/*.html` site is preserved during the transition. The `convert`
script reads from it on every build, so the canonical content lives there until
we explicitly retire it.

## Deploy

GitHub Pages is wired up via `.github/workflows/deploy.yml`:

1. Push to `main` (changes under `web/` or `pages/`)
2. Action installs deps, converts, builds, builds search index, uploads `out/`
3. `actions/deploy-pages` publishes to the `github-pages` environment

The live URL once Pages is enabled: `https://himanshu-nakrani.github.io/LearningAI/`.

To enable Pages: repo Settings → Pages → Source: GitHub Actions.

## Known gotchas the converter handles

- MDX treats `{` inside inline `<code>` as JSX expressions → HTML-entity-escape them
- MDX closes JSX list items on blank lines / 4-space indentation → flatten `<ul>`/`<ol>` to single line
- jsdom serializes custom elements lowercased → restore PascalCase (`<ascii>` → `<Ascii>`)
- `<pre><code>` blocks → fenced code so Shiki + escaping works automatically
- `<Ascii>` content goes inside a `{`backtick`}` template literal to preserve everything
- Inline `style="..."` strings → JSX `style={{...}}` objects
