#!/usr/bin/env python3
"""Behavior-link figure: category shares by reading band, both probes."""
import pandas as pd, numpy as np
import matplotlib
WS = "_v2"  # behavior worksheet version: "" = frozen 256-token captures, "_v2" = regenerated (Sept 2026)

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
     "Tank task: which sense does the answer settle on?"),
    (axes[1], "fr", ["fiction_frame", "mixed", "no_answer", "safety_response"],
     {"fiction_frame": BLUE, "safety_response": ORANGE, "mixed": AQUA, "no_answer": GRAY},
     "Fiction/real task: response type to the request")):
    df = pd.read_csv(OUT / f"r6_behavior_worksheet_{probe}{WS}_categorized.csv")
    df["band"] = pd.cut(df.reading, [-10, -0.5, 0.5, 10], labels=["origin side", "mid band", "dest side"])
    ct = pd.crosstab(df.band, df.category, normalize="index")
    ns = df.band.value_counts()
    # printed record for the paper: counts, then rates with no_answer counted and over delivered answers
    print(f"{probe}: bands on the raw reading (negative = {'aquarium' if probe == 'tank' else 'fiction'} side); all {len(df)} cells")
    print(pd.crosstab(df.band, df.category).to_string())
    print("rates, all cells:"); print(ct.round(2).to_string())
    dl = df[df.category != "no_answer"]
    print(f"rates, delivered answers only (n={len(dl)}):"); print(pd.crosstab(dl.band, dl.category, normalize="index").round(2).to_string())
    bottoms = np.zeros(3)
    for cat in order:
        if cat not in ct.columns: continue
        vals = ct[cat].reindex(["origin side", "mid band", "dest side"]).fillna(0).to_numpy()
        names = {"no_answer": "no answer", "both": "both senses", "fiction_frame": "fiction-writing assistance",
                 "safety_response": "safe-completion", "mixed": "mixed"}
        ax.bar(range(3), vals, bottom=bottoms, color=colors[cat], width=0.6, label=names.get(cat, cat))
        for i, (v, b) in enumerate(zip(vals, bottoms)):
            if v > 0.08:
                ax.text(i, b + v / 2, f"{v:.0%}", ha="center", va="center", fontsize=8, color="white")
        bottoms += vals
    ax.set_xticks(range(3))
    shown = ({"origin side": "aquarium side", "mid band": "middle band", "dest side": "vehicle side"} if probe == "tank"
             else {"origin side": "fiction side", "mid band": "middle band", "dest side": "real side"})
    ax.set_xticklabels([f"{shown[b]}\n(n = {ns.get(b, 0)})" for b in ["origin side", "mid band", "dest side"]], fontsize=8.5)
    ax.set_ylim(0, 1.0); ax.set_title(ttl, fontsize=9.5, color=INK)
    ax.set_ylabel("share of completions", fontsize=9, color=INK)
    ax.legend(fontsize=7.5, loc="lower right", framealpha=0.95)
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8)
fig.suptitle("Behavior by reading band at generation time\n"
             "(bands on the reading: below −0.5, within ±0.5 of the midpoint, above +0.5; negative is the aquarium side and the fiction side)",
             fontsize=9, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(FIG / "fig_r6_behavior_bands.png", dpi=150)
print("figure: fig_r6_behavior_bands.png")
