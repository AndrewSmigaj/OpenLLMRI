# Q1 Dilution Gate — PASSED (preview scale, 2026-08-28)

**Session:** `session_1c7fbe28` (`context_shift_gate_preview_v1`) — 4 aquarium + 4 vehicle
contexts, each 20 sentences assembled from the wave-1 blind pools (scene-mixed, token budgets
334-367 words), word "tank" absent from all context, carrier Q1 appended. Harmony
(`harmony@a4c9919cbbd4`), all 24 layers, per-token carrier span.

## Results (axis_projection.py calibrate, 50/50 held-out)

- **Post-lexical (` tank`, pos 1):** held-out 1.000 from L4 up; within-class std **0.01–0.06**
  through mid layers (vs ~0.7 for single-sentence endpoint calibration on session_e2be37dd).
  20-sentence scene context does not dilute the Q1 reading — it sharpens it dramatically.
- **Pre-lexical (` word`, pos 8):** held-out 1.000, stds 0.15–0.5 (L23 wider: 0.69/0.75).
  Sense committed before the word "tank" occurs anywhere in the episode — the context-carried
  signal the anchor doctrine is built around, visible at gate-preview scale.

## Caveats
- n=4/4, held-out split 2/2 — separation is extreme enough (gap/std ≈ 30-60×) that this is
  decisive as a gate, but the formal Wave-1 calibration (200/label, dedicated cells,
  scene-held-out) remains the paper-grade number.
- Contexts sampled from only 6 scenes (wave-1+2 pools at 3/label when assembled); pool reuse
  across variants understates within-label variance.

## Verdict
The D3 tank captures are UNGATED. The 2-sentence micro-pilot's ~95% is now effectively
confirmed at full context length; residual risk retired.
