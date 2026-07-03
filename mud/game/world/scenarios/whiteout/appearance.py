"""Whiteout — appearance content (DR-23): scene phrases, examine prose, salience. Tunable content —
this is Andrew's voice; rewrite freely. Structure per entry (keyed by sim_id, or by display NAME for
derived objects so identical deriveds share one entry):

    "salience": "prominent" | "ordinary" | "subtle"   (weighting, never hiding)
    "order":    int (sort within a tier; lower = earlier; default 50)
    "promote":  [({state-subset}, tier), ...]          (state promotes salience — a lit fire leads)
    "scene":    [({state-subset} | None, phrase), ...] (first match wins; prominent = a full
                sentence, ordinary/subtle = a noun phrase for the frame lines)
    "aggregate": "..."                                  (N>1 identical: one sentence, {count})
    "examine":  [({state-subset} | None, prose), ...]  (the unified look-at/examine body)

Anti-spoiler rule (GD20): examine prose hints at PROPERTIES and at most a couple of verbs — never
the full affordance set; attachments render physically via the DR-09a hint phrases.
"""

APPEARANCE = {
    "_frames": {
        "ordinary": "The crash left its litter everywhere: {items}.",
        "subtle": "Half-buried in the mess: {items}.",
    },

    # --- the anchors (prominent) ---------------------------------------------
    "pilot": {
        "salience": "prominent", "order": 10,
        "scene": [
            ({"dead": True}, "The pilot lies still against the forward bulkhead."),
            (None, "The pilot is slumped against the forward bulkhead, breathing shallow and slow."),
        ],
        "examine": [
            ({"dead": True}, "He has stopped breathing. His flight jacket is zipped to the chin, "
                             "one hand still resting on the radio cradle."),
            (None, "Grey-faced and half-conscious. A dark stain has stiffened along his left side, "
                   "and his breath comes in slow fog. He mumbles at the radio when he surfaces."),
        ],
    },
    "radio": {
        "salience": "prominent", "order": 20,
        "scene": [(None, "A field radio sits dark in its cradle beside the pilot.")],
        "examine": [(None, "A ruggedized field set, dials frosted over. The power lamp flickers "
                           "when you rock the case — the set seems alive, but deaf.")],
    },
    "seat": {
        "salience": "prominent", "order": 30,
        "scene": [
            ({"residue_cushion": "clipped"},
             "Seat 11B stands half-stripped, bared clips showing where its cushion was hacked out."),
            (None, "An aircraft seat — 11B stencilled on the frame — sits wrenched sideways on its "
                   "bolts."),
        ],
        "examine": [(None, "Slate-grey and crash-scarred, but still solid on its rails. The fabric "
                           "of the cover is thin; the foam under it is thick, dense and dry.")],
    },
    "snowdrift": {
        "salience": "prominent", "order": 40,
        "scene": [(None, "Snow has drifted in through the split hull, banking white against the "
                         "rear rows.")],
        "examine": [(None, "Fine, dry snow, knee-deep where the wind stacked it. Clean enough to "
                           "melt, cold enough to kill.")],
    },

    # --- the kit (ordinary) ---------------------------------------------------
    "multitool": {
        "salience": "ordinary", "order": 10,
        "scene": [(None, "a multitool lying open")],
        "examine": [(None, "Pliers, a stubby blade, a folding lever — cheap steel, but the edge "
                           "holds and the leverage is honest.")],
    },
    "bottle": {
        "salience": "ordinary",
        "scene": [(None, "an unbroken whisky bottle")],
        "examine": [(None, "A square-shouldered whisky bottle, empty. The glass is heavy — the kind "
                           "that breaks sharp.")],
    },
    "canteen": {
        "salience": "ordinary",
        "scene": [(None, "a dented canteen")],
        "examine": [(None, "A steel canteen, dented but tight. Something sloshes inside it, "
                           "half-frozen and slow.")],
    },
    "jerrycan": {
        "salience": "ordinary",
        "scene": [(None, "a jerry can on its side")],
        "examine": [(None, "A red jerry can, lying where it rolled. It is not empty, and what's "
                           "inside is not water.")],
    },
    "blanket": {
        "salience": "ordinary",
        "scene": [(None, "a wool blanket spilled from an overhead bin")],
        "examine": [(None, "Airline wool, scratchy and dense. Warmth, a windbreak, a bandage — "
                           "cloth this heavy is whatever you need it to be.")],
    },
    "jacket": {
        "salience": "ordinary",
        "scene": [(None, "the pilot's spare flight jacket")],
        "examine": [(None, "A lined flight jacket, fleece collar stiff with frost. Someone could "
                           "wear it, or wrap something that matters in it.")],
    },
    "manual": {
        "salience": "ordinary",
        "scene": [(None, "a flight manual splayed face-down")],
        "examine": [(None, "Three hundred pages of procedures nobody will fly again. Thin, dry "
                           "paper. Something is pencilled inside the cover.")],
        "read": [(None, "Checklists, frequencies, weight tables. The emergency section is "
                        "dog-eared: signal fires burn better wet-green over a hot core; keep "
                        "casualties off the ground. Pencilled inside the cover, underlined "
                        "twice: 'GUARD — 121.5'.")],
    },
    "ice": {
        "salience": "ordinary",
        "scene": [(None, "a chunk of ice broken off the wing root")],
        "examine": [(None, "A cloudy slab of ice, dense and clear at the core. Water, if you can "
                           "get heat into it.")],
    },

    # --- the small stuff (subtle) ---------------------------------------------
    "wire": {
        "salience": "subtle",
        "scene": [
            ({"shape": "bent"}, "a length of copper wire, bent to a worked shape"),
            (None, "a coil of copper wire"),
        ],
        "examine": [(None, "Fine copper wire, springy in the coil. It takes a bend and keeps it.")],
    },
    "paracord": {
        "salience": "subtle",
        "scene": [(None, "a hank of paracord")],
        "examine": [(None, "Two metres of paracord, kernmantle intact. It knots clean and holds "
                           "hard.")],
    },
    "tinder": {
        "salience": "subtle",
        "promote": [({"lit": True}, "prominent")],
        "scene": [
            ({"lit": True}, "A small fire cracks and spits where the dry grass caught."),
            (None, "a fist of dry grass jammed in a seat rail"),
        ],
        "examine": [
            ({"lit": True}, "It burns eager and fast — more flame than fuel. It will want feeding."),
            (None, "Sun-bleached grass, bone dry. It would take a spark like a held breath."),
        ],
    },
    "lighter": {
        "salience": "subtle",
        "scene": [(None, "a scratched brass lighter")],
        "examine": [(None, "A brass lighter, fuel sloshing faintly. The wheel sparks on the first "
                           "strike.")],
    },
    "chocolate": {
        "salience": "subtle",
        "scene": [(None, "a chocolate bar in a torn wrapper")],
        "examine": [(None, "A travel chocolate bar, frozen board-hard. Calories, whenever you're "
                           "willing to spend them.")],
    },

    # --- containers & fixtures (DR-24: the scene shows THESE; loot hides inside) ---
    "bin_fwd": {
        "salience": "ordinary", "order": 15,
        "scene": [
            ({"open": True}, "the forward overhead bin hanging open"),
            (None, "the forward overhead bin, latched shut"),
        ],
        "examine": [
            ({"open": True}, "The bin hangs on its hinge, latch sprung."),
            (None, "An overhead stowage bin, still latched. The latch looks willing."),
        ],
    },
    "bin_aft": {
        "salience": "ordinary", "order": 15,
        "scene": [
            ({"open": True}, "the aft overhead bin wrenched open"),
            (None, "the aft overhead bin, buckled shut in its track"),
        ],
        "examine": [
            ({"open": True}, "Levered open, lip bent where something forced it."),
            (None, "The impact buckled this bin in its track — the latch turns, but the lid "
                   "won't lift. A seam runs along the lip."),
        ],
    },
    "panel": {
        "salience": "ordinary", "order": 25,
        "scene": [
            ({"open": True}, "the avionics panel hanging off its screws"),
            (None, "an avionics panel, crumpled at one corner"),
        ],
        "examine": [
            ({"open": True}, "The panel hangs loose, a nest of dead circuits behind it."),
            (None, "A crumpled aluminium access panel below the radio cradle. One corner has "
                   "lifted, just enough to see darkness behind it."),
        ],
    },
    "duffel": {
        "salience": "ordinary", "order": 20,
        "scene": [(None, "a duffel bag burst half-open in the aisle")],
        "examine": [(None, "Somebody's weekend bag, seam split by the impact. Worth going "
                           "through.")],
    },
    "backpack": {
        "salience": "ordinary",
        "scene": [(None, "a scuffed backpack")],
        "examine": [(None, "A day-hiker's pack, straps still cinched. It has weight to it.")],
    },
    "firstaid": {
        "salience": "ordinary",
        "scene": [(None, "a first-aid kit")],
        "examine": [
            ({"open": True}, "The kit lies open, its clips sprung."),
            (None, "A white clamshell case, red cross scuffed nearly off. Clipped shut."),
        ],
    },
    "seatpocket": {
        "salience": "subtle",
        "scene": [(None, "a seatback pocket")],
        "examine": [(None, "The elastic-topped pocket on the seatback, stretched out of shape.")],
    },
    "masks": {
        "salience": "ordinary", "order": 40,
        "scene": [(None, "oxygen masks dangling from the sprung ceiling panel")],
        "examine": [(None, "Yellow cups on rubber tubing, swaying when the wind finds the "
                           "cabin. The tubing is tied into the drop unit; the cups just clip.")],
    },
    "spruce": {
        "salience": "prominent", "order": 45,
        "scene": [(None, "The first spruce stands close enough to touch, boughs bent white.")],
        "examine": [(None, "A young spruce, snow-loaded. A low branch hangs within easy reach; "
                           "a thicker bough above it would take real cutting.")],
    },
    "deadfall branch": {
        "salience": "ordinary",
        "aggregate": "Deadfall lies about — {count} good branches under the snow crust",
        "scene": [(None, "a deadfall branch")],
        "examine": [(None, "A wind-snapped branch, dry under the bark. Honest firewood.")],
    },
    "gloves": {
        "salience": "ordinary",
        "scene": [(None, "a pair of leather gloves")],
        "examine": [(None, "Lined leather work gloves, stiff with cold and worth their weight.")],
    },
    "socks": {
        "salience": "subtle",
        "scene": [(None, "a pair of wool socks")],
        "examine": [(None, "Thick wool socks, blessedly dry.")],
    },
    "shirt": {
        "salience": "subtle",
        "scene": [(None, "a spare shirt")],
        "examine": [(None, "A cotton shirt, creased from the pack.")],
    },
    "bandage": {
        "salience": "subtle",
        "scene": [(None, "a bandage roll")],
        "examine": [(None, "A rolled cotton bandage, still in its paper band.")],
    },
    "tape": {
        "salience": "subtle",
        "scene": [(None, "a roll of medical tape")],
        "examine": [(None, "Medical tape. Sticks to anything, including gloves.")],
    },

    # --- derived objects (keyed by display NAME; identical deriveds share one entry) ---
    "glass shard": {
        "salience": "ordinary",
        "aggregate": "Broken glass — {count} sharp shards — glitters where the bottle went",
        "scene": [(None, "a sharp glass shard")],
        "examine": [(None, "A curved shard of bottle glass, edge like a promise. It would cut "
                           "you as gladly as anything else.")],
    },
    "foam scrap": {
        "salience": "ordinary",
        "aggregate": "Hacked-out seat foam lies in {count} ragged lumps",
        "scene": [(None, "a ragged lump of seat foam")],
        "examine": [(None, "Torn seat foam, dense and dry. It holds warmth if you keep it dry — "
                           "and burns filthy if you don't care.")],
    },
    "water": {
        "salience": "ordinary",
        "scene": [(None, "a pool of clear meltwater")],
        "examine": [(None, "Clear meltwater, mirror-still and cold enough to ache.")],
    },
    "ash": {
        "salience": "subtle",
        "scene": [(None, "a smear of pale ash")],
        "examine": [(None, "Fine grey ash, still faintly warm underneath.")],
    },
    "loose fabric": {
        "salience": "ordinary",
        "scene": [(None, "a freed seat cover")],
        "examine": [(None, "The seat's fabric cover, cut free in one piece. Thin, tough weave — "
                           "it would tear into strips or wrap around something small.")],
    },
    "loose foam": {
        "salience": "ordinary",
        "scene": [(None, "an intact seat cushion, pried whole")],
        "examine": [(None, "The whole cushion, popped free with its shape intact — a full pad of "
                           "dry insulation, worth more unbroken than in scraps.")],
    },
    "loose webbing": {
        "salience": "ordinary",
        "scene": [(None, "a freed length of seatbelt webbing")],
        "examine": [(None, "Nylon webbing off the seatbelt, anchor-holes and all. Strong enough "
                           "to bear weight.")],
    },
}
