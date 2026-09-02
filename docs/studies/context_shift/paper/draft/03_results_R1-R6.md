<!-- Section 3: Results. Structure pass (2 Sept 2026): roadmap paragraph; 3.2 reordered
(figure → crossing → remnant gap + Table 1 → checks → integration → depth + Table 2 →
asymmetry); Table 3 in 3.3; old 3.4 split into 3.4 (dwell) and 3.5 (behavior); order
and geometry renumbered 3.6 and 3.7. Repository labels (R1–R6) dropped from headings.
Checklist from the drafting pass retained: gap>1 explainer; correction-15 CI honesty;
trimmed within-stream values; fr indeterminate rate; matched-k framing; 0/96 counts
(s12); same-hour retraction named; off-manifold never bare + positive controls in-text;
both-axes orthogonality; family-novelty numbers; provenance credit; graded senses +
tamest case; all numbers from FINDINGS_FINAL. -->

# 3. Results

We first check the instrument: whether an interpretation can be read out at all, and
whether what we read is the intended contrast (§3.1). We then follow a reading through
a shift and ask how far it moves and how fast (§3.2), what kind of process moves it
(§3.3), what a trajectory looks like when it stops between the two interpretations
(§3.4), and what the model does while there (§3.5). Two boundary tests close the
section: whether the order of evidence adds anything beyond recency weighting (§3.6),
and whether any of these states leaves the model's ordinary geometry (§3.7).

## 3.1 The instrument reads a real contrast, and reads the right thing

Before any dynamics, two questions: can an interpretation be read out at all, and is
what we read the intended contrast rather than a topical shadow of it?

On the first: single-sentence calibration axes separate the classes with held-out
accuracy 0.905 (tank, layer 4) and 0.910 (fiction/real, layer 14), and axes refit on
accumulated forty-sentence contexts separate held-out families with accuracy 0.93–1.00
at every layer from 1 to 23, in both tasks. Under these per-layer accumulated-context
axes, no-shift runs read class-consistently across the entire depth of the stack (Fig.
fig_r3_heatmap_secondary_fr) — with the caveat, established in Methods, that the
fiction/real direction itself rotates with accumulation and must be refit at depth (Fig.
fig_r3_axis_rotation).

On the second, three independent discriminations. First, an identity-matched comparison:
the nine tokens of the tank carrier ("What is the meaning of the word tank?") appear
verbatim in every checkpoint window, so class signal can be compared across tokens with
identity held fixed. The signal concentrates overwhelmingly at the sense-bearing token —
d′ = 11.7 at ' tank' against a context-token median of 1.4 (Fig. fig_r2_carrier_dprime;
n = 6 runs per class, and we caution that orderings among the non-peak bars are not
interpretable at this n, since d′ divides by a pooled standard deviation that is small
for highly predictable tokens). Second, minimal pairs: 150 sentence pairs sharing most
content words while differing only in framing cues shift the reading by +0.99 axis units
— half the full class separation — with 95% of pairs in the predicted direction
(pair-level p = 2.5×10⁻²⁵; clustered by content domain — the conservative unit, six
domains — t(5) = 12.0, p = 7.2×10⁻⁵; positive in each of the three independently
generated batches of pairs; Fig. fig_s9_d5_pairs). Third, dose-independence: the effect
does not scale with the number of framing-cue words (r = 0.05), and is not a length
artifact (r = 0.02; length-matched pairs +1.05) — one cue moves the reading as far as
four: the response saturates at a single cue rather than accumulating.

The licensed claim is modest: the reading tracks framing cues with content held fixed —
not an abstract frame representation. The two tasks also differ instructively in
contrast structure. Tank's signal anchors to one token; the fiction/real signal is
spread across the request's content words (' write' 6.4, ' suicide' 6.2, ' want' 4.5,
against a context-token median of 3.6; Fig. fig_r6_carrier_dprime_fr). The d′ values are
not comparable across tasks, but the shape is: a lexical-sense contrast lives at a
token; a framing contrast lives across the utterance.

## 3.2 The shape of reinterpretation: gradual, partial, lingering

Figure fig_s9_collapse shows both transition directions, both tasks, at each task's
calibrated site (layers 4 and 14), against the no-shift references. After the shift,
readings cross the midpoint at per-run medians of 4 to 10 sentences depending on task
and direction (tank 10.5 and 6.0; fiction/real 4.0 and 5.0; a few runs never cross) —
but neither direction, in either task, reaches the opposite reference within twenty
counter-sentences.

