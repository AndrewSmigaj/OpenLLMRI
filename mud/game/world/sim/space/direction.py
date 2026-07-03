"""world.sim.space.direction — relative direction between zones (DR-13, §11–12). Pure.

Bearing (from zone coords) → the 8 compass points; a real elevation difference (≥ 2 m) appends
"and upslope"/"and downslope". Phrases feed the graded look/event lines ("To the south, …").
"""
from __future__ import annotations

from world.sim.space import zones

_POINTS = ("north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest")
_ELEV_STEP_M = 2.0


def compass(bearing: float) -> str:
    """The 8-point compass name for a bearing in degrees (0 = north, clockwise)."""
    return _POINTS[int(((bearing % 360.0) + 22.5) // 45.0) % 8]


def phrase(observer_zone_id: str, target_zone_id: str) -> str:
    """'to the south' / 'to the northeast and upslope' — '' when zones are same/unknown."""
    a, b = zones.get(observer_zone_id), zones.get(target_zone_id)
    if a is None or b is None or a.id == b.id:
        return ""
    out = f"to the {compass(zones.bearing_deg(a.id, b.id))}"
    delta = b.elevation - a.elevation
    if delta >= _ELEV_STEP_M:
        out += " and upslope"
    elif delta <= -_ELEV_STEP_M:
        out += " and downslope"
    return out
