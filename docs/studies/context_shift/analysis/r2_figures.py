#!/usr/bin/env python3
"""R2 figures: within-stream occupancy histograms (2c), carrier-site mode-location track
(12a), and the carrier-token d' profile (6a)."""
import csv, json
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import tank_cfg

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
L = 4

def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8)
    ax.grid(True, lw=0.4, color="#e8e8e4")

# ---- load right-aligned windows ----
rows = [r for r in csv.DictReader(open("docs/studies/context_shift/captures/tank_ckpt_log.tsv"), delimiter="\t") if r["status"] == "ok"]
seen = set(); kept = []
for r in rows:
    if r["set"] not in seen: seen.add(r["set"]); kept.append(r)
def loadw(sess):
    res = pd.read_parquet(Path("data/lake") / sess / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] >= 2)].sort_values("token_position")
    return np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
win = {}
for r in kept:
    p = r["set"].split("_")
    win[(p[1], p[2], p[3], p[4])] = loadw(r["session"])

fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.2), facecolor=SURFACE, sharex=True)
prof40 = None
for j, ck in enumerate(("ck20", "ck30", "ck40")):
    d4A = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "a" and c == ck]
    d4B = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "b" and c == ck]
    m = min(min(x.shape[0] for x in d4A), min(x.shape[0] for x in d4B))
    A = np.stack([x[-m:] for x in d4A]); B = np.stack([x[-m:] for x in d4B])
    mid_p = (A.mean(0) + B.mean(0)) / 2; diff = B.mean(0) - A.mean(0)
    ctx = slice(0, m - 9)
    v = diff[ctx].mean(0); v /= np.linalg.norm(v)
    denom_p = diff @ v
    ok = np.where((np.arange(m) < m - 9) & (denom_p > 0.3 * np.median(denom_p[ctx])))[0]
    if ck == "ck40": prof40 = (A, B, v, m)
    for i, a_ in enumerate(("ab", "ba")):
        vals = []
        for (k, f, arm, c), X in win.items():
            if k != "d3" or c != ck or arm != a_: continue
            mm = min(X.shape[0], m)
            pp = ok[ok >= m - mm]
            r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom_p[pp]
            vals.extend((r_ * (+1 if a_ == "ab" else -1)).tolist())
        ax = axes[i, j]
        ax.hist(np.clip(vals, -6, 6), bins=48, color=BLUE if a_ == "ab" else ORANGE, alpha=0.85)
        for x0, lab in ((-1, "origin ref"), (+1, "dest ref")):
            ax.axvline(x0, color=INK, lw=0.9, ls="--")
        ax.axvline(float(np.mean(vals)), color=AQUA, lw=1.6)
        ckn = {"ck20": "at 20 sentences", "ck30": "at 30 sentences (10 post-shift)", "ck40": "at 40 sentences (20 post-shift)"}[ck]
        dirn = {"ab": "aquarium → vehicle", "ba": "vehicle → aquarium"}[a_]
        ax.set_title(f"{ckn}, {dirn}: mean {np.mean(vals):+.2f}", fontsize=8.5, color=INK)
        style(ax)
axes[1, 1].set_xlabel("per-token reading (−1 = mean of the same tokens in origin-class no-shift runs, +1 = mean in destination-class runs)",
                      fontsize=8.5, color=MUT)
axes[0, 0].set_ylabel("tokens", fontsize=8.5, color=INK); axes[1, 0].set_ylabel("tokens", fontsize=8.5, color=INK)
fig.suptitle("Tank task, layer 4: readings of the context tokens themselves, against no-shift references matched for content and position\n"
             "(the post-shift block is destination-class content; only the history differs; means sit short of +1)",
             fontsize=10.5, color=INK)
fig.tight_layout(rect=[0, 0.01, 1, 0.92])
fig.savefig(FIG / "fig_r2_within_stream.png", dpi=150)
plt.close(fig)

