#!/usr/bin/env python3
"""Second-pass review R3: instrument checks (Items 5, 15a, 16a, 17, 18).

- Item 17: per-layer cosine(secondary axis, single-sentence calibration axis); fr + tank
  heatmap re-render under the secondary instrument (see r3_heatmaps in r2 figure module).
- Item 18: per-depth-band crossing times under the secondary instrument (pre-stated
  prediction logged in predictions_suicide_arm.md P7 BEFORE this run).
- Item 5a: per-side calibration spreads/strengths. 5b: median-midpoint sensitivity.
- Item 15a: layer-band robustness of tank headline numbers (L4/L8/L12/L16 calibration axes).
"""
from __future__ import annotations
import json, csv
from pathlib import Path
import numpy as np
import pandas as pd
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import load_runs

OUT = Path("docs/studies/context_shift/analysis")
AXD = OUT / "axes"

# ---------------- Item 17: axis rotation check ----------------
print("=" * 78)
print("Item 17 — cos(secondary axis, single-sentence calibration axis) per layer")
for probe, calf in (("tank", "axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"),
                    ("fr", "axes_session_5247081b_fictional_vs_real_pos1.npz")):
    sec = np.load(AXD / f"secondary_axis_{probe}.npz")
    cal = np.load(AXD / calf)
    coss = []
    for L in range(24):
        a = cal[f"axis_{L}"]; a = a / np.linalg.norm(a)
        coss.append(float(sec[f"axis_{L}"] @ a))
    print(f"{probe}: " + " ".join(f"L{L}:{c:.2f}" for L, c in enumerate(coss)))
    print(f"  min {min(coss):.2f} at L{int(np.argmin(coss))}; median {np.median(coss):.2f}")

# ---------------- load all-layer readings under BOTH instruments ----------------
def proj_all_layers(log, axnpz, sec, name_filter=None):
    """Return {run: (24, 40) secondary readings} and same for calibration axis."""
    logdf = pd.read_csv(log, sep="\t")
    out_sec, out_cal = {}, {}
    for _, r in logdf.iterrows():
        name = r["run"]
        if name_filter and not name_filter(name): continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[res["token_position"] == 1]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        S = np.zeros((24, 40)); C = np.zeros((24, 40))
        for L in range(24):
            sub = df[df["layer"] == L].sort_values("pos")
            X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            S[L] = ((X - sec[f"mid_{L}"]) @ sec[f"axis_{L}"]) / float(sec[f"denom_{L}"])
            a = axnpz[f"axis_{L}"]
            C[L] = 2.0 * ((X - axnpz[f"mid_{L}"]) @ a) / float(axnpz[f"denom_{L}"])
        out_sec[name] = S; out_cal[name] = C
    return out_sec, out_cal

CFG = {
    "tank": dict(log="docs/studies/context_shift/captures/tank_d3_d4_log.tsv",
                 cal="axes_session_29a80932_aquarium_vs_vehicle_pos1.npz",
                 filt=None, dest=lambda n: +1.0 if n.endswith("_ab") else -1.0,
                 isd4=lambda n: "_d4_" in n, plus=lambda n: n.endswith("_b"),
                 dirs=("_ab", "_ba")),
    "fr": dict(log="docs/studies/context_shift/captures/fr_d3_d4_log.tsv",
               cal="axes_session_5247081b_fictional_vs_real_pos1.npz",
               filt=lambda n: n.startswith("fr_s1_"), dest=lambda n: +1.0 if n.endswith("_fr") else -1.0,
               isd4=lambda n: "_d4_" in n, plus=lambda n: n.endswith("_r"),
               dirs=("_fr", "_rf")),
}
DATA = {}
for probe, c in CFG.items():
    sec = np.load(AXD / f"secondary_axis_{probe}.npz")
    cal = np.load(AXD / c["cal"])
    DATA[probe] = proj_all_layers(c["log"], cal, sec, c["filt"])

# ---------------- Item 18: crossing times per depth band (secondary instrument) ----------------
print("\n" + "=" * 78)
print("Item 18 — mean-level crossing time (first post-shift k with dest-side mean), per layer")
BANDS = {"L2-4": range(2, 5), "L5-9": range(5, 10), "L10-17": range(10, 18), "L18-23": range(18, 24)}
xt_rows = []
for probe, c in CFG.items():
    S, _ = DATA[probe]
    for dsuf in c["dirs"]:
        runs = [S[n] * c["dest"](n) for n in S if not c["isd4"](n) and n.endswith(dsuf)]
        M = np.mean(runs, axis=0)          # (24, 40) dest-oriented mean
        cross = []
        for L in range(24):
            post = M[L, 20:40]
            k = next((i + 1 for i, v in enumerate(post) if v > 0), None)
            cross.append(k)
            xt_rows.append({"probe": probe, "dir": dsuf, "layer": L, "cross_k": k})
        summary = {bn: [cross[L] for L in Ls] for bn, Ls in BANDS.items()}
        def fmt(ks):
            vals = [c_ for c_ in ks if c_ is not None]
            s = f"med {np.median(vals):.0f}" if vals else "-"
            nc = sum(1 for c_ in ks if c_ is None)
            return s + (f" (nc={nc})" if nc else "")
        line = " | ".join(f"{bn}: {fmt(ks)}" for bn, ks in summary.items())
        print(f"  {probe} {dsuf}: {line}")
