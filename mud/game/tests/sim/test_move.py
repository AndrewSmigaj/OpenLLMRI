"""Tier-1: the move operation over the REAL crash-site zone map (DR-13a, §18). Pure fixtures."""
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.scenarios.whiteout.zones import ZONE_TABLE
from world.sim import narrator
from world.sim.contracts import ActionAttempt, EffectKind, EntityState, NounRef, Resolution
from world.sim.operations.handlers import move
from world.sim.space import zones

MATS = {}


def setup_module(_):
    narrator.load_responses(RESPONSES)
    zones.load_zones(ZONE_TABLE)


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


def _ent(id, name, zone=None, **kw):
    return EntityState(id=id, name=name, materials=kw.get("materials", []), parts=[], tags=[],
                       mass_g=kw.get("mass_g", 0),
                       state={"zone": zone} if zone else {}, provenance=[], owner=None)


def _world(actor_zone="mid_cabin"):
    return FakeWorld([_ent("p1", "Player", actor_zone),
                      _ent("radio", "field radio", "cockpit", materials=["plastic"], mass_g=900)])


def _go(dest_zone_ref, world, relation="to"):
    a = ActionAttempt(actor="p1", verb="move", X=None, relation=relation,
                      Y=(NounRef(dest_zone_ref),))
    return move.resolve_move(a, world, MATS)


def test_adjacent_move_emits_move_zone_and_footsteps():
    r = _go("zone:rear_cabin", _world())
    assert r.resolution == Resolution.SUCCESS and r.tier == "op:move:step"
    (eff,) = r.effects
    assert eff.kind == EffectKind.MOVE_ZONE and eff.args["zone"] == "rear_cabin"
    (ev,) = r.events
    assert ev.data == {"verb": "move", "from": "mid_cabin", "to": "rear_cabin"}
    assert "rear cabin" in r.narration


def test_non_adjacent_move_redirects_with_direction_and_first_step():
    r = _go("zone:treeline", _world())
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:move:no_route"
    assert "to the north" in r.narration and "rear cabin" in r.narration
    assert not r.effects


def test_approach_an_entity_derives_its_zone():
    a = ActionAttempt(actor="p1", verb="move", X=NounRef("radio"))
    r = move.resolve_move(a, _world(), MATS)   # radio is in the adjacent cockpit
    assert r.resolution == Resolution.SUCCESS
    assert r.effects[0].args["zone"] == "cockpit"


def test_already_there():
    r = _go("zone:mid_cabin", _world())
    assert r.tier == "op:move:already" and not r.effects


def test_bare_go_orients_with_walk_neighbors():
    a = ActionAttempt(actor="p1", verb="move", X=None)
    r = move.resolve_move(a, _world(), MATS)
    assert r.tier == "op:move:orient"
    assert "the cockpit" in r.narration and "the rear cabin" in r.narration


def test_no_walking_through_the_windscreen():
    r = _go("zone:outside_nose", _world(actor_zone="cockpit"))
    assert r.tier == "op:move:no_route"   # see-only edge: sight, not passage


def test_unzoned_actor_returns_none_for_the_generic_redirect():
    w = FakeWorld([_ent("p1", "Player", zone=None)])
    a = ActionAttempt(actor="p1", verb="move", X=None, relation="to",
                      Y=(NounRef("zone:cockpit"),))
    assert move.resolve_move(a, w, MATS) is None   # the one-zone compat rule
