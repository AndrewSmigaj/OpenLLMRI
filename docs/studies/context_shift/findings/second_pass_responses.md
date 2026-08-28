# Responses to Second-Pass Review (Items 0–18) — 2026-08-28

Per protocol: answers under each item; disagreements stated with evidence, never silent
compliance; NO findings-doc edits until Andrew reviews these responses, except Items 4/6b
drafted as proposed diffs (§R5 at bottom). All computational checks in this cycle have RUN;
results are inline under each item, with a summary digest at the bottom.

**Global context the review predates:** commit de65de4 (midpoint-referencing / accumulation
drift / two fr retractions) landed before this review arrived but was not visible to it.
Items 11, 16 (direction discrepancy), and 17 (regimes ii/iii) are partially superseded by
that commit; each response below says exactly how, with the evidence.

---

## Item 0 — STOP-FIRST: suicide-arm predictions file
**Complied, with an honest limitation and one premise correction.**
`docs/research/predictions_suicide_arm.md` is committed (2026-08-28), with the disclosure
"post-capture, post-partial-analysis" — stronger than the requested "post-capture,
pre-analysis," because analysis had already partially run (see Item 9). The file firewalls
the NOT-yet-computed analyses (letter-site full battery, occupancy bands, within-stream,
geometry, safeguard-vs-reading, full S2/S3, crossing times) with directional expectations;
already-seen results are enumerated exactly and claim no confirmatory status.
Premise correction: Andrew's in-session ruling made predictions optional (exploratory
science is first-class here). His ruling on this item (2026-08-28): commit predictions for
UNSEEN analyses only — the file implements that ruling, not full pre-registration.

## Item 1 — Per-run integrator-null / model selection
**Agree; the check was missing — RUN (R1), and it changes the conclusion in the direction
the review predicted, with more structure.** Script `analysis/second_pass_r1_dynamics.py`;
per-run CSVs `r1_model_selection_{tank_L4,fr_S1_L14}.csv`; figure
`figures/fig_r1_fit_gallery_tank.png`. All fits on midpoint-referenced,
destination-oriented post-shift readings (k=1..20).

(a) **Per-run null comparison:** the mean-level "ahead at every step" does NOT hold
per-run. Tank: 6/24 runs fully ahead of the uniform null; 21/24 majority-ahead; per-run
mean lead +0.58 (range −0.54..+1.95). fr S1: 27/48 fully ahead, 44/48 majority-ahead,
mean lead +0.54 (−0.30..+1.67).

(b) **Model selection (BIC over integrator/step/hybrid, ΔBIC<2 → indeterminate):**
tank: hybrid 11, indeterminate 8, integrator 3, step 2. fr S1: hybrid 19, indeterminate
17, step 7, integrator 5. Fitted γ medians 0.90–0.99 (mild recency).

(c) **Simulation controls calibrate both error directions:**
- pure-step truth → integrator verdict: 0.0% (tank amps), 2.1% (fr amps) — the pipeline
  does not fabricate integrators;
- integrator truth → integrator verdict: 67% / 64% recovered (rest mostly indeterminate,
  hybrid ≤7%) — if runs were true integrators we'd expect ~65% integrator verdicts;
  observed 12.5% / 10%.
- pure-step truth almost never yields hybrid (1/48, 4/96) — so the observed hybrid
  dominance (46% / 40%) is not a step artifact.

**Conclusion for finding 5's rewording:** BOTH single-mechanism accounts are rejected by
the class distribution. Per-run dynamics are best described as DRIFT PLUS A DISCRETE JUMP
(hybrid), heterogeneous across runs, with a persistent residual (Item 10). "Consistent
with recency-weighted evidence integration" survives only as a description of the
direction-mean curve, not of runs.

## Item 2 — Occupancy power + population identity
**Agree on all three — RUN (R2). Script `analysis/second_pass_r2_occupancy.py`.**

