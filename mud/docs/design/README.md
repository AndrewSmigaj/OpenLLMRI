# Whiteout — the design, one document per system

> **Status: living index.** This folder holds the game's design, one document per system, numbered in
> the order we review them. Each document's banner says where it stands: `draft for review` →
> `reviewed with Andrew <date>` → `finalized <date>`. **Nothing is built and no agent runs a
> world-building loop until every document here is finalized.** The GDD
> ([`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md)) is the one umbrella document —
> pitch, vision, cross-cutting rules — and points here for every system. *How* the engine does each
> thing lives in [`../architecture/`](../architecture/); these documents are the *what* and the *why*.
> The current decisions, all in one place, are `PLAN.md` §5.

## The review — a conversation, one document at a time

For each document, in the order below: Claude opens with the one-paragraph experience, the decisions
so far and the open questions, each with a recommendation. Andrew reads and reacts; we settle it in the
conversation. Claude writes the result into the document as the current design — in plain words, never
quoting the conversation — updates every other document the decision touches, and updates `PLAN.md`
§5. Several documents per sitting, at Andrew's pace. Ideas that are not design yet live in
[`IDEAS.md`](IDEAS.md).

**The season:** the first week of October in interior Alaska — about eleven hours of daylight at the
start, still over ten and a half by day seven; no big storm: bare, icy ground at the start, berries and
roots still findable, skim ice on still water; snow on and off, building to a couple of inches by the
end; a heavier flurry on day 6 that clears into the coldest night before the day-7 plane; the sky
always at least partly cloudy. The same weather every run (document 13 §4.2).

## The documents

| # | document | system | status | architecture counterpart |
|---|---|---|---|---|
| — | [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md) | the umbrella: pitch, vision, cross-cutting rules, chapter index | reviewed with Andrew 2026-09-17 (finalize at the close) | [`implementation-architecture.md`](../architecture/implementation-architecture.md) (the DR register) |
| 01 | [`01-premise-and-world.md`](01-premise-and-world.md) | the crash, the valley in early October: regions, the fifty outdoor zones, the map | reviewed with Andrew 2026-09-17 | — |
| 02 | [`02-the-experience.md`](02-the-experience.md) | what a run is like — the reference; the sample week is written again once the design is finalized | reviewed with Andrew 2026-09-17 | — |
| 03 | [`03-the-player-view.md`](03-the-player-view.md) | the look; exits as entities; groups; descriptions composed from state | reviewed with Andrew 2026-09-17 | [`presentation.md`](../architecture/presentation.md) (v2 pending) |
| 04 | [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) | the forms; state the act; clarification only; `help grammar`; how vocabulary grows | reviewed with Andrew 2026-09-18 | [`ontology-closure.md`](../architecture/ontology-closure.md) §5; `grammar.md` (pending) |
| 05 | [`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md) | what "anything reasonable" means; growing sets; the ontology store; the loops' scaffold; the viewer | reviewed with Andrew 2026-09-18 | [`ontology-closure.md`](../architecture/ontology-closure.md) |
| 06 | [`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md) | the clock; the three streams of text; activities; processes; sleep; the watch | reviewed with Andrew 2026-09-18 | [`tick-and-scheduler.md`](../architecture/tick-and-scheduler.md) |
| 07 | [`07-fire-and-shaping.md`](07-fire-and-shaping.md) | ignition; fire as a process; forms; the seven methods; the `make fire` goal rows | reviewed with Andrew 2026-09-18 | — |
| 08 | [`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md) | the night-one rule; the cold clock; clothing; huddle; shelter, heard through its holes; `status` and the meters | reviewed with Andrew 2026-09-18 | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 09 | [`09-water.md`](09-water.md) | liquids in millilitres; thirst; melting; eating snow's real cost; fuel contamination | reviewed with Andrew 2026-09-18 | — |
| 10 | [`10-food-and-hunger.md`](10-food-and-hunger.md) | what is aboard, the country, the body; hunger; cooking | reviewed with Andrew 2026-09-27 | — |
| 11 | [`11-injury-and-first-aid.md`](11-injury-and-first-aid.md) | wounds, bleeding, infection, frostbite, splints, the med pouch | reviewed with Andrew 2026-09-28 | — |
| 12 | [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md) | the pilot (starts the run dead); bodies persist; the moral question | reviewed with Andrew 2026-09-28 | — |
| 13 | [`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md) | the ladder; the event deck; weather; endings | reviewed with Andrew 2026-09-28 | — |
| 14 | [`14-rescue-paths.md`](14-rescue-paths.md) | rescue: the radio, the voice on the other end, signals a plane can see, surviving long enough and the flyovers | draft for review | [`implementation-architecture.md`](../architecture/implementation-architecture.md) §8 |
| 15 | [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) | possible, priced, witnessed, logged; action tags; the dilemma set | draft for review | — |
| 16 | [`16-players-and-kit.md`](16-players-and-kit.md) | the slots, draws, pockets, luggage; the 206 interior | draft for review | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 17 | [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) | individuation; state that persists; the prose style; the crash rooms | draft for review | [`containment.md`](../architecture/containment.md) |
| 18 | [`18-materials-and-forms.md`](18-materials-and-forms.md) | the material table in plain words; forms; what is missing | draft for review | [`ontology-closure.md`](../architecture/ontology-closure.md) §2–3 |
| 23 | [`23-flora-and-fauna.md`](23-flora-and-fauna.md) | the living things of the valley in October: what grows, what can be dug, caught, fished; the poison | draft for review | — |
| 19 | [`19-multiplayer-and-instances.md`](19-multiplayer-and-instances.md) | instanced runs; seeing and talking across zones; interdependence; run modes | draft for review | [`perception-model.md`](../architecture/perception-model.md) |
| 20 | [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) | what an agent is given; the same view as a human; the log; tags; replay; research runs | draft for review | [`adr/0005`](../architecture/adr/) |
| 21 | [`21-endings.md`](21-endings.md) | rescued or dead; ghosts | draft for review | — |
| 22 | [`22-the-world-building-loops.md`](22-the-world-building-loops.md) | the phases; both models as peers; the scaffold; the queue; walls per run | draft for review | `harness.md` (pending) |

**Companion lists** (living, never finished — the loops add to them): [`food-list.md`](food-list.md) —
every food in the valley and everything that makes people sick.

## The template — every document has these eight parts, in this order

1. **Status banner** — `draft for review` / `reviewed with Andrew <date>` / `finalized <date>`; the
   architecture counterpart.
2. **Decisions** — Andrew's decisions, in plain words, each with its date. Then *Proposals (Claude)*,
   marked as such. Nothing is left unlabelled.
3. **In one paragraph** — what the player experiences.
4. **The design** — the rules, then the Whiteout content (objects, events, numbers).
5. **Interactions** — which systems this depends on; which depend on it.
6. **Open questions** — only questions still open, each with the options and a recommendation.
7. **Review log** — one line per sitting: the date and what it settled, in plain words.
8. **What exists today** — built / designed / nothing, honestly, with pointers to code and probes.

## Writing rules (for anyone — person or agent — who writes here)

- **Current design only.** A document says what the design is now. When a decision changes something,
  the old text is deleted, not struck through or annotated — git keeps the history. No "superseded"
  notes, no struck-out questions, no blocks kept "as the record".
- **Never quote Andrew's messages.** This repository is public. Extract the decision into clean, neutral
  prose and date it: *Andrew decided (2026-09-27): …*. The same goes for commit messages.
- **Propagate every decision.** When a decision lands, every document that describes the thing — the
  GDD, these documents, `PLAN.md`, `VISION.md`, the architecture — is updated in the same pass. Search
  for the thing by name before calling it done.
- **Only Andrew's questions go to Andrew** — taste, vision, what the game is for, what his friends'
  evenings should feel like — **and never one he has already answered**: check `PLAN.md` §5 and the
  documents first, including for questions an agent wrote. What reality or the decided design already
  answers is answered in the document, marked *proposed by Claude, for Andrew's check*.
- **Real life is the default answer.** Physiology, ecology, physics, weather, how a snare or a fishing
  line actually works: answered from reality, with sources. Numbers come from real data first and are
  tuned by probes after.
- **State systems, not shortcuts.** Heat, wetness, spoilage, damage and the rest are states on every
  entity that really has them, body parts included, and systems change them. Never collapse a real
  process into one rule.
- **Never make the world less interactive.** Every real distinction a survivor would act on is in.
  "Modestly", "trivially", "no special verb", "falls out of existing operations" and "for v1" are
  warning words.
- **Plain words, common names.** Use the name people actually say — rabbit fever, not tularemia; the
  trichinosis worm, not *Trichinella* — and name every item by its most common name, with the technical
  and other names as its synonyms (Andrew, 2026-09-27).
- **Answer in the ontology's terms** (documents 03–05): entities and parts, materials, forms, states,
  what each could become, relations, the systems that change them, and the grammar forms that reach
  them. A variant that is ontologically significant is its own operation, within the grammar rules.
- **Several ways, no set number.** Every goal has several ways; clues are what a realistic world holds,
  plus some added to help players. No fixed counts — the world grows as the ontology is fleshed out.
- **Never propose a cut for economy.** Ordering is legitimate; dropping for surplus is not. A thing
  leaves the design only when it is wrong — untrue to the place, or contradicting a decision.
- **Ecology is a real filter.** A species has to live in this habitat, in this month, in numbers that
  matter — and every row says what it actually yields.
- **Never a menu, and common sense is hinted.** No design may have the game list options, suggest verbs
  or name what is reachable. When a player misses what any person would know, the world says why in its
  own voice (*"You talk into the mic, but the radio stays quiet while the button is up"*) — a reason,
  never a list of options.
- **The design is a work in progress** — never "locked" or "frozen". A new idea of Andrew's that a
  document does not allow changes the document.
- **Every claim has a source**: Andrew's dated decision, a document section, a code path, a probe id,
  or a real-world reference. If none exists, it is an open question.
- **No stats** in status text; *built / designed / nothing*.
- The doc-consistency gate applies: never write `Pass <digit>`, `event-driven`, `mass_kg`,
  `CMD_NOMATCH` or `intent-fallback`.
