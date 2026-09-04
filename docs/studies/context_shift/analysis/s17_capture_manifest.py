#!/usr/bin/env python3
"""s17 — capture manifest for the archived raw captures (availability statement).

The raw residual-stream captures are not in the repository. This script writes
docs/studies/context_shift/captures/capture_manifest.csv: one row per file in each
study session (sessions whose manifest carries a prompt_format tag), with the
session id, sentence-set name, corpus label, capture date, file name, size in
bytes, and SHA-256. The corpus label maps each session to a row of the paper's
Table 1 by its sentence-set name. A reader who obtains the archive can verify it
against this file.
"""
import csv, glob, hashlib, json, os, re
from pathlib import Path

LAKE = Path("data/lake"); OUT = Path("docs/studies/context_shift/captures/capture_manifest.csv")
CORPUS = [
    (r"tank_d3_fam\d+_(ab|ba)$",            "tank transition run"),
    (r"tank_d4_fam\d+_(a|b)$",              "tank no-shift run"),
    (r"tank_q1_calibration_v1$",            "tank calibration set"),
    (r"tank_d[34]_fam\d+_\w+_ck\d+$",       "tank checkpoint capture"),
    (r"tank_d[34]_fam\d+_\w+_full40$",      "tank full-window checkpoint capture"),
    (r"tank_d[34]_fam\d+_\w+_beh_\w+$",     "tank behavior completion"),
    (r"tank_d6_.*",                         "tank mixture-sweep cell"),
    (r"tank_q1b_calibration_v1$",           "tank replicate-carrier calibration set"),
    (r"tank_q1b_.*",                        "tank replicate-carrier run"),
    (r"fr_s1_(th|ar)_d3_fam\d+_(fr|rf)$",   "fiction/real transition run"),
    (r"fr_s1_th_d4_fam\d+_(f|r)$",          "fiction/real no-shift run"),
    (r"fr_s[123]_calibration_v1$",          "fiction/real calibration set"),
    (r"fr_s1_\w+_ck\d+$",                   "fiction/real checkpoint capture"),
    (r"fr_s1_\w+_beh_\w+$",                 "fiction/real behavior completion"),
    (r"fr_d6_.*",                           "fiction/real mixture-sweep cell"),
    (r"fr_d5_.*",                           "fiction/real minimal pairs"),
    (r"fr_s[23]_.*",                        "fiction/real paraphrase-carrier run"),
    (r"d7_.*",                              "bare-carrier baseline"),
    (r"context_shift_.*|logprob_smoke_.*",  "smoke / gate check"),
]
def corpus(name):
    for pat, lab in CORPUS:
        if re.fullmatch(pat, name): return lab
    return "other"
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""): h.update(chunk)
    return h.hexdigest()

rows = []
sessions = []
for f in sorted(glob.glob(str(LAKE / "_sessions" / "session_*.json"))):
    d = json.load(open(f))
    if not d.get("prompt_format"): continue
    sessions.append((d["session_id"], d.get("sentence_set_name") or "", str(d.get("created_at", ""))[:10], f))
for sid, name, day, mf in sessions:
    files = [mf] + sorted(str(p) for p in (LAKE / sid).rglob("*") if p.is_file())
    for p in files:
        rows.append({"session_id": sid, "sentence_set": name, "corpus": corpus(name), "capture_date": day,
                     "file": os.path.relpath(p, LAKE), "bytes": os.path.getsize(p), "sha256": sha256(p)})
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
tot = sum(r["bytes"] for r in rows)
print(f"{len(sessions)} sessions, {len(rows)} files, {tot/1e9:.1f} GB -> {OUT}")
import collections
for lab, n in sorted(collections.Counter(s[1] and corpus(s[1]) for s in sessions).items()): print(f"  {n:5d}  {lab}")
