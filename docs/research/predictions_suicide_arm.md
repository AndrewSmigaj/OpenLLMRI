# Suicide-Arm (fiction/real) Predictions & Analysis Firewall

**Committed: 2026-08-28.** Status disclosure: **post-capture, post-partial-analysis** — this
file was created AFTER the fr capture campaign (76 runs + 3 calibrations) and AFTER a first
analysis battery had already run. It therefore does NOT establish a clean pre-registration for
the suicide arm. Its purpose is narrower and honest: (1) an exact record of what has already
been seen, (2) procedures and directional expectations committed BEFORE the remaining
analyses, so that the not-yet-computed results retain confirmatory value. Tank is the
exploratory arm throughout; the suicide arm is confirmatory ONLY for the analyses listed in
§3, and exploratory for everything in §2.

Protocol context: second-pass review Items 0 and 9 (2026-08-28); Andrew's ruling: commit
predictions for unseen analyses only.

## 1. Doctrine constraints (standing, restated)
- Raw same-site per-carrier axes measure; UMAP lens discovers. Axis keyed to the run's
  carrier, never shared (cross-token trap, demonstrated twice).
- All absolute-position claims midpoint-referenced (accumulation drift is class-nonspecific).
- Label doctrine: readings are positions along a designed contrast — "real-side" may mean
  "not-fiction"; no meaning attribution without additional contrasts.

## 2. ALREADY SEEN (exact list — nothing here is confirmatory)
From `fr_battery.py`, `make_figures.py`, and their findings docs (all dated 2026-08-28):
1. S1 want-site L14 trajectories, both directions, both sub-arms (theme-only /
   artifact-mentioned), means and per-run curves; no-shift arm trajectories.
2. Integrator-null comparison at the want site (8/8 checked points ahead of null).
3. Pooled occupancy dip tests, both directions (unimodal, p ≈ 0.99–1.00).
4. Jump statistics (19/48 S1 runs jump-dominant).
5. Cross-carrier means on families 0–3: S2 (like-site) and S3 (letter-site) trajectory
   means and correlations with S1 (r = 0.95 S1↔S2; 0.80–0.93 S1↔S3). **This partially
   exposes the letter site and S2/S3 — §3 claims for them are replication-grade, not
   first-look.**
6. All-layers want-site heatmaps: raw, differential, and midpoint-referenced; per-layer
   D4 plateau/midpoint table (fic +0.12 / real +1.89 / mid +1.00 at L14; gap 2.3 mid-stack
   → 1.3 deep).
7. Two retractions + accumulation drift (see fr_battery_first_results.md REVISION v2).
Also seen upstream: S1–S3 calibration accuracies/spreads; scene-held-out CV (0.910 want,
0.877 letter); Q1-gate results.

## 3. NOT YET COMPUTED — procedures + directional expectations
Committed before computation. "Expect" = directional call I am accountable to; "procedure
only" = no call made.

**P1. Letter-site full battery (S1 letter token; partially exposed via §2.5).**
Procedure: same battery as want site, letter-site axis, midpoint-referenced.
Expect: same direction and qualitative shape as want site (no site inversion); class gap
within ±50% of want-site gap at matched layers.

**P2. Occupancy time-bands + rule-(b) band (fr).**
Procedure: position-matched D4-window band (inner-95th percentiles of no-shift arms at
matched positions); band occupancy per post-shift time band. Expect: transition-band
readings traverse the band with mode moving monotonically (midpoint-referenced); unimodal
per band; no persistent shared third mode.

**P3. Within-stream occupancy (fr).** Requires an fr checkpoint capture (not yet run).
Procedure: identical to tank Item-2c instrument (position-matched secondary axis from fr D4
arms). Procedure only — no directional call until the tank version calibrates the instrument.

**P4. Geometry battery (W3: passage vs off-manifold).**
Procedure: distance to class manifolds + to the D3 trajectory bundle, per step, per run.
Expect: majority of mid-transition states are passage-like (near the trajectory bundle,
not off-manifold); jump steps show elevated off-manifold distance relative to smooth steps.

**P5. Safeguard-vs-reading behavior cells (the confirmatory core).**
Procedure: generation-time behavior (refusal/safeguard categories, continuous primary
metric = first-token logprob when capability lands) vs final-position want-site reading;
event floor and tiers per the briefing; scenario-clustered CIs.
Expect: (a) real-side final readings → more safeguard triggering (positive correlation);
(b) runs ending inside the unresolved band → higher behavioral variance than either side
(the metastable-band unexpected-behavior hypothesis); (c) Andrew's hypothesis, attributed:
off-manifold placements trigger safeguards LESS than on-manifold real-side placements.
**Lag-vs-lead is the open question this arm adjudicates**: the motivating story predicted
readings LAG context (stale frame at generation); tank showed recency-lead plus a persistent
residual. Expect fr to replicate lead-plus-residual, with the residual (not a lag) carrying
the safety-relevant effect.

**P6. Full S2/S3 batteries (partially exposed via §2.5).**
Expect: ahead-of-null replicates; S1-correlation r ≥ 0.7 on held-out families (4–11).

**P7. Per-band crossing times by depth (gated on the Item-17 secondary-axis check).**
Pre-stated 2026-08-28, before computation: mid-stack layers L5–9 cross LATER than L10–17
(both probes, midpoint- or secondary-axis-referenced); deep layers (L18–23) intermediate,
not earliest.

Any deviation from these expectations is reported as such, not renegotiated.
