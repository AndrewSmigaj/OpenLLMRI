# 04 — Grammar and feedback

> **Status: reviewed with Andrew 2026-09-18 in part (the forms, `make`, the naming rule); Q1–Q10 at its sitting** Architecture counterpart:
> [`ontology-closure.md`](../architecture/ontology-closure.md) §5 (the tolerance layer and the
> feedback rule) and `implementation-architecture.md` DR-08 / DR-08a / DR-08b / DR-08c. A dedicated
> `docs/architecture/grammar.md` is **pending** — until it exists, §5 plus the DR-08 chain are the
> engine-level reference and this document is the design-level one. Built from:
> `docs/investigation/design/grammar-guide.md` (the primary source), `docs/investigation/design/
> phrasing-corpus.md`, `docs/architecture/ontology-closure.md` §5, `docs/architecture/
> implementation-architecture.md` (DR-08/08a/08b/08c), and `docs/investigation/design/
> 00-provenance-audit.md`.

## 1. Provenance

### Andrew's decisions (his words, dated)

**2026-09-16 — feedback is clarification only, never options:**
- "The agent is not given a set of options to choose."
- "Giving options changes how it thinks, it constrains it to those options."
- "You do not give other options, the only time you ask the user anything is if what object or
  action they can do is ambiguous (two cans in a scene it will ask 'which can do you mean?')."
- "No you do not have numbered nouns."
- "If you give options for like 'pick up can' and then you list all the cans in the reachable area
  it would just give away all the puzzles."
- "Any feedback needs to be clarification based and not giving options, we can have some feedback
  reminding them of the grammar help system (it would have example of each form, pretty simple
  guide, after we finalize all the possible forms)."
- "If the system recognizes they need to use another word then it would clearly understand that
  word."

**2026-09-07:**
- "State the act, not the aim" — his example: `shake thermos`, not "shake the thermos to see if
  there's coffee in it."
- Agents are given the grammar guide up front.

Everything below that isn't one of the lines above — the exact seven shapes and their tokens, the
disambiguation and unknown-word wording, the particle/synonym tolerance tables, the `use`/`make`
handling, the help text, the in-world manual page, and the lens verdicts — is a **proposal
(Claude)**, per `00-provenance-audit.md` §2, unless the audit marks it his.

### Proposals (Claude) that stay

| pass | proposal | why it serves his stated goal |
|---|---|---|
| ontology-closure | forms + derived capabilities; tier-4 physics; the probe corpus as coverage | his "a shard can cut but so can a knife, abstract it"; every attempt resolves |
| grammar-guide | the forms table; the three rules; the in-world manual page | his grammar guide + survival guide |
| phrasing-corpus | agent phrasing samples → synonyms and probes | his "sanity check our wording with agents" |

*(source: `00-provenance-audit.md` §2, filtered to the rows this document covers.)*

### Removed 2026-09-16 (Claude's additions taken back out)

| removed | was in | reason |
|---|---|---|
| the unknown-verb nudge naming 2–4 verbs | grammar-guide §3; closure §5; DR-08b | options; "if it can suggest the word it already knows it" |
| the numbered disambiguation menu | grammar-guide §2; closure §5; DR-08a (code) | "no numbered nouns"; listing gives away hidden things |
| `help verbs` (the verb-family list) | grammar-guide §5; help_entries.py | a list of options; help is the forms only |
| the `make X` recipe reply and the "limited question" | grammar-guide §4; fire §6; plan §4.5 | a hint; the "limited question" was a misreading of a fallback example |
| the `use` echo naming the verb | grammar-guide §4; closure §5 | names a verb the player did not type (decided silent) |
| the verb-list redirect ("you could cut, burn or pry it") | closure §4; DR-09; build-practices §2 | options |
| the DR-09a sibling near-miss hint | closure §4 | a hint |

*(source: `00-provenance-audit.md` §3, filtered to the rows this document covers.)*

## 2. In one paragraph

