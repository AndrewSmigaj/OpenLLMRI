# Sanity Pass — All Non-Routing Findings (2026-08-28, requested by Andrew)

Method: every committed script re-run fresh; per-claim adversarial checks; independent-path
arithmetic spot check. Routing excluded (dropped from study).

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| 1 | D1b tank calibration (0.930 random / 0.905 scene-held-out @L4) | **VERIFIED** | Re-run exact; 24 scenes × 25 intact. Transparency note: calibration cells and D3 contexts draw from the same pools (no CV leakage within calibration; stated for the paper). |
| 2 | S1 axes (was 0.925 want / 0.904 letter @L14) | **CORRECTED → 0.910 / 0.877** | Real defect: scene-name drift between sub-arm batches (01_novelist vs 01_novelist_editor; 07 likewise) made 14 fiction "scenes" — two settings leaked across CV folds and two (11,12) were never held out. Fixed by canonicalization (scene id = first two name tokens); tank D1b control unchanged (0.905) as expected. Reconciliation doc corrected. |
| 3 | Tank D3/D4 trajectory numbers | **VERIFIED** | Hand arithmetic (explicit loop) matches vectorized to 1e-6 at steps 1/20/40 of fam03_ab; aggregates reproduce. |
| 4 | Norms flat, cosine alignment grows | **VERIFIED** | 390→382 / 404→392; cos −0.30→−0.61 / +0.50→+0.62. |
| 5 | Observed ahead of integrator null, both directions | **VERIFIED + robust** | Survives per-direction plateau amplitudes (aq 1.93, vh 2.06): ahead at all 8 checked points. |
| 6 | 8/24 runs jump-dominant | **VERIFIED + sharpened** | Reproduces; jump steps scattered t=23–32 (dispersed, not boundary-clustered); jump sizes 4.3–5.8× pre-shift step-noise. |
| 7 | Between-family 0.60 vs within-run 0.33 | **VERIFIED (after checker bug)** | Today's re-check first showed 1.20/0.67 — traced to a 2× factor in the *checker's* mangled inline expression, not the finding; ratio identical, scale-invariant dip values match to 4 decimals. Original numbers stand. Lesson logged: checkers get the same code hygiene as findings. |
| 8 | Occupancy: band unimodality, no third mode, no pile-up | **VERIFIED + family-level added** | Pooled dip p reproduce exactly (.557/.845); family-mean dips (n=12) also unimodal (.955/.469). Effective-n honesty stands. |
| 9 | Pre-lexical trajectories | **VERIFIED + new finding** | Pos-8 axis convention confirmed (calibration classes symmetric ±1.00). The D4 asymmetry is REAL, not a bug: sustained vehicle context moves the pre-lexical reading only +0.60 vs aquarium −2.13. Logged to geometry log; pre-lexical claims now carry this asymmetry caveat. |
| 10 | Instrument traps (cross-position; cross-token) | **VERIFIED** | Pos-8-on-pos-1: all four conditions ≈ −1.72. Window tokens: per-window means −1.70 ± 0.13 regardless of content. Both traps reproduce as methods results. |
| 11 | Engineering/audits | **VERIFIED** | Ckpt coverage 144/144 unique-ok; 53/53 campaign sessions carry prompt_format; both pool audits PASS on re-run; suicide chain 58/76 all ok (in flight; assertions on completion). |
| 12 | Prior-design figure | **VERIFIED** | Regenerates; prior-design labeling intact. |

**Net:** one substantive correction (#2, S-carrier scene-held-out numbers −1.5/−2.7 points);
one checker-side bug caught and disclosed (#7); one new real finding (#9 asymmetry);
everything else reproduces, several claims strengthened.
