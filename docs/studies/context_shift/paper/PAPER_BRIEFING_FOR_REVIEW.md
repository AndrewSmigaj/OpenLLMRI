# Paper Briefing — "Off the Beaten Path: Semantic Metastability in a Large Language Model"

**For the chat-side reviewer, 2026-08-31.** This is the complete pre-planning handoff:
every audited finding, the corrections record, the locked framing decisions, and the
provisional paper shape. The science is FROZEN (post-QA; regeneration-verified,
fixture-tested); what we are planning together now is the PAPER — content selection,
emphasis, venue, and narrative. The structure below is provisional and will be planned
properly once topic and content are finalized. Engage adversarially; wording and
framing critique is in-scope, new analyses are not (they go to the roadmap).

## 1. Locked decisions

- **Title (locked): "Off the Beaten Path: Semantic Metastability in a Large Language
  Model."** "Semantic metastability" is the coined term — operational definition at
  first use: a persistent intermediate configuration of a token's contextual reading,
  held between two calibrated interpretations, on the path timescale. Singular "a
  Large Language Model" is the deliberate honesty hedge (one model, two probes).
- **Lag/hysteresis language = the present-frame sense** (correction 17). The reading
  genuinely lags the current frame — 7–13 sentences to cross, full arrival never — on
  the timescale its integration window implies (γ≈0.9–0.98 → ~10–17-sentence memory).
  Only lag IN EXCESS of evidence integration (drag/stickiness) is denied.
- **Humor lineage = context and inspiration, not subject.** Dynel's garden-path/pun
  distinction appears in intro/discussion as lineage. The park is framed as a garden
  path with an EXTENDED INCONGRUITY PHASE (not a pun — puns never resolve); whether any
  park is a true held-incongruity limit case is the framework's named open question →
  future work (extended-tail arm). Not a computational-humor paper (though such venues
  are plausible secondary targets).
- Voice: intro and discussion are Andrew's voice (paradigm scout; humor-research
  origins; the fish-tank joke; pre-LLM cosine-shift work on 'tank'). Discordant colony
  optimization is blog-only, never in the paper. Results sections stay under the label
  doctrine (readings = positions along designed contrasts, never meaning attributions).
- Suicide-arm motivation: one plain clinical paragraph on the real incident;
  safe-messaging norms throughout; no dramatization.
- Methods must state: the model runs STOCK (native top-4-experts-per-token routing, no
  config overrides; verified in code) — "K=1" in project shorthand referred only to a
  dropped routing-analysis convention.
- The corrections appendix (17 entries) is presented as METHOD — the mechanism that
  makes surviving claims trustworthy — not as confession.

## 2. Study snapshot

gpt-oss-20b, 24 layers, residual stream (2880-d), harmony format, deterministic greedy
forward passes. Two probe arms:
- **tank** (aquarium/vehicle sense): carrier "What is the meaning of the word tank?",
  ' tank' site, headline layer L4.
- **fr** (fictional/real framing): carrier "I want to write a suicide letter." (' want'
  site, L14), + paraphrase carriers S2 (' like') and S3 (' letter').
Per arm: 300/class single-sentence calibrations (scene-held-out 0.905/0.910); 40-step
cumulative transition runs, shift after 20 (tank 24; fr 48+16), the word "tank"/artifact
nouns absent from all contexts; token-budget-matched no-shift arms (12 each); 144
checkpoint window captures each; 150 D5 minimal pairs; 252 D6 mixture cells per probe;
312 behavior cells (generation + forced-final first-token logprobs); Q1b carrier
replicate ("Define the word tank.", 618); 5 bare carriers. Zero capture errors; every
number regenerates from committed scripts (QA: bit-identical axes, 23-script regen diff
green, 9/9 synthetic ground-truth fixtures pass, sign/boundary/join/shuffle audits pass).

**Instrument doctrine (a named methods contribution).** Three generations: (1)
single-sentence calibration axes (diff-of-class-means, ±1 endpoints); (2) MIDPOINT
REFERENCING against position-matched no-shift arms — required because of ACCUMULATION
DRIFT, a class-nonspecific component growing with context (one shared state-space
component; sign is axis-relative: S1↔S2 r=+0.75, S1↔S3 r=−0.86); (3) position-matched
SECONDARY AXES fit on accumulated no-shift states (LOFO 0.93–1.00 at all layers) —
required because of AXIS ROTATION: fr's class direction rotates to cos 0.57–0.63 vs the
single-sentence axis at L10–23 (tank stable 0.78–0.97; letter site 0.69). Two
demonstrated traps (cross-position and cross-token projection) motivate same-site,
per-carrier calibration. Depth claims on unverified single-sentence axes are invalid —
we demonstrated this on ourselves (retractions 3–5).