A player learns a handful of physical-action shapes in the first minutes — `cut the cover off the
seat with the multitool`, `go to the cockpit` — and from then on types one act per line, naming
things the way the room names them. Nearly everything that fits the shapes and is physically
sensible resolves, because resolution runs on materials and forms, not on a list of allowed
commands. When it can't resolve, the game never tells the player what else they could try: an
unknown word gets `I don't understand 'X'` and a pointer to `help grammar`; a thing it can't see
gets told it isn't there; a verb that doesn't fit gets the physics of why; two things that match
get one question — `Which can do you mean?` — and nothing else. The player is never shown a menu,
never shown a list of what's reachable, and never handed a verb they didn't type themselves.

## 3. The design

### 3.1 The forms

*(source: `grammar-guide.md` §1, plus the three added with Andrew on 2026-09-18)*

| shape | example | what the engine gets |
|---|---|---|
| `VERB thing` | `examine the radio` · `break bottle` | `{verb, X}` |
| `VERB thing WITH tool` | `cut the cushion with the shard` | `{verb, X, tool}` |
| `VERB thing RELATION thing [WITH tool]` | `put the branch on the fire` · `tie the paracord to the frame` · `take the wire from the panel` | `{verb, X, relation, Y, tool?}` |
| `VERB thing INTO form [WITH tool]` | `carve the branch into a spindle with the knife` *(shaping — the fire pass)* | `{verb, X, into, form:spindle, tool}` |
| `GO place` | `go to the cockpit` · `go outside` | `{move, to, zone}` |
| `say / whisper / call / shout …` | `shout for help` | speech, by range |
| `VERB thing, then VERB thing` | `take the shard and cut the cover` | two acts in order |
| `VERB exit` *(added 2026-09-18)* | `walk west` · `walk to the birch grove` · `run to the treeline` · `climb up` · `enter the tail` · `turn back` | `{move, exit, mode}` — exits are entities (document 03 §4.1a); the mode sets the time and what it costs |
| `MAKE goal [WITH means (and means)*]` *(added 2026-09-18)* | `make fire` · `make fire with the lighter and the stick` · `make a splint with the branch and the paracord` | a goal, not an act — §3.9 |
| meta *(added 2026-09-18)* | `propose fast forward` · `status` · `help` · `look` · `inventory` | out-of-world commands; they never interrupt an activity |

Everything else is the tolerance layer folding real phrasings onto these: particles (`pick
up`, `cut open`, `put on`), synonyms (`grab`, `find`, `place`), plurals, body parts (`bandage my
arm`), `it`, and the dropping of intent (`… to see if …`). None of it is new grammar — the same
shapes, reached from more directions (§3.7 has the mechanics and the measured numbers).

**This list is the one to finalize before the loops run** (Andrew, 2026-09-18): every room they write
assumes these forms exist. The shaping form (`INTO form`) and the movement, goal and meta forms are
designed here and unbuilt; the new-verb spike (Q1) tells us what adding a verb inside them costs.

The architecture register (`implementation-architecture.md` DR-08) states the same shape as
`VERB X [RELATION Y] [WITH Z]` at "action granularity," pipelined as tokenize → verb-to-synonym
match → slot bind → resolve each noun phrase to a reachable entity → emit
`ActionAttempt{actor, verb, X, relation, Y, tool, raw}`. **The RELATION slot is what makes
two-object actions first-class** (`cut … off …`, `wedge … against …`, `tie … between …`), not
single-target-only commands.

### 3.2 The three rules the guide states out loud

*(source: `grammar-guide.md` §2, reproduced)*

1. **State the act, not the aim.** `shake thermos`, not `shake the thermos to see if there's
   coffee in it`. The world answers physically either way; it never needs to know why.
2. **Name things the way the room names them.** `examine <thing>` shows what you can name,
   including its parts (`cut the seat's cover`). Two of a kind? The game asks `Which seat do you
   mean?` — nothing more — and you say it more exactly (`the wrenched seat`, `1b`, `the can in the
   bag`). Identical things (three shards) never ask.
3. **Tools are anything with the capability.** `with` names the tool; bare hands are the default.
   Anything with an edge cuts; anything rigid and long levers; anything long and flexible ties.

### 3.3 How it says no — clarification only, never options

*(source: `grammar-guide.md` §3, reproduced, cross-checked against `ontology-closure.md` §5 and
DR-08c)*

