"""Shared loading for the animal study's analyses (read-only).

- the set's entries by item text: group, way of life and taxonomy (the capture keeps only the
  categories, so the taxonomy is read from the set);
- a lens's items, in its order, and its embedding per layer (the space its nodes are cut in);
- the residual stream in the validation's raw recipe: standardized, then 50 principal components;
- nearest neighbours, and the null bands the analyses draw beside their lines.

Every analysis runs from the repo root with the project's Python, for example
  .venv/bin/python docs/studies/animals/analysis/taxonomic_neighbourhoods.py SESSION LENS
and writes its numbers to results/ and its charts to figures/ beside this file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backend/src"))

SET = ROOT / "data/sentence_sets/lexical/animals_kinship_v1.json"
HERE = Path(__file__).parent
FIGURES = HERE / "figures"
RESULTS = HERE / "results"
RANKS = ("phylum", "class", "order", "family", "genus")
NEIGHBOURS = 10
SEED = 1


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


def lens_embedding(session: str, lens: str) -> np.ndarray:
    """[layers, items, width]: each layer's embedding (zero columns pad layers of fewer dimensions,
    which changes no distance)."""
    return np.load(lens_folder(session, lens) / "fit" / "embed.npz")["embedding"]


def raw_layers(session: str, probe_ids: List[str], layers: List[int],
               centre_within: np.ndarray | None = None) -> Dict[int, np.ndarray]:
    """{layer: [items, 50]}: the residual stream at the target token, standardized, then its 50
    principal components (the validation's raw recipe, fitted on every item). With
    `centre_within` (a group per item), each group's mean is taken out first, which removes any
    offset between the groups."""
    from services.lenses.data import load_states
    from services.lenses.raw import pca_features

    states = load_states(session, probe_ids, layers=layers)
    out = {}
    for layer in layers:
        x = states[layer]
        if centre_within is not None:
            x = x.copy()
            for g in np.unique(centre_within):
                x[centre_within == g] -= x[centre_within == g].mean(axis=0)
        out[layer] = pca_features(x, x[:1], SEED)[0]
    return out


def neighbours(points: np.ndarray, k: int = NEIGHBOURS) -> np.ndarray:
    """[items, k]: each item's k nearest other items, nearest first (Euclidean)."""
    from sklearn.neighbors import NearestNeighbors

    index = NearestNeighbors(n_neighbors=k + 1).fit(points)
    found = index.kneighbors(points, return_distance=False)
    out = np.empty((len(points), k), dtype=np.int64)
    for i, row in enumerate(found):
        row = row[row != i][:k]
        out[i] = row
    return out


def band(values: np.ndarray) -> List[float]:
    """The middle 95% of a null's values."""
    return [float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))]


def write_results(name: str, payload: Dict[str, Any]) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return path


def figure_path(name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    return FIGURES / f"{name}.png"
