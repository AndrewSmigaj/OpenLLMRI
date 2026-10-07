"""game.typeclasses.propagator — the message propagator (DR-8/DR-13a). Shell.

Routes each pure `Event` to the OTHER characters in the room, rendered PER OBSERVER by perception
band × loudness (§14): full third-person line → direction-framed → "…is working at something." →
"A shape shifts…" → sound-only → nothing. Uses per-observer `obj.msg(...)` — **never
`msg_contents`** (the check_no_raw_output gate). The actor is excluded (they already got the
first-person `ActionResult.narration`). An unzoned room = the one-zone world: the same full line
to everyone (byte-identical to the P1 propagator). The frozen Event carries perception: the source
zone is derived from `Event.source_id` (a room-contents lookup), `data["zone"]` overrides. Voice:
`perceive.*` templates in the scenario responses win over the in-code fallbacks (Andrew-tunable).
"""
from __future__ import annotations

from world.sim import narrator
from world.sim.contracts import EventKind, PerceptionBand
from world.sim.space import perception, zones as zonemap

_VERB_PAST = {"cut": "saws at", "burn": "sets fire to", "pry": "levers at", "tear": "tears at",
              "break": "breaks", "move": "moves"}


def propagate(room, events, actor):
    if not room or not events:
        return
    observers = [o for o in room.contents if o is not actor and getattr(o, "account", None) is not None]
    if not observers:
        return
    zoned = bool(room.db.default_zone and zonemap.loaded())
    if not zoned:
        line = "\n".join(_render(ev, actor) for ev in events if _render(ev, actor))
        if line:
            for obs in observers:
                obs.msg(line)
        return

    from typeclasses.worldview import zone_of
    for obs in observers:
        ozone = zone_of(obs, room)
        lines = []
        for ev in events:
            szone = (ev.data or {}).get("zone") or _source_zone(ev, room, actor)
            res = perception.perceive(ozone, szone, loudness=ev.loudness)
            line = _render_band(ev, actor, res)
            if line:
                lines.append(line)
        if lines:
            obs.msg("\n".join(lines))


def _source_zone(ev, room, actor):
    from typeclasses.worldview import zone_of
    for o in room.contents:
        if (o.db.sim_id or o.key) == ev.source_id:
            return zone_of(o, room)
    return zone_of(actor, room) if actor is not None else None


def _render(ev, actor) -> str:
    who = getattr(actor, "key", "someone")
    verb = ev.data.get("verb") if ev.data else None
    part = ev.data.get("part") if ev.data else None
    if ev.kind == EventKind.FIRE_STATE_CHANGE:
        return f"{who} sets something alight; smoke rises."
    if verb == "move":
        to = zonemap.get(ev.data.get("to"))
        return f"{who} heads off to {to.name}." if to else f"{who} moves off."
    if verb in _VERB_PAST:
        tail = f" the {part}" if part else " something"
        return f"{who} {_VERB_PAST[verb]}{tail}."
    return f"{who} does something."


_WORD_BANDS = {  # §15: how far each voice mode carries actual WORDS (beyond: a blurred voice)
    "whisper": {PerceptionBand.SAME_ZONE},
    "say": {PerceptionBand.SAME_ZONE, PerceptionBand.ADJACENT_ZONE},
    "call": {PerceptionBand.SAME_ZONE, PerceptionBand.ADJACENT_ZONE, PerceptionBand.NEAR_VISIBLE},
    "shout": {PerceptionBand.SAME_ZONE, PerceptionBand.ADJACENT_ZONE,
              PerceptionBand.NEAR_VISIBLE, PerceptionBand.DISTANT_VISIBLE},
}


def _render_speech(ev, actor, res) -> "str | None":
    who = getattr(actor, "key", "someone")
    mode = (ev.data or {}).get("mode", "say")
    text = (ev.data or {}).get("text", "")
    where = res.direction_phrase or "nearby"
    if res.band is PerceptionBand.SAME_ZONE:
        return f'{who} {mode}s, "{text}"'
    if res.audible and res.band in _WORD_BANDS.get(mode, ()):
        return f'{where[0].upper()}{where[1:]}, {who} {mode}s, "{text}"'
    if res.audible:
        return f"A voice carries from somewhere {where}, but the words blur in the wind."
    return None


def _render_band(ev, actor, res) -> "str | None":
    """The §14 graded ladder. Templates `perceive.<band>` may override the fallbacks."""
    if ev.kind == EventKind.SPEECH:
        return _render_speech(ev, actor, res)
    band = res.band
    if band is PerceptionBand.OUT_OF_SIGHT:
        return None
    if band is PerceptionBand.SAME_ZONE:
        return _render(ev, actor)
    who = getattr(actor, "key", "someone")
    where = res.direction_phrase or "nearby"
    state = {"who": who, "where": where, "line": _render(ev, actor)}
    if band is PerceptionBand.ADJACENT_ZONE:
        t = narrator.get("perceive.adjacent") or "{Where}, {line_lower}"
        return _fill(t, state)
    if band is PerceptionBand.NEAR_VISIBLE:
        t = narrator.get("perceive.near") or "{Where}, {who} is working at something."
        return _fill(t, state)
    if band is PerceptionBand.DISTANT_VISIBLE:
        t = narrator.get("perceive.distant") or "Farther {where_bare}, someone is moving."
        return _fill(t, state)
    if band is PerceptionBand.BARELY_VISIBLE:
        t = narrator.get("perceive.barely") or "A shape shifts {where}, then is gone."
        return _fill(t, state)
    t = narrator.get("perceive.audible") or "A sound carries from somewhere {where}."
    return _fill(t, state)


def _fill(template, state):
    where = state["where"]
    line = state["line"]
    return narrator.render(template, {
        **state,
        "Where": where[0].upper() + where[1:],
        "where_bare": where.removeprefix("to the "),
        "line_lower": line[0].lower() + line[1:] if line else "",
    })