(a) **Dip power at observed separation/spread (2000 sims):** tank (sep ±1.99, sd 0.7): n=24
power 0.47 (1/3 mix) / 0.83 (1/2 mix); n=120: 0.99/1.00. fr (sep ±0.88, sd 0.5): power
0.01–0.10 at ALL n up to 120 — **fr's unimodality verdicts were uninformative**; at fr's
mode separation the dip test cannot detect any mixture at any realistic n.
(b) Verdict language accordingly: tank band-level unimodality is meaningful for balanced
mixtures (marginal for 1/3); fr finding 3 must be restated as "no power to detect"
(proposed edit queued for Andrew's review).

(c) **WITHIN-STREAM occupancy — the doctrine population, first run** (144 tank checkpoint
windows, L4; figure `figures/fig_r2_within_stream.png`). Instrument: per-position
calibration from D4 checkpoint windows, RIGHT-ALIGNED on the shared carrier tail (a first
draft left-aligned and misaligned the tail — caught and fixed; both in the script header),
pooled class direction, per-position mid/denominator, denominator floor 0.3×median
(~10% of positions dropped). Reading scale: −1 = origin-arm token mean, +1 =
destination-arm token mean at the matched position. Key design point: the post-shift-block
windows (ck30/ck40) contain only destination-class content at position-matched offsets —
so content and position are controlled and ONLY history differs.
- ck20 control (pre-shift content): means −0.64/−0.76 — window tokens read their own class.
- ck30: +0.34 (ab) / +0.52 (ba); ck40: +0.52/+0.86 — the destination-class tokens
  themselves read HALFWAY to their no-shift reference: history suppresses the class
  reading of even the new evidence's own tokens, recovering with distance from the
  boundary (recency thirds, old→new, e.g. ck40 ba +0.58/+1.14/+0.87).
- Dip tests all unimodal (p ≥ 0.96) BUT per-token instrument sd is 1.7–2.8 — as
  pre-declared, token-level multimodality is undetectable at this noise; the within-stream
  MEANS are the usable testimony.
This is a new result, not just a check: within-stream, the transition is visible as a
suppressed class reading distributed across the window's own post-shift tokens.

## Item 3 — Event-locked jump analysis
**RUN (R4) — clean negative result, and an informative one.** Script
`analysis/second_pass_r4_small.py`. Coverage: 456/456 post-shift added sentences matched
to their single-sentence calibration cells (100%). Jump-run jump sentences: median
class-percentile **0.50** (n=12); non-jump-run largest-step sentences 0.55 (n=12); all
other post-shift sentences 0.50 (n=432); Mann-Whitney "largest-step sentences are stronger
exemplars" p = 0.445. **Jumps are NOT carried by unusually strong sentences** — the same
evidence strength produces a jump in one state and not another. This supports
state-dependent reorganization over input-driven steps (caveat: strength measured on
single-sentence carrier readings; in-context strength could differ).

## Item 4 — Hysteresis wording + lead-not-lag tension
**Agree, and the review under-states my error slightly:** the reconciliation note's
"HYSTERESIS IS DEMONSTRATED" was itself an overcorrection — matched-input
history-dependence is entailed by ANY unconverged integrator, so it is not evidence of
metastable structure. **Arithmetic verified (R1):** under midpoint referencing the D4
amplitudes are symmetric by construction (tank ±1.99, fr ±0.88), so the uniform null at
k=20 is exactly 0. Observed y(20): tank →+ +0.07 (AT the null, as the review suspected of
the raw +0.11), tank →− +0.91 (ahead), fr +0.44/+0.46 (ahead). Proposed diff in §R5.
The lead-not-lag tension stands and belongs in the findings doc: the motivating story
predicted LAG; observed is recency-LEAD early plus a persistent residual late (Item 10) —
the residual, not a lag, is the candidate carrier of any safety-relevant effect
(suicide-arm behavior cells adjudicate; predictions P5).

## Item 5 — Asymmetry: calibration causes first
**RUN (R3); the check order paid off — a calibration-level candidate cause exists.**
(a) Per-side calibration spreads (n=300/side, sd of per-probe readings along the axis):
tank aquarium 0.56–0.70 vs vehicle 0.83–0.91 at every layer probed (L4/8/16/23) — the
vehicle class is intrinsically more diffuse. fr symmetric (0.73–1.07 both sides). The tank
direction asymmetry (gap→vehicle 2.16 vs gap→aquarium 1.15) therefore has a candidate
instrument-level correlate: transitions INTO the broader class show the larger residual.
Candidate, not mechanism — logged for the carrier-replicate arm to test.
(b) Median- vs mean-based D4 midpoint: residual gaps unchanged (+2.16/+1.15), crossings
13/8 vs 13/7 — the asymmetry is NOT a midpoint-estimator artifact.
(c) Cross-carrier: the register's fourth carrier was superseded by Andrew's Q1-only
decision; the approved carrier-replicate arm ("Define the word tank.") is the scheduled
instrument-independence test.

## Item 6 — Sense vs topic at the carrier
**Live confound — (a) now RUN, and it lands on the sense side.**
(a) **Carrier-token class-signal profile** (identity-matched: the 9 verbatim carrier tokens
appear in every window; ck40 D4 windows, L4; figure `figures/fig_r2_carrier_dprime.png`):
d′ at ' tank' = **11.7**, vs 0.5–3.8 at the other carrier tokens and context-token median
1.37. The class contrast concentrates at the sense-bearing token by ~an order of magnitude
— peak-at-carrier, not flat. Supporting geometry: cos(ambient context-class direction,
tank-site axis) ≈ 0.36–0.38 — the carrier reading is largely site-specific, not a readout
of the ambient topic direction. This substantially weakens the pure topic-tracker
alternative for finding 3, though behavior cells + D5 remain the decisive discriminators
(a topic-tracker feeding a sense-specific readout at the carrier is still constructible).
(b) The finding-3 hedge (proposed diff §R5) stays until then, softened to cite this result.
(c) D5 minimal pairs: **honest answer — drift.** Designed, never generated; dropped from
the corpus table by omission, not decision. Scheduled after this response cycle.

## Item 7 — Register drift
(a) **Routing:** not drift — Andrew's explicit decision ("let's drop expert routing
altogether"), conclusion-level. Capture-level logging continues on every run (routing
parquet is free), so the observable survives passively for later study. The register should
be amended by Andrew, not silently by me. Deferred notes preserved in
`router_track_tank.md` (out-of-scope banner): soft 32-dim routing weights separate senses
perfectly at L4 (1.000); D3-lower-entropy anomaly (paired p=.02).
(b) **D5:** drift, conceded (Item 6c).
(c) **Backfill:** approved, was blocked on disk; unblocked today (junk cleanup: 154
sessions, 7.5 GB recovered, 56 GB free; `captures/deleted_junk_sessions.tsv`). Scheduled
after the analysis batches in this cycle.

