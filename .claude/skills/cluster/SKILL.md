---
name: cluster
description: Build lenses (background jobs, k per layer, a new k without a refit, validation, node details, mass-mean axes, save) and look after legacy clustering schemas
---

# Lenses

A lens groups a capture's items at one site (a token position in the residual stream), layer by
layer (DESIGN.md C). Every layer is fitted once (6-D UMAP, then a Ward tree), k can differ per
layer and can change later without a refit, and the build runs as a background job. A lens lives
in `data/lake/<session>/lenses/<name>/`; saving a version copies its records and its atlas
entries (`nodes.json`) into `data/lenses/<session>/<name>/` in the repo, and queues its reports
(`/analyze`).

**Legacy schemas** (`data/lake/<session>/clusterings/<name>/`), built before lenses, stay
readable: in the app, and through the lens API with `?legacy=true`. They are no longer built; the
schema build route retired with lens slice 1.

All commands resolve `$ROOT` and `$PY` first:

```bash
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
```

## Defaults (the one place to change them)

The `/probe` and `/agent` post-run steps read these when they propose a lens.

```yaml
lens_defaults:
  source:         residual_stream
  token_position: 1
  dimensions:     6            # UMAP dimensions
  n_neighbors:    15           # UMAP neighbours
  k:              6            # per layer; or k_per_layer, or k_auto (elbow, silhouette, levels)

filter_defaults:
  last_occurrence_only: true
  max_items:            null   # a lens holds up to 4,095 items; a larger capture is subsampled by class

session_kind:
  probe: { steps: null }       # sentence sets: token rows have no step, so leave the filter out ([0] finds nothing)
  agent: { steps: [1] }        # agent runs: the post-examine tick (turn 1 by convention)

lens_name_convention:
  # lowercase letters, digits, _ and -, up to 64; for example
  #   <study-and-axes>-k<k>-n<n>[-<sweep suffix>]   e.g. tank-k5-n15, bus-stop-k6-n15-step01
```

## Operations
### OP-L1: Build a lens (returns a job at once)

Defaults follow every kept schema: residual stream, 6-D UMAP, Ward, last occurrence.
Replace `SID`, `NAME` (lowercase, digits, `_`, `-`) and the k you want.

```bash
curl -s -X POST http://localhost:8000/api/lenses -H "Content-Type: application/json" \
  -d '{"session_id":"SID","name":"NAME","n_neighbors":15,"dimensions":6,"k":6,"created_by":"claude-code"}'
```

Other ways to set k: `"k_per_layer":[...24 values...]`, or `"k_auto":"elbow"`, `"silhouette"`
or `"levels"` (the suggestion each method makes per layer, named in the version).

### OP-L2: Follow the job

```bash
curl -s http://localhost:8000/api/jobs/JOB_ID
```

`state` goes queued, running (with `progress`), done. A failure carries `error` and `log_tail`.
A 24-layer lens takes about a minute.

### OP-L3: List, open, choose a new k, save

```bash
curl -s http://localhost:8000/api/sessions/SID/lenses
curl -s "http://localhost:8000/api/sessions/SID/lenses/NAME/flows"
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/versions \
  -H "Content-Type: application/json" -d '{"k":5}'
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/save \
  -H "Content-Type: application/json" -d '{"version":"v2","keywords":["tank"]}'
```

A legacy schema opens through the same endpoints with `?legacy=true`. Saving freezes a
version and copies its records into `data/lenses/<session>/<name>/` in the repo.

### OP-L4: Validate a lens (held-out scores and the k profile; a job)

Folds hold out whole scene families when the items name one (`categories.scene`); otherwise
they are stratified with identical texts kept together, and marked weaker. Every k from 2 to
10 is scored at every layer. A 24-layer lens takes a few minutes.

```bash
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/validate \
  -H "Content-Type: application/json" -d '{"created_by":"claude-code"}'
curl -s http://localhost:8000/api/sessions/SID/lenses/NAME/validation
```

