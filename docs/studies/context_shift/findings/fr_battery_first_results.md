# Fiction/Real Arm — First Designed-Corpus Results (2026-08-28, exploratory)

**Data:** 76 runs (S1: 12 families × 2 directions × 2 sub-arms; S2/S3: 4 families × 2
directions; 12 no-shift arms), 40 steps, scene-context, per-carrier sites. All assertions ok.
**Instrument:** per-carrier same-site axes at L14 (calibration peak; corrected scene-held-out
0.910). Script: `fr_battery.py`; figure `figures/fr_traj_null_L14.png`. Convention fic −, real +.

## Findings

1. **THE headline (and the safety-relevant asymmetry, inverted from the legacy corpus):
   the REAL reading is durable; the FICTIONAL reading erodes.** Sustained fiction-craft
   context does not hold a fictional reading at the want site — no-shift fictional arms drift
   from −1 to ≈+0.1 (neutral) by mid-run, and fr transitions erode toward 0 during their own
   fiction block. Sustained real context deepens and holds (+1.9). Consequently real→fictional
   transitions END still meaningfully real-side (+0.5 at +20 counter-sentences), and
   fictional→real transitions leap quickly to +1.4. In the legacy word-context corpus both
   orderings collapsed TOWARD fictional; in scene-context (request not embedded in the
   context), the direction of durability inverts. Interpretation flags: (a) candidate
   axis-transfer artifact for the fictional class at long positions — though the real class
   deepens under the same axis at the same positions (internal control); D4-calibrated-axis
   cross-check is the queued test; (b) craft-DISCUSSION context may genuinely not sustain a
   "fictional request" frame the way embedded fictional requests did. Do not carry into any
   claim until (a) is run.
2. **Both directions run ahead of the integrator null** at every checked point (8/8) — same
   qualitative dynamics family as tank.
3. **Occupancy unimodal in both directions** (dip p ≈ 0.99–1.00; effective n = 12–24
   families): no shared third mode at the carrier site — consistent with tank.
4. **Jump-heavy paths:** 19/48 S1 runs are jump-dominant (vs tank's 8/24).
5. **Cross-carrier reliability (same-site axes): r = 0.95 (S1↔S2), 0.80–0.93 (S1↔S3)** —
   trajectory shapes replicate across carriers including S3's speech-act variation.
6. **Sub-arms nearly coincide** (theme-only vs artifact-mentioned): artifact mention slightly
   strengthens the fictional reading early in fr runs; post-shift behavior indistinguishable
   at current n.

## Process note (trap doctrine, enforced structurally)
The battery's first draft projected S2/S3 runs through the S1 axis — the documented
cross-token trap, self-committed — yielding a spurious S1↔S3 r = −0.6. Caught in review;
the script now keys every projection to its carrier's own axis, and the corrected r is +0.8
to +0.93. Rule promoted: axis selection is derived from the run's carrier, never shared.

## Queued
D4-axis cross-check for finding 1 · occupancy time-bands + rule-(b) band (needs fr D4-based
band) · suicide checkpoint pass · behavior cells (safeguard-vs-reading, continuous-primary).


---
## DEPTH REVISION (2026-08-28, all-layers heatmap `figures/fr_heatmap_layer_position.png`)

Finding 1's "erosion" is a depth AVERAGE of a sharper structure — a **depth disagreement**:

- In no-shift fictional arms, **layers ~4–11 hold the fictional reading across all 40
  sentences**, while **layers ~17–23 read real-side almost from the start**. L14 (the scalar
  summary layer) sits near the crossover, producing the apparent neutral drift.
- No-shift real arms are real-side at every depth and position — durability is stack-wide.
- Transitions: deep layers flip to real immediately after a fictional→real shift; layers 5–9
  retain fictional readings past the boundary. In real→fictional, no depth ever reads
  strongly fictional post-shift.

This weakens the axis-transfer-artifact alternative (a transfer artifact would not produce a
coherent depth-organized split under independently calibrated per-layer axes) and restates the
safety-relevant asymmetry precisely: **under sustained fiction-craft framing, the layers
nearest the output carry a real-request reading; the fictional frame lives mid-stack.**
Exploratory; the D4-axis cross-check remains queued, now per-layer.

---
## REVISION v2 (2026-08-28, midpoint-referenced sanity check — prompted by Andrew's label caution)

Two retractions and one new named phenomenon. Figure: `figures/fr_heatmap_midref.png`
(each layer×position cell re-centered on the position-matched D4 midpoint = class signal only).

1. **"Real durable / fictional erodes" — RETRACTED.** At L14 the D4 plateaus (fic +0.12,
   real +1.89) are exactly symmetric about their midpoint (+1.00): each class sits 0.88 on its
   own side. The apparent asymmetry was entirely common-mode. Both frames are equally durable
   relative to the accumulated-context reference, at every layer (midref heatmap: fictional
   blue and real orange across the full stack).
2. **"Depth disagreement" — RETRACTED** (supersedes the earlier depth revision). Deep-layer
   orange in the raw heatmap was common-mode drift; class separation persists at all depths
   (gap 2.3 mid → 1.3 deep — reduced, not inverted, not absent).
3. **NEW NAMED PHENOMENON — accumulation drift:** a layer-dependent, class-NONSPECIFIC
   component along the contrast axis that grows with context (fr: ≈+1.0 at L14, ≈+1.2–2.8-side
   at deep layers in BOTH arms; tank: ≈0 at L4, ≈−0.7 at L23). Its content is unknown —
   per the label doctrine it may be any long-context correlate of the calibration classes; it
   is NOT class evidence. It contaminates any absolute-position claim (crossing-zero times,
   single-arm colors, "erosion"); all such claims must be midpoint-referenced. Tank's
   L23 "not crossed zero by step 40" is a casualty: re-referenced to the L23 midpoint (−0.74),
   the aq→vh L23 trajectory crosses earlier than reported.

**Label doctrine (standing, from Andrew):** axis readings are positions along a DESIGNED
CONTRAST, never meaning attributions. Red = real-class side (which may mean "not-fiction" or
any correlate); white = no class signal; distinguishing "real" from "not-fiction" requires
additional contrasts (e.g., third-class calibrations) — future studies.

**Survives unchanged:** ahead-of-integrator-null (to be re-checked midpoint-referenced, but
both comparisons embed the same common-mode); unimodal occupancy (scale/shift-invariant);
jump statistics; cross-carrier reliability; sub-arm near-coincidence.
