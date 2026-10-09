# Lens validation: first runs (lens slice 1, 10b.7, 2026-10-08)

Related: docs/DESIGN.md (C3 choosing k, C4 validating and tuning), backend/src/services/lenses/validate.py,
backend/src/services/lenses/search.py

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
  0.57–0.62 at L11–L13 (0.60, 0.57, 0.62), then falls to about 0.4 by L20–L23.
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

## UMAP against raw space, and the mass-mean axis (10b.8)

The validation now scores raw-space groupings on the same folds and at the same k, on the label:
standardized PCA-50 with Ward, the same components with spectral clustering, and relevant-neuron
PCA (the top 200 neurons by ANOVA F chosen inside each training fold, 10 components, Ward). The
supervised ceiling is logistic regression on the standardized states. Held-out κ on the label:

| Capture, k | Layer | UMAP lens | raw Ward | raw spectral | relevant neurons | ceiling (accuracy) |
|---|---|---|---|---|---|---|
| calibration, k = 2 | L4 | 0.66 | 0.48 | 0.80 | 0.81 | 0.88 (0.940) |
| | L5 | 0.72 | 0.41 | 0.77 | 0.80 | 0.86 (0.928) |
| | L12 | 0.56 | 0.49 | 0.58 | 0.63 | 0.84 (0.922) |
| | L21 | −0.15 | 0.45 | 0.45 | 0.51 | 0.83 (0.915) |
| tank senses, k = 5 | L4 | 0.45 | 0.56 | 0.51 | 0.62 | 0.80 (0.842) |
| | L8 | 0.54 | 0.54 | 0.55 | 0.49 | 0.82 (0.856) |
| | L12 | 0.57 | 0.56 | 0.58 | 0.54 | 0.80 (0.844) |
| | L23 | 0.38 | 0.46 | 0.45 | 0.58 | 0.81 (0.848) |

- On these two captures, at the same k, the UMAP lens doesn't beat raw space. On the calibration
  scenes at k = 2, raw spectral clustering beats it at L4 (0.80 against 0.66); on the tank senses at
  k = 5 the three unsupervised groupings sit within about 0.1 of each other at most layers. This
  matches the design's 2026-10-06 preview, where raw space matched or beat UMAP on one five-way axis
  and UMAP won only on a combination of two axes (frame × voice). That combination is the next
  comparison to run.
- The ceiling stays well above every unsupervised grouping (κ 0.80 to 0.88 at the layers shown; about
  0.5 at L0): the classes are linearly separable far better than any clustering here recovers them.
- The mass-mean lens on the calibration capture (aquarium against vehicle, token position 1,
  12 scene-family folds) scores 0.905 at L4, the paper's figure exactly, built in 3.4 s.
- Disagreement marks: per layer, items whose co-members in the UMAP node and in the better raw
  grouping (Ward or spectral, by held-out κ at that k) overlap less than half (Jaccard) are marked,
  and the nodes holding them are outlined on the cluster Sankey.

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

## How the axis bears on routing (10b.9)

The node details job (`lens_details`) measured how the aquarium-against-vehicle mass-mean axis
(`aquarium-vs-vehicle-axis-p1`) bears on routing: the spread across experts of the logit change it
predicts through the next layer's router, against 1,000 random directions of the same length.
It stays below the random 95th percentile at every layer, at most 1.26 times the random median
(L11, the 94th percentile). It sits below the median at 19 of 23 layers, and far below it from L13
to L20 (0.19 to 0.59 times): there the routers see this concept less than a random direction.
Through the unembedding the axis reads as the two senses from L9 on, among the eight tokens each
side favours (" armored", " infantry", " convoy" against " aquarium", " fish"), except the
aquarium side at L19. On the tank lens the nodes explain between 0.11 (L1) and
0.49 (L11) of the next layer's routing variance, and surface features alone predict the nodes at
held-out κ 0.14 (L0) to 0.31 (L19).

## The analysts (10b.10)

