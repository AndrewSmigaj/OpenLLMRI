# 16 — Players and kit: the slots, draws, pockets, luggage, the 206 interior

> **Status: `draft for review` (2026-09-16).**
> **Architecture counterpart:** [`../architecture/clothing-warmth.md`](../architecture/clothing-warmth.md)
> (DR-25, the shipped v1; DR-25a's region/wind/wet model is live in code — `warmth.py` — but has not
> yet been written into that doc; see §8).
> **Sources:** `docs/investigation/design/players-and-kit.md` (primary — the draw, the pockets, the
> luggage, the clothing model, the honest interior) · `docs/investigation/plane-interior.md` (the
> 2026-07 investigation that chose the aircraft and proposed its curated v1 contents) ·
> `docs/architecture/implementation-architecture.md` (DR-25a; the DR-14a/DR-15a amendment,
> 2026-09-07 late and 2026-09-16, promoted on Andrew's review) ·
> `docs/investigation/design/00-provenance-audit.md` §1–§2 · code:
> `game/world/scenarios/whiteout/characters.py`, `objects.py`, `build.py`;
> `game/world/sim/systems/warmth.py`.

---

## 2. Provenance

### Andrew's decisions

- **Each player starts with a different clothing and injury draw and stuff in their pockets;
  luggage has stuff in it; the clothing system impacts warmth loss and other things; the plane is
  fine (the 206).** (2026-09-07, recorded in the DR-14a/DR-15a amendment and the provenance audit
  §1.) Nothing about a player's starting kit is chosen; it is decided the moment the run begins.
- **The four-seat interior (§4.6 below) is a go; the kid is in — a party of four or five; the crash
  is in December.** (2026-09-16, `players-and-kit.md`'s own banner and the same DR amendment.) The
  kid's inclusion sets the party at four adults plus the kid, or four without; exactly what a fifth
  player carries is still a proposal, not signed off item by item (open question 1).

### Proposals (Claude)

Everything else here is a proposal for review, per the provenance audit's own table
(`00-provenance-audit.md` §2: "players-and-kit — the five slots, luggage contents, clothing v2, the
206 interior"):

- The five specific slots — guide, townie, nurse, salesman, kid — and exactly what each wears,
  carries in their pockets, is injured by, and finds in their bag (§4.1–§4.3).
- The clothing model's mechanism — coverage by body region, the shell's wind/waterproof numbers,
  the wet fraction, sweat, dexterity, movement, signal, sharing (§4.4; designed in full in
  **08 — Warmth, clothing and shelter**).
- The honest interior's specific furniture — the seat labels 1A/1B/2A/2B and the right seat, the
  hat shelf, the baggage bay, the jammed cargo door, and the panel inventory (§4.5–§4.6): proposed
  2026-09-07 in `plane-interior.md` and `players-and-kit.md` §5, and approved as a four-seat interior
  on 2026-09-16 — but not a sign-off on every named object inside it.
- What this asks of the engine (§4.7) and the lens pass (§4.8).

---

## 3. In one paragraph

You come to belted into a seat you did not choose, wearing whatever you happened to have on when you
got on the plane, with a stranger's court date or ski trip or sales call in your pockets instead of
anything meant for this. The guide has a parka and a pocketknife and bruised ribs; the kid has a ski
jacket, mittens and a duffel full of hockey gear; the townie has a denim jacket, no gloves, and a
phone that is, for now, the party's only clock and light. What you are wearing when the plane stops
moving is the single biggest thing that decides whether you are cold tonight — and it is different
for everyone, which is what turns "who gets the good coat" into a question the party has to answer
together, in the first hour, long before anyone says the word "rescue."

---

## 4. The design

### 4.1 The draw (one slot per player, deterministic from the run seed)

A **slot** is a seat, plus what its occupant wore, carried, and suffered in the crash. Five slots are
authored; the run seed is meant to permute which player gets which — nothing is random at runtime
(§6, §8).

| slot | seat | wearing | pockets | injury | their bag |
|---|---|---|---|---|---|
| **the guide** (flying up to a lodge job) | right seat | parka (down, hood), wool base layer, insulated boots, gloves, wool hat | pocketknife, lighter, a chocolate bar, a compass on a lanyard | bruised ribs (slow, painful work; no bending) | the survival duffel is HIS (the kit is legally the plane's; his duffel adds a headlamp, a ferro rod, a steel cup) |
| **the townie** (going home from a court date) | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves | phone (light, clock, a dead battery by day 2), wallet (cash, cards, ID — paper), gum, keys, earbuds (wire) | a cut forearm (bleeding; the census wound) | a soft suitcase: cotton clothes, a towel, toiletries (floss = cordage; razor = edge; sanitizer = fire starter; tampons = tinder + wound packing), a paperback |
| **the nurse** (home leave) | 1B | fleece jacket, hiking boots, a scarf, thin gloves | a small med pouch (gauze, tape, ibuprofen, a suture kit — she knows how; the player has to), lip balm (wax), hair ties (cordage), a pen | a sprained ankle (walking costs double; splint it) | a backpack: canteen, spare shirt, a wool sweater, a headnet, a book of matches |
| **the salesman** (mine supply run) | 2A | wool overcoat, dress shoes, leather gloves, a good scarf | a metal lighter, a hip flask (whisky), reading glasses (a lens! sun only), a notebook (paper) | concussion (fatigue faster; confusion messages the first day) | a laptop bag: laptop (battery — sparks, heat, then dead), cables (wire), a metal water bottle, snacks, a wool blanket (bought for the trip) |
| **the kid** (16, visiting family) | 2B | ski jacket, snow pants, snow boots, mittens | a phone, a candy bar, a multitool (a gift), sunglasses (snow blindness) | shock: fine physically, slower to act day one | a duffel: hockey gear (a stick = a rod; tape = tape; pads = foam), a sleeping bag |

The **pilot** keeps his slot as designed (jacket, lighter, the radio, the manual, the chart) — he is
not a player slot; his own arc belongs to **12 — The pilot and bodies**.

The draw makes the party heterogeneous, which is what makes sharing a real act — the blanket, the
gloves, the huddle — instead of five copies of the same survivor with no reason to talk to each
other.

### 4.2 Pockets

Pockets are a per-character container: stowed, and already revealed to their owner (`search me` /
`inventory` needs no `open` or `search` step first — the owner already knows what is in their own
pockets). Everything in §4.1's table is a real object with real materials: a phone is glass and
plastic with a `powered` state and a light; a wallet is leather with paper inside; lip balm is wax
(fuel); earbuds are copper wire in rubber; keys are steel (a poor scraper). None of it is decoration —
the townie's phone is the party's only clock and light until its battery goes, and that is meant to
matter.

### 4.3 Luggage (the baggage bay, and what the crash threw into the cabin and along the trail)

Every bag in §4.1, plus: the **mail sack** (letters, postmarks, a parcel of candles, a parcel
addressed to V. Holt), the **freight** (flour, the coffee tin, dog food, a box of shear pins, a
toolbox — screwdrivers, pliers, a hacksaw blade that is both an edge and a saw), a **cooler** (a
family's frozen fish — a vessel), and a **guitar case** (a story object: the strings are wire, the
case is a sled, the neck is wood).

The rule that decides where all of this actually sits (`plane-interior.md` §8b, "the crash is the
difficulty engine"): realism supplies the inventory; the crash supplies the difficulty. An intact
survival kit sitting in the open would solve the game in one `search`, so the law says the kit was
aboard and the crash decides where it is now and what shape it is in — the toolbox is in the crushed
tail cone (pry it open), the cooler is under a drift on the trail (dig for it), and the hacksaw blade
— the keenest edge in the valley — is a walk away. The **power ∝ cost** curve follows from the same
rule: the more a thing solves, the farther, deeper, or more broken the crash left it. A paperback is
at your feet; the hatchet is a hundred meters out under snow with a cracked haft.

### 4.4 The clothing system (DR-25 → v2)

Each wearable declares which body regions it covers, how much wind its outer shell stops, how
waterproof it is, and its mass; it inherits a wetness quantity and damage state from the world's
general object model. From that, the model derives warmth loss by region, a sweat/drying cycle, a
dexterity penalty for cold or mittened hands, a movement effect from footwear, a visual-signal value,
and the physics of sharing — the huddle bonus among them. This mechanism, its numbers, and what of it
is built versus still designed is **08 — Warmth, clothing and shelter** in full; this document keeps
only the draw that feeds it (§4.1).

### 4.5 The aircraft

The July investigation (`plane-interior.md` §1) weighed two classic Alaska bush planes against "big
enough for two rows of seats in the back, pilot only aboard": the **Cessna 206/207 Stationair** (six
seats, piston single, a clamshell cargo double-door on the right rear, a hat shelf and netted baggage
bay behind the last row) and the **de Havilland DHC-2 Beaver**. It recommended the 206-class piston
single on wheel-skis — the default choice — and flagged one realism problem with the game's earlier
fiction: real bush planes have no airline-style overhead bins, only a hat shelf, floor tie-down
tracks, and cargo netting. Andrew's decision (2026-09-07) settled the aircraft: "the plane is fine
(the 206)."

The aircraft's own legal cargo is the reason the survival economy exists at all: Alaska Statute
AS 02.35.110 requires a minimum emergency kit aboard any in-state winter flight — a week of rations
per occupant, an axe or hatchet, a first-aid kit, two sealed signaling devices, and, winter-specific
(Oct 15–Apr 1), snowshoes, a sleeping bag, and a wool blanket per occupant. The pilot was legal. The
kit is in the tail. This single fact justifies the survival economy without inventing anything
(`plane-interior.md` §7).

### 4.6 The honest interior (the 206; supersedes the airline fiction)

- **Seats**: pilot plus the right seat up front; **1A/1B** (row one), **2A/2B** (row two) — the
  labels the manifest in the pilot's kneeboard uses to name who sat where, itself a clue and a story.
  Each seat is the same parts-machine (cover, cushion, belt, bolts — the seat-row exemplar in
  **17 — Rooms and living rooms**) with a DIFFERENT damage and find: 1A intact; 1B wrenched (the
  salesman's laptop bag under it); 2A thrown loose (a movable frame — a windbreak, a sled base); 2B
  thrown against the hull (the life-vest pouch: vest, straps, a whistle).
- **The hat shelf** (behind row two): hats, a scarf, the kid's helmet — a shelf, not a bin.
- **The baggage bay** behind it: the cargo net over the bags (cut it or unhook it), the survival kit
  lashed to the floor rings, the freight and the mail against the bulkhead.
- **The double cargo door** on the right rear: jammed by the impact (pry it) — the second way out
  besides the breach; ice seals it overnight as an event.
- The old "overhead bins" become the hat shelf and the cargo net — the same open/pry/search loops,
  re-ficted to what a real bush plane actually carries.
- **Windows**: crazed plexiglass — sharp sheets when broken, and a possible cover for the breach.
- **Up front**: the six-pack instruments, the whiskey compass on the glareshield (takeable), the ELT
  remote placard (the breadcrumb pointing at the tail), headsets on the yokes, the halon
  extinguisher, the magneto key in the ignition, the kneeboard with the manifest and the sectional
  chart.

### 4.7 What this asks of the engine

Small — mostly content plus the warmth v2 model: `characters.py`'s slot table, plus a pure
`outfit(seed, slot) -> rows`; a loader step that dresses a character and fills their pockets at run
start (the instance-spawn work, and a `dress` helper smokes can call directly); `covers` / `wind` /
`waterproof` on wearable rows; `warmth.py` v2 (regional loss, wet fraction, wind multiplier,
dexterity, the huddle); a `give` verb; wetness as grams on things; a phone with a battery process.
Probes: each slot's first-night warmth band; "give gloves to the townie"; "wear the sweater under
the coat"; "huddle under the blanket with 2".

### 4.8 Lens pass

- **The Player** (GD — who are they, what do they bring?) — GREEN. Five people with different coats
  is a party; four identical survivors is a chore list.
- **Cooperation** (GD) — GREEN. Heterogeneous kit is the engine of sharing; the huddle and the glove
  hand-off are the first co-op acts, hours before the antenna.
- **Fairness** (GD) — YELLOW. The townie's draw is harsh; the party's job is to fix it. The seed is
  meant to permute slots so no one player is always the townie — not yet true at runtime (§8).

---

## 5. Interactions

**This depends on:**
- **08 — Warmth, clothing and shelter** — the draw's worn items are the input to the warmth score;
  the draw itself is only summarized here (§4.4).
- **Containment** (`../architecture/containment.md`, DR-24) — pockets, the survival duffel, the
  toolbox, and the cargo net are all found by the one reveal rule (`open` or `searched`); nothing on
  a player's body is a list, it is a container.
- **Presentation** (`../architecture/presentation.md`, DR-23) — the self-view (`examine me` / `look
  at me`) weaves the draw's worn items and wounds into one composed sentence.
- **Determinism/seeding** (DR-12) — the run's per-seed RNG substrate is what a seed-permuted slot
  assignment would use; it exists elsewhere in the architecture and is not yet wired to slot
  assignment (§8, open question 2).
- **15 — Moral and social layer** — the guide's duffel is legally the plane's, not his; the pilot's
  wallet and jacket raise the dignity question of stripping a body.

**These depend on it:**
- **17 — Rooms and living rooms** — the seats are the parts-machine that carries each slot's
  luggage; the seat labels proposed here (§4.6) are what that document's seat-row exemplar was
  recast to describe.
- **02 — The experience** — the first night's warmth band differs by slot, which is the sample
  week's opening beat.
- **20 — The agent player and research** — an agent draws a slot exactly as a human does.

---

## 6. Open questions

1. **Are the five slots' specific contents final, or a placeholder for a fuller pass?** The
   provenance audit lists the whole table as Claude's proposal; Andrew's 2026-09-16 approval covers
   the four-seat interior and the kid's inclusion, not item-by-item sign-off on what each slot
   carries. *Options:* (a) approve the table as shipped — it is already built and probed (§8); (b)
   revise individual slots at the review sitting as Andrew reacts; (c) treat it as a placeholder and
   redo it from scratch. **Recommendation: (b)** — the table is a working baseline with real physics
   behind every item; review it slot by slot rather than wholesale.
2. **Does the seed actually permute who gets which slot?** The design's fairness note depends on it
   ("the seed permutes slots so no player is always the townie"), but `build.py::dress()` currently
   takes an explicit `slot` argument with no seed-driven permutation — nothing assigns slots to
   players at all yet. *Options:* (a) build the permutation now, using the seeded RNG substrate
   DR-12 already provides; (b) leave slot assignment to whoever forms the party (sign-up, not a
   draw); (c) permute only across repeated runs, not within one. **Recommendation: (a)** — the
   fairness claim is currently just a sentence in a document; it needs the mechanism it describes
   before more than one sitting relies on it.
3. **How many players does a run support?** Five slots are authored (four adults plus the kid).
   *Options:* (a) exactly five, no more, no fewer; (b) a run seats any subset of the five, and an
   unfilled slot's occupant becomes an unplayed body or is simply absent; (c) more slots get authored
   later for a bigger party. **Recommendation: (b)** — nothing requires every slot to be a human or
   an agent, and runs "for agents only" (per the framing every document keeps) may want fewer than
   five.
4. **Are a slot's luggage contents welded to the slot, or do they permute independently of the
   clothing/injury draw?** *Options:* (a) luggage is furniture of the bag, keyed to the seat, and
   travels with whoever draws that slot; (b) luggage is a second, independent draw; (c) no
   permutation at all — luggage stays exactly where it is regardless of the draw.
   **Recommendation: (a)** — simplest, and consistent with the guide's duffel being "legally the
   plane's," not his personally.
5. **The guide's duffel and the nurse's backpack are missing their named extras.** §4.1's table lists
   the guide's duffel as adding a headlamp, a ferro rod and a steel cup, and the nurse's backpack as
   adding a wool sweater, a headnet and a book of matches; neither appears in `objects.py` — only the
   pre-existing duffel (multitool, paracord, socks) and backpack (canteen, spare shirt) are there.
   **Recommendation: add the missing rows** — small, mechanical, and closes a real gap between this
   document and the shipped table.
6. **The four-seat interior is approved but not built.** `characters.py`'s slot `seat` fields already
   say `1A` / `1B` / `2A` / `2B` / `right seat`, but the only seat objects in `objects.py` are the
   earlier six-seat draft's leftovers (`seat`, ident `11B`, in `mid_cabin`; `seat2`, ident `12C`, in
   `rear_cabin`) — there is no seat object for 1A, 2A, or the right seat, and no hat shelf or cargo
   door object anywhere. **Recommendation: queue the recast as ordinary content work** behind the
   existing authoring seams (`objects.py` / `characters.py` rows only) — it needs no new mechanism,
   just the rows this document already specifies (§4.6).

---

## 7. Review log

*Not yet reviewed.*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

## 8. What exists today

**Built**
- The crash draw for all five slots — worn items, pockets, injuries — exactly as §4.1's table:
  `game/world/scenarios/whiteout/characters.py` (`SLOTS`, `outfit()`, `character_state()`).
- The clothing v2 fields the draw needs (`covers`, `wind`, `waterproof`) and the model that reads
  them (regional loss, wind multiplier, wet fraction, the mitten fine-work gate, warmth bands):
  `game/world/sim/systems/warmth.py`.
- Dressing at spawn: `game/world/scenarios/whiteout/build.py::dress()` — called with an explicit
  slot argument (no seed permutation; open question 2).
- Most of §4.3's luggage: the townie's suitcase and toiletry bag (floss, razor, sanitizer, tampons)
  and paperback; the salesman's laptop bag (laptop, cables, water bottle, snacks); the kid's hockey
  duffel (stick, tape, pads); the mail sack (letters, twine) and the parcel addressed to V. Holt
  (beaver mitts inside); the freight crate and toolbox (pliers, hacksaw blade, shear pins) and the
  dog food; the cooler (frozen fish); the guitar case (a guitar whose strings are wire and neck is
  wood, as parts) — all in `game/world/scenarios/whiteout/objects.py` (its "the luggage, the mail
  and the freight" section).
- Tests and probes: `game/tests/sim/test_kit.py` (every slot's rows are sound; luggage is placed and
  reachable; a dressed actor sees its own pockets); `game/world/scenarios/whiteout/probes/kit.py` —
  fifteen probes across the five slots and the luggage, all `status: pass`.

**Designed, not built**
- The seed-permuted slot assignment (open question 2) — nothing wires DR-12's per-run seeded RNG to
  "which player gets which slot."
- The guide's duffel extras (headlamp, ferro rod, steel cup) and the nurse's backpack extras (wool
  sweater, headnet, book of matches) named in §4.1 — open question 5.
- The four-seat interior recast (§4.6) — open question 6: the seat labels are designed and
  referenced in `characters.py`, but no seat objects, hat shelf, or cargo door exist for it in
  `objects.py` / `zones.py` / `spaces.py`.
- `give X to Y`, the huddle (two bodies, one blanket, shared loss), the sweat/drying cycle, and
  dexterity decaying by the minute for bare hands (§4.4, §4.7) — `warmth.py` has only the binary
  mitten check (`fine_work_ok`); `huddle` exists only as a parser synonym mapped to `put`
  (`game/world/sim/parser/vocab.py`) and one `todo`-status phrasing probe.
- A phone battery process — the phones carry a `battery` number in state, but nothing ticks it down.

**Nothing**
- The satellite communicator / PLB question (`plane-interior.md` §9) — omitted per the 2026-07-04
  decision to backlog it.
