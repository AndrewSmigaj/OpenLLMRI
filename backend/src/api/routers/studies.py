"""Studies (DESIGN.md G): the study files in the repo (`docs/studies/<id>/study.yaml`)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/studies")
def studies() -> List[Dict[str, Any]]:
    """Every study, with the references that don't resolve (or the error reading its file)."""
    from services.studies import list_studies

    return list_studies()


@router.get("/studies/{study_id}")
def study(study_id: str) -> Dict[str, Any]:
    from services.studies import list_studies

    found = next((s for s in list_studies() if s["id"] == study_id), None)
    if found is None:
        raise HTTPException(status_code=404, detail=f"No study {study_id!r} (docs/studies/{study_id}/study.yaml)")
    return found
