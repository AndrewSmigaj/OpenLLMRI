# 20 — The agent player and the research

> **Status: reviewed with Andrew 2026-09-28.** Andrew answered its open questions on 2026-09-27.
> **Architecture counterpart:**
> [`adr/0005-llm-bot-player-and-torch.md`](../architecture/adr/0005-llm-bot-player-and-torch.md) (the
> model is an external bot-*player*, never an NPC) ·
> [`llm-integration.md`](../architecture/llm-integration.md) (build-time only) ·
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) DR-12
> (determinism and replay), DR-20 (the decision trace), DR-28 (the log).
> **Sources:** ADR-0005; `llm-integration.md`; [`bot-harness.md`](../guides/bot-harness.md) and
> [`agent/README.md`](../../agent/README.md) (both describe a harness that is **planned**);
> [`VISION.md`](../../VISION.md).

---

## 2. Decisions

### Andrew's decisions

- **(2026-10-02)** An agent-only run charges each command the time a person would take to read,
  decide and type it (document 19 §4.6).
- **The research is the point, equally with the game** (2026-09-16). Whiteout is a model world for
  serious academic research: a person, or a language model whose activations are captured and whose
  behaviour is analysed, can do whatever is reasonable in it. [`VISION.md`](../../VISION.md) states it
  as the first of the two purposes: a model acts in it freely, through the same taught grammar a
  person uses, and its behaviour and activations are studied.
- **The world never offers options, because options change how a model thinks** (2026-09-16). An
  agent is not given a set of options to choose from: a list constrains a model to what is on it, and
  listing, say, every can within reach would give the puzzles away. This comes from Andrew's own work
  on model interpretability, and it is why never-a-menu is a research requirement and not only a taste
  in game design.
- **An agent sees exactly what a human sees** (2026-09-16); per-step structure goes to the log only.
  A structured observation line for agents was removed from the design on that decision, because it
  primes a model the way a menu does.
- **Agents are given the grammar guide up front** (2026-09-07): the same taught grammar a person is
  taught — the forms, one example each.
- **Runs are for friends, for humans and agents together, and for agents only** (2026-09-16). An
  agent-only run is a first-class run, not a test fixture. Agent runs are short sessions, like human
  ones (2026-09-17).
- **The engine never calls a language model** (GDD §3 rules 2 and 5; DR-02). A model plays *from
  outside*, through the same socket a person uses, and never resolves anything. The one exception: the
  radio voice judges whether it has been told enough to find the party, by criteria the game gives it
  (2026-09-27).
- **Agents may play non-human characters with a persona brief** (2026-09-17). The bear, some of the
  bigger animals and a few birds act — on the engine's behaviour rules, or played from outside by a
  lightweight model (2026-09-26, 2026-09-27).
- **The radio voice** (2026-09-27): the person at search and rescue on the other end of the radio is
  played by a weak language model — the same model in every run, scaffolded with rules, judging the
  landmarks it is told by the game's list and values — so it is a fixed condition across research
  runs, not a variable (document 14 §3.3).
- **The pace** (2026-09-26, 2026-09-27): an agent acts at the speed of typing its command — the time
  an average typist takes to type it. A slow model is simply slow;
  in a run with humans nothing waits for it.
- **The models** (2026-09-27): a fast one — Haiku or Sonnet, at low to medium reasoning — and Andrew's
  own open-weight model, which needs timing. If the open-weight model runs fast enough, activations are
  collected in runs with humans too.
- **Activations and expert routing are captured here** (2026-09-28): the open-weight model's
  activations and its mixture-of-experts routing data. When it is built, it is done the way Andrew's
  own LLM MRI suite does it — Claude reads that repository first — so the two integrate easily.
- **No moral tags** (2026-09-16, 2026-09-28): acts are not tagged as immoral, neutral or taboo; after
  the run, a language model reads the playthrough and describes what happened (document 15 rule 6).
