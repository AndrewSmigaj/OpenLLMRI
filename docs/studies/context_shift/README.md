# Context-shift study

Source, data, and paper for **"Unresolved: Semantic Metastability in a Language
Model Under Context Shift"** (Andrew Smigaj, 2026). The paper asks how a language
model's internal reading of a token moves when accumulating context changes what
the token means, and what the model does while that reading is unresolved.

> **Content note.** This study analyzes model behavior around suicide-related
> requests in a research context, and the behavior tables in this directory
> contain model output about such a request. If you or someone you know is
> struggling, help is available: in the US, call or text 988; elsewhere,
> findahelpline.com.

The built paper is `paper/tex/main.pdf`. Its source is the markdown under
`paper/draft/`, converted by `paper/tex/build.py`.

## What is here

| Path | Contents |
|---|---|
| `captures/` | The capture chains that produced every session (shell and Python scripts), their logs, and `capture_manifest.csv`, one row per archived file with size and SHA-256. |
| `analysis/` | Every analysis and figure script, the calibration axes (`axes/`), the projected-reading caches (`r3_projcache_*.npz`), model-selection and crossing-time tables, the behavior worksheets and their categorized versions, and the figures (`figures/`, with supplementary figures in `figures/other/`). |
| `findings/` | The frozen findings record (`FINDINGS_FINAL.md`), its predecessor (`FINDINGS_AND_ANALYSIS_v2.md`), the QA report, and the corrections log inside the findings record. |
| `generation/` | The blind sentence-generation batches and their audits. |
| `specs/` | The scene-family and sub-arm specifications the corpora were written to. |
| `paper/` | `draft/` (current source), `draft_v1/` and `draft_v2/` (frozen earlier versions), `tex/` (build, converter, checks, bibliography), `WRITING_STANDARD.md`. |
| `../../../data/sentence_sets/` | The context sentences, calibration items, minimal pairs, and mixture-sweep cells, as sentence-set JSON files (repository root). |
| `../../../data/lake/` | The raw captures. **Not in the repository**; see below. |

The platform that ran the captures (backend, adapters, capture routes) is the rest
of this repository; `docs/SOFTWARE_OVERVIEW.md` describes it.

## The raw captures

Every reading in the paper was computed from residual-stream captures of
gpt-oss-20b: 1,299 sessions, 7,794 files, 47.9 GB. They are git-ignored. They are
archived by the author and available to researchers on request, and a public
deposit is planned. `captures/capture_manifest.csv` lists every archived file with
its session id, sentence-set name, corpus label (the row of the paper's Table 1 it
belongs to), capture date, size, and SHA-256, so an archive copy can be verified
against this repository. `analysis/s17_capture_manifest.py` regenerates it.

Three facts about the captures that a reader should not discover by surprise:

- **Regeneration reproduces the paper; re-capture does not reproduce the
  activations bit for bit.** The model's chat template stamps the current date
  into its system message, so an input captured on another day differs by one or
  two tokens at fixed positions. Within a run the date is constant, because a run
  is one forward chain. The paper states the capture days per corpus (§2.1 and
  Appendix B); `analysis/s16_capture_days.py` prints them from the session
  manifests. Re-capture requires pinning the template's date; the effect of the
  date tokens has not been bounded empirically.
- **Precision.** The model ran as distributed: expert weights in MXFP4, all other
  weights in float16 (see `backend/src/adapters/gptoss_adapter.py`). The captured
  residual streams are stored as float64 in Parquet. Every session manifest
  records the chat-template hash (`prompt_format: harmony@a4c9919cbbd4`); a
  template upgrade changes that hash and invalidates the calibrations.
- **Reasoning effort** was the template default, "medium", for captures and
  completions alike.
- **Behavior completions were regenerated after the freeze.** The frozen behavior
  captures used a 256-token generation cap, which ended inside the model's
  reasoning channel in most outputs. All 312 cells were regenerated on 5–6
  September 2026 with a 2,048-token cap and the template date pinned to each
  cell's original capture day; every regenerated output extends its frozen text
  byte for byte with the reading unchanged (the pipeline is bit-deterministic:
  the same cell captured twice gives identical text and reading). Categories were
  re-read from the delivered answers; outputs that loop to the cap are
  `no_answer`. The frozen worksheets (`r6_behavior_worksheet_*_categorized.csv`)
  and the regenerated ones (`*_v2_categorized.csv`) are both committed, without
  completion text; the comparison is in
  `findings/behavior_regeneration_2026-09.md`, and the categorization rules and
  judgment calls in `analysis/behavior_categorization_v2.md`.

## Environment

