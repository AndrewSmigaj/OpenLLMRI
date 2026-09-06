<!-- Section 3: Results. Structure pass (2 Sept 2026): roadmap paragraph; 3.2 reordered
(figure → crossing → remnant gap + Table 2 → checks → integration → depth + Table 3 →
asymmetry); Table 4 in 3.3; old 3.4 split into 3.4 (dwell) and 3.5 (behavior); order
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
(§3.4), and what the model does while there (§3.5), where the behavioral question of §1
returns. Two boundary tests close the section: whether the order of evidence adds anything beyond recency weighting (§3.6),
and whether any of these states leaves the model's ordinary geometry (§3.7).

## 3.1 The instrument reads a real contrast, and reads the right thing

Before any dynamics, two questions. Can an interpretation be read out at all? And is
what we read the intended contrast, rather than the topical vocabulary that usually
accompanies it?

On the first question, the axes separate the classes at the calibrated sites and at
every depth. Single-sentence calibration axes reach held-out accuracy 0.905 in the
tank task (layer 4) and 0.910 in the fiction/real task (layer 14). Axes refit on
accumulated forty-sentence contexts separate held-out families with accuracy
0.93–1.00 at every layer from 1 to 23, in both tasks. Layer 0, the embedding output,
is lower: 0.88 in tank and 0.73 in fiction/real. Under these per-layer
accumulated-context axes, no-shift runs read on their own class's side at every layer
(Figs. fig_r3_heatmap_secondary_tank, fig_r3_heatmap_secondary_fr). One caveat from Methods
applies: the fiction/real direction itself rotates with accumulation and must be
refit at depth (Fig. fig_r3_axis_rotation).

On the second question we have three independent tests: one on the tank task, and
two on the fiction/real task, whose contrast has no single token to anchor to.

The first is an identity-matched comparison. The tank carrier is "What is the meaning of the word tank?" Its nine tokens appear verbatim in every checkpoint capture, so class signal can be compared across tokens
with token identity held fixed. We measure the class signal at each token as d′, the difference of class means
divided by the pooled standard deviation, from signal detection theory [CITE: Green
& Swets 1966]. The signal concentrates at the sense-bearing token: d′ = 11.7 at
' tank', against a context-token median of 1.4 (Fig. fig_r2_carrier_dprime). This comparison rests on 6 runs per class. Orderings
among the other tokens are not interpretable at that n. A pooled standard deviation
estimated from 6 runs is itself noisy, and d′ divides by it, so a token whose spread
happens to come out small prints a tall bar at a modest mean shift.

The second is a minimal-pair test. For the fiction/real task we wrote 150 sentence
pairs that share most content words and differ only in framing cues. One pair reads
"In the third draft, Mara finally tells her sister she is leaving Cleveland before
the lease renews." against "Last night, Mara finally told her sister she is leaving
Cleveland before the lease renews.", each followed by the carrier. The framing cues
alone shift the reading by +0.99 axis units, half the full class separation, and 95%
of pairs move in the predicted direction (Fig. fig_s9_d5_pairs). The effect is
positive in each of three independently generated batches of pairs, and it holds when
the six content domains the pairs were written in, rather than the pairs, are taken as
the unit of analysis. The statistics are in the caption.

The third is dose-independence. The effect does not grow with the
number of framing-cue words, and it is not a length artifact; both correlations are
near zero (Fig. fig_s9_d5_pairs). One cue moves the reading as far as four. The
response saturates at a single cue rather than accumulating.

The licensed claim is modest: the reading tracks framing cues with content held
fixed. The reading is not shown to track an abstract representation of the frame.

The two tasks differ in where the contrast lives. The tank signal anchors to one
token. The fiction/real signal is spread over several of the request's content words:
' write', ' suicide', and the measured ' want' token all read above the context-token
median (Fig. fig_r6_carrier_dprime_fr; values in the caption). The d′ values are not
comparable across tasks, since they are computed at different layers against
different context-token baselines and, with 6 runs per class, are unstable as point
estimates. The shape is comparable. A lexical-sense contrast
lives at a token. A framing contrast lives across the utterance.

