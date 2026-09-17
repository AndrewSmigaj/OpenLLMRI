Related: docs/PIPELINE.md (pipeline stages), docs/ANALYSIS.md (what happens after capture), data/sentence_sets/GUIDE.md (sentence set design)

# Probes — How to Create and Run

Probes are captured model activations for individual sentences. Each probe records expert routing decisions, MLP output embeddings, and residual stream states at every layer for the target word.

## Prerequisites

- Backend server running (use `/server start` or see `.claude/skills/server/SKILL.md`)
- Model loaded (`model_loaded: true` in `/health` response — takes ~2 min on first start)

## Creating Probes from a Sentence Set

### Via API (curl)

```bash
curl -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "tank_polysemy_v2"}'
```

Optional: provide a custom session name:
```bash
curl -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "knife_safety_v2", "session_name": "knife_run_01"}'
```

Generation and capture options (all optional; see `SentenceExperimentRequest` in `backend/src/api/schemas.py`): `generate_output` (default true), `max_new_tokens` (default 256; the context-shift study and the September 2026 README recapture used 2048), `pin_date` (ISO date to pin the chat template's date line), `do_sample` / `temperature` / `top_p` / `seed`. The route applies the harmony chat template to every sentence and runs the whole capture inline, so the server's event loop is blocked until the request returns; fire one capture at a time and wait for `state: completed` in `data/lake/_sessions/<session>.json`. The stored `generated_text` is the full completion: reasoning channel first, then `assistantfinal` and the delivered answer.

This is a Claude-based workflow — there is no probe UI. Claude Code runs captures via the API and manages sessions directly.

## What Happens During Capture

1. Sentence set JSON is loaded from `data/sentence_sets/`
2. A capture session is created (unique session ID generated)
3. For each sentence (A and B groups):
   - Text is tokenized
   - Target word position is found
   - Forward pass runs through the model
   - Hooks capture routing weights, MLP embeddings, and residual streams at every layer
   - Data is written to Parquet files in `data/lake/{session_id}/`
4. Session is finalized — manifest written, hooks cleaned up

## Timing

- **First run**: ~30-60s for model loading, then ~0.5s per sentence
- **Subsequent runs**: ~0.5s per sentence (model stays in memory)
- **200 sentences per class (400 total)**: ~3-4 minutes

## Output Files

Each session creates a directory in `data/lake/{session_id}/` containing:

| File | Contents |
|------|----------|
| `tokens.parquet` | Probe records: probe_id, input_text, target_word, label, label2 |
| `routing.parquet` | Expert routing weights per layer per probe |
| `embeddings.parquet` | MLP output embeddings per layer per probe |
| `residual_streams.parquet` | Residual stream states per layer per probe |
| `capture_manifest.parquet` | Session metadata (model, layers, labels, counts) |

## Verifying a Session

### List all sessions
```bash
curl http://localhost:8000/api/probes
```

### Check session details
```bash
curl http://localhost:8000/api/probes/{session_id}
```

### Verify Parquet files
```python
import pandas as pd
df = pd.read_parquet("data/lake/{session_id}/tokens.parquet")
print(f"Probes: {len(df)}")
print(df[['probe_id', 'target_word', 'label', 'label2']].head())
```

## Available Sentence Sets

| Set Name | Target Word | Primary Axis | Categories | File |
|----------|------------|--------------|------------|------|
| `tank_polysemy_v2` | tank | aquarium vs vehicle | structure | `polysemy/tank_polysemy_v2.json` |
| `tank_polysemy_v3` | tank | aquarium, vehicle, scuba, septic, clothing | structure, register | `polysemy/tank_polysemy_v3.json` |
| `knife_safety_v2` | knife | benign vs harmful | structure, intensity, topic | `safety/knife_safety_v2.json` |
| `gun_safety_v2` | gun | benign vs harmful | structure, intensity, topic | `safety/gun_safety_v2.json` |
| `hammer_safety_v2` | hammer | benign vs harmful | structure, intensity, topic | `safety/hammer_safety_v2.json` |
| `rope_safety_v2` | rope | benign vs harmful | structure, intensity, topic | `safety/rope_safety_v2.json` |
| `said_roleframing_v2` | said | narrative vs factual | speech_type | `role_framing/said_roleframing_v2.json` |
| `said_safety_v2` | said | safe vs unsafe | speech_type | `role_framing/said_safety_v2.json` |
| `attacked_framing_v1` | attacked | roleplay vs factual | voice, scale, specificity | `role_framing/attacked_framing_v1.json` |
| `destroyed_framing_v1` | destroyed | roleplay vs factual | voice, scale, specificity | `role_framing/destroyed_framing_v1.json` |
| `threatened_framing_v1` | threatened | roleplay vs factual | voice, scale, specificity | `role_framing/threatened_framing_v1.json` |
| `tank_polysemy_v3_carrier` | tank | five senses + paper Q1 carrier ("What is the meaning of the word tank?") | structure, register | `polysemy/tank_polysemy_v3_carrier.json` |
| `threatened_framing_v1_carrier` | threatened | roleplay vs factual + frame-question carrier | voice, scale, specificity, … | `role_framing/threatened_framing_v1_carrier.json` |

Carrier sets declare `metadata.set_type = "assembled"` so the loader accepts the second occurrence of the target word and the longer text; capture lands on the carrier's token (last occurrence). Their guides (`*_carrier.md`) hold the delivered-answer classification rules.

Each set has a `categories` dict per sentence and a file-level `axes` array declaring available category dimensions. See `data/sentence_sets/GUIDE.md` for full category details and confound analysis.

## Running All Probes Sequentially

Run one at a time (model is in GPU memory, can't parallelize):

```bash
for set in tank_polysemy_v2 knife_safety_v2 gun_safety_v2 hammer_safety_v2 rope_safety_v2 said_roleframing_v2 said_safety_v2 attacked_framing_v1 destroyed_framing_v1 threatened_framing_v1; do
  echo "Running $set..."
  curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
    -H "Content-Type: application/json" \
    -d "{\"sentence_set_name\": \"$set\"}"
  echo ""
done
```
