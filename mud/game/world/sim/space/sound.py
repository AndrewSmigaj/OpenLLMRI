"""world.sim.space.sound — loudness × zone hops × weather → audibility (DR-13, §15). Pure.

Speech ranges per §15: whisper → same zone, say → adjacent, call → near, shout → distant. Weather
shifts reach in band-steps (steady_snow −1 … whiteout −3) — a STUB in P3: callers pass
weather="clear" until the P7 weather arc threads real state through. Reach is clamped so the same
zone always hears (you're beside them, whiteout or not). Muffling is priced by zones.sound_hops
(a muffled edge costs 2 hops).
"""
from __future__ import annotations

from world.sim.space import zones

SPEECH_LOUDNESS = {"whisper": 0.15, "say": 0.35, "call": 0.6, "shout": 0.9}   # §15

# STUB until P7 (DR-13a): the §15 band-step table, applied but always "clear" today.
WEATHER_BAND_STEP = {"clear": 0, "light_snow": 0, "steady_snow": 1, "heavy_snow": 2, "whiteout": 3}


def reach_hops(loudness: float) -> int:
    """How many zone hops a sound of this loudness carries in clear air (§15 ranges)."""
    if loudness < 0.2:
        return 0          # whisper → same zone
    if loudness < 0.45:
        return 1          # say / a knife at work → adjacent
    if loudness < 0.7:
        return 2          # call / hacking, prying → near
    if loudness < 0.95:
        return 3          # shout / shattering glass → distant
    return 4              # explosions, fuselage shifts


def audible(loudness: float, hops: "int | None", weather: str = "clear") -> bool:
    """True if a sound of `loudness` carries `hops` (muffle-weighted) zone steps in `weather`."""
    if hops is None:
        return False
    reach = max(reach_hops(loudness) - WEATHER_BAND_STEP.get(weather, 0), 0)
    return hops <= reach


def hear_hops(observer_zone_id, source_zone_id) -> "int | None":
    """Muffle-weighted hops between zones (None-safe passthrough to zones.sound_hops)."""
    return zones.sound_hops(observer_zone_id, source_zone_id)
