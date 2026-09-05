#!/usr/bin/env python3
"""s12 — descriptive counts (logged post-freeze addition, QA appendix): how the tank
responses express, or fail to express, uncertainty about which sense is meant.
Descriptive re-count of the committed categorized worksheet plus a text scan for
clarification requests / declining pending disambiguation.

Usage: s12_r4_counts.py [v1|v2]
  v1 (default): the frozen 256-token captures; the scan covers the first 1,200
      characters of each raw output, as the frozen worksheet did, so the frozen
      printed values reproduce. Transition cells only (96), as frozen.
  v2: the regenerated captures (2,048-token cap); the scan covers the delivered
      final answer (text after "assistantfinal") and, separately, the full output;
      transition cells (96) and all cells (108) are both reported.
Text is read from the archived captures (data/lake), not from the worksheet: the
committed worksheets carry no completion text (release policy, paper §4).
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

VERSION = sys.argv[1] if len(sys.argv) > 1 else "v1"
SUF = "" if VERSION == "v1" else f"_{VERSION}"
A = Path("docs/studies/context_shift/analysis")
df = pd.read_csv(A / f"r6_behavior_worksheet_tank{SUF}_categorized.csv")

def raw(sid):
    t = pd.read_parquet(Path("data/lake") / sid / "tokens.parquet", columns=["generated_text"])
    return t.generated_text.iloc[0] or ""
df["full"] = df.session.map(raw)
if VERSION == "v1":
    df["scan"] = df.full.str[:1200]
else:
    df["scan"] = df.full.apply(lambda g: g[g.find("assistantfinal") + len("assistantfinal"):] if "assistantfinal" in g else "")

CLAR = [r"which (do you|did you|sense do you) mean", r"could you clarify", r"do you mean the",
        r"can you clarify", r"please clarify", r"ambiguous.*please", r"need more context to answer",
        r"cannot determine which", r"unclear which .* you mean"]
def asks_clarification(txt):
    t = str(txt).lower()
    return any(re.search(p, t) for p in CLAR)

tr = df[df.k != "d4_final"]
r_or = np.where(tr.set.str.contains("_ab_"), tr.reading, -tr.reading)
mid = tr[np.abs(r_or) <= 0.5]
print(f"[{VERSION}] transition cells n={len(tr)}; mid-band cells (|dest-oriented reading| <= 0.5): n={len(mid)}")
print(mid.category.value_counts().to_string())
n_clar_mid = int(mid.scan.apply(asks_clarification).sum()); n_clar_tr = int(tr.scan.apply(asks_clarification).sum())
what = "first 1,200 chars of the raw output" if VERSION == "v1" else "delivered final answer"
print(f"responses asking the user for clarification / declining pending disambiguation ({what}): "
      f"mid-band {n_clar_mid}/{len(mid)}; transition cells {n_clar_tr}/{len(tr)}")
if VERSION != "v1":
    n_all_final = int(df.scan.apply(asks_clarification).sum()); n_all_full = int(df.full.apply(asks_clarification).sum())
    print(f"  all {len(df)} cells (incl. no-shift finals): final answer {n_all_final}/{len(df)}; anywhere in the raw output {n_all_full}/{len(df)}")
    print(f"  cells whose output reached the final answer: {int(df.full.str.contains('assistantfinal').sum())}/{len(df)}")
commit = mid.category.isin(["aquarium", "vehicle"]).sum(); both = (mid.category == "both").sum()
print(f"mid-band: {commit} commit to a single sense ({commit/len(mid):.0%}), "
      f"{both} enumerate both senses ({both/len(mid):.0%}), {(mid.category=='no_answer').sum()} fail to answer")
