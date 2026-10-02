# 04 — Grammar and feedback

> **Status: reviewed with Andrew 2026-09-18 — every question answered; finalized at the close.**
> Architecture counterpart: [`ontology-closure.md`](../architecture/ontology-closure.md) §5 (the
> tolerance layer and the feedback rule) and `implementation-architecture.md` DR-08 / DR-08a /
> DR-08b / DR-08c. A dedicated `docs/architecture/grammar.md` is **pending** — until it exists, §5
> plus the DR-08 chain are the engine-level reference and this document is the design-level one.

## 1. Decisions

### Andrew's decisions

- **Feedback is clarification only, never options (2026-09-16).** The player — person or agent — is
  never given a set of options to choose from: options change how an agent thinks and constrain it
  to those options, and listing, say, every can in reach would give away the puzzles. The only time
  the game asks anything is when the thing or the act is ambiguous — two cans in a scene, and it asks
  `Which can do you mean?`. There are no numbered nouns. Feedback may remind the player of the
  grammar help: an example of each form, a simple guide, written once the forms are finalized.
- **No suggested words (2026-09-16).** If the system could tell a player which word to use, it
  already knows that word — so it understands it instead.
- **`use X on Y` resolves silently (2026-09-16)** — no verb is named back.
- **State the act, not the aim (2026-09-07)** — `shake thermos`, not "shake the thermos to see if
  there's coffee in it". **Agents are given the grammar guide up front** (2026-09-07).
- **`make` is the one aim-verb (2026-09-18).** Vague, it asks how; given the means, it performs the
  act they imply and the world answers physically. The recipe reply is not in the design; what a
  fire wants is learned in the world — the tutorial rooms and the physics of a failure. The goal table is brainstormed now and grown from what
  people and agents type; the first rows are fire, water, shelter, a signal and a splint (§3.9).
- **The forms are finalized before the loops run (2026-09-18)**, with the movement, goal, quantity
  and meta forms added (§3.1). Whether the grammar needs more is answered by the new-verb spike, not
  in advance. `help grammar` is written once, when the forms
  are final.
- **`use X on Y` stays (2026-09-18)**, silent.
- **Every line is in the world's voice (2026-09-18)** — "How do you mean to make a fire?", here and
  in every other line the game speaks.
- **Vocabulary is written word-first (2026-09-18)** — the canonical word, then its synonyms in the
  same pass, before the loops run; the gaps log is the backstop (§3.7).
- **Quantities are budgets (2026-09-18)** — counts and measures (a handful, some, all); `all` is
  scoped; a gathered quantity is one aggregate; inventory is limited by weight and space, and bulk
  comes from density (§3.11).
- **Distinguishable names are enforced (2026-09-18)** by `make validate` (§3.10).
- **Common sense is hinted (2026-09-27).** When a player misses something any person would know —
  holding the radio's button while talking — the world says why, in its own voice: a reason, never a
  list of options (§3.3).
- **(2026-09-28)** **Hints are added case by case.** Where something is very unobvious, or players struggle to understand what to do, a hint in the world's voice goes in when they try it. What needs one is found after agents have played a lot: other language models analyse their playthroughs, and the agent players answer a brief questionnaire — part of fleshing out and balancing the world (documents 20, 22). Examining a thing never names its uses. A character's knowledge, on the hidden skill sheet, also shows as
  subtle cues in what they notice — never a "do this" hint (document 16 §4.1, 2026-10-02).
- **(2026-09-27)** Every thing is named by its most common name; its technical and other names are its
  synonyms.
- **(2026-09-27)** Taking something unseen is its own verb: `steal`, or another fitting word; every other
  act is emoted to everyone in the zone (document 15 rule 5).

### Proposals (Claude)

- The exact shapes and their tokens (§3.1), the three rules as worded (§3.2), the disambiguation and
  unknown-word wording (§3.3), the particle and synonym tolerance tables (§3.7), the help text
  (§3.5), and the lens verdicts (§3.8).
- The forms-and-derived-capabilities model and tier-4 physics
  ([`ontology-closure.md`](../architecture/ontology-closure.md)) — the abstraction under "anything
  with an edge cuts" (a shard can cut, and so can a knife).
- Sampling agent phrasings to check the wording (§3.7).
- `make`'s parse-time mechanism and the goal table's fields (§3.9).

## 2. In one paragraph

