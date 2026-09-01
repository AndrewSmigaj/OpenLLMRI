#!/usr/bin/env python3
"""s12 — R4-5 descriptive counts (logged post-freeze addition, QA appendix): how
mid-band tank responses express (or fail to express) uncertainty. Descriptive
re-count of the committed categorized worksheet + text scan for clarification
requests / explicit uncertainty-about-which reports."""
import re
import numpy as np, pandas as pd

df = pd.read_csv("docs/studies/context_shift/analysis/r6_behavior_worksheet_tank_categorized.csv")
df = df[df.k != "d4_final"]
r_or = np.where(df.set.str.contains("_ab_"), df.reading, -df.reading)
mid = df[np.abs(r_or) <= 0.5]
print(f"mid-band cells (|dest-oriented reading| <= 0.5): n={len(mid)}")
print(mid.category.value_counts().to_string())
CLAR = [r"which (do you|did you|sense do you) mean", r"could you clarify", r"do you mean the",
        r"can you clarify", r"please clarify", r"ambiguous.*please", r"need more context to answer",
        r"cannot determine which", r"unclear which .* you mean"]
def asks_clarification(txt):
    t = str(txt).lower()
    return any(re.search(p, t) for p in CLAR)
n_clar = int(mid.generated_text.apply(asks_clarification).sum())
n_all = int(df.generated_text.apply(asks_clarification).sum())
print(f"responses asking the user for clarification / declining pending disambiguation: "
      f"mid-band {n_clar}/{len(mid)}; all cells {n_all}/{len(df)}")
commit = mid.category.isin(["aquarium", "vehicle"]).sum()
both = (mid.category == "both").sum()
print(f"mid-band: {commit} commit to a single sense ({commit/len(mid):.0%}), "
      f"{both} enumerate both senses ({both/len(mid):.0%}), "
      f"{(mid.category=='no_answer').sum()} fail to answer")
