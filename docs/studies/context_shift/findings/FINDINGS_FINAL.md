# Context-Shift Study — Final Preliminary Findings (2026-08-31)

**What this is.** The QA-input findings document, superseding FINDINGS_AND_ANALYSIS_v2
(which remains the fuller technical record). Every conclusion below passed a two-lens
audit: (1) SANITY — alternatives considered explicitly, five of them as new computations
(`analysis/s7_sanity_checks.py`); (2) SYNTHESIS — every study element judged on whether
it earns its place or is methodological ornament (§4); ornaments are named as such, not
silently kept. Framing: metastable states / three worlds; label doctrine throughout
(readings are positions along designed contrasts, never meaning attributions).

**Corpus.** Two probe arms on gpt-oss-20b (24 layers, residual stream, harmony format,
seed 1): tank (aquarium/vehicle sense; carrier "What is the meaning of the word tank?",
' tank' site, L4) and fiction/real (framing of "I want to write a suicide letter.",
' want' site, L14). Per arm: single-sentence calibrations (300/class, scene-held-out
0.905/0.910), 40-step cumulative transition runs with shift after 20 (tank 24, fr S1 48
+ S2/S3 16), token-budget-matched no-shift arms (12 each), checkpoint window captures
(144 each), plus: D5 minimal pairs (150), D6 mixture sweeps (252/probe), behavior cells
with generation (312), carrier replicate (Q1b, 618), bare carriers (5). Zero capture
errors; all row counts asserted; every number regenerable from committed scripts.

---

## 1. Findings

Format: claim → evidence → alternatives considered → confidence.

### F1. The class contrasts are real, context-borne, and measurable at every depth — but the measurement axis rotates with accumulated context (fr).
Evidence: held-out accuracy 0.87–0.91 single-sentence, 0.93–1.00 on accumulated states
(leave-one-family-out, chance 0.50) at every layer L1–23, both probes; no-shift arms
read class-consistently at all depths under per-layer accumulated-context axes.
cos(accumulated-axis, single-sentence-axis): tank 0.78–0.97; **fr declines to
0.57–0.63 at L10–23**; letter site 0.69. Alternatives: early "deep-layer regime"
readings were exactly such an artifact — common-mode drift plus rotation — and were
retracted; depth claims made on unverified single-sentence axes are invalid by our own
demonstration. Confidence: high (the finding is largely a validated instrument doctrine).

### F2. What the axis reads is the frame/sense contrast, not topic vocabulary.
Evidence (three independent lines): (a) identity-matched carrier tokens — tank's class
signal concentrates at ' tank' (d′ 11.7 vs ambient 1.4); (b) D5 minimal pairs — content
held within pair, framing cue varied: within-pair difference +0.99 = 50% of full class
separation, 95% of 150 pairs in direction, p = 2.5e-25, uniform across six domains;
(c) the effect is dose-INdependent (r = 0.05 with cue-word count; one cue moves the
reading as much as four) — categorical frame detection, not cue-lexicon accumulation.
Alternatives: the cue words are themselves lexical, so the licensed claim is "reading
tracks framing cues with content held," not "abstract frame representation"; fr's signal
is distributed across the request's content words ('write' 6.4, 'suicide' 6.2, 'want'
4.5 vs ambient 3.6) rather than token-anchored — a framing contrast lives across the
utterance, and cross-probe d′ comparisons are directional, not quantitative.
Confidence: high for the discriminations run; wording deliberately modest.

### F3. Transitions are two-phase: a fast partial update that leaves a persistent residual.
Evidence: best single-γ integrator fits underpredict the early rise AND overpredict late
convergence in 4/4 probe×direction cells; residual gap (plateau vs position-matched
no-shift level, midpoint-referenced, family-clustered 95% CI) excludes zero in all four:
tank →vehicle +2.16 [1.87, 2.44] (the plateau parks ON the midpoint), →aquarium +1.15
[0.82, 1.45]; fr +0.38 [0.28, 0.49] / +0.35 [0.11, 0.58]. Twenty counter-sentences never
buy back what twenty native sentences build. Alternatives: (i) weaker post-shift
material — REJECTED by direct check (calibration percentiles of D3-post vs D4 sentences
match, p = 0.24/0.90); (ii) "persistent" vs "very slow" — undecidable at 20 post-shift
steps (hybrid fits show shallow nonzero late slopes); stated limitation, extended-tail
is the decisive arm; (iii) a two-timescale integrator explains the two-phase SHAPE in
principle — but see F4. Confidence: high for the gap; "persistent" carries the stated
caveat.

### F4. The per-run mechanism is drift PLUS discrete jump — and this survives its strongest smooth alternative.
Evidence: per-run BIC over five models (uniform/fitted-γ integrator, change-point step,
drift+step hybrid, two-timescale integrator): hybrid wins 11/24 (tank) and 14/48 (fr)
with the two-timescale model winning ZERO runs. Simulation-calibrated identifiability:
hybrid-truth reads hybrid 13–15/24; two-timescale-truth reads hybrid only 2–3/24 (it
masquerades as integrator/indeterminate instead) — so observed hybrid dominance cannot
be produced by any smooth one- or two-timescale integration. Jumps are state-dependent,
not input-driven: every post-shift sentence matched to its calibration cell (456/456),
jump-step sentences are median-strength exemplars (percentile 0.50 vs 0.50, p = 0.445).
Alternatives: (i) two-timescale integration — explicitly tested, cannot produce the
signature; (ii) jump-step selection is post-hoc max (acknowledged; the sim controls use
the same selection); (iii) single-sentence percentile ≠ in-context strength
(acknowledged limitation of the event-locked check). Confidence: high; this is the
study's central mechanistic claim.

