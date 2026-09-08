# Ontology closure — forms, derived capabilities, fallback physics, and the probe corpus

> **Status: v1 — design of record (2026-09-07), promoted from the planning session.** Decisions
> DR-26 (closure), DR-05b / DR-17a / DR-18a (amendments) in
> [`implementation-architecture.md`](implementation-architecture.md) §2. The engine work this doc
> governs is the **closure loop**: closure → harness → parser tolerance → (time & stakes, designed
> separately) → tier-4 physics → verb gaps + nouns. Companion design passes (scratchpads until
> promoted): `docs/investigation/design/*.md`.

## 1. The property we are building toward

**Ontological sufficiency**: a player — a person, or an LLM agent whose trajectories we study — can
do *whatever is reasonable* and the world answers physically. Decomposed:

| axis | means | mechanism (this doc) |
|---|---|---|
| **closure** | every output of an operation is a full entity: it has a form, derived capabilities, and prose | §2, §3 |
| **fallback physics** | when no handler fires, the answer comes from mass / material / state, never from a verb list | §4 |
| **phrasing tolerance** | the taught grammar absorbs the phrasings people and agents actually type | §5 |
| **coverage, measured** | sufficiency is a number that only goes up | §6 (the probe corpus) |
| **entity sufficiency** | scenery and elusive things (cold, draft, light, smell, sound) are addressable | pseudo-nouns (§5.4) |
| **time & stakes** | activities with feedback; fire, warmth, hunger, injury on the clock | separate design pass (time-and-stakes, fire-and-shaping) |

The engine already had the tiers, the ledger, the single writer and the taught grammar. It lacked
closure: a shard minted by `break` carried only material, mass and provenance, so `cut X with shard`
counted as bare hands. That gap — outputs as dead ends — is what this doc closes.

## 2. Forms

A **form** is the shape a quantity of material takes. Materials (DR-04) say what a thing is made of;
forms say what shape it is in; capabilities (§3) fall out of the pair.

The taught forms vocabulary (v1, ~15; extend by evidence, never speculatively):

| form | typical origin | what it lends |
|---|---|---|
| `shard` | break glass / ice / instrument faces | edge, point |
| `piece` | break / cut a standalone thing in two | heft (if rigid) |
| `scrap` | hack a part off a mechanical fastener | little; fuel if flammable |
| `strip` | tear / cut cloth or bark lengthwise | cordage (if flexible), tinder (if thin) |
| `sheet` | tear hull skin; a flat flexible thing | sheet (cover, wrap, windbreak), edge if metal |
| `slab` / `board` | split wood | flat rigid surface; the drill board |
| `rod` / `stick` | a branch, a spindle blank | leverage, the drill spindle |
| `spindle` | carve a stick | rotation (the friction drill) |
| `point` / `stake` | whittle a stick | point |
| `bow` | string a springy stick with cord | the bow (drives a spindle) |
| `shavings` | shave wood | tinder (thin) |
| `bundle` | bundle grass / fibre | the tinder nest |
| `cord` | paracord, twine, a strip twisted | cordage |
| `vessel` | a can, a cup, a hollowed thing | holds liquid |
| `ember` / `ash` | friction drilling / burning | ignition (ember); nothing (ash) |

Minted objects carry `state["form"]`. Handlers that mint (break, cut, tear, pry, and the shaping
family) name the form they produce; `apply()` copies it into the new object's state. Authored
objects may declare a form too (the multitool is a `blade`; the whisky bottle is a `vessel`).

**Shaping** (`carve`, `split`, `shave`, `whittle`, `notch`, `string`, `bundle`) is the operation
family whose outputs are forms. Its grammar is `VERB X into <form> [with Z]`: the form word sits in
the Y slot as a **form pseudo-noun** (`form:spindle`), exactly as zones do (`zone:cockpit`). The
parser tries an entity match first; a real entity in Y means "one like that". No contract change.

## 3. Derived capabilities

