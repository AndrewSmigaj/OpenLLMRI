"""One shape for every lens the app opens: a new lens's version, or a legacy schema.

A view holds the items (in capture order), each item's node at every layer, and each item's top
four experts with the model's own weights. Flows, members and fingerprints are computed from it,
so legacy schemas open in the new Layers view without being rebuilt.
"""

from __future__ import annotations

import functools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

Array = np.ndarray[Any, Any]


@dataclass
class LensView:
    session_id: str
    name: str
    legacy: bool
    version: Optional[str]
    layers: List[int]
    items: List[Dict[str, Any]]  # probe_id, label, categories (dict), output_category, input_text, target_word
    nodes: Array  # [N, L] int16
    experts: Array  # [N, L, 4] int16, rank 1 first
    weights: Array  # [N, L, 4] float32, each row sums to 1
    settings: Dict[str, Any] = field(default_factory=dict)
    provenance: Dict[str, Any] = field(default_factory=dict)


def _item_dict(row: Dict[str, Any]) -> Dict[str, Any]:
    raw = row.get("categories_json")
    return {
        "probe_id": row["probe_id"], "label": row.get("label"),
        "categories": json.loads(raw) if raw else {},
        "output_category": row.get("output_category"),
        "input_text": row.get("input_text"), "target_word": row.get("target_word"),
    }


def open_lens(session_id: str, name: str, version: Optional[str] = None,
              lake: Optional[Path] = None) -> LensView:
    """A new lens at one of its versions (its current one by default)."""
    import pyarrow.parquet as pq

    from services.lenses.store import lens_dir, read_manifest

    folder = lens_dir(session_id, name, lake)
    if not (folder / "lens.json").exists():
        raise FileNotFoundError(f"Lens '{name}' not found in {session_id}")
    manifest = read_manifest(folder)
    chosen = version or manifest.current
    if chosen not in manifest.versions:
        raise FileNotFoundError(f"Lens '{name}' has no version {chosen!r}")
    top4 = np.load(folder / "fit" / "top4.npz")
    return LensView(
        session_id=manifest.session_id, name=name, legacy=False, version=chosen,
        layers=manifest.layers,
        items=[_item_dict(r) for r in pq.read_table(folder / "items.parquet").to_pylist()],
        nodes=np.load(folder / str(chosen) / "assign.npz")["nodes"],
        experts=top4["experts"], weights=top4["weights"].astype(np.float32),
        settings=manifest.settings.model_dump() | {"site": manifest.site.model_dump()},
        provenance=manifest.provenance.model_dump())


@functools.lru_cache(maxsize=8)
def open_legacy(session_id: str, schema: str, lake: Optional[Path] = None) -> LensView:
    """A clustering built the old way, read from its `probe_assignments.json` (which holds every
    layer and agrees with all its window files) and from the capture. Read only, and cached."""
    from core.parquet_reader import read_records
    from schemas.tokens import ProbeRecord
    from services.lenses.data import load_routing, own_top4, session_dir

    folder = session_dir(session_id, lake) / "clusterings" / schema
    if not (folder / "probe_assignments.json").exists():
        raise FileNotFoundError(f"Schema '{schema}' not found in {session_id}")
    assignments: Dict[str, Dict[str, int]] = json.loads((folder / "probe_assignments.json").read_text())
    meta = json.loads((folder / "meta.json").read_text()) if (folder / "meta.json").exists() else {}
    records = [r for r in read_records(str(session_dir(session_id, lake) / "tokens.parquet"), ProbeRecord)
               if r.probe_id in assignments]
    ids = [r.probe_id for r in records]
    layers = sorted(int(layer) for layer in assignments[ids[0]])
    nodes = np.array([[assignments[pid][str(layer)] for layer in layers] for pid in ids], dtype=np.int16)
    experts, weights = own_top4(load_routing(session_id, ids, lake=lake))
    return LensView(
        session_id=session_dir(session_id, lake).name, name=schema, legacy=True, version=None,
        layers=layers, items=[_item_dict(vars(r)) for r in records], nodes=nodes,
        experts=experts[:, layers], weights=weights[:, layers],
        settings={"legacy_params": meta.get("params", {}), "last_occurrence_only": meta.get("last_occurrence_only"),
                  "steps": meta.get("steps"), "max_probes": meta.get("max_probes")},
        provenance={"created_at": meta.get("created_at"), "created_by": meta.get("created_by")})
