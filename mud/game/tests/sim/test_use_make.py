"""Tier-1: the teaching verbs — `use` dispatches through capabilities to the real verb and echoes it;
`make` says what a thing is made of and never succeeds by itself."""
from world.scenarios.whiteout.materials.table import MATERIAL_TABLE
from world.scenarios.whiteout.responses.slice import RESPONSES
from world.sim import narrator
from world.sim.contracts import ActionAttempt, EntityState, NounRef, Part, Resolution
from world.sim.materials import load_materials
from world.sim.operations.handlers import make_op, use

MATS = load_materials(MATERIAL_TABLE)


def setup_module(_):
    narrator.load_responses(RESPONSES)


class W:
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
                       parts=[Part("cover", "synthetic_fabric", 200, "stitched", ("loose_fabric",))])


def test_use_shard_on_cover_cuts_and_echoes_the_verb():
    shard = EntityState(id="shard", name="glass shard", materials=["glass"], mass_g=166, state={"form": "shard"})
    w = W([shard, _seat()])
    r = use.resolve_use(ActionAttempt(actor="p", verb="use", X=NounRef("shard"), relation="on",
                                      Y=(NounRef("seat", "cover"),), raw="use shard on cover"), w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier == "use>op:cut:free"
    assert "'cut" in r.narration and "with glass shard" in r.narration


def test_use_lighter_on_grass_lights_it():
    lighter = EntityState(id="lighter", name="lighter", materials=["plastic"], mass_g=20, state={"ignition": True})
    grass = EntityState(id="tinder", name="dry grass", materials=["dry_grass"], mass_g=40)
    w = W([lighter, grass])
    r = use.resolve_use(ActionAttempt(actor="p", verb="use", X=NounRef("lighter"), relation="on",
                                      Y=(NounRef("tinder"),), raw="use lighter on grass"), w, MATS)
    assert r.resolution == Resolution.SUCCESS and r.tier.startswith("use>op:light")


def test_use_alone_names_what_it_affords_and_a_dud_says_so():
    shard = EntityState(id="shard", name="glass shard", materials=["glass"], mass_g=166, state={"form": "shard"})
    lump = EntityState(id="lump", name="foam lump", materials=["foam"], mass_g=100, state={"form": "scrap"})
    w = W([shard, lump])
    r = use.resolve_use(ActionAttempt(actor="p", verb="use", X=NounRef("shard"), raw="use shard"), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:use:what" and "cut" in r.narration
    r = use.resolve_use(ActionAttempt(actor="p", verb="use", X=NounRef("lump"), relation="on",
                                      Y=(NounRef("shard"),), raw="use lump on shard"), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:use:nothing"


def test_make_fire_teaches_components_and_never_succeeds():
    w = W([])
    r = make_op.resolve_make(ActionAttempt(actor="p", verb="make", raw="make a fire"), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:make:fire"
    assert "catches" in r.narration and "light" in r.narration
    r = make_op.resolve_make(ActionAttempt(actor="p", verb="make", raw="make fire with sticks"), w, MATS)
    assert "sticks" in r.narration and "How do you mean" in r.narration
    r = make_op.resolve_make(ActionAttempt(actor="p", verb="make", raw="build a spaceship"), w, MATS)
    assert r.resolution == Resolution.REDIRECT and r.tier == "op:make:unknown"
