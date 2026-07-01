"""Whiteout slice scenario loader — creates the cabin + the ~5 objects (P1.9).

Run: `make load-scenario SCENARIO=whiteout` (→ evennia shell -c 'from world.scenarios.whiteout.build
import build; build()'). Each object is tagged run_id=slice and carries the db schema the WorldView
marshals (sim_id / materials / mass_g / state / parts). Tunable content.
"""
from __future__ import annotations

import evennia

_OBJ = "typeclasses.objects.Object"
_ROOM = "typeclasses.rooms.Room"
_TAGS = [("slice", "run_id")]


def _mk(key, aliases, attrs, location):
    return evennia.create_object(_OBJ, key=key, location=location, aliases=aliases,
                                 attributes=attrs, tags=_TAGS)


def build():
    room = evennia.create_object(_ROOM, key="crash cabin", tags=_TAGS,
                                 attributes=[("world_time", 0)])
    room.db.desc = ("The crushed cabin of a downed light plane. Frost creeps across bent aluminium; "
                    "torn seats and scattered kit lie where the impact flung them.")
    room.db.seed = 1

    _mk("aircraft seat", ["seat"],
        [("sim_id", "seat"), ("materials", ["steel"]), ("mass_g", 5000), ("state", {"ident": "11B"}),
         ("parts", [
             {"id": "cover", "label": "cover", "material": "synthetic_fabric", "mass_g": 200,
              "attachment": "stitched", "outputs_when_removed": ["loose_fabric"]},
             {"id": "cushion", "label": "cushion", "material": "foam", "mass_g": 800,
              "attachment": "clipped", "outputs_when_removed": ["loose_foam"]},
             {"id": "belt", "label": "seatbelt", "material": "nylon_webbing", "mass_g": 150,
              "attachment": "bolted", "outputs_when_removed": ["loose_webbing"]},
             {"id": "bolt", "label": "bolt", "material": "steel", "mass_g": 30, "attachment": "bolted"},
         ])], room)

    _mk("multitool", ["tool", "knife"],
        [("sim_id", "multitool"), ("materials", ["steel"]), ("mass_g", 150),
         ("state", {"edge": 0.8, "leverage": 0.5})], room)

    _mk("dry grass", ["tinder", "grass"],
        [("sim_id", "tinder"), ("materials", ["dry_grass"]), ("mass_g", 40)], room)

    _mk("lighter", [],
        [("sim_id", "lighter"), ("materials", ["plastic"]), ("mass_g", 20),
         ("state", {"ignition": True})], room)

    _mk("field radio", ["radio"],
        [("sim_id", "radio"), ("materials", ["plastic", "copper_wire"]), ("mass_g", 900),
         ("state", {"ident": "RT-220", "powered": False})], room)

    _mk("the pilot", ["pilot", "body"],
        [("sim_id", "pilot"), ("materials", ["flesh"]), ("mass_g", 78000), ("state", {"dead": True})], room)

    return room