## 3.2 The shape of reinterpretation: gradual, partial, lingering

How far does a reading move after the evidence changes sides, and how fast? Figure
fig_s9_collapse shows both directions of both tasks at the calibrated sites, against
the no-shift references. After the shift the reading crosses the midpoint within a
median of 4 to 10.5 sentences, depending on the task and direction (Table 2). A few
runs never cross. The mean trajectories in Figure fig_s9_collapse cross later than the
median run in the tank task, because runs that cross late or never pull the mean
down. In neither task and neither direction does the reading reach the
opposite reference within the twenty sentences after the shift.

How far short do they stop? The **remnant gap** measures the shortfall. It is the
no-shift reference level minus the run's plateau, both over the last five post-shift
sentences and both measured from the midpoint between the two references (§2.5;
Fig. fig_r1_residual_gap). With the references held fixed, the gap is positive in both directions of both
tasks under the family-clustered bootstrap (Table 2). The largest is in the tank task from
aquarium to vehicle, where the gap is 1.09 times the no-shift amplitude, the distance
from the midpoint to the matched reference. Within the interval's precision, that plateau sits at the midpoint: the transition
stopped halfway.

**Table 2.** The transition in numbers, for both directions of both tasks. Crossing:
the per-run median number of post-shift sentences before the reading crosses the
midpoint. Decay: the median fitted γ of the recency integrator (§2.5). Remnant gap:
the no-shift reference level minus the run plateau, both over positions 36–40 and
both measured from the midpoint, in axis units, with family-clustered bootstrap 95%
intervals over 2,000 draws; the second interval also resamples the six no-shift
reference runs of the destination class on every draw (Appendix A). The last column divides the gap by the
no-shift amplitude, the distance from the midpoint to the matched reference.

| Transition | Crossing (median sentences) | Decay γ (median) | Remnant gap | 95% CI, references fixed | 95% CI, references resampled | Gap / amplitude |
|---|---|---|---|---|---|---|
| tank, aquarium→vehicle | 10.5 | 0.99 | +2.16 | [1.87, 2.44] | [1.70, 2.62] | 1.09 |
| tank, vehicle→aquarium | 6.0 | 0.94 | +1.15 | [0.82, 1.45] | [0.77, 1.48] | 0.57 |
| fiction-writing→real-world | 4.0 | 0.90 | +0.38 | [0.28, 0.49] | [0.27, 0.50] | 0.43 |
| real-world→fiction-writing | 5.0 | 0.90 | +0.35 | [0.11, 0.58] | [−0.12, +0.79] | 0.40 |

Three checks bear on the gap. First, one case weakens under a stricter bootstrap.
When the six no-shift reference runs of the destination class are also resampled, three gaps still
exclude zero, but the real-world to fiction-writing interval widens to [−0.12, +0.79] (Table 2), so
that remnant is suggestive only. Second, the mundane rival is that the post-shift evidence is simply weaker. In the
tank task, where we checked, it is not. We ranked each sentence's single-sentence reading as a percentile
within its class's calibration set. The post-shift sentences match the no-shift sentences. From aquarium to vehicle
the median percentiles are 0.51 against 0.45 (p = 0.24). From vehicle to aquarium they are 0.48 against 0.49 (p = 0.90). And no-shift runs
built from the same class pools, with no prior frame to overcome, read at the
reference level, so the shortfall belongs to the history, not the material. Third, whether the remnant
is permanent or only slower than twenty sentences can resolve is undecidable in this
corpus. The late slopes are shallow but nonzero in some runs. Deciding it is the first
item of future work (§5).

