#!/usr/bin/env python3
"""s20 — dwelling decomposition (logged post-freeze addition; criterion fixed before running).

Question: is the "dwelling" of §3.4 a property of individual runs or only of the run
population? For each transition run, on midpoint-referenced readings at the
calibrated site (tank ' tank' L4, fiction/real ' want' L14; single-sentence axis;
midpoint = per-position mean of the two no-shift classes' means), signed toward the
destination class:

  late slope     least-squares slope over post-shift sentences 11-20 (positions
                 31-40), in axis units per sentence
  residence      number of positions 31-40 with |reading| <= 0.5 axis units (the
                 behavior bands' middle band)
  plateau        |late slope| <= 0.02 units per sentence AND residence >= 5

Criterion written 6 September 2026 before any value was computed. Reported:
per-run values; the share of runs meeting the plateau criterion; the
family-clustered mean late slope with a 2,000-draw bootstrap 95% interval,
stated as an equivalence bound ("mean late slope within [lo, hi]"), never as
"not significantly different from zero"; the same for all four transitions.
Data: the archived captures via second_pass_r1_dynamics.tank_cfg / fr_cfg.
"""
import sys
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np
from second_pass_r1_dynamics import tank_cfg, fr_cfg

rng = np.random.default_rng(20)
POS = np.arange(31, 41)  # post-shift sentences 11-20
for cfg in (tank_cfg, fr_cfg):
    tag, d4a, d4b, d3, dest_fn, fam_fn = cfg()
    A = np.stack(d4a); B = np.stack(d4b); mid = (A.mean(0) + B.mean(0)) / 2.0
    amp = float(abs(A.mean(0) - B.mean(0))[30:40].mean() / 2.0)
    print("=" * 78); print(f"{tag}: {len(d3)} transition runs; no-shift amplitude over positions 31-40 = {amp:.2f} axis units")
    for direction in sorted({("→dest+" if dest_fn(n) > 0 else "→dest−") for n in d3}):
        names = [n for n in d3 if ("→dest+" if dest_fn(n) > 0 else "→dest−") == direction]
        rows = []
        for n in names:
            y = (np.asarray(d3[n]) - mid) * dest_fn(n)          # midpoint-referenced, destination-signed
            late = y[30:40]
            slope = float(np.polyfit(POS, late, 1)[0])
            res = int((np.abs(late) <= 0.5).sum())
            rows.append((n, fam_fn(n), slope, res, float(late.mean()), abs(slope) <= 0.02 and res >= 5))
        slopes = np.array([r[2] for r in rows]); fams = np.array([r[1] for r in rows])
        # family-clustered bootstrap of the mean late slope
        uf = np.unique(fams); boots = []
        for _ in range(2000):
            pick = rng.choice(uf, size=len(uf), replace=True)
            boots.append(np.mean(np.concatenate([slopes[fams == f] for f in pick])))
        lo, hi = np.percentile(boots, [2.5, 97.5])
        label = {"tank_L4": {"→dest+": "aquarium→vehicle", "→dest−": "vehicle→aquarium"},
                 "fr_S1_L14": {"→dest+": "fiction-writing→real-world", "→dest−": "real-world→fiction-writing"}}[tag][direction]
        n_plateau = sum(r[5] for r in rows)
        print(f"\n{label}: n={len(rows)} runs")
        print(f"  mean late slope {slopes.mean():+.4f} units/sentence, family-clustered 95% interval [{lo:+.4f}, {hi:+.4f}]"
              f"  ({slopes.mean()/amp*100:+.2f}% of amplitude per sentence; over 10 sentences the bound spans [{lo*10:+.3f}, {hi*10:+.3f}] units)")
        print(f"  runs meeting the plateau criterion (|slope| <= 0.02 and residence >= 5 of 10): {n_plateau} of {len(rows)}")
        print(f"  residence in the middle band (positions 31-40): median {int(np.median([r[3] for r in rows]))} of 10; late-window mean reading median {np.median([r[4] for r in rows]):+.2f} units")
        for n, fam, s, res, m, pl in sorted(rows, key=lambda r: r[2]):
            print(f"    {n:28s} slope {s:+.4f}  residence {res:2d}/10  late mean {m:+.2f}  {'PLATEAU' if pl else ''}")
