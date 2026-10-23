"""Build the two documents' web pages (DESIGN.md L24, L26; docs/architecture/plan.md "The two documents").

Usage (from the repo root):
  .venv/bin/python docs/pages/build.py design <out.html> --plan-url URL
  .venv/bin/python docs/pages/build.py plan <out.html> --design-url URL

The sources are docs/design/design.md, docs/architecture/plan.md and docs/design/requirements.yaml.
Each page is published privately with the `db`, `user` and `comments` (composer only) capabilities;
the design page keeps https://claude.ai/artifact/Wi63bmMUa3NXqkUwni4CJ5. Run docs/pages/check.py first.

What the markdown can carry, beyond plain markdown:
- `## Title {#anchor}`: a section with a fixed anchor (otherwise the title's slug);
- `[GOAL-1, PRIN-2 to PRIN-5]`: requirement citations, drawn as chips coloured by status, each
  linking to its line in the design page's requirements list and showing it in full on hover;
- `### L30. Title [Open]` with `- ( ) choice` / `- [ ] choice` lines: a question card; a choice ending
  "(recommended)" is Claude's pick; answers save to the page's store (`answers/<id>`);
- `<!-- words: L16.1 -->`: Andrew's own words for that item, read from the page's private store
  (`words/<id>`) and shown there; nothing is shown when the store holds none;
- `<!-- requirements -->`: the requirements list, by area;
- a ```mermaid fence: a diagram.
Every section (## and ###, questions apart) gets a box to write in, saved to the page's store
(`writing/<page>--<anchor>`) as you type, and a button that opens a comment on it; the last section
collects everything written, with a button that copies it all.
"""
import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {"design": ROOT / "docs/design/design.md", "plan": ROOT / "docs/architecture/plan.md"}
TITLES = {"design": "OpenLLMRI Design", "plan": "OpenLLMRI Plan"}
STATUS_LABEL = {"decided": "Decided", "idea": "Andrew's idea", "view": "Andrew's view", "proposed": "Proposed",
                "open": "Open", "built": "Built", "retired": "Retired"}
BUILT_LABEL = {True: "built", "partly": "partly built", False: "not built yet"}

parser = argparse.ArgumentParser()
parser.add_argument("page", choices=["design", "plan"])
parser.add_argument("out")
parser.add_argument("--design-url", default="https://claude.ai/artifact/Wi63bmMUa3NXqkUwni4CJ5")
parser.add_argument("--plan-url", default="")
args = parser.parse_args()
PAGE = args.page
URLS = {"design": args.design_url, "plan": args.plan_url}

data = yaml.safe_load((ROOT / "docs/design/requirements.yaml").read_text(encoding="utf-8"))
REQS: Dict[str, dict] = {r["id"]: r for r in data["requirements"]}
AREAS: Dict[str, str] = data["areas"]
md = MarkdownIt("commonmark", {"html": False}).enable("table")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", text)).lower()).strip("-")


def page_link(target: str, anchor: str) -> str:
    """A link to a section of one of the two pages, from this page."""
    if target == PAGE:
        return f"#{anchor}"
    return f"{URLS[target]}#{anchor}" if URLS[target] else f"#{anchor}"


# ---- 1. The markdown: anchors, questions, boxes and blocks become placeholders ----
QUESTION = re.compile(r"^(#{3,4}) (L\d+(?:\.\d+)*)\. (.+?)(?: \[Open\])?\s*$")


def card_anchors(page: str) -> Dict[str, str]:
    """Each card on a page, and its heading's anchor (as render_question makes it)."""
    text = SOURCES[page].read_text(encoding="utf-8")
    return {m.group(2): slug(m.group(2) + " " + m.group(3))
            for line in text.splitlines() if (m := QUESTION.match(line))}


CARDS = {page: card_anchors(page) for page in SOURCES}
CARD_REF = re.compile(r"\bL(\d+)((?:\.\d+)*)\b")
LAYERS = 24  # L0 to L23 also name layers, so a plain number in that range never links to a card
HEADING = re.compile(r"^(#{1,4}) (.+?)(?: \{#([a-z0-9-]+)\})?\s*$")
OPTION = re.compile(r"^- (\( \)|\[ \]) (.+)$")
lines = SOURCES[PAGE].read_text(encoding="utf-8").split("\n")

# A box goes at the end of every section that isn't a question: just before the next heading.
NO_BOX = {"decisions-needed"}  # its questions carry their own notes
with_boxes: List[str] = []
pending: Optional[str] = None
in_fence = False
for line in lines:
    if line.startswith("```"):
        in_fence = not in_fence
    heading = None if in_fence else HEADING.match(line)
    if heading and len(heading.group(1)) in (2, 3, 4):
        if pending:
            with_boxes += ["", f"BOXBLOCK:{pending}", ""]
            pending = None
        if not QUESTION.match(line) and len(heading.group(1)) in (2, 3):
            pending = heading.group(3) or slug(md.renderInline(heading.group(2)))
            if pending in NO_BOX:
                pending = None
    with_boxes.append(line)
if pending:
    with_boxes += ["", f"BOXBLOCK:{pending}", ""]

