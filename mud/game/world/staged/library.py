"""world.staged.library — the scenario library on disk. PURE (stdlib + PyYAML).

The library is data/scenarios/ in the repo (mounted read-only into the MUD's container; the folder is
SCENARIO_LIBRARY there). Each set has its own folder: set.yaml (its manifest) and scenarios/*.yaml.
A scenario's key is "<set_id>/<file stem>", never its room name: in the friend/foe set, 13 room names
are each shared by two scenarios.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from world.staged.scenario import Scenario, ScenarioError, parse

KINDS = {"staged", "world", "mini-world"}


def library_root() -> Path:
    """SCENARIO_LIBRARY if set (the MUD's container), else the repo's data/scenarios."""
    env = os.environ.get("SCENARIO_LIBRARY")
    return Path(env) if env else Path(__file__).resolve().parents[4] / "data" / "scenarios"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class ScenarioSet:
    id: str
    version: int | str
    kind: str
    folder: Path
    manifest: dict[str, Any] = field(default_factory=dict)

    @property
    def ref(self) -> str:
        """How a study cites the set: set_id@version."""
        return f"{self.id}@{self.version}"

    def keys(self, subset: str | None = None) -> list[str]:
        """Every scenario key of the set, or of one named subset (set.yaml `subsets`)."""
        stems = sorted(p.stem for p in (self.folder / "scenarios").glob("*.yaml"))
        if subset is not None:
            subsets = self.manifest.get("subsets") or {}
            if subset not in subsets:
                raise ScenarioError(f"{self.id}: no subset {subset!r} (has: {', '.join(subsets) or 'none'})")
            wanted = set(subsets[subset])
            unknown = wanted - set(stems)
            if unknown:
                raise ScenarioError(f"{self.id}: subset {subset!r} names missing files: {sorted(unknown)}")
            stems = [s for s in stems if s in wanted]
        return [f"{self.id}/{s}" for s in stems]


def load_set(set_id: str, root: Path | None = None) -> ScenarioSet:
    root = root or library_root()
    folder = root / set_id
    manifest_path = folder / "set.yaml"
    if not manifest_path.is_file():
        raise ScenarioError(f"no scenario set {set_id!r} (looked for {manifest_path})")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if manifest.get("id") != set_id:
        raise ScenarioError(f"{manifest_path}: id {manifest.get('id')!r} does not match its folder")
    kind = manifest.get("kind")
    if kind not in KINDS:
        raise ScenarioError(f"{manifest_path}: kind must be one of {sorted(KINDS)}, not {kind!r}")
    if manifest.get("version") in (None, ""):
        raise ScenarioError(f"{manifest_path}: needs a version")
    return ScenarioSet(id=set_id, version=manifest["version"], kind=kind, folder=folder,
                       manifest=manifest)


def list_sets(root: Path | None = None) -> list[ScenarioSet]:
    """Every set in the library (folders with a set.yaml; `_parked` and other `_` folders skipped)."""
    root = root or library_root()
    return [load_set(p.name, root) for p in sorted(root.iterdir())
            if p.is_dir() and not p.name.startswith("_") and (p / "set.yaml").is_file()]


@dataclass(frozen=True)
class Loaded:
    """A scenario with what a run records about it."""
    scenario: Scenario
    set: ScenarioSet
    file_hash: str


def load(key: str, root: Path | None = None) -> Loaded:
    """Load and validate one scenario by its key, "<set_id>/<file stem>"."""
    set_id, _, stem = key.partition("/")
    if not set_id or not stem:
        raise ScenarioError(f"a scenario key is <set_id>/<file>, not {key!r}")
    sset = load_set(set_id, root)
    path = sset.folder / "scenarios" / f"{stem}.yaml"
    if not path.is_file():
        raise ScenarioError(f"{sset.id}: no scenario {stem!r}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Loaded(scenario=parse(data, key), set=sset, file_hash=file_hash(path))