A player learns a handful of physical-action shapes in the first minutes — `cut the cover off the
seat with the multitool`, `go to the cockpit` — and from then on types one act per line, naming
things the way the room names them. Nearly everything that fits the shapes and is physically
sensible resolves, because resolution runs on materials and forms, not on a list of allowed
commands. When it can't resolve, the game never tells the player what else they could try: an
unknown word gets `I don't understand 'X'` and a pointer to `help grammar`; a thing it can't see
gets told it isn't there; a verb that doesn't fit gets the physics of why; two things that match
get one question — `Which can do you mean?` — and nothing else; a player who misses something any
person would know is told why, in the world's voice. The player is never shown a menu, never shown
a list of what's reachable, and never handed a verb they didn't type themselves.

## 3. The design

### 3.1 The forms

| shape | example | what the engine gets |
|---|---|---|
| `VERB thing` | `examine the radio` · `break bottle` | `{verb, X}` |
| `VERB thing WITH tool` | `cut the cushion with the shard` | `{verb, X, tool}` |
| `VERB thing RELATION thing [WITH tool]` | `put the branch on the fire` · `tie the paracord to the frame` · `take the wire from the panel` | `{verb, X, relation, Y, tool?}` |
| `VERB thing INTO form [WITH tool]` | `carve the branch into a spindle with the knife` *(shaping — document 07)* | `{verb, X, into, form:spindle, tool}` |
| `GO place` | `go to the cockpit` · `go outside` | `{move, to, zone}` |
| `say / whisper / call / shout …` | `shout for help` | speech, by range |
| `VERB thing, then VERB thing` | `take the shard and cut the cover` | two acts in order |
| `VERB exit` | `walk west` · `walk to the birch grove` · `run to the treeline` · `climb up` · `enter the tail` · `turn back` | `{move, exit, mode}` — exits are entities (document 03 §4.1a); the mode sets the time and what it costs |
| `MAKE goal [WITH means (and means)*]` | `make fire` · `make fire with the lighter and the stick` · `make a splint with the branch and the paracord` | a goal, not an act — §3.9 |
| `VERB <quantity> of X` | `take two rocks` · `grab a handful of rocks` · `pick up some branches` · `take all the bark from the birch` · `carry as much wood as I can` | a quantity is a **budget**, not a number — §3.11 |
| meta | `propose fast forward` · `status` · `help` · `look` · `inventory` | out-of-world commands; they never interrupt an activity |

The movement, goal, quantity and meta forms were added with Andrew on 2026-09-18.

Everything else is the tolerance layer folding real phrasings onto these: particles (`pick
up`, `cut open`, `put on`), synonyms (`grab`, `find`, `place`), plurals, body parts (`bandage my
arm`), `it`, and the dropping of intent (`… to see if …`). None of it is new grammar — the same
shapes, reached from more directions (§3.7 has the mechanics and the measured numbers).

**This list is finalized before the loops run** (Andrew, 2026-09-18): every room they write
assumes these forms exist. The shaping form (`INTO form`) and the movement, goal and meta forms are
designed here and unbuilt. The grammar is not expanded in advance for verbs that are coming; the
new-verb spike (a task, not a design question) tells us what adding a verb inside these forms costs.

The architecture register (`implementation-architecture.md` DR-08) states the same shape as
`VERB X [RELATION Y] [WITH Z]` at "action granularity," pipelined as tokenize → verb-to-synonym
match → slot bind → resolve each noun phrase to a reachable entity → emit
`ActionAttempt{actor, verb, X, relation, Y, tool, raw}`. **The RELATION slot is what makes
two-object actions first-class** (`cut … off …`, `wedge … against …`, `tie … between …`), not
single-target-only commands.

### 3.2 The three rules the guide states out loud

1. **State the act, not the aim.** `shake thermos`, not `shake the thermos to see if there's
   coffee in it`. The world answers physically either way; it never needs to know why. (`make` is
   the one exception — §3.9.)
2. **Name things the way the room names them.** `examine <thing>` shows what you can name,
   including its parts (`cut the seat's cover`). Two of a kind? The game asks `Which seat do you
   mean?` — nothing more — and you say it more exactly (`the wrenched seat`, `1b`, `the can in the
   bag`). Identical things (three shards) never ask.
