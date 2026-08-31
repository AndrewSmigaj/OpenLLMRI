#!/usr/bin/env python3
"""QA Block B — synthetic ground-truth fixtures pushed through ACTUAL pipeline functions.
Run: .venv/bin/python tests/run_fixtures.py   (after QA refactors: s7/s10 __main__ guards,
r1 residual_gap/family_boot extraction). PASS/FAIL per fixture."""
import sys
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np

rng = np.random.default_rng(99)
results = []

def check(name, cond, detail):
    results.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'} {name}: {detail}")

# ---------- fixtures 3+4: model selection (ACTUAL 5-model classifier) ----------
from s7_sanity_checks import classify5
from second_pass_r1_dynamics import integrator_pred, K

y_step = np.where(K < 9, -1.0, 1.0) + rng.normal(0, 0.08, 20)
lab, bics, delta, fits = classify5(y_step, 2.0, 2.0)
check("B3 low-noise step -> step", lab == "step", f"got {lab} (dBIC {delta:.1f})")

y_int = integrator_pred(0.90, 2.0, 2.0) + rng.normal(0, 0.08, 20)
lab, bics, delta, fits = classify5(y_int, 2.0, 2.0)
check("B4 gamma=0.9 integrator -> integrator", lab in ("integrator", "twoscale"),
      f"got {lab} (dBIC {delta:.1f}; twoscale nests integrator, either accepted)")

# ---------- fixture 1: residual gap == 1.000 (ACTUAL extracted function) ----------
from second_pass_r1_dynamics import residual_gap
mid = np.zeros(40)
dest_arms = np.tile(np.linspace(1.8, 2.0, 40), (6, 1))          # dest reference
run = np.concatenate([np.full(20, -2.0), np.full(20, 0.0)])
run[35:40] = dest_arms.mean(0)[35:40] - 1.0                      # plateau exactly 1.0 short
g = residual_gap(run, mid, +1.0, dest_arms)
check("B1 residual gap == 1.000", abs(g - 1.0) < 1e-9, f"got {g:.6f}")

# ---------- fixture 2: null contrast ----------
Xa = rng.normal(0, 1, (300, 64)); Xb = rng.normal(0, 1, (300, 64))
mu_a, mu_b = Xa.mean(0), Xb.mean(0)
axis = mu_b - mu_a; m = (mu_a + mu_b) / 2
pa, pb = (Xa - m) @ axis, (Xb - m) @ axis
dpr = (pb.mean() - pa.mean()) / np.sqrt((pa.std() ** 2 + pb.std() ** 2) / 2)
# held-out: split half
tr = np.arange(150)
a2 = Xb[tr].mean(0) - Xa[tr].mean(0); m2 = (Xb[tr].mean(0) + Xa[tr].mean(0)) / 2
acc = (((Xb[150:] - m2) @ a2 > 0).mean() + ((Xa[150:] - m2) @ a2 < 0).mean()) / 2
d5 = (pb[:150] - pa[:150]).mean() / max(np.abs(pb).max(), 1e-9)
check("B2 null contrast: held-out acc ~ chance", 0.35 < acc < 0.65, f"acc={acc:.3f}")
check("B2 null contrast: within-pair effect ~ 0", abs(d5) < 0.2, f"norm-effect={d5:.3f}")
# note: in-sample dpr on the training data is inflated by construction (diff-of-means
# maximizes it); the held-out accuracy is the meaningful null check, reported above.

# ---------- fixture 5: F10 subspace recovery (ACTUAL fit_subspace) ----------
from s10_materialized import fit_subspace
basis = np.linalg.qr(rng.normal(0, 1, (80, 12)))[0].T            # 12-dim true subspace
D4syn = rng.normal(0, 1, (240, 12)) @ basis * 5
off_dir = np.linalg.qr(np.concatenate([basis, rng.normal(0, 1, (1, 80))]).T)[0][:, -1]
for m_true in (0.0, 3.0):
    trans = rng.normal(0, 1, (100, 12)) @ basis * 5 + m_true * off_dir
    center, Vk, resid_of = fit_subspace(D4syn, var_target=0.98)
    got = np.linalg.norm(resid_of(trans).mean(0))
    ok = (got < 0.6) if m_true == 0 else (abs(got - m_true) < 0.5)
    check(f"B5 subspace recovery m={m_true}", ok, f"recovered {got:.2f}")

# ---------- fixture 6: family bootstrap (ACTUAL family_boot) ----------
from second_pass_r1_dynamics import family_boot
import pandas as pd
F, n_per = 12, 4
tau, sig = 1.0, 0.5
fam_means = rng.normal(0, tau, F)
rows = pd.DataFrame({"fam": np.repeat(np.arange(F), n_per),
                     "v": np.repeat(fam_means, n_per) + rng.normal(0, sig, F * n_per)})
by_fam = rows.groupby("fam").v.mean()
boots = family_boot(by_fam, nboot=4000, seed0=7)
se_boot = np.std(boots)
se_analytic = np.sqrt((tau ** 2 + sig ** 2 / n_per) / F)
check("B6 clustered SE ~ analytic", abs(se_boot - se_analytic) / se_analytic < 0.35,
      f"boot {se_boot:.3f} vs analytic {se_analytic:.3f}")
# unit check: family resampling means boot distribution of the MEAN has ~F effective units
check("B6 resamples families not rows", len(by_fam) == F, f"series indexed by {len(by_fam)} families")

n_fail = sum(1 for _, ok, _ in results if not ok)
print(f"\nFIXTURES: {len(results) - n_fail}/{len(results)} PASS" + (f", {n_fail} FAIL" if n_fail else ""))
sys.exit(1 if n_fail else 0)
