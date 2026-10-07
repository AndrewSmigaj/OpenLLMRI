"""Tier-1: the resolver tiers + coarse redirect + wall-sensor (DR-09, P1.4)."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim import narrator
from world.sim.contracts import ActionAttempt, ActionResult, EntityState, NounRef, Part, Resolution
from world.sim.materials import load_materials
from world.sim.resolver import resolve
from world.sim.resolver.wall_sensor import gap_record

MATS = load_materials(MATERIAL_TABLE)


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


def _world():
    seat = EntityState(id="seat", name="seat", materials=["steel"], mass_g=5000, state={"ident": "11B"},
                       parts=[Part(id="cover", material="synthetic_fabric", mass_g=200,
                                   attachment="stitched", outputs_when_removed=("loose_fabric",))])
    tool = EntityState(id="multitool", name="multitool", mass_g=150, state={"edge": 0.8, "leverage": 0.5})
    pool = EntityState(id="pool", name="puddle", materials=["water"], mass_g=1000)
    return FakeWorld([seat, tool, pool])


def setup_module(_):
    narrator.load_responses({"cut.free": "You cut the {part} free — {output}.", "__fallback__": "x"})


def test_tier3_dispatches_to_handler():
    r = resolve(ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"), tool=NounRef("multitool")),
                _world(), MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:cut:free"


def test_handler_none_falls_through_to_redirect():
    r = resolve(ActionAttempt(actor="p", verb="cut", X=NounRef("pool"), tool=NounRef("multitool")),
                _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "redirect:generic"


def test_redirect_names_plausible_verbs_for_material():
    r = resolve(ActionAttempt(actor="p", verb="polish", X=NounRef("seat", "cover")), _world(), MATS)
    assert r.resolution == Resolution.REDIRECT
    assert "cut" in r.narration or "burn" in r.narration


def test_missing_target_redirects_informatively():
    r = resolve(ActionAttempt(actor="p", verb="cut", X=NounRef("ghost")), _world(), MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "redirect:no_target"


def test_every_attempt_resolves_never_none():
    w = _world()
    for verb in ("cut", "burn", "pry", "polish", "sing"):
        for tgt in ("seat", "pool", "multitool", "ghost"):
            r = resolve(ActionAttempt(actor="p", verb=verb, X=NounRef(tgt), tool=NounRef("multitool")),
                        w, MATS)
            assert r is not None
            assert r.resolution in (Resolution.SUCCESS, Resolution.PARTIAL, Resolution.REDIRECT)


def test_authored_tier1_wins_over_operation():
    def radio_rule(attempt, world, materials):
        return ActionResult(Resolution.SUCCESS, narration="The radio hisses static.", tier="authored:radio")
    w = FakeWorld([EntityState(id="radio", name="radio", mass_g=500)])
    r = resolve(ActionAttempt(actor="p", verb="examine", X=NounRef("radio")), w, MATS,
                authored={"radio": radio_rule})
    assert r.tier == "authored:radio"


def test_wall_sensor_gap_record():
    rec = gap_record(ActionAttempt(actor="p", verb="polish", X=NounRef("seat", "cover"), raw="polish cover"))
    assert rec["verb"] == "polish" and rec["target"] == "seat" and rec["part"] == "cover"
