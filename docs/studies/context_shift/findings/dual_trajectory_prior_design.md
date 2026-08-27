# Dual-Trajectory Figure — Prior-Design Runs, Two Instruments (2026-08-28)

**Figure:** `analysis/dual_trajectory_L23.png` · **Script:** `analysis/dual_trajectory_figure.py`
· **Aggregates:** `analysis/dual_trajectory_L23_points.csv`
**Data:** chain-log paper-protocol temporal runs, harmony format only (`polysemy_h` + `suicide`,
10 orderings × 2 directions each), L23, target token. **Prior-design (word-context) data** — the
scene-context D3 corpus replaces these for the paper.
**Framing:** exploratory. These are observations, not confirmations of predictions.

## What the figure shows

**Instrument agreement (the credibility result).** The UMAP-6D lens and the raw 2880-d axis tell
the same qualitative story on both probes. The lens was not hallucinating structure: everything
below is now visible in the un-reduced activation space.

**Tank polysemy:**
- Clean basin hold pre-shift in both directions, both instruments.
- Rapid crossing at the shift (~2–4 sentences).
- **Incomplete consolidation post-shift on the raw axis**: A→B settles around +0.5–0.6 (endpoint
  = +1), B→A around −1.0 with wider bands than pre-shift. The lens-level "less snug" finding now
  has a raw-space counterpart.
- **Raw-only detail the lens does not show:** pre-shift A→B sits around −1.5, i.e. *beyond* the
  −1 endpoint calibration mean. Accumulated same-sense context pushes the reading past the
  single-sentence endpoint. (Candidate explanations: context accumulation amplifies the sense
  reading; or word-context repetition (this corpus repeats "tank" every sentence). The
  scene-context rerun separates these.)

**Fiction/real:**
- The paper's collapse phenomenon replicates on the raw axis: real→fictional collapses from
  +1.2 to the fictional side within ~3–5 sentences; both directions then sit around −1 to −1.5
  (fictional side, again past the endpoint mean) for the whole window.
- At the shift, fictional→real produces only a small transient rise (≈ −1.3 → −0.7 around
  positions 20–24) that decays — no completed transition in either direction.

## Status notes
- Claim-ledger rows "shift is detectable — raw confirmation pending" and "post-shift volatility —
  raw validation pending" now have raw-axis support **on prior-design data**; the rerun corpus
  provides the paper-grade version.
- The beyond-endpoint readings (both probes) are a new observation the reduced-space lens
  masked — logged in the dataset geometry log; relevant to axis-normalization interpretation
  (endpoint ±1 is a single-sentence convention, not a bound).