- Python virtual environment at the repository root (`.venv`, Python 3.10);
  packages pinned in `backend/requirements.txt` (torch 2.9.1, transformers, the
  `kernels` package for the MXFP4 experts, triton). Captures were made on one RTX
  5070 Ti (16 GB).
- Model weights at `data/models/gpt-oss-20b` (Hugging Face `openai/gpt-oss-20b`).
- Captures go through the backend API (`/api/probes/sentence` and the temporal
  route); the `.claude/skills/server` skill starts it. Analysis scripts run from
  the repository root with `.venv/bin/python`.
- Paper build: `tectonic` (`~/.local/bin/tectonic`), plus `pymupdf` and `pypdf`
  in the venv for the checks.

## Regenerating

From the repository root:

```bash
# any analysis or figure script
.venv/bin/python docs/studies/context_shift/analysis/<script>.py

# the paper (markdown -> tex -> pdf), then its checks
cd docs/studies/context_shift/paper/tex
../../../../../.venv/bin/python build.py && tectonic main.tex
../../../../../.venv/bin/python prose_metrics.py --all
../../../../../.venv/bin/python number_check.py all
```

Which scripts need the raw captures:

- **Run from committed caches and tables (no captures needed):**
  `s9_collapse_figure.py` (Figure 1), `r1_figures.py`, `r3_figures.py`,
  `s13_collapse_by_layer.py`, `s14_behavior_by_layer.py`, `r6_behavior_figure.py`,
  `s11_monitor_roc.py`, `s12_r4_counts.py` (v1 mode), `r5_fr_occupancy_bands.py`,
  `r5_letter_battery.py`, `reassessment_checks.py`, and the corpus assembly and
  audit scripts (`assemble_*.py`, `pool_audit.py`).
- **Read raw activations (captures needed):** `scene_heldout_calibration.py`,
  `axis_projection.py`, `second_pass_r1_dynamics.py`,
  `second_pass_r2_occupancy.py`, `second_pass_r3_instruments.py`,
  `second_pass_r4_small.py`, `tank_d3_trajectories.py`, `r2_figures.py`,
  `r5_geometry.py`, `r6_behavior.py`, `r6_carrier_dprime_fr.py`,
  `r6_d6_stickiness.py`, `r6_post_capture.py`, `fr_battery.py`,
  `s7_sanity_checks.py`, `s8_subspace_geometry.py`, `s9_adversarial_checks.py`,
  `s9_figures.py`, `s10_materialized.py`, `s12_r4_counts.py` (v2 mode), `s15_fr_frame_queries.py`, `s18_regeneration_checks.py`, `s19_date_bound.py`,
  `make_figures.py`, `dual_trajectory_figure.py`; `s16_capture_days.py` and
  `s17_capture_manifest.py` read only the session manifests.

The analysis freeze and the additions made after it are recorded in the paper's
Appendix B. Post-freeze scripts are `s11` through `s19`, each a logged addition
computed from the frozen captures, their manifests, or the regenerated behavior
captures (`captures/behavior_chain_v2.py`).

## Claims, scripts, figures

The paper's numbers trace to `findings/FINDINGS_FINAL.md`,
`findings/FINDINGS_AND_ANALYSIS_v2.md`, or `paper/tex/number_allowlist.md`, which
names the script and output behind every number not in the findings record;
`paper/tex/number_check.py` enforces the trace. The map below gives the primary
script for each claim.

