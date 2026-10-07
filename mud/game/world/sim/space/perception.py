"""world.sim.space.perception — the separate axes composed into a PerceptionResult (DR-13, §14).

visibility / audibility / reachability / direction / detail stay SEPARATE (§10: "do not collapse
these into 'room'"). Band v1 = see-edge hops → the §14 ladder; weather is a "clear"-defaulting
parameter (the P7 seam). THE ONE-ZONE COMPAT RULE: an observer or target with no zone is
SAME_ZONE — a zone-less world is a one-zone world (keeps every unzoned fixture/scenario exact).
Pure. `look` renders perception; reachability gates manipulation (the resolver's too-far gate).
"""
from __future__ import annotations

from world.sim.contracts import PerceptionBand, PerceptionResult
from world.sim.space import direction, sound, zones

_LADDER = (PerceptionBand.SAME_ZONE, PerceptionBand.ADJACENT_ZONE, PerceptionBand.NEAR_VISIBLE,
           PerceptionBand.DISTANT_VISIBLE, PerceptionBand.BARELY_VISIBLE)


def visual_band(observer_zone, target_zone, weather: str = "clear") -> PerceptionBand:
    """The §14 visual band from see-edge hops (+ weather band-steps). None zone → SAME_ZONE."""
    if observer_zone is None or target_zone is None:
        return PerceptionBand.SAME_ZONE
    hops = zones.see_hops(observer_zone, target_zone)
    if hops is None:
        return PerceptionBand.OUT_OF_SIGHT
    idx = hops + sound.WEATHER_BAND_STEP.get(weather, 0)
    if idx >= len(_LADDER):
        return PerceptionBand.OUT_OF_SIGHT
    return _LADDER[idx]


def perceive(observer_zone, target_zone, loudness: float = 0.0,
             weather: str = "clear") -> PerceptionResult:
    """One observer's full perception of one source: band + the separate axes + direction."""
    vband = visual_band(observer_zone, target_zone, weather)
    visible = vband is not PerceptionBand.OUT_OF_SIGHT
    heard = sound.audible(loudness, zones.sound_hops(observer_zone, target_zone), weather) \
        if (observer_zone is not None and target_zone is not None) else True
    band = vband if visible else (PerceptionBand.AUDIBLE_ONLY if heard else PerceptionBand.OUT_OF_SIGHT)
    reach = observer_zone is None or target_zone is None or observer_zone == target_zone
    dphrase = direction.phrase(observer_zone, target_zone) \
        if (observer_zone and target_zone and observer_zone != target_zone) else ""
    dist = zones.distance_m(observer_zone, target_zone) \
        if (zones.get(observer_zone) and zones.get(target_zone)) else 0.0
    return PerceptionResult(band=band, visible=visible, audible=heard, reachable=reach,
                            direction_phrase=dphrase, distance_m=dist)