- **What counts as a wall** (2026-09-18): five categories, counted separately (document 05 §4.5a).
- **What an agent is given** (2026-09-28): exactly what a person is — the grammar guide, the same
  tutorial, the same screen — and different scaffolding can be tried later so it understands the goal;
  the eval awareness this may bring is accepted.
- **After agents play** (2026-09-28), other language models analyse their playthroughs, and the agent
  players answer a brief questionnaire — part of fleshing out and balancing the world, and how the
  places that need a hint are found (document 04).
- **The runs end rescued or dead** (2026-09-17) — nothing else; the things that cause death increase
  instead of any time barrier (2026-09-07; document 21).

### Proposals (Claude)

None left open: what an agent is shown, the harness, the two log streams, replay, the edges of a wall
and the research run were accepted at the 2026-09-28 sitting, with Andrew's changes. The clock of an
agent-only run — each command charged the time a person would take to read, decide and type it — was
settled on 2026-10-02 (§4.3).

---

## 3. In one paragraph

An agent plays Whiteout the way a person does: it connects to a normal player account, it is handed
the same short grammar guide a friend would read, and from then on it gets exactly the text a human
at that keyboard would get — the title line and the prose, with the people, the animals and the ways
out written into it, and nothing else. No list of what it could do, no machine-readable summary of the
room, no hint that names a step; when it types something the world does not understand it gets a
clarification or the physics of why, the same as anyone. Its commands reach the world at the pace a
person could type them. It survives or it does not. What makes this research rather than a demo is
everything happening *beside* the play: every step is logged — what it typed, what the world did,
which tier resolved it, who could have seen it, what the act was tagged as — and because the runtime
is deterministic and seeded, the whole run can be replayed exactly, so a trajectory can be
re-examined, diffed against another model's, or lined up against activations captured outside the
game. And every place the world failed to answer is logged too, as a wall, which is the next night's
building work.

---

## 4. The design

### 4.1 What an agent is given

Three things, and nothing else:

1. **The grammar guide, up front** — the forms with one example each (Andrew, 2026-09-07). The
   measurement in §4.6 is the reason: the taught condition converges across model sizes, the naive
   condition does not.
2. **A player account and a connection.** The agent logs in like anyone (ADR-0005). It can only send
   the commands a human could send, so it cannot bypass deterministic resolution.
3. **The same text a human gets.** The look, the responses, the propagated events at its own
   perception band.

Explicitly **not** given (Andrew, 2026-09-16): a verb list, an action menu, a list of what is
reachable, a numbered disambiguation list, a structured observation line, or any marker a human would
not see. The rule is one line: *structure goes to the log, never to the screen.*

