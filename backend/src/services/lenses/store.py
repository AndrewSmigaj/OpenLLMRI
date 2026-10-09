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
import json
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


Metric = Literal["euclidean", "cosine", "correlation", "manhattan"]
METRICS: tuple[Metric, ...] = ("euclidean", "cosine", "correlation", "manhattan")


class UmapSettings(BaseModel):
    """UMAP's settings for one layer. Lenses built before the metric existed read as Euclidean."""
    n_neighbors: int = Field(default=15, ge=2, le=200)
    dimensions: int = Field(default=6, ge=2, le=50)
    min_dist: float = Field(default=0.1, ge=0.0, le=0.99)
    metric: Metric = "euclidean"

    @classmethod
    def of(cls, settings: Any) -> "UmapSettings":
        """The UMAP settings held in any settings object or dict, copied whole so that no field is
        dropped on the way (a lens's settings, a build's, a point of a search's grid)."""
        data = settings.model_dump() if isinstance(settings, BaseModel) else dict(settings)
        return cls.model_validate({key: value for key, value in data.items() if key in cls.model_fields})


# Where a layer's settings came from: the form's lens-wide values, the per-layer table, a preview
# (in-sample, or held out), or a search. Held-out previews and searches chose them on held-out
# scores, so the lens's own validation is selection-biased.
SettingsSource = Literal["form", "table", "preview", "preview held out", "tuned"]
CHOSEN_ON_HELDOUT = ("preview held out", "tuned")


class LensSettings(UmapSettings):
    """A lens's settings. A lens tuned or set by hand per layer keeps each layer's own in
    `per_layer` (aligned with the manifest's layers), and where each came from in `sources`; the
    lens-wide values record where it started. Lenses built before `sources` existed read as tuned
    when they have settings per layer (only a search made those), else as the form's."""
    seed: int = 42
    grouping: Literal["ward"] = "ward"
    per_layer: Optional[List[UmapSettings]] = None
    sources: Optional[List[SettingsSource]] = None

    def at(self, li: int) -> UmapSettings:
        """The settings of the li-th layer."""
        if self.per_layer is not None:
            return self.per_layer[li]
        return UmapSettings.of(self)

    def source_at(self, li: int) -> str:
        if self.sources is not None:
            return self.sources[li]
        return "tuned" if self.per_layer is not None else "form"

    def origin(self) -> str:
        """"tuned" when a search chose every layer's settings, "form" when they are the form's,
        else "by hand"."""
        n = len(self.per_layer) if self.per_layer is not None else 1
        found = {self.source_at(li) for li in range(n)}
        return "tuned" if found == {"tuned"} else "form" if found == {"form"} else "by hand"

    def chosen_on_heldout(self) -> bool:
        """Whether any layer's settings were chosen on held-out scores of these items."""
        n = len(self.per_layer) if self.per_layer is not None else 1
        return any(self.source_at(li) in CHOSEN_ON_HELDOUT for li in range(n))


class HoldoutDesign(BaseModel):
    """How a lens is held out, recorded so that later jobs on it use it (DESIGN.md C4).

    Whole families named by a categories field (none: stratified folds, marked weaker); the names
    whole or by their first two underscore parts; at most `max_folds` family folds, more merging
    round-robin (none: one fold per family index, as before); and the share of families a search's
    test portion takes, drawn by the lens's seed, which previews leave out too."""
    family_field: Optional[str] = "scene"
    whole_families: bool = False
    max_folds: Optional[int] = Field(default=12, ge=2, le=50)
    test_share: float = Field(default=0.2, ge=0.1, le=0.5)


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
    holdout: Optional[HoldoutDesign] = None  # lenses built before the record: see `holdout_of`


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


def declared_holdout(session_id: str, lake: Optional[Path] = None) -> Optional[HoldoutDesign]:
    """The hold-out design a capture's sentence set declared (its `metadata.holdout`, kept in the
    session file by the capture), or None."""
    folder = session_dir(session_id, lake)
    path = folder.parent / "_sessions" / f"{folder.name}.json"
    if not path.exists():
        return None
    declared = json.loads(path.read_text(encoding="utf-8")).get("holdout")
    return HoldoutDesign.model_validate(declared) if declared else None


def default_holdout(session_id: str, lake: Optional[Path] = None) -> HoldoutDesign:
    """A new lens's hold-out design: the one its capture's set declared, else the defaults (whole
    families by `scene`, which become stratified folds when the items name none)."""
    return declared_holdout(session_id, lake) or HoldoutDesign()


def holdout_of(folder: Path, manifest: LensManifest) -> HoldoutDesign:
    """A lens's hold-out design: its own record. A lens built before records existed takes the
    families field its validation used, else its capture's declaration, else the defaults, always
    without a fold cap, so its folds stay as they were."""
    if manifest.holdout is not None:
        return manifest.holdout
    path = folder / "validation.json"
    if path.exists():
        folds = json.loads(path.read_text(encoding="utf-8")).get("folds") or {}
        if folds.get("field"):
            return HoldoutDesign(family_field=folds["field"], whole_families=bool(folds.get("whole")), max_folds=None)
    declared = declared_holdout(manifest.session_id)
    return (declared or HoldoutDesign()).model_copy(update={"max_folds": None})


def resolve_holdout(folder: Path, manifest: LensManifest, family_field: Optional[str] = None,
                    whole_families: Optional[bool] = None) -> HoldoutDesign:
    """The design a job on a lens uses: what the request names, over the lens's own. An empty
    families field asks for no families (stratified folds)."""
    update: Dict[str, Any] = {}
    if family_field is not None:
        update["family_field"] = family_field or None
    if whole_families is not None:
        update["whole_families"] = whole_families
    return holdout_of(folder, manifest).model_copy(update=update)


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
        "settings_origin": manifest.settings.origin(),
        "selection_biased": manifest.settings.chosen_on_heldout(),
        "holdout": holdout_of(folder, manifest).model_dump(),
        "filters": manifest.filters.model_dump(),
        "versions": manifest.versions, "current": manifest.current,
        "state": current.state if current else None,
        "k_per_layer": current.k_per_layer if current else None,
        "created_at": manifest.provenance.created_at, "created_by": manifest.provenance.created_by,
        "self_check": manifest.self_check,
        "validation": validation_headline(folder, manifest, current),
        "tuning": _tuning(folder),
        "details": sorted(path.stem for path in (folder / "details").glob("*.json")),
        "readings": _readings(folder),
        "axes": (folder / "axes.json").exists(),
    }


def _readings(folder: Path) -> List[Dict[str, Any]]:
    from services.lenses.readout import list_readings

    return list_readings(folder)


def _tuning(folder: Path) -> Optional[Dict[str, Any]]:
    from services.lenses.search import tuning_headline

    return tuning_headline(folder)


def validation_headline(folder: Path, manifest: LensManifest, current: Optional[VersionRecord]) -> Optional[Dict[str, Any]]:
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
