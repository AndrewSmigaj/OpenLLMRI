# The rescue graph — goals × paths × the scarce resource each path burns × where it sits

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07).** The single artifact that
> makes rooms purposeful and "several ways of doing things" checkable: for every goal, ≥3 paths;
> for every path, the DISTINCT scarce resource it spends and the rooms it runs through. Compiled
> from GDD §37–39 (additive confidence; distinct resources), the valley design (`world/map.md` §1:
> each region anchors one route; the six currencies; `report.md` §2: the four routes as room
> itineraries) and the nine room censuses. Every path here becomes a **probe chain**
> (`probes/graph.py`); the ≥3-paths rule becomes a count the runner reports. Promotes to
> `docs/scenarios/whiteout/rescue-graph.md` on approval; the P5 systems implement it.

## 1. Goals (what "win" and "not lose" decompose into)
**Stay alive** — warmth · water · food · injury (each a goal with paths).
**Be found** — rescue confidence = Σ channels ≥ threshold inside a weather window, ≥4 winning
combinations, no single object required by all (GDD §39): stay-and-signal · beacon (ELT) · radio ·
visual · travel/shelter.
**Keep the party alive** — the injured co-player (carry, bind, warm). *(The pilot dies within the first
day and cannot be talked to — scripted lines only, Andrew 2026-09-16; whether his lines carry clues
is reviewed in the pilot's document; his body is a food path and a moral question.)*

## 2. The currencies (map.md §1) — a path must spend a DIFFERENT key account from its siblings
daylight · warmth · sweat (deferred cold) · tools · knowledge · risk. Every path also spends the
common survival economy (wood, food, daylight); the KEY resource is what makes route choice real.

## 3. The graph (v1 — the crash cluster + the valley's anchors)

### WARMTH (the antagonist is cold; GDD's warmth floor guarantees a fire-less night is survivable)
| path | key resource | rooms | probe chain (seed) |
|---|---|---|---|
| fire (7 methods — fire-and-shaping §6) | fuel + an ignition source | treeline / north wood (fuel); the source's room | lighter path; bow-drill path; battery path |
| insulation salvage | tools (to strip) + time | mid/rear cabin (foam, batting, blanket, engine cover, clothes) | `wear blanket` · `cut cushion` → stuff jacket · `wear engine cover` |
| shelter / windbreak | sweat + tools | rear cabin (block the breach with the sheet), outside (snow wall, boughs) | `cover breach with sheet` · `put boughs on floor` |
| huddle + fuselage + body heat (the floor) | nothing but proximity | any enclosed zone | `huddle with agent-2` (P6) |
Softlock guard: the floor path needs no object; the fire paths need ≥2 different sources present
at start (the lighter AND the flare AND the battery AND the friction kit are all in the cluster).

### WATER
| path | key resource | rooms | chain |
|---|---|---|---|
| the canteen / thermos as found | knowledge (search) | cockpit, rear cabin | `search backpack` → `drink from canteen` |
| melt snow/ice by fire in a vessel | fuel + a vessel | anywhere + fire | `put snow in thermos` → `put thermos by fire` → `drink` |
| melt by body heat (slow, costs warmth) | warmth | any | `put snow in canteen` → wear it under the jacket (time) |
| the lake lead / the seep (valley) | risk + daylight | inlet_mouth, shore | `fill canteen from lead` |
Eating snow is always possible and always costs heat (the manual's lesson; a probe with a REDIRECT-
with-consequence, not a refusal).

### FOOD
| path | key resource | rooms | chain |
|---|---|---|---|
| the kit (rations ×2, chocolate, flour, coffee tin) | search | seat pocket, survival duffel, crate | `open tin` → `eat rations` |
| the country (grubs, cranberries, hare snare, fish) | knowledge + tools + daylight | tamarack, tussocks, willows, the lead | `set snare with paracord at willows` (P5) |
| the pilot's body | the moral price (moral layer §3) | cockpit | `butcher pilot with knife` |
| Holt's cache | travel | homestead | the travel route's reward |

### INJURY (the cut forearm; frostbite; a co-player's break)
| path | key resource | rooms | chain |
|---|---|---|---|
| the first-aid kit (bandage, tape) | search | mid cabin bin | `press wound` → `wrap arm with bandage` |
| improvised (spare shirt strips, whisky as antiseptic, paracord + a rod as a splint) | tools + knowledge | rear cabin, duffel | `tear shirt` → `pour whisky on wound` → `wrap arm with strip` |
| warmth for frostbite (skin-to-skin, no rubbing — the manual) | warmth | any | `wrap hands in socks` · sit by fire |

### BE FOUND — the five channels (each a separate account; ≥4 combinations reach threshold)
| channel | key resource | rooms | clue paths (≥3 each) | chain |
|---|---|---|---|---|
| stay-and-signal (fire on the ice; the tire's black smoke; a ground sign) | fuel logistics + wind engineering | ice_flat, gear_gouge, crash site | the manual's SIGNALS page · the chart's search grid note · the reflector's glint (examine) | `put oil quart on fire` (smoke) · `put boughs on ice` (SOS) |
| beacon (ELT) | conductor + elevation | tail_section (ELT), cockpit panel (wire) or dooryard cable, fuselage_top / the_knob | the manual's 121.5 page · examine the ELT ("antenna sheared") · the sheared base on fuselage_top | `take elt` → `tie wire to elt` → `go to fuselage top` → `tie wire to antenna base` |
| radio | carry logistics + weather windows (the battery is 12 kg in the nose cowling) | cockpit, outside_nose (battery), the_knob | static-but-powered implies antenna · the pilot's fragment · the chart's ridge bearing | `pry cowling` → `take battery` → `tie wire to radio` → `talk to radio` (the FSM: authored.py) |
| visual (mirror, reflector, flare) | the flare's one shot / sun for the mirror | crash site, ice_flat, fuselage_top | the reflector's glint · the manual · the survival mirror (census: under the seat) | `light flare` (spends the fire source) · `examine reflector` → `signal with reflector` |
| travel/shelter (the cabin) | navigation + daylight | creek → trapline → homestead | the chart (V. HOLT) · blaze marks (knowledge) · the pilot's "ridge" | the walk, priced by the P4 durations |
**Distinctness check** *(a design note for this doc's review, not a decision asked of Andrew)*: wire
(beacon/radio share the conductor — the ONE deliberate overlap the GDD flags; the dooryard cable is
the second conductor so it isn't a single point) · elevation ·
fuel/wind · the flare · navigation. No object is required by every channel; the flare is fire OR
signal (Triangularity).

### THE PILOT (scripted, dies within the first day — Andrew, 2026-09-16)
Nobody can talk to him (no language model behind him): scripted things only — moaning softly, heard
only in the cockpit, maybe a line. The June design had every fact he holds reachable by ≥3 other
paths (the ridge bearing: chart, blaze, the wreck's scar; 121.5: the manual, the ELT placard, the
radio's dial detent) — what his lines carry is reviewed in the pilot's document. Tending him is a
physical act that resolves (cover, press a wound). Death within the first day → a body (food path;
the moral layer).

## 4. What the graph asks of the world (gaps it exposes — content for Phase C)
- **Missing objects**: the survival mirror (cockpit, under the seat), the tire (the smoke column),
  the aircraft battery (outside_nose, in the cowling), the wing drains (fuel), a rock (spark).
- **Missing verbs**: press (wound), cover/block (an opening), signal (with a reflector), set (a
  snare), fill/pour-into (vessels), carry (a person), butcher.
- **Missing systems** (step 3): fire process, warmth/hunger/injury numbers, drying; (P5) rescue
  confidence arithmetic, the ELT/radio FSMs (authored.py), the pilot's clock.
- **The solvability oracle** (DR-18): every goal's ≥3 chains pass from the start state; no chain's
  consumption makes another goal's LAST chain unreachable (the global softlock check) — a fuzz over
  the graph, not just the grid.

## 5. Lens pass
### Economy (GD — is there a working economy of resources?)
- **GREEN.** Six currencies, every path priced in a different key account, the common economy
  (wood, daylight) shared — spend here, can't spend there.
### Meaningful Choices (GD)
- **GREEN, conditional.** Route choice is real only once durations (P4) and the weather window
  (P7) price travel against staying; until then the graph is a promise the probes hold open.
### Triangularity (GD — risk vs reward)
- **GREEN.** The flare; the battery walk; the pilot's body; eating snow; the thin-ice shortcut.
### Problem Solving (GD)
- **GREEN.** Every goal ≥3 paths; every fact ≥3 clues; the counts are what `make probes` reports
  once `probes/graph.py` carries the chains.
