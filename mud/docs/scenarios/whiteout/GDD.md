# Whiteout — Game Design Document

> **Status: reviewed with Andrew 2026-09-17; finalized at the close.** The umbrella: the pitch, the
> vision, the cross-cutting rules and the chapter index. The design of each system lives in its own
> document in [`docs/design/`](../../design/README.md), and each section below points to its chapters.
> The current decisions, all in one place, are [`PLAN.md`](../../../PLAN.md) §5. **Architecture
> counterpart:** [`implementation-architecture.md`](../../architecture/implementation-architecture.md)
> (the DR register). The section numbers are stable anchors that other files cite (Appendix A).

The engine is fully deterministic and never calls a language model; models help build the world and
play characters in it from outside (§3 rules 2 and 5). Time is a continuously running clock, and a run
is instanced, synchronous co-op (§9/§16). Input is a structured command grammar, taught to the player
(§25a).

---

## Chapter index — the design, one document per system
- [`01-premise-and-world`](../../design/01-premise-and-world.md)
- [`02-the-experience`](../../design/02-the-experience.md)
- [`03-the-player-view`](../../design/03-the-player-view.md)
- [`04-grammar-and-feedback`](../../design/04-grammar-and-feedback.md)
- [`05-ontology-and-sufficiency`](../../design/05-ontology-and-sufficiency.md)
- [`06-time-sleep-and-the-clock`](../../design/06-time-sleep-and-the-clock.md)
- [`07-fire-and-shaping`](../../design/07-fire-and-shaping.md)
- [`08-warmth-clothing-and-shelter`](../../design/08-warmth-clothing-and-shelter.md)
- [`09-water`](../../design/09-water.md)
- [`10-food-and-hunger`](../../design/10-food-and-hunger.md)
- [`11-injury-and-first-aid`](../../design/11-injury-and-first-aid.md)
- [`12-the-pilot-and-bodies`](../../design/12-the-pilot-and-bodies.md)
- [`13-events-escalation-and-weather`](../../design/13-events-escalation-and-weather.md)
- [`14-rescue-paths`](../../design/14-rescue-paths.md)
- [`15-moral-and-social-layer`](../../design/15-moral-and-social-layer.md)
- [`16-players-and-kit`](../../design/16-players-and-kit.md)
- [`17-rooms-and-living-rooms`](../../design/17-rooms-and-living-rooms.md)
- [`18-materials-and-forms`](../../design/18-materials-and-forms.md)
- [`19-multiplayer-and-instances`](../../design/19-multiplayer-and-instances.md)
- [`20-the-agent-player-and-research`](../../design/20-the-agent-player-and-research.md)
- [`21-endings`](../../design/21-endings.md)
- [`22-the-world-building-loops`](../../design/22-the-world-building-loops.md)
- [`23-flora-and-fauna`](../../design/23-flora-and-fauna.md)

The index, the review order, the template and the writing rules: [`docs/design/README.md`](../../design/README.md).
Ideas that are not design yet: [`docs/design/IDEAS.md`](../../design/IDEAS.md).

## §1. Pitch & §2. Essential experience
> *Design:* [`01-premise-and-world`](../../design/01-premise-and-world.md) · [`02-the-experience`](../../design/02-the-experience.md)

**Whiteout** — survivors of a bush-plane crash in interior Alaska, in the first week of October,
improvise with a physically modelled world to stay alive — cold, injury, hunger and a worsening storm
against them — until they are rescued: by getting the hand radio working and raising someone, by a
signal a search plane can see, or by surviving long enough for the search to reach them, each path
harder than the last. **The only endings are rescued or dead.** **Essential experience:**
*understanding a living, reactive world under pressure — and being told, physically and specifically,
why each desperate idea works or doesn't.* **You survive by understanding the world, not by guessing
the author's verb.**

## §3. Binding design decisions
1. **Resolution, not success.** No `You can't do that.` ever ships; every sensible, desperate or silly
   attempt gets a real physical answer — what happens, or the physics of why not, in the world's voice.
   **Never a menu:** the game never lists options or names a verb the player did not type; when a
   player misses what any person would know, the world hints at it in its own voice — a reason, never a
   list (2026-09-16, 2026-09-27; document 04).
