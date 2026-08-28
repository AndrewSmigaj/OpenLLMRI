# Tank D3/D4 — First Designed-Corpus Results (2026-08-28, exploratory)

**Data:** 36 runs (12 scene-pair families × 2 directions + 12 no-shift arms), 40 cumulative
steps each, scene-context (word "tank" absent from all context), Q1 carrier re-appended per
step. All runs passed row-count assertions. Axis: Q1 calibration from `session_29a80932`
(300/label, ±1 = single-sentence endpoint means). Scripts committed
(`tank_d3_trajectories.py`; metrics CSV + curves saved).

## Instrument validity
- Step 1 readings ≈ ±1.0 — the calibration convention recovers exactly on fresh single-scene
  contexts. Internal consistency check passed.
- **Methods caution (found here):** projecting pos-8 states onto the pos-1 axis collapses all
  conditions to a constant — position identity swamps the sense direction. Anchor-site analyses
  MUST use same-site calibration. (D1b's per-token span provides every site's axis.)

## Findings (L4 tank-site unless noted; aq = −1, vh = +1)

1. **Long single-regime contexts are stable, not messy.** D4 arms plateau at ±2.0 by step 10
   and hold with tight σ through step 40. The length-matched control does its job: whatever
   happens at transitions is about the *shift*, not context length.
2. **Accumulation drives readings past the single-sentence endpoints** (±1 → ±2 plateau) in
   scene-context with zero occurrences of "tank" — resolving the prior-design open question:
   the overshoot is context accumulation, **not** lexical repetition.
3. **Transitions are slow and incomplete — the central phenomenon, now in designed data.**
   After the shift: 7–10 steps to first cross zero; ~7–9 steps dwelling in |x|<0.5; and at
   +20 sentences the reading reaches only +0.11 (aq→vh) / −0.87 (vh→aq) — versus ±2.0 when
   the SAME quantity of evidence starts from scratch (D4). Twenty sentences of scene evidence
   build a ±2 reading on empty context but recover only ~5–45% of that after a prior sense.
   History suppresses the new reading by a factor of roughly 2–20×, direction-dependent.
   Curves are still rising at step 40 — not settled; longer windows needed for asymptotes.
4. **Direction asymmetry:** vh→aq crosses faster (7.2 vs 10.0 steps) and gets further
   (residual 0.56 vs 0.96). Stronger at L23, where aq→vh has not even crossed zero on average
   by step 40 (−0.83). Candidate input to the inversion hypothesis; also note the D4
   asymmetry (aquarium arms deepen more than vehicle arms at L23 and pre-lexically).
5. **Depth:** L23 transitions lag L4 — later layers hold the old reading longer. First
   depth-propagation hint (Tier 2 heatmap will map it properly).
6. **Pre-lexical expectation shifts too** (pos-8-calibrated axis): the ` word`-site reading
   moves from the old sense toward the new one across the post-shift window while D4 stays
   flat — sense expectation before the word appears is itself history-laden, with the same
   slow-release signature.

## Status vs claim ledger (exploratory, tank arm)
- "Purity holds through growth until the shift": now signed by the raw axis (D4 + pre-shift).
- "Post-shift volatility / incomplete consolidation": signed, designed corpus, both directions.
- "History dependence": the D4-vs-post-shift gap is a direct history effect; the formal
  D6/D7 designs will quantify it as hysteresis.
- Three-worlds verdict: NOT yet — needs the checkpoint distribution pass (next capture step).

## Next
Checkpoint pass over these 36 runs (4 windowed full-position requests/run) → time-stratified
dip/trimodality tests; D2 calibration axes (capturing now) → suicide D3 assembly.
