# Number allowlist for number_check.py

Values that appear in the paper but not in FINDINGS_FINAL.md or
FINDINGS_AND_ANALYSIS_v2.md. Each entry names its source. `number_check.py trace`
reads every numeral in this file as traced, so add an entry only with a source that
can be re-run or opened.

| Value | Where it appears | Source |
|---|---|---|
| 2,880 | model residual width | `data/models/gpt-oss-20b/config.json`, `hidden_size` |
| 2,000 | bootstrap draws | `analysis/r1_figures.py` (range(2000)), `analysis/r6_d6_stickiness.py` (range(2000)) |
| 988 | content note (US crisis line) | constant |
| 96, 31, 52%, 45% | tank completions total; mid-band cells; mid-band commit and "both" rates | `analysis/s12_r4_counts.py` output (post-freeze, logged): "all cells 0/96", "mid-band 0/31", "16 commit (52%), 14 both (45%)" |
| 0.51, 0.45, 0.48, 0.49 | percentile medians, gap material check | `analysis/s7_sanity_checks.py` S1.4 output (logged in REVISION_LOG mechanical sweep) |
| −0.0052, −0.0065 | marker cosine to the class axis | `analysis/s10_materialized.py` docstring ("verified: tank -0.0052, fr -0.0065") |
| +0.57, +0.12, +0.00, −0.10 | tank aquarium→vehicle late-window band means, L0-2 / L3-12 / L13-18 / L19-23 | `analysis/s13_collapse_by_layer.py` output (post-freeze; re-run 2026-09-02) |
| +1.03, +0.30, +0.38, +0.42 | tank vehicle→aquarium band means | same |
| +0.99, +0.41, +0.41, +0.08 | fiction→real band means | same |
| +1.14, +0.32, +0.33, +0.48 | real→fiction band means | same |
| +0.3 to +0.4 | rounded range of the four fiction/real L3-18 band means above | derived from the s13 values |
| 0.4–1.1 | remnant gap range in amplitude units | derived from frozen 1.09 / 0.57 / 0.43 / 0.40 (FINDINGS_FINAL) |
| 0.61 [0.43, 0.76] | monitor ROC AUC | `analysis/s11_monitor_roc.py` output (post-freeze, logged) |
| [1.70, 2.62], [0.77, 1.48], [0.27, 0.50] | reference-resampled 95% CIs for the three remnant gaps that stand (Table 1) | `findings/qa_bughunt_report_2026-08-31.md`, row C5 (correction 15) |
| 8, 3, 2, 23, 4, 7 | real-run model-selection counts beyond the hybrid wins (Table 3) | `analysis/s9_figures.py` lines 56–57 (five-model selector; totals in FINDINGS_FINAL F4) |
| 28, 5, 1, 14; 5, 0, 18, 4, 21; 3, 27, 0, 0, 18 | synthetic-truth confusion counts, 48 runs per truth type (Table 3) | `analysis/s9_figures.py` lines 58–60 (per-task ranges 13–15/24 and 2–3/24 in FINDINGS_FINAL F4) |
| 0.68 | fiction/real axis-rotation cosine at layer 21, the one layer in 10–23 outside the record's 0.57–0.63 | computed from committed axes `analysis/axes/secondary_axis_fr.npz` and the fiction/real calibration axes (cos = 0.681); plotted in fig_r3_axis_rotation; correction candidate 20 pending Andrew's ruling |
| 0.5 | behavior band half-width (middle band = readings within ±0.5 of the midpoint) | `analysis/r6_behavior_figure.py` and `analysis/s12_r4_counts.py` (abs(r) <= 0.5) |
| 189, 44, 85 | completion counts in the per-layer behavior association (fiction/real; tank mid-transition; tank all transition cells) | `analysis/s14_behavior_by_layer.py` legend output (post-freeze, logged) |
| 0.88, 0.73 | layer-0 held-out accuracy of the per-layer accumulated-context axes (tank; fiction/real) | FINDINGS_AND_ANALYSIS_v2 Gen 3 |
| 34, 27, 30 | classifiable synthetic runs (48 minus indeterminate) in Table 4 | arithmetic on the s9_figures.py counts |
| 19 | stepped post-shift sentences per tank run (456 / 24) | `analysis/second_pass_r4_small.py` (consecutive differences over positions 2–20) |
| [−0.20, +0.21], 0.907, 0.530, +1.66, [−1.42, +1.31] | label-shuffle audit values (minimal-pair permutation band; scene-held-out accuracy real vs permuted; remnant gap real vs permutation band) | `findings/qa_bughunt_report_2026-08-31.md`, row C4 |
| 23 | analysis scripts covered by the regeneration diff | `findings/qa_bughunt_report_2026-08-31.md` / Appendix B spec ("23-script diff green") |
| 3, 204 | fiction/real completions categorized "mixed", out of all completions in the behavior worksheet | `analysis/r6_behavior_worksheet_fr_categorized.csv` (category counts) |
| .061, .045 | per-count matched-composition tests at 6 and 12 post-shift sentences (tank) | `analysis/s9_figures.py` panel title (committed) |
| 73%, 89% | marker magnitude retained under held-out direction estimation, per task (13.3/18.1; 154.6/174.5) | `analysis/s9_figures.py` panel-3 constants; range over folds 71–90% in FINDINGS_FINAL |
| 76, 87 | held-out direction estimation per task: tank 71–76%, fiction/real 87–90% | FINDINGS_FINAL (the marker paragraph) |
| 70% | the marker in static mixed contexts as a share of its transition strength in fiction/real (27 / 38) | derived from Table 6 values |
| +3.7 | retracted first stickiness estimate against the imported-γ null (Appendix A) | FINDINGS_FINAL F5 ("a first pass using γ imported from D3 gave +3.7 significant — retracted") |