# ---- 12a mode-location track ----
tag, d4a, d4b, d3, dest_fn, fam_fn = tank_cfg()
Ar = np.stack(d4a); Br = np.stack(d4b)
mid = (Ar.mean(0) + Br.mean(0)) / 2.0
fig, ax = plt.subplots(figsize=(8.4, 4.4), facecolor=SURFACE)
bands = [("post-shift 1–5", 0, 5), ("6–10", 5, 10), ("11–15", 10, 15), ("16–20", 15, 20)]
grid = np.linspace(-3, 3, 601)
for sign, color, lab in ((+1.0, BLUE, "aquarium → vehicle"), (-1.0, ORANGE, "vehicle → aquarium")):
    ys = np.stack([((d3[n] - mid) * sign)[20:40] for n in d3 if dest_fn(n) == sign])
    modes, sds = [], []
    for _, lo, hi in bands:
        x = ys[:, lo:hi].flatten()
        kde = np.exp(-0.5 * ((grid[:, None] - x[None, :]) / 0.35) ** 2).sum(1)
        modes.append(grid[kde.argmax()]); sds.append(x.std())
    xs = np.arange(4)
    ax.errorbar(xs, modes, yerr=sds, fmt="o-", color=color, capsize=4, lw=1.6, ms=6, label=lab)
    dest_lv = float((((Br if sign > 0 else Ar).mean(0) - mid) * sign)[30:40].mean())
    orig_lv = float((((Ar if sign > 0 else Br).mean(0) - mid) * sign)[30:40].mean())
    ax.axhline(dest_lv, color=color, lw=1.0, ls=":", alpha=0.8)
    ax.axhline(orig_lv, color=color, lw=1.0, ls="--", alpha=0.5)
ax.axhline(0, color=MUT, lw=0.8)
ax.set_xticks(range(4)); ax.set_xticklabels([b[0] for b in bands])
ax.set_ylabel("mode of the reading distribution\n(midpoint-referenced, signed toward the destination)", fontsize=9, color=INK)
ax.set_xlabel("post-shift sentences", fontsize=9, color=MUT)
ax.legend(fontsize=8.5)
ax.set_title("Tank task, ' tank' site: mode of the reading distribution by post-shift band (bars: ± 1 sd)\n"
             "dotted = destination reference, dashed = origin reference; aquarium → vehicle stays at the midpoint",
             fontsize=9.5, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "fig_r2_mode_track.png", dpi=150)
plt.close(fig)

# ---- 6a d' profile ----
A, B, v, m = prof40
projA, projB = A @ v, B @ v
sep = projB.mean(0) - projA.mean(0)
sd = np.sqrt((projA.std(0) ** 2 + projB.std(0) ** 2) / 2) + 1e-9
dpr = sep / sd
toks = ["What", "is", "the", "meaning", "of", "the", "word", "tank", "?"]
fig, ax = plt.subplots(figsize=(8.0, 4.0), facecolor=SURFACE)
ctx_med = float(np.median(dpr[:m - 9]))
xs = np.arange(9)
colors = [ORANGE if t == "tank" else BLUE for t in toks]
ax.bar(xs, dpr[m - 9:], color=colors, width=0.62)
for i in range(9):
    ax.text(i, dpr[m - 9 + i] + 0.15, f"sd\n{sd[m - 9 + i]:.0f}", ha="center", va="bottom",
            fontsize=6, color=MUT)
ax.axhline(ctx_med, color=MUT, lw=1.2, ls="--", label=f"context-token median d′ ({ctx_med:.1f})")
ax.set_xticks(xs); ax.set_xticklabels(toks, fontsize=9)
ax.set_ylabel("class-signal d′ (identity-matched tokens)", fontsize=9, color=INK)
ax.legend(fontsize=8.5)
ax.set_title("Tank task: class signal at each carrier token\n(layer 4, forty-sentence no-shift windows, 6 runs per class)",
             fontsize=10, color=INK)
ax.text(0.01, -0.22, "d′ = mean difference / pooled sd (printed above bars): tight within-class sd prints tall bars at modest\n"
        "mean shifts — orderings among non-peak bars are not interpretable at 6 runs per class; d′ 11.7 = complete\n"
        "separation at this n, an unstable point estimate.", transform=ax.transAxes, fontsize=6.5, color=MUT)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "fig_r2_carrier_dprime.png", dpi=150)
print("figures written: fig_r2_within_stream.png, fig_r2_mode_track.png, fig_r2_carrier_dprime.png")
