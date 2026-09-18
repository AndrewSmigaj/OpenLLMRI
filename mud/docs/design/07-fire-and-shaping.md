# 07 — Fire and shaping

> **Status: draft for review.** Architecture counterpart: none named in the design index; the closure
> mechanism this document rides is
> [`../architecture/ontology-closure.md`](../architecture/ontology-closure.md) §2 (forms) and §3
> (derived capabilities), DR-26 in
> [`../architecture/implementation-architecture.md`](../architecture/implementation-architecture.md).
> Primary source:
> [`../investigation/design/fire-and-shaping.md`](../investigation/design/fire-and-shaping.md) — its §8
> (chunk-after-mastery) was removed on 2026-09-16 and is not part of this document.

## Provenance

### Andrew's decisions
- **(2026-09-07, walked in conversation).** The lighter path and the bow-drill path, walked step by
  step; **"rubbing sticks doesn't work and the game says so."**
- **(2026-09-07, per the provenance audit).** Fire is made *somehow*: rubbing sticks fails and the game
  says so; a bow drill works; a lighter lights tinder, not a branch. **"State the act, not the aim"**:
  `shake thermos` — applied here to fire as `make fire with sticks` never being the command; you say
  what you *do*.
- **(2026-09-16).** No question about means, no options, when a player states an aim instead of an
  act: `make fire with sticks` gets a clarification, never a list of what would actually work. Never a
  menu, applied to fire specifically.

### Removed (2026-09-16)
The source's §8, "chunk-after-mastery" (a Hadean-Lands-style ritual macro that would let a player type
`make fire with bow drill` once mastered), was Claude's addition, not Andrew's design — it hands the
player a command, which is the game offering an option. Removed from the source and not carried into
this document.

### Proposals (Claude)
The forms vocabulary, the additive ignition formula, the fire-as-process stage ladder and its tending
verbs, the shaping family of operations, the pricing of the seven methods, and the framing of the two
walked transcripts as "seed probes" are all Claude's proposals for how to realize Andrew's fire
walkthrough and his "never a menu" rule mechanically. The transcripts' *steps* are Andrew's own, from
the 2026-09-07 conversation; the probe framing around them is not.

## In one paragraph
A player pats their pockets and finds a lighter — click, and the tinder catches, but hold that same
flame to a wrist-thick branch and it just blackens; you have to build up from tinder to kindling to
fuel, or the fire dies in your hands. Without a lighter it is a longer, harder-won path: carve a
spindle, split a board, notch a socket, string a bow, bundle tinder, and drill until a thread of smoke
becomes a coal you have to blow into life — or give up and let the cold win the argument. Rubbing two
sticks together does nothing but warm your palms, and the game says so plainly, pointing at the physics
of why without ever naming the verb that would actually work.

## The design

### What fire needs
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

### The ignition check
An additive, transparent score: `score = source_strength + receptivity(material, form) + air − wet −
wind`, checked against a threshold; every term is visible in the failure line. *"The flame licks at the
bark and blackens it, but a wrist-thick branch won't take from a flame this small. Something finer
would."* Failure **costs** something — a match, a minute, stamina on the bow — never a silent retry.

### The forms
The mechanism underneath is the closure model (`ontology-closure.md` §2–3, DR-26): a **form** is the
shape a quantity of material takes; materials say what a thing is made of, forms say what shape it is
in, and **capabilities** (`edge`, `point`, `leverage`, `ignition`, `flame`, `ember`, `tinder`, …) fall
out of the pair via `world/sim/affordances.derive(entity, materials)`. Capped (a derived level never
exceeds the material or form tier), authored wins (an explicit `state[axis]` overrides the derived
value; the multitool and hatchet stay hand-tuned), and every load-bearing capability has to show in the
examine text — "a shard of glass, one edge wicked-sharp" — because a capability nobody can see is the
top complaint across every property-crafting game this design draws on.

