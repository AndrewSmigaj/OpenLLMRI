"""Whiteout crash-site loader — the ZONED, CONTAINMENT-FIRST scene (P1.9 → DR-13a → DR-24 → DR-17a).

Run: `make load-scenario SCENARIO=whiteout`. The content is the OBJECT_TABLE in `objects.py` (the
authoring surface, docs/guides/authoring-objects.md); this module is the thin imperative loader that
walks it into Evennia — parents first, so a stowed thing (`in`) lands inside its container (DR-24:
the scene surfaces fixtures and containers; open/search/dig earn the contents). Each object is tagged
run_id=slice and carries the db schema the WorldView marshals (sim_id / materials / mass_g / state /
parts). The same table feeds the pure `PureWorld` used by probes and fuzz.
"""
from __future__ import annotations

import evennia

from world.scenarios.whiteout.characters import character_state, outfit
from world.scenarios.whiteout.objects import OBJECT_TABLE

_OBJ = "typeclasses.objects.Object"
_ROOM = "typeclasses.rooms.Room"
_TAGS = [("slice", "run_id")]
_ROOM_DESC = ("The crushed cabin of a downed light plane. Frost creeps across bent aluminium; "
              "torn seats and scattered kit lie where the impact flung them.")


def _attrs(row: dict) -> list:
    """The Attribute list for one table row (the schema `typeclasses/worldview.py` reads)."""
    state = dict(row.get("state") or {})
    if "zone" in row:
        state["zone"] = row["zone"]
    attrs = [("sim_id", row["sim_id"]), ("materials", list(row.get("materials") or [])),
             ("mass_g", int(row.get("mass_g", 0)))]
    if state:
        attrs.append(("state", state))
    if row.get("parts"):
        attrs.append(("parts", [dict(p) for p in row["parts"]]))
    return attrs


def load_table(rows, room, make=None):
    """Create every row as an Evennia object, parents before children. `make` is injectable so the
    loader can be exercised without Evennia (tests / tools). Returns {sim_id: object}."""
    make = make or (lambda key, aliases, attrs, location: evennia.create_object(
        _OBJ, key=key, location=location, aliases=aliases, attributes=attrs, tags=_TAGS))
    by_id: dict = {}
    pending = list(rows)
    while pending:
        progressed = False
        for row in list(pending):
            parent = row.get("in")
            if parent is not None and parent not in by_id:
                continue                                    # wait for the container
            location = by_id[parent] if parent is not None else room
            by_id[row["sim_id"]] = make(row["name"], list(row.get("aliases") or []), _attrs(row), location)
            pending.remove(row)
            progressed = True
        if not progressed:
            orphans = [r["sim_id"] for r in pending]
            raise ValueError(f"OBJECT_TABLE: rows stowed in unknown parents: {orphans}")
    return by_id


def build():
    room = evennia.create_object(_ROOM, key="crash cabin", tags=_TAGS,
                                 attributes=[("world_time", 0)])
    room.db.desc = _ROOM_DESC
    room.db.seed = 1
    room.db.default_zone = "mid_cabin"    # anything unzoned stands here (DR-13a)
    load_table(OBJECT_TABLE, room)
    return room


def dress(character, slot: str, make=None):
    """Give a character its crash draw (players-and-kit.md): the worn things (worn_by set), the
    pockets and their contents, and the slot's starting state (zone, wounds). Build-time only —
    the P6 instance spawn calls this per party member; smokes and tests call it directly."""
    sim_id = character.db.sim_id or character.key
    rows = []
    for r in outfit(slot):
        r = dict(r)
        st = dict(r.get("state") or {})
        if st.pop("worn", None):
            st["worn_by"] = sim_id
        r["state"] = st
        rows.append(r)
    made = load_table(rows, character, make=make)
    st = dict(character.db.state or {})
    st.update(character_state(slot))
    character.db.state = st
    return made
