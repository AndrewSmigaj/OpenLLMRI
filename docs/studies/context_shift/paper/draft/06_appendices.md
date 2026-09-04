<!-- Back matter. Rewrite step 2 (2 Sept 2026): Related work drafted into prose with
[CITE: ...] placeholders (Andrew fills citations); Appendices A–C written as short
prose from the frozen record (FINDINGS_FINAL corrections 15, 16, 18, 19; the QA report;
the post-freeze log). Acknowledgments placeholder unchanged. -->

# Back matter

## Acknowledgments

[DRAFT, for approval.] This study was carried out with language-model assistants,
Claude through Claude Code and in chat, used as the analysis runtime and as writing
and review assistants. Under the author's direction they authored the context
sentences under the blind protocol of §2.3, ran the captures and the committed
analysis scripts, categorized the completions, and drafted and revised the text. The
author reviewed every number and claim and is responsible for them.

## Ethics and safe messaging

[DRAFT, for Andrew's approval.] This paper studies how a model's internal reading of a
suicide-related request moves under context, and reports the model's behavior around
that request. It involves no human subjects and no user data. The fiction/real corpus
was written under the norms of §2.3: no context sentence contains the carrier request,
and the theme-only sub-arm never names a suicide letter or note. The content note on
the first page follows safe-messaging practice, and the paper quotes no
model-generated text that assists with the letter. [Data release policy per D1:
categorization tables with paraphrased excerpts and raw completions on request, or
full release.] The motivating case is contested litigation, and the paper
characterizes only what the filing and reporting describe.

## Related work

**Reading representations with probes.** Linear probes have been the standard way to
ask what a layer represents, and their validity has been questioned from the start:
a probe can learn its own task rather than report the model's [CITE: Alain & Bengio;
Hewitt & Liang; Belinkov]. Our answer to that concern is the three tests of §3.1
and the label shuffles of Box 1. The instrument assembles established methods. The difference-of-means axis is the
mass-mean probe [CITE: Marks & Tegmark 2023], which found such directions read out class
structure comparably to trained probes; difference directions between two
conditions go back to word-embedding analyses [CITE: Bolukbasi et al. 2016] and to
concept activation vectors [CITE: Kim et al. 2018], and rest on the linear
representation hypothesis [CITE: Park, Choe & Veitch 2023]. Classifying by the nearer class mean is nearest-centroid classification [CITE:
Tibshirani et al. 2002], and word senses were read from contextual activations in
just this way, by nearest sense centroid, in early geometry studies of BERT [CITE:
Reif et al. 2019]. The rotation of a readout direction across depth (Box 1) is the
effect that motivates refitting a lens at every layer [CITE: Belrose et al. 2023,
tuned lens]. The per-token class signal we report is d′ from signal detection theory
[CITE: Green & Swets 1966]. The two off-distribution scores of §3.7 are the
k-nearest-neighbor distance [CITE: Sun et al. 2022; Lee et al. 2018] and the
principal-component reconstruction error [CITE: Jackson & Mudholkar 1979]. The
nearest cousin of our fiction/real behavior link is the refusal direction, a single
difference-in-means direction along which refusal behavior can be read and steered
[CITE: Arditi et al. 2024], and the same direction family underlies contrastive
activation steering [CITE: Rimsky et al. 2024].

**Dynamics of in-context processing.** The account of in-context learning as
implicit Bayesian inference is the standing theory our recency-integrator comparison
speaks to [CITE: Xie et al.]. Function-vector and task-vector work shows that a
context's task can be summarized in a direction of the residual stream [CITE:
Hendel et al.; Todd et al.], and induction heads describe one mechanism by which
context propagates [CITE: Olsson et al.]. Those describe the summary once formed, or the mechanism that forms it. Probes of
belief state and board state follow a latent state as it updates, on synthetic or
game data [CITE: Shai et al. 2024; Li et al. 2023], and incremental parse-state
probes read a syntactic interpretation as words arrive [CITE: Eisape et al. 2022].
That in-context processing weights recent items more heavily is also established
[CITE: Zhao et al. 2021; Liu et al. 2023]. Our recency integrator turns that property
into one fitted timescale. What happens to a natural-language interpretation while
it is being overturned, and whether the model acts on the intermediate readings, is
the question here.