Analysts (`claude -p`, Claude Opus 5.5) were tested at L13 of `tank-k5-n15` before their cards were
trusted: no decoy (two random populations and the lens with its labels shuffled) was called a
clear pattern, every planted value (aquarium, vehicle, septic) was named, and the members picked
from three nodes' descriptions scored 0.90, 0.90 and 0.85 against majority-label baselines of
0.70, 0.85 and 0.85 (mean 0.88). The save plan then wrote 13 cards in 23 calls, every number
traced to its packet: the distinctive tokens and shares name what each node holds (aquarium, army,
clothing; storage for the node that holds scuba and septic together; nothing clear for the mixed
node).

## Tuned lenses (lens slice 1b, 10c.1, 2026-10-09)

A `lens_search` job tunes a lens. It first holds out a test portion: whole scene families per
label when the items name them, otherwise a stratified 20% (marked weaker). On at most five
selection folds of the rest it scores every UMAP setting (n_neighbors 5, 15 or 50 × 3, 6 or 12
dimensions, `min_dist` 0.1) and every k from 2 to 10 at every layer, and picks each layer's
highest held-out AMI. Then it scores the winner, the lens it started from, the raw-space
groupings and the logistic ceiling on the test portion, which never entered the choice, and
builds the tuned lens. All 9 settings passed the self-check on both captures.

### Tank polysemy (`tank-k5-n15-tuned`)

The test portion is 100 items, stratified (the set has no families); the other 399 make five
selection folds. The job took 8 minutes.

| Layer | settings (n, dims) | k | AMI chosen on | test AMI | test accuracy | untuned test AMI (k = 5) | raw Ward test AMI | ceiling test AMI |
|---|---|---|---|---|---|---|---|---|
| L0 | 50, 12-D | 10 | 0.11 | 0.10 | 0.43 | 0.09 | 0.07 | 0.25 |
| L1 | 15, 12-D | 10 | 0.13 | 0.19 | 0.51 | 0.16 | 0.16 | 0.45 |
| L2 | 15, 12-D | 9 | 0.20 | 0.24 | 0.54 | 0.18 | 0.18 | 0.59 |
| L3 | 15, 12-D | 10 | 0.29 | 0.35 | 0.66 | 0.32 | 0.36 | 0.66 |
| L4 | 15, 3-D | 10 | 0.40 | 0.43 | 0.66 | 0.38 | 0.48 | 0.64 |
| L5 | 15, 3-D | 6 | 0.48 | 0.54 | 0.69 | 0.46 | 0.48 | 0.66 |
| L6 | 15, 3-D | 6 | 0.49 | 0.49 | 0.68 | 0.44 | 0.48 | 0.66 |
| L7 | 15, 12-D | 6 | 0.48 | 0.51 | 0.73 | 0.47 | 0.57 | 0.65 |
| L8 | 15, 12-D | 5 | 0.48 | 0.54 | 0.66 | 0.54 | 0.49 | 0.65 |
| L9 | 50, 12-D | 6 | 0.48 | 0.53 | 0.67 | 0.54 | 0.57 | 0.63 |
| L10 | 15, 12-D | 6 | 0.48 | 0.57 | 0.73 | 0.51 | 0.55 | 0.70 |
| L11 | 15, 6-D | 6 | 0.51 | 0.57 | 0.73 | 0.57 | 0.58 | 0.69 |
| L12 | 15, 12-D | 6 | 0.51 | 0.55 | 0.74 | 0.52 | 0.56 | 0.69 |
| L13 | 15, 12-D | 6 | 0.50 | 0.49 | 0.74 | 0.52 | 0.57 | 0.75 |
| L14 | 5, 12-D | 6 | 0.48 | 0.47 | 0.67 | 0.51 | 0.60 | 0.66 |
| L15 | 15, 6-D | 6 | 0.47 | 0.51 | 0.75 | 0.51 | 0.55 | 0.63 |
| L16 | 15, 3-D | 4 | 0.43 | 0.34 | 0.55 | 0.47 | 0.50 | 0.66 |
| L17 | 15, 12-D | 4 | 0.42 | 0.50 | 0.59 | 0.42 | 0.51 | 0.69 |
| L18 | 5, 3-D | 6 | 0.40 | 0.32 | 0.61 | 0.48 | 0.52 | 0.68 |
| L19 | 15, 6-D | 5 | 0.39 | 0.39 | 0.61 | 0.39 | 0.53 | 0.63 |
| L20 | 15, 6-D | 5 | 0.35 | 0.37 | 0.56 | 0.37 | 0.44 | 0.66 |
| L21 | 15, 6-D | 9 | 0.40 | 0.41 | 0.64 | 0.36 | 0.59 | 0.65 |
| L22 | 15, 6-D | 8 | 0.41 | 0.45 | 0.70 | 0.35 | 0.51 | 0.65 |
| L23 | 15, 6-D | 9 | 0.39 | 0.46 | 0.68 | 0.36 | 0.50 | 0.67 |

