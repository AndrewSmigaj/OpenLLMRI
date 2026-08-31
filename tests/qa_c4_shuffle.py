#!/usr/bin/env python3
"""QA C4 — family-level label-shuffle leakage test.
F2/D5: randomly swap fictional/real within each pair (200 perms) -> effect must die.
F2/scene-CV: permute class labels at scene-pair level, rerun held-out accuracy -> chance.
F3: permute D4 arm-class labels at family level + D3 direction labels -> gap ~0 vs perm
distribution; real gap must sit outside the 95% band. F10 excluded per spec.
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(4)
FAILS = []

# ---- F2 / D5 pair-swap ----
piv = pd.read_csv("docs/studies/context_shift/analysis/r6_d5_pairs.csv")
real_eff = piv["diff"].mean()
perm_effs = []
for _ in range(200):
    signs = rng.choice([-1, 1], len(piv))
    perm_effs.append((piv["diff"] * signs).mean())
lo, hi = np.percentile(perm_effs, [2.5, 97.5])
print(f"D5 pair-swap: real +{real_eff:.2f}; perm 95% band [{lo:+.2f},{hi:+.2f}], "
      f"perm mean {np.mean(perm_effs):+.3f}")
if abs(np.mean(perm_effs)) > 0.1 or not (real_eff > hi):
    FAILS.append("D5 shuffle: effect survives or perm mean nonzero")

# ---- F2 / scene-CV label permutation (tank L4) ----
ax_sess = "session_29a80932"
lake = Path("data/lake") / ax_sess
res = pd.read_parquet(lake / "residual_streams.parquet")
res = res[(res["layer"] == 4) & (res["token_position"] == 1)]
tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "input_text", "label"])
df = res.merge(tok, on="probe_id")
X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
y = (df["label"] == "vehicle").to_numpy()
# scene id: match sentence back to pool scenes
pool = json.load(open("data/sentence_sets/polysemy/tank_scene_pools_v1.json"))
smap = {s["text"].strip(): s["categories"]["scene"] for g in pool["groups"] for s in g["sentences"]}
df["sent"] = df["input_text"].apply(lambda t: t.split(" What is the meaning")[0].strip())
df["scene"] = df["sent"].map(smap)
scenes = df["scene"].to_numpy()
uniq = sorted(pd.unique(scenes))
def lofo_acc(labels):
    accs = []
    for hold in uniq:
        tr = scenes != hold; te = ~tr
        if labels[tr].all() or not labels[tr].any(): return np.nan
        a = X[tr][labels[tr]].mean(0) - X[tr][~labels[tr]].mean(0)
        m = (X[tr][labels[tr]].mean(0) + X[tr][~labels[tr]].mean(0)) / 2
        pr = (X[te] - m) @ a
        accs.append(((pr > 0) == labels[te]).mean())
    return float(np.mean(accs))
real_acc = lofo_acc(y)
perm_accs = []
for _ in range(20):
    lab_of_scene = {s: bool(y[scenes == s][0]) for s in uniq}
    ks = list(lab_of_scene)
    vals = rng.permutation([lab_of_scene[k] for k in ks])
    newmap = dict(zip(ks, vals))
    yp = np.array([newmap[s] for s in scenes])
    a2 = lofo_acc(yp)
    if not np.isnan(a2): perm_accs.append(a2)
print(f"scene-CV: real acc {real_acc:.3f}; scene-permuted acc mean {np.mean(perm_accs):.3f} "
      f"(n={len(perm_accs)} perms, max {np.max(perm_accs):.3f})")
if np.mean(perm_accs) > 0.65: FAILS.append("scene-CV: permuted labels still separate = leakage")

# ---- F3 residual-gap shuffle (tank L4, calibration axis space) ----
from second_pass_r1_dynamics import tank_cfg
tag, d4a, d4b, d3, dest_fn, fam_fn = tank_cfg()
A = np.stack(d4a); B = np.stack(d4b)
arms = list(A) + list(B)
def gap_with(arm_assign, dir_assign):
    Ax = np.stack([arms[i] for i, c in enumerate(arm_assign) if c == 0])
    Bx = np.stack([arms[i] for i, c in enumerate(arm_assign) if c == 1])
    mid = (Ax.mean(0) + Bx.mean(0)) / 2
    gaps = []
    for j, (n, proj) in enumerate(sorted(d3.items())):
        dest = dir_assign[j]
        y = ((proj - mid) * dest)[20:40]
        Dm = (Bx if dest > 0 else Ax)
        gaps.append(float(((Dm.mean(0) - mid) * dest)[35:40].mean() - y[15:20].mean()))
    return float(np.mean(gaps))
real_assign = [0] * 6 + [1] * 6
real_dirs = [dest_fn(n) for n in sorted(d3)]
real_gap = gap_with(real_assign, real_dirs)
perm_gaps = []
for _ in range(200):
    pa = list(rng.permutation(real_assign))
    pd_ = list(rng.choice([-1, 1], len(real_dirs)))
    perm_gaps.append(gap_with(pa, pd_))
lo, hi = np.percentile(perm_gaps, [2.5, 97.5])
print(f"F3 gap shuffle: real {real_gap:+.2f}; perm mean {np.mean(perm_gaps):+.2f}, "
      f"95% band [{lo:+.2f},{hi:+.2f}]")
if not (real_gap > hi): FAILS.append("F3 gap: real not outside permuted band")
print("\nC4:", "FAIL: " + "; ".join(FAILS) if FAILS else "PASS")
