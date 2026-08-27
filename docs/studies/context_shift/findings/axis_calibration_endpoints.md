# N1 Axis Calibration — Endpoint Validation (2026-08-27)

**Script:** `docs/studies/context_shift/analysis/axis_projection.py` (committed)
**Scope guard:** endpoint separability only — an ESTABLISHED claim-ledger row. No transition
data touched (S1 gate: transition analyses wait for Andrew's predictions file).

## Method
Difference-of-class-means axis on raw 2880-d residuals, per layer, token_position=1.
Endpoints renormalized: mean(A)→−1, mean(B)→+1. Separability = best-threshold accuracy on a
50/50 stratified held-out split with the axis refit on train only. Harmony sessions only
(v2.1 consistency rule).

## Results

**Fiction/real** (`session_9358c2a1`, fictional vs real, n=99+99):
held-out accuracy 0.81 (L0) → 0.93 (L2) → **0.94–0.99 plateau L3–L23**; within-class spread
~0.4–0.5 through the mid layers.

**Tank** (`session_e2be37dd`, aquarium vs vehicle restricted, n=100+100):
held-out 0.63 (L0) → 0.84 (L2) → **0.91–0.94 plateau L4–L23**; aquarium-side spread
consistently wider than vehicle (sdA ~0.7 vs sdB ~0.5).

## Observations (logged, not interpreted)
1. **Raw-space separability confirmed for both probe families** — the claim-ledger row
   "shift is detectable / raw confirmation pending" now has its endpoint half signed by the
   raw instrument.
2. **Instrument comparison:** the lens-level finding was "polysemy very high purity;
   fiction/real lower." The raw axis orders them the other way (fiction/real 0.97–0.99 vs tank
   0.91–0.94). Not directly comparable (binary restriction vs 5-way clustering; different
   statistics), but this is exactly the kind of instrument disagreement the program treats as
   a result. Candidate input to the inversion hypothesis — goes to Andrew, not into any claim.
3. Tank's asymmetric spread (aquarium wider) is a dataset-geometry note for the geometry log.
4. Axis norms grow monotonically with depth in both probes (residual-stream norm growth);
   the ±1 normalization absorbs this per layer.

## Artifacts
- `analysis/axes/axes_session_9358c2a1_fictional_vs_real_pos1.{npz,json}`
- `analysis/axes/axes_session_e2be37dd_aquarium_vs_vehicle_pos1.{npz,json}`