Once validated, `"k_auto":"heldout"` (OP-L3's versions call) takes each layer's k with the best
held-out AMI (the nodes that best match the classes; held-out accuracy keeps rising with k); it
is selection-biased, and the version says so. For an unbiased choice, tune the lens (OP-L7). Every build also records a self-check
(planted classes found, nothing found in noise) in the lens list. A validation also scores raw
space on the same folds and k (PCA-50 Ward and spectral, relevant neurons, the logistic
ceiling: `comparison` in the result), and `.../marks` then lists the items where the lens and
raw space group differently.

### OP-L5: A mass-mean lens (one contrast, A at -1 and B at +1; a job)

Validated on held-out scene families as it is built (the paper's algorithm). Its readings work
on any capture at its site.

```bash
curl -s -X POST http://localhost:8000/api/lenses/mass-mean -H "Content-Type: application/json" \
  -d '{"session_id":"SID","name":"NAME","label_a":"A","label_b":"B","token_position":1,"created_by":"claude-code"}'
curl -s "http://localhost:8000/api/sessions/SID/lenses/NAME/readings?target=OTHER_SID"
```

### OP-L6: Work out node details (a job)

For every node of the current version: the neurons whose values track membership, the logit lens
(the tokens the node's centre favours, and those it favours more than the layer's average item),
the surface check, and how much of the next layer's routing the nodes explain. For a mass-mean
lens: the axis against each next layer's router (against 1,000 random directions) and the tokens
each class's mean favours. Read on the CPU from the model's files, in about ten seconds a lens.

```bash
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/details \
  -H "Content-Type: application/json" -d '{"created_by":"claude-code"}'
curl -s http://localhost:8000/api/sessions/SID/lenses/NAME/details
```

The details join the node cards, the reports' evidence and the atlas entries.

### OP-L7: Tune a lens (settings and k per layer, honestly scored; a job)

A search over UMAP's settings and k at every layer, chosen by held-out AMI on selection folds and
scored on a test portion the search never sees (whole families per label when the items name
them, else a stratified share, marked weaker). Settings that fail the self-check drop out. The
job then builds the tuned lens (`NAME-tuned` unless `name` is given) with each layer's winning
settings and k as v1, and validates it. The default grid is 9 settings (n_neighbors 5, 15, 50 ×
dimensions 3, 6, 12): about 8 minutes for 500 items, 17 for 1,000. The CPU lane runs one job at a
time, so builds queue behind it.

```bash
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/tune \
  -H "Content-Type: application/json" -d '{"target_axis":"label","family_field":"scene","created_by":"claude-code"}'
curl -s http://localhost:8000/api/sessions/SID/lenses/NAME-tuned/search
```

`search.json` holds every candidate's selection scores, each layer's winner and runners-up, the
test scores of the winner and of the lens it started from, and the raw groupings and ceiling on
the test portion. Quote the test scores: the tuned lens's own validation reuses items that chose
its settings. Advanced fields: `grid` (`n_neighbors`, `dimensions`, `min_dist` lists, at most 60
settings), `k_min`/`k_max`, `test_share`, `n_folds`, `seed`, `name`.

### OP-L8: Read a capture through a lens (a job)

Places each item of a capture in a saved UMAP lens's space at every layer, with its 15 nearest
lens items; its node is their vote, worked out when the reading is served, so a new version (k)
re-votes without reading again. The lens's own items keep their nodes. The usual use is a step the
lens wasn't built on: a lens on friend/foe tick 1 reading tick 0 (`"filters":{"steps":[0]}`, the
lens's own capture by default); `target` reads another capture at the lens's site. A reading also
says how far out its items sit: in the residual stream, each item's distance to its nearest lens
items as a percentile of the lens's own, with a warning when a layer's median passes the 75th
(the lens reading outside the context it was built from). About 40 seconds for 500 items.

```bash
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/readings \
  -H "Content-Type: application/json" -d '{"filters":{"steps":[0]},"created_by":"claude-code"}'
curl -s "http://localhost:8000/api/sessions/SID/lenses/NAME/readings?key=KEY&rank=1"
```

The POST returns the reading's `key` (for example `b629b6c5-steps-0`); the lens list names every
reading under `readings`. The GET gives each item's node per layer with the winner's share of the
vote (null for the lens's own items), its percentile per layer, and its expert at `rank`. In the
app, Layers' tick control offers the reading for a step the lens doesn't cover.

### OP-L9: Pipes and hubs (a job; every build also does it)

A lens's expert pipelines, its hubs and the experts involved in each designed value, from all four
of each item's experts and their gate weights (DESIGN.md C7). A pipeline follows the bundle: from
every (layer, expert) that 5% of the items (10 at least) have among their four, toward the expert
the members weight most at each next layer, kept at three layers or more; it says whether it is
found again in both halves of the folds. A hub is an expert whose items arrive from two experts or
more, counted between items. The experts involved differ by mean weight beyond a permutation
threshold (whole families move together when each holds one value). Seconds. Lenses built before
routes existed need the POST once; legacy schemas' are worked out when asked.

```bash
curl -s -X POST http://localhost:8000/api/sessions/SID/lenses/NAME/routes \
  -H "Content-Type: application/json" -d '{"created_by":"claude-code"}'
curl -s "http://localhost:8000/api/sessions/SID/lenses/NAME/routes"
```

In the app: the Pipes and hubs tab, the pipeline chips in the expert chart's header (a pipeline
lights its chain and its members), the expert chart's "all" rank (every expert sized by the
weight its items give it), and the fingerprint's "the rest (by class)".

### Reports

LLM-written cards on the lens, its k profile, nodes, experts, routes and split points, every
number checked: `/analyze`. Saving a version writes its first reports on its own.

## Legacy schemas

### OP-S1: List a session's schemas

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && \
curl -s http://localhost:8000/api/probes/sessions/SESSION_ID/clusterings | $PY -m json.tool
```

### OP-S2: Archive a schema

Moves it to `clusterings/_archive/<name>_<time>/`: gone from the lists, and back with a `mv`.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && \
curl -s -X POST http://localhost:8000/api/probes/sessions/SESSION_ID/clusterings/SCHEMA_NAME/archive | $PY -m json.tool
```

### OP-S3: Delete a schema

Permanent. Refused (409, `schema_has_invested_data`) while it holds reports or written
descriptions; `?force=true` overrides, only when nothing of value lives in it. Lake data is never
deleted without Andrew's OK.

```bash
ROOT=$(git rev-parse --show-toplevel) && PY="$ROOT/.venv/bin/python" && \
curl -s -X DELETE "http://localhost:8000/api/probes/sessions/SESSION_ID/clusterings/SCHEMA_NAME" | $PY -m json.tool
```

## Troubleshooting

- **409 on a build:** a lens of that name exists in the session, or is being built (the reply
  names the job). Pick another name.
- **400 on a build:** the name breaks the rule above, or a setting is out of range (the reply says
  which).
- **A job failed:** `GET /api/jobs/JOB_ID` carries `error` and the log's tail (`log_tail`). Jobs run
  in their own processes and outlive a backend restart.
- **No validation, marks or k advisor:** they need OP-L4 first.
- **Legacy schema 404:** OP-S1 lists what exists; archived schemas are left out.

## Important rules

- **Build lenses, not schemas.** A lens build is a job: the reply comes at once, OP-L2 follows it.
- **Versions are cut, not refitted:** a new k is a new draft version of the same fit (OP-L3).
- **Saving freezes a version** and writes its records and atlas entries into the repo, then
  queues its reports (25 calls on the Claude subscription by default; `"analysis_budget": 0`
  for none).
- **Never delete lake data without Andrew's OK**, a legacy schema included.
