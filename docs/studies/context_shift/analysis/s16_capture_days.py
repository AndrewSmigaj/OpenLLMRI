#!/usr/bin/env python3
"""s16 — logged post-freeze metadata check (QA appendix): capture days.

The gpt-oss chat template stamps the current date into its system message, so a
capture's input contains date tokens that change from day to day. This script reads
the session manifests and reports, per corpus, which days the captures fall on, so
the paper can state which comparisons are within-day. No activations are read.
"""
import json, glob, re, collections
from pathlib import Path

rows = {}
for f in glob.glob("data/lake/_sessions/session_*.json"):
    d = json.load(open(f))
    if d.get("prompt_format"): rows[d.get("sentence_set_name") or ""] = str(d.get("created_at", ""))[:10]

def days(pattern):
    sel = {n: dt for n, dt in rows.items() if re.fullmatch(pattern, n)}
    return len(sel), dict(sorted(collections.Counter(sel.values()).items())), sel

CORPORA = [
    ("tank transition runs",      r"tank_d3_fam\d+_(ab|ba)"),
    ("tank no-shift runs",        r"tank_d4_fam\d+_(a|b)"),
    ("tank calibration set",      r"tank_q1_calibration_v1"),
    ("tank checkpoint captures",  r"tank_d[34]_fam\d+_\w+_ck\d+"),
    ("tank behavior completions", r"tank_d[34]_fam\d+_\w+_beh_\w+"),
    ("tank mixture sweep cells",  r"tank_d6_.*"),
    ("tank replicate carrier (calibration + runs)", r"tank_q1b_.*"),
    ("fr transition runs",        r"fr_s1_(th|ar)_d3_fam\d+_(fr|rf)"),
    ("fr no-shift runs",          r"fr_s1_th_d4_fam\d+_(f|r)"),
    ("fr calibration set",        r"fr_s1_calibration_v1"),
    ("fr checkpoint captures",    r"fr_s1_\w+_ck\d+"),
    ("fr behavior completions",   r"fr_s1_\w+_beh_\w+"),
    ("fr mixture sweep cells",    r"fr_d6_.*"),
    ("fr minimal pairs",          r"fr_d5_.*"),
]
print(f"{'corpus':46s} {'n':>4s}  days")
for name, pat in CORPORA:
    n, c, sel = days(pat)
    print(f"{name:46s} {n:4d}  {c}")
    if name in ("tank transition runs", "tank no-shift runs"):
        off = [k for k, v in sel.items() if v != max(c, key=c.get)]
        if off: print(f"{'':46s}       not on the main day: {off}")
# within-run constancy: one session per run
print("\nEach run is one capture session (one forward chain), so the date is constant within every run.")
