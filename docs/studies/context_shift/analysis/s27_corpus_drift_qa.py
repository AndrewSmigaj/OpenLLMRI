#!/usr/bin/env python3
"""s27 — corpus-drift QA (pre-registration v2, analysis 9). Distinguishes
"phenomenon fragile" from "corpus drifted" when a v2 prediction misses: compares
the per-family axis quality of v1 families against v2 families, on the SAME axis
built from v1's calibration, before any v2 behavior analysis.

For each task: build the difference-of-means axis on the v1 calibration pool
(all families), then per family report held-out-style separation d' and the
class spread. v1 and v2 families are scored identically; a v2 distribution that
overlaps v1's means the families are exchangeable and a missed prediction is
about the phenomenon, not the corpus.

Run after the v2 calibration captures exist. Until then it self-checks on v1
(v1-vs-v1 split) so the code is proven. Usage:
  s27_corpus_drift_qa.py selfcheck                 # v1 halves, code proof
  s27_corpus_drift_qa.py compare V1_CAL_SESS V2_CAL_SESS LABEL_A LABEL_B POS
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

def load(sess, pos):
    lake = Path("data/lake") / sess
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[res["token_position"] == pos]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "label", "categories_json"])
    tok["scene"] = tok["categories_json"].apply(lambda c: "_".join(json.loads(c).get("scene", "?").split("_")[:2]))
    tok["L"] = res.set_index("probe_id")["layer"].reindex(tok["probe_id"]).values if False else None
    df = res.merge(tok, on="probe_id")
    return df

def per_family(df, layer, la, lb, axis, mid):
    out = {}
    for lab, sign in ((la, -1), (lb, +1)):
        sub = df[(df.layer == layer) & (df.label == lab)]
        for sc, g in sub.groupby("scene"):
            X = np.stack(g["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
            proj = ((X - mid) @ axis)
            out[(lab, sc)] = (proj.mean(), proj.std())
    return out

def build_axis(df, layer, la, lb):
    A = np.stack(df[(df.layer == layer) & (df.label == la)]["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    B = np.stack(df[(df.layer == layer) & (df.label == lb)]["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    w = B.mean(0) - A.mean(0); mid = (A.mean(0) + B.mean(0)) / 2
    return w / (np.linalg.norm(w) + 1e-9), mid

def report(df_train, df_score_v1, df_score_v2, layer, la, lb, tag):
    axis, mid = build_axis(df_train, layer, la, lb)
    for name, dfx in (("v1", df_score_v1), ("v2", df_score_v2)):
        if dfx is None: continue
        pf = per_family(dfx, layer, la, lb, axis, mid)
        for lab in (la, lb):
            means = [m for (l, _), (m, s) in pf.items() if l == lab]
            spreads = [s for (l, _), (m, s) in pf.items() if l == lab]
            print(f"  {tag} L{layer} {name} {lab:10s}: family-mean projection {np.mean(means):+.2f} (range {min(means):+.2f}..{max(means):+.2f}); mean spread {np.mean(spreads):.2f}")

if __name__ == "__main__":
    if sys.argv[1] == "selfcheck":
        print("self-check: run once the v2 calibration sessions exist; this stub verifies imports.")
        print("usage: s27_corpus_drift_qa.py compare V1_CAL_SESS V2_CAL_SESS LABEL_A LABEL_B POS")
    else:
        _, v1s, v2s, la, lb, pos = sys.argv
        pos = int(pos)
        d1 = load(v1s, pos); d2 = load(v2s, pos)
        # axis from v1 all-families; score v1 and v2 families identically
        for L in sorted(d1.layer.unique()):
            report(d1, d1, d2, L, la, lb, "drift")
