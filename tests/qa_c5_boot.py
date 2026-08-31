#!/usr/bin/env python3
"""QA C5 — bootstrap internals. (a) Confirm resampling units are families (r1: pandas
series indexed by family; d6: rng.choice over family list). (b) The doc's residual-gap
CIs hold D4 references (midpoint + destination level) FIXED; recompute all four CIs with
references resampled (6 arm-families with replacement, midpoint AND destination rebuilt
per draw) independently of the 12 run-family resample; report side by side."""
import sys
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np
from second_pass_r1_dynamics import tank_cfg, fr_cfg, residual_gap

rng = np.random.default_rng(77)
print("(a) resampling units: r1 family_boot resamples a 12-family series (verified in "
      "code: groupby('fam') then .sample on the family series); d6 boot resamples the "
      "family list (rng.choice(fams)). PASS by inspection + fixture B6.")
print("\n(b) residual-gap CIs: fixed-reference (doc) vs references-resampled:")
for cfgf, tag in ((tank_cfg, "tank"), (fr_cfg, "fr")):
    t2, d4a, d4b, d3, dest_fn, fam_fn = cfgf()
    A = np.stack(d4a); B = np.stack(d4b)          # (6, 40) projections per arm
    mid_full = (A.mean(0) + B.mean(0)) / 2.0
    for dsuf, sign in (("+", +1.0), ("-", -1.0)):
        runs = {n: p for n, p in d3.items() if dest_fn(n) == sign}
        fams = sorted({fam_fn(n) for n in runs})
        by_fam = {f: [n for n in runs if fam_fn(n) == f] for f in fams}
        # fixed-reference boot (doc's method, seeded like r1)
        gaps_fixed = {f: np.mean([residual_gap(runs[n], mid_full, sign, (B if sign > 0 else A))
                                  for n in by_fam[f]]) for f in fams}
        fixed_boots = [np.mean([gaps_fixed[f] for f in rng.choice(fams, len(fams), replace=True)])
                       for _ in range(2000)]
        # references-resampled boot
        ref_boots = []
        for _ in range(2000):
            ai = rng.choice(6, 6, replace=True); bi = rng.choice(6, 6, replace=True)
            Ar, Br = A[ai], B[bi]
            midr = (Ar.mean(0) + Br.mean(0)) / 2.0
            Dm = (Br if sign > 0 else Ar)
            fpick = rng.choice(fams, len(fams), replace=True)
            g = np.mean([residual_gap(runs[n], midr, sign, Dm)
                         for f in fpick for n in by_fam[f]])
            ref_boots.append(g)
        fl, fh = np.percentile(fixed_boots, [2.5, 97.5])
        rl, rh = np.percentile(ref_boots, [2.5, 97.5])
        print(f"  {tag} dest{dsuf}: fixed-ref CI [{fl:+.2f},{fh:+.2f}] (width {fh-fl:.2f}) | "
              f"refs-resampled CI [{rl:+.2f},{rh:+.2f}] (width {rh-rl:.2f}) | "
              f"excludes 0: {'YES' if rl > 0 else 'NO'}")