## Item 8 — Metric hygiene
**Agree; table below is the deliverable (PRELIMINARY_FINDINGS gets it as a proposed edit
after Andrew's review).** Every Tier-A number with metric, chance, n, scheme:

| Number | Metric | Chance | n per class | Scheme |
|---|---|---|---|---|
| tank calibration 0.905 (L4) | accuracy | 0.50 | 300 | 12-fold leave-one-scene-pair-out |
| fr want 0.910 / letter 0.877 (L14) | accuracy | 0.50 | 300 | 12-fold leave-one-scene-pair-out (scene-canonicalized) |
| secondary axes tank 0.97–1.00 (L1–23) | balanced accuracy | 0.50 | 30 states/fold test | 6-fold leave-one-family-out |
| secondary axes fr 0.93–1.00 (L1–23) | balanced accuracy | 0.50 | 30 states/fold test | 6-fold leave-one-family-out |
| residual gaps (4 cells) | gap in calibration units | 0 = no gap | 12–24 runs / 12 families | family-clustered bootstrap 95% CI |
| dip tests (tank bands) | Hartigan dip p | — | 60 obs/band (12 runs × 5) | power 0.47–0.83 at n=24 indep (2a) |
| dip tests (fr) | Hartigan dip p | — | ≤120 | **power 0.01–0.10 — uninformative** |
| GMM band verdicts | ΔBIC(1−2) | — | 60 obs/band | 1- vs 2-component GaussianMixture |
| jump fractions 12/24, 34/48 | largest-step/net > 0.5 | — | runs | midref dest-oriented (raw-metric counts 8/24, 19/48 also reported) |
| model classes (hybrid 46%/40%) | min-BIC, ΔBIC≥2 | sim-calibrated | 20 points/run | false-integrator 0–2%, integrator-recovery 64–67% |

## Item 9 — Disclosure of suicide-arm analyses already seen
**Full disclosure, exact list** (also §2 of the predictions file):
1. S1 want-site L14 trajectories (both directions, both sub-arms, means + per-run).
2. Want-site integrator-null comparison (8/8 points ahead).
3. Pooled occupancy dip tests (unimodal, p ≈ 0.99–1.00).
4. Jump statistics (19/48 jump-dominant).
5. Cross-carrier means, families 0–3 only: S2/S3 vs S1, r = 0.95 / 0.80–0.93 — the letter
   site and S2/S3 are therefore PARTIALLY exposed; their full batteries are
   replication-grade, not first-look.
6. All-layers want-site heatmaps (raw, differential, midpoint-referenced) + per-layer D4
   plateau/midpoint table.
7. The two retractions and the accumulation-drift finding built on the above.
Not seen: letter-site full battery, occupancy time-bands/rule-(b) band, within-stream
occupancy, geometry battery, safeguard-vs-reading behavior, S2/S3 held-out families,
per-band crossing times. These are the firewalled set.

## Item 10 — Two-phase transitions + residual gap
**Agree — the review's strongest constructive item; RUN (R1), CONFIRMED in all four
probe×direction cells.** Figure `figures/fig_r1_residual_gap.png`.

(a) **Two-phase test:** best-γ integrator fits on direction means UNDERpredict the early
rise and OVERpredict late convergence in 4/4 cells (mean residual k1–5 / k15–20: tank →+
+0.09/−0.30, →− +0.18/−0.10; fr →+ +0.21/−0.17, →− +0.20/−0.17). The single-γ integrator
cannot produce this signed pattern; "fast partial + persistent residual" is the correct
description.

(b) **Residual gap (position-matched D4 destination level minus run plateau, midref,
family-clustered bootstrap 95% CI):** tank →+ +2.16 [1.86, 2.46]; tank →− +1.15
[0.82, 1.44]; fr →+ +0.38 [0.28, 0.50]; fr →− +0.35 [0.11, 0.59]. All four exclude zero:
the persistent residual is real in both probes. Note the eyeballed fr residuals in the
review (0.45/0.4) were read off the raw figure containing common-mode drift; the midref
values are 0.38/0.35 — close, by coincidence of L14's drift geometry.

(c) **Cross-probe comparison — normalized by D4 amplitude:** tank →+ 1.09, tank →− 0.58,
fr 0.43/0.40. The sharper-endpoint probe (tank, amp 2.0) has the larger normalized
residual; fr (amp 0.9) the smaller. Direction consistent with
"sharper endpoints ↔ stickier transitions" — but n=2 probes; PROPOSED status: promote to
named hypothesis with the carrier-replicate + extended-tail arms as its test, not to a
finding. Tank →+ deserves emphasis: its plateau sits ON the midpoint (gap ≈ amplitude) —
this is Item 12's parked mid-axis mode measured a second way.

Extended-tail captures (approved round-2 arm) now adjudicate "persistent vs slow": the
hybrid fits say the post-jump drift slope is shallow but nonzero in most runs.

## Item 11 — No-shift fictional arms don't hold
**Premise superseded by evidence (commit de65de4, pre-review) — and now further confirmed
by the secondary instrument (R3).** The neutral drift is class-NONSPECIFIC: at L14 the
no-shift plateaus (fic +0.12 / real +1.89) are symmetric about the position-matched
midpoint; under the secondary axes (R3 heatmaps) no-shift fictional arms read
fictional-side at EVERY layer and position. "Fiction doesn't hold" and "fiction as
decaying overlay" described the common mode; both were retracted in
fr_battery_first_results.md REVISION v2.
(d) **S2/S3 replication — RUN (R4), replicates with a twist that strengthens the account:**
the common-mode time-course (mean of fr and rf direction means; class component cancels)
replicates across carriers — S1 vs S2 r = 0.75 (near-identical values: t20 +0.92/+0.92,
t40 +0.96/+0.96), S1 vs S3 r = **−0.86** — same time-course, opposite sign on the
letter-site axis. One shared state-space drift component, projected with axis-dependent
sign: exactly what a class-nonspecific common component predicts, and inconsistent with
class-evidence accounts (which would not flip sign between same-class axes). n=4/4 runs
for S2/S3 (families 0–3, within the disclosed exposure).

## Item 12 — Occupancy re-read: location + persistence
**Agree — the review's sharpest catch — RUN (R2); the parked mid-axis mode is REAL in one
direction.** Figure `figures/fig_r2_mode_track.png`.
(a) Location+persistence (carrier site, midref, dest-oriented; D4 refs ±2.02):
- **ab (→+): the mode PARKS at mid-axis** — k11–15 mode +0.07, k16–20 −0.23 (sd ~0.6,
  stationary within jitter), i.e. ≥10 consecutive steps at ≥2.9 band-sd from BOTH
  endpoint references. Variance does not shrink (0.59→0.58) — a parked location, not a
  tightening attractor-like state; but location+persistence criteria for a population-level
  intermediate hold in this direction.
- ba (→−): still traveling — mode −1.16 → +0.38 → +0.54 → +0.79, monotone, never parks,
  ends at 39% of the destination reference.
- Framed with Item 10: the ab park IS the residual gap (gap ≈ amplitude in that
  direction); two views of one phenomenon.
(b) 1-vs-2 GMM per band (incl. ba k6–15): one component favored in EVERY band
(ΔBIC 1.2–11.8) — the population transits/parks as a single moving mode; no band splits
into origin+destination subpopulations. The vh→aq t6–15 visual hint does not survive BIC.
**Verdict wording change queued:** "no shared third mode" → "single unimodal mode that, in
ab, parks mid-axis for ≥10 steps (candidate population-level intermediate); no
two-population structure in any band." Whether the park is a learned intermediate or slow
passage is exactly the W3 geometry battery's question (firewalled, predictions P4).

## Item 13 — Jump metric + overshoot
**Agree; RUN (R1).** (a) Under largest-step/|net| > 0.5 on midref destination-oriented
curves: tank 12/24, fr S1 34/48 jump-dominant (earlier counts 8/24, 19/48 used raw
trajectories; the criterion is metric-sensitive — both reported). Largest-step/path-length
median 0.16 (both probes): jumps are large relative to NET displacement, small relative to
total path — the paths wander. (b) **Overshoot dissolves under the correct reference:**
the metrics CSV measured overshoot against the ±1 single-sentence endpoints; against the
position-matched D4 level (±2), the largest excursion (fam01_ba, momentary −2.04) just
touches the no-shift level. No run exceeds its destination's accumulated-context plateau.
The overshoot column should be re-referenced in any future use (flagged for the findings
doc; no edit until review).

## Item 14 — Post-shift volatility
**RUN (R4), quantified and logged; claim deferred to D6 as the review prescribes.**
Mean |step-to-step change| (midref, dest-oriented, tank L4): pre-shift 0.199, post-shift
0.314 (1.6× pre), late post-shift t31–40 0.289 (still elevated), position-matched D4
0.143. Post-shift volatility is ~2.2× the no-shift control at matched positions and does
not fully settle by t40. Consistent with "the region traversed mid-transition is
noisier," but the D6 mid-axis stationary control decides whether it's the REGION or the
transit.

## Item 15 — Depth/site checks
(a) **Layer-band robustness — RUN (R3):** headline tank numbers across L4/L8/L12/L16
(midref, calibration axes): amplitude 1.68–1.99; ab gap 1.35–2.16 (0.80–1.09 amp),
ba gap 1.15–1.28 (0.57–0.73 amp); ab > ba at every layer; crossings 11–13 (ab) vs 8–12
(ba). The headline structure is band-robust; the ab park is strongest at L4.
**Layer-0 indexing resolved from code:** residual hooks are `register_forward_hook` on
`model.model.layers[L]` (routing_capture.py:63) — layer L = post-block-L OUTPUT. L0 is
post-attention, so its above-chance accuracy (0.62–0.70 single-sentence; 0.73–0.88
secondary) is legitimate contextual signal, not leakage. The L0→L4 gradient
(0.62→0.905) further argues contextual origin.
(b) Folded into Item 5 (site-specificity: pre-lexical asymmetry queued with the
carrier-replicate arm). (c) Agree — finding 3 wording becomes "rapid-then-flat" (§R5).
(d) Agree — sub-arm near-coincidence logged as a real negative with n (24 run-pairs).

## Item 16 — Direction discrepancy vs legacy + axis anchoring
(a) **Orientation cannot flip by construction:** each layer's axis is diff-of-class-means
with ±1 endpoint normalization — label_a → −1, label_b → +1, per layer, same convention;
no free sign. D4 plateau gap > 0 at every layer for both probes (tank 3.4–4.0; fr midref
2.3→1.3; secondary instrument ±1 by construction with LOFO accuracy 0.95–1.00).
(b/c) The raw-heatmap "deep layers read real-side" was common-mode drift plus (new, R3)
AXIS ROTATION — see Item 17. The re-rendered secondary heatmaps show class-consistent
readings at every depth. Letter-site heatmaps + difference maps: queued behind the
predictions firewall (P1).
(d) **Legacy comparison — scheduled, not superseded:** legacy corpus finding (both
orderings collapse toward fictional; L23, carrier site, word-context corpus) predates the
no-shift-arm methodology; v6a/b priming arms serve as nearest analogues for a
midpoint-referenced re-read. Note the rotation result cuts toward the review's suspicion:
fr's single-sentence axis at L23 has cos 0.57 with the accumulated-context class direction
— the legacy L23 reading may substantially under- or mis-read accumulated states.
Quarantine stands.

## Item 17 — Depth regimes + MANDATORY axis-transfer check
**Check RUN in full (R2 step 0 + R3) — the review was right to mandate it: it caught a
real instrument effect my midref correction missed.** Figures
`figures/fig_r3_heatmap_secondary_{fr,tank}.png`, `fig_r3_axis_rotation.png`.

Instrument: per-layer position-matched secondary axes (labels = D4 arm identity, band
steps 11–40, ±1 normalization). Family-held-out accuracy: tank 0.97–1.00 (L1–23; L0
0.88), fr 0.93–1.00 (L1–23; L0 0.73) — metric: balanced accuracy, chance 0.50, 6-fold
leave-one-family-out.

**Axis rotation under accumulation (new named instrument effect):**
cos(secondary, single-sentence calibration axis) per layer — tank 0.78–0.97 (median
0.90): the calibration axis transfers. **fr: declines to 0.57–0.63 for L10–23 (median
0.63): the fictional/real class direction genuinely ROTATES on accumulated states at
mid/deep layers**, while separability stays ≈1.00 along the rotated direction. So the
deep-layer anomalies in the raw heatmap were common-mode drift (caught by midref) PLUS
under-reading through a rotated axis (caught only by the secondary refit).

**Regime adjudication:** under the secondary instrument, no-shift arms read
class-consistently at EVERY layer and position, both probes — regimes (ii) "deep
convergence to real" and (iii) "off-band" are instrument artifacts; regime (i) mid-band
behavior is confirmed. Doctrine addition (proposed): depth claims require per-layer
accumulated-context axes; single-sentence axes measured at long contexts are only valid
where rotation is verified small (tank yes, fr no).

## Item 18 — Per-band crossing times
**RUN (R3), gated on Item 17's instrument as required. Pre-stated prediction (P7, logged
2026-08-28 before computation): mid-stack L5–9 later than L10–17; deep intermediate.
Outcome: HOLDS for fr, FAILS for tank — reported as such.**
Mean-level crossing k by depth band (secondary instrument, `r3_crossing_times.csv`):
- fr fr: L2-4: 3, L5-9: 9, L10-17: 8, L18-23: 8 (weakly consistent);
  fr rf: L2-4: 4, **L5-9: 13**, L10-17: 8, L18-23: 8 (clearly consistent).
