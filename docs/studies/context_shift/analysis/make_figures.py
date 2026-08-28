#!/usr/bin/env python3
"""Figure suite — metastable-states study (tank arm + calibrations).

One command regenerates every figure into analysis/figures/. Style: light surface
#fcfcfb, validated categorical pair blue #2a78d6 / orange #eb6834 (+ aqua #1baf7a,
yellow #eda100 where needed), thin marks, recessive grids, no dual axes.
Diverging map for heatmaps: blue -> neutral -> orange (two hues + neutral mid).
"""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import numpy as np
import pandas as pd

OUT = Path("docs/studies/context_shift/analysis/figures")
SURFACE, INK, INK2, GRID = "#fcfcfb", "#26261F", "#6b6b66", "#e8e8e4"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
DIV = LinearSegmentedColormap.from_list("aqvh", [BLUE, "#f4f4f2", ORANGE])
LOG = "docs/studies/context_shift/captures/tank_d3_d4_log.tsv"
AXES = "docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"
BOUNDARY = 20


def style(ax, ylab="", xlab=""):
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#c9c8c0")
    ax.tick_params(colors=INK2, labelsize=8)
    if ylab: ax.set_ylabel(ylab, fontsize=9, color="#3d3d3a")
    if xlab: ax.set_xlabel(xlab, fontsize=9, color="#3d3d3a")


def savefig(fig, name, title=None):
    if title:
        fig.suptitle(title, fontsize=11, color=INK, x=0.01, ha="left")
    fig.patch.set_facecolor(SURFACE)
    fig.tight_layout(rect=(0, 0.01, 1, 0.95))
    fig.savefig(OUT / name, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print("saved", name)


def load_traj(layer=4, position=1):
    """{(kind, dir): {run: (pos, proj)}} at the carrier site."""
    ax = np.load(AXES)
    A, M, D = ax[f"axis_{layer}"], ax[f"mid_{layer}"], float(ax[f"denom_{layer}"])
    log = pd.read_csv(LOG, sep="\t")
    out = {}
    for _, r in log.iterrows():
        kind = "d3" if "_d3_" in r["run"] else "d4"
        d = ("ab" if r["run"].endswith("_ab") else "ba") if kind == "d3" else \
            ("aq" if r["run"].endswith("_a") else "vh")
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == layer) & (res["token_position"] == position)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - M) @ A) / D
        out.setdefault((kind, d), {})[r["run"]] = (df["pos"].to_numpy(), proj)
    return out


def fig_trajectories_null(traj):
    """Flagship: D3 means + bands, D4 controls, integrator null."""
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    null_amp = {"ab": (1.93, 2.06), "ba": (2.06, 1.93)}
    for ax, d, col in ((axs[0], "ab", BLUE), (axs[1], "ba", ORANGE)):
        runs = traj[("d3", d)]
        arr = np.stack([p for _, p in runs.values()])
        m, s = arr.mean(0), arr.std(0)
        x = np.arange(1, 41)
        ax.plot(x, m, color=col, lw=2, zorder=4, label="transition mean")
        ax.fill_between(x, m - s, m + s, color=col, alpha=0.15, lw=0, zorder=2)
        # D4 controls
        for dd, c2, lbl in (("aq", "#9db9d8", "no-shift aquarium"), ("vh", "#e8b39b", "no-shift vehicle")):
            a2 = np.stack([p for _, p in traj[("d4", dd)].values()]).mean(0)
            ax.plot(x, a2, color=c2, lw=1.4, ls=":", zorder=3, label=lbl)
        # integrator null (per-direction amplitudes), post-shift
        src, dst = null_amp[d]
        sgn = (-1, +1) if d == "ab" else (+1, -1)
        k = np.arange(1, 21)
        null = (20 * sgn[0] * src + k * sgn[1] * dst) / (20 + k)
        ax.plot(np.arange(21, 41), null, color=INK2, lw=1.4, ls="--", zorder=3,
                label="uniform-integrator null")
        ax.axvline(BOUNDARY + 0.5, color="#8a8a85", lw=1, ls="--")
        ax.axhline(0, color="#c9c8c0", lw=0.8)
        style(ax, "reading (aq = −, vh = +)" if d == "ab" else "", "sentence position (shift after 20)")
        ax.set_title(f"{'aquarium → vehicle' if d=='ab' else 'vehicle → aquarium'}",
                     fontsize=10, color=INK, loc="left")
    axs[0].legend(fontsize=7.5, frameon=False, loc="lower right")
    savefig(fig, "traj_null_L4.png",
            "Transition readings vs no-shift controls and the integrator null — L4, carrier site")