## 3. The ten findings (audited; alternatives considered; QA-corrected)

**F1 — Contrasts are real, context-borne, measurable at every depth; the axis rotates
with accumulation (fr).** Held-out 0.87–0.91 single-sentence, 0.93–1.00 accumulated,
every layer, both probes. Rotation numbers above. Confidence high.
[Figs: calibration_layers, fig_r3_axis_rotation, fig_r3_heatmap_secondary_{fr,tank}]

**F2 — The axis reads the frame/sense contrast, not topic vocabulary.** (a) identity-
matched carrier tokens: tank class signal concentrates at ' tank' (d′ 11.7 vs ambient
1.4); (b) D5 minimal pairs, content held within pair: within-pair effect +0.99 = 50% of
class separation; 95% of 150 pairs in direction; pair-level p=2.5e-25, domain-clustered
t=12.0 p=7.2e-05, all 3 generation batches positive; (c) dose-INdependent (r=0.05 with
cue count) — categorical frame detection; not length-driven (r=0.02). Licensed claim:
"reading tracks framing cues with content held," not "abstract frame representation."
fr's signal is distributed across the request's words ('write' 6.4, 'suicide' 6.2,
'want' 4.5 vs ambient 3.6) where tank's is token-anchored. Confidence high.
[Figs: fig_s9_d5_pairs, fig_r2_carrier_dprime, fig_r6_carrier_dprime_fr]

**F3 — Transitions are two-phase: fast partial update + persistent residual.** Single-γ
integrator underpredicts early rise AND overpredicts late convergence, 4/4 cells.
Residual gaps (plateau vs position-matched no-shift level, midref, family-clustered):
tank →vehicle +2.16 [1.87,2.44] (plateau parks ON the midpoint); →aquarium +1.15
[0.82,1.45]; fr →real +0.38 [0.28,0.49]; fr →fictional +0.35 [0.11,0.58] fixed-ref —
**correction 15: with D4 reference uncertainty propagated, fr →fictional widens to
[−0.12,+0.79] and is SUGGESTIVE ONLY; the other three cells robust both ways.** Not
weaker material (sentence percentiles matched, p=.24/.90). "Persistent" vs "very slow"
undecidable at 20 steps → stated limitation; extended-tail is the named future arm.
[Figs: fig_s9_collapse (opening figure), fig_r1_residual_gap, traj_null_L4, fr_traj_null_L14]

**F4 — Mechanism: drift PLUS discrete jump; survives its strongest smooth rival.**
5-model per-run BIC (incl. two-timescale integrator): hybrid dominant among classifiable
runs (tank 11/16; fr 14/25 — 48% of fr runs indeterminate at its noise, stated);
two-timescale wins ZERO runs and in simulation masquerades as integrator, almost never
hybrid (2–3/24) while hybrid-truth reads hybrid 13–15/24. Jumps are not triggered by
evidence strength (456/456 sentences matched to calibration cells; jump sentences
median-strength, p=.445); other triggers untested — "state-dependent" is the working
interpretation. Confidence high; central mechanistic claim.
[Figs: fig_s9_model_classes, fig_r1_fit_gallery_tank, fig_s9_fit_gallery_fr, spaghetti_L4]

**F5 — Within-stream: history suppresses even the new evidence's own token readings.**
Content+position matched, only history differs. Pre-shift controls read own class
(−0.64/−0.76 tank; −0.88/−0.85 fr). Post-shift-block tokens read ~half their no-shift
reference — **correction 16: tank means quoted TRIMMED (|r|≤6): ck30 +0.34/+0.37, ck40
+0.52/+0.53; the untrimmed +0.86 was heavy-tail-inflated; suppression claim strengthens
and becomes direction-symmetric. fr not tail-sensitive.** Descriptive finding
(consistent with token-level recency integration); doctrinal + practical value.
[Figs: fig_r2_within_stream, fig_s9_within_stream_fr]

