#!/usr/bin/env python3
"""R1 figures: per-run model-fit gallery (tank) + cross-probe residual-gap chart."""
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from second_pass_r1_dynamics import (tank_cfg, fr_cfg, classify, integrator_pred,
                                     fit_integrator, fit_step, fit_hybrid, K)

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")

def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=7)
    ax.grid(True, lw=0.4, color="#e8e8e4")

# ---------- gallery: tank, 24 runs ----------
tag, d4a, d4b, d3, dest_fn, fam_fn = tank_cfg()
A = np.stack(d4a); B = np.stack(d4b)
mid = (A.mean(0) + B.mean(0)) / 2.0
band = slice(10, 40)
Ap = float((B.mean(0) - mid)[band].mean()); Am = float((mid - A.mean(0))[band].mean())

fig, axes = plt.subplots(4, 6, figsize=(15, 9), facecolor=SURFACE)
for ax, (name, proj) in zip(axes.flat, sorted(d3.items())):
    dest = dest_fn(name)
    y = ((proj - mid) * dest)[20:40]
    label, bics, delta, g, s, _ = classify(y, Ap, Am)
    _, gi = fit_integrator(y, Ap, Am)
    _, (c, a, b) = fit_step(y)
    _, (ch, *beta) = fit_hybrid(y)
    Xd = np.column_stack([np.ones(20), K, (K >= ch).astype(float)])
    ax.plot(K, y, "o-", color=INK, ms=2.5, lw=0.9, label="observed")
    ax.plot(K, integrator_pred(gi, Ap, Am), color=BLUE, lw=1.1, label=f"integrator γ={gi:.2f}")
    ax.plot(K, np.where(K < c, a, b), color=ORANGE, lw=1.1, label=f"step c={c}")
    ax.plot(K, Xd @ np.array(beta), color=AQUA, lw=1.1, label=f"hybrid c={ch}")
    ax.plot(K, integrator_pred(1.0, Ap, Am), color=MUT, lw=0.8, ls="--", label="uniform null")
    ax.set_title(f"{name.replace('tank_d3_','')}  →{label} (ΔBIC {delta:.1f})",
                 fontsize=7.5, color=INK)
    style(ax); ax.set_ylim(-2.6, 2.9)
axes.flat[0].legend(fontsize=5.5, loc="upper left", framealpha=0.9)
fig.suptitle("Tank L4 per-run model selection — destination-oriented midref readings, post-shift k=1..20",
             fontsize=11, color=INK)
fig.text(0.01, 0.005, "Item 1b/13a: BIC over {integrator, step, drift+step}; ΔBIC<2 → indeterminate. "
         "Axis units: single-sentence-endpoint calibration (±1), midpoint-referenced.",
         fontsize=7, color=MUT)
fig.tight_layout(rect=[0, 0.02, 1, 0.97])
fig.savefig(FIG / "fig_r1_fit_gallery_tank.png", dpi=150)
plt.close(fig)

# ---------- residual gap chart ----------
gap_rows = []
for cfg, probe in ((tank_cfg, "tank L4"), (fr_cfg, "fr S1 L14")):
    tag, d4a, d4b, d3, dest_fn, fam_fn = cfg()
    A = np.stack(d4a); B = np.stack(d4b)
    mid = (A.mean(0) + B.mean(0)) / 2.0
    band = slice(10, 40)
    amp = float((B.mean(0) - mid)[band].mean())
    for name, proj in sorted(d3.items()):
        dest = dest_fn(name)
        y = ((proj - mid) * dest)[20:40]
        Dmat = (B if dest > 0 else A)
        A_dest_t = float(((Dmat.mean(0) - mid) * dest)[35:40].mean())
        gap_rows.append({"probe": probe, "dir": "→+" if dest > 0 else "→−",
                         "fam": fam_fn(name), "gap": A_dest_t - y[15:20].mean(),
                         "gap_norm": (A_dest_t - y[15:20].mean()) / amp})
gdf = pd.DataFrame(gap_rows)
fig, axs = plt.subplots(1, 2, figsize=(9.5, 4), facecolor=SURFACE)
rng = np.random.default_rng(3)
for ax, col, ttl in ((axs[0], "gap", "residual gap (calibration units)"),
                     (axs[1], "gap_norm", "gap / D4 amplitude (normalized)")):
    cells = [(p, d) for p in ("tank L4", "fr S1 L14") for d in ("→+", "→−")]
    for i, (p, d) in enumerate(cells):
        sub = gdf[(gdf.probe == p) & (gdf["dir"] == d)]
        fams = sub.groupby("fam")[col].mean()
        boots = [fams.sample(len(fams), replace=True, random_state=int(rng.integers(1e9))).mean()
                 for _ in range(2000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        color = BLUE if p.startswith("tank") else ORANGE
        ax.scatter(np.full(len(sub), i) + rng.normal(0, 0.05, len(sub)), sub[col],
                   s=12, color=color, alpha=0.45, zorder=2)
        ax.errorbar([i], [sub[col].mean()], yerr=[[sub[col].mean() - lo], [hi - sub[col].mean()]],
                    fmt="D", color=INK, ms=5, capsize=4, lw=1.4, zorder=3)
    ax.axhline(0, color=MUT, lw=0.8, ls="--")
    ax.set_xticks(range(4)); ax.set_xticklabels([f"{p.split()[0]}\n{d}" for p, d in cells], fontsize=8)
    ax.set_title(ttl, fontsize=9.5, color=INK)
    style(ax)
fig.suptitle("Item 10b/c — plateau falls short of matched-position no-shift level (family-boot 95% CI)",
             fontsize=10.5, color=INK)
fig.text(0.01, 0.005, "gap = D4 destination level (positions 36–40, midref) − run plateau (k=16–20). "
         "Sharper-endpoint probe (tank, amp 2.0) shows larger normalized gaps than fr (amp 0.9).\n"
         "CIs shown hold D4 references fixed; with reference uncertainty propagated (QA C5), "
         "fr→fictional widens to [−0.12,+0.79] and no longer excludes zero; other cells robust.",
         fontsize=7, color=MUT)
fig.tight_layout(rect=[0, 0.03, 1, 0.94])
fig.savefig(FIG / "fig_r1_residual_gap.png", dpi=150)
print("figures written:", FIG / "fig_r1_fit_gallery_tank.png", FIG / "fig_r1_residual_gap.png")
