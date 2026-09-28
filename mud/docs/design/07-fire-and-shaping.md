# 07 — Fire and shaping

> **Status: reviewed with Andrew 2026-09-18.** **Architecture counterpart:** none named in the design
> index; the closure mechanism this document rides is
> [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md) §2 (forms) and §3
> (derived capabilities), DR-26 in
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md).

## 2. Decisions

### Andrew's decisions
- **(2026-09-07, 2026-09-28)** Andrew walked the lighter path and the bow-drill path step by step.
  Rubbing two sticks together at random does not make fire, and the game says so. Friction fire works
  in its real ways, each at a real cost in stamina: a stick rubbed hard up and down a trough cut in a
  board (the trough, or fire plough), a stick spun between the palms in a notch (the hand drill), and
  the bow drill, which costs the least; two people spinning one stick in turns make it far easier; a
  failure can carry a hint in the world's voice; a lighter lights tinder, not a branch.
- **(2026-09-28)** Nobody starts with a lighter or matches in hand. A lighter is fine, but it has to be
  found; there can be more than one, never everywhere. There can be more than one book of matches, and
  the easier one is to find, the fewer matches it holds. No whole fire kit; a flint striker (a ferro
  rod) in a duffel is fine. The dead pilot has a book of matches with two left. Not too hard, and never
  handed over (§4.6).
- **(2026-09-07)** State the act, not the aim: a player says what they do (`shake thermos`), not what
  they want. The one aim-verb is `make` (below).
- **(2026-09-16)** Never a menu, applied to fire: no reply lists what would work, and mastery is never
  packed into a command the game hands the player — a ritual shortcut such as `make fire with bow
  drill`, unlocked once learned, would be the game offering an option.
- **(2026-09-18)** `make` is the one aim-verb (document 04 §3.9): `make fire` alone asks how, and
  nothing else; given the means, it performs the first act they imply. Fire's goal rows are §4.9.
- **(2026-09-18)** The code's 26 forms are canonical; the closure spec's table follows them.
- **(2026-09-18)** The seven methods are priced by what each spends — time, a tool, the weather,
  knowledge, the flare's one shot. A failure-rate axis is added only if one method still dominates in
  play.
- **(2026-09-18)** Claude drafts the ignition weights and the threshold together with the
  fuel-to-heat curve, for Andrew's review (`PLAN.md` A5).
- **(2026-09-18)** This document's stage ladder — `unlit lay → catching → burning → established →
  embers → dead` — is the design; the older ladder in `systems/fire.py` is reconciled to it.
- **(2026-09-26)** Heat is a state system: a fire heats its area and leaves residual heat around it;
  the plane's cabin is rooms like any others, with openings, open or closed, and a shared internal heat
  that a fire inside raises (2026-09-28; document 17 §4.8; the heat system's own document is `PLAN.md` A10).
- **(2026-09-27)** Characters differ in how well and how fast they do things: a woodsman lights fires
  better (document 16).
- **(2026-09-17, 2026-09-27)** Fire and smoke are rescue signals — rubber, oil and green boughs make
  smoke a search crew can see (document 14 §3.4).

### Proposals (Claude)
The ignition mechanism (the additive score, its terms, and how a character's skill enters it), the
forms mechanism, the shaping family of operations, the tending verbs, where a fire lives, the probe
chains for each method, and the framing of the two walked transcripts as seed probes are Claude's
proposals for how to realize Andrew's walkthrough and the never-a-menu rule mechanically. The
transcripts' *steps* are Andrew's own, from 2026-09-07.

## 3. In one paragraph
Nobody has fire in their pocket. Somebody searches the dead pilot and finds a book of matches with two
left — strikes one at a handful of spruce twigs in the wind and watches it die, and learns, with one
match left, to gather birch bark and dry shavings first and build from tinder to kindling to fuel.
Somewhere in the luggage there is a lighter in a jacket pocket, if anyone digs for it; a damp book of
matches in a backpack; a ferro rod in a duffel. Without any of them it is a longer, harder-won path:
carve a spindle, split a board, notch a socket, spin or drill until a thread of smoke becomes a coal
you have to blow into life — paid for in stamina and raw palms — or give up and let the cold win the
argument. Rubbing two
sticks together does nothing but warm your palms, and the game says so plainly, pointing at the physics
of why without ever naming the verb that would actually work.

## 4. The design

### 4.1 What fire needs
Fire is an **ignition source × a receptive material × air × time**. The game models:
- **Sources**, each a capability: `flame` (a lighter, a match, a burning thing), `spark` (ferro rod,
  hatchet spine on quartz, battery + wire strands), `ember` (a coal from friction or a dying fire),
  `focus` (a lens or the landing-light reflector in sun — weather-gated). A source ignites only what
  its heat can reach: a flame catches tinder and thin kindling; a spark catches only prepared tinder
  (char, fluff, birch-bark curls, fuel-soaked cloth); an ember catches a tinder *bundle* when blown;
  focus catches dark fine tinder in sun.
- **Receptivity** = material `burnability` and `ignition_difficulty` × **form thinness**. The same
  wood is a log (won't catch from a lighter), a branch (won't), a splinter (might), shavings (will).
  Thinness lowers the threshold: shavings/fluff/bundle 0.4 · strip/scrap/bark 0.25 · piece/stick 0.1 ·
  rod/branch/log 0.
- **The fire itself is a process object** with a stage ladder, a fuel load, a heat output and a smoke
  character; it lives on the heartbeat ([`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md))
  and interrupts nearby activities when its stage changes.

