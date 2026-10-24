"""The institute's layout (DESIGN.md's rooms; ROOM-16): one file, `data/institute/layout.yaml`,
lists the floors, departments, rooms, exits and where the non-player characters stand. The app draws
the institute's map from it and the MUD builds the institute from it, so a polishing pass over the
layout changes only that file. Drafts for a pass sit beside it in `data/institute/drafts/`, one file
each, until Andrew picks one.

A layout is whole when (`problems`):
- ids are unique, and every room names a floor and department that exist;
- a closed floor holds no room, and no two rooms share a place on a floor;
- every exit leads to a room that exists, in the direction its place says (east along the same row,
  north up the same column, northeast along the diagonal; up and down the floor above and below)
  with no room in between, and has its way back;
- every room can be reached from the entrance through exits that are open;
- every department has its own room and at least one simulation room.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import yaml  # type: ignore[import-untyped]  # no PyYAML stubs (types-PyYAML) in the venv
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from api.config import PROJECT_ROOT

Direction = Literal["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest",
                    "up", "down"]
AppRoom = Literal["entrance", "simulation", "department", "lab", "observatory", "workshop", "library",
                  "studies", "meeting"]
# A room not built yet: "later", one the design already plans for later; "suggested", Claude's
# suggestion, waiting for Andrew to keep it or veto it
Stage = Literal["later", "suggested"]

# The grid step each direction takes: (columns east, rows south)
STEPS: Dict[str, Tuple[int, int]] = {
    "north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0),
    "northeast": (1, -1), "northwest": (-1, -1), "southeast": (1, 1), "southwest": (-1, 1),
}
OPPOSITE: Dict[str, Direction] = {
    "north": "south", "south": "north", "east": "west", "west": "east", "northeast": "southwest",
    "southwest": "northeast", "northwest": "southeast", "southeast": "northwest", "up": "down", "down": "up",
}


class Floor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    note: str = ""
    closed: bool = False


class Department(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str


class Character(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    note: str = ""


class Room(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    floor: str
    at: Tuple[int, int]  # [column, row] on its floor's grid
    summary: str
    opens: Optional[AppRoom] = None  # the app room it opens; none: in the MUD only
    department: Optional[str] = None
    stage: Optional[Stage] = None
    exits: Dict[Direction, str] = Field(default_factory=dict)
    closed: Dict[Direction, str] = Field(default_factory=dict)  # out of service, with what a player is told
    characters: List[Character] = Field(default_factory=list)


class Layout(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int
    title: str = ""
    about: str = ""  # what the layout is built around
    floors: List[Floor]  # from the bottom up
    departments: List[Department] = Field(default_factory=list)
    rooms: List[Room]


def layout_path() -> Path:
    return PROJECT_ROOT / "data" / "institute" / "layout.yaml"


def drafts_root() -> Path:
    return PROJECT_ROOT / "data" / "institute" / "drafts"


def draft_names() -> List[str]:
    root = drafts_root()
    return sorted(p.stem for p in root.glob("*.yaml")) if root.exists() else []


def load_layout(path: Optional[Path] = None) -> Layout:
    text = (path or layout_path()).read_text(encoding="utf-8")
    return Layout(**(yaml.safe_load(text) or {}))


def _along(start: Tuple[int, int], end: Tuple[int, int], step: Tuple[int, int]) -> bool:
    """Whether `end` lies some whole number of steps from `start` in the step's direction."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    n = max(abs(dx), abs(dy))
    return n > 0 and (dx, dy) == (step[0] * n, step[1] * n)


def _between(start: Tuple[int, int], end: Tuple[int, int], step: Tuple[int, int]) -> List[Tuple[int, int]]:
    n = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    return [(start[0] + step[0] * i, start[1] + step[1] * i) for i in range(1, n)]


def _duplicates(ids: List[str]) -> List[str]:
    return sorted({i for i in ids if ids.count(i) > 1})


