#!/usr/bin/env python3
"""Suicide-arm battery: trajectories, integrator null, jumpiness, occupancy,
sub-arm and carrier comparisons. S1 axes (want site), L14 primary (calibration
peak). Convention: fictional = -1, real = +1. Figures per standing practice.
"""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import diptest

L = 14
AX = np.load("docs/studies/context_shift/analysis/axes/axes_session_5247081b_fictional_vs_real_pos1.npz")
axis, mid, denom = AX[f"axis_{L}"], AX[f"mid_{L}"], float(AX[f"denom_{L}"])
LOG = pd.read_csv("docs/studies/context_shift/captures/fr_d3_d4_log.tsv", sep="\t")
OUT = Path("docs/studies/context_shift/analysis/figures")
SURFACE, INK, INK2, GRID = "#fcfcfb", "#26261F", "#6b6b66", "#e8e8e4"
BLUE, ORANGE = "#2a78d6", "#eb6834"

def load(sid):
    lake = Path("data/lake") / sid
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] == 1)]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
    tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
    df = res.merge(tok, on="probe_id").sort_values("pos")
    X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    return df["pos"].to_numpy(), 2.0 * ((X - mid) @ axis) / denom

def style(ax, ylab="", xlab=""):
    ax.set_facecolor(SURFACE); ax.grid(axis="y", color=GRID, lw=0.5); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color("#c9c8c0")
    ax.tick_params(colors=INK2, labelsize=8)
    if ylab: ax.set_ylabel(ylab, fontsize=9, color="#3d3d3a")
    if xlab: ax.set_xlabel(xlab, fontsize=9, color="#3d3d3a")

# ---- load all runs, keyed ----
runs = {}
for _, r in LOG.iterrows():
    runs[r["run"]] = load(r["session"])

# D4 plateaus (S1 theme)
plat = {"f": [], "r": []}
for name, (pos, p) in runs.items():
    if "_d4_" in name:
        plat["f" if name.endswith("_f") else "r"].extend(p[pos >= 11].tolist())
F_amp, R_amp = abs(np.mean(plat["f"])), abs(np.mean(plat["r"]))
print(f"D4 plateaus (S1 theme): fictional {np.mean(plat['f']):+.2f}, real {np.mean(plat['r']):+.2f}")

# trajectory aggregates: S1, direction x sub_arm
groups = {}
for name, (pos, p) in runs.items():
    if "_s1_" not in name or "_d3_" not in name: continue
    sub = "th" if "_th_" in name else "ar"
    d = "fr" if name.endswith("_fr") else "rf"
    groups.setdefault((d, sub), []).append(p)
print("\n== S1 trajectory band means (destination side +) ==")
tab = []
for (d, sub), cs in sorted(groups.items()):
    arr = np.stack(cs); m = arr.mean(0)
    tab.append((d, sub, len(cs), m[0], m[19], m[24], m[29], m[39]))
    print(f"  {d}/{sub} (n={len(cs)}): p1={m[0]:+.2f} p20={m[19]:+.2f} p25={m[24]:+.2f} p30={m[29]:+.2f} p40={m[39]:+.2f}")

# integrator null check (theme arm)
print("\n== vs uniform-integrator null (per-class amplitudes) ==")
for d in ("fr", "rf"):
    arr = np.stack(groups[(d, "th")]); m = arr.mean(0)
    src, dst = (F_amp, R_amp) if d == "fr" else (R_amp, F_amp)
    sgn_src, sgn_dst = (-1, +1) if d == "fr" else (+1, -1)
    ahead = 0
    for k in (5, 10, 15, 20):
        null = (20 * sgn_src * src + k * sgn_dst * dst) / (20 + k)
        obs = m[19 + k]
        ok = obs > null if d == "fr" else obs < null
        ahead += ok
        print(f"  {d} t={k}: obs={obs:+.2f} null={null:+.2f} ahead={'Y' if ok else 'N'}")

# jumpiness + occupancy (S1 both sub-arms)
jump = 0; tot = 0; occ = {"fr": [], "rf": []}
for name, (pos, p) in runs.items():
    if "_s1_" not in name or "_d3_" not in name: continue
    d = "fr" if name.endswith("_fr") else "rf"
    post = p[pos >= 20]; tot += 1
    if np.abs(np.diff(post)).max() > 0.5 * abs(post[-1] - post[0]): jump += 1
    for pp, v in zip(pos, p):
        if pp > 20: occ[d].append(v)
