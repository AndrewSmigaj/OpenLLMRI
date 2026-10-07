"""Tier-1: the taught-grammar parser — synonyms, identifiers, possessives, disambiguation (P1.5)."""
from world.sim.contracts import ActionAttempt, Disambiguation, ParseError, Reachable
from world.sim.operations.registry import VERB_TO_OP
from world.sim.parser import parse

SEAT = Reachable(id="seat", name="aircraft seat", ident="11B",
                 parts=(("cover", "cover"), ("cushion", "cushion"), ("bolt", "bolt")))
MULTITOOL = Reachable(id="multitool", name="multitool", aliases=("tool", "knife"))
LIGHTER = Reachable(id="lighter", name="lighter")
TINDER = Reachable(id="tinder", name="dry grass", aliases=("tinder", "grass"))
BOOK = Reachable(id="book", name="old book", parts=(("cover", "cover"),))
REACH = [SEAT, MULTITOOL, LIGHTER, TINDER]

# three IDENTICAL derived objects (same name, no ident) — the numbered-menu case
SHARDS = [Reachable(id=f"bottle:shard{i}:loose", name="glass shard") for i in range(3)]

# a zone pseudo-noun (DR-13a: destinations parse like nouns)
ZONE_COCKPIT = Reachable(id="zone:cockpit", name="the cockpit", aliases=("cockpit", "flight deck"))


def test_leading_relation_is_preserved():
    a = parse("go to the cockpit", VERB_TO_OP, REACH + [ZONE_COCKPIT])
    assert isinstance(a, ActionAttempt) and a.verb == "move"
    assert a.X is None and a.relation == "to" and a.Y[0].entity_id == "zone:cockpit"


def test_toward_is_a_to_synonym():
    a = parse("head toward the cockpit", VERB_TO_OP, REACH + [ZONE_COCKPIT])
    assert isinstance(a, ActionAttempt) and a.relation == "to"
    assert a.Y[0].entity_id == "zone:cockpit"


def test_zone_alias_matches():
    a = parse("go to the flight deck", VERB_TO_OP, REACH + [ZONE_COCKPIT])
    assert a.Y[0].entity_id == "zone:cockpit"


# --- containment parsing (DR-24/DR-25) ----------------------------------------

DUFFEL = Reachable(id="duffel", name="duffel bag", aliases=("duffel", "bag"))
SOCKS = Reachable(id="socks", name="wool socks", aliases=("socks",))
JACKET = Reachable(id="jacket", name="flight jacket", aliases=("jacket",))


def test_from_container_falls_back_to_entity_keeping_relation():
    # 'socks' is not a PART of the duffel — the fold falls back to the entity, container kept in Y
    # (verb-agnostic parser behavior; 'cut' stands in until the take op lands)
    a = parse("cut the socks from the duffel", VERB_TO_OP, REACH + [DUFFEL, SOCKS])
    assert isinstance(a, ActionAttempt)
    assert a.X.entity_id == "socks" and a.relation == "off" and a.Y[0].entity_id == "duffel"


def test_bare_verb_off_noun_keeps_y():
    a = parse("tear off the jacket", VERB_TO_OP, REACH + [JACKET])
    assert isinstance(a, ActionAttempt)
    assert a.X is None and a.relation == "off" and a.Y[0].entity_id == "jacket"


def test_part_fold_shape_is_unchanged():
    a = parse("cut the cover off the seat with the multitool", VERB_TO_OP, REACH)
    assert a.X.entity_id == "seat" and a.X.part_id == "cover"
    assert a.relation is None and a.Y is None      # the D6 fold keeps its pre-DR-24 shape


def _p(text, reach=REACH):
    return parse(text, VERB_TO_OP, reach)


def test_full_grammar_off_with_tool():
    a = _p("cut the cover off the seat with the multitool")
    assert isinstance(a, ActionAttempt) and a.verb == "cut"
    assert a.X.entity_id == "seat" and a.X.part_id == "cover"   # 'off seat' folded into X (D6)
    assert a.relation is None and a.Y is None
    assert a.tool.entity_id == "multitool"


def test_possessive_apostrophe():
    a = _p("cut the seat's cover")
    assert a.X.entity_id == "seat" and a.X.part_id == "cover"


def test_possessive_of():
    a = _p("cut cover of seat")
    assert a.X.entity_id == "seat" and a.X.part_id == "cover"


def test_owner_prefixed_part():
    a = _p("cut 11b cover")                     # identifier + part (a disambiguation ref is re-parseable)
    assert a.X.entity_id == "seat" and a.X.part_id == "cover"


