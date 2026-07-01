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
    # each option's ref re-parses to a concrete part
    for o in d.options:
        a = parse(f"cut {o.ref}", VERB_TO_OP, [SEAT, BOOK])
        assert isinstance(a, ActionAttempt) and a.X.part_id == "cover"


def test_unknown_verb_is_a_teaching_nudge():
    e = _p("xyzzy the seat")
    assert isinstance(e, ParseError) and "xyzzy" in e.nudge


def test_unknown_noun_becomes_none_target():
    a = _p("cut the flux capacitor")
    assert isinstance(a, ActionAttempt) and a.X is None    # → resolver gives an informative redirect


def test_articles_ignored():
    assert _p("cut the cover").X.part_id == _p("cut cover").X.part_id == "cover"
