"""Tier-1: clothing & warmth (DR-25) — wearability derived from materials; insulation-grams."""
from world.scenarios.whiteout.content import MATERIALS
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Resolution
from world.sim.operations.handlers import take, wear
from world.sim.systems import warmth


def setup_module(_):
    narrator.load_responses(RESPONSES)


class FakeWorld:
    seed_state = 0
    def __init__(self, ents):
        self._e = {e.id: e for e in ents}
    def get(self, i):
        return self._e.get(i)
    def reachable(self, a):
        return list(self._e)
    def in_zone(self, z):
        return list(self._e)


def _ent(id, name, materials=(), mass=100, state=None):
    return EntityState(id=id, name=name, materials=list(materials), parts=[], tags=[],
                       mass_g=mass, state=dict(state or {}), provenance=[], owner=None)


JACKET = _ent("jacket", "flight jacket", ["leather"], 1200)
BLANKET = _ent("blanket", "wool blanket", ["wool"], 700)
SOCKS = _ent("socks", "wool socks", ["wool"], 150, {"in": "p1"})
BOTTLE = _ent("bottle", "whisky bottle", ["glass"], 500)
SEAT = _ent("seat", "aircraft seat", ["steel"], 5000, {"fixed": True})
WATER = _ent("pool", "meltwater", ["water"], 500)


def test_wearable_is_derived_from_materials():
    assert warmth.wearable(JACKET, MATERIALS)        # leather: fabric+flexible
    assert warmth.wearable(BLANKET, MATERIALS)       # the blanket wears as a cloak
    assert not warmth.wearable(BOTTLE, MATERIALS)    # glass doesn't drape
    assert not warmth.wearable(SEAT, MATERIALS)      # fixtures never wear
    assert not warmth.wearable(WATER, MATERIALS)     # you cannot wear a puddle


def test_insulation_units_scale_with_capped_mass():
    strip = _ent("strip", "wool strip", ["wool"], 100)
    assert warmth.insulation_units(strip, MATERIALS) < warmth.insulation_units(BLANKET, MATERIALS)
    huge = _ent("roll", "wool roll", ["wool"], 30000)
    assert warmth.insulation_units(huge, MATERIALS) == round(0.7 * 3000)   # the mass cap


def test_band_ladder_and_summary():
    assert warmth.warmth_band(0) == "bare to the wind"
    assert warmth.warmth_band(9999).startswith("swaddled")
    line = warmth.worn_summary([JACKET, SOCKS], MATERIALS)
    assert "flight jacket" in line and "wool socks" in line and "You are" in line
    assert "wearing nothing" in warmth.worn_summary([], MATERIALS)


def test_wear_auto_takes_and_sets_worn():
    w = FakeWorld([_ent("p1", "Survivor"), BLANKET])
    a = ActionAttempt(actor="p1", verb="wear", X=NounRef("blanket"))
    r = wear.resolve_wear(a, w, MATERIALS)
    assert r.resolution == Resolution.SUCCESS
    kinds = [e.kind for e in r.effects]
    assert kinds == [EffectKind.SET_ATTR, EffectKind.TRANSFER]     # transfer LAST (DR-24)


def test_wear_refuses_the_unwearable_physically():
    w = FakeWorld([_ent("p1", "Survivor"), BOTTLE])
    r = wear.resolve_wear(ActionAttempt(actor="p1", verb="wear", X=NounRef("bottle")), w, MATERIALS)
    assert r.tier == "op:wear:unwearable" and "doesn't bend around a body" in r.narration


def test_shed_keeps_it_carried():
    worn = _ent("jacket", "flight jacket", ["leather"], 1200, {"in": "p1", "worn_by": "p1"})
    w = FakeWorld([_ent("p1", "Survivor"), worn])
    r = wear.resolve_shed(ActionAttempt(actor="p1", verb="remove", X=NounRef("jacket")),
                          w, MATERIALS)
    assert r.resolution == Resolution.SUCCESS
    assert [e.kind for e in r.effects] == [EffectKind.SET_ATTR]    # no transfer — still in hand


def test_take_off_routes_to_shed():
    worn = _ent("jacket", "flight jacket", ["leather"], 1200, {"in": "p1", "worn_by": "p1"})
    w = FakeWorld([_ent("p1", "Survivor"), worn])
    a = ActionAttempt(actor="p1", verb="take", X=None, relation="off", Y=(NounRef("jacket"),))
    r = take.resolve_take(a, w, MATERIALS)
    assert r.tier == "op:wear:shed" and "take off" in r.narration