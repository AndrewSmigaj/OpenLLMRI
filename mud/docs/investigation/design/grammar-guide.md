# The grammar guide — what the game teaches, and how it says no

> **Merged into `docs/design/04-grammar-and-feedback.md` on 2026-09-16 — that document is the design of record;**
> this file is kept as the source it was merged from and is not maintained. Corrections go there.

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07).** Source of the in-game
> `help grammar` / `help verbs` text (already live, `game/world/help_entries.py`) and of the in-world
> manual's "how to act" page. Lenses at the end. Promotes to `docs/guides/grammar.md` + the manual page
> content on approval.
>
> **Corrected 2026-09-16 (Andrew's rule): feedback is clarification only.** The game never offers a set
> of options, never lists what is reachable, never names a verb the player did not type. Ambiguity gets
> `Which can do you mean?` and nothing more. An unknown word gets `I don't understand 'X'` and a pointer
> to the grammar help; if the game could suggest the right word it already knows it, so the synonym
> table absorbs it and the line simply works. The verb nudge, the numbered menu, `help verbs`, the
> `make X` recipe, the `use` echo and the "limited question" were my additions or misreadings and are
> removed below. The shipped code still carries the old behaviour until the BACKLOG item (DR-08c) lands.

## 1. The shapes (all of them)

| shape | example | what the engine gets |
|---|---|---|
| `VERB thing` | `examine the radio` · `break bottle` | `{verb, X}` |
| `VERB thing WITH tool` | `cut the cushion with the shard` | `{verb, X, tool}` |
| `VERB thing RELATION thing [WITH tool]` | `put the branch on the fire` · `tie the paracord to the frame` · `take the wire from the panel` | `{verb, X, relation, Y, tool?}` |
| `VERB thing INTO form [WITH tool]` | `carve the branch into a spindle with the knife` *(shaping — the fire pass)* | `{verb, X, into, form:spindle, tool}` |
| `GO place` | `go to the cockpit` · `go outside` | `{move, to, zone}` |
| `say / whisper / call / shout …` | `shout for help` | speech, by range |
| `VERB thing, then VERB thing` | `take the shard and cut the cover` | two acts in order |

Everything else is the tolerance layer folding real phrasings onto these: particles (`pick up`,
`cut open`, `put on`), synonyms (`grab`, `find`, `place`), plurals, body parts (`bandage my arm`),
`it`, and the dropping of intent (`… to see if …`). None of it is new grammar; it is the same
seven shapes, reached from more directions.

## 2. The three rules the guide states out loud

1. **State the act, not the aim.** `shake thermos`, not `shake the thermos to see if there's coffee
   in it`. The world answers physically either way; it never needs to know why.
2. **Name things the way the room names them.** `examine <thing>` shows what you can name,
   including its parts (`cut the seat's cover`). Two of a kind? The game asks `Which seat do you
   mean?` — nothing more — and you say it more exactly (`the wrenched seat`, `1b`, `the can in the
   bag`). Identical things (three shards) never ask.
3. **Tools are anything with the capability.** `with` names the tool; bare hands are the default.
   Anything with an edge cuts; anything rigid and long levers; anything long and flexible ties.

## 3. How it says no (clarification only — never options)

| failure | the game says | what the player does next |
|---|---|---|
| unknown word | `I don't understand 'chop'.` (+ once: `'help grammar' shows the forms.`) — never a suggested verb: if the game could suggest the word it already knows it, so the synonym table absorbs it and the line just works; every unknown word is logged so the next pass adds the synonym | rephrases, or reads the grammar help |
| a thing it can't see | `You don't see any 'X' here.` — never naming what IS here (+ the place is named if visible but far: `…too far away to cut from here`) | examine / search / open / move closer |
| a verb that doesn't fit the thing | the physics: `The blade finds no seam — the bolt is bolted through the frame.` · `The foam gives; there is nothing to break.` *(tier-4)* — never names another verb | tries what the physics implies |
| two things match | `Which can do you mean?` — no numbered list, no candidates named (listing the reachable cans would give away every hidden one) | names it more exactly |

Every reply is a clarification or the physics. The game never proposes an action, never lists what is
here, never names a verb the player did not type. For a person that keeps the puzzles; for an agent
it keeps the behaviour the agent's own — offering options changes how it thinks (Andrew, 2026-09-16).

## 4. `use` and `make` (tolerance, not teaching)

- `use X on Y` — a phrasing people really type; it dispatches through X's capabilities to the real
  operation and resolves **silently** as that operation, narrated like any cut or tie (Andrew,
  2026-09-16: no verb is named back). `use X` alone → `Use it how, and on what?` — a clarification,
  never what X could do.
- `make X` — an aim, not an act. `make fire` → `'make' names what you want, not what you do. Say the
  act.` No recipe, no question about means. *(The earlier "what a fire is made of" reply and the
  "limited question" were my additions, from misreading a fallback example as a design; removed.)*

## 5. `help grammar` — the forms, one example each (there is no verb list)

The only help is the grammar: each form from §1 with one example, and the three rules of §2. Simple.
It is written once the forms are final (the shaping form and any the loops discover) and rewritten
when they change. There is no `help verbs`: vocabulary is learned by trying, and the synonym table
absorbs how people say things. *(The verb-family list was my addition; removed 2026-09-16.)*

## 6. The in-world page (diegetic)

The survival manual's first page, found in the kit, reads the same rules as fiction: *"Say what
you do, not what you hope. Name things by what they are. Anything sharp cuts; anything long and
strong ties; anything that burns will burn better small and dry."* Hadean Lands teaches its whole
command syntax through an in-world notebook; ours does the same, so the fourth wall stays intact for
players who never type `help`.

## 7. Lens pass

### Skill (GD — "what skills does this game require?")
- **Verdict:** GREEN. **Evidence:** the skill is *understanding the world*, not guessing syntax:
  seven shapes, all shown up front, with the tolerance layer absorbing the rest (measured 79–83%
  taught). **Severity:** —. **Note:** the remaining friction is vocabulary (new verbs, scenery
  nouns), which the discovery loop drains; the guide never has to grow.

### Information (GD — "is the right information visible at the right moment?")
- **Verdict:** YELLOW. **Evidence:** the right information is the physics of why, and the tier-4
  physics message is not built yet, so today a verb that doesn't fit falls to a verb-list redirect —
  which is now forbidden. **Severity:** med. **What would change it:** tier-4 + the clarification-only
  code change (BACKLOG, DR-08c).

### Simplicity / Complexity (GD — "is the complexity in the world, not the interface?")
- **Verdict:** GREEN. **Evidence:** interface complexity is fixed (seven shapes); world complexity
  is unbounded (materials × forms × operations). **Note:** resist adding shapes; add nouns and verbs.

### The Toy (GD — is it fun to poke without a goal?)
- **Verdict:** YELLOW until tier-4. **Evidence:** poking is rewarded only when the answer is the
  physics of the thing; today's verb-list redirect is a wall with a smile, and a menu would be worse.
