"""The institute's layout (ROOM-16): the file the app draws its map from (`data/institute/layout.yaml`)."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/institute/layout")
def layout() -> Dict[str, Any]:
    """The layout with what keeps it from being whole (`problems`), or the error reading the file."""
    from services.institute import layout_report

    return layout_report()
