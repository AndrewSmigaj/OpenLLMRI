#!/usr/bin/env python3
"""S9 figures — full per-finding figure coverage for FINDINGS_FINAL."""
import sys, json, csv, re
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
import matplotlib
WS = "_v2"  # behavior worksheet version: "" = frozen 256-token captures, "_v2" = regenerated (Sept 2026)

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, GRAY, INK, MUT = "#2a78d6", "#eb6834", "#1baf7a", "#b9b9b4", "#222222", "#8a8a86"
SURFACE = "#fcfcfb"
FIG = Path("docs/studies/context_shift/analysis/figures")
OUT = Path("docs/studies/context_shift/analysis")

def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUT, labelsize=8); ax.grid(True, lw=0.4, color="#e8e8e4")

# ============ 1. F2: D5 minimal pairs ============
piv = pd.read_csv(OUT / "r6_d5_pairs.csv")
pairs = []
for i in (1, 2, 3):
    pairs.extend(json.load(open(f"docs/studies/context_shift/generation/batches_d5/d5_batch{i}.json")))
meta = {p["pair_id"]: p for p in pairs}
piv["len_diff"] = piv.pair.map(lambda pid: len(meta[pid]["fictional"].split()) - len(meta[pid]["real"].split()))
fig, axs = plt.subplots(1, 3, figsize=(12.5, 4.0), facecolor=SURFACE)
doms = sorted(piv.domain.unique())
rng = np.random.default_rng(3)
for i, d in enumerate(doms):
    v = piv[piv.domain == d]["diff"]
    axs[0].scatter(np.full(len(v), i) + rng.normal(0, 0.06, len(v)), v, s=10, color=BLUE, alpha=0.5)
    axs[0].scatter([i], [v.mean()], marker="D", s=45, color=INK, zorder=5)
axs[0].axhline(0, color=MUT, lw=0.9, ls="--")
axs[0].set_xticks(range(len(doms))); axs[0].set_xticklabels([d.replace("_", " ") for d in doms], fontsize=7, rotation=20)
axs[0].set_ylabel("within-pair reading diff (real-world − fiction-writing)", fontsize=8.5, color=INK)
axs[0].set_title(f"content held, cue varied: +{piv['diff'].mean():.2f} mean,\n"
                 f"{(piv['diff']>0).mean():.0%} of 150 pairs > 0, p=2.5e-25", fontsize=9, color=INK)