How far short do they stop? The **remnant gap** measures the shortfall: the distance
between a run's plateau and the position-matched no-shift level, in axis units
measured from the midpoint of the two no-shift references (§2.5; Fig.
fig_r1_residual_gap). Both directions of both tasks show positive gaps under
family-clustered bootstrap (Table 1). The largest is tank aquarium→vehicle at +2.16
[1.87, 2.44] — equivalently 1.09× the no-shift amplitude, the distance from the class
midpoint to the matched reference; a shortfall larger than the amplitude itself means
this plateau sits at the class *midpoint*, the transition stopped at half-way.

**Table 1.** The remnant gap in both directions of both tasks: the destination
reference level (positions 36–40) minus the run plateau (post-shift sentences 16–20),
both midpoint-referenced, in axis units. Intervals are family-clustered bootstrap 95%
intervals over 2,000 draws; the second interval also resamples the six no-shift
reference families on every draw (Appendix A). The last column divides the gap by the
no-shift amplitude, the distance from the class midpoint to the matched reference.

| Transition | Gap | 95% CI, references fixed | 95% CI, references resampled | Gap / amplitude |
|---|---|---|---|---|
| tank, aquarium→vehicle | +2.16 | [1.87, 2.44] | [1.70, 2.62] | 1.09 |
| tank, vehicle→aquarium | +1.15 | [0.82, 1.45] | [0.77, 1.48] | 0.57 |
| fiction→real | +0.38 | [0.28, 0.49] | [0.27, 0.50] | 0.43 |
| real→fictional | +0.35 | [0.11, 0.58] | [−0.12, +0.79] | 0.40 |

One case demotes under a stricter bootstrap: when the uncertainty of the six-run
reference is propagated, three cases stand but real→fictional widens to
[−0.12, +0.79] and no longer excludes zero — that remnant is suggestive only. The gap
is not an artifact of weaker post-shift material: the post-shift sentences match the
no-shift runs' sentences in single-sentence calibration strength (percentile medians
0.51 vs 0.45 and 0.48 vs 0.49; p = 0.24, 0.90). Whether the remnant is truly
permanent or merely slower than twenty sentences can resolve is undecidable in this
corpus — the late slopes are shallow but nonzero in some runs — and deciding it is
the first item of future work.

The transition is two-phase in a specific sense: no single recency-weighted average
fits it. In both directions of both tasks the data sit above the best-fitting average
early and below it late, and the late shortfall is the remnant gap. The reading lags
the present frame on roughly the fitted recency timescale. The decay
parameters of §3.3's recency integrator (§2.5) have median γ = 0.90 in both
fiction/real directions and 0.94 in tank →aquarium — weighted-mean evidence ages of
about nine and fourteen sentences — while in tank →vehicle the median reaches 0.99:
weighting so close to uniform that the effective memory exceeds the window — the
dwell showing up inside the fit itself. Relative to an equal-weight average of all
evidence in the window, the mean trajectories run slightly *ahead* — the pattern a
recency weighting would produce; individual runs are heterogeneous around that mean.
What the data rule out is not lag but lag *in excess* of evidence integration.

The single-site view has depth structure behind it (Fig. fig_s13_collapse_layers
shows the collapse view at four layers per task; Fig. fig_r3_heatmap_secondary_fr and
supplementary heatmaps give all layers). In the fiction/real task the shallowest
layers cross almost immediately — within three to four sentences, and completely —
while mid-stack layers cross at medians of eight to thirteen. Tank crosses later
everywhere: its shallow band at medians of thirteen and eight, and in
aquarium→vehicle at median thirteen at every depth — the dwelling of §3.4 is
stack-wide there — while the reverse direction crosses earliest at depth (median
six). Our pre-stated prediction about the ordering of crossing times across layers
held in the fiction/real task and failed in tank (§5).

Where the stack ends up is more telling than when it crosses. Table 2 gives the
late-window means by depth band. In the last five sentences (destination-signed
means; regenerated by the committed layer script), fiction/real's layers 3–18 settle
at +0.3 to +0.4 of the reference in both directions and its shallowest layers at full
strength; tank aquarium→vehicle's shallow layers reach only +0.57, its layers 3–12 end
at +0.12, and its layers 13–23 at 0.00 to −0.10 — the dwelling direction's mid and
deep stack ends at the midpoint itself. The deepest band (layers 19–23) hovers near
the midpoint in one direction of each task (fiction→real +0.08; aquarium→vehicle
−0.10) while the reverse directions settle (+0.48; +0.42).

**Table 2.** Where each layer band ends up: mean reading over the last five post-shift
sentences (positions 36–40) under per-layer accumulated-context axes, signed so that
the destination class is positive, with class means at ±1 and the midpoint at 0.