Is the lag simply evidence integration? The transition is two-phase in a specific
sense: no single recency-weighted average fits it. Signed toward the destination, the data in both directions of both tasks run ahead
of the best-fitting average early and behind it late, and the late shortfall is the
remnant gap. The reading lags the present frame on roughly the
fitted recency timescale. The fitted decay parameters (Table 2) correspond to
weighted-mean evidence ages of about nine sentences in the fiction/real task and
fourteen in the tank task from vehicle to aquarium. From aquarium to vehicle the
fitted weighting is so close to uniform that the effective memory exceeds the window.
The stop near the midpoint, the dwelling of §3.4, shows up inside the fit itself. Relative to an equal-weight average of all
evidence in the window, the mean trajectories run slightly ahead, which is the
pattern a recency weighting would produce, and individual runs are heterogeneous
around that mean. The crossing delay is no longer than evidence integration predicts. What integration
does not explain is the late shortfall. Whether the path itself is smooth
integration is a separate question, tested head-to-head in §3.3.

Behind the single-site view there is depth structure. The depth analyses are exploratory. Crossing times by depth are measured under each layer's
accumulated-context axis (§2.4), so they differ from the calibrated-axis values of
Table 2 even at the calibrated layers. We group the layers into four bands: 0–2,
3–12, 13–18, and 19–23 (Table 3). Figure fig_s13_collapse_layers repeats Figure
fig_s9_collapse at five layers per task, and Figs. fig_r3_heatmap_secondary_tank, fig_r3_heatmap_secondary_fr give all layers. In the fiction/real task, layers 0 to 2
cross almost immediately, within three to four sentences, and completely, while
layers 3 to 18 cross at medians of eight to thirteen sentences. The tank task crosses
later everywhere. Its layers 0 to 2 cross at medians of thirteen and eight sentences
in the two directions. From aquarium to vehicle it crosses at a median of thirteen in
every band, so the stop near the midpoint spans the whole stack there. From vehicle
to aquarium it crosses earliest in the deepest band, at a median of six. Before
computing these values we predicted that layers 5 to 9 would cross later than layers
10 to 17, with the deepest layers in between. That held in the fiction/real task and
failed in the tank task (§5).

Where does each layer end up? Table 3 gives the mean reading over the last five
post-shift sentences by band, signed so that the destination class is positive. In
the fiction/real task, layers 3 to 18 settle at about +0.3 to +0.4 of the way to the
reference in both directions, and layers 0 to 2 settle fully. In the tank task from
aquarium to vehicle, layers 0 to 2 settle only partway, and every band below them
ends at or near the midpoint. The deepest band, layers 19 to 23, hovers near the midpoint in one direction
of each task, fiction-writing to real-world at +0.08 and aquarium to vehicle at −0.10, while the
reverse directions settle partway.

**Table 3.** Where each layer band ends up: the mean reading over the last five
post-shift sentences (positions 36–40) under per-layer accumulated-context axes,
averaged over the layers in each band and signed so that the destination class is
positive. Under these axes the no-shift references sit at ±1 and the midpoint at 0,
so a value is the fraction of the way from the midpoint to the destination reference.

| Layers | tank, aquarium→vehicle | tank, vehicle→aquarium | fiction-writing→real-world | real-world→fiction-writing |
|---|---|---|---|---|
| 0–2 | +0.57 | +1.03 | +0.99 | +1.14 |
| 3–12 | +0.12 | +0.30 | +0.41 | +0.32 |
| 13–18 | 0.00 | +0.38 | +0.41 | +0.33 |
| 19–23 | −0.10 | +0.42 | +0.08 | +0.48 |

