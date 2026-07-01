"""Tier-1: the conservation ledger (DR-11) — mass balances, sink monotonic, bugs rejected (P1.3)."""
import pytest

from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.sim import effects, narrator
from world.sim.conservation.ledger import EnvironmentSink, check
from world.sim.contracts import ActionAttempt, EntityState, NounRef, Part
from world.sim.materials import load_materials
from world.sim.operations.handlers import burn, cut

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


def test_freeing_a_part_conserves_exactly():
    seat = EntityState(id="seat", name="seat", mass_g=5000,
                       parts=[Part(id="cover", material="synthetic_fabric", mass_g=200, attachment="stitched")])
    eff = [effects.remove_part("seat", "cover"),
           effects.create_object("loose_fabric", "seat:cover:loose", {"mass_g": 200, "provenance": ["cut"]})]
    v = check(FakeWorld([seat]), eff)
    assert v.ok and v.sink_delta["mass_g"] == 0


def test_burning_sinks_the_lost_mass():
    tinder = EntityState(id="tinder", name="tinder", materials=["dry_grass"], mass_g=40)
    eff = [effects.consume("tinder"),
           effects.create_object("ash", "tinder:ash:loose", {"mass_g": 6, "provenance": ["burn"]})]
    v = check(FakeWorld([tinder]), eff)
    assert v.ok and v.sink_delta["mass_g"] == 34   # 40 removed - 6 ash = 34 to smoke/heat


def test_mass_from_nothing_is_rejected():
    v = check(FakeWorld([]), [effects.create_object("gold", "g", {"mass_g": 100, "provenance": ["x"]})])
    assert not v.ok and "nothing" in v.reason


def test_created_object_needs_provenance():
    seat = EntityState(id="seat", name="seat", mass_g=200)
    eff = [effects.consume("seat"), effects.create_object("piece", "p", {"mass_g": 200})]
    v = check(FakeWorld([seat]), eff)
    assert not v.ok and "provenance" in v.reason


def test_unknown_part_is_rejected():
    seat = EntityState(id="seat", name="seat", mass_g=100)
    v = check(FakeWorld([seat]), [effects.remove_part("seat", "ghost")])
    assert not v.ok and "no part" in v.reason


def test_environment_sink_is_monotonic():
    s = EnvironmentSink()
    s.absorb(34)
    s.absorb(6)
    assert s.mass_g == 40
    with pytest.raises(ValueError):
        s.absorb(-1)


# --- the operations produce ledger-valid effects (P1.2 × P1.3) ---

def test_cut_handler_output_balances():
    narrator.load_responses({})
    seat = EntityState(id="seat", name="aircraft seat", materials=["steel"], mass_g=5000,
                       parts=[Part(id="cover", material="synthetic_fabric", mass_g=200,
                                   attachment="stitched", outputs_when_removed=("loose_fabric",))])
    tool = EntityState(id="multitool", name="multitool", mass_g=150, state={"edge": 0.8})
    w = FakeWorld([seat, tool])
    r = cut.resolve_cut(ActionAttempt(actor="p", verb="cut", X=NounRef("seat", "cover"),
                                      tool=NounRef("multitool")), w, MATS)
    v = check(w, list(r.effects))
    assert v.ok and v.sink_delta["mass_g"] == 0


def test_burn_handler_output_balances():
    narrator.load_responses({})
    tinder = EntityState(id="tinder", name="dry grass", materials=["dry_grass"], mass_g=40)
    lighter = EntityState(id="lighter", name="lighter", mass_g=20, tags=["ignition"])
    w = FakeWorld([tinder, lighter])
    r = burn.resolve_burn(ActionAttempt(actor="p", verb="burn", X=NounRef("tinder"),
                                        tool=NounRef("lighter")), w, MATS)
    v = check(w, list(r.effects))
    assert v.ok and v.sink_delta["mass_g"] == 40 - int(40 * 0.15)   # 34 to the sink