| failure | the game says | what the player does next |
|---|---|---|
| unknown word | `I don't understand 'chop'.` (+ once: `'help grammar' shows the forms.`) — never a suggested verb: if the game could suggest the word it already knows it, so the synonym table absorbs it and the line just works; every unknown word is logged so the next pass adds the synonym | rephrases, or reads the grammar help |
| a thing it can't see | `You don't see any 'X' here.` — never naming what IS here (+ the place is named if visible but far: `…too far away to cut from here`) | examine / search / open / move closer |
| a verb that doesn't fit the thing | the physics: `The blade finds no seam — the bolt is bolted through the frame.` · `The foam gives; there is nothing to break.` *(tier-4)* — never names another verb | tries what the physics implies |
| two things match | `Which can do you mean?` — no numbered list, no candidates named (listing the reachable cans would give away every hidden one) | names it more exactly |

Every reply is a clarification or the physics. The game never proposes an action, never lists what
is here, never names a verb the player did not type. For a person that keeps the puzzles; for an
agent it keeps the behaviour the agent's own — offering options changes how it thinks (Andrew,
2026-09-16).

`ontology-closure.md` §5 adds one mechanism this table doesn't show: **silent disambiguation
first** — held beats reachable beats recent, and the more specific candidate wins — so a menu (in
this design, a bare question, never a numbered one) is a last resort, not the common case.
DR-08c's own wording of the same rule: it "supersedes DR-08b's 'three failure kinds', DR-08a's
numbered disambiguation menu, the DR-09 verb-list redirect ('you could cut, burn or pry it') and
the DR-09a sibling near-miss hint." Why, in the register's words: "listing gives away the puzzles,
and for an LLM agent offering options changes how it thinks (Andrew's LLM-MRI finding)."

### 3.4 `use` and `make` (tolerance, not teaching)

*(source: `grammar-guide.md` §4, reproduced)*

- `use X on Y` — a phrasing people really type; it dispatches through X's capabilities to the real
  operation and resolves **silently** as that operation, narrated like any cut or tie (Andrew,
  2026-09-16: no verb is named back). `use X` alone → `Use it how, and on what?` — a clarification,
  never what X could do.
- `make X` — an aim, not an act, and the one verb that bridges from an aim to an act. Vague, it asks
  how; given the means, it performs the act they imply. The whole rule is §3.9.

### 3.9 `make` — the one aim-verb, and how it dispatches (Andrew, 2026-09-18)

**"State the act, not the aim" (§3.2 rule 1) holds for every verb but this one.** `make` exists
precisely to catch an aim and turn it into an act. It behaves in exactly two ways.

**Vague — no means named.** A clarification, nothing else:

```
> make fire
Request too vague. How are you going to make the fire?
```

*(Andrew's own wording, 2026-09-18. Proposal for the voice, his to take or leave: "How do you mean to
make a fire?" — the same question, in the world's register rather than the system's.)* No recipe, no
list of what a fire needs, no naming of what is in reach. What a fire wants is knowledge, and
knowledge lives in the world: the survival manual's fire page says it, findable, readable, burnable.

**Means named — it performs the act they imply.** The goal's roles are filled from what each named
thing can do, and the real operation runs:

```
> make fire with the lighter and the stick
You hold the flame to the deadfall branch. The bark blackens and smokes, but a
wrist-thick branch won't catch from a flame this small. Something finer would.
```

That failure is not authored for `make`. It is the ignition model answering (document 07), reached
through the same pipeline as `light stick with lighter` typed directly.

**The mechanism (proposal).** A parse-time rewrite, exactly like the `use X to VERB Y` rewrite that
already ships: `make <goal> with A and B` binds A and B to the goal's roles by capability and emits
the ordinary `ActionAttempt` for the operation those roles imply. There is no second resolution
path — the locked one-pipeline rule (DR-09) is untouched, and `make` is the twin of `use`: `use`
dispatches by capability, `make` by goal plus capability, and both resolve **silently** as the real
operation (no verb is named back — Andrew, 2026-09-16).

**The goal table.** One row per goal, authored as content and grown by the loops the way objects
are, from what people and agents actually type:

| field | what it holds |
|---|---|
| `goal` | the noun and its synonyms (`fire`, `a fire`, `flame`) |
| `vague` | the clarification line for the bare `make <goal>` |
| `roles` | what the goal needs, as capabilities — fire: an ignition source (`flame`, `spark`, `ember`, `focus`) and a receptive fuel (`burnability > 0`) |
| `realize` | the operation a filled set of roles implies — fire: `light <fuel> with <ignition>` |

**The rows live in the system that owns the goal**, not here: fire in document 07, water in 09,
shelter in 08, the signal in 14. This document owns the form and the dispatch rule only.

**The honest edges.**
- **Means that fill no role**: the physics of the things themselves. `make fire with a rock and a
  sock` → the wool frays, nothing more. Never "you need an ignition source".
- **Roles half-filled**: the physics of what will not happen. `make fire with the branch and the
  grass` → neither will light the other. Never a shopping list.
- **Goals that are genuinely multi-step** (a bow-drill fire, a shelter): the dispatch performs the
  *first* act the means imply and the world answers it. `make fire with sticks` rubs the sticks
  together and they scuff and warm, nothing more. `make` never runs a procedure.
- **It is not an oracle.** Probing `make fire with X` tells you only what X physically does, which
  `examine` already signals. It costs time on the clock like any attempt.

### 3.10 Naming things apart — an authoring requirement, not a grammar one (Andrew, 2026-09-18)

Removing the numbered menu (DR-08c) puts a duty on the content. When two things a player can
plausibly confuse are in reach, the game asks `Which seat do you mean?` and nothing more — so the
player must have some word that separates them. Every pair of confusable things therefore needs
**distinguishable names or adjectives in its authored prose**: the *wrenched* seat and the *thrown*
seat, seat *1a* and seat *1b*, the *forward* bin and the *aft* bin. Identical things (three glass
shards) never ask, because it does not matter which one you take.

This is a rule the world-building loops must follow (document 17, document 22): a room that can ask
an unanswerable question is a bug in the room, and `make validate` should be able to catch it.

### 3.5 `help grammar` — the forms, one example each (there is no verb list)

*(source: `grammar-guide.md` §5, reproduced)*

The only help is the grammar: each form from §3.1 with one example, and the three rules of §3.2.
Simple. It is written once the forms are final (the shaping form and any the loops discover) and
rewritten when they change. There is no `help verbs`: vocabulary is learned by trying, and the
synonym table absorbs how people say things.

### 3.6 The in-world page (diegetic)

*(source: `grammar-guide.md` §6, reproduced)*

The survival manual's first page, found in the kit, reads the same rules as fiction: *"Say what
you do, not what you hope. Name things by what they are. Anything sharp cuts; anything long and
strong ties; anything that burns will burn better small and dry."* Hadean Lands teaches its whole
command syntax through an in-world notebook; ours does the same, so the fourth wall stays intact
for players who never type `help`.

### 3.7 How the vocabulary grows

**The mechanical tolerance layer** (`ontology-closure.md` §5; DR-08b in the architecture register).
Measured 2026-09-07 with the real parser against the real world's nouns: taught-condition agent
phrasings parsed 32–58%; six mechanical fixes lift that to 76–79% in simulation; the residue is a
short list of new verbs and scenery nouns owned by later steps. None of the six is free-text NLP —
all of it is inside the taught grammar:

1. **Particles, resolved positionally** (TADS 3's rule): a word right after the verb with no noun
   following is a verb-sense particle (`cut open`, `take out`, `put on`); the same word followed
   by a noun is the RELATION slot (`cut off the strap`).
2. **Multi-word relations** as greedy token sequences (`out of`, `on top of`) and the missing
   single ones (`over`, `onto`, `through`, `across`, `inside`, `behind`, `beside`).
3. **A synonym table** seeded from the sampled phrasings (find→search, check→examine, place/add→
   put, gather/collect/retrieve→take, secure→tie, heat→melt, shoot/fire→light, …).
4. **State the act, not the aim.** The game never needs intent: `shake thermos`, not `shake
   thermos to see if coffee is in there`. Trailing purpose clauses and adverbs are trimmed;
   meta-verbs (`try to`, `see if`) are stripped; `and` compounds become two commands.
5. **Body parts and pronouns**: `my arm` / `myself` → the actor; `it` → the last bound noun
   (ephemeral per-caller shell state, like a pending clarification).
6. **Noun binding**: whole-phrase entity match *before* the possessive `of` split (`canteen of
   water`), then longest-known-noun matching so trailing words don't poison the phrase.

**The measured numbers** (`phrasing-corpus.md`, measured 2026-09-07, real parser, real nouns — two
agents, Sonnet 5 and Haiku, seven survival tasks, naive (A) and taught (B) conditions, 294 lines →
`game/world/scenarios/whiteout/probes/phrasing.py`):

| | before (2026-09-07 morning) | after the tolerance layer |
|---|---|---|
| Sonnet 5, taught (B) | 58% | **83%** |
| Sonnet 5, naive (A) | 37% | 78% |
| Haiku, taught (B) | 32% | **79%** |
| Haiku, naive (A) | 23% | 71% |
| census candidate commands | 58% | 73% *(census probes: 26/89 pass)* |

Preposition tally (Sonnet): with 29 · on 24 · to 16 · in 14 · into 10 · from 10 · around 7 · off 7
· over 5 · against 5. Particles seen: put on, blow on, set off, turn on, pick up, scoop up, roll
up, tie off, take out, snap off, zip up.

**What the residue is** (the 17–21% that still fails, taught condition):

| category | examples | owner |
|---|---|---|
| verbs that don't exist yet | turn/switch/adjust (toggles), press, spin, wave, fix, carve/whittle (shaping), sit/huddle/rest, dry, block/shield/cover-an-opening, clear, stuff | steps 4–5 (verb gaps), the fire pass (shaping) |
| nouns that don't exist yet | the flame / the fire (no fire entity), the hull tear / the breach, the notch, sticks / twigs / bark (no such objects; only "deadfall branch"), a pulse, "the plane" | the fire pass (fire entity), scenery nouns (step 5), living rooms (more objects) |
| lines that aren't acts | "see if I can tell where we crashed", "keep the cover as a second layer", "let the water cool", "check if bleeding has stopped" | leave: not commands; the guide says state the act |
| junk tokens | "there's", "if no ember, …" (now handled), gerunds (now handled) | done |

Nothing in the residue is a grammar shape. The grammar is sufficient; the vocabulary and the world
are what grow.

**What the samples taught us** (rules adopted):
1. Agents type **particles** constantly (`put on`, `take out`, `pick up`) → positional particle
   table.
2. Agents narrate **intent** in the naive condition and mostly stop in the taught one → trim it,
   and put "state the act" in the guide.
3. **`use X on/to`** is the first thing an untaught agent tries → the teaching verb that resolves
   through capabilities.
4. **Synonym drift is bounded**: after the table, unknown verbs are real missing verbs, not
   phrasing.
5. Nouns fail more than verbs: **plurals, adjectives, head nouns** (`the quilted engine cover`),
   **possessives that aren't parts** (`the pilot's jacket`) → all four handled in the binder.
