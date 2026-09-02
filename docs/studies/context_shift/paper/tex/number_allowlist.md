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