A **capability** is a named, levelled affordance a thing offers to a verb: `edge`, `point`, `heft`,
`leverage`, `abrasive`, `ignition`, `flame`, `cordage`, `sheet`, `vessel`, `insulating`,
`absorbent`, `reflective`. Verbs require a capability at a level; they never name a tool. (This is
Cataclysm DDA's tool-quality model, which has run thousands of recipes on the same idea.)

`world/sim/affordances.derive(entity, materials) -> {axis: level}` computes capabilities from
**material × form × state**:

- `edge = cut_resistance(material) × FORM_FACTOR[form]` with blade 1.0 · shard .85 · sheet .6 ·
  piece .3 · else 0 — a hard material in a sharp form holds an edge; foam in any form does not.
- `leverage = rigidity × (rod .8 · piece .4 · slab .3)`, gated by mass (a toothpick is rigid but
  lends no leverage).
- `cordage` if the material is flexible and the form is `strip` or `cord`; `sheet` if flexible and
  the form is `sheet` or cloth-like; `reflective` if glass or metal in `sheet` or `shard` form;
  `ignition` / `flame` from state (`ignition`, `lit`, `ember`) as today.
- **Capped**: a derived level never exceeds min(material tier, form tier). Free composition must
  not mint an exploit.
- **Authored wins**: an explicit `state[axis]` on the object overrides the derived value. The
  golden objects (multitool 0.8, hatchet 0.5) stay hand-tuned.
- **State degrades**: a wet match has no ignition; a chipped edge is lower; a frozen cord is
  stiff. (The state axes are written by operations as the time & stakes pass lands.)

`_helpers.capability()` reads the authored value, then falls back to `derive()`. That one
function is the whole engine's reach into the model, so closure lands everywhere at once.

**The signifier rule.** A capability nobody can see is the top complaint across every
property-based game we studied. Every load-bearing derived capability must show in the examine
text: "a shard of glass, one edge wicked-sharp". Derived objects get **form-keyed generic prose**
(`"{material} shard, …"`) rendered through `narrator.render`; authored name-keyed entries in
`appearance.py` override it.

## 4. Tier-4 generic physics (the fallback that kills the verb list)

Today an unhandled verb×thing falls through to the coarse redirect: "you could cut, burn or pry
it" — or "Nothing you try seems to affect the X." Tier 4 sits between the handler returning `None`
and that list, and answers **from properties**: a soft thing "gives — there is nothing to break";
a liquid "parts around the blade"; a heavy thing "won't shift"; a non-flammable thing "won't take a
flame"; a wet thing "is too wet to catch"; a non-edible thing "would choke you". Each is a narrated
REDIRECT with a physical reason, and only then the ≤2-verb suggestion. The wall-sensor records the
attempt either way.

## 5. Parser tolerance (the largest measured gap to an agent playing)

Measured 2026-09-07 with the real parser against the real world's nouns: taught-condition agent
phrasings parsed 32–58%; six mechanical fixes lift that to 76–79% in simulation; the residue is a
short list of new verbs and scenery nouns owned by later steps. The fixes, all inside the taught
grammar (none of this is free-text NLP):

1. **Particles, resolved positionally** (TADS 3's rule): a word right after the verb with no noun
   following is a verb-sense particle (`cut open`, `take out`, `put on`); the same word followed by
   a noun is the RELATION slot (`cut off the strap`).
2. **Multi-word relations** as greedy token sequences (`out of`, `on top of`) and the missing
   single ones (`over`, `onto`, `through`, `across`, `inside`, `behind`, `beside`).
3. **A synonym table** seeded from the sampled phrasings (find→search, check→examine, place/add→
   put, gather/collect/retrieve→take, secure→tie, heat→melt, shoot/fire→light, …).
4. **State the act, not the aim.** The game never needs intent: `shake thermos`, not `shake
   thermos to see if coffee is in there`. Trailing purpose clauses and adverbs are trimmed;
   meta-verbs (`try to`, `see if`) are stripped; `and` compounds become two commands.
5. **Body parts and pronouns**: `my arm` / `myself` → the actor; `it` → the last bound noun
   (ephemeral per-caller shell state, like the pending menu).
6. **Noun binding**: whole-phrase entity match *before* the possessive `of` split (`canteen of
   water`), then longest-known-noun matching so trailing words don't poison the phrase.

Plus the teaching layer: **three distinct failure messages** (unknown verb → 2–4 plausible verbs;
unresolvable noun → "you don't see that here", point to `examine`; supported verb + wrong object →
the tier-4 physics), **silent disambiguation first** (held > reachable > recent; the more specific
candidate wins; ask only on a true tie), **`use X on Y`** dispatching through capabilities to the
real verb and echoing it, **`make X`** naming what X is made of, and **`help grammar` /
`help verbs`** teaching forms and verb families — never solutions.

### 5.4 Pseudo-nouns
Zones (`zone:`), forms (`form:`), and — as the verb-gap step lands — **scenery** (`scenery:`:
windscreen, bulkhead, instruments) and **elusive** entities (cold, draft, light, smell, sound) are
addressable nouns without being objects. They resolve through `reachables()`, skip the reach gate,
and answer `examine` / sense verbs with authored prose.

## 6. The probe corpus — coverage as a number

A **probe** is one typed command chain in one room with an expected outcome class:

```python
{"id": "cockpit.shard_cuts_cover", "zone": "mid_cabin", "holds": ["bottle"],
 "steps": ["break bottle", "take shard", "cut cover off seat with shard"],
 "expect": "SUCCESS", "tier_prefix": "op:cut", "status": "pass",
 "source": "rooms/cockpit.md §5 item 4"}
```

Probes run the **real parser** on typed lines against a **pure in-memory world** (`PureWorld`,
loaded from the same `OBJECT_TABLE` the Evennia loader uses, with an in-memory `apply()` for
chained steps). A disambiguation mid-chain takes the first option unless the step names a pick.

- `status: pass` probes are CI-enforced; `status: todo` probes are the work queue.
- `probes/BASELINE` holds the passing count; it may never drop (the ratchet).
- Every probe cites its source: a census row, a phrasing-corpus line, a rescue-graph node, or
  Andrew's approval. No self-graded probes.
- **Coverage (DR-18a)** = the probe corpus passing count + the seeded fuzz (every attempt resolves,
  every effect conserves). This replaces "the op×material matrix populated" as the definition.

The corpus grows from four sources: the room censuses (~120 rows), the phrasing corpus (agent-
generated commands), the rescue graph (goal paths), and the dilemma set.

## 7. The closure loop (how overnight runs work now)

The unit of overnight work is a **probe cluster**, not a room. Each firing (`/loop 30m`, one box,
then stop): take the next `todo` cluster → extend a material, a form rule, an operation, or an
object — never a one-off → `make test-host && make validate && make probes` → `make render-scenes`
→ commit code + docs + probes → tick the box. The morning artifact is
`docs/review/render-<date>.md`: Andrew reads prose, not diffs.

Day sessions design: a scratchpad per chunk → a lens pass → promotion → probes → the loop builds.

## 8. What this doc deliberately does not decide
The time & stakes model (activities, the fire ladder, warmth / hunger / injury), the rescue graph,
the moral & social layer, the living-room rule and the fire & shaping content are separate design
passes; they are referenced here only where the closure mechanism must leave a seam for them.
