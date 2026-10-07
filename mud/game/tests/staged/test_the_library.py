"""Tier-1 pure tests: the library in the repo (data/scenarios/) loads. Every set's manifest is valid,
every staged scenario parses, keys are unique, and every world set names a world the MUD has."""
from pathlib import Path

from world.staged import library

GAME = Path(__file__).resolve().parents[2]


def test_every_set_and_every_scenario_in_the_library_loads():
    sets = library.list_sets()
    assert {s.id for s in sets} >= {"bus_stop_friend_foe_v2", "winter_survival"}
    for s in sets:
        if s.kind != "staged":
            continue
        keys = s.keys()
        assert keys and len(keys) == len(set(keys)), s.id
        for key in keys:
            library.load(key)               # raises ScenarioError naming the file and the field


def test_the_friend_foe_set_is_the_250_files_its_session_used():
    s = library.load_set("bus_stop_friend_foe_v2")
    assert s.ref == "bus_stop_friend_foe_v2@1" and s.kind == "staged" and len(s.keys()) == 250


def test_every_world_set_names_a_world_the_mud_has():
    worlds = [s for s in library.list_sets() if s.kind in ("world", "mini-world")]
    assert worlds
    for s in worlds:
        assert (GAME / "world" / "scenarios" / s.manifest["world"] / "build.py").is_file(), s.id
