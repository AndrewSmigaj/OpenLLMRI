<!-- Section 2: Methods. Rewrite step 2 (2 Sept 2026), after review loop 1: sign
convention stated; calibration items pictured; readings unbounded; layer choice
stated; run counts added; Box 1 rules reworded where a non-practitioner could not
picture the failure; integrator inputs and parameter counts stated; remnant gap in one
coordinate system; axis named "calibration axis" throughout. All numbers of the
previous version retained. -->

# 2. Measuring an interpretation while it changes

## 2.1 Model and capture

All experiments use gpt-oss-20b, a 20-billion-parameter mixture-of-experts language
model, in its stock configuration. We make no modifications to the model or its
routing. Its native top-4-experts-per-token routing operates untouched. Inputs are
formatted with the model's chat template and processed with deterministic forward
passes, so identical inputs yield identical activations. We capture the full residual
stream (2,880 dimensions) at the output of each of the 24 decoder blocks. Throughout, a
*site* is a designated token of a fixed carrier sentence together with a layer. The
*reading* at a site is the residual stream at that token and layer, projected onto a
calibration axis as described next. The tank task reads at the ' tank' token, layer 4, and the fiction/real task at the
' want' token, layer 14. We call these two sites the calibrated sites. Layer 4 is where the tank
calibration axis separates held-out scene families best (the held-out split is
defined in §2.3). Layer 14 is near the fiction/real peak, which falls at layers 12–13; it was fixed
early in the project, with the ' want' token, and retained so that every fiction/real
analysis shares one site. The tasks themselves are introduced in §2.3.

## 2.2 The instrument

The calibration axis is a difference of class means. A *state* is the residual-stream
vector at a site. For a site, we average the states over the calibration items of each
class: single context sentences of that class, each followed by the carrier (§2.3). This gives two class means
and their difference, w. The reading of a state h is its position along that axis,
rescaled so the class means sit at −1 and +1: r(h) = 2(h − m)·w/|w|², where m is the
midpoint of the two class means. For the tank task the aquarium mean sits at −1 and the
vehicle mean at +1; for the fiction/real task, fictional at −1 and real at +1. A
reading is therefore a signed coordinate on the line through the two calibrated
interpretations. It is a projection, not a distance to either class, and readings are
not confined to the interval between −1 and +1.

None of this is new. The axis is the difference-of-means probe, called mass-mean
probing in the interpretability literature, where it was found to read out class
structure comparably to trained probes [CITE: Marks & Tegmark 2023]. The same
difference-in-means direction underlies recent steering and refusal-direction work
[CITE: Rimsky et al. 2024; Arditi et al. 2024], and the midpoint rule is
nearest-centroid classification [CITE: nearest class mean, e.g. Tibshirani et al.
2002]. We use the difference of class means rather than a trained classifier such
as a logistic probe because it has no hyperparameters and its geometry is
transparent. What is ours is the rescaling to ±1, the referencing of every reading
to matched no-shift contexts (§2.4), and the use of the axis over accumulating
context. Its adequacy here is checked empirically (§3.1).

Classification accuracies use the midpoint rule: a held-out item is assigned to the
class whose mean lies on its side of the midpoint. Splits are held out at the level of
scene families, defined in §2.3.

## 2.3 Tasks, carriers, and corpora

Each task pairs a fixed **carrier** with a designated measurement token. The carrier is
a sentence appended verbatim after the context at every step. The **tank task**
contrasts two senses of a polysemous word. Its carrier is "What is the meaning of the
word tank?", measured at the ' tank' token, with contexts drawn from aquarium-life and
armored-vehicle scene families. The **fiction/real task** contrasts two framings of one
fixed request. Its carrier is "I want to write a suicide letter.", measured at the
' want' token, with contexts drawn from fiction-craft discussion (novel drafts,
screenwriting, tabletop campaigns) or from real personal circumstance (grief,
diagnosis, eviction). Two paraphrase carriers support cross-carrier checks: "I would
like to write a suicide letter.", measured at ' like', and "Help me write a suicide
letter.", measured at ' letter'. A replicate tank carrier, "Define the word tank.",
supports carrier-independence checks. §3.1 shows that the framing signal is spread
across the request's content words, and replication at the strongest-reading ' write'
site is planned (§5).

Four terms recur throughout:

- A **run** is one 40-step context sequence. Each step adds one context sentence,
  re-appends the carrier, and yields one reading at the site. Transition runs flip
  class at twenty; no-shift control runs never do.
- A **cell** is one point of a mixture-sweep grid, described below: one class mixture,
  with the two classes' sentences arranged in one of two block orders, one class
  first or the other first.
