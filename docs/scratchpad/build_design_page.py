"""Render docs/DESIGN.md into the web page Andrew reads it in (the repo file stays the source).

Usage:
  .venv/bin/python docs/scratchpad/build_design_page.py docs/DESIGN.md <out.html> [--title T] [--intro HTML]
then publish <out.html> to the private web page https://claude.ai/artifact/Wi63bmMUa3NXqkUwni4CJ5
(Artifact tool, with that url, declaring the `db` and `user` capabilities so answers save). The same
script renders other documents written the same way (the slice plans), with their own --title and
--intro.

- The decision marks ([Decided, …], [Proposed …], [Built …], [Open …]) become coloured chips, the
  parts get a sidebar of links, and a toggle highlights one kind of mark.
- Questions become a form. A heading `### L20. Title` or `#### L16.1. Title` starts a question;
  list items `- ( ) choice` offer one choice among several, `- [ ] choice` any number of them, a
  choice ending in "(recommended)" is shown as Claude's recommendation, and every question with
  choices gets a note box. A question with neither choices nor sub-questions is answered in a text
  box. Answers save to the page's database (`answers/<question id>`), where Claude reads them; in a
  view without the database they stay in the browser as a draft.
"""
import argparse
import html
import json
import re
from collections import Counter
from typing import Dict, List

from markdown_it import MarkdownIt

parser = argparse.ArgumentParser()
parser.add_argument("src")
parser.add_argument("out")
parser.add_argument("--title", default="Open LLMRI Design")
parser.add_argument("--intro", default="Approved by Andrew on 2026-10-08. Rendered from <code>docs/DESIGN.md</code>, "
                    "which stays the source. Every passage carries a mark; pick one to highlight where it appears. "
                    "Part L's open questions are a form: your answers save as you go. "
                    '<a href="#part-l-questions-for-andrew">Go to the questions</a>.')
args = parser.parse_args()

text = open(args.src, encoding="utf-8").read()
md = MarkdownIt("commonmark", {"html": False}).enable("table")

# --- Questions: cut each question block out of the markdown, render it as a form, and put it back.
QUESTION = re.compile(r"^(#{3,4}) (L\d+(?:\.\d+)*)\. (.+)$")
HEADING = re.compile(r"^#{1,4} ")
OPTION = re.compile(r"^- (\( \)|\[ \]) (.+)$")
lines = text.split("\n")
heads = [i for i, line in enumerate(lines) if QUESTION.match(line)]
blocks: List[Dict] = []
out_lines: List[str] = []
i = 0
while i < len(lines):
    m = QUESTION.match(lines[i])
    if not m:
        out_lines.append(lines[i])
        i += 1
        continue
    level, qid, title = len(m.group(1)), m.group(2), m.group(3)
    j = i + 1
    while j < len(lines) and not HEADING.match(lines[j]):
        j += 1
    body_lines = lines[i + 1:j]
    options = []
    context = []
    for line in body_lines:
        om = OPTION.match(line)
        if om:
            label = om.group(2).strip()
            recommended = label.endswith("(recommended)")
            if recommended:
                label = label[: -len("(recommended)")].rstrip()
            options.append({"multi": om.group(1) == "[ ]", "label": label, "recommended": recommended})
        else:
            context.append(line)
    has_children = any(QUESTION.match(lines[k]).group(2).startswith(qid + ".") for k in heads if k > i)
    kind = "parent" if has_children else ("any" if options and options[0]["multi"] else ("one" if options else "text"))
    letters = "abcdefghij"
    for n, opt in enumerate(options):
        opt["key"] = "other" if opt["label"].lower().startswith("other") else letters[n]
    blocks.append({"id": qid, "level": level, "title": title, "kind": kind, "options": options,
                   "context": "\n".join(context).strip()})
    out_lines.extend(["", f"QUESTIONBLOCK{len(blocks) - 1}", ""])
    i = j


