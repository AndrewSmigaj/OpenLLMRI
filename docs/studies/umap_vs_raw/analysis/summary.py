"""Scores and comparisons from the held-out groupings (`heldout.py`), for every capture done.

For every attribute and every pair of attributes neither of which is a function of the other, at
every layer, per method (the UMAP lens, raw Ward, raw spectral) and k from 2 to 10: held-out kappa
and AMI, scored as validation scores them. Then three comparisons of the UMAP lens with each raw
grouping:

- **at the same k,** every k from 2 to 10: the difference in kappa;
- **at each method's best k** (by held-out kappa, chosen the same way for every method, so equally
  optimistic): the difference of the bests;
- **at the natural k** (the attribute's number of values, or the pair's joint values, kept within
  2 to 10): the difference with a 95% interval from 1,000 paired bootstraps of whole units (the
  folds' families, or texts where there are none), a seeded stream per capture, code and layer. The
  interval covers which items were held out, not UMAP's own randomness.

Also checked: on the label, every layer and k, the scores here equal the lens's stored validation
(UMAP, raw Ward and raw spectral), where the lens has one made with the same settings.

  .venv/bin/python docs/studies/umap_vs_raw/analysis/summary.py
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

import numpy as np

from common import CAPTURES, KS, METHODS, RESULTS, ROOT, cuts_dir, scores, write_json

SEED = 1
BOOTSTRAPS = 1000
MARGIN = 0.05  # the earlier notes' line for "ahead" or "behind" at the same k


def kappa_rows(truth: np.ndarray, guess: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Cohen's kappa for each row of item weights [B, n] (a bootstrap's multiplicities)."""
    values = np.unique(np.concatenate([truth, guess]))
    t = np.searchsorted(values, truth)
    g = np.searchsorted(values, guess)
    v = len(values)
    onehot = np.zeros((len(truth), v * v))
    onehot[np.arange(len(truth)), t * v + g] = 1.0
    table = (weights @ onehot).reshape(-1, v, v)
    total = table.sum(axis=(1, 2))
    observed = np.trace(table, axis1=1, axis2=2) / total
    expected = (table.sum(axis=2) * table.sum(axis=1)).sum(axis=1) / total ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (observed - expected) / (1 - expected)
    return np.where(np.isfinite(out), out, 0.0)


def bootstrap(pred: np.ndarray, code: np.ndarray, units: np.ndarray, rng: np.random.Generator) -> Dict[str, Any]:
    """Paired bootstrap of the kappa difference, UMAP minus each raw grouping, at one k."""
    keep = code >= 0
    truth, unit = code[keep], units[keep]
    names, index = np.unique(unit, return_inverse=True)
    draws = rng.integers(0, len(names), size=(BOOTSTRAPS, len(names)))
    counts = np.stack([np.bincount(row, minlength=len(names)) for row in draws]).astype(float)
    weights = counts[:, index]
    ones = np.ones((1, len(truth)))
    kap = {method: kappa_rows(truth, pred[m][keep], weights) for m, method in enumerate(METHODS)}
    point = {method: float(kappa_rows(truth, pred[m][keep], ones)[0]) for m, method in enumerate(METHODS)}
    out: Dict[str, Any] = {"kappa": {m: round(point[m], 4) for m in METHODS}}
    for method in METHODS[1:]:
        diff = kap["umap"] - kap[method]
        lo, hi = np.percentile(diff, [2.5, 97.5])
        out[f"umap-{method}"] = {"diff": round(point["umap"] - point[method], 4),
                                 "low": round(float(lo), 4), "high": round(float(hi), 4)}
    return out


def natural_k(values: int) -> int:
    return min(max(values, KS[0]), KS[-1])


def reproduce(name: str, design: Dict[str, Any], label_scores: Dict[int, Dict[str, np.ndarray]]) -> Any:
    """The largest difference from the lens's stored validation on the label, or None when it has none
    made with these settings."""
    path = ROOT / "data/lake" / design["session"] / "lenses" / design["lens"] / "validation.json"
    if not path.exists():
        return None
    stored = json.loads(path.read_text())
    worst = 0.0
    for layer, s in label_scores.items():
        for j, k in enumerate(KS):
            umap = stored["layers"][str(layer)][str(k)]["heldout"]["label"]
            for measure in ("kappa", "accuracy", "ami"):
                worst = max(worst, abs(round(float(s[measure][0, j]), 4) - umap[measure]))
                for m, method in enumerate(METHODS[1:], 1):
                    raw = stored["comparison"][str(layer)][method][str(k)]
                    worst = max(worst, abs(round(float(s[measure][m, j]), 4) - raw[measure]))
    return round(worst, 6)


