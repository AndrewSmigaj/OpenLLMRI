---
name: pipeline
description: Check analysis pipeline state for an experiment and suggest next step
---

# Pipeline State Check

Read `docs/PIPELINE.md` for the full pipeline reference.

## Step 1: Identify the Experiment

Ask the user which experiment to check, or list all available sessions:

```
GET /api/probes
```

Match by `sentence_set_name` field in session metadata (or `session_name` / `target_word` as fallback).

If multiple sessions match, present the list with dates and ask the user to pick one.

## Step 2: Find the Probe Guide

From the session's `sentence_set_name`, find the probe guide:

```
glob data/sentence_sets/**/{sentence_set_name}.md
```

Read it — it contains classification rules and analysis focus for this experiment.

## Step 3: Determine Pipeline Stage

Run these checks in order:

1. **No session found** → Stage 1 (design experiment with `/probe`)
2. **Session state != 'completed'** → Stage 2 (capture in progress or failed)
3. **`GET /api/probes/sessions/{id}/generated-outputs`** — check `output_category` field:
   - If null/empty on most probes → Stage 3 (categorize outputs with `/categorize`)
4. **`GET /api/sessions/{id}/lenses`** — the session's lenses (legacy schemas show with `legacy: true`):
   - No lens → USER GATE, then Stage 4 (build one: `/cluster` OP-L1, or the app's Build page)
5. **For each lens** — its `validation`, its `state`, and `GET /api/sessions/{id}/lenses/{lens}/cards`:
   - Not validated → Stage 5 (validate and work out details: `/cluster` OP-L4, OP-L6)
   - No cards → Stage 6 (reports: `/analyze`)
   - Cards exist → Stage 7 (present them)

## Step 4: Report & Suggest

Tell the user:
- Which experiment and session you found
- Current pipeline stage
- What the next action is
- Ask if they want to proceed

If user confirms, execute the next stage following docs/PIPELINE.md instructions.
