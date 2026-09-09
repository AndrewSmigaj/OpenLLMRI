#!/usr/bin/env python3
"""v2 pool audit (8 September 2026) — the pre-registered hard gates over the v2 batches.

Runs the checks of preregistration_v2.md ("Authoring and audit protocol") over
generation/batches_v2/*.txt, with the v1 pools folded in:
  1. bans: target word forms (tank batches), carrier fragments, worn phrases
  2. sub-arm rules: theme-only bans 'suicide letter/note/message'; artifact-mentioned
     requires 'suicide letter' or 'suicide note' in EVERY sentence; real bans
     suicide/self-harm lexicon and fiction-craft framing words
  3. exact duplicates within v2 and against v1 pools
  4. near-duplicates: lowercased content-token Jaccard >= 0.6, within v2 and vs v1
  5. batch counts (25) and word-count range (10-30)
  6. personal-name reuse across families (v2 x v2 and v2 x v1)
  7. chi-square balance of length bucket / opener class / punctuation across labels
Exit nonzero on any hard failure; prints per-batch replacement lists.
"""
import glob, json, re, sys, itertools
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency

B = "docs/studies/context_shift/generation/batches_v2"
V1_POOLS = ["data/sentence_sets/polysemy/tank_scene_pools_v1.json",
            "data/sentence_sets/role_framing/fiction_real_scene_pools_v1.json"]
CARRIER_FRAGS = ["what is the meaning of", "define the word", "i want to write a suicide",
                 "i would like to write a suicide", "help me write a suicide"]
WORN = ["nobody warn", "little did", "at the end of the day"]
METHOD = ["pills", "overdose", "rope", "noose", "hanging", "razor", "blade", "jump from", "bridge railing", "carbon monoxide", "firearm", "gun"]
STOPNAMES = set("""the a an i we you he she they it my our her his their monday tuesday wednesday thursday
friday saturday sunday january february march april may june july august september october november december
sherman tiger panzer churchill abrams leopard""".split())
FUNC = set("""a an the and or but if of in on at to for with by from as is are was were be been being it its
this that these those i we you he she they them his her their my our your me us not no so than then too very
just also only into over under after before during about against between out up down off""".split())

def toks(s): return [w for w in re.findall(r"[a-z']+", s.lower()) if w not in FUNC]
def jac(a, b):
    A, Bt = set(a), set(b)
    return len(A & Bt) / max(1, len(A | Bt))
def names_in(s):
    return {m.group(1) for m in re.finditer(r"(?<!^)(?<![.!?\"“] )\b([A-Z][a-z]{2,10})\b", s)
            if m.group(1).lower() not in STOPNAMES}
def opener(s):
    w = s.split()[0].strip('"“‘').rstrip(",").lower()
    if w in ("the","a","an"): return "article"
    if w in ("i","we","you","he","she","they","it","my","our","her","his"): return "pronoun"
    if s.split()[0].startswith(('"',"“")): return "quote"
    if w in ("who","what","why","how","did","do","does","was","is","are","have","has","would","will","can","could","should"): return "question"
    if w in ("by","under","over","between","after","before","during","at","on","in","behind","down","per","from","somewhere","along","inside","tonight","every"): return "prep/adv"
    return "other"
def punct(s):
    if s.endswith("?"): return "question"
    if '"' in s or "“" in s: return "quote"
    if ";" in s: return "semicolon"
    if "—" in s or " - " in s: return "dash"
    return "plain"

# ---- load v2 batches
rows = []  # (batch, label, idx, sentence)
for f in sorted(glob.glob(f"{B}/*.txt")):
    name = f.split("/")[-1].removesuffix(".txt")
    label = ("tank_aq" if name.startswith("tank_aq") else "tank_vh" if name.startswith("tank_vh")
             else "fic_theme" if name.startswith("fic_theme") else "fic_artifact" if name.startswith("fic_artifact")
             else "real")
    for i, l in enumerate([l.strip() for l in open(f) if l.strip()]):
        rows.append((name, label, i, l))
if not rows: sys.exit("no v2 batches found")

# ---- load v1 sentences + names + token sets
v1 = []
for p in V1_POOLS:
    d = json.load(open(p))
    for g in d["groups"]:
        for s in g["sentences"]:
            v1.append(s["text"])
v1_toks = [toks(s) for s in v1]
v1_names = set().union(*[names_in(s) for s in v1]) if v1 else set()

hard, repl = [], defaultdict(list)
def flag(batch, i, s, why):
    repl[batch].append((i, why, s[:70]))

