# Surface-feature confound analysis — v1 pools (12 September 2026)

Repository record for §3.1's third test and the Appendix B "Surface-feature confound"
paragraph. Added in the v1.1 cleanup cycle to answer, in print, the "some other variance"
worry about the reading, on the existing v1 pools (no recapture).

## Pre-decided choices (before reading the classifier output)
- **Deterministic surface features only** — length, punctuation/dialogue/digit rates,
  opener class, type-token ratio, within-scene 4-gram overlap (`feature_battery.py`). No
  second-AI rater and no judgment tags (tense, register, valence): those would be a second
  confounded model reading, not a clean surface baseline.
- **Classifier = a "ceiling"**: a standardized logistic regression (class-weight balanced) —
  a stronger linear rule than the reading's own difference-of-means — so the number is an
  upper bound on what surface features explain, not an understatement.
- **Validation = leave-one-scene-pair-out**, the same 12 scene folds as the reading's
  calibration (`scene_heldout_calibration.py`); the `_scene()` normalization collapses the
  fiction pool's 14 batch-file scene keys to 12 scenes. Report balanced accuracy + AUC
  (the fiction pool is 2× the real pool).
- **Interpretation fixed in advance, framing-proof to the result:** whatever the ceiling, it
  is disclosed. A high ceiling means the classes are surface-separable, so the reading does
  nothing surface features cannot — consistent with §3.1's scoped claim that the reading
  "tracks framing cues, not an abstract representation of the frame." A low ceiling means the
  reading separates the classes better than surface features do.

## Results
- **Tank (aquarium vs vehicle):** surface classifier at chance — balanced accuracy 0.467,
  AUC 0.470 — against the reading's held-out 0.905. The tank reading is not recoverable from
  surface form.
- **Fiction/real:** surface classifier balanced accuracy 0.737, AUC 0.825, against the
  reading's 0.910. Surface features carry real signal, as expected when the framing is itself
  cued by surface form (the classes differ most on length and type-token ratio), yet the
  reading separates the classes better than a strong surface classifier does.

## Artifacts
- `analysis/feature_battery.py` → `analysis/confound_features.csv` (1,500 sentences).
- `analysis/confound_features_analysis.py` → `analysis/figures/fig_confound_features.png`
  (paper Fig., wired into §3.1) and `findings/feature_table.md` (per-feature Cliff's delta).
- Paper: §3.1 third test; Appendix B "Surface-feature confound"; caption `fig_confound_features`.

The proper causal follow-up — which framing cue (tense, person, production noun) drives the
minimal-pair effect — is the orthogonal-cue decomposition deferred in `../EXPERIMENTS.md`.
