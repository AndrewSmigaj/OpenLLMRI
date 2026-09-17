#!/usr/bin/env python3
"""review_packet — build the design-review page from docs/design/*.md (host-side, stdlib only).

For each design document, in index order, extract: the status (from the banner), the one-paragraph
experience (part 3), the provenance (part 2: Andrew's decisions + the proposals), the open questions
(part 6) and the review log (part 7). Emit ONE HTML page: a progress strip (23 boxes), one section per
document with anchors, and the parked list. The GDD umbrella gets a hand-written section (it does not
follow the template). Andrew reads the page; answers land in the terminal; the page is regenerated.

    python3 tools/review_packet.py --current 01 --out /path/review-packet.html [--parked parked.md]
"""
from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs" / "design"

ORDER = [  # (key, block, file or None for the GDD)
    ("GDD", 1, None),
    ("01", 1, "01-premise-and-world.md"), ("02", 1, "02-the-experience.md"),
    ("03", 1, "03-the-player-view.md"), ("04", 1, "04-grammar-and-feedback.md"),
    ("05", 1, "05-ontology-and-sufficiency.md"),
    ("06", 2, "06-time-sleep-and-the-clock.md"), ("07", 2, "07-fire-and-shaping.md"),
    ("08", 2, "08-warmth-clothing-and-shelter.md"), ("09", 2, "09-water.md"),
    ("10", 2, "10-food-and-hunger.md"), ("11", 2, "11-injury-and-first-aid.md"),
    ("12", 2, "12-the-pilot-and-bodies.md"),
    ("13", 3, "13-events-escalation-and-weather.md"), ("14", 3, "14-rescue-paths.md"),
    ("15", 3, "15-moral-and-social-layer.md"), ("16", 3, "16-players-and-kit.md"),
    ("17", 3, "17-rooms-and-living-rooms.md"), ("18", 3, "18-materials-and-forms.md"),
    ("19", 4, "19-multiplayer-and-instances.md"), ("20", 4, "20-the-agent-player-and-research.md"),
    ("21", 4, "21-endings-and-recap.md"), ("22", 4, "22-the-world-building-loops.md"),
]
BLOCK_NAMES = {1: "Foundations", 2: "Survival systems", 3: "The world and the stakes",
               4: "Multiplayer, research, endings, the loops"}

SECTION_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(?P<name>[^\n]+?)\s*$", re.M)


def split_sections(text: str) -> dict[str, str]:
    """{normalised section name: body} for every '## ' heading (numbering stripped)."""
    out = {}
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        name = m.group("name").lower()
        name = re.sub(r"\s*[—–-].*$", "", name).strip()  # "Provenance — whose design this is"
        out[name] = text[m.end():end].strip("\n")
    return out


def status_of(text: str) -> str:
    head = text[:1500].lower()
    if "finalized" in head:
        return "finalized"
    if "reviewed with andrew" in head:
        return "reviewed"
    return "draft"