- On the test portion the tuned lens beats the untuned one at 15 layers, trails it at 6 and ties
  at 3; the median difference is +0.02 AMI. Both peak at L11 (0.57).
- The search chose k = 6 at L5–L15 apart from L8 (5): one node more than the five senses. It
  chose 9–10 at L0–L4 and 8–9 at L21–L23, where it gains most over the untuned lens's 5 nodes
  (+0.06 to +0.10 at L21–L23).
- It loses most at L16 (−0.13) and L18 (−0.16). There the winner led its best runner-up by 0.012
  and 0.007 AMI on the selection folds: near-ties, as at 22 of the 24 layers, where the winner
  leads by less than 0.02.
- Twelve dimensions won at 12 layers, six at 7 and three at 5; 15 neighbours won at 20 layers.

### Tank calibration (`calibration-q1-k2-n15-tuned`)

The test portion is two scene families per class (aquarium: aquascaping and quarantine_vet;
vehicle: museum and training_range), 100 items. The other 10 families per class make five
selection folds of 500 items. The job took 17 minutes.

| Layer | settings (n, dims) | k | AMI chosen on | test AMI | test accuracy | untuned test AMI (k = 2) | raw Ward test AMI | ceiling test AMI |
|---|---|---|---|---|---|---|---|---|
| L0 | 50, 3-D | 6 | 0.11 | 0.03 | 0.64 | -0.02 | 0.01 | 0.21 |
| L1 | 15, 3-D | 2 | 0.22 | 0.31 | 0.73 | 0.31 | 0.05 | 0.47 |
| L2 | 15, 6-D | 3 | 0.23 | 0.35 | 0.70 | 0.31 | 0.12 | 0.50 |
| L3 | 15, 12-D | 2 | 0.41 | 0.55 | 0.87 | 0.29 | 0.55 | 0.58 |
| L4 | 50, 12-D | 2 | 0.52 | 0.69 | 0.94 | 0.83 | 0.47 | 0.58 |
| L5 | 50, 6-D | 2 | 0.54 | 0.45 | 0.82 | 0.63 | 0.51 | 0.58 |
| L6 | 15, 12-D | 2 | 0.52 | 0.42 | 0.83 | 0.44 | 0.51 | 0.58 |
| L7 | 15, 6-D | 2 | 0.45 | 0.37 | 0.80 | 0.37 | 0.49 | 0.58 |
| L8 | 5, 3-D | 2 | 0.46 | 0.34 | 0.80 | 0.48 | 0.43 | 0.63 |
| L9 | 5, 6-D | 2 | 0.45 | 0.37 | 0.77 | 0.35 | 0.47 | 0.66 |
| L10 | 5, 6-D | 2 | 0.42 | 0.70 | 0.93 | 0.38 | 0.51 | 0.69 |
| L11 | 50, 6-D | 4 | 0.41 | 0.46 | 0.87 | 0.40 | 0.47 | 0.69 |
| L12 | 50, 3-D | 3 | 0.40 | 0.46 | 0.85 | 0.55 | 0.41 | 0.67 |
| L13 | 50, 3-D | 3 | 0.42 | 0.45 | 0.73 | 0.49 | 0.39 | 0.76 |
| L14 | 50, 6-D | 2 | 0.44 | 0.53 | 0.86 | 0.30 | 0.47 | 0.76 |
| L15 | 50, 3-D | 3 | 0.39 | 0.45 | 0.90 | 0.57 | 0.43 | 0.72 |
| L16 | 15, 6-D | 2 | 0.40 | 0.30 | 0.76 | 0.30 | 0.32 | 0.69 |
| L17 | 15, 3-D | 3 | 0.42 | 0.36 | 0.69 | 0.49 | 0.39 | 0.69 |
| L18 | 50, 12-D | 2 | 0.42 | 0.53 | 0.86 | 0.64 | 0.34 | 0.67 |
| L19 | 50, 12-D | 3 | 0.40 | 0.48 | 0.89 | 0.57 | 0.35 | 0.71 |
| L20 | 50, 6-D | 2 | 0.41 | 0.48 | 0.86 | 0.46 | 0.32 | 0.71 |
| L21 | 15, 12-D | 8 | 0.33 | 0.34 | 0.82 | 0.08 | 0.29 | 0.64 |
| L22 | 50, 12-D | 2 | 0.37 | 0.38 | 0.78 | 0.04 | 0.45 | 0.72 |
| L23 | 50, 3-D | 3 | 0.32 | 0.49 | 0.87 | 0.43 | 0.29 | 0.64 |

