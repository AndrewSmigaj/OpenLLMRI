# Whiteout — Game Design Document (authoritative)

> **Status: FINAL — design-frozen (v1 scope).** This GDD = **your original design** (`design.md`,
> §1–49) **+ a short list of targeted improvements** (§0a). The **goals and the core engine are
> unchanged.** Runtime is **fully deterministic — no LLM is ever called during play**; the LLM is a
> **build-time authoring tool only**. The previously-open mechanic decisions are now **locked** (§0b/§9):
> a **continuously running real-time clock** and **instanced, synchronous co-op**. Interaction input is a
> **structured, taught command grammar** (§25a). Legacy "design §N" references still resolve (Appendix A).

---

## §0a. The improvements (the actual delta from your original)
Same game, same goals, same engine. These are the targeted fixes:

1. **Runtime is 100% deterministic; all interactions are pre-built.** Remove the runtime LLM tier from
   §26 and the runtime intent-fallback from §41. The LLM is used **only at build time** to help author
   content (materials, operation rules, objects, response text), which a validator + a human then
   approve and **bake into data**. During play, the engine never calls an LLM.
2. **Author materials + operation rules richly; keep objects cheap.** The seat is just a parts-list;
   its behavior comes from the shared operations over its materials. Reserve full §43 packets for the
   handful of **puzzle-critical** objects (radio, beacon, pilot, one showcase seat). *Same outputs as
   §43, far less per-object authoring.*
3. **Conservation becomes a runtime assertion, not just a content-check.** A per-transform ledger
   makes the books balance before any change commits (your §24 was a rule + a §44 lint; this enforces
   it live).
4. **Add a global-resource softlock check** alongside your per-fact ≥3-paths rule (§44) — so a party
   can't burn/spend its way into an unwinnable world-state the per-fact rule can't see. Plus a
   guaranteed **no-materials warmth floor** so fire-failure is recoverable.
5. **Build the one-room ontology slice first** (revised build order, §42) — prove the core is fun
   before building perception/multiplayer/weather.
6. **Coverage = invariants + a fuzzer + a curated set**, replacing §46's 700+ enumerated tests (same
   confidence, actually doable).

That's the whole substantive change. Everything below is your design with these folded in.

## §0b. Decisions now locked + remaining nice-to-haves
The clock and session model that were once open are **decided and locked** (full detail in §9):
- **Clock — a continuously running real-time clock (LOCKED).** The world advances in real time on its
  own; it is never poked forward by player actions or chat, and no one can stall or yank the shared
  clock. Event-/turn-based time is **rejected** as clunky for a multiplayer game.
- **Session model — instanced, synchronous, small-party co-op (LOCKED).** One crash, played together
  online, to resolution (~1 in-game day), then reset.
- **Remaining nice-to-haves (genuinely optional — drop freely):** a knowledge/uncertainty layer
  (believed-vs-true) and an auto-generated end-of-run recap story. Pure additions.

---

## §1. Pitch & §2. Essential experience  *(unchanged)*
**Whiteout** — survivors of a snowy plane crash improvise with a physically-modeled world to outlast
cold, injury, hunger, and a worsening storm until rescue, escape, or collapse. **Essential
experience:** *understanding a living, reactive world under pressure — and being told, physically and
specifically, why each desperate idea works or doesn't.* **You survive by understanding the world, not
by guessing the author's verb.**

## §3. Binding design decisions  *(your originals; rule 2 sharpened to "no runtime LLM")*
1. **Resolution-not-success (§3.5).** No `You can't do that.` ever ships; every sensible/desperate/
   silly attempt gets a real, pre-authored physical answer (or an informative redirect).
2. **The deterministic engine owns state and runs the entire game.** **The LLM is a build-time
   authoring tool only and is never called during play.** It never invents state, decides survival
   math, grants success, or steps the world.
3. **Conservation holds at runtime (§24)** — material, mass (against an environment sink), temperature,
   wetness, contamination, damage, ownership, provenance survive every transform; *asserted*, not
   documented.
4. **Model-deep, requirement-light (§4).** Model everything plausible; gate only core blockers; reward
   depth with safety/quality/options.
5. **No autonomous in-scenario NPCs (§3.3).** The pilot is scripted; LLM-controlled *characters* are
   external bot *players* (ADR-0005), not authored NPCs.

