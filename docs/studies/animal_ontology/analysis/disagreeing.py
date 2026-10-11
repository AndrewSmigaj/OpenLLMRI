"""The animals where the ways disagree, with their nearest neighbours (read-only).

For each example animal, at a few layers and in both spaces (raw: the residual stream standardized
and reduced to 50 principal components; lens: the lens's own embedding), its 10 nearest neighbours,
and how many of them share its value on each axis where the ways part: descent says a whale is a
mammal, its everyday kind says fish-like, its habitat says sea. The examples show the measures at
work on single animals; the counts are within the whole set, not within each token count, so the
token count is printed beside each animal and its neighbours.

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/disagreeing.py SESSION LENS
Writes results/disagreeing.json.
"""
from __future__ import annotations

import argparse
from typing import Any, Dict, List

from ontology_common import (
    axis_values,
    lens_embedding,
    lens_items,
    neighbours,
    raw_layers,
    write_results,
)

EXAMPLES = ("whale", "dolphin", "orca", "narwhal", "manatee", "seal", "walrus", "otter", "platypus",
            "bat", "penguin", "ostrich", "emu", "cassowary", "starfish", "jellyfish", "cuttlefish",
            "crayfish", "silverfish", "eel", "lamprey", "hagfish", "slowworm", "caecilian",
            "amphiuma", "mudskipper")
COMPARED = ("group", "kind", "covering", "legs", "habitat", "movement", "tokens")
LAYERS = (2, 6, 12, 18, 23)
SHOWN = 5


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session")
    parser.add_argument("lens")
    args = parser.parse_args()
    items = lens_items(args.session, args.lens)
    words = [it["entry"]["target_word"] for it in items]
    values = {axis: axis_values(items, axis) for axis in COMPARED}
    present = [w for w in EXAMPLES if w in words]
    raw = raw_layers(args.session, args.lens, [it["probe_id"] for it in items], list(LAYERS))
    embedding = lens_embedding(args.session, args.lens)
    out: Dict[str, Any] = {"session": args.session, "lens": args.lens, "layers": list(LAYERS),
                           "compared": list(COMPARED), "animals": {}}
    for word in present:
        i = words.index(word)
        own = {axis: values[axis][i] for axis in COMPARED}
        rows: List[Dict[str, Any]] = []
        for space, points in (("raw", raw), ("lens", {layer: embedding[layer] for layer in LAYERS})):
            for layer in LAYERS:
                nbr = neighbours(points[layer])[i]
                rows.append({"space": space, "layer": layer,
                             "nearest": [words[j] for j in nbr[:SHOWN]],
                             "share": {axis: float(sum(values[axis][j] == own[axis] for j in nbr) / len(nbr))
                                       for axis in COMPARED}})
        out["animals"][word] = {"values": own, "rows": rows}
        print(f"\n{word} ({', '.join(f'{a} {own[a]}' for a in COMPARED)})")
        for row in rows:
            shares = " ".join(f"{a[:5]} {row['share'][a]:.1f}" for a in COMPARED)
            print(f"  {row['space']:4s} L{row['layer']:02d}  {shares}  | {', '.join(row['nearest'])}")
    print(f"\nwrote {write_results('disagreeing', out)}")


if __name__ == "__main__":
    main()
