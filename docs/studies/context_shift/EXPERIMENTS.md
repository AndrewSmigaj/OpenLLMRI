# Experiments and roadmap — context-shift study

Tracks deferred experiments for the "Unresolved: Semantic Metastability…" study. The
science future-work list lives in the paper's §5 (Limitations and future work); this file
holds the engineering-heavier items and the ones deferred in the 12 September 2026 cleanup
cycle, so nothing is forgotten. The released v1.1 paper stands on the v1 corpus.

## Deferred this cycle (12 September 2026)

### 1. Orthogonal-cue minimal-pair decomposition
**Why deferred:** it is a new experiment with an uncertain outcome, not a cleanup, and its
result could reshape §3.1 and §4. **What it is:** the current 150 minimal pairs (§3.1)
bundle their cue — the fiction arm pairs a fiction-production noun with present tense, the
real arm a temporal deictic with past tense — so a single low-level feature could carry the
+0.99 effect. Author content-fixed pairs that vary **one** dimension each, over the six D5
domains: *tense-only* (present vs past, present-compatible deictics both sides),
*person-only* (grammatical person flipped, frame held), *noun-only* (the production noun
swapped for a neutral connective, tense held). Capture on the sentence-experiment route,
then decompose the pair effect by arm with domain-clustered intervals. **This is also the
proper test of the dose question** that the v1.1 cleanup removed from §3.1 (the
"one cue moves as far as four" claim had no committed computation). **Risk:** if tense-only
or person-only carries a large share, that is a disclosed confound and §3.1's "framing
cues" wording (and §4's early, surface-keyed-trigger account) must be hedged. Needs blind
authoring + a small GPU capture + a new analysis (`s9_orth_decomposition.py`).

### 2. Full v2 corpus recapture
**Why deferred:** its main driver — removing the date-token discussion from the paper — is
now handled more cheaply by the v1.1 de-emphasis and the existing date-effect bound
(Appendix B, reading moves <1% of class separation). **What it is:** blind-authored corpus
with doubled scene families (24/class), two decoding policies from the start, constant
date-pinning, and every reading-side and behavior analysis regenerated on it. Design:
`specs/sentence_set_approach.md`; planned pre-registration: `findings/preregistration_v2.md`
(both marked deferred). Stage-A machinery exists (`analysis/pool_audit_v2.py`,
`generation/build_author_prompts.py`, `analysis/canonicalize_names.py`); 32 of 60 blind
batches were authored. Note before resuming: `pool_audit_v2.py` needs a `__main__` guard and
its balance gate is print-only and unclustered — fix before it gates authoring.

### 3. Causal steering (needs a code change)
Add a scaled copy of the frame axis to the residual at the ` want` site (layer 14) during
generation on the fixed request; sweep real↔fiction; score assist/redirect/refuse/mixed with
the existing categorizer; control sweeps along a random direction and along a length/tense
axis that should stay flat. Needs an additive forward hook near
`backend/src/services/probes/routing_capture.py` (today's hooks are read-only) and GPU time.
This is the decisive test of the §4 accounts and the flagship follow-up.

### 4. Multiple author models
One base model (Claude) authored both classes, so class-conditioned style is co-generated
with the label (the deepest confound, disclosed in `specs/sentence_set_approach.md` §7.1).
Re-authoring each class with a different model family would separate authoring style from the
contrast. Deferred; the surface-feature confound ceiling (§3.1, Appendix B) is the current
mitigation.

## Science future-work (see paper §5)

The extended-horizon and re-shift experiments (is the remnant permanent?), the
forty-sentence static sweep, the ` write`-site replication, the ` letter`-site family
expansion, a third-class calibration for the accumulation offset, the multi-site monitor,
shallow-vs-mid-stack patching, the benign-framing control arm, and the harder
context-manipulation battery are specified in §5 and not repeated here.

## Blog series (conceptual roadmap — recommend, don't draft)

One claim, one figure, one link to the paper per post. Science → Alignment Forum; methods /
platform → LessWrong or a personal blog.

| # | Post | One claim | When |
|---|---|---|---|
| 1 | The stall | When the context shifts, the reading crosses over and then stops halfway. | now (v1.1) |
| 2 | Stimulus sets that don't smuggle in the answer | Blind authoring, name convergence, the surface-feature confound ceiling, the circularity ban. | after the confound appendix lands |
| 3 | Visual data mining with colour blending and UMAP | Patterns visible in a blended projection are invisible in a table. | any time |
| 4 | Acting while unresolved | As a fiction-writing conversation turns real, sampled assistance declines gradually. | after v2 |
| 5 | Steering the frame | Pushing along the frame direction flips the safety behaviour; a length/tense axis does not. | after steering is built |

Recommended order 1 → 2 → 3 → 4 → 5.
