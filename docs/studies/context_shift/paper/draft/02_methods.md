<!-- Section 2: Methods. Outline: OUTLINES.md §2 (5 bullets). Checklist: stock-routing
verbatim [x]; boxed protocol [x]; glossary [x]; offset/rotation numbers from
FINDINGS_FINAL [x]; QA paragraph [x]. -->

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
calibrated axis as described below. The tank task reads at the ' tank' token, layer 4;
the fiction/real task at the ' want' token, layer 14.

## 2.2 Tasks, carriers, and corpora

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

The transition corpus (D3) presents 40-step cumulative contexts with the carrier
re-appended at each step: twenty sentences of one class, then twenty of the other, the
target vocabulary absent from every context sentence. Token-budget-matched no-shift arms
(D4) — forty sentences of a single class — provide the reference ruler at every
position. Additional corpora serve specific tests: single-sentence calibration cells
(300 per class per carrier); checkpoint captures — full recordings of every token's
activations at designated context lengths, not only the carrier's (144 per task);
minimal pairs holding content fixed while varying only framing cues (150 pairs); static
mixture sweeps — twenty-sentence contexts holding a fixed mix of the two classes (252
cells per task) — for order-dependence; behavior cells with generation enabled (312;
greedy decoding); and bare-carrier baselines. Context sentences were written by
language-model authoring agents (separate from the model under study) under a blind
protocol: an agent received only a contrast specification and diversity rules, never the
hypotheses. Per-class scene diversity was capped so that no setting dominates a class,
enabling scene-held-out validation.

Vocabulary used throughout: an **arm** is one condition sequence (a transition arm flips
class at twenty; a no-shift arm never does); a **cell** is one measured item — one
context at one length, with its carrier; sentences are authored in **scene families** —
sets of sentences sharing one concrete setting (a home aquarium, a tank museum) — twelve
per class per task, and every statistic in this paper is clustered at the family level;
**scene-held-out** validation holds out whole families, one from each class per fold.

## 2.3 The instrument, and how not to fool yourself with it

Our measurement axis is deliberately simple: the difference of class means over
calibration activations, normalized so the two class means read −1 and +1. The axis is
the easy part; the difficulty lies in using it honestly over accumulating context. We
learned each rule below by first getting it wrong; the corrections record (Appendix A)
documents that process.

**Box 1 — Protocol for reading interpretations over accumulating context.**
1. *Calibrate at the same site, same carrier, always.* Projected across token
   positions, readings become a constant set by position rather than content;
   projected through another carrier's axis, they are dominated by token identity
   (both failure modes demonstrated on our own data before becoming rules).
2. *Validate endpoints held-out at the scene level.* Our calibration axes separate
   classes with held-out accuracy 0.905 (tank, layer 4) and 0.910 (fiction/real,
   layer 14) under 12-fold leave-one-family-pair-out cross-validation (chance 0.50,
   300 per class) — the split that tests whether the axis learned the contrast or a
   setting.
3. *Reference every absolute claim to position-matched no-shift arms.* Readings
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
   (held-out accuracy 0.93–1.00 at every layer); the offset and the rotation together cost
   us three retracted findings before rules 3 and 4 were adopted.
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
reading sits there. *Remnant* — the component of a prior interpretation that
counter-evidence does not remove. *Mixed-context marker* — a systematic direction,
orthogonal to the content contrast, on which mixed-class contexts read high and
pure-class contexts read near zero.
*Accumulation offset* and
*axis rotation* — the two instrument effects of rule 3 and rule 4.

## 2.4 Reproducibility

Every number in this paper regenerates from committed analysis scripts over frozen
captures: a full regeneration audit reproduced all reported values (calibration axes
bit-identical; seeded bootstraps exact), a permanent fixture suite pushes synthetic data
with analytically known answers through the actual pipeline functions, and the
label-shuffle and positive-control audits above are committed tests. The study's
eighteen-entry corrections record — including two same-session retractions — is Appendix
A, and we regard it as part of the method: the surviving claims are the ones that
outlived our own attempts to kill them.
