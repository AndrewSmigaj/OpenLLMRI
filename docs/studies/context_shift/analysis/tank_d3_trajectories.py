#!/usr/bin/env python3
"""Tank D3/D4 trajectory analysis on the calibrated Q1 axis (designed corpus).

Projects every run's carrier readings (post-lexical ` tank` = pos 1; pre-lexical
` word` = pos 8) onto the Q1 axis calibrated from session_29a80932 (D1b, 300/label).
Outputs per-direction aggregate trajectories, transition metrics per run, and the
D4 no-shift control trajectories. Convention: aquarium = -1, vehicle = +1.

Transition metrics (plan Tier 1 item 4), computed on the raw axis at LAYER:
  tokens_to_crossing: steps after the boundary until the reading first crosses 0
  settled_mean: mean reading over the last 10 steps
  residual: distance of settled_mean from the destination endpoint (+-1)
  overshoot: max |reading| beyond the destination endpoint after crossing
  dwell_mid: number of post-boundary steps with |reading| < 0.5
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

LAYER = 4          # peak scene-held-out separability; L23 run as robustness
AXES = "docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"
LOG = "docs/studies/context_shift/captures/tank_d3_d4_log.tsv"
BOUNDARY = 20

def project(session_id, data, position, layer):
    lake = Path("data/lake") / session_id
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[(res["layer"] == layer) & (res["token_position"] == position)]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
    tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
    df = res.merge(tok, on="probe_id").sort_values("pos")
    X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    proj = 2.0 * ((X - data[f"mid_{layer}"]) @ data[f"axis_{layer}"]) / float(data[f"denom_{layer}"])
    return df["pos"].to_numpy(), proj

def metrics(pos, proj, direction):
    # sign convention: destination +1 if heading to vehicle, -1 if to aquarium
    dest = 1.0 if direction.endswith("vehicle") else -1.0
    post = proj[pos > BOUNDARY]
    signed = post * dest                      # >0 means on destination side
    crossing = next((i + 1 for i, v in enumerate(signed) if v > 0), None)
    settled = float(np.mean(proj[-10:]))
    return {
        "tokens_to_crossing": crossing,
        "settled_mean": round(settled, 3),
        "residual_from_dest": round(abs(dest - settled), 3),
        "overshoot": round(float(max(0.0, (signed).max() - 1.0)), 3) if len(signed) else None,
        "dwell_mid": int((np.abs(post) < 0.5).sum()),
        "pre_mean": round(float(np.mean(proj[pos <= BOUNDARY])), 3),
    }

def main():
    data = np.load(AXES)
    log = pd.read_csv(LOG, sep="\t")
    rows = []
    curves = {}
    for _, r in log.iterrows():
        name, sid = r["run"], r["session"]
        kind = "d3" if "_d3_" in name else "d4"
        direction = ("aquarium_then_vehicle" if name.endswith("_ab") else
                     "vehicle_then_aquarium") if kind == "d3" else \
                    ("aquarium_only" if name.endswith("_a") else "vehicle_only")
        pos, proj = project(sid, data, 1, LAYER)
        curves.setdefault((kind, direction), []).append(proj)
        m = metrics(pos, proj, direction) if kind == "d3" else {}
        rows.append({"run": name, "kind": kind, "direction": direction, **m})

    df = pd.DataFrame(rows)
    out = Path("docs/studies/context_shift/analysis")
    df.to_csv(out / f"tank_d3_metrics_L{LAYER}.csv", index=False)

    print(f"=== Layer {LAYER}, post-lexical ` tank` site, Q1 axis (aq=-1, vh=+1) ===")
    for (kind, direction), cs in sorted(curves.items()):
        arr = np.stack(cs)
        agg = arr.mean(0)
        print(f"\n{kind} {direction} (n={len(cs)}):")
        for p in (1, 10, 20, 21, 22, 25, 30, 40):
            print(f"  pos {p:>2}: {agg[p-1]:+.2f} ± {arr[:,p-1].std():.2f}")
    d3 = df[df.kind == "d3"]
    print("\n=== D3 transition metrics (mean over 12 families per direction) ===")
    print(d3.groupby("direction")[["tokens_to_crossing", "settled_mean",
          "residual_from_dest", "dwell_mid", "pre_mean"]].mean().round(2).to_string())
    np.save(out / f"tank_d3_curves_L{LAYER}.npy",
            {k: np.stack(v) for k, v in curves.items()}, allow_pickle=True)

if __name__ == "__main__":
    main()
