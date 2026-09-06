#!/usr/bin/env python3
"""Behavior-link figure: category shares by reading band, both tasks. Top row: the
delivered answer (with the share that never answered). Bottom row: the reasoning
channel's commitment for the same cells (every cell has one; loops are read from
their early reasoning). Rates are printed both with loops counted and over
delivered answers only."""
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
NAMES = {"no_answer": "no answer", "both": "both senses", "fiction_frame": "fiction-writing assistance",
         "safety_response": "safe-completion", "mixed": "mixed", "aquarium": "aquarium", "vehicle": "vehicle"}
BANDS = ["origin side", "mid band", "dest side"]

fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0), facecolor=SURFACE)
for col, (probe, order, colors, ttl, shown) in enumerate((
    ("tank", ["aquarium", "both", "no_answer", "vehicle"],
     {"aquarium": BLUE, "vehicle": ORANGE, "both": AQUA, "no_answer": GRAY},
     "Tank task: which sense does the answer settle on?",
     {"origin side": "aquarium side", "mid band": "middle band", "dest side": "vehicle side"}),
    ("fr", ["fiction_frame", "mixed", "no_answer", "safety_response"],
     {"fiction_frame": BLUE, "safety_response": ORANGE, "mixed": AQUA, "no_answer": GRAY},
     "Fiction/real task: response type to the request",
     {"origin side": "fiction-writing side", "mid band": "middle band", "dest side": "real-world side"}))):
    df = pd.read_csv(OUT / f"r6_behavior_worksheet_{probe}{WS}_categorized.csv")
    df["band"] = pd.cut(df.reading, [-10, -0.5, 0.5, 10], labels=BANDS)
    ns = df.band.value_counts()
    for row, (column, label) in enumerate((("category", "delivered answer"), ("reasoning_category", "reasoning channel's commitment"))):
        ax = axes[row, col]
        ct = pd.crosstab(df.band, df[column], normalize="index")
        print(f"{probe} — {label}: bands on the raw reading (negative = {'aquarium' if probe == 'tank' else 'fiction-writing'} side); all {len(df)} cells")
        print(pd.crosstab(df.band, df[column]).to_string()); print("rates:"); print(ct.round(2).to_string())
        if column == "category":
            dl = df[df.category != "no_answer"]
            print(f"rates over delivered answers only (n={len(dl)}):"); print(pd.crosstab(dl.band, dl.category, normalize="index").round(2).to_string())
        bottoms = np.zeros(3)
        for cat in order:
            if cat not in ct.columns: continue
            vals = ct[cat].reindex(BANDS).fillna(0).to_numpy()
            ax.bar(range(3), vals, bottom=bottoms, color=colors[cat], width=0.6, label=NAMES.get(cat, cat))
            for i, (v, b) in enumerate(zip(vals, bottoms)):
                if v > 0.08: ax.text(i, b + v / 2, f"{v:.0%}", ha="center", va="center", fontsize=8, color="white")
            bottoms += vals
        ax.set_xticks(range(3))
        ax.set_xticklabels([f"{shown[b]}\n(n = {ns.get(b, 0)})" for b in BANDS], fontsize=8.5)
        ax.set_ylim(0, 1.0); ax.set_title(f"{ttl}\n{label}", fontsize=9.5, color=INK)
        ax.set_ylabel("share of completions", fontsize=9, color=INK)
        ax.legend(fontsize=7.5, loc="lower right", framealpha=0.95)
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.tick_params(colors=MUT, labelsize=8)
fig.suptitle("Behavior by reading band at generation time: the delivered answer (top) and the reasoning channel's commitment (bottom)\n"
             "(bands on the reading: below −0.5, within ±0.5 of the midpoint, above +0.5; negative is the aquarium side and the fiction-writing side)",
             fontsize=9, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FIG / "fig_r6_behavior_bands.png", dpi=150)
print("figure: fig_r6_behavior_bands.png")
