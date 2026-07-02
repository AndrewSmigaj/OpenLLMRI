"""Whiteout — the slice's signature narration templates (DR-09; grows toward ~50 in P1.6).

Deterministic templates filled from state by world.sim.narrator. Tunable content — Andrew adjusts the
voice after P1. Placeholders: {tool} {target} {part} {output} {attachment} {smoke}.
"""

RESPONSES = {
    # cut ---------------------------------------------------------------------
    "cut.free": "You work {tool} through the {target}'s {part}; the stitching parts and it comes "
                "away — a {output}.",
    "cut.divide": "You draw {tool} across the {target}, parting it into two ragged pieces.",
    "cut.too_dull": "You bear down, but {tool} won't bite into the {target}. You'd need a keener edge.",
    "cut.hack_out": "A blade won't beat what holds the {part}, so you carve around it, hacking it out "
                    "in ragged pieces — {output}s now. {residue}",
    "cut.integral": "The blade finds no seam — the {part} is {why}. There's nothing for an edge to "
                    "part.",
    # burn --------------------------------------------------------------------
    "burn.success": "The {target} catches, curls, and burns down to ash, {smoke} coiling upward.",
    "burn.no_flame": "You've nothing to set the {target} alight with.",
    "burn.wont_catch": "The {target} smoulders sullenly and refuses to catch.",
    # pry ---------------------------------------------------------------------
    "pry.free": "You lever {tool} under the {part} and heave; it pops free — a {output}.",
    "pry.no_leverage": "You strain, but {tool} can't shift the {part}. You need more leverage.",
    "pry.no_purchase": "You feel for somewhere to lever, but the {part} is {why} — nothing to pry "
                       "against.",
    # tear --------------------------------------------------------------------
    "tear.free": "You get a grip on the {target}'s {part} and haul; the seams give and it rips away — a "
                 "{output}.",
    "tear.strips": "You worry at the {target} and tear it into long ragged strips.",
    "tear.too_tough": "The {target} holds — too tough to tear with bare hands. A blade might bite.",
    "tear.rip_out": "You get both hands into the {part} and haul it out in torn fistfuls — "
                    "{output}s. {residue}",
    "tear.integral": "You get a grip, but the {part} is {why} — there's no seam to start a tear.",
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
    # light -------------------------------------------------------------------
    "light.lit": "The {target} catches with a small eager flame — a fire, at last.",
    "light.no_spark": "You've no way to spark the {target} alight. You need a flame.",
    "light.already": "The {target} is already lit.",
    "light.wont_catch": "You coax it, but the {target} just won't take a flame.",
    # melt --------------------------------------------------------------------
    "melt.water": "The {target} softens, slumps, and runs to clear meltwater.",
    "melt.no_heat": "The {target} stays frozen solid — you'll need a heat source.",
    "melt.composite": "You can't melt the whole {target} down like that.",
    # pour --------------------------------------------------------------------
    "pour.douse": "You upend the {liquid} over the {target}; it hisses, steams, and goes out.",
    "pour.wet": "You pour the {liquid} over the {target}, soaking it through.",
    "pour.no_target": "You tip the {liquid} out — but onto what? (pour X on Y)",
    # tie ---------------------------------------------------------------------
    "tie.knot": "You lash the {cord} to the {anchor} and cinch it down — it holds.",
    "tie.no_anchor": "You loop the {cord}, ready to tie — but to what? (tie X to Y)",
    # wrap --------------------------------------------------------------------
    "wrap.wrapped": "You wind the {wrap} around the {target}, snug and secure.",
    "wrap.insulate": "You bundle the {wrap} around the {target}; it'll hold the warmth in.",
    "wrap.no_target": "You gather up the {wrap} to wrap — around what? (wrap X around Y)",
    # drink -------------------------------------------------------------------
    "drink.slake": "You drink the {target} down; cold and clean, it eases the thirst.",
    "drink.risky": "You force down the {target}. It's brackish — better than nothing, you hope.",
    "drink.frozen": "You can't drink the {target} frozen — melt it to water first.",
    # eat ---------------------------------------------------------------------
    "eat.eat": "You eat the {target}; it's something, and the gnaw of hunger eases a little.",
    "eat.meagre": "You get the {target} down. Precious few calories, but every one counts.",
    # the one-sibling near-miss (names the part, never the method — DR-09a) ----
    "hint.sibling": "The {sibling}, though, is only {sibling_phrase}.",
    # attachment voice (DR-09a; content-tunable; '_' = the kind's fallback) ----
    "attachment.explain.stitched": "hanging by stitching — nothing rigid to get behind",
    "attachment.explain.clipped": "snapped into its frame — a blade won't pop a clip",
    "attachment.explain.bolted": "bolted fast — an edge does nothing against a bolt",
    "attachment.explain.fixed": "part of the thing itself",
    "attachment.explain._": "{attachment} fast",
    "attachment.hint.stitched": "held by stitching",
    "attachment.hint.clipped": "snapped into a frame",
    "attachment.hint.bolted": "bolted down",
    "attachment.hint._": "{attachment}",
    "attachment.residue.clipped": "The crushed clips stay on the frame.",
    "attachment.residue.bolted": "The bolts stay put, stripped bare.",
    "attachment.residue._": "Whatever held it stays behind, wrecked.",
    # generic -----------------------------------------------------------------
    "__fallback__": "Something shifts, but not the way you meant.",
}
