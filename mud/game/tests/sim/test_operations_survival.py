"""Tier-1: the survival operations — tie / wrap / drink. Pure fixtures + conservation checks."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.conservation.ledger import check
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Resolution
from world.sim.materials import load_materials
from world.sim.operations.handlers import drink, tie, wrap

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


def _rope():
    return EntityState(id="rope", name="length of webbing", materials=["nylon_webbing"], mass_g=150)


def _frame():
    return EntityState(id="frame", name="frame", materials=["steel"], mass_g=1000)


def _conserves(world, r):
    assert check(world, list(r.effects)).ok


# --- tie ---------------------------------------------------------------------

def test_tie_cordage_to_an_anchor():
    w = FakeWorld([_rope(), _frame()])
    a = ActionAttempt(actor="p", verb="tie", X=NounRef("rope"), relation="to", Y=(NounRef("frame"),))
    r = tie.resolve_tie(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:tie:knot"
    keys = {e.args["key"] for e in r.effects if e.kind == EffectKind.SET_ATTR}
    assert {"tied_to", "secured"} <= keys
    _conserves(w, r)   # state only, no mass moved


def test_tie_using_cordage_as_the_tool():
    w = FakeWorld([_rope(), _frame()])
    a = ActionAttempt(actor="p", verb="tie", X=NounRef("frame"), tool=NounRef("rope"))
    assert tie.resolve_tie(a, w, MATS).tier == "op:tie:knot"


def test_tie_without_an_anchor_redirects():
    w = FakeWorld([_rope()])
    a = ActionAttempt(actor="p", verb="tie", X=NounRef("rope"))
    assert tie.resolve_tie(a, w, MATS).tier == "op:tie:no_anchor"


def test_tie_nothing_cordage_not_applicable():
    w = FakeWorld([_frame()])
    a = ActionAttempt(actor="p", verb="tie", X=NounRef("frame"))
    assert tie.resolve_tie(a, w, MATS) is None


# --- wrap --------------------------------------------------------------------

def test_wrap_fabric_around_a_target():
    w = FakeWorld([EntityState(id="cloth", name="cloth", materials=["synthetic_fabric"], mass_g=100),
                   EntityState(id="pilot", name="the pilot", materials=["flesh"], mass_g=78000)])
    a = ActionAttempt(actor="p", verb="wrap", X=NounRef("cloth"), relation="around", Y=(NounRef("pilot"),))
    r = wrap.resolve_wrap(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:wrap:wrapped"
    assert any(e.args == {"key": "wrapped", "value": True} for e in r.effects)
    _conserves(w, r)


def test_wrap_insulating_material_marks_insulated():
    w = FakeWorld([EntityState(id="pad", name="foam pad", materials=["foam"], mass_g=300), _frame()])
    a = ActionAttempt(actor="p", verb="wrap", X=NounRef("pad"), relation="around", Y=(NounRef("frame"),))
    r = wrap.resolve_wrap(a, w, MATS)
    keys = {e.args["key"] for e in r.effects}
    assert {"wrapped", "insulated"} <= keys and r.tier == "op:wrap:wrapped"


def test_wrap_target_with_wrapper_as_tool():
    w = FakeWorld([EntityState(id="cloth", name="cloth", materials=["synthetic_fabric"], mass_g=100),
                   EntityState(id="pilot", name="the pilot", materials=["flesh"], mass_g=78000)])
    a = ActionAttempt(actor="p", verb="wrap", X=NounRef("pilot"), tool=NounRef("cloth"))
    assert wrap.resolve_wrap(a, w, MATS).tier == "op:wrap:wrapped"


def test_wrap_without_a_target_redirects():
    w = FakeWorld([EntityState(id="cloth", name="cloth", materials=["synthetic_fabric"], mass_g=100)])
    a = ActionAttempt(actor="p", verb="wrap", X=NounRef("cloth"))
    assert wrap.resolve_wrap(a, w, MATS).tier == "op:wrap:no_target"


def test_wrap_nothing_wrappable_not_applicable():
    w = FakeWorld([_frame()])
    a = ActionAttempt(actor="p", verb="wrap", X=NounRef("frame"))
    assert wrap.resolve_wrap(a, w, MATS) is None


# --- drink -------------------------------------------------------------------

def test_drink_water_slakes_and_conserves():
    w = FakeWorld([EntityState(id="water", name="water", materials=["water"], mass_g=500)])
    a = ActionAttempt(actor="p", verb="drink", X=NounRef("water"))
    r = drink.resolve_drink(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:drink:drink"
    assert r.effects[0].kind == EffectKind.CONSUME
    _conserves(w, r)


def test_drink_frozen_water_says_melt_first():
    w = FakeWorld([EntityState(id="snow", name="snow", materials=["snow"], mass_g=200)])
    a = ActionAttempt(actor="p", verb="drink", X=NounRef("snow"))
    assert drink.resolve_drink(a, w, MATS).tier == "op:drink:frozen"


def test_drink_non_potable_not_applicable():
    w = FakeWorld([_frame()])
    a = ActionAttempt(actor="p", verb="drink", X=NounRef("frame"))
    assert drink.resolve_drink(a, w, MATS) is None