# Fixed anchors travel through the renderer as a marker in the heading's text.
marked = []
for line in with_boxes:
    h = HEADING.match(line)
    if h and h.group(3) and not QUESTION.match(line):
        line = f"{h.group(1)} {h.group(2)} ANCHOR{h.group(3)}ANCHOR"
    line = re.sub(r"^(\s*)<!-- words: (\S+) -->\s*$", r"\1WORDSBLOCK:\2", line)
    line = re.sub(r"^<!-- requirements -->\s*$", "REQUIREMENTSBLOCK", line)
    marked.append(line)

# Question blocks are cut out, rendered as forms, and put back.
blocks: List[Dict] = []
out_lines: List[str] = []
i = 0
while i < len(marked):
    m = QUESTION.match(marked[i])
    if not m:
        out_lines.append(marked[i])
        i += 1
        continue
    level, qid, title = len(m.group(1)), m.group(2), m.group(3)
    j = i + 1
    while j < len(marked) and not re.match(r"^#{1,4} ", marked[j]) and not marked[j].startswith("BOXBLOCK:"):
        j += 1
    options, context = [], []
    for line in marked[i + 1:j]:
        om = OPTION.match(line)
        if om:
            label = om.group(2).strip()
            recommended = label.endswith("(recommended)")
            if recommended:
                label = label[: -len("(recommended)")].rstrip()
            options.append({"multi": om.group(1) == "[ ]", "label": label, "recommended": recommended})
        else:
            context.append(line)
    kind = "any" if options and options[0]["multi"] else ("one" if options else "text")
    for n, opt in enumerate(options):
        opt["key"] = "other" if opt["label"].lower().startswith("other") else "abcdefghij"[n]
    blocks.append({"id": qid, "level": level, "title": title, "kind": kind, "options": options,
                   "context": "\n".join(context).strip()})
    out_lines += ["", f"QUESTIONBLOCK{len(blocks) - 1}", ""]
    i = j


# ---- 2. Rendering the pieces ----
def render_question(b: Dict) -> str:
    qid, tag = b["id"], f"h{b['level']}"
    parts = [f'<section class="q q-{b["kind"]}" id="q-{html.escape(qid)}" data-q="{html.escape(qid)}" data-kind="{b["kind"]}">',
             f'<{tag} id="{slug(qid + " " + b["title"])}">{html.escape(qid)}. {md.renderInline(b["title"])}</{tag}>']
    if b["context"]:
        parts.append(f'<div class="q-context">{md.render(b["context"])}</div>')
    if b["kind"] in ("one", "any"):
        kind = "radio" if b["kind"] == "one" else "checkbox"
        parts.append(f'<fieldset class="q-options"><legend class="sr-only">{html.escape(qid)}: choices</legend>')
        for opt in b["options"]:
            rec = '<span class="rec">Claude recommends</span>' if opt["recommended"] else ""
            parts.append(f'<label class="opt"><input type="{kind}" name="{html.escape(qid)}" value="{opt["key"]}" '
                         f'data-label="{html.escape(opt["label"])}"><span class="opt-text">{md.renderInline(opt["label"])}</span>{rec}</label>')
        parts.append("</fieldset>")
        parts.append('<label class="q-note-label"><span>Note <i>(say what you mean if you pick Other, or anything '
                     'else)</i></span><textarea class="q-note" rows="2"></textarea></label>')
    else:
        parts.append('<label class="q-note-label"><span>Your answer</span><textarea class="q-note" rows="4"></textarea></label>')
    parts.append('<div class="q-status" aria-live="polite"></div></section>')
    return "\n".join(parts)


def req_tip(r: dict) -> str:
    built = "" if r["status"] == "view" else f" · {BUILT_LABEL.get(r.get('built'), 'not built yet')}"
    dates = ", ".join(str(d) for d in r.get("dates") or [])
    source = f" · {r['source']}" if r.get("source") else ""
    text = re.sub(r"\s+", " ", r["text"]).strip().replace("`", "")
    return f"{r['id']} · {STATUS_LABEL[r['status']]}{(' ' + dates) if dates else ''}{source}{built}\n{text}"


cited: Counter = Counter()


def chip(item: str) -> str:
    if " to " in item:
        first, last = item.split(" to ")
        area, a, b = first.rsplit("-", 1)[0], int(first.rsplit("-", 1)[1]), int(last.rsplit("-", 1)[1])
        ids = [f"{area}-{n}" for n in range(a, b + 1) if f"{area}-{n}" in REQS]
        for rid in ids:
            cited[REQS[rid]["status"]] += 1
        kinds = Counter(REQS[rid]["status"] for rid in ids)
        tip = f"{first} to {last}: {len(ids)} requirements (" + ", ".join(
            f"{n} {STATUS_LABEL[k].lower()}" for k, n in kinds.most_common()) + ")"
        status = kinds.most_common(1)[0][0] if kinds else "open"
        return (f'<a class="req req-{status} req-range" href="{page_link("design", "req-" + first)}" '
                f'data-status="{" ".join(kinds)}" title="{html.escape(tip)}">{first}–{last.split("-")[1]}</a>')
    r = REQS.get(item)
    if not r:
        return f'<span class="req req-missing" title="not in the requirements list">{html.escape(item)}</span>'
    cited[r["status"]] += 1
    built = "" if r["status"] == "view" else {True: " built", "partly": " partly", False: ""}.get(r.get("built"), "")
    return (f'<a class="req req-{r["status"]}{built}" href="{page_link("design", "req-" + item)}" '
            f'data-status="{r["status"]}" title="{html.escape(req_tip(r))}">{item}</a>')


