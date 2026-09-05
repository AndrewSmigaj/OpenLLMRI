#!/usr/bin/env python3
"""QA Block A materialization — the four number sources that previously existed only as
inline session snippets (a regenerability FAIL, fixed by this script). Seeds preserved.

(i)   F10 cluster-aware systematic test + held-out direction estimation (rng 41; even/odd
      family split) — doc numbers: tank 18.1 vs null p95 7.8, park 22.6; fr 174.5 vs
      26.9, park 235.8; held-out 12.8/13.7 (tank), 151.9/157.3 (fr).
(ii)  Letter-site midref battery — amp 1.18, mid drift +0.07, gaps 0.90/0.33 amp (n=4/dir).
(iii) D7 bare-carrier readings — q1 +0.82, q1b +0.65, s1 -1.27, s2 -1.20, s3 +0.81.
(iv)  F10 family-split (D6 pure cells, novel vs subspace families) — tank +1.6 vs +6.7,
      fr +3.4 vs +6.0 (% of separation).
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
WS = "_v2"  # behavior worksheet version: "" = frozen 256-token captures, "_v2" = regenerated (Sept 2026)


C = Path("docs/studies/context_shift/captures")
AXD = Path("docs/studies/context_shift/analysis/axes")

def load_raw(log, L, keep, run_col="run"):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    out = {}
    for r in rows:
        n = r[run_col]
        if not keep(n): continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c).get("position", 0)))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        out[n] = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    return out

def fit_subspace(D4mat, var_target=0.90):
    """PCA subspace of a reference cloud + out-of-subspace residual fn (QA-extracted)."""
    center = D4mat.mean(0)
    _, S, Vt = np.linalg.svd(D4mat - center, full_matrices=False)
    cum = np.cumsum(S ** 2 / (S ** 2).sum())
    kc = int(np.searchsorted(cum, var_target)) + 1
    Vk = Vt[:kc]
    def resid_of(X):
        Y = np.atleast_2d(X) - center
        return Y - (Y @ Vk.T) @ Vk
    return center, Vk, resid_of


def marker_setup(log, L, d3k, d4k):
    d4 = load_raw(log, L, d4k); d3 = load_raw(log, L, d3k)
    D4mat = np.concatenate([v[20:40] for v in d4.values()])
    center, Vk, resid_of = fit_subspace(D4mat, 0.90)
    kc = Vk.shape[0]
    return d3, d4, D4mat, center, Vk, kc, resid_of

CFG = {
    "tank": dict(log=C / "tank_d3_d4_log.tsv", L=4, sep=72.0,
                 d3k=lambda n: "_d3_" in n, d4k=lambda n: "_d4_" in n,
                 fam=lambda n: n.split("_")[2], famint=lambda n: int(n.split("_")[2][3:]),
                 ab=lambda n: n.endswith("_ab"), d6log=C / "d6_tank_log.tsv"),
    "fr": dict(log=C / "fr_d3_d4_log.tsv", L=14, sep=457.0,
               d3k=lambda n: "fr_s1_" in n and "_d3_" in n,
               d4k=lambda n: "fr_s1_" in n and "_d4_" in n,
               fam=lambda n: n.split("_")[4], famint=lambda n: int(n.split("_")[4][3:]),
               ab=lambda n: n.endswith("_fr"), d6log=C / "d6_fr_log.tsv"),
}

def _run():
    print("=" * 74)
    print("(i) F10 cluster-aware systematic test + held-out direction (rng 41)")
    rng = np.random.default_rng(41)
    for tag, c in CFG.items():
        d3, d4, D4mat, center, Vk, kc, resid_of = marker_setup(c["log"], c["L"], c["d3k"], c["d4k"])
        fams4 = np.concatenate([[c["fam"](n)] * 20 for n in d4])
        null_by_fam = {}
        for hold in sorted(set(fams4)):
            tr = (D4mat - center)[fams4 != hold]
            _, _, Vtt = np.linalg.svd(tr, full_matrices=False)
            Vh = Vtt[:kc]
            te = D4mat[fams4 == hold] - center
            null_by_fam[hold] = te - (te @ Vh.T) @ Vh
        fam_keys = list(null_by_fam)
        post = {n: resid_of(v[20:40]) for n, v in d3.items()}
        park = np.concatenate([post[n][10:20] for n in d3 if c["ab"](n)])
        allpost = np.concatenate(list(post.values()))
        for nm, Q, ncl in (("post-shift", allpost, len(d3)), ("park", park, sum(1 for n in d3 if c["ab"](n)))):
            m = np.linalg.norm(Q.mean(0))
            per = len(Q) // ncl
            boots = []
            for _ in range(1000):
                pick = rng.choice(fam_keys, ncl, replace=True)
                sel = np.concatenate([null_by_fam[f][rng.choice(len(null_by_fam[f]), per, replace=True)] for f in pick])
                boots.append(np.linalg.norm(sel.mean(0)))
            p = float(np.mean([b >= m for b in boots]))
            print(f"  {tag} ||mean resid|| {nm}: {m:.1f} vs null med {np.median(boots):.1f} "
                  f"[p95 {np.percentile(boots, 95):.1f}] -> p={p:.3f}")
        vfull = allpost.mean(0); magf = np.linalg.norm(vfull)
        runs = list(post)
        even = [n for n in runs if c["famint"](n) % 2 == 0]; odd = [n for n in runs if c["famint"](n) % 2 == 1]
        for est, test, nm in ((even, odd, "even->odd"), (odd, even, "odd->even")):
            vd = np.concatenate([post[n] for n in est]).mean(0); vd /= np.linalg.norm(vd)
            proj = float(np.concatenate([post[n] for n in test]).mean(0) @ vd)
            print(f"  {tag} held-out {nm}: {proj:.1f} (in-sample {magf:.1f})")

    print("\n" + "=" * 74)
    print("(ii) letter-site midref battery (S3 D4 arms, L14)")
    ax = np.load(AXD / "axes_session_c913da46_fictional_vs_real_pos1.npz")
    L = 14
    from second_pass_r1_dynamics import load_runs
    d3s3 = load_runs(str(C / "fr_d3_d4_log.tsv"), str(AXD / "axes_session_c913da46_fictional_vs_real_pos1.npz"),
                     L, name_filter=lambda n: n.startswith("fr_s3_") and "_d3_" in n)
    arms = {}
    for r in csv.DictReader(open(C / "fr_s3_d4_log.tsv"), delimiter="\t"):
        if r["status"] != "ok": continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda cj: int(json.loads(cj).get("position", 0)))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
        arms[r["set"]] = 2.0 * ((X - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"])
    A = np.stack([v for k, v in arms.items() if k.endswith("_f")])
    B = np.stack([v for k, v in arms.items() if k.endswith("_r")])
    mid = (A.mean(0) + B.mean(0)) / 2
    amp = float((B.mean(0) - mid)[10:40].mean())
    print(f"  letter-site: {len(A)}f+{len(B)}r arms; amplitude {amp:.2f}; mid(band) {mid[10:40].mean():+.2f}")
    for dsuf, sign in (("_fr", +1.0), ("_rf", -1.0)):
        ys = np.stack([(d3s3[n] - mid) * sign for n in d3s3 if n.endswith(dsuf)])
        dest_lv = float((((B if sign > 0 else A).mean(0) - mid) * sign)[35:40].mean())
        gap = dest_lv - ys[:, 35:40].mean()
        kx = next((i + 1 for i, v in enumerate(ys.mean(0)[20:40]) if v > 0), None)
        print(f"  {dsuf}: cross k={kx}; gap {gap:+.2f} ({gap/amp:.2f} amp) n={len(ys)}")

    print("\n" + "=" * 74)
    print("(iii) D7 bare-carrier readings")
    AXES = {"q1": ("axes_session_29a80932_aquarium_vs_vehicle_pos1.npz", 4),
            "q1b": ("axes_session_29a80932_aquarium_vs_vehicle_pos1.npz", 4),
            "s1": ("axes_session_5247081b_fictional_vs_real_pos1.npz", 14),
            "s2": ("axes_session_589557e1_fictional_vs_real_pos1.npz", 14),
            "s3": ("axes_session_c913da46_fictional_vs_real_pos1.npz", 14)}
    for r in csv.DictReader(open(C / "d7_log.tsv"), delimiter="\t"):
        if r["status"] != "ok": continue
        cid = r["set"].replace("d7_bare_", "")
        axf, Lb = AXES[cid]
        axb = np.load(AXD / axf)
        res = pd.read_parquet(Path("data/lake") / r["session"] / "residual_streams.parquet")
        res = res[(res["layer"] == Lb) & (res["token_position"] == 1)]
        X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
        v = float(2.0 * ((X[0] - axb[f"mid_{Lb}"]) @ axb[f"axis_{Lb}"]) / float(axb[f"denom_{Lb}"]))
        print(f"  {cid:>4}: {v:+.2f}")

    print("\n" + "=" * 74)
    print("(iv) F10 family-split: D6 pure cells, D4-subspace fams vs novel fams")
    D4FAMS = {0, 2, 4, 6, 8, 10}
    for tag, c in CFG.items():
        d3, d4, D4mat, center, Vk, kc, resid_of = marker_setup(c["log"], c["L"], c["d3k"], c["d4k"])
        allpost = np.concatenate([resid_of(v[20:40]) for v in d3.values()])
        vdir = allpost.mean(0); vdir /= np.linalg.norm(vdir)
        ins, out_ = [], []
        for r in csv.DictReader(open(c["d6log"]), delimiter="\t"):
            if r["status"] != "ok": continue
            p2 = r["set"].split("_"); k = int(p2[3][1:])
            if k not in (0, 20): continue
            fam = int(p2[2][3:])
            res = pd.read_parquet(Path("data/lake") / r["session"] / "residual_streams.parquet")
            res = res[(res["layer"] == c["L"]) & (res["token_position"] == 1)]
            X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
            v = float(resid_of(X[0])[0] @ vdir) / c["sep"] * 100
            (ins if fam in D4FAMS else out_).append(v)
        print(f"  {tag}: subspace fams {np.mean(ins):+.1f} (n={len(ins)}) vs novel {np.mean(out_):+.1f} (n={len(out_)})")


if __name__ == "__main__":
    _run()


def _run_extra():
    """(v)-(vii): further inline-only numbers materialized during QA Block A."""
    import numpy as np, pandas as pd
    from scipy.stats import mannwhitneyu, ttest_1samp
    OUT = Path("docs/studies/context_shift/analysis")
    print("\n" + "=" * 74)
    print("(v) F7 pooled mid-k behavior test (tank, k in {6,12})")
    t = pd.read_csv(OUT / f"r6_behavior_worksheet_tank{WS}_categorized.csv")
    t = t[t.k.isin(["6", "12"])]
    r_or = np.abs(np.where(t.set.str.contains("_ab_"), t.reading, -t.reading))
    dec = t.category.isin(["aquarium", "vehicle"]).to_numpy()
    u, p = mannwhitneyu(r_or[dec], r_or[~dec], alternative="greater")
    print(f"  decided med {np.median(r_or[dec]):.2f} (n={dec.sum()}) vs undecided "
          f"{np.median(r_or[~dec]):.2f} (n={(~dec).sum()}); MW one-sided p={p:.4f}")
    print("\n(vi) D5 domain-clustered test + batch means")
    piv = pd.read_csv(OUT / "r6_d5_pairs.csv")
    dm = piv.groupby("domain")["diff"].mean()
    tt = ttest_1samp(dm, 0)
    piv["batch"] = piv.pair.str[0].map({"A": 1, "B": 1, "C": 2, "D": 2, "E": 3, "F": 3})
    bm = piv.groupby("batch")["diff"].mean()
    print(f"  domain means {[round(v,2) for v in dm.values]}; t={tt.statistic:.1f}, "
          f"p={tt.pvalue:.2e}; batch means {[round(v,2) for v in bm.values]}")
    print("\n(vii) within-stream display-clip counts + trimmed vs untrimmed ck means (tank L4)")
    import csv as _csv, json as _json
    rows = [r for r in _csv.DictReader(open(C / "tank_ckpt_log.tsv"), delimiter="\t") if r["status"] == "ok"]
    seen = set(); kept = []
    for r in rows:
        if r["set"] not in seen: seen.add(r["set"]); kept.append(r)
    def loadw(sess):
        res = pd.read_parquet(Path("data/lake") / sess / "residual_streams.parquet")
        res = res[(res["layer"] == 4) & (res["token_position"] >= 2)].sort_values("token_position")
        return np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    win = {}
    for r in kept:
        p2 = r["set"].split("_")
        win[(p2[1], p2[2], p2[3], p2[4])] = loadw(r["session"])
    for ck in ("ck20", "ck30", "ck40"):
        d4A = [v for (k, f, a, c2), v in win.items() if k == "d4" and a == "a" and c2 == ck]
        d4B = [v for (k, f, a, c2), v in win.items() if k == "d4" and a == "b" and c2 == ck]
        m = min(min(x.shape[0] for x in d4A), min(x.shape[0] for x in d4B))
        A = np.stack([x[-m:] for x in d4A]); B = np.stack([x[-m:] for x in d4B])
        mid_p = (A.mean(0) + B.mean(0)) / 2; diff = B.mean(0) - A.mean(0)
        ctx = slice(0, m - 9)
        v = diff[ctx].mean(0); v /= np.linalg.norm(v)
        denom = diff @ v
        ok = np.where((np.arange(m) < m - 9) & (denom > 0.3 * np.median(denom[ctx])))[0]
        for a_ in ("ab", "ba"):
            vals = []
            for (k, f, arm, c2), X in win.items():
                if k != "d3" or c2 != ck or arm != a_: continue
                mm = min(X.shape[0], m)
                pp = ok[ok >= m - mm]
                r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom[pp]
                vals.extend((r_ * (+1 if a_ == "ab" else -1)).tolist())
            x = np.asarray(vals)
            clip = int((np.abs(x) > 6).sum())
            xt = x[np.abs(x) <= 6]
            print(f"  {ck} {a_}: untrimmed mean {x.mean():+.3f} | trimmed(|r|<=6) {xt.mean():+.3f} "
                  f"| clipped-for-display {clip}/{len(x)} ({clip/len(x):.1%})")


if __name__ == "__main__":
    _run_extra()


def _run_marker_orthogonality():
    """(viii) paper-drafting verification: the mixed-context marker direction is
    orthogonal to BOTH class axes — calibration (measured s9: +0.015/+0.011) and
    secondary accumulated-context (by construction; verified: tank -0.0052, fr -0.0065)."""
    for tag, log, L, secf, d3k, d4k in (
        ("tank", C / "tank_d3_d4_log.tsv", 4, "secondary_axis_tank.npz",
         lambda n: "_d3_" in n, lambda n: "_d4_" in n),
        ("fr", C / "fr_d3_d4_log.tsv", 14, "secondary_axis_fr.npz",
         lambda n: "fr_s1_" in n and "_d3_" in n, lambda n: "fr_s1_" in n and "_d4_" in n)):
        d4 = load_raw(log, L, d4k); d3 = load_raw(log, L, d3k)
        D4mat = np.concatenate([v[20:40] for v in d4.values()])
        center, Vk, resid_of = fit_subspace(D4mat, 0.90)
        allpost = np.concatenate([resid_of(v[20:40]) for v in d3.values()])
        vdir = allpost.mean(0); vdir /= np.linalg.norm(vdir)
        sec = np.load(AXD / secf)[f"axis_{L}"]
        print(f"  {tag}: cos(marker, secondary axis) = {float(vdir @ sec):+.4f}")


if __name__ == "__main__":
    _run_marker_orthogonality()
