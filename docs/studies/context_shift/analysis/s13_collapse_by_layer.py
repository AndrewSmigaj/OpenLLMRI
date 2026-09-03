#!/usr/bin/env python3
"""Collapse-style panels at selected layers (secondary per-layer axes, class means
at +/-1, midpoint = 0 by construction): both transition directions + no-shift
reference bands + unresolved band, per layer. Answers: how does the single-site
collapse figure generalize across depth? Uses the r3 all-layer projection cache."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r3_instruments import CFG

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
OUT = Path("docs/studies/context_shift/analysis")
FIG = OUT / "figures"
LAYERS = {"tank": [2, 4, 12, 20, 23], "fr": [2, 8, 14, 20, 23]}
SITE = {"tank": 4, "fr": 14}

fig, axes = plt.subplots(2, 5, figsize=(17.5, 7.2), facecolor=SURFACE, sharex=True)
for row, (probe, c) in enumerate(CFG.items()):
    z = np.load(OUT / f"r3_projcache_{probe}.npz", allow_pickle=True)
    S = {k[2:]: z[k] for k in z.files if k.startswith("S_")}
    d1, d2 = c["dirs"]
    lab1, lab2 = (("aquarium → vehicle", "vehicle → aquarium") if probe == "tank"
                  else ("fictional → real", "real → fictional"))
    x = np.arange(1, 41)
    for col, L in enumerate(LAYERS[probe]):
        ax = axes[row, col]
        A = np.stack([S[n][L] for n in S if c["isd4"](n) and not c["plus"](n)])
        B = np.stack([S[n][L] for n in S if c["isd4"](n) and c["plus"](n)])
        for M, color in ((A, BLUE), (B, ORANGE)):
            ax.fill_between(x, M.mean(0) - M.std(0), M.mean(0) + M.std(0), color=color, alpha=0.10)
            ax.plot(x, M.mean(0), color=color, lw=1.0, ls=":", alpha=0.8)
        d4_all = np.concatenate([A[:, 10:40].ravel(), B[:, 10:40].ravel()])
        lo = np.percentile(d4_all[d4_all < 0], 95); hi = np.percentile(d4_all[d4_all > 0], 5)
        ax.axhspan(lo, hi, color=AQUA, alpha=0.10)
        for dsuf, color, lab in ((d1, ORANGE, lab1), (d2, BLUE, lab2)):
            ys = np.stack([S[n][L] for n in S if not c["isd4"](n) and n.endswith(dsuf)])
            ax.plot(x, ys.mean(0), color=color, lw=2.0, label=lab)
            ax.fill_between(x, ys.mean(0) - ys.std(0), ys.mean(0) + ys.std(0), color=color, alpha=0.18)
        ax.axvline(20.5, color=INK, lw=0.9, ls="--")
        ax.axhline(0, color=MUT, lw=0.6)
        star = " (calibrated site)" if L == SITE[probe] else ""
        task_name = "Tank task" if probe == "tank" else "Fiction/real task"
        ax.set_title(f"{task_name}, layer {L}{star}", fontsize=9.5, color=INK)
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.tick_params(colors=MUT, labelsize=7.5); ax.grid(True, lw=0.35, color="#e8e8e4")
        if row == 1: ax.set_xlabel("sentence position (shift after 20)", fontsize=8.5, color=MUT)
        if col == 0:
            ax.set_ylabel("reading under the layer\'s accumulated-context axis\n(class means at ±1; 0 = midpoint)",
                          fontsize=8.5, color=INK)
            ax.legend(fontsize=7, loc="lower left")
fig.suptitle("The collapse view across depth: Figure 1 repeated at five layers per task, each under its own accumulated-context axis", fontsize=11, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FIG / "fig_s13_collapse_layers.png", dpi=150, bbox_inches="tight", facecolor=SURFACE)
# late-window destination-signed band means (quoted in section 3.2)
for probe, c in CFG.items():
    z = np.load(OUT / f"r3_projcache_{probe}.npz", allow_pickle=True)
    S = {k[2:]: z[k] for k in z.files if k.startswith("S_")}
    for suf, dest in ((c["dirs"][0], +1), (c["dirs"][1], -1)):
        M = np.stack([S[n] for n in S if not c["isd4"](n) and n.endswith(suf)]).mean(0) * dest
        print(f"{probe} {suf} late-window (k16-20) dest-signed band means: "
              f"L0-2 {M[0:3,35:40].mean():+.2f} | L3-12 {M[3:13,35:40].mean():+.2f} | "
              f"L13-18 {M[13:19,35:40].mean():+.2f} | L19-23 {M[19:24,35:40].mean():+.2f}")
print("fig_s13_collapse_layers.png written")
