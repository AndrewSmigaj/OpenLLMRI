"""Whiteout crash-site loader — the ZONED, CONTAINMENT-FIRST scene (P1.9 → DR-13a → DR-24).

Run: `make load-scenario SCENARIO=whiteout`. Each object is tagged run_id=slice and carries the db
schema the WorldView marshals (sim_id / materials / mass_g / state / parts). Most loot is STOWED —
inside bins, bags, pockets, the pilot, the snow — per DR-24: the scene surfaces fixtures and
containers; open/search/dig earn the contents. Stowed items need no zone (effective zone chains
through the container). Tunable content.
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
    room.db.default_zone = "mid_cabin"    # anything unzoned stands here (DR-13a)

    # ------------------------------------------------------------------ cockpit
    _mk("field radio", ["radio"],
        [("sim_id", "radio"), ("materials", ["plastic", "copper_wire"]), ("mass_g", 900),
         ("state", {"zone": "cockpit", "ident": "RT-220", "powered": False, "fixed": True})], room)

    pilot = _mk("the pilot", ["pilot", "body"],
                [("sim_id", "pilot"), ("materials", ["flesh"]), ("mass_g", 78000),
                 ("state", {"zone": "cockpit", "dead": True})], room)
    _mk("lighter", [],
        [("sim_id", "lighter"), ("materials", ["plastic"]), ("mass_g", 20),
         ("state", {"ignition": True})], pilot)                       # his jacket pocket — frisk him
    _mk("flight jacket", ["jacket", "coat"],
        [("sim_id", "jacket"), ("materials", ["leather"]), ("mass_g", 1200),
         ("state", {"worn_by": "pilot"})], pilot)                     # worn — the visible layer

    _mk("flight manual", ["manual", "book", "handbook"],
        [("sim_id", "manual"), ("materials", ["paper"]), ("mass_g", 300),
         ("state", {"zone": "cockpit"})], room)                       # teaser — and readable (§38)

    panel = _mk("avionics panel", ["panel"],
                [("sim_id", "panel"), ("materials", ["aluminum"]), ("mass_g", 1800),
                 ("state", {"zone": "cockpit", "container": True, "open": False,
                            "jammed": True, "fixed": True})], room)
    _mk("coil of copper wire", ["wire", "coil"],
        [("sim_id", "wire"), ("materials", ["copper_wire"]), ("mass_g", 120)], panel)

    # ---------------------------------------------------------------- mid cabin
    seat = _mk("aircraft seat", ["seat"],
               [("sim_id", "seat"), ("materials", ["steel"]), ("mass_g", 5000),
                ("state", {"zone": "mid_cabin", "ident": "11B", "fixed": True}),
                ("parts", [
                    {"id": "cover", "label": "cover", "material": "synthetic_fabric", "mass_g": 200,
                     "attachment": "stitched", "outputs_when_removed": ["loose_fabric"]},
                    {"id": "cushion", "label": "cushion", "material": "foam", "mass_g": 800,
                     "attachment": "clipped", "outputs_when_removed": ["loose_foam"]},
                    {"id": "belt", "label": "seatbelt", "material": "nylon_webbing", "mass_g": 150,
                     "attachment": "bolted", "outputs_when_removed": ["loose_webbing"]},
                    {"id": "bolt", "label": "bolt", "material": "steel", "mass_g": 30,
                     "attachment": "bolted"},
                ])], room)
    pocket = _mk("seatback pocket", ["pocket"],
                 [("sim_id", "seatpocket"), ("materials", ["synthetic_fabric"]), ("mass_g", 100),
                  ("state", {"container": True})], seat)              # found by `search seat`
    _mk("chocolate bar", ["chocolate", "bar", "ration"],
        [("sim_id", "chocolate"), ("materials", ["chocolate"]), ("mass_g", 100)], pocket)

    bin_fwd = _mk("forward overhead bin", ["bin", "fwd bin"],
                  [("sim_id", "bin_fwd"), ("materials", ["aluminum"]), ("mass_g", 2500),
                   ("state", {"zone": "mid_cabin", "ident": "fwd", "container": True,
                              "open": False, "fixed": True})], room)
    kit = _mk("first-aid kit", ["kit", "first aid"],
              [("sim_id", "firstaid"), ("materials", ["plastic"]), ("mass_g", 400),
               ("state", {"container": True, "open": False})], bin_fwd)
    _mk("bandage roll", ["bandage", "bandages"],
        [("sim_id", "bandage"), ("materials", ["cotton_cloth"]), ("mass_g", 150)], kit)
    _mk("medical tape", ["tape"],
        [("sim_id", "tape"), ("materials", ["plastic"]), ("mass_g", 60)], kit)

    duffel = _mk("duffel bag", ["duffel", "bag", "luggage"],
                 [("sim_id", "duffel"), ("materials", ["synthetic_fabric"]), ("mass_g", 900),
                  ("state", {"zone": "mid_cabin", "container": True})], room)   # burst — searchable
    _mk("multitool", ["tool", "knife"],
        [("sim_id", "multitool"), ("materials", ["steel"]), ("mass_g", 150),
         ("state", {"edge": 0.8, "leverage": 0.5})], duffel)
    _mk("length of paracord", ["paracord", "cord", "rope"],
        [("sim_id", "paracord"), ("materials", ["nylon_webbing"]), ("mass_g", 90)], duffel)
    _mk("wool socks", ["socks"],
        [("sim_id", "socks"), ("materials", ["wool"]), ("mass_g", 150)], duffel)

    _mk("oxygen masks", ["masks", "mask"],
        [("sim_id", "masks"), ("materials", ["plastic"]), ("mass_g", 400),
         ("state", {"zone": "mid_cabin", "fixed": True}),
         ("parts", [
             {"id": "cup", "label": "mask cup", "material": "plastic", "mass_g": 120,
              "attachment": "clipped", "outputs_when_removed": ["loose_cup"]},
             {"id": "tubing", "label": "tubing", "material": "rubber", "mass_g": 180,
              "attachment": "tied", "outputs_when_removed": ["rubber_tubing"]},
         ])], room)

    # --------------------------------------------------------------- rear cabin
    drift = _mk("snowdrift", ["snow", "drift"],
                [("sim_id", "snowdrift"), ("materials", ["snow"]), ("mass_g", 4000),
                 ("state", {"zone": "rear_cabin", "fixed": True})], room)
    _mk("leather gloves", ["gloves"],
        [("sim_id", "gloves"), ("materials", ["leather"]), ("mass_g", 300)], drift)   # dig for them

    bin_aft = _mk("aft overhead bin", ["aft bin"],
                  [("sim_id", "bin_aft"), ("materials", ["aluminum"]), ("mass_g", 2500),
                   ("state", {"zone": "rear_cabin", "ident": "aft", "container": True,
                              "open": False, "jammed": True, "fixed": True})], room)
    backpack = _mk("backpack", ["pack", "rucksack"],
                   [("sim_id", "backpack"), ("materials", ["synthetic_fabric"]), ("mass_g", 700),
                    ("state", {"container": True})], bin_aft)         # the pry-loop reward
    _mk("canteen of water", ["canteen", "flask"],
        [("sim_id", "canteen"), ("materials", ["water"]), ("mass_g", 600),
         ("state", {"ident": "half-full"})], backpack)
    _mk("spare shirt", ["shirt"],
        [("sim_id", "shirt"), ("materials", ["cotton_cloth"]), ("mass_g", 250)], backpack)

    _mk("whisky bottle", ["bottle", "whisky"],
        [("sim_id", "bottle"), ("materials", ["glass"]), ("mass_g", 500),
         ("state", {"zone": "rear_cabin"})], room)                    # teaser
    _mk("wool blanket", ["blanket", "wool"],
        [("sim_id", "blanket"), ("materials", ["wool"]), ("mass_g", 700),
         ("state", {"zone": "rear_cabin"})], room)                    # teaser, half-spilled

    # ------------------------------------------------------------------ outside
    _mk("chunk of ice", ["ice", "chunk"],
        [("sim_id", "ice"), ("materials", ["ice"]), ("mass_g", 600),
         ("state", {"zone": "outside_tail"})], room)
    _mk("jerry can", ["can", "jerrycan"],
        [("sim_id", "jerrycan"), ("materials", ["fuel"]), ("mass_g", 3000),
         ("state", {"zone": "outside_tail", "sealed": True})], room)

    # ----------------------------------------------------------------- treeline
    _mk("dry grass", ["tinder", "grass"],
        [("sim_id", "tinder"), ("materials", ["dry_grass"]), ("mass_g", 40),
         ("state", {"zone": "treeline"})], room)
    _mk("spruce tree", ["spruce", "tree", "trees"],
        [("sim_id", "spruce"), ("materials", ["wood"]), ("mass_g", 200000),
         ("state", {"zone": "treeline", "fixed": True}),
         ("parts", [
             {"id": "low branch", "label": "low branch", "material": "wood", "mass_g": 900,
              "attachment": "grown", "outputs_when_removed": ["loose_branch"]},
             {"id": "bough", "label": "bough", "material": "wood", "mass_g": 2500,
              "attachment": "grown", "outputs_when_removed": ["loose_bough"]},
         ])], room)
    for i in (1, 2):
        _mk("deadfall branch", ["deadfall", "branch"],
            [("sim_id", f"deadfall{i}"), ("materials", ["wood"]), ("mass_g", 800),
             ("state", {"zone": "treeline"})], room)

    return room
