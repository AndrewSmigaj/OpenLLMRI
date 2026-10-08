"""Where a lens lives and what its records hold.

A lens is a folder in its capture's session: `<session>/lenses/<name>/`.
- `lens.json`: the manifest (capture, site, filters, settings, k suggestions, versions,
  provenance). The only file that changes after the build, and only by atomic replacement.
- `items.parquet`: the calibration items, in capture order.
- `fit/`: what does not depend on k, written once by the build: each layer's reducer without
  its training rows (`umap_LXX.joblib`), the embeddings (`embed.npz`), the Ward trees
  (`ward.npz`) and the model's own top-4 routing (`top4.npz`).
- `v1/`, `v2/`, ...: one folder per choice of k, each with `version.json` and `assign.npz`.
  A saved version never changes, and is also copied into the repo under `data/lenses/`.
"""

from __future__ import annotations

import functools
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from api import config
from api.config import PROJECT_ROOT
from services.jobs.store import now_iso
from services.lenses.data import LensFilters, session_dir

FORMAT_VERSION = 1
_NAME = re.compile(r"^[a-z0-9][a-z0-9_\-]{0,63}$")


def valid_name(name: str) -> bool:
    return bool(_NAME.match(name))


class LensSite(BaseModel):
    source: str = "residual_stream"
    token_position: int = 1


class LensSettings(BaseModel):
    n_neighbors: int = 15
    dimensions: int = 6
    min_dist: float = 0.1
    seed: int = 42
    grouping: Literal["ward"] = "ward"


class Provenance(BaseModel):
    commit: Optional[str] = None
    dirty: bool = False
    job_id: Optional[str] = None
    created_by: str = "unknown"
    created_at: str = Field(default_factory=now_iso)
    seconds: Optional[float] = None
    libraries: Dict[str, str] = Field(default_factory=dict)


class LensManifest(BaseModel):
    format_version: int = FORMAT_VERSION
    name: str
    kind: Literal["umap", "mass_mean"] = "umap"
    contrast: Optional[Dict[str, str]] = None  # mass-mean lenses: {"label_a": ..., "label_b": ...}
    session_id: str
    capture: Dict[str, Any] = Field(default_factory=dict)
    site: LensSite = Field(default_factory=LensSite)
    filters: LensFilters = Field(default_factory=LensFilters)
    settings: LensSettings = Field(default_factory=LensSettings)
    n_items: int = 0
    layers: List[int] = Field(default_factory=list)
    suggestions: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    versions: List[str] = Field(default_factory=list)
    current: Optional[str] = None
    provenance: Provenance = Field(default_factory=Provenance)
    self_check: Optional[Dict[str, Any]] = None  # planted and null layers, with the build's settings


class VersionRecord(BaseModel):
    version: str
    k_per_layer: List[int]
    k_source: List[str]
    state: Literal["draft", "saved"] = "draft"
    keywords: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=now_iso)
    saved_at: Optional[str] = None


def lenses_root(session_id: str, lake: Optional[Path] = None) -> Path:
    return session_dir(session_id, lake) / "lenses"


def lens_dir(session_id: str, name: str, lake: Optional[Path] = None) -> Path:
    if not valid_name(name):
        raise ValueError(f"not a lens name: {name!r} (lowercase letters, digits, '_' and '-')")
    return lenses_root(session_id, lake) / name


def _write_text_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def read_manifest(folder: Path) -> LensManifest:
    return LensManifest.model_validate_json((folder / "lens.json").read_text(encoding="utf-8"))


def write_manifest(folder: Path, manifest: LensManifest) -> None:
    _write_text_atomic(folder / "lens.json", manifest.model_dump_json(indent=2))


def read_version(folder: Path, version: str) -> VersionRecord:
    path = folder / version / "version.json"
    return VersionRecord.model_validate_json(path.read_text(encoding="utf-8"))


def write_version(folder: Path, record: VersionRecord) -> None:
    (folder / record.version).mkdir(parents=True, exist_ok=True)
    _write_text_atomic(folder / record.version / "version.json", record.model_dump_json(indent=2))