6. The taught condition converges across models (79 vs 83); the naive gap is larger (71 vs 78) —
   another reason the guide goes to agents up front.

**How an unknown word turns into vocabulary.** This is decided, not open: "every unknown word is
logged to the wall-sensor so the next pass adds the synonym" (DR-08c). Nothing auto-learns at
runtime — DR-02 holds, there is no runtime language model to do the learning — the log is a
build-time authoring queue read by the next design/implementation pass, the same mechanism that
already logs unhandled verb×thing attempts (`ontology-closure.md` §4/§6, the wall-sensor and the
probe corpus). §5 below has the one open point this leaves: today only the verb×thing gap is
logged; the unknown-*word* log is designed but not yet wired (see §7).

### 3.8 Lens pass

*(source: `grammar-guide.md` §7, reproduced)*

**Skill (GD — "what skills does this game require?").** Verdict: GREEN. Evidence: the skill is
*understanding the world*, not guessing syntax: a fixed set of shapes, all shown up front, with the
tolerance layer absorbing the rest (measured 79–83% taught). Severity: —. Note: the remaining
friction is vocabulary (new verbs, scenery nouns), which the discovery loop drains; the guide never
has to grow.

**Information (GD — "is the right information visible at the right moment?").** Verdict: YELLOW.
Evidence: the right information is the physics of why, and the tier-4 physics message is not built
yet, so today a verb that doesn't fit falls to a verb-list redirect — which is now forbidden.
Severity: med. What would change it: tier-4 + the clarification-only code change (BACKLOG,
DR-08c).

