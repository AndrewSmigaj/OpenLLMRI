"""One command interface (DESIGN.md E7): Claude Code, Claude agents and MUD commands open a view or
build a lens through it, and open apps hear about it on the event stream.

- `POST /api/commands`: `show` sends a view to every open app (200, with how many heard it);
  `build` starts a lens build in the background and returns its job at once (202).
- `GET /api/app/events`: the server-sent event stream (`show`, `job`, `lens`, `ping`).
- `GET /api/commands`: the latest commands, from the log every command is written to
  (`<lake>/_commands.jsonl`).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, ValidationError

router = APIRouter()

# The app's view state (frontend/src/hooks/useViewState.ts), plus which workspace shows it
VIEW_KEYS = {"session", "lens", "legacy", "layer", "zoom", "color", "color2", "fade", "stripes", "gradient",
             "rank", "top", "sel", "tab", "workspace"}


class Command(BaseModel):
    verb: Literal["show", "build"]
    view: Optional[Dict[str, Any]] = None  # show: the view, as the app's view state names it
    lens: Optional[Dict[str, Any]] = None  # build: the build's settings, as POST /api/lenses takes them
    by: str = Field(default="unknown", max_length=80)  # who sent it: claude-code, mud:<character>, ...


def command_log() -> Path:
    from api import config

    return Path(config.DATA_LAKE_PATH) / "_commands.jsonl"


def _log(command: Command, result: Dict[str, Any]) -> None:
    entry = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **command.model_dump(), "result": result}
    path = command_log()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log:
        log.write(json.dumps(entry) + "\n")


@router.post("/commands")
async def run_command(request: Request, body: Command) -> JSONResponse:
    """`show` a view in the open apps, or `build` a lens in the background."""
    if body.verb == "show":
        view = body.view or {}
        unknown = sorted(set(view) - VIEW_KEYS)
        if unknown or not view.get("session"):
            raise HTTPException(status_code=400, detail=(f"unknown view fields: {', '.join(unknown)}" if unknown
                                                         else "a view needs at least a session"))
        result: Dict[str, Any] = {"verb": "show", "delivered": request.app.state.events.publish(
            "show", {"view": view, "by": body.by})}
        _log(body, result)
        return JSONResponse(result)
    from api.routers.lenses import LensBuildRequest, build_lens

    try:
        build = LensBuildRequest(**{**(body.lens or {}), "created_by": body.by})
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=json.loads(e.json()))
    try:
        started = build_lens(request, build)
    except HTTPException as e:
        _log(body, {"error": e.detail})
        raise
    _log(body, started)
    return JSONResponse(started, status_code=202)


@router.get("/commands")
def recent_commands(limit: int = 20) -> List[Dict[str, Any]]:
    """The latest commands, newest last."""
    path = command_log()
    lines = path.read_text(encoding="utf-8").splitlines()[-max(1, min(limit, 500)):] if path.exists() else []
    return [json.loads(line) for line in lines if line.strip()]


@router.get("/app/events")
async def app_events(request: Request) -> StreamingResponse:
    """Server-sent events for an open app: `show`, `job`, `lens` and `ping`."""
    from api.app_events import stream

    return StreamingResponse(stream(request.app.state.events, request), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
