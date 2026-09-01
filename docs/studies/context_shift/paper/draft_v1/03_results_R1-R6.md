<!-- Section 3: Results R1-R6. Outline: OUTLINES.md §3. Checklist: gap>1 explainer [x];
correction-15 CI honesty [x]; trimmed within-stream values [x]; fr indeterminate rate
[x]; matched-k framing [x]; 0/96 counts (s12) [x]; same-hour retraction named [x];
off-manifold never bare + positive controls in-text [x]; both-axes orthogonality [x];
family-novelty numbers [x]; provenance credit [x]; graded senses + tamest case [x];
all numbers from FINDINGS_FINAL [x]. -->

# 3. Results

## 3.1 The instrument reads a real contrast, and reads the right thing (R1)

Before any dynamics, two questions: can an interpretation be read out at all, and is
what we read the intended contrast rather than a topical shadow of it?

On the first: single-sentence calibration axes separate the classes at 0.905 (tank,
layer 4) and 0.910 (fiction/real, layer 14) under scene-held-out cross-validation, and
axes refit on accumulated forty-sentence contexts separate held-out families at
0.93–1.00 at every layer from 1 to 23, in both probes. Under these per-layer
accumulated-context axes, no-shift arms read class-consistently across the entire
depth of the stack (Fig. fig_r3_heatmap_secondary_fr) — with the caveat, established
in Methods, that the fiction/real direction itself rotates with accumulation and must
be refit at depth (Fig. fig_r3_axis_rotation).

On the second, three independent discriminations. First, an identity-matched
comparison: the nine tokens of the tank carrier appear verbatim in every checkpoint
window, so class signal can be compared across tokens with identity held fixed. The
signal concentrates overwhelmingly at the sense-bearing token — d′ = 11.7 at ' tank'
against a context-token median of 1.4 (Fig. fig_r2_carrier_dprime; n = 6 runs per
class, and we caution that orderings among the non-peak bars are not interpretable at
this n, since d′ divides by a pooled standard deviation that is small for highly
predictable tokens). Second, minimal pairs: 150 sentence pairs sharing most content
words while differing only in framing cues shift the reading by +0.99 axis units —
half the full class separation — with 95% of pairs in the predicted direction
(pair-level p = 2.5×10⁻²⁵; domain-clustered, the conservative unit, t(5) = 12.0,
p = 7.2×10⁻⁵; all three blind generation batches positive; Fig. fig_s9_d5_pairs).
Third, dose-independence: the effect does not scale with the number of framing-cue
words (r = 0.05), and is not a length artifact (r = 0.02; length-matched pairs +1.05)
— one cue moves the reading as far as four, the signature of categorical frame
detection rather than cue-lexicon accumulation.

The licensed claim is deliberately modest: the reading tracks framing cues with
content held fixed — not an abstract frame representation. The two probes also differ
instructively in contrast structure: tank's signal anchors to one token, while the
fiction/real signal distributes across the request's content words (' write' 6.4,
' suicide' 6.2, ' want' 4.5 against an ambient 3.6; Fig. fig_r6_carrier_dprime_fr) —
a lexical-sense contrast lives at a token; a framing contrast lives across the
utterance. This comparison is directional only.

## 3.2 The shape of reinterpretation: fast, partial, permanent (R2)

Figure fig_s9_collapse shows the study in one image: both transition directions, both
probes, on one axis against the no-shift references. After the shift, readings cross
zero within 7–13 sentences — but neither direction, in either probe, reaches the
opposite reference within twenty counter-sentences. The reading lags the present frame
in the plain sense: it trails what the conversation has become, on roughly the
timescale its integration window implies (fitted recency weights γ ≈ 0.9–0.98
correspond to an effective memory of ten to seventeen sentences). Relative to an
equal-weight average of all evidence in the window, the mean trajectories actually run
slightly *ahead* — the model mildly over-weights recent sentences; individual runs are
heterogeneous around that mean. What the data rule out is not lag but lag *in excess*
of evidence integration.

