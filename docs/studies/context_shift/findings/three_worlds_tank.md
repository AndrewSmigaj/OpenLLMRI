# Three-Worlds Verdict — Tank Transitions (2026-08-28, exploratory)

**Question (plan Tier 1 item 3):** during a context shift, is the in-between a place (metastable
third mode), a passage (bimodal endpoint pile-up), or a graded state (smear)?
**Population:** post-shift occupancy ONLY (population doctrine). Primary P1 = per-step carrier
readings (` tank` site, same-token, 240/direction across 12 scene families); secondary P2 =
checkpoint window context tokens (~16k states). Time-stratified per the design-review guard.
**Instruments:** Hartigan dip + explicit 1/2/3-component GMM-BIC trimodality check, on the
calibrated Q1 axis. Script committed: `three_worlds_tank.py`.

## Verdict (tank arm, L4 primary, L23 robustness): a TRAVELING UNIMODAL PACKET — the graded
world, sharpened by stratification.

- Every time band, both directions, L4: unimodal (dip p = 0.35–0.97; GMM k=1 in 10/11 cells).
  Pooled across all post-shift time and both directions (n=480): dip p = 0.92, GMM k=1.
- The stratification guard did its job in reverse: pooled unimodality alone could have been
  "smear from mixing times," but the bands show a single coherent packet (sd ≈ 0.55–0.75)
  whose MEAN slides step by step. At any given time-since-shift the runs agree on where the
  reading is; that location moves smoothly through the middle. No endpoint pile-up (contra
  passage), no third mode (contra metastable middle).
- L23 agrees: all bands unimodal (min dip p = 0.11), packet wider (sd ≈ 0.9–1.2) and slower.
- Combined with D4: the picture is stable attractor-like ENDPOINT regions under consistent
  evidence, but transition paths that are continuous drifts — not punctuated hops between
  basins — and that do not complete within 20 sentences.

## P2 (window context tokens): the documented cross-token caveat is confirmed empirically
All post-shift window-token distributions sit at mean ≈ −1.7 regardless of checkpoint,
direction, or window content — token-identity offsets dominate the axis for arbitrary tokens
(the same trap as the cross-position projection). GMM k=2–3 substructure there reflects token
classes, not sense states. P2 is reported for completeness and is NOT evidence about the
three worlds; P1 is the valid population. (Methods note: occupancy tests need same-site
readings; the per-step carrier population provides exactly that.)

## Caveats
- n = 60/band/direction limits dip power for subtle modes; the verdict rests on the CONSISTENT
  unimodality across 8 bands × 2 layers plus GMM preferences, not one test.
- Tank arm only; suicide D3 (capturing now) gets the same analysis, and the plan's inversion
  hypothesis predicts the two probes may differ exactly here.
- L4/L23 shown; full layer scan pending.
