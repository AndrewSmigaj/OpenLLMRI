"""Whiteout — appearance content: scene phrases, examine prose, and each object's home space.
Tunable content — this is Andrew's voice; rewrite freely. Structure per entry (keyed by sim_id, or
by display NAME for derived objects so identical deriveds share one entry):

    "space":    str   the object's home space within its zone (see spaces.py) — where it renders and
                where a "look at <space>" finds it. Unset → the zone's default space (a safe fallback).
    "anchor":   bool  this object DEFINES its space and leads it as its own sentence (the pilot, the
                radio, seat 11B). Anchors carry a full-sentence `scene`; non-anchors a noun phrase.
    "scene":    [({state-subset} | None, phrase), ...] (first match wins; anchor = a full sentence,
                otherwise a noun phrase that drops into the space's frame)
    "aggregate": "..."                                  (N>1 identical: one sentence, {count})
    "examine":  [({state-subset} | None, prose), ...]  (the unified look-at/examine body)
    "read":     [({state-subset} | None, text), ...]   (authored `read` text, if any)
    "salience"/"order": retained ONLY for the banded cross-zone view (a zone away, detail is lost and
                things grade by salience); the same-zone render now orders by SPACE, not by tier.

Tell/hide rule (supersedes the DR-23 "weighting, never hiding"): a space describes CHARACTER, not a
full inventory. Show functional flavor; never leave a load-bearing item lying in the open — the
puzzle-critical stuff hides INSIDE containers (DR-24), found by open/search/dig, never listed here.
Anti-spoiler (GD20): examine prose hints at PROPERTIES and at most a couple of verbs.
"""

