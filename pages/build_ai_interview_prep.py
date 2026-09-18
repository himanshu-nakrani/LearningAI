#!/usr/bin/env python3
"""Convert ai_engineering_interview_prep.md into a styled HTML guide page."""

import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "ai_engineering_interview_prep.md"
TEMPLATE_PATH = Path(__file__).resolve().parent / "interview-prep.html"
OUT_PATH = Path(__file__).resolve().parent / "ai-engineering-interview-prep.html"
SEARCH_INDEX_PATH = Path(__file__).resolve().parent / "search-index.json"

TITLE = "AI Engineering Interview Preparation Guide"
DESCRIPTION = (
    "Concise reference for AI engineering interviews — LLMs, RAG, agents, "
    "fine-tuning, vector DBs, system design, LLMOps, evaluation, safety, and more."
)
FILENAME = "ai-engineering-interview-prep.html"
GUIDE_GROUP = "AI Engineering Interview"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def blocks_to_html(blocks: list[str]) -> str:
    parts: list[str] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if not block.strip():
            i += 1
            continue

        lines = block.split("\n")
        if lines[0].startswith("```"):
            lang = lines[0][3:].strip()
            code_lines = lines[1:]
            if code_lines and code_lines[-1].strip() == "```":
                code_lines = code_lines[:-1]
            code = html.escape("\n".join(code_lines))
            cls = f' class="language-{lang}"' if lang else ""
            parts.append(f"<pre><code{cls}>{code}</code></pre>")
            i += 1
            continue

        if all(re.match(r"^[-*]\s+", ln) or ln.strip() == "" for ln in lines if ln.strip()):
            items = []
            for ln in lines:
                m = re.match(r"^[-*]\s+(.*)", ln)
                if m:
                    items.append(f"<li>{inline_md(m.group(1))}</li>")
            if items:
                parts.append("<ul>" + "".join(items) + "</ul>")
            i += 1
            continue

        if all(re.match(r"^\d+\.\s+", ln) or ln.strip() == "" for ln in lines if ln.strip()):
            items = []
            for ln in lines:
                m = re.match(r"^\d+\.\s+(.*)", ln)
                if m:
                    items.append(f"<li>{inline_md(m.group(1))}</li>")
            if items:
                parts.append("<ol>" + "".join(items) + "</ol>")
            i += 1
            continue

        para = "<p>" + "<br>\n".join(inline_md(ln) for ln in lines if ln.strip()) + "</p>"
        parts.append(para)
        i += 1

    return "\n".join(parts)


def parse_markdown(text: str):
    lines = text.splitlines()
    subtitle = ""
    sections: list[dict] = []
    current_section = None
    current_question = None
    answer_blocks: list[str] = []
    block_buf: list[str] = []

    def flush_block():
        nonlocal block_buf
        if block_buf:
            answer_blocks.append("\n".join(block_buf))
            block_buf = []

    def flush_question():
        nonlocal current_question, answer_blocks
        if current_section and current_question:
            flush_block()
            current_section["questions"].append(
                {"title": current_question, "blocks": answer_blocks.copy()}
            )
        current_question = None
        answer_blocks = []

    def flush_section():
        flush_question()
        nonlocal current_section
        current_section = None

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("# ") and not line.startswith("## "):
            i += 1
            continue

        if line.strip() == "---":
            i += 1
            continue

        if line.startswith("## "):
            flush_section()
            title = line[3:].strip()
            current_section = {"title": title, "id": slugify(title), "questions": []}
            sections.append(current_section)
            i += 1
            continue

        if line.startswith("### "):
            flush_question()
            current_question = line[4:].strip()
            i += 1
            continue

        if current_section is None and not subtitle and line.strip():
            subtitle = line.strip()
            i += 1
            continue

        if current_question is None:
            i += 1
            continue

        if line.startswith("```"):
            flush_block()
            block_buf = [line]
            i += 1
            while i < len(lines):
                block_buf.append(lines[i])
                if lines[i].startswith("```") and len(block_buf) > 1:
                    i += 1
                    break
                i += 1
            answer_blocks.append("\n".join(block_buf))
            block_buf = []
            continue

        if not line.strip():
            flush_block()
            i += 1
            continue

        block_buf.append(line)
        i += 1

    flush_section()
    return subtitle, sections


