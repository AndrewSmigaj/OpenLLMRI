<!-- Section 2: Methods. Order (structure pass, 2 Sept 2026): model and capture → the
instrument → tasks and corpora → protocol (Box 1, glossary) → analysis methods →
reproducibility. -->

# 2. Measuring an interpretation while it changes

## 2.1 Model and capture

All experiments use gpt-oss-20b, a 20-billion-parameter mixture-of-experts language
model, run in its stock configuration: we apply no modifications to the model or its
routing — its native top-4-experts-per-token routing operates untouched. Inputs are
formatted with the model's chat template and processed with deterministic forward
passes; identical inputs yield identical activations. We capture the full residual
stream (2,880 dimensions) at the output of each of the 24 decoder blocks. Throughout, a
*site* is a designated token of a fixed carrier sentence together with a layer, and "the
reading at a site" means the residual stream at that token and layer, projected onto a
calibrated axis as described next. The tank task reads at the ' tank' token, layer 4;
the fiction/real task at the ' want' token, layer 14 (the tasks are introduced in §2.3).

## 2.2 The instrument

The measurement axis is simple. For a site (token, layer), we average
the residual-stream states of the single-sentence calibration corpus by class,
giving two class means and their difference w. The reading of a state h is its
position along that axis, rescaled so the class means sit at −1 and +1:
r(h) = 2(h − m)·w/|w|², where m is the midpoint of the two class means. A reading
is a signed coordinate between the two calibrated interpretations — a projection,
not a distance to either class. We use the difference of class means rather than a trained classifier such as a
logistic probe: it has no hyperparameters,
its geometry is transparent, and mean-difference directions read out class structure
comparably to trained probes [CITE: mass-mean probing]; its adequacy here is checked
empirically. Classification accuracies use the midpoint rule — a held-out sentence
is assigned to the class whose mean lies on its side of the midpoint — with splits
held out at the scene-family level.

## 2.3 Tasks, carriers, and corpora

Each task pairs a fixed **carrier** — a sentence appended verbatim after the context at
every step — with a designated measurement token. The **tank task** contrasts two senses
of a polysemous word: the carrier is "What is the meaning of the word tank?", measured
at the ' tank' token, with contexts drawn from aquarium-life and armored-vehicle scene
pools. The **fiction/real task** contrasts two framings of one fixed request: the
carrier is "I want to write a suicide letter.", measured at the ' want' token, with
contexts drawn from fiction-craft discussion (novel drafts, screenwriting, tabletop
campaigns) versus real personal circumstance (grief, diagnosis, eviction). Paraphrase
carriers ("I would like to write…", ' like'; "Help me write…", ' letter') support
cross-carrier checks, and a replicate tank carrier ("Define the word tank.") supports
carrier-independence checks. The ' want' site was fixed early in the project and
retained for comparability; §3.1 shows the framing signal is spread across the request's
content words, and replication at the strongest-reading ' write' site is planned (§5).

Each corpus answers one question. *How does a reading move when the evidence changes
sides?* The transition corpus presents 40-step cumulative contexts with the carrier
re-appended at each step: twenty sentences of one class, then twenty of the other, the
target vocabulary absent from every context sentence. *What would the reading be with
no shift?* Token-budget-matched no-shift control runs — forty sentences of a single
class — provide the reference at every position. *Where do the two interpretations
sit?* Single-sentence calibration sentences (300 per class per carrier) define the axis
of §2.2. *What does every token read, not only the carrier's?* Checkpoint captures are
full recordings of every token's activations at designated context lengths (144 per
task). *Does the reading track framing cues rather than content?* Minimal pairs hold
content fixed while varying only framing cues (150 pairs). *Does the order of evidence
matter beyond its amount?* Static mixture sweeps — twenty-sentence contexts holding a
fixed mix of the two classes (252 cells per task) — test order dependence. *What does
the model do?* Behavior prompts with generation enabled (312; greedy decoding) supply
completions. Bare-carrier baselines complete the set.

Context sentences were written by language-model authoring agents (separate from the
model under study) under a blind protocol: an agent received only a contrast
specification and diversity rules, never the hypotheses. Per-class scene diversity was
capped so that no setting dominates a class, enabling scene-held-out validation.

Four terms recur throughout:

- A **run** is one 40-step context sequence. Transition runs flip class at twenty;
  no-shift control runs never do.
- A **cell** is one point of a mixture-sweep grid: one class mixture in one block
  order.
- A **scene family** is a set of sentences sharing one concrete setting (a home
  aquarium, a tank museum). There are twelve per class per task, and every statistic
  in this paper is clustered at the family level.
- **Scene-held-out** validation holds out whole families, one from each class per
  fold.

## 2.4 The protocol

Box 1 states the protocol for using the axis over accumulating context.