### F5. Within the stream, history suppresses even the new evidence's own token readings.
Evidence: per-position D4-calibrated window instrument (right-aligned), content and
position matched, only history differing. Pre-shift control windows read own class
(tank −0.64/−0.76; fr −0.88/−0.85). Post-shift-block tokens — 100% destination-class
content — read only +0.34..+0.52 (ck30) recovering to +0.52..+0.86 (ck40) against a +1
reference; recency-graded; replicated across both probes (fr tighter, sd 0.7–0.9).
Alternatives: this is DESCRIPTIVE of where window tokens sit — it is consistent with
token-level recency integration and is not by itself evidence of a distinct mechanism;
its value is doctrinal (the population testifies, not just the carrier summary) and
practical (any window-level readout inherits the suppression). Token-level multimodality
is undetectable at instrument noise (declared). Confidence: high as description.

### F6. One direction per probe PARKS at a mid-manifold configuration — functionally an intermediate, geometrically a passage.
Evidence: tank aq→vh occupancy mode stationary at mid-axis for ≥10 steps at ≥2.9 sd
from both endpoint references (variance flat, GMM 1-component in every band — a parked
single mode, not a hidden two-population mixture); pre-lexical site and letter site
(fr→real, 0.90 amp short, n=4) show the same signature; Q1b replicates it under an
independent carrier (0.92 amp). Geometry: park states sit ON the trajectory bundle
(0.96× null; positive control 1.73×). Behavior: the mid band yields hedged/"both"
answers at 45% — double either side. Alternatives: (i) "park" vs still-rising — the
late slope is small but nonzero in some runs (F3's caveat applies); (ii) the D6
equilibrium map is smooth through this region, so the park is a property of the
sequential path, not a stable attractor of the mixture map; (iii) k-NN "on-bundle" is a
weak manifold notion — displacement along a low-variance direction could hide under
high-dimensional noise (stated limitation). Confidence: the phenomenon is solid; its
INTERPRETATION is the study's headline open question — the learned-intermediate vs
passage dichotomy itself fails to carve it.

### F7. Behavior co-varies with the reading — and carries a within-context component at mid-transition; the safety-relevant gradient is real but partly scene-driven.
Evidence: tank — answer-sense means −1.03/+0.74; side bands answer their side (56%/66%);
mid band 45% hedged. WITHIN matched context composition (fixed k), decided answers have
larger |reading| at k=6 (p=0.061) and k=12 (p=0.045) — mid-transition, the reading
predicts decidedness beyond context mixture; at k=2/20 (readings settled) no within-k
signal. fr — safe-completion dominates (88%); band gradient 50%→80%→91% (origin n=4,
fragile); within-k the reading separates fiction-frame from safety responses at k=2
(−0.06 vs +1.13, p=0.010) but NOT at later k, where response type follows scene family.
11/108 tank responses are degenerate repetition loops (new observation, not band-linked).
Alternatives: the band gradient alone would be compatible with context→both causation;
the matched-k analysis is what licenses the stronger (still correlational) wording. The
continuous logprob margin (+0.13) failed as an instrument (refusal-starter tokens overlap
compliant replies) — categorical evidence carries the finding. Confidence: solid as
co-variation + the two within-k results; NOT a causal claim.

### F8. Order-dependence at matched evidence is large, real — and fully attributable to recency weighting. No measurable stickiness.
Evidence: D6 loop areas tank +14.4 [12.2, 16.8], fr +10.5 [7.5, 13.3] — far from zero
(hysteresis in the operational sense exists). Against the reserved null (one-parameter
recency integrator FIT TO the D6 cells): stickiness +0.1 / −0.5, both ns. Cross-order
validation (fit one branch, predict the other): areas preserved; a mild real structure
remains — the two branches prefer different γ (tank 0.91 vs 0.97, fr 0.84 vs 0.90), a
direction-dependent recency weight not capturable by one γ, echoing F3's asymmetry.
A first pass using γ imported from D3 gave "+3.7 significant" — retracted within the
hour as a misspecified null (documented in script). RESOLUTION with F4: the equilibrium
mixture→reading MAP is integrator-smooth; the sequential PATH is drift+jump — different
observables, both true. Confidence: high; the retraction cycle is part of the evidence.

### F9. The direction asymmetry is carrier-independent and site-dependent — with a calibration-level candidate cause.
Evidence: tank gaps 1.09/0.57 amp (Q1) replicate as 0.92/0.61 under Q1b ("Define the
word tank."); robust to median-vs-mean midpoints; per-side calibration spreads differ
(vehicle sd 0.83–0.91 vs aquarium 0.56–0.70 at every layer) — transitions INTO the
broader class park harder. Within fr, the want site is symmetric but the letter site is
not (0.90 vs 0.33 amp, n=4/direction — exploratory). Alternatives: Q1b separation is
in-sample (0.895); the spread account is a correlate, not a demonstrated mechanism.
Confidence: asymmetry robust; explanation candidate-level.

### F10. No off-manifold world — anywhere we looked.
Evidence: k=3-NN off-bundle scores with validated positive control (calibration states
1.73×/1.77× null): jumps 1.06×/1.12×, park 0.96×, D4 1.04–1.07× — everything inside the
null's p95 (~1.25×). My pre-registered jump prediction FAILED (on record); P5c
(off-manifold → fewer safeguards) is moot for lack of off-manifold states.
Alternatives: the subspace caveat of F6(iii). Confidence: high within the instrument's
sensitivity; the caveat is stated, not waved off.

---

## 2. What the study now says (three worlds)

The in-between of a contextual shift, in these two probes, is: ON the learned trajectory
manifold (F10), traversed by drift-plus-discrete-jump paths (F4) whose jumps are
state-triggered rather than evidence-triggered, leaving a persistent residual of the old
frame (F3), with one direction per probe parking at a mid-configuration whose behavioral
output is indecision (F6/F7). The equilibrium evidence-mixture map is smooth and
recency-governed (F8). "Learned intermediate vs passage vs off-manifold" resolves as:
off-manifold — no; and the intermediate/passage dichotomy fails to carve the phenomenon —
the park is functionally a state and geometrically a passage. The safety-relevant
residual: what persists after a frame shift is not a lag but an un-bought-back remainder,
and behavior tracks it (F7) — the suicide-arm safeguard gradient runs 50%→91% along the
reading axis with the scene-driven caveat stated.

## 3. Corrections & retractions (cumulative, 14 entries)

Unchanged from v2 §5 + Phase F additions (12–14). New from this audit: none retracted,
two REWORDED — A10 → F7 (causal → co-variation + within-k), B8 → F8 (branch-γ asymmetry
added). The two live rewordings are the audit's product; everything else survived.

## 4. Synthesis audit — does each element earn its place?

| Element | Role | Verdict |
|---|---|---|
| D3/D4 + checkpoints + calibrations + scene-CV | the study's spine | EARNS |
| Midpoint referencing + secondary axes | killed three artifact findings | EARNS |
| Per-run model selection + sim controls (5 models) | central mechanism claim | EARNS |
| Residual gap + material check | central quantity | EARNS |
| D5 minimal pairs | closed sense-vs-topic decisively | EARNS |
| D6 mixture sweep | killed the stickiness claim — that is earning | EARNS |
| Q1b carrier replicate | confound control for F9 | EARNS |
| Behavior cells (categorical) | the safety-relevant link | EARNS |
| Geometry battery | closed the off-manifold world | EARNS |
| Power analysis | killed fr dip claims | EARNS |
| Within-stream instrument | doctrine compliance + F5 | EARNS |
| D7 bare carriers | n=1 each; suggestive speech-act sensitivity | BORDERLINE → appendix observation |
| D6 interleaved cells | one supporting datapoint | BORDERLINE |
| Crossing-time depth table | accountability record (prediction half-failed) | BORDERLINE — keep as accountability |
| Volatility quantification | unusable until D6-stationary control | BORDERLINE — logged only |
| Pre-lexical site | one supporting line for F6 | BORDERLINE |
| fr occupancy time-bands (P2) | computed because tank had them; powerless (B2) | ORNAMENT — appendix |
| Backfill "old block holds origin" | entailed by causal attention — not a finding | ORNAMENT (backfill itself: mandated completeness) |
| Path-length metric (13a) | answered a review item, unused since | ORNAMENT |
| Logprob margin (+0.13) | failed token-set design | ORNAMENT — marked failed instrument |
| fr dip-test rows | zero power | ORNAMENT |
| Raw fr heatmap narrative | superseded twice | historical only |

## 5. Limitations & deferred

Persistent-vs-slow (extended-tail); S2/S3 families 4–11; third-class calibrations (drift
content unknown); geometry subspace sensitivity; behavior logprob token sets (redesign);
fr behavior origin-band n=4; letter-site asymmetry n=4; single model, single seed,
K=1 routing; two probes ⇒ all cross-probe patterns (sharper-endpoints↔larger-residuals,
distributed-vs-anchored contrast) are n=2 hypotheses, not findings.

## 6. Load-bearing figures

fig_r1_fit_gallery_tank · fig_r1_residual_gap · fig_r2_within_stream · fig_r2_mode_track
· fig_r2_carrier_dprime · fig_r6_carrier_dprime_fr · fig_r3_heatmap_secondary_{fr,tank}
· fig_r3_axis_rotation · fig_r5_geometry · fig_r6_d6_loop_{tank,fr} ·
fig_r6_behavior_bands. (Historical: raw/midref fr heatmaps, traj_null, spaghetti,
occupancy_bands, jumpiness, prelexical, norm_vs_alignment, calibration_layers.)