def render_main(subtitle: str, sections: list[dict]) -> tuple[str, list[dict]]:
    search_sections: list[dict] = []
    main_html = [
        f"<h1>{html.escape(TITLE)}</h1>",
        '<div class="meta">',
        f"  {html.escape(subtitle)}<br>",
        "  Self-contained study guide. Open in browser, or print to PDF.",
        "</div>",
        '<div class="toc">',
        "<h2>Table of Contents</h2>",
        "<ol>",
    ]
    for sec in sections:
        main_html.append(
            f'  <li><a href="#{sec["id"]}">{html.escape(sec["title"])}</a></li>'
        )
    main_html.append("</ol>")
    main_html.append("</div>")

    for sec in sections:
        first_q_text = ""
        if sec["questions"] and sec["questions"][0]["blocks"]:
            first_q_text = re.sub(r"\s+", " ", sec["questions"][0]["blocks"][0])[:240]

        search_sections.append(
            {"l": "h2", "i": sec["id"], "t": sec["title"], "x": first_q_text}
        )

        main_html.append(f'<h2 id="{sec["id"]}">{html.escape(sec["title"])}</h2>')
        for q in sec["questions"]:
            qid = slugify(q["title"])
            answer_html = blocks_to_html(q["blocks"])
            preview = re.sub(r"\s+", " ", q["blocks"][0] if q["blocks"] else "")[:240]
            search_sections.append(
                {"l": "h3", "i": qid, "t": q["title"], "x": preview}
            )
            main_html.extend(
                [
                    f'<div class="qa" id="{qid}">',
                    f'  <div class="qa-q">Q: {html.escape(q["title"])}</div>',
                    f'  <div class="qa-a">{answer_html}</div>',
                    "</div>",
                ]
            )

    return "\n\n".join(main_html), search_sections


def build_shell(main_html: str) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    start = template.index('<main id="main"')
    end = template.index("</main>", start) + len("</main>")
    before = template[:start]
    after = template[end:]

    before = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE)}</title>", before)
    before = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{html.escape(DESCRIPTION)}">',
        before,
    )
    before = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{html.escape(TITLE)}">',
        before,
    )
    before = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{html.escape(DESCRIPTION)}">',
        before,
    )
    before = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{html.escape(TITLE)}">',
        before,
    )
    before = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{html.escape(DESCRIPTION)}">',
        before,
    )

    # Teal accent for general AI engineering interview prep
    before = before.replace("--accent: #b8453a;", "--accent: #0f7b8a;")
    before = before.replace("--accent-soft: #f4e8e5;", "--accent-soft: #e3f1f3;")
    before = before.replace("--gap-bd: #b8453a;", "--gap-bd: #0f7b8a;")
    before = before.replace("--accent: #d48f89;", "--accent: #5fd6cd;")

    booknav = (
        '<nav class="booknav">\n'
        '  <a class="home" href="index.html">← Index</a>\n'
        '  <a href="ai-engineering-guide.html">AI Engineering</a>\n'
        '  <a href="agentic-ai-guide.html">Agentic AI</a>\n'
        '  <a href="llm-inference-guide.html">LLM Inference</a>\n'
        '  <a href="aws-guide.html">AWS</a>\n'
        '  <a href="azure-guide.html">Azure</a>\n'
        '  <a href="gcp-guide.html">GCP</a>\n'
        '  <a href="cloud-ai-comparison.html">Cloud AI Compare</a>\n'
        '  <a href="python-guide.html">Python</a>\n'
        '  <a href="dsa-guide.html">DSA</a>\n'
        '  <a href="system-design-guide.html">System Design</a>\n'
        '  <a href="interview-prep.html">Interview Prep</a>\n'
        f'  <a href="{FILENAME}" class="current">AI Eng Interview</a>\n'
        '  <a href="glossary.html">Glossary</a>\n'
        '  <button class="search-trigger" id="search-trigger" type="button" aria-label="Search guides">Search <kbd>⌘K</kbd></button>\n'
        '  <button class="theme-toggle-inline" id="theme-toggle" aria-label="Toggle dark mode">🌙</button>\n'
        "</nav>"
    )
    before = re.sub(r"<nav class=\"booknav\">.*?</nav>", booknav, before, flags=re.S)

    return before + f'<main id="main" tabindex="-1">\n\n{main_html}\n\n</main>' + after


def update_search_index(search_sections: list[dict]):
    if not SEARCH_INDEX_PATH.exists():
        return
    index = json.loads(SEARCH_INDEX_PATH.read_text(encoding="utf-8"))
    index = [entry for entry in index if entry.get("f") != FILENAME]
    index.append({"f": FILENAME, "g": GUIDE_GROUP, "s": search_sections})
    index.sort(key=lambda e: e.get("f", ""))
    SEARCH_INDEX_PATH.write_text(json.dumps(index), encoding="utf-8")


def main():
    md_text = MD_PATH.read_text(encoding="utf-8")
    subtitle, sections = parse_markdown(md_text)
    main_html, search_sections = render_main(subtitle, sections)
    page = build_shell(main_html)
    OUT_PATH.write_text(page, encoding="utf-8")
    update_search_index(search_sections)
    print(f"Wrote {OUT_PATH}")
    print(f"  Sections: {len(sections)}")
    print(f"  Questions: {sum(len(s['questions']) for s in sections)}")
    print(f"  Size: {OUT_PATH.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()