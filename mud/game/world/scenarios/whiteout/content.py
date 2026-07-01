"""Whiteout — content loading (materials + response templates), shared by the shell + tests.

`MATERIALS` is the baked material table (loaded once). `load()` installs the narration templates and
returns MATERIALS. Called from server startup (at_server_start) and from tests' setUp. Pure-ish: the
only side effect is populating the narrator's response registry (loaded-once content).
"""
from __future__ import annotations

from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.materials import load_materials

MATERIALS = load_materials(MATERIAL_TABLE)


def load():
    narrator.load_responses(RESPONSES)
    return MATERIALS
