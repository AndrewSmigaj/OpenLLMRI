"""world.sim.systems.warmth — warmth & cold exposure (§32). Pure. P5 builds the exposure clock;
DR-25 landed wearability + the clothing warmth score; DR-25a (players-and-kit.md, 2026-09-07)
lands the CLOTHING SYSTEM v2: coverage by body REGION, the outer shell's WIND, WATERPROOF, and the
WET fraction (soaked down is worth nothing) — the numbers the exposure clock (step 3) will spend.

DR-25 math (unchanged): an item contributes `round(insulation × min(mass_g, 3000))` "insulation-
grams" — an INTENSIVE property scaled by an EXTENSIVE mass, then summed. v2 multiplies each item by
its wet fraction, distributes it over the regions it `covers` (an item with no `covers` counts as
general warmth, as before), and reads the strongest `wind` over each region as the shell. Wearability
stays DERIVED from materials — never a whitelist. Thresholds and bands are tunable content.
"""
from __future__ import annotations

from world.sim.presentation import _and_list

WEARABLE_TAGS = frozenset({"fabric", "flexible", "soft", "insulating"})
BLOCKED_TAGS = frozenset({"liquid", "edible", "food"})
_MAX_WEAR_G = 4000
_MASS_CAP_G = 3000

BANDS = ((0, "bare to the wind"), (250, "thinly covered"), (700, "adequately dressed"),
         (1500, "well bundled"), (2600, "swaddled like a survival-manual illustration"))

# the body's regions and the share of heat each loses when bare (sums to 1.0)
REGIONS = {"head": 0.20, "torso": 0.35, "arms": 0.10, "hands": 0.10, "legs": 0.15, "feet": 0.10}
# material → the wind a shell of it stops (used when an item declares no `wind`)
_WIND_BY_MATERIAL = {"nylon_shell": 0.9, "rubber": 0.9, "leather": 0.6, "denim": 0.4, "wool": 0.3,
                     "synthetic_fabric": 0.4, "fleece": 0.2, "cotton_cloth": 0.15, "insulation_batting": 0.2}
# how much of its mass in water makes an item worthless (down soaks and dies; wool forgives)
_SOAK_FRACTION = {"down": 0.2, "cotton_cloth": 0.5, "denim": 0.5, "wool": 1.2, "fleece": 0.9,
                  "insulation_batting": 0.6, "synthetic_fabric": 0.7, "leather": 0.8, "nylon_shell": 2.0}


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