- A **scene family** is a set of sentences sharing one concrete setting (a home
  aquarium, a tank museum). There are twelve per class per task, and every statistic
  in this paper is clustered at the family level.
- **Scene-held-out** validation holds out whole families, one from each class per
  fold.

Each corpus answers one question (Table 1). *How does a reading move when the
evidence changes sides?* The transition corpus presents 40-step cumulative contexts
with the carrier re-appended at each step: twenty sentences of one class, then twenty
of the other. No context sentence contains the carrier sentence itself, and tank context
sentences never contain the word "tank" in any form. *What would the reading be with
no shift?* No-shift control runs, forty sentences of a single class with the same
number of tokens, provide the reference at every position. *Where do the two
interpretations sit?* Calibration items are one context sentence of a class followed
by the carrier, read at the site; their class means define the axis of §2.2. *What
does every token read, not only the carrier's?* Checkpoint captures record the
activations of every token at designated context lengths. *Does the reading track
framing cues rather than content?* Minimal pairs hold content fixed while varying
only the framing cues. *Does the order of evidence matter beyond its amount?* Static
mixture sweeps hold a fixed mix of the two classes in a twenty-sentence context.
*What does the model do?* Behavior prompts with generation enabled supply
completions. *What does the carrier read with no context at all?* Bare-carrier
baselines, the carrier alone, complete the set.

**Table 1.** The corpora, the question each answers, and their sizes.

| Corpus | Question | Composition | Size |
|---|---|---|---|
| Transition runs | How does a reading move when the evidence changes sides? | 40 steps; twenty sentences of one class, then twenty of the other | 12 runs per direction (tank); 24 per direction (fiction/real) |
| No-shift control runs | What would the reading be with no shift? | 40 sentences of one class, same number of tokens | 6 runs per class per task |
| Calibration items | Where do the two interpretations sit? | one context sentence, then the carrier | 300 per class per carrier |
| Checkpoint captures | What does every token read? | every token's activations at designated context lengths | 144 captures per task |
| Minimal pairs | Does the reading track framing cues rather than content? | content held within the pair, framing cue varied | 150 pairs |
| Static mixture sweeps | Does the order of evidence matter beyond its amount? | twenty-sentence contexts at a fixed class mix, in two block orders | 252 cells per task |
| Behavior prompts | What does the model do? | generation enabled, greedy decoding | 312 completions |
| Bare-carrier baselines | What does the carrier read with no context? | the carrier alone | — |

Context sentences were written by language-model authoring agents, separate from the
model under study, under a blind protocol. An agent received only a contrast
specification and diversity rules, never the hypotheses. Within each class, the number
of sentences per scene family was capped so that no family dominates the class, which
is what makes scene-held-out validation possible.

## 2.4 The protocol

Box 1 states the protocol for using the calibration axis over accumulating context.
Each rule names the way the instrument fails when the rule is broken.

**Box 1 — Protocol for reading interpretations over accumulating context.**

1. *Calibrate at the same site, same carrier, always.* An axis calibrated at one token,
   applied to the states of other tokens, returns a value fixed by the token's
   position rather than by the context's content. An axis calibrated for one carrier,
   applied to another carrier's states, returns a value dominated by token identity.
   Both failures occur in our data.
2. *Validate the axis with whole scene families held out.* Our calibration axes
   separate the classes with held-out accuracy 0.905 for tank (layer 4) and 0.910 for
   fiction/real (layer 14). The split is 12-fold leave-one-family-pair-out
   cross-validation. Chance is 0.50, with 300 items per class. Holding out whole scene
   families is the split that tests whether the axis learned the contrast or a
   setting.
3. *Reference every claim about a reading's level to position-matched no-shift runs.*
   Readings carry an **accumulation offset**: a component that grows with context
   length and does not depend on class. At the fiction/real site it reaches about
   +1.0 axis units by twenty sentences, an offset as large as half the distance
   between the two classes. At the tank site it is about 0. We measure it as the position-by-position midpoint
   of the two classes' no-shift references. The offset is one direction in activation
   space, shared across the three fiction/real carriers, which each carrier's axis
   meets at its own angle. Its time course at the ' want' site correlates with the
   time course at the ' like' site at r = +0.75 and at the ' letter' site at
   r = −0.86, the sign following that angle. Any claim about a reading's level that is not referenced to a matched
   no-shift run is contaminated by the offset.
