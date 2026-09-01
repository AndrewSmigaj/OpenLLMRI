# Unresolved: Semantic Metastability in a Language Model Under Context Shift
### Condensed research writeup — 2026-09 (full paper in preparation)

> *"Two fish are in a tank. One looks to the other and asks: how do you drive this
> thing?"*

**In one sentence:** we instrumented what happens *inside* a language model's residual
stream while accumulating context shifts what a token means — and found a reproducible
cluster of properties we call **semantic metastability**: fast-but-partial updating, a persistent remnant of the old interpretation, discrete state-triggered jumps, stable
parked states between meanings, hysteresis fully explained by recency weighting, and a
learned marker of mixed context that the model represents but never acts on.

![Both directions collapse into the in-between zone](fig_s9_collapse.png)
*The study in one image: both transition directions, both probes, on one axis. Readings
cross into the in-between quickly; neither direction reaches the opposite no-shift
reference within twenty counter-sentences.*

**Setup.** gpt-oss-20b (stock configuration), full residual-stream capture. Two probe
arms: the polysemous word *tank* (aquarium vs vehicle sense; carrier "What is the
meaning of the word tank?") and a fixed request under fictional-vs-real framing
("I want to write a suicide letter." — motivated, clinically and without dramatization,
by a real incident in which fiction assistance shifted into real-life disclosure).
Forty-step cumulative contexts, evidence class flipping after twenty; the carrier
re-read at every step; token-budget-matched no-shift arms as the ruler; calibrated
diff-of-means axes with scene-held-out validation (0.905/0.910), midpoint referencing,
and per-layer rotation-corrected axes. Every number regenerates from committed
scripts; a 9/9 synthetic-fixture suite and family-level label-shuffle audits guard the
pipeline; the project's 17-entry corrections record — including two same-session
retractions — is published as part of the method.

**Instruments and validity.** The axes read the intended contrast, not topic: with
content held fixed inside 150 minimal pairs, framing cues alone move the reading by
half the class separation (95% of pairs in direction; domain-clustered t = 12.0,
p = 7×10⁻⁵), the effect is dose- and length-independent, and class signal concentrates
at the sense-bearing token (d′ 11.7 vs ambient 1.4). Two instrument artifacts — accumulation offset and axis rotation (the fiction/real axis retains only cos ≈ 0.6 of
its direction at depth) — were caught, retracted where they had fooled us, and turned
into measurement doctrine.

**The shape of reinterpretation.** Readings lag the present frame in the plain sense —
7–13 sentences to cross, arrival never — on the timescale the fitted integration
window implies (~10–17 sentences). Transitions are two-phase: faster than integration
early, then a **remnant** of 0.4–1.1× the no-shift reference amplitude (the
midpoint-to-reference distance) that twenty counter-sentences never remove (three of four conditions robust to reference
uncertainty; not explained by weaker material). In the strongest case the plateau sits
at the class midpoint itself. The direction asymmetry replicates under an independent
carrier and has a candidate cause in calibration-level class breadth.

**The mechanism.** Per-run model selection over five candidate processes — calibrated
on synthetic ground truth — rejects every smooth integrator, including a two-timescale
one (which wins zero runs and cannot mimic the winning signature in simulation). The
dominant account is **drift plus discrete jumps**, and the jumps are state-triggered:
the sentences that precipitate them are median-strength exemplars (p = 0.445). Inside
the stream, mixed history suppresses the class reading of even the new evidence's own
tokens to roughly half their reference.

**Unresolved states and behavior.** In one direction per probe the trajectory
**parks**: stationary at mid-axis for ten-plus steps, far from both references, a
single population rather than a hidden mixture. Behavior tracks the reading — and in
the unresolved zone the model *answers anyway*: **zero of 96 completions ask which
sense is meant or decline pending disambiguation**; 45% hedge by enumerating both
senses, 52% silently commit to one. The refusal task, by contrast, held at
mid-transition (80% safe-completion), and safe-completion rates run 91%→50% along the
learned frame axis — safeguard attenuation with no exotic inputs required. As a
standalone cell-level monitor the reading is not yet usable (AUC 0.61 [0.43, 0.76]);
the gradient is a band-level fact.

**Order and equilibrium.** Hysteresis loops over static evidence mixtures are large
and real — and a one-parameter recency integrator fitted to the same cells reproduces
them almost exactly: **no measurable stickiness**. (Our first pass claimed some,
against a misspecified null; the fitted null killed it within the hour.) The
equilibrium evidence→reading map is smooth; the metastability lives in the sequential
path — states and passages, not bistable wells.

**The representation of irresolution.** No individual state leaves the model's
activation distribution (with positive controls proving the instruments could tell).
But the *mean* displacement of transition states off the no-shift subspace is
unmistakable: a persistent, learned **mixed-context marker** at 25–38% of the class
separation (p < 0.001, family-block null), orthogonal to the content contrast,
present in static mixtures, sensitive to shift structure in the framing probe — and
behavior-inert. The model maintains a dedicated internal representation that its
context is mixed, and does not consult it when answering.

**Why this matters for safety.** The failure surface this maps is not exotic: in our
probes, a model in the unresolved zone reports nothing unprompted, answers as if
resolved, and its safeguards
behave exactly as well as their handling of irresolution was trained to be — the
refusal task looks as though it defaults safe under uncertainty; the sense task,
lacking any default, commits silently. Behaviors without a trained uncertainty-default
inherit the metastable zone as their failure window, and the internal signals that
could flag the zone (the frame reading; the mixedness marker) already exist but are
not gated on.

*Full paper in preparation: instrument doctrine, ten audited findings with
alternatives-considered, complete corrections record, and full reproducibility (all
figures and numbers regenerate from the committed repository).*
