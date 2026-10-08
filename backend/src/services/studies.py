"""Studies (DESIGN.md G): a research question with its sets, captures, lenses, findings and a
ledger, kept as files in the repo, one folder each: `docs/studies/<id>/study.yaml`. The Study
workspace's view settings (runs, references, the event to align on, grouping; E6) join the file
when that workspace is built.

    id: lens_core                  # the folder's name
    title: The lens core
    question: ...
    status: active                 # proposed, active or finished
    started: 2026-10-08
    sets: [tank_polysemy_v3]       # sentence sets (data/sentence_sets) or scenario sets (data/scenarios)
    captures: [session_1434a9be]   # sessions in the lake
    lenses: [session_1434a9be/tank-k5-n15@v1]   # <session>/<lens>, with @<version> for a saved one
    findings: [docs/research/lens_core_validation.md]   # notes, from the repo root
    ledger:                        # one line per idea, experiment and finding
      - idea: ...
        experiment: ...
        finding: ...
        status: proposed           # proposed, reviewed or retracted; Andrew reviews (DESIGN.md H)
        evidence: [docs/research/lens_core_validation.md]
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import yaml  # type: ignore[import-untyped]  # no PyYAML stubs (types-PyYAML) in the venv
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from api.config import PROJECT_ROOT


class LedgerLine(BaseModel):
    model_config = ConfigDict(extra="forbid")
    idea: str
    experiment: str
    finding: str
    status: Literal["proposed", "reviewed", "retracted"] = "proposed"
    evidence: List[str] = Field(default_factory=list)


class Study(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    question: str
    status: Literal["proposed", "active", "finished"] = "active"
    started: Optional[datetime.date] = None
    sets: List[str] = Field(default_factory=list)
    captures: List[str] = Field(default_factory=list)
    lenses: List[str] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)
    ledger: List[LedgerLine] = Field(default_factory=list)


def studies_root() -> Path:
    return PROJECT_ROOT / "docs" / "studies"


def load_study(folder: Path) -> Study:
    study = Study(**(yaml.safe_load((folder / "study.yaml").read_text(encoding="utf-8")) or {}))
    if study.id != folder.name:
        raise ValueError(f"the study's id {study.id!r} isn't its folder's name {folder.name!r}")
    return study


def _has_set(name: str) -> bool:
    root = PROJECT_ROOT / "data"
    return any((root / "sentence_sets").rglob(f"{name}.json")) or (root / "scenarios" / name / "set.yaml").exists()


def _has_lens(ref: str) -> bool:
    from services.lenses.store import lens_dir, read_manifest

    where, _, version = ref.partition("@")
    session, _, name = where.partition("/")
    folder = lens_dir(session, name)
    return (folder / "lens.json").exists() and (not version or version in read_manifest(folder).versions)


def problems(study: Study) -> List[str]:
    """The study's references that don't resolve: sets, captures, lenses, notes."""
    from services.lenses.data import session_dir

    found = [f"no set {name}" for name in study.sets if not _has_set(name)]
    for capture in study.captures:
        try:
            session_dir(capture)
        except (FileNotFoundError, ValueError):
            found.append(f"no capture {capture} in the lake")
    found += [f"no lens {ref}" for ref in study.lenses if not _has_lens(ref)]
    notes = study.findings + [path for line in study.ledger for path in line.evidence]
    found += [f"no file {path}" for path in dict.fromkeys(notes) if not (PROJECT_ROOT / path).exists()]
    return found


def list_studies(root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Every study with a study.yaml, with the references that don't resolve; a study whose file
    can't be read shows its error instead."""
    found: List[Dict[str, Any]] = []
    for folder in sorted((root or studies_root()).iterdir()):
        if not (folder / "study.yaml").exists():
            continue
        try:
            study = load_study(folder)
        except (ValueError, ValidationError, yaml.YAMLError) as e:
            found.append({"id": folder.name, "error": str(e)})
            continue
        found.append({**study.model_dump(mode="json"), "problems": problems(study)})
    return found