| Layers | tank, aquarium→vehicle | tank, vehicle→aquarium | fiction→real | real→fictional |
|---|---|---|---|---|
| 0–2 | +0.57 | +1.03 | +0.99 | +1.14 |
| 3–12 | +0.12 | +0.30 | +0.41 | +0.32 |
| 13–18 | 0.00 | +0.38 | +0.41 | +0.33 |
| 19–23 | −0.10 | +0.42 | +0.08 | +0.48 |

**Direction matters, and the asymmetry is not an instrument accident.** Tank
transitions toward the vehicle sense fall 1.09 amplitude-fractions short versus 0.57 in
the reverse direction; the same pattern replicates under an independent carrier ("Define
the word tank.": 0.92 vs 0.61; the replicate's calibration axis is in-sample, not
held-out) and survives median-based midpoints. Within the fiction/real task the
asymmetry is site-dependent: symmetric at the ' want' site (0.43/0.40) but strongly
asymmetric at the ' letter' site of the paraphrase carrier "Help me write…" (0.90/0.33 —
against that site's own healthy reference amplitude of 1.18, though at n = 4 per
direction, exploratory). A candidate cause exists at the calibration level: the vehicle
class is intrinsically broader (per-side spread 0.83–0.91 versus 0.56–0.70 for aquarium,
at every layer tested) — transitions *into* the broader class stop farther short. We
flag this as a correlate, not a demonstrated mechanism (Fig. fig_s9_asymmetry).

## 3.3 The form of the dynamics: drift plus discrete jumps

What process produces these trajectories? We fit the four model forms of §2.5 per run to
the twenty post-shift readings — recency integrator (with the uniform, equal-weight
integrator as its γ = 1 case), change-point step, drift-plus-step hybrid, and
two-timescale integrator — selecting by BIC with an indeterminacy band, and we
calibrated the selector on synthetic truth (Table 3): hybrid-truth is recovered as
hybrid in 13–15 of 24 simulations; step-truth is called integrator in 0–2%; and
two-timescale truth masquerades as a plain integrator or indeterminate, reading as
hybrid in only 2–3 of 24. The selector cannot fabricate the hybrid verdict from any of
the smooth forms tested. This is a claim about the form of the trajectories, not their
implementation: it excludes smooth
integration of the evidence and establishes discrete changes in the reading; what
inside the network produces one is not identified here.

On the real runs the selector nonetheless returns hybrid: among classifiable runs,
drift-plus-jump is dominant — 11 of 16 tank runs and 14 of 25 fiction/real runs (48% of
fiction/real runs are indeterminate at that task's noise level, and we state the claim
as "hybrid-dominant among classifiable runs" accordingly). The two-timescale model wins
zero runs in either task (Fig. fig_s9_model_classes; per-run fits in Fig.
fig_r1_fit_gallery_tank; the raw paths in Fig. spaghetti_L4 show the heterogeneity
directly — some runs glide, some step). The two-phase shape of §3.2 could in principle
have been smooth multi-timescale integration; tested head-to-head, it is not.

**Table 3.** Per-run model selection by BIC on the real transition runs and on
synthetic runs of known type. A model wins a run only when its BIC leads the
runner-up by at least 2; otherwise the run is indeterminate. Synthetic runs: 24 per
task per truth type, pooled across the two tasks.

| Runs | Drift + step (hybrid) | Step | Recency integrator | Two-timescale | Indeterminate |
|---|---|---|---|---|---|
| tank (24 runs) | 11 | 2 | 3 | 0 | 8 |
| fiction/real (48 runs) | 14 | 7 | 4 | 0 | 23 |
| synthetic, hybrid truth (48) | 28 | 5 | 1 | 0 | 14 |
| synthetic, two-timescale truth (48) | 5 | 0 | 18 | 4 | 21 |
| synthetic, step truth (48) | 3 | 27 | 0 | 0 | 18 |

Jump timing is not predicted by evidence strength. Every post-shift sentence has a
single-sentence calibration reading (456 of 456 matched), and the sentences at which
runs jump are median-strength exemplars of their class — percentile 0.50 against 0.50
for all other added sentences (p = 0.445). The same-strength evidence moves one run smoothly and jolts another: what
differentiates a jump step is not the stimulus property we measured — though we
have tested only evidence strength — and single-sentence calibration
strength may understate in-context strength; surprisal, syntax, and discourse position
remain untested — so "state-dependent" is our working interpretation rather than a
demonstrated exclusion.

