"""world.sim.parser.grammar — the taught-grammar parser (DR-08 / GDD §25a).

Grammar: `VERB  X  [RELATION  Y]  [WITH Z]`, at action granularity. Pipeline: tokenize → match verb
against the synonym table (built from every operation's `verbs`) → bind X (a thing OR a part;
possessive and `of` both parse) → optional RELATION preposition + a second object Y → optional WITH
tool Z → resolve each noun phrase to a REACHABLE entity (adjective + disambiguation on ties) → emit
ActionAttempt{actor, verb, X, relation, Y, tool, raw}. Unknown verb / no match → a ParseError carrying
a help nudge that teaches the format (never a hard refusal).

The RELATION slot is what makes two-object actions (cut…off…, wedge…against…, tie…between…)
first-class. Richness comes from rule coverage + the generative operation×material engine, not parser
cleverness or an enumerated command list. (Internal planned modules: tokenizer, synonym table, slot
binding.) Pure given a vocabulary + the reachable-entity set.
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, ParseError  # noqa: F401


def parse(text: str, vocab, reachable) -> "ActionAttempt | ParseError":
    """Parse one typed line into an ActionAttempt, or a ParseError with a teaching nudge. Implemented
    in roadmap P1. See parser/README.md."""
    raise NotImplementedError("parser.parse — roadmap P1")