def fig_spaghetti(traj):
    """Run-level heterogeneity: drifts and jumps."""
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.0), sharey=True)
    for ax, d, col in ((axs[0], "ab", BLUE), (axs[1], "ba", ORANGE)):
        x = np.arange(1, 41)
        for _, (pos, p) in traj[("d3", d)].items():
            ax.plot(x, p, color=INK2, lw=0.8, alpha=0.35, zorder=2)
        arr = np.stack([p for _, p in traj[("d3", d)].values()])
        ax.plot(x, arr.mean(0), color=col, lw=2.2, zorder=4)
        ax.axvline(BOUNDARY + 0.5, color="#8a8a85", lw=1, ls="--")
        ax.axhline(0, color="#c9c8c0", lw=0.8)
        style(ax, "reading" if d == "ab" else "", "sentence position")
        ax.set_title("aquarium → vehicle" if d == "ab" else "vehicle → aquarium",
                     fontsize=10, color=INK, loc="left")
    savefig(fig, "spaghetti_L4.png",
            "Individual transition paths (12 scene families each) — drifts and single-step jumps")


def fig_occupancy(traj):
    """Time-banded occupancy histograms with rule-(b) band shading."""
    band = (-1.516, 1.213)  # rule (b), position-matched D4 endpoints, L4
    bands = [("t1–5", 1, 5), ("t6–10", 6, 10), ("t11–15", 11, 15), ("t16–20", 16, 20)]
    fig, axs = plt.subplots(2, 4, figsize=(12, 4.6), sharex=True, sharey=True)
    edges = np.linspace(-3.2, 3.2, 33)
    for row, (d, col) in enumerate((("ab", BLUE), ("ba", ORANGE))):
        vals = {}
        for _, (pos, p) in traj[("d3", d)].items():
            for pp, v in zip(pos, p):
                if pp > BOUNDARY:
                    vals.setdefault(pp - BOUNDARY, []).append(v)
        for ci, (lbl, lo, hi) in enumerate(bands):
            ax = axs[row, ci]
            data = np.concatenate([vals[t] for t in range(lo, hi + 1)])
            ax.axvspan(*band, color="#f1efe9", zorder=0)
            ax.hist(data, bins=edges, color=col, alpha=0.85, zorder=2)
            ax.axvline(0, color="#c9c8c0", lw=0.8)
            style(ax)
            if row == 0:
                ax.set_title(lbl, fontsize=9, color=INK)
            if ci == 0:
                ax.set_ylabel("aq → vh count" if row == 0 else "vh → aq count",
                              fontsize=8, color="#3d3d3a")
    for ax in axs[1]:
        ax.set_xlabel("reading", fontsize=8, color="#3d3d3a")
    savefig(fig, "occupancy_bands_L4.png",
            "Post-shift occupancy by time-since-shift — unimodal at every band; shaded = unresolved band (rule b)")