The same process is visible from inside the stream. Using per-position axes calibrated
from no-shift checkpoint windows — content and position matched, only history differing
— the tokens of the post-shift block themselves read only about half their no-shift
reference: +0.34/+0.37 (the two transition directions) at ten post-shift sentences,
+0.52/+0.53 at twenty (trimmed means; the untrimmed tank values are inflated by a heavy
tail we document in the QA appendix), replicated with a tighter instrument in the
fiction/real task (Figs. fig_r2_within_stream, fig_s9_within_stream_fr). Mixed history
suppresses the class reading of even the new evidence's own tokens, in a recency-graded
way. This is descriptive — it is what token-level recency integration would produce —
but it establishes that the transition is not merely a summary-site phenomenon: any
window-level readout inherits the suppression.

## 3.4 The dwelling within the unresolved zone

In one direction of the tank task — aquarium→vehicle — the trajectory dwells within the
unresolved zone: it becomes stationary mid-transition and, on the measured horizon, does
not leave. The central tendency of the run distribution is stationary at mid-axis for at
least ten consecutive steps, ≥2.9 across-run standard deviations from
*both* endpoint references, with the spread across runs flat rather than tightening;
Gaussian-mixture comparison favors a single component in every time bin — one stationary
population, not a hidden mixture of resolved and unresolved runs (Fig.
fig_r2_mode_track). Within tank, the same signature appears at the pre-lexical ' word'
site and under the replicate carrier; in the fiction/real task it appears only at the '
letter' site of the paraphrase carrier, at n = 4 per direction, exploratory.
"Stationary" is bounded by the horizon: whether these runs would ever complete on a
longer one is the same open question §3.2 leaves for the remnant, and some individual
runs retain shallow nonzero late slopes. Geometrically, the dwelling states sit squarely
inside the trajectory bundle — the spread of transition trajectories across runs — at
0.96× the null distance (§3.7); functionally, they are a distinct condition, as the
model's behavior shows.

## 3.5 What the model does in the unresolved zone

The dwelling states have a behavioral signature. We generated completions at matched
counts of post-shift sentences (k = 2, 6, 12, 20) for every run; all behavioral claims
in this subsection are correlational. For analysis we partition readings into three
bands — origin side, middle, destination side. Behavior tracks the reading: completions
whose readings sit on a side answer that side (56% and 66% for the two sides), while
the mid band answers "both" — enumerating the two senses — in 45% of mid-band
completions, roughly double either side (Fig. fig_r6_behavior_bands). One descriptive
fact anchors this paper's framing: **not one of the 96 tank responses asks which sense
is meant or declines to answer pending disambiguation** — zero of 96, by regex scan and
manual review of the committed categorized worksheet. In the unresolved zone the model
either enumerates senses (45%) or silently commits to one (52% at mid-band); it answers
as if resolved. One further response class appears across all 108 tank completions
(the 96 transition completions plus 12 no-shift completions): 11 are degenerate
repetition loops, unrelated to reading band.

When does the reading carry information *beyond* the context composition that drives
both reading and behavior? At matched composition: mid-transition, yes — pooling k ∈ {6,
12}, decided answers come from runs with more extreme readings (median
|reading| 0.72 vs 0.38, one-sided p = 0.0138 — a pooling chosen after the per-depth
pattern was seen, so we grade this suggestive); at the settled extremes, no. In the
fiction/real task we categorize each completion as fiction-framed assistance or a safety
response — a *safe-completion*, which addresses the request as a risk (declining the
letter, redirecting to support) rather than fulfilling it. The reading separates the two
at k = 2
(−0.06 vs +1.13, p = 0.010, one of four k values tested) but not later, where
response type follows scene family (Fig. fig_s9_behavior_matchedk).

The safety-relevant gradient is nonetheless plain at the band level: safe-completion rates run 50% → 80% →
91% as the reading moves from fiction-side through mid to real-side (origin band n = 4, fragile).

An exploratory post-freeze check (Appendix B) asks whether any other layer's
reading associates more strongly with behavior than the calibrated site's: per-layer
association curves (Fig. fig_s14_behavior_by_layer) are roughly flat from mid-stack to
the final layer in both tasks — nothing singles out the deep layers — though the
instrument is blunt (band-level, imbalanced outcomes), so this neither establishes nor
rules out depth-specific behavioral readout.

## 3.6 Order and equilibrium: hysteresis without stickiness

Does the order of evidence matter beyond its amount? We built static mixture sweeps:
twenty-sentence contexts with k destination-class sentences, k swept 0→20, in two block
orders, from each family's own transition sentences. The resulting loops are large — the
same mixture read with the destination block recent versus old differs by loop areas of
+14.4 [12.2, 16.8] (tank) and +10.5 [7.5, 13.3] (fiction/real): operational hysteresis,
plainly present (Fig. fig_r6_d6_loop_tank).