| Paper | Claim | Script | Output |
|---|---|---|---|
| §3.1 | Calibration axes separate held-out families (0.905 / 0.910); per-layer refit axes | `scene_heldout_calibration.py`, `second_pass_r3_instruments.py` | `analysis/axes/*.npz` |
| §3.1 | Axis rotation with depth; per-layer heatmaps | `r3_figures.py` | `fig_r3_axis_rotation`, `fig_r3_heatmap_secondary_*` |
| §3.1 | Class signal by carrier token (d′) | `r2_figures.py` (tank), `r6_carrier_dprime_fr.py` | `fig_r2_carrier_dprime`, `fig_r6_carrier_dprime_fr` |
| §3.1 | Minimal pairs track framing cues | `r6_post_capture.py`, `s9_figures.py` | `r6_d5_pairs.csv`, `fig_s9_d5_pairs` |
| §3.2 | Collapse view, both tasks (Figure 1); by layer (Table 3) | `s9_collapse_figure.py`, `s13_collapse_by_layer.py` | `fig_s9_collapse`, `fig_s13_collapse_layers` |
| §3.2 | Crossing medians (Table 2) | `second_pass_r3_instruments.py` | `r3_crossing_times.csv` |
| §3.2 | Remnant gap, decay γ, per-run fits | `second_pass_r1_dynamics.py`, `r1_figures.py` | `r1_model_selection_*.csv`, `fig_r1_residual_gap`, `fig_r1_fit_gallery_tank` |
| §3.2 | Direction asymmetry and replicate carrier | `s9_figures.py` | `fig_s9_asymmetry` |
| §3.3 | Five-model selection and synthetic calibration (Table 4) | `s7_sanity_checks.py`, tallied in `s9_figures.py` | `fig_s9_model_classes` |
| §3.3 | Jump sentences are median-strength; within-stream readings | `s7_sanity_checks.py`, `r2_figures.py`, `s9_figures.py` | `fig_r2_within_stream`, `fig_s9_within_stream_fr` |
| §3.4 | Dwell at the midpoint (mode track) | `r2_figures.py`, `second_pass_r2_occupancy.py` | `fig_r2_mode_track` |
| §3.5 | Behavior by reading band; matched composition | `r6_behavior.py`, `r6_behavior_figure.py`, `s7_sanity_checks.py`, `s9_figures.py` | `r6_behavior_worksheet_*_categorized.csv`, `fig_r6_behavior_bands`, `fig_s9_behavior_matchedk` |
| §3.5 | Zero clarification requests; channel reach; frame queries; regeneration integrity | `s12_r4_counts.py v2`, `s15_fr_frame_queries.py v2`, `s18_regeneration_checks.py` | printed counts |
| §3.5 | Behavior association by layer | `s14_behavior_by_layer.py` | `fig_s14_behavior_by_layer` |
| §3.6 | Hysteresis loops and fitted integrator (Table 5) | `r6_d6_stickiness.py`, `s7_sanity_checks.py` | `fig_r6_d6_loop_*` |
| §3.7 | Per-state geometry; mixed-context marker (Table 6) | `r5_geometry.py`, `s8_subspace_geometry.py`, `s9_figures.py` | `fig_r5_geometry`, `fig_s9_shift_marker` |
| §4 | Standalone monitor ROC | `s11_monitor_roc.py` | `fig_s11_monitor_roc` |
| App. B | Label-shuffle audits (Table 7); capture days; archive manifest; date-effect bound | `s9_adversarial_checks.py`, `s16_capture_days.py`, `s17_capture_manifest.py`, `s19_date_bound.py` | printed; `capture_manifest.csv` |

## Names

The paper renamed some things the repository still calls by their working names.

| Paper | Repository |
|---|---|
| remnant | residual |
| dwelling within the unresolved zone | park |
| accumulation offset | accumulation drift |
| task | probe, probe arm |
| transition, no-shift, minimal-pair, mixture-sweep corpora | D3, D4, D5, D6 |
| tank task, fiction/real task | tank, fr (carriers S1, S2, S3; Q1b is the replicate tank carrier) |

## Behavior data and release policy

The paper's policy (§4): the categorization tables and paraphrased excerpts are
released; raw completions and reasoning traces are available to researchers on
request, since some contain model-generated text engaging with the letter
request. Completions containing such text are withheld from open release.

The committed behavior worksheets (`analysis/r6_behavior_worksheet_*.csv`) carry
the reading, logprob sets, and category for every completion but no completion
text; the full-text versions live with the archived captures. Scripts that scan
the text (`s12_r4_counts.py`, `s15_fr_frame_queries.py`) read it from the archive.

## Corrections and superseded analyses

The paper's Appendix A points here. Values that changed during the study's audits,
each with its date and the script that changed it, are in the corrections log inside
`findings/FINDINGS_FINAL.md`; the paper's revision history is
`paper/draft/REVISION_LOG.md`. The four corrections that changed printed values:

1. The real→fictional remnant gap was first reported with an interval holding the
   no-shift references fixed, [0.11, 0.58]; resampling the six reference runs
   widens it to [−0.12, +0.79], so that remnant is reported as suggestive only.
2. The tank within-stream readings were first reported as untrimmed means, which
   heavy tails inflated; the paper reports trimmed means (+0.34 and +0.37 at ten
   post-shift sentences, +0.52 and +0.53 at twenty).
3. Crossing times were first summarized as a range read from mean trajectories;
   the paper reports per-run medians (10.5 and 6.0 sentences in the tank task, 4.0
   and 5.0 in fiction/real), with mean-trajectory crossings in the Figure 1 caption.
4. The recency integrator's memory was first stated loosely as a range of
   sentences; the paper reports the per-direction median decay values and the
   evidence ages they imply.

A first estimate of stickiness (+3.7, significant) used a null with γ imported from
the transition fits and was retracted the same day; the paper reports only the
fitted-null values. Analyses added after the analysis freeze (`s11`–`s19`) are each
marked as post-freeze in their script docstrings, and the behavior completions of
§3.5 come from the 2,048-token pass that superseded the 256-token pass
(`findings/behavior_regeneration_2026-09.md`).
