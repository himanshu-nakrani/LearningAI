"""Convert all .md files in this directory to .html with MathJax + code highlighting."""
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$', '$']], displayMath: [['$$', '$$']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
<style>
  body {{ max-width: 820px; margin: 2rem auto; padding: 0 1rem;
         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         line-height: 1.6; color: #222; }}
  h1, h2, h3 {{ border-bottom: 1px solid #eee; padding-bottom: .2em; }}
  code {{ background: #f4f4f4; padding: .1em .3em; border-radius: 3px;
          font-family: "SF Mono", Monaco, monospace; font-size: .92em; }}
  pre {{ background: #f6f8fa; padding: 1em; border-radius: 6px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; margin: 1em 0; }}
  th, td {{ border: 1px solid #ddd; padding: .4em .8em; text-align: left; }}
  th {{ background: #f6f8fa; }}
  blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 1em; color: #666; }}
  a {{ color: #0366d6; }}
  hr {{ border: none; border-top: 1px solid #eee; margin: 2em 0; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

md = markdown.Markdown(extensions=["fenced_code", "tables", "codehilite"],
                       extension_configs={"codehilite": {"guess_lang": False}})

for src in HERE.glob("*.md"):
    title = src.stem
    body = md.convert(src.read_text())
    # Rewrite .md links → .html so cross-doc links work in the browser
    body = body.replace('.md"', '.html"').replace(".md'", ".html'")
    out = src.with_suffix(".html")
    out.write_text(TEMPLATE.format(title=title, body=body))
    md.reset()
    print(f"  {src.name} → {out.name}")
