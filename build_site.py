"""Prebuild the site: markdown -> HTML with the custom theme, .nojekyll.

Removes the Jekyll build queue from the critical path entirely.
Usage: uv run --no-project --with markdown python build_site.py
"""
import markdown, os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
LAYOUT = open(os.path.join(DOCS, "_layouts", "default.html")).read()

PAGES = ["index", "setup", "sweep", "data", "frontier", "failures", "shipped", "gallery"]

def strip_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text[m.end():] if m else text

def fm_get(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else ""

for page in PAGES:
    src = os.path.join(DOCS, f"{page}.md")
    if not os.path.exists(src):
        print("missing", page); continue
    fm, body = strip_fm(open(src).read())
    title = fm_get(fm, "title")
    prev, nxt = fm_get(fm, "prev"), fm_get(fm, "next")
    html = markdown.markdown(body, extensions=["tables", "fenced_code"])
    page_html = (LAYOUT
                 .replace("{{ content }}", html)
                 .replace("{% if page.title %}{{ page.title }} · {{ site.title }}{% else %}{{ site.title }}{% endif %}",
                          f"{title} · teach-aws experiment walkthrough" if title else "teach-aws experiment walkthrough")
                 .replace("{% if page.prev %}<a href=\"{{ page.prev }}.html\">← previous</a>{% else %}<span></span>{% endif %}",
                          f'<a href="{prev}.html">← previous</a>' if prev else "<span></span>")
                 .replace("{% if page.next %}<a href=\"{{ page.next }}.html\">next →</a>{% else %}<span></span>{% endif %}",
                          f'<a href="{nxt}.html">next →</a>' if nxt else "<span></span>"))
    # nav active state
    for name, frag in [("setup", "Setup"), ("sweep", "sweep"), ("data", "Data"), ("frontier", "frontier"),
                       ("failures", "Failures"), ("shipped", "shipped"), ("gallery", "service")]:
        on = 'class="on"' if (page == name or (page == "index" and name == "")) else ''
        page_html = page_html.replace(
            "{% if page.title contains '" + frag + "' %}class=\"on\"{% endif %}", on)
    # relative_url filters -> plain paths
    page_html = page_html.replace("{{ '/' | relative_url }}", "index.html" if page != "index" else "index.html")
    for name in PAGES:
        page_html = page_html.replace(f"{{ '/{name}.html' | relative_url }}", f"{name}.html")
    # any leftover jekyll tags
    leftover = re.findall(r"\{\{[^}]*\}\}|\{%[^%]*%\}", page_html)
    if leftover:
        print(f"WARN {page}: leftover tags {leftover[:3]}")
    out = os.path.join(DOCS, f"{page}.html")
    open(out, "w").write(page_html)
    print("built", page)
open(os.path.join(DOCS, ".nojekyll"), "w").write("")
print("done")
