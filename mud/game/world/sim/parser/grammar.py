"""world.sim.parser.grammar — the taught-grammar parser (DR-08 / GDD §25a). Pure given vocab+reachable.

`VERB X [RELATION Y] [WITH Z]`. Verb synonyms via `vocab` (the registry's VERB_TO_OP) plus the
tolerance tables in `parser.vocab`; nouns matched against `reachable` (Reachable descriptors —
name/aliases/ident + parts). Returns `ActionAttempt | ParseError(nudge) | Disambiguation`. Unknown
input never hard-fails — a ParseError carries a teaching nudge. An unresolved noun becomes `X=None`,
which the resolver turns into an informative redirect (so "everything resolves").

The tolerance layer (2026-09-07, ontology-closure.md §5 — measured, not guessed) maps what people
and agents actually type onto the grammar WITHOUT free-text NLP:
  * meta prefixes stripped (`try to`, `see if`); first-token SYNONYMS; verb+PARTICLE forms resolved
    POSITIONALLY (`cut open X`, `pick up X`, `put on X`→wear — TADS's rule: a relation word right
    after the verb with nothing before it is a particle only if the pair is listed, else it stays a
    relation: `go to X`, `tear off X`);
  * `use X to VERB Y` rewrites to `VERB Y with X`; other purpose clauses are dropped — the game
    never needs the aim, only the act (`shake thermos`, not `shake thermos to see if…`);
  * multi-word relations (`out of`, `on top of`) matched greedily before single ones;
  * body parts and self → `me`; pronouns (`it`) → the last bound noun via `bindings["it"]`;
  * nouns: the whole phrase first (`canteen of water`), then possessives, then OWNER PART, then
    the longest known prefix (`copper wire in detail` → the wire);
  * disambiguation is resolved SILENTLY when it can be (exact matches beat partial; identical
    things pick the first; a held thing wins the tool slot), and asked only on a true tie;
  * an unknown verb nudges with 2–4 close verbs and points to `help grammar` / `help verbs`.
`bindings` (optional): `{term: (entity_id, part_id)}` — a numbered-menu pick (DR-08a) pins a term;
`bindings["it"]` is the anaphora slot. Plain input data; parse stays pure.
"""
from __future__ import annotations

import difflib
import re

from world.sim.contracts import ActionAttempt, DisambigOption, Disambiguation, NounRef, ParseError
from world.sim.parser.vocab import (ARTICLES, BODY_NOUNS, META_PREFIXES, MULTIWORD_RELATIONS,
                                    PARTICLES, PRONOUNS, PURPOSE_CUTS, RELATIONS, SYNONYMS,
                                    TOOL_KEYWORDS, TRAIL_ADVERBS, TRAIL_PARTICLES, VERB_FAMILIES)

_NUDGE = ("Try:  VERB thing [RELATION thing] [WITH tool]  —  e.g. 'cut the cover off the seat with the "
          "multitool'. 'help grammar' shows the shape; 'help verbs' lists the verb families; "
          "'examine <thing>' shows what you can name.")
_IT = "__it__"
_SPLIT = re.compile(r"\s*(?:,|;)?\s*\b(?:and then|then|and|after that)\b\s+")


# --- the public surface ------------------------------------------------------