ID = r"[A-Z]+-\d+"
ITEM = rf"{ID}(?: to {ID})?"
CITATION = re.compile(rf"\[({ITEM}(?:,\s*{ITEM})*)\]")


def cite(m: re.Match) -> str:
    items = re.split(r",\s*", m.group(1))
    return '<span class="cites">' + " ".join(chip(i) for i in items) + "</span>"


def requirements_html() -> str:
    by_area: Dict[str, List[dict]] = {}
    for r in data["requirements"]:
        by_area.setdefault(r["id"].rsplit("-", 1)[0], []).append(r)
    parts = []
    for area, label in AREAS.items():
        reqs = by_area.get(area, [])
        rows = []
        for r in reqs:
            built = "—" if r["status"] == "view" else BUILT_LABEL.get(r.get("built"), "not built yet")
            dates = ", ".join(str(d) for d in r.get("dates") or [])
            replaced = ""
            if r.get("replaced_by"):
                replaced = " Replaced by " + ", ".join(
                    f'<a href="#req-{x}">{x}</a>' for x in r["replaced_by"]) + "."
            text = md.renderInline(re.sub(r"\s+", " ", r["text"]).strip())
            rows.append(f'<tr id="req-{r["id"]}"><td class="rid">{r["id"]}</td>'
                        f'<td><span class="req req-{r["status"]}">{STATUS_LABEL[r["status"]]}</span></td>'
                        f'<td>{text}{replaced}</td>'
                        f'<td class="small">{html.escape(dates)}<br>{html.escape(str(r.get("source") or ""))}</td>'
                        f'<td class="small">{built}</td></tr>')
        parts.append(f'<details class="area" id="area-{area}"><summary><b>{area}</b> {html.escape(label)} '
                     f'<span class="count">{len(reqs)}</span></summary><div class="table-wrap"><table class="reqs">'
                     '<thead><tr><th>Id</th><th>Status</th><th>Requirement</th><th>Date, source</th><th>Built</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></div></details>')
    return "\n".join(parts)


def box_html(anchor: str) -> str:
    key = f"{PAGE}--{anchor}"
    return (f'<div class="box" data-box="{key}" data-anchor="{anchor}">'
            f'<label><span class="box-label">Your notes on this section</span>'
            f'<textarea rows="2" placeholder="Write anything here: a question, a change, a yes or a no."></textarea></label>'
            f'<div class="box-row"><span class="box-status" aria-live="polite"></span>'
            f'<button type="button" class="comment-btn" hidden>Comment on this section</button></div></div>')


# ---- 3. Render, then fill the placeholders ----
body = md.render("\n".join(out_lines))
for n, b in enumerate(blocks):
    body = body.replace(f"<p>QUESTIONBLOCK{n}</p>", render_question(b))
body = re.sub(r"<h(\d)>(.*?) ANCHOR([a-z0-9-]+)ANCHOR</h\1>", r'<h\1 id="\3">\2</h\1>', body)
body = re.sub(r"<h([23])>(.*?)</h\1>", lambda m: f'<h{m.group(1)} id="{slug(m.group(2))}">{m.group(2)}</h{m.group(1)}>', body)
body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<pre class="mermaid">\1</pre>', body, flags=re.S)
body = re.sub(r"<p>BOXBLOCK:([a-z0-9-]+)</p>", lambda m: box_html(m.group(1)), body)

body = re.sub(r"\s*WORDSBLOCK:(\S+?)(?=<|\s|$)", lambda m: f'<span class="words" data-words="{html.escape(m.group(1))}" hidden></span>', body)
body = re.sub(r'href="(design|plan)\.md#([a-z0-9-]+)"', lambda m: f'href="{page_link(m.group(1), m.group(2))}"', body)
body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
body = body.replace("<p>REQUIREMENTSBLOCK</p>", requirements_html())  # after the wrapping: its tables come wrapped
# Citations become chips, outside code and preformatted blocks.
pieces = re.split(r"(<pre[\s\S]*?</pre>|<code>[\s\S]*?</code>)", body)
body = "".join(p if p.startswith(("<pre", "<code>")) else CITATION.sub(cite, p) for p in pieces)


# A card's number in the text links to its card, on this page or the other one; never inside a
# link, code, a heading, a form's legend or a text box.
SKIP_OPEN = re.compile(r"^<(a|pre|code|h[1-6]|legend|textarea)\b", re.I)
SKIP_CLOSE = re.compile(r"^</(a|pre|code|h[1-6]|legend|textarea)>", re.I)


def card_link(m: re.Match) -> str:
    qid = m.group(0)
    if not m.group(2) and int(m.group(1)) < LAYERS:
        return qid
    for page in (PAGE, *(p for p in SOURCES if p != PAGE)):
        if qid in CARDS[page]:
            return f'<a class="qref" href="{page_link(page, CARDS[page][qid])}">{qid}</a>'
    return qid


linked: List[str] = []
skipping = 0
for piece in re.split(r"(<[^>]+>)", body):
    if piece.startswith("<"):
        if SKIP_OPEN.match(piece):
            skipping += 1
        elif SKIP_CLOSE.match(piece):
            skipping = max(0, skipping - 1)
        linked.append(piece)
    else:
        linked.append(piece if skipping else CARD_REF.sub(card_link, piece))
