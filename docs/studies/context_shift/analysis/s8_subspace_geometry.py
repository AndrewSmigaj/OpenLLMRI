#!/usr/bin/env python3
"""S8 — subspace-sensitive off-manifold check (Andrew: "even a little off manifold is
off manifold"; the k-NN aggregate is dominated by high-variance noise).

Reference manifold: PCA subspace of D4 no-shift states at matched positions (21-40),
fit on all 240 D4 states. Null: leave-one-family-out D4 residuals (subspace refit per
fold). Queries: D3 post-shift states (jump steps / park / all), pre-shift states
(should match D4), calibration states (positive control).

Detector 1 (individual excursions): per-state out-of-subspace residual norm vs the
held-out D4 null distribution, at 80/90/95% variance-capture subspaces.
Detector 2 (systematic small displacement): ||mean out-of-subspace residual|| of the
query set vs a size-matched bootstrap of held-out D4 residual vectors — sensitive to a
consistent displacement far below the per-state noise floor. Plus direction-consistency
(mean pairwise cos of per-run mean residuals).
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
from second_pass_r1_dynamics import tank_cfg, fr_cfg

rng = np.random.default_rng(31)

def battery(cfgf, tag, cal_sess, L):
    tag2, d4a, d4b, d3, dest_fn, fam_fn = cfgf()
    D4 = {**{f"a{i}": v for i, v in enumerate(d4a)}, **{f"b{i}": v for i, v in enumerate(d4b)}}
    # arms carry family identity via cfg loaders' order; rebuild with fam labels
    # (use run names from d3/d4 dicts directly instead)
    tagd, d4a2, d4b2, d3r, destf, famf = cfgf()
    # reload with names: use the log-based loader keys
    # Simpler: reconstruct from cfg's d3/d4 by re-calling load in r1 module pattern
    # -> we already have per-arm arrays; family labels come from position in list; treat
    #    each ARM as its own cluster for the LOFO folds (leave-one-ARM-PAIR-out ~ family).
    A = np.stack(d4a); B = np.stack(d4b)          # (6, 40, ...)? -> actually (6, 40) proj...
    return None

# The cfg loaders return projections, not raw states — load raw states directly.
def load_raw(log, L, keep):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    out = {}
    for r in rows:
        n = r["run"]
        if not keep(n): continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        out[n] = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    return out

CFG = {
    "tank_L4": dict(log="docs/studies/context_shift/captures/tank_d3_d4_log.tsv", L=4,
                    cal="session_29a80932", d3k=lambda n: "_d3_" in n, d4k=lambda n: "_d4_" in n,
                    fam=lambda n: n.split("_")[2], ab=lambda n: n.endswith("_ab")),
    "fr_L14": dict(log="docs/studies/context_shift/captures/fr_d3_d4_log.tsv", L=14,
                   cal="session_5247081b", d3k=lambda n: "fr_s1_" in n and "_d3_" in n,
                   d4k=lambda n: "fr_s1_" in n and "_d4_" in n,
                   fam=lambda n: n.split("_")[4], ab=lambda n: n.endswith("_fr")),
}
for tag, c in CFG.items():
    d4 = load_raw(c["log"], c["L"], c["d4k"])
    d3 = load_raw(c["log"], c["L"], c["d3k"])
    D4mat = np.concatenate([v[20:40] for v in d4.values()])          # 240 x 2880
    fams4 = np.concatenate([[c["fam"](n)] * 20 for n in d4])
    center = D4mat.mean(0)
    Xc = D4mat - center
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = S ** 2 / (S ** 2).sum()
    cum = np.cumsum(var)
    print("=" * 78)
    print(f"### {tag}: D4 subspace — components for 80/90/95% var: "
          f"{int(np.searchsorted(cum, .80)) + 1}/{int(np.searchsorted(cum, .90)) + 1}/"
          f"{int(np.searchsorted(cum, .95)) + 1} of {len(S)}")
    for target in (0.80, 0.90, 0.95):
        kc = int(np.searchsorted(cum, target)) + 1
        # null: leave-one-family-out residual norms + residual vectors
        null_norms, null_vecs = [], []
        for hold in sorted(set(fams4)):
            tr = Xc[fams4 != hold]
            Ut, St, Vtt = np.linalg.svd(tr - tr.mean(0) + 0, full_matrices=False)
            Vk = Vtt[:kc]
            te = D4mat[fams4 == hold] - (tr + center).mean(0)
            resid = te - (te @ Vk.T) @ Vk
            null_norms.extend(np.linalg.norm(resid, axis=1))
            null_vecs.append(resid)
        null_norms = np.array(null_norms)
        null_vecs = np.concatenate(null_vecs)
        nmed = np.median(null_norms); np95 = np.percentile(null_norms, 95)
        Vk = Vt[:kc]
        def resid_of(X):
            Y = X - center
            return Y - (Y @ Vk.T) @ Vk
        # query sets
        post = {n: resid_of(v[20:40]) for n, v in d3.items()}
        pre = np.concatenate([resid_of(v[:20]) for v in d3.values()])
        park = np.concatenate([post[n][10:20] for n in d3 if c["ab"](n)])
        jumps = []
        for n, v in d3.items():
            step_sz = np.linalg.norm(np.diff(v[20:40], axis=0), axis=1)
            jumps.append(post[n][int(np.argmax(step_sz)) + 1])
        jumps = np.stack(jumps)
        allpost = np.concatenate(list(post.values()))
        res = pd.read_parquet(Path("data/lake") / c["cal"] / "residual_streams.parquet")
        res = res[(res["layer"] == c["L"]) & (res["token_position"] == 1)]
        calX = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)[:200]
        calr = resid_of(calX)
        line = [f"  k={kc} ({target:.0%}): null med {nmed:.0f} p95 {np95:.0f}"]
        for nm, Q in (("post-shift", allpost), ("jumps", jumps), ("park", park),
                      ("pre-shift", pre), ("CAL ctrl", calr)):
            nn = np.linalg.norm(Q, axis=1)
            line.append(f"{nm} {np.median(nn)/nmed:.2f}x(>p95 {(nn > np95).mean():.0%})")
        print(" | ".join(line))
        if target == 0.90:
            # Detector 2: systematic mean residual
            for nm, Q in (("post-shift", allpost), ("park", park), ("jumps", jumps)):
                m = np.linalg.norm(Q.mean(0))
                boots = [np.linalg.norm(null_vecs[rng.choice(len(null_vecs), len(Q), replace=True)].mean(0))
                         for _ in range(500)]
                p = float(np.mean([b >= m for b in boots]))
                print(f"    systematic ||mean resid|| {nm}: {m:.1f} vs null "
                      f"{np.median(boots):.1f} [p95 {np.percentile(boots, 95):.1f}] -> p={p:.3f}")
            # direction consistency across runs
            runmeans = np.stack([post[n].mean(0) for n in d3])
            runmeans /= (np.linalg.norm(runmeans, axis=1, keepdims=True) + 1e-9)
            cosm = (runmeans @ runmeans.T)[np.triu_indices(len(runmeans), 1)].mean()
            print(f"    direction consistency (mean pairwise cos of per-run mean residuals): {cosm:.2f}")

# ============================================================================
# FOLLOW-UPS RUN 2026-08-31 (inline first, results recorded here; rerunnable
# by uncommenting the calls in git history / see FINDINGS_FINAL F10):
# 1. CLUSTER-AWARE null (family-block bootstrap): systematic ||mean resid||
#    tank post 18.1 vs null p95 7.8; park 22.6; fr post 174.5 vs p95 26.9;
#    park 235.8 — all p<0.001. Magnitude = 25% (tank) / 38% (fr) of the raw
#    class separation (||muB-muA|| = 72 / 457).
# 2. Time course: rises over ~5 post-shift steps, persists undiminished to k=20.
#    cos with pre-shift residual direction: 0.24/0.26 (largely transition-specific;
#    pre-shift row is position-mismatched and serves as a second positive control).
# 3. D6 DISCRIMINATOR: pure cells +3.0/+21.4 (absent); mixed blocked +19.6/+127.6
#    (near-full D3 level -> substantially a mixed-context marker, present at
#    equilibrium); interleaved: tank +19.0 (order-insensitive) but fr +67.5 —
#    HALF the blocked level: fr's component partly encodes coherent shift
#    STRUCTURE, not mere class co-presence.
# 4. Behavior link at matched k: null (one p=.047 in 8 uncorrected tests; fr all
#    ns) — the marker does not predict behavior; the frame-axis reading remains
#    the behavior-relevant coordinate. P5c stays unsupported in modified form.
# ============================================================================
