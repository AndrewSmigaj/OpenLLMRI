"""Tier-1: the fire/water operations — light / melt / pour. Pure fixtures + conservation checks.

Exercises the systemic chain the fun-gate is meant to reward: light the tinder, melt snow off its heat,
pour water to douse a fire. Every effect-producing result must balance in the ledger.
"""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.conservation.ledger import check
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Resolution
from world.sim.materials import load_materials
from world.sim.operations.handlers import light, melt, pour

MATS = load_materials(MATERIAL_TABLE)


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


def _lighter():
    return EntityState(id="lighter", name="lighter", materials=["plastic"], mass_g=20,
                       state={"ignition": True})


def _tinder(lit=False):
    return EntityState(id="tinder", name="dry grass", materials=["dry_grass"], mass_g=40,
                       state={"lit": True} if lit else {})


def _ice():
    return EntityState(id="ice", name="chunk of ice", materials=["ice"], mass_g=300)


def _water():
    return EntityState(id="water", name="water", materials=["water"], mass_g=500)


def _conserves(world, r):
    assert check(world, list(r.effects)).ok


# --- light -------------------------------------------------------------------

def test_light_tinder_with_a_spark_makes_a_fire():
    w = FakeWorld([_tinder(), _lighter()])
    a = ActionAttempt(actor="p", verb="light", X=NounRef("tinder"), tool=NounRef("lighter"))
    r = light.resolve_light(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:light:lit"
    assert r.effects[0].kind == EffectKind.SET_ATTR and r.effects[0].args == {"key": "lit", "value": True}
    _conserves(w, r)


def test_light_without_a_spark_redirects():
    w = FakeWorld([_tinder()])
    a = ActionAttempt(actor="p", verb="light", X=NounRef("tinder"))   # no ignition source
    r = light.resolve_light(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:light:no_spark"


def test_light_already_lit_redirects():
    w = FakeWorld([_tinder(lit=True), _lighter()])
    a = ActionAttempt(actor="p", verb="light", X=NounRef("tinder"), tool=NounRef("lighter"))
    assert light.resolve_light(a, w, MATS).tier == "op:light:already"


def test_light_non_flammable_not_applicable():
    w = FakeWorld([EntityState(id="bolt", name="bolt", materials=["steel"], mass_g=30), _lighter()])
    a = ActionAttempt(actor="p", verb="light", X=NounRef("bolt"), tool=NounRef("lighter"))
    assert light.resolve_light(a, w, MATS) is None


# --- melt --------------------------------------------------------------------

def test_melt_ice_with_flame_conserves_mass():
    w = FakeWorld([_ice(), _lighter()])
    a = ActionAttempt(actor="p", verb="melt", X=NounRef("ice"), tool=NounRef("lighter"))
    r = melt.resolve_melt(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:melt:water"
    created = next(e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT)
    assert created.args["material"] == "water" and created.args["mass_g"] == 300   # ice grams → water grams
    _conserves(w, r)


def test_melt_off_a_nearby_fire_no_tool_needed():
    w = FakeWorld([_ice(), _tinder(lit=True)])            # a lit fire is reachable
    a = ActionAttempt(actor="p", verb="melt", X=NounRef("ice"))
    assert melt.resolve_melt(a, w, MATS).tier == "op:melt:water"


def test_melt_without_heat_redirects():
    w = FakeWorld([_ice()])
    a = ActionAttempt(actor="p", verb="melt", X=NounRef("ice"))
    assert melt.resolve_melt(a, w, MATS).tier == "op:melt:no_heat"


def test_melt_non_frozen_not_applicable():
    w = FakeWorld([_water(), _lighter()])
    a = ActionAttempt(actor="p", verb="melt", X=NounRef("water"), tool=NounRef("lighter"))
    assert melt.resolve_melt(a, w, MATS) is None


# --- pour --------------------------------------------------------------------

def test_pour_water_douses_a_fire_and_conserves():
    w = FakeWorld([_water(), _tinder(lit=True)])
    a = ActionAttempt(actor="p", verb="pour", X=NounRef("water"), relation="on", Y=(NounRef("tinder"),))
    r = pour.resolve_pour(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:pour:douse"
    setattr_e = next(e for e in r.effects if e.kind == EffectKind.SET_ATTR)
    assert setattr_e.args == {"key": "lit", "value": False}
    assert any(e.kind == EffectKind.CONSUME for e in r.effects)     # the water leaves the scene
    _conserves(w, r)


def test_pour_water_on_dry_thing_wets_it():
    w = FakeWorld([_water(), EntityState(id="rag", name="rag", materials=["synthetic_fabric"], mass_g=100)])
    a = ActionAttempt(actor="p", verb="pour", X=NounRef("water"), relation="on", Y=(NounRef("rag"),))
    r = pour.resolve_pour(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:pour:wet"
    _conserves(w, r)


def test_pour_with_no_target_redirects():
    w = FakeWorld([_water()])
    a = ActionAttempt(actor="p", verb="pour", X=NounRef("water"))
    assert pour.resolve_pour(a, w, MATS).tier == "op:pour:no_target"


def test_pour_non_liquid_not_applicable():
    w = FakeWorld([EntityState(id="bolt", name="bolt", materials=["steel"], mass_g=30)])
    a = ActionAttempt(actor="p", verb="pour", X=NounRef("bolt"), relation="on", Y=(NounRef("bolt"),))
    assert pour.resolve_pour(a, w, MATS) is None