Direction matters, and the asymmetry survives a change of carrier and a change of
midpoint definition. In the tank task,
transitions toward the vehicle sense stop about twice as far short as transitions
toward the aquarium sense: gap-to-amplitude ratios of 1.09 against 0.57 (Table 2). The same pattern replicates under the independent carrier "Define the word tank.",
at 0.92 against 0.61 (Fig. fig_s9_asymmetry). It also survives median-based
midpoints, which leave both tank gaps unchanged. The replicate
carrier's calibration axis is in-sample, not held-out. Within the fiction/real task
the asymmetry depends on the site. At the ' want' site the two directions are
symmetric. At the ' letter' site of the paraphrase carrier "Help me write…" they are
strongly asymmetric. That comparison rests on 4 runs per direction and is
exploratory. A candidate cause exists at the calibration level. The vehicle class is intrinsically broader than the aquarium class at every layer
tested, with a per-class spread of 0.83–0.91 against 0.56–0.70, and transitions into
the broader class stop farther short. The ' letter'
site, where the two classes are alike in spread, does not fit this account, but with
4 runs per direction it cannot test it. We flag the breadth account as a correlate,
not a demonstrated cause.

## 3.3 The form of the dynamics: drift plus discrete jumps

What process produces these trajectories? We fit the four model forms of §2.5 to each
run's twenty post-shift readings: the recency integrator, the change-point step, the
drift-plus-step hybrid, and the two-timescale integrator. We select by BIC with an
indeterminacy band. Before reading the real runs we calibrated the selector on
synthetic runs of known type (Table 4). Hybrid truth is recovered as hybrid in 28 of 48 simulations. Step truth is never
called integrator, 0 of 48, and is called hybrid in only 3 of 48, so the selector
does not mistake a discrete change for smooth integration. Two-timescale truth is
called hybrid in only 5 of 48, so hybrid dominance cannot come from a smooth truth
(Table 4).

On the real runs the selector favors the hybrid. Among classifiable runs, those where BIC gave a clear winner, the hybrid is
dominant: 11 of the 16 classifiable tank runs and 14 of the 25 classifiable
fiction/real runs (Table 4). In the fiction/real task, whose readings are noisier, 23
of 48 runs are indeterminate, so we state the claim as hybrid-dominant among
classifiable runs. The two-timescale model wins zero runs in either task (Fig.
fig_s9_model_classes). Per-run fits are shown in Fig. fig_r1_fit_gallery_tank, and the
raw paths in Fig. spaghetti_L4 show the heterogeneity directly: some runs glide, some
step. The two-phase shape of §3.2 could in principle have been smooth multi-timescale
integration. The head-to-head fit rejects it. The hybrid verdict is a claim about the
form of the trajectories, not about their implementation. It excludes smooth
integration of the evidence and establishes discrete changes in the reading. What
inside the network produces such a change is not identified here.

**Table 4.** Per-run model selection by BIC on the real transition runs and on
synthetic runs of known type. A model wins a run only when its BIC leads the
runner-up by at least 2; otherwise the run is indeterminate, and the classifiable
runs are the rest. Synthetic runs: 24 per task per truth type, pooled across the two
tasks; per task, hybrid truth was recovered as hybrid in 13 and 15 of 24, and
two-timescale truth read as hybrid in 2 and 3 of 24.

| Runs | Drift + step (hybrid) | Step | Recency integrator | Two-timescale | Indeterminate | Classifiable |
|---|---|---|---|---|---|---|
| tank (24 runs) | 11 | 2 | 3 | 0 | 8 | 16 |
| fiction/real (48 runs) | 14 | 7 | 4 | 0 | 23 | 25 |
| synthetic, hybrid truth (48) | 28 | 5 | 1 | 0 | 14 | 34 |
| synthetic, two-timescale truth (48) | 5 | 0 | 18 | 4 | 21 | 27 |
| synthetic, step truth (48) | 3 | 27 | 0 | 0 | 18 | 30 |

