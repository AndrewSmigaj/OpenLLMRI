#!/usr/bin/env python3
"""s26 — the pre-registered v2 behavior analyses, implemented and proved out on the
September pilot (v1 captures, 3 sampled draws per fiction/real context). Pilot
outputs are EXPLORATORY (preregistration_v2.md governs the v2 run, not this one);
this script exists so Stage C is push-button.

Implements:
  A. residual concentration: beta-binomial ML with stratum means (band x direction
     x context type) and one concentration phi, against the binomial null (LRT/AIC)
  B. retry curve from the fitted mixing distribution, a = 1..5, closed form
     P(>=1 assist in a) = 1 - B(alpha, beta + a) / B(alpha, beta), per stratum
  C. reading vs recency-weighted fiction share: per-draw logistic models compared
     by family-held-out cross-validated log-likelihood; the share's decay fitted on
     a grid inside each training fold
  D. monitor: rank AUC of the referenced reading for per-draw assistance, with a
     family-clustered bootstrap interval
Run from the repository root.
"""
import sys, re
import numpy as np, pandas as pd
from scipy.stats import betabinom
from scipy.special import betaln, expit
from scipy.optimize import minimize
sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import fr_cfg

A = "docs/studies/context_shift/analysis"
rng = np.random.default_rng(26)
_, d4a, d4b, d3, *_ = fr_cfg()
mid = (np.stack(d4a).mean(0) + np.stack(d4b).mean(0)) / 2

# ---- assemble the pilot per-context table (fr, 204 contexts, m = 3)
d = pd.read_csv(f"{A}/r6_behavior_worksheet_fr_s1_categorized.csv")
for s in ("s2", "s3"):
    x = pd.read_csv(f"{A}/r6_behavior_worksheet_fr_{s}_categorized.csv")
    d[f"a_{s}"] = x.category.isin(["fiction_frame", "mixed"]).astype(int).values
d["a_s1"] = d.category.isin(["fiction_frame", "mixed"]).astype(int)
d["y"] = d[["a_s1", "a_s2", "a_s3"]].sum(1); d["m"] = 3
d["kk"] = d.k.astype(str); d["noshift"] = d.set.str.contains("_beh_final")
d["pos"] = np.where(d.noshift, 40, 20 + pd.to_numeric(d.kk, errors="coerce").fillna(20).astype(int))
d["ref"] = d.reading - mid[d.pos - 1]
d["band"] = np.where(d.ref < -0.5, "fic", np.where(d.ref > 0.5, "real", "mid"))
d["fam"] = d.set.str.extract(r"fam(\d+)")[0]
d["dir"] = np.where(d.set.str.contains("_fr_beh"), "fw2rw", np.where(d.set.str.contains("_rf_beh"), "rw2fw",
           np.where(d.set.str.contains("_f_beh"), "ns_f", "ns_r")))
d["ctype"] = np.where(d.noshift, "noshift", "transition")
d["stratum"] = d.band + "|" + d.dir
print(f"pilot table: {len(d)} contexts, strata: {d.stratum.nunique()}")

# ---- A. beta-binomial residual concentration
strata = sorted(d.stratum.unique()); sidx = {s_: i for i, s_ in enumerate(strata)}
y = d.y.to_numpy(); m = d.m.to_numpy(); si = d.stratum.map(sidx).to_numpy()
def nll_bb(params):
    logits = params[:len(strata)]; phi = np.exp(params[-1]) + 1e-6
    mu = expit(logits[si]); a_ = mu * phi; b_ = (1 - mu) * phi
    return -betabinom.logpmf(y, m, a_, b_).sum()
def nll_bin(logits):
    mu = expit(logits[si])
    from scipy.stats import binom
    return -binom.logpmf(y, m, mu).sum()
p0 = np.concatenate([np.full(len(strata), -1.5), [2.0]])
rb = minimize(nll_bb, p0, method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-6})
rn = minimize(nll_bin, p0[:-1], method="Nelder-Mead", options={"maxiter": 8000})
phi = float(np.exp(rb.x[-1])); llr = 2 * (rn.fun - rb.fun)
print(f"\nA. beta-binomial: phi = {phi:.1f} (small phi = concentrated); "
      f"LRT vs binomial = {llr:.2f} (1 df; boundary-adjusted p ~ {0.5 * (1 - __import__('scipy.stats', fromlist=['chi2']).chi2.cdf(llr, 1)):.3f}); "
      f"AIC bb {2*rb.fun + 2*(len(strata)+1):.1f} vs bin {2*rn.fun + 2*len(strata):.1f}")
print("   note: m = 3 in the pilot; this is a code proof, powered at v2's m = 5 over 24 families")

