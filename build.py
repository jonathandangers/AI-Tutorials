#!/usr/bin/env python3
"""Assemble the site.

Edit page bodies in src/ (plain HTML fragments, no <head> or nav),
then run:  python3 build.py
Built pages are written next to this file (index.html, core/, topics/,
examples/) so GitHub Pages can serve the repo root as-is.

In a fragment:
  {{pre}}          -> relative path back to the site root
  {{icon:name}}    -> inline line icon from ICONS below
Everything up to and including the first <p class="lede"> becomes the
page's header band.

To add a page: create src/<path>.html and add one line to PAGES below.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

SITE_NAME = "Practical AI Workflows"
ELECTIVE_URL = "https://claude.ai/artifact/Q6PUc5QvV6muvLbgsadrvh"
AUTHOR = "Jonathan Dangers, MD"

# (path, page title, nav label, group, tag, icon)
# group None = home. tag: "" | "new" | "placeholder" | "draft"
PAGES = [
    ("index.html", SITE_NAME, "Home", None, "", "compass"),

    ("core/start-here.html", "Start here", "Start here", "core", "", "compass"),
    ("core/ways-to-use.html", "Ways to use an LLM", "Ways to use an LLM", "core", "", "grid"),
    ("core/context.html", "Giving the model context", "Giving context", "core", "", "layers"),
    ("core/iteration.html", "Iteration, verification, and judgment", "Iterate and verify", "core", "", "loop"),
    ("core/project-memory.html", "Threads, memory, and project homes", "Threads and memory", "core", "", "stack"),
    ("core/project-workflow.html", "A workflow for larger projects", "Larger projects", "core", "", "flow"),
    ("core/connectors.html", "Connectors and agents", "Connectors and agents", "core", "", "plug"),
    ("core/models.html", "Models, reasoning, and usage", "Models and usage", "core", "", "gauge"),
    ("core/going-deeper.html", "Going deeper", "Going deeper", "core", "", "clock"),

    ("topics/when-not-to-use.html", "When not to use AI", "When not to use AI", "topics", "placeholder", "pause"),
    ("topics/teaching.html", "AI for teaching", "AI for teaching", "topics", "placeholder", "book"),
    ("topics/research.html", "Research use cases", "Research use cases", "topics", "placeholder", "flask"),

    ("examples/meeting-summary.html", "Meeting summary", "Meeting summary", "examples", "", "chat"),
    ("examples/research-workshop.html", "Research groups project home", "Research groups", "examples", "", "folder"),
    ("examples/exercise-tracker.html", "Exercise tracker", "Exercise tracker", "examples", "", "pulse"),
    ("examples/pubmed-scout.html", "PubMed scout", "PubMed scout", "examples", "", "search"),
    ("examples/newsletter-digest.html", "Newsletter digest", "Newsletter digest", "examples", "", "mail"),

]

GROUPS = [
    ("core", "Core modules", True),
    ("topics", "Topic modules", False),
    ("examples", "Worked examples", False),
]

TAG_TEXT = {"new": "new", "placeholder": "soon", "draft": "draft"}

# 24x24 line icons, drawn in currentColor.
ICONS = {
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "grid": '<rect x="3" y="5" width="5" height="5" rx="1"/><rect x="9.5" y="5" width="5" height="5" rx="1"/><rect x="16" y="5" width="5" height="5" rx="1"/><rect x="3" y="14" width="5" height="5" rx="1"/><rect x="9.5" y="14" width="5" height="5" rx="1"/><rect x="16" y="14" width="5" height="5" rx="1"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "loop": '<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M18.5 2.5v4h-4"/>',
    "stack": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    "flow": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M9 6h4a2 2 0 0 1 2 2v7"/>',
    "plug": '<path d="M9 3v5M15 3v5"/><path d="M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v4"/>',
    "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pause": '<circle cx="12" cy="12" r="9"/><path d="M10 9v6M14 9v6"/>',
    "book": '<path d="M3 5c3-1 6-1 9 1 3-2 6-2 9-1v14c-3-1-6-1-9 1-3-2-6-2-9-1z"/><path d="M12 6v14"/>',
    "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 14h9"/>',
    "chat": '<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "table": '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 14h18M9 4v16"/>',
    "pulse": '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "folder": '<path d="M3 6h6l2 2h10v11H3z"/>',
    "blocks": '<rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/><rect x="8" y="3" width="8" height="8" rx="1"/>',
    "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h7"/>',
    # six roles
    "partner": '<path d="M3 5h11v7H8l-3 3v-3H3z"/><path d="M17 9h4v7h-2v3l-3-3h-5v-2"/>',
    "tutor": '<path d="M3 5c3-1 6-1 9 1 3-2 6-2 9-1v14c-3-1-6-1-9 1-3-2-6-2-9-1z"/><path d="M12 6v14"/>',
    "organizer": '<path d="M3 6h6M4 10h4M3 14h5M5 18h3"/><path d="M11 12h3"/><path d="M13 10l2 2-2 2"/><path d="M17 7h4M17 12h4M17 17h4"/>',
    "writer": '<path d="M4 20l1-5L16 4l4 4L9 19z"/><path d="M14 6l4 4"/>',
    "research": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/><path d="M8 10.5h5"/>',
    "builder": '<rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/><rect x="8" y="3" width="8" height="8" rx="1"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="1"/><circle cx="9" cy="10" r="2"/><path d="M3 18l6-5 4 3 3-2 5 4"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def prefix_for(path: str) -> str:
    return "../" * path.count("/")


def nav_html(current: str) -> str:
    pre = prefix_for(current)
    parts = [
        f'<a class="nav-cta" href="{ELECTIVE_URL}"><span class="k">Resident?</span>'
        '<span class="t">Explore the AI elective</span><span class="arr" aria-hidden="true">&#8599;</span></a>'
    ]
    for gkey, glabel, numbered in GROUPS:
        items = [p for p in PAGES if p[3] == gkey]
        lis = []
        for i, (path, _title, label, _g, tag, _ic) in enumerate(items, start=1):
            cur = ' aria-current="page"' if path == current else ""
            num = f'<span class="num">{i:02d}</span>' if numbered else ""
            tg = f'<span class="tag">{TAG_TEXT[tag]}</span>' if tag else ""
            lis.append(f'<li><a href="{pre}{path}"{cur}>{num}<span>{label}</span>{tg}</a></li>')
        tagname = "ol" if numbered else "ul"
        parts.append(f'<div class="navgroup"><h2>{glabel}</h2><{tagname}>{"".join(lis)}</{tagname}></div>')
    return "\n".join(parts)


def pager_html(current: str) -> str:
    page = next(p for p in PAGES if p[0] == current)
    if page[3] is None:
        return ""
    items = [p for p in PAGES if p[3] == page[3]]
    i = items.index(page)
    pre = prefix_for(current)
    prev_html = next_html = ""
    if i > 0:
        p = items[i - 1]
        prev_html = f'<a class="prev" href="{pre}{p[0]}"><span class="dir">Previous</span><span>{p[2]}</span></a>'
    if i < len(items) - 1:
        n = items[i + 1]
        next_html = f'<a class="next" href="{pre}{n[0]}"><span class="dir">Next</span><span>{n[2]}</span></a>'
    if not (prev_html or next_html):
        return ""
    return f'<nav class="pager" aria-label="Page">{prev_html}{next_html}</nav>'


def head_mark(path: str) -> str:
    page = next(p for p in PAGES if p[0] == path)
    if page[3] == "core":
        n = [p for p in PAGES if p[3] == "core"].index(page) + 1
        return f'<div class="head-mark" aria-hidden="true"><span class="bignum">{n:02d}</span></div>'
    return f'<div class="head-mark" aria-hidden="true">{icon(page[5], "bigicon")}</div>'


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400&display=swap">
<link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>
<div class="shell">
<aside class="sidenav">
  <div class="navbar">
    <a class="brand" href="{pre}index.html"><span class="mark">FIELD GUIDE</span><span class="name">{site}</span></a>
    <button class="menu-toggle" type="button" id="menu-toggle" aria-expanded="false" aria-controls="navlinks">Menu</button>
  </div>
  <nav class="navlinks" id="navlinks" data-open="true" aria-label="Site">
{nav}
  </nav>
</aside>
<main>
<header class="page-head"><div class="head-inner"><div class="head-text">
{head}
</div>{mark}</div></header>
<article class="page">
{body}
{pager}
<footer class="site">{site} &middot; Created by {author} &middot; Draft v1.6</footer>
</article>
</main>
</div>
<script src="{pre}assets/site.js"></script>
</body>
</html>
"""


def render_fragment(text: str, pre: str) -> str:
    text = text.replace("{{pre}}", pre).replace("{{elective}}", ELECTIVE_URL)
    return re.sub(r"\{\{icon:([a-z]+)\}\}", lambda m: icon(m.group(1)), text)


def build():
    for path, title, _label, _group, _tag, _ic in PAGES:
        pre = prefix_for(path)
        body = render_fragment((SRC / path).read_text(encoding="utf-8"), pre)
        m = re.search(r'<!-- /head -->', body) or re.search(r'<p class="lede">.*?</p>', body, flags=re.S)
        if m:
            head, body = body[: m.end()], body[m.end():]
        else:
            head = ""
        full_title = title if path == "index.html" else f"{title} · {SITE_NAME}"
        html = TEMPLATE.format(
            title=full_title, pre=pre, site=SITE_NAME, author=AUTHOR,
            nav=nav_html(path), head=head.strip(), mark=head_mark(path),
            body=body.strip(), pager=pager_html(path),
        )
        out = ROOT / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("built", path)


if __name__ == "__main__":
    build()