The transition is two-phase. The best-fitting single-γ recency integrator
underpredicts the early rise and overpredicts late convergence in all four
probe-by-direction cells: the reading moves faster than integration early, then stops
short of where integration says it should end. The shortfall is the **residual gap**:
the distance between a run's plateau and the position-matched no-shift level, in
midpoint-referenced units (Fig. fig_r1_residual_gap). All four cells show positive
gaps under family-clustered bootstrap: tank →vehicle +2.16 [1.87, 2.44] — a gap
exceeding 1.0 in amplitude-normalized units, meaning the plateau sits at the class
*midpoint* itself, the full transition never even half-completing beyond it; tank
→aquarium +1.15 [0.82, 1.45]; fiction→real +0.38 [0.28, 0.49]; real→fictional +0.35
[0.11, 0.58]. Honesty requires one demotion: when the uncertainty of the six-arm
reference is propagated into the bootstrap, three cells stand but real→fictional
widens to [−0.12, +0.79] and no longer excludes zero — that cell's residual is
suggestive only. The gap is not an artifact of weaker post-shift material: the
post-shift sentences match the no-shift arms' sentences in single-sentence calibration
strength (percentile medians 0.51 vs 0.45 and 0.48 vs 0.49; p = 0.24, 0.90). Whether
the residual is truly permanent or merely slower than twenty sentences can resolve is
undecidable in this corpus — the late slopes are shallow but nonzero in some runs —
and deciding it is the first item of future work.

**Direction matters, and the asymmetry is not an instrument accident.** Tank
transitions toward the vehicle sense fall 1.09 amplitude-fractions short versus 0.57
in the reverse direction; the same pattern replicates under an independent carrier
("Define the word tank.": 0.92 vs 0.61) and survives median-based midpoints. Within
the fiction/real probe the asymmetry is site-dependent: symmetric at the ' want' site
(0.43/0.40) but strongly asymmetric at the ' letter' site (0.90/0.33 — measured
against that site's own healthy reference amplitude of 1.18, though at n = 4 per
direction, exploratory). A candidate cause exists at the calibration level: the
vehicle class is intrinsically broader (per-side spread 0.83–0.91 versus 0.56–0.70 for
aquarium, at every layer probed) — transitions *into* the broader class park harder.
We flag this as a correlate, not a demonstrated mechanism (Fig. fig_s9_asymmetry).

## 3.3 The mechanism: drift plus discrete, state-triggered jumps (R3)

What process produces these trajectories? We fit five models per run to the twenty
post-shift readings — uniform integrator, fitted-γ recency integrator, change-point
step, drift-plus-step hybrid, and a two-timescale integrator (fast and slow components
mixed) — selecting by BIC with an indeterminacy band, and we calibrated the selector
on synthetic truth: hybrid-truth is recovered as hybrid in 13–15 of 24 simulations;
step-truth is called integrator in 0–2%; and critically, two-timescale truth
masquerades as a plain integrator or indeterminate, reading as hybrid in only 2–3 of
24. The selector cannot fabricate the hybrid verdict from any smooth mechanism.

The data return that verdict anyway: among classifiable runs, drift-plus-jump is
dominant — 11 of 16 tank runs and 14 of 25 fiction/real runs (48% of fiction/real
runs are indeterminate at that probe's noise level, and we state the claim as
"hybrid-dominant among classifiable runs" accordingly). The two-timescale model wins
zero runs in either probe (Fig. fig_s9_model_classes; per-run fits in
Fig. fig_r1_fit_gallery_tank; the raw paths in Fig. spaghetti_L4 show the
heterogeneity directly — some runs glide, some step). The two-phase shape of §3.2
could in principle have been smooth multi-timescale integration; tested head-to-head,
it is not.