3. **Tools are anything with the capability.** `with` names the tool; bare hands are the default.
   Anything with an edge cuts; anything rigid and long levers; anything long and flexible ties.

### 3.3 How it says no — clarification only, never options

| failure | the game says | what the player does next |
|---|---|---|
| unknown word | `I don't understand 'chop'.` (+ once: `'help grammar' shows the forms.`) — never a suggested verb: if the game could suggest the word it already knows it, so the synonym table absorbs it and the line just works; every unknown word is logged so the next pass adds the synonym | rephrases, or reads the grammar help |
| a thing it can't see | `You don't see any 'X' here.` — never naming what IS here (+ the place is named if visible but far: `…too far away to cut from here`) | examine / search / open / move closer |
| a verb that doesn't fit the thing | the physics: `The blade finds no seam — the bolt is bolted through the frame.` · `The foam gives; there is nothing to break.` *(tier-4)* — never names another verb | tries what the physics implies |
| two things match | `Which can do you mean?` — no numbered list, no candidates named (listing the reachable cans would give away every hidden one) | names it more exactly |
| an act that misses what any person would know | the world's reason, in its voice: `You talk into the mic, but the radio stays quiet while the button is up.` | does what a person would |

Every reply is a clarification or the physics. The game never proposes an action, never lists what
is here, never names a verb the player did not type. For a person that keeps the puzzles; for an
agent it keeps the behaviour the agent's own — offering options changes how it thinks (Andrew,
2026-09-16).

**Common sense is hinted (Andrew, 2026-09-27).** Players are not left to work out things any person
would know. When a player misses one — talking into the radio without holding its button — the world
says why, in its own voice. The hint is a reason, never a list of options, and it never names a verb
the player did not type.

`ontology-closure.md` §5 adds one mechanism this table doesn't show: **silent disambiguation
first** — held beats reachable beats recent, and the more specific candidate wins — so the bare
question is a last resort, not the common case. The architecture register records the rule as
DR-08c, which retires DR-08b's three failure kinds, DR-08a's numbered disambiguation menu, the DR-09
verb-list redirect and the DR-09a sibling near-miss hint.

**Not in the design (2026-09-16):** a suggested verb for an unknown word · a numbered disambiguation
menu · `help verbs` (a verb list) · a recipe in reply to `make` · `use` naming the verb it chose · a
redirect naming other verbs that would work · a near-miss hint naming a sibling verb.

### 3.4 `use` and `make` (tolerance, not teaching)

- `use X on Y` — a phrasing people really type (the phrasing corpus found it is the first thing an
  untaught agent tries); it dispatches through X's capabilities to the real operation and resolves
  **silently** as that operation, narrated like any cut or tie (Andrew, 2026-09-16: no verb is named
  back). It stays in the design (2026-09-18). `use X` alone → `Use it how, and on what?` — a
  clarification, never what X could do.
- `make X` — an aim, not an act, and the one verb that bridges from an aim to an act. Vague, it asks
  how; given the means, it performs the act they imply. The whole rule is §3.9.

### 3.5 `help grammar` — the forms, one example each (there is no verb list)

The only help is the grammar: each form from §3.1 with one example, and the three rules of §3.2.
Simple. It is written once the forms are final and rewritten when they change (Andrew, 2026-09-18).
There is no `help verbs`: vocabulary is learned by trying, and the synonym table absorbs how people
say things.

### 3.6 Teaching the grammar

There is no survival manual or other in-world page in the world (2026-10-02). The grammar is taught by
the tutorial rooms, each one simple situation that shows what sort of things players can do
(2026-09-27), and by `help grammar`; an attempt that fails says why, in the world's voice (§3.3).

### 3.7 How the vocabulary grows

**How vocabulary is built — word first, then its synonyms (Andrew, 2026-09-18).** The synonym table
is not harvested, it is **authored**, and it is cheap: start with the word, then flesh out its
synonyms, before the world-building passes. So the rule is —

1. **A word is chosen when the thing or the act is designed**: one canonical verb, one canonical
   noun. That is the word the world uses in its own prose.
2. **Its synonyms are authored in the same pass**, immediately, because writing out the ten ways a
   person says *cut* costs minutes and guessing later costs a player their sentence. A verb or a
   noun is not finished until its synonym set is written.
3. **This happens before the world-building loops run**, so the loops are fleshing out a world whose
   words already have their variants, rather than one where every new noun is a fresh gap.
4. **The gaps log is the backstop, not the mechanism.** Every unknown word is still logged to the
   wall-sensor (DR-08c) and read at build time by the next pass — it catches what the authoring
   missed, which is exactly what a sample of real play is good for. Nothing auto-learns at runtime:
   DR-02 holds, there is no runtime language model to do the learning. *(Proposed by Claude, for
   Andrew's check: unknown words go into the same `gaps.jsonl` the wall-sensor already writes, with a
   minimal record — the raw line, the unrecognized word, `actor`, `zone`, `at` — so the loop reads
   one queue, not two.)*

Today only the verb×thing gap is logged; the unknown-*word* log is designed and not yet wired (§7).

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

**The measured numbers** (the phrasing corpus, measured 2026-09-07, real parser, real nouns — two
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
3. **`use X on/to`** is the first thing an untaught agent tries → the tolerance path that resolves
   through capabilities.
4. **Synonym drift is bounded**: after the table, unknown verbs are real missing verbs, not
   phrasing.
5. Nouns fail more than verbs: **plurals, adjectives, head nouns** (`the quilted engine cover`),
   **possessives that aren't parts** (`the pilot's jacket`) → all four handled in the binder.