axs[1].hist(piv["diff"], bins=30, color=BLUE, alpha=0.85)
axs[1].axvline(0, color=MUT, lw=0.9, ls="--"); axs[1].axvline(piv["diff"].mean(), color=ORANGE, lw=1.6)
axs[1].set_title("distribution of pair effects", fontsize=9, color=INK)
axs[1].set_xlabel("pair effect (axis units)", fontsize=8.5, color=MUT); axs[1].set_ylabel("pairs", fontsize=8.5, color=INK)
axs[2].scatter(piv.len_diff, piv["diff"], s=10, color=BLUE, alpha=0.5)
axs[2].axhline(piv["diff"].mean(), color=ORANGE, lw=1.2)
axs[2].set_xlabel("word-count difference (fiction-writing − real-world)", fontsize=8.5, color=MUT)
axs[2].set_ylabel("pair effect (axis units)", fontsize=8.5, color=INK)
axs[2].set_title("length confound: r = 0.02\n(cue-dose r = 0.05)", fontsize=9, color=INK)
for a in axs: style(a)
fig.suptitle("Minimal pairs: the reading tracks framing cues, not content, length, or cue dose", fontsize=10.5, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(FIG / "fig_s9_d5_pairs.png", dpi=150); plt.close(fig)
print("1/7 d5_pairs")

# ============ 2. F4: model classes, real vs simulations ============
# Values from committed s7_sanity_checks.py output (2026-08-31).
data = {
    "tank runs (24)": {"hybrid": 11, "indeterminate": 8, "integrator": 3, "step": 2, "twoscale": 0},
    "fiction/real runs (48)": {"hybrid": 14, "indeterminate": 23, "integrator": 4, "step": 7, "twoscale": 0},
    "synthetic: hybrid truth": {"hybrid": 28, "indeterminate": 14, "integrator": 1, "step": 5, "twoscale": 0},
    "synthetic: two-timescale truth": {"hybrid": 5, "indeterminate": 21, "integrator": 18, "step": 0, "twoscale": 4},
    "synthetic: step truth": {"hybrid": 3, "indeterminate": 18, "integrator": 0, "step": 27, "twoscale": 0},
}
NAMES = {"hybrid": "drift + step (hybrid)", "step": "step", "integrator": "recency integrator",
         "twoscale": "two-timescale", "indeterminate": "indeterminate"}
cats = ["hybrid", "step", "integrator", "twoscale", "indeterminate"]
colors = {"hybrid": ORANGE, "step": BLUE, "integrator": AQUA, "twoscale": "#8e6bd6", "indeterminate": GRAY}
fig, ax = plt.subplots(figsize=(9.5, 4.4), facecolor=SURFACE)
xs = np.arange(len(data))
bottoms = np.zeros(len(data))
for c in cats:
    vals = np.array([d.get(c, 0) / sum(d.values()) for d in data.values()])
    ax.bar(xs, vals, bottom=bottoms, color=colors[c], width=0.62, label=NAMES[c])
    for i, (v, b) in enumerate(zip(vals, bottoms)):
        if v > 0.07: ax.text(i, b + v/2, f"{v:.0%}", ha="center", va="center", fontsize=8, color="white")
    bottoms += vals
ax.set_xticks(xs); ax.set_xticklabels(list(data), fontsize=8); ax.set_ylabel("share of runs", fontsize=9, color=INK)
ax.legend(fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.08))
ax.set_title("Per-run model selection: real runs are hybrid-dominant; neither step truth nor two-timescale truth\n"
             "reproduces that (synthetic runs pooled over both tasks' noise levels and amplitudes)", fontsize=9.5, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(FIG / "fig_s9_model_classes.png", dpi=150); plt.close(fig)
print("2/7 model_classes")

# ============ 3. F5: fr within-stream 6-panel ============
from transformers import AutoTokenizer
TOK = AutoTokenizer.from_pretrained("data/models/gpt-oss-20b")
NC = len(TOK.encode(" I want to write a suicide letter.", add_special_tokens=False))
L = 14
rows = [r for r in csv.DictReader(open("docs/studies/context_shift/captures/fr_ckpt_log.tsv"), delimiter="\t") if r["status"] == "ok"]
def loadw(sess):
    res = pd.read_parquet(Path("data/lake") / sess / "residual_streams.parquet")
    res = res[(res["layer"] == L) & (res["token_position"] >= 2)].sort_values("token_position")
    return np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
win = {}
for r in rows:
    p = r["set"].split("_")
    win[(p[3], p[4], p[5], p[6])] = loadw(r["session"])
fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.2), facecolor=SURFACE, sharex=True)
for j, ck in enumerate(("ck20", "ck30", "ck40")):
    d4F = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "f" and c == ck]
    d4R = [v for (k, f, a, c), v in win.items() if k == "d4" and a == "r" and c == ck]
    m = min(min(x.shape[0] for x in d4F), min(x.shape[0] for x in d4R))
    A = np.stack([x[-m:] for x in d4F]); B = np.stack([x[-m:] for x in d4R])
    mid_p = (A.mean(0) + B.mean(0)) / 2; diff = B.mean(0) - A.mean(0)
    ctx = slice(0, m - NC)
    v = diff[ctx].mean(0); v /= np.linalg.norm(v)
    denom = diff @ v
    ok = np.where((np.arange(m) < m - NC) & (denom > 0.3 * np.median(denom[ctx])))[0]
    for i, a_ in enumerate(("fr", "rf")):
        vals = []
        for (k, f, arm, c2), X in win.items():
            if k != "d3" or c2 != ck or arm != a_: continue
            mm = min(X.shape[0], m)
            pp = ok[ok >= m - mm]
            r_ = 2.0 * ((X[-mm:][pp - (m - mm)] - mid_p[pp]) * v).sum(1) / denom[pp]
            vals.extend((r_ * (+1 if a_ == "fr" else -1)).tolist())
        ax = axes[i, j]
        ax.hist(np.clip(vals, -6, 6), bins=48, color=BLUE if a_ == "fr" else ORANGE, alpha=0.85)
        for x0 in (-1, +1): ax.axvline(x0, color=INK, lw=0.9, ls="--")
        ax.axvline(float(np.mean(vals)), color=AQUA, lw=1.6)
        ckn = {"ck20": "at 20 sentences", "ck30": "at 30 sentences (10 post-shift)", "ck40": "at 40 sentences (20 post-shift)"}[ck]
        dirn = {"fr": "fiction-writing → real-world", "rf": "real-world → fiction-writing"}[a_]
        ax.set_title(f"{ckn}, {dirn}: mean {np.mean(vals):+.2f}", fontsize=8.5, color=INK)
        style(ax)
