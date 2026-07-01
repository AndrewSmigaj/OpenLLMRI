"""world.sim.parser.grammar — the taught-grammar parser (DR-08 / GDD §25a). Pure given vocab+reachable.

`VERB X [RELATION Y] [WITH Z]`. Verb synonyms via `vocab` (the registry's VERB_TO_OP); keyword/relation
synonyms via `parser.vocab`; nouns matched against `reachable` (Reachable descriptors — name/aliases/
ident + parts). Returns `ActionAttempt | ParseError(nudge) | Disambiguation` (the user refinements:
`with`=`using` synonyms, object/part identifiers, and the disambiguation list). Unknown input never
hard-fails — a ParseError carries a teaching nudge. An unresolved noun becomes `X=None`, which the
resolver turns into an informative redirect (so "everything resolves").
"""
from __future__ import annotations

from world.sim.contracts import ActionAttempt, DisambigOption, Disambiguation, NounRef, ParseError
from world.sim.parser.vocab import ARTICLES, RELATIONS, TOOL_KEYWORDS

_NUDGE = ("Try:  VERB thing [RELATION thing] [WITH tool]  —  e.g. 'cut the cover off the seat with the "
          "multitool'. Use 'examine <thing>' to see what you can name.")


def parse(text, vocab, reachable):
    raw = (text or "").strip()
    toks = _tokenize(raw)
    if not toks:
        return ParseError("empty", _NUDGE)

    verb = (vocab or {}).get(toks[0])
    if verb is None:
        return ParseError(f"unknown verb {toks[0]!r}", f"I don't know how to '{toks[0]}'. " + _NUDGE)

    main, tool_words = _split_on(toks[1:], TOOL_KEYWORDS)
    x_words, relation, y_words = _split_relation(main)

    y_ref = _resolve(y_words, reachable)
    if isinstance(y_ref, Disambiguation):
        return y_ref
    owner_hint = y_ref.entity_id if (relation == "off" and isinstance(y_ref, NounRef)) else None
    x_ref = _resolve(x_words, reachable, owner_hint=owner_hint)
    if isinstance(x_ref, Disambiguation):
        return x_ref
    tool_ref = _resolve(tool_words, reachable)
    if isinstance(tool_ref, Disambiguation):
        return tool_ref

    X = x_ref if isinstance(x_ref, NounRef) else None
    Z = tool_ref if isinstance(tool_ref, NounRef) else None
    if relation == "off":                       # 'off'/'from' fold Y into X as the part's owner (D6)
        return ActionAttempt(actor="", verb=verb, X=X, relation=None, Y=None, tool=Z, raw=raw)
    Y = (y_ref,) if isinstance(y_ref, NounRef) else None
    return ActionAttempt(actor="", verb=verb, X=X, relation=(relation if Y else None), Y=Y, tool=Z, raw=raw)


# --- tokenization / splitting ------------------------------------------------

def _tokenize(raw):
    return [t for t in raw.lower().replace("'s", " 's ").split() if t]


def _split_on(words, keywords):
    for i, w in enumerate(words):
        if w in keywords:
            return words[:i], words[i + 1:]
    return words, []


def _split_relation(words):
    for i, w in enumerate(words):
        if i > 0 and w in RELATIONS:
            return words[:i], RELATIONS[w], words[i + 1:]
    return words, None, []


# --- noun resolution ---------------------------------------------------------

def _resolve(words, reachable, owner_hint=None):
    words = [w for w in (words or []) if w not in ARTICLES]
    if not words:
        return None

    owner_ws, part_ws = _split_possessive(words)          # "seat's cover" / "cover of seat"
    if owner_ws is not None:
        ent = _match_entity(owner_ws, reachable)
        if not isinstance(ent, NounRef):
            return ent
        return _part_of(ent.entity_id, part_ws, reachable)

    if owner_hint is not None:                            # "... off <owner>" → X is a part of owner
        return _part_of(owner_hint, words, reachable)

    for k in range(len(words) - 1, 0, -1):               # "OWNER PART" e.g. "11b cover", "old book cover"
        head = _match_entity(words[:k], reachable)
        if isinstance(head, NounRef):
            p = _part_of(head.entity_id, words[k:], reachable)
            if isinstance(p, NounRef):
                return p

    ent = _match_entity(words, reachable)                 # whole phrase as an entity
    if ent is not None:
        return ent
    return _match_part_anywhere(words, reachable)          # a part label across all entities


def _split_possessive(words):
    if "'s" in words:
        i = words.index("'s")
        return words[:i], words[i + 1:]                    # owner before, part after
    if "of" in words:
        i = words.index("of")
        return words[i + 1:], words[:i]                    # "cover of seat" → owner=seat, part=cover
    return None, None


def _match_entity(words, reachable):
    phrase = " ".join(words)
    hits, seen = [], set()
    for r in reachable or []:
        names = {r.name.lower()} | {a.lower() for a in r.aliases}
        if r.ident:
            names.add(r.ident.lower())
        if phrase in names or (len(words) == 1 and words[0] in r.name.lower().split()):
            if r.id not in seen:
                seen.add(r.id)
                hits.append(r)
    if not hits:
        return None
    if len(hits) == 1:
        return NounRef(hits[0].id)
    return _disambig(phrase, [(h, None) for h in hits])


def _part_of(entity_id, part_words, reachable):
    part_words = [w for w in (part_words or []) if w not in ARTICLES]
    r = _by_id(entity_id, reachable)
    if r is None or not part_words:
        return None
    phrase = " ".join(part_words)
    for pid, label in r.parts:
        if phrase in (pid.lower(), label.lower()) or (len(part_words) == 1 and part_words[0] in label.lower().split()):
            return NounRef(entity_id, pid)
    return None


def _match_part_anywhere(words, reachable):
    phrase = " ".join(words)
    hits = []
    for r in reachable or []:
        for pid, label in r.parts:
            if phrase in (pid.lower(), label.lower()) or (len(words) == 1 and words[0] in label.lower().split()):
                hits.append((r, pid, label))
    if not hits:
        return None
    if len(hits) == 1:
        r, pid, _ = hits[0]
        return NounRef(r.id, pid)
    return _disambig(phrase, [(r, (pid, label)) for r, pid, label in hits])


def _disambig(term, entries):
    opts = []
    for r, part in entries:
        who = r.name + (f" {r.ident}" if r.ident else "")
        key = (r.ident or r.name).lower()
        if part is None:
            opts.append(DisambigOption(label=who, ref=key))
        else:
            pid, plabel = part
            opts.append(DisambigOption(label=f"{who}'s {plabel}", ref=f"{key} {plabel.lower()}"))
    return Disambiguation(term=term, options=tuple(opts))


def _by_id(entity_id, reachable):
    for r in reachable or []:
        if r.id == entity_id:
            return r
    return None