The reserved question was whether any of that order-dependence exceeds what recency
weighting alone produces — call any such excess *stickiness*. There is none: a
one-parameter recency integrator fitted to the sweep cells reproduces the loop areas
almost exactly (+14.3; +11.1) — excess "stickiness" of +0.1 and −0.5, both
indistinguishable from zero — and cross-order validation (fit one branch, predict the
other) preserves the verdict. An earlier pass computed this against a
misspecified null (γ imported from the transition fits) and found apparent
stickiness; the fitted null supersedes it (Appendix A). What remains real beyond the single-γ
account is mild: the two sweep directions prefer slightly different recency weights (γ
0.91/0.97 tank, 0.84/0.90 fiction/real), echoing the directional asymmetry of §3.2.

This resolves an apparent contradiction with §3.3. The *equilibrium map* from evidence
mixture to reading is smooth and integrator-like; the *sequential path* through a
transition is drift punctuated by jumps. Both are true; they are different observables.
The metastability this paper names is a property of paths, not of the equilibrium map —
there is no bistability to fall into and no barrier to escape.

## 3.7 The geometry of irresolution

Finally, the third of the introduction's three worlds: do these in-between states leave
the model's learned distribution? "Off-manifold" is meaningful only relative to a
reference, a measure, and a noise level, so we fix all three: reference — the
position-matched no-shift states (and the cross-run transition bundle); measures —
k-nearest-neighbor distance and out-of-subspace reconstruction error against the
no-shift PCA subspace; noise level — the held-out self-distances of the reference
itself. (Paired values in this section are tank/fiction-real throughout.) The
instruments detect real displacement: single-sentence calibration states — a genuinely
different context regime, serving as a positive control — read 1.7–2.2× the null across
the two instruments, and position-mismatched states are flagged at 13–44%.

At the individual-state level, nothing leaves the reference distribution. Jump steps
read 1.06×/1.12× the null, the stationary dwelling states 0.96×, all inside the null's
spread (Fig. fig_r5_geometry). Our pre-registered prediction that jump
steps would show elevated off-manifold distance failed.

The subtle result appeared only when the per-state verdict was challenged: a
displacement too small to flag any single state could still be shared by all of them, so
we tested the mean directly. The *mean* out-of-subspace reconstruction error of
transition states, against a family-block bootstrap null, is far outside the null's
range: a shared displacement equal to **25% and 38% of the full class separation**, p <
0.001 in both tasks, rising over the first five post-shift sentences and persisting
undiminished to twenty — largest in the stationary dwelling states (Fig.
fig_s9_shift_marker). We call the direction that carries it the
**mixed-context marker**. It is not class leakage: the
direction is orthogonal both to the single-sentence class axis (cos +0.015, +0.011) and,
by construction and by measurement, to the accumulated-context class axis (−0.0052,
−0.0065). It survives held-out direction estimation (71–90% of in-sample magnitude). It
is not family novelty: if the marker merely reflected unfamiliar scene families,
pure-class cells from families *outside* the reference construction should sit higher on
it than cells from familiar families; they sit lower (+1.6%/+3.4% of separation versus
+6.7%/+6.0%), and both sit far below mixed cells (≈ +27%).

What is it? Held-out mixture cells locate what elevates it: the marker is absent from
pure-class contexts and near its full transition strength in *static* mixed contexts —
so it marks mixed context, not temporal shifting per se. One qualification: in the
fiction/real task it halves when the mixture is interleaved rather than blocked, so there, part of
what elevates it is the coherent, blocked structure of the shift. It did not predict
behavior in eight matched-composition tests at the calibrated site and layer (one
nominal hit, uncorrected; other layers untested). The model, in other words, carries a
persistent, systematic signal that its context is mixed — a direction on which pure
contexts sit near zero and mixed contexts near 27% of the class separation — and its
behavior does not appear to use it. Whether this signal is a learned representation of
mixedness or a systematic consequence of heterogeneous input is not decided by our
measurements.

Three graded senses of "off-distribution" should be kept distinct: exotic natural
inputs; interventional states (patching, steering); and states of one context regime
measured against a reference built from another, as our single-sentence positive
controls are. Our shifts are the tamest possible case — clean block transitions between
two well-learned frames — and the fact that even the dwelling states stay
on-distribution here says nothing about adversarial or incoherent contexts, where
genuine excursions remain most likely; that battery is future work.
