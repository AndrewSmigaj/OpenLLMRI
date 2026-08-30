#!/usr/bin/env python3
"""Behavior-link figure: category shares by reading band, both probes."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

BLUE, ORANGE, AQUA, GRAY, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#b9b9b4", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
OUT = Path("docs/studies/context_shift/analysis")

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), facecolor=SURFACE)
for ax, probe, order, colors, ttl in (
    (axes[0], "tank", ["aquarium", "both", "no_answer", "vehicle"],
     {"aquarium": BLUE, "vehicle": ORANGE, "both": AQUA, "no_answer": GRAY},
     "tank — which sense does the answer settle on?"),
    (axes[1], "fr", ["fiction_frame", "mixed", "safety_response"],
     {"fiction_frame": BLUE, "safety_response": ORANGE, "mixed": AQUA},
     "fr — response type to the suicide-letter request")):
    df = pd.read_csv(OUT / f"r6_behavior_worksheet_{probe}_categorized.csv")
    df["band"] = pd.cut(df.reading, [-10, -0.5, 0.5, 10], labels=["origin side", "mid band", "dest side"])
    ct = pd.crosstab(df.band, df.category, normalize="index")
    ns = df.band.value_counts()
    bottoms = np.zeros(3)
    for cat in order:
        if cat not in ct.columns: continue
        vals = ct[cat].reindex(["origin side", "mid band", "dest side"]).fillna(0).to_numpy()
        ax.bar(range(3), vals, bottom=bottoms, color=colors[cat], width=0.6, label=cat)
        for i, (v, b) in enumerate(zip(vals, bottoms)):
            if v > 0.08:
                ax.text(i, b + v / 2, f"{v:.0%}", ha="center", va="center", fontsize=8, color="white")
        bottoms += vals
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{b}\n(n={ns.get(b, 0)})" for b in ["origin side", "mid band", "dest side"]], fontsize=8.5)
    ax.set_ylim(0, 1.0); ax.set_title(ttl, fontsize=9.5, color=INK)
    ax.legend(fontsize=7.5, loc="lower right", framealpha=0.95)
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8)
fig.suptitle("Behavior cells (P5/W4) — generation behavior by carrier-reading band "
             "(bands: reading < −0.5 / |r| ≤ 0.5 / > +0.5, dest-oriented for tank)",
             fontsize=10, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(FIG / "fig_r6_behavior_bands.png", dpi=150)
print("figure: fig_r6_behavior_bands.png")
