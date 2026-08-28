# Responses to Second-Pass Review (Items 0–18) — 2026-08-28

Per protocol: answers under each item; disagreements stated with evidence, never silent
compliance; NO findings-doc edits until Andrew reviews these responses, except Items 4/6b
drafted as proposed diffs (§R5 at bottom). Computational results are appended to their items
as they complete; items marked **PENDING** are queued in this response cycle.

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
**Agree; the check is mandatory and was missing.** "Ahead of null" was established on
direction-condition MEANS; with 8/24 (tank) and 19/48 (fr S1) jump-dominant runs, a
mean-level lead is compatible with a step mixture (averaged-learning-curve artifact).
**PENDING (R1):** (a) per-run null comparison; (b) per-run BIC over {fitted-γ recency
integrator, single change-point step, drift+step hybrid}; (c) simulation control — synthetic
pure-step runs with observed jump-time dispersion through the same pipeline; report the
false-integrator rate. Expected honest outcome: many runs indeterminate at 20 points; the
simulation calibrates exactly how much the pipeline can discriminate.

## Item 2 — Occupancy power + population identity
**Agree on all three.** (a) **PENDING (R2):** dip power at observed effective n for 1/3–2/3
mixtures at observed separation. (b) Verdict language will be corrected to "no evidence of
multimodality at n with power X for mixture Y" once power is known. (c) Correct and
conceded: the population doctrine's within-stream test has never run — the earlier window
attempt died on the cross-token trap and was not replaced. **PENDING (R2):** within-stream
occupancy on the 144 tank checkpoint windows using a position-matched secondary axis
(labels = D4 arm identity; band-pooled primary, per-position sensitivity). Known risk
declared up front: n=6 families/class — if histograms are mush, that is reported as an
instrument limit.

## Item 3 — Event-locked jump analysis
**Agree; cheap and high-value. PENDING (R4).** Method: for each jump step, the added
sentence's own single-sentence calibration reading (session_29a80932 cells) → percentile
within its class; compare jump-sentence percentiles vs non-jump added sentences. Coverage
caveat: only sentences present in the calibration cells get percentiles; coverage fraction
reported.

## Item 4 — Hysteresis wording + lead-not-lag tension
**Agree, and the review under-states my error slightly:** the reconciliation note's
"HYSTERESIS IS DEMONSTRATED" was itself an overcorrection — matched-input history-dependence
is entailed by ANY unconverged integrator, so it is not evidence of metastable structure;
it is a property the null already predicts. **PENDING (R1):** arithmetic re-verified under
actual per-direction D4 amplitudes and the midpoint convention. Proposed diff drafted in
§R5. The lead-not-lag tension is real and belongs in the findings doc: the motivating
safety story predicted LAG; tank shows recency-LEAD plus (Item 10) a persistent residual —
the residual, not a lag, is now the candidate carrier of the safety-relevant effect.
The suicide arm's behavior cells adjudicate (predictions file P5).

## Item 5 — Asymmetry: calibration causes first
**Agree with the check order; one premise partially superseded.** The fr durability
asymmetry was retracted pre-review (common-mode accumulation drift; commit de65de4) — the
surviving asymmetries are tank directional (crossing 7.2 vs 10.0 steps; residual per Item
10) and pre-lexical-site asymmetry. **PENDING (R3):** (a) per-side calibration spreads and
separation strengths per layer/site; (b) quantile-midpoint sensitivity (does the asymmetry
survive median-based midpoints?); (c) cross-carrier check: superseded as stated — the
register's fourth carrier was dropped by Andrew's Q1-only decision; the approved
carrier-replicate arm ("Define the word tank.") is the scheduled instrument-independence
test.

