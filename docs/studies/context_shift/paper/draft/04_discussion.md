<!-- Section 4: Discussion. Rewrite step 2 (2 Sept 2026). Grouped: what we found (the
term; typicality vs commitment) → what it means for safety (descriptive → trained
default → three candidate accounts → calibration → the unused signal) → connections
(human parallel; garden path or pun) → closing. All claims and numbers of the previous
version retained. -->

# 4. Discussion

**What "metastable" means here.** We take the term from the dynamics of biological
neural systems rather than from physics. In coordination dynamics and in the
winnerless-competition framework, two models of sequential transient dynamics in
neural populations, cognition is described as a sequence of transiently stable states
that are not fixed-point attractors [CITE: metastability in neural dynamics]. These
are structured passages through state space, in which dwelling and moving are not
opposites. That is the geometry our data show. A run that dwells mid-transition
occupies something functionally state-like: it is stationary for many steps and has
its own behavioral signature. Geometrically it is a passage, inside the trajectory
bundle and on a smooth equilibrium map. One disclaimer follows. Nothing here is
equilibrium bistability, since the map from evidence mixture to reading is smooth
(§3.6), and readers should not import a barrier-crossing picture. Semantic
metastability, as we use it, is a property of paths.

**Typicality is not commitment.** The three-worlds question of §1 dissolved because
it conflated two axes. On distributional typicality the stationary states are
unremarkable: inside the bundle, on-distribution. On semantic commitment they are
distinctive: uncommitted, between calibrated interpretations, with hedging as their
behavioral expression. A learned state of unresolvedness would be typical and
uncommitted at once. That is the profile the stationary states show, which is why the first two worlds of
§1, a learned state and a passage, were never alternatives. Genuinely off-distribution states, such as glitch inputs,
interventions, and adversarial incoherence, fall elsewhere on the typicality axis and
remain untested here. The general lesson is that a state can be geometrically typical
without being functionally normal. Our behavior data document the functional
difference.

**Safety and alignment, first descriptively.** The failure surface this study maps
needs no adversary. During an ordinary, coherent shift of conversational frame, a
model's reading of a critical token trails the present frame for roughly the fitted
recency timescale. Here that is nine to fourteen sentences, and effectively without
bound in the dwelling direction. It retains a remnant of the prior frame beyond that.
In one tank direction it dwells between frames for the remainder of the tested
horizon. The fiction/real task shows an exploratory echo of this, resting on 4 runs
per direction.

Behavior inside this window tracks the reading. Throughout, in the tank task, the
model never asks which reading is meant or flags the ambiguity as an obstacle. That
holds in zero of 96 completions across all bands. Even so, 45% of middle-band answers
surface both senses. And safeguard-relevant behavior co-varies with the internal
reading. Safe-completion rates fall from 91% to 50% across reading bands. The
fiction-side endpoint rests on four completions, and the gradient is partly
scene-driven (§3.5). This weakening is reachable by ordinary context, with no exotic
inputs required.

**A trained default for unresolved cases?** What follows is a post-hoc reading of an
asymmetry we noticed, not a designed manipulation, and training provenance is
unobservable. Our two tasks appear to differ in whether they carry a trained default
for unresolved cases. The covered fiction/real task behaved as though it does. In the middle reading
band, 80% of its completions safe-complete. In sampled chain-of-thought traces, both
framings are weighed before the safe reply. These traces are the reasoning channel
the chat format exposes, and we release them with our behavior data. That is a
qualitative observation, not a coded rate. The tank task showed no such default.
There the model silently commits: 52% of middle-band completions pick a sense. If
this reading is right, the unresolved zone is the failure window for every behavior
without a trained uncertainty-default, and refusal-style safeguards may be the
well-covered exception rather than the rule.

**Why the safeguard held: three candidate accounts.** Three accounts could explain why
the covered fiction/real task mostly safe-completed in the middle reading band, and
we cannot yet separate them. They are not exclusive: one is about what training
installed, one about what deeper layers see, one about where in the stack the trigger
reads. None is causally established. With two tasks these are observations. The
exploratory per-layer curves of §3.5 cannot separate them either. Shallow readings
saturate after the shift, which blinds that instrument in exactly the layers the
third account below points to.

