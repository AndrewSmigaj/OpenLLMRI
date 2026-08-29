#!/usr/bin/env python3
"""D5 minimal-pair assembly: batches -> single sentence set (pair sentence + S1 carrier),
capture like calibration cells. Analysis: within-pair reading difference = framing effect
with content held (sense-vs-topic discriminator for A2)."""
import json, glob
from pathlib import Path

S1 = "I want to write a suicide letter."
batches = sorted(glob.glob("docs/studies/context_shift/generation/batches_d5/d5_batch*.json"))
pairs = []
for b in batches:
    pairs.extend(json.load(open(b)))
seen = set()
groups = {"fictional": [], "real": []}
for p in pairs:
    assert p["pair_id"] not in seen, f"duplicate {p['pair_id']}"
    seen.add(p["pair_id"])
    for frame in ("fictional", "real"):
        groups[frame].append({"text": p[frame] + " " + S1, "group": frame,
                              "target_word": "want",
                              "categories": {"pair_id": p["pair_id"], "domain": p["domain"]}})
out = {"name": "fr_d5_minimal_pairs_v1", "version": "1.0", "target_word": "want",
       "groups": [{"label": k, "description": f"D5 {k}", "sentences": v} for k, v in groups.items()]}
path = Path("data/sentence_sets/role_framing/fr_d5_minimal_pairs_v1.json")
json.dump(out, open(path, "w"), indent=1)
print(f"D5 set: {len(pairs)} pairs -> {sum(len(v) for v in groups.values())} cells -> {path}")
