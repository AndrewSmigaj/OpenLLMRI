# Whiteout — the design of record, one document per system

> **Status: LIVING INDEX (created 2026-09-16).** This folder holds the game's design, one document
> per system, numbered in the order we review them. Each document's banner says where it stands:
> `draft for review` → `reviewed with Andrew <date>` → `finalized <date>` (or `superseded`).
> **Rule: nothing is built and no agent runs a world-building loop until every document here is
> finalized.** The GDD ([`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md)) is the
> umbrella — pitch, vision, cross-cutting rules — and points here for every system. *How* the engine
> does each thing lives in [`../architecture/`](../architecture/); these documents are the *what* and
> the *why*. Provenance is marked in every document: Andrew's decisions are quoted with dates;
> everything else is a proposal. How that came to be:
> [`../investigation/design/00-provenance-audit.md`](../investigation/design/00-provenance-audit.md).

## The review — a conversation, one document at a time

For each document, in the order below: Claude opens with the one-paragraph experience, the provenance
(what is Andrew's, what is proposed) and the open questions with recommendations. Andrew reads and
reacts — *not interesting*, *not fleshed out*, *cut this*, *more of that*. We rewrite together in the
conversation. Claude records every decision in the document's review log, flips its status, and appends
an amendment to the DR register where a locked decision moved. This table updates. Several documents
per sitting, at Andrew's pace.

**Suggested first sitting:** the GDD umbrella (what the game is, in one read) → 01 → 02 (the sample
week — the document to react to) → 03 → 04 → 05. Then the survival systems 06–12, the world 13–18 and 23,
then 19–22. Ideas that are not design yet live in [`IDEAS.md`](IDEAS.md).

## The documents

| # | document | system | status | architecture counterpart |
|---|---|---|---|---|
| — | [`../scenarios/whiteout/GDD.md`](../scenarios/whiteout/GDD.md) | the umbrella: pitch, vision, cross-cutting rules, chapter index | reviewed with Andrew 2026-09-17 (finalize at the close) | [`implementation-architecture.md`](../architecture/implementation-architecture.md) (the DR register) |
| 01 | [`01-premise-and-world.md`](01-premise-and-world.md) | the crash, December, the valley: regions, the 59 zones, routes, currencies, the map | reviewed with Andrew 2026-09-17 | — |
| 02 | [`02-the-experience.md`](02-the-experience.md) | what a run is like: a sample week in prose, then the reference | reviewed with Andrew 2026-09-17 (sample week regenerated after block 4) | — |
| 03 | [`03-the-player-view.md`](03-the-player-view.md) | the look; exits as entities; groups; descriptions composed from state | reviewed with Andrew 2026-09-17 | [`presentation.md`](../architecture/presentation.md) (v2 pending) |
| 04 | [`04-grammar-and-feedback.md`](04-grammar-and-feedback.md) | the forms; state the act; clarification only; `help grammar`; how vocabulary grows | reviewed with Andrew 2026-09-18 | [`ontology-closure.md`](../architecture/ontology-closure.md) §5; `grammar.md` (pending) |
| 05 | [`05-ontology-and-sufficiency.md`](05-ontology-and-sufficiency.md) | what "anything reasonable" means; growing sets; the ontology store; the loops' scaffold; the viewer | reviewed with Andrew 2026-09-18 | [`ontology-closure.md`](../architecture/ontology-closure.md) |
| 06 | [`06-time-sleep-and-the-clock.md`](06-time-sleep-and-the-clock.md) | the clock; the three streams of text; activities; processes; sleep; the watch | reviewed with Andrew 2026-09-18 | [`tick-and-scheduler.md`](../architecture/tick-and-scheduler.md) |
| 07 | [`07-fire-and-shaping.md`](07-fire-and-shaping.md) | ignition; fire as a process; forms; the seven methods; the `make fire` goal rows | reviewed with Andrew 2026-09-18 | — |
| 08 | [`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md) | the cold clock; clothing; huddle; shelter as a property; drying | draft for review | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 09 | [`09-water.md`](09-water.md) | the paths to water; vessels; melting; eating snow | draft for review | — |
| 10 | [`10-food-and-hunger.md`](10-food-and-hunger.md) | the kit, the freight, the country, the body; hunger; cooking | draft for review | — |
| 11 | [`11-injury-and-first-aid.md`](11-injury-and-first-aid.md) | wounds, bleeding, infection, frostbite, splints, the med pouch | draft for review | — |
| 12 | [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md) | the pilot (starts the run dead); bodies persist; the moral question | draft for review | — |
| 13 | [`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md) | the ladder; the event deck; weather; endings | draft for review | — |
| 14 | [`14-rescue-paths.md`](14-rescue-paths.md) | the goals; ≥3 paths; the flyover clock; the radio mini game; the ELT; signals; surviving long enough | draft for review | [`implementation-architecture.md`](../architecture/implementation-architecture.md) §8 |
| 15 | [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) | possible, priced, witnessed, logged; action tags; the dilemma set | draft for review | — |
| 16 | [`16-players-and-kit.md`](16-players-and-kit.md) | the slots, draws, pockets, luggage; the 206 interior | draft for review | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 17 | [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) | individuation; state that persists; the prose style; the crash rooms | draft for review | [`containment.md`](../architecture/containment.md) |
| 18 | [`18-materials-and-forms.md`](18-materials-and-forms.md) | the material table in plain words; forms; what is missing | draft for review | [`ontology-closure.md`](../architecture/ontology-closure.md) §2–3 |
| 23 | [`23-flora-and-fauna.md`](23-flora-and-fauna.md) | the living things of the valley in December: what grows, what can be dug, caught, fished; the poison | draft for review | — |
| 19 | [`19-multiplayer-and-instances.md`](19-multiplayer-and-instances.md) | instanced runs; seeing and talking across zones; interdependence; run modes | draft for review | [`perception-model.md`](../architecture/perception-model.md) |
| 20 | [`20-the-agent-player-and-research.md`](20-the-agent-player-and-research.md) | what an agent is given; the same view as a human; the log; tags; replay; research runs | draft for review | [`adr/0005`](../architecture/adr/) |
| 21 | [`21-endings-and-recap.md`](21-endings-and-recap.md) | rescued or dead; surviving long enough as the hardest rescue; ghosts; the recap | draft for review | — |
| 22 | [`22-the-world-building-loops.md`](22-the-world-building-loops.md) | the phases; both models as peers; the scaffold; the queue; walls per run | draft for review | `harness.md` (pending) |

## The template — every document has these eight parts, in this order

1. **Status banner** — `draft for review` / `reviewed with Andrew <date>` / `finalized <date>` /
   `superseded`; the architecture counterpart; the sources it was built from.
2. **Provenance** — Andrew's decisions, quoted, with dates. Then *Proposals (Claude)*. Nothing is left
   unlabelled.
3. **In one paragraph** — what the player experiences.
4. **The design** — the rules, then the Whiteout content (objects, events, numbers) as proposals.
5. **Interactions** — which systems this depends on; which depend on it.
6. **Open questions** — for the review; each with the options and a recommendation.
7. **Review log** — date, what was decided, what was cut, what was sent back.
8. **What exists today** — built / designed / nothing, honestly, with pointers to code and probes.

## Writing rules (for anyone — person or agent — who writes here)

- **Known facts and open questions only.** Nothing is invented to fill a section. A short honest
  document beats a full invented one; a half-thought placeholder is worse than a blank marked open.
- **Every claim has a source**: a quote of Andrew's with a date, a document section, a code path, or a
  probe id. If none exists, it is an open question.
- **The world is open-ended**: never describe a verb set, a vocabulary or a room as finished or
  bounded; every count is a floor.
- **Never a menu**: no design here may have the game list options, suggest verbs, or name what is
  reachable; feedback is a clarification or the physics of why.
- **No stats** in status text (no test counts, no percentages that rot); *built / designed / nothing*.
- The doc-consistency gate applies: never write `Pass <digit>`, `event-driven`, `mass_kg`,
  `CMD_NOMATCH`, `intent-fallback`, or a Markdown link to `design.md`.
