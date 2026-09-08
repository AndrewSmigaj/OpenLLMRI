"""world.sim.parser.vocab — the non-verb vocabulary of the taught grammar (DR-08, GDD §25a) plus the
tolerance tables (parser tolerance, 2026-09-07 — ontology-closure.md §5).

Verb synonyms proper come from the operations registry (VERB_TO_OP). Here: the tool marker, the
relation words (single and MULTI-word), the articles, and the tolerance layer that maps what people
and agents actually type onto the grammar without becoming free-text NLP: first-token SYNONYMS,
verb+PARTICLE forms (`pick up`, `cut open`, `put on`), META prefixes (`try to`, `see if`), the
purpose/adverb TRIM (the game never needs the aim, only the act — "shake thermos", not "shake
thermos to see if coffee is in there"), BODY nouns (`my arm` → the actor), and PRONOUNS. All of it
is seeded from the 2026-09-07 phrasing samples and grows by the discovery loop. Tunable content.
"""
from __future__ import annotations

TOOL_KEYWORDS = frozenset({"with", "using", "w/"})
POSSESSIVE = frozenset({"of", "'s"})
ARTICLES = frozenset({"the", "a", "an", "some", "my", "your", "that", "this", "these", "those",
                      "few", "bit", "piece"})

# relation word (+ synonyms) -> canonical relation
RELATIONS = {
    "off": "off", "from": "off",
    "on": "on", "onto": "on", "upon": "on", "over": "over", "atop": "on",
    "to": "to", "toward": "to", "towards": "to",
    "against": "against",
    "between": "between",
    "into": "into", "in": "into", "inside": "into",
    "under": "under", "beneath": "under", "underneath": "under",
    "around": "around", "round": "around",
    "through": "through", "across": "across", "behind": "behind",
    "beside": "beside", "near": "beside", "by": "beside",
}
# multi-word relations, matched greedily BEFORE the single words (token tuples -> canonical)
MULTIWORD_RELATIONS = {
    ("out", "of"): "off", ("off", "of"): "off", ("away", "from"): "off",
    ("on", "top", "of"): "on", ("in", "front", "of"): "beside", ("next", "to"): "beside",
    ("close", "to"): "beside", ("in", "to"): "into", ("on", "to"): "on",
}

# first-token synonyms → canonical verbs (verbs the registry already knows map to themselves there;
# these are the phrasings the samples used that the registry does NOT know). `use` and `make` are
# real teaching operations (handlers/use.py, handlers/make_op.py).
SYNONYMS = {
    "find": "search", "locate": "search", "look": "examine", "see": "examine", "test": "examine",
    "watch": "examine", "view": "examine", "feel": "examine", "touch": "examine",
    "retrieve": "take", "fetch": "take", "gather": "take", "pick": "take", "hold": "take",
    "carry": "take", "pull": "take", "grasp": "take", "acquire": "take", "obtain": "take",
    "drop": "put", "leave": "put", "rest": "put",
    "place": "put", "set": "put", "lay": "put", "add": "put", "stack": "put", "pile": "put",
    "arrange": "put", "position": "put", "hit": "break", "punch": "break", "kick": "break",
    "chop": "cut", "sever": "cut", "hack": "cut", "trim": "cut", "bandage": "wrap", "treat": "wrap",
    "rub": "light",
    
    "bash": "break", "crack": "break",
    
    "drape": "wear", "dress": "wear", "clothe": "wear", "cover": "wrap", "apply": "wrap",
    "swathe": "wrap", "tape": "tie", "attach": "tie", "connect": "tie", "strap": "tie",
    "hitch": "tie", "hang": "tie", "string": "tie",
    "heat": "melt", "warm": "melt", "boil": "melt", "cook": "melt", "defrost": "melt",
    "shoot": "light", "fire": "light", "blow": "light", "fan": "light",
    "refill": "pour", "fill": "pour", "empty": "pour", "spill": "pour", "wash": "pour",
    "rinse": "pour", "clean": "pour", "dampen": "pour", "wet": "pour",
    "sniff": "examine", "smell": "examine", "listen": "examine", "taste": "drink",
    "consume": "eat", "swallow": "eat", "nibble": "eat",
    "unlock": "open", "unseal": "open", "unzip": "open", "uncap": "open", "unscrew": "open",
    "zip": "close", "seal": "close", "shut": "close", "lock": "close",
    "unfold": "bend", "flatten": "bend", "shape": "bend", "reshape": "bend",
    
    "run": "go", "crawl": "go", "climb": "go", "step": "go", "exit": "go", "return": "go",
    
    "use": "use", "utilize": "use", "employ": "use", "operate": "use", "wield": "use",
    "make": "make", "build": "make", "create": "make", "craft": "make", "construct": "make",
    "assemble": "make", "prepare": "make", "improvise": "make", "fashion": "make", "form": "make",
    "start": "make", "begin": "make", "erect": "make", "rig": "make", "setup": "make",
    "speak": "talk", "say": "talk", "shout": "talk", "call": "talk", "yell": "talk", "whisper": "talk",
    
    
    
}

