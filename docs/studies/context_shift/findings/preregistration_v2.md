# Pre-registration — context-shift study, version 2 corpus (drafted 8 September 2026)

This document is committed before the first v2 capture and is binding under the
single-amendment rule: every commitment below is fixed now; anything added later
goes into one dated amendment committed before the analyses it governs, and
nothing is added after the captures it concerns have begun. Analyses not named
here are exploratory and will be labeled so. Andrew reads this document before
it is committed.

## Purpose

Version 2 recaptures the whole study with the chat template's date held
constant, removing the date-token discussion from the paper, and doubles the
scene families to strengthen every family-clustered interval. The behavior
corpus is generated under both decoding policies from the start. The v1
captures and the September sampled pilot are design input; their results are
predictions here, to be tested, not re-fit.

## Fixed configuration

- Model, precision, capture route, carriers, sites, and layers exactly as in
  the paper's §2 (gpt-oss-20b as distributed; ' tank' at layer 4; ' want' at
  layer 14; reasoning effort medium).
- **Constant date**: every capture and completion pins the chat template's
  date line to **2026-09-10** via the route's `pin_date` field. The template
  is otherwise stock.
- **Corpora** (24 scene families per class per task; 25 distinct sentences per
  family per class; no paraphrases):
  - Transition runs: 40 steps, shift after 20; 48 tank (24 families × 2
    directions) and 96 fiction/real.
  - No-shift runs: 12 per class per task (even families; a no-shift run draws
    from its own scene plus the next same-label scene, so its "family" label
    spans two scenes' material; clustering treats it by its label as in v1).
  - Calibration: every pool sentence followed by the carrier (600 per class
    for tank; per sub-arm for fiction/real), one capture set per class.
  - Checkpoint captures: 12 runs per class per task (doubled from 6), at the
    v1 checkpoint lengths; d′ by carrier token recomputed on these.
  - Minimal pairs and bare-carrier baselines: recaptured as in v1.
  - Static mixture sweeps: v1 grid per family, both block orders, all 24
    families' even subset as in v1 conventions (the assembled counts are
    recorded in the capture manifest before capture).
  - Paraphrase-carrier and replicate-carrier sets: v1 size.
- **Behavior corpus**: generation contexts at k ∈ {2, 6, 9, 12, 20} post-shift
  sentences for every transition run, plus every no-shift run at its full
  length (tank 264 contexts; fiction/real 504). Two decoding policies from
  identical inputs: greedy, one pass; and the model's recommended sampling
  (temperature 1.0, top-p 1.0, no top-k truncation), m = 5 draws per context,
  the seed for draw n fixed in advance as 20260910 + n and set per request, so
  every draw is reproducible in isolation and later draw extensions never
  re-roll existing draws. Cap 2,048 tokens.
- **Sweep-cell behavior subset**: fiction/real sweep cells at k ∈ {8, 10, 12}
  in both block orders across the 12 sweep families (72 cells), greedy plus
  the same five draws. Purpose: the order-dependence test of behavior at
  fixed total composition.
- **Bands**: the reading minus the position-matched midpoint of the two
  no-shift class means, cut at ±0.5 axis units, both tasks. The sensitivity
  grid (±0.25, ±0.5, ±0.75 of the no-shift amplitude, and ±0.5 axis units) is
  reported alongside every band table.

## Authoring and audit protocol

- Blind authoring: each batch subagent receives one filled template
  (`specs/blind_batch_template.md`) and nothing else. The v2 scene settings
  are in `specs/scene_families.md` (families 13–24 per label).
- Pool audit, hard gates before any capture: target-word and carrier bans;
  fiction/real sub-arm rules (theme-only bans "suicide letter/note/message";
  artifact-mentioned requires one per sentence); exact duplicates; a
  near-duplicate gate — two sentences whose lowercased content-token sets
  have Jaccard overlap ≥ 0.6 count as duplicates, within the v2 pool and
  against the v1 pools; scene share ≤ 15% of a label's pool; chi-square
  balance of length, opener class, and punctuation style across labels; the
  worn-phrase 4-gram scan over v1 plus v2; no personal name in more than one
  family across both versions; and a safe-messaging method-lexicon ban in the
  fiction and real-world classes (no context sentence names a method of
  self-harm), matching the release policy.
- Blind rater pass: a separate rater agent, blind to the design, labels each
  pooled sentence's class from its text alone (forced choice between the two
  class descriptions). Sentences the rater misclassifies are replaced by the
  authoring path and re-audited. **Circularity ban**: no sentence is ever
  screened, selected, or replaced on the basis of the model-under-study's
  readings.
