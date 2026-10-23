"""The institute's layout: the repo's file is whole, each way a layout can break is reported, and
GET /api/institute/layout serves the file with its problems."""

from pathlib import Path
from typing import Any, Dict

import pytest
import yaml  # type: ignore[import-untyped]
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import institute
from services.institute import Layout, layout_path, layout_report, load_layout, problems

SMALL: Dict[str, Any] = {
    "version": 1,
    "floors": [{"id": "ground", "name": "Ground"}, {"id": "upper", "name": "Upper"},
               {"id": "attic", "name": "Attic", "closed": True}],
    "departments": [{"id": "dept", "name": "A department"}],
    "rooms": [
        {"id": "hall", "name": "Hall", "floor": "ground", "at": [0, 0], "opens": "entrance", "summary": "s",
         "exits": {"east": "sim", "up": "landing"}},
        {"id": "sim", "name": "Sim", "floor": "ground", "at": [1, 0], "opens": "simulation", "summary": "s",
         "department": "dept", "exits": {"west": "hall"}},
        {"id": "landing", "name": "Landing", "floor": "upper", "at": [0, 0], "summary": "s",
         "exits": {"down": "hall", "southeast": "office"}, "closed": {"up": "Out of service."}},
        {"id": "office", "name": "Office", "floor": "upper", "at": [1, 1], "opens": "department", "summary": "s",
         "department": "dept", "exits": {"northwest": "landing"}},
    ],
}


def small(**changes: Any) -> Layout:
    """The small layout, with rooms changed by id (a field set to None is removed)."""
    data = yaml.safe_load(yaml.safe_dump(SMALL))
    for room in data["rooms"]:
        for field, value in changes.get(room["id"], {}).items():
            if value is None:
                room.pop(field, None)
            else:
                room[field] = value
    data["rooms"] += changes.get("extra", [])
    return Layout(**data)


def test_the_repo_layout_is_whole() -> None:
    layout = load_layout()
    assert problems(layout) == []
    assert {r.opens for r in layout.rooms} >= {"entrance", "simulation", "department", "observatory",
                                               "workshop", "library", "studies", "meeting"}
    assert [f.id for f in layout.floors if f.closed] == ["third"]  # the out-of-service stairs lead there (L38.4)


def test_a_whole_layout_has_no_problems() -> None:
    assert problems(small()) == []


@pytest.mark.parametrize("changes, expected", [
    ({"sim": {"exits": {}}}, "no way back"),
    ({"sim": {"at": [2, 0]}}, "isn't the next place east"),
    ({"hall": {"exits": {"east": "sim", "up": "landing", "north": "nowhere"}}}, "leads to no room 'nowhere'"),
    ({"landing": {"floor": "attic"}}, "closed, so it holds no room"),
    ({"office": {"at": [0, 0], "exits": {"north": "landing"}}}, "share the place"),
    ({"extra": [{"id": "island", "name": "I", "floor": "ground", "at": [5, 5], "summary": "s"}]},
     "island can't be reached"),
    ({"landing": {"exits": {"down": "hall", "southeast": "office", "up": "hall"}}}, "both open and out of service"),
    ({"office": {"opens": "library"}}, "needs one room of its own"),
    ({"sim": {"department": None}}, "has no simulation room"),
    ({"sim": {"department": "gone"}}, "no department 'gone'"),
])
def test_each_way_a_layout_breaks_is_reported(changes: Dict[str, Any], expected: str) -> None:
    found = problems(small(**changes))
    assert any(expected in p for p in found), found


def test_stairs_must_reach_the_next_floor() -> None:
    data = yaml.safe_load(yaml.safe_dump(SMALL))
    data["floors"].insert(1, {"id": "mezzanine", "name": "M"})  # the landing is now two floors up
    assert any("isn't on the floor up" in p for p in problems(Layout(**data)))


def test_a_broken_file_is_reported_not_raised(tmp_path: Path) -> None:
    path = tmp_path / "layout.yaml"
    path.write_text("version: 1\nfloors: [\n", encoding="utf-8")
    report = layout_report(path)
    assert report["layout"] is None and report["error"]
    path.write_text("version: 1\nfloors: []\nrooms: []\nwings: 3\n", encoding="utf-8")  # an unknown field
    assert "wings" in layout_report(path)["error"]


def test_the_endpoint_serves_the_layout() -> None:
    app = FastAPI()
    app.include_router(institute.router, prefix="/api")
    answer = TestClient(app).get("/api/institute/layout")
    assert answer.status_code == 200
    body = answer.json()
    assert body["error"] is None and body["problems"] == []
    assert len(body["layout"]["rooms"]) == len(load_layout(layout_path()).rooms)