print(f"\njump-dominant runs: {jump}/{tot}")
for d in ("fr", "rf"):
    x = np.array(occ[d]); dip, pv = diptest.diptest(x)
    print(f"occupancy {d}: n={len(x)} dip p={pv:.3f}")

# cross-carrier agreement (families 0-3, theme, S1 vs S2 vs S3)
print("\n== carrier agreement (fam 0-3, theme, mean trajectories r) ==")
# STRUCTURAL RULE (after catching a cross-token trap in this very script): every
# projection uses the axis calibrated at ITS carrier's own site. S2 site = ` like`,
# S3 site = ` letter`; projecting them on the S1 (` want`) axis produced a spurious
# r = -0.6 before this fix.
CAX = {"s2": np.load("docs/studies/context_shift/analysis/axes/axes_session_589557e1_fictional_vs_real_pos1.npz"),
       "s3": np.load("docs/studies/context_shift/analysis/axes/axes_session_c913da46_fictional_vs_real_pos1.npz")}

def carrier_mean(cid, d):
    cs = []
    for _, rr in LOG.iterrows():
        name = rr["run"]
        if f"_{cid}_" in name and "_d3_" in name and "_th_" in name                 and name.endswith("_" + d) and int(name.split("fam")[1][:2]) < 4:
            if cid == "s1":
                cs.append(runs[name][1])
            else:
                ax = CAX[cid]
                lake = Path("data/lake") / rr["session"]
                res = pd.read_parquet(lake / "residual_streams.parquet")
                res = res[(res["layer"] == L) & (res["token_position"] == 1)]
                tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
                tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
                df = res.merge(tok, on="probe_id").sort_values("pos")
                X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
                cs.append(2.0 * ((X - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"]))
    return np.stack(cs).mean(0) if cs else None
for d in ("fr", "rf"):
    s1 = carrier_mean("s1", d)
    for cid in ("s2", "s3"):
        other = carrier_mean(cid, d)
        r = np.corrcoef(s1, other)[0, 1]
        print(f"  {d}: S1 vs {cid.upper()} r = {r:.3f}")

# ---- figures ----
fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
for ax, d, col in ((axs[0], "fr", BLUE), (axs[1], "rf", ORANGE)):
    x = np.arange(1, 41)
    for sub, ls, lbl in (("th", "-", "theme-only"), ("ar", "--", "artifact-mentioned")):
        arr = np.stack(groups[(d, sub)])
        ax.plot(x, arr.mean(0), color=col, lw=2, ls=ls, label=lbl, zorder=4)
        ax.fill_between(x, arr.mean(0) - arr.std(0), arr.mean(0) + arr.std(0),
                        color=col, alpha=0.10, lw=0, zorder=2)
    for k, c2, lbl in (("f", "#9db9d8", "no-shift fictional"), ("r", "#e8b39b", "no-shift real")):
        a2 = np.stack([p for n, (pos, p) in runs.items()
                       if "_d4_" in n and n.endswith("_" + k)]).mean(0)
        ax.plot(x, a2, color=c2, lw=1.4, ls=":", zorder=3, label=lbl)
    src, dst = (F_amp, R_amp) if d == "fr" else (R_amp, F_amp)
    sgn = (-1, +1) if d == "fr" else (+1, -1)
    kk = np.arange(1, 21)
    null = (20 * sgn[0] * src + kk * sgn[1] * dst) / (20 + kk)
    ax.plot(np.arange(21, 41), null, color=INK2, lw=1.4, ls="--", label="integrator null", zorder=3)
    ax.axvline(20.5, color="#8a8a85", lw=1, ls="--"); ax.axhline(0, color="#c9c8c0", lw=0.8)
    style(ax, "reading (fic = −, real = +)" if d == "fr" else "", "sentence position (shift after 20)")
    ax.set_title("fictional → real" if d == "fr" else "real → fictional", fontsize=10, color=INK, loc="left")
axs[0].legend(fontsize=7, frameon=False, loc="lower right")
fig.suptitle("Fiction/real transitions (S1 want site, L14) — sub-arms, controls, integrator null",
             fontsize=11, color=INK, x=0.01, ha="left")
fig.patch.set_facecolor(SURFACE); fig.tight_layout(rect=(0, 0.01, 1, 0.94))
fig.savefig(OUT / "fr_traj_null_L14.png", dpi=200, facecolor=SURFACE)
print("\nsaved fr_traj_null_L14.png")
