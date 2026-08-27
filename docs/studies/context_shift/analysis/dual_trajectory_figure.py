#!/usr/bin/env python3
"""Dual-trajectory figure (N3) — same transitions rendered through two instruments.

Rows: probe family (tank polysemy, fiction/real suicide-letter).
Cols: instrument (UMAP-6D lens centroid-axis projection; raw 2880-d
difference-of-means axis, this study's N1 script).

Data: chain-log paper-protocol temporal runs (harmony format only —
`polysemy_h` and `suicide` families), L23, target token (position 1).
Lens points: docs/studies/suicide_letter_polysemy/analysis/
paper_protocol_basin_points.json (committed prior script's output).
Raw points: computed here from saved N1 axes.

NOTE: these runs are PRIOR-DESIGN (word-context) data — context sentences
contain the target word. The rerun program's scene-context D3 corpus replaces
them for the paper; this figure is the instrument-comparison artifact.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path("docs/studies/context_shift/analysis")
LENS_JSON = Path("docs/studies/suicide_letter_polysemy/analysis/paper_protocol_basin_points.json")
CHAIN_TSV = Path("docs/studies/suicide_letter_polysemy/captures/paper_protocol_log.tsv")
LAYER = 23

# direction semantics: A -> B. suicide A=fictional B=real(distress); polysemy A=aquarium B=vehicle
FAMS = {
    "polysemy": dict(chain_family="polysemy_h",
                     axes=BASE / "axes/axes_session_e2be37dd_aquarium_vs_vehicle_pos1.npz",
                     lens_family="polysemy", a="aquarium", b="vehicle",
                     title="Tank polysemy (aquarium → vehicle axis)"),
    "suicide": dict(chain_family="suicide",
                    axes=BASE / "axes/axes_session_9358c2a1_fictional_vs_real_pos1.npz",
                    lens_family="suicide", a="fictional", b="real",
                    title="Fiction/real (fictional → distress axis)"),
}
DIR_COLOR = {"block_ab": "#2a78d6", "block_ba": "#eb6834"}  # validated pair, light mode
SURFACE = "#fcfcfb"


def raw_points(fam_cfg) -> pd.DataFrame:
    log = pd.read_csv(CHAIN_TSV, sep="\t")
    runs = log[(log["family"] == fam_cfg["chain_family"]) & (log["status"] == "ok")]
    data = np.load(fam_cfg["axes"])
    axis, mid, denom = data[f"axis_{LAYER}"], data[f"mid_{LAYER}"], float(data[f"denom_{LAYER}"])
    rows = []
    for _, r in runs.iterrows():
        sid = r["new_session"]
        lake = Path("data/lake") / sid
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == LAYER) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "sentence_index"])
        res = res.merge(tok, on="probe_id")
        X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - mid) @ axis) / denom
        for pos, p in zip(res["sentence_index"], proj):
            rows.append({"direction": r["dir"], "position": int(pos), "projection": float(p)})
    return pd.DataFrame(rows)


def lens_points(fam_cfg) -> pd.DataFrame:
    pts = pd.DataFrame(json.loads(LENS_JSON.read_text()))
    return pts[pts["probe_family"] == fam_cfg["lens_family"]][["direction", "position", "projection"]]


def draw(ax, df, ylab, boundary=19.5):
    for d, dfd in df.groupby("direction"):
        agg = dfd.groupby("position")["projection"].agg(["mean", "std"])
        c = DIR_COLOR[d]
        ax.plot(agg.index, agg["mean"], color=c, lw=2, zorder=3)
        ax.fill_between(agg.index, agg["mean"] - agg["std"], agg["mean"] + agg["std"],
                        color=c, alpha=0.16, lw=0, zorder=2)
    ax.axvline(boundary, color="#8a8a85", lw=1, ls="--", zorder=1)
    ax.set_ylabel(ylab, fontsize=9, color="#3d3d3a")
    ax.grid(axis="y", color="#e8e8e4", lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#c9c8c0")
    ax.tick_params(colors="#6b6b66", labelsize=8)
    ax.set_facecolor(SURFACE)


def main():
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.6), sharex=True)
    fig.patch.set_facecolor(SURFACE)
    all_agg = []
    for i, (fam, cfg) in enumerate(FAMS.items()):
        lens = lens_points(cfg)
        raw = raw_points(cfg)
        for df, tag in ((lens, "lens"), (raw, "raw")):
            a = df.groupby(["direction", "position"])["projection"].agg(["mean", "std", "count"]).reset_index()
            a["family"], a["instrument"] = fam, tag
            all_agg.append(a)
        draw(axes[i, 0], lens, f"lens axis (0={cfg['a']}, 1={cfg['b']})")
        draw(axes[i, 1], raw, f"raw axis (−1={cfg['a']}, +1={cfg['b']})")
        axes[i, 0].set_title(f"{cfg['title']} — UMAP-6D lens", fontsize=10, color="#26261F", loc="left")
        axes[i, 1].set_title(f"{cfg['title']} — raw 2880-d axis", fontsize=10, color="#26261F", loc="left")
        axes[i, 1].axhline(0, color="#c9c8c0", lw=0.8, zorder=1)
    for ax in axes[1]:
        ax.set_xlabel("sentence position (shift after 20)", fontsize=9, color="#3d3d3a")
    handles = [plt.Line2D([], [], color=DIR_COLOR["block_ab"], lw=2, label="A → B"),
               plt.Line2D([], [], color=DIR_COLOR["block_ba"], lw=2, label="B → A"),
               plt.Line2D([], [], color="#8a8a85", lw=1, ls="--", label="regime shift")]
    fig.legend(handles=handles, loc="upper right", fontsize=9, frameon=False, ncols=3,
               bbox_to_anchor=(0.99, 1.0))
    fig.suptitle("Same transitions, two instruments — prior-design (word-context) runs, L23, target token",
                 fontsize=11, color="#26261F", x=0.01, ha="left")
    fig.text(0.01, 0.002,
             "Chain-log paper-protocol runs (harmony): polysemy_h + suicide families, 10 orderings × 2 directions each.\n"
             "Lens: UMAP-6D centroid axis (paper_protocol_basin_projection.py). Raw: N1 difference-of-means axis (axis_projection.py). Bands: ±1 std over orderings.",
             fontsize=6.5, color="#6b6b66")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    out = BASE / "dual_trajectory_L23.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    pd.concat(all_agg).to_csv(BASE / "dual_trajectory_L23_points.csv", index=False)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
