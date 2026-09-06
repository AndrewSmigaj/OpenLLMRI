#!/usr/bin/env python3
"""s18 — integrity checks for the regenerated behavior corpus (logged post-freeze).

Modes:
  determinism LOG          rows of LOG come in pairs <set>_r1 / <set>_r2 (same cell fired
                           twice with the same pin and cap): compare generated text and
                           the calibrated-site reading between repeats.
  extension PROBE [V2LOG]  for every cell in captures/behavior_{PROBE}_log.tsv (frozen)
                           and its twin in V2LOG (default behavior_{PROBE}_v2_log.tsv):
                           the frozen text must be a prefix of the regenerated text
                           (the frozen text was decoded from exactly 256 tokens, so a
                           trailing U+FFFD from a split multi-byte character is
                           stripped first); readings must match; count reached-final
                           and capped cells; report lengths.
  agreement PROBE          reasoning-channel commitment vs delivered final answer: needs
                           the v2 categorized worksheet (category = from the final answer)
                           and the frozen categorized worksheet (category = from the
                           reasoning channel where the final was not reached).
"""
import csv, sys, json, re
from pathlib import Path
import numpy as np, pandas as pd

C = Path("docs/studies/context_shift/captures"); A = Path("docs/studies/context_shift/analysis")
AX = {"tank": (4, A / "axes/axes_session_29a80932_aquarium_vs_vehicle_pos1.npz"),
      "fr": (14, A / "axes/axes_session_5247081b_fictional_vs_real_pos1.npz")}
FINAL = "assistantfinal"

def text_of(sid):
    t = pd.read_parquet(Path("data/lake") / sid / "tokens.parquet", columns=["generated_text"])
    return t.generated_text.iloc[0] or ""

def reading_of(sid, probe):
    L, axf = AX[probe]; ax = np.load(axf)
    res = pd.read_parquet(Path("data/lake") / sid / "residual_streams.parquet")
    res = res[(res.layer == L) & (res.token_position == 1)]
    X = np.asarray(res.residual_stream.iloc[0], dtype=np.float64)
    return float(2.0 * ((X - ax[f"mid_{L}"]) @ ax[f"axis_{L}"]) / float(ax[f"denom_{L}"]))

def rows(log):
    return [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]

def repetition(text, n=60, step=20):
    """Share of overlapping n-character shingles that repeat, over the given text.
    Degenerate loops score high (about 0.5 to 0.9); ordinary prose scores near 0."""
    sh = [text[i:i + n] for i in range(0, max(0, len(text) - n), step)]
    return 1 - len(set(sh)) / max(1, len(sh))

def enumeration_loop(text):
    """Second loop signature: the same sentence frame repeated with a varying noun
    ("The user might be wanting help with X." ...). Returns the share of the last
    3,000 characters' sentences that open with the single most common four-word
    opener; degenerate enumerations score 0.4 and above."""
    import collections
    sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", text[-3000:]) if x.strip()]
    if len(sents) < 8: return 0.0
    openers = [" ".join(x.split()[:4]) for x in sents]
    return collections.Counter(openers).most_common(1)[0][1] / len(sents)

def n_tokens(text):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("data/models/gpt-oss-20b")
    return len(tok.encode(text, add_special_tokens=False))

def determinism(log):
    rs = rows(log); by = {}
    for r in rs: by.setdefault(r["set"].rsplit("_r", 1)[0], {})[r["set"].rsplit("_r", 1)[1]] = r
    probe = "fr" if next(iter(by)).startswith("fr_") else "tank"
    for base, reps in sorted(by.items()):
        if len(reps) < 2: print(f"  {base}: only one repeat logged"); continue
        (k1, r1), (k2, r2) = sorted(reps.items())[:2]
        t1, t2 = text_of(r1["session"]), text_of(r2["session"])
        v1, v2 = reading_of(r1["session"], probe), reading_of(r2["session"], probe)
        same_text = t1 == t2
        ndiff = next((i for i, (a, b) in enumerate(zip(t1, t2)) if a != b), min(len(t1), len(t2)))
        print(f"  {base}: text identical={same_text} (first differing char {ndiff} of {len(t1)}/{len(t2)}); "
              f"reading {v1:+.6f} vs {v2:+.6f}, |delta|={abs(v1-v2):.2e}; seconds {r1['seconds']}/{r2['seconds']}")

