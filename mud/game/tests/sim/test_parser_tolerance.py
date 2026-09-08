"""Tier-1: parser tolerance (ontology-closure.md §5, 2026-09-07) — particles, multi-word relations,
synonyms, purpose trimming, body nouns, pronouns, `use … to …`, command splitting, silent
disambiguation, the unknown-verb nudge. All inside the taught grammar; no free-text NLP."""
from world.sim.contracts import ActionAttempt, Disambiguation, ParseError, Reachable
from world.sim.operations.registry import VERB_TO_OP
from world.sim.parser import parse, split_commands

SEAT = Reachable(id="seat", name="aircraft seat", aliases=("seat",), ident="11B",
                 parts=(("cover", "cover"), ("cushion", "cushion"), ("bolt", "bolt")))
SEAT2 = Reachable(id="seat2", name="aircraft seat", aliases=("seat",), ident="12C",
                  parts=(("cover", "cover"), ("cushion", "cushion")))
SHARD_HELD = Reachable(id="shard0", name="glass shard", held=True)
SHARD_FLOOR = Reachable(id="shard1", name="glass shard")
SHARD_FLOOR2 = Reachable(id="shard2", name="glass shard")
LIGHTER = Reachable(id="lighter", name="lighter")
CANTEEN = Reachable(id="canteen", name="canteen of water", aliases=("canteen", "flask"))
BAG = Reachable(id="backpack", name="backpack", aliases=("pack", "bag"))
WIRE = Reachable(id="wire", name="coil of copper wire", aliases=("wire", "coil"))
GRASS = Reachable(id="tinder", name="dry grass", aliases=("tinder", "grass"))
JACKET = Reachable(id="jacket", name="flight jacket", aliases=("jacket",))
ME = Reachable(id="me", name="you", aliases=("me", "self", "myself"))
BANDAGE = Reachable(id="bandage", name="bandage roll", aliases=("bandage",))
REACH = [SEAT, SHARD_HELD, SHARD_FLOOR, SHARD_FLOOR2, LIGHTER, CANTEEN, BAG, WIRE, GRASS, JACKET,
         ME, BANDAGE]


def _p(line, reach=REACH, **kw):
    return parse(line, VERB_TO_OP, reach, **kw)


def test_particles_are_positional():
    a = _p("cut open the cushion")
    assert isinstance(a, ActionAttempt) and a.verb == "cut" and a.X.part_id == "cushion"
    a = _p("pick up the lighter")
    assert a.verb == "take" and a.X.entity_id == "lighter"
    a = _p("put on the jacket")
    assert a.verb == "wear" and a.X.entity_id == "jacket"
    a = _p("go to the cockpit", reach=REACH + [Reachable(id="zone:cockpit", name="the cockpit", aliases=("cockpit",))])
    assert a.verb == "move" and a.relation == "to"            # a real relation stays a relation


def test_multiword_relations_and_out_of():
    a = _p("take the canteen out of the bag")
    assert a.verb == "take" and a.X.entity_id == "canteen" and a.relation == "off" and a.Y[0].entity_id == "backpack"
    a = _p("put the lighter on top of the seat")
    assert a.X.entity_id == "lighter" and a.relation == "on" and a.Y[0].entity_id == "seat"


def test_whole_phrase_binds_before_the_possessive_split():
    a = _p("take the canteen of water")
    assert isinstance(a, ActionAttempt) and a.X.entity_id == "canteen"


def test_synonyms_and_trailing_words():
    assert _p("find the lighter").verb == "search"
    assert _p("grab the lighter").verb == "take"
    a = _p("examine the copper wire in detail")
    assert a.X.entity_id == "wire"
    a = _p("light the grass to make a fire")                 # purpose clause dropped
    assert a.verb == "light" and a.X.entity_id == "tinder" and a.relation is None
    a = _p("light the grass with the lighter carefully")
    assert a.tool.entity_id == "lighter"


def test_meta_prefixes_are_stripped():
    a = _p("try to light the grass with the lighter")
    assert a.verb == "light" and a.X.entity_id == "tinder"
    a = _p("see if i can open the bag")
    assert a.verb == "open" and a.X.entity_id == "backpack"


def test_body_nouns_and_pronouns():
    a = _p("bandage my arm with the bandage")
    assert a.verb == "wrap" and a.X.entity_id == "me" and a.tool.entity_id == "bandage"
    a = _p("blow on it", bindings={"it": ("tinder", None)})
    assert a.verb == "light" and a.X.entity_id == "tinder"
    a = _p("examine it")                                       # nothing bound → X None, never an error
    assert isinstance(a, ActionAttempt) and a.X is None


def test_use_to_verb_rewrites_to_the_real_verb():
    a = _p("use the shard to cut the cushion")
    assert a.verb == "cut" and a.X.part_id == "cushion" and a.tool.entity_id == "shard0"   # the held shard
    a = _p("use the lighter on the grass")
    assert a.verb == "use" and a.X.entity_id == "lighter" and a.relation == "on" and a.Y[0].entity_id == "tinder"


def test_silent_disambiguation():
    a = _p("take shard")                                       # three identical shards: no question
    assert isinstance(a, ActionAttempt) and a.X.entity_id in ("shard0", "shard1", "shard2")
    a = _p("cut the cushion with the shard")                   # the tool slot prefers what you hold
    assert a.tool.entity_id == "shard0"
    d = _p("cut cover off seat", reach=REACH + [SEAT2])        # two DIFFERENT seats: a true tie → ask
    assert isinstance(d, Disambiguation)
    a = _p("cut cover off 12c", reach=REACH + [SEAT2])
    assert a.X.entity_id == "seat2" and a.X.part_id == "cover"


def test_unknown_verb_nudge_names_close_verbs_and_kind():
    e = _p("chop the grass")
    assert isinstance(e, ParseError) and e.kind == "unknown_verb" or (isinstance(e, ActionAttempt) and e.verb == "cut")
    e = _p("slce the cover")
    assert isinstance(e, ParseError) and "slice" in e.nudge or "cut" in e.nudge
    assert "help grammar" in e.nudge


def test_split_commands():
    parts = split_commands("take the shard and cut the cushion", VERB_TO_OP)
    assert parts == ["take the shard", "cut the cushion"]
    parts = split_commands("tie the letters and the sheet", VERB_TO_OP)
    assert parts == ["tie the letters and the sheet"]
    parts = split_commands("open the bag, then take the canteen", VERB_TO_OP)
    assert parts == ["open the bag", "take the canteen"]


def test_make_never_binds_a_noun():
    ext = Reachable(id="extinguisher", name="fire extinguisher", aliases=("extinguisher",))
    a = _p("make fire with sticks", reach=REACH + [ext])
    assert isinstance(a, ActionAttempt) and a.verb == "make" and a.X is None and a.tool is None
    assert a.raw == "make fire with sticks"
