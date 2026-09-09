#!/usr/bin/env python3
"""Blind rater QC pass, builder + scorer (pre-registration v2).

build: shuffles all v2 pool sentences (seed 17) into chunks of 50 and writes one
rater prompt per chunk. The rater sees only the two class descriptions for the
task and the sentences; forced choice A or B per line. Chunks are per task
(tank; fiction/real with three-way choice fiction-writing / real-world, since the
sub-arms share the fiction-writing class).
score: reads the raters' answer files, joins to the hidden key, prints
misclassified sentences per batch (these are replaced authoring-side).

Usage: build_rater_pass.py build   |   build_rater_pass.py score
"""
import glob, json, random, sys, pathlib
G = pathlib.Path("docs/studies/context_shift/generation")
R = G / "rater_v2"; R.mkdir(exist_ok=True)
DESC = {
 "tank": ("A: about keeping fish or aquatic life (aquariums, ponds, aquaculture)",
          "B: about armored military vehicles (their history, models, depictions, industry)"),
 "fr":   ("A: about making or discussing a work of fiction (any craft or medium)",
          "B: a first-person account of the speaker's own real life circumstances"),
}
def rows():
    for f in sorted(glob.glob(str(G / "batches_v2" / "*.txt"))):
        b = f.split("/")[-1].removesuffix(".txt")
        task = "tank" if b.startswith("tank") else "fr"
        truth = "A" if (b.startswith("tank_aq") or b.startswith("fic")) else "B"
        for i, l in enumerate([l.strip() for l in open(f) if l.strip()]):
            yield {"batch": b, "task": task, "truth": truth, "i": i, "text": l}
if sys.argv[1] == "build":
    data = list(rows()); random.Random(17).shuffle(data)
    key = {}
    chunks = {"tank": [], "fr": []}
    for r in data: chunks[r["task"]].append(r)
    n = 0
    for task, items in chunks.items():
        for c in range(0, len(items), 50):
            chunk = items[c:c+50]; cid = f"{task}_{c//50:02d}"
            lines = [f"{j+1}. {r['text']}" for j, r in enumerate(chunk)]
            key[cid] = [[r["batch"], r["i"], r["truth"]] for r in chunk]
            a, b = DESC[task]
            (R / f"{cid}.prompt.txt").write_text(
f"""You are labeling sentences for a linguistics dataset. For each numbered sentence, decide which description fits better:
{a}
{b}

Answer with one line per sentence: the number, a space, then A or B. Nothing else.

{chr(10).join(lines)}
""")
            n += 1
    json.dump(key, open(R / "key.json", "w"))
    print(f"{n} rater chunks built over {len(data)} sentences -> {R}")
else:
    key = json.load(open(R / "key.json")); bad = {}
    for cid, entries in key.items():
        af = R / f"{cid}.answers.txt"
        if not af.exists(): print(f"missing answers: {cid}"); continue
        ans = {}
        for l in af.read_text().splitlines():
            p = l.strip().split()
            if len(p) >= 2 and p[0].rstrip(".").isdigit(): ans[int(p[0].rstrip("."))] = p[1].upper()[:1]
        for j, (batch, i, truth) in enumerate(entries):
            got = ans.get(j + 1, "?")
            if got != truth: bad.setdefault(batch, []).append((i, got, truth))
    total = sum(len(v) for v in bad.values())
    for b in sorted(bad):
        print(f"MISCLASSIFIED in {b}: {len(bad[b])} -> lines {[i+1 for i,_,_ in bad[b]]}")
    print(f"RESULT: {total} misclassified of {sum(len(v) for v in key.values())}")