- tank ab: 13 at every band (3 deep layers never cross — the park is stack-wide);
  tank ba: L2-4: 8, L5-9: 10, L10-17: 10, **L18-23: 6 — deep layers cross EARLIEST**,
  contradicting the prediction's "deep intermediate."
Also notable: the earliest crossings anywhere are the shallowest layers in fr (k=3–4).
Interpretation is deferred (this analysis is descriptive; the depth story needs the
extended-tail arm), but the prediction's failure on tank is on the record.

---

## §R5 — Proposed diffs (drafted per protocol; NOT applied)

**Diff 1 — tank_d3_first_results.md, REVISION block, finding 1 terminology correction.**
Replace:
> "TERMINOLOGY CORRECTION (briefing reconciliation, 2026-08-28): under the briefing's
> operational definition — same final sentence, different history, different reading —
> HYSTERESIS IS DEMONSTRATED by these data."
With:
> "TERMINOLOGY NOTE (revised after second-pass review, 2026-08-28): same-final-input
> history-dependence is present in these data, but it is exactly what ANY unconverged
> evidence integrator produces — including the fitted recency null. It is therefore not,
> by itself, evidence of metastable structure. 'Hysteresis' is reserved for the D6 loop
> protocol; 'stickiness' for loop area beyond the fitted one-parameter recency model. What
> these data add beyond the integrator account is the candidate persistent residual
> (see residual-gap analysis), which D6/extended-tail will test."
Also append to finding 4 (direction asymmetry): "Both directions run ahead of the
integrator baseline; the motivating story predicted LAG. The lead-plus-residual structure —
not a lag — is now the candidate carrier of any safety-relevant effect; the suicide-arm
behavior cells adjudicate."

