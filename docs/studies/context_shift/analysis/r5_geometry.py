#!/usr/bin/env python3
"""P4 — geometry battery (three-worlds decider): passage vs off-manifold.

Prototype-validated instrument (2026-08-29): k=3-NN distance to the D3 post-shift
trajectory bundle, leave-own-run-out; null = bundle self-distances; positive control =
single-sentence calibration states (must read off-cloud). Prediction on record (P4):
majority of mid-transition states passage-like; JUMP STEPS ELEVATED off-manifold distance
(prototype trended AGAINST the jump call). D4 arm clouds (6 pts) secondary only.
Rule (from a caught prototype bug): bundle-member queries MUST exclude own run.
"""
import sys, json, csv
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
OUT = Path("docs/studies/context_shift/analysis")

CFG = {
    "tank_L4": dict(L=4, log="docs/studies/context_shift/captures/tank_d3_d4_log.tsv",
                    cal_sess="session_29a80932", d3="_d3_",
                    dest=lambda n: +1.0 if n.endswith("_ab") else -1.0,
                    park=lambda n: n.endswith("_ab")),
    "fr_L14": dict(L=14, log="docs/studies/context_shift/captures/fr_d3_d4_log.tsv",
                   cal_sess="session_5247081b", d3="fr_s1_",
                   dest=lambda n: +1.0 if n.endswith("_fr") else -1.0,
                   park=lambda n: False),
}

def load_states(log, L, want_d3):
    rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
    st = {}
    for r in rows:
        n = r["run"]
        if want_d3 not in n: continue
        lake = Path("data/lake") / r["session"]
        res = pd.read_parquet(lake / "residual_streams.parquet")
        res = res[(res["layer"] == L) & (res["token_position"] == 1)]
        tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "categories_json"])
        tok["pos"] = tok["categories_json"].apply(lambda c: int(json.loads(c)["position"]))
        df = res.merge(tok, on="probe_id").sort_values("pos")
        st[n] = np.stack(df["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
    return st

def knn(X, bundle, tags, own, k=3):
    out = []
    for x, o in zip(X, own):
        d = np.linalg.norm(bundle - x, axis=1)
        d = d[tags != o] if o is not None else d
        out.append(np.sort(d)[:k].mean())
    return np.array(out)

report = {}
for probe, c in CFG.items():
    st_all = load_states(c["log"], c["L"], "")
    d3 = {n: v for n, v in st_all.items() if "_d3_" in n and (c["d3"] in n)}
    d4 = {n: v for n, v in st_all.items() if "_d4_" in n and (c["d3"] in n or probe == "tank_L4")}
    bundle = np.concatenate([v[20:40] for v in d3.values()])
    tags = np.concatenate([[n] * 20 for n in d3])
    null = knn(bundle, bundle, tags, tags)
    med = float(np.median(null))
    # calibration positive control
    lake = Path("data/lake") / c["cal_sess"]
    res = pd.read_parquet(lake / "residual_streams.parquet")
    res = res[(res["layer"] == c["L"]) & (res["token_position"] == 1)]
    cal = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)[:200]
    cal_s = knn(cal, bundle, tags, [None] * len(cal)) / med
    d4s = np.concatenate([v[20:40] for v in d4.values()])
    d4_s = knn(d4s, bundle, tags, [None] * len(d4s)) / med
    # per-run per-step scores + jump/smooth/park splits
    rows_out, jump_s, smooth_s, park_s, travel_s = [], [], [], [], []
    for n, X in sorted(d3.items()):
        sc = knn(X[20:40], bundle, tags, [n] * 20) / med
        # jump step from midref-oriented reading trace
        d4A = np.stack([v for k2, v in d4.items() if k2.endswith(("_a", "_f"))])
        d4B = np.stack([v for k2, v in d4.items() if k2.endswith(("_b", "_r"))])
        midproj = None  # reading-based jump detection uses raw diffs of the state proj
        # simple jump proxy: largest state-space step
        step_sz = np.linalg.norm(np.diff(X[20:40], axis=0), axis=1)
        jk = int(np.argmax(step_sz)) + 1
        for k2 in range(20):
            rows_out.append({"probe": probe, "run": n, "k": k2 + 1,
                             "score": round(float(sc[k2]), 3), "is_jump": k2 == jk})
        jump_s.append(sc[jk]); smooth_s.extend(np.delete(sc, jk))
        (park_s if c["park"](n) else travel_s).extend(sc[10:20])
    df = pd.DataFrame(rows_out)
    df.to_csv(OUT / f"r5_geometry_{probe}.csv", index=False)
    rep = {
        "null_med": med, "null_p95_ratio": float(np.percentile(null, 95) / med),
        "calibration_ctrl": float(np.median(cal_s)),
        "d4_states": float(np.median(d4_s)),
        "jump_steps": float(np.median(jump_s)),
        "smooth_steps": float(np.median(smooth_s)),
        "late_park_or_ab": float(np.median(park_s)) if park_s else None,
        "late_travel": float(np.median(travel_s)) if travel_s else None,
    }
    report[probe] = rep
    print(f"{probe}: null med {med:.1f} (p95 {rep['null_p95_ratio']:.2f}x) | "
          f"calibration ctrl {rep['calibration_ctrl']:.2f}x | D4 {rep['d4_states']:.2f}x | "
          f"jump {rep['jump_steps']:.2f}x vs smooth {rep['smooth_steps']:.2f}x | "
          f"late ab/park {rep['late_park_or_ab']} | late travel/other {rep['late_travel']}")

# figure: score distributions
fig, axes = plt.subplots(1, 2, figsize=(11, 4), facecolor=SURFACE)
for ax, (probe, c) in zip(axes, CFG.items()):
    df = pd.read_csv(OUT / f"r5_geometry_{probe}.csv")
    ax.hist(df[~df.is_jump].score, bins=40, color=BLUE, alpha=0.7, density=True, label="smooth steps")
    ax.hist(df[df.is_jump].score, bins=20, color=ORANGE, alpha=0.7, density=True, label="jump steps (largest step per run)")
    ax.axvline(1.0, color=INK, lw=1.0, ls="--", label="null: held-out reference states")
    ax.axvline(report[probe]["calibration_ctrl"], color=AQUA, lw=1.4, ls=":",
               label=f"positive control: calibration states ({report[probe]['calibration_ctrl']:.1f}×)")
    task_name = {"tank_L4": "Tank task, layer 4", "fr_L14": "Fiction/real task, layer 14"}.get(probe, probe)
    ax.set_title(task_name, fontsize=10, color=INK)
    ax.set_xlabel("distance to the bundle (3-nearest-neighbor distance / null median)", fontsize=8.5, color=MUT)
    ax.set_facecolor(SURFACE); ax.legend(fontsize=7.5)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")
fig.suptitle("Per-state geometry: transition states against the trajectory bundle", fontsize=11, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(FIG / "fig_r5_geometry.png", dpi=150)
print("figure written: fig_r5_geometry.png")
