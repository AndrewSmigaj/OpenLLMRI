"""What the build form offers: a capture's labels, steps and sites, and the methods a lens can use.

The form reads these instead of hard-coding them, so a capture shows only what it holds (its
token positions, the sources it captured) and the methods named here are the ones the build runs.
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import pyarrow.compute as pc
import pyarrow.parquet as pq

from core.parquet_reader import read_records
from schemas.tokens import ProbeRecord
from services.lenses.build import MAX_ITEMS
from services.lenses.data import SOURCES, LensFilters, load_items, session_dir
from services.lenses.versions import AUTO_METHODS

AUTO_METHOD_NOTES = {
    "elbow": "the k after which the clusters' spread stops falling steeply",
    "silhouette": "the k whose clusters are best separated (in-sample)",
    "levels": "the finest clear level of the merge tree; a layer without one takes the silhouette's k",
    "heldout": "the k whose nodes best match the classes on held-out data, by AMI (selection-biased; needs a validated lens)",
}
BUILD_METHODS = ("elbow", "silhouette", "levels")  # the held-out best needs a validation first


def _positions(path: Path) -> List[int]:
    if "token_position" not in pq.ParquetFile(path).schema_arrow.names:
        return [1]
    column = pq.read_table(path, columns=["token_position"]).column(0)
    return sorted(int(v) for v in pc.unique(column).to_pylist())


def capture_options(session_id: str, lake: Optional[Path] = None) -> Dict[str, Any]:
    """A capture's labels and steps (with counts), its sources and token positions, and how many
    items the default filters keep."""
    folder = session_dir(session_id, lake)
    records = read_records(str(folder / "tokens.parquet"), ProbeRecord)
    steps = Counter(s for r in records if (s := r.turn_id if r.turn_id is not None else r.sentence_index) is not None)
    sources = {name: _positions(folder / file) for name, (file, _) in SOURCES.items() if (folder / file).exists()}
    return {
        "session_id": folder.name,
        "n_records": len(records),
        "target_words": dict(Counter(r.target_word for r in records).most_common(5)),
        "labels": dict(sorted(Counter(r.label for r in records if r.label).items())),
        "steps": {str(k): v for k, v in sorted(steps.items())},
        "sources": sources,
        "default_items": len(load_items(session_id, LensFilters(), lake)),
        "max_items": MAX_ITEMS,
    }


def lens_methods() -> Dict[str, Any]:
    """The reductions, groupings and automatic k methods a lens build can use, with their defaults."""
    return {
        "reductions": [{"id": "umap", "label": "UMAP", "defaults": {"n_neighbors": 15, "dimensions": 6}}],
        "groupings": [{"id": "ward", "label": "Ward (hierarchical); any k is a cut of its tree"}],
        "k_auto": [{"id": m, "note": AUTO_METHOD_NOTES.get(m, "")} for m in BUILD_METHODS],
        "k_auto_validated": [{"id": m, "note": AUTO_METHOD_NOTES.get(m, "")} for m in AUTO_METHODS
                             if m not in BUILD_METHODS],
        "defaults": {"k": 6, "seed": 42, "source": "residual_stream", "token_position": 1,
                     "last_occurrence_only": True},
        "tuning": _tuning_defaults(),
    }


def _tuning_defaults() -> Dict[str, Any]:
    """What a lens search starts from (DESIGN.md C4), and the numbers its time estimate uses."""
    from services.lenses.search import MAX_SETTINGS, SECONDS_PER_FIT, LensSearchParams

    defaults = LensSearchParams(session_id="", source_lens="")
    return {"grid": defaults.grid.model_dump(), "k_min": defaults.k_min, "k_max": defaults.k_max,
            "test_share": defaults.test_share, "n_folds": defaults.n_folds, "family_field": defaults.family_field,
            "max_settings": MAX_SETTINGS, "seconds_per_fit": list(SECONDS_PER_FIT),
            "workers": max(1, min(6, (os.cpu_count() or 2) - 2))}
