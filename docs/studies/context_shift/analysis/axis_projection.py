#!/usr/bin/env python3
"""Raw-space axis projection (N1) — Context-Shift Dynamics program.

Per layer: difference-of-class-means direction computed on RAW 2880-d residual
streams (no reduction, no neuron thresholding) from design-time-labeled endpoint
data. Endpoints renormalized so class means project to -1 (class A) and +1
(class B). Projection of any other session onto the same axis preserves that
coordinate convention.

Method precedent: lying_v4 centroid projection (docs/research/StudiesByClaude/
lying_v4_findings.md). Population doctrine: endpoint sets CALIBRATE; transition
windows are projected, never used to fit the axis.

Usage:
  axis_projection.py calibrate SESSION_ID LABEL_A LABEL_B [--position 1] [--out DIR]
  axis_projection.py project SESSION_ID AXES_NPZ [--position 1] [--out FILE]

calibrate: fits per-layer axes from the session's labeled probes, reports
  per-layer separability (best-threshold accuracy on a 50/50 stratified held-out
  split), and saves axes + normalization to an .npz.
project: projects a session's residuals through saved axes; writes a CSV of
  (probe_id, layer, position-tagged metadata, projection).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(1)


def load_residuals(session_id: str, position: int) -> pd.DataFrame:
    lake = Path("data/lake") / session_id
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[res["token_position"] == position]
    tok = pd.read_parquet(lake / "tokens.parquet",
                          columns=["probe_id", "label", "input_text", "categories_json"])
    return res.merge(tok, on="probe_id", how="left")


def calibrate(session_id: str, label_a: str, label_b: str, position: int, out_dir: Path):
    df = load_residuals(session_id, position)
    df = df[df["label"].isin([label_a, label_b])]
    layers = sorted(df["layer"].unique())
    axes, report = {}, []

    for L in layers:
        sub = df[df["layer"] == L]
        X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        y = (sub["label"] == label_b).to_numpy()
        mean_a, mean_b = X[~y].mean(0), X[y].mean(0)
        axis = mean_b - mean_a
        denom = float(axis @ axis)
        if denom < 1e-12:
            continue
        mid = (mean_a + mean_b) / 2.0
        # proj(mean_a) = -1, proj(mean_b) = +1 by construction
        proj = 2.0 * ((X - mid) @ axis) / denom

        # Held-out separability: 50/50 stratified split, axis refit on train only
        idx_a, idx_b = np.where(~y)[0], np.where(y)[0]
        RNG_local = np.random.default_rng(1)
        RNG_local.shuffle(idx_a); RNG_local.shuffle(idx_b)
        tr = np.concatenate([idx_a[: len(idx_a) // 2], idx_b[: len(idx_b) // 2]])
        te = np.concatenate([idx_a[len(idx_a) // 2:], idx_b[len(idx_b) // 2:]])
        ax_tr = X[tr][y[tr]].mean(0) - X[tr][~y[tr]].mean(0)
        mid_tr = (X[tr][y[tr]].mean(0) + X[tr][~y[tr]].mean(0)) / 2.0
        p_te = (X[te] - mid_tr) @ ax_tr
        # best threshold on test projections
        order = np.argsort(p_te)
        sorted_y = y[te][order]
        n_b = sorted_y.sum(); n_a = len(sorted_y) - n_b
        # accuracy sweeping threshold between consecutive points
        cum_b = np.concatenate([[0], np.cumsum(sorted_y)])
        k = np.arange(len(sorted_y) + 1)
        acc = ((k - cum_b) + (n_b - cum_b)) / len(sorted_y)
        best_acc = float(acc.max())

        axes[str(L)] = {"axis": axis, "mid": mid, "denom": denom}
        report.append({"layer": int(L), "n_a": int((~y).sum()), "n_b": int(y.sum()),
                       "axis_norm": float(np.sqrt(denom)),
                       "heldout_acc": round(best_acc, 4),
                       "mean_proj_a": round(float(proj[~y].mean()), 3),
                       "mean_proj_b": round(float(proj[y].mean()), 3),
                       "std_a": round(float(proj[~y].std()), 3),
                       "std_b": round(float(proj[y].std()), 3)})

    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{session_id}_{label_a}_vs_{label_b}_pos{position}"
    npz_path = out_dir / f"axes_{tag}.npz"
    np.savez_compressed(
        npz_path,
        **{f"axis_{L}": v["axis"] for L, v in axes.items()},
        **{f"mid_{L}": v["mid"] for L, v in axes.items()},
        **{f"denom_{L}": np.array(v["denom"]) for L, v in axes.items()},
    )
    meta = {"session_id": session_id, "label_a": label_a, "label_b": label_b,
            "position": position, "convention": "mean(A)->-1, mean(B)->+1",
            "report": report}
    (out_dir / f"axes_{tag}.json").write_text(json.dumps(meta, indent=1))
    print(f"saved {npz_path}")
    print(f"{'L':>3} {'n_a':>4} {'n_b':>4} {'|axis|':>8} {'heldout':>8} {'muA':>6} {'muB':>6} {'sdA':>5} {'sdB':>5}")
    for r in report:
        print(f"{r['layer']:>3} {r['n_a']:>4} {r['n_b']:>4} {r['axis_norm']:>8.2f} "
              f"{r['heldout_acc']:>8.3f} {r['mean_proj_a']:>6.2f} {r['mean_proj_b']:>6.2f} "
              f"{r['std_a']:>5.2f} {r['std_b']:>5.2f}")


def project(session_id: str, axes_npz: Path, position: int, out_file: Path | None):
    data = np.load(axes_npz)
    layer_keys = sorted({k.split("_")[1] for k in data.files if k.startswith("axis_")}, key=int)
    df = load_residuals(session_id, position)
    rows = []
    for L in layer_keys:
        sub = df[df["layer"] == int(L)]
        if not len(sub):
            continue
        X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - data[f"mid_{L}"]) @ data[f"axis_{L}"]) / float(data[f"denom_{L}"])
        for pid, lab, cats, p in zip(sub["probe_id"], sub["label"], sub["categories_json"], proj):
            rows.append({"probe_id": pid, "layer": int(L), "label": lab,
                         "categories_json": cats, "projection": float(p)})
    out = pd.DataFrame(rows)
    if out_file:
        out.to_csv(out_file, index=False)
        print(f"saved {out_file} ({len(out)} rows)")
    else:
        print(out.groupby(["layer", "label"])["projection"].agg(["mean", "std", "count"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("calibrate")
    c.add_argument("session_id"); c.add_argument("label_a"); c.add_argument("label_b")
    c.add_argument("--position", type=int, default=1)
    c.add_argument("--out", default="docs/studies/context_shift/analysis/axes")
    p = sp.add_parser("project")
    p.add_argument("session_id"); p.add_argument("axes_npz")
    p.add_argument("--position", type=int, default=1)
    p.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.cmd == "calibrate":
        calibrate(a.session_id, a.label_a, a.label_b, a.position, Path(a.out))
    else:
        project(a.session_id, Path(a.axes_npz), a.position, Path(a.out) if a.out else None)
