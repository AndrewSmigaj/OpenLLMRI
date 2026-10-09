Related: docs/PIPELINE.md (orchestration context), docs/DESIGN.md (C lenses, E8 LLM analysis), docs/PROBES.md (probe creation), data/sentence_sets/GUIDE.md (sentence set design)

# Analysis Guide — reading lenses and writing checked reports

**Primary workflow:** the `/cluster` skill builds, validates and saves lenses; the `/analyze` skill
writes reports. This document is the reference for the methodology behind them.

## Prerequisites

- A completed probe session (run via `POST /api/probes/sentence-experiment`), its outputs
  categorized when the set has output axes (below).
- A lens on it (`/cluster` OP-L1), validated (OP-L4) before its scores are read as results.

## Pipeline overview

1. **Categorize outputs** — read each generated text, classify it, POST the categories back.
2. **Build a lens** and choose k per layer from the k profile.
3. **Validate it** — held-out scores, the k profile, raw space on the same folds and k.
4. **Work out node details** — neurons, the logit lens, the surface check, routing.
5. **Read it** — the flows, the expert flows, the split points (below).
6. **Write reports** — cards, every number checked against its evidence packet.

## Output categorization

Read generated texts:
```
GET /api/probes/sessions/{session_id}/generated-outputs
```

Returns list of `{probe_id, input_text, label, generated_text, output_category}`.

Read each `generated_text`. Classify along the **output axes** defined in the sentence set JSON (see `output_axes` array in the file). Each set type has different output axes — read them from the JSON, not hardcoded.

For each generated text, choose:
1. **Multi-axis classifications** (`output_category_json`) — classify along EVERY axis in the sentence set's `output_axes` array
2. A **primary output category** (`output_category`) — the cross-cell label from the axes

### Finding classification rules

Classification rules are **per-experiment**, stored in the probe guide alongside the sentence set JSON:
```
# From session metadata, get sentence_set_name
# Find probe guide: data/sentence_sets/**/{sentence_set_name}.md
# Read the "Output Classification Rules" section
```

Do NOT hardcode classification rules here — always read them from the probe guide.

### POST format

```
POST /api/probes/sessions/{session_id}/output-categories
Body: {
  "probe_id_1": {
    "output_category": "category_value",
    "output_category_json": "{\"axis_id\": \"value\"}"
  },
  "probe_id_2": {
    "output_category": "other_value",
    "output_category_json": "{\"axis_id\": \"other_value\"}"
  }
}
```

The `output_category_json` must be a **JSON string** (not a dict) — the backend stores it as a string column in Parquet. The keys must match `output_axes[].id` and values must be from `output_axes[].values`.

Both fields are written to existing columns on ProbeRecord in tokens.parquet. The output category nodes in Sankey diagrams group by `output_category` and use `output_category_json` for color blending.

For multi-axis output designs (e.g., 2×2 factorial), the `output_category` is typically a composite: `{axis1_value}_{axis2_value}` (e.g., `fictional_physical`). For single-axis designs, `output_category` is just the axis value directly (e.g., `aquarium`).

## Reading a lens

**Scores first.** A node is a group the lens made at one layer, measured against the designed
labels; only held-out scores say it generalizes.
- **Held-out κ per layer** at the version's k: where the designed axis separates, and where it
  doesn't. Folds that hold out whole scene families are the real test; stratified folds (sets
  with no scene families) are weaker, and say so.
- **The k profile** (k 2 to 10 at every layer): held-out κ and AMI per axis, silhouette, seed
  agreement. In-sample methods (elbow, silhouette, hierarchy levels) don't use the labels; a k
  chosen by its held-out score is selection-biased.
- **Raw space on the same folds and k** (PCA-50 Ward and spectral, relevant neurons, the logistic
  ceiling): when raw space matches the lens, say so; marked nodes hold items the two group
  differently.

**Then the flows** (Layers):
1. **Purity:** does a node specialize in one label? Above 80% one label is strong specialization;
   50/50 is shared processing (interesting).
2. **Continuity:** do items stay in "the same kind" of node across layers, or diverge?
3. **Split points:** where a node's items part ways at the next layer, and which axis the
   branches follow.
4. **Other axes:** check whether register, structure or a scene axis line up with the nodes in
   their own right.
5. **Experts:** the expert flows at ranks 1 to 4 (the model's own weights) and the fingerprints:
   whether populations take their own experts, and where routing doesn't follow the nodes.

**Node details** (Layers' node card): the neurons that track membership, the tokens the node's
centre favours over the layer's average item, the surface check (a flagged node may be a split by
sentence shape, not by meaning), and how much of the next layer's routing the nodes explain.

## Reports: cards with checked numbers

A **card** is an LLM-written report on one thing in a lens: the lens (the lens report), its k
profile (the k advisor), a node, an expert at a rank, a route, an expert route or a split point.
Card ids and commands: `/analyze`.

- **Evidence packets.** A card is written from its packet alone: numbered facts (the only numbers
  it may cite), example sentences in proportion to their labels, the node's tokens and notes.
  Packets are hashed and kept with the card, so a card names what it was written from, and a card
  whose evidence has changed since shows as out of date.
- **The number checker.** Every numeral must be followed, in its sentence, by the id of the fact it
  comes from, and must equal it at the precision written; a share may be written as a percentage.
  Identifiers (L12, L12C0, rank 2) and quoted sentences are skipped. A card that fails is retried
  once with the failures listed, then kept and flagged; Claude Code's cards are refused until they
  pass.
- **Agreement.** The lens report is two independent drafts, reconciled, with their differences
  listed. Other cards have one analyst and say so.
- **Analyst tests.** Decoys (random populations, the lens with its labels shuffled), planted
  findings, and predictive descriptions scored beside a majority-label baseline. Cards by an
  analyst whose model and prompt version haven't passed are marked untested.
- **Budgets.** A save writes the lens report, the k advisor, the biggest split points and the
  nodes at the best layer within 25 calls on the Claude subscription; everything else is on demand.
- **Where they live:** `data/lake/<sid>/lenses/<lens>/analysis/<version>/` (cards, packets,
  questions); a saved version's node reports also join its atlas entries in `data/lenses/`.

Cards are LLM-written: a finding still goes through the paradigm's review (DESIGN.md H).

## Legacy schemas

Schemas built before lenses keep their window reports and written descriptions, which the app
still shows beside them. New analysis goes into lens cards.
