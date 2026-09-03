#!/usr/bin/env python3
"""R3 figures: Item 17 secondary-instrument heatmap re-render (fr + tank) and the
axis-rotation profile. Caches all-layer projections to r3_projcache_{probe}.npz."""
import json
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r3_instruments import CFG, proj_all_layers

BLUE, ORANGE, INK, MUT = "#2a78d6", "#eb6834", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
DIV = LinearSegmentedColormap.from_list("div", [BLUE, "#f4f4f2", ORANGE])
FIG = Path("docs/studies/context_shift/analysis/figures")
OUT = Path("docs/studies/context_shift/analysis")
AXD = OUT / "axes"

for probe, c in CFG.items():
    cache = OUT / f"r3_projcache_{probe}.npz"
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        S = {k[2:]: z[k] for k in z.files if k.startswith("S_")}
    else:
        sec = np.load(AXD / f"secondary_axis_{probe}.npz")
        cal = np.load(AXD / c["cal"])
        S, C = proj_all_layers(c["log"], cal, sec, c["filt"])
        np.savez(cache, **{f"S_{k}": v for k, v in S.items()}, **{f"C_{k}": v for k, v in C.items()})
    d1, d2 = c["dirs"]
    neg, pos = ("aquarium", "vehicle") if probe == "tank" else ("fictional", "real")
    panels = [
        (f"no-shift, {neg}", [S[n] for n in S if c["isd4"](n) and not c["plus"](n)]),
        (f"no-shift, {pos}", [S[n] for n in S if c["isd4"](n) and c["plus"](n)]),
        (f"transition, {neg} → {pos}", [S[n] for n in S if not c["isd4"](n) and n.endswith(d1)]),
        (f"transition, {pos} → {neg}", [S[n] for n in S if not c["isd4"](n) and n.endswith(d2)]),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(14.5, 4.4), facecolor=SURFACE, sharey=True)
    vmax = 2.0
    for ax, (ttl, mats) in zip(axes, panels):
        M = np.mean(mats, axis=0)
        im = ax.imshow(M, aspect="auto", origin="lower", cmap=DIV, vmin=-vmax, vmax=vmax,
                       extent=[1, 40, 0, 23])
        ax.axvline(20.5, color=INK, lw=1.0, ls="--")
        ax.set_title(f"{ttl} (n={len(mats)})", fontsize=9.5, color=INK)
        ax.set_xlabel("sentence position", fontsize=8.5, color=MUT)
        ax.set_facecolor(SURFACE)
        ax.tick_params(colors=MUT, labelsize=8)
    axes[0].set_ylabel("layer", fontsize=9, color=INK)
    cb = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.01)
    cb.set_label("reading (±1 = accumulated-context class means)", fontsize=8, color=MUT)
    task = "Tank task, ' tank' site" if probe == "tank" else "Fiction/real task, ' want' site"
    fig.suptitle(f"{task}: readings under per-layer accumulated-context axes", fontsize=11, color=INK)
    fig.savefig(FIG / f"fig_r3_heatmap_secondary_{probe}.png", dpi=150,
                bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(f"written fig_r3_heatmap_secondary_{probe}.png")

# rotation profile figure
fig, ax = plt.subplots(figsize=(7.6, 3.8), facecolor=SURFACE)
for probe, color in (("tank", BLUE), ("fr", ORANGE)):
    sec = np.load(AXD / f"secondary_axis_{probe}.npz")
    cal = np.load(AXD / CFG[probe]["cal"])
    coss = [float(sec[f"axis_{L}"] @ (cal[f"axis_{L}"] / np.linalg.norm(cal[f"axis_{L}"]))) for L in range(24)]
    ax.plot(range(24), coss, "o-", color=color, lw=1.6, ms=4, label="tank task" if probe == "tank" else "fiction/real task")
ax.set_ylim(0, 1.05); ax.axhline(1.0, color=MUT, lw=0.7, ls=":")
ax.set_xlabel("layer", fontsize=9, color=MUT); ax.set_ylabel("cosine (accumulated-context axis, calibration axis)", fontsize=9, color=INK)
ax.legend(fontsize=9)
ax.set_title("Axis rotation with accumulating context", fontsize=10, color=INK)
ax.set_facecolor(SURFACE)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")
fig.tight_layout()
fig.savefig(FIG / "fig_r3_axis_rotation.png", dpi=150)
print("written fig_r3_axis_rotation.png")
