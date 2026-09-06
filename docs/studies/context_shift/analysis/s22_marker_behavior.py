#!/usr/bin/env python3
"""s22 — does the mixed-context marker predict behavior? Re-run on the v2 categories.

Written 6 September 2026, before running. The original eight tests (31 August 2026)
were run inline with the superseded 256-token categories and their code was not
committed (s8_subspace_geometry.py records the result only: one p = .047 in 8
uncorrected tests). The test form is therefore fixed here, before the numbers:

  Marker score per behavior cell, exactly as the held-out mixture cells are scored in
  s9_figures.py: the D4 no-shift PCA subspace at the calibrated site (positions
  21-40 of the 12 no-shift runs, 90% variance), the residual of the cell's state
  outside that subspace, projected on the shared transition direction vdir (the mean
  post-shift residual of the D3 transition runs), in percent of the raw class
  separation (SEP = 72 tank, 457 fr).

  Pre-stated tests (eight): per task x post-shift count k in {2, 6, 12, 20}, over
  delivered answers only, two-sided Mann-Whitney U of the marker score between the two
  outcome classes -- tank: one sense (aquarium or vehicle) vs both senses;
  fiction/real: fiction-writing assistance vs safe completion -- with rank AUC
  (P(score_class1 > score_class2)). p-values reported uncorrected and Holm-adjusted
  over the eight. Cell counts printed with every test. The fiction/real tests are
  underpowered (8 fiction-writing answers over four k's) and are reported as such.

  Exploratory block (new, not pre-stated): marker score for delivered vs no-answer
  (looping) cells, per task, pooled over k and per k, same test.

Outputs: analysis/s22_marker_behavior.csv (per-cell scores and categories, no text)
and printed tables. Run from the repository root with the project venv.
"""
import csv, json, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu

A = Path("docs/studies/context_shift/analysis")
C = Path("docs/studies/context_shift/captures")
SEP = {"tank": 72.0, "fr": 457.0}
KS = (2, 6, 12, 20)


def load_raw(log, L, keep):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    out = {}
    for r in rows:
        n = r["run"]
        if not keep(n):
            continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        out[n] = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    return out


def cell_state(session, L):
    res = pd.read_parquet(Path("data/lake") / session / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] == 1)]
    X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
    return X[0]


def mwu(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 1 or len(b) < 1:
        return np.nan, np.nan
    u, p = mannwhitneyu(a, b, alternative="two-sided")
    return float(u / (len(a) * len(b))), float(p)


def holm(ps):
    ps = np.asarray(ps, float)
    order = np.argsort(ps)
    adj = np.empty_like(ps)
    m = len(ps)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * ps[i])
        adj[i] = min(1.0, running)
    return adj


CFG = {
    "tank": dict(log=C / "tank_d3_d4_log.tsv", L=4,
                 d3k=lambda n: "_d3_" in n, d4k=lambda n: "_d4_" in n,
                 ws=A / "r6_behavior_worksheet_tank_v2_categorized.csv",
                 one=("aquarium", "vehicle"), both=("both",),
                 c1=("aquarium", "vehicle"), c2=("both",), names=("one sense", "both senses")),
    "fr": dict(log=C / "fr_d3_d4_log.tsv", L=14,
               d3k=lambda n: "fr_s1_" in n and "_d3_" in n,
               d4k=lambda n: "fr_s1_" in n and "_d4_" in n,
               ws=A / "r6_behavior_worksheet_fr_v2_categorized.csv",
               c1=("fiction_frame",), c2=("safety_response",),
               names=("fiction-writing assistance", "safe completion")),
}