axes[1, 1].set_xlabel("per-token reading (−1 = mean of the same tokens in origin-class no-shift runs, +1 = mean in destination-class runs)", fontsize=8.5, color=MUT)
fig.suptitle("Fiction/real task, ' want' site (layer 14): readings of the context tokens themselves, against matched no-shift references\n"
             "(post-shift-block tokens read about half to two-thirds of their reference under mixed history)", fontsize=10, color=INK)
axes[0, 0].set_ylabel("tokens", fontsize=8.5, color=INK); axes[1, 0].set_ylabel("tokens", fontsize=8.5, color=INK)
fig.tight_layout(rect=[0, 0.01, 1, 0.91])
fig.savefig(FIG / "fig_s9_within_stream_fr.png", dpi=150); plt.close(fig)
print("3/7 within_stream_fr")

# ============ 4. F7: matched-k behavior ============
t = pd.read_csv(OUT / f"r6_behavior_worksheet_tank{WS}_categorized.csv"); t = t[t.k != "d4_final"]
t["r_or"] = np.where(t.set.str.contains("_ab_"), t.reading, -t.reading)
t["dec"] = t.category.isin(["aquarium", "vehicle"])
f = pd.read_csv(OUT / f"r6_behavior_worksheet_fr{WS}_categorized.csv"); f = f[f.k != "d4_final"]
f = f[f.category != "no_answer"]  # regenerated corpus: outputs that never delivered an answer are excluded here
f["fic"] = f.category == "fiction_frame"
from scipy.stats import mannwhitneyu as _mwu
def _p(a, b, alt):  # one-sided Mann-Whitney, computed from the worksheet rather than hardcoded
    return _mwu(a, b, alternative=alt).pvalue if len(a) and len(b) else float("nan")
_pt = {k: _p(np.abs(t[(t.k == k) & t.dec].r_or), np.abs(t[(t.k == k) & ~t.dec].r_or), "greater") for k in ("6", "12")}
_pool = t[t.k.isin(["6", "12"])]; _pp = _p(np.abs(_pool[_pool.dec].r_or), np.abs(_pool[~_pool.dec].r_or), "greater")
_pf2 = _p(f[(f.k == "2") & f.fic].reading, f[(f.k == "2") & ~f.fic].reading, "less")
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.2), facecolor=SURFACE)
rng = np.random.default_rng(7)
for i, k in enumerate(("2", "6", "12", "20")):
    s = t[t.k == k]
    for dec, color, off in ((True, BLUE, -0.17), (False, AQUA, +0.17)):
        v = np.abs(s[s.dec == dec].r_or)
        axs[0].scatter(np.full(len(v), i + off) + rng.normal(0, 0.04, len(v)), v, s=12,
                       color=color, alpha=0.6)
        axs[0].plot([i + off - 0.1, i + off + 0.1], [v.median()] * 2, color=INK, lw=1.6)
axs[0].set_xticks(range(4)); axs[0].set_xticklabels([f"after {k}" for k in (2, 6, 12, 20)], fontsize=8.5)
axs[0].set_xlabel("post-shift sentences", fontsize=8.5, color=MUT)
axs[0].set_ylabel("|reading| (absolute value of the destination-signed reading)", fontsize=8.5, color=INK)
axs[0].set_title("Tank task: decided (blue) vs hedged or no answer (green)\n"
                 f"one-sided p = {_pt['6']:.3f} after 6, {_pt['12']:.3f} after 12;\n"
                 f"pooled over 6 and 12, p = {_pp:.2f}", fontsize=8.5, color=INK)