def test_ident_reference():
    a = _p("examine 11b")
    assert a.verb == "examine" and a.X.entity_id == "seat" and a.X.part_id is None


def test_tool_synonyms():
    for kw in ("with", "using", "w/"):
        a = _p(f"burn tinder {kw} lighter")
        assert a.tool.entity_id == "lighter" and a.X.entity_id == "tinder"


def test_alias_matching():
    a = _p("cut cover with knife")              # 'knife' is an alias of the multitool
    assert a.tool.entity_id == "multitool"


def test_separate_object_relation_keeps_Y():
    a = _p("burn tinder on lighter")            # a non-'off' relation keeps relation + Y
    assert a.relation == "on" and a.Y[0].entity_id == "lighter" and a.X.entity_id == "tinder"


def test_disambiguation_lists_options():
    d = _p("cut cover", reach=[SEAT, BOOK])     # two 'cover's
    assert isinstance(d, Disambiguation) and d.term == "cover"
    labels = " | ".join(o.label for o in d.options)
    assert "11B" in labels and "book" in labels
    # each option carries its concrete identity (the menu binds by entity, not by label)
    assert {o.entity_id for o in d.options} == {"seat", "book"}
    assert all(o.part_id == "cover" for o in d.options)
    # each option's ref re-parses to a concrete part
    for o in d.options:
        a = parse(f"cut {o.ref}", VERB_TO_OP, [SEAT, BOOK])
        assert isinstance(a, ActionAttempt) and a.X.part_id == "cover"


def test_identical_objects_are_picked_silently_but_a_binding_still_pins_one():
    # DR-08b (2026-09-07): three IDENTICAL shards are a tie that doesn't matter — pick one, no menu
    a = parse("examine shard", VERB_TO_OP, SHARDS + [MULTITOOL])
    assert isinstance(a, ActionAttempt) and a.X.entity_id in {s.id for s in SHARDS}
    # things that DIFFER (an ident) still get the numbered menu with distinct identities
    d = parse("examine shard", VERB_TO_OP, SHARDS[:2] + [Reachable(id="bottle:shard2:loose", name="glass shard", ident="big")])
    assert isinstance(d, Disambiguation) and len({o.entity_id for o in d.options}) == 3
    assert all(o.part_id is None for o in d.options)


def test_binding_pins_the_ambiguous_slot():
    a = parse("examine shard", VERB_TO_OP, SHARDS,
              bindings={"shard": ("bottle:shard1:loose", None)})
    assert isinstance(a, ActionAttempt) and a.X.entity_id == "bottle:shard1:loose"


def test_binding_preserves_tool_and_relation():
    a = parse("cut shard with multitool", VERB_TO_OP, SHARDS + [MULTITOOL],
              bindings={"shard": ("bottle:shard2:loose", None)})
    assert isinstance(a, ActionAttempt)
    assert a.X.entity_id == "bottle:shard2:loose" and a.tool.entity_id == "multitool"


def test_binding_pins_an_ambiguous_part():
    a = parse("cut cover", VERB_TO_OP, [SEAT, BOOK], bindings={"cover": ("book", "cover")})
    assert isinstance(a, ActionAttempt)
    assert a.X.entity_id == "book" and a.X.part_id == "cover"


def test_stale_binding_falls_back_safely():
    # the picked entity is gone → the binding is ignored; identical shards pick silently (DR-08b),
    # DIFFERENT ones come back as a fresh menu — never an error
    a = parse("examine shard", VERB_TO_OP, SHARDS, bindings={"shard": ("gone:id", None)})
    assert isinstance(a, ActionAttempt)
    distinct = [Reachable(id=f"bottle:shard{i}:loose", name="glass shard", ident=str(i)) for i in range(3)]
    d = parse("examine shard", VERB_TO_OP, distinct, bindings={"shard": ("gone:id", None)})
    assert isinstance(d, Disambiguation) and len(d.options) == 3


def test_unknown_verb_is_a_teaching_nudge():
    e = _p("xyzzy the seat")
    assert isinstance(e, ParseError) and "xyzzy" in e.nudge


def test_unknown_noun_becomes_none_target():
    a = _p("cut the flux capacitor")
    assert isinstance(a, ActionAttempt) and a.X is None    # → resolver gives an informative redirect


def test_articles_ignored():
    assert _p("cut the cover").X.part_id == _p("cut cover").X.part_id == "cover"
