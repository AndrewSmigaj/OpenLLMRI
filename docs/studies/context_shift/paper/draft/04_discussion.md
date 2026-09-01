<!-- Section 4: Discussion. Outline §4 (9 paragraphs; c gets two). Checklist: NEURO
anchoring + bistability disclaimer [x]; good-enough parallel [x]; incongruity-
resolution [x]; c1 descriptive / c2 interpretation-with-caveat-first [x]; ROC
calibration [x]; garden-path-vs-pun [x]; typicality-vs-commitment [x];
represented-but-ungated elevated [x]; SCOUT close with one cross-scale sentence [x]. -->

# 4. Discussion

**What "metastable" means here.** We anchor the term in the dynamics of biological
neural systems rather than in physics. In coordination dynamics and in the
winnerless-competition framework — models of sequential transient dynamics in neural
populations — cognition is described as sequences of transiently stable states that are
not fixed-point attractors — structured passages through state space in which dwelling
and moving are not opposites. That is the geometry the data show: a run that dwells
mid-transition occupies something functionally state-like (stationary for many steps,
with its own behavioral signature) yet geometrically a passage (inside the trajectory
bundle, on a smooth equilibrium map). One disclaimer: nothing here is equilibrium
bistability — the evidence-mixture map is smooth (§3.5) — and readers should not import
a barrier-crossing picture. Semantic metastability, as we use it, is a property of
paths.

**The human parallel.** The signature of §3.2 — fast partial reanalysis that leaves a
lingering trace of the initial misreading — is also the signature of human sentence
processing in the "good-enough" tradition: after recovering from a garden-path sentence,
comprehenders measurably retain components of the initial, incorrect interpretation. We
make no mechanistic identification; we note that a language model trained on human text
reproduces, at the representational level, the reanalysis profile humans show
behaviorally — including the part where the old reading never fully leaves.

**The study as its own subject.** This project began expecting basins, stickiness, and
off-manifold escape routes, and the data dismantled each expectation in turn: the
stickiness died against a properly fitted null within an hour of being announced; the
off-manifold excursions never appeared; what replaced them — recency dynamics, jumps, a
remnant, a marker — is stranger and better supported. The arc is the one §1 took from
humor theory — incongruity, then resolution — replayed in the study's own history. We
kept the corrections record (nineteen entries, Appendix A) in the paper because the
surviving claims owe their credibility to that process, not despite it.

**Safety and alignment, first descriptively.** The failure surface this study maps
needs no adversary. During an ordinary, coherent shift of conversational frame, a
model's reading of a critical token trails the present frame for roughly its integration
window (here, nine to fourteen sentences, and effectively unbounded in the dwelling
direction), retains a remnant of the prior frame beyond that, and — in one tank
direction, with an exploratory n = 4 echo in fiction/real — dwells between frames for
the remainder of the tested horizon. Throughout, the model never asks which reading is
meant or flags the ambiguity as an obstacle — zero of 96 tank completions, across all
bands — though 45% of mid-band answers do surface both senses. And safeguard-relevant
behavior co-varies with the internal reading: safe-completion rates fall from 91% to 50%
across reading bands (the fiction-side endpoint rests on four completions, and the
gradient is partly scene-driven — §3.4) — attenuation reachable by ordinary context, no
exotic inputs required.

