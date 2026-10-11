"""Shared loading for the animal ontology study's analyses (read-only).

- the set's entries by item text, with the fourteen axes of the nine ways (the capture keeps the
  categories; the group is the entry's label);
- a lens's items, in its order, and its embedding per layer (the space its nodes are cut in);
- the residual stream in the validation's raw recipe: standardized, then 50 principal components;
- nearest neighbours, shuffles within each token count, and where results and figures go.

Every analysis runs from the repo root with the project's Python, for example
  .venv/bin/python docs/studies/animal_ontology/analysis/ways.py SESSION LENS
and writes its numbers to results/ and its charts to figures/ beside this file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend/src"))

SET = ROOT / "data/sentence_sets/lexical/animals_ontology_v1.json"
HERE = Path(__file__).parent
FIGURES = HERE / "figures"
RESULTS = HERE / "results"
NEIGHBOURS = 10
SHUFFLES = 1000
SEED = 1

# The fourteen axes, in the order of the nine ways (data/sentence_sets/lexical/animals_ontology_v1.md).
AXES = ("group", "order", "kind", "covering", "size", "legs", "where_met", "relation", "danger",
        "feeling", "habitat", "movement", "diet", "wild_or_domestic")
WAY_OF_AXIS = {"group": "descent", "order": "descent", "kind": "everyday kind",
               "covering": "body covering", "size": "size", "legs": "legs",
               "where_met": "where people meet it", "relation": "relation to people",
               "danger": "danger and feeling", "feeling": "danger and feeling",
               "habitat": "way of life", "movement": "way of life", "diet": "way of life",
               "wild_or_domestic": "way of life"}
AXIS_NAMES = {"group": "group (descent)", "order": "order (descent)", "kind": "everyday kind",
              "covering": "body covering", "size": "size", "legs": "legs",
              "where_met": "where met", "relation": "relation", "danger": "danger",
              "feeling": "feeling", "habitat": "habitat", "movement": "movement", "diet": "diet",
              "wild_or_domestic": "wild or domestic"}


def set_entries() -> Dict[str, Dict[str, Any]]:
    """Each entry of the set by its text, with its group."""
    data = json.loads(SET.read_text(encoding="utf-8"))
    return {e["text"]: {**e, "group": g["label"]} for g in data["groups"] for e in g["sentences"]}


def lens_folder(session: str, lens: str) -> Path:
    from services.lenses.store import lens_dir
    return lens_dir(session, lens)


def lens_items(session: str, lens: str) -> List[Dict[str, Any]]:
    """The lens's items in its order, each joined to its set entry by text."""
    import pyarrow.parquet as pq

    entries = set_entries()
    rows = pq.read_table(lens_folder(session, lens) / "items.parquet").to_pylist()
    missing = [r["input_text"] for r in rows if r["input_text"] not in entries]
    if missing:
        raise SystemExit(f"{len(missing)} lens items aren't in the set, e.g. {missing[:3]}")
    return [{**r, "entry": entries[r["input_text"]]} for r in rows]


def axis_values(items: List[Dict[str, Any]], axis: str) -> List[str]:
    if axis == "group":
        return [it["entry"]["group"] for it in items]
    return [it["entry"]["categories"][axis] for it in items]


def codes(values: List[str]) -> np.ndarray:
    """Each value as a small integer, in sorted order of the values."""
    order = {v: i for i, v in enumerate(sorted(set(values)))}
    return np.array([order[v] for v in values], dtype=np.int32)


def token_groups(items: List[Dict[str, Any]]) -> np.ndarray:
    """0 for a one-token name, 1 for a name that splits (the set's `tokens`, which the audit
    checked against the tokenizer)."""
    return np.array([0 if it["entry"]["categories"]["tokens"] == "one" else 1 for it in items])


def lens_embedding(session: str, lens: str) -> np.ndarray:
    """[layers, items, width]: each layer's embedding (zero columns pad layers of fewer dimensions,
    which changes no distance)."""
    return np.load(lens_folder(session, lens) / "fit" / "embed.npz")["embedding"]


def lens_site(session: str, lens: str) -> int:
    manifest = json.loads((lens_folder(session, lens) / "lens.json").read_text(encoding="utf-8"))
    return int(manifest["site"]["token_position"])


def raw_layers(session: str, lens: str, probe_ids: List[str], layers: List[int]) -> Dict[int, np.ndarray]:
    """{layer: [items, 50]}: the residual stream at the lens's site, standardized, then its 50
    principal components (the validation's raw recipe, fitted on every item)."""
    from services.lenses.data import load_states
    from services.lenses.raw import pca_features

    states = load_states(session, probe_ids, token_position=lens_site(session, lens), layers=layers)
    return {layer: pca_features(states[layer], states[layer][:1], SEED)[0] for layer in layers}


def neighbours(points: np.ndarray, k: int = NEIGHBOURS) -> np.ndarray:
    """[items, k]: each item's k nearest other items, nearest first (Euclidean)."""
    from sklearn.neighbors import NearestNeighbors

    found = NearestNeighbors(n_neighbors=k + 1).fit(points).kneighbors(points, return_distance=False)
    out = np.empty((len(points), k), dtype=np.int64)
    for i, row in enumerate(found):
        out[i] = row[row != i][:k]
    return out


def shuffles(groups: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """[n, items]: n permutations of the items that keep every item within its group (the token
    count), as index arrays: values[perm] shuffles the values within each group."""
    out = np.tile(np.arange(len(groups)), (n, 1))
    for g in np.unique(groups):
        members = np.flatnonzero(groups == g)
        for row in out:
            row[members] = rng.permutation(members)
    return out


def layer_stream(layer: int, space: str, axis: Optional[str] = None) -> np.random.Generator:
    """A seeded random stream of its own for every layer, space and axis."""
    parts = [SEED, layer, 0 if space == "raw" else 1]
    if axis is not None:
        parts.append(AXES.index(axis) + 1)
    return np.random.default_rng(parts)


def write_results(name: str, payload: Dict[str, Any]) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return path


def figure_path(name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    return FIGURES / f"{name}.png"
