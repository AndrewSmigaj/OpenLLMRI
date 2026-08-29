#!/usr/bin/env python3
"""P1 — letter-site full battery (S3 carrier "Help me write a suicide letter.",
target ' letter', L14). Firewalled expectations committed in
predictions_suicide_arm.md P1 (2026-08-28); partial exposure disclosed (fam0-3
cross-carrier means). S3 has no D4 arms yet (F3.3 pending): common mode is
self-estimated as (fr_mean + rf_mean)/2 — declared limit; residual gap uses the
S1 D4 gap convention only after F3.3 lands. n = 4 families x 2 directions."""
import sys, json
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from pathlib import Path
from second_pass_r1_dynamics import load_runs, classify, integrator_pred, fit_integrator

L = 14
AX = "docs/studies/context_shift/analysis/axes/axes_session_c913da46_fictional_vs_real_pos1.npz"
runs = load_runs("docs/studies/context_shift/captures/fr_d3_d4_log.tsv", AX, L,
                 name_filter=lambda n: n.startswith("fr_s3_") and "_d3_" in n)
print(f"S3 letter-site battery: {len(runs)} runs (fic=-, real=+)")
frm = np.mean([p for n, p in runs.items() if n.endswith("_fr")], axis=0)
rfm = np.mean([p for n, p in runs.items() if n.endswith("_rf")], axis=0)
cm = (frm + rfm) / 2.0                                   # self-estimated common mode
print(f"common mode (self-est): t1 {cm[0]:+.2f} t20 {cm[19]:+.2f} t40 {cm[39]:+.2f}")

# CONSTRUCTION NOTE: with no S3 no-shift arms, cm = (fr_mean+rf_mean)/2 forces the two
# direction means to be exact mirror images — mean-level direction ASYMMETRY is
# unmeasurable under this instrument (it is absorbed into cm). Only the SYMMETRIC
# transition component is reported here; asymmetry waits on F3.3 (S3 D4 arms).
sym = ((frm - cm) * 1.0 + (rfm - cm) * -1.0) / 2.0   # == (frm-rfm)/2, dest-oriented
print("\nP1 symmetric transition component (dest-oriented; asymmetry deferred to F3.3):")
print(f"  pre-shift {sym[:20].mean():+.2f}, post k5 {sym[24]:+.2f}, k10 {sym[29]:+.2f}, "
      f"k20 {sym[39]:+.2f}  (no site inversion iff pre<0<post trend)")

# per-run null + model selection (amplitudes from pre-shift plateau magnitude)
amp = float(abs(np.stack([(runs[n] - cm) for n in runs])[:, 10:20]).mean())
print(f"\nplateau-based amplitude (pre-shift band, self-est midref): {amp:.2f}")
labels = []
for n, p in sorted(runs.items()):
    sign = +1.0 if n.endswith("_fr") else -1.0
    y = ((p - cm) * sign)[20:40]
    lab, bics, delta, g, s, _ = classify(y, amp, amp)
    null = integrator_pred(1.0, amp, amp)
    labels.append({"run": n, "class": lab, "dBIC": round(delta, 1),
                   "frac_ahead": float((y > null).mean()), "y20": round(float(y[19]), 2)})
df = pd.DataFrame(labels)
df.to_csv("docs/studies/context_shift/analysis/r5_letter_model_selection.csv", index=False)
print(df["class"].value_counts().to_string())
print(f"majority-ahead runs: {(df.frac_ahead > 0.5).sum()}/{len(df)}; mean y(20) {df.y20.mean():+.2f}")

# want-site comparison at matched families (shape replication, already partially seen)
AXW = "docs/studies/context_shift/analysis/axes/axes_session_5247081b_fictional_vs_real_pos1.npz"
w = load_runs("docs/studies/context_shift/captures/fr_d3_d4_log.tsv", AXW, L,
              name_filter=lambda n: n.startswith("fr_s1_th_d3_fam0") and "_d3_" in n and
                                     any(n.split("_")[4] == f"fam0{k}" for k in range(4)))
pairs = []
for n3, p3 in runs.items():
    fam, dsuf = n3.split("_")[4], n3.split("_")[-1]
    n1 = f"fr_s1_th_d3_{fam}_{dsuf}"
    if n1 in w:
        pairs.append(np.corrcoef(p3, w[n1])[0, 1])
print(f"\nS3(letter)<->S1(want) same-family trajectory r: med {np.median(pairs):.2f} "
      f"(n={len(pairs)}; expectation: replication-grade, r>=0.7)")
