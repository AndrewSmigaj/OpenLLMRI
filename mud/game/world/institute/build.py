"""world.institute.build — the institute's rooms: the hub, the polysemy lab and the simulator, with
exits between them.

Idempotent: it finds each room by its tag and creates only what is missing, so it is safe to re-run.
The hub is the server's start room (settings.START_LOCATION, Evennia's Limbo), converted in place, so
new characters start there. Run by `make institute`, and on a new database's first start
(server/conf/at_initial_setup.py). Room descriptions are placeholders.
"""
from __future__ import annotations

import yaml
from django.conf import settings
from evennia import create_object, search_object, search_tag

from typeclasses.institute.rooms import lab_presets_root

HUB = "typeclasses.institute.rooms.HubRoom"
LAB = "typeclasses.institute.rooms.LabRoom"
SIMULATOR = "typeclasses.institute.rooms.SimulatorRoom"
EXIT = "typeclasses.exits.Exit"
CATEGORY = "institute"
POLYSEMY_PRESET = "polysemy_tank"

HUB_DESC = ("The hub of the Scaffold Dynamics institute. Corridors lead to the polysemy lab and the "
            "simulator. (Placeholder description.)")
SIMULATOR_DESC = ("The simulator. Every scenario in the library can be played from here: type "
                  "|wsimulator|n to see them. (Placeholder description.)")


def _tagged(name: str):
    found = search_tag(name, category=CATEGORY)
    return found[0] if found else None


def _hub(start=None):
    hub = _tagged("hub")
    if hub is not None:
        return hub
    if start is None:
        start = search_object(settings.START_LOCATION)[0]
    if not start.is_typeclass(HUB, exact=True):
        start.swap_typeclass(HUB, clean_attributes=False)
    start.key = "Hub"
    start.db.desc = HUB_DESC
    start.tags.add("hub", category=CATEGORY)
    return start


def _room(name: str, typeclass: str, key: str, desc: str, **attributes):
    room = _tagged(name)
    if room is None:
        room = create_object(typeclass, key=key, tags=[(name, CATEGORY)])
        room.db.desc = desc
    for attr, value in attributes.items():
        room.attributes.add(attr, value)
    return room


def _exit(source, destination, key: str, aliases=()):
    if not any(e.destination == destination for e in source.exits):
        create_object(EXIT, key=key, aliases=list(aliases), location=source, destination=destination)


def build(start=None):
    """Make the institute (or finish making it). `start`: the room to make the hub, by default the
    server's start room. Returns (hub, lab, simulator)."""
    hub = _hub(start)
    preset = yaml.safe_load((lab_presets_root() / f"{POLYSEMY_PRESET}.yaml").read_text(encoding="utf-8"))
    lab = _room("polysemy_lab", LAB, preset["name"], " ".join(preset["description"].split()),
                preset=POLYSEMY_PRESET)
    simulator = _room("simulator", SIMULATOR, "Simulator", SIMULATOR_DESC)
    _exit(hub, lab, "polysemy lab", aliases=("lab", "polysemy"))
    _exit(lab, hub, "hub")
    _exit(hub, simulator, "simulator", aliases=("sim",))
    _exit(simulator, hub, "hub")
    return hub, lab, simulator
