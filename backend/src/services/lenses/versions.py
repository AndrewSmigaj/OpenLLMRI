"""Versions of a lens: one choice of k per layer, cut from the saved Ward trees.

Choosing k needs no refit. The build makes `v1`; each new choice of k makes the next version, a
draft until it is saved.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from services.lenses.fit import cut
from services.lenses.store import (
    LensManifest,
    VersionRecord,
    read_manifest,
    write_manifest,
    write_version,
)

AUTO_METHODS = ("elbow", "silhouette", "levels", "heldout")


def heldout_best(validation: Dict[str, Any], axis: str = "label") -> Dict[str, int]:
    """Each layer's k with the best held-out kappa on an axis (from a lens's validation.json).
    Choosing k by its held-out score is selection-biased, and the k's source says so."""
    best: Dict[str, int] = {}
    for layer, profile in validation["layers"].items():
        scored = [(entry["heldout"][axis]["kappa"], int(k)) for k, entry in profile.items() if axis in entry["heldout"]]
        if scored:
            best[layer] = max(scored, key=lambda pair: (pair[0], -pair[1]))[1]  # ties go to the smaller k
    return best


def resolve_k(layers: List[int], suggestions: Dict[str, Dict[str, object]], k: Optional[int] = None,
              k_per_layer: Optional[List[int]] = None,
              k_auto: Optional[str] = None) -> Tuple[List[int], List[str]]:
    """k for each layer, and where each came from: chosen by hand, or a named method's suggestion.

    `levels` takes the finest clear level of the tree; a layer without one falls back to the
    silhouette's choice, and says so. `heldout` needs the lens validated (its best held-out k is
    merged into the suggestions as "heldout").
    """
    if k_per_layer is not None:
        if len(k_per_layer) != len(layers):
            raise ValueError(f"k_per_layer has {len(k_per_layer)} values for {len(layers)} layers")
        return [int(v) for v in k_per_layer], ["manual"] * len(layers)
    if k_auto is None:
        return [int(k or 6)] * len(layers), ["manual"] * len(layers)
    if k_auto not in AUTO_METHODS:
        raise ValueError(f"unknown k method {k_auto!r}; one of {AUTO_METHODS}")
    ks: List[int] = []
    sources: List[str] = []
    for layer in layers:
        found = suggestions[str(layer)]
        if k_auto == "heldout":
            if "heldout" not in found:
                raise ValueError("the held-out best needs a validated lens; validate it first")
            ks.append(int(str(found["heldout"])))
            sources.append("auto:heldout (selection-biased)")
            continue
        if k_auto == "levels":
            levels = found.get("levels") or []
            if isinstance(levels, list) and levels:
                ks.append(int(max(levels)))
                sources.append("auto:levels")
                continue
            ks.append(int(str(found["silhouette"])))
            sources.append("auto:silhouette (no clear level)")
            continue
        ks.append(int(str(found[k_auto])))
        sources.append(f"auto:{k_auto}")
    return ks, sources


def new_version(folder: Path, k_per_layer: List[int], k_source: List[str]) -> VersionRecord:
    """Cut every layer's tree at its k and record the result as the lens's next (draft) version."""
    manifest: LensManifest = read_manifest(folder)
    trees = np.load(folder / "fit" / "ward.npz")["trees"]
    if len(k_per_layer) != trees.shape[0]:
        raise ValueError(f"{len(k_per_layer)} values of k for {trees.shape[0]} layers")
    largest = trees.shape[1] + 1  # items
    for k in k_per_layer:
        if not 1 <= k <= largest:
            raise ValueError(f"k must be between 1 and {largest}, got {k}")
    nodes = np.stack([cut(trees[i], k) for i, k in enumerate(k_per_layer)], axis=1)
    record = VersionRecord(version=f"v{len(manifest.versions) + 1}", k_per_layer=k_per_layer,
                           k_source=k_source)
    write_version(folder, record)
    np.savez_compressed(folder / record.version / "assign.npz", nodes=nodes)
    write_manifest(folder, manifest.model_copy(
        update={"versions": manifest.versions + [record.version], "current": record.version}))
    return record