The jumps are not triggered by strong evidence. Every post-shift sentence has a
single-sentence calibration reading (456 of 456 matched), and the sentences at which
runs jump are median-strength exemplars of their class — percentile 0.50 against 0.50
for all other added sentences (p = 0.445). The same evidence moves one run smoothly
and jolts another: whatever triggers a jump is a property of the state, not of the
stimulus — though we have tested only evidence strength; surprisal, syntax, and
discourse position remain untested, so "state-dependent" is our working
interpretation rather than a demonstrated exclusion.

The same process is visible from inside the stream. Using per-position axes
calibrated from no-shift checkpoint windows — content and position matched, only
history differing — the tokens of the post-shift block themselves read only about
half their no-shift reference: +0.34/+0.37 at ten post-shift sentences, +0.52/+0.53
at twenty (trimmed means; the untrimmed tank values are inflated by a heavy tail we
document in the QA appendix), replicated with a tighter instrument in the fiction/real
arm (Figs. fig_r2_within_stream, fig_s9_within_stream_fr). Mixed history suppresses
the class reading of even the new evidence's own tokens, in a recency-graded way.
This is descriptive — it is what token-level recency integration would produce — but
it establishes that the transition is not merely a summary-site phenomenon: any
window-level readout inherits the suppression.

## 3.4 Unresolved states, and what the model does in them (R4)

In one direction per probe, the trajectory does not merely travel slowly — it stops.
The tank aquarium→vehicle occupancy mode is stationary at mid-axis for at least ten
consecutive steps, at ≥2.9 band standard deviations from *both* endpoint references,
with flat variance; Gaussian-mixture comparison favors a single component in every
time band — a parked population, not a hidden mixture of resolved and unresolved runs
(Fig. fig_r2_mode_track). The same signature appears at the pre-lexical ' word' site,
at the ' letter' site in the fiction/real probe, and under the replicate carrier.
Geometrically, the parked states sit squarely inside the trajectory bundle (0.96× the
null distance — §3.6); functionally, they are a distinct condition, as the model's
behavior shows.

We generated completions at matched transition depths (k = 2, 6, 12, 20) for every
run. Behavior tracks the reading: cells whose readings sit on a side answer that side
(56% and 66% for the two sides), while the mid band answers "both" — enumerating the
two senses — in 45% of cells, roughly double either side (Fig. fig_r6_behavior_bands).
And here is the descriptive fact that anchors this paper's framing: **not one of the
96 tank responses asks which sense is meant or declines to answer pending
disambiguation** — zero of 96, by regex scan and by full manual categorization. In the
unresolved zone the model either enumerates senses (45%) or silently commits to one
(52% at mid-band); it answers as if resolved. One further response class — 11 of 108
including no-shift cells — consists of degenerate repetition loops, not band-linked.

When does the reading carry information *beyond* the context composition that drives
both reading and behavior? At matched composition: mid-transition, yes — pooling
k ∈ {6, 12}, decided answers come from runs with more extreme readings (median
|reading| 0.72 vs 0.38, one-sided p = 0.0138); at the settled extremes, no. In the
fiction/real arm the reading separates fiction-framed from safety responses at k = 2
(−0.06 vs +1.13, p = 0.010, one of four depths tested) but not later, where response
type follows scene family (Fig. fig_s9_behavior_matchedk). The safety-relevant
gradient is nonetheless plain at the band level: safe-completion rates run 50% →
80% → 91% as the reading moves from fiction-side through mid to real-side (origin
band n = 4, fragile). All behavioral claims here are correlational.

## 3.5 Order and equilibrium: hysteresis without stickiness (R5)

Does the order of evidence matter beyond its amount? We built static mixture sweeps:
twenty-sentence contexts with k destination-class sentences, k swept 0→20, in two
block orders, from each family's own transition sentences. The resulting loops are
large and unmistakable — the same mixture read with the destination block recent
versus old differs by loop areas of +14.4 [12.2, 16.8] (tank) and +10.5 [7.5, 13.3]
(fiction/real): operational hysteresis, plainly present (Fig. fig_r6_d6_loop_tank).

