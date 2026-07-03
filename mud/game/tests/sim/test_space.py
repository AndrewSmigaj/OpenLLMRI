"""Tier-1: the pure space core — zones/hops/direction/sound/perception (DR-13/DR-13a, §10–15).

Synthetic map shaped like the crash site: a walk+see chain A—B—C—D—E, a see-only edge A~F
(the shattered-windscreen pattern), and a muffled edge D—G (a closed hatch)."""
import pytest

from world.sim.contracts import PerceptionBand
from world.sim.space import direction, perception, sound, zones

MAP = {
    "a": {"name": "the cockpit-like end", "x": 0, "y": -8,
          "adjacent": {"b": {"walk": True, "see": True}, "f": {"see": True}}},
    "b": {"name": "the mid", "x": 0, "y": -2, "adjacent": {"c": {"walk": True, "see": True}}},
    "c": {"name": "the rear", "x": 0, "y": 4, "adjacent": {"d": {"walk": True, "see": True}}},
    "d": {"name": "the breach", "x": 3, "y": 10,
          "adjacent": {"e": {"walk": True, "see": True}, "g": {"walk": True, "muffle": True}}},
    "e": {"name": "the treeline", "x": 0, "y": 40, "elevation": 2,
          "terrain_tags": ["trees"], "aliases": ["trees"]},
    "f": {"name": "the snow outside", "x": -4, "y": -12},
    "g": {"name": "the hold", "x": 6, "y": 10, "elevation": -3},
}


def setup_module(_):
    zones.load_zones(MAP)


# --- zones: load validation, hops -------------------------------------------

def test_load_rejects_unknown_and_self_and_contradictory_edges():
    with pytest.raises(ValueError):
        zones.load_zones({"x": {"name": "x", "x": 0, "y": 0, "adjacent": {"nope": {"walk": True}}}})
    with pytest.raises(ValueError):
        zones.load_zones({"x": {"name": "x", "x": 0, "y": 0, "adjacent": {"x": {"walk": True}}}})
    with pytest.raises(ValueError):
        zones.load_zones({
            "x": {"name": "x", "x": 0, "y": 0, "adjacent": {"y": {"walk": True, "see": True}}},
            "y": {"name": "y", "x": 1, "y": 0, "adjacent": {"x": {"walk": False, "see": True}}},
        })
    zones.load_zones(MAP)   # restore


def test_see_hops_walk_chain_and_see_only_edge():
    assert zones.see_hops("a", "a") == 0
    assert zones.see_hops("a", "b") == 1
    assert zones.see_hops("a", "e") == 4          # a-b-c-d-e
    assert zones.see_hops("a", "f") == 1          # see-only edge: sightline without a walk route
    assert "f" not in zones.walk_neighbors("a")   # ...and no walking through the windscreen
    assert zones.see_hops("d", "g") is None       # muffled hatch passes sound, not sight


def test_sound_hops_prices_muffle_at_two():
    assert zones.sound_hops("d", "g") == 2        # one muffled edge = 2
    assert zones.sound_hops("c", "g") == 3        # c-d (1) + muffled d-g (2)


def test_none_and_unknown_zones_are_safe():
    assert zones.see_hops(None, "a") is None
    assert zones.see_hops("a", "stale_id") is None
    assert zones.get("stale_id") is None and zones.get(None) is None


# --- direction ----------------------------------------------------------------

def test_compass_covers_all_eight_points():
    got = [direction.compass(b) for b in (0, 45, 90, 135, 180, 225, 270, 315)]
    assert got == ["north", "northeast", "east", "southeast",
                   "south", "southwest", "west", "northwest"]


def test_phrase_direction_and_slope():
    assert direction.phrase("a", "e") == "to the north and upslope"     # Δelev +2
    assert direction.phrase("e", "a") == "to the south and downslope"
    assert direction.phrase("a", "a") == "" and direction.phrase("a", None) == ""


# --- perception bands -----------------------------------------------------------

def test_visual_band_ladder_and_one_zone_compat():
    assert perception.visual_band("a", "a") is PerceptionBand.SAME_ZONE
    assert perception.visual_band("a", "b") is PerceptionBand.ADJACENT_ZONE
    assert perception.visual_band("a", "c") is PerceptionBand.NEAR_VISIBLE
    assert perception.visual_band("a", "d") is PerceptionBand.DISTANT_VISIBLE
    assert perception.visual_band("a", "e") is PerceptionBand.BARELY_VISIBLE
    assert perception.visual_band("d", "g") is PerceptionBand.OUT_OF_SIGHT
    # THE ONE-ZONE COMPAT RULE: no zone data -> SAME_ZONE (a zone-less world is one zone)
    assert perception.visual_band(None, "a") is PerceptionBand.SAME_ZONE
    assert perception.visual_band("a", None) is PerceptionBand.SAME_ZONE


def test_weather_steps_collapse_bands():
    assert perception.visual_band("a", "c", weather="steady_snow") is PerceptionBand.DISTANT_VISIBLE
    assert perception.visual_band("a", "d", weather="heavy_snow") is PerceptionBand.OUT_OF_SIGHT


def test_perceive_composes_the_axes():
    r = perception.perceive("a", "b", loudness=0.35)          # say / knife-work, adjacent
    assert r.band is PerceptionBand.ADJACENT_ZONE and r.visible and r.audible
    assert not r.reachable                                     # visible ≠ manipulable (§17)
    assert r.direction_phrase == "to the north"
    r2 = perception.perceive("d", "g", loudness=0.6)           # hatch: heard, unseen
    assert r2.band is PerceptionBand.AUDIBLE_ONLY and not r2.visible and r2.audible
    r3 = perception.perceive("d", "g", loudness=0.15)          # a whisper doesn't carry through
    assert r3.band is PerceptionBand.OUT_OF_SIGHT and not r3.audible
    r4 = perception.perceive("a", "a")
    assert r4.band is PerceptionBand.SAME_ZONE and r4.reachable and r4.direction_phrase == ""


def test_speech_ranges_and_whiteout():
    assert sound.reach_hops(sound.SPEECH_LOUDNESS["whisper"]) == 0
    assert sound.reach_hops(sound.SPEECH_LOUDNESS["say"]) == 1
    assert sound.reach_hops(sound.SPEECH_LOUDNESS["call"]) == 2
    assert sound.reach_hops(sound.SPEECH_LOUDNESS["shout"]) == 3
    # whiteout collapses a say to same-zone only (clamped: the same zone always hears)
    assert sound.audible(sound.SPEECH_LOUDNESS["say"], 1, weather="whiteout") is False
    assert sound.audible(sound.SPEECH_LOUDNESS["say"], 0, weather="whiteout") is True
