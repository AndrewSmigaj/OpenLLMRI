# Plan: v1.1 correction now, then study version 2 (date-free recapture at scale with the sampled arm built in)

## Context

Andrew wants the date issue out of the paper: recapture every corpus with the
chat template's date held constant, and use the recapture to enlarge the study.
Rulings (8 September, two sets): constant date through the existing
`pin_date`, stock template, no source change; double the families to 24 per
class per task with distinct sentences (no paraphrases); runs stay 40 steps
(R-C: hold at 40, the 60-step study queued with its own later capture, since
its real cost is about 1,900 more blind sentences); behavior = greedy one pass
plus sampled m = 5 at k ∈ {2, 6, 9, 12, 20} (R-B: k = 9 added, about +25%
behavior time) and at the no-shift end, sampled primary; plus the sweep-cell
subset (R-A: k ∈ {8, 10, 12} in both block orders, 144 fiction/real cells,
greedy plus five draws, about 29 GPU-hours) as the order-dependence test of
behavior and the substrate for the marker regression; bands ±0.5 axis units
from the position-matched midpoint in both tasks (A4), amplitude-relative
bands in the sensitivity table; a v1.1 correction on the existing captures
first, because the posted paper's fiction/real band labels are wrong in
public. The reviewer's adjudication (8 Sept) approves the plan as the program
of record and green-lights Stage 0 now.

Facts that shape the plan:
- Every study chain uses `/api/probes/sentence-experiment`, which accepts
  `pin_date`; pinning is a payload field in each chain. The v1 corpus took
  2.5 GPU-days; sampled draws cost ~128 s (fiction/real) and ~57 s (tank).
- Pools: 25 sentences per family per class (tank 12 × 25 per class; fiction/real
  12 × 25 per sub-arm and per class). Runs take 20 per block.
- Disk: lake 70 GB; v2 at doubled families ~100 GB; 184 GB free.
- The v1 behavior bands cut the raw reading at ±0.5. The tank midpoint is 0.04,
  so its bands are right. The fiction/real accumulation offset puts the
  fiction-writing reference at +0.13 and the real-world reference at +1.81 at
  position 40 (midpoint ≈ +1.0), so v1's "middle band" (40 cells) lies wholly
  inside the referenced fiction-writing side and v1's "real-world side" pools
  the referenced middle (109) with the real side (50). The numbers on those
  cells were computed correctly; their labels were not, against the paper's
  own Box 1 rule 3.
- Pilot (sampled arm on v1 captures): loops 0 of 720; assistance follows the
  recent fiction-writing content (real-world→fiction-writing: 0, 3, 12, 22% at
  k = 2, 6, 12, 20; fiction-writing→real-world: 19, 14, 12, 10%; pure-fiction
  no-shift 22%, pure-real 0%); by referenced band, 20 / 10 / 7% per draw at the
  fiction side / middle / real side, monotone at every cut tried (±0.25, 0.5,
  0.75 amplitude); within direction × k strata the reading adds little
  (13% vs 10% below and above the stratum median). Position matching of
  behavior cells to run steps verified (median difference 0.005 axis units,
  the date effect; the same position is the best match in 158 of 192).

## Adjudication amendments adopted (8 September)

- **A1.** Pre-register residual concentration (overdispersion after
  conditioning on band, direction, and context type; beta-binomial or
  clustered quasi-likelihood, m handled natively) and the retry curve from
  the fitted mixing distribution for a = 1..5, anything beyond labeled
  extrapolation.
- **A2.** The abstract P3 sentence gates on five checks at Stage 0's end: the
  four cells it asserts at ≥ 90% (middle and real side under each policy) and
  the fiction-versus-middle difference interval excluding zero. Fallback
  drafted now, composition form: "as the fiction-writing block lengthens from
  two to twenty sentences, the share of answers that take up the letter rises
  from none to one in five." Both sentences in the number trace.
  Gate evaluated on 8 Sept with the ±0.5 axis-unit referenced bands: the four
  ≥ 90% cells pass (greedy delivered middle 95%, real 94%; sampled per draw
  middle 90%, real 94%), but the fiction-minus-middle per-draw difference is
  +0.11 [−0.02, +0.21] (12 families), so the fifth check fails and the
  composition-form sentence is the abstract's sentence for v1.1; the band
  contrast is stated in §3.5 with its interval, and its resolution is a
  pre-registered v2 prediction. Prompt identity between behavior cells and run
  steps confirmed (12 of 12 identical), so the wider date bound is the date
  alone.
- **A3.** Corpus-drift QA before any v2 behavior analysis: per-family held-out
  d′ and calibration spread, v1 families against v2 families, so "fragile"
  and "drifted" are distinguishable if pilot predictions fail.
