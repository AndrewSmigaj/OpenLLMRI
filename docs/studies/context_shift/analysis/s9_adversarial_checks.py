#!/usr/bin/env python3
"""S9 — peer-review hardening checks (adversarial pass on FINDINGS_FINAL).

C1 (F2/D5): length confound (fictional versions are longer?) + low-overlap robustness.
C2 (F10): axis-leakage — cos(shared marker direction, class axis) should be ~0
    (class axis lives INSIDE the D4 subspace by construction).
C3 (F10): held-out direction estimation — estimate vdir on half the families,
    measure the other half's mean-residual projection on it (kills in-sample
    direction inflation; the D6 projection already served as capture-level holdout).
"""
import sys, json, csv, glob
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(51)

# ---------------- C1: D5 confounds ----------------
print("=" * 74)
print("C1 — D5: length confound + low-overlap robustness")
piv = pd.read_csv("docs/studies/context_shift/analysis/r6_d5_pairs.csv")
pairs = []
for i in (1, 2, 3):
    pairs.extend(json.load(open(f"docs/studies/context_shift/generation/batches_d5/d5_batch{i}.json")))
import re
meta = {p["pair_id"]: p for p in pairs}
piv["len_diff"] = piv.pair.map(lambda pid: len(meta[pid]["fictional"].split()) - len(meta[pid]["real"].split()))
def jac(pid):
    fw = set(re.findall(r"[a-z']+", meta[pid]["fictional"].lower()))
    rw = set(re.findall(r"[a-z']+", meta[pid]["real"].lower()))
    return len(fw & rw) / max(len(fw | rw), 1)
piv["jaccard"] = piv.pair.map(jac)
r_len = np.corrcoef(piv.len_diff, piv["diff"])[0, 1]
print(f"  word-count diff (fic-real): mean {piv.len_diff.mean():+.1f}; corr with effect r={r_len:.2f}")
matched = piv[piv.len_diff.abs() <= 2]
print(f"  length-matched pairs (|dlen|<=2): n={len(matched)}, effect {matched['diff'].mean():+.2f} "
      f"(all pairs {piv['diff'].mean():+.2f})")
hi = piv[piv.jaccard >= 0.35]
print(f"  overlap-robust (jaccard>=0.35): n={len(hi)}, effect {hi['diff'].mean():+.2f}; "
      f"low-overlap excluded n={len(piv)-len(hi)}")

# ---------------- C2/C3: F10 marker ----------------
def load_raw(log, L, keep):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    out = {}
    for r in rows:
        n = r["run"]
        if not keep(n): continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        out[n] = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    return out

print("\n" + "=" * 74)
print("C2/C3 — F10 marker: axis leakage + held-out direction estimation")
for tag, log, L, axf, d3k, d4k, fam in (
    ("tank_L4", "docs/studies/context_shift/captures/tank_d3_d4_log.tsv", 4,
     "axes_session_29a80932_aquarium_vs_vehicle_pos1.npz",
     lambda n: "_d3_" in n, lambda n: "_d4_" in n, lambda n: int(n.split("_")[2][3:])),
    ("fr_L14", "docs/studies/context_shift/captures/fr_d3_d4_log.tsv", 14,
     "axes_session_5247081b_fictional_vs_real_pos1.npz",
     lambda n: "fr_s1_" in n and "_d3_" in n, lambda n: "fr_s1_" in n and "_d4_" in n,
     lambda n: int(n.split("_")[4][3:]))):
    d4 = load_raw(log, L, d4k); d3 = load_raw(log, L, d3k)
    D4mat = np.concatenate([v[20:40] for v in d4.values()])
    center = D4mat.mean(0)
    _, S, Vt = np.linalg.svd(D4mat - center, full_matrices=False)
    cum = np.cumsum(S**2 / (S**2).sum()); kc = int(np.searchsorted(cum, 0.90)) + 1
    Vk = Vt[:kc]
    def resid_of(X): Y = np.atleast_2d(X) - center; return Y - (Y @ Vk.T) @ Vk
    post = {n: resid_of(v[20:40]) for n, v in d3.items()}
    vdir = np.concatenate(list(post.values())).mean(0)
    mag_full = np.linalg.norm(vdir); vdir /= mag_full
    ax = np.load(f"docs/studies/context_shift/analysis/axes/{axf}")
    a = ax[f"axis_{L}"].astype(np.float64); a /= np.linalg.norm(a)
    print(f"  {tag}: cos(marker dir, class axis) = {float(vdir @ a):+.3f} "
          f"(expected ~0: class axis lies inside the D4 subspace)")
    # C3: split families even/odd; direction from one half, magnitude on the other
    runs = list(post)
    even = [n for n in runs if fam(n) % 2 == 0]; odd = [n for n in runs if fam(n) % 2 == 1]
    for est, test, nm in ((even, odd, "even->odd"), (odd, even, "odd->even")):
        vd = np.concatenate([post[n] for n in est]).mean(0)
        vd /= np.linalg.norm(vd)
        proj = float(np.concatenate([post[n] for n in test]).mean(0) @ vd)
        print(f"    held-out {nm}: test-half mean-resid projection on train-dir = "
              f"{proj:.1f} (in-sample magnitude {mag_full:.1f})")
