"""The institute's layout (ROOM-16): the file the app draws its map from (`data/institute/layout.yaml`),
and the drafts of a polishing pass (`data/institute/drafts/`)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/institute/layouts")
def layouts() -> List[Dict[str, Any]]:
    """The layout in use ("current") and every draft, each with its title and number of problems."""
    from services.institute import layouts as listed

    return listed()


@router.get("/institute/layout")
def layout(draft: Optional[str] = None) -> Dict[str, Any]:
    """The layout in use, or a draft by name, with what keeps it from being whole (`problems`), or
    the error reading the file."""
    from services.institute import draft_names, drafts_root, layout_report

    if draft is None or draft == "current":
        return layout_report()
    if draft not in draft_names():  # only names listed in the folder, never a path
        raise HTTPException(status_code=404, detail=f"No draft {draft!r} in data/institute/drafts/")
    return layout_report(drafts_root() / f"{draft}.yaml")
