"""The institute's floor plan: the repo's layout is whole, each way a layout can break is reported, and
GET /api/institute/layout serves the file with its problems."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
import yaml  # type: ignore[import-untyped]
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import institute
from services.institute import Layout, layout_report, load_layout, problems

# A small building, two columns by three rows: a department with its simulation room at the back,
# a corridor, and the entrance hall beside a public room at the front
SMALL: Dict[str, Any] = {
    "version": 2,
    "grid": {"columns": [6, 6], "rows": [4, 2, 4]},
    "departments": [{"id": "dept", "name": "A department"}],
    "entrance": "hall",
    "rooms": [
        {"id": "dept", "name": "Dept", "area": [0, 0, 0, 0], "summary": "s", "department": "dept",
         "opens": "department"},
        {"id": "deptsim", "name": "Dept sim", "area": [1, 0, 1, 0], "summary": "s", "department": "dept",
         "opens": "simulation"},
        {"id": "corridor", "name": "Corridor", "area": [0, 1, 1, 1], "summary": "s", "corridor": True},
        {"id": "public", "name": "Public", "area": [0, 2, 0, 2], "summary": "s", "opens": "simulation"},
        {"id": "hall", "name": "Hall", "area": [1, 2, 1, 2], "summary": "s", "opens": "entrance"},
    ],
    "doors": [["hall", "public"], ["hall", "corridor"], ["corridor", "dept"], ["dept", "deptsim"]],
}
DOORS = SMALL["doors"]


def small(rooms: Optional[Dict[str, Dict[str, Any]]] = None, doors: Optional[List[List[str]]] = None,
          **top: Any) -> Layout:
    """The small building with rooms changed by id (a field set to None is removed)."""
    data = yaml.safe_load(yaml.safe_dump(SMALL))
    for room in data["rooms"]:
        for field, value in (rooms or {}).get(room["id"], {}).items():
            if value is None:
                room.pop(field, None)
            else:
                room[field] = value
    if doors is not None:
        data["doors"] = doors
    data.update(top)
    return Layout(**data)


def test_the_repo_layout_is_whole() -> None:
    layout = load_layout()
    assert problems(layout) == []
    ids = {r.id for r in layout.rooms}
    assert {"entrance_hall", "polysemy_lab", "library", "lounge", "meeting_room", "scaffold_studio"} <= ids
    assert sum(r.opens == "simulation" and r.department is None for r in layout.rooms) == 3  # the public ones
    # the departments sit together along the back of the building, the visitors' rooms at the front
    assert {r.area[1] for r in layout.rooms if r.opens == "department"} == {1}
    front = {r.id for r in layout.rooms if r.area[3] == len(layout.grid.rows) - 1}
    assert {"entrance_hall", "library", "public_sim_3"} <= front


def test_a_whole_layout_has_no_problems() -> None:
    assert problems(small()) == []


@pytest.mark.parametrize("change, expected", [
    ({"rooms": {"public": {"area": [0, 2, 1, 2]}}}, "overlap"),
    ({"grid": {"columns": [6, 6, 6], "rows": [4, 2, 4]}}, "isn't one rectangle"),
    ({"rooms": {"public": {"area": [0, 3, 0, 3]}}}, "isn't on the 2 by 3 grid"),
    ({"doors": DOORS + [["hall", "dept"]]}, "has no wall to sit in"),
    ({"doors": [["hall", "public"], ["corridor", "dept"], ["dept", "deptsim"]]}, "can't be reached from the entrance"),
    ({"doors": DOORS + [["corridor", "deptsim"]]}, "deptsim belongs to dept but opens onto corridor"),
    ({"doors": DOORS + [["public", "hall"]]}, "two doors join hall and public"),
    ({"doors": DOORS + [["hall", "nowhere"]]}, "a door leads to no room 'nowhere'"),
    ({"entrance": "dept"}, "isn't on the front edge"),
    ({"rooms": {"deptsim": {"opens": None}}}, "has no simulation room"),
    ({"rooms": {"deptsim": {"department": "gone"}}}, "no department 'gone'"),
])
def test_each_way_a_layout_breaks_is_reported(change: Dict[str, Any], expected: str) -> None:
    found = problems(small(**change))
    assert any(expected in p for p in found), found


def test_a_broken_file_is_reported_not_raised(tmp_path: Path) -> None:
    path = tmp_path / "layout.yaml"
    path.write_text("version: 2\ngrid: [\n", encoding="utf-8")
    report = layout_report(path)
    assert report["layout"] is None and report["error"]
    path.write_text(yaml.safe_dump({**SMALL, "wings": 3}), encoding="utf-8")  # an unknown field
    assert "wings" in layout_report(path)["error"]


def test_the_endpoint_serves_the_layout() -> None:
    app = FastAPI()
    app.include_router(institute.router, prefix="/api")
    answer = TestClient(app).get("/api/institute/layout")
    assert answer.status_code == 200
    body = answer.json()
    assert body["error"] is None and body["problems"] == []
    assert len(body["layout"]["rooms"]) == len(load_layout().rooms)