## §6/§8. The world  *(unchanged; §6 premise, §8 weather arc)*
One authored crash. One **dense scene** (cabin + camp + near-forest) gets the whole data budget —
modeled to the hilt — rather than spread thin. Premise (§6): off-route winter crash, wrong search
area, dead radio, weak beacon, unstable wreck, ~5h daylight. Weather (§8) escalates light → steady →
heavy → near-whiteout → night (−15 to −20 °C), degrading visibility/audibility/fire/tracks/rescue.
Seed 2–3 timed beats (a search plane that misses you; the pilot's last lucid line) so the curve
doesn't sag.

---

## §5/§20–§27. The interaction engine  *(your engine; runtime now fully deterministic)*

### §5/§21. Operations over materials  *(your §5 + §20–24, with cheap objects emphasized)*
- **Objects are cheap:** `{materials, parts?, size, mass, tags, state{temp,wetness,contamination,
  damage}}`. No per-object affordance scripts — behavior comes from the shared operations.
- **Materials are the real content:** ~25 **ordinal property vectors** (cut/tear/bend resistance,
  burnability, ignition difficulty, smoke toxicity, insulation, conductivity, edibility…). Hand-curated
  (the quality anchor).
- **~20 operation categories (your §5):** each a pre-authored rule with roles, preconditions,
  modifiers, effects (with conservation), partial-success (keep progress), and an **informative
  failure**. Few operations × many materials = a huge interaction space (BotW's 3 chemistry rules;
  ScienceWorld's 25 actions → ~200k pairs).

### §24. Conservation ledger  *(improvement #3)*
Before any change commits, a per-transform check asserts the post-state balances the pre-state on
material/mass(±environment sink)/contamination/heat/provenance/length-count — else the transform is
rejected. This is what makes "everything interacts" *trustworthy*.

### §25a. Interaction input — the *taught* command grammar  *(LOCKED)*
Input is **not** free-form natural language and **not** a short menu of canned verbs. It is a
**structured command grammar, taught to the player**, pitched at the granularity of real physical
actions. The player is shown the shape and learns it in the first minutes; `help`/onboarding teach it;
ambiguity prompts a clarification, never a flat refusal.

**Shape (the gist — exact tokens are authored vocabulary):** `VERB  X  [RELATION  Y]  [WITH Z]`
- **VERB** — the action/operation (`cut`, `pry`, `burn`, `tie`, `wedge`, `melt`, `pour`, `wear`,
  `light`…). A synonym table maps phrasings to one canonical verb (`slice/saw/cut`).
- **X** — the primary target: a thing **or a part of a thing**. Possessive and "of" both parse
  (`the seat's cover` = `the cover of the seat`); adjectives disambiguate (`the torn strap`).
- **RELATION** — the preposition binding a **second** object (`off`, `onto`, `against`, `between`,
  `into`, `from`, `under`, `around`, `to`). **This slot is what makes two-object actions first-class** —
  `cut … off …`, `wedge … against …`, `tie … between …` — not single-target-only commands.
- **Y** — the secondary object the relation points at (some relations, e.g. `between`, take a pair).
- **WITH Z** — the optional tool/instrument (`with the multitool`, `using a strap`).

The parser (deterministic, §25–27) turns this into one `ActionAttempt = {verb, X, relation, Y, tool}`,
resolving each noun phrase to a reachable entity or part. Examples a player might type:

| Typed | Parsed `{verb, X, relation, Y, tool}` |
|---|---|
| `cut cover off seat with multitool` | `{cut, cover‹of seat›, off, seat, multitool}` |
| `wedge seat against door` | `{wedge, seat, against, door, —}` |
| `tie strap between tree and pole` | `{tie, strap, between, (tree, pole), —}` |
| `pour water on fire` | `{pour, water, on, fire, —}` |
| `wear the jacket` | `{wear, jacket, —, —, —}` |
| `burn the seat` | `{burn, seat, —, —, —}` |

**What "you can do everything" means here (LOCKED intent).** *Everything that fits this grammar and is
physically sensible resolves* — because resolution runs through the **generative** operation×material
engine (§5/§21), **not** a hand-enumerated list of allowed commands. The grammar is the *expression
surface*; the engine *generates* the outcome from the verb's operation applied to the materials of
X/Y/Z. It deliberately does **not** parse arbitrary prose or absurd over-specification ("scrape a z into
the snow with your third fingernail") — it covers the real, sensible actions a survivor would express.
The verb/relation vocabulary is finite and discoverable; the *objects and materials* are scene content;
the *interaction space* is the (operations × materials × relations) product, which is vast.

### §25–§27. The action pipeline — **deterministic end to end, no LLM**
```
player types  e.g.  "cut the cover of the seat with the multitool"
 └─ PARSER (deterministic): the taught grammar (§25a) + synonyms → one `ActionAttempt`
        {verb, X, relation, Y, tool}; resolve each noun phrase to reachable things.  (classic IF/MUD parser — no LLM)
 └─ RESOLVE (deterministic) through your §26 tiers, now WITHOUT an LLM tier:
        authored-special → object-rule → OPERATION×MATERIAL (the workhorse)
        → generic-physics → INFORMATIVE REDIRECT (nearest possible operations)
 └─ APPLY effects (single source of truth) ⊳ conservation ledger ⊳ route messages by perception
 └─ NARRATE from pre-written templates + current state.  (no LLM)
```
- **"Soft" judgements** (is this contraption a windbreak ≥ 0.5? does this plea move morale?) are
  **pre-authored thresholds/rules evaluated deterministically** — not a runtime judge.
- **Gaps:** if a sensible attempt has no matching rule, the engine gives a pre-written **generic
  redirect** and **logs the gap (the "wall-sensor")** so *developers* can author the missing
  interaction later (build time). Players never trigger generation.

### §41. The LLM — **build-time authoring only**
| Stage | Who | LLM? |
|------|-----|------|
| Write the material table, operation rules, objects, response text | developers + LLM, **in the workshop** | **yes (build time)** |
| Validate authored content (conservation, no dead-ends, coverage) | the validator + humans | no |
| A player acts and gets a result, during play | the deterministic engine | **no — never** |
| A player tries something nobody authored | engine gives a pre-written redirect; logs the gap for devs | no at runtime |
**One sentence:** *the LLM helps build the world; it is never in the world.*

---

## §10–§18. Perception & space  *(your design, unchanged; built after the slice)*
Overlapping perceptual zones, not chunky rooms: a Scene is one space; a character's zone is a position
within it; **visibility, audibility, reachability, direction, detail are separate**, each distance/
weather/occlusion-aware (§14 bands). `look` renders perception; activity/speech route by band × loudness
× weather (Evennia: `return_appearance`/`get_display_*` + an rpsystem-`send_emote`-style propagator).
Speech ranges whisper/say/call/shout, weather-modified (§15). *Deferred past the first slice.*

## §9/§16. Time, multiplayer, cooperation  *(LOCKED — running real-time clock + instanced co-op)*
**Clock — a continuously running real-time clock (LOCKED).** Game time advances on its own, in real
time, at a fixed pace (a tunable constant, ~10–20 real-seconds per game-minute, so one ~5-hour daylight
arc fits a sitting). It is **not** advanced by player actions or chat, no one pokes it forward, and no
one can stall or yank the shared clock for everyone else. The world — storm, dying pilot, fires, cooling
bodies — moves whether or not the party is acting, and **that pressure is the survival gameplay** (not
"rushing"). A long action is a *scheduled activity* that occupies its actor for N game-minutes while the
shared clock keeps running uniformly for everyone (§9.1: long actions never skip the clock for others).
Event-/turn-based time is **rejected** as clunky in multiplayer. *Build note (no gameplay effect): under
the hood the clock is a deterministic logical clock — time is an input — so replay/fuzz/tests are
reproducible; real time is simply its pacing.*

**Session model — instanced, synchronous, small-party co-op (LOCKED).** A party plays one crash
together, online at the same time, acting concurrently, to resolution (~1 in-game day); then the
instance resets (idiomatic on Evennia — the dungeon-contrib instancing pattern).

**Cooperation:** add **≥1 first-class interdependence** (one holds/raises the antenna or relays the
scout's landmark while another transmits) so co-op is a shared-story engine, not parallel solitaire.

## §19. The dying pilot  *(unchanged; one tweak)*
A condition-scripted, deteriorating information source — not AI dialogue. Tending buys lucidity/time/
fragments; he dies on a timer and becomes a body. **Give tending a real opportunity cost** (time,
exposure) so tend/question/loot is a genuine choice. Every fact he holds has **≥3 independent clue
paths** so his death never softlocks.

## §31–§36. Survival systems  *(unchanged; + the warmth floor, improvement #4)*
Fire (state ladder + hazards), warmth (fire **plus** windbreak/shelter/insulation/huddling/body-heat),
water (safety gated by container state), shelter (by properties; partial shelters count), injury/
medicine (systemic, improvised), food/death/bodies (incl. consequential cannibalism). **A no-materials
warmth floor** (huddle + fuselage + body heat) lets a competent party survive one night without fire,
so fire-failure is recoverable.

## §37–§39. Rescue  *(your additive-confidence model; one improvement)*
Rescue = additive confidence + a weather window; ≥4 winning combinations; no single required path.
Routes: stay-and-signal, beacon, radio, visual, travel. **Improvement:** make routes draw on
**distinct** scarce resources (not all on warmth/fire) so the choice between them is real and total
warmth failure doesn't kill every route at once. The radio is the one authored deep puzzle (§38).

---

## §43. Authoring model  *(improvement #2)*
**Default:** cheap objects + ordinal materials + pre-authored operation rules (the `ontology-generator`
skill drafts them at build time, generate-then-validate; the material table is hand-curated).
**Exception:** full §43 packets only for puzzle-critical objects, authored as *goals with ≥3 clue/
solution paths*, never recipes. **Gap-filling (build time):** the fuzzer's wall-sensor log tells devs
which interactions still need authoring; the LLM helps draft them; the validator gates them; they're
baked in. None of this happens at runtime.

## §44/§45. Correctness  *(improvements #3, #4, #6)*
Validator (content-lint) + **runtime assertions** + property tests + **fuzz**, replacing 700 enumerated
tests. Enforced invariants: the conservation ledger; **narration↔Effect** (no prose-only change);
**rescue-confidence monotonic & always-reachable**; **every-attempt-resolves** (0 fuzz dead-ends);
**warmth floor**; **activity durability across `@reload`**. **Coverage = the
operation×material matrix is complete + property-tested, plus a ≥10k-attempt fuzz corpus with 0
unresolved / 0 conservation violations / rescue reachable.** This proves *resolution + conservation +
solvability*; **quality** (does it read well?) is curated + playtested, not automated.

## §42. Build plan — vertical slice first  *(improvement #5)*
1. **Slice (co-op multiplayer, one shared room, ~5 objects, ~25 materials, ~15 operations):** the
   operation×material core + conservation ledger + the deterministic parser + the §26 tiers + redirect +
   wall-sensor + ~50 hand-curated signature responses + a stub radio rescue, with **2–3 players co-op in
   one shared room** (all game output through the message **propagator** seam — trivially "everyone in
   the room" for now) and a **basic running clock** (world-time + cold ticks). **Built behind seams**
   (propagator for all output; `WorldView.reachable/in_zone` for reach; the logical clock; run-tagging)
   so the deferred systems drop in without refactoring. **Defer:** the graded perception zones, the full
   activity scheduler, instanced-run lifecycle, authored interdependence, weather.
2. Materials/operations breadth + property tests + the fuzz harness.
3. Perception/zones (§10–15). 4. Running real-time clock + activity scheduler (timed tasks). 5. Rescue
   confidence + distinct-resource routes + authored radio/beacon/pilot. 6. Instanced synchronous co-op
   multiplayer + the graded propagator + co-op interdependence. 7. Weather arc (+ optional recap story).

**Slice success test:** a couple of friends, no manual, ~15 minutes **co-op** in the cabin — come away
saying *the world felt alive and reactive* (and *fun to poke at together*), **zero** "you can't do
that", and at least one delighted *"I can't believe that worked / that it told me why."* Pass → layer
the rest; fail → the depth is tedium, rethink first.

## §46. Scope & non-goals (v1)
**In:** the slice → the layered build, one dense scene, additive rescue. **Out (v1):** procedural
variants; the §46 density numbers (cut); the graded perception zones / instanced lifecycle / weather *until the slice proves fun*;
**any runtime LLM.**

## §49. Bottom line
Structurally sound, buildable, and now simpler (no runtime LLM). **Why this is feasible now:** deep
world-model text systems (SHRDLU → Infocom → MUDs → simulationist IF) were historically limited by
*hand-authored* ontology — the Cyc bottleneck; LLMs lift that ceiling **at build time, with validation**
(generate-then-validate), which is exactly where this design puts them. See
`docs/investigation/research/lineage-and-the-llm-unlock.md`. The make-or-break is **fun**, and it's
**empirical**: it rests on the bet that pre-authored, validated responses read as *specific and witty*.
**Confidence in the plan-to-find-out ~90%; in the game-being-fun ~50%** until the slice is playtested.
Full reasoning: `docs/investigation/certainty-assessment.md` and `scope-and-risk-register.md`. (Note:
removing runtime LLM retires the determinism/latency/mis-parse risks those docs raised — the picture
is now better.)

---

## Appendix A — §-anchor map
§1–2 Pitch/Essential · §3 Binding decisions · §4 (in §3.4) · §5/§21 Operations/Materials · §6/§8 World
· §9/§16 Time/multiplayer (clock+session **LOCKED**) · §10–18 Perception · §19 Pilot · §20–27
Interaction engine (§24 Conservation ledger · §25a Taught input grammar) · §31–36 Survival · §37–39
Rescue · §40 UI (in the pipeline) · §41 LLM = build-time only · §42 Build plan · §43 Authoring ·
§44/45 Correctness · §46 Scope. Improvements are §0a; §0b = now-locked clock/session + optional
nice-to-haves.

## Appendix B — Sources
Seed: `design.md`. Proposal: `../../proposals/whiteout-engine-proposal.md`. Investigation:
`../../investigation/`. Skills: `.claude/skills/{lenses,ontology-generator,solvability-fuzz}` (all
build-time tools).