def problems(layout: Layout) -> List[str]:
    """Everything that keeps the layout from being whole (empty when it is)."""
    found: List[str] = []
    floors = {f.id: i for i, f in enumerate(layout.floors)}
    closed_floors = {f.id for f in layout.floors if f.closed}
    departments = {d.id for d in layout.departments}
    rooms = {r.id: r for r in layout.rooms}
    characters = [c.id for r in layout.rooms for c in r.characters]
    for kind, ids in (("floor", [f.id for f in layout.floors]), ("department", [d.id for d in layout.departments]),
                      ("room", [r.id for r in layout.rooms]), ("character", characters)):
        found += [f"two {kind}s share the id {i!r}" for i in _duplicates(ids)]

    places: Dict[Tuple[str, int, int], str] = {}
    for room in layout.rooms:
        if room.floor not in floors:
            found.append(f"{room.id}: no floor {room.floor!r}")
            continue
        if room.floor in closed_floors:
            found.append(f"{room.id}: the {room.floor} floor is closed, so it holds no room")
        if room.department is not None and room.department not in departments:
            found.append(f"{room.id}: no department {room.department!r}")
        place = (room.floor, *room.at)
        if place in places:
            found.append(f"{room.id} and {places[place]} share the place {list(room.at)} on the {room.floor} floor")
        places[place] = room.id
        for direction in set(room.exits) & set(room.closed):
            found.append(f"{room.id}: the {direction} exit is both open and out of service")
        for direction, target_id in room.exits.items():
            target = rooms.get(target_id)
            if target is None:
                found.append(f"{room.id}: its {direction} exit leads to no room {target_id!r}")
                continue
            if target.exits.get(OPPOSITE[direction]) != room.id:
                found.append(f"{room.id}: its {direction} exit to {target_id} has no way back ({OPPOSITE[direction]})")
            if target.floor not in floors:
                continue
            if direction in STEPS:
                if target.floor != room.floor or not _along(room.at, target.at, STEPS[direction]):
                    found.append(f"{room.id}: {target_id} isn't {direction} of it")
                    continue
                between = _between(room.at, target.at, STEPS[direction])
                blocking = [r.id for r in layout.rooms if r.floor == room.floor and tuple(r.at) in between]
                if blocking:
                    found.append(f"{room.id}: its {direction} exit to {target_id} passes through {', '.join(blocking)}")
            else:
                rise = 1 if direction == "up" else -1
                if floors[target.floor] != floors[room.floor] + rise:
                    found.append(f"{room.id}: {target_id} isn't on the floor {direction} from it")

    entrances = [r.id for r in layout.rooms if r.opens == "entrance"]
    if len(entrances) != 1:
        found.append(f"one room opens the entrance; found {len(entrances)}")
    else:
        reached = {entrances[0]}
        frontier = [entrances[0]]
        while frontier:
            for next_id in rooms[frontier.pop()].exits.values():
                if next_id in rooms and next_id not in reached:
                    reached.add(next_id)
                    frontier.append(next_id)
        found += [f"{r.id} can't be reached from the entrance" for r in layout.rooms if r.id not in reached]

    for department in layout.departments:
        own = [r for r in layout.rooms if r.department == department.id]
        if sum(r.opens == "department" for r in own) != 1:
            found.append(f"the {department.id} department needs one room of its own")
        if not any(r.opens == "simulation" for r in own):
            found.append(f"the {department.id} department has no simulation room")
    return found


def layout_report(path: Optional[Path] = None) -> Dict[str, Any]:
    """The layout with its problems, or the error reading the file."""
    try:
        layout = load_layout(path)
    except (OSError, yaml.YAMLError, ValidationError, TypeError) as error:
        return {"layout": None, "problems": [], "error": str(error)}
    return {"layout": layout.model_dump(), "problems": problems(layout), "error": None}


def layouts() -> List[Dict[str, Any]]:
    """The layout in use and every draft: name, title, file, and how many problems each has."""
    found = []
    for name, path in [("current", layout_path()), *[(n, drafts_root() / f"{n}.yaml") for n in draft_names()]]:
        report = layout_report(path)
        layout = report["layout"] or {}
        found.append({"name": name, "title": layout.get("title") or name,
                      "file": str(path.relative_to(PROJECT_ROOT)),
                      "problems": len(report["problems"]) + (1 if report["error"] else 0)})
    return found
