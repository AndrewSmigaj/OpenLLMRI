# Players & kit — starting draws, pockets, luggage, the clothing system, and the plane's honest interior

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07, late).** Andrew decided:
> each player starts with a different clothing and injury draw and stuff in their pockets; the
> luggage has stuff in it; the clothing system impacts warmth loss and other things; the plane is
> the 206-class single on wheel-skis. This doc specifies the draws and the clothing model and
> proposes the plane's honest interior (cargo net, hat shelf, jammed cargo door; seats 1A/1B/2A/2B
> + the right seat). Promotes to `docs/architecture/clothing-warmth.md` v2 (DR-25a) + the
> `characters.py` / `objects.py` tables on approval.

## 1. The draw (deterministic from the run seed; one slot per player)
A **slot** = a seat + what they wore + what they carried + what the crash did to them. Slots are
authored (4–6); the seed permutes which player gets which. Nothing is random at runtime.

| slot | seat | wearing | pockets | injury | their bag |
|---|---|---|---|---|---|
| **the guide** (was flying up to a lodge job) | right seat | parka (down, hood), wool base layer, insulated boots, gloves, wool hat | pocketknife, lighter, a chocolate bar, a compass on a lanyard | bruised ribs (slow, painful work; no bending) | the survival duffel is HIS (the kit is legally the plane's; his duffel adds a headlamp, a ferro rod, a steel cup) |
| **the townie** (going home from a court date) | 1A | denim jacket, cotton hoodie, jeans, sneakers, no gloves | phone (light, clock, a dead battery by day 2), wallet (cash, cards, ID — paper), gum, keys, earbuds (wire) | a cut forearm (bleeding; the census wound) | a soft suitcase: cotton clothes, a towel, toiletries (floss = cordage; razor = edge; sanitizer = fire starter; tampons = tinder + wound packing), a paperback |
| **the nurse** (home leave) | 1B | fleece jacket, hiking boots, a scarf, thin gloves | a small med pouch (gauze, tape, ibuprofen, a suture kit — she knows how; the player has to), lip balm (wax), hair ties (cordage), a pen | a sprained ankle (walking costs double; splint it) | a backpack: canteen ✓, spare shirt ✓, a wool sweater, a headnet, a book of matches |
| **the salesman** (mine supply run) | 2A | wool overcoat, dress shoes, leather gloves, a good scarf | a metal lighter, a hip flask (whisky ✓), reading glasses (a lens! sun only), a notebook (paper) | concussion (fatigue faster; confusion messages the first day) | a laptop bag: laptop (battery — sparks, heat, then dead), cables (wire), a metal water bottle, snacks, a wool blanket ✓ (bought for the trip) |
| **the kid** (16, visiting family — optional 5th) | 2B | ski jacket, snow pants, snow boots, mittens | a phone, a candy bar, a multitool ✓ (a gift), sunglasses (snow blindness!) | shock: fine physically, slower to act day one | a duffel: hockey gear (a stick = a rod; tape = tape; pads = foam), a sleeping bag ✓ |
The **pilot** keeps his slot as designed (jacket, lighter, the radio, the manual, the chart).
What a player WEARS at the crash is the largest single determinant of the first night; the draw
makes the party heterogeneous, which is what makes sharing a real act (the blanket, the gloves,
the huddle). The kid is optional (party of four) and exists to make "who gets the good coat" a
question with a right answer.

## 2. Pockets (a container the player starts with; `search me` / `inventory`)
Pockets are a per-character container (stowed, revealed to its owner). Everything above is a real
object with materials: a phone is glass + plastic with `powered` and a light; a wallet is leather
with paper inside; lip balm is wax (fuel); earbuds are copper wire in rubber; keys are steel (a
poor scraper). Nothing here is decoration — the townie's phone is the party's only clock and light
until the batteries go, and that matters.

## 3. Luggage (the baggage bay + what the crash threw into the cabin and the trail)
Every bag above plus: the **mail sack** ✓ (letters, postmarks, a parcel of candles, a parcel for
V. Holt), the **freight** ✓ (flour, the coffee tin, dog food, a box of shear pins, a toolbox:
screwdrivers, pliers, hacksaw blade = edge + a saw), a **cooler** (a family's fish — frozen; a
vessel), a **guitar case** (a story object: strings = wire, the case = a sled, the neck = wood).
The anti-easy rule holds: the toolbox is in the crushed tail cone (pry), the cooler is under the
drift on the trail (dig), the hacksaw blade is the second real edge and it is a WALK away.

## 4. The clothing system (DR-25 → v2)
Each wearable declares: `covers` (head · torso · arms · hands · legs · feet — a list),
`insulation` (from its material ✓), `wind` (0–1: a shell stops wind, a sweater doesn't),
`waterproof` (0–1), `mass_g` ✓, and inherits `wet` (grams of water) and `damage` state. Derived:
- **Warmth by region**: the body loses heat per region by exposure × (1 − coverage insulation);
  bare hands and feet drive frostbite; a bare head is a third of the loss. Layers add; the outer
  shell's `wind` multiplies the whole stack; wet insulation counts for a fraction that falls with
  wetness (down to zero for soaked down).
- **Sweat**: hard activities in a heavy stack add water to the inner layer (the deferred cold
  debt — the manual's "don't sweat" lesson). Drying is a process by a fire or on the body.
- **Dexterity**: bare hands in the cold lose fine-work capability by the minute (tying, striking a
  match, the drill); thick mittens can't do fine work at all (take them off, pay warmth).
- **Movement**: snow boots vs sneakers changes wet-feet rate and speed; snowshoes double speed on
  snow; dress shoes on ice is a fall.
- **Signal**: a bright jacket on the wing is visual confidence; a dark one is not.
- **Sharing**: `give X to Y`, `wear X` from another's hand, the blanket over two (`huddle`) — the
  huddle bonus is real physics (two bodies, one blanket, shared loss).
Status words, never numbers: "your hands are numb", "your feet are soaked", "you are sweating in
the parka".

## 5. The plane's honest interior (the 206; supersedes the airline fiction)
- **Seats**: pilot + right seat up front; **1A/1B** (row one), **2A/2B** (row two) — labels the
  chart uses (the manifest in the pilot's kneeboard names who sat where: a clue and a story).
  Each seat is the parts-machine ✓ with a DIFFERENT damage and find (living-rooms.md §3 recast to
  four seats): 1A intact; 1B wrenched (the salesman's laptop bag under it); 2A thrown loose (a
  movable frame: windbreak, sled base); 2B thrown against the hull (the life-vest pouch: vest,
  straps, a whistle).
- **The hat shelf** (behind row two): hats, a scarf, the kid's helmet — a shelf, not a bin.
- **The baggage bay** behind it: the cargo net over the bags (cut or unhook), the survival kit
  lashed to the floor rings, the freight and the mail against the bulkhead.
- **The double cargo door** on the right rear: jammed by the impact (pry) — the second way out
  besides the breach; ice seals it overnight (an event).
- The two "overhead bins" → the hat shelf and the cargo net. Same open/pry/search loops.
- **Windows**: crazed plexiglass (sharp sheets when broken; a cover for the breach).
- **Up front**: the six-pack instruments, the whiskey compass on the glareshield (takeable), the ELT
  remote placard (the breadcrumb to the tail), headsets on the yokes, the halon extinguisher, the
  magneto key in the ignition, the kneeboard with the manifest and the sectional chart ✓.

## 6. What this asks of the engine (small, mostly content + warmth v2)
`characters.py` (the slots table) + a pure `outfit(seed, slot) -> rows`; a loader step that dresses
a character and fills pockets at run start (P6's instance spawn; a `dress` helper for smokes);
`covers`/`wind`/`waterproof` on wearable rows; `warmth.py` v2 (regional loss, wet fraction, wind
multiplier, dexterity, the huddle); `give`; wetness as grams on things; a phone with a battery
process. Probes: each slot's first-night warmth band; "give gloves to the townie"; "wear the
sweater under the coat"; "huddle under the blanket with 2".

## 7. Lens pass
### The Player (GD — who are they, what do they bring?) — GREEN. Five people with different
coats is a party; four identical survivors is a chore list.
### Cooperation (GD) — GREEN. Heterogeneous kit is the engine of sharing; the huddle and the
glove hand-off are the first co-op acts, hours before the antenna.
### Fairness (GD) — YELLOW. The townie's draw is harsh; the party's job is to fix it. The seed
permutes slots so no player is always the townie.
