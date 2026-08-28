> **OUT OF SCOPE (Andrew, 2026-08-28): expert routing is dropped from this study entirely —
> deferred to later work. This file is retained for provenance only (it contains a retraction
> that belongs in the honest record). No routing analyses feed this study's claims; the
> off-manifold question is adjudicated by the geometry battery (a,b,c) and behavior.**

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

---
## SANITY-CHECK REVISION (2026-08-28, prompted by Andrew)

The headline above is RETRACTED as an instrument-granularity artifact; the checks:

1. Instrument validity confirmed: stored gate_entropy recomputes exactly from routing_weights
   (Δ≤0.0015); routing is genuinely diffuse (mean top-1 weight 0.13, entropy near ln 32); the
   observable has real dynamic range across token identities (2.85–3.34). Not a data problem.
2. **Top-1 and scalar entropy are the WRONG granularity at a fixed token**: top-1 is
   token-identity-dominated (each semantic position has its own dominant expert). Meanwhile the
   **full 32-dim soft routing-weight vector separates aquarium vs vehicle PERFECTLY at the same
   token** (D4-plateau, leave-one-family-out: 1.000 @L4, 0.989 @L23). The router DOES track the
   latent state — in its soft weights.
3. Consequently "no routing anomaly / off-manifold signature absent" is NOT established. The
   battery-1(d) adjudication is REOPENED and must run on the routing-weight axis: does the
   unresolved band show a distinctive stable soft pattern (learned), an endpoint blend
   (passage/integration), or anomalous low-density weights (off-manifold)?
4. Flagged anomaly (not folded into conclusions): D3 late-phase entropy is LOWER than D4 at
   matched positions, family-paired t=−3.38, p=0.020, Δ=−0.039 — direction opposite to the
   off-manifold prediction; interpretation deferred.
5. Frame note (Andrew): latent space remains the primary study object; the router is the
   designed secondary observable (Plan v2 item 9 / briefing 1(d)). The soft-weight result is
   itself frame-relevant: even the router's 32-dim summary reflects the latent state.
