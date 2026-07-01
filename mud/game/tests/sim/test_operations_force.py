"""Tier-1: the force operations — tear / break / bend (functions-first, D-series). Pure fixtures.

Each success asserts the systemic outcome AND that the effects conserve mass (the ledger agrees), so a
new operation can never silently mint matter. Uses the real scenario responses so narration is exercised.
"""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.conservation.ledger import check
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Part, Resolution
from world.sim.materials import load_materials
from world.sim.operations.handlers import bend, break_op, tear

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


def _seat():
    return EntityState(id="seat", name="aircraft seat", materials=["steel"], mass_g=5000,
                       state={"ident": "11B"},
                       parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",)),
                              Part("belt", "nylon_webbing", 150, "bolted"),
                              Part("bolt", "steel", 30, "bolted")])


def _multitool():
    return EntityState(id="multitool", name="multitool", materials=["steel"], mass_g=150,
                       state={"edge": 0.8, "leverage": 0.5})


def _conserves(world, r):
    assert check(world, list(r.effects)).ok, "effects must balance in the conservation ledger"


# --- tear --------------------------------------------------------------------

def test_tear_frees_stitched_part_by_hand():
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("seat", "cover"))  # no tool — bare hands
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:tear:free"
    created = next(e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT)
    assert created.args["mass_g"] == 200
    _conserves(w, r)


def test_tear_standalone_fabric_into_strips_conserves():
    w = FakeWorld([EntityState(id="rag", name="rag", materials=["synthetic_fabric"], mass_g=101)])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("rag"))
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:tear:strips"
    masses = [e.args["mass_g"] for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert sum(masses) == 101 and len(masses) == 2   # split, nothing lost
    _conserves(w, r)


def test_tear_tough_webbing_redirects():
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("seat", "belt"))  # nylon webbing: high tear-res
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:tear:too_tough"
    assert not r.effects


def test_tear_liquid_not_applicable():
    w = FakeWorld([EntityState(id="pool", name="puddle", materials=["water"], mass_g=500)])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("pool"))
    assert tear.resolve_tear(a, w, MATS) is None   # no tear axis → resolver redirects


# --- break -------------------------------------------------------------------

def test_break_brittle_glass_shatters_and_conserves():
    w = FakeWorld([EntityState(id="bottle", name="bottle", materials=["glass"], mass_g=400)])
    a = ActionAttempt(actor="p", verb="break", X=NounRef("bottle"))
    r = break_op.resolve_break(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:break:shatter"
    masses = [e.args["mass_g"] for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert sum(masses) == 400 and len(masses) == 3   # shards sum to the whole
    _conserves(w, r)


def test_break_wood_snaps_with_leverage():
    w = FakeWorld([EntityState(id="plank", name="plank", materials=["wood"], mass_g=600), _multitool()])
    a = ActionAttempt(actor="p", verb="break", X=NounRef("plank"), tool=NounRef("multitool"))
    r = break_op.resolve_break(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:break:snap"
    _conserves(w, r)


def test_break_metal_bolt_too_tough():
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="break", X=NounRef("seat", "bolt"))
    r = break_op.resolve_break(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:break:too_tough"


def test_break_soft_fabric_not_applicable():
    w = FakeWorld([EntityState(id="rag", name="rag", materials=["synthetic_fabric"], mass_g=100)])
    a = ActionAttempt(actor="p", verb="break", X=NounRef("rag"))
    assert break_op.resolve_break(a, w, MATS) is None


# --- bend --------------------------------------------------------------------

def test_bend_ductile_wire_takes_a_shape():
    w = FakeWorld([EntityState(id="wire", name="coil of wire", materials=["copper_wire"], mass_g=50)])
    a = ActionAttempt(actor="p", verb="bend", X=NounRef("wire"))
    r = bend.resolve_bend(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:bend:shaped"
    eff = r.effects[0]
    assert eff.kind == EffectKind.SET_ATTR and eff.args == {"key": "shape", "value": "bent"}
    _conserves(w, r)   # state change → no mass moved


def test_bend_steel_too_stiff():
    w = FakeWorld([EntityState(id="bar", name="steel bar", materials=["steel"], mass_g=900)])
    a = ActionAttempt(actor="p", verb="bend", X=NounRef("bar"))
    r = bend.resolve_bend(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:bend:too_stiff"


def test_bend_fabric_not_applicable():
    w = FakeWorld([EntityState(id="rag", name="rag", materials=["synthetic_fabric"], mass_g=100)])
    a = ActionAttempt(actor="p", verb="bend", X=NounRef("rag"))
    assert bend.resolve_bend(a, w, MATS) is None   # a pure fabric just flops
