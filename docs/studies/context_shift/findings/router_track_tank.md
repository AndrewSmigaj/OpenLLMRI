# Router Track — Tank Transitions (2026-08-28, exploratory)

**Battery 1(d).** Band = rule (b) with the position-matched refinement (endpoint distributions
from D4 plateau readings, steps 11–40; single-sentence calibration yields an EMPTY p95 band at
every layer — recorded, and the refinement is flagged for the other AI). Script:
`analysis/router_track_tank.py`. Layers 4/14/23, carrier token.

## Result: NO routing anomaly of any predicted kind at the carrier site

- **Entropy is flat everywhere.** Phase means differ by ≤0.04 against layer means of ~3.07–3.17,
  with no D3-vs-D4 elevation at matched positions and no in-band elevation (L4 in-band is
  actually 0.03 LOWER). No spikes, no post-shift bump.
- **Top-1 routing at this token is token-identity-dominated:** one expert carries ~95–99% of
  steps per layer (L4: expert 14; L14: expert 6; L23: expert 24) for band and endpoints alike.
  Band mass on endpoint experts ≈ 100%; zero meaningful novel-expert usage; switch rates in
  band are at or below out-of-band and D4 baselines (no flicker).

## Reading (instruments sign their own claims)

- **Off-manifold signature: ABSENT** at this site — no entropy elevation, no flicker, no
  fallback experts. This is affirmative evidence against the off-manifold world for
  transition-state occupancy at the carrier token, as far as the router can see.
- **Learned-third-pattern signature: ABSENT** — but note the instrument caveat: top-1 at a
  fixed carrier token is largely determined by token identity, so top-1/entropy may simply be
  insensitive to contextual state here. The sharper observable is the full 32-dim soft
  routing-weight vector (captured): a "router axis" (difference of D4-endpoint class means in
  routing-weight space) is the planned follow-up before concluding the router carries no
  state information.
- Coheres with the integrator picture: smooth evidence-integration drift predicts exactly
  "no routing anomaly" — supporting the reconciliation question to the other AI about adding a
  fourth signature (integration-drift, no anomaly) to the taxonomy.

## Follow-ups
1. Router-axis (soft weights) version of this analysis; same battery, D4-calibrated.
2. Same track on the suicide corpus when its chain completes.
