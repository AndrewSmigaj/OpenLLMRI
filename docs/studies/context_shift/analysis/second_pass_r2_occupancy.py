#!/usr/bin/env python3
"""Second-pass review R2: occupancy (Items 2, 12) + shared secondary-axis instrument
(Item 17 step 0) + carrier-token positional profile (Item 6a).

Step 0: position-matched secondary axis — per layer, diff-of-class-means on D4 no-shift
        arm CARRIER states, band steps 11..40, labels = arm identity, leave-one-family-out
        accuracy. Saved to axes/secondary_axis_{probe}.npz for R3 re-renders.
2a:     dip-test power simulation at observed n / separation / spread.
2c:     WITHIN-STREAM occupancy on checkpoint windows (tank): per-position calibration
        from D4 ck windows (n=6/class), pooled class direction, d3 windows projected.
        ck20 = pre-shift content (control: content+history agree); ck30/ck40 = post-shift
        block (content = destination, history = mixed) — a content-controlled history test.
12a:    location+persistence across post-shift bands (carrier site, across-run population).
12b:    per-band 1-vs-2 GMM BIC.
6a:     class-separation profile across the 10 verbatim carrier tokens (identity-matched).
"""
from __future__ import annotations
import json, csv
from pathlib import Path
import numpy as np
import pandas as pd
import diptest
from sklearn.mixture import GaussianMixture
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import tank_cfg, fr_cfg

OUT = Path("docs/studies/context_shift/analysis")
rng = np.random.default_rng(11)

# ---------------- Step 0: secondary axis (carrier site, band-pooled) ----------------
def secondary_axis(probe):
    if probe == "tank":
        log, layers = "docs/studies/context_shift/captures/tank_d3_d4_log.tsv", range(24)
        d4f = lambda n: "_d4_" in n
        cls = lambda n: 0 if n.endswith("_a") else 1
        fam = lambda n: n.split("_")[2]
    else:
        log, layers = "docs/studies/context_shift/captures/fr_d3_d4_log.tsv", range(24)
        d4f = lambda n: "_d4_" in n and n.startswith("fr_s1_")
        cls = lambda n: 0 if n.endswith("_f") else 1
        fam = lambda n: n.split("_")[4]
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok" and d4f(r["run"])]
    arms = []
    for r in rows:
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[res["token_position"] == 1]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id")
        df = df[(df["pos"] >= 11)]
        arms.append((cls(r["run"]), fam(r["run"]), df))
    fams = sorted({f for _, f, _ in arms})
    out, accs = {}, {}
    for L in layers:
        def states(sel):
            X = []
            for c, f, df in arms:
                if not sel(c, f): continue
                d = df[df["residual_stream"].notna()]
                d = df[df.apply(lambda r: True, axis=1)]
                dl = df.merge(pd.DataFrame(), how="left", left_index=True, right_index=True) if False else df
                sub = df[df["layer"] == L] if "layer" in df.columns else df
                X.append((c, np.stack(sub[sub["layer"] == L]["residual_stream"].apply(np.asarray).to_numpy())))
            return X
        # simpler: collect per-arm layer states once
        acc_folds = []
        A_all, B_all = [], []
        per_arm = []
        for c, f, df in arms:
            sub = df[df["layer"] == L]
            X = np.stack(sub["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            per_arm.append((c, f, X))
            (A_all if c == 0 else B_all).append(X)
        muA = np.concatenate(A_all).mean(0); muB = np.concatenate(B_all).mean(0)
        axis = muB - muA; mid = (muA + muB) / 2.0
        denom = float(axis @ axis) ** 0.5
        axis = axis / max(denom, 1e-9)
        halfsep = float((muB - mid) @ axis)
        out[f"axis_{L}"] = axis; out[f"mid_{L}"] = mid; out[f"denom_{L}"] = halfsep
        for hold in fams:
            trA = np.concatenate([X for c, f, X in per_arm if c == 0 and f != hold])
            trB = np.concatenate([X for c, f, X in per_arm if c == 1 and f != hold])
            teA = np.concatenate([X for c, f, X in per_arm if c == 0 and f == hold])
            teB = np.concatenate([X for c, f, X in per_arm if c == 1 and f == hold])
            ax = trB.mean(0) - trA.mean(0); md = (trA.mean(0) + trB.mean(0)) / 2
            pa = (teA - md) @ ax; pb = (teB - md) @ ax
            acc_folds.append(((pa < 0).mean() + (pb > 0).mean()) / 2)
        accs[L] = float(np.mean(acc_folds))
    np.savez(OUT / "axes" / f"secondary_axis_{probe}.npz", **out)
    return accs

print("=" * 78)
print("STEP 0 — secondary axes (D4-arm identity, carrier site, band 11-40, LOFO accuracy)")
for probe in ("tank", "fr"):
    accs = secondary_axis(probe)
    line = " ".join(f"L{L}:{accs[L]:.2f}" for L in sorted(accs))
    print(f"{probe}: {line}")
    print(f"  (metric: balanced accuracy, chance 0.50, 6-fold leave-one-family-out, "
          f"n=30 states/class/fold test)")

# ---------------- 2a: dip power simulation ----------------
print("\n" + "=" * 78)
print("2a — dip-test power at observed n/separation/spread (2000 sims, alpha=.05)")
for tag, amp, sd in (("tank_L4", 1.99, 0.60), ("fr_L14", 0.88, 0.60)):
    for n in (24, 48, 120):
        for w in (1/3, 1/2):
            hits = 0
            for _ in range(2000):
                k = rng.binomial(n, w)
                x = np.concatenate([rng.normal(-amp, sd, k), rng.normal(+amp, sd, n - k)])
                if diptest.diptest(x)[1] < 0.05: hits += 1
            print(f"  {tag} n={n:>3} mix={w:.2f}: power {hits/2000:.2f}")

# ---------------- 2c: within-stream occupancy (tank checkpoint windows) ----------------
print("\n" + "=" * 78)
print("2c — WITHIN-STREAM occupancy, tank L4, per-position D4-calibrated window instrument")
L = 4
ckrows = [r for r in csv.DictReader(open("docs/studies/context_shift/captures/tank_ckpt_log.tsv"), delimiter="\t") if r["status"] == "ok"]
seen = set(); kept = []
for r in ckrows:
    if r["set"] not in seen: seen.add(r["set"]); kept.append(r)

def load_window(session):
    lake = Path("data/lake") / session
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] >= 2)].sort_values("token_position")
    X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    return X  # substring tokens only, in order; carrier = last 9 rows (verbatim)