rows_out, tests = [], []
for task, c in CFG.items():
    L = c["L"]
    d4 = load_raw(c["log"], L, c["d4k"]); d3 = load_raw(c["log"], L, c["d3k"])
    D4mat = np.concatenate([v[20:40] for v in d4.values()])
    center = D4mat.mean(0)
    _, S, Vt = np.linalg.svd(D4mat - center, full_matrices=False)
    cum = np.cumsum(S ** 2 / (S ** 2).sum()); kc = int(np.searchsorted(cum, 0.90)) + 1
    Vk = Vt[:kc]

    def resid_of(X):
        Y = np.atleast_2d(X) - center
        return Y - (Y @ Vk.T) @ Vk

    post = {n: resid_of(v[20:40]) for n, v in d3.items()}
    allpost = np.concatenate(list(post.values()))
    vdir = allpost.mean(0); vdir /= np.linalg.norm(vdir)
    print(f"### {task}: D4 subspace k={kc} (90% var), {len(d4)} no-shift runs, {len(d3)} transition runs",
          flush=True)

    ws = pd.read_csv(c["ws"])
    ws["k"] = pd.to_numeric(ws["k"], errors="coerce")
    for i, r in ws.iterrows():
        x = cell_state(r["session"], L)
        score = float(resid_of(x)[0] @ vdir) / SEP[task] * 100
        rows_out.append(dict(task=task, set=r["set"], session=r["session"], run=r["run"],
                             k=r["k"], category=r["category"], reading=r["reading"],
                             marker_pct=round(score, 3)))
    df = pd.DataFrame([x for x in rows_out if x["task"] == task])
    print(f"  scored {len(df)} cells; marker mean by category:")
    print(df.groupby("category")["marker_pct"].agg(["count", "mean", "median"]).round(2).to_string())

    # pre-stated eight tests (four per task)
    for k in KS:
        sub = df[(df["k"] == k) & (df["category"] != "no_answer")]
        a = sub[sub["category"].isin(c["c1"])]["marker_pct"]
        b = sub[sub["category"].isin(c["c2"])]["marker_pct"]
        auc, p = mwu(a, b)
        tests.append(dict(task=task, k=k, n1=len(a), n2=len(b), auc=auc, p=p,
                          med1=float(np.median(a)) if len(a) else np.nan,
                          med2=float(np.median(b)) if len(b) else np.nan))

    # exploratory: delivered vs no-answer
    print(f"  exploratory (new): delivered vs no-answer, {task}")
    tr = df[df["k"].isin(KS)]
    for label, sub in [("pooled k", tr)] + [(f"k={k}", tr[tr["k"] == k]) for k in KS]:
        a = sub[sub["category"] != "no_answer"]["marker_pct"]
        b = sub[sub["category"] == "no_answer"]["marker_pct"]
        auc, p = mwu(a, b)
        print(f"    {label:9s} delivered n={len(a):3d} med {np.median(a) if len(a) else np.nan:6.2f} | "
              f"no-answer n={len(b):3d} med {np.median(b) if len(b) else np.nan:6.2f} | "
              f"AUC(delivered>no-answer) {auc:.2f} p={p:.3f}")

T = pd.DataFrame(tests)
T["p_holm"] = holm(T["p"].fillna(1.0).values)
print("\n### Pre-stated tests: marker score by delivered outcome class at matched k")
for _, t in T.iterrows():
    n1, n2 = CFG[t["task"]]["names"]
    print(f"  {t['task']:4s} k={int(t['k']):2d}  {n1} n={int(t['n1'])} med {t['med1']:6.2f} | "
          f"{n2} n={int(t['n2'])} med {t['med2']:6.2f} | AUC {t['auc']:.2f} | "
          f"p={t['p']:.3f} (Holm {t['p_holm']:.3f})")
hits = int((T["p"] < 0.05).sum())
print(f"  {hits} of {len(T)} uncorrected tests at p < .05; "
      f"{int((T['p_holm'] < 0.05).sum())} after Holm.")

pd.DataFrame(rows_out).to_csv(A / "s22_marker_behavior.csv", index=False)
T.to_csv(A / "s22_marker_behavior_tests.csv", index=False)
print("wrote analysis/s22_marker_behavior.csv and s22_marker_behavior_tests.csv")
