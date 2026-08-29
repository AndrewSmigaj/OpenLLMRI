#!/usr/bin/env python3
"""P2 — fr occupancy time-bands + rule-(b) band (S1 want site, L14).
Band = inner-95th percentiles of D4-arm readings at matched positions (midref).
Power caveat (B2) applies to any dip verdict: at fr separation, dip power 0.01-0.10 —
band occupancy fractions and mode locations are the informative outputs, not dip tests."""
import sys
sys.path.insert(0, "docs/studies/context_shift/analysis")
import numpy as np, pandas as pd
from second_pass_r1_dynamics import fr_cfg

tag, d4a, d4b, d3, dest_fn, fam_fn = fr_cfg()
A = np.stack(d4a); B = np.stack(d4b)
mid = (A.mean(0) + B.mean(0)) / 2.0
# rule-(b) band from position-matched D4 midref readings, steps 11-40 pooled
d4_all = np.concatenate([(A - mid)[:, 10:40].ravel(), (B - mid)[:, 10:40].ravel()])
neg = d4_all[d4_all < 0]; pos = d4_all[d4_all > 0]
lo, hi = np.percentile(neg, 5), np.percentile(pos, 95)
inner_lo, inner_hi = np.percentile(neg, 95), np.percentile(pos, 5)   # inner edges
print(f"fr rule-(b) unresolved band (inner-95th of D4 sides, midref L14): "
      f"[{inner_lo:+.2f}, {inner_hi:+.2f}]  (side spans: neg {lo:+.2f}..{inner_lo:+.2f}, "
      f"pos {inner_hi:+.2f}..{hi:+.2f})")
bands = [("k1-5", 0, 5), ("k6-10", 5, 10), ("k11-15", 10, 15), ("k16-20", 15, 20)]
grid = np.linspace(-3, 3, 601)
for dsuf, sign in (("_fr", +1.0), ("_rf", -1.0)):
    ys = np.stack([((d3[n] - mid) * sign)[20:40] for n in d3 if n.endswith(dsuf)])
    print(f"\n{dsuf} (n={len(ys)} runs):")
    for bn, l, h in bands:
        x = ys[:, l:h].ravel()
        inband = ((x > inner_lo) & (x < inner_hi)).mean()
        kde = np.exp(-0.5*((grid[:,None]-x[None,:])/0.30)**2).sum(1)
        print(f"  {bn:>6}: mode {grid[kde.argmax()]:+.2f} sd {x.std():.2f} "
              f"in-band frac {inband:.2f}")