def split_commands(text, vocab) -> list:
    """`take the shard and cut the cover` → two lines. A segment that doesn't start with a verb is
    glued back onto the previous one (`tie the letters and the sheet` stays one command)."""
    raw = (text or "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in _SPLIT.split(raw) if p and p.strip()]
    out = []
    for p in parts:
        toks = _strip_meta(_tokenize(p))
        if out and not (toks and _canon_verb(toks, vocab)[0]):
            out[-1] = f"{out[-1]} and {p}"
        else:
            out.append(p)
    return out or [raw]


def parse(text, vocab, reachable, bindings=None):
    raw = (text or "").strip()
    toks = _strip_meta(_tokenize(_body_nouns(raw)))
    if not toks:
        return ParseError("empty", _NUDGE, kind="empty")

    verb, rest = _canon_verb(toks, vocab)
    if verb is None:
        return ParseError(f"unknown verb {toks[0]!r}", _unknown_verb_nudge(toks[0], vocab), kind="unknown_verb")

    if verb == "use":                                  # `use X to VERB Y` → `VERB Y with X`
        rewritten = _rewrite_use(rest, vocab)
        if rewritten is not None:
            return parse(rewritten, vocab, reachable, bindings)

    rest = _trim_purpose(rest, vocab)
    rest = [w for w in rest if w not in TRAIL_ADVERBS]
    rest = _pronouns(rest, bindings)

    main, tool_words = _split_on(rest, TOOL_KEYWORDS)
    x_words, relation, y_words = _split_relation(main)
    x_words, y_words, tool_words = (_strip_trailing(x_words), _strip_trailing(y_words),
                                    _strip_trailing(tool_words))

    y_ref = _resolve(y_words, reachable, bindings=bindings, allow_forms=(relation == "into"))
    if isinstance(y_ref, Disambiguation):
        return y_ref
    owner_hint = y_ref.entity_id if (relation == "off" and isinstance(y_ref, NounRef)) else None
    x_ref = _resolve(x_words, reachable, owner_hint=owner_hint, bindings=bindings)
    if x_ref is None and owner_hint is not None:
        # DR-24: not a PART of the owner — maybe a thing INSIDE it ("take socks from duffel").
        x_ref = _resolve(x_words, reachable, bindings=bindings)
        if isinstance(x_ref, Disambiguation):
            return x_ref
        X = x_ref if isinstance(x_ref, NounRef) else None
        Z0 = _resolve(tool_words, reachable, bindings=bindings, prefer_held=True)
        if isinstance(Z0, Disambiguation):
            return Z0
        return ActionAttempt(actor="", verb=verb, X=X, relation="off", Y=(y_ref,),
                             tool=Z0 if isinstance(Z0, NounRef) else None, raw=raw)
    if isinstance(x_ref, Disambiguation):
        return x_ref
    tool_ref = _resolve(tool_words, reachable, bindings=bindings, prefer_held=True)
    if isinstance(tool_ref, Disambiguation):
        return tool_ref

    X = x_ref if isinstance(x_ref, NounRef) else None
    Z = tool_ref if isinstance(tool_ref, NounRef) else None
    if relation == "off":                       # 'off'/'from' fold Y into X as the part's owner (D6)
        if X is None and isinstance(y_ref, NounRef):
            return ActionAttempt(actor="", verb=verb, X=None, relation="off", Y=(y_ref,), tool=Z, raw=raw)
        return ActionAttempt(actor="", verb=verb, X=X, relation=None, Y=None, tool=Z, raw=raw)
    Y = (y_ref,) if isinstance(y_ref, NounRef) else None
    return ActionAttempt(actor="", verb=verb, X=X, relation=(relation if Y else None), Y=Y, tool=Z, raw=raw)


# --- tokenization / normalization ------------------------------------------------------------

def _tokenize(raw):
    raw = raw.lower()
    # a leading conditional clause is intent, not act: "if no ember, strike the wire again"
    m = re.match(r"^\s*(?:if|when|once|unless|after|before|while)\b[^,]*,\s*(.+)$", raw)
    if m:
        raw = m.group(1)
    raw = re.sub(r"[^\w\s'/\-]", " ", raw)               # punctuation → space (keep 's, w/, hyphens)
    return [t for t in raw.replace("'s", " 's ").split() if t]


def _body_nouns(raw: str) -> str:
    low = raw.lower()
    for phrase in sorted(BODY_NOUNS, key=len, reverse=True):
        low = re.sub(rf"\b{re.escape(phrase)}\b", "me", low)
    return low


def _strip_meta(toks):
    changed = True
    while toks and changed:
        changed = False
        for pre in sorted(META_PREFIXES, key=lambda p: -len(p.split())):
            n = len(pre.split())
            if toks[:n] == pre.split() and len(toks) > n:
                toks = toks[n:]
                changed = True
                break
    return toks


def _stem(word, vocab):
    """`striking` → strike, `speaking` → speak: a gerund whose stem is a verb we know."""
    if len(word) > 5 and word.endswith("ing"):
        for stem in (word[:-3], word[:-3] + "e", word[:-4] if word[-4] == word[-5] else None):
            if stem and ((vocab or {}).get(SYNONYMS.get(stem, stem))):
                return stem
    return word


def _canon_verb(toks, vocab):
    """(canonical operation id, remaining tokens) — synonyms + positional particles; (None, toks)
    when the first token is no verb we know."""
    if not toks:
        return None, toks
    if toks[0] in ("if", "when", "once", "unless", "after", "before") and "," in " ".join(toks):
        pass                                             # handled in _strip_meta (comma clause)
    v = _stem(toks[0], vocab)
    canon = SYNONYMS.get(v, v)
    if len(toks) > 1:
        pair = (v, toks[1]) if (v, toks[1]) in PARTICLES else ((canon, toks[1]) if (canon, toks[1]) in PARTICLES else None)
        if pair is not None:
            return (vocab or {}).get(PARTICLES[pair]), toks[2:]
    op = (vocab or {}).get(canon)
    return (op, toks[1:]) if op else (None, toks)


def _unknown_verb_nudge(word, vocab) -> str:
    pool = list(vocab or {}) + list(SYNONYMS)
    close = difflib.get_close_matches(word, pool, n=4, cutoff=0.72)
    seen, verbs = set(), []
    for c in close:
        canon = (vocab or {}).get(SYNONYMS.get(c, c)) or SYNONYMS.get(c, c)
        if canon and canon not in seen:
            seen.add(canon)
            verbs.append(canon)
    hint = ""
    if verbs:
        hint = " Did you mean " + (" or ".join(verbs[:2]) if len(verbs) <= 2 else ", ".join(verbs[:-1]) + f", or {verbs[-1]}") + "?"
    fams = "; ".join(f"{k}: {', '.join(v[:4])}…" for k, v in list(VERB_FAMILIES.items())[:3])
    return f"I don't know how to '{word}'.{hint} " + _NUDGE + f" (Verb families — {fams})"


def _rewrite_use(rest, vocab):
    """`use X to VERB Y` → `VERB Y with X`; `use X on Y` is left to the use operation."""
    for i, w in enumerate(rest):
        if w == "to" and i + 1 < len(rest):
            nxt = rest[i + 1]
            canon = SYNONYMS.get(nxt, nxt)
            if (vocab or {}).get(canon) and canon != "use":
                x_words = [t for t in rest[:i] if t not in ARTICLES]
                tail = rest[i + 1:]
                return " ".join(tail + (["with"] + x_words if x_words else []))
    return None


def _trim_purpose(rest, vocab):
    """Drop a trailing purpose clause: `… to VERB …` (a verb after `to`), `… for …`, `… so …`."""
    for i, w in enumerate(rest):
        if i == 0:
            continue
        if w in PURPOSE_CUTS:
            return rest[:i]
        if w == "to" and i + 1 < len(rest):
            nxt = rest[i + 1]
            if (vocab or {}).get(SYNONYMS.get(nxt, nxt)) or nxt in META_PREFIXES:
                return rest[:i]
        if w == "in" and rest[i + 1:i + 3] == ["order", "to"]:
            return rest[:i]
    return rest


def _pronouns(rest, bindings):
    bound = (bindings or {}).get("it")
    if not bound:
        return rest
    return [_IT if w in PRONOUNS else w for w in rest]


def _split_on(words, keywords):
    for i, w in enumerate(words):
        if w in keywords:
            return words[:i], words[i + 1:]
    return words, []


def _split_relation(words):
    # A relation may be the FIRST token ("go to the cockpit" → X=None, relation, Y=dest) — the
    # split is strictly information-preserving. Multi-word relations match first.
    for i in range(len(words)):
        for n in (3, 2):
            key = tuple(words[i:i + n])
            if len(key) == n and key in MULTIWORD_RELATIONS:
                return words[:i], MULTIWORD_RELATIONS[key], words[i + n:]
        if words[i] in RELATIONS:
            return words[:i], RELATIONS[words[i]], words[i + 1:]
    return words, None, []


def _strip_trailing(words):
    words = list(words or [])
    while words and words[-1] in TRAIL_PARTICLES:
        words.pop()
    return words


# --- noun resolution ---------------------------------------------------------

def _resolve(words, reachable, owner_hint=None, bindings=None, prefer_held=False, allow_forms=False):
    """Bind a noun phrase. Form pseudo-nouns (`form:spindle`) are eligible ONLY when `allow_forms`
    (the Y slot of `into`) and never outrank a real thing."""
    if not allow_forms:
        reachable = [r for r in (reachable or []) if not r.id.startswith("form:")]
    else:
        real = [r for r in (reachable or []) if not r.id.startswith("form:")]
        hit = _resolve(words, real, owner_hint, bindings, prefer_held, allow_forms=False)
        if hit is not None:
            return hit                                    # a real entity in Y means "one like that"
    words = [w for w in (words or []) if w not in ARTICLES]
    if not words:
        return None
    if words == [_IT]:
        bound = (bindings or {}).get("it")
        return NounRef(bound[0], bound[1]) if bound else None
    words = [w for w in words if w != _IT]
    if not words:
        return None

    if owner_hint is not None:                            # "... off <owner>" → X is a part of owner
        return _part_of(owner_hint, words, reachable)     # (None → the caller's DR-24 fallback)

    whole = _match_entity(words, reachable, bindings, exact_only=True, prefer_held=prefer_held)
    if whole is not None:                                 # "canteen of water" is one thing
        return whole

    owner_ws, part_ws = _split_possessive(words)          # "seat's cover" / "cover of seat"
    if owner_ws is not None:
        ent = _match_entity(owner_ws, reachable, bindings)
        if not isinstance(ent, NounRef):
            return ent
        part = _part_of(ent.entity_id, part_ws, reachable)
        if part is not None:
            return part
        # "the pilot's jacket" — not a PART of the pilot but a thing he wears / holds
        return _match_entity([w for w in part_ws if w not in ARTICLES], reachable, bindings)

    for k in range(len(words) - 1, 0, -1):               # "OWNER PART" e.g. "11b cover", "old book cover"
        head = _match_entity(words[:k], reachable, bindings)
        if isinstance(head, NounRef):
            p = _part_of(head.entity_id, words[k:], reachable)
            if isinstance(p, NounRef):
                return p

    ent = _match_entity(words, reachable, bindings, prefer_held=prefer_held)   # whole phrase as an entity
    if ent is not None:
        return ent
    part = _match_part_anywhere(words, reachable, bindings)   # a part label across all entities
    if part is not None:
        return part
    for n in range(len(words) - 1, 0, -1):               # the longest KNOWN prefix ("copper wire in detail")
        ent = _match_entity(words[:n], reachable, bindings, prefer_held=prefer_held)
        if ent is not None:
            return ent
        part = _match_part_anywhere(words[:n], reachable, bindings)
        if part is not None:
            return part
    for n in range(1, len(words)):                       # the head noun after adjectives ("quilted engine cover")
        ent = _match_entity(words[n:], reachable, bindings, prefer_held=prefer_held)
        if ent is not None:
            return ent
        part = _match_part_anywhere(words[n:], reachable, bindings)
        if part is not None:
            return part
    return None


def _split_possessive(words):
    if "'s" in words:
        i = words.index("'s")
        return words[:i], words[i + 1:]                    # owner before, part after
    if "of" in words:
        i = words.index("of")
        return words[i + 1:], words[:i]                    # "cover of seat" → owner=seat, part=cover
    return None, None


def _singular(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith(("ches", "shes", "sses", "xes")):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _match_entity(words, reachable, bindings=None, exact_only=False, prefer_held=False):
    phrase = " ".join(words)
    forms = {phrase, " ".join(_singular(w) for w in words)}          # "branches" finds a branch
    single = {words[0], _singular(words[0])} if len(words) == 1 else set()
    exact, partial, seen = [], [], set()
    for r in reachable or []:
        names = {r.name.lower()} | {a.lower() for a in r.aliases}
        if r.ident:
            names.add(r.ident.lower())
        if r.id in seen:
            continue
        if forms & names:
            seen.add(r.id)
            exact.append(r)
        elif not exact_only and single and (single & set(r.name.lower().split())):
            seen.add(r.id)
            partial.append(r)
    hits = exact or partial                               # exact matches beat partial ones
    if not hits:
        return None
    if len(hits) == 1:
        return NounRef(hits[0].id)
    bound = (bindings or {}).get(phrase)                  # a menu pick pins the tie — LIVE hits only
    if bound:
        for h in hits:
            if h.id == bound[0]:
                return NounRef(h.id)
    if prefer_held:                                       # the tool slot: what you hold wins
        held = [h for h in hits if getattr(h, "held", False)]
        if len(held) == 1:
            return NounRef(held[0].id)
    if _identical(hits):                                  # three identical shards: any will do
        return NounRef(hits[0].id)
    return _disambig(phrase, [(h, None) for h in hits])


def _identical(hits) -> bool:
    first = hits[0]
    return all(h.name == first.name and h.ident == first.ident and tuple(h.parts) == tuple(first.parts)
               for h in hits[1:])


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


def _match_part_anywhere(words, reachable, bindings=None):
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
    bound = (bindings or {}).get(phrase)                  # a menu pick pins the tie — LIVE hits only
    if bound:
        for r, pid, _label in hits:
            if r.id == bound[0] and (bound[1] is None or pid == bound[1]):
                return NounRef(r.id, pid)
    return _disambig(phrase, [(r, (pid, label)) for r, pid, label in hits])


def _disambig(term, entries):
    opts = []
    for r, part in entries:
        who = r.name + (f" {r.ident}" if r.ident else "")
        key = (r.ident or r.name).lower()
        if part is None:
            opts.append(DisambigOption(label=who, ref=key, entity_id=r.id))
        else:
            pid, plabel = part
            opts.append(DisambigOption(label=f"{who}'s {plabel}", ref=f"{key} {plabel.lower()}",
                                       entity_id=r.id, part_id=pid))
    return Disambiguation(term=term, options=tuple(opts))


def _by_id(entity_id, reachable):
    for r in reachable or []:
        if r.id == entity_id:
            return r
    return None
