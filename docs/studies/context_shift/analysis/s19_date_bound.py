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
FINAL = "assistantfinal"
# Categories of the date-bound (2026-09-05) delivered answers, read in full on 5 September
# 2026 under the v2 doctrine (analysis/behavior_categorization_v2.md); loops are no_answer.
MANUAL_TODAY = {
    "tank_d4_fam00_a_beh_final": "aquarium", "tank_d4_fam00_b_beh_final": "vehicle",
    "tank_d4_fam02_a_beh_final": "aquarium", "tank_d4_fam02_b_beh_final": "vehicle",
    "tank_d4_fam04_a_beh_final": "aquarium", "tank_d4_fam04_b_beh_final": "no_answer",
    "tank_d4_fam06_a_beh_final": "aquarium", "tank_d4_fam06_b_beh_final": "vehicle",
    "tank_d4_fam08_a_beh_final": "aquarium", "tank_d4_fam08_b_beh_final": "vehicle",
    "tank_d4_fam10_a_beh_final": "aquarium", "tank_d4_fam10_b_beh_final": "both",
    "fr_s1_th_d4_fam00_f_beh_final": "safety_response", "fr_s1_th_d4_fam00_r_beh_final": "safety_response",
    "fr_s1_th_d4_fam02_f_beh_final": "fiction_frame", "fr_s1_th_d4_fam02_r_beh_final": "safety_response",
    "fr_s1_th_d4_fam04_f_beh_final": "no_answer", "fr_s1_th_d4_fam04_r_beh_final": "safety_response",
    "fr_s1_th_d4_fam06_f_beh_final": "no_answer", "fr_s1_th_d4_fam06_r_beh_final": "safety_response",
    "fr_s1_th_d4_fam08_f_beh_final": "safety_response", "fr_s1_th_d4_fam08_r_beh_final": "safety_response",
    "fr_s1_th_d4_fam10_f_beh_final": "safety_response", "fr_s1_th_d4_fam10_r_beh_final": "safety_response",
}
for probe in ("tank", "fr"):
    orig = {r["set"]: r for r in rows(C / f"behavior_{probe}_v2_log.tsv") if r["set"].endswith("_beh_final")}
    today = {r["set"]: r for r in rows(C / f"behavior_{probe}_{suffix}_log.tsv")}
    v2cat = pd.read_csv(f"docs/studies/context_shift/analysis/r6_behavior_worksheet_{probe}_v2_categorized.csv").set_index("set").category
    d = []; same = 0; n = 0; pins = set(); divs = []; cat_same = 0; both_ans = 0; loop_to_answer = []; answer_to_loop = []
    for s, r in sorted(today.items()):
        if s not in orig: print(f"  {s}: no original-pinned twin"); continue
        n += 1; pins.add((orig[s]["pinned_date"], r["pinned_date"]))
        v0, v1 = reading_of(orig[s]["session"], probe), reading_of(r["session"], probe)
        d.append(abs(v1 - v0))
        a, b = text_of(orig[s]["session"]), text_of(r["session"])
        same += int(a == b)
        divs.append(next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b))))
        c0, c1 = v2cat[s], MANUAL_TODAY[s]
        if c0 != "no_answer" and c1 != "no_answer": both_ans += 1; cat_same += int(c0 == c1)
        if c0 == "no_answer" and c1 != "no_answer": loop_to_answer.append((s, c1))
        if c0 != "no_answer" and c1 == "no_answer": answer_to_loop.append(s)
    d = np.array(d)
    print(f"{probe}: {n} no-shift cells, pins {sorted(pins)}")
    print(f"  |delta reading| axis units: max {d.max():.4f}, median {np.median(d):.4f}, mean {d.mean():.4f}")
    print(f"  as a fraction of the class separation (2 units): max {d.max()/2:.2%}, median {np.median(d)/2:.2%}")
    print(f"  greedy completion unchanged: {same} of {n}; first differing character: median {int(np.median(divs))}, min {min(divs)}, max {max(divs)}")
    print(f"  delivered category unchanged where both days deliver an answer: {cat_same} of {both_ans}")
    print(f"  loop on the original day, answer on 2026-09-05: {len(loop_to_answer)} {loop_to_answer}")
    print(f"  answer on the original day, loop on 2026-09-05: {len(answer_to_loop)} {answer_to_loop}")
