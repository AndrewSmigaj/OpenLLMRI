#!/usr/bin/env python3
"""Adversarial reassessment checks (2026-08-28) — run against tank D3/D4 at L4.

CHECK 1: is the ±2 'deepening' a positional norm artifact? -> ||x|| flat (~380-400)
         across positions; cos(x-mid, axis) grows (0.30->0.62). NOT an artifact.
CHECK 2: per-run jumpiness -> 8/24 runs have one step covering >50% of total
         post-shift travel. Run-level dynamics are heterogeneous (drifts AND jumps).
CHECK 3: uniform evidence-averaging null reading(t) = 2*(k-20)/(20+k) ->
         observed is AHEAD of the null in both directions at every t.
         Recency-weighted integration, not sticky history.
CHECK 4: between-family sd (0.60) ~ 2x within-run 5-step sd (0.33) at matched t:
         families occupy genuinely different locations; band sigma mixes dispersion.

(Body identical to the inline run recorded in the session; kept as the
reproducibility artifact for the revision notes in the findings docs.)
"""
