"""Each axis alone: a descriptive companion to ways.py's own share (read-only).

ways.py gives each axis's own share of the pairwise distances with every other axis held fixed.
Several ways follow descent closely (everyday kind, covering, legs), so most of what they explain
they explain together, and their own shares are small. Here each axis is fitted alone, beside the
two controls only (whether the names differ in token count, and their difference in length), and
its share is the variance it explains over the controls, as a fraction of the variance the
controls leave (a partial R²). The gap between an axis's share alone and its own share is what it
holds in common with the other ways. No p-values: alone, every axis tied to descent explains far
more than chance, and the question here is how much.

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/alone.py SESSION LENS
Writes results/alone_<space>.json; figures.py draws it.
"""
from __future__ import annotations

import argparse

import numpy as np
from scipy.spatial.distance import pdist

from ontology_common import (
    AXES,
    axis_values,
    codes,
    lens_embedding,
    lens_items,
    raw_layers,
    token_groups,
    write_results,
)


def r2(basis: np.ndarray, y: np.ndarray) -> float:
    yc = y - y.mean()
    fitted = basis @ (basis.T @ y)
    return float(1.0 - ((y - fitted) ** 2).sum() / (yc @ yc))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session")
    parser.add_argument("lens")
    args = parser.parse_args()
    items = lens_items(args.session, args.lens)
    groups = token_groups(items)
    lengths = np.array([len(it["entry"]["target_word"]) for it in items], dtype=float)
    ii, jj = np.triu_indices(len(items), 1)
    controls = np.column_stack([np.ones(len(ii)), (groups[ii] != groups[jj]).astype(float),
                                np.abs(lengths[ii] - lengths[jj])])
    control_basis, _ = np.linalg.qr(controls)
    bases = {}
    for axis in AXES:
        c = codes(axis_values(items, axis))
        bases[axis], _ = np.linalg.qr(np.column_stack([controls, (c[ii] != c[jj]).astype(float)]))
    layers = list(range(24))
    spaces = {"raw": raw_layers(args.session, args.lens, [it["probe_id"] for it in items], layers)}
    embedding = lens_embedding(args.session, args.lens)
    spaces["lens"] = {layer: embedding[layer] for layer in layers}
    for space, points in spaces.items():
        rows = []
        for layer in layers:
            y = pdist(points[layer])
            base = r2(control_basis, y)
            alone = {axis: (r2(bases[axis], y) - base) / (1.0 - base) for axis in AXES}
            rows.append({"layer": layer, "r2_controls": base, "alone": alone})
            lead = max(AXES, key=lambda a: alone[a])
            print(f"  {space} L{layer:02d}: controls R² {base:.3f}; alone, {lead} leads with "
                  f"{100 * alone[lead]:.1f}% of what the controls leave")
        print(f"wrote {write_results(f'alone_{space}', {'space': space, 'session': args.session, 'lens': args.lens, 'layers': rows})}")


if __name__ == "__main__":
    main()
