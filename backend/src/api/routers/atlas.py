"""The atlas's node catalogue (DESIGN.md H, atlas v1): every node of every saved lens version, read
from the `nodes.json` files beside the versions' records in the repo."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

router = APIRouter()


def _matches(entry: Dict[str, Any], text: str) -> bool:
    report = entry.get("report") or {}
    words = [str(entry["majority"].get("value") or ""), str(report.get("title") or ""),
             str(report.get("summary") or ""), *((entry.get("details") or {}).get("tokens") or [])]
    return any(text in word.lower() for word in words)


@router.get("/atlas/nodes")
def atlas_nodes(session: Optional[str] = None, lens: Optional[str] = None, layer: Optional[int] = None,
                q: Optional[str] = None, validated: bool = False) -> List[Dict[str, Any]]:
    """The node entries, narrowed by capture, lens, layer, validated lenses only, or text found in
    a node's majority value, report or tokens."""
    from services.lenses.atlas import atlas_nodes as read_all

    found = read_all()
    if session:
        found = [e for e in found if e["session_id"] == session]
    if lens:
        found = [e for e in found if e["lens"] == lens]
    if layer is not None:
        found = [e for e in found if e["layer"] == layer]
    if validated:
        found = [e for e in found if e["validated"]]
    if q:
        found = [e for e in found if _matches(e, q.lower())]
    return found


@router.post("/atlas/nodes/{session_id}/{name}/{version}")
def write_lens_nodes(session_id: str, name: str, version: str) -> Dict[str, Any]:
    """Write a saved version's entries again (they're written on save and after its details or
    reports are worked out)."""
    from services.lenses.atlas import write_nodes

    try:
        path = write_nodes(session_id, name, version)
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    if path is None:
        raise HTTPException(status_code=400, detail=f"{name} {version} isn't saved: only saved versions join the atlas")
    return {"written": str(path)}
