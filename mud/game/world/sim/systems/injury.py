"""world.sim.systems.injury — wounds (§35). Pure. The exposure/bleeding clock is step 3 (time &
stakes); DR-25a lands the DATA now: a character's `state['wounds']` is a list of
`{kind, part, severity (1–3), bleeding (g/min, 0 = none), bound?, note}` set by the crash draw
(`scenarios/<s>/characters.py`) and later by the injury verbs. `wounds_summary` is the self-view line.
"""
from __future__ import annotations


def wounds(ent) -> list:
    return [w for w in ((ent.state or {}).get("wounds") or []) if hasattr(w, "get") and w.get("kind")]


def wounds_summary(ent) -> str:
    """'Your forearm is cut and bleeding; your ankle is sprained.' — or '' when unhurt."""
    ws = wounds(ent)
    if not ws:
        return ""
    bits = []
    for w in ws:
        part = w.get("part") or "body"
        kind = w.get("kind", "hurt")
        desc = {"cut": "cut", "sprain": "sprained", "concussion": "throbbing", "bruised ribs": "bruised",
                "burn": "burned", "frostbite": "frostbitten", "shock": "shaky"}.get(kind, kind)
        line = f"your {part} is {desc}" if part not in ("none", "body") else f"you are {desc}"
        if w.get("bleeding") and not w.get("bound"):
            line += " and bleeding"
        elif w.get("bound"):
            line += ", bound"
        bits.append(line)
    text = "; ".join(bits)
    return text[0].upper() + text[1:] + "."