- Name canonicalization (assembly-side, deterministic, logged): blind authors
  converge on a small pool of given names, so after all batches pass the audit,
  `analysis/canonicalize_names.py` renames every given name that occurs in more
  than one family, keeping the first family's use and substituting fresh unique
  names elsewhere from a curated list. Detection is by the lowercase-elsewhere
  heuristic (a capitalized token whose lowercase form never appears as an
  ordinary word). This is a single-token, class-neutral transform (names occur
  in both classes and carry no class signal); the substitution log is committed.
- Logs and paths: v2 chains write the canonical log filenames; v1 logs are
  archived under `captures/v1/`; axes and log paths route through one
  indirection (`analysis/corpus_paths.py`) whose defaults are the v1 values.

## Pre-stated analyses

1. **Regeneration audit**: every committed v1 analysis script runs unchanged
   over the v2 captures; axes bit-identical across a backend restart on the
   constant date; seeded bootstraps exact.
2. **Reading-side quantities**, as in the paper: held-out calibration accuracy
   with the per-fold table recorded; crossing medians; remnant gaps with
   family-clustered and reference-resampled intervals; per-run model
   selection; within-stream readings; dwelling decomposition; hysteresis and
   fitted-integrator excess; geometry and the mixed-context marker with its
   checks; d′ by carrier token on 12 runs per class.
3. **Behavior, per regime and never pooled across regimes**: loop rates;
   category tables; referenced-band rates with family-clustered intervals and
   the band differences with intervals; the composition view (assistance by
   direction and k, with intervals); clarification-request counts by regime;
   loop resolution against the greedy reasoning commitment; matched
   composition (the tank pooled test at k ∈ {6, 12} on |referenced signed
   reading|; the fiction/real comparison at k = 2 per draw).
4. **Within-stratum permutation test**: reading permuted among contexts within
   each direction-and-count stratum, 4,000 permutations, two-sided.
5. **Reading versus composition, model comparison**: per-context assistance
   probability predicted by (a) the referenced reading and (b) the best
   recency-weighted fiction share with its own fitted decay, compared by
   family-clustered cross-validated likelihood; the two separate only to the
   extent the predictors decorrelate, and the paper says so if they do not.
6. **Sweep-cell order dependence**: at fixed k, assistance rate by block
   order, family-clustered difference; read beside the reading's hysteresis.
7. **Residual concentration**: overdispersion of per-context assistance after
   conditioning on band, direction, and context type (transition, sweep,
   no-shift), beta-binomial or clustered quasi-likelihood, m handled natively.
8. **Retry curve**: from the fitted mixing distribution, the probability that
   at least one of a draws assists, reported for a = 1..5 only; anything
   beyond labeled model-based extrapolation.
9. **Corpus-drift QA**, before any v2 behavior analysis: per-family held-out
   d′ and calibration spread, v1 families against v2 families, so "phenomenon
   fragile" and "corpus drifted" are distinguishable.
10. **Monitor retest**: the reading as a predictor of per-context assistance,
    fit and scored on disjoint scene families.

## Predictions (from v1 and the September pilot; tested, not re-fit)

P1. No sampled draw loops; greedy loops recur at a nonzero rate.
P2. In the fiction-writing→real-world direction, sampled assistance declines
    with accumulating real-world sentences (pilot: 19, 14, 12, 10% at
    k = 2, 6, 12, 20) and its floor stays above the pure real-world rate
    (pilot: 0 of 18 draws).
P3. In the real-world→fiction-writing direction, sampled assistance rises
    with the fiction block (pilot: 0, 3, 12, 22%).
P4. Referenced-band ordering: assistance highest at the fiction-writing side,
    lowest on the real-world side, in both regimes; with 24 families the
    fiction-side-minus-middle per-draw difference's clustered interval
    excludes zero (pilot point estimate +0.11).
P5. All four remnant gaps positive with references fixed; the tank
    aquarium→vehicle population dwell (level and late-slope bounds as in the
    paper) recurs.
P6. Crossing medians fall in the v1 range by task and direction (4–10.5).
P7. The minimal-pair framing effect replicates in sign and rough size.
P8. The mixed-context marker is present (family-clustered null, p < 0.01).
P9. The reasoning channel's final commitment matches the delivered answer
    wherever one arrives, in both regimes.
P10. The tank matched-composition pooled test (k ∈ {6, 12}) separates under
     sampling (pilot p = 0.012).

## Exploratory (labeled as such wherever reported)

Per-layer analyses; the fiction/real matched-composition comparisons beyond
k = 2; marker-versus-behavior tests; the ' write'-site replication; anything
using the v1 captures; any analysis not named above.

## Sign-off

Committed after Andrew's read, before the first v2 capture. Amendments: one
dated amendment file at most, per the single-amendment rule.