def extension(probe, v2log=None):
    frozen = {r["set"]: r for r in rows(C / f"behavior_{probe}_log.tsv")}
    new = {re.sub(r"_r\d+$", "", r["set"]): r for r in rows(v2log or C / f"behavior_{probe}_v2_log.tsv")}
    cap = int(next(iter(new.values()))["cap"]) if new else None
    ok = bad = fin = capped = 0; dr = []; lens = []; bad_list = []; capped_list = []
    for s, r in sorted(new.items()):
        if s not in frozen: print(f"  {s}: no frozen twin"); continue
        old, cur = text_of(frozen[s]["session"]), text_of(r["session"])
        old_c = old.rstrip("�")
        if cur.startswith(old_c): ok += 1
        else:
            bad += 1; i = next((i for i, (a, b) in enumerate(zip(old_c, cur)) if a != b), min(len(old_c), len(cur)))
            bad_list.append((s, i, len(old_c), len(cur)))
        f = FINAL in cur; fin += int(f); lens.append(len(cur))
        if not f or n_tokens(cur) >= cap - 4: capped += 1; capped_list.append((s, f, len(cur), max(repetition(cur[-3000:]), enumeration_loop(cur))))
        dr.append(abs(reading_of(frozen[s]["session"], probe) - reading_of(r["session"], probe)))
    n = ok + bad
    print(f"{probe}: {n} regenerated cells; frozen text is a prefix of the new text in {ok}; mismatches {bad}")
    for s, i, lo, lc in bad_list: print(f"   MISMATCH {s}: first differing char {i} (frozen {lo} chars, new {lc})")
    print(f"  reached final answer: {fin} of {n}; still capped or unfinished: {capped}")
    loops = [x for x in capped_list if x[3] >= 0.3]
    print(f"  of the capped cells, {len(loops)} score as loops (verbatim repetition >= 30% of shingles, or one sentence frame >= 30% of sentences, over the last 3,000 chars); "
          f"{len(capped_list) - len(loops)} do not")
    for s, f, l, rp in capped_list:
        if rp < 0.3: print(f"   capped but NOT a loop {s}: reached_final={f}, chars={l}, repetition={rp:.2f}")
    if dr: print(f"  |reading(new) - reading(frozen)|: max {max(dr):.2e}, median {np.median(dr):.2e}")
    if lens: print(f"  new text length chars: min {min(lens)}, median {int(np.median(lens))}, max {max(lens)}")

def agreement(probe):
    """Reasoning channel vs delivered answer, on the v2 categorized worksheet. Two
    reasoning readings: `reasoning_commitment` (frozen category: for cells whose
    256-token output had not reached an answer, the early reasoning, first 1,200
    characters) and `reasoning_category` (the reasoning channel's final commitment
    before the answer, read for every cell that delivered one; early reading kept
    for loops)."""
    new = pd.read_csv(A / f"r6_behavior_worksheet_{probe}_v2_categorized.csv")
    print(f"{probe}: {len(new)} cells")
    print("frozen category (early reasoning where the 256-token output had not answered) vs delivered:")
    print(pd.crosstab(new.reasoning_commitment, new.category).to_string())
    print("reasoning channel's final commitment vs delivered:")
    print(pd.crosstab(new.reasoning_category, new.category).to_string())
    dl = new[new.category != "no_answer"]
    print(f"  delivered cells: {len(dl)}; reasoning final commitment equals the delivered category in {int((dl.reasoning_category == dl.category).sum())}")
    if probe == "fr":
        from scipy.stats import fisher_exact
        fic = new.reasoning_category.isin(["fiction_frame", "mixed"]); loop = new.category == "no_answer"
        a, b, c, d = int((fic & loop).sum()), int((fic & ~loop).sum()), int((~fic & loop).sum()), int((~fic & ~loop).sum())
        print(f"  loop rate by reasoning commitment: fiction-writing-committed {a} of {a+b}; safety-committed {c} of {c+d}; Fisher exact p = {fisher_exact([[a, b], [c, d]])[1]:.3f}")
        new["band"] = pd.cut(new.reading, [-10, -0.5, 0.5, 10], labels=["fiction-writing side", "middle", "real-world side"])
        g = new.groupby("band").agg(n=("set", "size"), reasoning_fiction=("reasoning_category", lambda s: s.isin(["fiction_frame", "mixed"]).sum()),
                                    reasoning_safety=("reasoning_category", lambda s: (s == "safety_response").sum()),
                                    delivered=("category", lambda s: (s != "no_answer").sum()), delivered_fiction=("category", lambda s: (s == "fiction_frame").sum()),
                                    delivered_safety=("category", lambda s: (s == "safety_response").sum()), loops=("category", lambda s: (s == "no_answer").sum()))
        print("  by band (reasoning commitment counts all cells; delivered counts answered cells):"); print(g.to_string())

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "determinism": determinism(sys.argv[2])
    elif mode == "extension": extension(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif mode == "agreement": agreement(sys.argv[2])