2. **The deterministic engine owns state and runs the entire game.** The engine never calls a language
   model to decide what happens or to write what a player sees. Language models play *characters* from
   outside, as players, through the same grammar as a person — survivors, non-human characters (NHCs),
   animals, the voice on the radio — and help build the world at build time. A model never invents
   state, decides survival math, grants success, or steps the world (2026-09-17). **One exception,
   because the party is talking to someone (2026-09-27):** the voice on the radio judges whether the
   party has told it enough to be found — by criteria the game gives it (the landmarks and what each is
   worth) — and that judgement is its act, logged like any player's. The same model plays the voice in
   every run, scaffolded with rules (document 14).
3. **Conservation holds at runtime (§24)** — material, mass (against an environment sink), temperature,
   wetness, contamination, damage, ownership, provenance survive every transform; *asserted*, not
   documented.
4. **Model-deep, requirement-light.** Model everything plausible; gate only core blockers; reward depth
   with safety, quality and options. Every goal has **several ways**, with no set number; clues are what
   a realistic world holds, plus some added to help players (2026-09-27).
5. **The engine runs the world; language models play characters from outside.** The pilot is authored
   content: he starts the run dead (§19). Animals are part of the world: the bear, some of the bigger
   animals and a few birds — fewer than three in a room, not constantly calling — act, on behaviour
   rules the engine runs; the fish are scripted; other wildlife shows as events and sign (document 23).
   A model-played character — a survivor, an NHC, or an animal a lightweight model plays when a run
   wants one — is a *player* from the engine's side (ADR-0005), never engine logic. (2026-09-17,
   2026-09-26, 2026-09-27)

## §6/§8. The world
> *Design:* [`01-premise-and-world`](../../design/01-premise-and-world.md) · [`13-events-escalation-and-weather`](../../design/13-events-escalation-and-weather.md) · [`16-players-and-kit`](../../design/16-players-and-kit.md) · [`23-flora-and-fauna`](../../design/23-flora-and-fauna.md)

**Premise (§6).** An off-route crash in an interior-Alaska side valley in the first week of October
(2026-09-26, 2026-09-27); the search looking in the wrong area; the hand radio dead and the ELT broken;
an unstable wreck. The aircraft is a Cessna 206-class single with a four-seat interior (1A, 1B, 2A, 2B
and the right seat), a hat shelf, a cargo net and a jammed cargo door; the plane's battery is in the
nose, wired and fine. **What is aboard** is not too easy and not too hard: there is no survival kit; the sleeping bag is buried with the tail wreckage; two blankets are
hidden inside the plane; there is no firearm (2026-09-27; document 16). **Holt's cabin** is supplies —
some trapline gear and modest stores — and walking out is not an ending. The crash site is the densest
place in the valley — modelled to the hilt — and the whole valley, all fifty outdoor zones in eleven
regions, is in the run (document 01).

**Weather and the ladder (§8).** The same weather every run: an inch of snow at the start, bushes
dusted but visible, berries and roots findable, skim ice on still water; light snow, then the storm,
then clear cold behind it. The days, the daylight and the numbers are document 13 §4.2. The escalation
ladder — snow that deepens, forage and fuel going under, the cold behind the storm — is designed in
document 13. What lives in the valley, filtered by ecology (this habitat, this month, real numbers), is
document 23.

## §5/§20–§27. The interaction engine — deterministic end to end
> *Design:* [`05-ontology-and-sufficiency`](../../design/05-ontology-and-sufficiency.md) · [`18-materials-and-forms`](../../design/18-materials-and-forms.md) · [`04-grammar-and-feedback`](../../design/04-grammar-and-feedback.md)

### §5/§21. Operations over materials
- **Objects are cheap:** `{materials, parts?, size, mass, tags, state{temp,wetness,contamination,
  damage}}`. No per-object affordance scripts — behaviour comes from the shared operations.
- **Materials are the real content:** ~25 **ordinal property vectors** (cut/tear/bend resistance,
  burnability, ignition difficulty, smoke toxicity, insulation, conductivity, edibility…). Hand-curated
  (the quality anchor).