6. The taught condition converges across models (79 vs 83); the naive gap is larger (71 vs 78) —
   another reason the guide goes to agents up front.

### 3.8 Lens pass (Claude)

**Skill (GD — "what skills does this game require?").** Verdict: GREEN. Evidence: the skill is
*understanding the world*, not guessing syntax: a fixed set of shapes, all shown up front, with the
tolerance layer absorbing the rest (measured 79–83% taught). Severity: —. Note: the remaining
friction is vocabulary (new verbs, scenery nouns), which the discovery loop drains; the guide never
has to grow.

**Information (GD — "is the right information visible at the right moment?").** Verdict: YELLOW.
Evidence: the right information is the physics of why, and the tier-4 physics message is not built
yet, so today a verb that doesn't fit falls to a verb-list redirect — which the design forbids.
Severity: med. What would change it: tier-4 + the clarification-only code change (DR-08c).

**Simplicity / Complexity (GD — "is the complexity in the world, not the interface?").** Verdict:
GREEN. Evidence: interface complexity is fixed (a short list of shapes); world complexity is unbounded
(materials × forms × operations). Note: resist adding shapes; add nouns and verbs.

**The Toy (GD — is it fun to poke without a goal?).** Verdict: YELLOW until tier-4. Evidence:
poking is rewarded only when the answer is the physics of the thing; today's verb-list redirect is
a wall with a smile, and a menu would be worse.

### 3.9 `make` — the one aim-verb, and how it dispatches (Andrew, 2026-09-18)

**"State the act, not the aim" (§3.2 rule 1) holds for every verb but this one.** `make` exists
precisely to catch an aim and turn it into an act. It behaves in exactly two ways.

**Vague — no means named.** A clarification, nothing else:

```
> make fire
How do you mean to make a fire?
```

The request is too vague, so the game asks how — in the world's voice, as every line the game speaks
is (Andrew, 2026-09-18). No recipe, no list of what a fire needs, no naming of what is in reach. What
a fire wants is knowledge, and knowledge lives in the world: the tutorial rooms, and the physics of
each failure.

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
path — the one-pipeline rule (DR-09) is untouched, and `make` is the twin of `use`: `use`
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
shelter in 08, the signal in 14, the splint in 11. This document owns the form and the dispatch rule
only. **Those five come first** (Andrew, 2026-09-18) — the ones a party reaches for on day one — and
the loops grow the rest.

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

With no numbered menu (DR-08c), the content carries a duty. When two things a player can plausibly
confuse are in reach, the game asks `Which seat do you mean?` and nothing more — so the player must
have some word that separates them. Every pair of confusable things therefore needs
**distinguishable names or adjectives in its authored prose**: the *wrenched* seat and the *thrown*
seat, seat *1a* and seat *1b*, the *forward* bin and the *aft* bin. Identical things (three glass
shards) never ask, because it does not matter which one you take.

This is a rule the world-building loops must follow (document 17, document 22): a room that can ask
an unanswerable question is a bug in the room, and **`make validate` catches it** — it fails when two
reachable things in a zone share a name with no distinguishing adjective or label.