def title_of(text: str, key: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    t = m.group(1).strip() if m else key
    t = re.sub(r"^\d+\s*[—–-]\s*", "", t)  # "01 — The premise…" → "The premise…"
    return t


# ---------- a small Markdown → HTML (paragraphs, lists, tables, quotes, ### heads, inline) ----------
def inline(md: str) -> str:
    s = html.escape(md, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href=\"\2\">\1</a>", s)
    return s


def md_to_html(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            out.append(f"<h4>{inline(ln[4:].strip())}</h4>"); i += 1; continue
        if ln.startswith("#### "):
            out.append(f"<h5>{inline(ln[5:].strip())}</h5>"); i += 1; continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i]); i += 1
            hdr = [c.strip() for c in rows[0].strip().strip("|").split("|")]
            body = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows[2:]]
            t = ["<div class='tablewrap'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in hdr) + "</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue
        if ln.startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip()); i += 1
            out.append(f"<blockquote>{md_to_html(chr(10).join(q))}</blockquote>"); continue
        if ln.startswith("```"):
            code = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out.append("<pre>" + html.escape("\n".join(code)) + "</pre>"); continue
        m_ol = re.match(r"^(\s*)(\d+)\.\s+(.*)$", ln)
        m_ul = re.match(r"^(\s*)[-*]\s+(.*)$", ln)
        if m_ol or m_ul:
            tag = "ol" if m_ol else "ul"
            items = []
            while i < len(lines):
                cur = lines[i]
                mo = re.match(r"^(\s*)(\d+)\.\s+(.*)$", cur) if tag == "ol" else re.match(r"^(\s*)[-*]\s+(.*)$", cur)
                if mo:
                    items.append(mo.group(3) if tag == "ol" else mo.group(2)); i += 1
                elif cur.startswith(("   ", "\t")) and items and cur.strip():
                    items[-1] += " " + cur.strip(); i += 1
                elif not cur.strip():
                    # a blank line ends the list only if the next non-blank line is not a list item
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    nxt = lines[j] if j < len(lines) else ""
                    if (tag == "ol" and re.match(r"^\s*\d+\.\s+", nxt)) or (tag == "ul" and re.match(r"^\s*[-*]\s+", nxt)):
                        i = j
                    else:
                        break
                else:
                    break
            start = f" start=\"{m_ol.group(2)}\"" if m_ol and m_ol.group(2) != "1" else ""
            out.append(f"<{tag}{start}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>"); continue
        # paragraph: gather until blank / block start
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{3,}\s|>|```|\s*[-*]\s+|\s*\d+\.\s+|\s*\|)", lines[i]):
            para.append(lines[i].strip()); i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        else:
            i += 1
    return "\n".join(out)


# ---------- the GDD umbrella (hand-written brief; it does not follow the template) ----------
GDD_BRIEF = {
    "title": "The GDD — the umbrella",
    "paragraph": (
        "Whiteout — survivors of a snowy plane crash improvise with a physically-modeled world to outlast "
        "cold, injury, hunger and a worsening storm until rescue, escape, or collapse. The essential experience: "
        "understanding a living, reactive world under pressure, and being told, physically and specifically, "
        "why each desperate idea works or doesn't. You survive by understanding the world, not by guessing the "
        "author's verb. The GDD is now the umbrella — pitch, vision, cross-cutting rules, and the chapter index "
        "into the 22 documents."),
    "decisions": [
        "Runtime is 100% deterministic; no language model in the running game, ever (§3, June; DR-02).",
        "A continuously running real-time clock nobody can stall; 20× by consensus when everyone sleeps or waits (June; DR-14a, 2026-09-07).",
        "Instanced, synchronous co-op; a run is roughly a week of game time, persisting across sittings (DR-15a — the one-day wording was never Andrew's).",
        "Input is the taught grammar `VERB X [RELATION Y] [WITH Z]`; feedback is clarification only, never a menu (§25a; DR-08c, 2026-09-16).",
        "The world is open-ended; every count is a floor (VISION, 2026-09-16).",
    ],
    "proposals": [
        "P1 — §0a improvement 1: all interactions pre-built; the LLM is a build-time authoring tool only.",
        "P2 — §0a improvement 2: cheap objects, rich materials and operation rules; heavy packets only for puzzle-critical things (packets since retired, DR-17a).",
        "P3 — §0a improvement 3: conservation as a runtime ledger.",
        "P4 — §0a improvement 4: the global softlock check + a no-materials warmth floor (the floor is also Q1 of doc 08).",
        "P5 — §0a improvement 5: the one-room slice first (history now — built in June/July).",
        "P6 — §0a improvement 6: coverage = invariants + a fuzzer + a curated set (since replaced by the probe corpus, DR-18a).",
        "P7 — §6 'one dense scene (cabin + camp + near-forest) gets the whole data budget rather than spread thin' (June text; the whole valley is now in the first run).",
        "P8 — §42 build plan and §46 scope as written (the June waterfall; PLAN.md now holds the order).",
    ],
    "questions": [
        ("Q1", "Is the pitch and the essential experience (§1–§2) right as written?",
         ["(a) yes, as the umbrella's opening", "(b) rewrite — say what"], "a"),
        ("Q2", "The six §0a improvements: keep as decisions (P1–P6), with P2/P5/P6 marked as history?",
         ["(a) keep, mark history where noted", "(b) strike P5/P6 entirely", "(c) revisit one — name it"], "a"),
        ("Q3", "§6's 'one dense scene … rather than spread thin' against the whole valley being in the first run.",
         ["(a) strike the line; the valley is the scene", "(b) keep it as the density principle: the crash site densest, the valley as designed", "(c) rewrite"], "b"),
        ("Q4", "The per-system sections (§19, §31–§39 etc.) carry June seed text that is now superseded: pointer lines only, or strike the seed text?",
         ["(a) pointer lines only, body untouched", "(b) strike the superseded seed text; keep the pointers", "(c) rewrite each section as a two-line summary of its chapter"], "c"),
    ],
}

CSS = r"""
:root{--bg:#F3F5F7;--panel:#FFFFFF;--ink:#17212B;--muted:#5B6B78;--rule:#D5DCE2;--ember:#C2551F;--spruce:#2E7D5B;--ice:#8FB3C9;--amber:#B08A1E;--codebg:#E9EEF2;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#101820;--panel:#172230;--ink:#E6ECF1;--muted:#9AAAB8;--rule:#2A3745;--ember:#E0733A;--spruce:#4FA57F;--ice:#7FA6C0;--amber:#D1A93E;--codebg:#1F2C3A;}}
:root[data-theme="dark"]{--bg:#101820;--panel:#172230;--ink:#E6ECF1;--muted:#9AAAB8;--rule:#2A3745;--ember:#E0733A;--spruce:#4FA57F;--ice:#7FA6C0;--amber:#D1A93E;--codebg:#1F2C3A;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.55;padding-block:0 4rem;padding-inline:16px}
a{color:inherit}
code,pre,.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-size:.92em}
code{background:var(--codebg);padding:.05em .35em;border-radius:3px}
pre{background:var(--codebg);padding:.8rem 1rem;overflow-x:auto;border-radius:4px}
.wrap{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:2.5rem}
@media (max-width:860px){.wrap{grid-template-columns:1fr}}
.rail{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding-block:1.5rem 1rem}
@media (max-width:860px){.rail{position:static;max-height:none}}
.brand{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.25rem;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:.85rem;margin:.15rem 0 1rem}
.strip{display:grid;grid-template-columns:repeat(auto-fill,minmax(30px,1fr));gap:4px;margin-bottom:1rem}
.strip a{display:block;aspect-ratio:1;border:1.5px solid var(--rule);border-radius:3px;text-decoration:none;text-align:center;font-size:.68rem;line-height:28px;color:var(--muted)}
.strip a.finalized{background:var(--spruce);border-color:var(--spruce);color:#fff}
.strip a.reviewed{background:var(--ice);border-color:var(--ice);color:#fff}
.strip a.current{outline:2px solid var(--ember);outline-offset:1px;color:var(--ember);font-weight:700}
.toc{list-style:none;padding:0;margin:0;font-size:.88rem}
.toc li{padding:.22rem 0;border-top:1px solid var(--rule)}
.toc li a{text-decoration:none;display:flex;gap:.5rem;align-items:baseline}
.toc .k{font-family:"IBM Plex Mono",monospace;font-size:.75rem;color:var(--muted);min-width:2.6em}
.toc li.current a{color:var(--ember);font-weight:600}
.toc li.finalized .k::after{content:" ✓";color:var(--spruce)}
.toc .blk{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:.9rem 0 .25rem;border-top:0}
main{padding-block:1.5rem;min-width:0}
.procedure{border:1px solid var(--rule);background:var(--panel);padding:1rem 1.25rem;border-radius:4px;font-size:.92rem;max-width:68ch}
.procedure ol{margin:.4rem 0 0;padding-left:1.2rem}
section.doc{max-width:68ch;padding-block:2.2rem 1rem;border-top:1px solid var(--rule);margin-top:1.5rem}
section.doc:first-of-type{border-top:0}
.eyebrow{font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);display:flex;gap:.75rem;align-items:center;flex-wrap:wrap}
.pill{display:inline-block;padding:.05rem .5rem;border-radius:99px;border:1px solid var(--rule);font-size:.72rem;letter-spacing:.06em}
.pill.finalized{background:var(--spruce);border-color:var(--spruce);color:#fff}
.pill.reviewed{background:var(--ice);border-color:var(--ice);color:#fff}
.pill.current{border-color:var(--ember);color:var(--ember)}
h2{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:1.65rem;line-height:1.2;margin:.35rem 0 1rem;text-wrap:balance;letter-spacing:-.01em}
h3{font-size:.8rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:1.8rem 0 .6rem;font-weight:600}
h4{font-size:1rem;margin:1.1rem 0 .3rem}
h5{font-size:.92rem;margin:.9rem 0 .2rem;color:var(--muted)}
.lead{font-family:"Source Serif 4",Georgia,serif;font-size:1.12rem;line-height:1.55}
.lead p{margin:0 0 .8rem}
.decisions{border-left:3px solid var(--spruce);padding-left:1rem}
.questions ol{padding-left:0;list-style:none;margin:0}
.questions li{margin:.9rem 0;padding:.75rem .9rem;background:var(--panel);border:1px solid var(--rule);border-radius:4px}
.questions .q{font-weight:600}
.questions .opts{margin:.35rem 0 0;padding-left:1.1rem;color:var(--muted)}
.questions .opts li{margin:.1rem 0;padding:0;border:0;background:none}
.qid{font-family:"IBM Plex Mono",monospace;color:var(--ember);font-size:.85rem;margin-right:.4rem}
.default{display:inline-block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--spruce);border:1px solid var(--spruce);border-radius:99px;padding:0 .45rem;margin-left:.4rem;vertical-align:middle}
blockquote{margin:.6rem 0;padding:.2rem 0 .2rem 1rem;border-left:3px solid var(--rule);color:var(--ink)}
.tablewrap{overflow-x:auto;margin:.6rem 0}
table{border-collapse:collapse;font-size:.9rem;width:100%}
th,td{text-align:left;vertical-align:top;padding:.35rem .55rem;border-bottom:1px solid var(--rule)}
th{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.howto{font-size:.88rem;color:var(--muted);margin:.4rem 0 0}
.parked{max-width:68ch;margin-top:2.5rem;padding-top:1.5rem;border-top:2px solid var(--amber)}
.parked h2{font-size:1.3rem}
:focus-visible{outline:2px solid var(--ember);outline-offset:2px}
@media (prefers-reduced-motion: no-preference){.strip a{transition:background .2s}}
"""


def render_questions_from_md(md: str) -> str:
    """Turn a doc's open-questions markdown into numbered Q cards. The docs use either
    '1. **Title**…' lists or '**Q1 — Title**' paragraphs; we keep each question's own text."""
    # Split on top-level numbered items or **Qn** markers.
    chunks = re.split(r"\n(?=(?:\d+\.\s+\*\*|\*\*Q\d+|\*\*\d+\.\s))", "\n" + md.strip())
    chunks = [c.strip() for c in chunks if c.strip()]
    if len(chunks) <= 1:
        return md_to_html(md)
    items = []
    for n, c in enumerate(chunks, 1):
        c = re.sub(r"^\d+\.\s+", "", c)
        c = re.sub(r"^\*\*Q\d+\s*[—–-]\s*", "**", c)
        c = re.sub(r"^\*\*\d+\.\s+", "**", c)
        # mark the recommendation
        c = re.sub(r"\*?\*?(Recommendation|Recommend)\*?\*?\s*:?", r"<span class='default'>default</span> **\1:**", c, count=1)
        items.append(f"<li><span class='qid'>Q{n}</span>{md_to_html(c)}</li>")
    return "<div class='questions'><ol>" + "".join(items) + "</ol></div>"


def render_doc(key: str, block: int, idx: int, total: int, text: str, current: str) -> tuple[str, str, str]:
    sec = split_sections(text)
    status = status_of(text)
    title = title_of(text, key)
    para = sec.get("in one paragraph", "")
    prov = sec.get("provenance", "")
    oq = sec.get("open questions", "")
    log = sec.get("review log", "")
    cls = status + (" current" if key == current else "")
    pill = f"<span class='pill {status}'>{status}</span>"
    if key == current:
        pill += " <span class='pill current'>now</span>"
    body = [
        f"<section class='doc' id='doc-{key}'>",
        f"<div class='eyebrow'><span>Block {block} · {BLOCK_NAMES[block]}</span><span>document {idx} of {total}</span>{pill}</div>",
        f"<h2>{inline(title)}</h2>",
        f"<div class='lead'>{md_to_html(para)}</div>",
        "<h3>Provenance — yours, and the proposals</h3>",
        f"<div class='decisions'>{md_to_html(prov)}</div>",
        "<h3>Open questions — answer by number; “defaults” takes every recommendation</h3>",
        render_questions_from_md(oq),
        "<p class='howto'>For anything that reads alien or thin, say <em>cut</em> or <em>rewrite: what it should be</em>. Decisions land in the review log below and the page is regenerated.</p>",
    ]
    if log.strip():
        body += ["<h3>Review log</h3>", md_to_html(log)]
    body.append("</section>")
    return "\n".join(body), status, title


def render_gdd(block: int, idx: int, total: int, current: str, gdd_text: str) -> tuple[str, str, str]:
    b = GDD_BRIEF
    status = "finalized" if "finalized" in gdd_text[:800].lower() else "draft"
    pill = f"<span class='pill {status}'>{status}</span>" + (" <span class='pill current'>now</span>" if current == "GDD" else "")
    qs = []
    for qid, q, opts, default in b["questions"]:
        badge = "<span class='default'>default</span>"
        opts_html = "".join(
            f"<li>{inline(o)} {badge if o.startswith('(' + default + ')') else ''}</li>" for o in opts)
        qs.append(f"<li><span class='qid'>{qid}</span><span class='q'>{inline(q)}</span><ul class='opts'>{opts_html}</ul></li>")
    body = [
        "<section class='doc' id='doc-GDD'>",
        f"<div class='eyebrow'><span>Block {block} · {BLOCK_NAMES[block]}</span><span>document {idx} of {total}</span>{pill}</div>",
        f"<h2>{inline(b['title'])}</h2>",
        f"<div class='lead'><p>{inline(b['paragraph'])}</p></div>",
        "<h3>Your decisions in it</h3>",
        "<div class='decisions'><ul>" + "".join(f"<li>{inline(d)}</li>" for d in b["decisions"]) + "</ul></div>",
        "<h3>Proposals — keep, cut, or change</h3>",
        "<ul>" + "".join(f"<li>{inline(p)}</li>" for p in b["proposals"]) + "</ul>",
        "<h3>Open questions — answer by number; “defaults” takes every recommendation</h3>",
        "<div class='questions'><ol>" + "".join(qs) + "</ol></div>",
        "</section>",
    ]
    return "\n".join(body), status, b["title"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", default="GDD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--parked", default=None, help="a markdown file with the parked list")
    a = ap.parse_args()

    total = len(ORDER)
    sections, strip, toc = [], [], []
    last_block = None
    gdd_text = (ROOT / "docs/scenarios/whiteout/GDD.md").read_text(encoding="utf-8")
    for idx, (key, block, fname) in enumerate(ORDER, 1):
        if fname is None:
            html_sec, status, title = render_gdd(block, idx, total, a.current, gdd_text)
        else:
            text = (DESIGN / fname).read_text(encoding="utf-8")
            html_sec, status, title = render_doc(key, block, idx, total, text, a.current)
        sections.append(html_sec)
        cur = " current" if key == a.current else ""
        strip.append(f"<a class='{status}{cur}' href='#doc-{key}' title='{html.escape(title)}'>{key}</a>")
        if block != last_block:
            toc.append(f"<li class='blk'>Block {block} · {BLOCK_NAMES[block]}</li>")
            last_block = block
        toc.append(f"<li class='{status}{cur}'><a href='#doc-{key}'><span class='k'>{key}</span><span>{inline(title)}</span></a></li>")
    done = sum(1 for s in strip if "finalized" in s)
    parked_md = pathlib.Path(a.parked).read_text(encoding="utf-8") if a.parked and pathlib.Path(a.parked).exists() else "_Nothing parked._"

    page = f"""<title>Whiteout Design Review</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
<aside class="rail">
  <div class="brand">Whiteout — the design review</div>
  <div class="sub">{done} of {total} finalized · one document at a time, in this order</div>
  <div class="strip">{''.join(strip)}</div>
  <ul class="toc">{''.join(toc)}</ul>
</aside>
<main>
  <div class="procedure"><strong>How this works.</strong> Each document below has the same five parts. Read the one marked <span class="pill current">now</span>.
    <ol>
      <li>The paragraph — what the player experiences.</li>
      <li>Provenance — your decisions, quoted; then the proposals (P…) to keep, cut or change.</li>
      <li>The open questions (Q…), each with options and a <span class="default">default</span>.</li>
      <li>Answer in the terminal by number, or “defaults”. Say <em>cut</em> or <em>rewrite:</em> for anything alien.</li>
      <li>I rewrite the document, log the decisions, flip its status, and this page updates. Anything needing more thought is parked with an owner — the list is at the bottom.</li>
    </ol>
  </div>
  {''.join(sections)}
  <section class="parked" id="parked"><h2>Parked — owned, not forgotten</h2>{md_to_html(parked_md)}</section>
</main>
</div>
"""
    pathlib.Path(a.out).write_text(page, encoding="utf-8")
    print(f"wrote {a.out} ({len(page)//1024} KB); finalized {done}/{total}; current {a.current}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