body = "".join(linked)

title_match = re.search(r"<h1>(.*?)</h1>", body)
body = re.sub(r"<h1>.*?</h1>", "", body, count=1)
toc = []
for m in re.finditer(r'<h([23]) id="([a-z0-9-]+)">(.*?)</h\1>', body):  # cards too, under their section
    toc.append((int(m.group(1)), m.group(2), re.sub(r"<[^>]+>", "", m.group(3))))
toc.append((2, "everything-written", "Everything you've written"))
toc_html = "".join(f'<li class="toc{lvl}"><a href="#{a}">{t}</a></li>' for lvl, a, t in toc)
answerable = [b["id"] for b in blocks]
if answerable:
    bar = ('<div class="answers-bar" id="answers-bar"><span id="answers-count">0 of '
           f'{len(answerable)} answered</span><span id="answers-mode">Connecting…</span></div>')
    body = re.sub(r'(<h2 id="decisions-needed">[^<]*</h2>)', r"\1" + bar, body, count=1)
other = "plan" if PAGE == "design" else "design"
other_link = (f'<a href="{URLS[other]}">{"The plan-and-architecture document" if other == "plan" else "The design-and-requirements document"}</a>'
              if URLS[other] else "")
legend = " ".join(f'<button type="button" class="filter req req-{k}" data-kind="{k}" aria-pressed="false">'
                  f'{STATUS_LABEL[k]} <b>{cited[k]}</b></button>' for k in STATUS_LABEL if cited[k])
everything = ('<section class="everything" id="everything-written-section"><h2 id="everything-written">'
              "Everything you've written</h2><p>Every box on this page, in order, as you write. Claude reads them here.</p>"
              '<div id="everything-list"><p class="empty">Nothing written yet.</p></div>'
              '<button type="button" id="copy-all">Copy it all</button> <span id="copy-status" aria-live="polite"></span>'
              "</section>")

