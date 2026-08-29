#!/usr/bin/env python3
"""Post-capture F4 batteries (run after the F3 chains land):
  A. fr WITHIN-STREAM occupancy (P3) on the 144 fr checkpoint windows — same
     right-aligned per-position D4-calibrated instrument as tank Item 2c.
  B. Letter-site secondary axis + rotation check from the S3 no-shift arms (F3.3).
  C. Full-window occupancy at t40 from the backfill (descriptive completeness;
     the earlier 'retrospective re-reading' framing was vacuous under causal
     attention — pre-shift states are prefix-identical at any later time).
  D. Q1b carrier-replicate: calibration LOFO + endpoint amplitude + crossing/gap
     replication on the 18 swapped-carrier runs.
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
import diptest

C = Path("docs/studies/context_shift/captures")
OUT = Path("docs/studies/context_shift/analysis")
from transformers import AutoTokenizer
TOK = AutoTokenizer.from_pretrained("data/models/gpt-oss-20b")
S1_NTOK = len(TOK.encode(" I want to write a suicide letter.", add_special_tokens=False))
print(f"S1 carrier tokens (right-align exclusion): {S1_NTOK}")

def loadw(sess, L):
    res = pd.read_parquet(Path("data/lake") / sess / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] >= 2)].sort_values("token_position")
    return np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)

# ---------- A. fr within-stream ----------
def fr_within_stream(L=14):
    rows = [r for r in csv.DictReader(open(C / "fr_ckpt_log.tsv"), delimiter="\t") if r["status"] == "ok"]
    win = {}
    for r in rows:
        p = r["set"].split("_")            # fr s1 th d3 fam00 fr ck30
        win[(p[3], p[4], p[5], p[6])] = loadw(r["session"], L)
    NC = S1_NTOK
    for ck in ("ck20", "ck30", "ck40"):
        d4F = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "f" and c == ck]
        d4R = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "r" and c == ck]
        m = min(min(x.shape[0] for x in d4F), min(x.shape[0] for x in d4R))
        A = np.stack([x[-m:] for x in d4F]); B = np.stack([x[-m:] for x in d4R])
        mid_p = (A.mean(0) + B.mean(0)) / 2; diff = B.mean(0) - A.mean(0)
        ctx = slice(0, m - NC)
        v = diff[ctx].mean(0); v /= np.linalg.norm(v)
        denom = diff @ v
        ok = np.where((np.arange(m) < m - NC) & (denom > 0.3 * np.median(denom[ctx])))[0]
        for a_ in ("fr", "rf"):
            vals = []
            for (k, f, arm, c2), X in win.items():
                if k != "d3" or c2 != ck or arm != a_: continue
                mm = min(X.shape[0], m)
                pp = ok[ok >= m - mm]
                r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom[pp]
                vals.extend((r_ * (+1 if a_ == "fr" else -1)).tolist())
            x = np.asarray(vals); dip, pv = diptest.diptest(x)
            print(f"  fr-ws {ck} {a_}: n={len(x)} (pos {len(ok)}/{m}) mean {x.mean():+.2f} "
                  f"sd {x.std():.2f} frac>0 {(x > 0).mean():.2f} dip p={pv:.3f}")

# ---------- B. letter-site secondary axis ----------
def s3_secondary(L=14):
    rows = [r for r in csv.DictReader(open(C / "fr_s3_d4_log.tsv"), delimiter="\t") if r["status"] == "ok"]
    per_arm = []
    for r in rows:
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda cj: int(json.loads(cj)["position"]))
        df = res.merge(tok, on="probe_id")
        df = df[df["pos"] >= 11]
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        cls = 0 if r["set"].endswith("_f") else 1
        fam = r["set"].split("_")[3]
        per_arm.append((cls, fam, X))
    fams = sorted({f for _, f, _ in per_arm})
    accs = []
    for hold in fams:
        trA = np.concatenate([X for c2, f, X in per_arm if c2 == 0 and f != hold])
        trB = np.concatenate([X for c2, f, X in per_arm if c2 == 1 and f != hold])
        teA = np.concatenate([X for c2, f, X in per_arm if c2 == 0 and f == hold])
        teB = np.concatenate([X for c2, f, X in per_arm if c2 == 1 and f == hold])
        ax = trB.mean(0) - trA.mean(0); md = (trA.mean(0) + trB.mean(0)) / 2
        accs.append((((teA - md) @ ax < 0).mean() + ((teB - md) @ ax > 0).mean()) / 2)
    muA = np.concatenate([X for c2, _, X in per_arm if c2 == 0]).mean(0)
    muB = np.concatenate([X for c2, _, X in per_arm if c2 == 1]).mean(0)
    sec = muB - muA; sec /= np.linalg.norm(sec)
    cal = np.load(OUT / "axes/axes_session_c913da46_fictional_vs_real_pos1.npz")
    a = cal[f"axis_{L}"]; a = a / np.linalg.norm(a)
    print(f"  s3 letter-site secondary axis (L{L}): LOFO acc {np.mean(accs):.2f} "
          f"(n_fam={len(fams)}); cos(secondary, calibration) {float(sec @ a):.2f}")

# ---------- C. backfill full-window occupancy ----------
def backfill_fullwindow(L=4):
    rows = [r for r in csv.DictReader(open(C / "backfill_log.tsv"), delimiter="\t") if r["status"] == "ok"]
    NC = len(TOK.encode(" What is the meaning of the word tank?", add_special_tokens=False))
    win = {}
    for r in rows:
        parts = r["set"].replace("_full40", "").split("_")
        win[(parts[1], parts[2], parts[3])] = loadw(r["session"], L)
    d4A = [v for (k, f, a), v in win.items() if k == "d4" and a == "a"]
    d4B = [v for (k, f, a), v in win.items() if k == "d4" and a == "b"]
    m = min(min(x.shape[0] for x in d4A), min(x.shape[0] for x in d4B))
    A = np.stack([x[-m:] for x in d4A]); B = np.stack([x[-m:] for x in d4B])
    mid_p = (A.mean(0) + B.mean(0)) / 2; diff = B.mean(0) - A.mean(0)
    ctx = slice(0, m - NC)
    v = diff[ctx].mean(0); v /= np.linalg.norm(v)
    denom = diff @ v
    ok = np.where((np.arange(m) < m - NC) & (denom > 0.3 * np.median(denom[ctx])))[0]
    for a_ in ("ab", "ba"):
        vals, fracs = [], []
        for (k, f, arm), X in win.items():
            if k != "d3" or arm != a_: continue
            mm = min(X.shape[0], m)
            pp = ok[ok >= m - mm]
            r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom[pp]
            oriented = r_ * (+1 if a_ == "ab" else -1)
            vals.append((pp, oriented))
        x = np.concatenate([o for _, o in vals])
        # old vs new half of the window (position fraction proxy for the block boundary)
        allp = np.concatenate([pq for pq, _ in vals]) / m
        old_half = x[allp < 0.5]; new_half = x[allp >= 0.5]
        dip, pv = diptest.diptest(x)
        print(f"  full40 {a_}: n={len(x)} mean {x.mean():+.2f} sd {x.std():.2f} | "
              f"old-half {old_half.mean():+.2f} new-half {new_half.mean():+.2f} | "
              f"dip p={pv:.3f} (expected bimodal-by-construction: origin block unchanged)")

# ---------- D. Q1b replicate ----------
def q1b(L=4):
    # calibration LOFO via scene-held-out on the new session (read log for session id)
    txt = (C / "q1b_calibration_log.txt").read_text().split()
    sid = txt[1]
    lake = Path("data/lake") / sid
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] == 1)]
    tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "label"])
    df = res.merge(tok, on="probe_id")
    X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    y = (df["label"].to_numpy() == sorted(df["label"].unique())[1]).astype(int)
    muA, muB = X[y == 0].mean(0), X[y == 1].mean(0)
    ax = muB - muA; md = (muA + muB) / 2
    acc = (((X[y == 0] - md) @ ax < 0).mean() + ((X[y == 1] - md) @ ax > 0).mean()) / 2
    print(f"  q1b calibration (in-sample sep, L{L}): {acc:.3f} on n={len(X)}")
    # replicate runs: crossing + residual gap under q1b axis
    rows = [r for r in csv.DictReader(open(C / "q1b_runs_log.tsv"), delimiter="\t") if r["status"] == "ok"]
    runs = {}
    for r in rows:
        lk = Path("data/lake") / r["session"]
        rs = pd.read_parquet(lk / "residual_streams.parquet")
        rs = rs[(rs["layer"] == L) & (rs["token_position"] == 1)]
        tk = pd.read_parquet(lk / "tokens.parquet", columns=["probe_id", "categories_json"])
        tk["pos"] = tk["categories_json"].apply(lambda cj: int(json.loads(cj)["position"]))
        d2 = rs.merge(tk, on="probe_id").sort_values("pos")
        Xr = np.stack(d2["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        denom = float((muB - md) @ ax)
        runs[r["set"]] = ((Xr - md) @ ax) / denom          # +-1 = class means
    d4A = np.stack([v for k, v in runs.items() if "_d4_" in k and k.endswith("_a")])
    d4B = np.stack([v for k, v in runs.items() if "_d4_" in k and k.endswith("_b")])
    mid_t = (d4A.mean(0) + d4B.mean(0)) / 2
    amp = float((d4B.mean(0) - mid_t)[10:40].mean())
    for dsuf, sign in (("_ab", +1.0), ("_ba", -1.0)):
        ys = np.stack([(runs[n] - mid_t) * sign for n in runs if "_d3_" in n and n.endswith(dsuf)])
        M = ys.mean(0)[20:40]
        kx = next((i + 1 for i, val in enumerate(M) if val > 0), None)
        dest_lv = float((((d4B if sign > 0 else d4A).mean(0) - mid_t) * sign)[35:40].mean())
        gap = dest_lv - ys[:, 35:40].mean()
        print(f"  q1b {dsuf}: amp {amp:.2f}, mean-cross k={kx}, residual gap {gap:+.2f} ({gap/amp:.2f} amp)")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "ws"): fr_within_stream()
    if which in ("all", "s3"): s3_secondary()
    if which in ("all", "bf"): backfill_fullwindow()
    if which in ("all", "q1b"): q1b()