**Simplicity / Complexity (GD — "is the complexity in the world, not the interface?").** Verdict:
GREEN. Evidence: interface complexity is fixed (a short list of shapes); world complexity is unbounded
(materials × forms × operations). Note: resist adding shapes; add nouns and verbs.

**The Toy (GD — is it fun to poke without a goal?).** Verdict: YELLOW until tier-4. Evidence:
poking is rewarded only when the answer is the physics of the thing; today's verb-list redirect is
a wall with a smile, and a menu would be worse.

## 4. Interactions

**Depends on:**
- The forms and derived-capability model (`ontology-closure.md` §2–3) — what "a verb that doesn't
  fit" or "tools are anything with the capability" cashes out to.
- Tier-4 generic physics (`ontology-closure.md` §4) for the "verb that doesn't fit" reply — not yet
  built (§7).
- The operation×material resolver (DR-09, `implementation-architecture.md`) that a bound
  `ActionAttempt` is handed to.
- Whatever `examine` shows for a thing's nameable parts — the player-view document (`03-the-player-
  view.md` / `presentation.md`, pending) governs what naming-them-the-way-the-room-does actually
  displays.

**Depended on by:**
- Every survival system's verbs type through this grammar — fire and shaping, water, food, injury,
  the moral/social layer (docs 07, 09–11, 15) all express their acts as one of the seven shapes.
- The agent-player document (`20-the-agent-player-and-research.md`): agents are given the grammar
  guide up front (Andrew, 2026-09-07) — this document is that guide's design source.
- The world-building loops (`22-the-world-building-loops.md`): the wall-sensor's logged gaps and
  the phrasing corpus are two of the four sources that feed the overnight authoring loop (the other
  two are the room censuses and the rescue graph — `ontology-closure.md` §6).
- The growing-sets framing itself (`05-ontology-and-sufficiency.md`): the vocabulary — verbs, nouns,
  forms — is one of the growing sets that document frames; this document is where its parser-level
  mechanics live.

## 5. Open questions

1. **Does the grammar need expanding for the planned actions?**
   - *Options:* (a) assume the current seven shapes cover everything the roadmap's later systems
     need until proven otherwise; (b) pre-emptively add shapes for verbs already known to be coming
     (fire's shaping family already added `VERB X INTO form`).
   - *Recommendation:* neither, here. The "is it easy to add a verb?" spike is a task on the
     roadmap/BACKLOG, not a question this design document answers — it's evidence, not opinion. Note
     the question; let the spike answer it.

2. **What is the finalized forms list?**
   - *Options:* (a) freeze the current seven shapes now and write `help grammar` and the in-world
     manual page against them; (b) wait until the shaping pass and the verb-gap steps (4–5) land,
     since Andrew's own rule is that the help is written "after we finalize all the possible forms."
   - *Recommendation:* (b). The source is explicit that the help text waits for the forms to be
     final; finalizing early risks rewriting player-facing text twice.

3. **Does `use X on Y` stay at all?**
   - *Options:* (a) keep it as a permanent tolerance path that resolves silently through
     capabilities (current design); (b) drop it once enough synonyms exist that players/agents
     reach for the real verb directly, since it's redundant with "state the act."
   - *Recommendation:* (a), keep it. The phrasing corpus found `use X on/to` is "the first thing an
     untaught agent tries" — dropping it would break the most common naive phrasing rather than
     teach past it; the silent resolution (no verb echoed back) already satisfies "never a menu."

4. **What does the in-world manual page actually say?**
   - *Options:* (a) treat the §3.6 line ("Say what you do, not what you hope...") as final flavor
     text now; (b) treat it as a draft, to be finalized alongside `help grammar` once the forms list
     is locked (question 2).
   - *Recommendation:* (b), for the same reason as question 2 — the two texts teach the same rules
     and should be finalized together, once, not twice.

5. **How exactly do unknown words reach the synonym table?**
   - *Decided:* the wall-sensor logs them (DR-08c) — this part isn't open.
   - *What's open is the mechanism:* (a) unknown-verb parse failures write into the same
     `gaps.jsonl` file and record shape the verb×thing wall-sensor already uses
     (`wall_sensor.gap_record`); (b) a separate log/schema, since an unknown verb parses to no
     `ActionAttempt` at all (no `X`, no `relation`) — the existing record shape assumes one.
   - *Recommendation:* (a) with a minimal record for this case (`raw`, the unrecognized word,
     `actor`, `zone`, `at`) — one authoring queue is easier for the overnight loop to read than two,
     and the existing file is already the established convention (§7 below: this isn't built yet
     either way).

6. **Counts: do they mean anything?** Today `take two branches` takes one branch and says nothing
   about the two; `take all` answers "You don't see that here". A quantifier that is silently
   dropped teaches the player the wrong thing.
   - *Options:* (a) counts work, bounded by what is there and by what you can carry — "you take two
     of the three branches"; (b) counts are refused honestly — "one at a time"; (c) leave as is.
   - *Recommendation:* (a). It needs the class-yields-individuals primitive (`PLAN.md` E16) for
     classes like deadfall and snow, which the outdoor zones need anyway.

7. **`all`: in, and scoped to what?**
   - *Options:* (a) scoped only — `take all from the duffel`, `take all the branches` — never a bare
     `take all` over the room; (b) bare `take all` scoops everything loose in reach; (c) no `all`.
   - *Recommendation:* (a). A bare room-wide `take all` is both unphysical (you cannot carry a
     room) and a discovery shortcut: it would reveal what is takeable by taking it, which is the
     never-list rule leaking out through a convenience.

8. **The `make` clarification's wording.** Andrew's line is "Request too vague. How are you going to
   make the fire?"
   - *Options:* (a) his wording as written; (b) the same question in the world's register — "How do
     you mean to make a fire?"
   - *Recommendation:* (b), but it is his line and his call.

9. **Which goals get rows first?**
   - *Options:* (a) fire, water, shelter, a signal, a splint — the five a party reaches for on day
     one; (b) fire only, and grow the rest from what agents type; (c) a larger set up front.
   - *Recommendation:* (a), with the rows written in the owning documents (07, 09, 08, 14, 11) and
     grown by the loops afterwards.

10. **Is the distinguishable-names rule (§3.10) enforced, or just written down?**
   - *Options:* (a) `make validate` fails when two reachable things in a zone share a name with no
     distinguishing adjective; (b) an authoring rule in the guide only.
   - *Recommendation:* (a). It is mechanically checkable, and the alternative is a room that can
     ask a question the player cannot answer.

## 6. Review log

Not yet reviewed with Andrew. This is the first draft: a straight merge of `grammar-guide.md`,
`phrasing-corpus.md`, `ontology-closure.md` §5, and the DR-08/08a/08b/08c paragraphs of
`implementation-architecture.md` into the template, re-labelled for provenance per
`00-provenance-audit.md`. No content was changed in the merge beyond reorganizing it under the
eight parts; nothing new was added to the design itself.

- **2026-09-18 (Andrew, block 1):** **`make` becomes the one aim-verb that bridges to an act** — vague, it
  asks how ("Request too vague. How are you going to make the fire?"); given the means, it performs
  the act they imply and the world answers physically ("you light the stick but it won't catch").
  The recipe reply that ships today is cut; what a fire wants belongs in the survival manual. The
  goal table is a hint corpus brainstormed now and grown from what agents type. The form list is
  finalized **before** the loops run; the movement, goal and meta forms are added (§3.1). §3.9 and
  §3.10 written; §3.4 now points at §3.9. New questions Q6–Q10 (counts, `all`, the wording, which
  goals first, enforcing distinguishable names).

## 7. What exists today

**Built, but shipping the pre-2026-09-16 behaviour** (the BACKLOG "Next" item under DR-08c has not
landed — checked directly against the code, 2026-09-16):

- `game/world/sim/parser/grammar.py` — the parser itself (tokenize → verb/synonym match → slot
  bind → resolve to reachable entities) is built and is the DR-08 pipeline. But `_NUDGE` and
  `_unknown_verb_nudge` (naming 2–4 close verbs, "Did you mean X or Y?") are still the DR-08b nudge,
  not DR-08c's `I don't understand 'X'.`
