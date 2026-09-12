# Surface-feature confound baseline (v1 pools)

Deterministic surface features only (feature_battery.py); no judgment tags.
Cliff's delta is 2·AUC − 1 between the two classes (0 = full overlap, ±1 = full separation).
The confound-ceiling classifier is a standardized logistic regression (class-weight
balanced), leave-one-scene-pair-out (12 folds) — a stronger linear rule than the reading's
own difference-of-means, so it is an upper bound on what surface features explain.
Reading accuracies are the paper's Box 1 held-out values.

## tank (aquarium vs vehicle)

- Confound-ceiling balanced accuracy: **0.467** (AUC 0.470; mean per-fold accuracy 0.467; n=600, aquarium 300 / vehicle 300).
- The reading's held-out accuracy (Box 1): **0.905**.

| feature | Cliff's delta |
|---|---|
| comma rate | +0.07 |
| sentence count | -0.07 |
| token length | -0.06 |
| char length | -0.05 |
| mean word length | +0.05 |
| type-token ratio | -0.02 |
| has dash | +0.01 |
| digit rate | +0.01 |
| semicolon rate | +0.00 |
| has dialogue quote | +0.00 |
| within-scene 4-gram overlap | +0.00 |

## fiction/real

- Confound-ceiling balanced accuracy: **0.737** (AUC 0.825; mean per-fold accuracy 0.737; n=900, fictional 600 / real 300).
- The reading's held-out accuracy (Box 1): **0.910**.

| feature | Cliff's delta |
|---|---|
| mean word length | -0.50 |
| char length | -0.47 |
| type-token ratio | +0.19 |
| token length | -0.19 |
| semicolon rate | +0.08 |
| digit rate | -0.04 |
| has dialogue quote | -0.04 |
| comma rate | -0.02 |
| has dash | -0.01 |
| sentence count | +0.01 |
| within-scene 4-gram overlap | -0.00 |
