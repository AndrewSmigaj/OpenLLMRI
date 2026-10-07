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
                              Part("bolt", "steel", 30, "bolted"),
                              Part("cushion", "foam", 800, "clipped", ("loose_foam",)),
                              Part("liner", "synthetic_fabric", 100, "fixed")])


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
    # derived names read material-first ("synthetic fabric strip", never "strip synthetic fabric")
    templates = [e.args["template"] for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert templates == ["synthetic_fabric_strip", "synthetic_fabric_strip"]
    _conserves(w, r)


def test_tear_tough_webbing_redirects():
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("seat", "belt"))  # nylon webbing: high tear-res
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:tear:too_tough"
    assert not r.effects


def test_tear_clipped_foam_rips_out_scraps_conserving_mass():
    # DR-05a: bare hands beat the foam but not the clips — destructive extraction, mass conserved
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("seat", "cushion"))
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:tear:rip_out"
    made = [e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert {e.args["template"] for e in made} == {"foam_scrap"}
    assert sum(e.args["mass_g"] for e in made) == 800 and len(made) == 3
    assert "crushed clips" in r.narration
    _conserves(w, r)


def test_tear_fixed_part_explains_integral():
    w = FakeWorld([_seat()])
    a = ActionAttempt(actor="p", verb="tear", X=NounRef("seat", "liner"))
    r = tear.resolve_tear(a, w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:tear:integral"
    assert not r.effects
    assert "part of the thing itself" in r.narration
    assert "cover" in r.narration  # the tearable stitched sibling gets the one near-miss


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
    # derived names read material-first ("glass shard", never "shard glass")
    templates = {e.args["template"] for e in r.effects if e.kind == EffectKind.CREATE_OBJECT}
    assert templates == {"glass_shard"}
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


# --- DR-26 closure: the example chain — break a bottle, cut with the shard, burn the cover ------------

def _mint(effect, name=None):
    """Build the EntityState a CREATE_OBJECT effect would produce (what the shell's apply() writes)."""
    a = effect.args
    st = {"form": a["form"]} if a.get("form") else {}
    return EntityState(id=effect.target_id, name=(name or a["template"].replace("_", " ")),
                       materials=[a["material"]], mass_g=int(a["mass_g"]), state=st,
                       provenance=list(a.get("provenance", [])))


def test_closure_chain_break_bottle_cut_cover_with_shard_burn_it():
    from world.sim.operations.handlers import burn, cut
    bottle = EntityState(id="bottle", name="whisky bottle", materials=["glass"], mass_g=500)
    seat = _seat()
    lighter = EntityState(id="lighter", name="lighter", materials=["plastic"], mass_g=20,
                          state={"ignition": True})
    w = FakeWorld([bottle, seat, lighter])

    # 1. break → three shards, each carrying its FORM
    r1 = break_op.resolve_break(ActionAttempt(actor="p", verb="break", X=NounRef("bottle")), w, MATS)
    assert r1.resolution == Resolution.SUCCESS and r1.tier == "op:break:shatter"
    _conserves(w, r1)
    mints = [e for e in r1.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert len(mints) == 3 and all(e.args["form"] == "shard" for e in mints)
    shard = _mint(mints[0])
    assert shard.state["form"] == "shard"

    # 2. cut the cover off the seat WITH THE SHARD — the closure: a minted thing is a real tool
    w2 = FakeWorld([shard, seat, lighter])
    r2 = cut.resolve_cut(ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"),
                                       tool=NounRef(shard.id)), w2, MATS)
    assert r2.resolution == Resolution.SUCCESS, r2.narration
    assert r2.tier == "op:cut:free"
    _conserves(w2, r2)
    cover_mint = [e for e in r2.effects if e.kind == EffectKind.CREATE_OBJECT][0]
    assert cover_mint.args["form"] == "sheet"                # loose_fabric → a sheet (a cover, a wrap)
    cover = _mint(cover_mint)

    # 3. burn the freed cover with the lighter → ash (form) + the rest to the sink
    w3 = FakeWorld([cover, lighter])
    r3 = burn.resolve_burn(ActionAttempt(actor="p", verb="burn", X=NounRef(cover.id),
                                         tool=NounRef("lighter")), w3, MATS)
    assert r3.resolution == Resolution.SUCCESS and r3.tier == "op:burn:success"
    _conserves(w3, r3)
    ash = [e for e in r3.effects if e.kind == EffectKind.CREATE_OBJECT][0]
    assert ash.args["form"] == "ash"


def test_shard_still_cannot_cut_steel_and_a_foam_lump_is_no_blade():
    from world.sim.operations.handlers import cut
    shard = EntityState(id="shard", name="glass shard", materials=["glass"], mass_g=166,
                        state={"form": "shard"})
    lump = EntityState(id="lump", name="foam lump", materials=["foam"], mass_g=166, state={"form": "shard"})
    seat = _seat()
    w = FakeWorld([shard, lump, seat])
    r = cut.resolve_cut(ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "bolt"), tool=NounRef("shard")), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:too_dull"
    r = cut.resolve_cut(ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"), tool=NounRef("lump")), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:too_dull"


def test_a_torn_strip_ties_because_it_is_cordage_by_form():
    from world.sim.operations.handlers import tie
    strip = EntityState(id="strip", name="synthetic fabric strip", materials=["synthetic_fabric"], mass_g=40,
                        state={"form": "strip"})
    frame = EntityState(id="frame", name="seat frame", materials=["steel"], mass_g=3000)
    w = FakeWorld([strip, frame])
    r = tie.resolve_tie(ActionAttempt(actor="p", verb="tie", X=NounRef("strip"), relation="to",
                                      Y=(NounRef("frame"),)), w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:tie:knot"
