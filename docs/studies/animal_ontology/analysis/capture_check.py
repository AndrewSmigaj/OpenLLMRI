"""The ontology capture against the first animal capture (read-only).

The set holds the same 524 names as animals_kinship_v1, and both captures pin the chat template's
date to 2026-09-16, so for every name the token record (position, token, count, offset) and the
model's states at the name's last token should be identical: the residual stream and the routing
weights at all 24 layers, bit for bit. The categories differ on purpose (the new set adds eight).

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/capture_check.py NEW_SESSION OLD_SESSION
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np
import pyarrow.parquet as pq

from ontology_common import ROOT, set_entries, write_results

RECORD_FIELDS = ("target_word", "target_token_id", "target_token_position", "total_tokens",
                 "target_char_offset", "target_token_count", "label")


def records(session: str):
    table = pq.read_table(ROOT / "data/lake" / session / "tokens.parquet").to_pylist()
    return {r["input_text"]: r for r in table}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("new")
    parser.add_argument("old")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "backend/src"))
    from services.lenses.data import load_routing, load_states

    new, old = records(args.new), records(args.old)
    entries = set_entries()
    problems = []
    if set(new) != set(old) or set(new) != set(entries):
        problems.append(f"texts differ: {len(set(new) ^ set(old))} between captures, "
                        f"{len(set(new) ^ set(entries))} between the new capture and the set")
    texts = sorted(set(new) & set(old))
    for text in texts:
        for field in RECORD_FIELDS:
            if new[text][field] != old[text][field]:
                problems.append(f"{text!r}: {field} {new[text][field]!r} vs {old[text][field]!r}")
        cats = json.loads(new[text]["categories_json"])
        expected = entries[text]["categories"]
        if cats != expected:
            problems.append(f"{text!r}: the capture's categories differ from the set's")

    new_ids = [new[t]["probe_id"] for t in texts]
    old_ids = [old[t]["probe_id"] for t in texts]
    layers = list(range(24))
    a = load_states(args.new, new_ids, layers=layers)
    b = load_states(args.old, old_ids, layers=layers)
    residual_equal = {layer: bool(np.array_equal(a[layer], b[layer])) for layer in layers}
    largest = {layer: float(np.abs(a[layer] - b[layer]).max()) for layer in layers}
    ra = load_routing(args.new, new_ids)
    rb = load_routing(args.old, old_ids)
    routing_equal = bool(np.array_equal(ra, rb))
    for layer in layers:
        if not residual_equal[layer]:
            problems.append(f"L{layer}: residual stream differs (largest difference {largest[layer]:.3g})")
    if not routing_equal:
        problems.append(f"routing weights differ (largest difference {float(np.abs(ra - rb).max()):.3g})")

    print(f"{len(texts)} names in both captures; residual stream identical at "
          f"{sum(residual_equal.values())} of 24 layers; routing identical: {routing_equal}")
    write_results("capture_check", {"new": args.new, "old": args.old, "names": len(texts),
                                    "residual_identical_layers": sum(residual_equal.values()),
                                    "routing_identical": routing_equal, "problems": problems})
    print(f"{len(problems)} problems" + (":" if problems else ""))
    for p in problems[:30]:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
