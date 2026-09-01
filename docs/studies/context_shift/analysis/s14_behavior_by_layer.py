#!/usr/bin/env python3
"""Per-layer reading->behavior association (EXPLORATORY, post-freeze; logged App. C).
Joins the r3 all-layer projection cache with the categorized behavior worksheets:
does the reading at layer L associate with the behavioral outcome, and does the
association strengthen at deep layers (where fr resolves) vs stay flat (tank)?
Metric: rank AUC. Family-clustered bootstrap bands. No per-layer significance
claims -- descriptive curves."""
import re
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("docs/studies/context_shift/analysis")
FIG = OUT / "figures"
rng = np.random.default_rng(1)

def auc(pos, neg):
    if len(pos) == 0 or len(neg) == 0: return np.nan
    from scipy.stats import rankdata
    allv = np.concatenate([pos, neg]); r = rankdata(allv)
    return (r[:len(pos)].sum() - len(pos)*(len(pos)+1)/2) / (len(pos)*len(neg))

def curves(probe, wf, label_fn, value_fn, subsets):
    z = np.load(OUT / f"r3_projcache_{probe}.npz", allow_pickle=True)
    S = {k[2:]: z[k] for k in z.files if k.startswith("S_")}
    df = pd.read_csv(OUT / wf)
    df = df[df.run.isin(S)].copy()
    df["k"] = pd.to_numeric(df.k, errors="coerce")
    df = df[df.k.notna()]; df["k"] = df.k.astype(int)
    df["y"] = df.category.map(label_fn)
    df = df[df.y.notna()]
    df["fam"] = df.run.str.extract(r"(fam\d+)")
    res = {}
    for name, mask in subsets.items():
        sub = df[mask(df)]
        fams = sub.fam.unique()
        layer_auc, layer_lo, layer_hi = [], [], []
        for L in range(24):
            vals = np.array([value_fn(S[r.run][L, 19 + r.k]) for r in sub.itertuples()])
            y = sub.y.values.astype(bool)
            layer_auc.append(auc(vals[y], vals[~y]))
            boots = []
            for _ in range(400):
                bf = rng.choice(fams, len(fams), replace=True)
                idx = np.concatenate([np.flatnonzero(sub.fam.values == f) for f in bf])
                boots.append(auc(vals[idx][y[idx]], vals[idx][~y[idx]]))
            layer_lo.append(np.nanpercentile(boots, 2.5)); layer_hi.append(np.nanpercentile(boots, 97.5))
        res[name] = (np.array(layer_auc), np.array(layer_lo), np.array(layer_hi), len(sub), int(sub.y.sum()))
    return res

fr = curves("fr", "r6_behavior_worksheet_fr_categorized.csv",
            {"safety_response": 1, "fiction_frame": 0}.get, lambda v: v,
            {"all transition cells": lambda d: d.k.isin([2, 6, 12, 20])})
tank = curves("tank", "r6_behavior_worksheet_tank_categorized.csv",
              {"aquarium": 1, "vehicle": 1, "both": 0}.get, abs,
              {"mid-transition (k in 6,12)": lambda d: d.k.isin([6, 12]),
               "all transition cells": lambda d: d.k.isin([2, 6, 12, 20])})

BLUE, ORANGE, INK, MUT, SURFACE = "#2a78d6", "#eb6834", "#222222", "#8a8a86", "#fcfcfb"
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4), facecolor=SURFACE, sharey=True)
x = np.arange(24)
for (a, lo, hi, n, npos), color, lab in [(fr["all transition cells"], ORANGE,
        f"fr: reading vs safety-response (n={fr['all transition cells'][3]})")]:
    axes[0].fill_between(x, lo, hi, color=color, alpha=0.15)
    axes[0].plot(x, a, color=color, lw=2, label=lab)
axes[0].axvline(14, color=INK, lw=0.8, ls=":"); axes[0].text(14.2, 0.97, "L14 (site)", fontsize=8, color=INK)
axes[0].set_title("fiction/real — per-layer reading vs response type", fontsize=10, color=INK)
for key, color in [("mid-transition (k in 6,12)", BLUE), ("all transition cells", MUT)]:
    a, lo, hi, n, npos = tank[key]
    axes[1].fill_between(x, lo, hi, color=color, alpha=0.13)
    axes[1].plot(x, a, color=color, lw=2, label=f"tank |reading|: decided vs hedged, {key} (n={n})")
axes[1].axvline(4, color=INK, lw=0.8, ls=":"); axes[1].text(4.2, 0.97, "L4 (site)", fontsize=8, color=INK)
axes[1].set_title("tank — per-layer |reading| vs decided-vs-hedged", fontsize=10, color=INK)
for ax in axes:
    ax.axhline(0.5, color=MUT, lw=0.8)
    ax.set_xlabel("layer", fontsize=9, color=MUT); ax.set_facecolor(SURFACE)
    ax.legend(fontsize=7.5, loc="lower right"); ax.grid(True, lw=0.35, color="#e8e8e4")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[0].set_ylabel("AUC (family-clustered 95% band)", fontsize=9, color=INK)
fig.suptitle("EXPLORATORY (post-freeze): reading→behavior association by layer", fontsize=11, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FIG / "fig_s14_behavior_by_layer.png", dpi=150, bbox_inches="tight", facecolor=SURFACE)

for probe, res in (("fr", fr), ("tank", tank)):
    for k, (a, lo, hi, n, npos) in res.items():
        print(f"{probe} [{k}] n={n} pos={npos}: L2={a[2]:.2f} L4={a[4]:.2f} L8={a[8]:.2f} "
              f"L14={a[14]:.2f} L20={a[20]:.2f} L23={a[23]:.2f} | max L{np.nanargmax(a)}={np.nanmax(a):.2f}")
print("fig_s14_behavior_by_layer.png written")