win = {}
for r in kept:
    parts = r["set"].split("_")          # tank d3 fam00 ab ck30 / tank d4 fam00 a ck30
    kind, fam, arm, ck = parts[1], parts[2], parts[3], parts[4]
    win[(kind, fam, arm, ck)] = load_window(r["session"])

# RIGHT-ALIGNED windows: every substring ends with the same 9 carrier tokens, so aligning
# on the tail gives exact carrier alignment and recency-matched context alignment.
# (A first draft left-aligned to min length, misaligning the carrier tail across arms of
# different lengths — the 6a profile under that alignment was invalid.)
profile_store = {}
for ck in ("ck20", "ck30", "ck40"):
    d4A = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "a" and c == ck]
    d4B = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "b" and c == ck]
    m = min(min(x.shape[0] for x in d4A), min(x.shape[0] for x in d4B))
    A = np.stack([x[-m:] for x in d4A]); B = np.stack([x[-m:] for x in d4B])
    muA, muB = A.mean(0), B.mean(0)
    mid_p = (muA + muB) / 2.0
    diff = muB - muA
    ctx = slice(0, m - 9)                                  # all but the verbatim carrier
    v = diff[ctx].mean(0); v /= np.linalg.norm(v)
    denom_p = diff @ v
    dmed = np.median(denom_p[ctx])
    ok_p = np.where((np.arange(m) < m - 9) & (denom_p > 0.3 * dmed))[0]
    profile_store[ck] = (A, B, v, mid_p, denom_p, m)
    for a_ in ("ab", "ba"):
        vals, rec = [], []
        for (k, f, arm, c), X in win.items():
            if k != "d3" or c != ck or arm != a_: continue
            mm = min(X.shape[0], m)
            pp = ok_p[ok_p >= m - mm]
            r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom_p[pp]
            dest = +1.0 if a_ == "ab" else -1.0
            vals.extend((r_ * dest).tolist()); rec.append(((pp - (m - mm)) / mm, r_ * dest))
        x = np.asarray(vals)
        dip, pv = diptest.diptest(x)
        allp = np.concatenate([q for q, _ in rec]); allr = np.concatenate([r2 for _, r2 in rec])
        th = [allr[(allp >= lo) & (allp < hi)].mean() for lo, hi in ((0, 1/3), (1/3, 2/3), (2/3, 1.01))]
        print(f"  {ck} {a_}: n_tok={len(x)} (pos kept {len(ok_p)}/{m}); mean {x.mean():+.2f} "
              f"sd {x.std():.2f}; frac dest-side(>0) {(x > 0).mean():.2f}; "
              f"frac near-dest(>0.5) {(x > 0.5).mean():.2f}; dip p={pv:.3f}; "
              "thirds(old->new) " + " ".join(f"{t2:+.2f}" for t2 in th))

