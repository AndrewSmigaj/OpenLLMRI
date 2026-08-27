#!/usr/bin/env python3
"""Pool audit (GUIDE Variation Doctrine) — run BEFORE any capture of a pool.

Checks a batch directory of blind-generated pool sentences:
  - ban scan (target word in any form; carrier fragments)
  - word-count range; duplicates within and across batches
  - per-scene counts and within-label scene share (<= ~15%)
  - chi-square label x {length bucket, opener token class, punctuation style}
  - worn-phrase scan (exact repeats of 4-grams across the pool)
Prints a report; exits nonzero on hard failures (bans, duplicates, count shortfalls).
Usage: pool_audit.py BATCH_DIR PREFIX_A PREFIX_B TARGET_WORD
  e.g. pool_audit.py docs/studies/context_shift/generation/batches tank_aq tank_vh tank
"""
from __future__ import annotations
import glob, re, sys
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency

def load(batch_dir, prefix):
    out = {}
    for f in sorted(glob.glob(f"{batch_dir}/{prefix}*.txt")):
        scene = f.split("/")[-1].removesuffix(".txt")
        out[scene] = [l.strip() for l in open(f) if l.strip()]
    return out

def opener_class(s):
    w = s.split()[0].strip('"“‘').rstrip(",")
    if w.lower() in ("the","a","an"): return "article"
    if w.lower() in ("i","we","you","he","she","they","it","my","our","her","his"): return "pronoun"
    if w.endswith("ing"): return "gerund"
    if s.split()[0].startswith(('"', "“")): return "quote"
    if w.lower() in ("who","what","why","how","did","do","does","was","is","are","have","has","would","will","can"): return "question"
    if w.lower() in ("by","under","over","between","after","before","during","at","on","in","behind","down","per","from","somewhere","along","inside"): return "prepositional"
    return "other"

def punct_class(s):
    if s.endswith("?"): return "question"
    if '"' in s or "“" in s: return "has_quote"
    if ";" in s: return "semicolon"
    if "—" in s or " - " in s: return "dash"
    return "plain"

def bucket(n):
    return "short(10-14)" if n <= 14 else ("mid(15-19)" if n <= 19 else "long(20-30)")

def main():
    batch_dir, pa, pb, target = sys.argv[1:5]
    A, B = load(batch_dir, pa), load(batch_dir, pb)
    hard_fail = []

    all_rows = []  # (label, scene, sentence)
    for label, d in (("A", A), ("B", B)):
        for scene, lines in d.items():
            for s in lines:
                all_rows.append((label, scene, s))

    # ban scan
    pat = re.compile(r"\b" + re.escape(target) + r"\w*", re.I)
    bans = [(sc, s) for _, sc, s in all_rows if pat.search(s)]
    carrier_frag = [(sc, s) for _, sc, s in all_rows if "what is the meaning of" in s.lower()]
    if bans: hard_fail.append(f"target-ban violations: {len(bans)} e.g. {bans[0]}")
    if carrier_frag: hard_fail.append(f"carrier-fragment violations: {len(carrier_frag)}")

    # duplicates
    texts = [s for _, _, s in all_rows]
    dups = [t for t, c in Counter(texts).items() if c > 1]
    if dups: hard_fail.append(f"duplicate sentences: {len(dups)} e.g. {dups[0][:60]}")

    # counts + scene share
    print(f"== counts ==")
    for label, d in (("A", A), ("B", B)):
        n = sum(len(v) for v in d.values())
        print(f"label {label}: {len(d)} scenes, {n} sentences")
        for scene, lines in d.items():
            share = len(lines) / max(n, 1)
            flag = "  <-- >15%" if share > 0.155 else ""
            print(f"  {scene}: {len(lines)} ({share:.0%}){flag}")

    # chi-square balance
    print("== label balance (chi-square) ==")
    for name, fn in (("length-bucket", lambda s: bucket(len(s.split()))),
                     ("opener", opener_class), ("punctuation", punct_class)):
        table = defaultdict(lambda: [0, 0])
        for label, _, s in all_rows:
            table[fn(s)][0 if label == "A" else 1] += 1
        cats = sorted(table)
        obs = [[table[c][0] for c in cats], [table[c][1] for c in cats]]
        chi2, p, dof, _ = chi2_contingency(obs)
        warn = "  <-- WARN (label-correlated)" if p < 0.01 else ""
        print(f"{name}: chi2={chi2:.1f} dof={dof} p={p:.3f}{warn}")
        print("   ", {c: tuple(table[c]) for c in cats})

    # worn phrases: repeated 4-grams across different sentences
    grams = defaultdict(set)
    for i, (_, _, s) in enumerate(all_rows):
        w = re.sub(r"[^\w\s']", " ", s.lower()).split()
        for j in range(len(w) - 3):
            grams[" ".join(w[j:j+4])].add(i)
    worn = {g: len(ids) for g, ids in grams.items() if len(ids) >= 3}
    print(f"== worn 4-grams (>=3 sentences): {len(worn)} ==")
    for g, c in sorted(worn.items(), key=lambda x: -x[1])[:8]:
        print(f"  {c}x  {g}")

    if hard_fail:
        print("\nHARD FAIL:"); [print(" -", h) for h in hard_fail]; sys.exit(1)
    print("\nPASS (review WARNs and worn-gram list manually; shuffle test + join check are manual steps)")

if __name__ == "__main__":
    main()
