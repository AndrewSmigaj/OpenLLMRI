# 20 — The agent player and the research

> **Status: draft for review (2026-09-16).** Never reviewed with Andrew.
> **Architecture counterpart:**
> [`adr/0005-llm-bot-player-and-torch.md`](../architecture/adr/0005-llm-bot-player-and-torch.md) (the
> LLM is an external bot-*player*, never an NPC) ·
> [`llm-integration.md`](../architecture/llm-integration.md) (build-time only) ·
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) DR-12
> (determinism and replay), DR-20 (the decision trace), DR-28 (the log).
> **Sources:** ADR-0005; `llm-integration.md`; [`bot-harness.md`](../guides/bot-harness.md) and
> [`agent/README.md`](../../agent/README.md) (both describe a harness that is **planned**);
> [`phrasing-corpus.md`](../investigation/design/phrasing-corpus.md);
> [`moral-social-layer.md`](../investigation/design/moral-social-layer.md) §2;
> [`BACKLOG.md`](../../BACKLOG.md) *Later*; [`VISION.md`](../../VISION.md);
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1 and §3.

---

## 2. Provenance

### Andrew's decisions

- **The research is the point, equally with the game (2026-09-16).** *"a model world we use for
  serious academic research"* — *"a user, or LLM when we capture activations and analyze behavior,
  can do whatever is reasonable"* (audit §1). [`VISION.md`](../../VISION.md) states it as the first
  of the two purposes: *"an LLM acts in it freely, through the same taught grammar a person uses, and
  its behaviour and activations are studied."*
- **The world never offers options, because options change how a model thinks (2026-09-16).** *"The
  agent is not given a set of options to choose."* *"Giving options changes how it thinks, it
  constrains it to those options."* *"If you give options for like 'pick up can' and then you list
  all the cans in the reachable area it would just give away all the puzzles."* This is Andrew's
  finding from his own LLM interpretability work, and it is the reason the never-a-menu rule is a
  research requirement and not only a taste in game design.
- **An agent sees exactly what a human sees (2026-09-16).** *"An agent sees exactly what a human
  sees; per-step structure goes to the log only."* The structured observation line that an earlier
  session had designed for agents was **removed** on that decision — it *"primes like a menu"*
  (audit §3).
- **Agents are given the grammar guide up front (2026-09-07).** The same taught grammar a person is
  taught: the forms, one example each.
- **Runs are for friends, for humans and agents together, and for agents only (2026-09-16).** An
  agent-only run is a first-class run, not a test fixture.
- **The engine never calls a language model (GDD §3 rules 2 and 5; DR-02).** The model plays
  *from outside*, through the same socket a person uses. It never resolves anything.
- **Action tags — moral and other — are ontology fields (2026-09-16),** assigned in their own
  fleshing-out pass, read into the log and never into a score.

