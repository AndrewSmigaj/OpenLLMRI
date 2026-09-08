# Fire & shaping — the forms vocabulary, the ignition model, fire as a process

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07).** Walked with Andrew in
> conversation (the lighter path; the bow-drill path; "rubbing sticks doesn't work and the game
> says so"). Grounded in the property-crafting research (Cataclysm DDA tool qualities, NEO Scavenger
> property recipes, UnReal World's multi-step chains, The Long Dark's additive ignition formula) and
> the moral rule that failure explains physics and never lists steps. Promotes to
> `docs/architecture/fire-and-shaping.md` + DR-29 on approval; the time & stakes pass owns the clock
> side (durations, ticks, the fire as an unattended process).

## 1. What fire needs (the physics the game models)
Fire is **an ignition source × a receptive material × air × time**. The game models:
- **Sources**, each a capability: `flame` (a lighter, a match, a burning thing), `spark` (ferro rod,
  hatchet spine on quartz, battery + wire strands), `ember` (a coal from friction or a dying fire),
  `focus` (a lens or the landing-light reflector in sun — weather-gated). A source ignites only what
  its heat can reach: a flame catches tinder and thin kindling; a spark catches only prepared tinder
  (char, fluff, birch-bark curls, fuel-soaked cloth); an ember catches a tinder *bundle* when blown;
  focus catches dark fine tinder in sun.
- **Receptivity** = material `burnability` and `ignition_difficulty` × **form thinness**. The same
  wood is a log (won't catch from a lighter), a branch (won't), a splinter (might), shavings (will).
  Thinness lowers the threshold: shavings/fluff/bundle 0.4 · strip/scrap/bark 0.25 · piece/stick
  0.1 · rod/branch/log 0.
- **The fire itself is a process object** with a stage ladder, a fuel load, a heat output and a
  smoke character; it lives on the heartbeat (time & stakes) and interrupts nearby activities when
  its stage changes.

## 2. The ignition check (additive, transparent — The Long Dark's shape)
`score = source_strength + receptivity(material, form) + air − wet − wind` against a threshold;
every term is visible in the failure line. "The flame licks at the bark and blackens it, but a
wrist-thick branch won't take from a flame this small. Something finer would." Failure **costs**
something: a match, a minute, stamina on the bow — never a silent retry.

## 3. The forms (the second axis beside material) — v1 vocabulary
`blade` · `shard` · `flake` · `piece` · `scrap` · `strip` · `sheet` · `slab` / `board` · `rod` /
`stick` / `bar` / `pole` · `spindle` · `point` / `stake` · `bow` · `shavings` · `bundle` · `cord` ·
`block` · `vessel` · `ember` · `ash` · `liquid` · `cloth`. (Live since step 1 for minted objects;
authored objects declare theirs in `OBJECT_TABLE` — the multitool is a `blade`, a bottle a `vessel`,
a branch a `rod`, paracord `cord`.) Capabilities derive from material × form, capped, authored wins.

## 4. The shaping family (new operations; outputs are forms)
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

Form pseudo-nouns arrive in the Y slot only after `into`; a real entity there means "one like that".
Implicit accessories (a handhold for the drill, a reachable flame for melt) are chosen when
unambiguous and **named in the prose**.

## 5. Fire as a process (stages; the clock side is in time & stakes)
`unlit lay` → `catching` (tinder flame, 1–2 game-min, dies without kindling) → `burning` (kindling,
heat rising) → `established` (fuel load ≥ 800 g, steady heat, the warmth source) → `embers` (fuel
gone; blow + tinder restarts) → `dead` (ash). Fuel is TRANSFERred into the fire (`put branch on
fire`); each tick CONSUMEs fuel mass by material burn rate into ash + the sink; heat output is a
function of stage and fuel; smoke reads from material toxicity (the foam warning). Tending verbs:
`blow on` / `fan` (stage push, +air), `feed` (= put fuel), `bank` (slow burn overnight), `smother` /
`douse` (out). Wind and wet degrade; the windbreak is a real object property (the shelter pass).
**Where a fire lives:** the first burning thing on the ground with a lay becomes the fire entity at
that space; a burning thing in the hand is a torch, not a fire.

## 6. The seven fire methods in this world (each ≥1 probe chain; the honest failures too)
1. **Lighter** (the pilot's pocket) — flame → tinder → kindling → fuel. Fails on: a branch straight
   from the flame; wet tinder; wind without a windbreak.
2. **Matches** — the soaked box: `dry matchbox` by a fire or body heat (a process) → strike.
3. **The flare** — ignites anything, once, loudly; spends the visual-signal resource (the graph's
   trade-off).
4. **Battery + wire** — pry the panel, the aircraft battery in the nose cowling (12 kg), copper
   strands across the terminals glow → tinder. Needs the wire AND a walk outside.
5. **Focus** — the landing-light reflector or an ice lens, sun only (weather-gated; the P7 seam).
6. **Spark** — the hatchet spine on quartz (the ridge; a rock is in the muskeg census) into char or
   fuel-soaked cloth.
7. **Friction** — the bow drill (carve, split, notch, string, bundle, drill → ember → blow); the hand
   drill (near-impossible for a novice in winter; a real partial with raw palms).
`rub sticks together` → "The bark scuffs and warms under your hands, nothing more. Friction fire
wants one stick spinning hard and fast in a notch of another, not two sticks scraping." `make fire
with sticks` → the limited question.

## 7. The two walked transcripts are the seed probes (`probes/graph.py`, the fire goal)
The lighter path (5 steps, 3 honest failures) and the bow-drill path (11 steps, 2 honest failures)
from the 2026-09-07 conversation, verbatim, with expected tiers. The runner will fail them until the
shaping family, the ignition model and the fire process land — they are the acceptance test of this
pass.

## 8. Chunk-after-mastery (Hadean Lands; approved as optional, after the base paths work)
When a character has completed a procedure once (bow-drill fire), `make fire with bow drill` becomes
a single long activity if the parts are present — offered, never imposed, named back to the player
("You know this now: 'make fire with bow drill' does the whole thing."). Per character, deterministic.

## 9. Lens pass
### Problem Solving (GD — are there several real solutions?)
- **GREEN.** Seven methods, each gated by a different scarce resource (time, tool, weather,
  knowledge, the flare's one shot). **Note:** the graph must price them so none dominates.
### Skill (GD)
- **GREEN.** The skill is knowing what catches from what — physics, learnable from failure lines
  and the manual, never from a recipe.
### Visible Progress (GD)
- **YELLOW.** Depends on the time & stakes pass: drilling must tick ("a thread of smoke", "black
  dust piles", "an ember") or the hardest path reads as a coin flip. Blocking dependency.
### Economy (GD — does the fire loop create and spend resources?)
- **GREEN.** Fuel is mass; shavings are tinder AND lost wood; the flare is fire OR signal; the
  manual is fire OR knowledge. Every fire choice spends something else.
