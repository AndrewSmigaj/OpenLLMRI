"""world.sim.operations.handlers.examine — inspect an object's systemic state (D10). Pure.

`examine X` renders X's materials, visible condition, and its PARTS **with their identifiers** (so a
player can reference them — user refinement), from the EntityState. Returns a SUCCESS description with
no effects. The `detail` arg is the perception context — always 'full' in P1; DR-13 later supplies a
band-limited context here WITHOUT changing the signature (the examine detail-context seam).
"""
from __future__ import annotations

from world.sim.contracts import ActionResult, Resolution
from world.sim.operations._helpers import resolve_ref

VERBS = ("examine", "inspect", "x", "study", "check")


def resolve_examine(attempt, world, materials, detail: str = "full"):
    ent, _ = resolve_ref(attempt.X, world)
    if ent is None:
        return None

    ident = (ent.state or {}).get("ident")
    head = f"{ent.name}" + (f" [{ident}]" if ident else "")
    lines = [head + ":"]
    if ent.materials:
        lines.append("  Made of " + ", ".join(ent.materials) + ".")
    cond = _condition(ent)
    if cond:
        lines.append("  " + cond)
    if ent.parts:
        lines.append("  Parts:")
        for p in ent.parts:
            lines.append(f"    - {p.id} ({p.material}, {p.attachment})")
    else:
        lines.append("  No separable parts.")
    return ActionResult(Resolution.SUCCESS, narration="\n".join(lines), tier="op:examine")


def _condition(ent) -> str:
    """A short read of the systemic state flags the operations set — so a player can SEE what they did
    (lit it, doused it, wrapped it, bent it, tied it). Legibility is what makes the world feel reactive."""
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
