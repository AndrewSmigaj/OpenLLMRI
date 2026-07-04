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


def compose_scene(ents, perceived=None) -> str:
    """The {things} slot of a room look. `perceived` (DR-13a, optional) maps entity id →
    PerceptionResult; None = the one-zone world, exactly the pre-P3 render (locked by test).
    Same-zone entities render with full salience prose; farther visible bands group into
    direction-framed graded lines (§14: clear → summarized → vague → shape); OUT_OF_SIGHT and
    AUDIBLE_ONLY are absent (a static look is visual)."""
    if perceived is not None:
        from world.sim.contracts import PerceptionBand
        same = [e for e in ents
                if perceived.get(e.id) is None
                or perceived[e.id].band is PerceptionBand.SAME_ZONE]
        away = [(e, perceived[e.id]) for e in ents
                if perceived.get(e.id) is not None
                and perceived[e.id].band is not PerceptionBand.SAME_ZONE
                and perceived[e.id].visible]
        out = [compose_scene(same)] if same else []
        out.extend(_graded_groups(away))
        return " ".join(s for s in out if s)

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


def _graded_groups(away) -> list:
    """Direction-framed graded lines for visible-but-not-here entities, grouped by
    (band, direction), deterministic. §14: clear → summarized → vague → shape-or-motion."""
    from world.sim.contracts import PerceptionBand
    order = {PerceptionBand.ADJACENT_ZONE: 0, PerceptionBand.NEAR_VISIBLE: 1,
             PerceptionBand.DISTANT_VISIBLE: 2, PerceptionBand.BARELY_VISIBLE: 3}
    groups = {}
    for ent, res in away:
        groups.setdefault((order.get(res.band, 3), res.direction_phrase), []).append(ent)
    out = []
    for (band_ix, dphrase) in sorted(groups):
        ents = sorted(groups[(band_ix, dphrase)], key=lambda e: e.name)
        where = dphrase or "nearby"
        if band_ix == 0:      # clear (not detailed): noun phrases — a zone away, prominent things
            items = []        # lose their vivid sentence phrasing (§14: detail is a SAME_ZONE gift)
            for name, group in _by_name(ents):
                if len(group) > 1:
                    items.append(f"{_count_word(len(group))} {name}s")
                    continue
                entry = _entry(group[0]) or {}
                if entry.get("salience", "ordinary") == "prominent":
                    items.append(_article(name))
                else:
                    items.append(_pick(entry.get("scene"), group[0].state) or _article(name))
            out.append(_sentence(f"{where[0].upper()}{where[1:]}: {', '.join(items)}"))
        elif band_ix == 1:    # summarized: articled names, duplicates counted
            items = [f"{_count_word(len(g))} {n}s" if len(g) > 1 else _article(n)
                     for n, g in _by_name(ents)]
            out.append(f"Farther {where.removeprefix('to the ')}, "
                       f"you can make out {', '.join(items)}.")
        elif band_ix == 2:    # vague: count only
            n = len(ents)
            if n > 1:
                out.append(f"Farther {where.removeprefix('to the ')}, "
                           f"{_count_word(n)} shapes in the snow, hard to make out.")
            else:
                out.append(f"Farther {where.removeprefix('to the ')}, "
                           f"a shape in the snow, hard to make out.")
        else:                 # shape or motion
            out.append(f"Something — maybe more — {where}, almost lost in the snow.")
    return out


def _by_name(ents) -> list:
    grouped = {}
    for e in ents:
        grouped.setdefault(e.name, []).append(e)
    return sorted(grouped.items())


def describe(ent) -> str:
    """The ONE detailed renderer for `look at X` / `examine X`: authored state-conditioned prose,
    the systemic condition woven in, and parts as physical sentences with their names intact (so
    the player learns what to type) — attachments as phrases, never `(material, attachment)` data."""
    if "zone" in (ent.tags or []):                 # a zone pseudo-entity: its survey prose
        from world.sim.space import zones as zonemap
        z = zonemap.get((ent.state or {}).get("zone"))
        return f"{ent.name} — {z.look}" if z and z.look else ent.name

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
    st = ent.state or {}
    worn = st.get("worn") or []
    if worn:
        lines.append(f"{ent.name[0].upper()}{ent.name[1:]} wears {_and_list(worn)}.")
    if st.get("open") or st.get("searched"):       # DR-24: revealed contents weave in
        inside = st.get("contents") or []
        if inside:
            lines.append(f"Inside: {_and_list(inside)}.")
        elif st.get("container"):
            lines.append("It's empty.")
    if ent.parts:
        woven = "; ".join(f"its {p.id} {attachment_phrase(p.attachment, 'hint')}"
                          for p in ent.parts)
        lines.append(f"You can make out {woven}.")
    return " ".join(lines)


def _and_list(names) -> str:
    items = [_article(n) for n in names]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def read_text(ent) -> "str | None":
    """The authored, state-conditioned `read` entry for an entity (None = nothing written)."""
    entry = _entry(ent)
    return _pick((entry or {}).get("read"), ent.state) if entry else None


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
    if st.get("broken"):
        bits.append("broken")
    if st.get("fuel_soaked"):
        bits.append("reeking of avgas")
    if st.get("dead"):
        bits.append("lifeless")
    t = st.get("temperature_c")
    if isinstance(t, (int, float)) and not isinstance(t, bool) and t <= 0:
        bits.append("frost-stiff")
    return ("It's " + ", ".join(bits) + ".") if bits else ""