# ---- 4. The page ----
CSS = """
:root {
  --bg: #f6f7f9; --surface: #ffffff; --fg: #18202c; --muted: #586274; --line: #dde2ea;
  --accent: #2c55c4; --hl: #fff4cc; --ok: #17633d; --warn: #8a4b00; --chosen: #eef3ff;
  --decided-bg: #e3f3ea; --decided-fg: #17633d; --proposed-bg: #f1e8fb; --proposed-fg: #5b2f91;
  --built-bg: #e5ecf7; --built-fg: #2f4f80; --open-bg: #fbeedb; --open-fg: #8a4b00;
  --idea-bg: #dff1f1; --idea-fg: #12615f; --view-bg: #eceef2; --view-fg: #444c5a;
  --retired-bg: #eceef2; --retired-fg: #6a7280;
  --display: "IBM Plex Sans Condensed", "Arial Narrow", system-ui, sans-serif;
  --body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #11151c; --surface: #171c25; --fg: #e3e8f0; --muted: #9aa5b6; --line: #2a3240;
  --accent: #8aa8ff; --hl: #3a3420; --ok: #8fd9b0; --warn: #f2bf7a; --chosen: #1d2638;
  --decided-bg: #17352a; --decided-fg: #8fd9b0; --proposed-bg: #2c2140; --proposed-fg: #d2b2f0;
  --built-bg: #1c2a40; --built-fg: #a9c2ee; --open-bg: #3a2a14; --open-fg: #f2bf7a;
  --idea-bg: #143534; --idea-fg: #8fd6d2; --view-bg: #232a35; --view-fg: #b9c2d0;
  --retired-bg: #232a35; --retired-fg: #8a93a3; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #11151c; --surface: #171c25; --fg: #e3e8f0; --muted: #9aa5b6; --line: #2a3240;
  --accent: #8aa8ff; --hl: #3a3420; --ok: #8fd9b0; --warn: #f2bf7a; --chosen: #1d2638;
  --decided-bg: #17352a; --decided-fg: #8fd9b0; --proposed-bg: #2c2140; --proposed-fg: #d2b2f0;
  --built-bg: #1c2a40; --built-fg: #a9c2ee; --open-bg: #3a2a14; --open-fg: #f2bf7a;
  --idea-bg: #143534; --idea-fg: #8fd6d2; --view-bg: #232a35; --view-fg: #b9c2d0;
  --retired-bg: #232a35; --retired-fg: #8a93a3; color-scheme: dark; }
body { background: var(--bg); color: var(--fg); font: 16px/1.6 var(--body); }
.wrap { display: grid; grid-template-columns: 15rem minmax(0, 46rem); gap: 2.5rem; justify-content: center;
  padding-inline: 16px; padding-block: 2rem 4rem; }
header { grid-column: 1 / -1; display: grid; gap: .6rem; border-bottom: 1px solid var(--line); padding-bottom: 1.2rem; }
header h1 { font: 600 2.1rem/1.15 var(--display); margin: 0; letter-spacing: .01em; text-wrap: balance; }
header p { margin: 0; color: var(--muted); max-width: 72ch; }
.filters { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; }
.filters > span { color: var(--muted); font-size: .85rem; }
nav { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 1rem); align-self: start; max-height: calc(100vh - 2rem); overflow: auto; }
nav h2 { font: 600 .75rem/1 var(--display); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 .6rem; }
nav ol { list-style: none; padding: 0; margin: 0; display: grid; gap: .1rem; }
nav a { color: var(--fg); text-decoration: none; font-size: .9rem; display: block; padding: .15rem .4rem; border-radius: 4px; }
nav .toc3 a { font-size: .8rem; padding-left: 1.2rem; color: var(--muted); }
nav a:hover, nav a:focus-visible { background: var(--surface); color: var(--accent); outline: none; }
main { min-width: 0; }
main h2 { font: 600 1.5rem/1.25 var(--display); margin: 2.6rem 0 .8rem; padding-top: .4rem; border-top: 1px solid var(--line); text-wrap: balance; }
main h3 { font: 600 1.18rem/1.3 var(--display); margin: 2rem 0 .5rem; text-wrap: balance; }
main p, main li { max-width: 68ch; }
main ul, main ol { padding-left: 1.3rem; }
main li { margin: .2rem 0; }
a { color: var(--accent); }
code { font: .88em var(--mono); background: var(--surface); border: 1px solid var(--line); border-radius: 3px; padding: 0 .25em; overflow-wrap: anywhere; }
pre { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 1rem; line-height: 1.2; }
pre code { font: 12px/1.2 var(--mono); border: 0; background: none; padding: 0; white-space: pre; }
pre.mermaid { background: var(--surface); text-align: center; }
.table-wrap { overflow-x: auto; margin: 1rem 0; }
table { border-collapse: collapse; font-size: .92rem; min-width: 32rem; background: var(--surface); }
th, td { border: 1px solid var(--line); padding: .45rem .6rem; vertical-align: top; text-align: left; }
th { font: 600 .8rem var(--display); letter-spacing: .04em; text-transform: uppercase; color: var(--muted); }
td.small { font-size: .8rem; color: var(--muted); white-space: nowrap; }
td.rid { font: 500 .8rem var(--mono); white-space: nowrap; }
.cites { white-space: normal; }
.req { display: inline-block; font: 500 .74rem/1.45 var(--mono); padding: 0 .35rem; border-radius: 4px; text-decoration: none;
  border: 1px solid transparent; margin: .05rem 0; }
.req.built { border-color: currentColor; }
.req.partly { border-style: dashed; border-color: currentColor; }
.req-decided { background: var(--decided-bg); color: var(--decided-fg); }
.req-proposed { background: var(--proposed-bg); color: var(--proposed-fg); }
.req-built { background: var(--built-bg); color: var(--built-fg); }
.req-open { background: var(--open-bg); color: var(--open-fg); }
.req-idea { background: var(--idea-bg); color: var(--idea-fg); }
.req-view { background: var(--view-bg); color: var(--view-fg); }
.req-retired { background: var(--retired-bg); color: var(--retired-fg); text-decoration: line-through; }
.req-missing { background: var(--hl); color: var(--warn); }
a.req:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
button.filter { cursor: pointer; font-size: .8rem; padding: .25rem .55rem; }
button.filter[aria-pressed="true"] { outline: 2px solid currentColor; outline-offset: 1px; }
.lit { background: var(--hl); border-radius: 4px; box-shadow: 0 0 0 4px var(--hl); }
details.area { border: 1px solid var(--line); border-radius: 8px; background: var(--surface); margin: .5rem 0; padding: .3rem .8rem; }
details.area summary { cursor: pointer; padding: .3rem 0; }
details.area .count { color: var(--muted); font-size: .85rem; }
.legend-key { color: var(--muted); font-size: .85rem; }
/* boxes to write in, and the comment button */
.box { max-width: 68ch; margin: 1rem 0 1.6rem; padding: .6rem .8rem; border: 1px dashed var(--line); border-radius: 8px; background: var(--surface); }
.box label { display: grid; gap: .25rem; }
.box-label { font-size: .78rem; color: var(--muted); letter-spacing: .02em; }
.box textarea, .q-note { width: 100%; box-sizing: border-box; font: 15px/1.5 var(--body); color: var(--fg); background: var(--bg);
  border: 1px solid var(--line); border-radius: 6px; padding: .4rem .55rem; resize: vertical; }
.box textarea:focus, .q-note:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
.box.written { border-style: solid; border-color: color-mix(in srgb, var(--accent) 40%, var(--line)); }
.box-row { display: flex; justify-content: space-between; align-items: center; gap: .6rem; flex-wrap: wrap; margin-top: .3rem; }
.box-status { font-size: .78rem; color: var(--muted); min-height: 1rem; }
.box-status.saved { color: var(--ok); }
.box-status.error { color: var(--warn); }
.comment-btn, #copy-all { font: 500 .8rem var(--body); color: var(--accent); background: transparent; border: 1px solid var(--line);
  border-radius: 6px; padding: .25rem .6rem; cursor: pointer; }
.comment-btn:hover, #copy-all:hover { border-color: var(--accent); }
.words { display: block; margin: .4rem 0 .2rem; padding: .5rem .7rem; border-left: 3px solid var(--accent); background: var(--surface);
  border-radius: 0 6px 6px 0; font-size: .92rem; }
.words[hidden] { display: none; }
.words .who { display: block; font-size: .75rem; color: var(--muted); margin-bottom: .2rem; }
.everything .entry { border-left: 3px solid var(--line); padding: .2rem .7rem; margin: .6rem 0; }
.everything .entry h4 { margin: 0 0 .2rem; font: 600 .9rem var(--display); }
.everything .entry p { margin: 0; white-space: pre-wrap; }
.everything .empty { color: var(--muted); }
/* the questions' form */
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.answers-bar { display: flex; flex-wrap: wrap; gap: .4rem 1.2rem;
  justify-content: space-between; align-items: center; background: var(--surface); border: 1px solid var(--line);
  border-radius: 8px; padding: .5rem .8rem; margin: .4rem 0 1.2rem; font-size: .9rem; max-width: 68ch; box-sizing: border-box; }
#answers-count { font-weight: 600; }
#answers-mode { color: var(--muted); }
section.q { max-width: 68ch; background: var(--surface); border: 1px solid var(--line); border-radius: 10px;
  padding: .2rem 1rem 1rem; margin: 1rem 0 1.4rem; }
section.q.answered { border-color: color-mix(in srgb, var(--ok) 45%, var(--line)); }
.q-options { border: 0; padding: 0; margin: .6rem 0 .4rem; display: grid; gap: .4rem; }
.opt { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: .6rem; align-items: start;
  padding: .55rem .7rem; border: 1px solid var(--line); border-radius: 8px; cursor: pointer; background: var(--bg); }
.opt:hover { border-color: var(--accent); }
.opt:has(input:checked) { border-color: var(--accent); background: var(--chosen); }
.opt input { margin-top: .3rem; accent-color: var(--accent); width: 1.05rem; height: 1.05rem; }
.opt-text { min-width: 0; }
.rec { font: 500 .72rem/1.4 var(--mono); color: var(--decided-fg); background: var(--decided-bg); border-radius: 4px;
  padding: .1rem .4rem; align-self: center; white-space: nowrap; }
.q-note-label { display: grid; gap: .25rem; margin-top: .5rem; font-size: .88rem; color: var(--muted); }
.q-note-label i { font-style: normal; }
.q-note.wanted { border-color: var(--warn); }
.q-status { min-height: 1.2rem; margin-top: .3rem; font-size: .8rem; color: var(--muted); }
.q-status.saved { color: var(--ok); }
.q-status.error { color: var(--warn); }
@media (max-width: 860px) {
  .wrap { grid-template-columns: minmax(0, 1fr); gap: 1.2rem; }
  nav { position: static; max-height: none; }
  nav ol { grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr)); }
  nav .toc3 { display: none; }
  .opt { grid-template-columns: auto minmax(0, 1fr); }
  .rec { grid-column: 2; justify-self: start; }
}
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
"""