The reserved question was whether any of that order-dependence exceeds what recency
weighting alone produces. Answer: none of it. A one-parameter recency integrator
fitted to the sweep cells reproduces the loop areas almost exactly (+14.3; +11.1) —
excess "stickiness" of +0.1 and −0.5, both indistinguishable from zero — and
cross-order validation (fit one branch, predict the other) preserves the verdict. We
note, as part of the method, that our own first pass computed this against a
misspecified null (γ imported from the transition fits) and declared significant
stickiness; the fitted null killed the claim within the hour, and both versions are in
the corrections record. What remains real beyond the single-γ account is mild:
the two sweep directions prefer slightly different recency weights (γ 0.91/0.97 tank,
0.84/0.90 fiction/real), echoing the directional asymmetry of §3.2.

This resolves an apparent contradiction with §3.3. The *equilibrium map* from evidence
mixture to reading is smooth and integrator-like; the *sequential path* through a
transition is drift punctuated by jumps. Both are true; they are different
observables. The metastability this paper names is a property of paths, not of the
equilibrium map — there is no bistability to fall into, and nothing needed to escape.

## 3.6 The representation of irresolution (R6)

Finally, the geometric question the title poses: do these in-between states leave the
model's learned distribution? "Off-manifold" is meaningful only relative to a
reference, a measure, and a noise level, so we fix all three: reference — the
position-matched no-shift states (and the cross-run transition bundle); measures —
k-nearest-neighbor distance and out-of-subspace reconstruction residual against the
no-shift PCA subspace; noise level — the held-out self-distances of the reference
itself. The instruments demonstrably detect displacement: single-sentence calibration
states read 1.7–2.2× the null (a different context regime, correctly flagged), and
position-mismatched states are flagged at 13–44%.

At the individual-state level, nothing leaves. Jump steps read 1.06×/1.12× the null,
parked states 0.96×, all inside the null's spread (Fig. fig_r5_geometry). Our
pre-registered prediction that jump steps would show elevated off-manifold distance
failed, and we report it as failed.

The subtle result appeared only when the per-state verdict was challenged — the check
exists because one of us insisted that *even a little off-manifold is off-manifold*
[provenance: A.S.]. The *mean* out-of-subspace residual of transition states, against
a family-block bootstrap null, is unmistakably nonzero: a shared displacement equal to
**25% (tank) and 38% (fiction/real) of the full class separation**, p < 0.001 in both
probes, rising over the first five post-shift sentences and persisting undiminished to
twenty — largest at the park (Fig. fig_s9_shift_marker). It is not class leakage: the
direction is orthogonal both to the single-sentence class axis (cos +0.015, +0.011)
and, by construction and by measurement, to the accumulated-context class axis
(−0.0052, −0.0065). It survives held-out direction estimation (71–90% of in-sample
magnitude). It is not family novelty: no-shift-style cells from families *outside* the
reference construction sit lower on the marker (+1.6%/+3.4% of separation) than cells
from families inside it (+6.7%/+6.0%), the opposite of the novelty prediction, both
far below mixed cells (≈ +27%).

What is it? Held-out mixture cells locate its content: the marker is absent from
pure-class contexts, near its full transition strength in *static* mixed contexts —
so it marks mixed context, not temporal shifting per se — and, in the fiction/real
probe, it halves when the mixture is interleaved rather than blocked: there it partly
encodes coherent shift *structure*. It does not predict behavior at matched
composition. The model, in other words, maintains a persistent, learned representation
that its context is mixed — carried in a dedicated direction the no-shift world never
occupies — and does not act on it.

Three graded senses of "off-distribution" should be kept distinct: exotic natural
inputs, interventional states (patching, steering), and foreign regimes relative to
one another. Our shifts are the tamest possible case — clean block transitions between
two well-learned frames — and the fact that even the park stays on-distribution here
says nothing about adversarial or incoherent contexts, where genuine excursions remain
most likely; that battery is future work.
