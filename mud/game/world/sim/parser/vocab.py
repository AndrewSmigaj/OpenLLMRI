"""world.sim.parser.vocab — keyword & relation synonyms for the taught grammar (DR-08, GDD §25a).

Verb synonyms come from the operations registry (VERB_TO_OP). These are the NON-verb keywords: the tool
marker (`with`=`using`), the relation words with synonyms, the possessive markers, and ignorable
articles. Tunable content — Andrew adjusts feel after P1.
"""
from __future__ import annotations

TOOL_KEYWORDS = frozenset({"with", "using", "w/"})
POSSESSIVE = frozenset({"of", "'s"})
ARTICLES = frozenset({"the", "a", "an", "some", "my", "your", "that", "this"})

# relation word (+ synonyms) -> canonical relation
RELATIONS = {
    "off": "off", "from": "off",
    "on": "on", "onto": "on",
    "to": "to",
    "against": "against",
    "between": "between",
    "into": "into", "in": "into",
    "under": "under",
    "around": "around",
}
