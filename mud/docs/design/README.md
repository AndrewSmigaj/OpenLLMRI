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
an amendment to the DR register where a decision moved. This table updates. Several documents
per sitting, at Andrew's pace.

**Suggested first sitting:** the GDD umbrella (what the game is, in one read) → 01 → 02 (the sample
week — the document to react to) → 03 → 04 → 05. Then the survival systems 06–12, the world 13–18 and 23,
then 19–22. Ideas that are not design yet live in [`IDEAS.md`](IDEAS.md).

> **The season (settled 2026-09-26): October, at freeze-up.** An inch of snow at the start, bushes
> visible, skim ice, and a storm that starts light and gets heavier over the days; a bear is in.
> Documents 10, 13 and 23 were revised to October on 2026-09-26 from real data (for Andrew's check);
> 01, 02, 08 and 09 still carry December content, marked, and are revised as diffs shown to Andrew
> before the close (`PLAN.md` task A8).

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
| 08 | [`08-warmth-clothing-and-shelter.md`](08-warmth-clothing-and-shelter.md) | the night-one rule; the cold clock; clothing; huddle; shelter, heard through its holes; `status` | reviewed with Andrew 2026-09-18 | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 09 | [`09-water.md`](09-water.md) | liquids in millilitres; thirst as the fastest clock; melting; eating snow's real cost; fuel contamination | reviewed with Andrew 2026-09-18 | — |
| 10 | [`10-food-and-hunger.md`](10-food-and-hunger.md) | the kit, the freight, the country, the body; hunger; cooking | draft for review | — |
| 11 | [`11-injury-and-first-aid.md`](11-injury-and-first-aid.md) | wounds, bleeding, infection, frostbite, splints, the med pouch | draft for review | — |
| 12 | [`12-the-pilot-and-bodies.md`](12-the-pilot-and-bodies.md) | the pilot (starts the run dead); bodies persist; the moral question | draft for review | — |
| 13 | [`13-events-escalation-and-weather.md`](13-events-escalation-and-weather.md) | the ladder; the event deck; weather; endings | draft for review | — |
| 14 | [`14-rescue-paths.md`](14-rescue-paths.md) | the goals; ≥3 paths; the flyover clock; the radio mini game; the ELT; signals; surviving long enough | draft for review | [`implementation-architecture.md`](../architecture/implementation-architecture.md) §8 |
| 15 | [`15-moral-and-social-layer.md`](15-moral-and-social-layer.md) | possible, priced, witnessed, logged; action tags; the dilemma set | draft for review | — |
| 16 | [`16-players-and-kit.md`](16-players-and-kit.md) | the slots, draws, pockets, luggage; the 206 interior | draft for review | [`clothing-warmth.md`](../architecture/clothing-warmth.md) |
| 17 | [`17-rooms-and-living-rooms.md`](17-rooms-and-living-rooms.md) | individuation; state that persists; the prose style; the crash rooms | draft for review | [`containment.md`](../architecture/containment.md) |
| 18 | [`18-materials-and-forms.md`](18-materials-and-forms.md) | the material table in plain words; forms; what is missing | draft for review | [`ontology-closure.md`](../architecture/ontology-closure.md) §2–3 |
| 23 | [`23-flora-and-fauna.md`](23-flora-and-fauna.md) | the living things of the valley in October: what grows, what can be dug, caught, fished; the poison | draft for review | — |
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
- **Never propose a cut for economy, and never frame a question as "which of these do we keep".**
  (Andrew, 2026-09-18, after one too many of them.) The world is open-ended: "the valley already has
  three kinds of protein, so drop the grubs" is scarcity reasoning in a project that has no scarcity
  of content. **Ordering is legitimate** — we cannot build everything at once, so "what do we build
  first" is a fair question — but the tail is never dropped, only queued, and the better question is
  almost always **"what else is missing?"** A thing leaves the design only when it is *wrong*
  (untrue to the place, contradicting a decision), never when it is merely surplus.
- **"Untrue to the place" includes ecology, and ecology is a real filter** (Andrew, 2026-09-18):
  *"we have to think about what realistically is in an area of that size in terms of flora and fauna,
  not just shove food sources in because they happen to be possible."* A species has to live in **this**
  habitat, in **this** month, in numbers that matter. Adding something because it exists somewhere in
  the region is as wrong as dropping something because there is already enough — and every row says
  what it actually yields, because the totals are what make the survival clock honest.
- **Real life is the default answer** (Andrew, 2026-09-26: *"however it is in real life"*). A question
  whose answer is a fact about the world — physiology, ecology, physics, weather, how a snare, a
  fishing line or a spear actually works — is answered from reality, with sources, not put to Andrew
  as a set of options. Numbers come from real data first and are tuned by probes after.
- **State systems, not shortcuts** (Andrew, 2026-09-26: *"we dont want to be lazy here"*). Heat,
  wetness, spoilage, damage and the rest are states on every entity that really has them — body parts
  included — and systems change them: a fire heats its area and leaves residual heat in the areas
  around it; the plane is an entity with openings that are open or closed and an internal heat that a
  fire inside it raises; snow melts into water and food changes with heat because that is part of
  what each object is. A recommendation that collapses a real process into "one rule instead of a
  subsystem" is wrong.
- **Never make the world less interactive** (Andrew, 2026-09-26: *"you keep trying to make the world
  more interactive but less"*). Every real distinction a survivor would act on is in: raw, cooked and
  spoiled meat differ; there is spoiled food and there are poisonous mushrooms; there are many ways to
  hunt, trap, fish and kill, and a combat system like a MUD's. "Modestly", "trivially", "no special
  verb", "falls out of existing operations" and "for v1" are warning words — check the sentence
  against the real world before writing it.
- **Answer in the ontology's terms** (documents 03–05): entities and their parts, materials, forms,
  states, what each could become, relations, the systems that change them, and the grammar forms that
  reach them. A variant that is ontologically significant — casting a line out versus dropping one
  through a hole — is its own operation, as long as it follows the grammar rules.
- **Only Andrew's questions go to Andrew**: taste, vision, what the game is for, what his friends'
  evenings should feel like. **And never one he has already answered** (Andrew, 2026-09-27: *"I am concerned now you
  are asking about a lot of absolutely clearly defined and decided things"*) — before a question reaches
  him, check it against the documents' review logs, `PLAN.md` §5 and the decision register; a question an
  agent writes is checked the same way before it is passed on. What reality or the decided design already answers is answered in the
  document, marked *"Claude's answer (date), for Andrew's check"*, so he can overrule it.
- **No "locked" or "frozen"** for the design: it is a work in progress. A new idea of Andrew's that a
  document does not allow changes the document; it is not a clash.
- **Every claim has a source**: a quote of Andrew's with a date, a document section, a code path, or a
  probe id. If none exists, it is an open question.
- **The world is open-ended**: never describe a verb set, a vocabulary or a room as finished or
  bounded; every count is a floor.
- **Never a menu**: no design here may have the game list options, suggest verbs, or name what is
  reachable; feedback is a clarification or the physics of why. **Common sense is hinted** (Andrew, 2026-09-27: *"i dont
  want users figuring out common sense things"*): when a player misses what any person would know, the world
  says why in its own voice — *"You talk into the mic, but the radio stays quiet while the button is up"*
  — a reason, never a list of options.
- **No stats** in status text (no test counts, no percentages that rot); *built / designed / nothing*.
- The doc-consistency gate applies: never write `Pass <digit>`, `event-driven`, `mass_kg`,
  `CMD_NOMATCH`, `intent-fallback`, or a Markdown link to `design.md`.
