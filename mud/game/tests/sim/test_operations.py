"""Tier-1: operation handlers (functions-first) over pure fixtures — cut (D12) + examine (P1.2)."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim import narrator
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Part, Resolution
from world.sim.materials import load_materials
from world.sim.operations.handlers import burn, cut, examine, pry
from world.sim.operations.registry import VERB_TO_OP, handler_for

MATS = load_materials(MATERIAL_TABLE)

# A minimal WorldView (satisfies the Protocol: get / reachable / in_zone / seed_state).
class FakeWorld:
    seed_state = 0
    def __init__(self, entities):
        self._e = {e.id: e for e in entities}
    def get(self, eid):
        return self._e.get(eid)
    def reachable(self, actor_id):
        return list(self._e)
    def in_zone(self, zone):
        return list(self._e)


def _seat():
    return EntityState(
        id="seat", name="aircraft seat", materials=["steel"], mass_g=5000,
        state={"ident": "11B"},
        parts=[
            Part(id="cover", material="synthetic_fabric", mass_g=200, attachment="stitched",
                 outputs_when_removed=("loose_fabric",)),
            Part(id="panel", material="plastic", mass_g=120, attachment="bolted"),
            Part(id="bolt", material="steel", mass_g=30, attachment="bolted"),
            Part(id="latch", material="aluminum", mass_g=60, attachment="clipped",
                 outputs_when_removed=("loose_latch",)),
        ],
    )


def _multitool():
    return EntityState(id="multitool", name="multitool", materials=["steel"], mass_g=150,
                       state={"edge": 0.8, "leverage": 0.5})


def _tinder():
    return EntityState(id="tinder", name="dry grass", materials=["dry_grass"], mass_g=40)


def _lighter():
    return EntityState(id="lighter", name="lighter", materials=["plastic"], mass_g=20, tags=["ignition"])


def _world():
    return FakeWorld([_seat(), _multitool(), _tinder(), _lighter()])


def setup_module(_):
    narrator.load_responses({
        "cut.free": "You work the {tool} through the {target}'s {part}; it comes free — {output}.",
        "cut.too_dull": "The {tool} just skates off the {target}.",
        "cut.slash_fixed": "You slash the {part}, but it's {attachment} — you'd need to unbolt it.",
        "cut.divide": "You cut the {target} into two pieces.",
        "burn.success": "The {target} catches and burns down to ash, {smoke} curling up.",
        "burn.no_flame": "You've nothing to light the {target} with.",
        "burn.wont_catch": "The {target} refuses to catch.",
        "pry.free": "You lever the {tool} under the {part} and it pops free — {output}.",
        "pry.no_leverage": "The {tool} can't shift the {part}; you need more leverage.",
        "__fallback__": "It gives way.",
    })


def test_cut_stitched_part_frees_it():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:cut:free"
    kinds = [e.kind for e in r.effects]
    assert EffectKind.REMOVE_PART in kinds and EffectKind.CREATE_OBJECT in kinds
    # mass is conserved: the freed object carries the part's grams
    created = next(e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT)
    assert created.args["mass_g"] == 200
    assert "comes free" in r.narration


def test_cut_steel_bolt_too_dull():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "bolt"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:too_dull"
    assert not r.effects


def test_cut_cuttable_but_bolted_slashes_not_frees():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "panel"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:slash_fixed"
    assert "unbolt" in r.narration


def test_cut_liquid_not_applicable():
    world = FakeWorld([EntityState(id="pool", name="puddle", materials=["water"], mass_g=1000)])
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("pool"), tool=NounRef("multitool"))
    assert cut.resolve_cut(a, world, MATS) is None  # water has no cut_resistance → resolver redirects


def test_examine_lists_parts_with_ids_and_ident():
    a = ActionAttempt(actor="p", verb="examine", X=NounRef("seat"))
    r = examine.resolve_examine(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS
    assert "[11B]" in r.narration
    for pid in ("cover", "panel", "bolt"):
        assert pid in r.narration, f"examine should list part id {pid}"


def test_pry_clipped_part_frees_it():
    a = ActionAttempt(actor="p", verb="pry", X=NounRef("seat", "latch"), tool=NounRef("multitool"))
    r = pry.resolve_pry(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:pry:free"
    created = next(e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT)
    assert created.args["mass_g"] == 60 and "pops free" in r.narration


def test_pry_steel_bolt_no_leverage():
    a = ActionAttempt(actor="p", verb="pry", X=NounRef("seat", "bolt"), tool=NounRef("multitool"))
    r = pry.resolve_pry(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:pry:no_leverage"


def test_pry_non_pryable_not_applicable():
    a = ActionAttempt(actor="p", verb="pry", X=NounRef("seat", "cover"), tool=NounRef("multitool"))
    assert pry.resolve_pry(a, _world(), MATS) is None  # stitched, not pryable → resolver redirects


def test_burn_flammable_with_flame():
    a = ActionAttempt(actor="p", verb="burn", X=NounRef("tinder"), tool=NounRef("lighter"))
    r = burn.resolve_burn(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:burn:success"
    kinds = [e.kind for e in r.effects]
    assert EffectKind.CONSUME in kinds and EffectKind.CREATE_OBJECT in kinds  # consumed → ash
    assert "ash" in r.narration


def test_burn_no_flame_redirects():
    a = ActionAttempt(actor="p", verb="burn", X=NounRef("tinder"), tool=NounRef("multitool"))
    r = burn.resolve_burn(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:burn:no_flame"


def test_burn_steel_not_applicable():
    a = ActionAttempt(actor="p", verb="burn", X=NounRef("seat", "bolt"), tool=NounRef("lighter"))
    assert burn.resolve_burn(a, _world(), MATS) is None  # steel won't burn → resolver redirects


def test_registry_synonyms_map_to_canonical_verbs():
    assert VERB_TO_OP["saw"] == "cut" and VERB_TO_OP["slice"] == "cut"
    assert VERB_TO_OP["inspect"] == "examine"
    assert VERB_TO_OP["ignite"] == "burn" and VERB_TO_OP["lever"] == "pry"
    assert handler_for("saw") is cut.resolve_cut
    assert handler_for("nonsense") is None