- **A5.** Stage A status line: the benign-framing arm has no captures and no
  committed predictions beyond §5's description.
- **A6.** No correction owed to the posted summary sentence (the referenced
  middle is about 90% safe under both policies); any new post waits for v1.1.
- **§4 rework.** The corrected picture removes the middle band's
  special-protection exhibit: the middle is intermediate on a monotone
  content gradient. The trained-default paragraph is rewritten, not
  number-swapped; the surface-keyed account gains standing; the three-accounts
  structure stays, re-weighted. Andrew reads §4 in the v1.1 pass with this in
  mind.
- **V1, V2.** The stale-claim sweep adds "in-between zone", paraphrases of the
  89% claim in §1 and §4, and contribution 5; the number trace covers every
  cell of the side-by-side table and both abstract candidates.

## Writing rule for v1.1 and v2 prose (Andrew, 8 September)

Standard technical English, plain register, the paper's naming rule and
quote-alone rule; stay within the writing standard's length targets unless
going over makes the paper better. Every rewritten section gets a readability
pass by a Sonnet reviewer (subagent, model sonnet) asked for human readability
and writing advice, before Andrew reads it; the reviewer advises, it does not
author. Its advice is applied by hand and logged in REVISION_LOG.

## Refinements from the review

1. **Band definition.** Use the same ±0.5 axis-unit band as frozen, measured
   from the position-matched no-shift midpoint instead of from zero. This is
   the minimal correction: the tank bands are provably unchanged (midpoint
   0.04) and the fiction/real bands become what the paper's own referencing
   rule says they must be. Sensitivity at ±0.25, ±0.5, ±0.75 amplitude
   reported in the record. The same definition is pre-registered for v2.
2. **What the gradient means.** The composition view is the honest primary
   statement: assistance rises with the length of the recent fiction-writing
   block and falls as real-world material accumulates, in both regimes. The
   band view restates this through the reading. Whether the reading adds
   anything beyond composition is not detectable on transition cells. The
   sweep cells do not settle it either: the two block orders hold the total
   composition fixed but not its recency, and both the reading and, plausibly,
   the behavior weight recent content, so order moves both. What the
   sweep-cell behavior arm can test is whether behavior shows the same
   hysteresis as the reading at fixed composition (an order-dependence test,
   worth having). The reading-versus-composition question is a model
   comparison, pre-registered as such: assistance predicted by the reading
   against assistance predicted by the best recency-weighted fiction share
   (its own fitted decay), family-clustered, on all behavior points. It
   separates them only to the extent the two decorrelate; if they do not, the
   paper says so. Neither v1.1 nor v2 says "the reading drives behavior."
3. **The date-effect bound widens.** Across the 192 transition cells, captured
   one day after their runs, the reading differs by a median of 0.005 and at
   most 0.067 axis units, against the 0.02 the paper states from 24 cells. v1.1
   states the wider bound after a prompt-identity check (one cell's input text
   against its run step); it does not change any conclusion (3% of the class
   separation, still an order of magnitude below the smallest effect) and it
   disappears in v2.

## Stage 0. v1.1 correction on the existing captures (about a day)

- Analysis: `s24_sampling_analysis.py` and `r6_behavior_figure.py` take the
  referenced band for the fiction/real task (position = 20 + k, or 40 for
  no-shift cells; midpoint and amplitude from `second_pass_r1_dynamics.fr_cfg`);
  greedy delivered, greedy reasoning commitments, sampled per draw, sampled
  per cell recomputed with family-clustered intervals; the cross-tab of raw
  against referenced bands; the k-by-direction composition table with
  intervals; the within-stratum permutation test; the sensitivity table; the
  prompt-identity check and the 192-cell date-effect distribution.
- Record: FINDINGS_FINAL corrections log entry (date, script, old labels, new
  values); sampling addendum Part 3 re-tabulated with the raw-band table kept
  and marked superseded, Part 5 for the discovery; REVISION_LOG.
- Paper v1.1: Appendix A item 5 (what was wrong, what was not, the rule that
  forced it, tank unaffected); §2.5 band definition and the two decoding
  policies; §3.5 rewritten on referenced bands with the sampled regime primary
  and greedy kept for the loops, the loop-versus-commitment association, and
  the bracket the sampled arm resolves; one side-by-side table (bands × greedy
  delivered / greedy reasoning / sampled per draw / sampled per cell) and the
  composition table; loops resolved as committed (77 of 85); mixed answers;
  matched composition; clarification counts by regime; the per-layer note.
  Abstract P1 two policies; P3 re-proposed for Andrew's ruling: "The
  suicide-letter task has a refusal safeguard. It holds while the reading sits
  between the frames and once it has settled on the real-world side, in nine
  answers of ten or more under either decoding policy, and it is weakest once
  the reading has reached the fiction-writing frame: there, under the model's
  recommended sampling, one answer in five takes up the letter." §1 opening
  and contribution 5; §4 safety and trained-default paragraphs on the
  gradient; §5 decoding paragraph and deferred list; Appendix B both passes
  and the wider date bound; new sampled figure beside the regenerated greedy
  figure; bib entry for the README's sampling recommendation; number_check
  RECORD; stale-claim sweep for "middle band", "between the frames", "89%",
  "holds", "one answer in four".
