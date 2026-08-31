# Clean-Room Data Layout

Raw model-activation captures from gpt-oss-20b (24 transformer layers; residual stream
width 2880; inputs formatted with the model's harmony chat template; deterministic
forward passes). Each session directory under `data/<group>/session_XXXXXXXX/` contains
Parquet files; `data/session_manifest.json` maps each session to its dataset name.

## Files per session

- `residual_streams.parquet` — one row per (probe_id, layer, token_position).
  Columns: `probe_id` (str), `layer` (int 0–23; the residual stream captured at the
  OUTPUT of decoder block N), `token_position` (int; SEMANTIC index — see below),
  `residual_stream` (list<float>, length 2880).
- `tokens.parquet` — one row per probe. Key columns: `probe_id`, `input_text` (full text
  fed to the model), `target_word` (the tracked word), `target_token_id`,
  `target_token_position` (absolute index in the tokenized input), `total_tokens`,
  `label` (class label, see per-dataset notes), `categories_json` (JSON string of
  per-probe metadata), `generated_text` (nullable), `first_token_logprobs_json` (nullable).
- `routing.parquet`, `embeddings.parquet` — per (probe, layer, position) MoE routing
  weights / MLP outputs; not needed for the brief, present for completeness.

## token_position semantics (the measurement-site field)

`token_position` in residual_streams is SEMANTIC, not absolute:
- `1` = the TARGET token (the site row; the tracked word's activation),
- `0` = optional context token (rarely present),
- `2, 3, …` = consecutive tokens of a captured substring span, in order.
The site of measurement for every dataset below is `token_position == 1`.

## Datasets

### tank_d3_ab_runs (12 sessions; 40 probes each)
Cumulative-context runs. Probe i's `input_text` = the first i scene sentences plus a
fixed final question ending in the word "tank". `label` field is not class-bearing here;
`categories_json` has `position` (1–40, the step index; sentence i is the newest).
Target: `tank` (site = token_position 1). Sentences 1–20 come from one scene register,
21–40 from another (see labels in tank_calibration for the two registers).

### tank_d4_arms (12 sessions; 40 probes each)
Same cumulative structure, but all 40 sentences from a single register per session.
Arm register identity: session's set name suffix `_a` or `_b` in
`session_manifest.json` (`_a` and `_b` correspond to the two `label` values used in
tank_calibration). `categories_json.position` = step 1–40. Target: `tank`.

### tank_calibration (1 session; 600 probes)
Single-sentence cells: one scene sentence + the same fixed question. `label` ∈
{`aquarium`, `vehicle`} — the sentence's scene register. Target: `tank`
(token_position 1). `categories_json` may carry scene metadata.

### tank_d6_cells (252 sessions; 1 probe each)
Static 20-sentence compositions + the fixed question. `categories_json` has `family`
(scene family id), `k` (how many of the 20 sentences are from the `_b` register,
0–20), `order` (`B_recent`, `A_recent`, `pure_A`, `pure_B`, or `interleaved` —
the arrangement of the two registers). Target: `tank`.

### fr_calibrations (3 sessions; 600/300/300 probes)
Single-sentence cells: one context sentence + a fixed final sentence. `label` ∈
{`fictional`, `real`} — the context sentence's framing register. Targets differ per
session (each session's `target_word` column states it): `want`, `like`, `letter`
respectively. Site = token_position 1.

### fr_d5_minimal_pairs (1 session; 300 probes)
Paired single-sentence cells: `label` ∈ {`fictional`, `real`}; `categories_json` has
`pair_id` (links the two versions of the same pair) and `domain` (content domain,
6 values). The two members of a pair share most content words and differ in framing.
Target: `want` (token_position 1).

## Notes
- All sessions were captured with the same model, precision, and template; forward
  passes are deterministic (greedy, fixed seed).
- `input_text` is the plain user text; the harmony template wrapping is applied at
  capture time and is identical across all probes.
- Disk layout is flat copies of the original capture directories; no files were
  modified.
