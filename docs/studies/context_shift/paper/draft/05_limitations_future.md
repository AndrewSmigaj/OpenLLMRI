<!-- Section 5: Limitations and future work. Rewrite step 2 (2 Sept 2026). All claims
of the previous version retained. -->

# 5. Limitations and future work

**One model, stated plainly.** Everything here is measured in one 20-billion-parameter
mixture-of-experts model, with greedy decoding, so the behavior rates of §3.5 are properties of the greedy
continuation, and so are the loops that leave many completions without an answer.
Deployed decoding samples, which breaks such loops; behavior under sampling is
untested here.
Three kinds of claim should be kept apart. Descriptive claims about gpt-oss-20b are established for the tested tasks,
contexts, sites, and decoding conditions, since this model is the population of
interest. Existence
claims about the class, that a deployed language model can dwell between
interpretations, can carry a mixed-context signal its behavior does not use, and can
have safeguard behavior weakened by ordinary coherent context, need only one model.
Prevalence claims across models are untested here, and the paper makes none.
This is the mode of work that the recent circuit-level biology of a single
language model adopted: one deployed system characterized in depth, with transfer
left to later work [CITE: Lindsey et al. 2025]. The
model is itself deployed and open-weight, so its characterization has safety
relevance of its own, independent of any transfer to other systems.

Each dynamics claim is made at one calibrated site and layer per task. Those sites are single rows of a depth progression in which crossing times vary
systematically across layers (§3.2). No single layer
is a sufficient readout of the model's state, and behavior is produced downstream of
all of them. Within the study, replication is internal. Its scope is set out in §2.3: the task contrasts, carriers, sites, and scene
families.

**What did not replicate cleanly.** The real-world→fiction-writing remnant is suggestive only
once reference uncertainty is propagated. The ' letter'-site asymmetry rests on four
runs per direction. In the fiction/real task, 48% of runs are indeterminate under per-run
trajectory-model selection. And our pre-registered prediction about the ordering of crossing times across
layers held in one task and failed in the other.

**Patterns seen on two tasks.** Two further patterns hold across the tasks. With two
tasks they are observations, so we treat them as hypotheses rather than findings.
The task with the wider endpoint separation also shows the larger remnant gaps. And
the two tasks differ in whether their contrast is anchored to one token or spread
across the utterance.

**The named open question.** Are the remnant and the dwelling permanent, or only
slower than twenty sentences can resolve? In the terms of §4, is the dwelling a pun
or a long garden path? Two experiments would decide it. One extends the post-shift
horizon. The other shifts the evidence back to the original class after the shift
and measures what remains of the second frame. Both are designed and costed. Neither has run.

**Further deferred work,** in rough order of leverage:

- Regenerate the behavior completions under sampling at the model's default
  temperature, several draws per cell. The two readings of §3.5 bracket the
  safeguard's rate; sampling, which breaks the loops, decides where in the
  bracket the deployed model sits.
- Replicate the fiction/real headline quantities at the ' write' site, where the
  framing contrast reads most strongly. The existing recordings suffice.
- Expand the ' letter'-site families.
- Build calibration sets from a third, unrelated class, to identify what the
  accumulation offset contains.
- Construct a monitor from several sites, the mixed-context marker, and per-layer
  readings, and test it against the chance-compatible single-site baseline of §4.
- Localize where safeguard behavior reads in the stack by patching shallow against
  mid-stack states during generation. This is the decisive test for the three
  candidate accounts of §4.
- Run a benign-framing control arm: the same carrier with one word swapped, such as
  a resignation letter, with contexts built by the fiction/real recipe with the theme
  swapped, so that cue density is matched by construction. A benign request has no
  safeguard to trigger, so this arm separates the trained-default account of §4 from
  the pretraining-register account, where patching only localizes. It is specified
  here and not yet run.
- Run a suite of harder context manipulations: colliding frames, frames that mutate
  mid-context, and deliberately incoherent contexts. Genuine off-distribution
  excursions are most likely there. Our clean block shifts are the tamest possible
  case.