def render_question(b: Dict) -> str:
    qid, tag = b["id"], f"h{b['level']}"
    slug = re.sub(r"[^a-z0-9]+", "-", f"{qid} {b['title']}".lower()).strip("-")
    parts = [f'<section class="q q-{b["kind"]}" id="q-{html.escape(qid)}" data-q="{html.escape(qid)}" data-kind="{b["kind"]}">',
             f'<{tag} id="{slug}">{html.escape(qid)}. {md.renderInline(b["title"])}</{tag}>']
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
    elif b["kind"] == "text":
        parts.append('<label class="q-note-label"><span>Your answer</span><textarea class="q-note" rows="4"></textarea></label>')
    if b["kind"] != "parent":
        parts.append('<div class="q-status" aria-live="polite"></div>')
    parts.append("</section>")
    return "\n".join(parts)


body = md.render("\n".join(out_lines))
for n, b in enumerate(blocks):
    body = body.replace(f"<p>QUESTIONBLOCK{n}</p>", render_question(b))
answerable = [b for b in blocks if b["kind"] != "parent"]
if answerable:
    progress = ('<div class="answers-bar" id="answers-bar"><span id="answers-count">0 of '
                f'{len(answerable)} answered</span><span id="answers-mode">Connecting…</span></div>')
    body = re.sub(r"(<h2>Part L[^<]*</h2>)", r"\1" + progress, body, count=1)

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
filters = (f'<div class="filters" role="group" aria-label="Highlight one kind of mark"><span>Highlight:</span> {summary}</div>'
           if sum(counts.values()) else "")
question_ids = json.dumps([b["id"] for b in answerable])

