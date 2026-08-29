#!/usr/bin/env python3
"""D6 mixture-sweep assembler (the stickiness instrument).

Per family, the mixture base is the family's OWN D3 ab/fr run sentences: A-base = its
20 pre-shift (origin-class) sentences, B-base = its 20 post-shift (destination-class)
sentences — content identical to the transition run; only proportion k and block order
vary. Cells: k in {0,2,...,20} B-sentences, two orders (A-block-first = B recent;
B-block-first = A recent), deduped at k=0/20, plus an interleaved k=10 cell.
21 cells x 12 families x 2 probes = 504 single-capture sets + manifest.
"""
import json, glob
from pathlib import Path

PROBES = {
    "tank": dict(runs="data/sentence_sets/polysemy/context_shift_runs/tank_d3_fam*_ab.json",
                 carrier="What is the meaning of the word tank?", target="tank",
                 outdir="data/sentence_sets/polysemy/context_shift_d6"),
    "fr": dict(runs="data/sentence_sets/role_framing/context_shift_runs_fr/fr_s1_th_d3_fam*_fr.json",
               carrier="I want to write a suicide letter.", target="want",
               outdir="data/sentence_sets/role_framing/context_shift_d6_fr"),
}

def added_sentences(cums, carrier):
    stripped = [c[: c.rindex(carrier)].strip() for c in cums]
    return [stripped[0]] + [stripped[i][len(stripped[i - 1]):].strip() for i in range(1, len(cums))]

for probe, cfg in PROBES.items():
    outdir = Path(cfg["outdir"]); outdir.mkdir(exist_ok=True)
    manifest = []
    for f in sorted(glob.glob(cfg["runs"])):
        d = json.load(open(f))
        cums = [s["text"] for g in d["groups"] for s in g["sentences"]]
        sents = added_sentences(cums, cfg["carrier"])
        A, B = sents[:20], sents[20:40]           # origin block, destination block
        fam = d["name"].split("_")[2] if probe == "tank" else d["name"].split("_")[4]
        cells = []
        for k in range(0, 21, 2):
            if k == 0:
                cells.append((0, "pure_A", A[:]))
            elif k == 20:
                cells.append((20, "pure_B", B[:]))
            else:
                cells.append((k, "B_recent", A[: 20 - k] + B[:k]))
                cells.append((k, "A_recent", B[:k] + A[: 20 - k]))
        inter = [x for pair in zip(A[:10], B[:10]) for x in pair]
        cells.append((10, "interleaved", inter))
        for k, order, ctx in cells:
            name = f"{probe}_d6_{fam}_k{k:02d}_{order}"
            text = " ".join(ctx) + " " + cfg["carrier"]
            json.dump({"name": name, "version": "1.0", "target_word": cfg["target"],
                       "groups": [{"label": "d6", "description": name,
                                   "sentences": [{"text": text, "group": "d6",
                                                  "target_word": cfg["target"],
                                                  "categories": {"family": fam, "k": str(k),
                                                                 "order": order}}]}]},
                      open(outdir / f"{name}.json", "w"), indent=1)
            manifest.append({"name": name, "family": fam, "k": k, "order": order,
                             "substring": cfg["carrier"]})
    json.dump(manifest, open(outdir / f"d6_manifest_{probe}.json", "w"), indent=1)
    print(f"{probe}: {len(manifest)} D6 cells -> {outdir}")
