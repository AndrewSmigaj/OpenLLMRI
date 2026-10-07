"""Tier-1: the DR-24 verbs — take/put, open/close, search/dig — over pure fixtures.

Containment is modeled the way the worldview marshals it: state['in'] on the contained,
state['contents']/['worn'] on the holder. Uses the real scenario RESPONSES (voice exercised)."""
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Resolution
from world.sim.operations.handlers import open_op, search, take

MATS = {}


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


def _ent(id, name, state=None, mass=100, materials=(), parts=()):
    return EntityState(id=id, name=name, materials=list(materials), parts=list(parts), tags=[],
                       mass_g=mass, state=dict(state or {}), provenance=[], owner=None)


def _world():
    return FakeWorld([
        _ent("p1", "Survivor"),
        _ent("duffel", "duffel bag", {"container": True, "contents": ["wool socks", "multitool"]}),
        _ent("socks", "wool socks", {"in": "duffel"}, mass=150),
        _ent("bin", "overhead bin", {"container": True, "open": False, "fixed": True}, mass=2500),
        _ent("jammed_bin", "aft bin", {"container": True, "open": False, "jammed": True,
                                       "fixed": True}, mass=2500),
        _ent("jerrycan", "jerry can", {"sealed": True}, mass=3000, materials=["fuel"]),
        _ent("pilot", "the pilot", {"dead": True, "contents": ["lighter"]}, mass=78000,
             materials=["flesh"]),
        _ent("jacket", "flight jacket", {"worn_by": "pilot"}, mass=1200, materials=["leather"]),
        _ent("held", "chocolate bar", {"in": "p1"}, mass=100),
        _ent("drift", "snowdrift", {"contents": ["leather gloves"], "fixed": True}, mass=4000,
             materials=["snow"]),
        _ent("rag", "rag", {}, mass=100, materials=["synthetic_fabric"]),
    ])


def _a(verb, x=None, relation=None, y=None):
    return ActionAttempt(actor="p1", verb=verb, X=NounRef(x) if x else None, relation=relation,
                         Y=(NounRef(y),) if y else None)


# --- take ----------------------------------------------------------------------

def test_take_loose_transfers_to_actor():
    r = take.resolve_take(_a("take", "rag"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:take:take"
    assert r.effects[-1].kind == EffectKind.TRANSFER and r.effects[-1].args["dest"] == "p1"


def test_take_from_container_names_it():
    r = take.resolve_take(_a("take", "socks", relation="off", y="duffel"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS
    assert "duffel bag" in r.narration


def test_take_already_carried():
    r = take.resolve_take(_a("take", "held"), _world(), MATS)
    assert r.tier == "op:take:already" and not r.effects


def test_take_fixed_and_too_heavy_refuse():
    assert take.resolve_take(_a("take", "bin"), _world(), MATS).tier == "op:take:fixed"
    r = take.resolve_take(_a("take", "pilot"), _world(), MATS)
    assert r.tier == "op:take:too_heavy" and "dead weight" in r.narration


def test_take_strips_a_dead_wearer():
    r = take.resolve_take(_a("take", "jacket"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:take:strip"
    kinds = [e.kind for e in r.effects]
    assert kinds == [EffectKind.SET_ATTR, EffectKind.TRANSFER]     # transfer LAST (DR-24 rule)
    assert "He doesn't mind" in r.narration


def test_take_refuses_a_living_wearer():
    w = _world()
    w._e["pilot"] = _ent("pilot", "the pilot", {"contents": ["lighter"]}, mass=78000)
    r = take.resolve_take(_a("take", "jacket"), w, MATS)
    assert r.tier == "op:take:worn_other"


def test_put_into_and_its_gates():
    r = take.resolve_put(_a("put", "held", relation="into", y="duffel"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.effects[-1].args["dest"] == "duffel"
    assert take.resolve_put(_a("put", "rag", relation="into", y="duffel"),
                            _world(), MATS).tier == "op:put:not_held"
    assert take.resolve_put(_a("put", "held", relation="into", y="bin"),
                            _world(), MATS).tier == "op:put:shut"
    assert take.resolve_put(_a("put", "held", relation="into", y="rag"),
                            _world(), MATS).tier == "op:put:not_container"


# --- open / close ---------------------------------------------------------------

def test_open_container_jammed_and_sealed():
    r = open_op.resolve_open(_a("open", "bin"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.effects[0].args == {"key": "open", "value": True}
    r2 = open_op.resolve_open(_a("open", "jammed_bin"), _world(), MATS)
    assert r2.tier == "op:open:jammed" and "lever" in r2.narration
    r3 = open_op.resolve_open(_a("open", "jerrycan"), _world(), MATS)
    assert r3.tier == "op:open:unseal" and r3.effects[0].args == {"key": "sealed", "value": False}
    assert open_op.resolve_open(_a("open", "rag"), _world(), MATS) is None


def test_close_mirrors():
    w = _world()
    w._e["bin"] = _ent("bin", "overhead bin", {"container": True, "open": True}, mass=2500)
    r = open_op.resolve_close(_a("close", "bin"), w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.effects[0].args["value"] is False
    assert open_op.resolve_close(_a("close", "duffel"), _world(), MATS).tier == "op:close:already"


# --- search / dig ----------------------------------------------------------------

def test_search_names_actual_contents_and_sets_searched():
    r = search.resolve_search(_a("search", "duffel"), _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:search:found"
    assert "wool socks" in r.narration and "multitool" in r.narration
    assert r.effects[0].args == {"key": "searched", "value": True}


def test_frisk_excludes_worn_from_finds():
    r = search.resolve_search(_a("frisk", "pilot"), _world(), MATS)
    assert "lighter" in r.narration and "jacket" not in r.narration


def test_search_again_and_shut():
    w = _world()
    w._e["duffel"] = _ent("duffel", "duffel bag", {"container": True, "searched": True})
    assert search.resolve_search(_a("search", "duffel"), w, MATS).tier == "op:search:again"
    assert search.resolve_search(_a("search", "bin"), _world(), MATS).tier == "op:search:shut"


def test_dig_requires_snow_and_reveals():
    r = search.resolve_dig(_a("dig", "rag"), _world(), MATS)
    assert r.tier == "op:dig:nothing"
    r2 = search.resolve_dig(_a("dig", "drift"), _world(), MATS)
    assert r2.resolution == Resolution.SUCCESS and "leather gloves" in r2.narration