# (verb, particle) → canonical verb; the particle is the word RIGHT AFTER the verb, and it changes
# the verb's sense. Positional rule (TADS): a relation word in that slot with no noun before it is a
# particle only if the pair is listed here — otherwise it stays a relation (`go to X`, `tear off X`).
PARTICLES = {
    ("take", "out"): "take", ("take", "up"): "take", ("take", "off"): "remove", ("take", "down"): "take",
    ("pick", "up"): "take", ("get", "out"): "take", ("pull", "out"): "take", ("pull", "off"): "remove",
    ("pull", "up"): "take", ("scoop", "up"): "take", ("gather", "up"): "take", ("dig", "out"): "take",
    ("dig", "up"): "dig", ("dig", "in"): "dig", ("dig", "into"): "dig", ("dig", "through"): "dig",
    ("put", "on"): "wear", ("pull", "on"): "wear", ("slip", "on"): "wear", ("wrap", "up"): "wrap",
    ("put", "out"): "douse", ("put", "down"): "put", ("set", "down"): "put", ("lay", "down"): "put",
    ("put", "away"): "put", ("put", "back"): "put", ("set", "off"): "light", ("set", "up"): "make",
    ("light", "up"): "light", ("fire", "up"): "light", ("blow", "on"): "light", ("blow", "out"): "douse",
    ("cut", "open"): "cut", ("cut", "up"): "cut", ("cut", "off"): "cut", ("cut", "down"): "cut",
    ("cut", "through"): "cut", ("cut", "away"): "cut", ("slice", "open"): "cut", ("slice", "up"): "cut",
    ("tear", "open"): "tear", ("tear", "up"): "tear", ("tear", "apart"): "tear", ("rip", "open"): "tear",
    ("rip", "up"): "tear", ("rip", "apart"): "tear", ("rip", "off"): "tear", ("tear", "down"): "tear",
    ("break", "open"): "break", ("break", "up"): "break", ("break", "apart"): "break",
    ("break", "off"): "break", ("break", "down"): "break", ("snap", "off"): "break", ("smash", "open"): "break",
    ("pry", "open"): "pry", ("pry", "off"): "pry", ("pry", "up"): "pry", ("pry", "loose"): "pry",
    ("force", "open"): "pry", ("lever", "open"): "pry", ("lever", "off"): "pry",
    ("open", "up"): "open", ("close", "up"): "close", ("zip", "up"): "close", ("seal", "up"): "close",
    ("turn", "on"): "turn", ("turn", "off"): "turn", ("switch", "on"): "turn", ("switch", "off"): "turn",
    ("look", "at"): "examine", ("look", "in"): "search", ("look", "inside"): "search",
    ("look", "into"): "search", ("look", "under"): "search", ("look", "behind"): "search",
    ("look", "through"): "search", ("look", "for"): "search", ("look", "around"): "examine",
    ("look", "over"): "examine", ("check", "on"): "examine", ("check", "out"): "examine",
    ("check", "for"): "search", ("search", "for"): "search", ("search", "through"): "search",
    ("search", "in"): "search", ("feel", "for"): "search", ("rummage", "through"): "search",
    ("rummage", "in"): "search", ("go", "back"): "go", ("go", "over"): "go", ("go", "out"): "go",
    ("go", "outside"): "go", ("go", "inside"): "go", ("go", "up"): "go", ("go", "down"): "go",
    ("climb", "up"): "go", ("climb", "down"): "go", ("climb", "onto"): "go", ("climb", "into"): "go",
    ("get", "in"): "go", ("get", "into"): "go", ("get", "out"): "go", ("head", "back"): "go",
    ("sit", "by"): "put", ("sit", "near"): "put", ("sit", "down"): "put", ("sit", "on"): "put",
    ("lie", "down"): "put", ("huddle", "up"): "put", ("wake", "up"): "talk",
    ("tie", "off"): "tie", ("tie", "up"): "tie", ("tie", "down"): "tie", ("tie", "together"): "tie",
    ("lash", "together"): "tie", ("hook", "up"): "tie", ("bind", "up"): "tie",
    ("wipe", "off"): "pour", ("wipe", "down"): "pour", ("rinse", "off"): "pour", ("pour", "out"): "pour",
    ("melt", "down"): "melt", ("heat", "up"): "melt", ("warm", "up"): "melt", ("boil", "up"): "melt",
    ("eat", "up"): "eat", ("drink", "up"): "drink", ("chew", "on"): "eat", ("sip", "from"): "drink",
    ("drink", "from"): "drink", ("drink", "out"): "drink", ("read", "through"): "read",
    ("roll", "up"): "bend", ("fold", "up"): "bend", ("straighten", "out"): "bend", ("bend", "back"): "bend",
    ("talk", "to"): "talk", ("speak", "to"): "talk", ("speak", "into"): "talk", ("call", "out"): "talk",
    ("call", "for"): "talk", ("shout", "for"): "talk", ("cry", "out"): "talk", ("ask", "for"): "talk",
    ("use", "up"): "use", ("make", "up"): "make", ("build", "up"): "make", ("start", "up"): "turn",
    ("light", "a"): "make", ("light", "the"): "light", ("start", "a"): "make",
}