Jump timing is not predicted by evidence strength. In runs where the largest single
step carries more than half the net change, we call the sentence arriving at that
step the run's jump sentence. We rank each added sentence's single-sentence reading
as a percentile within its class's calibration set. Steps are taken between consecutive post-shift readings, so the first post-shift
sentence has none. In the tank task, 456 added sentences enter this test, 19 per run
across 24 runs, and all have such a reading. The jump sentences are median-strength exemplars of
their class: percentile 0.50, against 0.50 for all other added sentences
(Mann–Whitney p = 0.445). The same evidence strength produces a jump in one run and
not in another. What differentiates a jump is therefore not
the stimulus property we measured. We have tested only evidence strength, and
single-sentence calibration strength may understate in-context strength. Surprisal,
syntax, and discourse position remain untested. Our working interpretation is that
jump timing depends on the run's internal state rather than on the sentence. We call
this state-dependent. It is an interpretation. The untested sentence properties have not been excluded.

The context tokens themselves show the transition. Using per-position axes calibrated
from no-shift checkpoint windows, so that content and position are matched and only
the history differs, we read the tokens of the post-shift block. They read about a
third to a half of their no-shift reference at ten post-shift sentences, and about
half to two-thirds at twenty (Figs. fig_r2_within_stream, fig_s9_within_stream_fr;
values in the captions). The tank values are trimmed means, because the untrimmed
values are inflated by a heavy tail (Appendix A). The fiction/real task
replicates the pattern with a tighter instrument. Mixed history suppresses the class
reading of even the new evidence's own tokens, in a recency-graded way. This is
descriptive: it is what token-level recency integration would produce. It shows that
the transition is present in the context tokens as well as at the calibrated site.
Any readout that averages over a window of context tokens inherits the suppression.

## 3.4 The dwelling within the unresolved zone

Does any trajectory stop between the two interpretations rather than merely slow
down? One does. In the tank task from aquarium to vehicle, the trajectory dwells
within the unresolved zone: it becomes stationary mid-transition and, on the measured
horizon, does not leave. Figure fig_r2_mode_track tracks the mode of the run
distribution by post-shift band. The mode is stationary at the midpoint for at least
ten consecutive steps, and it sits at least 2.9 across-run standard deviations from
both endpoint references. The spread across runs stays flat rather than tightening. A one-component fit beats a two-component fit in every time bin, so this is one
stationary population, not a hidden mixture of resolved and unresolved runs. The
stationarity is a property of the population, not of each run. Over the last ten
post-shift sentences the family-clustered mean late slope lies within −0.040 and
+0.024 axis units per sentence, under a fifth of the no-shift amplitude across the
whole window, and the median late reading sits at −0.11, at the midpoint. But
individual late slopes range from −0.09 to +0.09 units per sentence, and only 3 of
the 12 runs are individually flat by a criterion fixed before computing (slope
within ±0.02 and at least half the window in the middle band). In the reverse
direction the population is still moving, with a late slope bounded away from
zero at +0.025 to +0.133.

The signature replicates within the tank task and barely appears in the other.
Within tank it appears at the ' word' site, the token just before ' tank' in the
carrier, and under the replicate
carrier "Define the word tank." (§2.3). In the fiction/real task it appears only at
the ' letter' site of the paraphrase carrier "Help me write a suicide letter.", with 4
runs per direction, and we treat that as exploratory.

Two qualifications bound the claim. "Stationary" is bounded by the horizon: whether
these runs would ever complete on a longer one is the same open question §3.2 leaves
for the remnant, and some individual runs retain shallow nonzero late slopes. And
geometrically the dwelling states are unremarkable. They sit inside the trajectory bundle, the spread of transition trajectories across
runs, at 0.96 times the null distance, the typical distance among held-out reference
states that §3.7 uses as its baseline. Functionally they are a distinct condition, as the model's behavior
shows next.

## 3.5 What the model does in the unresolved zone

What does the model say while its reading sits between the two interpretations? We
generated a completion from every run at four points after the shift: after 2, 6,
12, and 20 post-shift sentences. All behavioral claims in this subsection are
correlational. For analysis we partition readings into three bands, one side, the middle, and the other side (Fig. fig_r6_behavior_bands).

