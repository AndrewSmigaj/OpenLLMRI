#!/usr/bin/env python3
"""s23 — weight the destination block carries under recency weighting (6 September 2026).

Supports the §4 caveat on the dwelling plateau's location. A recency integrator
weights the sentence of age a by gamma**a. In a forty-sentence context whose last
twenty sentences are the destination class, the destination block's share of the
weight is (1 - gamma**20) / (1 - gamma**40), and the equilibrium reading, in units of
the no-shift amplitude and signed toward the destination, is 2*share - 1. Uniform
weighting (gamma = 1) gives share 0.5: the midpoint, reached only when the twentieth
post-shift sentence arrives. The tank sweep-fitted gammas are 0.91 and 0.97 (Table 5).
"""
for g in (0.91, 0.94, 0.97, 0.99, 1.0):
    share = 0.5 if g == 1.0 else (1 - g**20) / (1 - g**40)
    print(f"gamma {g:.2f}: destination block carries {share:.3f} of the weight -> "
          f"equilibrium reading {2*share-1:+.2f} of the amplitude toward the destination")
# crossing under uniform weighting: after k post-shift sentences the average of
# twenty origin and k destination sentences is (k - 20)/(k + 20): zero at k = 20.
print("uniform weighting crosses the midpoint at post-shift sentence", 20)
