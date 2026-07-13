# ADK Course Webapp

Interactive learning UI for the **Agentic AI with Google ADK** course. Reads module markdown from the repo, packs it into JSON, and serves a static SPA with progress tracking and search.

## Features

- **29 modules** across Core, Deep ADK, and Production tracks
- Markdown reader with syntax highlighting
- Local progress (browser `localStorage`)
- Full-text search (`/` keyboard shortcut)
- Resources: glossary, cheatsheet, curriculum, coverage matrix
- No build toolchain required — plain HTML/CSS/JS

## Quick start

```bash
cd agents/webapp

# Rebuild content from modules/*.md (after editing course material)
python3 scripts/build_content.py

# Serve (rebuilds content if you pass --build)
python3 serve.py --build
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/)

```bash
python3 serve.py -p 9000 --no-open   # custom port, no browser
```

## Layout

```
webapp/
├── public/
│   ├── index.html          # SPA shell
│   ├── styles.css
│   ├── app.js
│   └── course-data.json    # generated — do not edit by hand
├── scripts/
│   └── build_content.py    # modules + resources → course-data.json
├── serve.py
└── README.md
```

## Content pipeline

`build_content.py` walks `agents/modules/00-setup` … `28-a2a-demo`, reads each `README.md` (plus extra docs listed in module metadata), and bundles:

- Track metadata and colors  
- Module titles, summaries, levels, hours  
- Full markdown bodies  
- Root resources (`glossary`, `cheatsheet`, `ADK_COVERAGE.md`, …)

Re-run the builder whenever you change course markdown.

## Routes (hash)

| Route | View |
|-------|------|
| `#/` | Home — tracks + all modules |
| `#/track/core` | Track module list |
| `#/module/05-multi-agent` | Module reader |
| `#/resources` | Resource index |
| `#/resource/glossary` | Resource reader |

## Progress

Completed modules are stored under key `adk-course-progress-v1` in `localStorage`. Use **Reset progress** in the sidebar footer to clear.

## Deploy

Any static host works for `public/` after a content build:

```bash
python3 scripts/build_content.py
# upload public/ to Netlify, Cloudflare Pages, S3, GitHub Pages, etc.
```

For GitHub Pages from this folder, publish the `public` directory (or copy it to `docs/` if you prefer that convention).