### 3.11 Quantities: counts, measures, and what you can carry (Andrew, 2026-09-18)

People do not count when they gather. They say *a handful of rocks*, *some branches*, *an armful of
wood*, and the world tells them what they got. So a quantity in the grammar is a **budget the engine
spends**, never a number the player has to get right. Counts and measures are both in.

| what they type | what it means | what the world answers |
|---|---|---|
| `take rock` | one | "You pick up a fist-sized stone." |
| `take two rocks` | a count, bounded by what is there and what you can carry | "You take two of them." / "You take two; there is only one more." |
| `a handful of X` | what one hand holds | "You gather a handful — five or six fist-sized stones." |
| `an armful of X` | what both arms hold | "You get an armful of deadfall across your chest." |
| `some X` · `a few X` | a small sensible amount, resolved like a handful | as above |
| `all the X` | everything of that class in reach, **bounded by what you can carry** | "You can manage four; the rest stay where they are." |
| `as much X as I can carry` | fill to the limit deliberately | "You load up until your arms ache." |

Three rules make this honest.

**A quantity resolves against what is physically there.** The source is a class that yields
individuals (document 17; `PLAN.md` E16) — deadfall, snow, rocks, bark, berries. Ask for more than
exists and you get what exists, and the world says so. No refusal, no menu.

**A quantity resolves against what you can carry**, which needs two budgets:
- **mass**, in integer grams, which the contract already tracks and conserves;
- **bulk**, which does not exist today and is the real gap. A down sleeping bag is light and
  enormous; the aircraft battery is small and crushing. **Bulk derives from mass ÷ the material's density**
  (Andrew, 2026-09-18), with an authored value winning — the same derive-then-override shape the
  capabilities use. `density` becomes a material axis (document 18). *(Proposed by Claude,
  2026-09-26, for Andrew's check: porous things — snow, down, moss, a sleeping bag — use their
  as-found density, with compression as a state, so a stuffed sack is smaller than a loose one;
  document 18 §4.8.)*

**What a gathered quantity *is*, in your hands: an aggregate (Andrew, 2026-09-18).** Five gathered
stones are one entity carrying a count and a total mass, not five objects — the object count stays
sane and conservation stays exact, because the grams live on the aggregate. It splits when one is
spent (`wedge a stone under the runner`) or when one stops being interchangeable — a stone with
blood on it earns its own identity, which is the same *individuate what a player would individuate*
rule the rooms use (document 17).

**Capacity lives on containers, not on a character stat.** Your hands hold a couple of things; your
pockets hold small ones; a backpack, a duffel or a laptop bag holds what its capacity says; a seat
frame dragged behind you (document 16) hauls far more and costs you speed. What you can carry is the
sum of what you are holding, wearing and hauling. Exceeding it is never a refusal: you take what
fits, the world names what you left, and the load feeds the travel time in document 03 §4.1a
(distance ÷ pace × terrain × snow × **load** × fitness).

**`all` is scoped (Andrew, 2026-09-18)** — `take all from the duffel`, `take all the branches` —
never a bare `take all` over the room. A room-wide `take all` would be both unphysical (you cannot
carry a room) and a discovery shortcut: it would reveal what is takeable by taking it, which is the
never-list rule leaking out through a convenience. A scoped `all` is still bounded by what you can
carry, and what you cannot carry stays where it is, in the prose.

## 4. Interactions

**Depends on:**
- The forms and derived-capability model (`ontology-closure.md` §2–3) — what "a verb that doesn't
  fit" or "tools are anything with the capability" cashes out to.
- Tier-4 generic physics (`ontology-closure.md` §4) for the "verb that doesn't fit" reply — not yet
  built (§7).
- The operation×material resolver (DR-09, `implementation-architecture.md`) that a bound
  `ActionAttempt` is handed to.
- Whatever `examine` shows for a thing's nameable parts — the player view
  ([`03-the-player-view.md`](03-the-player-view.md); `presentation.md` v2 pending) governs what
  naming-them-the-way-the-room-does actually displays.

**Depended on by:**
- Every survival system's verbs type through this grammar — fire and shaping, water, food, injury,
  the moral/social layer (documents 07, 09–11, 15) all express their acts in these forms.
- The agent-player document (`20-the-agent-player-and-research.md`): agents are given the grammar
  guide up front (Andrew, 2026-09-07) — this document is that guide's design source.
