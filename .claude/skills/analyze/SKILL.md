---
name: analyze
description: Analyse a lens with checked reports — read a card's evidence packet, write the card here and submit it through the number checker, or have the backend's analysts write cards in the background
---

# Lens analysis

Reports on a lens are **cards** (DESIGN.md E8). A card is about one thing in a lens: the lens
itself, its k profile, its pipes and hubs, a cluster node, an expert, a route, an expert route or a
split point. It is written from that thing's **evidence packet**: numbered facts (the only numbers
a card may cite), plus example sentences, tokens and notes.

The lens report has three sections beside its summary (DESIGN.md C7): **clusters** (where and how
the nodes separate the designed values), **experts** (which differ by designed value, and how
well) and **pipelines and hubs** (which groups of items keep which experts, and whether any stand
apart from all items' shares). A pipeline (P1, P2, ...) is a chain of experts across consecutive
layers that a group of items keeps among its four; a hub (H1, ...) is an expert whose items arrive
from different experts at the layer before. A pipeline every value takes in about its usual share
is a trunk, not a pattern: with one target word, routing is close to the same for every item.

A checker re-computes every number. Each numeral must be followed, in its sentence, by the id of
the fact it comes from (`89 items [F1]`, `84% [F4]`, `0.33–0.79 [F4, F5]`), and must equal that
fact at the precision written; a share may be written as a percentage.

Two ways to write cards:
- **In the background** (OP-2), by `claude -p` analysts on the Claude subscription. A card whose
  numbers don't trace is retried once, then kept and flagged. The lens report is two independent
  drafts, reconciled.
- **Here in Claude Code** (OP-3, OP-4): read the packet, write the card, submit it. The backend
  keeps it only when every number traces; otherwise it answers 422 with the failures to fix.

Analysts are tested before they are trusted (OP-5): cards by an analyst without a passing test
for its model and prompt version are marked untested.

Cards are for lenses (built with `/cluster`). Legacy schemas keep their old reports and
descriptions, which the app still shows.

## Card ids

| Id | The card is about |
|---|---|
| `lens` | the lens across its layers: the lens report |
| `k` | the k profile: which k to cut at each layer (the lens must be validated) |
| `routes` | the pipes and hubs: the lens's expert pipelines, its hubs and the experts involved in each designed value (`/cluster` OP-L9 works them out; every build does) |
| `L12C0` | cluster node 0 at layer 12 |
| `L12E5r1` | expert 5 at layer 12, at rank 1 |
| `L12C0-L13C2` | the route from L12C0 to L13C2 |
| `L12E5-L13E7r1` | the expert route from L12E5 to L13E7, at rank 1 |
| `split-L12C1` | the split point: where L12C1's items part ways at the next layer |

All operations read the lens's current version unless `version` is given. "P2", "pipeline 3",
"hub 2" and "top-1" are references, not numbers: they need no citation.

A save writes, within 28 calls: the lens report, the k advisor (once validated), the pipes and
hubs, the biggest split points, then the nodes at the best layer.

## Before writing: the probe guide

The capture's sentence set has a guide saying what it tests and what to look for. Read it first:

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s http://localhost:8000/api/probes/SESSION_ID | $PY -c "import json,sys; print(json.load(sys.stdin).get('sentence_set_name'))"
```

Then `Glob data/sentence_sets/**/<name>.md` and read it.

## Operations

### OP-1: List a lens's cards

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/cards" | $PY -m json.tool
```

One card in full, with the facts it cites, whether its analyst is tested, and whether its
evidence has changed since it was written (`stale`):

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/cards/CARD_ID" | $PY -m json.tool
```

### OP-2: Write cards in the background

`cards` lists card ids; leave it empty for a save's plan (the lens report, the k advisor, the
five biggest split points, then the nodes at the best layer). `budget` caps the calls: a card
takes one or two, the lens report three to six. Saving a version runs the plan with a budget of
25 on its own.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/analysis" -H "Content-Type: application/json" -d '{"cards": ["L12C0", "split-L12C1"], "budget": 6, "created_by": "claude-code"}' | $PY -m json.tool
```

Follow the job with `curl -s http://localhost:8000/api/jobs/JOB_ID`; its result lists the cards
written, failed and skipped.

### OP-3: Read a card's packet

The same evidence the background analysts read: `text` is the packet as they see it.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/packets/CARD_ID" | $PY -c "import json,sys; print(json.load(sys.stdin)['text'])"
```

### OP-4: Submit a card written here

Write the card from the packet alone, by the analysts' rules:
- say only what the evidence shows;
- every number copied from a fact (rounding is fine) and cited right after it, in its sentence;
  no computed numbers (sums, differences, ratios);
- layers, nodes and experts by their ids (L12, L12C0, L12E5), never as bare numbers; no dates;
- quoted sentences and tokens inside double quotes;
- `pattern`: `clear` for a specific pattern, `weak` for a tendency, `none` for a mix. A card that
  reports nothing is the right card when there is nothing;
- `title`: at most eight words, no numbers; `summary`: two or three sentences; `points`: up to
  five; `caveats`: up to three.

Save the card as JSON in the scratchpad, e.g. `card.json`:

```json
{"output": {"title": "...", "pattern": "clear", "summary": "...", "points": ["..."], "caveats": []},
 "model": "Claude Code"}
```

Then submit it:

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/cards/CARD_ID" -H "Content-Type: application/json" -d @CARD_FILE | $PY -m json.tool
```

A 422 lists each failure: the numeral, its context and the reason (no citation, an unknown fact,
or the value it doesn't match). Fix those sentences and submit again. A stored card shows in the
app as written in Claude Code.

### OP-5: Test the analysts

Before trusting the background analysts, and again whenever their prompts or model change. At one
layer of a lens (its best by default), about 20 calls:
- decoys: random populations and the lens with its labels shuffled; a sound analyst calls none
  of them a clear pattern;
- planted findings: populations built around one label value; a sound analyst names it;
- predictive descriptions: from a node's card, a second call picks the node's members out of
  held-out sentences (half are members), scored beside a majority-label baseline.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST http://localhost:8000/api/analysts/tests -H "Content-Type: application/json" -d '{"session_id": "SESSION_ID", "name": "LENS", "created_by": "claude-code"}' | $PY -m json.tool
```

The latest run, and which model and prompt versions have passed:

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s http://localhost:8000/api/analysts/tests | $PY -m json.tool
```

### OP-6: Ask about a card's subject

An analyst answers from the card's packet, in the background; the answer's numbers are checked.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s -X POST "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/ask" -H "Content-Type: application/json" -d '{"card_id": "L12C0", "question": "Which register leans into this node?"}' | $PY -m json.tool
```

The answers, newest first:

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && curl -s "http://localhost:8000/api/sessions/SESSION_ID/lenses/LENS/questions?card_id=L12C0" | $PY -m json.tool
```

## Key principles

- **The packet is the evidence.** A claim the packet can't support stays out of the card, however
  plausible.
- **A node is a group the lens made at one layer**, measured against designed labels; say which
  instrument a claim rests on (the UMAP lens's nodes, raw space, the routing).
- **Nothing to report is a finding.** Decoys exist because analysts find patterns in noise.
- **Cards are LLM-written.** A finding still goes through the paradigm's review (DESIGN.md H).
