# QA Bug-Hunt Report — 2026-08-31

Tasking: implementation bugs behind FINDINGS_FINAL's numbers (Blocks A–D + 0, plus the
same-day addendum: 3 figure items ride, 2 roadmap-only). Nothing patched silently.
Run logs: session scratchpad `qa_logs/` (per-script stdout, exit codes all 0).

## Block A — full regeneration diff: GREEN (2 FIXED, 0 open FAILs)

Environment: clean process per script, PYTHONHASHSEED=0, project venv ("clean process"
interpretation of the spec; fresh venv would need a torch reinstall). Frozen captures as
inputs; no capture scripts run. Derived caches (r3_projcache_{tank,fr}.npz) deleted first.
Number inventory: 377 numeric tokens (F1:17 F2:30 F3:26 F4:26 F5:21 F6:18 F7:29 F8:23
F9:17 F10:47 + sections); every substantive value diffed.

| Item | Status | Evidence |
|---|---|---|
| Axes regeneration (10 npz) | PASS | bit-exact (allclose atol=0); calibrate deterministic (full-data means; heldout split seeded rng(1)) |
| 23 analysis-script runs | PASS | all exit 0; headline values exact-match doc (30-item spot table incl. gaps w/ seeded boot CIs, model classes, rotation cos, D6 loops+fitted null, F10 systematic/held-out/family-split, letter amp, q1b gaps, within-stream means, D7 readings) |
| Secondary-axis npz overwrite during regen | PASS | git diff empty after rerun — deterministic |
| Behavior worksheets vs committed categorized CSVs | PASS | 108/108 + 204/204 sets matched, max reading diff 0.000000 |
| Inline-only number sources | FIXED ×6 | materialized into `s10_materialized.py` §(i)–(vii): s8 cluster null + held-out, letter-site battery, D7 bare readings, F10 family-split, F7 pooled mid-k test (p=0.0138 ✓), D5 domain-clustered (t=12.0, p=7.22e-05 ✓) — all regenerate exactly |
| Refactor neutrality | PASS | post-refactor r1 rerun byte-identical to pre-refactor log |

## Block C — historical-bug-class audits

| Item | Status | Evidence |
|---|---|---|
| C1 signs | PASS | midref: zero own-class-sign violations, all 24 layers × both probes; secondary axes: held-out sign via LOFO 0.93–1.00. Raw-axis at long positions: 16 fr layers wrong-signed for the fictional class, tank none — exactly the documented accumulation drift (expected, enumerated, not a bug) |
| C2 boundaries | PASS | positions 1..40 contiguous (sampled 12 runs); per-carrier target ids verified (' tank' 16109; per-sub-carrier want/like/letter — first test draft wrongly assumed ' want' for S2, test fixed); k=1↔position 21 via contiguity + sort; ckpt windows end with carrier text (right-alignment anchor, 9/8 tokens) |
| C3 joins | PASS | 20-row samples both ckpt logs; calibration ⊆ pools (600/600, by design; leakage handled by scene-CV not disjointness); LOFO folds separate by construction. NOTE (metadata only): tank ckpt stores scenario_family "0" vs fr "fam09" — builder format inconsistency; no analysis joins on this field (all derive family from run names) |
| C4 label shuffle | PASS | D5 pair-swap: real +0.99 vs perm band [−0.20,+0.21], perm mean +0.003; scene-CV: real 0.907 → scene-permuted mean 0.530; F3 gap: real +1.66 vs perm mean −0.00 band [−1.42,+1.31]. All effects die; no leakage. F10 excluded per spec |
| C5 bootstrap internals | **FAIL→FIXED (correction 15)** | resampling units confirmed families (code + fixture B6). D4 references were fixed constants: with references resampled (6 arm-families rebuilt per draw), tank +[1.70,2.62]/+[0.77,1.48] and fr→real [0.27,0.50] still exclude 0; **fr→fictional widens [0.11,0.58]→[−0.12,+0.79], no longer excludes 0** — F3 demoted for that cell; figure caption updated |
| C6 ±6 pile | **FAIL→FIXED (correction 16)** | pile = display-only np.clip in figure code; statistics computed unclipped — but trimmed-vs-untrimmed comparison shows heavy-tail sensitivity: ck40 ba +0.862→+0.529 trimmed (206/4612 tokens), ck20 ab −0.641→−0.288. Suppression claim strengthens under trimming; F5 now quotes trimmed values; fr not tail-sensitive |
| C7a D5 clustered p | PASS (pre-resolved, now materialized) | domain-clustered t=12.0 p=7.22e-05; batches +1.18/+0.86/+0.94 |
| C7b F10 pool table | PASS | D6 pure cells span 12 fams (24 cells: 12 subspace-fam, 12 novel-fam); subspace built from 6 even fams. Family-split refutes novelty directionally: novel +1.6/+3.4 vs subspace +6.7/+6.0 (% sep), mixed ≈+27 |

## Block B — fixtures: 9/9 PASS (`tests/run_fixtures.py`, permanent regression suite)

B1 residual gap 1.000000 exact · B2 null contrast: held-out acc 0.517, effect 0.16 ·
B3 low-noise step → step (ΔBIC 2.5) · B4 γ=0.9 integrator → integrator (ΔBIC 6.0;
twoscale-nests-integrator acceptance documented) · B5 subspace recovery: m=0→0.00,
m=3→3.00 · B6 clustered SE 0.267 vs analytic 0.298; family-unit resampling confirmed.
QA refactors enabling imports (all logged, all behavior-preserving, r1 byte-verified):
r1 +residual_gap()/family_boot(); s7/s10 __main__ guards; s10 +fit_subspace().
Fixture 2 note: d′/LOFO fixture code mirrors the inline pipeline; equivalence proven
against real-data outputs (full extraction deferred past freeze).

## Addendum (rode today)

1. Letter-site D4 amplitude = 1.18 cal units (regenerated in s10; vs want 0.88 — NOT
   small, no demotion needed). fig_s9_asymmetry annotated (amplitude note + hatched
   n=4/dir letter bars).
2. Both carrier d′ figures: n=6 runs/class in title, per-bar pooled sd printed,
   denominator caveat caption (tall bars from tight sd; non-peak orderings not
   interpretable; d′ 11.7 = complete separation at n, unstable point estimate).
3. fig_s9_collapse in figure index: already done (commit db92f02), verified present.
Roadmap-only items 4–5: appended to FINDINGS_FINAL §5 + RECOMMENDATIONS (not run).

## Block D — fixes applied

Corrections 15 (C5) and 16 (C6) entered in FINDINGS_FINAL §3 with F3/F5 wording updated;
figure caption fig_r1_residual_gap updated; test-side bugs (C2 S2-target assumption, C3
segment parsing) fixed in tests, not data. Re-diff after fixes: green (r1 byte-identical;
s10 extras regenerate all materialized numbers exactly).

## Test-side bugs found while testing (for honesty's sake)
- qa_c2 first draft assumed ' want' target for S2 runs (S2 targets ' like') — test fixed.
- qa_c3 first draft parsed the direction from the wrong name segment for fr — test fixed.
Neither reflected a data problem.

## Block 0 — clean-room
(see cleanroom/ + DATA_LAYOUT.md; cleanroom-brief.md OPEN pending Andrew's file)

## Done-state
Blocks A–D GREEN. Two result-relevant corrections (15, 16) — both DEMOTIONS/refinements,
no silent patches. 6 inline-only sources materialized. 9/9 fixtures as permanent suite.
One OPEN item: cleanroom-brief.md awaited from Andrew.