- The world-building loops (`22-the-world-building-loops.md`): the wall-sensor's logged gaps and
  the phrasing corpus are two of the four sources that feed the authoring loop (the other two are
  the room censuses and the rescue paths of document 14 — `ontology-closure.md` §6).
- The growing-sets framing itself (`05-ontology-and-sufficiency.md`): the vocabulary — verbs, nouns,
  forms — is one of the growing sets that document frames; this document is where its parser-level
  mechanics live.

## 5. Open questions

None open. Every question this document asked was answered on 2026-09-18 and is written into §3.

## 6. Review log

- **2026-09-16** — first draft, merged from the grammar guide, the phrasing corpus, `ontology-closure.md`
  §5 and the DR-08 chain; the same day, feedback became clarification only, with no numbered nouns,
  no suggested verbs and a silent `use`.
- **2026-09-18** — reviewed in full with Andrew: `make` as the one aim-verb; the forms list finalized
  before the loops, with the movement, goal, quantity and meta forms; `use X on Y` stays, silent;
  `help grammar` written once the forms are final; vocabulary authored
  word-first, with the gaps log as the backstop; quantities as budgets, counts and measures both;
  `all` scoped; a gathered quantity is an aggregate; bulk from density; every line in the world's
  voice; the first five goal rows; distinguishable names enforced by `make validate`.
- **2026-09-27** — common sense is hinted, in the world's voice (from the rescue review, document 14).

## 7. What exists today

**Built, but shipping the pre-2026-09-16 behaviour** (the DR-08c code change, `PLAN.md` B13, has not
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
  properties (`ontology-closure.md` §4) has not replaced it yet.
- `game/commands/cmd_act.py` and `game/commands/cmd_items.py` — both still show a **numbered**
  disambiguation menu (`Which X do you mean?` followed by a printed `1. / 2. / …` list and "type a
  number to choose"), the DR-08a mechanism; not yet the bare question with nothing else.
- `game/world/help_entries.py` — `help grammar` is close in shape (the forms + one example each)
  but still says `'use X on Y' works — the game tells you which verb it did` (should be silent) and
  still carries a `help verbs` entry (the verb-family list) that DR-08c says to delete.
- `game/world/sim/operations/handlers/use.py` — resolves through capabilities correctly, but still
  **echoes** the verb it picked (`"(That's 'cut cover with shard'.)"`); the design is silent
  resolution.
- `game/world/sim/operations/handlers/make_op.py` — answers with what the thing is made of, and
  still supports a tool-named "limited question" reply; the design is the plain clarification of
  §3.9.
- `game/world/sim/operations/_helpers.py`'s `sibling_hint()` (used by `handlers/cut.py`, `pry.py`,
  `tear.py`) — the DR-09a near-miss hint; still present in three handlers.
- `game/world/sim/testing/probes.py` — a disambiguation mid-chain still defaults to "the first
  option" (its own docstring: "default the first"); probe steps should name nouns unambiguously
  instead, removing the need for a default.
- The wall-sensor (`game/world/sim/resolver/wall_sensor.py` + `cmd_act.py`'s `_log_gap`) logs
  resolved-but-unhandled verb×thing attempts (tier-5 generic redirects) to
  `server/logs/gaps.jsonl`. It does **not** yet log unknown-verb parse failures — so "every unknown
  word is logged" (§3.7) is decided and designed, not yet built.

**Designed, not built:**
- The DR-08c clarification-only rewrite as a whole (`PLAN.md` B13: remove the nudge and the
  verb-list redirect, replace both numbered menus with the bare question, delete `help verbs`,
  silence `use`/`make`, drop the DR-09a hint, stop defaulting probe disambiguation, wire the
  unknown-word log).
- `make` as the aim-bridge, quantities, the distinguishable-names gate, and word-first vocabulary
  (`PLAN.md` E20, E21, E22, E25).
- `docs/architecture/grammar.md` — referenced as the architecture counterpart in
  `docs/design/README.md`'s table, not yet written; `ontology-closure.md` §5 stands in for it.

**Measured (not code, but a real artifact):**
- `game/world/scenarios/whiteout/probes/phrasing.py` — the phrasing corpus's agent-typed lines as
  probes (`expect: "PARSED"`), 302 lines including a small number marked `status: "todo"`; this is
  the artifact §3.7's numbers were measured against.