*A trained default.* The first account is the reading above: the fiction/real task
carries a trained default for unresolved cases, and the tank task does not.

*Resolution at depth.* The second account emerged from the depth data, and it is
weaker than it first looked. In the fiction/real task, layers 3 to 18, the two middle bands, settle clearly on
the destination side in both directions, where the tank task from aquarium to
vehicle ends at the midpoint (§3.2). Downstream layers in the fiction/real task may
therefore act on a more settled reading than the site we measure. But the deepest
layer band hovers near the midpoint in the fictional-to-real direction too, the
direction in which safeguard behavior must appear, and did. Resolution at depth cannot carry the
explanation alone.

*An early, surface-keyed trigger.* The third account points the opposite way through
the stack. The shallowest layers resolve the framing composition almost immediately
and completely (§3.2), with the profile of surface-cue tracking. The minimal-pair test
that rules out cue-only tracking was run at the calibrated site, not at shallow
layers. A safeguard that reads early, from surface content and frame cues, would fire
whenever the alarming request is present and be suppressed only by a well-established
fictional frame. That is the shape of our behavioral data, including its fragile 50%
fiction-side floor. The fast, complete shallow response is specific to the
fiction/real task. The tank task's shallow layers respond later and, in one direction,
only partway (§3.2). That is what a trigger sculpted by safety post-training would
look like. But ordinary register statistics learned in pretraining predict the same
asymmetry, and training provenance is unobservable here. Patching shallow against
mid-stack states during generation is the decisive test (§5).

**One limit.** As a standalone monitor, predicting each response from its reading alone, the frame reading is not
yet usable: its AUC is 0.61 [0.43, 0.76], compatible with chance (Fig.
fig_s11_monitor_roc). The band-level gradient of §3.5 is real. A usable monitor would
combine several sites, the mixed-context marker, and per-layer readings. Building one
is future work, not a claim.

**A signal behavior does not appear to use.** The mixed-context marker gives the
sharpest form of the dissociation between what the model represents and what it does.
The model carries a persistent, systematic signal that its context is mixed, and its
behavior does not appear to use that signal when the mixture of frames in the context
is held fixed, at the one site and layer tested. This is the structure reported
in the hallucination literature, where models internally encode uncertainty or
truthfulness that their generations do not respect [CITE: internal encoding versus
expression]. Here it appears in transition dynamics. An internal signal correlated
with the conditions that produce the unresolved zone already exists inside the model,
and behavior does not appear to use it. Whether it could actually flag the zone is
untested; the one monitor we built, from the frame reading, is compatible with
chance. The motivating case of §1 reportedly had the same structure at system scale:
the provider's moderation layer was flagging the user's messages for self-harm risk
in real time while assistance continued [CITE: filing/reporting]. That suggests a
constructive direction for alignment work: test whether behavior can be gated on the
uncertainty signals already there, before building new ones.

**The human parallel.** The §3.2 signature is a partial reanalysis that leaves a
lingering trace of the initial misreading. That is also the signature of human
sentence processing in the "good-enough" tradition [CITE: good-enough processing]. After
recovering from a garden-path sentence, comprehenders measurably retain components of
the initial, incorrect interpretation. We make no mechanistic identification. We note
that a language model trained on human text reproduces, at the activation level, the
reanalysis profile humans show behaviorally, including the part where the old reading
never fully leaves.

**Garden path or pun.** In the terms of Dynel's account of garden-path humor [CITE:
Dynel], our transition corpus is a slow-motion garden path, and most trajectories treat it as one: incongruity, then resolution toward the
new reading. The dwelling runs are the interesting case. They form an extended
incongruity phase, in which the model, asked what the word means, answers like
someone explaining a pun: both senses, held. Whether any of them is a true pun, a
held incongruity that never resolves, or only a long garden path is the
persistent-versus-slow question our twenty-sentence horizon cannot decide. The
extended-tail experiment named in §5 is its dedicated test.

**Closing.** Word-sense reinterpretation is the tractable laboratory instance of a
much larger family. Frames, personas, tasks, and safety postures all shift under
accumulating context, and there is no obvious reason the metastable structure
documented here is unique to word senses. The states are what the title calls them:
unresolved. For now, so is the question of what a model should do while inside one.
