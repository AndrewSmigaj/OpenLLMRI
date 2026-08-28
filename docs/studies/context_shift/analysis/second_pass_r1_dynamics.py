#!/usr/bin/env python3
"""Second-pass review R1: per-run dynamics mechanics (Items 1, 4, 10, 13).

Per run (tank L4 pos1; fr S1 L14 pos1), midpoint-referenced and destination-oriented:
  - uniform-integrator null comparison (Item 1a)
  - BIC model selection: fitted-gamma recency integrator vs change-point step vs
    drift+step hybrid (Item 1b); largest-step/path metrics (Item 13a)
  - synthetic pure-step simulation control through the same classifier (Item 1c)
  - two-phase test on direction means (Item 10a)
  - residual gap vs position-matched D4 destination level, family-clustered
    bootstrap CIs (Item 10b/c)
  - Item 4 arithmetic at k=20 under actual amplitudes
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
OUT = Path("docs/studies/context_shift/analysis")
FIG = Path("docs/studies/context_shift/figures")

def load_runs(log_path, axes_path, layer, name_filter=None):
    ax = np.load(axes_path)
    axis, mid, den = ax[f"axis_{layer}"], ax[f"mid_{layer}"], float(ax[f"denom_{layer}"])
    log = pd.read_csv(log_path, sep="\t")
    runs = {}
    for _, r in log.iterrows():
        name = r["run"]
        if name_filter and not name_filter(name):
            continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == layer) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        X = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
        proj = 2.0 * ((X - mid) @ axis) / den
        runs[name] = proj[np.argsort(df["pos"].to_numpy())] if not np.all(np.diff(df["pos"]) > 0) else proj
    return runs

# ---------- probe configs ----------
def tank_cfg():
    runs = load_runs("docs/studies/context_shift/captures/tank_d3_d4_log.tsv",
                     "docs/studies/context_shift/analysis/axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz", 4)
    d4a = [v for k, v in runs.items() if "_d4_" in k and k.endswith("_a")]   # aquarium (-)
    d4b = [v for k, v in runs.items() if "_d4_" in k and k.endswith("_b")]   # vehicle (+)
    d3 = {k: v for k, v in runs.items() if "_d3_" in k}
    def dest(name): return +1.0 if name.endswith("_ab") else -1.0            # ab -> vehicle(+)
    def fam(name): return name.split("_")[2]
    return "tank_L4", d4a, d4b, d3, dest, fam

def fr_cfg():
    runs = load_runs("docs/studies/context_shift/captures/fr_d3_d4_log.tsv",
                     "docs/studies/context_shift/analysis/axes/axes_session_5247081b_fictional_vs_real_pos1.npz", 14,
                     name_filter=lambda n: n.startswith("fr_s1_"))
    d4a = [v for k, v in runs.items() if "_d4_" in k and k.endswith("_f")]   # fictional (-)
    d4b = [v for k, v in runs.items() if "_d4_" in k and k.endswith("_r")]   # real (+)
    d3 = {k: v for k, v in runs.items() if "_d3_" in k}
    def dest(name): return +1.0 if name.endswith("_fr") else -1.0            # fr -> real(+)
    def fam(name): return name.split("_")[4]
    return "fr_S1_L14", d4a, d4b, d3, dest, fam

# ---------- models on y(k), k=1..20 ----------
K = np.arange(1, 21)

def integrator_pred(gamma, Ap, Am):
    # weights gamma^age; new sentences ages 0..k-1 (value +Ap), old ages k..k+19 (value -Am)
    preds = np.empty(20)
    for i, k in enumerate(K):
        ages = np.arange(k + 20)
        w = gamma ** ages
        vals = np.concatenate([np.full(k, Ap), np.full(20, -Am)])
        preds[i] = (w * vals).sum() / w.sum()
    return preds

def fit_integrator(y, Ap, Am):
    best = (np.inf, None)
    for g in np.arange(0.30, 1.201, 0.005):
        rss = float(((y - integrator_pred(g, Ap, Am)) ** 2).sum())
        if rss < best[0]: best = (rss, g)
    return best  # (rss, gamma)

def fit_step(y):
    best = (np.inf, None)
    for c in range(2, 21):
        a, b = y[:c - 1].mean(), y[c - 1:].mean()
        pred = np.where(K < c, a, b)
        rss = float(((y - pred) ** 2).sum())
        if rss < best[0]: best = (rss, (c, a, b))
    return best

def fit_hybrid(y):
    best = (np.inf, None)
    for c in range(2, 21):
        Xd = np.column_stack([np.ones(20), K, (K >= c).astype(float)])
        beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
        rss = float(((y - Xd @ beta) ** 2).sum())
        if rss < best[0]: best = (rss, (c, *beta))
    return best

def bic(rss, p, n=20):
    return n * np.log(max(rss, 1e-9) / n) + p * np.log(n)

def classify(y, Ap, Am):
    r1, g = fit_integrator(y, Ap, Am)
    r2, s = fit_step(y)
    r3, h = fit_hybrid(y)
    bics = {"integrator": bic(r1, 1), "step": bic(r2, 3), "hybrid": bic(r3, 4)}
    order = sorted(bics, key=bics.get)
    delta = bics[order[1]] - bics[order[0]]
    label = order[0] if delta >= 2.0 else "indeterminate"
    return label, bics, delta, g, s, (r1, r2, r3)

def path_metrics(y):
    d = np.abs(np.diff(y))
    net = abs(y[-1] - y[0])
    return {"largest_over_net": float(d.max() / net) if net > 1e-9 else np.nan,
            "largest_over_path": float(d.max() / d.sum()) if d.sum() > 1e-9 else np.nan}

# ---------- main per-probe battery ----------
def battery(tag, d4a, d4b, d3, dest_fn, fam_fn, rng):
    print("=" * 78); print(f"### {tag}: n_d3={len(d3)}, d4 arms {len(d4a)}+{len(d4b)}")
    A = np.stack(d4a); B = np.stack(d4b)
    mid = (A.mean(0) + B.mean(0)) / 2.0                    # position-matched midpoint
    band = slice(10, 40)                                   # steps 11..40
    ApB = float((B.mean(0) - mid)[band].mean())            # +class amplitude (band)
    AmA = float((mid - A.mean(0))[band].mean())            # -class amplitude (band)
    print(f"band amplitudes (midref): +side {ApB:.2f}, -side {AmA:.2f}; mid(band) {mid[band].mean():+.2f}")

    rows, sim_pool = [], []
    for name, proj in sorted(d3.items()):
        dest = dest_fn(name)
        y = ((proj - mid) * dest)[20:40]                   # k=1..20, destination-positive
        Ap = ApB if dest > 0 else AmA                      # destination amplitude
        Am = AmA if dest > 0 else ApB                      # origin amplitude
        null = integrator_pred(1.0, Ap, Am)                # uniform null
        label, bics, delta, g, s, rsss = classify(y, Ap, Am)
        pm = path_metrics(y)
        # position-matched destination D4 level, k=16..20
        Dmat = (B if dest > 0 else A)
        A_dest_t = ((Dmat.mean(0) - mid) * dest)[35:40].mean()
        gap = float(A_dest_t - y[15:20].mean())
        rows.append({"run": name, "fam": fam_fn(name), "dest": "+" if dest > 0 else "-",
                     "frac_ahead": float((y > null).mean()), "mean_lead": float((y - null).mean()),
                     "class": label, "dBIC": round(delta, 1), "gamma": s and round(g, 3),
                     "step_c": s[0] if label in ("step", "hybrid", "indeterminate") else None,
                     "resid_gap": round(gap, 3), **{k: round(v, 3) for k, v in pm.items()},
                     "y20": round(float(y[19]), 3), "null20": round(float(null[19]), 3)})
        sim_pool.append((fit_step(y), y))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"r1_model_selection_{tag}.csv", index=False)
    print("\n-- Item 1a: per-run uniform-null comparison --")
    print(f"runs fully ahead (frac_ahead=1.0): {(df.frac_ahead == 1.0).sum()}/{len(df)}; "
          f"majority-ahead (>0.5): {(df.frac_ahead > 0.5).sum()}/{len(df)}; "
          f"mean lead {df.mean_lead.mean():+.2f} (per-run range {df.mean_lead.min():+.2f}..{df.mean_lead.max():+.2f})")
    print("\n-- Item 1b: model classes --")
    print(df["class"].value_counts().to_string())
    print("median |dBIC| best-vs-2nd:", round(df.dBIC.median(), 1))
    for d in ("+", "-"):
        sub = df[df.dest == d]
        print(f"  dest {d}: " + ", ".join(f"{k}={v}" for k, v in sub["class"].value_counts().items()),
              f"| gamma median {sub.gamma.median():.3f}")
    print("\n-- Item 13a: path metrics --")
    print(f"largest/net > 0.5 (jump-dominant): {(df.largest_over_net > 0.5).sum()}/{len(df)}; "
          f"largest/path median {df.largest_over_path.median():.2f}")
    print("\n-- Item 4 arithmetic at k=20 --")
    for d in ("+", "-"):
        sub = df[df.dest == d]
        print(f"  dest {d}: observed y(20) {sub.y20.mean():+.2f} vs uniform null {sub.null20.mean():+.2f}")
    print("\n-- Item 10b: residual gap (position-matched D4 dest level minus plateau, midref) --")
    for d in ("+", "-"):
        sub = df[df.dest == d]
        gaps = sub.groupby("fam").resid_gap.mean()
        boots = [gaps.sample(len(gaps), replace=True, random_state=None).mean() for _ in range(2000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        print(f"  dest {d}: gap {sub.resid_gap.mean():+.2f} [family-boot CI {lo:+.2f}, {hi:+.2f}] "
              f"(n_runs={len(sub)}, n_fam={sub.fam.nunique()})")

    # Item 10a two-phase on direction means
    print("\n-- Item 10a: two-phase test on direction means --")
    for d, sign in (("+", 1.0), ("-", -1.0)):
        ys = np.stack([((d3[n] - mid) * sign)[20:40] for n in d3 if dest_fn(n) == sign])
        ym = ys.mean(0)
        Ap = ApB if sign > 0 else AmA; Am = AmA if sign > 0 else ApB
        rss, g = fit_integrator(ym, Ap, Am)
        pred = integrator_pred(g, Ap, Am)
        early, late = (ym - pred)[:5].mean(), (ym - pred)[14:].mean()
        print(f"  dest {d}: gamma* {g:.3f}; mean residual k1-5 {early:+.3f}, k15-20 {late:+.3f} "
              f"-> {'TWO-PHASE (under early, over late)' if early > 0.02 and late < -0.02 else 'not two-phase-signed'}")

    # Item 1c simulation control: pure-step synthetic runs through same classifier
    print("\n-- Item 1c: simulation control (pure step + matched noise) --")
    labels = []
    for (rss_s, (c, a, b)), y in sim_pool:
        sd = np.sqrt(rss_s / 20)
        for _ in range(2):
            ysim = np.where(K < c, a, b) + rng.normal(0, sd, 20)
            Ap = ApB; Am = AmA   # amplitudes only feed the integrator candidate
            lab, *_ = classify(ysim, Ap, Am)
            labels.append(lab)
    vc = pd.Series(labels).value_counts()
    print(f"synthetic n={len(labels)}: " + ", ".join(f"{k}={v}" for k, v in vc.items()))
    print(f"FALSE-INTEGRATOR rate: {vc.get('integrator', 0) / len(labels):.2%}")
    return df, mid, A, B

def main():
    rng = np.random.default_rng(1)
    results = {}
    for cfg in (tank_cfg, fr_cfg):
        tag, d4a, d4b, d3, dest_fn, fam_fn = cfg()
        results[tag] = battery(tag, d4a, d4b, d3, dest_fn, fam_fn, rng)
    # Item 13b: overshoot inspection (tank metrics CSV)
    m = pd.read_csv(OUT / "tank_d3_metrics_L4.csv")
    ov = m[(m.kind == "d3") & (m.overshoot > 0)]
    print("\n-- Item 13b: overshoot runs (tank) --")
    print(ov[["run", "direction", "overshoot", "tokens_to_crossing", "settled_mean"]].to_string(index=False)
          if len(ov) else "none")

if __name__ == "__main__":
    main()

# --- complementary control (appended after first run): integrator-TRUE recovery ---
def integrator_recovery(cfg, rng):
    tag, d4a, d4b, d3, dest_fn, fam_fn = cfg()
    A = np.stack(d4a); B = np.stack(d4b)
    mid = (A.mean(0) + B.mean(0)) / 2.0
    band = slice(10, 40)
    Ap = float((B.mean(0) - mid)[band].mean()); Am = float((mid - A.mean(0))[band].mean())
    labels = []
    for name, proj in sorted(d3.items()):
        dest = dest_fn(name)
        y = ((proj - mid) * dest)[20:40]
        rss, g = fit_integrator(y, Ap, Am)
        sd = np.sqrt(rss / 20)
        for _ in range(2):
            lab, *_ = classify(integrator_pred(g, Ap, Am) + rng.normal(0, sd, 20), Ap, Am)
            labels.append(lab)
    vc = pd.Series(labels).value_counts()
    print(f"{tag} integrator-TRUE sims n={len(labels)}: recovery "
          f"{vc.get('integrator', 0) / len(labels):.2%} ({dict(vc)})")
