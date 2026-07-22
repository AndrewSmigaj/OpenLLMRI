"""world.sim.presentation — scene-as-prose composition + the unified thing renderer. Pure.

The scene composer turns a zone's EntityStates into prose built from SPACES (the scene-space model,
superseding the DR-23 salience-tier list): each object sits in a space (the floor, the footwell,
overhead), and each space renders as a framed sentence describing POSITION, not history. A space
describes CHARACTER, never a full inventory — loose things show, but discovery of what is INSIDE
things stays a `look at` / `search` / `open` (DR-24 containment). Empty spaces render nothing;
a space names at most `cap` things and absorbs the rest into an overflow phrase. `describe()` is the
ONE detailed renderer behind both `look at X` and `examine X` (synonyms by design). Appearance
phrases + the space table are loaded-once scenario content (state-conditioned, Andrew-tunable).

The banded cross-zone view (DR-13a §14) is a separate concern: a zone away, detail is lost, so those
still grade by salience into direction-framed lines — detail is a same-zone gift. Fallbacks guarantee
EVERY object renders (unzoned world / un-authored zone → a plain spaceless render). Attachments
render physically via the DR-09a hint phrases ("held by stitching"), never as data.
"""
from __future__ import annotations

from world.sim.operations._helpers import attachment_phrase

_APPEARANCE: dict = {}

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


def _article(phrase: str) -> str:
    low = phrase.lower()
    if low.startswith(("the ", "a ", "an ", "some ")):
        return phrase                     # already determined ("the pilot") — never "a the pilot"
    if low[:1] in "aeiou":
        return f"an {phrase}"
    return f"a {phrase}"


def _bare_or_article(ent) -> str:
    """`_article`, but a mass/plural-named object ('oxygen masks', 'dry grass') marked `mass` in its
    appearance reads wrong with a/an — bare its name instead ('you can make out oxygen masks')."""
    entry = _entry(ent)
    if entry and entry.get("mass"):
        return ent.name
    return _article(ent.name)


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

    return _render_zone(ents)


def _render_zone(ents) -> str:
    """Group same-zone entities into their spaces and render each space as framed prose, in survey
    order, omitting empties. An unzoned / un-authored zone (no space table) degrades to a plain
    spaceless render so every object still shows."""
    from world.sim.space import spaces as spacemap
    zone = _zone_of(ents)
    layout = spacemap.for_zone(zone) if zone else ()
    if not layout:
        return _render_spaceless(ents)
    by_space = {}
    for ent in ents:
        by_space.setdefault(_space_of(ent, layout), []).append(ent)
    out = []
    for sp in layout:                          # already in survey order
        here = by_space.get(sp.id)
        if here:                               # an empty space renders NOTHING
            out.extend(_render_space(sp, here))
    return " ".join(s for s in out if s)


def _zone_of(ents):
    """The single zone these entities share (a base render is always one zone); None if they carry
    no zone (the unzoned one-zone world) or disagree — either way, a spaceless render."""
    zones = {(e.state or {}).get("zone") for e in ents}
    zones.discard(None)
    return next(iter(zones)) if len(zones) == 1 else None


def _space_of(ent, layout) -> str:
    """Where an entity sits: an explicit `state['space']` (a player drop), else its appearance home,
    else the zone's default (or the first space). Always resolves to a space that exists here."""
    ids = {sp.id for sp in layout}
    sid = (ent.state or {}).get("space") or (_entry(ent) or {}).get("space")
    if sid in ids:
        return sid
    return next((sp.id for sp in layout if sp.default), layout[0].id)


