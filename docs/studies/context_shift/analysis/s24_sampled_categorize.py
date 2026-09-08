#!/usr/bin/env python3
"""s24 — blind categorization helper for the sampled-decoding arm (8 September 2026).

Doctrine: findings/behavior_sampling_2026-09.md Part 1, item 7 (unchanged from v2).
Categories are read from the delivered final answer; the reasoning channel's final
commitment is read from its last sentences before the answer. Categorization is
blind to the greedy category and to the other draws: `show` prints rows of one draw
in a shuffled order (seed 7) with no greedy column and no other draw's text.

  show  DRAW START END      print rows [START, END) of the shuffled order: id, set, the
                            first 400 characters of the final answer, the last 300 of
                            the reasoning channel
  apply DRAW MAPPING.json   write r6_behavior_worksheet_{task}_{DRAW}_categorized.csv
                            (no text columns) from {id: {category, safety_subtype,
                            reasoning_category}}; the full-text worksheet moves to
                            data/lake/_worksheets_raw/ (git-ignored)

DRAW is fr_s1, fr_s2, fr_s3, or tank_s1. Run from the repository root.
"""
import sys, json, re, shutil
from pathlib import Path
import numpy as np, pandas as pd

A = Path("docs/studies/context_shift/analysis")
RAW = Path("data/lake/_worksheets_raw")
FINAL = "assistantfinal"
KEEP = ["set", "session", "run", "k", "reading", "logprobs", "reached_final", "channel"]

def load(draw):
    task, s = draw.split("_")
    return task, s, pd.read_csv(A / f"r6_behavior_worksheet_{task}_{s}.csv")

def order(n):
    return np.random.default_rng(7).permutation(n)

def squash(t, n, tail=False):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
    return (t[-n:] if tail else t[:n])

def show(draw, start, end):
    task, s, df = load(draw)
    idx = order(len(df))[start:end]
    for i in idx:
        r = df.iloc[i]
        gen = str(r.generated_text or ""); j = gen.find(FINAL)
        reasoning = gen[:j] if j >= 0 else gen
        final = r.final_text if isinstance(r.final_text, str) else ""
        print(f"--- id={i} set={r.set} reached_final={r.reached_final}")
        print(f"REASONING TAIL: {squash(reasoning, 300, tail=True)}")
        print(f"FINAL HEAD: {squash(final, 400)}")

def apply(draw, mapping_path):
    task, s, df = load(draw)
    m = {int(k): v for k, v in json.load(open(mapping_path)).items()}
    missing = [i for i in range(len(df)) if i not in m]
    assert not missing, f"{len(missing)} rows without a category: {missing[:10]}"
    out = df[KEEP].copy()
    out["draw"] = s
    for col in ("category", "safety_subtype", "reasoning_category"):
        out[col] = [m[i].get(col, "") for i in range(len(df))]
    out["channel"] = ["final" if f == 1 else "reasoning" for f in df.reached_final]
    dest = A / f"r6_behavior_worksheet_{task}_{s}_categorized.csv"
    out.to_csv(dest, index=False)
    RAW.mkdir(parents=True, exist_ok=True)
    src = A / f"r6_behavior_worksheet_{task}_{s}.csv"
    shutil.move(str(src), str(RAW / src.name))
    print(f"wrote {dest} ({len(out)} rows); full-text worksheet moved to {RAW / src.name}")
    print(out.category.value_counts().to_string())

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "show": show(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "apply": apply(sys.argv[2], sys.argv[3])
    else: sys.exit(__doc__)