A first result is that the model often does not answer at all. Under the greedy
decoding used here, 14 of the 108 tank outputs and 85 of the 204 fiction/real
outputs never leave the reasoning channel. They repeat one sentence to the cap, cycle through one
sentence frame with a changing noun, or re-read the passage without concluding. No
cap would finish them. We call these "no answer" and report every rate below both with them counted and
over delivered answers only. Deployed decoding samples rather than taking the
greedy token, which is what breaks such loops, so their frequency in use is
untested (§5).

In the tank task, behavior tracks the reading. Completions whose reading sits on
the aquarium side answer with the aquarium sense in 52% of cases, 62% of those that
answer. On the vehicle side the vehicle sense is given in 59%, 63% of those that
answer. The middle band lists both senses in 45% of its completions, 52% of those
that answer, and commits to one sense in 42%, 48% of those that answer. None of the
94 delivered tank answers asks which sense is meant or declines to answer pending
disambiguation, by manual review and regular-expression scan of the committed
table. In the unresolved zone the model either lists both senses or commits to
one. It answers as if resolved.

Does the reading carry information beyond the context composition that drives both
reading and behavior? We test this at matched composition, comparing completions
generated after the same number of post-shift sentences (Fig.
fig_s9_behavior_matchedk). The evidence is thin. At 6 post-shift sentences, decided
answers come from runs with more extreme readings, with a median absolute reading of
0.90 against 0.38 for hedged or absent answers (one-sided p = 0.037); at 12 sentences
they do not (0.53 against 0.56), the pooled test over both counts, fixed in advance, gives p = 0.10,
and at the settled extremes there is no difference. We report it as one significant
count of four and claim nothing further.

In the fiction/real task we categorize each delivered answer as fiction-writing
assistance, which takes up the fiction-writing frame and helps with the letter or
the manuscript, or a safe completion, which declines the letter or redirects to
support. No delivered answer mixes the two. Of the 119 delivered answers, 111 are
safe completions, 95 of them redirecting to support and 16 only declining, and 8
are fiction-writing assistance. Read over delivered answers, the safeguard holds
across the reading bands: safe completions are 89% of the middle band's delivered
answers and 95% of the real-world side's, and the fiction-writing side delivers one
answer in four, a safe completion (Fig. fig_r6_behavior_bands, top right).

The reasoning channel tells the other half. Its final commitment matches the
delivered answer in every one of the 119 cells that answered, so where an answer
arrives the channel is expressed, not overridden. By band, the channel commits to a safe completion in 91% of the real-world side's
cells, 82% of the middle band's, and 2 of 4 on the fiction-writing side (Fig.
fig_r6_behavior_bands, bottom right). Neither reading shows a band difference the
sample can distinguish from none: for the reasoning channel the family-clustered
interval on the real-world-minus-middle difference runs from −0.07 to +0.23
(Fisher p = 0.14), and for delivered answers from −0.07 to +0.18 (p = 0.38). The difference between the two panels is
the loops. Reasoning that commits to fiction-writing assistance loops in 15 of 23 cells,
safety-committed reasoning in 70 of 181, a difference of +0.27 with a
family-clustered interval of +0.16 to +0.38 (Fisher exact p = 0.023), and no
fiction-writing-committed reasoning ever delivers a safe completion. So the two
panels bracket what a user would see: delivered answers bound the safe rate from
above, and the reasoning's commitments, which are what the loops would resolve to
if they completed as committed, bound it from below. Where in that bracket the
model sits under the sampling it is used with is the first item of future work
(§5).

None of the 119 delivered fiction/real answers asks whether the request belongs to
fiction writing or to the speaker's real circumstances. One assumes the story frame and ends by inviting correction. In
the reasoning channels, one proposes asking whether the request is for a story and
one proposes asking the letter's purpose, and neither question is delivered. Two
float a clarifying question and drop it, and seven safe completions plan to ask
whether the user is safe. So the task with a safeguard surfaces the question no
more than the tank task does. At matched composition the reading does not clearly separate the two response
types: at 2 post-shift sentences the medians are +0.06 for fiction-writing
assistance and +0.99 for safe completions, 3 answers against 26 (p = 0.065), and
at later counts they do not differ.