JS = """
{
const PAGE = __PAGE__;
const QUESTION_IDS = __QUESTIONS__;
// Highlight every chip of one status.
const filters = [...document.querySelectorAll("button.filter")];
let current = null;
function light(kind) {
  document.querySelectorAll(".lit").forEach(e => e.classList.remove("lit"));
  filters.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.kind === kind)));
  if (!kind) return;
  document.querySelectorAll("main .req").forEach(c => {
    if ((c.dataset.status || "").split(" ").includes(kind)) c.classList.add("lit");
  });
}
filters.forEach(b => b.addEventListener("click", () => { current = current === b.dataset.kind ? null : b.dataset.kind; light(current); }));
// A link to a requirement opens its area's list.
function openTarget() {
  const id = decodeURIComponent(location.hash.slice(1));
  const el = id && document.getElementById(id);
  const area = el && el.closest("details");
  if (area && !area.open) { area.open = true; el.scrollIntoView(); }
  if (el && el.tagName === "TR") { el.classList.add("lit"); setTimeout(() => el.classList.remove("lit"), 2500); }
}
window.addEventListener("hashchange", openTarget);
openTarget();

let db = null, canWrite = true;
// ---- the questions: answers/<question id> ----
const sections = Object.fromEntries([...document.querySelectorAll("section.q")].map(s => [s.dataset.q, s]));
const dirty = new Set(), inFlight = new Map(), again = new Set(), timers = new Map();
function readForm(q) {
  const s = sections[q];
  const note = (s.querySelector(".q-note")?.value || "").trim();
  const picked = [...s.querySelectorAll("input:checked")];
  const answer = { question: q, kind: s.dataset.kind, note, updated: new Date().toISOString() };
  if (s.dataset.kind === "one") { answer.choice = picked[0]?.value ?? null; answer.choice_label = picked[0]?.dataset.label ?? null; }
  else if (s.dataset.kind === "any") { answer.choices = picked.map(i => i.value); answer.choice_labels = picked.map(i => i.dataset.label); }
  return answer;
}
function isAnswered(a) {
  if (!a) return false;
  if (a.kind === "one") return !!a.choice;
  if (a.kind === "any") return (a.choices || []).length > 0;
  return !!(a.note && a.note.trim());
}
function showState(q) {
  const s = sections[q], a = readForm(q);
  s.classList.toggle("answered", isAnswered(a));
  const note = s.querySelector(".q-note");
  const other = [...s.querySelectorAll("input:checked")].some(i => i.value === "other");
  if (note && s.dataset.kind !== "text") note.classList.toggle("wanted", other && !a.note);
  const n = QUESTION_IDS.filter(id => isAnswered(readForm(id))).length;
  const count = document.getElementById("answers-count");
  if (count) count.textContent = n + " of " + QUESTION_IDS.length + " answered";
}
function setStatus(el, text, cls) { if (!el) return; el.textContent = text; el.className = el.className.split(" ")[0] + (cls ? " " + cls : ""); }
function fill(q, a) {
  const s = sections[q];
  if (!s || !a) return;
  s.querySelectorAll("input").forEach(i => { i.checked = s.dataset.kind === "one" ? i.value === a.choice : (a.choices || []).includes(i.value); });
  const note = s.querySelector(".q-note");
  if (note) note.value = a.note || "";
  showState(q);
}
async function writeAnswer(q) {
  const status = sections[q].querySelector(".q-status");
  if (!db) { keepDraft(); setStatus(status, "Kept in this browser only", "error"); return; }
  if (!canWrite) { setStatus(status, "This view can't save answers", "error"); return; }
  if (inFlight.has(q)) { again.add(q); return; }
  const job = (async () => {
    setStatus(status, "Saving…");
    try { await db.doc("answers/" + q).set(readForm(q)); setStatus(status, "Saved", "saved"); return true; }
    catch (e) { setStatus(status, "Not saved (" + ((e && e.code) || "error") + "); edit again to retry", "error"); return false; }
  })();
  inFlight.set(q, job);
  const ok = await job;
  inFlight.delete(q);
  if (again.has(q)) { again.delete(q); return writeAnswer(q); }
  if (ok) dirty.delete(q);
}
function changedAnswer(q, delay) {
  dirty.add(q); showState(q);
  clearTimeout(timers.get("q:" + q));
  timers.set("q:" + q, setTimeout(() => writeAnswer(q), delay));
}
for (const [q, s] of Object.entries(sections)) {
  s.querySelectorAll("input").forEach(i => i.addEventListener("change", () => changedAnswer(q, 150)));
  s.querySelector(".q-note")?.addEventListener("input", () => changedAnswer(q, 900));
}

// ---- the boxes: writing/<page>--<anchor> ----
const boxes = Object.fromEntries([...document.querySelectorAll(".box")].map(b => [b.dataset.box, b]));
const boxDirty = new Set(), boxFlight = new Map(), boxAgain = new Set();
function sectionTitle(box) {
  const id = box.dataset.anchor;
  const h = document.getElementById(id);
  return h ? h.textContent.trim() : id;
}
function renderEverything() {
  const list = document.getElementById("everything-list");
  const written = Object.values(boxes).filter(b => b.querySelector("textarea").value.trim());
  Object.values(boxes).forEach(b => b.classList.toggle("written", !!b.querySelector("textarea").value.trim()));
  list.textContent = "";
  if (!written.length) { const p = document.createElement("p"); p.className = "empty"; p.textContent = "Nothing written yet."; list.append(p); return; }
  for (const b of written) {
    const entry = document.createElement("div"); entry.className = "entry";
    const h = document.createElement("h4"); const a = document.createElement("a");
    a.href = "#" + b.dataset.anchor; a.textContent = sectionTitle(b); h.append(a);
    const p = document.createElement("p"); p.textContent = b.querySelector("textarea").value.trim();
    entry.append(h, p); list.append(entry);
  }
}
async function writeBox(key) {
  const box = boxes[key], status = box.querySelector(".box-status");
  if (!db) { keepDraft(); setStatus(status, "Kept in this browser only", "error"); return; }
  if (!canWrite) { setStatus(status, "This view can't save", "error"); return; }
  if (boxFlight.has(key)) { boxAgain.add(key); return; }
  const job = (async () => {
    setStatus(status, "Saving…");
    try {
      await db.doc("writing/" + key).set({ page: PAGE, section: box.dataset.anchor, title: sectionTitle(box),
        text: box.querySelector("textarea").value, updated: new Date().toISOString() });
      setStatus(status, "Saved", "saved"); return true;
    } catch (e) { setStatus(status, "Not saved (" + ((e && e.code) || "error") + "); edit again to retry", "error"); return false; }
  })();
  boxFlight.set(key, job);
  const ok = await job;
  boxFlight.delete(key);
  if (boxAgain.has(key)) { boxAgain.delete(key); return writeBox(key); }
  if (ok) boxDirty.delete(key);
}
for (const [key, box] of Object.entries(boxes)) {
  box.querySelector("textarea").addEventListener("input", () => {
    boxDirty.add(key); renderEverything();
    clearTimeout(timers.get("b:" + key));
    timers.set("b:" + key, setTimeout(() => writeBox(key), 900));
  });
}
document.getElementById("copy-all").addEventListener("click", async () => {
  const text = Object.values(boxes).filter(b => b.querySelector("textarea").value.trim())
    .map(b => "## " + sectionTitle(b) + "\\n\\n" + b.querySelector("textarea").value.trim()).join("\\n\\n");
  const status = document.getElementById("copy-status");
  try { await navigator.clipboard.writeText(text || ""); status.textContent = text ? "Copied" : "Nothing to copy yet"; }
  catch (e) {
    const list = document.getElementById("everything-list");
    const range = document.createRange(); range.selectNodeContents(list);
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range);
    status.textContent = "Selected: press Ctrl+C (or Cmd+C) to copy";
  }
});
// A draft in this browser, when the page can't reach its store.
const DRAFT_KEY = "openllmri-" + PAGE + "-draft";
function keepDraft() {
  try {
    const all = { answers: Object.fromEntries(QUESTION_IDS.map(q => [q, readForm(q)])),
      boxes: Object.fromEntries(Object.entries(boxes).map(([k, b]) => [k, b.querySelector("textarea").value])) };
    localStorage.setItem(DRAFT_KEY, JSON.stringify(all));
  } catch (e) { /* storage may be blocked */ }
}
function loadDraft() {
  try {
    const all = JSON.parse(localStorage.getItem(DRAFT_KEY) || "{}");
    for (const [q, a] of Object.entries(all.answers || {})) if (sections[q]) fill(q, a);
    for (const [k, t] of Object.entries(all.boxes || {})) if (boxes[k]) boxes[k].querySelector("textarea").value = t;
    renderEverything();
  } catch (e) { /* nothing to restore */ }
}
function setMode(text) { const el = document.getElementById("answers-mode"); if (el) el.textContent = text; }

(async () => {
  let found = null;
  try { found = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { found = null; }
  if (!found) { loadDraft(); setMode("Not connected: what you write stays in this browser. Open the page at claude.ai, signed in, to save it for Claude."); return; }
  db = found;
  try {
    const user = await window.claude.use("user");
    const may = user ? await user.can("data.write") : null;
    if (may === false) {
      canWrite = false;
      document.querySelectorAll("section.q input, textarea").forEach(el => { el.disabled = true; });
      setMode("Read only: what Andrew wrote shows here.");
    }
  } catch (e) { /* a refused write decides */ }
  if (canWrite) setMode("Answers save as you go, and Claude reads them here.");
  db.collection("answers").onSnapshot(snap => {
    for (const d of snap.docs) {
      if (!d.exists || !sections[d.id] || dirty.has(d.id) || inFlight.has(d.id)) continue;
      fill(d.id, d.data()); setStatus(sections[d.id].querySelector(".q-status"), "Saved", "saved");
    }
  }, err => setMode("Answers can't load right now (" + (err && err.code) + "); reload to try again."));
  db.collection("writing").onSnapshot(snap => {
    for (const d of snap.docs) {
      if (!d.exists || !boxes[d.id] || boxDirty.has(d.id) || boxFlight.has(d.id)) continue;
      boxes[d.id].querySelector("textarea").value = (d.data() || {}).text || "";
      setStatus(boxes[d.id].querySelector(".box-status"), "Saved", "saved");
    }
    renderEverything();
  }, () => { /* the boxes keep what is typed */ });
  const words = [...document.querySelectorAll(".words")];
  if (words.length) db.collection("words").onSnapshot(snap => {
    const byId = Object.fromEntries(snap.docs.filter(d => d.exists).map(d => [d.id, d.data()]));
    for (const w of words) {
      const doc = byId[w.dataset.words];
      if (!doc || !doc.text) { w.hidden = true; continue; }
      w.textContent = "";
      const who = document.createElement("span"); who.className = "who";
      who.textContent = "Andrew's own words" + (doc.when ? ", " + doc.when : "") + " (from this page's private store)";
      const q = document.createElement("span"); q.textContent = doc.text;
      w.append(who, q); w.hidden = false;
    }
  }, () => {});
})();
// The comment buttons open the page's comment composer on their section.
(async () => {
  let comments = null;
  try { comments = window.claude && window.claude.use ? await window.claude.use("comments") : null; } catch (e) { comments = null; }
  if (!comments) return;
  document.querySelectorAll(".box").forEach(box => {
    const btn = box.querySelector(".comment-btn");
    btn.hidden = false;
    btn.addEventListener("click", async () => {
      const target = document.getElementById(box.dataset.anchor) || box;
      try { await comments.openComposer({ element: target }); }
      catch (e) { if (e && e.code === "unavailable") document.querySelectorAll(".comment-btn").forEach(b => { b.hidden = true; }); }
    });
  });
})();
QUESTION_IDS.forEach(showState);
renderEverything();
}
"""