# ---------------- 6a: carrier-token d-prime profile (identity-matched) ----------------
print("\n" + "=" * 78)
print("6a — class-signal d' across the 9 verbatim carrier tokens (ck40 D4 windows, L4)")
A, B, v, mid_p, denom_p, m = profile_store["ck40"]
projA, projB = A @ v, B @ v
sep = projB.mean(0) - projA.mean(0)
sd = np.sqrt((projA.std(0) ** 2 + projB.std(0) ** 2) / 2) + 1e-9
dpr = sep / sd
toks = ["What", " is", " the", " meaning", " of", " the", " word", " tank", "?"]
print("  context-token d' median:", round(float(np.median(dpr[:m - 9])), 2),
      "(content differs by class; recency-aligned)")
for i in range(9):
    j = m - 9 + i
    print(f"    {toks[i]:>9}: sep {sep[j]:7.1f}  d' {dpr[j]:6.2f}")
sec = np.load(OUT / "axes" / "secondary_axis_tank.npz")[f"axis_{L}"]
pa, pb = A[:, m - 2] @ sec, B[:, m - 2] @ sec
print("  d' at ' tank' along SITE-SPECIFIC secondary axis:",
      round(float((pb.mean() - pa.mean()) / np.sqrt((pa.std() ** 2 + pb.std() ** 2) / 2)), 2),
      "(n=6/class)")

# ---------------- 12a/12b: location+persistence + GMM (carrier site, across-run) ----------------
print("\n" + "=" * 78)
print("12a/12b — carrier-site across-run occupancy: mode location, variance, 1v2 GMM")
tag, d4a, d4b, d3, dest_fn, fam_fn = tank_cfg()
A = np.stack(d4a); B = np.stack(d4b)
mid = (A.mean(0) + B.mean(0)) / 2.0
bands = {"k1-5": (0, 5), "k6-10": (5, 10), "k11-15": (10, 15), "k16-20": (15, 20), "k6-15": (5, 15)}
for sign, dname in ((+1.0, "ab(->+)"), (-1.0, "ba(->-)")):
    ys = np.stack([((d3[n] - mid) * sign)[20:40] for n in d3 if dest_fn(n) == sign])  # (12,20)
    dest_lv = float((((B if sign > 0 else A).mean(0) - mid) * sign)[30:40].mean())
    orig_lv = float((((A if sign > 0 else B).mean(0) - mid) * sign)[30:40].mean())
    print(f"\n  {dname}: D4 refs origin {orig_lv:+.2f} dest {dest_lv:+.2f}")
    for bn, (lo, hi) in bands.items():
        x = ys[:, lo:hi].flatten()
        # KDE mode
        grid = np.linspace(-3, 3, 601)
        kde = np.exp(-0.5 * ((grid[:, None] - x[None, :]) / 0.35) ** 2).sum(1)
        mode = float(grid[kde.argmax()])
        g1 = GaussianMixture(1, random_state=0).fit(x[:, None])
        g2 = GaussianMixture(2, random_state=0).fit(x[:, None])
        b1, b2 = g1.bic(x[:, None]), g2.bic(x[:, None])
        mus = sorted(g2.means_.flatten())
        print(f"    {bn:>6}: mode {mode:+.2f} sd {x.std():.2f} | GMM dBIC(1-2) {b1 - b2:+.1f} "
              f"{'(2 favored: mu=' + ','.join(f'{u:+.2f}' for u in mus) + ')' if b2 < b1 else '(1 favored)'}")
