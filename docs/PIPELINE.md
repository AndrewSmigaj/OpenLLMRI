Related: CLAUDE.md (pipeline skills table), docs/ANALYSIS.md (methodology detail), docs/PROBES.md (probe creation)

# Open LLMRI Analysis Pipeline

This document is the master orchestration runbook for Claude Code. Read it at the start of any analysis session.

## Terminology

- **lens** — a capture's items grouped layer by layer at one site (DESIGN.md C): every layer fitted
  once (6-D UMAP, then a Ward tree), with k per layer. Lives at
  `data/lake/<sid>/lenses/<name>/`; built, validated and saved through `/cluster`.
- **version** — one cut of a lens's trees (a k for each layer). A new k is a new draft version, with
  no refit; saving freezes one and copies its records and atlas entries into `data/lenses/`.
- **node** — a group at one layer (`L12C0`). The Layers view shows every layer's nodes and the
  flows between them, beside the expert flows at ranks 1 to 4.
- **card** — an LLM-written report on the lens, its k profile, a node, an expert, a route or a split
  point, with every number checked against its evidence packet (`/analyze`).
- **legacy schema** — a clustering built before lenses (`data/lake/<sid>/clusterings/<name>/`),
  still readable in the app; no longer built.

## How to Use

1. Read this document to understand the pipeline stages
2. Check pipeline state (below) to determine where we are
3. Execute the next incomplete stage
4. **Stop at USER GATES** — wait for user direction before proceeding

## Checking Pipeline State

Run these checks to determine the current stage for a given experiment:

```
1. GET /api/probes
   → Find session by sentence_set_name or session_name
   → If no session found → Stage 1 (design experiment)

2. Check session state field
   → If not 'completed' → Stage 2 (still capturing)

3. GET /api/probes/sessions/{session_id}/generated-outputs
   → Check output_category field on first few entries
   → If null/empty → Stage 3 (categorize outputs)

4. GET /api/sessions/{session_id}/lenses   (legacy schemas show with legacy: true)
   → No lens → USER GATE, then Stage 4 (build one)

5. For each lens: its `validation`, its `state`, and GET .../cards
   → Not validated → Stage 5 (validate and work out details)
   → No cards → Stage 6 (reports)
   → Cards exist → Stage 7 (present)
```

### Finding the probe guide

From session metadata, read `sentence_set_name`. Then:
```
glob data/sentence_sets/**/{sentence_set_name}.md
```
The probe guide contains experiment-specific classification rules, hypotheses, and analysis focus.

---

## Stage 1: Experiment Design (Interactive)

Use `/probe` skill or freeform conversation. This is the creative phase — user and Claude co-design the experiment.

**Inputs**: User brings a concept to probe (word + semantic question)
**Outputs**:
- Probe guide: `data/sentence_sets/{category}/{name}.md`
- Sentence set: `data/sentence_sets/{category}/{name}.json`

See `data/sentence_sets/GUIDE.md` for quality rules and schema format.

---

## Stage 2: Probe Capture

**Prerequisites**: Backend server running (see SERVERS.md)

```bash
curl -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "EXPERIMENT_NAME"}'
```

Returns `session_id`. Monitor progress:
```bash
curl http://localhost:8000/api/probes/{session_id}/status
```

**Timing**: ~0.5s per sentence. First run adds ~30-60s for model loading.
**Completion**: `state = 'completed'` in status response.

---

## Stage 3: Output Categorization

**Prerequisites**: Session completed with `generate_output=true`

### Step 1: Read generated outputs
```bash
curl http://localhost:8000/api/probes/sessions/{session_id}/generated-outputs
```
Returns list of `{probe_id, input_text, label, generated_text, output_category}`.

### Step 2: Read classification rules
Read the probe guide (`data/sentence_sets/**/{name}.md`) for output axes and classification rules.

### Step 3: Classify each output
For each `generated_text`, determine:
- `output_category`: Primary classification label
- `output_category_json`: JSON string with per-axis classifications

### Step 4: POST categories
```bash
curl -X POST http://localhost:8000/api/probes/sessions/{session_id}/output-categories \
  -H "Content-Type: application/json" \
  -d '{
    "probe_id_1": {
      "output_category": "aquarium",
      "output_category_json": "{\"topic\": \"aquarium\"}"
    },
    "probe_id_2": {
      "output_category": "vehicle",
      "output_category_json": "{\"topic\": \"vehicle\"}"
    }
  }'
```

