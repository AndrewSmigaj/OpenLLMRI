#!/usr/bin/env python3
"""s25 — behavior under the model's recommended sampling, by referenced reading band
(8 September 2026). Companion to r6_behavior_figure.py (greedy). Regimes are never
pooled: this figure is the sampled regime only.

Panels: (a) fiction/real, share of draws by response type per band, three draws per
cell pooled (safe completions split into redirect and refusal-only; mixed = helps with
the letter and redirects; fiction-writing assistance); (b) fiction/real, share of cells
by how many of their three draws delivered assistance (0–3), per band; (c) tank, share
of draws by the sense the answer settles on, one draw per cell. Bands: reading minus the
position-matched no-shift midpoint, cut at ±0.5 axis units (s25_referenced_bands.py).
Prints every plotted count. Run from the repository root.
"""
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import fr_cfg, tank_cfg
A = Path("docs/studies/context_shift/analysis"); FIG = A / "figures"
BLUE, ORANGE, AQUA, GRAY, INK, MUT, SURFACE = "#2a78d6", "#eb6834", "#1baf7a", "#b9b9b4", "#222222", "#8a8a86", "#fcfcfb"
def mid(cfg): _, a, b, *_ = cfg(); return (np.stack(a).mean(0) + np.stack(b).mean(0)) / 2
MID = {"fr": mid(fr_cfg), "tank": mid(tank_cfg)}
def load(task, tag):
    d = pd.read_csv(A / f"r6_behavior_worksheet_{task}_{tag}_categorized.csv")
    pos = np.where(d.set.str.contains("_beh_final"), 40, 20 + pd.to_numeric(d.k, errors="coerce").fillna(20).astype(int))
    d["ref"] = d.reading - MID[task][pos - 1]
    lo, hi = ("fiction-writing side", "real-world side") if task == "fr" else ("aquarium side", "vehicle side")
    d["band"] = np.where(d.ref < -0.5, lo, np.where(d.ref > 0.5, hi, "middle")); d["bands"] = [lo, "middle", hi][0:0] or None
    return d, [lo, "middle", hi]
fr = pd.concat([load("fr", s)[0].assign(draw=s) for s in ("s1", "s2", "s3")]); FB = load("fr", "s1")[1]
fr["type"] = np.where(fr.category == "safety_response", np.where(fr.safety_subtype == "refusal_only", "refusal only", "redirect to support"), np.where(fr.category == "mixed", "mixed", "fiction-writing assistance"))
tk, TB = load("tank", "s1")

fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.6), facecolor=SURFACE)
# (a) fr per-draw response type by band
order_a = ["fiction-writing assistance", "mixed", "refusal only", "redirect to support"]; col_a = {"fiction-writing assistance": BLUE, "mixed": AQUA, "refusal only": "#f2a071", "redirect to support": ORANGE}
ct = pd.crosstab(fr.band, fr.type).reindex(index=FB, columns=order_a, fill_value=0); n = ct.sum(1)
print("(a) fiction/real draws by band and type:\n" + ct.to_string())
ax = axes[0]; bottom = np.zeros(len(FB))
for t in order_a:
    v = (ct[t] / n).to_numpy(); ax.bar(range(len(FB)), v, bottom=bottom, color=col_a[t], label=t, width=0.6); bottom += v
ax.set_xticks(range(len(FB))); ax.set_xticklabels([f"{b}\n{int(n[b])} draws" for b in FB], fontsize=8.5, color=INK); ax.set_ylim(0, 1); ax.set_ylabel("share of draws", color=INK)
ax.set_title("Fiction/real: response type per draw", fontsize=10, color=INK); ax.legend(fontsize=7.5, frameon=False, loc="lower left")
# (b) fr per-cell draws with assistance
cells = fr.groupby("set").agg(band=("band", "first"), n=("category", lambda c: int(c.isin(["fiction_frame", "mixed"]).sum())))
ct2 = pd.crosstab(cells.band, cells.n).reindex(index=FB, columns=[0, 1, 2, 3], fill_value=0); n2 = ct2.sum(1)
print("(b) fiction/real cells by band and number of assisting draws:\n" + ct2.to_string())
ax = axes[1]; bottom = np.zeros(len(FB)); shades = {0: ORANGE, 1: "#f2b58f", 2: "#8fc4ea", 3: BLUE}
for k in [0, 1, 2, 3]:
    v = (ct2[k] / n2).to_numpy(); ax.bar(range(len(FB)), v, bottom=bottom, color=shades[k], label=f"{k} of 3 draws assist", width=0.6); bottom += v
ax.set_xticks(range(len(FB))); ax.set_xticklabels([f"{b}\n{int(n2[b])} cells" for b in FB], fontsize=8.5, color=INK); ax.set_ylim(0, 1); ax.set_ylabel("share of cells", color=INK)
ax.set_title("Fiction/real: assisting draws per cell", fontsize=10, color=INK); ax.legend(fontsize=7.5, frameon=False, loc="lower left")
# (c) tank per-draw sense by band
order_c = ["aquarium", "both", "vehicle"]; col_c = {"aquarium": BLUE, "both": AQUA, "vehicle": ORANGE}
ct3 = pd.crosstab(tk.band, tk.category).reindex(index=TB, columns=order_c, fill_value=0); n3 = ct3.sum(1)
print("(c) tank cells by band and sense:\n" + ct3.to_string())
ax = axes[2]; bottom = np.zeros(len(TB))
for t in order_c:
    v = (ct3[t] / n3).to_numpy(); ax.bar(range(len(TB)), v, bottom=bottom, color=col_c[t], label={"both": "both senses"}.get(t, t), width=0.6); bottom += v
ax.set_xticks(range(len(TB))); ax.set_xticklabels([f"{b}\n{int(n3[b])} draws" for b in TB], fontsize=8.5, color=INK); ax.set_ylim(0, 1); ax.set_ylabel("share of draws", color=INK)
ax.set_title("Tank: sense the answer settles on", fontsize=10, color=INK); ax.legend(fontsize=7.5, frameon=False, loc="lower left")
for ax in axes:
    ax.set_facecolor(SURFACE); ax.spines[["top", "right"]].set_visible(False); ax.tick_params(colors=MUT)
fig.suptitle("Behavior under the model's recommended sampling, by reading band at generation time\n(bands on the reading referenced to the position-matched no-shift midpoint, ±0.5 axis units; no draw loops)", fontsize=10.5, color=INK)
fig.tight_layout(); fig.savefig(FIG / "fig_s25_behavior_sampled.png", dpi=150); print("figure: fig_s25_behavior_sampled.png")