- Tuning gains nothing reliable here. The tuned lens beats the untuned one at 11 layers, trails
  it at 10 and ties at 3; the median difference is 0.00, and the differences run from −0.18 to
  +0.34.
- The test portion disagrees with the selection folds. At L4 the selection folds preferred the
  tuned settings (50 neighbours, 12-D) to the untuned ones (15, 6-D) by 0.52 to 0.33 AMI at
  k = 2. On the test portion the untuned lens scores 0.83 (accuracy 0.97) and the tuned one 0.69
  (0.94). Slice 1's validation over all 12 scene folds gave the untuned lens accuracy 0.83 at L4,
  in line with the selection folds: the four test scenes are easy for it at L4.
- With two families per class, which scenes are held out moves the score more than the settings
  do: the winners' AMI moves by −0.12 to +0.27 between the selection folds and the test portion.
  One test portion is unbiased but imprecise. Repeating the split, so that every family serves in
  a test portion once, would give the test score a spread (RECOMMENDATIONS.md).
- The search chose k = 2 at 14 layers and 3 at 7; 4 at L11, 6 at L0 and 8 at L21.

### What the two runs show

On these two captures, settings chosen per layer don't beat the default settings on held-out
data, which matches the planning measurement that settings move held-out AMI less than k does.
The search still gives each lens an honest held-out score, and its runners-up show how flat the
choice is.

## Caveats

- The tank lens has no scene families, so its held-out scores are from weaker folds.
- `carrier_id` and `n_context` hold one value each in the calibration capture; they appear as
  axes but carry no information.
- Two lenses, one model; these are first readings of the instrument, not results about meaning.

## Files

- `data/lake/session_1434a9be/lenses/tank-k5-n15/validation.json` (75 s)
- `data/lake/session_29a80932/lenses/calibration-q1-k2-n15/validation.json` (165 s)
- `data/lake/session_29a80932/lenses/aquarium-vs-vehicle-axis-p1/details/mass_mean.json`
- `data/lake/session_1434a9be/lenses/tank-k5-n15/details/v1.json` and `analysis/v1/`
- `data/lake/_analysts/tests/` (the analyst test runs)
- Each lens's `lens.json` holds its in-sample suggestions and self-check.
- `data/lake/session_1434a9be/lenses/tank-k5-n15-tuned/search.json` and
  `data/lake/session_29a80932/lenses/calibration-q1-k2-n15-tuned/search.json` (the tuning: the
  split, every candidate's selection scores, the winners and runners-up, the test scores)
