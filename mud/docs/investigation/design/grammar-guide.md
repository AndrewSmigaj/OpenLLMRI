# The grammar guide — what the game teaches, and how it says no

> **Status: SCRATCHPAD — design pass for Andrew's review (2026-09-07).** Source of the in-game
> `help grammar` / `help verbs` text (already live, `game/world/help_entries.py`) and of the in-world
> manual's "how to act" page. Lenses at the end. Promotes to `docs/guides/grammar.md` + the manual page
> content on approval.

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
   including its parts (`cut the seat's cover`). Two of a kind? Add the label (`12c`) or answer the
   numbered question. Identical things (three shards) never ask.
3. **Tools are anything with the capability.** `with` names the tool; bare hands are the default.
   Anything with an edge cuts; anything rigid and long levers; anything long and flexible ties.

## 3. How it says no (three messages, never one)

| failure | the game says | what the player does next |
|---|---|---|
| unknown verb | `I don't know how to 'chop'. Did you mean cut? Try: VERB thing … 'help grammar' shows the shape; 'help verbs' lists the families.` | picks a family verb |
| a thing it can't see | `You don't see that here.` (+ the place is named if visible but far: `…too far away to cut from here`) | examine / search / open / move closer |
| a verb that doesn't fit the thing | the physics: `The blade finds no seam — the bolt is bolted through the frame.` · `The foam gives; there is nothing to break.` *(tier-4, step 4)* | tries the verb the physics implies |

The grammar nudge is cheap and automatic. A puzzle hint is expensive and opt-in — it never rides on
a parse error. (InvisiClues / Inform's own caution: syntax confusion and puzzle-stuckness are
different failure modes with different remedies.)

## 4. The teaching verbs

- `use X on Y` — dispatches through X's capabilities to the real verb and **echoes it**:
  `(That's 'cut cover with glass shard'.) You work the glass shard through the cover…`. Next time
  the player says `cut`. `use X` alone: `The glass shard has edge to it — you could cut with it.`
- `make X` — never runs steps. `make fire` → `A fire wants three things: something fine and dry
  that catches from a flame or a spark, small dry wood to build it up, and bigger fuel to keep it —
  and a way to light it.` `make fire with sticks` → adds `How do you mean to use the sticks for
  that? Name the act.` (Andrew's limited-hint form.)

## 5. `help verbs` — the families (what the player sees)

cutting & shaping — cut, tear, break, bend, pry (carve, split, notch: the fire pass) ·
fire — light, burn, melt, douse · binding & covering — tie, wrap, put, cover ·
moving & carrying — take, put, go, open, close, search, dig · body & senses — examine, eat, drink,
wear, remove, read (smell, listen, feel: the verb-gap step) · social — say, whisper, call, shout,
talk to.

Listing families teaches the language, not the puzzle. The list never says which verb opens which
puzzle.

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
- **Verdict:** YELLOW. **Evidence:** the three failure messages give the right *kind* of
  information; the tier-4 physics message is not built yet, so today a verb that doesn't fit falls
  to "you could cut or pry it". **Severity:** med. **What would change it:** step 4 (tier-4).

### Simplicity / Complexity (GD — "is the complexity in the world, not the interface?")
- **Verdict:** GREEN. **Evidence:** interface complexity is fixed (seven shapes); world complexity
  is unbounded (materials × forms × operations). **Note:** resist adding shapes; add nouns and verbs.

### The Toy (GD — is it fun to poke without a goal?)
- **Verdict:** YELLOW until tier-4. **Evidence:** `use X on Y` and `make X` reward poking with a
  lesson rather than a wall; but "you could cut or pry it" is a wall with a smile.