def _render_space(sp, ents, uncapped=False) -> list:
    """One space → its lines. Anchor objects lead as their own sentences (they DEFINE the space —
    the pilot, the radio); the rest fill the space's frame with number agreement; identical deriveds
    keep their authored aggregate sentence. A room look caps the frame and absorbs the rest into an
    overflow phrase; `uncapped=True` (the `look at <space>` path) names every thing instead."""
    anchors = [e for e in ents if (_entry(e) or {}).get("anchor")]
    rest = [e for e in ents if not (_entry(e) or {}).get("anchor")]
    lines = [_sentence(_scene_phrase(a))
             for a in sorted(anchors, key=lambda e: (_order(e), e.name))]
    items = []                                    # (order, name, phrase, plural?)
    for name, group in _by_name(rest):
        n, entry = len(group), _entry(group[0])
        if n > 1 and entry and entry.get("aggregate"):
            items.append((_order(group[0]), name, entry["aggregate"].format(count=_count_word(n)), True))
        elif n > 1:
            items.append((_order(group[0]), name, f"{_count_word(n)} {_plural(name)}", True))
        else:
            items.append((_order(group[0]), name, _scene_phrase(group[0]), False))
    if items:
        items.sort()
        phrases = [p for _o, _n, p, _pl in items]
        if not uncapped and sp.cap and len(phrases) > sp.cap and sp.overflow:
            phrases = phrases[:sp.cap] + [sp.overflow]
        be = "is" if (len(phrases) == 1 and not items[0][3]) else "are"    # a lone aggregate is plural
        lines.append(sp.frame.format(be=be, items=_and_join(phrases)) if sp.frame
                     else _sentence(_and_join(phrases)))
    return lines


def _plural(name: str) -> str:
    """A forgiving plural for the count fallback ('branch'→'branches', not 'branchs')."""
    if name.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    if name.endswith("y") and name[-2:-1].lower() not in "aeiou":
        return name[:-1] + "ies"
    return name + "s"


def look_space(zone, alias, ents) -> "str | None":
    """`look at <space>`: the named space rendered UNCAPPED — every loose thing in it, no overflow.
    None if `alias` names no space in `zone` (the shell then falls through to a normal examine)."""
    from world.sim.space import spaces as spacemap
    sid = spacemap.resolve_space(zone, alias)
    if sid is None:
        return None
    sp = spacemap.get(zone, sid)
    layout = spacemap.for_zone(zone)
    here = [e for e in ents if _space_of(e, layout) == sid]
    if not here:
        return "Nothing catches your eye there."
    return " ".join(s for s in _render_space(sp, here, uncapped=True) if s)


def _render_spaceless(ents) -> str:
    """No authored spaces (unzoned one-zone world / un-authored zone): render each object's scene
    phrase as its own sentence, aggregation-aware, deterministically ordered. No frames, no tiers."""
    lines = []
    for name, group in _by_name(ents):
        entry = _entry(group[0])
        if len(group) > 1 and entry and entry.get("aggregate"):
            phrase = entry["aggregate"].format(count=_count_word(len(group)))
        elif len(group) > 1:
            phrase = f"{_count_word(len(group))} {_plural(name)}"
        else:
            phrase = _scene_phrase(group[0])
        lines.append((_order(group[0]), name, _sentence(phrase)))
    return " ".join(s for _o, _n, s in sorted(lines))


def _order(ent) -> int:
    return (_entry(ent) or {}).get("order", 50)


def _scene_phrase(ent) -> str:
    return _pick((_entry(ent) or {}).get("scene"), ent.state) or _article(ent.name)


def _and_join(parts) -> str:
    """Join pre-formed phrases with a serial 'and' (no re-articling — the phrases already read)."""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + f" and {parts[-1]}"


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
                    items.append(f"{_count_word(len(group))} {_plural(name)}")
                    continue
                entry = _entry(group[0]) or {}
                # an anchor's `scene` is a full SENTENCE (a same-zone lead) — a zone away it must
                # collapse to its bare name, never drop a sentence into this comma list.
                if entry.get("salience", "ordinary") == "prominent" or entry.get("anchor"):
                    items.append(_bare_or_article(group[0]))
                else:
                    items.append(_pick(entry.get("scene"), group[0].state) or _bare_or_article(group[0]))
            out.append(_sentence(f"{where[0].upper()}{where[1:]}: {', '.join(items)}"))
        elif band_ix == 1:    # summarized: articled names, duplicates counted
            items = [f"{_count_word(len(g))} {_plural(n)}" if len(g) > 1 else _bare_or_article(g[0])
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