**F6 — One direction per probe PARKS at a mid-manifold configuration — functionally an
intermediate, geometrically a passage.** tank aq→vh: occupancy mode stationary at
mid-axis ≥10 steps, ≥2.9 sd from both endpoint references; variance flat; GMM
1-component every band (single parked mode, not two populations). Replicates: pre-lexical
site; letter site (0.90 amp short, n=4/dir, exploratory); Q1b carrier (0.92 amp).
Geometry: park states ON the trajectory bundle (0.96× null). Behavior: mid-band answers
45% hedged/"both". D6 equilibrium map is smooth through this region → the park is a
property of the sequential path, not equilibrium bistability (this defuses the physics
reading of "metastable" — one sentence in discussion). Interpretation = the paper's
headline open question: the intermediate/passage dichotomy fails to carve it.
[Figs: fig_s9_collapse, fig_r2_mode_track, fig_r5_geometry, fig_r6_behavior_bands, fig_s9_asymmetry]

**F7 — Behavior co-varies with the reading; a within-context component exists
mid-transition; the safety gradient is real but partly scene-driven.** tank answer-sense
means −1.03/+0.74; side bands answer their side (56%/66%); mid band 45% hedged. At
matched context composition: pooled mid-k test (k∈{6,12}) decided |reading| 0.72 vs
undecided 0.38, p=.0138. fr: safe-completion dominates (88%); band gradient 50%→80%→91%
(origin band n=4, fragile); within-k separation at k=2 only (p=.010, one of four tested)
— later k scene-driven. 11/108 tank responses are degenerate repetition loops (new
observation, not band-linked). Correlational claim only; logprob margin (+0.13) was a
failed instrument (token-set design), categorical evidence carries the finding.
[Figs: fig_r6_behavior_bands, fig_s9_behavior_matchedk]

**F8 — Order-dependence is large and real — and fully attributable to recency
weighting. No measurable stickiness.** D6 loop areas tank +14.4 [12.2,16.8], fr +10.5
[7.5,13.3] — hysteresis in the operational sense exists. Against the reserved null
(one-parameter recency integrator FIT TO the D6 cells): stickiness +0.1/−0.5, ns;
cross-order validation preserves the verdict; a mild real structure remains
(direction-dependent γ: 0.91/0.97 tank, 0.84/0.90 fr). A first pass with γ imported
from D3 gave "+3.7 significant" — retracted within the hour (misspecified null;
correction 12). RESOLUTION with F4: the equilibrium mixture→reading MAP is
integrator-smooth; the sequential PATH is drift+jump. Different observables, both true.
[Figs: fig_r6_d6_loop_tank (+ _fr in supplement)]

**F9 — The direction asymmetry is carrier-independent and site-dependent, with a
calibration-level candidate cause.** Tank gaps 1.09/0.57 amp (Q1) replicate as
0.92/0.61 (Q1b); robust to median midpoints; per-side calibration spreads differ
(vehicle sd 0.83–0.91 vs aquarium 0.56–0.70 — transitions INTO the broader class park
harder; candidate, not mechanism). Within fr: want site symmetric, letter site not
(0.90/0.33 amp; letter-site D4 amplitude 1.18 — not weak; n=4/dir, exploratory).
[Figs: fig_s9_asymmetry]

**F10 — No individual off-manifold excursions — but a small, systematic, PERSISTENT
displacement off the no-shift manifold: a learned mixed-context marker.** Per-state:
jumps 1.06×/1.12×, park 0.96× — inside the null (positive controls detected at
1.7–2.2×); the pre-registered jump prediction FAILED, on record. SYSTEMATIC: mean
out-of-subspace residual = **25% (tank) / 38% (fr) of the class separation**, family-
block null p<0.001 both probes; rises over ~5 steps, persists to k=20, largest at the
park. Hardening: orthogonal to the class axis (cos ~.01); survives held-out direction
estimation (71–90%); family novelty refuted directionally. Content (D6 holdout): absent
in pure contexts; near-full in static mixed contexts; tank order-insensitive, fr HALVES
under interleaving (partly a coherent-shift-structure marker). Does NOT predict behavior
at matched k. Provenance: this finding exists because Andrew challenged the per-state
verdict ("even a little off manifold is off manifold") — the paper credits that.
[Figs: fig_s9_shift_marker, fig_r5_geometry]

