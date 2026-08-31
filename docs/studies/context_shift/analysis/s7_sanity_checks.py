#!/usr/bin/env python3
"""Pre-QA sanity checks (S1.1-S1.5) — checks that can change conclusions.

S1.1 Two-timescale integrator M4 = w*integ(gf) + (1-w)*integ(gs), p=3, added to the
     per-run BIC battery + simulation controls. Threatens A3/A4 ("drift+jump").
S1.2 D6 cross-order validation: fit (g, amp) on one order branch, predict the other.
     Threatens B8 (no-stickiness could be a null overfit to its own test data).
S1.3 Behavior vs reading at MATCHED k. Threatens A10's causal wording.
S1.4 Residual-gap material check: calibration percentiles of D4 step-21-40 sentences
     vs D3 post-shift blocks. Threatens A3/B1 (weaker-material alternative).
S1.5 D5 cue-lexicon scope check: within-pair diff vs fiction-cue word count.
"""
import sys, json, csv, glob
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
from second_pass_r1_dynamics import (tank_cfg, fr_cfg, integrator_pred, fit_integrator,
                                     fit_step, fit_hybrid, bic, K)

rng = np.random.default_rng(21)

# ---------------- S1.1 two-timescale model ----------------
GF = np.arange(0.30, 0.951, 0.05)
GS = np.arange(0.90, 1.0001, 0.01)
W = np.arange(0.1, 0.91, 0.1)
def fit_twoscale(y, Ap, Am):
    best = (np.inf, None)
    cache = {}
    for g in set(np.round(np.concatenate([GF, GS]), 3)):
        cache[g] = integrator_pred(g, Ap, Am)
    for gf in GF:
        pf = cache[round(gf, 3)]
        for gs in GS:
            ps = cache[round(gs, 3)]
            for w in W:
                pred = w * pf + (1 - w) * ps
                rss = float(((y - pred) ** 2).sum())
                if rss < best[0]: best = (rss, (gf, gs, w))
    return best

def classify5(y, Ap, Am):
    r1, g = fit_integrator(y, Ap, Am)
    r2, s = fit_step(y)
    r3, h = fit_hybrid(y)
    r4, ts = fit_twoscale(y, Ap, Am)
    bics = {"integrator": bic(r1, 1), "step": bic(r2, 3), "hybrid": bic(r3, 4),
            "twoscale": bic(r4, 3)}
    order = sorted(bics, key=bics.get)
    delta = bics[order[1]] - bics[order[0]]
    return (order[0] if delta >= 2.0 else "indeterminate"), bics, delta, (g, s, h, ts)

