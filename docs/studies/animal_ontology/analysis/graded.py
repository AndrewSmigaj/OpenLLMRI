"""Danger's own share with size and danger graded (read-only): a check on ways.py.

ways.py enters every axis as "differ or not", so a pair of a huge and a tiny animal counts the same
as a pair of a large and a huge one. The animals that can kill are mostly large, so part of what
danger explains there may be graded size. Here size (tiny < small < medium < large < huge) and
danger (harmless < can hurt < can kill) enter as how many steps apart the two animals are, every
other axis and the controls as before, and danger's and size's own shares are tested again with
1,000 permutations within each token count, in both spaces at every layer.

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/graded.py SESSION LENS
Writes results/graded.json.
"""
from __future__ import annotations

import argparse
from typing import Dict

import numpy as np
from scipy.spatial.distance import pdist

from ontology_common import (
    AXES,
    SHUFFLES,
    axis_values,
    codes,
    layer_stream,
    lens_embedding,
    lens_items,
    raw_layers,
    shuffles,
    token_groups,
    write_results,
)

GRADED = {"size": ["tiny", "small", "medium", "large", "huge"],
          "danger": ["harmless", "can hurt", "can kill"]}
BATCH = 100


def column(values: np.ndarray, axis: str, ii: np.ndarray, jj: np.ndarray) -> np.ndarray:
    """A pair's column for an axis: steps apart for a graded axis, else whether they differ."""
    if axis in GRADED:
        return np.abs(values[..., ii] - values[..., jj]).astype(np.float32)
    return (values[..., ii] != values[..., jj]).astype(np.float32)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session")
    parser.add_argument("lens")
    args = parser.parse_args()
    items = lens_items(args.session, args.lens)
    groups = token_groups(items)
    lengths = np.array([len(it["entry"]["target_word"]) for it in items], dtype=float)
    values: Dict[str, np.ndarray] = {}
    for axis in AXES:
        raw = axis_values(items, axis)
        values[axis] = (np.array([GRADED[axis].index(v) for v in raw], dtype=np.int32)
                        if axis in GRADED else codes(raw))
    ii, jj = np.triu_indices(len(items), 1)
    columns = {axis: column(values[axis], axis, ii, jj) for axis in AXES}
    controls = [(groups[ii] != groups[jj]).astype(np.float32), np.abs(lengths[ii] - lengths[jj]).astype(np.float32)]
    bases, residuals = {}, {}
    for axis in GRADED:
        others = np.column_stack([np.ones(len(ii), dtype=np.float32)] + controls
                                 + [columns[a] for a in AXES if a != axis])
        q, _ = np.linalg.qr(others.astype(np.float64))
        bases[axis] = q.astype(np.float32)
        c = columns[axis][:, None]
        residuals[axis] = (c - bases[axis] @ (bases[axis].T @ c))[:, 0]
    layers = list(range(24))
    spaces = {"raw": raw_layers(args.session, args.lens, [it["probe_id"] for it in items], layers)}
    embedding = lens_embedding(args.session, args.lens)
    spaces["lens"] = {layer: embedding[layer] for layer in layers}
    out = {"session": args.session, "lens": args.lens, "graded": GRADED, "shuffles": SHUFFLES, "spaces": {}}
    for space, points in spaces.items():
        rows = []
        for layer in layers:
            y = pdist(points[layer]).astype(np.float32)
            yc = y - y.mean()
            sst = float(yc @ yc)
            row = {"layer": layer}
            for axis in GRADED:
                r = residuals[axis]
                observed = float((r @ yc) ** 2 / (r @ r) / sst)
                perms = shuffles(groups, SHUFFLES, layer_stream(layer, space, axis))
                null = []
                q = bases[axis]
                for start in range(0, SHUFFLES, BATCH):
                    shuffled = values[axis][perms[start:start + BATCH]]
                    cols = column(shuffled, axis, ii, jj).T
                    res = cols - q @ (q.T @ cols)
                    null.append((res.T @ yc).astype(np.float64) ** 2 / (res * res).sum(axis=0) / sst)
                null = np.concatenate(null)
                row[axis] = {"share": observed, "p": float((1 + (null >= observed).sum()) / (1 + SHUFFLES))}
            rows.append(row)
            print(f"  {space} L{layer:02d}: danger {100 * row['danger']['share']:.3f}% (p {row['danger']['p']:.3f}), "
                  f"size {100 * row['size']['share']:.3f}% (p {row['size']['p']:.3f})", flush=True)
        out["spaces"][space] = rows
    print(f"wrote {write_results('graded', out)}")


if __name__ == "__main__":
    main()