intro_match = re.search(r"<p><strong>Status:</strong>(.*?)</p>", body, re.S)
intro = intro_match.group(1).strip() if intro_match else ""
body = re.sub(r"<p><strong>Status:</strong>.*?</p>", "", body, count=1, flags=re.S)
body = re.sub(r"<p>Related:.*?</p>", "", body, count=1, flags=re.S)
title_text = title_match.group(1) if title_match else TITLES[PAGE]
page = f"""<title>{TITLES[PAGE]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <h1>{title_text}</h1>
    <p><b>Status:</b> {intro}</p>
    <p>{other_link}{" · " if other_link else ""}Write in the box under any section; it saves as you type. Chips are requirements:
    point at one to read it, click it to open it in the list.</p>
    <div class="filters" role="group" aria-label="Highlight the requirements of one status"><span>Highlight:</span> {legend}</div>
  </header>
  <nav aria-label="Sections"><h2>Sections</h2><ol>{toc_html}</ol></nav>
  <main>{body}{everything}</main>
</div>
<script>{JS.replace("__PAGE__", json.dumps(PAGE)).replace("__QUESTIONS__", json.dumps(answerable))}</script>
"""
Path(args.out).write_text(page, encoding="utf-8")
box_count = page.count('<div class="box"')
print(f"{PAGE}: {len(toc)} sections, {len(blocks)} questions, {box_count} boxes, "
      f"{sum(cited.values())} citations ({dict(cited)}), {len(page)} bytes")
