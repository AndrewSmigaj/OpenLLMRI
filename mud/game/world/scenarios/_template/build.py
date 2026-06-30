"""<scenario> loader (Evennia shell side). Copy to world/scenarios/<name>/build.py and implement
`build()` to create the rooms/objects/zones from the manifest; run via
`make load-scenario SCENARIO=<name>`.
"""
from __future__ import annotations


def build():
    """Create the scene in Evennia from the manifest."""
    raise NotImplementedError("scenarios._template.build — copy and implement per scenario")