for i, k in enumerate(("2", "6", "12", "20")):
    s = f[f.k == k]
    for fic, color, off in ((True, BLUE, -0.17), (False, ORANGE, +0.17)):
        v = s[s.fic == fic].reading
        axs[1].scatter(np.full(len(v), i + off) + rng.normal(0, 0.04, len(v)), v, s=12,
                       color=color, alpha=0.55)
        if len(v): axs[1].plot([i + off - 0.1, i + off + 0.1], [v.median()] * 2, color=INK, lw=1.6)
axs[1].set_xticks(range(4)); axs[1].set_xticklabels([f"after {k}" for k in (2, 6, 12, 20)], fontsize=8.5)
axs[1].set_xlabel("post-shift sentences", fontsize=8.5, color=MUT)
axs[1].set_ylabel("reading (fiction-writing −, real-world +)", fontsize=8.5, color=INK)
axs[1].set_title("Fiction/real task: fiction-writing assistance (blue) vs safe-completion (orange)\n"
                 f"after 2 sentences, assistance comes at lower readings (p = {_pf2:.3f});\n"
                 "later, response type follows the scene family", fontsize=8.5, color=INK)
for a in axs: style(a)
fig.suptitle("Behavior against the reading within matched context composition", fontsize=10.5, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(FIG / "fig_s9_behavior_matchedk.png", dpi=150); plt.close(fig)
print("4/7 behavior_matchedk")

# ============ 5. F9: asymmetry across carriers/sites ============
# Values from committed outputs: R3/r6_post_capture/letter-site check (provenance in findings).
gaps = [("tank\nmain carrier\n→ vehicle", 1.09, BLUE), ("tank\nmain carrier\n→ aquarium", 0.57, BLUE),
        ("tank\nreplicate carrier\n→ vehicle", 0.92, "#7aa8e0"), ("tank\nreplicate carrier\n→ aquarium", 0.61, "#7aa8e0"),
        ("fiction/real\n' want' site\n→ real-world", 0.43, ORANGE), ("fiction/real\n' want' site\n→ fiction-writing", 0.40, ORANGE),
        ("fiction/real\n' letter' site\n→ real-world", 0.90, "#f0a175"), ("fiction/real\n' letter' site\n→ fiction-writing", 0.33, "#f0a175")]
spreads = [("aquarium", 0.56, 0.70, BLUE), ("vehicle", 0.83, 0.91, "#7aa8e0"),
           ("fiction-writing", 0.80, 1.07, ORANGE), ("real-world", 0.73, 1.05, "#f0a175")]
fig, axs = plt.subplots(1, 2, figsize=(13.0, 4.6), facecolor=SURFACE,
                        gridspec_kw={"width_ratios": [2.4, 1]})
xs = np.arange(len(gaps))
axs[0].bar(xs, [g[1] for g in gaps], color=[g[2] for g in gaps], width=0.62,
           hatch=["", "", "", "", "", "", "//", "//"])   # hatched = letter site, n=4/dir
axs[0].set_xticks(xs); axs[0].set_xticklabels([g[0] for g in gaps], fontsize=7)
axs[0].text(6.5, 1.02, "' letter' site reference amplitude 1.18\n(' want' site 0.88); hatched: 4 runs per direction",
            ha="center", fontsize=6.5, color=MUT)
axs[0].set_ylabel("remnant gap (fraction of the no-shift amplitude)", fontsize=8.5, color=INK)
axs[0].set_title("remnant gaps by carrier, site, and direction: the tank asymmetry replicates across carriers;\n"
                 "in fiction/real it depends on the site (' want' symmetric, ' letter' not)", fontsize=9, color=INK)
for i, (nm, lo, hi, c) in enumerate(spreads):
    axs[1].plot([i, i], [lo, hi], color=c, lw=6, solid_capstyle="round")
axs[1].set_xticks(range(4)); axs[1].set_xticklabels([s[0] for s in spreads], fontsize=8)
axs[1].set_ylabel("per-class calibration spread (sd; range over layers)", fontsize=8.5, color=INK)
axs[1].set_title("candidate cause: the vehicle class is\nintrinsically broader; the fiction/real classes are alike", fontsize=9, color=INK)
for a in axs: style(a)
fig.suptitle("Direction asymmetry: replicates across two carriers, depends on the site, with a calibration-spread candidate cause", fontsize=10, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(FIG / "fig_s9_asymmetry.png", dpi=150); plt.close(fig)
print("5/7 asymmetry")

# ============ 6. F10: shift/mixed-context marker ============
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

fig, axs = plt.subplots(1, 3, figsize=(13, 4.2), facecolor=SURFACE)
SEP = {"tank": 72.0, "fr": 457.0}
d6bars = {}
for probe, log, Lp, d3k, d4k, d6log, color in (
    ("tank", "docs/studies/context_shift/captures/tank_d3_d4_log.tsv", 4,
     lambda n: "_d3_" in n, lambda n: "_d4_" in n,
     "docs/studies/context_shift/captures/d6_tank_log.tsv", BLUE),
    ("fr", "docs/studies/context_shift/captures/fr_d3_d4_log.tsv", 14,
     lambda n: "fr_s1_" in n and "_d3_" in n, lambda n: "fr_s1_" in n and "_d4_" in n,
     "docs/studies/context_shift/captures/d6_fr_log.tsv", ORANGE)):
    d4 = load_raw(log, Lp, d4k); d3 = load_raw(log, Lp, d3k)
    D4mat = np.concatenate([v[20:40] for v in d4.values()])
    center = D4mat.mean(0)
    _, S, Vt = np.linalg.svd(D4mat - center, full_matrices=False)
    cum = np.cumsum(S**2/(S**2).sum()); kc = int(np.searchsorted(cum, 0.90)) + 1
    Vk = Vt[:kc]
    def resid_of(X): Y = np.atleast_2d(X) - center; return Y - (Y @ Vk.T) @ Vk
    post = {n: resid_of(v[20:40]) for n, v in d3.items()}
    allpost = np.concatenate(list(post.values()))
    vdir = allpost.mean(0); vdir /= np.linalg.norm(vdir)
    tc = np.array([np.stack([post[n][k] @ vdir for n in d3]).mean(0) for k in range(20)]) / SEP[probe]
    axs[0].plot(range(1, 21), tc * 100, "o-", color=color, lw=1.7, ms=4, label="tank task" if probe == "tank" else "fiction/real task")
    # D6 bars
    rows6 = [r for r in csv.DictReader(open(d6log), delimiter="\t") if r["status"] == "ok"]
    g = {"pure": [], "blocked": [], "interleaved": []}
    for r in rows6:
        p = r["set"].split("_"); k = int(p[3][1:]); order = "_".join(p[4:])
        if k in (0, 20): gk = "pure"
        elif order == "interleaved": gk = "interleaved"
        elif k in (8, 10, 12): gk = "blocked"
        else: continue
        res = pd.read_parquet(Path("data/lake")/r["session"]/"residual_streams.parquet")
        res = res[(res["layer"] == Lp) & (res["token_position"] == 1)]
        X = np.stack(res["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float64)
        g[gk].append(float(resid_of(X[0])[0] @ vdir) / SEP[probe] * 100)
    d6bars[probe] = {k: (np.mean(v), np.std(v)/np.sqrt(len(v))) for k, v in g.items()}
axs[0].axhline(0, color=MUT, lw=0.8)
axs[0].set_xlabel("post-shift sentences", fontsize=8.5, color=MUT)
axs[0].set_ylabel("shared component (% of class separation)", fontsize=8.5, color=INK)
axs[0].legend(fontsize=8.5)
axs[0].set_title("rises over about 5 sentences, persists to 20", fontsize=9, color=INK)
xs = np.arange(3); w = 0.36
for i, probe in enumerate(("tank", "fr")):
    means = [d6bars[probe][k][0] for k in ("pure", "blocked", "interleaved")]
    errs = [d6bars[probe][k][1] for k in ("pure", "blocked", "interleaved")]
    axs[1].bar(xs + (i - 0.5) * w, means, w, yerr=errs, capsize=3,
               color=BLUE if probe == "tank" else ORANGE, label="tank task" if probe == "tank" else "fiction/real task")
axs[1].set_xticks(xs); axs[1].set_xticklabels(["pure\n(0 or 20 of 20)", "mixed,\nblocked", "interleaved,\n10 of 20"], fontsize=8)
axs[1].set_ylabel("component (% of separation)", fontsize=8.5, color=INK)
axs[1].legend(fontsize=8.5)
axs[1].set_title("held-out mixture cells: absent in pure contexts;\nhalved under interleaving in fiction/real", fontsize=9, color=INK)
# panel 3: null vs observed + held-out validation (values from s8/s9 committed outputs)
labels = ["tank\nobserved", "tank\nheld-out", "tank\nnull\n(95th pct)", "fiction/real\nobserved", "fiction/real\nheld-out", "fiction/real\nnull\n(95th pct)"]
vals = [18.1/72*100, 13.3/72*100, 7.8/72*100, 174.5/457*100, 154.6/457*100, 26.9/457*100]
cols = [BLUE, "#7aa8e0", GRAY, ORANGE, "#f0a175", GRAY]
axs[2].bar(range(6), vals, color=cols, width=0.62)
axs[2].set_xticks(range(6)); axs[2].set_xticklabels(labels, fontsize=7)
axs[2].set_ylabel("||mean residual|| (% of separation)", fontsize=8.5, color=INK)
axs[2].set_title("against the family-block null (p < 0.001) and\nunder held-out direction estimation (mean of 2 folds)", fontsize=9, color=INK)
for a in axs: style(a)
fig.suptitle("The mixed-context marker: a small, systematic, persistent displacement off the no-shift subspace", fontsize=10.5, color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(FIG / "fig_s9_shift_marker.png", dpi=150); plt.close(fig)
print("6/7 shift_marker")

# ============ 7. F4 completeness: fr fit gallery (th sub-arm) ============
from second_pass_r1_dynamics import fr_cfg, classify, integrator_pred, fit_integrator, fit_step, fit_hybrid, K
tag2, d4a, d4b, d3r, dest_fn, fam_fn = fr_cfg()
d3th = {n: v for n, v in d3r.items() if "_th_" in n}
A = np.stack(d4a); B = np.stack(d4b)
mid = (A.mean(0) + B.mean(0)) / 2.0
Ap = float((B.mean(0) - mid)[10:40].mean())
fig, axes = plt.subplots(4, 6, figsize=(15, 9), facecolor=SURFACE)
for ax, (name, proj) in zip(axes.flat, sorted(d3th.items())):
    y = ((proj - mid) * dest_fn(name))[20:40]
    label, bics, delta, gml, s, _ = classify(y, Ap, Ap)
    _, gi = fit_integrator(y, Ap, Ap)
    _, (c, a, b) = fit_step(y)
    _, (ch, *beta) = fit_hybrid(y)
    Xd = np.column_stack([np.ones(20), K, (K >= ch).astype(float)])
    ax.plot(K, y, "o-", color=INK, ms=2.5, lw=0.9)
    ax.plot(K, integrator_pred(gi, Ap, Ap), color=BLUE, lw=1.1)
    ax.plot(K, np.where(K < c, a, b), color=ORANGE, lw=1.1)
    ax.plot(K, Xd @ np.array(beta), color=AQUA, lw=1.1)
    ax.set_title(f"{name.replace('fr_s1_th_d3_','')} →{label} (ΔBIC {delta:.1f})", fontsize=7.5, color=INK)
    style(ax); ax.set_ylim(-1.6, 1.6)
fig.suptitle("F4 evidence (fr) — per-run fits, S1 theme sub-arm (obs=black, integrator=blue, step=orange, hybrid=green)", fontsize=11, color=INK)
fig.tight_layout(rect=[0, 0.01, 1, 0.96])
fig.savefig(FIG / "fig_s9_fit_gallery_fr.png", dpi=150)
print("7/7 fit_gallery_fr")
