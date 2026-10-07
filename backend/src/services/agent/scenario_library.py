"""The scenario library (data/scenarios/) as the agent runner reads it.

A scenario is named by its key, "<set_id>/<file stem>". The runner reads the file for the labels it
records and the action table its results use; the MUD reads the same file when the runner loads it
through the control channel, validates it and plays it (mud/game/world/staged/). Every run records
the set as "<set_id>@<version>" and the file's sha256, so a result names exactly what was played.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import yaml  # type: ignore[import-untyped]  # no PyYAML stubs (types-PyYAML) in the venv

from api import config


class ScenarioNotFoundError(ValueError):
    """No such set or scenario file in the library."""


@dataclass(frozen=True)
class LibraryScenario:
    key: str                    # "<set_id>/<file stem>"
    set_ref: str                # "<set_id>@<version>"
    file_hash: str              # sha256 of the scenario file
    config: Dict[str, Any]      # the file's contents

    @property
    def target_words(self) -> List[str]:
        return list(self.config.get("target_words") or [])

    @property
    def condition(self) -> Optional[str]:
        return cast(Optional[str], self.config.get("condition"))


def _manifest(set_id: str, root: Path) -> Dict[str, Any]:
    path = root / set_id / "set.yaml"
    if not path.is_file():
        raise ScenarioNotFoundError(f"no scenario set {set_id!r} (looked for {path})")
    return cast(Dict[str, Any], yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def load_scenario(key: str, root: Optional[Path] = None) -> LibraryScenario:
    """A scenario by its key. Raises ScenarioNotFoundError."""
    root = root or config.SCENARIO_LIBRARY
    set_id, _, stem = key.partition("/")
    if not set_id or not stem:
        raise ScenarioNotFoundError(f"a scenario key is <set_id>/<file>, not {key!r}")
    manifest = _manifest(set_id, root)
    path = root / set_id / "scenarios" / f"{stem}.yaml"
    if not path.is_file():
        raise ScenarioNotFoundError(f"{set_id}: no scenario {stem!r}")
    data = path.read_bytes()
    return LibraryScenario(
        key=key,
        set_ref=f"{set_id}@{manifest.get('version')}",
        file_hash=hashlib.sha256(data).hexdigest(),
        config=cast(Dict[str, Any], yaml.safe_load(data.decode("utf-8")) or {}),
    )


def scenario_keys(set_id: str, subset: Optional[str] = None,
                  root: Optional[Path] = None) -> List[str]:
    """Every scenario key of a set, or of one of its named subsets, in file order."""
    root = root or config.SCENARIO_LIBRARY
    manifest = _manifest(set_id, root)
    stems = sorted(p.stem for p in (root / set_id / "scenarios").glob("*.yaml"))
    if subset is not None:
        subsets = manifest.get("subsets") or {}
        if subset not in subsets:
            raise ScenarioNotFoundError(f"{set_id}: no subset {subset!r}")
        wanted = set(subsets[subset])
        stems = [s for s in stems if s in wanted]
    return [f"{set_id}/{s}" for s in stems]
