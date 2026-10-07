"""Render docs/DESIGN.md into the web page Andrew reads it in (the repo file stays the source).

Usage: .venv/bin/python docs/scratchpad/build_design_page.py docs/DESIGN.md <out.html>, then publish <out.html> to
the private web page https://claude.ai/artifact/Wi63bmMUa3NXqkUwni4CJ5 (Artifact tool, with that url).
The decision marks ([Decided, …], [Proposed …], [Built …], [Open …]) become coloured chips, the
parts get a sidebar of links, and a toggle highlights one kind of mark.
"""
import html
import re
import sys
from collections import Counter

from markdown_it import MarkdownIt

src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
md = MarkdownIt("commonmark", {"html": False}).enable("table")
body = md.render(text)

KINDS = {"Decided": "decided", "Andrew's idea": "idea", "Andrew's view": "idea", "Proposed": "proposed", "Built": "built", "Open": "open"}
counts: Counter = Counter()


def _chip(m: re.Match) -> str:
    raw = html.unescape(m.group(0))
    first = re.match(r"\[(Decided|Andrew's idea|Andrew's view|Proposed|Built|Open)", raw).group(1)
    kind = KINDS[first]
    counts[kind] += 1
    return f'<span class="mark mark-{kind}">{m.group(0)}</span>'


body = re.sub(r"\[(?:Decided|Andrew(?:&#x27;|')s (?:idea|view)|Proposed|Built|Open)[^\]<]*\]", _chip, body)

toc = []


def heading(m: re.Match) -> str:
    title = re.sub(r"<[^>]+>", "", m.group(1))
    slug = re.sub(r"[^a-z0-9]+", "-", html.unescape(title).lower()).strip("-")
    toc.append((slug, title))
    return f'<h2 id="{slug}">{m.group(1)}</h2>'


body = re.sub(r"<h2>(.*?)</h2>", heading, body)
body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
title_match = re.search(r"<h1>(.*?)</h1>", body)
body = re.sub(r"<h1>.*?</h1>", "", body, count=1)

toc_html = "\n".join(f'<li><a href="#{s}">{t}</a></li>' for s, t in toc)
summary = " · ".join(f'<button type="button" class="filter mark mark-{k}" data-kind="{k}" aria-pressed="false">'
                     f'{label} <b>{counts[k]}</b></button>'
                     for k, label in (("decided", "Decided"), ("idea", "Andrew's idea"), ("proposed", "Proposed"), ("built", "Built"), ("open", "Open")))

