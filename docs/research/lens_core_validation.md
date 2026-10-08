# Lens validation: first runs (lens slice 1, 10b.7, 2026-10-08)

Related: docs/DESIGN.md (C3 choosing k, C4 validating), backend/src/services/lenses/validate.py

What the k profile and held-out scores show on two captures, beside the in-sample automatic k
methods. Every number here comes from the lenses' `validation.json` and `lens.json` files in the
lake (paths below), produced by the `lens_validate` job and the build's self-check.

## How the scores are made

- **Folds.** When items name a scene family, fold *i* holds out family *i* of every class (the
  paper's scheme). Otherwise folds are stratified by label with identical texts kept together;
  these are weaker, because sentences from one setting can sit on both sides.
- **Held-out scoring,** per layer and fold: UMAP (the lens's neighbours, dimensions and seed) and
  Ward are fitted on the training items; held-out items are transformed into that space and each
  takes the cluster its 15 nearest training items vote for (weighted by 1/distance); a cluster
  predicts the majority label of its training items. Cohen's κ and accuracy are pooled over all
  held-out items; AMI is computed per fold and averaged by fold size.
- **The k profile:** for every k from 2 to 10, silhouette and agreement with each axis (in-sample,
  on the lens's own embedding), agreement across three UMAP seeds (mean ARI), and the held-out
  scores.

## Tank polysemy, five senses (`session_1434a9be`, lens `tank-k5-n15`)

499 items, k = 5 at every layer, UMAP n = 15, 6-D. No scene families, so 5 stratified folds
(weaker). Chance accuracy is 0.2.

| Layer | κ at k = 5 | accuracy | worst fold | held-out best k (κ) | elbow | silhouette | levels |
|---|---|---|---|---|---|---|---|
| L0 | 0.15 | 0.32 | 0.25 | 7 (0.17) | 2 | 2 | 2 |
| L4 | 0.45 | 0.56 | 0.53 | 7 (0.56) | 2 | 6 | 3 |
| L8 | 0.54 | 0.63 | 0.55 | 9 (0.61) | 2 | 6 | 2 |
| L11 | 0.60 | 0.68 | 0.60 | 10 (0.65) | 2 | 6 | 2, 6 |
| L13 | 0.62 | 0.69 | 0.56 | 10 (0.65) | 2 | 3 | 2, 8 |
| L16 | 0.49 | 0.59 | 0.51 | 9 (0.58) | 2 | 2 | none |
| L20 | 0.41 | 0.53 | 0.45 | 8 (0.44) | 2 | 4 | 3, 4 |
| L23 | 0.38 | 0.51 | 0.43 | 8 (0.51) | 3 | 3 | 3, 4, 7 |

- The senses separate most in the middle layers: held-out κ at k = 5 rises from 0.15 at L0 to
  0.60–0.62 at L11–L13, then falls to about 0.4 by L20–L23.
- The in-sample methods still don't find five. Elbow picks 2 at 20 of 24 layers; silhouette
  wanders between 2 and 8; hierarchy levels include 5 only at L18 and L19.
- The held-out best k is 7 to 10 at every layer, above the five senses: finer clusters are purer,
  so they classify better. The gain over k = 5 is small (L13: κ 0.62 to 0.65), and choosing k on
  the held-out score is selection-biased, so it is offered as a suggestion that says so.
- Seed agreement at k = 5 is 0.48–0.94 (mean ARI with two other seeds).

## Tank calibration, aquarium against vehicle (`session_29a80932`, lens `calibration-q1-k2-n15`)

600 items at token position 1, k = 2, UMAP n = 15, 6-D. Items name their scene (24 scenes, 12 per
class), so 12 folds each hold out one aquarium scene and one vehicle scene. Chance accuracy is 0.5.

| Layer | κ at k = 2 | accuracy | worst fold | held-out best k (κ) |
|---|---|---|---|---|
| L0 | 0.04 | 0.52 | 0.42 | 10 (0.29) |
| L3 | 0.59 | 0.79 | 0.58 | 9 (0.72) |
| L4 | 0.66 | 0.83 | 0.64 | 9 (0.79) |
| L5 | 0.72 | 0.86 | 0.66 | 9 (0.81) |
| L12 | 0.56 | 0.78 | 0.70 | 9 (0.69) |
| L20 | 0.53 | 0.77 | 0.60 | 9 (0.74) |
| L21 | −0.15 | 0.42 | 0.20 | 8 (0.71) |
| L22 | 0.01 | 0.51 | 0.36 | 9 (0.78) |

- On held-out scenes the two-cluster lens peaks at L5 (accuracy 0.86) and reaches 0.83 at L4. The
  paper's mass-mean axis on the same data scores 0.905 at L4 (reproduced in the plan review), so
  here the designed axis classifies better than the top split of the UMAP lens. Slice 1's fair
  comparison (10b.8) sets them side by side at the same k.
- With more clusters the UMAP lens closes most of the gap: held-out κ 0.79–0.81 at k = 9 in L4–L5.
- At L21–L22 the top split follows none of the designed axes (in-sample AMI with the label −0.00
  and 0.02, with the scene 0.04), while finer cuts still classify (κ 0.71–0.78). The surface
  check (10b.9) is the tool for asking what it follows.

## The self-check, and what it showed about nesting

Every build now fits a planted layer (five classes in two groups) and a null layer, both shaped
like residuals, with the build's own settings and item count. It passes when the 5-cut finds the
planted classes (ARI ≥ 0.9) and the null's 5-cut agrees with random labels no better than
AMI 0.1. The calibration lens passed (ARI 1.0, null AMI −0.002).

Building the check showed a limit of UMAP + Ward for nested structure: both levels (2 and 5)
appear only when class and group separations are comparable. With classes well apart, UMAP keeps
them and loses the groups' distances (in the calibration lens's self-check the 2-cut scored ARI
0.025 against the groups); with classes close together, only the groups appear. So the check requires the classes and reports the groups,
and the hierarchy-levels method can miss an upper level for the same reason. This bears on the
open question of better automatic methods (DESIGN.md C3).

## Caveats

- The tank lens has no scene families, so its held-out scores are from weaker folds.
- `carrier_id` and `n_context` hold one value each in the calibration capture; they appear as
  axes but carry no information.
- Two lenses, one model; these are first readings of the instrument, not results about meaning.

## Files

- `data/lake/session_1434a9be/lenses/tank-k5-n15/validation.json` (75 s)
- `data/lake/session_29a80932/lenses/calibration-q1-k2-n15/validation.json` (165 s)
- Each lens's `lens.json` holds its in-sample suggestions and self-check.