def fig_heatmap():
    """Layer x position reading heatmap, direction means."""
    ax_np = np.load(AXES)
    log = pd.read_csv(LOG, sep="\t")
    layers = list(range(24))
    grids = {"ab": [], "ba": []}
    for _, r in log.iterrows():
        if "_d3_" not in r["run"]:
            continue
        d = "ab" if r["run"].endswith("_ab") else "ba"
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[res["token_position"] == 1]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        g = np.full((24, 40), np.nan)
        for L in layers:
            sub = df[df["layer"] == L].sort_values("pos")
            X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            proj = 2.0 * ((X - ax_np[f"mid_{L}"]) @ ax_np[f"axis_{L}"]) / float(ax_np[f"denom_{L}"])
            g[L, sub["pos"].to_numpy() - 1] = proj
        grids[d].append(g)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.2), sharey=True)
    for ax, d in ((axs[0], "ab"), (axs[1], "ba")):
        G = np.nanmean(np.stack(grids[d]), axis=0)
        im = ax.imshow(G, aspect="auto", origin="lower", cmap=DIV,
                       norm=TwoSlopeNorm(vcenter=0, vmin=-2.6, vmax=2.6),
                       extent=(0.5, 40.5, -0.5, 23.5))
        ax.axvline(BOUNDARY + 0.5, color=INK, lw=1, ls="--")
        style(ax, "layer" if d == "ab" else "", "sentence position")
        ax.grid(False)
        ax.set_title("aquarium → vehicle" if d == "ab" else "vehicle → aquarium",
                     fontsize=10, color=INK, loc="left")
    cb = fig.colorbar(im, ax=axs, shrink=0.85, pad=0.015)
    cb.set_label("reading (aq − / vh +)", fontsize=8, color="#3d3d3a")
    cb.ax.tick_params(labelsize=7, colors=INK2)
    fig.suptitle("Depth × position: where the new reading forms — direction means, per-layer axes",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.patch.set_facecolor(SURFACE)
    fig.savefig(OUT / "heatmap_layer_position.png", dpi=200, facecolor=SURFACE,
                bbox_inches="tight")
    plt.close(fig)
    print("saved heatmap_layer_position.png")


def fig_calibration_layers():
    """Scene-held-out accuracy per layer, three axes."""
    import subprocess
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    runs = [("session_29a80932", "aquarium", "vehicle", 1, "tank (aq/vh), tank site", BLUE),
            ("session_5247081b", "fictional", "real", 1, "fiction/real, want site", ORANGE),
            ("session_5247081b", "fictional", "real", 8, "fiction/real, letter site", AQUA)]
    for sid, a, b, pos, lbl, col in runs:
        r = subprocess.run([".venv/bin/python",
                            "docs/studies/context_shift/analysis/scene_heldout_calibration.py",
                            sid, a, b, "--position", str(pos)],
                           capture_output=True, text=True)
        xs, ys = [], []
        for line in r.stdout.splitlines():
            p = line.split()
            if len(p) >= 3 and p[0].isdigit() and p[1].replace(".", "").isdigit() and "." in p[1]:
                xs.append(int(p[0])); ys.append(float(p[1]))
        ax.plot(xs, ys, color=col, lw=2, label=lbl)
    ax.axhline(0.5, color="#c9c8c0", lw=0.8, ls=":")
    ax.set_ylim(0.45, 1.0)
    style(ax, "scene-held-out accuracy", "layer")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    savefig(fig, "calibration_layers.png",
            "Endpoint separability by depth (leave-one-scene-pair-out)")


def fig_norm_cosine(traj):
    ax_np = np.load(AXES)
    u = ax_np["axis_4"] / np.sqrt(float(ax_np["denom_4"]))
    log = pd.read_csv(LOG, sep="\t")
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.6))
    for suffix, lab, col in (("_a", "aquarium-only", BLUE), ("_b", "vehicle-only", ORANGE)):
        norms, cosines = {}, {}
        for _, r in log.iterrows():
            if "_d4_" not in r["run"] or not r["run"].endswith(suffix):
                continue
            lake = Path("data/lake") / r["session"]
            res = pd.read_parquet(lake / "residual_streams.parquet")
            res = res[(res["layer"] == 4) & (res["token_position"] == 1)]
            tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
            tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
            df = res.merge(tok, on="probe_id")
            X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            c = X - ax_np["mid_4"]
            for p_, x, cc in zip(df["pos"], X, c):
                norms.setdefault(p_, []).append(float(np.linalg.norm(x)))
                cosines.setdefault(p_, []).append(abs(float(cc @ u / np.linalg.norm(cc))))
        xs = sorted(norms)
        axs[0].plot(xs, [np.mean(norms[p]) for p in xs], color=col, lw=2, label=lab)
        axs[1].plot(xs, [np.mean(cosines[p]) for p in xs], color=col, lw=2, label=lab)
    style(axs[0], "‖state‖", "sentence position"); axs[0].set_ylim(0, 450)
    style(axs[1], "|cos(state − mid, axis)|", "sentence position"); axs[1].set_ylim(0, 0.8)
    axs[0].set_title("norms stay flat", fontsize=9, color=INK, loc="left")
    axs[1].set_title("alignment grows", fontsize=9, color=INK, loc="left")
    axs[1].legend(fontsize=8, frameon=False, loc="lower right")
    savefig(fig, "norm_vs_alignment.png",
            "Accumulation deepens commitment by rotation, not scale — no-shift arms, L4")


def fig_jumpiness(traj):
    rows = []
    import itertools
    for run, (pos, p) in itertools.chain(traj[("d3", "ab")].items(), traj[("d3", "ba")].items()):
        post = p[pos >= 20]
        pre = p[(pos >= 5) & (pos <= 19)]
        rows.append((run, float(np.abs(np.diff(post)).max()),
                     abs(float(post[-1] - post[0])),
                     float(np.std(np.diff(pre)))))
    df = pd.DataFrame(rows, columns=["run", "max_d", "travel", "noise"]).sort_values("max_d")
    frac = (df["max_d"] / df["travel"]).to_numpy()
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    cols = [ORANGE if f > 0.5 else BLUE for f in np.sort(frac)]
    ax.bar(range(len(frac)), np.sort(frac), color=cols, width=0.72)
    ax.axhline(0.5, color=INK2, lw=1, ls="--")
    ax.text(0.3, 0.52, "jump-dominant threshold", fontsize=7.5, color=INK2)
    style(ax, "largest single step ÷ total travel", "runs (sorted)")
    ax.set_xticks([])
    savefig(fig, "jumpiness.png",
            "Run-level path character: 8 of 24 transitions are jump-dominant")