page = f"""<title>Open LLMRI Design</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
/* Layout: a reading column beside a sticky list of parts; one column on phones. */
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --fg: #18202c; --muted: #586274; --line: #dde2ea;
  --accent: #2c55c4; --hl: #fff4cc;
  --decided-bg: #e3f3ea; --decided-fg: #17633d;
  --proposed-bg: #fbeedb; --proposed-fg: #8a4b00;
  --built-bg: #e5ecf7; --built-fg: #2f4f80;
  --open-bg: #f0e7f7; --open-fg: #6a3594;
  --idea-bg: #dff1f1; --idea-fg: #12615f;
  --display: "IBM Plex Sans Condensed", "Arial Narrow", system-ui, sans-serif;
  --body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
  --sketch: ui-monospace, Menlo, Consolas, "DejaVu Sans Mono", monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #11151c; --surface: #171c25; --fg: #e3e8f0; --muted: #9aa5b6; --line: #2a3240;
  --accent: #8aa8ff; --hl: #3a3420;
  --decided-bg: #17352a; --decided-fg: #8fd9b0; --proposed-bg: #3a2a14; --proposed-fg: #f2bf7a;
  --built-bg: #1c2a40; --built-fg: #a9c2ee; --open-bg: #2c2140; --open-fg: #d2b2f0; --idea-bg: #143534; --idea-fg: #8fd6d2; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #11151c; --surface: #171c25; --fg: #e3e8f0; --muted: #9aa5b6; --line: #2a3240;
  --accent: #8aa8ff; --hl: #3a3420;
  --decided-bg: #17352a; --decided-fg: #8fd9b0; --proposed-bg: #3a2a14; --proposed-fg: #f2bf7a;
  --built-bg: #1c2a40; --built-fg: #a9c2ee; --open-bg: #2c2140; --open-fg: #d2b2f0; --idea-bg: #143534; --idea-fg: #8fd6d2; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font: 16px/1.6 var(--body); }}
.wrap {{ display: grid; grid-template-columns: 15rem minmax(0, 46rem); gap: 2.5rem; justify-content: center;
  padding-inline: 16px; padding-block: 2rem 4rem; }}
header {{ grid-column: 1 / -1; display: grid; gap: .6rem; border-bottom: 1px solid var(--line); padding-bottom: 1.2rem; }}
header h1 {{ font: 600 2.1rem/1.15 var(--display); margin: 0; letter-spacing: .01em; text-wrap: balance; }}
header p {{ margin: 0; color: var(--muted); }}
.filters {{ display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; }}
.filters span {{ color: var(--muted); font-size: .85rem; }}
nav {{ position: sticky; top: calc(env(safe-area-inset-top, 0px) + 1rem); align-self: start; max-height: calc(100vh - 2rem); overflow: auto; }}
nav h2 {{ font: 600 .75rem/1 var(--display); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 .6rem; }}
nav ol {{ list-style: none; padding: 0; margin: 0; display: grid; gap: .15rem; }}
nav a {{ color: var(--fg); text-decoration: none; font-size: .9rem; display: block; padding: .2rem .4rem; border-radius: 4px; }}
nav a:hover, nav a:focus-visible {{ background: var(--surface); color: var(--accent); outline: none; }}
main {{ min-width: 0; }}
main h2 {{ font: 600 1.5rem/1.25 var(--display); margin: 2.6rem 0 .8rem; padding-top: .4rem; border-top: 1px solid var(--line); text-wrap: balance; }}
main p, main li {{ max-width: 68ch; }}
main ul, main ol {{ padding-left: 1.3rem; }}
main li {{ margin: .2rem 0; }}
main li > ul, main li > ol {{ margin: .2rem 0; }}
code {{ font: .88em var(--mono); background: var(--surface); border: 1px solid var(--line); border-radius: 3px; padding: 0 .25em; }}
pre {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 1rem; line-height: 1.2; }}
pre code {{ font: 12px/1.2 var(--sketch); border: 0; background: none; padding: 0; white-space: pre; }}
.table-wrap {{ overflow-x: auto; margin: 1rem 0; }}
table {{ border-collapse: collapse; font-size: .92rem; min-width: 32rem; background: var(--surface); }}
th, td {{ border: 1px solid var(--line); padding: .45rem .6rem; vertical-align: top; text-align: left; }}
th {{ font: 600 .8rem var(--display); letter-spacing: .04em; text-transform: uppercase; color: var(--muted); }}
.mark {{ display: inline; font: 500 .78rem/1.5 var(--mono); padding: .05rem .35rem; border-radius: 4px; white-space: normal; border: 0; }}
.mark-decided {{ background: var(--decided-bg); color: var(--decided-fg); }}
.mark-proposed {{ background: var(--proposed-bg); color: var(--proposed-fg); }}
.mark-built {{ background: var(--built-bg); color: var(--built-fg); }}
.mark-open {{ background: var(--open-bg); color: var(--open-fg); }}
.mark-idea {{ background: var(--idea-bg); color: var(--idea-fg); }}
button.filter {{ cursor: pointer; font-size: .82rem; padding: .3rem .6rem; }}
button.filter[aria-pressed="true"] {{ outline: 2px solid currentColor; outline-offset: 1px; }}
button.filter:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.lit {{ background: var(--hl); border-radius: 4px; box-shadow: 0 0 0 4px var(--hl); }}
@media (max-width: 860px) {{
  .wrap {{ grid-template-columns: minmax(0, 1fr); gap: 1.2rem; }}
  nav {{ position: static; max-height: none; }}
  nav ol {{ grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr)); }}
}}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
</style>
<div class="wrap">
  <header>
    <h1>{title_match.group(1) if title_match else "Open LLMRI — the design document"}</h1>
    <p>A draft for Andrew's review, rendered from <code>docs/DESIGN.md</code>, which stays the source. Every passage carries a mark; pick one to highlight where it appears.</p>
    <div class="filters" role="group" aria-label="Highlight one kind of mark"><span>Highlight:</span> {summary}</div>
  </header>
  <nav aria-label="Parts"><h2>Parts</h2><ol>{toc_html}</ol></nav>
  <main>{body}</main>
</div>
<script>
const buttons = [...document.querySelectorAll("button.filter")];
function blockOf(el) {{ return el.closest("li, p, tr") || el; }}
function light(kind) {{
  document.querySelectorAll(".lit").forEach(e => e.classList.remove("lit"));
  buttons.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.kind === kind)));
  if (!kind) return;
  document.querySelectorAll("main .mark-" + kind).forEach(m => blockOf(m).classList.add("lit"));
}}
let current = null;
buttons.forEach(b => b.addEventListener("click", () => {{ current = current === b.dataset.kind ? null : b.dataset.kind; light(current); }}));
</script>
"""
open(out, "w", encoding="utf-8").write(page)
print(f"{len(toc)} parts; marks: {dict(counts)}; {len(page)} bytes")