**Diff 2 — PRELIMINARY_FINDINGS.md, finding 3 ("sense reading at the carrier") hedge.**
Replace the claim's noun phrase "sense reading" with "class-contrast reading at the carrier
site" and append:
> "Open confound (second-pass review Item 6): a topic-tracker readout at the carrier
> position would produce the same projections. Discriminators queued: positional
> class-signal profile (peak-at-carrier vs flat), D5 minimal pairs (same topic, different
> sense), and behavior cells (does the reading predict output beyond topic?). Until one
> lands, this finding claims a reliable class contrast measurable at the carrier site, not
> a lexical-sense readout."

---

## Summary digest (what this response cycle changed)

**Corrections to our own findings (queued as proposed edits, pending Andrew):**
1. Finding 5 ("recency-weighted integration") — rejected at per-run level; the supported
   account is DRIFT + DISCRETE JUMP (hybrid), simulation-calibrated (Item 1).
2. fr occupancy unimodality — uninformative (power 0.01–0.10 at fr separation) (Item 2a).
3. "No shared third mode" — restated: single unimodal mode that PARKS mid-axis in ab for
   ≥10 steps; candidate population-level intermediate (Item 12).
4. Hysteresis/"demonstrated" wording — replaced per §R5 diff 1 (Item 4).
5. Overshoot metric — mis-referenced (vs ±1 instead of D4 level); no true overshoot (13b).
6. Finding 3 wording — "rapid-then-flat"; sense-vs-topic hedge softened by the new 6a
   result (Items 15c, 6).

