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
and moving are not opposites. That is the geometry our data show: the park is functionally a state (stationary for many steps, with its own behavioral signature) and
geometrically a passage (inside the trajectory bundle, on a smooth equilibrium map). One
disclaimer: nothing here is equilibrium bistability — the evidence-mixture map is smooth
(§3.5) — and readers should not import a barrier-crossing picture. Semantic
metastability, as we use it, is a property of paths.

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
remnant, a marker — is stranger and better supported. The arc is
the one §1 took from humor theory — incongruity, then resolution — replayed in the
study's own history. We kept the corrections
record (seventeen entries, Appendix A) in the paper because the surviving claims owe
their credibility to that process, not despite it.

**Safety and alignment, first descriptively.** The failure surface this study maps
needs no adversary. During an ordinary, coherent shift of conversational frame, a
model's reading of a critical token trails the present frame for roughly its integration
window (here, ten to seventeen sentences), retains a remnant of the prior frame beyond
that, and — in one direction per task — parks between frames indefinitely on the tested
horizon. Throughout that zone the model reports nothing: zero of 96 completions ask for
disambiguation. And safeguard-relevant behavior tracks the internal reading:
safe-completion rates fall from 91% to 50% as the reading moves along the learned
fiction/real axis — attenuation reachable by ordinary context, no exotic inputs
required.

**Then the interpretation, with its caveat stated first.** The following is a post-hoc
reading of an asymmetry we noticed, not a designed manipulation, and training provenance
is unobservable: our two tasks appear to differ in whether they carry a trained default
for unresolved cases. The refusal task behaved as though it does — at mid-transition,
80% of completions safe-complete, and in the model's own chain-of-thought text — the
reasoning channel its chat format exposes, released with our behavior data — both
framings are visibly weighed before the safe reply. The sense task carries no such
default, and there the model silently commits (52% of mid-band completions pick a
sense). If this reading is right, the metastable zone is the failure window for every
behavior *without* a trained uncertainty-default — refusal-style safeguards may be the
well-covered exception rather than the rule. We add one calibration so this section
cannot overpromise: as a standalone cell-level monitor, the frame reading is not yet
usable (AUC 0.61 [0.43, 0.76], chance-compatible; Fig. fig_s11_monitor_roc, supplement).
The band-level gradient is real; building a usable monitor — combining several sites,
the mixed-context marker, and per-layer readings — is future work, not a claim.

**Garden path or pun.** In Dynel's terms our transition corpus is a slow-motion garden
path, and most trajectories treat it as one: incongruity, then resolution toward the new
reading. The park is the interesting case — an *extended incongruity phase*, in which
the model, asked what the word means, answers like someone explaining a pun: both
senses, held. Whether any park is a true pun — held incongruity that never resolves — or
only a long garden path is the persistent-versus-slow question our twenty-sentence
horizon cannot decide, and the extended-tail experiment named in future work is its
dedicated test.

**Typicality is not commitment.** The three-worlds question dissolved because it
conflated two axes. On *distributional typicality* the park is unremarkable — inside the
bundle, on-distribution. On *semantic commitment* it is distinctive — uncommitted,
between calibrated interpretations, with hedging as its behavioral expression. A learned
state of unresolvedness is typical *and* uncommitted; genuinely off-distribution states
(glitch inputs, interventions, adversarial incoherence) occupy a different cell of that
table and remain untested here. The general lesson: that a state is geometrically
typical does not make it functionally normal — our behavior data document the functional
difference directly.

**Represented but not consulted.** The mixed-context marker gives the dissociation its
sharpest form: the model maintains a persistent, dedicated representation that its
context is mixed — and that representation is behavior-inert at matched composition.
This is the same structure reported in the hallucination literature, where models
internally encode uncertainty or truthfulness that their generations do not respect.
Here it appears in transition dynamics: the information needed to flag the unresolved
zone already exists inside the model; nothing routes it to behavior. That suggests a
constructive direction for alignment work — not creating uncertainty signals, but gating
behavior on the ones already there.

**Closing.** Word-sense reinterpretation is the tractable laboratory instance of a much
larger family — frames, personas, tasks, and safety
postures all shift under accumulating context, and there is no obvious reason the
metastable structure documented here is unique to word senses. The states are what the title calls them: unresolved. For now, so is
the question of what a model should do while inside one.