**Long-context safety.** Many-shot jailbreaking and multi-turn escalation attacks
show that accumulated context can override trained behavior [CITE: many-shot
jailbreaking; Crescendo]. Our shifts are not attacks. They are coherent
conversations, and the weakening of the safeguard we observe needs no adversary.

**Verbalized uncertainty and ambiguity.** Models can be trained or prompted to
express confidence, and their verbalized confidence can be calibrated [CITE:
Kadavath et al.; Lin et al.; Xiong et al.]. Ambiguity in questions has been modeled
directly [CITE: Liu et al.]. These ground the scoped claim of §1: models can express uncertainty, and in the 96
completions we examined none asked which sense was meant.

**Internal encoding versus expression.** Models internally encode truthfulness and
uncertainty that their generations do not respect [CITE: Azaria & Mitchell; Orgad et
al.]. Residual-stream signals of conflict between the context and stored knowledge
have also been reported [CITE: Zhao et al. 2024, knowledge conflicts in the residual
stream]. The mixed-context marker of §3.7 belongs to this family: a signal, here of
conflict within the context itself, that is present and, as far as we tested,
unused.

**Long-context artifacts.** Attention sinks and related position effects raise the
question of whether the accumulation offset of Box 1 is positional [CITE: attention
sinks]. Midpoint referencing makes our findings robust either way, since every level
claim is measured against a matched no-shift reference at the same position.

**Human sentence processing.** The good-enough tradition documents that
comprehenders retain components of an initial misreading after recovering from a
garden path [CITE: Christianson & Ferreira; Slattery et al.; van Schijndel &
Linzen]. This is the parallel drawn in §4. Dynel's taxonomy of conversational humor supplies
the garden-path and pun distinction of §1 and §4 [CITE: Dynel].

**Metastability in neural dynamics.** Coordination dynamics and the
winnerless-competition framework describe cognition as sequences of transiently
stable states that are not fixed-point attractors [CITE: Kelso; Rabinovich et al.;
Sussillo & Barak]. We take the term from there.

**The motivating case and the model.** The case described in §1 is Raine v. OpenAI, filed in the Superior Court of
California, San Francisco, on 26 August 2025, with contemporaneous reporting [CITE:
filing; CNN, 26 August 2025; NBC News]. A later report covers the defendant's answer
denying causation [CITE: TechCrunch, 26 November 2025]. The litigation is contested.
This paper characterizes only what the filing and reporting describe. The safety training of the model we study is
documented in its model card [CITE: gpt-oss model card].

## Appendix A — Corrections that changed reported values

Four corrections made during the study's audits changed values as printed. Each is
recorded here in one line; the complete corrections record, nineteen entries, is in
the repository.

1. The real→fictional remnant gap was first reported with an interval that held
   the no-shift references fixed, [0.11, 0.58]. Resampling the six reference runs
   as well widens it to [−0.12, +0.79], which includes zero, so that remnant is
   reported as suggestive only (§3.2, Table 2).
2. The within-stream readings of the tank task were first reported as untrimmed
   means, which heavy tails inflated. The paper now reports trimmed means: +0.34 and
   +0.37 at ten post-shift sentences and +0.52 and +0.53 at twenty (§3.3).
3. Crossing times were first summarized as a range read from the mean trajectories.
   The paper now reports per-run medians: 10.5 and 6.0 sentences in the tank task and
   4.0 and 5.0 in fiction/real (§3.2, Table 2), with the mean-trajectory crossings
   given separately in the Figure 1 caption.
4. The recency integrator's memory was first stated as a range of sentences derived
   loosely from its decay parameter. The paper now reports the per-direction median
   decay values (Table 2) and the weighted-mean evidence ages they imply: about nine
   sentences in the fiction/real task, fourteen from vehicle to aquarium, and beyond
   the window from aquarium to vehicle (§3.2).

