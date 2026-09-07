#!/usr/bin/env python3
"""s23 — what a fixed recency weighting predicts for the dwelling window (6 September 2026).

Supports the §4 caveat on the dwelling plateau's location. A recency integrator
weights the sentence of age a by gamma**a and reads the weighted mean of the class
reference levels, here in units of the no-shift amplitude, signed toward the
destination. After k post-shift sentences (twenty origin sentences, then k
destination), the destination block's share of the weight is
(1 - gamma**k) / (1 - gamma**(20 + k)) and the reading is 2*share - 1. Uniform
weighting (gamma = 1) gives (k - 20)/(k + 20): the midpoint exactly at k = 20.

Observed values entered as constants from the paper: tank aquarium->vehicle late
slope bound [-0.040, +0.024] axis units per sentence over post-shift sentences 11-20
(addendum Part 5); amplitude 2.02 axis units (Part 5); remnant gap +2.16 [1.87, 2.44]
axis units (Table 2), so the plateau sits at 1 - gap/amplitude of the way to the
destination. Reverse direction: gamma 0.94 (Table 2), gap +1.15 [0.82, 1.45].
"""
AMP = 2.02
SLOPE_HI = 0.024          # axis units per sentence, upper bound of the late-slope interval
FLAT = SLOPE_HI * 10 / AMP  # the largest rise over the ten-sentence window the data allow, in amplitude units

def reading(g, k):
    share = (k / (20 + k)) if g == 1.0 else (1 - g**k) / (1 - g**(20 + k))
    return 2 * share - 1

print(f"observed plateau, aquarium->vehicle: {1 - 2.16/AMP:+.2f} of the amplitude "
      f"[{1 - 2.44/AMP:+.2f}, {1 - 1.87/AMP:+.2f}]; allowed rise over sentences 11-20: <= {FLAT:+.2f}")
for g in (0.91, 0.94, 0.97, 0.99, 1.0):
    r10, r20 = reading(g, 10), reading(g, 20)
    print(f"gamma {g:.2f}: reading {r10:+.2f} at k=10, {r20:+.2f} at k=20; rise over 11-20 {r20 - r10:+.2f}")
# the largest gamma whose rise over 11-20 stays within the observed bound, and where it sits
g = 1.0
while reading(g, 20) - reading(g, 10) > FLAT:
    g -= 0.001
print(f"flat within the bound requires gamma <= {g:.2f}, which sits at {reading(g, 20):+.2f} of the amplitude at k=20")
print(f"reverse direction, gamma 0.94: predicted {reading(0.94, 20):+.2f} at k=20 against observed "
      f"{1 - 1.15/AMP:+.2f} [{1 - 1.45/AMP:+.2f}, {1 - 0.82/AMP:+.2f}]; predicted rise over 11-20 "
      f"{(reading(0.94, 20) - reading(0.94, 10)) * AMP / 10:+.3f} axis units per sentence against observed [+0.025, +0.133]")