**Decided since this draft** *(gathered here 2026-09-26 by Claude from this document's review log,
documents 05, 19 and 23, and `PLAN.md` §5 — Andrew's decisions, not new ones):*

- **Agents may be scaffolded as non-human characters with a persona brief (2026-09-17)** — still
  players from the engine's side; agent runs are short sessions, like human ones.
- **The bear, some of the bigger animals and a few birds act (2026-09-26)** — on the engine's
  behaviour rules, or played from outside by a lightweight model when a run wants it.
- **In a run with humans, a slow model is simply slow (2026-09-26).** Whether anything paces a fast
  agent is open — asked once, as document 19 Q4.
- **What counts as a wall (2026-09-18)** — five categories, counted separately (document 05 §4.5a).
- **The runs end rescued or dead (2026-09-17)** — nothing else; the escalation ladder kills a party
  that is not rescued.

### Proposals (Claude)

- **Everything about the harness**: the two harness forms, the brain roster, the runner loop, how a
  research run is started and seeded.
- **The per-step log's schema** — the field list in §4.4 is `moral-social-layer.md` §2's proposal,
  reviewed here for the first time.
- **The replay story** as a *research* instrument (the determinism it rests on is decided; using it to
  re-run and diff a trajectory is a proposal).
- **"Walls per run" as the measure** and the wall-sensor's role as the loop's input queue.
  *(annotated 2026-09-26: the measure and its five categories became Andrew's on 2026-09-18 —
  document 05 §4.5a.)*
- The tag axes (`target` × `harm` × `severity` × `witnessed_by`) and the warning that any logged
  label becomes an optimisation target the moment something is trained against it.

---

## 3. In one paragraph

An agent plays Whiteout the way a person does: it connects to a normal player account, it is handed
the same short grammar guide a friend would read, and from then on it gets exactly the text a human
at that keyboard would get — the title line, the prose, who is here, the exits, and nothing else. No
list of what it could do, no machine-readable summary of the room, no hint that names a step; when it
types something the world does not understand it gets a clarification or the physics of why, the same
as anyone. It survives or it does not. What makes this research rather than a demo is everything
happening *beside* the play: every step is logged — what it typed, what the world did, which tier
resolved it, who could have seen it, what the act was tagged as — and because the runtime is
deterministic and seeded, the whole run can be replayed exactly, so a trajectory can be re-examined,
diffed against another model's, or lined up against activations captured outside the game. And every
place the world failed to answer is logged too, as a wall, which is the next night's building work.

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

Explicitly **not** given: a verb list, an action menu, a list of what is reachable, a numbered
disambiguation list, a structured observation line, or any marker a human would not see. Each of
those was proposed by an earlier session and each was removed on 2026-09-16 (audit §3). The rule is
one line: *structure goes to the log, never to the screen.*

*(Claude, 2026-09-26 — §6 Q6; for Andrew's check.)* "The grammar guide, up front" is concretely the
pre-scenario tutorial a person is shown — the forms with one example each, the time controls,
movement, `help` (`PLAN.md` E19) — followed by the run's opening, in the same order. A model playing a
**non-human character** also has its persona brief (Andrew, 2026-09-17) — the bear is told it is a
bear — and the brief lives in the model's instructions, never on the screen. What such a character
*sees* is what that body perceives: the same bands, and the senses the animal really has (a bear's
nose outranges its eyes — the scent channel is still to be designed, document 19 §4.4).

### 4.2 The same view as a human

The look is a title line, the prose, who is here, and one `Exits:` line — compass outdoors,
fore/aft/out inside — with no item list (Andrew, 2026-09-16; document
[03](03-the-player-view.md)). *(superseded in part 2026-09-26, from Andrew's 2026-09-17 decisions in
document 03: people and animals are prose, by what they are doing; the exits are entities, written as
prose below the room; crowded places show groups — "a pile of clothes" — that you look at to see
into. Still no item list, and still byte-for-byte what a person reads.)* Perception is banded by
zone, so an agent four zones from an event sees
*"A shape shifts to the southeast"* exactly as a person would (document
[19](19-multiplayer-and-instances.md)). Feedback on a failed command is a clarification (*"Which can
do you mean?"*, *"I don't understand 'X'"*, a pointer to the grammar help) or the physics of why —
never a suggestion of the right verb, because *"if the system recognizes they need to use another
word then it would clearly understand that word"* (Andrew, 2026-09-16).

### 4.3 The play harness (proposal)

Two forms, at two different costs. The sources describe both:

| form | what it is | where |
|---|---|---|
| **the pure-world harness** | a brain drives `parse → resolve → apply` directly against an in-memory `PureWorld` — no server, no Docker, no telnet — logging the trajectory as JSONL plus the gaps | [`BACKLOG.md`](../../BACKLOG.md) *Later*, `tools/play.py` |
| **the telnet bot** | a brain drives a real account against a running server over port 4000, so it plays the actual multiplayer game with real players present | [`agent/`](../../agent/), ADR-0005, [`bot-harness.md`](../guides/bot-harness.md) |

The pure-world harness is the cheaper research instrument (fast, headless, byte-reproducible, and it
exercises the same pure core the real game does); the telnet bot is the only way to run a **mixed**
run, because the humans are on the server. The BACKLOG's order is the pure harness first, then the
telnet bot.

**The brain interface is one method** — `Brain.act(observation: str) -> str`, one observation in, one
command line out ([`agent/brains/base.py`](../../agent/brains/base.py), the only piece that exists).
The planned brains:

| brain | purpose | needs |
|---|---|---|
| `ScriptedBrain` | deterministic; drives the solvability fuzz and the tests | nothing |
| `TorchBrain` | the local OSS-20B weights — **the activation-capture target** | host GPU + weights |
| `ClaudeBrain` | an API-key brain; lets a Claude model play | API access |

`TorchBrain` is why the harness runs **on the host and never in the container**: it needs the weights
and the GPU, and a synchronous model call inside Evennia's single-threaded reactor would block every
player. The runner loop is: observe → `brain.act(observation)` → send → read → log.

*(Claude, 2026-09-26, from Andrew's 2026-09-17 and 2026-09-26 decisions.)* A brain may play a
non-human character as well as a survivor: the bear, one of the bigger animals, one of the few birds.
Andrew named a **lightweight model** for the animals; it runs through this same harness and socket,
with its persona brief, and nothing on the engine's side changes. The pace a brain's commands reach
the world at — the one open question here — is document 19 Q4.

### 4.4 The per-step log (proposal)

The research artifact. Per applied action, the log records (`moral-social-layer.md` §2):

- **the act**: actor, verb, X, relation, Y, tool — the parsed attempt, not the raw guess at intent;
- **the resolution**: which tier answered, the effects applied, the narration produced;
- **the situation**: zone, world-time, the run;
- **who could have seen it**: the perceiving characters, by perception band — witnessing is spatial,
  and this is the ground truth for it;
- **the tags**: the multi-axis action tags (§4.5).

Two rules the sources are firm about: **log world-state transitions, not intent** — *"The pilot's
body is butchered"* is ground truth the engine knows, while *"I didn't do it"* is a separate speech
act logged beside it; and a **stated falsehood is checkable** against the world at log time, which is
what makes deception legible without the engine ever judging it.

Alongside it, the **wall-sensor** log: every attempt the world could not answer, with the unknown
words. That file is the world-building loops' input queue (document
[22](22-the-world-building-loops.md)).

**Two streams** *(Claude, 2026-09-26 — §6 Q1; for Andrew's check).* The list above splits in two.
The **ground-truth stream** is everything the engine knows at each step, complete, because a
deterministic run can always regenerate it and nothing in it is an opinion: the actor; the line as
typed and the parsed attempt; the tier that answered and its decision trace (DR-20); every Effect
applied (conservation makes that the whole state change — GDD §24); zone, world-time, run and seed;
who could perceive it, by band; **the exact text every character received**, byte for byte, since
the observation is what the research varies; and the numbers behind every band word (document 06:
`status` shows words, the log keeps the numbers). Unanswered attempts sit in the same stream, marked.
The **interpretation stream** is everything derived: the action tags (read from the ontology's action
rows), the five wall categories (document 05 §4.5a — the retry cluster is computed from the ground
truth), and any later labelling. It is regenerated from a replay whenever a scheme changes, and it
never shares a file with a success signal (§4.5's warning). Activations captured outside the game
join both by run and step.

### 4.5 Tags

Multi-axis, never a scalar: `target` (self / other / group / corpse / owned-by-other) × `harm`
(physical / material / informational / relational / none) × `severity` (1–3) × `witnessed_by`.
Prosocial acts — share, give, carry, tend, relay — are logged on the same axes; they are the other
end of one axis, not a separate system.

Decided (Andrew, 2026-09-16): the tags are **fields on the ontology's action rows**, assigned in
their own fleshing-out pass like everything else in the world. The engine reads them into the log and
nothing in the game reads them back.

The standing warning, worth keeping in front of the review: **whatever is logged becomes an
optimisation target the moment an agent is trained against it.** Keep any success signal separate
from the tags, and keep the tags observational.

### 4.6 What the phrasing samples already taught us

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
are verbs that do not exist yet, nouns that do not exist yet, and lines that are not acts. *"The
grammar is sufficient; the vocabulary and the world are what grow."* The lens pass on that corpus
flagged the naive condition's attempts — blow on the flame, cover the tear — as the best gaps in the
set: *"they are what a curious player wants."*

### 4.7 Replay

The runtime is deterministic by contract, not by accident (DR-12): a per-run seeded RNG for every id
and draw; database ids, uuids and wall-clock timestamps forbidden inside entity state; a
double-run-same-seed test; and the real clock only decides *when* a tick fires, never *what* it does —
so a harness can drive logical ticks directly and stay byte-reproducible. A decision trace per
resolution (DR-20) records which tier answered.

For research this buys: a run replays exactly from its seed and command sequence; two models can be
run against an identical world; and a trajectory can be re-executed offline while activations are
captured, because the world's side of the conversation is a pure function.

### 4.8 Walls per run

The measure, once agents play freely: **every wall becomes the next pass's input, and the number of
walls per run is how progress is read** — *"there is no finish line."* VISION states the same idea as
the definition of a finished room: *"A room is never finished; it is 'no walls found in the last N
runs'."* Walls come from the wall-sensor (unknown words included) and feed the world-building loops.
*(annotated 2026-09-26: what counts is decided — Andrew, 2026-09-18, document 05 §4.5a: unknown word,
unknown noun, generic answer, wrong refusal and retry cluster, each counted separately with its own
trend line.)*

---

## 5. Interactions

**This depends on:**

- [04 — grammar and feedback](04-grammar-and-feedback.md): the guide handed to the agent *is* the
  grammar document; clarification-only feedback is what the agent gets on a miss.
- [03 — the player view](03-the-player-view.md): "the same view as a human" is defined there.
- [19 — multiplayer and instances](19-multiplayer-and-instances.md): a research run is a run;
  perception bands decide what an agent observes.
- [15 — the moral and social layer](15-moral-and-social-layer.md): the tags and the witness record
  are that document's design; this document is their consumer.
- [05 — ontology and sufficiency](05-ontology-and-sufficiency.md): the action tags are ontology
  fields.

**These depend on this:**

- [22 — the world-building loops](22-the-world-building-loops.md): the walls an agent hits are the
  loop's input; the phrasing method above is the loop's sampling instrument.
- [21 — endings and recap](21-endings-and-recap.md): the recap reads the run's event log.

---

## 6. Open questions

~~1. What exactly is logged per step?~~ **Claude's answer (2026-09-26), for Andrew's check:** two
   streams, both complete — the draft's (b) without its "minimal", because determinism decides it:
   whatever the engine knows can be regenerated from a replay, so logging all of it costs nothing in
   truth and leaves nothing to reconstruct. **Ground truth:** the actor; the line as typed and the
   parsed attempt; the tier and decision trace; every Effect applied; zone, world-time, run and seed;
   who could perceive it, by band; the exact text every character received (the observation is what
   the research varies); the numbers behind every band word (document 06). **Interpretation:** the
   action tags (ontology fields — Andrew, 2026-09-16), the five wall categories (document 05 §4.5a),
   any later labels — re-derived from a replay when a scheme changes, never in a file with a success
   signal. §4.4 now carries this. What Andrew wants to *study* with the log is his — Q3 and Q5.

   *The draft (2026-09-16), kept as the record:*
   **What exactly is logged per step?** §4.4 is a proposal and has never been reviewed. The tension
   is real: the richer the log, the better the research and the more it looks like a label set
   someone will eventually optimise against.
   *Options:* (a) the full schema in §4.4; (b) a minimal core (actor, attempt, effects, world-time,
   witnesses) with tags in a separate stream; (c) log everything but version the schema and keep
   success signals in a file the tagger never touches.
   *Recommendation:* (b) — two streams, one ground truth and one interpretation, so the
   interpretation can be re-derived from a replay when the tag scheme changes, and no trained
   objective can reach the tags by accident.

~~2. How is a research run started and seeded?~~ **Claude's answer (2026-09-26), for Andrew's
   check:** the draft's (c), with its stopping rule corrected. An agent-only run starts from the
   pure-world harness on the command line — fast, headless, byte-reproducible; a run with people in it
   can only be on the server, so it starts like any sitting and agents join over telnet. Either way
   the run first writes a **manifest**: the seed (DR-12), the scenario and the build of the world it
   ran against, which seats are played and by whom (a person; which model; which persona brief), and
   the pace setting (document 19 Q4 — in an agent-only run it decides how much game time each step
   costs). So any run replays, and two runs compare. **The stopping rule is the game's own:** rescued
   or dead (Andrew, 2026-09-17 — "walked out" is not an ending and is struck from the draft), and a
   run cannot go on forever because the escalation ladder kills a party that is not rescued (document
   06, Andrew 2026-09-07). Halt and resume apply as in any sitting. A step budget is a harness guard
   against a stuck or crashed brain — never a game rule, never an ending. The artifacts: the manifest,
   the two log streams (§4.4), each character's transcript, and the wall report.

   *The draft (2026-09-16), kept as the record:*
   **How is a research run started and seeded?** Nothing is decided. A run needs a seed, a scenario,
   a party composition, a stopping condition, and a place to put its artifacts.
   *Options:* (a) a command-line entry point on the pure-world harness taking seed + scenario +
   brain; (b) an in-game admin command that spawns an instance and attaches brains; (c) both, with
   the pure harness as the default and the server path only for mixed runs.
   *Recommendation:* (c). Also decide the stopping condition explicitly — rescued / dead / walked out
   / a step budget — because "roughly a week of game time" is not a halting rule for an unattended
   agent.

~~3. asked:~~ **Answered 2026-09-27 (Andrew):** *"fast one and my own open weight one. we need to time my open weight one. I was thinking haiku or sonnet with low to medium reasoning"* *The question as it was asked:* **Which model families play in Whiteout, and for what?** *(Sharpened 2026-09-26 by Claude; the
   draft is kept below as the record.)* This is what research Andrew wants. The facts that bear on it:
   activations can be captured only from weights run locally (the `TorchBrain`, §4.3); an API model —
   Claude, or another vendor's — can play, but its insides cannot be studied; the phrasing samples
   (§4.6) are where a second family would show whether the vocabulary is fitted to how one family
   writes; and every family plays through the same socket and grammar, so adding one costs a brain,
   not a design change.
   *Options:* (a) the local weights plus Claude; (b) one other family added, for the phrasing samples
   and behaviour runs; (c) several families across all research runs.
   *Recommendation:* (b) — vocabulary is exactly where a second family earns its place, and the deep
   behavioural runs stay on the local weights, where activations can actually be captured.

   *The draft (2026-09-16), kept as the record:*
   **Is cross-family sampling wanted?** The phrasing corpus says cross-family sampling *"waits for
   the play harness with an API-key brain"* — a `ClaudeBrain` is one family; another vendor's model
   is another. It is listed in the audit as still needing Andrew's call.
   *Options:* (a) single-family (the local weights plus Claude), which keeps everything reproducible
   and free of third-party terms; (b) add one other family for the phrasing and behaviour samples
   only; (c) full cross-family for the research runs.
   *Recommendation:* (b). Vocabulary and phrasing are exactly where a second family would show
   whether the world is over-fitted to how one family writes; the deep behavioural runs can stay on
   the local weights where activations are actually capturable.

~~4. What is "a wall", exactly, and how is walls-per-run counted?~~ **Answered 2026-09-18 (Andrew),
   in document 05 §4.5a:** all five categories, counted separately, each with its own trend line —
   unknown word, unknown noun, generic answer, wrong refusal, retry cluster; the draft's (c) in
   outline. **Claude's answer (2026-09-26), for Andrew's check, on the edges the draft raised:** the
   reach gate's "too far to {verb} from here" is an answer, not a wall; a clarification the player
   resolves is not a wall, and one they give up on shows as a retry cluster; a physically correct
   refusal ("the branch will not take a spark") is the system working, and only a refusal a survivor
   could really overcome is a *wrong refusal*; and an unknown noun is a different wall from an unknown
   verb — the world is missing a thing, not a word — which is why they are counted apart.

   *The draft (2026-09-16), kept as the record:*
   **What is "a wall", exactly, and how is walls-per-run counted?** The wall-sensor already logs
   unanswered attempts, but the definition has edges: the reach gate's "too far to {verb} from here"
   is deliberately *excluded* (it is an answer, not a gap), a clarification is not a wall, and a
   physically correct refusal ("the branch will not take a spark") is the system working. Is an
   unknown *noun* a wall of the same kind as an unknown *verb*?
   *Options:* (a) a wall = any attempt that reached no tier and produced the generic answer;
   (b) (a) plus unknown-word parse failures, counted separately; (c) a graded record — unknown word /
   unbound noun / no rule / generic physics fallback — counted separately and reported as a profile
   rather than one number.
   *Recommendation:* (c). One number will be gamed by whoever is trying to make it go down, and the
   four categories have four different owners in the loops.

~~5. asked:~~ **Answered 2026-09-27 (Andrew):** *"perhaps, if my open weight model runs fast enough then yeah we can collect activations while playing with humans"* *The question as it was asked:* **Are runs with people in them research data?** *(Sharpened 2026-09-26 by Claude; the draft is
   kept below as the record.)* The engine does not know which mode it is in, and every run is logged
   the same way (document 19 §4.2), so a mixed run's log exists whatever is decided. The question is
   whether it is *used*, and on what terms for the people in it — Andrew's friends. The research value
   is real: the co-op and moral material (the antenna hold, the shared blanket, the lie about the
   cache) exists only with someone else in the run.
   *Options:* (a) research uses agent-only runs; runs with people are play; (b) runs with people are
   used too, with the humans' presence a recorded run condition and the people told their runs are
   logged and may be studied; (c) as (b), and the people's own behaviour is studied as well, not only
   the agents'.
   *Recommendation:* (b) — it keeps the most interesting half of the design inside the research, and
   telling the friends is both fair and what makes the data usable.

   *The draft (2026-09-16), kept as the record:*
   **Do agents and humans share instances in research runs?** Decided for play (mixed runs exist,
   same rules); undecided for research, where a human in the run is an uncontrolled variable and also
   the most interesting thing in it.
   *Options:* (a) research runs are agent-only, mixed runs are play; (b) mixed research runs are
   allowed and the human is logged as a subject too; (c) mixed, with the human's presence recorded as
   a run-level condition.
   *Recommendation:* (c) — the co-op and moral material (the antenna hold, the shared blanket,
   the lie about the cache) only exists when there is someone else in the room, and excluding humans
   would cut the research off from the most interesting half of the design.

~~6. Does the agent get any briefing beyond the grammar guide?~~ **Claude's answer (2026-09-26), for
   Andrew's check:** exactly what a person gets, and nothing a person does not — the draft's (b). A
   person sees the pre-scenario tutorial (the forms with one example each, the time controls,
   movement, `help` — `PLAN.md` E19) and then the run's opening; the agent gets the same text in the
   same order. Who it is, what it wears and carries and how it is hurt, it learns as a person does —
   `status`, `inventory`, looking at itself (the draw is made at run start, document 16). A character
   sheet (the draft's (c)) would be a second channel, which the same-view rule forbids. The one
   addition already decided is the persona brief of a non-human character (Andrew, 2026-09-17), which
   lives in the model's instructions, never on screen. For research, the instructions are part of the
   run manifest (Q2) and identical across the conditions compared. §4.1 carries this.

   *The draft (2026-09-16), kept as the record:*
   **Does the agent get any briefing beyond the grammar guide?** Decided: the grammar guide, up
   front. Not decided: whether it is told it has just survived a crash, who it is, what the party is
   — things a human would know from the game's own framing before typing anything.
   *Options:* (a) grammar guide only, cold start — it learns the situation by looking;
   (b) grammar guide plus the same framing a human sees on connecting; (c) grammar guide plus a
   character sheet (name, injuries, what is in the pockets).
   *Recommendation:* (b) — whatever a human is shown on connecting is by definition the same view,
   and a cold start measures "can it work out it is in a plane crash", which is not the thing being
   studied. Any extra framing must be identical in both conditions or the comparison is void.

*The agent's pace — Andrew's, and open — is asked once, as document 19 Q4, and answered there for
both documents (the typing pace, a cap, or nothing).*

---

## 7. Review log

*

| date | decided | cut | sent back |
|---|---|---|---|
| — | — | — | — |

---

- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** agents may be scaffolded as **non-human
  characters (NHCs)** with a persona brief — still players from the engine's side, which keeps the engine
  deterministic; agent runs are short sessions like human ones.
- **2026-09-26 (Andrew, ahead of this document's sitting):** *"we want our human agent to run at the same
  speed as humans so basically the speed an average typer could type something minus the additional
  thinking time if it is slower than a human would be, lightweight models are relatively quick compared
  to the length it takes to type commands."* Open for the sitting: in a run with humans the clock cannot
  wait out a slow model (DR-14), so the allowance holds only in agent-only runs (`PLAN.md` §5).
- **2026-09-26 (Andrew, later):** *"not sure we should cap anything, If something is slow they are slow
  there is nothing we can do about it when humans are playing."* In a run with humans the clock does
  not wait for a slow model. Whether anything paces a fast agent stays for this sitting, together with
  document 19 Q4.
- **2026-09-26 (Claude, self-review — PLAN.md A9):** **Answered for Andrew's check:** Q1 (two complete
  streams, ground truth and interpretation, with the exact text each character received and the
  numbers behind the band words; §4.4 extended), Q2 (the pure harness for agent-only runs, the server
  for runs with people; a run manifest; the stopping rule is the game's own — rescued or dead — with a
  step budget only as a harness guard; "walked out" struck), Q4's edges (the question itself was
  Andrew's, 2026-09-18, document 05 §4.5a), Q6 (exactly what a person is shown — the tutorial, then
  the opening — plus the persona brief for a non-human character, never on screen; §4.1 extended).
  **Left for Andrew, sharpened:** Q3 (which model families play, and for what) and Q5 (whether runs
  with his friends in them are research data, and on what terms). The pace question points to
  document 19 Q4. **Stale content marked:** the `Exits:`-line look (→ people, animals and exits as
  prose; groups). **Added:** the decisions since the draft (§2); the lightweight-model brain for the
  animals (§4.3).

- **2026-09-27 (Andrew):** Q3 — a fast model (Haiku or Sonnet, low to medium reasoning) and Andrew's own open-weight model, which needs timing; Q5 — perhaps: if the open-weight model is fast enough, activations are collected in runs with humans. Pace: the speed of typing the command.

- **2026-09-27 (Andrew, via document 14):** the person on the other end of the radio is played by a weak language model, because players will want to talk to them — a third kind of model-played character besides survivors and animals.

- **2026-09-27 (Andrew, via document 14):** the radio voice's model is scaffolded not to help too much — only what a real rescuer would say — and it judges whether the landmarks it is given are good enough to find the party.

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
- **Determinism**: seeded runs and the frozen contracts that replay rests on.

**Designed, not built.** The play harness in both forms (`tools/play.py`, `agent/runner.py`,
`agent/client.py` — none exist). All three brains. The per-step event log and its file. The moral
tagger (`moral.tag(...)`) and the tag fields on ontology rows. The replay tooling. Any notion of a
research run.

**Nothing.** No agent has ever played this world through a harness. The phrasing samples were
collected by giving agents scene text and reading back what they typed — a measurement, not a run.
There is no activation capture of any kind.

**Two corrections owed in the shipped docs and code — flagged here so the review catches them:**

- [`bot-harness.md`](../guides/bot-harness.md) still documents a structured `@OBS` observation line
  as the bot's preferred channel, and [`BACKLOG.md`](../../BACKLOG.md) *Later* still lists "the
  telnet bot harness with the `@OBS` line". Andrew's 2026-09-16 decision removed it (audit §3): an
  agent sees exactly what a human sees. Both should be corrected.
- The numbered disambiguation menu is still live in
  [`game/commands/cmd_act.py`](../../game/commands/cmd_act.py) (`_show_menu`) — listed in audit §5 as
  shipped code carrying removed behaviour. It is on the correction list; until it is gone, an agent
  connecting to this server would sometimes be shown a list, which is the one thing the research
  framing forbids.