One further correction predates the draft. A first estimate of stickiness (§3.6)
used a null with γ imported from the transition fits and gave +3.7, significant; it
was retracted the same day when the null was fitted to the sweep cells, and the
paper reports only the fitted-null values (Table 5).

## Appendix B — Quality assurance and reproducibility

**Regeneration.** A full regeneration audit re-ran every committed analysis script
over the frozen captures and reproduced every reported value. The calibration axes regenerated bit-identically. The seeded bootstraps regenerated
exactly. The diff over all 23 scripts was clean.

**Fixtures.** A permanent fixture suite pushes synthetic data with analytically known
answers through the actual pipeline functions. Nine of nine fixtures recover their
known answers.

**Audits.** Sign audits confirmed that midpoint-referenced readings have zero
own-class sign violations across all 24 layers of both tasks, and that the
per-layer accumulated-context axes keep held-out sign with accuracy 0.93–1.00.
Boundary audits confirmed contiguous positions 1 to 40 in every run and the correct
target token for every carrier. Join audits confirmed that calibration items are
drawn from the same pools as the context sentences and that held-out folds separate
by construction. Family-level label shuffles kill every effect they are run on (Table 7).

**Table 7.** Label-shuffle audits. Each effect is recomputed with the class labels
shuffled at the scene-family level. The shuffled column gives the permutation band
or mean. The minimal-pair row is the fiction/real task; the remnant-gap row is the
tank task, averaged over its two directions.

| Effect | Unshuffled | Shuffled |
|---|---|---|
| Minimal-pair shift (axis units) | +0.99 | band [−0.20, +0.21] |
| Scene-held-out accuracy | 0.907 | 0.530 |
| Remnant gap (axis units) | +1.66 | band [−1.42, +1.31] |


**Capture days.** The chat template stamps the capture date into every input (§2.1).
The tank transition runs, no-shift runs, and calibration set were captured on 27
August 2026, except two transition runs and one no-shift run captured the next day.
Every fiction/real transition run, no-shift run, and calibration item was captured on
28 August. Each task's checkpoint captures fall on one day, as do its mixture-sweep
cells and the minimal pairs. Behavior completions were generated on later days, and
each completion's reading comes from the same forward pass as the completion. A
committed script reproduces this table from the session manifests.

**Additions after the freeze.** Six analyses were added after the analysis freeze, all
computed from the frozen captures or their manifests through committed scripts, and each
is noted as a post-freeze addition where it appears: the tank response counts of §3.5 (zero of 96
completions ask which sense is meant); the monitor ROC of §4 (AUC 0.61 [0.43,
0.76]); the per-layer collapse panels of §3.2 (Fig. fig_s13_collapse_layers and
Table 3); the exploratory per-layer behavior association of §3.5 (Fig.
fig_s14_behavior_by_layer); the channel-reach and frame-query counts of §3.5; and
the capture-day table above.

**Names used in the repository.** Readers of the repository will meet different
names for some of the paper's terms.

- The paper's *remnant* is the repository's "residual".
- The dwelling within the unresolved zone is the repository's "park".
- The *accumulation offset* is the repository's "accumulation drift".
- The paper's *tasks* are the repository's "probes" or "probe arms".
- The corpus directories D3, D4, D5, and D6 are the transition, no-shift,
  minimal-pair, and mixture-sweep corpora.
- The repository's "K=1" label names an analysis convention for a routing track this
  study dropped.

Regeneration instructions are in the study README. [That README does not exist yet;
Andrew's ruling on writing it.]

## Appendix C — Supplementary figures

Eleven supplementary figures are in the repository's figure directory, alongside a
copy of the matched-composition behavior figure of §3.5. They are: the per-run fit
gallery for the fiction/real task; the hysteresis loop for the fiction/real sweep;
the per-layer heatmap for the tank task under the refit axes; the raw-axis heatmaps
for both tasks and the midpoint-referenced heatmap for the fiction/real task, which
show the instrument before the corrections of Box 1; the ' word' site just before ' tank' in the carrier;
the occupancy bands at layer 4; the jumpiness diagnostic; the norm-against-alignment
diagnostic; and the calibration accuracy by layer. The monitor ROC is in the main
text.
