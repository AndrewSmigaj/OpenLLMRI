#!/usr/bin/env python3
"""Second-pass review R4: event-locked jumps (Item 3), post-shift volatility (Item 14),
S2/S3 common-mode replication of accumulation drift (Item 11d)."""
from __future__ import annotations
import json, glob
from pathlib import Path
import numpy as np
import pandas as pd
import sys; sys.path.insert(0, "docs/studies/context_shift/analysis")
from second_pass_r1_dynamics import tank_cfg, load_runs

OUT = Path("docs/studies/context_shift/analysis")

# ---------------- Item 3: event-locked jump analysis (tank L4) ----------------
print("=" * 78)
print("Item 3 — are jump steps carried by unusually strong sentences?")
# calibration cell readings: sentence text -> reading (L4, pos1 axis)
ax = np.load(OUT / "axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz")
L = 4
lake = Path("data/lake/session_29a80932")
res = pd.read_parquet(lake / "residual_streams.parquet")
res = res[(res["layer"] == L) & (res["token_position"] == 1)]
tok = pd.read_parquet(lake / "tokens.parquet", columns=["probe_id", "input_text", "label"])
cal = res.merge(tok, on="probe_id")
X = np.stack(cal["residual_stream"].apply(np.asarray).to_numpy()).astype(np.float32)
cal["reading"] = 2.0 * ((X - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"])
CARRIER = " What is the meaning of the word tank?"
def strip_carrier(t):
    return t[:-len(CARRIER)].strip() if t.endswith(CARRIER.strip()) or CARRIER.strip() in t else t
cal["sentence"] = cal["input_text"].apply(lambda t: t.split(" What is the meaning")[0].strip())
cal_map = dict(zip(cal["sentence"], cal["reading"]))
# percentile within class
by_label = {lab: np.sort(cal[cal.label == lab].reading.to_numpy()) for lab in cal.label.unique()}
def pct(sent, lab):
    r = cal_map.get(sent)
    if r is None: return None
    arr = by_label[lab]
    return float(np.searchsorted(arr, r) / len(arr))

tag, d4a, d4b, d3, dest_fn, fam_fn = tank_cfg()
A = np.stack(d4a); B = np.stack(d4b)
mid = (A.mean(0) + B.mean(0)) / 2.0
jump_pcts, nonjump_pcts, miss = [], [], 0
largest_pcts = []
for name, proj in sorted(d3.items()):
    dest = dest_fn(name)
    y = ((proj - mid) * dest)[20:40]
    d = np.abs(np.diff(y))                       # step k -> k+1 magnitude, k=1..19
    run_file = Path("data/sentence_sets/polysemy/context_shift_runs") / f"{name}.json"
    rj = json.load(open(run_file))
    cums = [s["text"].split(" What is the meaning")[0].strip()
            for g in rj["groups"] for s in g["sentences"]]
    # cumulative texts -> the sentence ADDED at each step
    sents = [cums[0]] + [cums[i][len(cums[i - 1]):].strip() for i in range(1, len(cums))]
    # sentence added at post-shift step k (k=1..20) = context sentence index 20+k-1 (0-based 20+k-1)
    dest_lab = "vehicle" if dest > 0 else "aquarium"
    # the step from k to k+1 is driven by the sentence added at k+1
    jump_k = int(np.argmax(d)) + 2               # k of the arriving sentence
    net = abs(y[-1] - y[0])
    is_jump_run = d.max() > 0.5 * net if net > 1e-9 else False
    for k in range(2, 21):
        sent = sents[20 + k - 2] if 20 + k - 2 < len(sents) else None
        # context sentences order: run JSON sentences 0..39 = positions 1..40; added at pos 20+k
        sent = sents[20 + k - 1 - 1]
        p = pct(sent, dest_lab)
        if p is None: miss += 1; continue
        if k == jump_k:
            (jump_pcts if is_jump_run else largest_pcts).append(p)
        else:
            nonjump_pcts.append(p)
print(f"  coverage: {miss} sentence-steps unmatched in calibration cells "
      f"(of {miss + len(jump_pcts) + len(nonjump_pcts) + len(largest_pcts)})")
print(f"  jump-run jump sentences: n={len(jump_pcts)} median class-percentile "
      f"{np.median(jump_pcts):.2f}" if jump_pcts else "  (no jump runs matched)")
print(f"  non-jump-run largest-step sentences: n={len(largest_pcts)} median "
      f"{np.median(largest_pcts):.2f}" if largest_pcts else "")
print(f"  all other post-shift sentences: n={len(nonjump_pcts)} median {np.median(nonjump_pcts):.2f}")
from scipy.stats import mannwhitneyu
if jump_pcts:
    u, pv = mannwhitneyu(jump_pcts + largest_pcts, nonjump_pcts, alternative="greater")
    print(f"  Mann-Whitney (largest-step sentences stronger?): p = {pv:.3f}")

# ---------------- Item 14: post-shift volatility ----------------
print("\n" + "=" * 78)
print("Item 14 — step-to-step variance: post-shift vs pre-shift vs D4 matched positions")
for label, mats, sl in (("d3 pre-shift (t2-20)", [((d3[n] - mid) * dest_fn(n)) for n in d3], slice(1, 20)),
                        ("d3 post-shift (t21-40)", [((d3[n] - mid) * dest_fn(n)) for n in d3], slice(20, 40)),
                        ("d3 late post (t31-40)", [((d3[n] - mid) * dest_fn(n)) for n in d3], slice(30, 40)),
                        ("D4 arms (t21-40)", [(m_ - mid) for m_ in list(A) + list(B)], slice(20, 40))):
    sds = [np.abs(np.diff(m_[sl])).mean() for m_ in mats]
    print(f"  {label:>24}: mean |step| {np.mean(sds):.3f} (sd across runs {np.std(sds):.3f})")

# ---------------- Item 11d: S2/S3 common-mode replication ----------------
print("\n" + "=" * 78)
print("Item 11d — accumulation drift (common mode) replicates across carriers? (L14)")
AXES = {"s1": "axes_session_5247081b_fictional_vs_real_pos1.npz",
        "s2": "axes_session_589557e1_fictional_vs_real_pos1.npz",
        "s3": "axes_session_c913da46_fictional_vs_real_pos1.npz"}
cm = {}
for s, axf in AXES.items():
    runs = load_runs("docs/studies/context_shift/captures/fr_d3_d4_log.tsv",
                     str(OUT / "axes" / axf), 14,
                     name_filter=lambda n, s=s: n.startswith(f"fr_{s}_") and "_d3_" in n)
    frm = np.mean([p for n, p in runs.items() if n.endswith("_fr")], axis=0)
    rfm = np.mean([p for n, p in runs.items() if n.endswith("_rf")], axis=0)
    cm[s] = (frm + rfm) / 2.0        # class component cancels (opposite origins) -> common mode
    print(f"  {s}: common-mode t1 {cm[s][0]:+.2f} -> t20 {cm[s][19]:+.2f} -> t40 {cm[s][39]:+.2f} "
          f"(n_runs fr/rf = {sum(n.endswith('_fr') for n in runs)}/{sum(n.endswith('_rf') for n in runs)})")
print(f"  r(S1,S2) = {np.corrcoef(cm['s1'], cm['s2'])[0,1]:.2f}, "
      f"r(S1,S3) = {np.corrcoef(cm['s1'], cm['s3'])[0,1]:.2f}")
