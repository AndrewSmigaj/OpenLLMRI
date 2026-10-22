"""Shared loading for the UMAP-against-raw-space study (read-only; DESIGN.md C4, LENS-6;
docs/research/umap_vs_raw.md).

The question is the one Andrew set for preferring UMAP: does a UMAP lens's grouping recover the
designed structure on held-out items better than plain raw-space groupings at the same number of
groups? Validation already answers it on the label alone (`comparison` in validation.json); this
study asks it of every designed attribute and every pair of attributes, the combinations UMAP's
local neighbourhoods are expected to keep.

Each capture is read through its default-settings UMAP lens (15 neighbours, 6-D, min_dist 0.1,
Euclidean, seed 42): no tuned lens, since a search chose its settings on held-out scores of the
same items. The folds are the lens's validation folds, remade with the same design and seed.

Every analysis runs from the repo root with the project's Python, for example
  .venv/bin/python docs/studies/umap_vs_raw/analysis/heldout.py framing
and writes its numbers to results/ and its charts to figures/ beside this file.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend/src"))

HERE = Path(__file__).parent
FIGURES = HERE / "figures"
RESULTS = HERE / "results"

METHODS = ("umap", "raw_ward", "raw_spectral")
KS = list(range(2, 11))  # validation's k range
CROSSED_BELOW = 0.5  # a pair counts as crossed when its two attributes' Cramér's V is below this

# The captures, each read through one default-settings UMAP lens, with the fold design its
# validation used: the families field (None: stratified folds, identical texts kept together),
# whether family names are kept whole, the fold cap and the number of folds asked for
CAPTURES: Dict[str, Dict[str, Any]] = {
    "tank": {"session": "session_1434a9be", "lens": "tank-k5-n15", "family": None, "whole": False,
             "max_folds": None, "n_folds": 5},
    "calibration": {"session": "session_29a80932", "lens": "calibration-q1-k2-n15", "family": "scene",
                    "whole": False, "max_folds": None, "n_folds": 5},
    "framing": {"session": "session_673360a5", "lens": "framing-k4-auto-levels", "family": None,
                "whole": False, "max_folds": None, "n_folds": 5},
    "words": {"session": "session_8f536bea", "lens": "words-k8-n15", "family": "family", "whole": False,
              "max_folds": None, "n_folds": 5},
    "ontology": {"session": "session_5cd7091d", "lens": "onto-k8-n15", "family": "order", "whole": True,
                 "max_folds": 12, "n_folds": 5},
    "objects": {"session": "session_2be574c4", "lens": "objects-k3-n15", "family": "domain", "whole": True,
                "max_folds": 12, "n_folds": 5},
}


def open_capture(name: str) -> Tuple[Any, Any, Dict[str, Any]]:
    """The capture's lens view and manifest, and its entry in CAPTURES."""
    from services.lenses.store import lens_dir, read_manifest
    from services.lenses.view import open_lens

    spec = CAPTURES[name]
    view = open_lens(spec["session"], spec["lens"])
    manifest = read_manifest(lens_dir(spec["session"], spec["lens"]))
    return view, manifest, spec


def single_codes(view: Any, family: Optional[str]) -> Tuple[Dict[str, np.ndarray], Dict[str, List[str]]]:
    """Every designed attribute with two values or more, as integer codes (-1: no value). The
    families field is left out: held out whole, it can't be read on held-out items."""
    from services.lenses.flows import axes_of
    from services.lenses.validate import axis_codes

    axes = {axis: values for axis, values in axes_of(view).items() if axis != family and len(values) >= 2}
    return axis_codes(view.items, axes), axes


def function_of(a: np.ndarray, b: np.ndarray) -> bool:
    """Whether a is a function of b wherever both are known."""
    known = (a >= 0) & (b >= 0)
    pairs = set(zip(b[known].tolist(), a[known].tolist()))
    return len(pairs) == len({x for x, _ in pairs})


def cramers_v(a: np.ndarray, b: np.ndarray) -> float:
    known = (a >= 0) & (b >= 0)
    x, y = a[known], b[known]
    xs, ys = np.unique(x), np.unique(y)
    table = np.array([[np.sum((x == i) & (y == j)) for j in ys] for i in xs], dtype=float)
    expected = table.sum(1, keepdims=True) @ table.sum(0, keepdims=True) / table.sum()
    chi2 = float(((table - expected) ** 2 / np.where(expected > 0, expected, 1)).sum())
    r = min(len(xs), len(ys)) - 1
    return float(np.sqrt(chi2 / (table.sum() * r))) if r > 0 else 0.0


