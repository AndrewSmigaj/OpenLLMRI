"""Whiteout — content loading (materials + response templates + appearance), shared by the shell +
tests.

`MATERIALS` is the baked material table (loaded once). `load()` installs the narration templates and
the appearance registry (DR-23) and returns MATERIALS. Called from server startup (at_server_start)
and from tests' setUp. Pure-ish: the only side effects populate the loaded-once content registries.
"""
from __future__ import annotations

from world.scenarios.whiteout.appearance import APPEARANCE
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator, presentation
from world.sim.materials import load_materials

MATERIALS = load_materials(MATERIAL_TABLE)


def load():
    narrator.load_responses(RESPONSES)
    presentation.load_appearance(APPEARANCE)
    return MATERIALS
