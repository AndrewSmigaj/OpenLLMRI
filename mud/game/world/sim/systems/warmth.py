"""world.sim.systems.warmth — warmth & cold exposure (§32). Pure. P5 builds the exposure clock;
DR-25 lands the first real pieces NOW: wearability + the clothing warmth score.

Warmth from fire PLUS windbreak/shelter/insulation/huddling/body-heat. Includes the **no-materials
warmth floor**: a competent party survives one night without fire, so fire-failure is recoverable
(improvement #4). See systems/README.md.

DR-25 math: an item contributes `round(insulation × min(mass_g, 3000))` "insulation-grams" —
an INTENSIVE property scaled by an EXTENSIVE mass, then summed. This is not ordinal-summing
(DR-04/DR-11 hold): a 100 g strip warms less than a 700 g blanket of the same wool. Wearability
is DERIVED from materials (Andrew: "you should be able to wear everything" that physically wears)
— never a whitelist. Thresholds and bands are tunable content-adjacent constants.
"""
from __future__ import annotations

from world.sim.presentation import _and_list

WEARABLE_TAGS = frozenset({"fabric", "flexible", "soft", "insulating"})
BLOCKED_TAGS = frozenset({"liquid", "edible", "food"})
_MAX_WEAR_G = 4000
_MASS_CAP_G = 3000

BANDS = ((0, "bare to the wind"), (250, "thinly covered"), (700, "adequately dressed"),
         (1500, "well bundled"), (2600, "swaddled like a survival-manual illustration"))


def _mats(ent, materials):
    return [m for m in (materials.get(mid) for mid in (ent.materials or [])) if m is not None]


def wearable(ent, materials) -> bool:
    """Does this physically wear? Flexible/fabric/soft/insulating stuff light enough to drape —
    the blanket as a cloak, a freed seat cover, socks; never fixtures, liquids or lunch."""
    if (ent.state or {}).get("fixed") or ent.mass_g > _MAX_WEAR_G:
        return False
    mats = _mats(ent, materials)
    if not mats:
        return False
    tags = set().union(*(m.tags for m in mats))
    return bool(tags & WEARABLE_TAGS) and not (tags & BLOCKED_TAGS)


def insulation_units(ent, materials) -> int:
    """One worn item's contribution: best material insulation × capped mass."""
    mats = _mats(ent, materials)
    if not mats:
        return 0
    ins = max(float(m.props.get("insulation", 0.0)) for m in mats)
    return round(ins * min(int(ent.mass_g or 0), _MASS_CAP_G))


def clothing_warmth(worn_ents, materials) -> int:
    return sum(insulation_units(e, materials) for e in worn_ents)


def warmth_band(units: int) -> str:
    word = BANDS[0][1]
    for floor, name in BANDS:
        if units >= floor:
            word = name
    return word


def worn_summary(worn_ents, materials) -> str:
    """The shared self-view suffix — one function so `look at me` ≡ `examine me` byte-for-byte."""
    band = warmth_band(clothing_warmth(worn_ents, materials))
    if not worn_ents:
        return f"You are wearing nothing. You are {band}."
    names = _and_list(sorted(e.name for e in worn_ents))
    return f"You are wearing {names}. You are {band}."