**Then the interpretation, with its caveat stated first.** The following is a post-hoc
reading of an asymmetry we noticed, not a designed manipulation, and training provenance
is unobservable: our two tasks appear to differ in whether they carry a trained default
for unresolved cases. The refusal task behaved as though it does — at mid-transition,
80% of completions safe-complete, and in sampled chain-of-thought traces — the reasoning
channel its chat format exposes, released with our behavior data — both framings are
weighed before the safe reply (a qualitative observation, not a coded rate). The sense
task carries no such default, and there the model silently commits (52% of mid-band
completions pick a sense). If this reading is right, the metastable zone is the failure
window for every behavior *without* a trained uncertainty-default — refusal-style
safeguards may be the well-covered exception rather than the rule. A second, compatible
candidate emerged from the depth data, though it is weaker than it first looked:
fiction/real's mid-deep stack (layers 3–18) settles clearly on the destination side in
both directions, where tank aquarium→vehicle's ends at the midpoint — so downstream
layers in the covered task may act on a more settled reading than the site we measure.
But the deepest band hovers near the midpoint in fiction→real too — precisely the
direction where the safeguard must engage and did (§3.2) — so depth-resolution cannot
carry the explanation alone. A third candidate points the opposite way through the
stack: the shallowest layers resolve the framing composition almost immediately and
completely (§3.2), with the profile of surface-cue tracking — the minimal-pair
discrimination that rules out cue-only tracking was run at the calibrated site, not at
shallow layers — and a safeguard that reads early, from surface content and frame cues,
would fire broadly whenever the alarming request is present and be suppressed only by a
well-established fictional frame: the shape of our behavioral data, including its
fragile 50% fiction-side floor. The fast, complete shallow response is itself
fr-specific — tank's shallow layers respond later and, in one direction, only partially
(§3.2) — which is what a trigger sculpted by safety post-training would look like,
though ordinary register statistics learned in pretraining predict the same asymmetry
and training provenance is unobservable here. The three accounts are not exclusive — one
names the policy, one the downstream state, one the trigger's plausible locus — and none
is causally established: with two tasks these are observations, and the exploratory
per-layer curves (§3.4) are too blunt to separate them (shallow readings saturate
post-shift, leaving that instrument blind exactly where the third account lives). We add
one calibration so this section cannot overpromise: as a standalone monitor of
individual readings, the frame reading is not yet usable (AUC 0.61 [0.43, 0.76],
chance-compatible; Fig. fig_s11_monitor_roc, supplement). The band-level gradient is
real; building a usable monitor — combining several sites, the mixed-context marker, and
per-layer readings — is future work, not a claim.

**Garden path or pun.** In Dynel's terms our transition corpus is a slow-motion garden
path, and most trajectories treat it as one: incongruity, then resolution toward the new
reading. The dwelling runs are the interesting case — an *extended incongruity phase*,
in which the model, asked what the word means, answers like someone explaining a pun:
both senses, held. Whether any of them is a true pun — held incongruity that never
resolves — or only a long garden path is the persistent-versus-slow question our
twenty-sentence horizon cannot decide, and the extended-tail experiment named in future
work is its dedicated test.

**Typicality is not commitment.** The three-worlds question dissolved because it
conflated two axes. On *distributional typicality* the stationary states are
unremarkable — inside the bundle, on-distribution. On *semantic commitment* they are
distinctive — uncommitted, between calibrated interpretations, with hedging as their
behavioral expression. A learned state of unresolvedness is typical *and* uncommitted;
genuinely off-distribution states (glitch inputs, interventions, adversarial
incoherence) occupy a different cell of that table and remain untested here. The general
lesson: that a state is geometrically typical does not make it functionally normal — our
behavior data document the functional difference directly.

**Represented but not consulted.** The mixed-context marker gives the dissociation its
sharpest form: the model carries a persistent, systematic signal that its context is
mixed — and behavior does not appear to use it at matched composition, at the one site
and layer tested. This is the same structure reported in the hallucination literature,
where models internally encode uncertainty or truthfulness that their generations do not
respect. Here it appears in transition dynamics: an internal signal correlated with the
conditions that produce the unresolved zone already exists inside the model, and
behavior does not appear to use it — whether it could actually flag the zone is untested
(the one monitor built, from the frame reading, is chance-compatible). The motivating
case of §1 reportedly had the same structure at system scale — the provider's moderation
layer was flagging the user's messages for self-harm risk in real time while assistance
continued [CITE: filing/reporting]. That suggests a constructive direction for alignment
work — not creating uncertainty signals, but testing whether behavior can be gated on
the ones already there.

**Closing.** Word-sense reinterpretation is the tractable laboratory instance of a much
larger family — frames, personas, tasks, and safety postures all shift under
accumulating context, and there is no obvious reason the metastable structure documented
here is unique to word senses. The states are what the title calls them: unresolved. For
now, so is the question of what a model should do while inside one.
