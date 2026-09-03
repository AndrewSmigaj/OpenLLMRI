#!/usr/bin/env python3
"""D6 mixture-sweep analysis — the briefing's reserved stickiness measurement.

For each family x k x order cell (single capture, carrier reading, midref units):
  curve_recentB(k) = reading when the k destination sentences are the RECENT block
  curve_recentA(k) = reading when they are the OLD block
Hysteresis loop = area between the curves over k (signed, recentB - recentA).
STICKINESS = observed loop area MINUS the loop area of the best-fitting one-parameter
recency integrator — the reserved definition. PRIMARY NULL (verdict-bearing): gamma AND
amplitude fit jointly to the D6 cells themselves (see robustness block at bottom).
SECONDARY: gamma imported from the R1 D3 fits (reported, but a misspecified null —
the first run's "+3.7 tank stickiness" under it did not survive the fitted null:
tank obs +14.4 vs best-fit +14.3, fr +10.5 vs +11.1 — NO measurable stickiness;
the loops are large and real but fully attributable to recency weighting).
Interleaved k=10 cells test order-sensitivity at fixed proportion.
Run AFTER d6 chains complete (d6_{tank,fr}_log.tsv).
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
from second_pass_r1_dynamics import tank_cfg, fr_cfg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
C = Path("docs/studies/context_shift/captures")

CFG = {
    "tank": dict(log=C / "d6_tank_log.tsv", L=4, cfg=tank_cfg, gamma={"+": 0.980, "-": 0.935},
                 ax="docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"),
    "fr": dict(log=C / "d6_fr_log.tsv", L=14, cfg=fr_cfg, gamma={"+": 0.910, "-": 0.900},
               ax="docs/studies/context_shift/analysis/axes/axes_session_5247081b_fictional_vs_real_pos1.npz"),
}

def integrator_reading(gamma, k, Ap, Am, order):
    # 20 sentences total; ages: recent block age 0..; value +Ap for B, -Am for A
    if order == "B_recent":
        vals = [Ap] * k + [-Am] * (20 - k)      # ages 0..k-1 = B
    else:
        vals = [-Am] * (20 - k) + [Ap] * k      # ages 0..19-k = A first (recent)
    w = gamma ** np.arange(20)
    return float((w * np.array(vals)).sum() / w.sum())

for probe, c in CFG.items():
    if not c["log"].exists():
        print(f"{probe}: log not found — chain not complete yet"); continue
    rows = [r for r in csv.DictReader(open(c["log"]), delimiter="\t") if r["status"] == "ok"]
    ax = np.load(c["ax"]); L = c["L"]
    tag, d4a, d4b, d3, dest_fn, fam_fn = c["cfg"]()
    A = np.stack(d4a); B = np.stack(d4b)
    mid20 = float(((A.mean(0) + B.mean(0)) / 2)[19])       # position-20 midpoint
    Ap = float((B.mean(0) - (A.mean(0) + B.mean(0)) / 2)[10:40].mean())
    readings = {}
    for r in rows:
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = float(2.0 * ((X[0] - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"]))
        parts = r["set"].split("_")                        # probe d6 famXX kNN order...
        fam, k, order = parts[2], int(parts[3][1:]), "_".join(parts[4:])
        readings[(fam, k, order)] = proj - mid20
    fams = sorted({f for f, _, _ in readings})
    ks = list(range(2, 20, 2))
    up, dn, up_pred, dn_pred = [], [], [], []
    g = np.mean(list(c["gamma"].values()))
    for k in ks:
        u = [readings[(f, k, "B_recent")] for f in fams if (f, k, "B_recent") in readings]
        d_ = [readings[(f, k, "A_recent")] for f in fams if (f, k, "A_recent") in readings]
        up.append(np.mean(u)); dn.append(np.mean(d_))
        up_pred.append(integrator_reading(g, k, Ap, Ap, "B_recent"))
        dn_pred.append(integrator_reading(g, k, Ap, Ap, "A_recent"))
    up, dn = np.array(up), np.array(dn)
    obs_area = float(np.trapz(up - dn, ks))
    pred_area = float(np.trapz(np.array(up_pred) - np.array(dn_pred), ks))
    # family-clustered bootstrap on the area
    boots = []
    rng = np.random.default_rng(6)
    for b in range(2000):
        fb = rng.choice(fams, len(fams), replace=True)
        ub = [np.mean([readings[(f, k, "B_recent")] for f in fb if (f, k, "B_recent") in readings]) for k in ks]
        db = [np.mean([readings[(f, k, "A_recent")] for f in fb if (f, k, "A_recent") in readings]) for k in ks]
        boots.append(np.trapz(np.array(ub) - np.array(db), ks))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    # PRIMARY NULL: best-fit integrator with gamma AND amplitude free, fit on all cells
    cells = []
    for (f2, k2, o2), v2 in readings.items():
        if o2 in ("B_recent", "A_recent"): cells.append((k2, o2, v2))
        elif o2 == "pure_A": cells += [(0, "A_recent", v2), (0, "B_recent", v2)]
        elif o2 == "pure_B": cells += [(20, "A_recent", v2), (20, "B_recent", v2)]
    bestfit = (np.inf, None)
    for g2 in np.arange(0.60, 1.001, 0.005):
        for amp2 in np.arange(0.5, 3.01, 0.05):
            rss = sum((v2 - integrator_reading(g2, k2, amp2, amp2, o2)) ** 2 for k2, o2, v2 in cells)
            if rss < bestfit[0]: bestfit = (rss, (g2, amp2))
    gf, ampf = bestfit[1]
    fit_area = float(np.trapz([integrator_reading(gf, k2, ampf, ampf, "B_recent")
                               - integrator_reading(gf, k2, ampf, ampf, "A_recent") for k2 in ks], ks))
    stick = obs_area - fit_area
    verdict = "SIGNIFICANT" if lo > fit_area else "ns"
    print(f"  PRIMARY (fitted null g={gf:.3f} amp={ampf:.2f}): pred {fit_area:+.1f} -> "
          f"stickiness {stick:+.1f} ({verdict})")
    inter = [readings[(f, 10, "interleaved")] for f in fams if (f, 10, "interleaved") in readings]
    print(f"{probe}: loop area OBS {obs_area:+.1f} [boot {lo:+.1f},{hi:+.1f}] vs "
          f"integrator(g={g:.2f}) {pred_area:+.1f} -> STICKINESS {obs_area - pred_area:+.1f}")
    print(f"  interleaved k=10 mean {np.mean(inter):+.2f} vs blocked B_recent {up[ks.index(10)]:+.2f} "
          f"/ A_recent {dn[ks.index(10)]:+.2f}")
    # figure
    fig, axp = plt.subplots(figsize=(7.2, 4.6), facecolor=SURFACE)
    axp.plot(ks, up, "o-", color=ORANGE, lw=1.8, label="destination block last (observed)")
    axp.plot(ks, dn, "o-", color=BLUE, lw=1.8, label="destination block first (observed)")
    axp.plot(ks, up_pred, "--", color=ORANGE, lw=1.0, alpha=0.6, label="fitted recency integrator")
    axp.plot(ks, dn_pred, "--", color=BLUE, lw=1.0, alpha=0.6)
    axp.fill_between(ks, dn, up, color=AQUA, alpha=0.12)
    if inter: axp.scatter([10], [np.mean(inter)], marker="D", s=60, color=AQUA, zorder=5, label="interleaved, 10 of 20")
    axp.axhline(0, color=MUT, lw=0.8)
    axp.set_xlabel("destination-class sentences in the context (of 20)", fontsize=9, color=MUT)
    axp.set_ylabel("carrier reading (midpoint-referenced)", fontsize=9, color=INK)
    task_name = "Tank task" if probe == "tank" else "Fiction/real task"
    axp.set_title(f"{task_name}: hysteresis loop in the static mixture sweep\n"
                  f"observed loop area {obs_area:+.1f} [{lo:+.1f}, {hi:+.1f}]; fitted recency integrator {fit_area:+.1f}; "
                  f"excess {stick:+.1f} ({verdict})",
                  fontsize=9.5, color=INK)
    axp.legend(fontsize=8); axp.set_facecolor(SURFACE)
    for s in ("top", "right"): axp.spines[s].set_visible(False)
    axp.tick_params(colors=MUT, labelsize=8); axp.grid(True, lw=0.4, color="#e8e8e4")
    fig.tight_layout()
    fig.savefig(FIG / f"fig_r6_d6_loop_{probe}.png", dpi=150)
    print(f"  figure: fig_r6_d6_loop_{probe}.png")
