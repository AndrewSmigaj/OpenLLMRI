#!/usr/bin/env python3
"""Sweep-cell behavior manifest (pre-registration v2): fiction/real sweep cells at
k in {8,10,12}, both block orders, all sweep families -> [{name, substring}] for
behavior_chain_v2.py. Usage: build_sweep_behavior_manifest.py D6_LOG CARRIER OUT"""
import csv, json, re, sys
log, carrier, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows = [r for r in csv.DictReader(open(log), delimiter="\t") if r["status"] == "ok"]
man, seen = [], set()
for r in rows:
    name = r["set"]
    m = re.search(r"_k(\d+)_", name + "_")
    if not m: continue
    if int(m.group(1)) in (8, 10, 12) and "interleav" not in name and name not in seen:
        seen.add(name); man.append({"name": name, "substring": carrier})
json.dump(man, open(out, "w"), indent=1)
print(f"{len(man)} sweep behavior cells -> {out}")