def _run_battery():
    print("=" * 78)
    print("S1.1 — per-run BIC with two-timescale integrator added (threatens A4)")
    for cfgf, tag in ((tank_cfg, "tank_L4"), (fr_cfg, "fr_S1_L14")):
        tag2, d4a, d4b, d3, dest_fn, fam_fn = cfgf()
        A = np.stack(d4a); B = np.stack(d4b)
        mid = (A.mean(0) + B.mean(0)) / 2.0
        Ap = float((B.mean(0) - mid)[10:40].mean())
        labels, ts_params = [], []
        for name, proj in sorted(d3.items()):
            y = ((proj - mid) * dest_fn(name))[20:40]
            lab, bics, delta, fits = classify5(y, Ap, Ap)
            labels.append(lab)
            if lab == "twoscale": ts_params.append(fits[3][1])
        vc = pd.Series(labels).value_counts()
        print(f"  {tag}: " + ", ".join(f"{k}={v}" for k, v in vc.items()))
        if ts_params:
            gfs = [p[0] for p in ts_params]; gss = [p[1] for p in ts_params]; ws = [p[2] for p in ts_params]
            print(f"    twoscale medians: gf {np.median(gfs):.2f} gs {np.median(gss):.2f} w {np.median(ws):.2f}")
        # simulation controls: can the 5-way classifier tell twoscale from hybrid?
        sims = {"hybrid_truth": [], "twoscale_truth": [], "step_truth": []}
        for name, proj in sorted(d3.items())[:12]:
            y = ((proj - mid) * dest_fn(name))[20:40]
            rss_h, (c, *beta) = fit_hybrid(y)
            rss_t, (gf, gs, w) = fit_twoscale(y, Ap, Ap)
            rss_s, (cs, a_, b_) = fit_step(y)
            Xd = np.column_stack([np.ones(20), K, (K >= c).astype(float)])
            sd_h, sd_t, sd_s = np.sqrt(rss_h/20), np.sqrt(rss_t/20), np.sqrt(rss_s/20)
            for _ in range(2):
                sims["hybrid_truth"].append(classify5(Xd @ np.array(beta) + rng.normal(0, sd_h, 20), Ap, Ap)[0])
                pred_t = w * integrator_pred(gf, Ap, Ap) + (1 - w) * integrator_pred(gs, Ap, Ap)
                sims["twoscale_truth"].append(classify5(pred_t + rng.normal(0, sd_t, 20), Ap, Ap)[0])
                sims["step_truth"].append(classify5(np.where(K < cs, a_, b_) + rng.normal(0, sd_s, 20), Ap, Ap)[0])
        for truth, labs in sims.items():
            vc2 = pd.Series(labs).value_counts()
            print(f"    sim {truth} (n={len(labs)}): " + ", ".join(f"{k}={v}" for k, v in vc2.items()))

    # ---------------- S1.2 D6 cross-order validation ----------------
    print("\n" + "=" * 78)
    print("S1.2 — D6 cross-order validation (threatens B8)")
    def integ_cell(g, amp, k, order):
        vals = ([amp]*k + [-amp]*(20-k)) if order == "B_recent" else ([-amp]*(20-k) + [amp]*k)
        w = g ** np.arange(20)
        return float((w*np.array(vals)).sum()/w.sum())
    C = Path("docs/studies/context_shift/captures")
    for probe, log, L, axf, cfgf in (("tank", C/"d6_tank_log.tsv", 4,
                                      "axes_session_29a80932_aquarium_vs_vehicle_pos1.npz", tank_cfg),
                                     ("fr", C/"d6_fr_log.tsv", 14,
                                      "axes_session_5247081b_fictional_vs_real_pos1.npz", fr_cfg)):
        ax = np.load(f"docs/studies/context_shift/analysis/axes/{axf}")
        tag2, d4a, d4b, d3, dest_fn, fam_fn = cfgf()
        mid20 = float(((np.stack(d4a).mean(0)+np.stack(d4b).mean(0))/2)[19])
        rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"]=="ok"]
        readings = {}
        for r in rows:
            res = pd.read_parquet(Path("data/lake")/r["session"]/"residual_streams.parquet")
            res = res[(res["layer"]==L)&(res["token_position"]==1)]
            X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
            proj = float(2.0*((X[0]-ax[f"mid_{L}"])@ax[f"axis_{L}"])/float(ax[f"denom_{L}"]))
            p = r["set"].split("_")
            readings[(p[2], int(p[3][1:]), "_".join(p[4:]))] = proj - mid20
        fams = sorted({f for f,_,_ in readings})
        ks = list(range(2, 20, 2))
        curves = {o: np.array([np.mean([readings[(f,k,o)] for f in fams]) for k in ks])
                  for o in ("B_recent", "A_recent")}
        for fit_on, pred_on in (("A_recent","B_recent"), ("B_recent","A_recent")):
            best = (np.inf, None)
            for g in np.arange(0.60, 1.001, 0.005):
                for amp in np.arange(0.5, 3.01, 0.05):
                    rss = sum((curves[fit_on][i] - integ_cell(g, amp, k, fit_on))**2 for i,k in enumerate(ks))
                    if rss < best[0]: best = (rss, (g, amp))
            g, amp = best[1]
            pred = np.array([integ_cell(g, amp, k, pred_on) for k in ks])
            resid = curves[pred_on] - pred
            print(f"  {probe} fit-{fit_on[:1]}->predict-{pred_on[:1]}: g={g:.3f} amp={amp:.2f}; "
                  f"pred-branch rmse {np.sqrt((resid**2).mean()):.2f}, mean resid {resid.mean():+.2f} "
                  f"(branch spans ~{curves[pred_on].min():+.1f}..{curves[pred_on].max():+.1f})")

    # ---------------- S1.3 behavior vs reading at matched k ----------------
    print("\n" + "=" * 78)
    print("S1.3 — behavior vs reading WITHIN matched k (threatens A10 wording)")
    from scipy.stats import mannwhitneyu
    t = pd.read_csv("docs/studies/context_shift/analysis/r6_behavior_worksheet_tank_categorized.csv")
    t = t[t.k != "d4_final"]
    t["decided"] = t.category.isin(["aquarium", "vehicle"])
    t["dest_ans"] = (t.category == "vehicle") == t.set.str.contains("_ab_")   # answered destination sense
    for k in ("2", "6", "12", "20"):
        sub = t[t.k == k]
        dec, und = sub[sub.decided], sub[~sub.decided]
        # orient reading destination-positive
        r_or = np.where(sub.set.str.contains("_ab_"), sub.reading, -sub.reading)
        sub = sub.assign(r_or=r_or)
        dec, und = sub[sub.decided], sub[~sub.decided]
        if len(dec) and len(und):
            u, pv = mannwhitneyu(np.abs(dec.r_or), np.abs(und.r_or), alternative="greater")
            print(f"  tank k={k}: |reading| decided {np.abs(dec.r_or).median():.2f} (n={len(dec)}) vs "
                  f"undecided {np.abs(und.r_or).median():.2f} (n={len(und)}); MW p={pv:.3f}")
    f = pd.read_csv("docs/studies/context_shift/analysis/r6_behavior_worksheet_fr_categorized.csv")
    f = f[f.k != "d4_final"]
    f["fic"] = f.category == "fiction_frame"
    for k in ("2", "6", "12", "20"):
        sub = f[f.k == k]
        a, b = sub[sub.fic], sub[~sub.fic]
        if len(a) >= 2 and len(b) >= 2:
            u, pv = mannwhitneyu(a.reading, b.reading, alternative="less")
            print(f"  fr k={k}: reading fiction_frame {a.reading.median():+.2f} (n={len(a)}) vs "
                  f"safety {b.reading.median():+.2f} (n={len(b)}); MW p={pv:.3f}")

    # ---------------- S1.4 residual-gap material check ----------------
    print("\n" + "=" * 78)
    print("S1.4 — gap material check: D4 vs D3-post-shift sentence percentiles (tank)")
    ax = np.load("docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz")
    L = 4
    lake = Path("data/lake/session_29a80932")
    res = pd.read_parquet(lake/"residual_streams.parquet")
    res = res[(res["layer"]==L)&(res["token_position"]==1)]
    tok = pd.read_parquet(lake/"tokens.parquet", columns=["probe_id","input_text","label"])
    cal = res.merge(tok, on="probe_id")
    X = np.stack(cal["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    cal["reading"] = 2.0*((X-ax[f"mid_{L}"])@ax[f"axis_{L}"])/float(ax[f"denom_{L}"])
    cal["sentence"] = cal["input_text"].apply(lambda s: s.split(" What is the meaning")[0].strip())
    cmap = dict(zip(cal.sentence, cal.reading))
    bylab = {lab: np.sort(cal[cal.label==lab].reading.to_numpy()) for lab in cal.label.unique()}
    def pcts(run_glob, lo, hi, lab_fn):
        out = []
        for fpath in sorted(glob.glob(run_glob)):
            d = json.load(open(fpath))
            if "groups" not in d: continue
            cums = [s["text"].split(" What is the meaning")[0].strip() for g in d["groups"] for s in g["sentences"]]
            sents = [cums[0]] + [cums[i][len(cums[i-1]):].strip() for i in range(1, len(cums))]
            lab = lab_fn(d["name"])
            for s in sents[lo:hi]:
                r = cmap.get(s)
                if r is not None:
                    out.append(float(np.searchsorted(bylab[lab], r)/len(bylab[lab])))
        return np.array(out)
    d3v = pcts("data/sentence_sets/polysemy/context_shift_runs/tank_d3_*_ab.json", 20, 40, lambda n: "vehicle")
    d4v = pcts("data/sentence_sets/polysemy/context_shift_runs/tank_d4_*_b.json", 20, 40, lambda n: "vehicle")
    d3a = pcts("data/sentence_sets/polysemy/context_shift_runs/tank_d3_*_ba.json", 20, 40, lambda n: "aquarium")
    d4a_ = pcts("data/sentence_sets/polysemy/context_shift_runs/tank_d4_*_a.json", 20, 40, lambda n: "aquarium")
    for nm, d3x, d4x in (("vehicle-dest", d3v, d4v), ("aquarium-dest", d3a, d4a_)):
        u, pv = mannwhitneyu(d3x, d4x)
        print(f"  {nm}: D3-post median pct {np.median(d3x):.2f} (n={len(d3x)}) vs "
              f"D4 steps21-40 {np.median(d4x):.2f} (n={len(d4x)}); MW p={pv:.3f}")

    # ---------------- S1.5 D5 cue-lexicon check ----------------
    print("\n" + "=" * 78)
    print("S1.5 — D5 within-pair diff vs fiction-cue word count")
    piv = pd.read_csv("docs/studies/context_shift/analysis/r6_d5_pairs.csv")
    pairs = []
    for i in (1, 2, 3):
        pairs.extend(json.load(open(f"docs/studies/context_shift/generation/batches_d5/d5_batch{i}.json")))
    CUES = ["draft","chapter","scene","script","workshop","rehears","screen","novel","story","fic",
            "episode","act ","stage","playtest","beta reader","editor","manuscript","panel","storyboard",
            "audiobook","narrat","writer","page","outline","libretto","zine","anthology","serial","campaign"]
    cue_n = {p["pair_id"]: sum(p["fictional"].lower().count(c) for c in CUES) for p in pairs}
    piv["cues"] = piv.pair.map(cue_n)
    r = np.corrcoef(piv.cues, piv["diff"])[0,1]
    print(f"  corr(fiction-cue count, within-pair diff): r = {r:.2f} "
          f"(cue counts {piv.cues.min()}-{piv.cues.max()}, median {piv.cues.median():.0f})")
    lo = piv[piv.cues <= piv.cues.quantile(0.33)]; hi = piv[piv.cues >= piv.cues.quantile(0.67)]
    print(f"  low-cue tercile diff {lo['diff'].mean():+.2f} (n={len(lo)}) vs high-cue {hi['diff'].mean():+.2f} (n={len(hi)})")


if __name__ == "__main__":
    _run_battery()