- **Operation categories**, grown by evidence without a ceiling: each a rule with roles, preconditions,
  modifiers, effects (with conservation), partial success (keep progress), and an **informative
  failure** — the physics of why. Few operations × many materials = a huge interaction space (BotW's 3
  chemistry rules; ScienceWorld's 25 actions → ~200k pairs).

### §24. Conservation ledger
Before any change commits, a per-transform check asserts the post-state balances the pre-state on
material/mass(±environment sink)/contamination/heat/provenance/length-count — else the transform is
rejected. This is what makes "everything interacts" *trustworthy*.

### §25a. Interaction input — the *taught* command grammar
Input is **not** free-form natural language and **not** a short menu of canned verbs. It is a
**structured command grammar, taught to the player**, pitched at the granularity of real physical
actions. The player learns it in the tutorial — a series of rooms, each one simple situation that shows
what sort of things they can do (2026-09-27) — and `help grammar` shows the forms with one example
each; nothing else is explained. Ambiguity prompts a clarification, never a flat refusal.

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

**What "you can do everything" means here.** *Everything that fits this grammar and is physically
sensible resolves* — because resolution runs through the **generative** operation×material engine
(§5/§21), **not** a hand-enumerated list of allowed commands. The grammar is the *expression surface*;
the engine *generates* the outcome from the verb's operation applied to the materials of X/Y/Z. It
deliberately does **not** parse arbitrary prose or absurd over-specification ("scrape a z into the snow
with your third fingernail") — it covers the real, sensible actions a survivor would express. The
verb/relation vocabulary is finite at any moment and grown by evidence without a ceiling (2026-09-16);
the *objects and materials* are scene content; the *interaction space* is the (operations × materials ×
relations) product, which is vast. The forms, `make` as the one aim-verb, quantities, naming and the
feedback rules: document 04.

### §25–§27. The action pipeline — no language model anywhere in it
```
player types  e.g.  "cut the cover of the seat with the multitool"
 └─ PARSER (deterministic): the taught grammar (§25a) + synonyms → one `ActionAttempt`
        {verb, X, relation, Y, tool}; resolve each noun phrase to reachable things.  (classic IF/MUD parser — no LLM)
 └─ RESOLVE (deterministic) through the tiers (§26):
        authored-special → object-rule → OPERATION×MATERIAL (the workhorse)
        → generic-physics → THE PHYSICS OF WHY (never a list of operations; DR-08c, 2026-09-16)
 └─ APPLY effects (single source of truth) ⊳ conservation ledger ⊳ route messages by perception
 └─ NARRATE from pre-written templates + current state.  (no LLM)
```
- **"Soft" judgements** (is this contraption a windbreak ≥ 0.5? does this plea move morale?) are
  **pre-authored thresholds/rules evaluated deterministically** — not a runtime judge. The radio
  voice's judgement of what it has been told is the one exception, and it is a player's act (§3 rule 2).
- **Gaps:** if a sensible attempt has no matching rule, the engine answers from the things' properties
  — the physics of why — and **logs the gap (the "wall-sensor")** so *developers* can author the missing
  interaction later (build time). Players never trigger generation.

### §41. Language models — they build the world and play in it; the engine never calls one
| Stage | Who | Language model? |
|------|-----|------|
| Write the material table, operation rules, objects, response text | developers + a model, **in the workshop** | **yes (build time)** |
| Validate authored content (conservation, no dead-ends, coverage) | the validator + humans | no |
| A player acts and gets a result, during play | the deterministic engine | **no — never** |
| A player tries something nobody authored | the engine answers with the physics of why; logs the gap for developers | no at runtime |
| A character is played — a survivor, an NHC, an animal, the radio voice | a model, from outside, through the grammar | **yes — as a player, never engine logic** |

**One sentence:** *language models help build the world and play in it from outside; the engine never
calls one.*

---

## §10–§18. Perception & space
> *Design:* [`03-the-player-view`](../../design/03-the-player-view.md) · [`19-multiplayer-and-instances`](../../design/19-multiplayer-and-instances.md)

Overlapping perceptual zones, not chunky rooms: a Scene is one space; a character's zone is a position
within it; **visibility, audibility, reachability, direction, detail are separate**, each distance/
weather/occlusion-aware (§14 bands). `look` renders perception; activity/speech route by band × loudness
× weather (Evennia: `return_appearance`/`get_display_*` + an rpsystem-`send_emote`-style propagator).
Speech ranges whisper/say/call/shout, weather-modified (§15). The look is a title line, prose composed
from state, people and animals as prose and exits as entities in prose — no item list; an agent sees
exactly what a human sees (2026-09-16, 2026-09-17; document 03). Zones and perception bands are built
in a first version (DR-13a).

## §9/§16. Time, multiplayer, cooperation
> *Design:* [`06-time-sleep-and-the-clock`](../../design/06-time-sleep-and-the-clock.md) · [`19-multiplayer-and-instances`](../../design/19-multiplayer-and-instances.md) · [`20-the-agent-player-and-research`](../../design/20-the-agent-player-and-research.md) · [`21-endings`](../../design/21-endings.md)

**The clock (DR-14/14b).** Game time runs on its own at **15 game-minutes per real minute**; nobody can
stall or yank it. **Fast forward**, proposed and agreed by the players, runs it at about **150×**: awake
players can stay in it, seeing events faster, and type a command to slow it when they want to act; a
player waking or any non-ambient event drops it back to 15×; ambient events do not. Sleeping players can
chat out of character to pass the time. The numbers are tuned by playtesting (2026-09-17, 2026-09-27).
Small attended jobs take one to three game-minutes and bigger ones take honest durations; a long act
occupies its actor while the clock runs for everyone; processes (a fire burning down, snow melting, a
wound bleeding) are the clock's own work; being awake is being on watch (2026-09-18). The time controls
are taught in the tutorial. Under the hood the clock is a deterministic logical clock, so runs replay
exactly. Design: document 06.

**The session (DR-15/15a/15b).** Instanced, synchronous, small-party co-op: **one sitting of two or
three hours** covering about a week of game time, which the players can pause and return to — a game
played with friends, not an ongoing world. **The party:** up to five play (four adults and the kid); a
seat nobody plays is a dead character whose clothes and pockets can be searched; AI agents may play
seats. No back stories: characters differ in clothes, injuries and what they carry, and in how well and
how fast they do things — a woodsman lights fires better; a technically proficient character sees a
fault in a device (document 16). A missing player's character goes catatonic, sits down and stares; the
others can keep them alive, and they can die. An agent acts at the speed of typing its command; a slow
model is simply slow (document 20). **The only endings are rescued or dead**; the run ends when they
die, of anything. Dead players are ghosts: they move freely and use the out-of-character chat; ghosts
hear ghosts, the living cannot; anyone can use the out-of-character chat. There is no recap.
(2026-09-17, 2026-09-26, 2026-09-27.) Design: documents 19, 20 and 21.

**Cooperation:** at least one first-class interdependence (one raises the antenna while another works
the radio; one relays a landmark) so co-op is a shared-story engine, not parallel solitaire
(2026-09-17).

## §19. The pilot
> *Design:* [`12-the-pilot-and-bodies`](../../design/12-the-pilot-and-bodies.md)

He starts the run dead (2026-09-17). He carries no clues; nothing the party needs for rescue depends on
him. His body is food, and eating it is taboo, not immoral (2026-09-27). His kit is where he sat.
Design: document 12.

## §31–§36. Survival systems
> *Design:* [`06-time-sleep-and-the-clock`](../../design/06-time-sleep-and-the-clock.md) · [`07-fire-and-shaping`](../../design/07-fire-and-shaping.md) · [`08-warmth-clothing-and-shelter`](../../design/08-warmth-clothing-and-shelter.md) · [`09-water`](../../design/09-water.md) · [`10-food-and-hunger`](../../design/10-food-and-hunger.md) · [`11-injury-and-first-aid`](../../design/11-injury-and-first-aid.md) · [`23-flora-and-fauna`](../../design/23-flora-and-fauna.md)

One chapter per system; each is its own document, reviewed separately.
- **Time and sleep** — the clock at 15 game-minutes per real minute; fast forward; attended acts with
  feedback; processes; pausing a run and returning to it. Document 06.
- **Fire** — ignition needs the right source for the right material in the right form (a lighter
  lights tinder, not a branch); fire is a process with a stage ladder; seven methods, each priced by what
  it costs. Heat is a state on every entity, body parts included: a fire heats its area and leaves
  residual heat around it, and the plane is an entity with openings, open or closed, and an internal
  heat (2026-09-26). Document 07.
- **Warmth, clothing and shelter** — cold is the antagonist; clothing by region and wetness; the huddle;
  shelter as a property of a place, heard through its openings. There is no guaranteed floor: night one
  is survivable inside the wreck in the clothes they crashed in; from night two they need a heat source,
  better gear, conserving or huddling (2026-09-18). Document 08.
- **Water** — liquids in millilitres; vessels, melting; eating snow costs body heat; no boiling gate;
  contamination is fuel and oil, carried as provenance (2026-09-18). Document 09.
- **Food and hunger** — hunger works as it does in real life; food changes with heat — raw, cooked,
  spoiled — and there are poisonous mushrooms. The freight, people's bags, the
  country (berries, snares, birds brought down by anything thrown, fish, roots), the body; hunting, trapping, fishing
  and killing are real operations, each variant its own (2026-09-26, 2026-09-27). Documents 10 and 23.
- **Injury and first aid** — named wounds with clocks; improvised care. **Death comes from blood loss,
  the bear and the cold**; poison makes people very sick but never kills; other harms — infection,
  carbon monoxide and the rest — make them weak and sick; dangerous places injure but never kill
  outright, fitness matters, and a seeded dice roll is announced. There is no gate on violence: it
  resolves with real physics, through a combat system like a MUD's (2026-09-26, 2026-09-27). Document 11.
- **The pilot and bodies** — document 12.

## §37–§39. Rescue
> *Design:* [`14-rescue-paths`](../../design/14-rescue-paths.md) §3 · [`21-endings`](../../design/21-endings.md)

Rescue is the only good ending, and it comes three ways (2026-09-17). Players never see a number. **The
ELT is broken** (2026-09-27).
- **The radio.** A hand radio in the plane's cabin; its batteries are buried in a bag in the tail section. You
  need something to open it; inside, a loose wire is seen at once by a technically proficient character
  and found more slowly by anyone else, and the world says so. The antenna is anything metal and long
  enough, raised — higher is better, and a poor match only weakens the signal. Flip through the channel
  buttons or find the written emergency frequency; hold the button to talk. The batteries drain with
  use, and the light dims. Contact comes fairly quickly once the antenna is fixed — not only during
  flyovers.
- **The voice** on the other end is a person at search and rescue, played by a weak language model —
  the same model every run, scaffolded with rules (§3 rule 2). It helps only as a real rescuer would,
  may hint (raise the antenna) through the bad signal, asks for landmarks and judges them by the game's
  list and values, says they will come once the storm dies down, and tells a party that cannot be found
  what it needs to do. A party that cannot say where it is can be homed in on, at a battery cost
  *(Claude's choice, at Andrew's request)*.
- **A signal a search plane can see:** fire and smoke (rubber, oil, green boughs), a piece of mirror once
  clear of the trees, burning Holt's cabin during a flyover. Whether a crew sees a signal follows physics
  — contrast, weather, how close the pass comes *(Claude's choice, at Andrew's request)*. The plane is
  heard before it is seen; a party may not make it in time.
- **Surviving long enough:** search and rescue is searching; **the same flyovers every run**; **the
  default rescue is day 7**; being findable after the storm takes work. The rest of the schedule is
  Claude's (document 13 §4.2). No boats.

Holt's cabin is supplies, never an exit. Design: document 14 §3; endings: document 21.

## §43. Authoring model
> *Design:* [`05-ontology-and-sufficiency`](../../design/05-ontology-and-sufficiency.md) · [`17-rooms-and-living-rooms`](../../design/17-rooms-and-living-rooms.md) · [`18-materials-and-forms`](../../design/18-materials-and-forms.md) · [`22-the-world-building-loops`](../../design/22-the-world-building-loops.md) · [`16-players-and-kit`](../../design/16-players-and-kit.md)

**Behaviour derives; authoring has no ceiling.** Objects get their behaviour from materials, forms and
the shared operations, so nothing needs a hand-written rule in order to exist; authored rules go on top
of anything, without limit, when they make the world truer or more interesting — the derived answer is
the floor, never the ceiling (2026-09-17). Content is authored in tables (`objects.py`,
`materials/table.py`, `zones.py`, `spaces.py`, `appearance.py`, `responses/`) and grown by the
world-building loops from the ontology store (`docs/ontology/`, its schema designed in full up front),
where Sonnet and Opus flesh out every room as peers, the merge never drops, and every addition flows
back into the design and the plan. `make validate` is the gate. Design: documents 05, 18, 22.

## §44/§45. Correctness

Invariants, enforced at runtime and in the gates: the **conservation ledger** (mass and material never
appear from nowhere or vanish); **narration ↔ effect** (no prose-only change); **rescue always
reachable** (no run can become unwinnable — a party cannot spend or burn its way into a dead end);
**every attempt resolves**; **activities survive a reload**. **Coverage** is the probe corpus — every
`pass` probe green, the count never drops — plus the seeded fuzz (every attempt resolves, every effect
conserves): DR-18a. Quality — does it read well, is it interesting — is judged by reading rendered
scenes, never automated. There is no guaranteed warmth floor; the night-one rule is document 08 §4.1a.

## §42. The order of work

The order of work is [`PLAN.md`](../../../PLAN.md): the design review, the machine, the world-building
loops, the cabin zone done right, the systems, play.

## §46. Scope & non-goals

**In:** the whole valley — the nine crash-site rooms and all fifty outdoor zones in eleven regions; the
systems in documents 06–23; the world-building loops before anyone plays; runs for friends, for humans
with agents, and for agents only. **Out:** a language model inside the engine (models play characters
and help build the world; the engine never calls one); procedural variants of the crash; an ongoing
world — a run is one sitting of two or three hours.

## §49. Bottom line

Two things, both first-class. A **model world for serious research**: a language model acts in it
freely through the same grammar a person uses, never offered options, and its behaviour and activations
are studied; the runtime is deterministic, so every run replays exactly. A **new kind of MUD**: a
survival game where you can do anything within reason to solve it. What makes both work is one property
— the world answers anything reasonable — and the loops keep growing what it can answer. The current
decisions, all in one place: `PLAN.md` §5.

## Review log
- **2026-09-17** — reviewed in full with Andrew: every section rewritten to that sitting's decisions and
  pointed to its design documents.
- **2026-09-26** — at document 10's sitting, Andrew found the vision too small (a combat system like a
  MUD's, and more besides); the broadening is `PLAN.md` A11.

## Appendix A — §-anchor map
The section numbers other files cite: §1–2 Pitch/Essential · §3 Binding decisions (model-deep is rule
4) · §5/§21 Operations/Materials · §6/§8 World and weather · §9/§16 Time/multiplayer (the clock and the
session) · §10–18 Perception · §19 The pilot · §20–27 Interaction engine (§24 Conservation ledger ·
§25a Taught input grammar · §25–27 the pipeline) · §31–36 Survival · §37–39 Rescue · §40 UI (in the
pipeline) · §41 Language models · §42 The order of work · §43 Authoring · §44/45 Correctness · §46
Scope · §49 Bottom line.

## Appendix B — Where else to look
[`VISION.md`](../../../VISION.md) (the anchor) · [`PLAN.md`](../../../PLAN.md) (§5, the current decisions) ·
[`docs/design/README.md`](../../design/README.md) (the index, the template, the writing rules) ·
[`implementation-architecture.md`](../../architecture/implementation-architecture.md) (the DR register) ·
the build-time skills `.claude/skills/{lenses,ontology-generator,solvability-fuzz}`.
