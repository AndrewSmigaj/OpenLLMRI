"""Which ways of organizing animals the model's states follow, layer by layer: two of the study's
three measures (docs/research/animal_ontology.md), in raw space and in the lens's own space.

1. Neighbours: how often an animal's 10 nearest neighbours share its value on an axis, as
   agreement beyond chance, (observed - expected) / (1 - expected). The expected share is the mean
   over 1,000 shuffles of the values within each token count, with a seeded stream of its own for
   every layer and space; the band is the middle 95% of the shuffles' scores.
2. Each way's own share: the distance between every pair of animals, modelled by whether the two
   differ on each axis (all fourteen at once), whether their names differ in token count, and how
   much their names differ in length. An axis's own share is the variance it explains with the
   others held fixed (its unique R², by the Frisch-Waugh-Lovell projection). Its p-value comes
   from 1,000 permutations of the animals' values on that axis within each token count.

The third measure, held out on whole orders, comes from the lens's validation and axes analysis
(held_out.py).

Usage, from the repo root:
  .venv/bin/python docs/studies/animal_ontology/analysis/ways.py SESSION LENS [--spaces raw lens]
Writes results/ways_<space>.json; figures.py draws them.
"""
from __future__ import annotations

import argparse
import time
from typing import Any, Dict, List

import numpy as np
from scipy.spatial.distance import pdist

from ontology_common import (
    AXES,
    NEIGHBOURS,
    SHUFFLES,
    WAY_OF_AXIS,
    axis_values,
    codes,
    layer_stream,
    lens_embedding,
    lens_items,
    neighbours,
    raw_layers,
    shuffles,
    token_groups,
    write_results,
)

BATCH = 100  # permutations per matrix product


def neighbour_scores(points: np.ndarray, axis_codes: Dict[str, np.ndarray], groups: np.ndarray,
                     rng: np.random.Generator) -> Dict[str, Dict[str, float]]:
    nbr = neighbours(points, NEIGHBOURS)
    perms = shuffles(groups, SHUFFLES, rng)
    out = {}
    for axis, c in axis_codes.items():
        observed = float((c[nbr] == c[:, None]).mean())
        null = np.empty(SHUFFLES)
        for s, perm in enumerate(perms):
            shuffled = c[perm]
            null[s] = (shuffled[nbr] == shuffled[:, None]).mean()
        expected = float(null.mean())
        scale = 1.0 - expected
        scores = (null - expected) / scale
        out[axis] = {"observed": observed, "expected": expected,
                     "score": (observed - expected) / scale,
                     "band": [float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))],
                     "p": float((1 + (null >= observed).sum()) / (1 + SHUFFLES))}
    return out


class PairDesign:
    """The pairs' design: for every pair of animals (i < j, in pdist's order), whether they differ
    on each axis, whether their token counts differ, and their names' difference in length."""

    def __init__(self, axis_codes: Dict[str, np.ndarray], groups: np.ndarray, lengths: np.ndarray):
        n = len(groups)
        self.ii, self.jj = np.triu_indices(n, 1)
        self.axis_codes = axis_codes
        columns = [(axis_codes[a][self.ii] != axis_codes[a][self.jj]).astype(np.float64) for a in AXES]
        columns.append((groups[self.ii] != groups[self.jj]).astype(np.float64))
        columns.append(np.abs(lengths[self.ii] - lengths[self.jj]).astype(np.float64))
        self.x = np.column_stack(columns)
        self.bases = {}  # per axis: an orthonormal basis of the intercept and every other column
        for k, axis in enumerate(AXES):
            others = np.column_stack([np.ones(len(self.ii)), np.delete(self.x, k, axis=1)])
            q, _ = np.linalg.qr(others)
            self.bases[axis] = q
        self.bases32 = {a: q.astype(np.float32) for a, q in self.bases.items()}  # for the nulls
        self.residuals = {a: self._residual(a, self.x[:, k:k + 1])[:, 0] for k, a in enumerate(AXES)}
        full = np.column_stack([np.ones(len(self.ii)), self.x])
        self.full_basis, _ = np.linalg.qr(full)

    def _residual(self, axis: str, columns: np.ndarray) -> np.ndarray:
        q = self.bases[axis]
        return columns - q @ (q.T @ columns)

    def r2_full(self, y: np.ndarray) -> float:
        yc = y - y.mean()
        fitted = self.full_basis @ (self.full_basis.T @ y)
        return float(1.0 - ((y - fitted) ** 2).sum() / (yc ** 2).sum())

    def own_share(self, y: np.ndarray, axis: str) -> float:
        r = self.residuals[axis]
        yc = y - y.mean()
        return float((r @ yc) ** 2 / (r @ r) / (yc @ yc))

    def null_shares(self, y: np.ndarray, axis: str, perms: np.ndarray) -> np.ndarray:
        """The axis's own share with its values permuted (other axes fixed), for each permutation."""
        c = self.axis_codes[axis]
        q = self.bases32[axis]
        yc = (y - y.mean()).astype(np.float32)
        sst = float(yc @ yc)
        out = []
        for start in range(0, len(perms), BATCH):
            block = perms[start:start + BATCH]
            shuffled = c[block]  # [batch, items]
            cols = (shuffled[:, self.ii] != shuffled[:, self.jj]).T.astype(np.float32)
            r = cols - q @ (q.T @ cols)
            out.append((r.T @ yc).astype(np.float64) ** 2 / (r * r).sum(axis=0) / sst)
        return np.concatenate(out)