pd.DataFrame(xt_rows).to_csv(OUT / "r3_crossing_times.csv", index=False)

# ---------------- Item 5a: per-side calibration spreads ----------------
print("\n" + "=" * 78)
print("Item 5a — per-side calibration spread along axis (sd of per-probe readings)")
for probe, sess, axf, Ls in (("tank", "session_29a80932", "axes_session_29a80932_aquarium_vs_vehicle_pos1.npz", (4, 8, 16, 23)),
                             ("fr", "session_5247081b", "axes_session_5247081b_fictional_vs_real_pos1.npz", (4, 14, 23))):
    ax = np.load(AXD / axf)
    lake = Path("data/lake") / sess
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[res["token_position"] == 1]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "label"])
    df = res.merge(tok, on="probe_id")
    labs = sorted(df["label"].unique())
    for L in Ls:
        sub = df[df["layer"] == L]
        X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        r = 2.0 * ((X - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"])
        parts = []
        for lab in labs:
            m_ = sub["label"].to_numpy() == lab
            parts.append(f"{lab}: mean {r[m_].mean():+.2f} sd {r[m_].std():.2f} n={m_.sum()}")
        print(f"  {probe} L{L}: " + " | ".join(parts))

# ---------------- Item 5b: median-midpoint sensitivity (tank) ----------------
print("\n" + "=" * 78)
print("Item 5b — tank direction asymmetry under mean- vs median-based D4 midpoint (L4, calibration axis)")
_, Ctank = DATA["tank"]
c = CFG["tank"]
d4A = np.stack([Ctank[n][4] for n in Ctank if c["isd4"](n) and not c["plus"](n)])
d4B = np.stack([Ctank[n][4] for n in Ctank if c["isd4"](n) and c["plus"](n)])
for mname, mid_t in (("mean", (d4A.mean(0) + d4B.mean(0)) / 2),
                     ("median", (np.median(d4A, 0) + np.median(d4B, 0)) / 2)):
    for dsuf, sign in (("_ab", +1.0), ("_ba", -1.0)):
        ys = np.stack([(Ctank[n][4] - mid_t) * sign for n in Ctank if not c["isd4"](n) and n.endswith(dsuf)])
        dest_lv = float((((d4B if sign > 0 else d4A).mean(0) - mid_t) * sign)[35:40].mean())
        gap = dest_lv - ys[:, 35:40].mean()
        M = ys.mean(0)[20:40]
        k = next((i + 1 for i, v in enumerate(M) if v > 0), None)
        print(f"  {mname:>6} mid, {dsuf}: mean-cross k={k}, residual gap {gap:+.2f}")

# ---------------- Item 15a: layer-band robustness (tank headline numbers) ----------------
print("\n" + "=" * 78)
print("Item 15a — tank headline numbers across L4/L8/L12/L16 (calibration axes, midref)")
for L in (4, 8, 12, 16):
    d4A = np.stack([Ctank[n][L] for n in Ctank if c["isd4"](n) and not c["plus"](n)])
    d4B = np.stack([Ctank[n][L] for n in Ctank if c["isd4"](n) and c["plus"](n)])
    mid_t = (d4A.mean(0) + d4B.mean(0)) / 2
    amp = float(((d4B.mean(0) - mid_t))[10:40].mean())
    parts = [f"amp {amp:.2f}"]
    for dsuf, sign in (("_ab", +1.0), ("_ba", -1.0)):
        ys = np.stack([(Ctank[n][L] - mid_t) * sign for n in Ctank if not c["isd4"](n) and n.endswith(dsuf)])
        M = ys.mean(0)[20:40]
        k = next((i + 1 for i, v in enumerate(M) if v > 0), None)
        dest_lv = float((((d4B if sign > 0 else d4A).mean(0) - mid_t) * sign)[35:40].mean())
        gap = dest_lv - ys[:, 35:40].mean()
        parts.append(f"{dsuf} cross k={k} gap {gap:+.2f} ({gap/amp:.2f} amp)")
    print(f"  L{L}: " + " | ".join(parts))

np.save("/tmp/r3_done.npy", np.array([1]))
print("\nR3 core battery complete.")