An exploratory check asks whether any
other layer's reading associates more strongly with behavior than the calibrated
site's. Per-layer association curves (Fig. fig_s14_behavior_by_layer), computed
over delivered answers, are roughly flat from mid-stack to the final layer in both
tasks. Nothing singles out the deep layers. The instrument is blunt, a band-level
association with imbalanced outcomes, so this neither establishes nor rules out a
depth-specific behavioral readout.

## 3.6 Order and equilibrium: hysteresis without stickiness

Does the order of evidence matter beyond its amount? To ask this we built static
mixture sweeps: twenty-sentence contexts holding k destination-class sentences, with
k swept from 0 to 20, in two block orders, using each family's own transition
sentences. The resulting loops are large. The same mixture reads differently depending on block order, with a loop area of
+14.4 [12.2, 16.8] in the tank task (Fig. fig_r6_d6_loop_tank) and a comparable one
in fiction/real (Table 5).
Operational hysteresis is plainly present.

The open question was whether any of that order dependence exceeds what recency
weighting alone produces. We call any such excess *stickiness*. There is none. A
one-parameter recency integrator fitted to the sweep cells reproduces the loop areas
almost exactly, and the excess is indistinguishable from zero in both tasks (Table 5).
Cross-order validation preserves the verdict: fitting one branch predicts the other. A null that imports γ from the transition fits instead of fitting it to the sweep
cells shows apparent stickiness. The fitted null supersedes it (Appendix A).
What remains beyond the one-parameter integrator is mild. The two sweep
directions prefer slightly different recency weights, echoing the directional
asymmetry of §3.2.

**Table 5.** Hysteresis in the static mixture sweeps. Loop area is the area between
the two block-order branches of the sweep, in axis units times sentences, with a
family-clustered bootstrap 95% interval. The fitted loop area comes from a
one-parameter recency integrator fitted to the same cells; the excess is the
observed area minus the fitted area. The last column gives the recency weight γ
fitted separately to each block order, with the destination block placed first or
last in the context.

| Task | Observed loop area | Fitted integrator loop area | Excess (stickiness) | γ, destination block first / last |
|---|---|---|---|---|
| tank | +14.4 [12.2, 16.8] | +14.3 | +0.1, not significant | 0.91 / 0.97 |
| fiction/real | +10.5 [7.5, 13.3] | +11.1 | −0.5, not significant | 0.90 / 0.84 |

This resolves an apparent contradiction with §3.3. The equilibrium map from evidence
mixture to reading is smooth and integrator-like. The sequential path through a
transition is drift punctuated by jumps. Both are true. They are different
observables. The metastability this paper names is a property of paths, not of the
equilibrium map. There is no bistable equilibrium and no barrier between states.

## 3.7 The geometry of irresolution

Finally, the third of the introduction's three worlds: do these in-between states
leave the model's learned distribution? "Off-manifold" is meaningful only relative to
a reference, a measure, and a noise level, so we fix all three. The reference is the position-matched no-shift states, together with the trajectory bundle of §3.4, the pooled set of transition-run states
across all runs. The measures are two standard novelty scores: the distance to the nearest neighbors
in the reference [CITE: k-nearest-neighbor out-of-distribution scoring, e.g. Sun et
al. 2022] and the reconstruction error of a state against the principal-component
subspace of the no-shift states [CITE: PCA reconstruction error as a novelty score,
e.g. Jackson & Mudholkar 1979]. The noise level, which we call the null, is the held-out self-distance of the
reference itself.
Throughout this section, paired values are for the tank and fiction/real tasks in
that order. The instruments detect real displacement. Single-sentence calibration states read 1.7 to 2.2 times the null across the two
instruments. They are a genuinely different context regime and serve as a positive
control. No-shift states compared against the reference of a different position,
which we call position-mismatched, are flagged as displaced in 13% to 44% of cases.