## 4. The synthesis (three worlds, answered)

The in-between of a contextual shift, in these probes: free of individual off-manifold
excursions yet carrying a persistent learned mixed-context marker (F10); traversed by
drift-plus-jump paths whose jumps are state-triggered (F4); lagging the present frame on
its integration timescale while running slightly ahead of equal-weight evidence (F3/17);
leaving a residual new evidence never buys back (F3); with one direction per probe
parking at a configuration whose behavioral output is indecision (F6/F7); and an
equilibrium evidence map that is smooth and recency-governed (F8). "Learned intermediate
vs passage vs off-manifold" resolves as: off-manifold — no (with the marker as the
subtle yes); and the intermediate/passage dichotomy fails to carve the park —
functionally a state, geometrically a passage.

## 5. Corrections record (17 entries — a paper appendix, presented as method)

1 withdrawal of "history suppresses 2–20×" (integrator null); 2 softening of
graded-packet claim; 3–5 the fr drift/rotation retraction cluster (durability, depth
disagreement, L23 crossing); 6 "hysteresis demonstrated" overcorrection withdrawn;
7 "no shared third mode" → parked single mode; 8 overshoot metric mis-referenced;
9 fr dip verdicts → no power; 10 routing claims out of scope; 11 two process bugs
caught pre-conclusion (window alignment; cumulative parsing); 12 D6 "+3.7 stickiness"
retracted same-session (fitted null); 13 "retrospective re-reading" recognized vacuous
under causal attention before running; 14 letter-battery construction limit (self-
estimated common mode forces mirror symmetry); 15 reference-resampled CIs demote
fr→fictional gap; 16 within-stream trimmed means; 17 lag-sense clarification.

## 6. What is deliberately NOT in the paper

Ornaments (named in the synthesis audit): fr occupancy time-bands (no power), backfill
"old block holds origin" (entailed by causality), path-length metric, logprob margin
(failed token sets), fr dip rows, raw-heatmap narrative beyond the instrument story.
Trimmed to appendix/supplement: crossing-time depth table (accountability: the
pre-stated depth prediction held for fr, FAILED for tank — on record), D7 bare-carrier
observations (n=1; includes the suggestive speech-act sensitivity: bare S1/S2 read at
the fictional class mean, S3's imperative flips real-side), volatility (logged, awaits
D6-stationary control), D6 interleaved cells, sub-arm invariance (validity paragraph),
degenerate loops (one line).

## 7. Roadmap / future work (paper's future-work section draws from this)

Extended-tail runs (persistent-vs-slow = the garden-path-vs-pun discriminator, the
framework's named open question); A→B→A return arms (classical remanence); write-site
replication (fr d′ peaks at ' write' 6.4 > ' want' 4.5; existing windows suffice);
letter-site expansion (n=4/dir now); S2/S3 families 4–11; third-class calibrations
(drift content); geometry subspace sensitivity; behavior logprob token-set redesign;
conceptual-operator battery (frame collisions, mutations — where off-manifold might
genuinely appear, since our shifts are the tamest possible: clean blocks between two
well-learned frames).

## 8. Provisional paper shape (to be planned properly with you)

Conventional skeleton, voice-led bookends: Intro (lineage → question → three worlds;
opening figure fig_s9_collapse) → Methods (probes, capture geometry, instrument
doctrine as named contribution, K=1 note, determinism) → Results R1–R10 following
F1–F10 order above → Discussion (the study as its own incongruity-resolution: expected
basins/stickiness/off-manifold escapes, found recency+jumps+residual+marker+on-manifold
gradient; semantic metastability defined; safety reading: present-frame lag + residual
+ the on-manifold safeguard gradient — no exotic excursion needed; limitations: n=2
probes, one model, deferred arms) → Appendices (corrections log, synthesis audit, QA
summary, supplementary figures).

Figure budget: 20-figure main-text candidate set exists (paste set); 12 more in
supplement (figures/other/). All regenerable from committed scripts.

## 9. What we want from you in the planning round

Venue thoughts; abstract angle (term-coining vs claim-led); which of R1–R10 merge or
demote to keep the paper tight; related-work anchors you'd expect a reviewer to demand
(context interference, in-context learning dynamics, representation drift, safety
steering); and anything in §3 you think cannot survive review as stated.
