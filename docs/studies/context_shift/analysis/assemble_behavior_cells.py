#!/usr/bin/env python3
"""Assemble v2 behavior generation contexts (pre-registration v2).

From assembled run JSONs (PREFIX_d3_famNN_{dir}.json, PREFIX_d4_famNN_{x}.json) emit
one behavior cell set per (run, k) with the cumulative text at post-shift step k
(position 20+k) for transitions, and at position 40 for no-shift runs. k in
{2,6,9,12,20}. Cells are captured by behavior_chain_v2.py, which supplies the
generation flags. Also writes the chain manifest [{name, substring, run, k}].

Usage: assemble_behavior_cells.py RUN_DIR CARRIER OUT_DIR MANIFEST_OUT
"""
import json, glob, sys
from pathlib import Path
KS = [2, 6, 9, 12, 20]
run_dir, carrier, out_dir, man_out = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
out_dir.mkdir(parents=True, exist_ok=True)
man = []
def emit(run_name, tw, text, tag, k):
    name = f"{run_name}_beh_{tag}"
    doc = {"name": name, "version": "1.0", "target_word": tw,
           "groups": [{"label": "beh", "description": f"behavior cell {tag}",
                       "sentences": [{"text": text, "group": "beh", "target_word": tw,
                                      "categories": {"run": run_name, "k": k}}]}]}
    json.dump(doc, open(out_dir / f"{name}.json", "w"))
    man.append({"name": name, "substring": carrier, "run": run_name, "k": k})
for f in sorted(glob.glob(f"{run_dir}/*_d3_fam*.json")) + sorted(glob.glob(f"{run_dir}/*_d4_fam*.json")):
    d = json.load(open(f))
    run_name = d["name"]; tw = d["target_word"]
    sents = d["groups"][0]["sentences"]
    bypos = {int(s["categories"]["position"]): s["text"] for s in sents}
    if "_d3_" in run_name:
        for k in KS:
            emit(run_name, tw, bypos[20 + k], f"k{k:02d}", str(k))
    else:
        emit(run_name, tw, bypos[40], "final", "d4_final")
json.dump(man, open(man_out, "w"), indent=1)
print(f"{len(man)} behavior cells -> {out_dir}; manifest {man_out}")