# 1+2: bans and sub-arm rules
for batch, label, i, s in rows:
    low = s.lower()
    if label.startswith("tank") and re.search(r"\btank\w*", low): flag(batch, i, s, "target-ban")
    if any(c in low for c in CARRIER_FRAGS): flag(batch, i, s, "carrier-fragment")
    if any(w in low for w in WORN): flag(batch, i, s, "worn-phrase")
    if label == "fic_theme" and re.search(r"suicide (letter|note|message)", low): flag(batch, i, s, "theme-only artifact ban")
    if label == "fic_artifact" and not re.search(r"suicide (letter|note)", low): flag(batch, i, s, "artifact-required missing")
    if label == "real" and re.search(r"suicide|self-harm|kill (myself|himself|herself)", low): flag(batch, i, s, "real-label lexicon ban")
    if label == "real" and re.search(r"\b(novel|manuscript|screenplay|fiction|character arc|plot)\b", low): flag(batch, i, s, "real-label fiction framing")
    if label in ("fic_theme", "fic_artifact", "real") and any(m in low for m in METHOD): flag(batch, i, s, "method-lexicon ban (safe messaging)")
    n = len(s.split())
    if not (10 <= n <= 30): flag(batch, i, s, f"word-count {n}")

# 3+4: duplicates and near-duplicates
seen = {}
tok_cache = {(b, i): toks(s) for b, _, i, s in rows}
for b, _, i, s in rows:
    key = s.lower()
    if key in seen: flag(b, i, s, f"exact dup of {seen[key]}")
    else: seen[key] = f"{b}:{i}"
    if key in {t.lower() for t in v1}: flag(b, i, s, "exact dup of a v1 sentence")
v2_list = [(b, i, tok_cache[(b, i)]) for b, _, i, s in rows]
for (b1, i1, t1), (b2, i2, t2) in itertools.combinations(v2_list, 2):
    if abs(len(t1) - len(t2)) <= 6 and jac(t1, t2) >= 0.6:
        flag(b2, i2, "", f"near-dup (J>=0.6) of {b1}:{i1}")
for b, i, t in v2_list:
    for j, tv in enumerate(v1_toks):
        if abs(len(t) - len(tv)) <= 6 and jac(t, tv) >= 0.6:
            flag(b, i, "", f"near-dup of v1 sentence {j}"); break

# 5: counts
per = Counter(b for b, *_ in rows)
for b, c in per.items():
    if c != 25: hard.append(f"{b}: {c} sentences (need 25)")

# 6: name reuse
by_fam_names = defaultdict(set)
for b, _, i, s in rows: by_fam_names[b] |= names_in(s)
for b1, b2 in itertools.combinations(sorted(by_fam_names), 2):
    shared = by_fam_names[b1] & by_fam_names[b2]
    if shared: hard.append(f"name reuse {b1} & {b2}: {sorted(shared)}")
for b, ns in by_fam_names.items():
    shared = ns & v1_names
    if shared: hard.append(f"name reuse with v1 pool in {b}: {sorted(shared)}")

# 7: balance (tank aq vs vh; fic vs real)
def balance(la, lb, tag):
    sel = [(lab, s) for _, lab, _, s in rows if lab in (la, lb)]
    if not sel: return
    for fn, nm in ((lambda s: "short" if len(s.split()) <= 14 else "mid" if len(s.split()) <= 19 else "long", "length"),
                   (opener, "opener"), (punct, "punct")):
        tab = defaultdict(Counter)
        for lab, s in sel: tab[lab][fn(s)] += 1
        cats = sorted({c for v in tab.values() for c in v})
        m = [[tab[l][c] for c in cats] for l in (la, lb)]
        try:
            chi, p, *_ = chi2_contingency(m)
            print(f"balance {tag} {nm}: chi2={chi:.1f} p={p:.3f}" + ("  <-- imbalance p<0.01" if p < 0.01 else ""))
        except Exception: pass

print(f"v2 batches: {len(per)}; sentences: {len(rows)}")
balance("tank_aq", "tank_vh", "tank")
balance("fic_theme", "real", "fr(theme)")
balance("fic_artifact", "real", "fr(artifact)")
for b in sorted(repl):
    print(f"REPLACE in {b}: {len(repl[b])}")
    for i, why, s in repl[b][:8]: print(f"   line {i+1}: {why}  {s}")
nfail = sum(len(v) for v in repl.values()) + len(hard)
for h in hard: print("HARD:", h)
print(f"RESULT: {'PASS' if nfail == 0 else f'FAIL ({nfail} items)'}")
sys.exit(0 if nfail == 0 else 1)