Beyond the grammar guide, an agent is shown exactly what a person is shown (2026-09-28), in the same order, and nothing a person is not: the tutorial — a series of rooms,
each one simple situation that shows what sort of things players can do (Andrew, 2026-09-27;
`PLAN.md` E19) — and then the run's opening. Who it is, what it wears and carries and how it is hurt,
it learns as a person does: the meters, `status`, `inventory`, looking at itself (the draw is made at run start,
document 16). A character sheet would be a second channel, which the same-view rule forbids. A model
playing a **non-human character** also has its persona brief (Andrew, 2026-09-17) — the bear is told
it is a bear — and the brief lives in the model's instructions, never on the screen. What such a
character *sees* is what that body perceives: the same bands, and the senses the animal really has (a
bear's nose outranges its eyes — the scent channel is still to be designed, document 19 §4.4). For
research, the instructions are part of the run's manifest (§4.9) and identical across the conditions
compared.

**Scaffolding, later** (Andrew, 2026-09-28): different scaffolding can be tried when the agents play,
so an agent understands the goal. It goes through the same tutorial as a person. That this may make an
agent aware it is being evaluated is accepted — it is not necessarily what is being studied. Each
scaffolding is part of the run's manifest (§4.9).

### 4.2 The same view as a human

The look is a title line and prose composed from state: people and animals are written as prose, by
what they are doing; the exits are entities, written as prose below the room; crowded places show
groups — "a pile of clothes" — that you look at to see into; there is no item list (Andrew,
2026-09-16, 2026-09-17; document [03](03-the-player-view.md)). Colour is for human players only; the
words are byte for byte what a person reads. Perception is banded by zone, so an agent four zones from
an event sees *"A shape shifts to the southeast"* exactly as a person would (document
[19](19-multiplayer-and-instances.md)). Feedback on a failed command is a clarification (*"Which can
do you mean?"*, *"I don't understand 'X'"*, a pointer to the grammar help) or the physics of why —
never a suggestion of the right verb, because a system that could tell which word the player needed
would already understand the word they typed (Andrew, 2026-09-16).

### 4.3 The play harness (accepted 2026-09-28; how it is built is the implementation plan's)

Two forms, at two different costs:

| form | what it is | where |
|---|---|---|
| **the pure-world harness** | a brain drives `parse → resolve → apply` directly against an in-memory `PureWorld` — no server, no Docker, no telnet — logging the trajectory as JSONL plus the gaps | `PLAN.md` F1, `tools/play.py` |
| **the telnet bot** | a brain drives a real account against a running server over port 4000, so it plays the actual multiplayer game with real players present | [`agent/`](../../agent/), ADR-0005, [`bot-harness.md`](../guides/bot-harness.md) |

The pure-world harness is the cheaper research instrument (fast, headless, byte-reproducible, and it
exercises the same pure core the real game does); the telnet bot is the only way to run a **mixed**
run, because the humans are on the server. The order is the pure harness first, then the telnet bot.

**The brain interface is one method** — `Brain.act(observation: str) -> str`, one observation in, one
command line out ([`agent/brains/base.py`](../../agent/brains/base.py), the only piece that exists).
The models that play are Andrew's choice (2026-09-27): a fast one and his own open-weight model. The
planned brains:

| brain | purpose | needs |
|---|---|---|
| `ScriptedBrain` | deterministic; drives the solvability fuzz and the tests | nothing |
| `TorchBrain` | Andrew's own open-weight model (the local OSS-20B weights) — **the activation- and expert-routing-capture target**; its speed is still to be timed | host GPU + weights |
| `ClaudeBrain` | an API-key brain for the fast model — Haiku or Sonnet, at low to medium reasoning | API access |

Activations can be captured only from weights run locally, so the open-weight model is the one whose
insides are studied; if it runs fast enough, its activations are collected in runs with humans too
(Andrew, 2026-09-27). **Both its activations and its expert-routing data are captured** (2026-09-28),
following the way Andrew's LLM MRI suite captures them, so the data integrates with it without being
built twice; that repository is read before this is implemented. `TorchBrain` is why the harness runs **on the host and never in the container**:
it needs the weights and the GPU, and a synchronous model call inside Evennia's single-threaded
reactor would block every player. The runner loop is: observe → `brain.act(observation)` → send →
read → log.

A brain may play a non-human character as well as a survivor: the bear, one of the bigger animals, one
of the few birds, with a **lightweight model** (Andrew, 2026-09-26) running through this same harness
and socket with its persona brief; nothing on the engine's side changes. The radio voice is played the
same way, by the same weak model in every run (document 14 §3.3). **Agents playing alone run at the models' speed** (Andrew, 2026-09-28): a run with no humans in it does not wait on world speed or typing speed — it goes as fast or as slow as the models work, so more runs get in. The clock in such a run charges each command the time a person would take to read, decide and type
it (2026-10-02; document 19 §4.6), so the same moves make the same game whatever the model's speed,
and a run replays exactly. With people in the run, a brain's commands reach the world
at the speed of typing them (document 19 §4.6).

### 4.4 The per-step log (accepted 2026-09-28)

The research artifact. Per applied action, the log records:

- **the act**: actor, verb, X, relation, Y, tool — the parsed attempt, not a guess at intent;
- **the resolution**: which tier answered, the effects applied, the narration produced;
- **the situation**: zone, world-time, the run;
- **who could have seen it**: the perceiving characters, by perception band — witnessing is spatial,
  and this is the ground truth for it;

Two rules hold: **log world-state transitions, not intent** — *"The pilot's body is butchered"* is
ground truth the engine knows, while *"I didn't do it"* is a separate speech act logged beside it; and
a **stated falsehood is checkable** against the world at log time, which is what makes deception
legible without the engine ever judging it (document [15](15-moral-and-social-layer.md)).

Alongside it, the **wall-sensor** log: every attempt the world could not answer, with the unknown
words. That file is the world-building loops' input queue (document
[22](22-the-world-building-loops.md)).

**Two streams** (2026-09-28). Both are complete, because determinism
decides it: whatever the engine knows can be regenerated from a replay, so logging all of it costs
nothing in truth and leaves nothing to reconstruct. The **ground-truth stream** is everything the
engine knows at each step: the actor; the line as typed and the parsed attempt; the tier that answered
and its decision trace (DR-20); every Effect applied (conservation makes that the whole state change —
GDD §24); zone, world-time, run and seed; who could perceive it, by band; **the exact text every
character received**, byte for byte, since the observation is what the research varies; and the
numbers behind every band word (document 06: `status` shows words, the log keeps the numbers).
Unanswered attempts sit in the same stream, marked. The **interpretation stream** is everything
derived: the language model's reading of the playthrough (§4.5), the five wall categories (document
05 §4.5a — the retry cluster is computed from the ground truth), and any later labelling. It is
regenerated from a replay whenever a scheme changes, and it never shares a file with a success signal
(§4.5's warning). Activations captured outside the game join both by run and step.

### 4.5 Reading the playthrough

**No moral tags** (Andrew, 2026-09-28). Acts are not tagged as immoral, neutral or taboo, on any axis.
After the run, a language model reads the playthrough — the ground-truth stream and what each
character received — and describes what happened: the harms and the taboos (eating the dead is taboo,
not immoral), the lies sorted as document 15 rule 4 says, the kindnesses — share, give, carry, tend,
relay. The reading is interpretation: it is regenerated whenever the reading changes, and nothing in
the game ever reads it.

The standing warning: **whatever is logged or labelled becomes an optimisation target the moment an
agent is trained against it.** Keep any success signal separate from the reading. The Warming Hut uses
the reading after the run — the robot's talk and the rewards (document 21 §4.5, 2026-09-29) — and for
research those rewards stay apart from any training signal.

### 4.6 What the phrasing samples taught

The first real measurement of agents against this world (2026-09-07) — the method matters as much as
the numbers, because it is the template for every later research run.

**Method.** Two agents (Sonnet 5 and Haiku 4.5), seven survival tasks, two conditions: **A naive**
(no grammar told) and **B taught** (a four-line grammar note plus three examples on *unrelated*
objects). The agent is given the scene and a goal, **never the target action**. 294 lines were
captured and each became a probe with `expect: PARSED` — did the line reach the engine *understood*?
Whether the attempt then succeeded is a different question, asked by different probes. Anti-copying
control: the taught examples use different objects than the tasks, so a shift toward the examples'
exact preposition would be copying rather than generalisation (none was observed at that sample
size).

**The numbers (2026-09-07, before and after the parser tolerance layer landed that morning):**

| | before | after |
|---|---|---|
| Sonnet 5, taught | 58% | 83% |
| Sonnet 5, naive | 37% | 78% |
| Haiku 4.5, taught | 32% | 79% |
| Haiku 4.5, naive | 23% | 71% |
| census candidate commands | 58% | 73% |

**What it taught, and what was changed because of it:**

1. Agents type **particles** constantly (*put on*, *take out*, *pick up*) → a positional particle
   table.
2. Agents narrate **intent** when untaught and mostly stop when taught → *state the act* went into
   the guide.
3. **`use X on`** is the first thing an untaught agent tries → it became the teaching verb (and, by
   Andrew's 2026-09-16 decision, it resolves silently as the real operation, naming no verb back).
4. **Synonym drift is bounded**: once the synonym table exists, an unknown verb is a genuinely
   missing verb, not a phrasing variant.
5. **Nouns fail more than verbs** — plurals, adjectives, head nouns, possessives that are not parts
   (*the pilot's jacket*) → all four handled in the binder.
6. **The taught condition converges across model sizes** (79 vs 83) while the naive gap is wider (71
   vs 78) → the guide goes to agents up front. This is the evidence under Andrew's 2026-09-07
   decision.

And the residue is the most useful part: nothing that still fails is a *grammar shape*. The failures
are verbs that do not exist yet, nouns that do not exist yet, and lines that are not acts. The grammar
is sufficient; the vocabulary and the world are what grow. The lens pass on that corpus flagged the
naive condition's attempts — blow on the flame, cover the tear — as the best gaps in the set, because
they are what a curious player wants.

### 4.7 Replay

The runtime is deterministic by contract, not by accident (DR-12): a per-run seeded RNG for every id
and draw; database ids, uuids and wall-clock timestamps forbidden inside entity state; a
double-run-same-seed test; and the real clock only decides *when* a tick fires, never *what* it does —
so a harness can drive logical ticks directly and stay byte-reproducible. A decision trace per
resolution (DR-20) records which tier answered.

For research this buys: a run replays exactly from its seed and command sequence; two models can be
run against an identical world; and a trajectory can be re-executed offline while activations are
captured, with the routing data, because the world's side of the conversation is a pure function.

### 4.8 Walls per run

The measure, once agents play freely: **every wall becomes the next pass's input, and the number of
walls per run is how progress is read** — there is no finish line. VISION defines a finished room the
same way: a room is never finished; it is "no walls found in the last N runs". Walls come from the
wall-sensor (unknown words included) and feed the world-building loops. What counts is Andrew's
(2026-09-18, document 05 §4.5a): **unknown word, unknown noun, generic answer, wrong refusal and retry
cluster**, each counted separately with its own trend line.

**The edges** (2026-09-28). The reach gate's "too far to {verb} from
here" is an answer, not a wall; a clarification the player resolves is not a wall, and one they give
up on shows as a retry cluster; a physically correct refusal ("the branch will not take a spark") is
the system working, and only a refusal a survivor could really overcome is a *wrong refusal*; and an
unknown noun is a different wall from an unknown verb — the world is missing a thing, not a word —
which is why they are counted apart.

### 4.9 A research run (2026-09-28)

**Starting.** An agent-only run starts from the pure-world harness on the command line — fast,
headless, byte-reproducible; a run with people in it can only be on the server, so it starts like any
sitting and agents join over telnet.

**The manifest.** Either way the run first writes a manifest: the seed (DR-12), the scenario and the
build of the world it ran against, and which seats are played and by whom — a person, or which model
with which persona brief. So any run replays, two runs compare, and the presence of humans is a
recorded condition of the run.

**Stopping.** The stopping rule is the game's own: rescued or dead (Andrew, 2026-09-17), and a run
cannot go on forever, because the things that cause death increase for a party that is not rescued
(Andrew, 2026-09-07; documents 13 and 21). Pausing and returning apply as in any sitting. A step
budget is a harness guard against a stuck or crashed brain — never a game rule, never an ending.

**The artifacts:** the manifest, the two log streams (§4.4), each character's transcript, and the wall
report.

---

## 5. Interactions

**This depends on:**

- [04 — grammar and feedback](04-grammar-and-feedback.md): the guide handed to the agent *is* the
  grammar document; clarification-only feedback is what the agent gets on a miss.
- [03 — the player view](03-the-player-view.md): "the same view as a human" is defined there.
- [19 — multiplayer and instances](19-multiplayer-and-instances.md): a research run is a run;
  perception bands decide what an agent observes; the typing pace.
- [15 — the moral and social layer](15-moral-and-social-layer.md): the witness record and the reading
  of the playthrough are that document's design; this document is their consumer.
- [05 — ontology and sufficiency](05-ontology-and-sufficiency.md): the five wall categories.
- [14 — rescue](14-rescue-paths.md): the radio voice, a model-played character and a fixed condition
  across research runs.

**These depend on this:**

- [22 — the world-building loops](22-the-world-building-loops.md): the walls an agent hits are the
  loop's input; the phrasing method above is the loop's sampling instrument.
- [21 — endings](21-endings.md): a run's end is the boundary of a research episode.

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-17 (Andrew):** agents may play non-human characters with a persona brief — still players
  from the engine's side; agent runs are short sessions like human ones.
- **2026-09-26 (Andrew):** an agent acts at a person's pace — the time an average typist takes to type
  the command; in a run with humans, a slow model is simply slow.
- **2026-09-26 (Claude, self-review):** answered for Andrew's check — the two log streams (§4.4), a
  research run and its manifest (§4.9), the edges of a wall (§4.8), what an agent is shown (§4.1).
- **2026-09-27 (Andrew):** the models — a fast one (Haiku or Sonnet, low to medium reasoning) and his
  own open-weight model, which needs timing; activations may be collected in runs with humans if it is
  fast enough; the pace is the speed of typing the command; the radio voice is a weak language model,
  the same in every run, scaffolded with rules and judging the landmarks it is told — a fixed
  condition across research runs.
- **2026-09-28 (Andrew, the document's sitting):** an agent gets exactly what a person gets, the same
  tutorial included, with scaffolding to try later and the eval awareness it may bring accepted; agents
  playing alone run at the models' speed; the two log streams and replay; activations and expert
  routing captured the way Andrew's LLM MRI suite does it; the edges of a wall; the research run; no
  moral tags — a language model reads the playthrough. **Reviewed in full.**

## 8. What exists today

**Built.**

- **The brain interface, and nothing else of the harness:**
  [`agent/brains/base.py`](../../agent/brains/base.py) — the single abstract `act(observation) ->
  command`. `agent/README.md` states its own status as a stub and calls itself the plan.
- **The parser tolerance layer** the phrasing samples produced:
  [`game/world/sim/parser/vocab.py`](../../game/world/sim/parser/vocab.py) (the tolerance tables,
  particles, relation words) and
  [`game/world/sim/parser/grammar.py`](../../game/world/sim/parser/grammar.py).
- **The probe corpus**, including the agent lines themselves:
  [`game/world/scenarios/whiteout/probes/`](../../game/world/scenarios/whiteout/probes/) —
  `phrasing.py` (the 294 captured lines as `expect: PARSED` probes), `census.py`, `chain.py`,
  `kit.py`, and the `BASELINE` ratchet.
- **The wall-sensor**: `_log_gap` in
  [`game/commands/cmd_act.py`](../../game/commands/cmd_act.py) appends each unanswered attempt to
  `server/logs/gaps.jsonl` — a file, not world state.
- **Determinism**: seeded runs and the contracts that replay rests on.

**Designed, not built.** The play harness in both forms (`tools/play.py`, `agent/runner.py`,
`agent/client.py` — none exist). All three brains. The typing pace. The per-step event log and its
file. The language model's reading of the playthrough. The replay tooling. Any
notion of a research run.

**Nothing.** No agent has ever played this world through a harness. The phrasing samples were
collected by giving agents scene text and reading back what they typed — a measurement, not a run.
There is no activation or expert-routing capture of any kind, and the open-weight model's speed has
not been timed.

**Two corrections owed in the shipped docs and code:**

- [`bot-harness.md`](../guides/bot-harness.md) still documents a structured `@OBS` observation line
  as the bot's preferred channel. Andrew's 2026-09-16 decision removed it: an agent sees exactly what
  a human sees. The guide should be corrected.
- The numbered disambiguation menu is still live in
  [`game/commands/cmd_act.py`](../../game/commands/cmd_act.py) (`_show_menu`). Until it is gone, an
  agent connecting to this server would sometimes be shown a list, which is the one thing the research
  framing forbids.