def fig_prelexical():
    AX8 = np.load("docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos8.npz")
    log = pd.read_csv(LOG, sep="\t")
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    series = [("d3", "_ab", "transition aq→vh", BLUE, "-"),
              ("d3", "_ba", "transition vh→aq", ORANGE, "-"),
              ("d4", "_a", "no-shift aquarium", "#9db9d8", ":"),
              ("d4", "_b", "no-shift vehicle", "#e8b39b", ":")]
    for kind, suf, lbl, col, ls in series:
        curves = []
        for _, r in log.iterrows():
            if f"_{kind}_" not in r["run"] or not r["run"].endswith(suf):
                continue
            lake = Path("data/lake") / r["session"]
            res = pd.read_parquet(lake / "residual_streams.parquet")
            res = res[(res["layer"] == 4) & (res["token_position"] == 8)]
            tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
            tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
            df = res.merge(tok, on="probe_id").sort_values("pos")
            X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            curves.append(2.0 * ((X - AX8["mid_4"]) @ AX8["axis_4"]) / float(AX8["denom_4"]))
        ax.plot(np.arange(1, 41), np.stack(curves).mean(0), color=col, lw=2, ls=ls, label=lbl)
    ax.axvline(BOUNDARY + 0.5, color="#8a8a85", lw=1, ls="--")
    ax.axhline(0, color="#c9c8c0", lw=0.8)
    style(ax, "pre-lexical reading (` word` site)", "sentence position")
    ax.legend(fontsize=8, frameon=False, loc="center right")
    savefig(fig, "prelexical_L4.png",
            "Context signal before the word appears — note the aquarium/vehicle saturation asymmetry")


def main():
    OUT.mkdir(exist_ok=True)
    traj = load_traj()
    fig_trajectories_null(traj)
    fig_spaghetti(traj)
    fig_occupancy(traj)
    fig_norm_cosine(traj)
    fig_jumpiness(traj)
    fig_prelexical()
    fig_heatmap()
    fig_calibration_layers()


if __name__ == "__main__":
    main()


def fig_fr_heatmap():
    """Fiction/real want-site reading, all 24 layers x 40 positions.
    Top row: transitions (direction means, S1 both sub-arms).
    Bottom row: no-shift arms — where the fictional-erosion story lives per layer."""
    AXF = np.load("docs/studies/context_shift/analysis/axes/axes_session_5247081b_fictional_vs_real_pos1.npz")
    log = pd.read_csv("docs/studies/context_shift/captures/fr_d3_d4_log.tsv", sep="\t")
    panels = {"fr": [], "rf": [], "d4f": [], "d4r": []}
    for _, r in log.iterrows():
        n = r["run"]
        if "_s1_" not in n:
            continue
        if "_d3_" in n:
            key = "fr" if n.endswith("_fr") else "rf"
        elif "_d4_" in n:
            key = "d4f" if n.endswith("_f") else "d4r"
        else:
            continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[res["token_position"] == 1]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        g = np.full((24, 40), np.nan)
        for L in range(24):
            sub = df[df["layer"] == L].sort_values("pos")
            X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            proj = 2.0 * ((X - AXF[f"mid_{L}"]) @ AXF[f"axis_{L}"]) / float(AXF[f"denom_{L}"])
            g[L, sub["pos"].to_numpy() - 1] = proj
        panels[key].append(g)
    titles = {"fr": "fictional → real", "rf": "real → fictional",
              "d4f": "no-shift fictional (erosion)", "d4r": "no-shift real (durable)"}
    fig, axs = plt.subplots(2, 2, figsize=(11.5, 7.6), sharey=True)
    order = [("fr", axs[0, 0]), ("rf", axs[0, 1]), ("d4f", axs[1, 0]), ("d4r", axs[1, 1])]
    for key, ax in order:
        G = np.nanmean(np.stack(panels[key]), axis=0)
        im = ax.imshow(G, aspect="auto", origin="lower", cmap=DIV,
                       norm=TwoSlopeNorm(vcenter=0, vmin=-2.4, vmax=2.4),
                       extent=(0.5, 40.5, -0.5, 23.5))
        if key in ("fr", "rf"):
            ax.axvline(BOUNDARY + 0.5, color=INK, lw=1, ls="--")
        style(ax, "layer" if key in ("fr", "d4f") else "",
              "sentence position" if key in ("d4f", "d4r") else "")
        ax.grid(False)
        ax.set_title(titles[key], fontsize=10, color=INK, loc="left")
    cb = fig.colorbar(im, ax=axs, shrink=0.8, pad=0.015)
    cb.set_label("reading (fictional − / real +)", fontsize=8, color="#3d3d3a")
    cb.ax.tick_params(labelsize=7, colors=INK2)
    fig.suptitle("Fiction/real ` want` site across all layers — transitions (top) and no-shift arms (bottom)",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.patch.set_facecolor(SURFACE)
    fig.savefig(OUT / "fr_heatmap_layer_position.png", dpi=200, facecolor=SURFACE,
                bbox_inches="tight")
    plt.close(fig)
    print("saved fr_heatmap_layer_position.png")