def capture_summary(ci: int, name: str) -> Dict[str, Any]:
    folder = cuts_dir(name)
    design = json.loads((folder / "design.json").read_text())
    folds = [np.asarray(f) for f in design["folds"]]
    units = np.asarray(design["units"])
    codes = {**{a: np.asarray(c) for a, c in design["codes"].items()},
             **{p: np.asarray(c) for p, c in design["pair_codes"].items()}}
    kinds = {**{a: "attribute" for a in design["codes"]},
             **{p: ("crossed pair" if about["crossed"] else "correlated pair") for p, about in design["pairs"].items()}}
    values = {**{a: len(v) for a, v in design["axes"].items()},
              **{p: about["values"] for p, about in design["pairs"].items()}}
    table: Dict[str, Dict[str, Any]] = {c: {} for c in codes}
    full: Dict[str, np.ndarray] = {}
    label_scores: Dict[int, Dict[str, np.ndarray]] = {}
    for layer in design["layers"]:
        cuts = np.load(folder / f"cuts_L{layer:02d}.npy")
        for c_i, (code_name, code) in enumerate(codes.items()):
            s = scores(cuts, folds, code)
            if code_name == "label":
                label_scores[layer] = s
            full[f"{code_name}|{layer}|kappa"] = s["kappa"]
            full[f"{code_name}|{layer}|ami"] = s["ami"]
            kn = natural_k(values[code_name])
            j = KS.index(kn)
            rng = np.random.default_rng([SEED, ci, c_i, layer])
            boot = bootstrap(s["predictions"][:, j, :], code, units, rng)
            best_j = s["kappa"].argmax(axis=1)
            best_ami = s["ami"].argmax(axis=1)
            same_k = {method: (s["kappa"][0] - s["kappa"][m]).round(4).tolist() for m, method in enumerate(METHODS) if m}
            table[code_name][str(layer)] = {
                "natural_k": kn, "at_natural_k": boot,
                "best": {method: {"k": KS[int(best_j[m])], "kappa": round(float(s["kappa"][m, best_j[m]]), 4)}
                         for m, method in enumerate(METHODS)},
                "best_ami": {method: {"k": KS[int(best_ami[m])], "ami": round(float(s["ami"][m, best_ami[m]]), 4)}
                             for m, method in enumerate(METHODS)},
                "same_k_diff": same_k}
        print(f"  {name} L{layer:02d}", flush=True)
    np.savez_compressed(folder / "scores.npz", **{key: value for key, value in full.items()})
    return {"session": design["session"], "lens": design["lens"], "items": len(design["items"]),
            "folding": design["folding"], "kinds": kinds, "values": values, "pairs": design["pairs"],
            "reproduces_validation": reproduce(name, design, label_scores), "codes": table}


def tally(summaries: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Counts over every capture, code and layer, by kind of code and comparison."""
    out: Dict[str, Any] = {}
    for kind in ("attribute", "crossed pair", "correlated pair", "all"):
        for method in METHODS[1:]:
            boot = {"ahead": 0, "behind": 0, "unclear": 0}
            best = {"ahead": 0, "behind": 0, "within": 0}
            same = {"ahead": 0, "behind": 0, "within": 0}
            best_diffs: List[float] = []
            for summary in summaries.values():
                for code_name, by_layer in summary["codes"].items():
                    if kind != "all" and summary["kinds"][code_name] != kind:
                        continue
                    for cell in by_layer.values():
                        b = cell["at_natural_k"][f"umap-{method}"]
                        boot["ahead" if b["low"] > 0 else "behind" if b["high"] < 0 else "unclear"] += 1
                        d = cell["best"]["umap"]["kappa"] - cell["best"][method]["kappa"]
                        best_diffs.append(d)
                        best["ahead" if d > MARGIN else "behind" if d < -MARGIN else "within"] += 1
                        for x in cell["same_k_diff"][method]:
                            same["ahead" if x > MARGIN else "behind" if x < -MARGIN else "within"] += 1
            if best_diffs:
                out[f"{kind}|{method}"] = {"natural_k_bootstrap": boot, "best_k": best, "same_k": same,
                                           "best_k_median_diff": round(float(np.median(best_diffs)), 4),
                                           "cells": len(best_diffs)}
    return out


def main(names: List[str]) -> None:
    summaries = {}
    for ci, name in enumerate(CAPTURES):
        if name in names and (cuts_dir(name) / "design.json").exists():
            summaries[name] = capture_summary(ci, name)
    RESULTS.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS / "summary.json", {"methods": list(METHODS), "ks": KS, "margin": MARGIN,
                                          "bootstraps": BOOTSTRAPS, "seed": SEED,
                                          "tally": tally(summaries), "captures": summaries})
    for key, row in tally(summaries).items():
        print(key, row)
    for name, summary in summaries.items():
        print(name, "reproduces validation (largest difference):", summary["reproduces_validation"])


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAPTURES))
