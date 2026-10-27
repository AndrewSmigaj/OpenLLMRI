"""The institute's layout (DESIGN.md's rooms; ROOM-16): one file, `data/institute/layout.yaml`, holds
the institute's floor plan: a grid of columns and rows, each room a rectangle of grid cells, and the
doors between rooms that share a wall. The app draws the map from it and the MUD builds the
institute from it, so a change to the layout changes only that file.

The grid's columns and rows each have a size of their own (in metres), so a corridor can be narrow
and a room wide. A layout is whole when (`problems`):
- ids are unique, every department a room names exists, and every room lies on the grid;
- the rooms fill the grid with no overlap, so the building is one rectangle;
- every door joins two rooms that share a wall, and the entrance room is on the front (bottom) edge;
- every room can be reached from the entrance through doors;
- every department has its own room and a simulation room, and its other rooms open only from
  rooms of that department.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Tuple

import yaml  # type: ignore[import-untyped]  # no PyYAML stubs (types-PyYAML) in the venv
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from api.config import PROJECT_ROOT

AppRoom = Literal["entrance", "simulation", "department", "lab", "observatory", "workshop", "library",
                  "studies", "meeting"]
Cell = Tuple[int, int]  # (column, row), rows counted from the back of the building


class Grid(BaseModel):
    model_config = ConfigDict(extra="forbid")
    columns: List[float]  # each column's width, in metres, from left to right
    rows: List[float]  # each row's depth, in metres, from the back to the front


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
    area: Tuple[int, int, int, int]  # first column, first row, last column, last row (inclusive)
    summary: str
    opens: Optional[AppRoom] = None  # the app room it opens; none: in the MUD only
    department: Optional[str] = None
    corridor: bool = False  # a way through, drawn as circulation
    notes: List[str] = Field(default_factory=list)  # what else is there, such as stairs out of service
    characters: List[Character] = Field(default_factory=list)

    def cells(self) -> List[Cell]:
        c0, r0, c1, r1 = self.area
        return [(c, r) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]


class Layout(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int
    title: str = ""
    about: str = ""
    grid: Grid
    departments: List[Department] = Field(default_factory=list)
    rooms: List[Room]
    doors: List[Tuple[str, str]]  # each a pair of room ids
    entrance: str  # the room the front door opens into


def layout_path() -> Path:
    return PROJECT_ROOT / "data" / "institute" / "layout.yaml"


def load_layout(path: Optional[Path] = None) -> Layout:
    text = (path or layout_path()).read_text(encoding="utf-8")
    return Layout(**(yaml.safe_load(text) or {}))


def _duplicates(ids: List[str]) -> List[str]:
    return sorted({i for i in ids if ids.count(i) > 1})


def owners(layout: Layout) -> Dict[Cell, str]:
    """Which room holds each grid cell (the first room listed, where two overlap)."""
    held: Dict[Cell, str] = {}
    for room in layout.rooms:
        for cell in room.cells():
            held.setdefault(cell, room.id)
    return held


def share_a_wall(layout: Layout, a: str, b: str) -> bool:
    held = owners(layout)
    return any(held.get((c + dc, r + dr)) == b
               for (c, r), room in held.items() if room == a
               for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def problems(layout: Layout) -> List[str]:
    """Everything that keeps the layout from being whole (empty when it is)."""
    found: List[str] = []
    columns, rows = len(layout.grid.columns), len(layout.grid.rows)
    departments = {d.id for d in layout.departments}
    rooms = {r.id: r for r in layout.rooms}
    characters = [c.id for r in layout.rooms for c in r.characters]
    for kind, ids in (("department", [d.id for d in layout.departments]), ("room", [r.id for r in layout.rooms]),
                      ("character", characters)):
        found += [f"two {kind}s share the id {i!r}" for i in _duplicates(ids)]

    seen: Dict[Cell, str] = {}
    for room in layout.rooms:
        c0, r0, c1, r1 = room.area
        if not (0 <= c0 <= c1 < columns and 0 <= r0 <= r1 < rows):
            found.append(f"{room.id}: its area {list(room.area)} isn't on the {columns} by {rows} grid")
            continue
        if room.department is not None and room.department not in departments:
            found.append(f"{room.id}: no department {room.department!r}")
        for cell in room.cells():
            if cell in seen:
                found.append(f"{room.id} and {seen[cell]} overlap at {list(cell)}")
            seen.setdefault(cell, room.id)
    empty = [list(cell) for cell in ((c, r) for r in range(rows) for c in range(columns)) if cell not in seen]
    if empty:
        found.append(f"no room fills {empty}: the building isn't one rectangle")

    links: Dict[str, Set[str]] = {r: set() for r in rooms}
    pairs = [tuple(sorted(d)) for d in layout.doors]
    found += [f"two doors join {a} and {b}" for a, b in sorted({p for p in pairs if pairs.count(p) > 1})]
    for a, b in layout.doors:
        missing = [x for x in (a, b) if x not in rooms]
        if missing:
            found.append(f"a door leads to no room {missing[0]!r}")
        elif a == b or not share_a_wall(layout, a, b):
            found.append(f"the door between {a} and {b} has no wall to sit in")
        else:
            links[a].add(b)
            links[b].add(a)

    if layout.entrance not in rooms:
        found.append(f"no entrance room {layout.entrance!r}")
    else:
        if rooms[layout.entrance].area[3] != rows - 1:
            found.append(f"the entrance room {layout.entrance} isn't on the front edge")
        reached, frontier = {layout.entrance}, [layout.entrance]
        while frontier:
            for next_id in links[frontier.pop()]:
                if next_id not in reached:
                    reached.add(next_id)
                    frontier.append(next_id)
        found += [f"{r} can't be reached from the entrance" for r in rooms if r not in reached]

    for department in layout.departments:
        own = [r for r in layout.rooms if r.department == department.id]
        if sum(r.opens == "department" for r in own) != 1:
            found.append(f"the {department.id} department needs one room of its own")
        if not any(r.opens == "simulation" for r in own):
            found.append(f"the {department.id} department has no simulation room")
        for room in own:
            if room.opens != "department":
                outside = sorted(n for n in links[room.id] if rooms[n].department != department.id)
                if outside:
                    found.append(f"{room.id} belongs to {department.id} but opens onto {', '.join(outside)}")
    return found


def layout_report(path: Optional[Path] = None) -> Dict[str, Any]:
    """The layout with its problems, or the error reading the file."""
    try:
        layout = load_layout(path)
    except (OSError, yaml.YAMLError, ValidationError, TypeError) as error:
        return {"layout": None, "problems": [], "error": str(error)}
    return {"layout": layout.model_dump(), "problems": problems(layout), "error": None}
