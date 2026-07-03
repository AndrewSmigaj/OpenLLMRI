"""world.sim.presentation — scene-as-prose composition + the unified thing renderer (DR-23). Pure.

The scene composer turns the room's EntityStates into a few prose sentences — salience-WEIGHTED,
never a list, never hiding (everything present is mentioned, so the world stays navigable while
discovery stays intact). `describe()` is the ONE detailed renderer behind both `look at X` and
`examine X` (they are synonyms by design). Appearance phrases are loaded-once scenario content
(`load_appearance`, mirroring the narrator's registry): state-conditioned, Andrew-tunable.
Fallbacks guarantee EVERY object renders — derived scraps included; nothing is ever invisible.

Attachments render physically via the DR-09a hint phrases ("held by stitching"), never as data.
"""
from __future__ import annotations

from world.sim.operations._helpers import attachment_phrase

_APPEARANCE: dict = {}

_TIERS = ("prominent", "ordinary", "subtle")
_COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def load_appearance(appearance: dict) -> None:
    """Install the appearance registry (`sim_id or display-name -> entry`). Replaces any prior set."""
    _APPEARANCE.clear()
    _APPEARANCE.update(appearance)


def _entry(ent):
    """The appearance entry for an entity: exact sim_id first, then display name (derived objects
    share name-keyed entries: three 'glass shard's, one entry), else None (generic fallback)."""
    return _APPEARANCE.get(ent.id) or _APPEARANCE.get(ent.name)


def _pick(variants, state):
    """The first (condition, phrase) whose condition is a subset of `state`; `None` = the default."""
    for cond, phrase in variants or ():
        if cond is None or all((state or {}).get(k) == v for k, v in cond.items()):
            return phrase
    return None


def _salience(entry, state):
    base = (entry or {}).get("salience", "ordinary")
    for cond, tier in (entry or {}).get("promote", ()):
        if all((state or {}).get(k) == v for k, v in cond.items()):
            return tier
    return base


def _article(phrase: str) -> str:
    low = phrase.lower()
    if low.startswith(("the ", "a ", "an ", "some ")):
        return phrase                     # already determined ("the pilot") — never "a the pilot"
    if low[:1] in "aeiou":
        return f"an {phrase}"
    return f"a {phrase}"


def _count_word(n: int) -> str:
    return _COUNT_WORDS.get(n, "several")


def compose_scene(ents) -> str:
    """The {things} slot of a room look: prominent sentences, then the ordinary and subtle groups
    framed as prose. Identical names aggregate (an authored `aggregate` phrase, or a counted item).
    Deterministic: sorted by (tier, authored order, name)."""
    buckets = {t: [] for t in _TIERS}
    by_name = {}
    for ent in ents:
        by_name.setdefault(ent.name, []).append(ent)

    for name in sorted(by_name):
        group = by_name[name]
        ent = group[0]
        entry = _entry(ent)
        tier = _salience(entry, ent.state)
        order = (entry or {}).get("order", 50)
        if len(group) > 1 and entry and entry.get("aggregate"):
            phrase = entry["aggregate"].format(count=_count_word(len(group)))
            buckets[tier].append((order, name, _sentence(phrase), True))
        elif len(group) > 1:
            buckets[tier].append((order, name, f"{_count_word(len(group))} {name}s", False))
        else:
            phrase = _pick((entry or {}).get("scene"), ent.state) or _article(name)
            buckets[tier].append((order, name, phrase, tier == "prominent"))

    frames = _APPEARANCE.get("_frames", {})
    out = []
    for _order, _name, phrase, _is_sentence in sorted(buckets["prominent"]):
        out.append(_sentence(phrase))

    for tier, default_frame in (("ordinary", "Scattered around: {items}."),
                                ("subtle", "Among the debris: {items}.")):
        sentences, items = [], []
        for _order, _name, phrase, is_sentence in sorted(buckets[tier]):
            (sentences if is_sentence else items).append(_sentence(phrase) if is_sentence else phrase)
        if items:
            frame = frames.get(tier, default_frame)
            out.append(frame.format(items=", ".join(items)))
        out.extend(sentences)

    return " ".join(out)


def _sentence(phrase: str) -> str:
    return phrase if phrase.endswith((".", "!", "?")) else phrase + "."


def describe(ent) -> str:
    """The ONE detailed renderer for `look at X` / `examine X`: authored state-conditioned prose,
    the systemic condition woven in, and parts as physical sentences with their names intact (so
    the player learns what to type) — attachments as phrases, never `(material, attachment)` data."""
    ident = (ent.state or {}).get("ident")
    head = ent.name + (f" [{ident}]" if ident else "")
    entry = _entry(ent)

    prose = _pick((entry or {}).get("examine"), ent.state)
    if prose is None:
        mats = " and ".join(m.replace("_", " ") for m in ent.materials) or "no material in particular"
        prose = f"Nothing remarkable — {mats}, {ent.mass_g} grams of it."

    lines = [f"{head} — {prose}"]
    cond = _condition(ent)
    if cond:
        lines.append(cond)
    if ent.parts:
        woven = "; ".join(f"its {p.id} {attachment_phrase(p.attachment, 'hint')}"
                          for p in ent.parts)
        lines.append(f"You can make out {woven}.")
    return " ".join(lines)


def _condition(ent) -> str:
    """A short read of the systemic state flags the operations set — legibility: the player SEES
    what they (or others) did. (Moved here from the examine handler; same flags.)"""
    st = ent.state or {}
    bits = []
    if st.get("lit"):
        bits.append("alight")
    if st.get("wet") or st.get("wetness"):
        bits.append("soaked")
    if st.get("insulated"):
        bits.append("bundled for warmth")
    elif st.get("wrapped"):
        bits.append("wrapped up")
    if st.get("shape") == "bent":
        bits.append("bent out of true")
    if st.get("secured") or st.get("tied_to"):
        bits.append("tied off")
    if st.get("damage"):
        bits.append("battered")
    if st.get("dead"):
        bits.append("lifeless")
    t = st.get("temperature_c")
    if isinstance(t, (int, float)) and not isinstance(t, bool) and t <= 0:
        bits.append("frost-stiff")
    return ("It's " + ", ".join(bits) + ".") if bits else ""