# leading META phrases that carry intent, not action — stripped
META_PREFIXES = (
    "try to", "try and", "try", "attempt to", "attempt", "see if i can", "see if you can", "see if",
    "check if", "check whether", "check that", "figure out how to", "figure out", "let me", "let's",
    "lets", "i want to", "i'd like to", "i will", "i'll", "i", "please", "now", "then", "next",
    "first", "carefully", "quickly", "go and", "maybe", "perhaps", "just", "also",
)
# after these words a PURPOSE clause begins and is dropped (never needed: state the act, not the aim);
# `to` counts only when a VERB follows it (`tie strap to seat` keeps its relation)
PURPOSE_CUTS = frozenset({"for", "so", "until", "till", "when", "if", "once", "because", "while",
                          "unless", "whether", "before", "after", "as", "since", "where", "in-order-to"})
# adverbs and fillers dropped wherever they occur
TRAIL_ADVERBS = frozenset({
    "carefully", "gently", "vigorously", "tightly", "finely", "slightly", "firmly", "quickly",
    "slowly", "hard", "harder", "faster", "more", "forcefully", "closely", "thoroughly", "really",
    "very", "again", "now", "first", "too", "please", "here", "there", "properly", "well",
    "immediately", "briefly", "a", "little", "lot", "lots", "bit", "instead", "anyway", "then",
    "next", "later", "still", "also", "just", "quietly", "loudly", "detail",
})
# particles that may trail a noun phrase ("pick the shard up", "take the canteen out") — dropped
# only at the END of a phrase, never mid-phrase (they are relations there)
TRAIL_PARTICLES = frozenset({"up", "down", "out", "away", "back", "apart", "together", "around"})
# body parts and self-references → the actor (`me` is an alias the world gives the actor)
BODY_NOUNS = (
    "my forearm", "the forearm", "forearm", "my arm", "the arm", "my arms", "my hand", "my hands",
    "my feet", "my foot", "my shoulders", "my shoulder", "my neck", "my head", "my leg", "my legs",
    "my chest", "my back", "my face", "my body", "the cut", "my cut", "cut on my forearm",
    "the wound", "my wound", "my sleeve", "myself", "my mouth", "my eyes", "my fingers", "my torso",
    "my skin", "my knee", "my knees", "my wrist", "my ankle", "my thigh", "my elbow", "torso",
    # bare limb words are safe (no verb, alias or particle in this world spells them)
    "arm", "arms", "leg", "legs", "wrist", "ankle", "knee", "elbow", "thigh", "shin", "shoulder",
    "shoulders",
)
PRONOUNS = frozenset({"it", "them", "that", "this", "one", "those", "these"})

# for the unknown-verb nudge: name the families, never the whole list
VERB_FAMILIES = {
    "cutting & shaping": ("cut", "tear", "break", "bend", "pry", "carve", "split"),
    "fire": ("light", "burn", "melt", "douse"),
    "binding & covering": ("tie", "wrap", "put", "cover"),
    "moving & carrying": ("take", "put", "go", "open", "close", "search", "dig"),
    "body & senses": ("examine", "eat", "drink", "wear", "remove", "read"),
    "social": ("talk", "say", "whisper", "shout"),
}
