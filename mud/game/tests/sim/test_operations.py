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
            Part(id="cushion", material="foam", mass_g=800, attachment="clipped",
                 outputs_when_removed=("loose_foam",)),
            Part(id="shell", material="plastic", mass_g=400, attachment="fixed"),
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
        # {tool} arrives PRE-ARTICLED via tool_phrase(): "the multitool" / "your bare hands".
        # Templates never write their own article before it; verbs on {tool} are number-invariant.
        "cut.free": "You work {tool} through the {target}'s {part}; it comes free — {output}.",
        "cut.too_dull": "You press hard, but {tool} won't bite into the {target}.",
        "cut.hack_out": "You hack the {part} out in ragged pieces — {output}s. {residue}",
        "cut.integral": "No seam — the {part} is {why}.",
        "cut.divide": "You cut the {target} into two pieces.",
        "pry.no_purchase": "Nothing to lever — the {part} is {why}.",
        "hint.sibling": "The {sibling}, though, is only {sibling_phrase}.",
        "attachment.explain.fixed": "part of the thing itself",
        "attachment.explain.stitched": "hanging by stitching",
        "attachment.explain._": "{attachment} fast",
        "attachment.hint.stitched": "held by stitching",
        "attachment.hint.clipped": "snapped into a frame",
        "attachment.hint._": "{attachment}",
        "attachment.residue.clipped": "The crushed clips stay on the frame.",
        "attachment.residue._": "Whatever held it stays behind, wrecked.",
        "burn.success": "The {target} catches and burns down to ash, {smoke} curling up.",
        "burn.no_flame": "You've nothing to light the {target} with.",
        "burn.wont_catch": "The {target} refuses to catch.",
        "pry.free": "You lever {tool} under the {part} and it pops free — {output}.",
        "pry.no_leverage": "You strain, but {tool} can't shift the {part}; you need more leverage.",
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


def test_cut_bolted_panel_hacks_out_scraps():
    # DR-05a: the blade beats the plastic but not the bolts — destructive extraction, not refusal
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "panel"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:cut:hack_out"
    made = [e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert {e.args["template"] for e in made} == {"plastic_scrap"}
    assert sum(e.args["mass_g"] for e in made) == 120 and len(made) == 3


def test_cut_clipped_cushion_hacks_out_scraps_conserving_mass():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cushion"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:cut:hack_out"
    kinds = [e.kind for e in r.effects]
    assert EffectKind.REMOVE_PART in kinds and EffectKind.SET_ATTR in kinds  # residue is recorded
    made = [e for e in r.effects if e.kind == EffectKind.CREATE_OBJECT]
    assert {e.args["template"] for e in made} == {"foam_scrap"}
    assert sum(e.args["mass_g"] for e in made) == 800
    assert "crushed clips" in r.narration


def test_cut_fixed_part_explains_integral_and_hints_sibling():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "shell"), tool=NounRef("multitool"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:integral"
    assert not r.effects
    assert "part of the thing itself" in r.narration
    assert "cover" in r.narration and "held by stitching" in r.narration  # the one near-miss


def test_cut_dull_tool_still_too_dull_before_attachment_logic():
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cushion"))  # bare hands, clipped foam
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:cut:too_dull"


def test_tool_phrase_is_grammatical_for_bare_hands_and_named_tools():
    # bare hands (no WITH clause): plural-safe phrase, never "the your bare hands"
    a = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"))
    r = cut.resolve_cut(a, _world(), MATS)
    assert r.tier == "op:cut:too_dull"
    assert "your bare hands" in r.narration and "the your" not in r.narration
    # a named tool arrives pre-articled: "the multitool"
    b = ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "bolt"), tool=NounRef("multitool"))
    r2 = cut.resolve_cut(b, _world(), MATS)
    assert r2.tier == "op:cut:too_dull" and "the multitool" in r2.narration


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


def test_pry_stitched_cover_explains_no_purchase_and_hints_sibling():
    a = ActionAttempt(actor="p", verb="pry", X=NounRef("seat", "cover"), tool=NounRef("multitool"))
    r = pry.resolve_pry(a, _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:pry:no_purchase"
    assert "hanging by stitching" in r.narration
    # leverage 0.5 pops a clip (0.3) but not a bolt (0.8): the hint must be the latch, not the panel
    assert "latch" in r.narration and "panel" not in r.narration


def test_pry_hint_skips_siblings_beyond_the_tool():
    a = ActionAttempt(actor="p", verb="pry", X=NounRef("seat", "cover"))  # bare hands: leverage 0.0
    r = pry.resolve_pry(a, _world(), MATS)
    assert r.tier == "op:pry:no_purchase"
    assert "though" not in r.narration  # no sibling is feasible bare-handed → no hint at all


def test_sibling_hint_first_match_and_none_when_nothing_works():
    from world.sim.operations._helpers import sibling_hint
    seat = _seat()
    cover = seat.parts[0]
    hit = sibling_hint(seat, cover, lambda p: p.attachment == "clipped")
    assert hit is not None and hit.id == "latch"  # first clipped sibling in parts order
    assert sibling_hint(seat, cover, lambda p: False) is None


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