**New results produced by the review's checks:**
7. Persistent residual gap, all four probe×direction cells, CIs exclude zero; tank ab
   plateau parks ON the midpoint; normalized gaps order tank→+ > tank→− > fr — evidence
   toward "sharper endpoints ↔ stickier transitions" (n=2 probes, proposed hypothesis).
8. Two-phase structure confirmed 4/4 cells (fast partial + persistent residual).
9. WITHIN-STREAM population testimony (first run): destination-class tokens read only
   ~half their no-shift reference under mixed history; recency-graded (Item 2c).
10. Class signal concentrates at the sense token: d′ 11.7 at ' tank' vs ~1.4 ambient
    (identity-matched) (Item 6a).
11. AXIS ROTATION under accumulation: fr class direction rotates at L10–23 (cos ≈ 0.6);
    tank stable; separability ≈ 1.00 along the rotated axis (Item 17). Doctrine addition
    proposed.
12. Jumps are not input-driven (jump sentences = median-strength exemplars, p 0.445)
    (Item 3).
13. Post-shift volatility 2.2× matched no-shift control; not settled by t40 (Item 14).
14. Accumulation drift is ONE shared state-space component: time-course replicates across
    carriers with axis-dependent sign (r +0.75 / −0.86) (Item 11d).
15. Item 18 pre-stated depth prediction: holds for fr, FAILS for tank (deep layers cross
    earliest in ba) — on the record.

**New figures (all regenerable from r1_figures.py / r2_figures.py / r3_figures.py):**
fig_r1_fit_gallery_tank, fig_r1_residual_gap, fig_r2_within_stream, fig_r2_mode_track,
fig_r2_carrier_dprime, fig_r3_heatmap_secondary_fr, fig_r3_heatmap_secondary_tank,
fig_r3_axis_rotation.

**Process disclosures from this cycle:** the within-stream instrument's first draft
left-aligned windows (misaligning the carrier tail); caught via an internal consistency
contradiction and fixed to right-alignment — both alignments documented in the script.
Item 3's first draft mis-parsed cumulative run files (0% match); fixed to differenced
texts (100% match).
