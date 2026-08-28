#!/usr/bin/env python3
"""Three-worlds distribution tests — tank transition windows (plan Tier 1 item 3).

Population doctrine: ONLY post-shift occupancy is tested; endpoint sets never feed
these tests. Two populations, per the time-stratification guard:

P1 (primary, same-token — no cross-position caveat): per-step carrier readings
   (` tank` site, pos 1) from the D3 trajectory runs, post-shift steps only,
   stratified by time-since-shift bands and pooled. Each reading is one run-step
   state produced by the model's dynamics.
P2 (secondary, window context tokens): checkpoint-window token states projected on
   the same axis. CAVEAT (documented): token-identity offsets can shape this
   distribution; reported alongside P1, never alone.

Worlds: passage -> bimodal pile-up at the endpoints; metastable middle -> third
mode; graded -> unimodal smear. Tests: Hartigan dip (unimodality), plus a 2-vs-3
component Gaussian-mixture BIC comparison as the explicit trimodality check.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import diptest
from sklearn.mixture import GaussianMixture

LAYER = 4
AXES = "docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"
BOUNDARY = 20

def gmm_bic(x):
    x = x.reshape(-1, 1)
    bics = {}
    for k in (1, 2, 3):
        g = GaussianMixture(k, random_state=1, n_init=3).fit(x)
        bics[k] = g.bic(x)
    best = min(bics, key=bics.get)
    return best, {k: round(v, 1) for k, v in bics.items()}

def report(tag, x):
    if len(x) < 20:
        print(f"{tag}: n={len(x)} (too small)"); return
    dip, p = diptest.diptest(x)
    best, bics = gmm_bic(x)
    print(f"{tag}: n={len(x)} mean={x.mean():+.2f} sd={x.std():.2f} | "
          f"dip={dip:.4f} p={p:.4f} {'MULTIMODAL' if p<0.05 else 'unimodal-ok'} | "
          f"GMM best k={best} (BIC {bics})")

def main():
    data = np.load(AXES)
    axis, mid, denom = data[f"axis_{LAYER}"], data[f"mid_{LAYER}"], float(data[f"denom_{LAYER}"])

    # ---------- P1: per-step carrier readings ----------
    log = pd.read_csv("docs/studies/context_shift/captures/tank_d3_d4_log.tsv", sep="\t")
    readings = []  # (direction, step_after_shift, value)
    for _, r in log.iterrows():
        if "_d3_" not in r["run"]:
            continue
        direction = "ab" if r["run"].endswith("_ab") else "ba"
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == LAYER) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - mid) @ axis) / denom
        for p_, v in zip(df["pos"], proj):
            if p_ > BOUNDARY:
                readings.append((direction, p_ - BOUNDARY, float(v)))
    P1 = pd.DataFrame(readings, columns=["dir", "t", "v"])

    print("=" * 70)
    print("P1 — per-step carrier readings (same-token; the clean population)")
    print("=" * 70)
    for d in ("ab", "ba"):
        sub = P1[P1["dir"] == d]
        # orient so destination = +1 for pooling across directions
        for band, lo, hi in (("t1-5", 1, 5), ("t6-10", 6, 10), ("t11-15", 11, 15), ("t16-20", 16, 20)):
            report(f"dir {d} {band}", sub[(sub.t >= lo) & (sub.t <= hi)]["v"].to_numpy())
        report(f"dir {d} pooled t1-20", sub["v"].to_numpy())
    # both directions pooled, oriented to destination-positive
    both = np.concatenate([P1[P1["dir"] == "ab"]["v"].to_numpy(),
                           -P1[P1["dir"] == "ba"]["v"].to_numpy()])
    report("both dirs pooled (destination-positive)", both)

    # ---------- P2: checkpoint window context tokens ----------
    print("=" * 70)
    print("P2 — window context tokens (cross-token caveat applies)")
    print("=" * 70)
    ck = pd.read_csv("docs/studies/context_shift/captures/tank_ckpt_log.tsv", sep="\t")
    ck = ck[ck["status"] == "ok"].drop_duplicates(subset=["set"], keep="first")
    for band in ("ck21", "ck30", "ck40"):
        vals = []
        for _, r in ck.iterrows():
            if not r["set"].endswith(band) or "_d3_" not in r["set"]:
                continue
            lake = Path("data/lake") / r["session"]
            try:
                res = pd.read_parquet(lake / "residual_streams.parquet")
            except Exception:
                continue
            res = res[(res["layer"] == LAYER) & (res["token_position"] >= 2)]
            # exclude the 10 carrier tokens at the window tail
            top = res["token_position"].max()
            res = res[res["token_position"] <= top - 10]
            if not len(res):
                continue
            X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            vals.append(2.0 * ((X - mid) @ axis) / denom)
        if vals:
            report(f"{band} post-shift window tokens", np.concatenate(vals))

if __name__ == "__main__":
    main()
