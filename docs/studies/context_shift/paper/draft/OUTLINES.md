# OUTLINES — "Unresolved: Semantic Metastability in Language Models When Context Shifts"

Per-section ordered bullets: exactly what gets written, in order, with every figure and
headline number placed, and interpretive-thread placements marked [HUMOR] [NEURO]
[SCOUT]. Nothing outside these bullets enters prose. Epigraph under title: the fish-tank
joke, one line, attributed as classic.

---

## Abstract (~200 w)
1. First line: model + scale ("in gpt-oss-20b, a 20-billion-parameter
   mixture-of-experts model, we track...") — the honesty anchor for the plural title.
2. Setup, one sentence: calibrated raw-activation readings of a token's interpretation
   while the surrounding context is shifted from one meaning/frame to another
   (polysemy arm; fiction/real framing arm — motivated by a real safety incident, named
   neutrally).
3. Claim 1: transitions are two-phase — fast partial update, then a persistent residual
   the counter-evidence never buys back (0.6–1.1× the class separation after 20
   counter-sentences, three of four cells robust to reference uncertainty).
4. Claim 2: per-run dynamics are drift plus discrete state-triggered jumps; every smooth
   integrator tested — including two-timescale — is rejected by simulation-calibrated
   model selection.
5. Claim 3: one direction per probe parks at a stable intermediate whose behavioral
   output is indecision (45% hedged answers in the mid band).
6. Claim 4: order-dependence is large and fully attributable to fitted recency
   weighting — no measurable stickiness.
7. Claim 5: everything runs on learned structure — no off-distribution excursions —
   except a small persistent learned marker of mixed context (25–38% of class
   separation), orthogonal to the content contrast.
8. Coin: "we call this cluster of properties semantic metastability."
9. Safety close, two sentences (uncertainty-default framing): the model never reports
   the unresolved state — it answers anyway, and internal mixedness is represented (the
   marker) but not gated on; safeguards with a trained uncertainty-default hold in the
   unresolved zone (80% safe-completion mid-band) while behaviors without one silently
   commit — and safeguard behavior attenuates along the learned frame axis (91%→50%).

## 1. Introduction (~900 w) — Andrew's voice
1. FAILURE-STAKES OPENING (the paper's center of gravity, 4–5 sentences): language
   models do not report uncertainty — when an interpretation is unresolved they go with
   it; many behaviors and safeguards implicitly assume a RESOLVED interpretation; so
   the interesting failures live in the unresolved zone. This paper measures that zone
   directly: what a token's interpretation looks like, inside the residual stream,
   while context is actively shifting what it means. (No [SCOUT] here — moved to
   discussion close.)
2. [HUMOR] Lineage paragraph: incongruity and its resolution at the core of humor
   theory; Dynel's garden path (incongruity resolves) vs pun (incongruity held); the
   fish-tank joke (epigraph referenced, not retold); the author's pre-LLM work
   visualizing 'tank' shifting between meanings in web-mined association space.
3. Bridge, 2 sentences: LLMs make the old question mechanically addressable — the
   in-between of a meaning shift is a measurable trajectory in the residual stream.
4. fr motivation paragraph (plain, clinical, safe-messaging): the incident — fiction
   assistance shifting to real-life disclosure; the probe asks how the internal
   fiction/real framing of one fixed request tracks that shift; NOTE the design
   contrast that pays off in discussion: the refusal safeguard plausibly carries a
   trained uncertainty-default, while the tank arm's sense question carries none —
   the two arms instantiate behavior-with-default and behavior-without.
5. The question + three worlds (brief): learned state, passage, or off the learned
   distribution? [NEURO: one framing sentence — transiently stable states without
   fixed-point attractors are the norm in coordination dynamics.]
6. Design-in-one-paragraph + fig_s9_collapse as the study in one image.
7. Contributions list (six results + instrument doctrine + corrections-as-method +
   full reproducibility).

## 2. Methods (~1,200 w)
1. Model + capture: gpt-oss-20b, stock configuration (native top-4 routing — the
   verbatim clarification), 24-layer residual stream (2880-d), harmony template,
   deterministic greedy passes; semantic token_position convention.
2. Probes and corpora table: carriers (Q1/Q1b; S1/S2/S3), sites, D1–D8 datasets with
   sizes; scene-diversity and ban rules; blind generation protocol.
3. Instrument doctrine (boxed protocol — the reusable artifact): (i) same-site,
   same-carrier calibration (the two demonstrated traps); (ii) scene-held-out validation
   (0.905/0.910); (iii) midpoint referencing vs position-matched no-shift arms —
   accumulation drift (one shared component, axis-relative sign, S1↔S2 r=+0.75,
   S1↔S3 r=−0.86); (iv) rotation verification — secondary axes (LOFO 0.93–1.00), fr
   rotates cos 0.57–0.63 at L10–23 (figure fig_r3_axis_rotation); (v) label doctrine;
   (vi) family-clustered statistics; (vii) shuffle audits + positive controls.
4. Glossary box (six terms).
5. QA/reproducibility paragraph: every number regenerates from committed scripts;
   bit-identical axes; 9/9 synthetic ground-truth fixtures; label-shuffle audits kill
   all headline effects; 17-entry corrections record (appendix A, presented as method).

## 3. Results

### R1 — Instruments and validity (F1+F2, ~900 w)
1. Endpoint separability: 0.87–0.91 single-sentence held-out; 0.93–1.00 on accumulated
   states at every layer; secondary heatmaps show class signal at all depths
   (fig_r3_heatmap_secondary_fr; tank version supplement).
2. What the ruler reads — three discriminations: identity-matched carrier d′
   concentration (tank d′ 11.7 at ' tank' vs 1.4 ambient; fig_r2_carrier_dprime);
   D5 minimal pairs (+0.99 = 50% of separation; 95% of 150 pairs; domain-clustered
   t=12.0 p=7.2e-05; fig_s9_d5_pairs); dose-independence (r=0.05) + length-cleanliness
   (r=0.02).
3. Anchored vs distributed contrast (tank token-anchored; fr spread across the request:
   'write' 6.4, 'suicide' 6.2, 'want' 4.5; fig_r6_carrier_dprime_fr) — directional
   comparison only.
4. Licensed-claim sentence: framing cues with content held, not abstract frame
   representation.

### R2 — The shape of reinterpretation (F3 + F9, ~1,000 w)
1. The collapse re-read quantitatively (fig_s9_collapse recalled): crossing 7–13
   sentences; lag defined in the present-frame sense with the integration-timescale
   sentence (γ → ~10–17-sentence memory); ahead-of-equal-weight noted as means-level.
2. Two-phase signature: single-γ fits underpredict early, overpredict late, 4/4 cells.
3. The residual gap (fig_r1_residual_gap): four cells with CIs; the normalized-gap>1
   explainer sentence (tank →vehicle plateau sits at the midpoint itself); correction-15
   honesty — fr→fictional suggestive only under reference resampling.
4. Material control: percentile match p=.24/.90.
5. F9 subsection: asymmetry replicates across carriers (Q1→Q1b 1.09/0.57→0.92/0.61
   amp), site-dependent within fr (want symmetric; letter 0.90/0.33, n=4/dir,
   exploratory; letter amplitude 1.18 — not weak); calibration-spread candidate
   (vehicle sd 0.83–0.91 vs aquarium 0.56–0.70) as candidate, not mechanism
   (fig_s9_asymmetry).
6. Persistent-vs-slow limitation named; forward-pointer to future work.

### R3 — The mechanism (F4+F5, ~1,000 w)
1. Per-run model selection setup: five models incl. two-timescale; ΔBIC≥2 rule;
   simulation calibration table-in-text (hybrid-truth→hybrid 13–15/24;
   twoscale-truth→hybrid 2–3/24; step-truth→integrator 0–2%).
2. Verdict: hybrid-dominant among classifiable runs (tank 11/16; fr 14/25 with 48%
   indeterminate stated); two-timescale wins zero (fig_s9_model_classes;
   galleries fig_r1_fit_gallery_tank + fr supplement; raw paths spaghetti_L4).
3. Jumps not evidence-strength-triggered (456/456 matched; percentile 0.50 vs 0.50,
   p=.445); untested trigger space named; "state-dependent" as working interpretation.
4. F5 within-stream: the token-population view — content+position matched, only history
   differs; pre-shift controls read own class; post-shift-block tokens at ~half
   reference, trimmed values quoted (ck30 +0.34/+0.37; ck40 +0.52/+0.53), fr
   replication (fig_r2_within_stream, fig_s9_within_stream_fr); descriptive framing
   sentence (consistent with token-level recency integration).

### R4 — Unresolved states and their behavior (F6+F7, ~900 w)
1. The park: mode stationary ≥10 steps at ≥2.9 sd from both references; variance flat;
   GMM one component every band (fig_r2_mode_track).
2. Replications: pre-lexical site; letter site; Q1b.
3. Geometry cross-reference (forward to R6): park states on-bundle 0.96×.
4. Behavior: category means −1.03/+0.74; side bands 56%/66% own-side; mid band 45%
   hedged (fig_r6_behavior_bands); degenerate loops one line.
4b. HOW uncertainty is (not) expressed: mid-band answers enumerate senses or commit to
   one (51% commit single-sense at mid) — characterize, with exact counts from the
   categorized worksheets at drafting time, whether ANY response reports uncertainty
   about which sense is meant, vs answering as if resolved. (The "they go with it"
   descriptive anchor.)
5. Matched-k framing: when the reading carries independent information — pooled
   mid-transition test p=.0138; fr at k=2 only (p=.010), later k scene-driven
   (fig_s9_behavior_matchedk).
6. Safety gradient: 50%→80%→91% by band (origin n=4 flagged); correlational-claim
   sentence.

### R5 — Order and equilibrium (F8, ~600 w)
1. D6 design one paragraph (mixture sweep, two orders, family's own sentences).
2. Loops large and real (tank +14.4 [12.2,16.8]; fr +10.5 [7.5,13.3]) —
   operational hysteresis exists (fig_r6_d6_loop_tank; fr supplement).
3. The reserved stickiness test: fitted null reproduces areas (+14.3; +11.1) —
   stickiness +0.1/−0.5 ns; cross-order validation; direction-dependent γ
   (0.91/0.97; 0.84/0.90) as the remaining real structure; the same-hour retraction
   named (corrections-as-method in action).
4. Path-vs-map resolution with R3: the equilibrium map is integrator-smooth; the
   sequential path is drift+jump — different observables, both true.

### R6 — The representation of irresolution (F10, ~600 w — compressed per Andrew; off-manifold treated honestly but briefly; the marker's role is to serve the represented-but-ungated story)
1. Off-manifold operationalized (never bare): reference = position-matched no-shift
   states; measures = k-NN distance + subspace reconstruction residual; noise level =
   per-state null spread; positive controls in-text (calibration 1.7–2.2×;
   position-mismatched states flagged 13–44%).
2. Per-state verdict: no individual excursions (jumps 1.06×/1.12×; park 0.96×); the
   pre-registered jump prediction failed — stated (fig_r5_geometry).
3. The systematic test (provenance sentence: the check exists because the per-state
   verdict was challenged — Andrew's "even a little off manifold is off manifold"):
   mean out-of-subspace residual 25%/38% of class separation; family-block null
   p<0.001; persists to k=20; largest at the park (fig_s9_shift_marker).
4. Hardening with numbers: orthogonal to calibration axis (cos +0.015/+0.011) and to
   the secondary accumulated-context axis (−0.0052/−0.0065); held-out direction 71–90%;
   family-novelty comparison stated numerically (novel +1.6/+3.4 vs subspace +6.7/+6.0,
   mixed ≈+27).
5. Content via D6 holdout: absent in pure contexts; near-full in static mixtures; fr
   halves under interleaving (shift-structure sensitivity); does NOT predict behavior
   at matched k.
6. Graded senses of off-distribution stated once + tamest-case note (operator battery
   as the future arm where genuine excursions are most likely).

## 4. Discussion (~950 w) — one paragraph each
1. Term anchoring [NEURO]: semantic metastability defined; Kelso coordination dynamics,
   Rabinovich winnerless competition / heteroclinic channels — metastable regimes ARE
   structured passages (F6's verdict); one-sentence equilibrium-bistability disclaimer
   (F8).
2. (a) [NEURO] Human parallel: good-enough processing — fast-but-partial reanalysis
   with lingering misinterpretation (Christianson & Ferreira; Slattery); the model
   reproduces the signature at the representation level.
3. (b) [HUMOR] The study as its own incongruity-resolution: expected basins, stickiness,
   off-manifold escapes; the data resolved to recency + jumps + residual + marker +
   on-manifold gradient.
4. (c) Safety & alignment — THE emphasis paragraph, restructured around the
   uncertainty-default contrast [interpretation, framed as such: training provenance
   unobservable; the arms differ in more than default-presence]: (i) the model never
   reports the unresolved state — it answers (R4's counts); (ii) the refusal safeguard
   behaves as if trained to default safe under irresolution (80% mid-band
   safe-completion; the reasoning traces weigh both readings then err safe) and so
   HOLDS in the metastable zone; (iii) the tank arm shows what happens without a
   default: silent commitment to one sense; any behavior lacking a trained
   uncertainty-default inherits this failure mode; (iv) present-frame lag + residual
   define WHEN the zone occurs; the gradient (91%→50%) shows safeguard attenuation
   along the learned axis, no exotic inputs needed; (v) monitor-expectation
   calibration: standalone cell-level AUC 0.61 [0.43,0.76], chance-compatible
   (fig_s11_monitor_roc, supplement) — band-level gradient real, monitor design future
   work, not a claim.
5. (d) [HUMOR] Garden-path-with-extended-incongruity vs pun (held incongruity); the
   park as extended incongruity phase; extended-tail as the named discriminator.
6. (f) Typicality-vs-commitment two-axis cut: the park is distributionally typical and
   semantically uncommitted — a learned state of unresolvedness (hedging its behavioral
   expression); genuine off-distribution is a different cell; never infer functional
   normalcy from geometric typicality (F7 documents the functional difference).
7. (g) Represented-but-ungated — ELEVATED (the mechanism behind "they go with it"):
   the mixedness marker exists, persists, and is behavior-inert at matched k; the same
   dissociation as internal-uncertainty vs generation in hallucination work (Kadavath;
   truthfulness directions; semantic entropy), observed here in transition dynamics;
   gating behavior on already-present internal signals is the constructive alignment
   suggestion that follows.
8. [SCOUT] Close (Andrew's home paragraph): one restrained cross-scale sentence
   (word-sense reinterpretation as the tractable instance of a broader family of
   frame shifts); metastable paradigm exploration mention lands here; the unresolved
   title's second meaning surfaces without irony.

## 5. Limitations & future work (~400 w)
1. Generalization candor: one model, one scale; internal-replication inventory (2
   probes, 3 carriers, 2 sites, carrier replicate) — what replicated vs what didn't
   (fr→fictional CI; letter n=4; fr indeterminate rate; depth prediction half-failed).
2. Deferred arms as the roadmap: extended-tail (garden-path-vs-pun); A→B→A return
   (remanence); write-site replication; letter-site expansion; third-class calibrations
   (drift content); operator battery (frame collisions/mutations — where off-manifold
   is most likely); monitor design.
3. Freeze/corrections sentence pointing to Appendix A.

## Appendices
A. Corrections record (17 entries, as method — one line each + the two same-session
   retractions called out).
B. Synthesis audit table (earns/borderline/ornament).
C. QA summary (regen diff, fixtures, shuffle audits) + reproducibility pointer.
D. Supplementary figures (figures/other/ + fr galleries/loops + fig_s11_monitor_roc).
E. Related-work notes woven per handoff §6 (anchors listed in Methods/Discussion where
   used; full list here).