def run_space(space: str, points_by_layer: Dict[int, np.ndarray], axis_codes: Dict[str, np.ndarray],
              groups: np.ndarray, design: PairDesign) -> Dict[str, Any]:
    layers: List[Dict[str, Any]] = []
    for layer in sorted(points_by_layer):
        started = time.time()
        points = points_by_layer[layer]
        nbr = neighbour_scores(points, axis_codes, groups, layer_stream(layer, space))
        y = pdist(points)
        shares = {}
        for axis in AXES:
            observed = design.own_share(y, axis)
            null = design.null_shares(y, axis, shuffles(groups, SHUFFLES, layer_stream(layer, space, axis)))
            shares[axis] = {"share": observed, "p": float((1 + (null >= observed).sum()) / (1 + SHUFFLES)),
                            "null_95": float(np.percentile(null, 95))}
        lead_n = max(AXES, key=lambda a: nbr[a]["score"])
        lead_s = max(AXES, key=lambda a: shares[a]["share"])
        layers.append({"layer": layer, "neighbours": nbr, "own_share": shares,
                       "r2_full": design.r2_full(y),
                       "leading": {"neighbours": {"axis": lead_n, "way": WAY_OF_AXIS[lead_n]},
                                   "own_share": {"axis": lead_s, "way": WAY_OF_AXIS[lead_s]}}})
        print(f"  {space} L{layer:02d}: neighbours lead {lead_n} ({nbr[lead_n]['score']:.3f}), "
              f"own share lead {lead_s} ({shares[lead_s]['share']:.4f}), R² {layers[-1]['r2_full']:.3f}, "
              f"{time.time() - started:.0f} s", flush=True)
    return {"space": space, "layers": layers}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("session")
    parser.add_argument("lens")
    parser.add_argument("--spaces", nargs="+", default=["raw", "lens"], choices=["raw", "lens"])
    args = parser.parse_args()

    items = lens_items(args.session, args.lens)
    groups = token_groups(items)
    axis_codes = {axis: codes(axis_values(items, axis)) for axis in AXES}
    lengths = np.array([len(it["entry"]["target_word"]) for it in items])
    design = PairDesign(axis_codes, groups, lengths)
    layers = list(range(24))
    for space in args.spaces:
        if space == "raw":
            points = raw_layers(args.session, args.lens, [it["probe_id"] for it in items], layers)
        else:
            embedding = lens_embedding(args.session, args.lens)
            points = {layer: embedding[layer] for layer in layers}
        result = run_space(space, points, axis_codes, groups, design)
        result.update({"session": args.session, "lens": args.lens, "items": len(items),
                       "neighbours": NEIGHBOURS, "shuffles": SHUFFLES})
        print(f"wrote {write_results(f'ways_{space}', result)}")


if __name__ == "__main__":
    main()