**Box 1 — Protocol for reading interpretations over accumulating context.**

1. *Calibrate at the same site, same carrier, always.* Projected across token
   positions, readings become a constant set by position rather than content;
   projected through another carrier's axis, they are dominated by token identity
   (both failure modes
   occur in our data).
2. *Validate endpoints held-out at the scene level.* Our calibration axes separate
   classes with held-out accuracy 0.905 (tank, layer 4) and 0.910 (fiction/real,
   layer 14) under 12-fold leave-one-family-pair-out cross-validation (chance 0.50,
   300 per class) — the split that tests whether the axis learned the contrast or a
   setting.
3. *Reference every absolute claim to position-matched no-shift runs.* Readings
   carry an **accumulation offset**: a class-nonspecific component that grows with
   context — ≈ +1.0 axis units by twenty sentences at the fiction/real site, half
   the class separation on an axis whose class means sit at ±1 (≈ 0 at the tank
   site). It is one shared component: its time-course replicates across paraphrase
   carriers, with the sign set by each carrier's axis orientation (r = +0.75
   same-oriented, −0.86 opposite-oriented). It contaminates any unreferenced
   position claim.
4. *Verify the axis still points the right way at depth.* The class direction itself
   can rotate as context accumulates: on accumulated states the fiction/real axis
   retains only cos 0.57–0.63 of its single-sentence direction at layers 10–23 (tank:
   0.78–0.97). Depth claims require per-layer axes refit on accumulated no-shift states
   (held-out accuracy 0.93–1.00 at every layer); uncorrected depth readings produced three
   spurious findings, since retracted.
5. *Treat readings as positions along a designed contrast, never as meaning.* A
   "real-side" reading may mean "not-fiction" or any correlate; distinguishing these
   requires contrasts this study does not contain.
6. *Cluster statistics at the family level.* Sentences within a scene family are not
   independent; every interval in this paper is family-clustered.
7. *Prove the pipeline can fail.* Family-level label shuffles must kill every effect
   they are run on (they do: separations fall to chance, within-pair effects to
   zero; the mixed-context marker is tested against its own family-block null
   instead); synthetic
   ground-truth fixtures must recover known answers through the actual pipeline code
   (nine of nine do); positive controls must show each null-result instrument
   detecting real displacement (they do).

**Glossary.** *Semantic metastability* — the name Discussion gives to the cluster of
properties documented in Results: persistent intermediate configurations of a contextual
reading between two calibrated interpretations. *Unresolved zone* — the band of readings
between the two calibrated interpretations, and the stretch of context during which a
reading sits there. *Dwelling* — a trajectory that becomes stationary within the
unresolved zone and, on the measured horizon, does not leave it. *Remnant* — the
component of a prior interpretation that twenty counter-sentences do not remove.
*Mixed-context marker* — a systematic direction, orthogonal to the content contrast, on
which mixed-class contexts read high and pure-class contexts read near zero.
*Accumulation offset* and *axis rotation* — the two instrument effects of rule 3 and
rule 4.

## 2.5 Analysis methods

**Trajectory models.** No regression is involved in the instrument; least squares
enters only here. Per-run dynamics are fit to each run's twenty post-shift readings
by least squares over four model forms. The first is a recency-weighted integrator:
the reading as a weighted average of all evidence so far, each sentence weighted
γ^age so that recent sentences count more, with the single decay parameter γ
grid-searched. The uniform, equal-weight integrator is its γ = 1 case and also serves
as the lead/lag reference. The second is a change-point step: a constant level before
and after a fitted change point (three parameters). The third is a drift-plus-step
hybrid: a linear trend plus a step at a fitted change point (four parameters). The
fourth is a two-timescale integrator: a mixture of fast and slow recency weightings
(three parameters). Selection is by BIC over the twenty points, declaring a winner
only when it leads the runner-up by at least 2, and "indeterminate" otherwise. The
selector's identifiability is calibrated on synthetic runs of known type (§3.3).

**The remnant gap.** The destination reference level (positions 36–40) minus the
run's plateau (post-shift sentences 16–20), both midpoint-referenced.

**Uncertainty.** Intervals are family-clustered bootstraps: 2,000 seeded draws
resampling scene families with replacement. Where a named test appears, its
clustering unit is stated in place.

**Behavior.** Completions are categorized by regular-expression scan plus manual
review of the committed worksheets.

## 2.6 Reproducibility

Every number in this paper regenerates from committed analysis scripts over frozen
captures: a full regeneration audit reproduced all reported values (calibration axes
bit-identical; seeded bootstraps exact), a permanent fixture suite pushes synthetic data
with analytically known answers through the actual pipeline functions, and the
label-shuffle and positive-control audits above are committed tests. Corrections that
changed reported values are listed in Appendix A; the complete record is in the
repository.
