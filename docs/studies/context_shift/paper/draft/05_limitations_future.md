<!-- Section 5: Limitations and future work. Rewrite step 2 (2 Sept 2026). All claims
of the previous version retained. -->

# 5. Limitations and future work

**One model, stated plainly.** Everything here is measured in one 20-billion-parameter
mixture-of-experts model, with deterministic decoding. Each dynamics claim is made at
one calibrated site and layer per task. Those sites are single rows of a depth progression in which crossing times vary
systematically across layers (§3.2). No single layer
is a sufficient readout of the model's state, and behavior is produced downstream of
all of them. Within the study, replication is internal. Its scope is set out in §2.3: the task contrasts, carriers, sites, and scene
families.

**What did not replicate cleanly.** The real→fictional remnant is suggestive only
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
- Run a suite of harder context manipulations: colliding frames, frames that mutate
  mid-context, and deliberately incoherent contexts. Genuine off-distribution
  excursions are most likely there. Our clean block shifts are the tamest possible
  case.

The analyses reported here were frozen before drafting. The additions made after the
freeze are logged as such in Appendix B.