### 4.2 The ignition check
An additive, transparent score: `score = source_strength + receptivity(material, form) + air − wet −
wind`, checked against a threshold; every term is visible in the failure line. *"The flame licks at the
bark and blackens it, but a wrist-thick branch won't take from a flame this small. Something finer
would."* Failure **costs** something — a match, a minute, stamina on the bow — never a silent retry.

**Who is trying matters.** Characters differ in how well and how fast they do things (Andrew,
2026-09-27): a woodsman lights fires better, and a novice's attempt takes longer and fails more.
*(How skill enters the score is proposed by Claude, drafted with the weights, for Andrew's check.)*

### 4.3 The forms
The mechanism underneath is the closure model (`ontology-closure.md` §2–3, DR-26): a **form** is the
shape a quantity of material takes; materials say what a thing is made of, forms say what shape it is
in, and **capabilities** (`edge`, `point`, `leverage`, `ignition`, `flame`, `ember`, `tinder`, …) fall
out of the pair via `world/sim/affordances.derive(entity, materials)`. Capped (a derived level never
exceeds the material or form tier), authored wins (an explicit `state[axis]` overrides the derived
value; the multitool and hatchet stay hand-tuned), and every load-bearing capability has to show in the
examine text — "a shard of glass, one edge wicked-sharp" — because a capability nobody can see is the
top complaint across every property-crafting game this design draws on.

The forms — the code's 26, canonical (Andrew, 2026-09-18), and like every list here a floor the loops
grow (document 18 holds the candidates):
`blade` · `shard` · `flake` · `piece` · `scrap` · `strip` · `sheet` · `slab` / `board` · `rod` /
`stick` / `bar` / `pole` · `spindle` · `point` / `stake` · `bow` · `shavings` · `bundle` · `cord` ·
`block` · `vessel` · `ember` · `ash` · `liquid` · `cloth`. Live since closure step 1 for minted
objects; authored objects declare theirs in `OBJECT_TABLE` (the multitool is a `blade`, a bottle a
`vessel`, a branch a `rod`, paracord `cord`).

### 4.4 The shaping family
An operation family whose outputs are forms:

| verb | grammar | needs | makes |
|---|---|---|---|
| `carve X into spindle/point/stake/board/bowl` | `VERB X into <form> [with Z]` | edge ≥ .4 on the tool; X rigid & shapeable (wood, bone, antler, soft plastic); time | the form, mass conserved (shavings as by-product: tinder!) |
| `split X` [with Z] | `split log with hatchet` | heft or edge ≥ .5; X wood/ice in rod/block/log form | 2 × slab/board (the drill board) |
| `shave X` [with Z] | `shave branch with knife` | edge ≥ .3; X wood | shavings + a thinner rod |
| `whittle X` | = carve into point | | point |
| `notch X` [with Z] | `notch board with knife` | edge ≥ .3; X board/rod | `state["notched"]` (the drill socket) |
| `string X with Y` | `string branch with paracord` | X springy (wood, bend_resistance ≤ .5, rod, mass ≥ 300); Y cordage ≥ .5 | a `bow` (the cord becomes a part: `attachment: tied`) |
| `bundle X` | `bundle grass` | X tinder-class in loose/strip/fluff form | a `bundle` (the nest) |
| `strike X against Y` / `strike X with Y` | (the verb-gap step) | X spark-capable vs Y hard, or X hard vs Y | sparks (an ephemeral `spark` source for one turn) or impact |

Form pseudo-nouns arrive in the Y slot only after `into`; a real entity there means "one like that" —
the same mechanism zones use (`zone:cockpit`). Implicit accessories (a handhold for the drill, a
reachable flame for melt) are chosen when unambiguous and **named in the prose**.

### 4.5 Fire as a process
`unlit lay` → `catching` (tinder flame, 1–2 game-min, dies without kindling) → `burning` (kindling,
heat rising) → `established` (fuel load ≥ 800 g, steady heat, the warmth source) → `embers` (fuel gone;
blow + tinder restarts) → `dead` (ash). Fuel is TRANSFERred into the fire (`put branch on fire`); each
tick CONSUMEs fuel mass by material burn rate into ash and the sink; heat output is a function of stage
and fuel. **The heat goes into the world as state** (Andrew, 2026-09-26): the fire heats its area and
leaves residual heat around it — outdoors the warmed ground and hearth stones, inside the plane the
cabin's one internal heat (document 17 §4.8). Smoke reads from material toxicity (the foam warning) and
has a colour a search crew can see: rubber and oil burn dark against snow, green boughs white against
dark spruce (document 14 §3.4). Tending verbs: `blow on` / `fan` (stage push, +air), `feed` (= put
fuel), `bank` (slow burn overnight), `smother` / `douse` (out), and `tend the fire` (2026-09-28) — an
open-ended activity that keeps feeding it from the wood at hand, runs on through fast forward, and when
the wood runs out stops and drops the clock back to 15× (document 06 §4.3). Wind and wet degrade the fire; the
windbreak is a real object property ([`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md)
§4.4). **Where a fire lives:** the first burning thing on the ground with a lay becomes the fire entity
at that space; a burning thing in the hand is a torch, not a fire.

### 4.6 The seven methods
Each has at least one probe chain proposed, including the honest failures:
*Where the flames are* (Andrew, 2026-09-28): nothing in anyone's hand at the start, and the easier a source is to find, the less of
it there is — **the pilot's book of matches, two left**, in his shirt pocket (Andrew's); **the nurse's
book of matches, about eight, damp** where her canteen leaked in the crash, in her backpack behind the
jammed aft bin — dried against the body or near a fire before it strikes; **a cheap butane lighter** in
a canvas jacket rolled in the townie's suitcase in the baggage bay — bag, then jacket, then pocket — which
sputters in the cold until it is warmed in a hand or a pocket; **the salesman's old metal lighter, dry**,
in a side pocket of his laptop bag — it lights again once its wick is fed fuel, and the avgas in the
wing will do; and **a ferro rod** in the guide's duffel (Andrew's), thousands of sparks into fine dry
tinder only.

1. **Lighter** (found — above) — flame → tinder → kindling → fuel. Fails on: a branch straight from
   the flame; wet tinder; wind without a windbreak; a butane lighter too cold to light.
2. **Matches** — the pilot's two, and the nurse's damp book: `dry the matches` against the body or near
   a fire (a process) → strike. Each match is one try.
3. **The flare** — ignites
   anything, once, loudly; it is fire *or* signal, never both
   ([`14-rescue-paths.md`](14-rescue-paths.md) §3.4).
4. **Battery + wire** — pry the panel: the plane's battery in the nose cowling (12 kg, wired and
   fine), copper strands across the terminals glow → tinder. Needs the wire *and* a walk outside.
5. **Focus** — the salesman's reading glasses (convex, 2026-09-28), the landing-light reflector or an
   ice lens, onto fine dark tinder — sun only (weather-gated; the October sun is low, so it is slow).
6. **Spark** — the ferro rod from the guide's duffel, scraped with a knife's spine, into fine dry tinder
   (birch bark, old-man's-beard lichen, shavings); or the hatchet spine on quartz (the ridge; a rock in
   the muskeg) into char or fuel-soaked cloth.
7. **Friction** (Andrew, 2026-09-28) — a dry board and a stick worked hard against it: rubbed up and
   down a trough cut in the board (the trough, or fire plough), or spun between the palms in a notch
   (the hand drill) → a coal → blow. Two people who know how make it far easier: they take turns
   spinning the same stick without letting it stop, so the heat never drops and each spends less
   stamina (2026-09-28) — an act of two people on one thing (documents 04 and 19).
   It works with the right dry wood, and it costs stamina hard — tired, cold or raw hands fail, and the
   stamina meter shows it. The bow drill (carve, split, notch, string with a bootlace or paracord,
   bundle, drill → ember → blow) takes much less stamina for the same coal. The ferro rod's spark is
   its own way (6).

`rub sticks together` → *"The bark scuffs and warms under your hands, nothing more. Friction fire needs
the heat kept in one place — wood ground to hot dust in a notch or a groove — not two sticks sliding
past each other."* A failure can carry a hint like this, in the world's voice — the physics of why —
never a list of what would work (2026-09-28). `make fire with
sticks` performs the first act the means imply — it rubs them together — and gets the same answer
(§4.9). Nothing names the act that would work.

### 4.7 The two walked transcripts
The lighter path (5 steps, 3 honest failures) and the bow-drill path (11 steps, 2 honest failures) from
the 2026-09-07 conversation are proposed as the seed probes for this whole document — every method and
every honest failure line above should be able to play out as one of these two chains, or a variant of
them, with real tiers.

### 4.8 Why this matters (the lens pass)
Seven methods, each gated by a different scarce resource (time, tool, weather, knowledge, the flare's
one shot) — a real "several ways of doing things." The skill is knowing what catches from what —
physics, learnable from failure lines and the manual, never from a recipe. Every fire choice spends
something else: fuel is mass; shavings are tinder *and* lost wood; the flare is fire *or* signal; the
manual is fire *or* knowledge.

### 4.9 The `make fire` rows (Andrew, 2026-09-18)

`make` is the one aim-verb: vague it asks how, given the means it performs the act they imply and this
model answers (document 04 §3.9). Fire's rows in the goal table:

| field | fire |
|---|---|
| `goal` | fire · a fire · flame · blaze |
| `vague` | "How do you mean to make a fire?" — nothing else; what a fire wants is in the survival manual, not in the reply |
| `roles` | **ignition**: a thing with `flame`, `spark`, `ember` or `focus` · **fuel**: a thing with `burnability > 0`, and its form decides whether this ignition can reach it |
| `realize` | `light <fuel> with <ignition>` — the ordinary operation, resolved through §4.2's additive check |
| half-filled | two fuels and no ignition → neither will light the other, stated physically; an ignition and nothing receptive → the flame burns alone |
| multi-step | `make fire with sticks` rubs them together and they scuff and warm, nothing more — `make` performs the first act the means imply, never a procedure |

Worked, and this is the line the whole design exists to produce:

```
> make fire with the lighter and the stick
You hold the flame to the deadfall branch. The bark blackens and smokes, but a
wrist-thick branch won't catch from a flame this small. Something finer would.
```

Today the shipped engine lights the branch ("a fire, at last") because the additive check is not
built. That refusal is the acceptance test for this document.

## 5. Interactions
**Depends on:** the ontology closure mechanism
([`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md), DR-26) for the forms and derived
capabilities (`edge`, `tinder`, `ignition`, `flame`, `ember`) that the shaping family mints and the
ignition check consumes; the taught grammar
([`04-grammar-and-feedback.md`](04-grammar-and-feedback.md)) for the `into <form>` syntax the shaping
verbs use and the `make` rows; the running clock ([`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md),
DR-27) for fire as an unattended process, the drying process for the damp matches, and
`FIRE_STATE_CHANGE` as an activity-interrupt signal; the characters' differing skill (document 16);
the heat system (`PLAN.md` A10), which carries the fire's heat into its area and the plane
([`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) §4.8).

**Depended on by:** warmth ([`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md)) —
the fire's heat, through the heat system, is one of the ways to stay warm and the fast way to dry
things; water ([`09-water.md`](09-water.md)) — melting snow needs a reachable heat source, the same
gate fire provides; food ([`10-food-and-hunger.md`](10-food-and-hunger.md)) — cooking, thawing,
smoking and drying; rescue ([`14-rescue-paths.md`](14-rescue-paths.md)) — a fire and its smoke are
signals, and the flare is fire *or* signal, never both.

## 6. Open questions

None open.

## 7. Review log
- **2026-09-16** — first draft, from the fire-and-shaping pass, `ontology-closure.md` §2–3, and a
  direct read of `affordances.py` and the shipped handlers.
- **2026-09-18 (Andrew)** — the `make fire` goal rows, with the honest refusal as this document's
  acceptance test; the code's 26 forms canonical; the seven methods priced by what each spends; Claude
  to draft the ignition weights, threshold and fuel-to-heat curve together; this document's stage
  ladder is the design. Reviewed in full.
- **2026-09-27** — the decisions of 2026-09-26 and 2026-09-27 carried in: heat as a state system,
  characters' differing skill, fire and smoke as signals; there is no survival kit.

## 8. What exists today
**Built (closure step 1).**
[`game/world/sim/affordances.py`](../../game/world/sim/affordances.py) — the `FORMS` frozenset (26
forms, matching this document's list exactly) and `derive()`, computing capability levels including
`tinder`, `ignition`, `flame` and `ember` from material × form × state (DR-26).
[`game/world/sim/operations/handlers/break_op.py`](../../game/world/sim/operations/handlers/break_op.py),
[`cut.py`](../../game/world/sim/operations/handlers/cut.py) and
[`tear.py`](../../game/world/sim/operations/handlers/tear.py) mint forms (`shard`, `piece`, `scrap`,
`strip`) from breaking, cutting and tearing, attachment-gated and mass-conserving.
[`light.py`](../../game/world/sim/operations/handlers/light.py) sets `state["lit"] = True` on a
flammable thing, gated by a single `has_ignition()` boolean check on the tool plus an
`ignition_difficulty` threshold — there is no distinction yet between a flame, spark, ember or focus
source, and no additive score.
[`burn.py`](../../game/world/sim/operations/handlers/burn.py) is a single-shot, one-tick operation:
consumes the target into ash (a fixed 15% ash fraction) plus smoke narration by material toxicity — not
a multi-tick process; there is no stage ladder, no fuel transfer, no heat output.
[`melt.py`](../../game/world/sim/operations/handlers/melt.py) turns frozen water into liquid water given
any reachable heat source, single-shot, mass-conserved. The exact chain Andrew walked on 2026-09-07
(break bottle → take shard → cut the cover free → burn the fabric) passes end to end as
`chain.break_bottle` / `chain.shard_cuts_cover` / `chain.burn_the_cover` in
[`game/world/scenarios/whiteout/probes/chain.py`](../../game/world/scenarios/whiteout/probes/chain.py),
`status: pass`, held in `probes/BASELINE`.

**Designed, not built.** The shaping family — `carve`, `split`, `shave`, `whittle`, `notch`, `string`,
`bundle`, `strike` — has no handler files and no `VERBS` entries anywhere in the codebase. Fire as a
persistent process object (the stage ladder, fuel load, heat output, tending verbs `blow`/`feed`/
`bank`/`smother`) does not exist; `game/world/sim/systems/fire.py` is a 6-line docstring stub (roadmap
P5) naming an older stage ladder (`unlit → smouldering → small → steady → spreading → dangerous`),
to be reconciled to §4.5's. The additive ignition score and the skill term are not implemented. Four of
the seven fire methods have no path at all: the flare, battery + wire, focus/lens, and the full
friction chain (which needs the whole shaping family first); the lighter and match paths work only as
far as lighting a flammable thing directly, because there is no fire process object yet to feed. The
two walked transcripts are named as the intended seed probes (a `probes/graph.py`), but that file does
not exist — only the break→cut→burn chain above is in the probe corpus today.
