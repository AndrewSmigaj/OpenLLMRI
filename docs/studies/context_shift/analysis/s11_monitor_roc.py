#!/usr/bin/env python3
"""s11 — monitor operating characteristic (paper freeze exception, logged in plan):
descriptive re-presentation of the 204 categorized fr behavior cells as a runtime-
monitor curve: does the carrier frame reading predict fiction-frame (vs safety)
response? Positive class = fiction_frame (n=21); score = -reading (fiction-ward).
mixed (n=3) grouped with safety (non-fiction-framed). Stratified caveat from S1.3
(within-k signal at k=2 only) reported alongside."""
import numpy as np, pandas as pd
from pathlib import Path
import matplotlib
WS = "_v2"  # behavior worksheet version: "" = frozen 256-token captures, "_v2" = regenerated (Sept 2026)

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, INK, MUT = "#2a78d6", "#eb6834", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")

df = pd.read_csv(f"docs/studies/context_shift/analysis/r6_behavior_worksheet_fr{WS}_categorized.csv")
df = df[df.k != "d4_final"]
y = (df.category == "fiction_frame").to_numpy()
score = -df.reading.to_numpy()
order = np.argsort(-score)
ys = y[order]
tpr = np.concatenate([[0], np.cumsum(ys) / ys.sum()])
fpr = np.concatenate([[0], np.cumsum(~ys) / (~ys).sum()])
auc = float(np.trapz(tpr, fpr))
rng = np.random.default_rng(13)
boots = []
for _ in range(2000):
    idx = rng.choice(len(y), len(y), replace=True)
    if y[idx].sum() == 0: continue
    o = np.argsort(-score[idx]); yb = y[idx][o]
    t = np.concatenate([[0], np.cumsum(yb) / yb.sum()])
    f = np.concatenate([[0], np.cumsum(~yb) / (~yb).sum()])
    boots.append(np.trapz(t, f))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"AUC(reading -> fiction-frame response): {auc:.2f} [boot {lo:.2f},{hi:.2f}] "
      f"(n={len(df)} transition cells, {int(y.sum())} positives = fiction_frame; {int((df.category == 'no_answer').sum())} no_answer cells counted as negatives)")
# operating point example: threshold at reading < 0.5
thr = 0.5
flag = df.reading < thr
tp = (flag & y).sum(); fp = (flag & ~y).sum()
print(f"example operating point (reading < {thr}): recall {tp/y.sum():.2f}, "
      f"false-flag rate {fp/(~y).sum():.2f}")

fig, ax = plt.subplots(figsize=(5.4, 5.0), facecolor=SURFACE)
ax.plot(fpr, tpr, color=BLUE, lw=2.0, label=f"frame reading (AUC {auc:.2f} [{lo:.2f},{hi:.2f}])")
ax.plot([0, 1], [0, 1], color=MUT, lw=0.9, ls="--", label="chance")
ax.scatter([fp/(~y).sum()], [tp/y.sum()], color=ORANGE, s=50, zorder=5,
           label=f"reading below {thr}: recall {tp/y.sum():.2f}, FPR {fp/(~y).sum():.2f}")
ax.set_xlabel("false-positive rate (safe-completions flagged)", fontsize=9, color=MUT)
ax.set_ylabel("true-positive rate (fiction-writing responses caught)", fontsize=9, color=INK)
ax.set_title("The frame reading as a standalone monitor:\npredicting fiction-writing responses to the request", fontsize=9.5, color=INK)
ax.legend(fontsize=8, loc="lower right")
ax.set_facecolor(SURFACE)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")
fig.tight_layout()
fig.savefig(FIG / "fig_s11_monitor_roc.png", dpi=150)
print("figure: fig_s11_monitor_roc.png")
