#!/usr/bin/env python3
"""Smoke test for the sampled arm (7 September 2026), pre-stated in
findings/behavior_sampling_2026-09.md Part 1, items 8 and 9. Four generations:

  A. greedy path unchanged: a v2 cell re-run with no sampling fields must reproduce
     its stored greedy text byte for byte (fr_s1_ar_d3_fam00_fr_beh_k06, delivered
     under greedy decoding);
  B, C. determinism: a cell that looped under greedy decoding
     (fr_s1_ar_d3_fam00_fr_beh_k12) sampled twice with seed 20260907 must give
     identical text;
  D. the same cell with seed 20260908 must differ from B.

Also reports whether B, C, D reach the final channel. Run from the repository root
with the backend READY. Smoke sessions carry the suffix _smk2 (the first attempt, _smoke, pinned the wrong
date through a manifest-lookup bug, fixed 7 Sept) and are excluded
from the arm's logs.
"""
import subprocess, sys, csv
from pathlib import Path
import pandas as pd

ROOT = Path(".").resolve()
PY = str(ROOT / ".venv/bin/python")
CH = "docs/studies/context_shift/captures/behavior_chain_v2.py"
FR = "data/sentence_sets/role_framing/context_shift_behavior_fr/behavior_manifest_fr.json"
LOG = "docs/studies/context_shift/captures/behavior_fr_smk2_sampled_log.tsv"
DELIVERED, LOOPED = "fr_s1_ar_d3_fam00_fr_beh_k06", "fr_s1_ar_d3_fam00_fr_beh_k12"
V2 = "docs/studies/context_shift/analysis/r6_behavior_worksheet_fr_v2_categorized.csv"

def run(tag, cell, *extra):
    log = LOG.replace("smk2_sampled", f"smk2_{tag}")
    subprocess.run([PY, CH, FR, log, "fr", "--only", cell, "--suffix", f"_smk2{tag}", *extra], check=True)
    row = list(csv.DictReader(open(log), delimiter="\t"))[-1]
    t = pd.read_parquet(f"data/lake/{row['session']}/tokens.parquet", columns=["generated_text"])
    return row, (t.generated_text.iloc[0] or "")

def stored_text(cell):
    ws = pd.read_csv(V2); sid = ws[ws.set == cell].session.iloc[0]
    t = pd.read_parquet(f"data/lake/{sid}/tokens.parquet", columns=["generated_text"])
    return t.generated_text.iloc[0] or ""

rA, A = run("A", DELIVERED)
same_greedy = A == stored_text(DELIVERED)
rB, B = run("B", LOOPED, "--sample", "--temperature", "1.0", "--top-p", "1.0", "--seed", "20260907")
rC, C = run("C", LOOPED, "--sample", "--temperature", "1.0", "--top-p", "1.0", "--seed", "20260907")
rD, D = run("D", LOOPED, "--sample", "--temperature", "1.0", "--top-p", "1.0", "--seed", "20260908")
print("\n=== SMOKE RESULT ===")
print(f"A greedy path byte-identical to stored v2 text: {same_greedy} ({len(A)} chars)")
print(f"B==C same seed identical: {B == C} ({len(B)} / {len(C)} chars); reached final B={rB['reached_final']} C={rC['reached_final']}")
print(f"D differs from B: {D != B} ({len(D)} chars); reached final D={rD['reached_final']}")
print("secs:", rA["seconds"], rB["seconds"], rC["seconds"], rD["seconds"])
ok = same_greedy and B == C and D != B
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
