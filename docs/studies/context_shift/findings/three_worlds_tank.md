> **Verdict update (2026-08-29, second-pass Item 12):** "no shared third mode" is restated — the population moves as a SINGLE unimodal mode that, in aq→vh, PARKS at mid-axis for ≥10 steps (candidate population-level intermediate; FINDINGS_AND_ANALYSIS_v2 B1). GMM finds no two-population structure in any band. Geometry battery (2026-08-29): park and jump states are ON the trajectory bundle — no off-manifold world at these sites.

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
- Combined with D4: endpoint readings are STABLE under consistent evidence, while transition
  paths move through the in-between continuously at the population level and do not complete
  within 20 sentences. (No dynamical-systems commitment implied — see terminology note below.)

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


---
## REVISION (2026-08-28, adversarial reassessment)

The population-level statistics stand; the world-assignment is SOFTENED.

- Per-run jumpiness check: 8/24 D3 runs have a single post-shift step covering >50% of their
  total travel (mean max-step/travel = 0.46; within-run local sd 0.33, so ~1.0-unit single-step
  moves are ~3σ events, not noise). Run-level dynamics are HETEROGENEOUS: some runs drift, a
  substantial minority jump at dispersed times.
- Between-family sd at matched t (0.60) ≈ 2× within-run sd — the band distributions mix real
  family dispersion, and each band's n=60 carries only ~12 independent runs. Dip power at that
  effective n cannot separate "all runs drift together" from "runs jump at dispersed times."
- Honest verdict, revised: **no evidence of a shared metastable third mode, and no endpoint
  pile-up at matched times** (both firm, and both still exclude the strong metastable-middle
  world at the carrier site). Between "graded drift" and "dispersed-time passage" the
  population test is not decisive; run-level evidence shows a MIX of both. The "traveling
  unimodal packet" description applies to the population mean, not to every run.
- Coheres with the integrator reframe in `tank_d3_first_results.md`: a recency-weighted
  evidence integrator with per-run noise produces exactly this signature.


---
## TERMINOLOGY NOTE (2026-08-28)

Program doctrine (Research Plan v2): attractor-basin language is DROPPED. The framework under
study is metastable states — whether the in-between is a learned, habitable state; a passage;
or an off-manifold artifact — with instruments signing their own claims. Earlier phrasing in
this file ("attractor-like", "hops between basins") slipped back into the legacy paper's
vocabulary and is retracted; "basin" appears in this study's artifacts only inside legacy
schema/session names. The observables here (occupancy distributions, stability under
consistent evidence, integration dynamics) make no commitment to basin geometry. The
off-manifold vs learned-structure question is adjudicated by the ROUTER observable
(entropy/top-1 patterns through transitions), reported separately.
