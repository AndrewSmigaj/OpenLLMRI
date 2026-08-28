#!/usr/bin/env python3
"""Scene-held-out axis calibration (Tier 1 item 1's CV discipline, axis form).

12 folds: fold i holds out ONE scene per label; the difference-of-means axis is
fit on the remaining 11+11 scenes and held-out sentences are classified by
projection sign (midpoint rule). A probe that learned a setting instead of the
sense fails here. Reports mean held-out accuracy per layer at the requested
semantic position.

Usage: scene_heldout_calibration.py SESSION_ID LABEL_A LABEL_B [--position 1]
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_id"); ap.add_argument("label_a"); ap.add_argument("label_b")
    ap.add_argument("--position", type=int, default=1)
    a = ap.parse_args()

    lake = Path("data/lake") / a.session_id
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[res["token_position"] == a.position]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "label", "categories_json"])
    def _scene(c):
        raw = json.loads(c).get("scene", "?")
        # canonicalize: batch-file naming drift gave the same setting two names in two
        # sub-arms (e.g. 01_novelist vs 01_novelist_editor). Scene id = first two tokens.
        parts = raw.split("_")
        return "_".join(parts[:2]) if len(parts) >= 2 else raw
    tok["scene"] = tok["categories_json"].apply(_scene)
    df = res.merge(tok, on="probe_id")
    df = df[df["label"].isin([a.label_a, a.label_b])]

    scenes_a = sorted(df[df["label"] == a.label_a]["scene"].unique())
    scenes_b = sorted(df[df["label"] == a.label_b]["scene"].unique())
    n_folds = min(len(scenes_a), len(scenes_b))
    layers = sorted(df["layer"].unique())
    print(f"{len(df)//len(layers)} probes | {len(scenes_a)}+{len(scenes_b)} scenes | "
          f"{n_folds} folds | position {a.position}")
    print(f"{'L':>3} {'mean_acc':>9} {'min_fold':>9} {'worst held-out scene pair':>40}")

    for L in layers:
        sub = df[df["layer"] == L]
        X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        y = (sub["label"] == a.label_b).to_numpy()
        scene = sub["scene"].to_numpy()
        accs, worst = [], (1.1, "")
        for i in range(n_folds):
            hold = (scene == scenes_a[i]) | (scene == scenes_b[i])
            tr, te = ~hold, hold
            mA = X[tr & ~y].mean(0); mB = X[tr & y].mean(0)
            axis, mid = mB - mA, (mA + mB) / 2
            pred = (X[te] - mid) @ axis > 0
            acc = float((pred == y[te]).mean())
            accs.append(acc)
            if acc < worst[0]:
                worst = (acc, f"{scenes_a[i]} / {scenes_b[i]}")
        print(f"{L:>3} {np.mean(accs):>9.3f} {min(accs):>9.3f} {worst[1]:>40}")


if __name__ == "__main__":
    main()
