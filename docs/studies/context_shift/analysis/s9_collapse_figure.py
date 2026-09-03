#!/usr/bin/env python3
"""The collapse overlay — both transition directions on ONE axes per probe, with the
no-shift reference bands and the unresolved band: the central phenomenon in one image."""
import sys
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from second_pass_r1_dynamics import tank_cfg, fr_cfg

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")

fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), facecolor=SURFACE)
for ax, cfgf, ttl, d1, d2, lab1, lab2, refA, refB in (
    (axes[0], tank_cfg, "Tank task: ' tank' token, layer 4 (aquarium −, vehicle +)",
     "_ab", "_ba", "aquarium → vehicle", "vehicle → aquarium",
     "no-shift reference, aquarium (mean ± 1 sd)", "no-shift reference, vehicle (mean ± 1 sd)"),
    (axes[1], fr_cfg, "Fiction/real task: ' want' token, layer 14 (fictional −, real +)",
     "_fr", "_rf", "fictional → real", "real → fictional",
     "no-shift reference, fictional (mean ± 1 sd)", "no-shift reference, real (mean ± 1 sd)")):
    tag, d4a, d4b, d3, dest_fn, fam_fn = cfgf()
    A = np.stack(d4a); B = np.stack(d4b)
    mid = (A.mean(0) + B.mean(0)) / 2.0
    x = np.arange(1, 41)
    for M, color, rl in ((A - mid, BLUE, refA), (B - mid, ORANGE, refB)):
        ax.fill_between(x, M.mean(0) - M.std(0), M.mean(0) + M.std(0), color=color, alpha=0.10)
        ax.plot(x, M.mean(0), color=color, lw=1.0, ls=":", alpha=0.8, label=rl)
    d4_all = np.concatenate([(A - mid)[:, 10:40].ravel(), (B - mid)[:, 10:40].ravel()])
    lo = np.percentile(d4_all[d4_all < 0], 95); hi = np.percentile(d4_all[d4_all > 0], 5)
    ax.axhspan(lo, hi, color=AQUA, alpha=0.10, label="core of unresolved zone")
    for dsuf, color, lab in ((d1, ORANGE, lab1), (d2, BLUE, lab2)):
        ys = np.stack([(d3[n] - mid) for n in d3 if n.endswith(dsuf)])
        ax.plot(x, ys.mean(0), color=color, lw=2.2, label=lab)
        ax.fill_between(x, ys.mean(0) - ys.std(0), ys.mean(0) + ys.std(0), color=color, alpha=0.20)
    ax.axvline(20.5, color=INK, lw=1.0, ls="--", label="shift")
    ax.axhline(0, color=MUT, lw=0.7)
    ax.set_title(ttl, fontsize=10, color=INK)
    ax.set_xlabel("sentence position (shift after sentence 20)", fontsize=9, color=MUT)
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False)
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")
axes[0].set_ylabel("reading (axis units; 0 = midpoint between the references)", fontsize=9.5, color=INK)
fig.tight_layout()
fig.savefig(FIG / "fig_s9_collapse.png", dpi=150)
print("fig_s9_collapse.png written")