def pair_codes(codes: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], Dict[str, Dict[str, Any]]]:
    """Every pair of attributes neither of which is a function of the other, as one joint code
    (-1 where either is unknown), and per pair its number of joint values and Cramér's V."""
    joint: Dict[str, np.ndarray] = {}
    about: Dict[str, Dict[str, Any]] = {}
    for a, b in itertools.combinations(codes, 2):
        ca, cb = codes[a], codes[b]
        if function_of(ca, cb) or function_of(cb, ca):
            continue
        known = (ca >= 0) & (cb >= 0)
        raw = np.where(known, ca * 1000 + cb, -1)
        values = np.unique(raw[known])
        code = np.full(len(raw), -1)
        code[known] = np.searchsorted(values, raw[known])
        name = f"{a}×{b}"
        joint[name] = code
        v = cramers_v(ca, cb)
        about[name] = {"a": a, "b": b, "values": int(len(values)), "cramers_v": round(v, 4),
                       "crossed": v < CROSSED_BELOW}
    return joint, about


def units_of(view: Any, spec: Dict[str, Any]) -> List[str]:
    """Each item's resampling unit for the bootstrap: its family where the folds hold out families,
    otherwise its text."""
    from services.lenses.validate import family_key

    if spec["family"]:
        return [family_key(str(item["categories"].get(spec["family"])), spec["whole"]) for item in view.items]
    return [item.get("input_text") or item["probe_id"] for item in view.items]


def folds_of(view: Any, manifest: Any, spec: Dict[str, Any]) -> Tuple[List[np.ndarray], Dict[str, Any]]:
    from services.lenses.validate import make_folds

    return make_folds(view.items, spec["family"], spec["n_folds"], manifest.settings.seed, spec["whole"],
                      spec["max_folds"])


def predictions(cuts: np.ndarray, folds: List[np.ndarray], code: np.ndarray) -> np.ndarray:
    """[method, k, item]: each held-out item's predicted value of `code`, its assigned cluster's
    majority value among that fold's training items (validation's rule; -1 where the cluster's
    training items have no value)."""
    from services.lenses.validate import _majority

    n_methods, n_ks = cuts.shape[1], cuts.shape[2]
    out = np.full((n_methods, n_ks, len(code)), -1, dtype=np.int32)
    for f, test in enumerate(folds):
        train = np.setdiff1d(np.arange(len(code)), test)
        for m in range(n_methods):
            for j, k in enumerate(KS):
                out[m, j, test] = _majority(cuts[f, m, j, train].astype(np.int64), code[train], k)[cuts[f, m, j, test]]
    return out


def scores(cuts: np.ndarray, folds: List[np.ndarray], code: np.ndarray) -> Dict[str, np.ndarray]:
    """Held-out kappa, accuracy and AMI per [method, k], as validation's `_scores` computes them:
    kappa and accuracy over every held-out item with a value, AMI between the assigned clusters and
    the values per fold, averaged by fold size."""
    from sklearn.metrics import adjusted_mutual_info_score as ami
    from sklearn.metrics import cohen_kappa_score

    pred = predictions(cuts, folds, code)
    keep = code >= 0
    n_methods, n_ks = cuts.shape[1], cuts.shape[2]
    out = {measure: np.zeros((n_methods, n_ks)) for measure in ("kappa", "accuracy", "ami")}
    for m in range(n_methods):
        for j in range(n_ks):
            truth, guess = code[keep], pred[m, j, keep]
            out["kappa"][m, j] = cohen_kappa_score(truth, guess) if len(set(truth.tolist())) > 1 else 0.0
            out["accuracy"][m, j] = float((truth == guess).mean())
            total, weighted = 0, 0.0
            for f, test in enumerate(folds):
                held = test[code[test] >= 0]
                if held.size:
                    weighted += float(ami(code[held], cuts[f, m, j, held])) * held.size
                    total += held.size
            out["ami"][m, j] = weighted / total if total else 0.0
    out["predictions"] = pred
    return out


def cuts_dir(name: str) -> Path:
    """Where a capture's groupings and design go: derived data, in the lake (git-ignored), not in
    the repo; the scores `summary.py` writes go to results/."""
    path = ROOT / "data/lake/_studies/umap_vs_raw" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=1), encoding="utf-8")