**Note**: `output_category_json` must be a JSON **string** (not a dict). Keys match `output_axes[].id`, values from `output_axes[].values`.

**Resumability**: If interrupted, re-read generated-outputs and skip probes that already have `output_category` set.

**Completion**: All probes have `output_category` populated.

---

## USER GATE: Building a lens

**Stop here.** Tell the user:

> "Outputs categorized. You can build lenses in the app's Build page (http://localhost:5173/build,
> this capture chosen), or I can build the default one (`/cluster` defaults: k 6, 6-D UMAP,
> 15 neighbours). Which do you want, and with what k?"

Wait for the user's answer.

---

## Stage 4: Build a lens

Build it as a background job and follow it (`/cluster` OP-L1, OP-L2), or let the Build page's form
do it. A 24-layer lens takes about a minute; the app opens it in Layers when it's done. A new k,
for every layer or layer by layer, is a new version of the same fit (OP-L3), not a rebuild.

- **Settings by hand:** minimum distance and the distance metric beside neighbours and dimensions,
  and each layer's own settings under Advanced. Preview a layer first (OP-L11, or "Preview a layer"
  in the form): its clusters in seconds, held out on request; "Rebuild with…" starts a new lens
  from any lens's settings.
- **The hold-out design:** the lens takes the one its set declared (`metadata.holdout`), else whole
  `scene` families, and records it; every later job uses it unless told otherwise.

---

## Stage 5: Validate and work out the details

1. **Validate** (`/cluster` OP-L4, or Validate in Build): held-out scores by the lens's held-out
   families (weaker stratified folds when the set names none), the k profile from 2 to 10 at every layer, and raw
   space on the same folds and k. Read the k profile beside the in-sample suggestions; a
   held-out best k is selection-biased.
2. **Choose k per layer** and cut that version (OP-L3, or "k per layer" in Build).
3. **Or tune the lens** (OP-L7, or "tune" in Build): settings and k searched per layer by held-out
   AMI, then scored on a test portion of whole families the search never saw; the tuned lens is
   built and validated. Quote its test scores. "compare" in Build puts several lenses' held-out
   scores per layer on one chart, with the tuned lens's test line.
4. **Work out node details** (OP-L6): neurons, the logit lens, the surface check, routing. Every
   build also works out its pipelines and hubs (OP-L9; run it again with the set's family field).
5. **Count the axes** (OP-L10, or "axes" in Build) for a set with several designed attributes: how
   many each technique recovers at each layer, against decoys, with the attributes' angles.
6. **Read other captures** through the lens when the question needs it (OP-L8): another step of a
   run, or another set at the same site.
7. **Save the version** to keep (OP-L3, or Save in Build): its records and atlas entries go into
   the repo, and its first reports are written in the background (28 calls on the Claude
   subscription).

---

## Stage 6: Reports

Cards are written by `claude -p` analysts in the background, or here in Claude Code; either way
every number must trace to the card's evidence packet (`/analyze`).

1. **Check the analysts are tested** (`/analyze` OP-5): a card by an analyst whose model and prompt
   version haven't passed is marked untested.
2. **The save plan** (written on save, or `/analyze` OP-2 with no cards named): the lens report (two
   drafts, reconciled, with sections on its clusters, its experts, and its pipelines and hubs), the
   k advisor, the routes card, the biggest split points, then the nodes at the best layer.
3. **Anything else on demand:** a card for a node, an expert, a route or a split point, from the
   app's report panel ("Write report") or `/analyze` OP-2 with its card ids.
4. **Write one here** when it helps: read the packet (OP-3), write the card, submit it through the
   checker (OP-4).

---

## Stage 7: Present

The lens report and the k advisor sit on the lens's card in Build; each node's, expert's and
route's card sits beside the Layers view when it's selected, with the lens report when nothing
is. Over the API: `GET /api/sessions/{session_id}/lenses/{lens}/cards` and `.../cards/{card_id}`.
Present the lens report first, then what the user picks; questions go to the report panel's box
or `/analyze` OP-6.

---

## Time

The basin-era temporal gate and the `/temporal` skill were retired on 2026-10-08. Reading over time is designed in `docs/DESIGN.md` Part D, and arrives with slice 4 (time on sentence runs).

---

## Naming and defaults

Lens names and every build default live in one place: the defaults block of `/cluster`
(`.claude/skills/cluster/SKILL.md`). Lens names use lowercase letters, digits, `_` and `-`, for
example `<study-and-axes>-k<k>-n<n>`.