page = f"""<title>{html.escape(args.title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
/* Layout: a reading column beside a sticky list of parts; one column on phones. */
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --fg: #18202c; --muted: #586274; --line: #dde2ea;
  --accent: #2c55c4; --hl: #fff4cc; --ok: #17633d; --warn: #8a4b00; --chosen: #eef3ff;
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
  --accent: #8aa8ff; --hl: #3a3420; --ok: #8fd9b0; --warn: #f2bf7a; --chosen: #1d2638;
  --decided-bg: #17352a; --decided-fg: #8fd9b0; --proposed-bg: #3a2a14; --proposed-fg: #f2bf7a;
  --built-bg: #1c2a40; --built-fg: #a9c2ee; --open-bg: #2c2140; --open-fg: #d2b2f0; --idea-bg: #143534; --idea-fg: #8fd6d2; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #11151c; --surface: #171c25; --fg: #e3e8f0; --muted: #9aa5b6; --line: #2a3240;
  --accent: #8aa8ff; --hl: #3a3420; --ok: #8fd9b0; --warn: #f2bf7a; --chosen: #1d2638;
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
main h3 {{ font: 600 1.18rem/1.3 var(--display); margin: 2rem 0 .5rem; text-wrap: balance; }}
main h4 {{ font: 600 1rem/1.35 var(--display); margin: 1.4rem 0 .4rem; text-wrap: balance; }}
main p, main li {{ max-width: 68ch; }}
main ul, main ol {{ padding-left: 1.3rem; }}
main li {{ margin: .2rem 0; }}
main li > ul, main li > ol {{ margin: .2rem 0; }}
code {{ font: .88em var(--mono); background: var(--surface); border: 1px solid var(--line); border-radius: 3px; padding: 0 .25em; overflow-wrap: anywhere; }}
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
/* The questions' form */
.sr-only {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
.answers-bar {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 2; display: flex; flex-wrap: wrap; gap: .4rem 1.2rem;
  justify-content: space-between; align-items: center; background: var(--surface); border: 1px solid var(--line);
  border-radius: 8px; padding: .5rem .8rem; margin: .4rem 0 1.2rem; font-size: .9rem; max-width: 68ch; box-sizing: border-box; }}
#answers-count {{ font-weight: 600; }}
#answers-mode {{ color: var(--muted); }}
section.q {{ max-width: 68ch; }}
section.q-one, section.q-any, section.q-text {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px;
  padding: .2rem 1rem 1rem; margin: 1rem 0 1.4rem; }}
section.q.answered {{ border-color: color-mix(in srgb, var(--ok) 45%, var(--line)); }}
.q-context p, .q-context li {{ color: var(--fg); }}
.q-options {{ border: 0; padding: 0; margin: .6rem 0 .4rem; display: grid; gap: .4rem; }}
.opt {{ display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: .6rem; align-items: start;
  padding: .55rem .7rem; border: 1px solid var(--line); border-radius: 8px; cursor: pointer; background: var(--bg); }}
.opt:hover {{ border-color: var(--accent); }}
.opt:has(input:checked) {{ border-color: var(--accent); background: var(--chosen); }}
.opt input {{ margin-top: .3rem; accent-color: var(--accent); width: 1.05rem; height: 1.05rem; }}
.opt-text {{ min-width: 0; }}
.rec {{ font: 500 .72rem/1.4 var(--mono); color: var(--decided-fg); background: var(--decided-bg); border-radius: 4px;
  padding: .1rem .4rem; align-self: center; white-space: nowrap; }}
.q-note-label {{ display: grid; gap: .25rem; margin-top: .5rem; font-size: .88rem; color: var(--muted); }}
.q-note-label i {{ font-style: normal; }}
.q-note {{ width: 100%; box-sizing: border-box; font: 15px/1.5 var(--body); color: var(--fg); background: var(--bg);
  border: 1px solid var(--line); border-radius: 8px; padding: .45rem .6rem; resize: vertical; }}
.q-note:focus, .opt:focus-within {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
.q-note.wanted {{ border-color: var(--warn); }}
.q-status {{ min-height: 1.2rem; margin-top: .3rem; font-size: .8rem; color: var(--muted); }}
.q-status.saved {{ color: var(--ok); }}
.q-status.error {{ color: var(--warn); }}
@media (max-width: 860px) {{
  .wrap {{ grid-template-columns: minmax(0, 1fr); gap: 1.2rem; }}
  nav {{ position: static; max-height: none; }}
  nav ol {{ grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr)); }}
  .opt {{ grid-template-columns: auto minmax(0, 1fr); }}
  .rec {{ grid-column: 2; justify-self: start; }}
}}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
</style>
<div class="wrap">
  <header>
    <h1>{title_match.group(1) if title_match else html.escape(args.title)}</h1>
    <p>{args.intro}</p>
    {filters}
  </header>
  <nav aria-label="Parts"><h2>Parts</h2><ol>{toc_html}</ol></nav>
  <main>{body}</main>
</div>
<script>
{{  // one block, so the page's names stay its own
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

// The questions' form: every answer is one document, answers/<question id>, in the page's database.
const QUESTION_IDS = {question_ids};
const DRAFT_KEY = "design-answers-draft";
const sections = Object.fromEntries([...document.querySelectorAll("section.q")]
  .filter(s => s.dataset.kind !== "parent").map(s => [s.dataset.q, s]));
let db = null;
let canWrite = true;
const dirty = new Set();        // questions with an edit not yet saved
const inFlight = new Map();     // question -> the write in progress
const again = new Set();        // questions edited while their write was in progress
const timers = new Map();

function readForm(q) {{
  const s = sections[q];
  const note = (s.querySelector(".q-note")?.value || "").trim();
  const picked = [...s.querySelectorAll("input:checked")];
  const answer = {{ question: q, kind: s.dataset.kind, note, updated: new Date().toISOString() }};
  if (s.dataset.kind === "one") {{
    answer.choice = picked[0]?.value ?? null;
    answer.choice_label = picked[0]?.dataset.label ?? null;
  }} else if (s.dataset.kind === "any") {{
    answer.choices = picked.map(i => i.value);
    answer.choice_labels = picked.map(i => i.dataset.label);
  }}
  return answer;
}}

function isAnswered(a) {{
  if (!a) return false;
  if (a.kind === "one") return !!a.choice;
  if (a.kind === "any") return (a.choices || []).length > 0;
  return !!(a.note && a.note.trim());
}}

function showState(q) {{
  const s = sections[q];
  const a = readForm(q);
  s.classList.toggle("answered", isAnswered(a));
  const note = s.querySelector(".q-note");
  const otherPicked = [...s.querySelectorAll("input:checked")].some(i => i.value === "other");
  if (note && s.dataset.kind !== "text") note.classList.toggle("wanted", otherPicked && !a.note);
  const n = QUESTION_IDS.filter(id => isAnswered(readForm(id))).length;
  const count = document.getElementById("answers-count");
  if (count) count.textContent = n + " of " + QUESTION_IDS.length + " answered";
}}

function setStatus(q, text, cls) {{
  const el = sections[q]?.querySelector(".q-status");
  if (!el) return;
  el.textContent = text;
  el.className = "q-status" + (cls ? " " + cls : "");
}}

function fill(q, a) {{
  const s = sections[q];
  if (!s || !a) return;
  s.querySelectorAll("input").forEach(i => {{
    i.checked = s.dataset.kind === "one" ? i.value === a.choice : (a.choices || []).includes(i.value);
  }});
  const note = s.querySelector(".q-note");
  if (note) note.value = a.note || "";
  showState(q);
}}

function saveDraft() {{
  try {{
    const all = Object.fromEntries(QUESTION_IDS.map(q => [q, readForm(q)]));
    localStorage.setItem(DRAFT_KEY, JSON.stringify(all));
  }} catch (e) {{ /* storage may be blocked; the draft is a convenience only */ }}
}}

function loadDraft() {{
  try {{
    const all = JSON.parse(localStorage.getItem(DRAFT_KEY) || "{{}}");
    for (const [q, a] of Object.entries(all)) if (sections[q]) fill(q, a);
  }} catch (e) {{ /* nothing to restore */ }}
}}

async function write(q) {{
  if (!db) {{ saveDraft(); setStatus(q, "Kept in this browser only", "error"); return; }}
  if (!canWrite) {{ setStatus(q, "This view can't save answers", "error"); return; }}
  if (inFlight.has(q)) {{ again.add(q); return; }}
  const job = (async () => {{
    setStatus(q, "Saving…");
    try {{
      await db.doc("answers/" + q).set(readForm(q));
      setStatus(q, "Saved", "saved");
      return true;
    }} catch (e) {{
      const code = e && e.code;
      if (code === "invalid_argument") {{ canWrite = false; setStatus(q, "This view can't save answers", "error"); }}
      else setStatus(q, "Not saved (" + (code || "error") + "); edit again to retry", "error");
      return false;
    }}
  }})();
  inFlight.set(q, job);
  const ok = await job;
  inFlight.delete(q);
  if (again.has(q)) {{ again.delete(q); return write(q); }}
  if (ok) dirty.delete(q);  // an unsaved edit stays, so a later snapshot can't overwrite it
}}

function changed(q, delay) {{
  dirty.add(q);
  showState(q);
  clearTimeout(timers.get(q));
  timers.set(q, setTimeout(() => write(q), delay));
}}

for (const [q, s] of Object.entries(sections)) {{
  s.querySelectorAll("input").forEach(i => i.addEventListener("change", () => changed(q, 150)));
  s.querySelector(".q-note")?.addEventListener("input", () => changed(q, 900));
}}

function setMode(text) {{
  const el = document.getElementById("answers-mode");
  if (el) el.textContent = text;
}}

(async () => {{
  if (!QUESTION_IDS.length) return;
  let found = null;
  try {{ found = window.claude && window.claude.use ? await window.claude.use("db") : null; }} catch (e) {{ found = null; }}
  if (!found) {{
    loadDraft();
    setMode("Not connected: answers stay in this browser. Open the page at claude.ai, signed in, to save them for Claude.");
    return;
  }}
  db = found;
  try {{
    const user = window.claude.use ? await window.claude.use("user") : null;
    const may = user ? await user.can("data.write") : null;
    if (may === false) {{
      canWrite = false;
      document.querySelectorAll("section.q input, section.q textarea").forEach(el => {{ el.disabled = true; }});
      setMode("Read only: answers saved by Andrew show here.");
    }}
  }} catch (e) {{ /* keep the inputs; a refused write decides */ }}
  if (canWrite) setMode("Answers save as you go, and Claude reads them here.");
  db.collection("answers").onSnapshot(snap => {{
    for (const d of snap.docs) {{
      if (!d.exists || !sections[d.id] || dirty.has(d.id) || inFlight.has(d.id)) continue;
      fill(d.id, d.data());
      setStatus(d.id, "Saved", "saved");
    }}
  }}, err => setMode("Answers can't load right now (" + (err && err.code) + "); reload the page to try again."));
}})();
QUESTION_IDS.forEach(showState);
}}
</script>
"""
open(args.out, "w", encoding="utf-8").write(page)
print(f"{len(toc)} parts; marks: {dict(counts)}; {len(answerable)} questions; {len(page)} bytes")
