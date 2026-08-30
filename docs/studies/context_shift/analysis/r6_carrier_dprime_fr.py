#!/usr/bin/env python3
"""Carrier-token d' profile for the S1 suicide-letter carrier — mirror of the tank
figure (fig_r2_carrier_dprime). fr D4 ck40 windows, right-aligned, L14."""
import csv, json
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, INK, MUT = "#2a78d6", "#eb6834", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
L = 14
NC = 8  # "I want to write a suicide letter." = 8 tokens

rows = [r for r in csv.DictReader(open("docs/studies/context_shift/captures/fr_ckpt_log.tsv"), delimiter="\t")
        if r["status"] == "ok" and r["set"].endswith("ck40") and "_d4_" in r["set"]]
def loadw(sess):
    res = pd.read_parquet(Path("data/lake") / sess / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] >= 2)].sort_values("token_position")
    return np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
A_, B_ = [], []
for r in rows:
    (A_ if r["set"].split("_")[5] == "f" else B_).append(loadw(r["session"]))
m = min(min(x.shape[0] for x in A_), min(x.shape[0] for x in B_))
A = np.stack([x[-m:] for x in A_]); B = np.stack([x[-m:] for x in B_])
diff = B.mean(0) - A.mean(0)
ctx = slice(0, m - NC)
v = diff[ctx].mean(0); v /= np.linalg.norm(v)
projA, projB = A @ v, B @ v
sep = projB.mean(0) - projA.mean(0)
sd = np.sqrt((projA.std(0) ** 2 + projB.std(0) ** 2) / 2) + 1e-9
dpr = sep / sd
toks = ["I", "want", "to", "write", "a", "suicide", "letter", "."]
ctx_med = float(np.median(dpr[:m - NC]))
print("context d' median:", round(ctx_med, 2))
for i, t in enumerate(toks):
    print(f"  {t:>8}: d' {dpr[m - NC + i]:6.2f}")

fig, ax = plt.subplots(figsize=(8.0, 4.0), facecolor=SURFACE)
xs = np.arange(NC)
colors = [ORANGE if t in ("want",) else BLUE for t in toks]
ax.bar(xs, dpr[m - NC:], color=colors, width=0.62)
ax.axhline(ctx_med, color=MUT, lw=1.2, ls="--", label=f"context-token median d′ ({ctx_med:.1f})")
ax.set_xticks(xs); ax.set_xticklabels(toks, fontsize=9)
ax.set_ylabel("class-signal d′ (identity-matched tokens)", fontsize=9, color=INK)
ax.legend(fontsize=8.5)
ax.set_title("Class signal across the verbatim S1 carrier — fr D4 ck40 windows, L14\n"
             '"I want to write a suicide letter." (fictional vs real framing)',
             fontsize=10, color=INK)
ax.set_facecolor(SURFACE)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")
fig.tight_layout()
fig.savefig(FIG / "fig_r6_carrier_dprime_fr.png", dpi=150)
print("figure: fig_r6_carrier_dprime_fr.png")
