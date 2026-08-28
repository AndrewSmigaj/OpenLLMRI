# D1b Wave-1 Calibration — Q1 axis, paper-grade (2026-08-28)

**Session:** `session_29a80932` (`tank_q1_calibration_v1`) — 300 aquarium + 300 vehicle cells,
each ONE blind-pool scene sentence + Q1 carrier. Harmony (`harmony@a4c9919cbbd4`), 24 layers,
positions 1-10 (full carrier span). Row-count assertions exact (144,000 rows).
**Scripts:** `axis_projection.py` (random-split), `scene_heldout_calibration.py` (12-fold
leave-one-scene-pair-out). Axes saved: `axes_session_29a80932_aquarium_vs_vehicle_pos1.npz`
— this is the Q1 calibration axis for the program.

## Results (single-sentence context — the hardest cell of the design)

| site | random-split held-out (peak) | scene-held-out mean (peak) | scene-held-out worst fold |
|---|---|---|---|
| ` tank` (pos 1, post-lexical) | 0.930 @ L4 (0.90-0.93 L4-23) | **0.905 @ L4** (0.87-0.90 L4-23) | 0.64-0.78 (always aquascaping/archaeology) |
| ` word` (pos 8, pre-lexical) | — | 0.71 @ L4, 0.61-0.64 later | 0.44-0.54 |

## Reading (exploratory)

1. **Scene-generalization cost is small**: scene-held-out sits only ~2-3 points below
   random-split. The Q1 axis is measuring the sense, not the setting — the "pet store" worry is
   quantified and bounded at ~0.03 accuracy.
2. **The hard scenes are informative**: aquascaping (stones/judging/photography vocabulary,
   few fish words) and archaeology (buried hull + museum-conservation vocabulary) are the
   least prototypical scenes for their senses — genuinely ambiguous single sentences, not a
   generation defect. Logged to the geometry log.
3. **Pre-lexical commitment is dose-dependent**: from ONE context sentence, the ` word`-site
   reading is weakly sense-committed (0.71 peak); from TWENTY sentences (gate preview) it was
   perfectly separated. Evidence accumulates into pre-lexical expectation — a dose-response
   hint directly relevant to the anchor-site story (P5).
4. Depth profile: separability jumps at L2-L4 and plateaus — consistent with every other probe
   family measured so far.
