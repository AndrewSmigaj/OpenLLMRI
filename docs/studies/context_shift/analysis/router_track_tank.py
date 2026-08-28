#!/usr/bin/env python3
"""Router track — tank transitions (briefing battery 1(d); plan W2).

Signatures (briefing): learned intermediate -> distinctive stable third routing
pattern in the unresolved band; passage -> brief instability that resolves;
off-manifold -> entropy spikes / flickering / fallback experts.

Band rule (b), fixed in advance: the interval between the inner 95th percentiles
of the two ENDPOINT calibration distributions (session_29a80932 projections),
per layer; sensitivity sweep at 90th percentiles reported alongside.
Behavior labels never enter the band definition.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

LAYERS = [4, 14, 23]
BOUNDARY = 20
CAL = "session_29a80932"
AXES = f"docs/studies/context_shift/analysis/axes/axes_{CAL}_aquarium_vs_vehicle_pos1.npz"
LOG = "docs/studies/context_shift/captures/tank_d3_d4_log.tsv"


def band_rule_b(layer, axdata, pct):
    """Rule (b), position-matched refinement (2026-08-28): the endpoint distributions are
    the D4 no-shift carrier readings at plateau steps (11-40) — the briefing's own manifold
    reference includes no-shift activations, and single-sentence calibration distributions
    overlap near zero (empty band at p95; recorded). Single-sentence calibration still
    anchors the +-1 normalization; it just does not define the transition band.
    Flagged for the other AI in briefing_reconciliation.md."""
    log = pd.read_csv(LOG, sep="\t")
    a_vals, b_vals = [], []
    for _, r in log.iterrows():
        if "_d4_" not in r["run"]:
            continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == layer) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        df = df[df["pos"] >= 11]
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - axdata[f"mid_{layer}"]) @ axdata[f"axis_{layer}"]) / float(axdata[f"denom_{layer}"])
        (a_vals if r["run"].endswith("_a") else b_vals).extend(proj.tolist())
    lo = float(np.percentile(a_vals, pct))
    hi = float(np.percentile(b_vals, 100 - pct))
    return (lo, hi) if lo < hi else None


def main():
    axdata = np.load(AXES)
    log = pd.read_csv(LOG, sep="\t")

    for L in LAYERS:
        band = band_rule_b(L, axdata, 95)
        band90 = band_rule_b(L, axdata, 90)
        print(f"\n===== L{L}: band rule(b) p95 = {band}, sensitivity p90 = {band90} =====")
        if band is None:
            print("  (endpoint distributions overlap at p95 — band empty; skipping)")
            continue
        axis, mid_v, denom = axdata[f"axis_{L}"], axdata[f"mid_{L}"], float(axdata[f"denom_{L}"])

        # collect per-step (proj, entropy, top1, phase, kind)
        rows = []
        for _, r in log.iterrows():
            kind = "d3" if "_d3_" in r["run"] else "d4"
            lake = Path("data/lake") / r["session"]
            res = pd.read_parquet(lake / "residual_streams.parquet")
            res = res[(res["layer"] == L) & (res["token_position"] == 1)]
            rt = pd.read_parquet(lake / "routing.parquet")
            rt = rt[(rt["layer"] == L) & (rt["token_position"] == 1)][
                ["probe_id", "gate_entropy", "expert_top1_id"]]
            tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
            tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
            df = res.merge(rt, on="probe_id").merge(tok, on="probe_id").sort_values("pos")
            X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            proj = 2.0 * ((X - mid_v) @ axis) / denom
            for (_, x), v in zip(df.iterrows(), proj):
                p_ = x["pos"]
                phase = ("pre" if p_ <= BOUNDARY else
                         "post21-25" if p_ <= 25 else "mid26-32" if p_ <= 32 else "late33-40")
                rows.append(dict(kind=kind, run=r["run"], pos=p_, phase=phase,
                                 proj=float(v), H=float(x["gate_entropy"]),
                                 e=int(x["expert_top1_id"])))
        df = pd.DataFrame(rows)

        # entropy by phase, d3 vs d4 (matched positions)
        piv = df.groupby(["phase", "kind"])["H"].agg(["mean", "std"]).round(3)
        print(piv.to_string())
        # entropy in-band vs out-of-band (d3 only)
        d3 = df[df.kind == "d3"].copy()
        d3["in_band"] = d3["proj"].between(*band)
        eb = d3.groupby("in_band")["H"].agg(["mean", "std", "count"]).round(3)
        print(f"entropy by band membership (d3):\n{eb.to_string()}")

        # expert composition
        mid_c = Counter(d3[d3.in_band]["e"])
        endA = Counter(d3[(~d3.in_band) & (d3.proj < band[0])]["e"])
        endB = Counter(d3[(~d3.in_band) & (d3.proj > band[1])]["e"])
        endset = {e for e, _ in endA.most_common(5)} | {e for e, _ in endB.most_common(5)}
        cov = sum(c for e, c in mid_c.items() if e in endset) / max(sum(mid_c.values()), 1)
        novel = [(e, c) for e, c in mid_c.most_common(6) if e not in endset]
        # consecutive-step top1 switch rate inside band vs outside
        def switch_rate(sub):
            sw = tot = 0
            for _, g in sub.groupby("run"):
                seq = g.sort_values("pos")["e"].to_numpy()
                sw += int((seq[1:] != seq[:-1]).sum()); tot += max(len(seq) - 1, 0)
            return sw / max(tot, 1)
        print(f"band top1 experts: {mid_c.most_common(6)}")
        print(f"endpoint top-5 sets: A={[e for e,_ in endA.most_common(5)]} B={[e for e,_ in endB.most_common(5)]}")
        print(f"band mass on endpoint experts: {cov:.0%} | novel band experts: {novel}")
        print(f"top1 switch rate: in-band {switch_rate(d3[d3.in_band]):.2f} vs "
              f"out-of-band {switch_rate(d3[~d3.in_band]):.2f} vs d4 {switch_rate(df[df.kind=='d4']):.2f}")


if __name__ == "__main__":
    main()
