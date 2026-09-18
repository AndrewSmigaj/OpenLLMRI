# Whiteout — Game Design Document (authoritative)

> **Status: THE UMBRELLA — pitch, vision, cross-cutting rules, and the chapter index (2026-09-16). Reviewed with Andrew 2026-09-17 in full (block 1); finalized at the close.**
> The per-system design of record now lives in [`docs/design/`](../../design/README.md), one document
> per system, reviewed with Andrew one at a time; each section below points to its chapter. This
> GDD = **your original design** (`design.md`,
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
2. **Behaviour derives; authoring has no ceiling.** Objects get their behaviour from their materials,
   forms and the shared operations, so nothing needs a hand-written rule in order to exist. Authored
   rules can be layered on top of anything, without limit, whenever they make the world truer or more
   interesting — the derived answer is the floor, never the ceiling. *(Reworded with Andrew, 2026-09-17;
   the June "packets" were retired, DR-17a.)*
3. **Conservation becomes a runtime assertion, not just a content-check.** A per-transform ledger
   makes the books balance before any change commits (your §24 was a rule + a §44 lint; this enforces
   it live).
4. **Add a global-resource softlock check** alongside your per-fact ≥3-paths rule (§44) — so a party
   can't burn/spend its way into an unwinnable world-state the per-fact rule can't see. *(The
   "guaranteed no-materials warmth floor" this improvement also proposed was replaced on 2026-09-18 by
   the night-one rule: the first night is survivable inside the wreck, and the ladder takes that away
   afterwards — `docs/design/08-warmth-clothing-and-shelter.md` §4.1a.)*
5. ~~Build the one-room ontology slice first~~ — *history (2026-09-17): the slice was built in June–July;
   the order of work is `PLAN.md`.*
6. ~~Coverage = invariants + a fuzzer + a curated set~~ — *history (2026-09-17): replaced by the probe
   corpus and the fuzz (DR-18a).*

That's the whole substantive change. Everything below is your design with these folded in.

## §0b. Decisions now locked + remaining nice-to-haves
> **Amended 2026-09-07 and 2026-09-16** (recorded in `../../architecture/implementation-architecture.md`
> §2; the June text below is kept as written): DR-14a — the clock may run 20× by consensus when all
> sleep or wait, events interrupt it; DR-15a — a roughly week-long run with an escalation ladder and
> no hard time barriers, not a one-day reset; DR-17a/18a — tables and the probe corpus replace
> packets, bake and the matrix; DR-08c — feedback is clarification only, never a menu, never a verb
> list; the world is open-ended: the vocabulary and the entities grow by evidence without a ceiling;
> and the pilot dies within the first day: nobody can talk to him (no language model behind him),
> so scripted things only — moaning heard in the cockpit, maybe a line; what he says is designed in
> `../../design/12-the-pilot-and-bodies.md` (§19 stands until that review).
The clock and session model that were once open are **decided and locked** (full detail in §9):
- **Clock — a continuously running real-time clock (LOCKED).** The world advances in real time on its
  own; it is never poked forward by player actions or chat, and no one can stall or yank the shared
  clock. Event-/turn-based time is **rejected** as clunky for a multiplayer game.
- **Session model — instanced, synchronous, small-party co-op (LOCKED).** One crash, played together
  online, to resolution — **roughly a week of game time inside one sitting of two or three hours** (one
  shot, or two with a halt and resume; a member missing at resume is incapacitated where they lie). It is
  a game played in sessions with friends, not an ongoing world. *(Andrew, 2026-09-17, DR-15b; the June
  draft's "~1 in-game day, then reset" was never his.)*
- The end-of-run recap is design (document 21). The knowledge/uncertainty layer (believed vs true) is
  an idea in `docs/design/IDEAS.md`, not design. *(2026-09-17.)*

---

## Chapter index — the design of record, one document per system
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
- [`21-endings-and-recap`](../../design/21-endings-and-recap.md)
- [`22-the-world-building-loops`](../../design/22-the-world-building-loops.md)
The index, the review order and the template: [`docs/design/README.md`](../../design/README.md).

## §1. Pitch & §2. Essential experience  *(unchanged)*
> *Design of record (reviewed per system):* [`02-the-experience`](../../design/02-the-experience.md)

**Whiteout** — survivors of a bush-plane crash in an Alaskan December improvise with a physically
modelled world to stay alive — cold, injury, hunger and a worsening storm against them — until they are
rescued: by fixing the radio and raising someone during a flyover, by a signal a search plane can see, or
by simply surviving long enough for the search to reach them, each path harder than the last. **The only
endings are rescued or dead.** *(Reworded with Andrew, 2026-09-17.)* **Essential
experience:** *understanding a living, reactive world under pressure — and being told, physically and
specifically, why each desperate idea works or doesn't.* **You survive by understanding the world, not
by guessing the author's verb.**

## §3. Binding design decisions  *(your originals; rule 2 sharpened to "no runtime LLM")*
1. **Resolution-not-success (§3.5).** No `You can't do that.` ever ships; every sensible/desperate/
   silly attempt gets a real, pre-authored physical answer (or an informative redirect).
2. **The deterministic engine owns state and runs the entire game.** The engine never calls a language
   model to decide what happens or to write what a player sees. Language models play *characters* —
   agents through the same grammar as a person, including agents scaffolded as non-human characters
   (NHCs) — and help build the world at build time. An LLM never invents state, decides survival math,
   grants success, or steps the world. *(Reworded with Andrew, 2026-09-17.)*
3. **Conservation holds at runtime (§24)** — material, mass (against an environment sink), temperature,
   wetness, contamination, damage, ownership, provenance survive every transform; *asserted*, not
   documented.
4. **Model-deep, requirement-light (§4).** Model everything plausible; gate only core blockers; reward
   depth with safety/quality/options.
5. **No scripted-AI NPCs inside the engine (§3.3).** The pilot is authored content (he starts dead).
   Language-model-driven *characters* — including agents scaffolded as non-human characters (NHCs) —
   are *players* from the engine's side (ADR-0005), never engine logic. *(Reworded with Andrew, 2026-09-17.)*

## §6/§8. The world  *(unchanged; §6 premise, §8 weather arc)*
> *Design of record (reviewed per system):* [`01-premise-and-world`](../../design/01-premise-and-world.md) · [`13-events-escalation-and-weather`](../../design/13-events-escalation-and-weather.md)

Premise (§6): an off-route December crash; the search grid in the wrong area; a dead radio, a weak
beacon, an unstable wreck; about five hours of daylight. The crash site is the densest place in the
valley — modelled to the hilt — and the whole valley is in the run (document 01). Weather and the
escalation ladder — snow that deepens, cold that drops by the day, storms, the search moving on — are
designed in document 13; the June arc (light → steady → heavy → near-whiteout; −15 to −20 °C) is
superseded by the December ladder there. *(Reviewed with Andrew, 2026-09-17.)*

## §5/§20–§27. The interaction engine  *(your engine; runtime now fully deterministic)*
> *Design of record (reviewed per system):* [`05-ontology-and-sufficiency`](../../design/05-ontology-and-sufficiency.md) · [`18-materials-and-forms`](../../design/18-materials-and-forms.md) · [`04-grammar-and-feedback`](../../design/04-grammar-and-feedback.md)

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
The verb/relation vocabulary is finite at any moment, discoverable, and grown by evidence without a ceiling (amended 2026-09-16); the *objects and materials* are scene content;
the *interaction space* is the (operations × materials × relations) product, which is vast.

### §25–§27. The action pipeline — **deterministic end to end, no LLM**
```
player types  e.g.  "cut the cover of the seat with the multitool"
 └─ PARSER (deterministic): the taught grammar (§25a) + synonyms → one `ActionAttempt`
        {verb, X, relation, Y, tool}; resolve each noun phrase to reachable things.  (classic IF/MUD parser — no LLM)
 └─ RESOLVE (deterministic) through your §26 tiers, now WITHOUT an LLM tier:
        authored-special → object-rule → OPERATION×MATERIAL (the workhorse)
        → generic-physics → INFORMATIVE REDIRECT (the physics of why — never a list of operations; DR-08c, 2026-09-16)
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
> *Design of record (reviewed per system):* [`19-multiplayer-and-instances`](../../design/19-multiplayer-and-instances.md) · [`03-the-player-view`](../../design/03-the-player-view.md)
Overlapping perceptual zones, not chunky rooms: a Scene is one space; a character's zone is a position
within it; **visibility, audibility, reachability, direction, detail are separate**, each distance/
weather/occlusion-aware (§14 bands). `look` renders perception; activity/speech route by band × loudness
× weather (Evennia: `return_appearance`/`get_display_*` + an rpsystem-`send_emote`-style propagator).
Speech ranges whisper/say/call/shout, weather-modified (§15). *Deferred past the first slice.*

## §9/§16. Time, multiplayer, cooperation  *(LOCKED — running real-time clock + instanced co-op)*
> *Design of record (reviewed per system):* [`06-time-sleep-and-the-clock`](../../design/06-time-sleep-and-the-clock.md) · [`19-multiplayer-and-instances`](../../design/19-multiplayer-and-instances.md)

**The clock (LOCKED, DR-14/14b).** Game time runs on its own, always faster than real time: **15
game-minutes per real minute**. Nobody can stall or yank it. `propose fast forward` raises it to
**180×** when every player agrees — for sleeping and waiting — and events drop it back; a player who
does not agree keeps it at the base pace. Time controls are taught in the pre-scenario tutorial. A long
act is an attended activity that occupies its actor for game-minutes while the clock runs for everyone;
processes (a fire burning down, snow melting, a wound bleeding) are the clock's own work. Under the
hood the clock is a deterministic logical clock, so runs replay exactly. Design: document 06.

**The session (LOCKED, DR-15/15a/15b).** Instanced, synchronous, small-party co-op: **one sitting of
two or three hours** covering roughly a week of game time — a game played with friends, one shot or two
with a halt and resume; a member missing at resume is incapacitated where they lie. Not an ongoing
world. The only endings are rescued or dead; a dead player is a ghost who moves freely and talks only
in the out-of-character chat. Design: documents 19 and 21.

**Cooperation:** at least one first-class interdependence (one raises the antenna while another works
the radio; one relays a landmark) so co-op is a shared-story engine, not parallel solitaire.
*(Reviewed with Andrew, 2026-09-17.)*

## §19. The dying pilot  *(unchanged; one tweak)*
> *Design of record (reviewed per system):* [`12-the-pilot-and-bodies`](../../design/12-the-pilot-and-bodies.md)

He is dead at the start (Andrew, 2026-09-17). His body is a food path and a moral question; his kit is where
he sat. Nothing the party needs for rescue depends on him. Design: document 12.

## §31–§36. Survival systems
> *Design of record (reviewed per system):* [`07-fire-and-shaping`](../../design/07-fire-and-shaping.md) · [`08-warmth-clothing-and-shelter`](../../design/08-warmth-clothing-and-shelter.md) · [`09-water`](../../design/09-water.md) · [`10-food-and-hunger`](../../design/10-food-and-hunger.md) · [`11-injury-and-first-aid`](../../design/11-injury-and-first-aid.md)

One chapter per system; each is its own document, reviewed separately. *(Rewritten with Andrew, 2026-09-17;
the June one-liners came from the archived seed.)*
- **Time and sleep** — the clock at 15 game-minutes per real minute; `propose fast forward`; attended
  acts with feedback; processes; halt and resume. Document 06.
- **Fire** — ignition needs the right source for the right material in the right form (a lighter lights
  tinder, not a branch); fire is a process with a stage ladder; seven ways to make it. Document 07.
- **Warmth, clothing and shelter** — cold is the antagonist; clothing by region and wetness; the huddle;
  shelter as a property of a place. Document 08.
- **Water** — vessels, melting, boiling; eating snow costs heat. Document 09.
- **Food and hunger** — the kit, the freight, the country (berries, snares, birds with a thrown rock,
  fish under the ice, roots in frozen ground), the body. Documents 10 and 23.
- **Injury and first aid** — named wounds with clocks; improvised care. Document 11.
- **The pilot and bodies** — document 12.

## §37–§39. Rescue  *(your additive-confidence model; one improvement)*
> *Design of record (reviewed per system):* [`14-rescue-paths`](../../design/14-rescue-paths.md) · [`21-endings-and-recap`](../../design/21-endings-and-recap.md)

Rescue is the only good ending, and it comes three ways, each harder than the last. **The hand radio
during a flyover:** find the battery in the tail wreckage under the snow, raise the antenna, turn the
dial through the static — a high screech, a low hum, a faint voice — and piece together what the voice
asks for (*improve your signal*, *adjust antenna*), a medium-difficulty mini game; the radio is static
except when a plane is overhead. **A signal a search plane can see:** a smoke column past a threshold —
rubber, oil, green boughs — or the cabin burning during a pass. **Surviving long enough** for the
search to reach a findable party — the hardest path, because every day is worse. The flyover schedule
is the hidden rescue clock: an early pass for the story, real chances, then the late pass. Players never
see a number. The cabin is supplies, never an exit. The ELT — a silent beacon you rig an antenna onto —
is decided in the rescue document. Design: document 14; endings in 21. *(Rewritten with Andrew, 2026-09-17.)*

## §43. Authoring model  *(improvement #2)*
> *Design of record (reviewed per system):* [`17-rooms-and-living-rooms`](../../design/17-rooms-and-living-rooms.md) · [`22-the-world-building-loops`](../../design/22-the-world-building-loops.md) · [`16-players-and-kit`](../../design/16-players-and-kit.md)

**Behaviour derives; authoring has no ceiling.** Objects get their behaviour from materials, forms and
the shared operations, so nothing needs a hand-written rule in order to exist; authored rules go on top
of anything, without limit, when they make the world truer or more interesting. Content is authored in
tables (`objects.py`, `materials/table.py`, `zones.py`, `spaces.py`, `appearance.py`, `responses/`)
and grown by the world-building loops from the ontology store (`docs/ontology/`), where Sonnet and
Opus flesh out every room as peers and every addition flows back into the design and the plan.
`make validate` is the gate. Design: documents 05, 18, 22. *(Rewritten with Andrew, 2026-09-17.)*

## §44/§45. Correctness  *(improvements #3, #4, #6)*

Invariants, enforced at runtime and in the gates: the **conservation ledger** (mass and material never
appear from nowhere or vanish); **narration ↔ effect** (no prose-only change); **rescue always
reachable** (no run can become unwinnable); **every attempt resolves**; **activities survive a
reload**. **Coverage** is the probe corpus — every `pass` probe green, the count never drops — plus the
seeded fuzz (every attempt resolves, every effect conserves): DR-18a. Quality — does it read well, is it
interesting — is judged by reading rendered scenes, never automated. The warmth floor is decided in
document 08. *(Reviewed with Andrew, 2026-09-17.)*

## §42. Build plan — vertical slice first  *(improvement #5)*

Superseded (2026-09-17). The order of work is [`PLAN.md`](../../../PLAN.md): the design review, the machine,
the world-building loops, the cabin zone done right, the systems, play.

## §46. Scope & non-goals (v1)

**In:** the whole valley (59 zones); the systems in documents 06–23; the world-building loops before
anyone plays; runs for friends, for humans with agents, and for agents only. **Out:** a language model
inside the engine (models play characters and help build the world; the engine never calls one);
procedural variants of the crash; an ongoing world — a run is one sitting of two or three hours.
*(Rewritten with Andrew, 2026-09-17.)*

## §49. Bottom line

Two things, both first-class. A **model world for serious research**: an LLM acts in it freely through
the same grammar a person uses, never offered options, and its behaviour and activations are studied;
the runtime is deterministic, so every run replays exactly. A **new kind of MUD**: a survival game where
you can do anything within reason to solve it. What makes both work is one property — the world answers
anything reasonable — and the loops keep growing what it can answer. The reasoning and the history:
`docs/investigation/` (not authoritative). *(Rewritten with Andrew, 2026-09-17.)*

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
