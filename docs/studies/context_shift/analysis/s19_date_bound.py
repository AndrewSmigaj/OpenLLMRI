#!/usr/bin/env python3
"""s19 — empirical bound on the chat-template date tokens (logged post-freeze).

The chat template stamps the current date into the system message. The 24
no-shift behavior cells (12 per task, forty-sentence contexts plus the carrier)
were regenerated twice: pinned to their original capture day
(captures/behavior_{probe}_v2_log.tsv) and pinned to 2026-09-05
(captures/behavior_{probe}_datebound_log.tsv). This script reports, per task, the
distribution of |reading(today) - reading(original)| at the calibrated site, in
axis units and as a fraction of the full class separation (2 axis units), and the
share of cells whose greedy completion is unchanged. Read against the repeat-run
floor from s18 determinism (identical inputs).

Usage: s19_date_bound.py [DATEBOUND_SUFFIX]   (default "datebound")
"""
import csv, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, "docs/studies/context_shift/analysis")
from s18_regeneration_checks import text_of, reading_of, rows, C

suffix = sys.argv[1] if len(sys.argv) > 1 else "datebound"
for probe in ("tank", "fr"):
    orig = {r["set"]: r for r in rows(C / f"behavior_{probe}_v2_log.tsv") if r["set"].endswith("_beh_final")}
    today = {r["set"]: r for r in rows(C / f"behavior_{probe}_{suffix}_log.tsv")}
    d = []; same = 0; n = 0; pins = set()
    for s, r in sorted(today.items()):
        if s not in orig: print(f"  {s}: no original-pinned twin"); continue
        n += 1; pins.add((orig[s]["pinned_date"], r["pinned_date"]))
        v0, v1 = reading_of(orig[s]["session"], probe), reading_of(r["session"], probe)
        d.append(abs(v1 - v0))
        same += int(text_of(orig[s]["session"]) == text_of(r["session"]))
    d = np.array(d)
    print(f"{probe}: {n} no-shift cells, pins {sorted(pins)}")
    print(f"  |delta reading| axis units: max {d.max():.4f}, median {np.median(d):.4f}, mean {d.mean():.4f}")
    print(f"  as a fraction of the class separation (2 units): max {d.max()/2:.2%}, median {np.median(d)/2:.2%}")
    print(f"  greedy completion unchanged: {same} of {n}")