APPEARANCE = {
    # --- the anchors -----------------------------------------------------------
    "pilot": {
        "space": "left_seat", "anchor": True,
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
        "space": "cradle", "anchor": True,
        "salience": "prominent", "order": 20,
        "scene": [(None, "A field radio sits dark in its cradle beside the pilot.")],
        "examine": [(None, "A ruggedized field set, dials frosted over. The power lamp flickers "
                           "when you rock the case — the set seems alive, but deaf.")],
    },
    "seat": {
        "space": "seat_rows", "anchor": True,
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
        "space": "rear_rows", "anchor": True,
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
        "space": "floor",
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
        "space": "hull_side",
        "salience": "ordinary",
        "scene": [(None, "a red jerry can")],
        "examine": [(None, "A red jerry can, lying where it rolled. It is not empty, and what's "
                           "inside is not water.")],
    },
    "blanket": {
        "space": "floor",
        "salience": "ordinary",
        "scene": [(None, "a half-unrolled wool blanket")],
        "examine": [(None, "Airline wool, scratchy and dense. Warmth, a windbreak, a bandage — "
                           "cloth this heavy is whatever you need it to be.")],
    },
    "jacket": {
        "space": "left_seat",
        "salience": "ordinary",
        "scene": [(None, "the pilot's spare flight jacket")],
        "examine": [(None, "A lined flight jacket, fleece collar stiff with frost. Someone could "
                           "wear it, or wrap something that matters in it.")],
    },
    "manual": {
        "space": "floor",
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
        "space": "the_snow",
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
        "space": "under_spruces", "mass": True,
        "salience": "subtle",
        "promote": [({"lit": True}, "prominent")],
        "scene": [
            ({"lit": True}, "a knot of grass burning low in the snow"),
            (None, "a wind-combed fist of dry grass"),
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
        "space": "overhead",
        "salience": "ordinary", "order": 15,
        "scene": [
            ({"open": True}, "the forward overhead bin hanging open"),
            (None, "the latched forward overhead bin"),
        ],
        "examine": [
            ({"open": True}, "The bin hangs on its hinge, latch sprung."),
            (None, "An overhead stowage bin, still latched. The latch looks willing."),
        ],
    },
    "bin_aft": {
        "space": "overhead",
        "salience": "ordinary", "order": 15,
        "scene": [
            ({"open": True}, "the aft overhead bin wrenched open"),
            (None, "the aft overhead bin buckled shut in its track"),
        ],
        "examine": [
            ({"open": True}, "Levered open, lip bent where something forced it."),
            (None, "The impact buckled this bin in its track — the latch turns, but the lid "
                   "won't lift. A seam runs along the lip."),
        ],
    },
    "panel": {
        "space": "cradle",
        "salience": "ordinary", "order": 25,
        "scene": [
            ({"open": True}, "the avionics panel hanging off its screws"),
            (None, "a crumpled avionics panel"),
        ],
        "examine": [
            ({"open": True}, "The panel hangs loose, a nest of dead circuits behind it."),
            (None, "A crumpled aluminium access panel below the radio cradle. One corner has "
                   "lifted, just enough to see darkness behind it."),
        ],
    },
    "duffel": {
        "space": "aisle",
        "salience": "ordinary", "order": 20,
        "scene": [(None, "a duffel bag burst half-open")],
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
        "space": "overhead", "mass": True,
        "salience": "ordinary", "order": 40,
        "scene": [(None, "oxygen masks swaying from a sprung panel")],
        "examine": [(None, "Yellow cups on rubber tubing, swaying when the wind finds the "
                           "cabin. The tubing is tied into the drop unit; the cups just clip.")],
    },
    "spruce": {
        "space": "under_spruces", "anchor": True,
        "salience": "prominent", "order": 45,
        "scene": [(None, "The first spruce stands close enough to touch, boughs bent white.")],
        "examine": [(None, "A young spruce, snow-loaded. A low branch hangs within easy reach; "
                           "a thicker bough above it would take real cutting.")],
    },
    "deadfall branch": {
        "space": "under_spruces",
        "salience": "ordinary",
        "aggregate": "{count} snow-crusted deadfall branches",
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
        "space": "the_scar", "anchor": True,
        "salience": "prominent", "order": 30,
        "scene": [(None, "The survival duffel lies split along its seam, half-sunk in the gouged "
                         "snow — the crash shook it out like a pillowcase.")],
        "examine": [(None, "The legally-required kit bag, torn open on impact. What stayed inside "
                           "stayed; the rest is somewhere out there under the white.")],
    },
    "drift2": {
        "space": "the_scar",
        "salience": "ordinary", "order": 40,
        "scene": [(None, "a wind-packed drift with a punched-in crust")],
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
        "space": "the_scar", "anchor": True,
        "salience": "ordinary", "order": 35,
        "scene": [(None, "A grey mail sack has burst across the snow, already freezing down.")],
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
        "space": "the_scar",
        "salience": "ordinary",
        "scene": [(None, "a twisted sheet of fuselage skin")],
        "examine": [(None, "A shed panel of aircraft aluminum, edges bright and mean. A "
                           "windbreak, a fire-back, a sled for a strong back.")],
    },
    "tailcone": {
        "space": "the_snow", "anchor": True,
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
        "mass": True,
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
        "space": "the_snow", "anchor": True,
        "salience": "ordinary", "order": 30,
        "scene": [
            ({"open": True}, "A freight crate stands open, its lid levered off."),
            (None, "A nailed freight crate sits half-buried, stencilled CHUGIAK LAKE CO-OP."),
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
        "space": "footwell",
        "salience": "ordinary",
        "scene": [(None, "the pilot's worn leather flight bag")],
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
        "space": "floor",
        "salience": "ordinary",
        "scene": [(None, "a sectional chart folded to this valley")],
        "examine": [(None, "The Anchorage sectional, folded and refolded to one creased "
                           "rectangle of nowhere. There is handwriting on it.")],
        "read": [(None, "The valley, in the pilot's pencil: the creek winding south, a spot "
                        "height, and — three miles east, up the feeder stream — a small square "
                        "drawn by hand, marked 'V. HOLT — CABIN, WOOD STOVE'. Underlined "
                        "once.")],
    },
    "thermos": {
        "space": "footwell",
        "salience": "subtle",
        "scene": [(None, "a capped steel thermos")],
        "examine": [(None, "The pilot's thermos. Through the steel, faintly, unbelievably: "
                           "still warm.")],
    },
    "extinguisher": {
        "space": "cradle",
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
        "space": "floor",
        "salience": "ordinary",
        "scene": [(None, "the quilted engine cover folded thick as a mattress")],
        "examine": [(None, "The insulated cover the pilot bagged the cowling with at every cold "
                           "stop — a great quilted blanket built for exactly one job: holding "
                           "heat against metal all night. It would hold it against a person.")],
    },
    "aircraft seat": {    # the second row (12C) — name-keyed; 11B keeps its sim-id entry
        "space": "rear_rows", "anchor": True,
        "salience": "prominent", "order": 32,
        "scene": [
            ({"residue_cushion": "clipped"},
             "Another seat stands half-stripped, clips bared where its cushion went."),
            (None, "A second passenger seat — 12C on the frame — lies thrown against the hull."),
        ],
        "examine": [(None, "Same crash-scarred build as its row-mate: thin cover, thick dry "
                           "foam, a belt on a bolted anchor.")],
    },
    "oil quart": {
        "space": "hull_side",
        "salience": "subtle",
        "aggregate": "{count} quarts of engine oil",
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
    # --- form-keyed GENERICS (DR-26 closure): any minted thing without an entry of its own reads
    # from its FORM, with {material} filled in. Name-keyed entries above override these. Each one
    # carries the SIGNIFIER of the capability the form derives (the edge, the tie, the cover) — a
    # capability nobody can see is the first thing players complain about. Tunable voice.
    "form:shard": {
        "salience": "ordinary",
        "aggregate": "Broken {material} — {count} sharp shards — glitters where it went",
        "scene": [(None, "a sharp {material} shard")],
        "examine": [(None, "A shard of {material}, one edge wicked-sharp. It would cut — you, as "
                           "gladly as whatever you meant to cut.")],
    },
    "form:flake": {
        "salience": "subtle",
        "scene": [(None, "a {material} flake")],
        "examine": [(None, "A thin flake of {material} with a keen, brittle edge. A scraper, "
                           "for as long as it lasts.")],
    },
    "form:piece": {
        "salience": "ordinary",
        "aggregate": "{count} broken pieces of {material}",
        "scene": [(None, "a broken piece of {material}")],
        "examine": [(None, "A rough piece of {material}, snapped clean. Heft enough to matter in "
                           "the hand.")],
    },
    "form:scrap": {
        "salience": "subtle",
        "aggregate": "{count} ragged scraps of {material}",
        "scene": [(None, "a ragged scrap of {material}")],
        "examine": [(None, "Torn {material}, ragged where it was hacked free. Not much of a thing "
                           "alone; a few together might be stuffing, or fuel.")],
    },
    "form:strip": {
        "salience": "ordinary",
        "aggregate": "{count} torn strips of {material}",
        "scene": [(None, "a strip of {material}")],
        "examine": [(None, "A long strip of {material}. It would tie, bind or wrap something "
                           "small — or feed a young fire.")],
    },
    "form:sheet": {
        "salience": "ordinary",
        "scene": [(None, "a loose sheet of {material}")],
        "examine": [(None, "A loose sheet of {material}. It would cover an opening, wrap "
                           "around a body, or tear down into strips.")],
    },
    "form:shavings": {
        "salience": "subtle",
        "scene": [(None, "a heap of {material} shavings")],
        "examine": [(None, "Fine pale curls of {material}. Thin enough to catch from a small "
                           "flame and burn hot for a minute.")],
    },
    "form:bundle": {
        "salience": "ordinary",
        "scene": [(None, "a loose bundle of {material}")],
        "examine": [(None, "A nest of {material} worked loose and airy, the way a spark or an "
                           "ember wants it.")],
    },
    "form:rod": {
        "salience": "ordinary",
        "aggregate": "{count} lengths of {material}",
        "scene": [(None, "a length of {material}")],
        "examine": [(None, "A straight length of {material}, wrist-thick. Lever, stake or "
                           "firewood, as you choose.")],
    },
    "form:block": {
        "salience": "ordinary",
        "scene": [(None, "a solid block of {material}")],
        "examine": [(None, "A solid block of {material}, whole. Worth more unbroken than in "
                           "pieces.")],
    },
    "form:vessel": {
        "salience": "ordinary",
        "scene": [(None, "a {material} vessel")],
        "examine": [(None, "A hollow of {material} that would hold water, or snow to melt.")],
    },
    "form:ember": {
        "salience": "prominent",
        "scene": [(None, "a glowing ember")],
        "examine": [(None, "A pinhead of orange alive in black dust, good for a minute or two. "
                           "It wants a nest of tinder and a slow breath.")],
    },
    "form:ash": {
        "salience": "subtle",
        "scene": [(None, "a smear of pale ash")],
        "examine": [(None, "Fine grey ash, still faintly warm underneath.")],
    },
    "form:liquid": {
        "salience": "ordinary",
        "scene": [(None, "a pool of {material}")],
        "examine": [(None, "A pool of {material}, spreading where it was spilled.")],
    },
    # --- the luggage, the mail and the freight (players-and-kit.md §3) — plain first pass; Andrew tunes ---
    'suitcase': {"salience": "ordinary", "scene": [(None, 'a soft suitcase')], "examine": [(None, "A soft-sided suitcase, one zip burst. Somebody's whole trip is in it.")]},
    'laptop_bag': {"salience": "ordinary", "scene": [(None, 'a laptop bag')], "examine": [(None, 'A padded satchel. Heavier than clothes; something with a battery.')]},
    'hockey_duffel': {"salience": "ordinary", "scene": [(None, 'a hockey duffel')], "examine": [(None, "A hockey bag, the size of a body. Tape, pads, a stick — a kit that isn't for hockey any more.")]},
    'cooler': {"salience": "ordinary", "scene": [(None, 'a plastic cooler')], "examine": [(None, "A cooler, lid iced shut. Whatever's inside was frozen before the crash was.")]},
    'guitar_case': {"salience": "ordinary", "scene": [(None, 'a guitar case')], "examine": [(None, 'A hard guitar case, latches sprung. Wood, wire, and a shape that would slide.')]},
    'toolbox': {"salience": "ordinary", "scene": [(None, 'a steel toolbox')], "examine": [(None, 'A steel toolbox, mine freight. Heavy the way useful things are.')]},
    'candles': {"salience": "ordinary", "scene": [(None, 'a parcel of candles')], "examine": [(None, 'A parcel of wax candles, mail-order. Light for an hour each, and a slow hot fuel.')]},
    'holt_parcel': {"salience": "ordinary", "scene": [(None, 'a parcel addressed to V. Holt')], "examine": [(None, 'Brown paper, twine, a name in marker: V. HOLT. Somebody upriver is waiting for this.')]},
    'hacksaw_blade': {"salience": "ordinary", "scene": [(None, 'a hacksaw blade')], "examine": [(None, 'A fine-toothed hacksaw blade, loose in the box. The keenest edge in the valley — and a saw, given a frame.')]},
    'frozen_salmon': {"salience": "ordinary", "scene": [(None, 'a frozen salmon')], "examine": [(None, 'A salmon, frozen to a plank. Food, once it thaws, and a lot of it.')]},
    'dog_food': {"salience": "ordinary", "scene": [(None, 'a sack of dog food')], "examine": [(None, "Forty pounds of kibble. Dry, dense, and edible if you're honest with yourself.")]},
    # --- pockets and luggage (players-and-kit.md) — plain first pass; Andrew tunes ---
    'pliers': {"salience": "ordinary", "scene": [(None, 'a pair of pliers')], "examine": [(None, 'Slip-joint pliers. Grip, twist, pull a nail — leverage in a small package.')]},
    'shear_pins': {"salience": "ordinary", "scene": [(None, 'a box of shear pins')], "examine": [(None, 'Mine hardware: soft steel pins meant to break first. Scrap metal, mostly.')]},
    'holt_gloves': {"salience": "ordinary", "scene": [(None, 'a pair of beaver mitts')], "examine": [(None, 'Beaver-fur mitts, hand-sewn, warmer than anything the crash brought. Somebody upriver made these for Holt.')]},
    'phone': {"salience": "ordinary", "scene": [(None, 'a phone')], "examine": [(None, 'A phone with no signal and a light that works. The battery is the clock now.')]},
    'wallet': {"salience": "ordinary", "scene": [(None, 'a wallet')], "examine": [(None, 'A worn wallet: cash, cards, a licence with a face on it. The paper burns.')]},
    'fold of cash': {"salience": "ordinary", "scene": [(None, 'a fold of cash')], "examine": [(None, 'Banknotes. Paper, out here.')]},
    "driver's licence": {"salience": "ordinary", "scene": [(None, "a driver's licence")], "examine": [(None, "A plastic card with a name and a face. Somebody's.")]},
    'pack of gum': {"salience": "ordinary", "scene": [(None, 'a pack of gum')], "examine": [(None, 'Sugar-free gum. A dozen calories of comfort.')]},
    'ring of keys': {"salience": "ordinary", "scene": [(None, 'a ring of keys')], "examine": [(None, 'House keys, a car key. Steel, and a poor scraper.')]},
    'earbuds': {"salience": "ordinary", "scene": [(None, 'a pair of earbuds')], "examine": [(None, 'Earbuds on a thin cord. The cord is copper under the rubber.')]},
    'medical pouch': {"salience": "ordinary", "scene": [(None, 'a small medical pouch')], "examine": [(None, "A nurse's pouch: gauze, tape, painkillers, a suture kit. Knowing how is the other half.")]},
    'gauze pads': {"salience": "ordinary", "scene": [(None, 'gauze pads')], "examine": [(None, 'Sterile gauze in paper. Press it on, bind it down.')]},
    'roll of medical tape': {"salience": "ordinary", "scene": [(None, 'a roll of medical tape')], "examine": [(None, 'Cloth tape that holds on skin.')]},
    'bottle of ibuprofen': {"salience": "ordinary", "scene": [(None, 'a bottle of ibuprofen')], "examine": [(None, 'Twenty tablets. Pain, fever, swelling — not hunger.')]},
    'suture kit': {"salience": "ordinary", "scene": [(None, 'a suture kit')], "examine": [(None, 'A curved needle and thread in a sterile sleeve. A point, and a way to close what a blade opened.')]},
    'lip balm': {"salience": "ordinary", "scene": [(None, 'a lip balm')], "examine": [(None, 'Wax in a tube. It burns slow and hot, if it comes to that.')]},
    'hair ties': {"salience": "ordinary", "scene": [(None, 'a few hair ties')], "examine": [(None, 'Elastic loops. Cord, in a pinch; a bowstring, in a smaller pinch.')]},
    'ballpoint pen': {"salience": "ordinary", "scene": [(None, 'a ballpoint pen')], "examine": [(None, 'A pen. A hollow tube, a spring, ink.')]},
    'steel lighter': {"salience": "ordinary", "scene": [(None, 'a steel lighter')], "examine": [(None, 'A steel windproof lighter. It works in the cold longer than a plastic one.')]},
    'hip flask': {"salience": "ordinary", "scene": [(None, 'a hip flask')], "examine": [(None, 'A steel hip flask, half full by the slosh. Spirit inside — a drink, an antiseptic, a fire starter.')]},
    'whisky': {"salience": "ordinary", "scene": [(None, 'whisky')], "examine": [(None, 'Whisky. It warms nothing, cleans a wound, and burns.')]},
    'reading glasses': {"salience": "ordinary", "scene": [(None, 'reading glasses')], "examine": [(None, 'Reading glasses — a lens. On a bright day that is a fire source.')]},
    'notebook': {"salience": "ordinary", "scene": [(None, 'a notebook')], "examine": [(None, 'A notebook, half written in. Paper and a place to leave a message.')]},
    'pocketknife': {"salience": "ordinary", "scene": [(None, 'a pocketknife')], "examine": [(None, "A folding pocketknife, sharp. The guide's, and it shows.")]},
    'brass lighter': {"salience": "ordinary", "scene": [(None, 'a brass lighter')], "examine": [(None, 'A brass lighter, full. The single most valuable object in the valley.')]},
    'compass on a lanyard': {"salience": "ordinary", "scene": [(None, 'a compass on a lanyard')], "examine": [(None, 'A baseplate compass on a cord. North is where it says.')]},
    'candy bar': {"salience": "ordinary", "scene": [(None, 'a candy bar')], "examine": [(None, 'A candy bar. Sugar, fat, and a wrapper that burns.')]},
    'sunglasses': {"salience": "ordinary", "scene": [(None, 'a pair of sunglasses')], "examine": [(None, 'Dark glasses. On the ice at noon, the difference between seeing and snow-blind.')]},
    'ski mittens': {"salience": "ordinary", "scene": [(None, 'ski mittens')], "examine": [(None, 'Thick ski mittens. Warm, and useless for anything fiddly.')]},
    'down parka': {"salience": "ordinary", "scene": [(None, 'a down parka')], "examine": [(None, 'A down parka with a hood — the warmest thing here, and worthless if it soaks.')]},
    'denim jacket': {"salience": "ordinary", "scene": [(None, 'a denim jacket')], "examine": [(None, 'A denim jacket. It stops some wind and no cold.')]},
    'cotton hoodie': {"salience": "ordinary", "scene": [(None, 'a cotton hoodie')], "examine": [(None, 'A cotton hoodie. Comfortable, and a cold-soaked sponge the moment it gets wet.')]},
    'sneakers': {"salience": "ordinary", "scene": [(None, 'sneakers')], "examine": [(None, 'Canvas sneakers. Wet in a minute in snow, and frozen in an hour.')]},
    'fleece jacket': {"salience": "ordinary", "scene": [(None, 'a fleece jacket')], "examine": [(None, 'A fleece. Warm even damp; it melts near a flame.')]},
    'wool overcoat': {"salience": "ordinary", "scene": [(None, 'a wool overcoat')], "examine": [(None, 'A long wool overcoat, city cut. Heavy, warm, and it forgives being damp.')]},
    'dress shoes': {"salience": "ordinary", "scene": [(None, 'dress shoes')], "examine": [(None, 'Leather dress shoes with slick soles. Not made for ice.')]},
    'snow boots': {"salience": "ordinary", "scene": [(None, 'snow boots')], "examine": [(None, 'Snow boots, insulated and dry. The kid was dressed by someone who knew.')]},
    'insulated boots': {"salience": "ordinary", "scene": [(None, 'insulated boots')], "examine": [(None, 'Rubber-and-felt boots. Dry feet, all day.')]},
    'bundle of cotton clothes': {"salience": "ordinary", "scene": [(None, 'a bundle of cotton clothes')], "examine": [(None, 'Shirts and tees. Layers, strips, bandages, tinder — cotton does everything badly and everything.')]},
    'bath towel': {"salience": "ordinary", "scene": [(None, 'a bath towel')], "examine": [(None, 'A big cotton towel. A sheet, a wrap, a drying cloth.')]},
    'toiletry bag': {"salience": "ordinary", "scene": [(None, 'a toiletry bag')], "examine": [(None, 'A zip bag of toiletries. More useful than it looks.')]},
    'dental floss': {"salience": "ordinary", "scene": [(None, 'dental floss')], "examine": [(None, 'Fifty metres of waxed nylon thread on a spool. Strong cord, thin.')]},
    'disposable razor': {"salience": "ordinary", "scene": [(None, 'a disposable razor')], "examine": [(None, 'A razor. A small keen edge that dulls fast.')]},
    'bottle of hand sanitizer': {"salience": "ordinary", "scene": [(None, 'a bottle of hand sanitizer')], "examine": [(None, 'Alcohol gel. It cleans a wound and it takes a flame like a wish.')]},
    'box of tampons': {"salience": "ordinary", "scene": [(None, 'a box of tampons')], "examine": [(None, 'Cotton, compressed and sterile: tinder, and packing for a wound.')]},
    'paperback novel': {"salience": "ordinary", "scene": [(None, 'a paperback novel')], "examine": [(None, 'A paperback. Three hundred pages of tinder, or of company.')]},
    'laptop': {"salience": "ordinary", "scene": [(None, 'a laptop')], "examine": [(None, 'A laptop, screen cracked. The battery is a spark source, once, if you know how.')]},
    'tangle of cables': {"salience": "ordinary", "scene": [(None, 'a tangle of cables')], "examine": [(None, 'Charging cables. Copper inside; cord outside.')]},
    'steel water bottle': {"salience": "ordinary", "scene": [(None, 'a steel water bottle')], "examine": [(None, 'A steel bottle, insulated. A vessel that can sit by a fire.')]},
    'bag of trail mix': {"salience": "ordinary", "scene": [(None, 'a bag of trail mix')], "examine": [(None, 'Nuts and raisins. Dense calories.')]},
    'hockey stick': {"salience": "ordinary", "scene": [(None, 'a hockey stick')], "examine": [(None, 'A hockey stick. A straight, strong length of wood.')]},
    'roll of hockey tape': {"salience": "ordinary", "scene": [(None, 'a roll of hockey tape')], "examine": [(None, 'Cloth tape. Grip, splint, repair.')]},
    'hockey pads': {"salience": "ordinary", "scene": [(None, 'hockey pads')], "examine": [(None, "Foam shin pads with plastic shells. Warm on the legs, and a sled's worth of padding.")]},
    'acoustic guitar': {"salience": "ordinary", "scene": [(None, 'an acoustic guitar')], "examine": [(None, 'An acoustic guitar, neck cracked. Six steel strings, a wooden neck, a hollow body.')]},
}
