"""Whiteout — the slice's signature narration templates (DR-09; grows toward ~50 in P1.6).

Deterministic templates filled from state by world.sim.narrator. Tunable content — Andrew adjusts the
voice after P1. Placeholders: {tool} {target} {part} {output} {attachment} {smoke}.
"""

RESPONSES = {
    # cut ---------------------------------------------------------------------
    "cut.free": "You work the {tool} through the {target}'s {part}; the stitching parts and it comes "
                "away — a {output}.",
    "cut.divide": "You draw the {tool} across the {target}, parting it into two ragged pieces.",
    "cut.slash_fixed": "You slash at the {part}, scoring it — but it's {attachment} fast and won't come "
                       "free this way.",
    "cut.too_dull": "The {tool} skates off the {target} without biting. You'd need a keener edge.",
    # burn --------------------------------------------------------------------
    "burn.success": "The {target} catches, curls, and burns down to ash, {smoke} coiling upward.",
    "burn.no_flame": "You've nothing to set the {target} alight with.",
    "burn.wont_catch": "The {target} smoulders sullenly and refuses to catch.",
    # pry ---------------------------------------------------------------------
    "pry.free": "You lever the {tool} under the {part} and heave; it pops free — a {output}.",
    "pry.no_leverage": "You strain, but the {tool} can't shift the {part}. You need more leverage.",
    # tear --------------------------------------------------------------------
    "tear.free": "You get a grip on the {target}'s {part} and haul; the seams give and it rips away — a "
                 "{output}.",
    "tear.strips": "You worry at the {target} and tear it into long ragged strips.",
    "tear.too_tough": "The {target} holds — too tough to tear with bare hands. A blade might bite.",
    "tear.attached": "You can't rip the {part} loose; it's {attachment} fast.",
    "tear.composite": "The {target} is more than one piece — tear at a specific part.",
    # break -------------------------------------------------------------------
    "break.shatter": "You smash the {target}; it shatters into glittering shards.",
    "break.snap": "You brace and heave — the {target} cracks and snaps apart.",
    "break.no_force": "You strain against the {target} with {tool}, but can't bring enough force to break "
                      "it.",
    "break.too_tough": "The {target} takes the blow and shrugs it off — too tough to break. Try cutting "
                       "or bending it.",
    "break.composite": "The {target} is built of parts — smash a specific one.",
    # bend --------------------------------------------------------------------
    "bend.shaped": "You work the {target} back and forth until it takes a new bend.",
    "bend.too_stiff": "The {target} won't give — far too stiff to bend by hand.",
    # generic -----------------------------------------------------------------
    "__fallback__": "Something shifts, but not the way you meant.",
}