| 37 of 108; 84 of 204; 120; 21 | completions reaching the final channel per task; fr completions ending in the reasoning channel; fiction-framed completions (all reasoning-only) | `analysis/s15_fr_frame_queries.py` output (post-freeze, 4 Sept 2026) |
| 0 of 84; two; seven | final-channel replies asking whether the request is fictional or real; reasoning channels floating a clarifying question; safety check-ins (manual verdicts in the script) | `analysis/s15_fr_frame_queries.py` output |
| 256 | generation cap in new tokens | `backend/src/api/routers/probes.py` (`max_new_tokens=256`) |
| 4-bit MXFP4; 16-bit | model precision as distributed and as loaded | `data/models/gpt-oss-20b/config.json` (`quant_method: mxfp4`); `backend/src/adapters/gptoss_adapter.py` (`dtype=torch.float16`) |
| 27 August 2026; 28 August; two transition runs and one no-shift run | capture days per corpus | `analysis/s16_capture_days.py` output |
| 12 families × two sub-arms = 24 runs per direction | fr transition-run structure | FINDINGS_AND_ANALYSIS_v2 corpus table (S1: 12 fam × 2 dir × 2 sub-arms); sub-arm near-coincidence: v2 B6 |
| 48 GB; 1,299 sessions | size and count of the study's raw capture sessions (not in git) | session manifests with prompt_format set, summed on disk (4 Sept 2026) |
| 300 | completions in which none asks which reading is meant: 96 tank transition completions (s12) + 204 fiction/real completions (s15) | `analysis/s12_r4_counts.py` and `analysis/s15_fr_frame_queries.py` outputs |
| 72 | transition runs on the main carriers: tank 12 families × 2 directions + fiction/real 12 families × 2 directions × 2 sub-arms (Table 1) | Table 1 sizes; `analysis/s17_capture_manifest.py` corpus counts (24 + 48) |
| 40% to 109% | remnant gap as a share of the no-shift amplitude, range over the four transitions (1.09, 0.57, 0.43, 0.40) | Table 2 last column |
| 312 | all behavior completions examined (108 tank + 204 fiction/real), regenerated corpus | `analysis/r6_behavior_worksheet_{tank,fr}_v2_categorized.csv` row counts |
| 2,048 | regeneration cap in new tokens | `captures/behavior_chain_v2.py` (`--cap 2048`), logs `captures/behavior_*_v2_log.tsv` |
| 256 | frozen generation cap | `backend/src/api/routers/probes.py` before the regeneration (schemas default) |
| 0.02; 0.0024; 0.0182; 24; 23 of 24; 18; three | date-effect bound: max reading shift per task, cells, diverged texts, same-category pairs, loops that became answers | `analysis/s19_date_bound.py` output (5 Sept 2026) |