def wet_fraction(ent, materials) -> float:
    """1.0 dry → 0.0 soaked: how much of an item's insulation survives its water (grams in
    `state['wet']`; a bare `wet: True` counts as half-soaked)."""
    st = ent.state or {}
    wet = st.get("wet") or st.get("wetness") or 0
    if wet is True:
        wet = max(1, int(ent.mass_g or 0) // 4)
    try:
        wet_g = float(wet)
    except (TypeError, ValueError):
        return 1.0
    if wet_g <= 0:
        return 1.0
    mats = _mats(ent, materials)
    frac = min((_SOAK_FRACTION.get(m.id, 0.7) for m in mats), default=0.7)
    ruin_g = max(1.0, frac * float(ent.mass_g or 1))
    return max(0.0, 1.0 - wet_g / ruin_g)


def insulation_units(ent, materials) -> int:
    """One worn item's contribution: best material insulation × capped mass × the wet fraction."""
    mats = _mats(ent, materials)
    if not mats:
        return 0
    ins = max(float(m.props.get("insulation", 0.0)) for m in mats)
    return round(ins * min(int(ent.mass_g or 0), _MASS_CAP_G) * wet_fraction(ent, materials))


def wind_of(ent, materials) -> float:
    """How much wind this item stops (an authored `wind`, else the outer material's)."""
    st = ent.state or {}
    if isinstance(st.get("wind"), (int, float)) and not isinstance(st.get("wind"), bool):
        return float(st["wind"])
    return max((_WIND_BY_MATERIAL.get(m.id, 0.2) for m in _mats(ent, materials)), default=0.0)


def covers(ent) -> tuple:
    return tuple(r for r in ((ent.state or {}).get("covers") or ()) if r in REGIONS)


def clothing_warmth(worn_ents, materials) -> int:
    """The total warmth score (insulation-grams, wet-adjusted) — the band's input."""
    return sum(insulation_units(e, materials) for e in worn_ents)


def regional(worn_ents, materials) -> dict:
    """Per region: {'units': insulation-grams covering it, 'wind': the best shell over it,
    'bare': no item covers it}. Items with no `covers` spread their units over torso/arms."""
    out = {r: {"units": 0, "wind": 0.0, "bare": True} for r in REGIONS}
    for e in worn_ents:
        units = insulation_units(e, materials)
        regs = covers(e) or ("torso", "arms")
        w = wind_of(e, materials)
        for r in regs:
            out[r]["units"] += units
            out[r]["wind"] = max(out[r]["wind"], w)
            if covers(e):
                out[r]["bare"] = False
    return out


def exposure_fraction(worn_ents, materials) -> float:
    """0.0 (fully shelled, thickly insulated) → 1.0 (naked): the share of the body's heat loss the
    clothing does NOT stop — the number the exposure clock multiplies the weather by."""
    reg = regional(worn_ents, materials)
    total = 0.0
    for r, share in REGIONS.items():
        units = reg[r]["units"]
        insulated = min(1.0, units / 600.0)             # ~600 insulation-grams on a region = fully insulated
        shelled = reg[r]["wind"]
        stop = 0.6 * insulated + 0.4 * shelled * min(1.0, 0.3 + insulated)
        total += share * (1.0 - stop)
    return round(total, 3)


def bare_regions(worn_ents, materials) -> list:
    reg = regional(worn_ents, materials)
    return [r for r in REGIONS if reg[r]["bare"]]


def fine_work_ok(worn_ents) -> bool:
    """Mittens can't tie a knot or strike a match (take them off; pay the cold)."""
    return not any((e.state or {}).get("fine_work") is False for e in worn_ents)


def _plain_list(names) -> str:
    names = list(names)
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + f" and {names[-1]}"


def warmth_band(units: int) -> str:
    word = BANDS[0][1]
    for floor, name in BANDS:
        if units >= floor:
            word = name
    return word


def self_view(ent, worn_ents, materials) -> str:
    """THE self-view (`look at me` ≡ `examine me`, byte for byte): what you wear, the warmth band,
    what is bare or soaked, and your wounds (DR-25a). One pure helper behind both shell paths."""
    from world.sim.systems import injury
    line = worn_summary(worn_ents, materials)
    hurt = injury.wounds_summary(ent)
    return f"{line} {hurt}" if hurt else line


def worn_summary(worn_ents, materials) -> str:
    """The shared self-view suffix — one function so `look at me` ≡ `examine me` byte-for-byte.
    v2 adds what is bare and what is soaked, when anything is worn at all."""
    band = warmth_band(clothing_warmth(worn_ents, materials))
    if not worn_ents:
        return f"You are wearing nothing. You are {band}."
    names = _and_list(sorted(e.name for e in worn_ents))
    line = f"You are wearing {names}. You are {band}."
    declared = [e for e in worn_ents if covers(e)]
    if declared:
        bare = bare_regions(worn_ents, materials)
        if bare:
            line += f" Your {_plain_list(bare)} {'are' if len(bare) > 1 else 'is'} bare."
        soaked = sorted(e.name for e in worn_ents if wet_fraction(e, materials) < 0.5)
        if soaked:
            line += f" Your {_plain_list(soaked)} {'are' if len(soaked) > 1 else 'is'} soaked through."
        if not fine_work_ok(worn_ents):
            line += " Your hands are mittened — no fine work until they come off."
    return line