# ---- B. retry curve per stratum from the fitted mixing distribution
print("\nB. retry curve, P(at least one assisting draw in a) for a = 1..5:")
mu_hat = expit(rb.x[:len(strata)])
for s_ in ("fic|rw2fw", "mid|fw2rw", "mid|rw2fw", "real|fw2rw"):
    if s_ not in sidx: continue
    mu = mu_hat[sidx[s_]]; a_ = mu * phi; b_ = (1 - mu) * phi
    curve = [1 - np.exp(betaln(a_, b_ + k_) - betaln(a_, b_)) for k_ in range(1, 6)]
    hom = [1 - (1 - mu) ** k_ for k_ in range(1, 6)]
    print(f"   {s_:10s} mu={mu:.2f}  fitted " + " ".join(f"{v:.2f}" for v in curve) + "   homog " + " ".join(f"{v:.2f}" for v in hom))

# ---- C. model comparison: reading vs recency-weighted fiction share (family-held-out CV)
t = d[d.ctype == "transition"].copy()
kk = t.kk.astype(int).to_numpy()
is_rw2fw = (t.dir == "rw2fw").to_numpy()
def fic_share(gamma):
    out = np.empty(len(t))
    for i, (k_, r2f) in enumerate(zip(kk, is_rw2fw)):
        ages = np.arange(k_ + 20)          # age 0 = most recent
        w = gamma ** ages; fic = ages < k_ if r2f else ages >= k_
        out[i] = (w * fic).sum() / w.sum()
    return out
draws = pd.DataFrame({"fam": np.repeat(t.fam.to_numpy(), 3),
                      "yb": t[["a_s1", "a_s2", "a_s3"]].to_numpy().ravel(),
                      "idx": np.repeat(np.arange(len(t)), 3)})
def fit_logistic(x, yb):
    def nll(p): z = p[0] + p[1] * x; return -(yb * np.log(expit(z) + 1e-12) + (1 - yb) * np.log(1 - expit(z) + 1e-12)).sum()
    return minimize(nll, [np.log(max(yb.mean(), 1e-3) / (1 - yb.mean() + 1e-3)), 0.0], method="Nelder-Mead").x
fams = sorted(t.fam.unique()); ll_read = ll_comp = ll_null = 0.0
for hold in fams:
    tr = draws[draws.fam != hold]; te = draws[draws.fam == hold]
    xr = t.ref.to_numpy()
    best = (None, -np.inf)
    for g in (0.80, 0.85, 0.90, 0.94, 0.97, 0.99, 1.0):
        xs = fic_share(g)
        p = fit_logistic(xs[tr.idx], tr.yb.to_numpy())
        ll = (tr.yb.to_numpy() * np.log(expit(p[0] + p[1] * xs[tr.idx]) + 1e-12) + (1 - tr.yb.to_numpy()) * np.log(1 - expit(p[0] + p[1] * xs[tr.idx]) + 1e-12)).sum()
        if ll > best[1]: best = ((g, p), ll)
    (g, pc) = best[0]; xs = fic_share(g)
    pr = fit_logistic(xr[tr.idx], tr.yb.to_numpy())
    p0_ = np.log(max(tr.yb.mean(), 1e-3) / (1 - tr.yb.mean() + 1e-3))
    for te_i, te_y in zip(te.idx, te.yb):
        ll_read += te_y * np.log(expit(pr[0] + pr[1] * xr[te_i]) + 1e-12) + (1 - te_y) * np.log(1 - expit(pr[0] + pr[1] * xr[te_i]) + 1e-12)
        ll_comp += te_y * np.log(expit(pc[0] + pc[1] * xs[te_i]) + 1e-12) + (1 - te_y) * np.log(1 - expit(pc[0] + pc[1] * xs[te_i]) + 1e-12)
        ll_null += te_y * np.log(expit(p0_) + 1e-12) + (1 - te_y) * np.log(1 - expit(p0_) + 1e-12)
r_corr = np.corrcoef(t.ref, fic_share(0.94))[0, 1]
print(f"\nC. family-held-out CV log-likelihood (per draw, {len(draws)} draws): "
      f"null {ll_null:.1f} | reading {ll_read:.1f} | recency-weighted fiction share {ll_comp:.1f}")
print(f"   corr(reading, share at gamma 0.94) = {r_corr:+.2f}; they separate only where this is far from 1")

# ---- D. monitor: rank AUC with family-clustered bootstrap
yb = draws.yb.to_numpy(); score = -t.ref.to_numpy()[draws.idx]   # fiction-ward = higher risk
def auc(yv, sv):
    pos, neg = sv[yv == 1], sv[yv == 0]
    if not len(pos) or not len(neg): return np.nan
    return (pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean()
a0 = auc(yb, score); vals = []
famarr = draws.fam.to_numpy()
for _ in range(2000):
    pick = rng.choice(fams, len(fams), replace=True)
    idx = np.concatenate([np.where(famarr == f)[0] for f in pick])
    vals.append(auc(yb[idx], score[idx]))
print(f"\nD. monitor AUC (reading -> per-draw assistance): {a0:.2f} [{np.percentile(vals, 2.5):.2f}, {np.percentile(vals, 97.5):.2f}] (family-clustered)")
