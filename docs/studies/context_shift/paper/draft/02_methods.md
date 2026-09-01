<!-- Section 2: Methods. Outline: OUTLINES.md §2 (5 bullets). Checklist: stock-routing
verbatim [x]; boxed protocol [x]; glossary [x]; drift/rotation numbers from
FINDINGS_FINAL [x]; QA paragraph [x]. -->

# 2. Measuring an interpretation while it changes

## 2.1 Model and capture

All experiments use gpt-oss-20b, a 20-billion-parameter mixture-of-experts language
model, run in its stock configuration: we apply no modifications to the model or its
routing — its native top-4-experts-per-token routing operates untouched (the "K=1" label
in the released tooling names an analysis convention for a routing track this study
dropped). Inputs are formatted with the model's chat template and processed with
deterministic forward passes; identical inputs yield identical activations. We capture
the full residual stream (2,880 dimensions) at the output of each of the 24 decoder
blocks. Throughout, "the reading at a site" means the residual stream at one designated
token of a fixed carrier sentence, projected onto a calibrated axis as described below.

## 2.2 Probes, carriers, and corpora

Each probe pairs a fixed **carrier** — a sentence appended verbatim after the context at
every step — with a designated measurement token. The **tank arm** contrasts two senses
of a polysemous word: the carrier is "What is the meaning of the word tank?", measured
at the ' tank' token, with contexts drawn from aquarium-life and armored-vehicle scene
pools. The **fiction/real arm** contrasts two framings of one fixed request: the carrier
is "I want to write a suicide letter.", measured at the ' want' token, with contexts
drawn from fiction-craft discussion (novel drafts, screenwriting, tabletop campaigns)
versus real personal circumstance (grief, diagnosis, eviction). Paraphrase carriers ("I
would like to write…", ' like'; "Help me write…", ' letter') support cross-carrier
checks, and a replicate tank carrier ("Define the word tank.") supports
carrier-independence checks.

The transition corpus (D3) presents 40-step cumulative contexts with the carrier
re-appended at each step: twenty sentences of one class, then twenty of the other, the
target vocabulary absent from every context sentence. Token-budget-matched no-shift arms
(D4) — forty sentences of a single class — provide the reference ruler at every
position. Additional corpora serve specific tests: single-sentence calibration cells
(300 per class per carrier); checkpoint captures storing every token of designated
context windows (144 per arm); minimal pairs holding content fixed while varying only
framing cues (150 pairs); static mixture sweeps for order-dependence (252 cells per
probe); generation-enabled behavior cells (312; greedy decoding); and bare-carrier
baselines. Context sentences were generated under a blind protocol — authoring agents
received only a contrast specification and diversity rules, never hypotheses — with
per-class scene diversity capped so that no setting dominates a class, enabling
scene-held-out validation.

## 2.3 The instrument, and how not to fool yourself with it

Our measurement axis is deliberately simple: the difference of class means over
calibration activations, normalized so the two class means read −1 and +1. The axis is
the easy part; the difficulty lies in using it honestly over accumulating context. We
learned each rule below by first getting it wrong; the corrections record (Appendix A)
documents that process.

**Box 1 — Protocol for reading interpretations over accumulating context.**
1. *Calibrate at the same site, same carrier, always.* Projecting across token positions
   collapses to a positional constant; projecting one carrier's states through another
   carrier's axis is dominated by token identity (both failure modes demonstrated on our
   own data before becoming rules).
2. *Validate endpoints held-out at the scene level.* Our calibration axes separate
   classes at 0.905 (tank, layer 4) and 0.910 (fiction/real, layer 14) under 12-fold
   leave-one-scene-pair-out cross-validation (chance 0.50, 300 per class) — the split
   that tests whether the axis learned the contrast or a setting.
3. *Reference every absolute claim to position-matched no-shift arms.* Readings carry
   **accumulation drift**: a class-nonspecific component that grows with context
   (≈ +1.0 axis units by twenty sentences at the fiction/real site; ≈ 0 at the tank
   site's layer). It is one shared component — its time-course replicates across
   carriers with axis-dependent sign (r = +0.75, −0.86) — and it contaminates any
   unreferenced position claim.
4. *Verify the axis still points the right way at depth.* The class direction itself
   can rotate as context accumulates: on accumulated states the fiction/real axis
   retains only cos 0.57–0.63 of its single-sentence direction at layers 10–23 (tank:
   0.78–0.97). Depth claims require per-layer axes refit on accumulated no-shift states
   (held-out accuracy 0.93–1.00 at every layer); drift and rotation together cost
   us three retracted findings before rules 3 and 4 were adopted.
5. *Treat readings as positions along a designed contrast, never as meaning.* A
   "real-side" reading may mean "not-fiction" or any correlate; distinguishing these
   requires contrasts this study does not contain.
6. *Cluster statistics at the family level.* Sentences within a scene family are not
   independent; every interval in this paper is family-clustered.
7. *Prove the pipeline can fail.* Family-level label shuffles must kill every effect
   (they do: separations fall to chance, within-pair effects to zero); synthetic
   ground-truth fixtures must recover known answers through the actual pipeline code
   (nine of nine do); positive controls must show each null-result instrument
   detecting real displacement (they do).

**Glossary.** *Semantic metastability* — the name Discussion gives to the cluster of
properties documented in Results: persistent intermediate configurations of a contextual
reading between two calibrated interpretations. *Unresolved zone* — the band of readings
between the two calibrated interpretations, and the stretch of context during which a
reading sits there. *Residual* — the component of a prior interpretation that
counter-evidence does not remove. *Park* — a stationary intermediate configuration
holding for many steps. *Mixed-context marker* — a learned direction, orthogonal to the
content contrast, that activates for mixed-class contexts. *Accumulation drift* and
*axis rotation* — the two instrument effects of rule 3 and rule 4.

## 2.4 Reproducibility

Every number in this paper regenerates from committed analysis scripts over frozen
captures: a full regeneration audit reproduced all reported values (calibration axes
bit-identical; seeded bootstraps exact), a permanent fixture suite pushes synthetic data
with analytically known answers through the actual pipeline functions, and the
label-shuffle and positive-control audits above are committed tests. The study's
seventeen-entry corrections record — including two same-session retractions — is
Appendix A, and we regard it as part of the method: the surviving claims are the ones
that outlived our own attempts to kill them.