- `game/world/sim/parser/vocab.py` — the tolerance layer itself (§3.7's six fixes) **is** built and
  live: `SYNONYMS`, `PARTICLES`, `MULTIWORD_RELATIONS`, `META_PREFIXES`, `PURPOSE_CUTS`,
  `TRAIL_ADVERBS`, `TRAIL_PARTICLES`, `BODY_NOUNS`, `PRONOUNS` (170 lines) — this is what produced
  the "after" column in §3.7's numbers table. `VERB_FAMILIES` (the same file) still exists to feed
  the old unknown-verb nudge above and should go with it.
- `game/world/sim/resolver/redirect.py` — `generic_redirect` still says "you can't X the Y like
  that — but you could cut, burn or pry it" (the DR-09 verb-list redirect); tier-4 physics-from-
  properties (§3.7 note above; `ontology-closure.md` §4) has not replaced it yet.
- `game/commands/cmd_act.py` and `game/commands/cmd_items.py` — both still show a **numbered**
  disambiguation menu (`Which X do you mean?` followed by a printed `1. / 2. / …` list and "type a
  number to choose"), the DR-08a mechanism; not yet the bare question with nothing else.
- `game/world/help_entries.py` — `help grammar` is close in shape (the forms + one example each)
  but still says `'use X on Y' works — the game tells you which verb it did` (should be silent) and
  still carries a `help verbs` entry (the verb-family list) that DR-08c says to delete.
- `game/world/sim/operations/handlers/use.py` — resolves through capabilities correctly, but still
  **echoes** the verb it picked (`"(That's 'cut cover with shard'.)"`); the 2026-09-16 decision is
  silent resolution.
- `game/world/sim/operations/handlers/make_op.py` — answers with what the thing is made of, but
  still supports a tool-named "limited question" reply, which the audit says was a misreading and
  should be a plain clarification instead.
- `game/world/sim/operations/_helpers.py`'s `sibling_hint()` (used by `handlers/cut.py`, `pry.py`,
  `tear.py`) — the DR-09a near-miss hint; still present in three handlers.
- `game/world/sim/testing/probes.py` — a disambiguation mid-chain still defaults to "the first
  option" (its own docstring: "default the first"); the BACKLOG item calls for probe steps to name
  nouns unambiguously instead, removing the need for a default.
- The wall-sensor (`game/world/sim/resolver/wall_sensor.py` + `cmd_act.py`'s `_log_gap`) logs
  resolved-but-unhandled verb×thing attempts (tier-5 generic redirects) to
  `server/logs/gaps.jsonl`. It does **not** yet log unknown-verb parse failures — so "every unknown
  word is logged" (§3.7, §5 question 5) is decided and designed, not yet built.

**Designed, not built:**
- The DR-08c clarification-only rewrite as a whole — scoped concretely in `BACKLOG.md` under
  "Next" (remove the nudge and the verb-list redirect, replace both numbered menus with the bare
  question, delete `help verbs`, silence `use`/`make`, drop the DR-09a hint, stop defaulting probe
  disambiguation, wire the unknown-word log).
- `docs/architecture/grammar.md` — referenced as the architecture counterpart in
  `docs/design/README.md`'s table, not yet written; `ontology-closure.md` §5 stands in for it.

**Measured (not code, but a real artifact):**
- `game/world/scenarios/whiteout/probes/phrasing.py` — the phrasing corpus's agent-typed lines as
  probes (`expect: "PARSED"`), 302 lines including a small number marked `status: "todo"`; this is
  the artifact §3.7's numbers were measured against.
