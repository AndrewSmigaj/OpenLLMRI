# Briefing Reconciliation — Repo vs Briefing v2 (2026-08-28)

Hand-off artifact for the other AI. Status per decisions-register item:
**ALIGNED** = no action · **REPO-SUPERSEDES** = Andrew decided in-session after v2, update the
briefing copy · **BRIEFING-ADOPTED** = repo corrected to the briefing · **RESOLVED** = was a
conflict, Andrew ruled.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Hysteresis replaces basin language | BRIEFING-ADOPTED | Repo scrub done (findings + terminology notes; README/CLAUDE.md rephrase Andrew-authorized, hence not "silent"). Repo correction: an earlier reassessment note "retired hysteresis language" is fixed — hysteresis (operational sense) is DEMONSTRATED by tank D3; integrator-consistency is the mechanism finding; stickiness = D6 loop area, pending. |
| 2 | Engagement/persona/Waluigi dropped; KV out | ALIGNED | README fixed; trace table rows DROPPED/flagged. |
| 3 | UMAP demoted to discovery | ALIGNED | All campaign numbers raw-axis; lens only in the labeled legacy figure. |
| 4 | Population doctrine | ALIGNED | Three-worlds tests ran on transition occupancy only. |
| 5 | Predictions before capture | RESOLVED | Andrew rejected mandatory prereg in-session; convergence = PROCEDURES committed pre-capture, outcome calls optional. |
| 6 | D6 mixture loop | ALIGNED+ | Design matches; round-2 adds an interleaved third ordering; stickiness measured beyond fitted-γ. |
| 7 | Router observable | ALIGNED | gate_entropy + top-1 captured on every run; analysis is W2. |
| 8 | Scenario-level stats | BRIEFING-ADOPTED | Scene-held-out CV was already scenario-level; distribution tests upgraded to family-level (earlier step-pooled dips had effective n≈12, flagged). |
| 9 | Anchor sites | ALIGNED | Implemented; per-carrier tables in design doc. |
| 10 | Data standards | ALIGNED | Harmony-only; prompt_format hash stamped in manifests (new backend field); legacy tagged (48 raw-text sessions inventoried). |
| 11 | Restriction protocol | ALIGNED | Pending D1a capture. |
| 12 | Probe Design v1 decisions | REPO-SUPERSEDES | Carrier strings: T1–T4 DROPPED by Andrew; tank carrier = Q1 meaning-question (see addendum). Scene-context rule, D1a/D1b split, unified geometry: aligned. |
| 13 | Final-step all-positions; within-stream population; T4; join audit | MIXED | Join audit: ALIGNED (in GUIDE + run). T4: superseded by Q1. Final-step all-positions: RESOLVED — backfill approved (interim captures were post-shift-window only). Within-stream dip population: instrument problem found empirically (token-identity offsets dominate cross-token projection); proposed fix = axis calibrated from D4 no-shift windows — please sanity-check. Carrier-curve = frame evolution: adopted as the distinct analysis it is. |
| 14 | Unresolved-zone battery | BRIEFING-ADOPTED | Battery 1 reference = endpoints + D4 (better than repo's endpoint-span draft). Band rules replace the repo's ad-hoc \|x\|<0.5 (rule (b) primary, sweep reported). Continuous-primary behavior endpoint: first-token logprob capture approved as backend addition. Tiers adopted verbatim. Repo addition kept: D6 mixtures as a second manifold reference. |
| 15 | Tier 2 items | ALIGNED | |

## Questions for the other AI
1. Any objection to the D4-window-calibrated axis as the within-stream instrument (register 13)?
2. Does your copy contain iterations beyond v2 to merge?
3. Given the integrator-null result, should the router-signature taxonomy add a sub-case for
   integration-driven drift with no routing anomaly (currently falls between "passage" and
   "learned")?

## Repo status snapshot for context
Tank D3/D4: 36 runs captured + analyzed; checkpoints 144/144; three-worlds (carrier site): no
shared third mode, no endpoint pile-up at matched times; run dynamics heterogeneous (8/24 runs
jump >50% of travel in one step). Suicide corpus (76 runs) capturing. S-carrier axes calibrated
(want .925 / letter .904 scene-held-out @L14). All scripts committed; every number reproduces.

## Addendum (2026-08-28, later): rule (b) empirical note for the other AI
Rule (b) on single-sentence calibration distributions produces an EMPTY band at p95 (classes
overlap near zero at 1-sentence context). Adopted refinement: endpoint distributions for band
definition = position-matched D4 no-shift plateau readings (consistent with battery 1's
"endpoint plus no-shift" reference). Bands then: L4 [−1.52, +1.21], L14 similar, L23
[−2.03, +0.46]. Please confirm or amend the rule hierarchy accordingly.
Router track: initial top-1/entropy "no anomaly" reading RETRACTED after sanity check —
top-1 is token-identity-dominated and scalar entropy is too coarse; the FULL soft
routing-weight vector separates the senses perfectly at the same token (family-held-out 1.000
@L4). Battery 1(d) reopened on the routing-weight axis. Flagged anomaly: D3 late entropy LOWER
than D4 (paired p=.02), opposite the off-manifold prediction.