At the level of individual states, nothing leaves the reference distribution. Jump steps read 1.06 and 1.12 times the null (Fig. fig_r5_geometry). The dwelling
states read 0.96 times. All three sit inside the null's spread. Our pre-registered
prediction that jump steps would show elevated off-manifold distance failed.

A displacement too small to flag any single state could still be shared by all of
them, so we tested the mean directly. The mean out-of-subspace reconstruction error of transition states
is far outside the range of a null built by resampling whole scene families, the
family-clustered bootstrap of §2.5 (Fig. fig_s9_shift_marker).
It is a shared displacement equal to 25% and 38% of the full class separation, with
p < 0.001 in both tasks. It rises over the first five post-shift sentences and persists
undiminished to twenty, and it is largest in the stationary dwelling states. We call
the direction that carries it the **mixed-context marker**.

Three checks say what the marker is not (Table 6). It is not class leakage: the
direction is orthogonal to the single-sentence class axis and, by construction and by
measurement, to the accumulated-context class axis. It survives held-out direction estimation, in which the direction is estimated on
half the families and the magnitude measured on the other half. It retains 71% to
76% of its in-sample magnitude in the tank task and 87% to 90% in fiction/real. And it is not family
novelty. If the marker merely reflected unfamiliar scene families, pure-class cells
from families outside the reference construction should sit higher on it than cells
from familiar families. They sit lower, and both sit far below mixed cells.

**Table 6.** The mixed-context marker and its checks. Values are for the tank and
fiction/real tasks. The displacement rows are in percent of the full class
separation; the cosine rows measure the marker direction against the two class axes.

| Quantity | tank | fiction/real |
|---|---|---|
| Shared displacement of transition states | 25% | 38% |
| Cosine with the single-sentence class axis | +0.015 | +0.011 |
| Cosine with the accumulated-context class axis | −0.0052 | −0.0065 |
| Retained under held-out direction estimation | 71–76% | 87–90% |
| Pure-class cells from families outside the reference construction | +1.6% | +3.4% |
| Pure-class cells from familiar families | +6.7% | +6.0% |
| Mixed cells | ≈ +27% | ≈ +27% |

What is it? Held-out mixture cells, cells of the static sweeps that were not used to
construct the marker, locate what elevates it. The marker is absent from pure-class contexts. In static mixed contexts it is near
its full transition strength in the tank task and about 70% of it in fiction/real
(Table 6), so it marks mixed context, not temporal shifting as such. Those cells were all
captured on one day, so the separation between pure and mixed cells cannot be a
capture-day effect (§2.1). One qualification: in the
fiction/real task it halves when the mixture is interleaved rather than blocked, so
there, part of what elevates it is the coherent, blocked structure of the shift. It did not predict behavior in eight matched-composition tests at the calibrated
site and layer, with one nominal hit, uncorrected. Those tests used the categories of the superseded 256-token pass and were not
repeated. Other
layers are untested. The model,
in other words, carries a persistent, systematic signal that its context is mixed: a
direction on which pure contexts sit near zero and mixed contexts near 27% of the
class separation. Its behavior does not appear to use it. Whether this signal is
a learned representation of mixedness or a systematic consequence of heterogeneous
input is not decided by our measurements.

Three graded senses of what we have called off-manifold, or more broadly
off-distribution, should be kept distinct. The first is
exotic natural inputs. The second is interventional states, such as patching and
steering. The third is states of one context regime measured against a reference
built from another, as our single-sentence positive controls are. Our shifts are the tamest possible case, clean
block transitions between two well-learned frames. That even the dwelling states stay
on-distribution here says nothing about adversarial or incoherent contexts, where
genuine excursions remain most likely. That battery is future work.