4. *Verify the axis still points the right way once context has accumulated, at
   every layer.* The class direction itself can rotate as context accumulates; we call this
   **axis rotation**. On accumulated states, the class direction at layers 10–23 has
   cosine 0.57–0.63 with the single-sentence fiction/real calibration axis, except
   layer 21 at 0.68 (tank: 0.78–0.97). Claims about
   layers other than the calibrated site therefore require per-layer axes refit on
   accumulated no-shift states, which reach held-out accuracy 0.93–1.00 at every
   layer. The readings at the calibrated sites in §3, including the fiction/real site
   at layer 14, use the single-sentence calibration axis. They are referenced
   throughout to no-shift runs read with the same axis, as rule 3 requires. Because
   the references are read with the same axis, a reading's position between them
   stays interpretable even where that axis captures less of the accumulated class
   contrast. The per-layer analyses use the refit axes. Uncorrected per-layer readings produced
   three spurious findings, retracted before this version.
5. *Treat readings as positions along a designed contrast, never as meaning.* A
   "real-side" reading may mean "not fiction" or any correlate of it. Distinguishing
   these requires contrasts this study does not contain.
6. *Cluster statistics at the family level.* Sentences within a scene family are not
   independent, and treating them as independent would shrink every interval. Every
   interval in this paper is family-clustered.
7. *Prove the pipeline can fail.* Three checks apply. Family-level label shuffles
   kill every effect they are run on: separations fall to chance and within-pair
   effects to zero. The mixed-context marker, defined in the glossary, has no class
   label to shuffle; it is tested instead against a null built by resampling whole
   scene families. Synthetic ground-truth fixtures recover known answers through the
   actual pipeline code, nine of nine. Wherever an instrument in §3 returns a null result, a positive control shows that
   instrument detecting a real displacement.

**Glossary.**

- *Semantic metastability*: the name §4 gives to the cluster of properties documented
  in §3: persistent intermediate configurations of a contextual reading between two
  calibrated interpretations.
- *Unresolved zone*: the band of readings between the two classes' position-matched
  no-shift references, and the stretch of context during which a reading sits there.
- *Dwelling*: a trajectory that becomes stationary within the unresolved zone and, on
  the measured horizon, does not leave it.
- *Remnant*: the component of a prior interpretation that twenty counter-sentences do
  not remove.
- *Mixed-context marker*: a systematic direction, orthogonal to the calibration axis,
  on which mixed-class contexts read high and pure-class contexts read near zero.
- *Accumulation offset* and *axis rotation*: the two instrument effects of rules 3
  and 4.

## 2.5 Analysis methods

**Trajectory models.** We describe each run's twenty post-shift readings with four
candidate model forms, fit by least squares. This is the only place regression
enters; the instrument itself involves none. The first form is a recency-weighted
integrator: the reading is a weighted average of the evidence so far. Each sentence
contributes the reference level of its class, a constant taken from the no-shift
runs over positions 10–40, weighted by γ^age so that recent sentences count more. Its one fitted parameter, the decay γ, is
grid-searched. The uniform, equal-weight integrator is its γ = 1 case, and it also
serves as the reference against which §3 asks whether a reading runs ahead of or
behind the evidence. The second form is a change-point step: a constant level before
and after a fitted change point (three parameters). The third is a drift-plus-step
hybrid: a linear trend plus a step at a fitted change point (four parameters). The
fourth is a two-timescale integrator: a mixture of a fast and a slow recency
weighting (three parameters). We select by BIC over the twenty points and declare a
winner only when it leads the runner-up by at least 2. Otherwise the run is
indeterminate. The selector's identifiability is calibrated on synthetic runs of
known type (§3.3).

**The remnant gap.** The reading of the no-shift run of the post-shift class minus the
reading of the transition run, both averaged over positions 36–40 (post-shift
sentences 16–20) and both measured from the midpoint. The gap is signed so that a
positive value means the transition run falls short of the post-shift class's
reference.

**Uncertainty.** Intervals are family-clustered bootstraps: 2,000 seeded draws
resampling scene families with replacement. Where a named test appears, its clustering
unit is stated in place.

**Behavior.** Completions are categorized by regular-expression scan plus manual review
of the committed categorization tables.

## 2.6 Reproducibility

Every number in this paper regenerates from committed analysis scripts over frozen
captures. A full regeneration audit reproduced all reported values, with calibration
axes bit-identical and seeded bootstraps exact. A permanent fixture suite pushes
synthetic data with analytically known answers through the actual pipeline functions.
The label-shuffle and positive-control audits of Box 1 are committed tests. Corrections
that changed reported values are listed in Appendix A. The complete record is in the
repository.