## Item 6 — Sense vs topic at the carrier
**Live confound, agreed.** (a) **PENDING (R3):** positional class-signal profile across
window positions under the secondary axis — peak-at-carrier favors sense-reading; flat
favors topic-tracking. (b) Agreed that finding 3's "sense reading" language must hedge to
"class-contrast reading at the carrier site" until (a) plus behavior cells discriminate —
proposed diff in §R5. (c) D5 minimal pairs: **honest answer — drift.** Designed, never
generated; dropped from the corpus table by omission, not decision. Scheduled after this
response cycle.

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
**Agree; uncontroversial. PENDING (R4):** every Tier-A number gets metric name, chance
level, per-class n, and CV scheme inline; a hygiene table added to PRELIMINARY_FINDINGS
(as a proposed edit for Andrew's review, per protocol).

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
**Agree; this is the review's strongest constructive item.** The "fast partial + persistent
residual" reading unifies: recency-lead early, plateau-short-of-D4 late, and Item 12's
parked mid-axis mode. One caution on the review's numbers: the eyeballed fr residuals
(0.45/0.4) were read off the RAW L14 figure, which contains common-mode accumulation drift —
the honest quantity is midpoint-referenced. **PENDING (R1):** (a) fitted-γ two-phase test
(underpredicts early rise AND overpredicts late convergence?); (b) residual gap
|plateau − matched-position D4 level|, midpoint-referenced, family-clustered CIs, per
direction/probe; (c) cross-probe comparison → decision on promoting
"sharper endpoints ↔ stickier transitions" (the original inversion hypothesis, resurfacing
with evidence). Extended-tail captures become decisive for "persistent vs slow"; already
approved as a round-2 arm.

## Item 11 — No-shift fictional arms don't hold
**Premise superseded by evidence (commit de65de4, pre-review).** The neutral drift is
class-NONSPECIFIC: at L14 the no-shift plateaus (fic +0.12 / real +1.89) are exactly
symmetric about the position-matched midpoint (+1.00) — 0.88 on each side; the midref
heatmap shows fictional blue / real orange across the full stack. So (a)'s "fiction doesn't
hold" and (c)'s "fiction as decaying overlay" describe the common mode, not the class
signal; both were retracted in fr_battery_first_results.md REVISION v2. What remains real
and named: **accumulation drift** (layer-dependent, class-nonspecific, fr ≈+1.0@L14, tank
≈0@L4/−0.7@L23) — content unknown per the label doctrine. (d) **PENDING (R4):** S2/S3
common-mode replication check (does the drift itself replicate across carriers?).

## Item 12 — Occupancy re-read: location + persistence
**Agree, and this is the review's sharpest catch.** My "no shared third mode" verdict was
structurally blind to a single PARKED mid-axis mode — which is not evidence against a
middle state; it is a candidate middle state. The t11–20 ab mode near +0.05–0.13 is exactly
that. **PENDING (R2):** (a) location-plus-persistence test — per band: mode location vs
both endpoint reference distributions, and variance trend across bands (transit predicts
moving mode + high variance; metastable middle predicts stationary mode + shrinking
variance). Framed jointly with Item 10's residual gap — the park and the residual are the
same phenomenon measured twice. (b) per-band 1-vs-2 GMM BIC, incl. vh→aq t6–15.

## Item 13 — Jump metric + overshoot
**Agree. PENDING (R1, folded into model selection):** largest-step/path-length ratio per
run; individual inspection of the overshoot run(s); jump-dominance recomputed under the
ratio metric for comparability with the literature-standard.

## Item 14 — Post-shift volatility
**Agree. PENDING (R4):** step-variance post-shift vs pre-shift vs position-matched D4;
logged as a quantity, claim deferred until D6 provides a mid-axis stationary control.

## Item 15 — Depth/site checks
(a) **PENDING (R3):** headline results recomputed on the L4–16 band; layer-0 indexing
resolved from capture code with the leakage argument (a true embedding layer must read
chance at a verbatim token — 0.62–0.70 implies post-block-0; verified in code, reported).
(b) Folded into Item 5. (c) Agree — finding 3's wording becomes "rapid-then-flat"
(proposed diff §R5). (d) Agree — sub-arm near-coincidence logged as a real negative result
with its n.
Numbers note: L0 calibration 0.62–0.70 vs L4 0.905/0.910 — the gradient itself argues the
signal is contextual, not positional leakage.

## Item 16 — Direction discrepancy vs legacy + axis anchoring
(a) **Orientation cannot flip by construction:** each layer's axis is diff-of-class-means
with ±1 endpoint normalization — label_a mean maps to −1, label_b to +1, per layer, by the
same convention; there is no free sign. The per-layer D4 plateau table confirms gap > 0 at
every layer for both probes (tank 3.4–4.0; fr 2.3→1.3).
(b/c) The raw-heatmap "deep layers read real-side" that motivated this item is the
common-mode drift (Item 11); the midref heatmap removes it. Letter-site heatmaps: firewalled,
queued (predictions P1); difference maps ship with them.
(d) **Legacy comparison — scheduled, not superseded:** the legacy corpus finding (both
orderings collapse toward fictional, L23, carrier site, word-context corpus) used the same
raw-axis instrument class but no no-shift arms exist in that corpus; the v6a/b priming arms
are the nearest analogues and will serve as the reference for a midpoint-referenced re-read.
Until then the inversion claim stays quarantined (it already carries the do-not-carry flag).

## Item 17 — Depth regimes + MANDATORY axis-transfer check
**Check accepted and runs; the regime interpretation is already largely dissolved.**
Regimes (ii)/(iii) were artifacts of common-mode drift (retraction, de65de4): under midref,
class separation persists at ALL depths (gap reduced 2.3→1.3, never inverted). The review's
secondary-axis check is nonetheless STRONGER than my midref (it re-fits the direction on
accumulated states rather than re-centering the single-sentence axis) and is the shared
instrument for Items 2c/6a/18. **PENDING (R2 step 0 + R3):** per-layer position-matched
secondary axis (labels = D4 arm identity, band-pooled steps 11–40, family-held-out accuracy
reported per layer), re-rendered heatmaps (fr want-site; tank), formal adjudication.

## Item 18 — Per-band crossing times
**Agree; gated on Item 17's instrument.** Pre-stated prediction logged 2026-08-28 in
predictions_suicide_arm.md P7 (mid-stack L5–9 cross later than L10–17; deep intermediate)
BEFORE computation. **PENDING (R3).**

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
