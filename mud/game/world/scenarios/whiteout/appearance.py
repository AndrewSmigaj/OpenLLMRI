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

    # --- the scattered wreck (DR-24 §8b: the crash is the difficulty engine) -----
    "survivalduffel": {
        "salience": "prominent", "order": 30,
        "scene": [(None, "The survival duffel lies split along its seam, half-sunk in the gouged "
                         "snow — the crash shook it out like a pillowcase.")],
        "examine": [(None, "The legally-required kit bag, torn open on impact. What stayed inside "
                           "stayed; the rest is somewhere out there under the white.")],
    },
    "drift2": {
        "salience": "ordinary", "order": 40,
        "scene": [(None, "a wind-packed drift, its crust dented where something punched in")],
        "examine": [(None, "Hard-packed snow. Something heavy hit here at speed — the entry hole "
                           "has already half-healed with blown powder.")],
    },
    "hatchet": {
        "salience": "ordinary",
        "scene": [(None, "a hatchet, half out of the snow")],
        "examine": [(None, "A forest hatchet — but the haft is CRACKED through below the head; "
                           "it twists in the grip. Choked up, it still bites. Lashed and taped, "
                           "it could be whole again.")],
    },
    "matchbox": {
        "salience": "subtle",
        "scene": [(None, "a waterproof matchbox")],
        "examine": [(None, "The irony is complete: the waterproof case cracked, and the strike-"
                           "anywheres inside drank the snowmelt. Dried out — slowly, by a fire — "
                           "they might live again.")],
    },
    "ration tin": {
        "salience": "subtle",
        "aggregate": "{count} olive-drab ration tins, dented but sealed",
        "scene": [(None, "an olive-drab ration tin")],
        "examine": [(None, "Dense survival rations, sealed in tin. Dull as a sermon and worth "
                           "more than gold.")],
    },
    "fishingkit": {
        "salience": "subtle",
        "scene": [(None, "a pocket fishing kit")],
        "examine": [(None, "Hooks, split-shot, and eighty feet of line wound on a plastic "
                           "spool. The creek is out there somewhere under the ice.")],
    },
    "headnet": {
        "salience": "subtle",
        "scene": [(None, "a mosquito headnet")],
        "examine": [(None, "Fine summer netting — useless against snow, fine for straining "
                           "meltwater.")],
    },
    "mailsack": {
        "salience": "ordinary", "order": 35,
        "scene": [(None, "a grey mail sack, spilled and freezing to the snow")],
        "examine": [(None, "US MAIL — CHUGIAK LAKE, stencilled and half-drifted. Someone is "
                           "waiting for all of this.")],
    },
    "letters": {
        "salience": "subtle",
        "scene": [(None, "a rubber-banded bundle of letters")],
        "examine": [(None, "Forty-odd envelopes, addresses running in the damp. Paper burns; "
                           "these would burn like anything else. They would, though, be these.")],
        "read": [(None, "You shouldn't. You do. A child's pencil, pressed hard: 'DEAR DAD the "
                        "ice is good and Mr K says my slapshot is a HAZERD. Come home before "
                        "the river shuts.' You put the bundle down with more care than you "
                        "picked it up.")],
    },
    "twine": {
        "salience": "subtle",
        "scene": [(None, "a ball of postal twine")],
        "examine": [(None, "Rough brown twine, a few hundred feet of it. Knots, snares, "
                           "lashings.")],
    },
    "alusheet": {
        "salience": "ordinary",
        "scene": [(None, "a twisted sheet of fuselage skin")],
        "examine": [(None, "A shed panel of aircraft aluminum, edges bright and mean. A "
                           "windbreak, a fire-back, a sled for a strong back.")],
    },
    "tailcone": {
        "salience": "prominent", "order": 10,
        "scene": [
            ({"open": True}, "The crushed tail cone gapes where it was levered open, its cargo "
                             "bay finally giving up its dead."),
            (None, "The tail cone is crushed like paper — the baggage bay is in there, behind "
                   "buckled aluminum that fingers won't move."),
        ],
        "examine": [
            ({"open": True}, "Pried wide. The lashing points hang empty now."),
            (None, "The whole aft bay folded in on itself when the tail struck. Through a "
                   "fist-sized gap you can make out webbing and something quilted. It wants "
                   "a lever and real anger."),
        ],
    },
    "sleepingbag": {
        "salience": "ordinary",
        "scene": [(None, "a rolled sleeping bag, dark-stained")],
        "examine": [(None, "A heavy wool-lined bag — soaked along one side with avgas from a "
                           "ruptured line. Warm as a stove; keep it the hell away from one.")],
    },
    "snowshoes": {
        "salience": "ordinary",
        "scene": [(None, "a pair of trail snowshoes")],
        "examine": [(None, "Ash frames, webbing decks, leather bindings. The drifts stop being "
                           "walls the moment these go on.")],
    },
    "cargonet": {
        "salience": "subtle",
        "scene": [(None, "a cargo net, still lashed to its rings")],
        "examine": [(None, "Metres of knotted webbing. Cut free, it's cordage beyond counting.")],
    },
    "elt": {
        "salience": "prominent", "order": 20,
        "scene": [(None, "An orange box rides its bracket in the wreckage, a red lamp pulsing "
                         "slow as a heartbeat.")],
        "examine": [(None, "The emergency locator transmitter. The g-switch tripped on impact — "
                           "ARM light pulsing, faithfully shouting on 121.5 — but its antenna "
                           "ends two inches up in bright sheared metal. It is screaming into "
                           "its own throat. It needs a real antenna, and wire enough to reach "
                           "one.")],
    },
    "crate": {
        "salience": "ordinary", "order": 30,
        "scene": [
            ({"open": True}, "the freight crate, lid levered off"),
            (None, "a freight crate, lid nailed fast and stencilled CHUGIAK LAKE CO-OP"),
        ],
        "examine": [
            ({"open": True}, "Groceries for a village store, riding a lid that's already off."),
            (None, "Somebody's monthly order, nailed shut for the flight. The lid seam is a "
                   "lever's invitation.")],
    },
    "coffeetin": {
        "salience": "subtle",
        "scene": [(None, "a catering tin of coffee")],
        "examine": [(None, "Three pounds of ground coffee, vacuum-sealed. Morale in a can.")],
    },
    "flour": {
        "salience": "subtle",
        "scene": [(None, "a sack of flour")],
        "examine": [(None, "Ten pounds of flour, dry inside its paper. Bannock over a fire, if "
                           "the fire ever happens.")],
    },
    # --- cockpit & cabin additions ------------------------------------------------
    "flightbag": {
        "salience": "ordinary",
        "scene": [(None, "the pilot's leather flight bag, wedged by the rudder pedals")],
        "examine": [(None, "A working pilot's bag: chart pockets, pen loops, twenty years of "
                           "wear. Zipped.")],
    },
    "flashlight": {
        "salience": "subtle",
        "scene": [(None, "an aluminum flashlight")],
        "examine": [(None, "A heavy D-cell flashlight. The beam is strong now; batteries are a "
                           "countdown.")],
    },
    "fueltester": {
        "salience": "subtle",
        "scene": [(None, "a fuel tester cup")],
        "examine": [(None, "A clear sump cup with a probe pin — made for pulling avgas a "
                           "swallow at a time. The wing drains would answer to this.")],
    },
    "chart": {
        "salience": "ordinary",
        "scene": [(None, "a sectional chart, folded to this valley")],
        "examine": [(None, "The Anchorage sectional, folded and refolded to one creased "
                           "rectangle of nowhere. There is handwriting on it.")],
        "read": [(None, "The valley, in the pilot's pencil: the creek winding south, a spot "
                        "height, and — three miles east, up the feeder stream — a small square "
                        "drawn by hand, marked 'V. HOLT — CABIN, WOOD STOVE'. Underlined "
                        "once.")],
    },
    "thermos": {
        "salience": "subtle",
        "scene": [(None, "a steel thermos, upright against the pedals")],
        "examine": [(None, "The pilot's thermos. Through the steel, faintly, unbelievably: "
                           "still warm.")],
    },
    "extinguisher": {
        "salience": "subtle",
        "scene": [(None, "a small fire extinguisher in its bracket")],
        "examine": [(None, "A halon bottle, charged, pin seated. The one fire you'll want to "
                           "stop, someday, in a shelter.")],
    },
    "toolroll": {
        "salience": "subtle",
        "scene": [(None, "a canvas tool roll")],
        "examine": [(None, "A mechanic's roll, oil-dark with years. It clinks with competence.")],
    },
    "ducttape": {
        "salience": "subtle",
        "scene": [(None, "a roll of duct tape")],
        "examine": [(None, "Half a roll. Out here, that's currency.")],
    },
    "safetywire": {
        "salience": "subtle",
        "scene": [(None, "a spool of safety wire")],
        "examine": [(None, "Fine stainless lockwire — metres of it. Binds anything to anything, "
                           "forever.")],
    },
    "screwdriver": {
        "salience": "subtle",
        "scene": [(None, "a long flat screwdriver")],
        "examine": [(None, "A long flat-blade. Half tool, half small crowbar.")],
    },
    "enginecover": {
        "salience": "ordinary",
        "scene": [(None, "the quilted engine cover, folded fat as a mattress")],
        "examine": [(None, "The insulated cover the pilot bagged the cowling with at every cold "
                           "stop — a great quilted blanket built for exactly one job: holding "
                           "heat against metal all night. It would hold it against a person.")],
    },
    "aircraft seat": {    # the second row (12C) — name-keyed; 11B keeps its sim-id entry
        "salience": "prominent", "order": 32,
        "scene": [
            ({"residue_cushion": "clipped"},
             "Another seat stands half-stripped, clips bared where its cushion went."),
            (None, "A second passenger seat — 12C on the frame — thrown hard against the hull."),
        ],
        "examine": [(None, "Same crash-scarred build as its row-mate: thin cover, thick dry "
                           "foam, a belt on a bolted anchor.")],
    },
    "oil quart": {
        "salience": "subtle",
        "aggregate": "{count} quarts of engine oil, rolled against the hull",
        "scene": [(None, "a quart of engine oil")],
        "examine": [(None, "Straight-weight aviation oil. Burns filthy and black — which, for "
                           "a signal, is the entire point.")],
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