def list_lenses(session_id: str, lake: Optional[Path] = None) -> List[LensManifest]:
    root = lenses_root(session_id, lake)
    if not root.exists():
        return []
    return [read_manifest(p) for p in sorted(root.iterdir())
            if p.is_dir() and valid_name(p.name) and (p / "lens.json").exists()]


@functools.lru_cache(maxsize=1)
def git_state() -> tuple[Optional[str], bool]:
    """The repo's commit, and whether the working tree has uncommitted changes."""
    try:
        commit = subprocess.run(["git", "-C", str(PROJECT_ROOT), "rev-parse", "HEAD"],
                                capture_output=True, text=True, check=True, timeout=10).stdout.strip()
        status = subprocess.run(["git", "-C", str(PROJECT_ROOT), "status", "--porcelain"],
                                capture_output=True, text=True, check=True, timeout=10).stdout
        return commit, bool(status.strip())
    except (OSError, subprocess.SubprocessError):
        return None, False


def save_version(session_id: str, name: str, version: str, keywords: List[str],
                 lake: Optional[Path] = None, records_root: Optional[Path] = None) -> VersionRecord:
    """Freeze a version and copy its records into the repo (`data/lenses/<session>/<name>/`).

    A saved version never changes; a different k makes a new version.
    """
    import shutil

    folder = lens_dir(session_id, name, lake)
    record = read_version(folder, version)
    if record.state == "saved":
        raise ValueError(f"{name} {version} is already saved")
    record = record.model_copy(update={"state": "saved", "keywords": keywords, "saved_at": now_iso()})
    write_version(folder, record)
    manifest = read_manifest(folder)
    write_manifest(folder, manifest.model_copy(update={"current": version}))
    target = (records_root or config.LENS_RECORDS_PATH) / session_id / name
    (target / version).mkdir(parents=True, exist_ok=True)
    shutil.copy2(folder / "lens.json", target / "lens.json")
    shutil.copy2(folder / version / "version.json", target / version / "version.json")
    return record


def summary(manifest: LensManifest, folder: Path) -> Dict[str, Any]:
    """What a lens list shows: name, kind, settings, items, versions and the current k, and what has
    been worked out for it (its validation headline; the versions with node details)."""
    current = read_version(folder, manifest.current) if manifest.current else None
    return {
        "name": manifest.name, "kind": manifest.kind, "legacy": False, "contrast": manifest.contrast,
        "session_id": manifest.session_id, "n_items": manifest.n_items,
        "settings": manifest.settings.model_dump(), "site": manifest.site.model_dump(),
        "filters": manifest.filters.model_dump(),
        "versions": manifest.versions, "current": manifest.current,
        "state": current.state if current else None,
        "k_per_layer": current.k_per_layer if current else None,
        "created_at": manifest.provenance.created_at, "created_by": manifest.provenance.created_by,
        "self_check": manifest.self_check,
        "validation": _validation_headline(folder, manifest, current),
        "details": sorted(path.stem for path in (folder / "details").glob("*.json")),
    }


def _validation_headline(folder: Path, manifest: LensManifest, current: Optional[VersionRecord]) -> Optional[Dict[str, Any]]:
    """Whether the lens is validated, and its best held-out layer on the label at its own k."""
    import json

    path = folder / "validation.json"
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    best: Optional[Dict[str, Any]] = None
    if manifest.kind == "mass_mean":  # one axis per layer: its best held-out layer
        for layer, scores in record["layers"].items():
            if best is None or scores["accuracy"] > best["accuracy"]:
                best = {"layer": int(layer), **{key: scores[key] for key in ("accuracy", "kappa", "worst_fold")}}
        return {"folds": record["folds"], "best": best, "created_at": record["provenance"]["created_at"]}
    for li, layer in enumerate(manifest.layers):
        k = current.k_per_layer[li] if current else None
        scores = record["layers"].get(str(layer), {}).get(str(k), {}).get("heldout", {}).get("label")
        if scores and (best is None or scores["kappa"] > best["kappa"]):
            best = {"layer": layer, "k": k, **scores}
    return {"folds": record["folds"], "best": best, "created_at": record["provenance"]["created_at"]}