The forms this pass proposes (v1 vocabulary):
`blade` · `shard` · `flake` · `piece` · `scrap` · `strip` · `sheet` · `slab` / `board` · `rod` /
`stick` / `bar` / `pole` · `spindle` · `point` / `stake` · `bow` · `shavings` · `bundle` · `cord` ·
`block` · `vessel` · `ember` · `ash` · `liquid` · `cloth`. Live since closure step 1 for minted
objects; authored objects declare theirs in `OBJECT_TABLE` (the multitool is a `blade`, a bottle a
`vessel`, a branch a `rod`, paracord `cord`).

### The shaping family
A new operation family whose outputs are forms:

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

### Fire as a process
`unlit lay` → `catching` (tinder flame, 1–2 game-min, dies without kindling) → `burning` (kindling,
heat rising) → `established` (fuel load ≥ 800 g, steady heat, the warmth source) → `embers` (fuel gone;
blow + tinder restarts) → `dead` (ash). Fuel is TRANSFERred into the fire (`put branch on fire`); each
tick CONSUMEs fuel mass by material burn rate into ash and the sink; heat output is a function of stage
and fuel; smoke reads from material toxicity (the foam warning). Tending verbs: `blow on` / `fan`
(stage push, +air), `feed` (= put fuel), `bank` (slow burn overnight), `smother` / `douse` (out). Wind
and wet degrade the fire; the windbreak is a real object property (the shelter pass,
[`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md)). **Where a fire lives:** the
first burning thing on the ground with a lay becomes the fire entity at that space; a burning thing in
the hand is a torch, not a fire.

### The seven methods
Each has at least one probe chain proposed, including the honest failures:
1. **Lighter** (the pilot's pocket) — flame → tinder → kindling → fuel. Fails on: a branch straight
   from the flame; wet tinder; wind without a windbreak.
2. **Matches** — the soaked box: `dry matchbox` by a fire or body heat (a process) → strike.
3. **The flare** — ignites anything, once, loudly; spends the visual-signal resource (the rescue
   graph's trade-off, [`14-rescue-paths.md`](14-rescue-paths.md)).
4. **Battery + wire** — pry the panel, the aircraft battery in the nose cowling (12 kg), copper strands
   across the terminals glow → tinder. Needs the wire *and* a walk outside.
5. **Focus** — the landing-light reflector or an ice lens, sun only (weather-gated).
6. **Spark** — the hatchet spine on quartz (the ridge; a rock is in the muskeg census) into char or
   fuel-soaked cloth.
7. **Friction** — the bow drill (carve, split, notch, string, bundle, drill → ember → blow); the hand
   drill (near-impossible for a novice in winter; a real partial with raw palms).

`rub sticks together` → *"The bark scuffs and warms under your hands, nothing more. Friction fire wants
one stick spinning hard and fast in a notch of another, not two sticks scraping."* `make fire with
sticks` → a clarification only: *"'make' names what you want, not what you do. Say the act."* No
question about means, no options.

### The two walked transcripts
The lighter path (5 steps, 3 honest failures) and the bow-drill path (11 steps, 2 honest failures) from
the 2026-09-07 conversation are proposed as the seed probes for this whole document — every method and
every honest failure line above should be able to play out as one of these two chains, or a variant of
them, with real tiers.

### Why this matters (the lens pass)
Seven methods, each gated by a different scarce resource (time, tool, weather, knowledge, the flare's
one shot) — a real "several ways of doing things." The skill is knowing what catches from what —
physics, learnable from failure lines and the manual, never from a recipe. Every fire choice spends
something else: fuel is mass; shavings are tinder *and* lost wood; the flare is fire *or* signal; the
manual is fire *or* knowledge.

### The `make fire` rows (Andrew, 2026-09-18)

`make` is the one aim-verb: vague it asks how, given the means it performs the act they imply and this
model answers (document 04 §3.9). Fire's rows in the goal table:

| field | fire |
|---|---|
| `goal` | fire · a fire · flame · blaze |
| `vague` | "Request too vague. How are you going to make the fire?" — nothing else; what a fire wants is in the survival manual, not in the reply |
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

## Interactions
**Depends on:** the ontology closure mechanism
([`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md), DR-26) for the forms and derived
capabilities (`edge`, `tinder`, `ignition`, `flame`, `ember`) that the shaping family mints and the
ignition check consumes; the taught grammar
([`04-grammar-and-feedback.md`](04-grammar-and-feedback.md)) for the `into <form>` syntax the shaping
verbs use; the running clock ([`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md),
DR-27) for fire as an unattended process, the drying process for the soaked matchbox, and
`FIRE_STATE_CHANGE` as an activity-interrupt signal.

**Depended on by:** warmth ([`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md)) —
the fire's heat output feeds the core-temperature formula directly; water
([`09-water.md`](09-water.md)) — melting snow needs a reachable heat source, the same gate fire
provides; food ([`10-food-and-hunger.md`](10-food-and-hunger.md)) — cooking; the pilot
([`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md)) — tended near a fire, at a real time and
warmth cost; rescue ([`14-rescue-paths.md`](14-rescue-paths.md)) — the flare is fire *or* signal, never
both.

## Open questions
1. **The final forms list.** This document's list (26 form-words, several doubled under one bullet —
   `slab`/`board`, `rod`/`stick`/`bar`/`pole`, `point`/`stake`) does not match
   `ontology-closure.md` §2's table (15 rows, ~19 distinct words). *Finding:* the shipped
   `game/world/sim/affordances.py` `FORMS` constant already contains the exact 26-word list from this
   document, word for word — the code has settled this question in this document's favor.
   *Recommendation:* treat this document's list as canonical and update `ontology-closure.md` §2 to
   match; it is the stale one, not this pass.
2. **Pricing the seven methods so none dominates.** Named as a requirement (*"the graph must price them
   so none dominates"*) but not valued. *Options:* price by time and resource cost alone (lighter fast
   and cheap but a limited pocket item; bow drill free but slow and skill-gated; flare instant but
   one-shot and loud) versus adding a genuine failure-rate/skill axis on top. *Recommendation:*
   cost-only pricing first — every method here already spends something distinct (fuel, tool charges,
   time, the flare's one shot), which is most of what "none dominates" needs; add a failure-rate axis
   only if playtesting shows one method winning anyway.
3. **The ignition score's actual numbers.** `source_strength`, `receptivity`, `air`, `wet`, `wind` and
   the threshold are named as axes, not valued anywhere in the source. *Recommendation:* value them
   together with the fire ladder's fuel-to-heat-output curve (also unvalued) when this pass is next
   worked, since both feed the same formula and neither can be tuned alone.
4. **Anything else open:** the fire ladder names stages but gives no fuel-mass-to-heat-output formula;
   the stub `game/world/sim/systems/fire.py` names a *different* stage ladder (`unlit → smouldering →
   small → steady → spreading → dangerous`, from an older §31 spec) than this document's proposed one
   (`unlit lay → catching → burning → established → embers → dead`) — the two have never been
   reconciled, and that reconciliation is this document's business, not architecture's, since this is
   where the ladder is designed.

## Review log
2026-09-16 — first draft, written from `fire-and-shaping.md` (primary), `ontology-closure.md` §2–3, and
a direct read of `affordances.py` and the shipped handlers. Not yet reviewed with Andrew.

- **2026-09-18 (Andrew, block 1, ahead of this document's sitting):** the `make fire` goal rows written
  here; `make fire with the lighter and the stick` must produce the honest refusal, which is this
  document's acceptance test. The `make` form and dispatch rule are document 04 §3.9.

## What exists today
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
P5) naming a different, older stage ladder (see *Open questions* above). The additive ignition-score
formula is not implemented. Four of the seven fire methods have no path at all: the flare, battery +
wire, focus/lens, and the full friction chain (which needs the whole shaping family first); the lighter
and match paths work only as far as lighting a flammable thing directly, because there is no fire
process object yet to feed. The two walked transcripts are named in the source as the intended seed
probes (as a `probes/graph.py`) but that file does not exist — only the break→cut→burn chain above is
in the probe corpus today.