- Andrew reads the abstract, §3.5, §4, Appendix A; commit; push; `paper-v1`
  moved, label "Preprint, version 1.1 — date"; upload fields updated.

## Stage A. v2 design and pre-registration (before any capture)

- `findings/preregistration_v2.md`, one dated document, committed before the
  first capture. Contents: the constant date; corpora and sizes (24 families
  per class per task; transitions 48 tank and 96 fiction/real runs; no-shift
  12 per class per task; checkpoint runs 12 per class, doubled from 6 because
  the d′ estimates were the paper's stated weak point; minimal pairs
  recaptured as is; sweeps per family; behavior points at k ∈ {2, 6, 12, 20}
  and the no-shift end, greedy plus m = 5, seeds fixed per point and draw; the
  optional sweep-cell behavior subset, k ∈ {8, 10, 12} in both orders, 144
  cells, as the matched-composition test); the band definition; the
  categorization doctrine including mixed, blind and shuffled; the analyses
  (every v1 script unchanged as the regeneration audit; the sampled items;
  the composition view; the referenced-band view; the within-stratum test;
  the reading-versus-recency-weighted-composition model comparison; the
  sweep-cell arm as an order-dependence test of behavior); predictions
  from the pilot, to be tested not re-fit (loops absent under sampling;
  assistance rising with recent fiction content; safe rate lowest at the
  fiction side, about 80% per draw; positive remnant gaps in all four
  transitions; the tank aquarium→vehicle dwell); the exploratory list; the
  single-amendment rule.
- Authoring under the blind protocol: 12 new scene settings per class per
  task, distinct from the existing 12, added to `specs/scene_families.md`;
  batches of 25 from `specs/blind_batch_template.md` by authoring sessions
  that see only the contrast spec (never this plan or the findings);
  `pool_audit.py` for the "tank" ban, sub-arm rules, family caps, duplicates;
  token budgets by `assemble_contexts.py`; pool files versioned v2.
- Chains: constant `pin_date` in every payload; the behavior chain's draw loop;
  new family manifests; `s16`/`s17` labels for v2. Old lake untouched.
- Optional, Andrew's call, costed: extra behavior points at k = 4 and 9
  (+50% behavior time); the sweep-cell behavior subset (~29 GPU-hours).

## Stage B. Captures (about 5 GPU-days before behavior, about 4.5 for behavior)

Order as v1: calibration → transitions and no-shift → checkpoints → minimal
pairs → sweeps → behavior greedy → behavior sampled (→ sweep-cell behavior if
chosen). Each corpus verified before the next (counts, `has_gen`, no-shift
runs on their own side at every layer); determinism smoke on the constant
date across a backend restart; detached processes; monitored at boundaries.

## Stage C. Analysis

The committed scripts over the v2 captures (regeneration audit), then the
pre-registered analyses; corrections log continues; figures regenerated.

## Stage D. Paper v2

Numbers rewritten throughout; §2.1 keeps one sentence on the constant date;
§2.5 two policies; §3.5 on referenced bands with the composition view and the
sampled regime primary; §3.1 d′ on 12 runs; §4 and §5 revised; Appendix B
without the date material; Appendix A carries the v1 band-label correction.
Version 2 label, tag `paper-v2`, upload fields; v1.1 stays at its tag.

## Risks and how they are held

- Authoring blindness: sessions with the spec only; audit before capture.
- Harness interruptions over a ten-day run: detached chains, resumable logs.
- Disk: old lake kept until the audit passes, then archived off the system
  drive; the v1 archive promise is kept.
- Over-claiming: the reading-drives-behavior sentence is banned; the
  composition view leads; the sweep-cell test decides.

## Verification

- Pre-registration committed before the first capture; later analyses named
  there or labeled exploratory.
- Regeneration audit passes on v2; axes bit-identical across a restart.
- Band cross-tab printed once; no-shift cells fall on their own side.
- Number trace and preservation; stale-claim sweeps for "date", "pinned",
  "middle band", "between the frames".

## Queued: README refresh (approved in principle, 6 Sept); the reviewer's
surviving items (stratified deeper draws, residual concentration, marker
regression on sweep cells, monitor retest, retry curve, benign-framing arm,
60-step extension).
