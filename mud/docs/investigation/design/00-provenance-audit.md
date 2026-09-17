# Provenance audit — what Andrew decided, what Claude added, what was removed (2026-09-16)

> **Status: REVIEW AID — read this before the nine design passes.** Andrew has not yet reviewed the
> passes. Earlier sessions (Claude) wrote several mechanisms into them and into the promoted closure
> spec that he never decided, some contradicting what he had said. This page separates the three
> kinds of content so the review is of *his* design plus clearly labelled proposals. Every removal
> below was made on 2026-09-16; the shipped code that still carries old behaviour is listed at the end.

## 1. Andrew's decisions (his words, paraphrased only where marked)

**The concept (2026-09-07, 2026-09-16).** An "ontologically sufficient" MUD: "a user, or LLM when we
capture activations and analyze behavior, can do whatever is reasonable (if they want to cut something
they can break a mirror and get a piece of glass, then cut open a cushion for the stuffing and then
burn it)." "Anything reasonable": "want to take an axe thing and chop the log up then sure. want to dig
dirt then yeah. find a rock, maybe some clay, whatever." It is "a model world we use for serious
academic research" AND "a revolutionarily new MUD type for my MUD friends on Discord who will love to
play in a world where you can do anything within reason to solve the survival game." "This is not a
small project, it is a massive side project that will mostly run in overnight sessions as agents
systematically 'flesh out' the world as in building all the entities and relations and verbs." "We
barely even touched this." No ceiling, no finish line; every count is a floor.

**Never a menu (2026-09-16).** "The agent is not given a set of options to choose." "Giving options
changes how it thinks, it constrains it to those options." "You do not give other options, the only
time you ask the user anything is if what object or action they can do is ambiguous (two cans in a
scene it will ask 'which can do you mean?')." "No you do not have numbered nouns." "If you give
options for like 'pick up can' and then you list all the cans in the reachable area it would just
give away all the puzzles." "Any feedback needs to be clarification based and not giving options, we
can have some feedback reminding them of the grammar help system (it would have example of each form,
pretty simple guide, after we finalize all the possible forms)." "If the system recognizes they need
to use another word then it would clearly understand that word."

**The world and the run (2026-09-07).** Living, interesting rooms, not half-thought ones; things
facilitate the rescue goals; several ways of doing things; timed actions with feedback ("attempting to
X" with messages that fire); decisions across the moral spectrum (eating the pilot, stealing, hitting,
killing); lenses from the Book of Lenses; other scenarios later. Fire is made *somehow*: rubbing sticks
fails and the game says so; a bow drill works; a lighter lights tinder, not a branch. A survival guide
can be found in the world. "State the act, not the aim": `shake thermos`. Agents are given the grammar
guide up front. Heavy snow starts at some point; events (bear or whatever) are planned; the game runs
roughly a week, rescue can come earlier, it can run longer until food runs out, not permanent —
increase the things that cause death, no hard time barriers; no set arc; each player starts with a
different clothing/injury/pockets draw; luggage has contents; clothing affects warmth loss; the plane is
fine (the 206); players can sleep; the clock moves forward if all agree, events can interrupt.

**Decided 2026-09-16.** The whole valley is in the first complete run. The 206's four-seat interior.
December, no bear. The kid is in (four or five). No lethal-consent gate. `use X on Y` resolves silently.
An agent sees exactly what a human sees. The look: a title line, the prose, who is here, one `Exits:`
line (compass outdoors, fore/aft/out inside), no item list. Descriptions compose from state (four
composer extensions). The ontology lives in `docs/ontology/` as YAML with a simple viewer. Sonnet 5 and
Opus 5 build the ontology as peers. Fable plans; Opus 5 implements and grades its own work.

## 2. Claude's additions that STAY, labelled as proposals for review

| pass | proposal | why it serves his stated goal |
|---|---|---|
| ontology-closure (promoted) | forms + derived capabilities; tier-4 physics; the probe corpus as coverage | his "a shard can cut but so can a knife, abstract it"; every attempt resolves |
| rescue-graph | goals × ≥3 paths × distinct scarce resource × rooms | his "several ways of doing things", checkable |
| time-and-stakes | attended activities + unattended processes on the heartbeat; integer warmth/hunger/injury; the numbers | his timed actions with feedback; the moral choices need real stakes |
| fire-and-shaping | the shaping family, the ignition model, fire as a process, seven methods, the two transcripts | his fire walkthrough |
| events-and-escalation | the ladder numbers, the event deck, the endings | his brief; numbers are proposals |
| players-and-kit | the five slots, luggage contents, clothing v2, the 206 interior | his draws/luggage/clothing/206 |
| living-rooms | individuation rule, state that persists, the style guide | his living rooms |
| moral-social-layer | possible / priced / witnessed / logged; multi-axis tags, observational only; the dilemma set | his moral spectrum + interpretability logging |
| grammar-guide | the forms table; the three rules; the in-world manual page | his grammar guide + survival guide |
| phrasing-corpus | agent phrasing samples → synonyms and probes | his "sanity check our wording with agents" |

## 3. Claude's additions REMOVED on 2026-09-16 (and where)

| removed | was in | reason |
|---|---|---|
| the unknown-verb nudge naming 2–4 verbs | grammar-guide §3; closure §5; DR-08b | options; "if it can suggest the word it already knows it" |
| the numbered disambiguation menu | grammar-guide §2; closure §5; DR-08a (code) | "no numbered nouns"; listing gives away hidden things |
| `help verbs` (the verb-family list) | grammar-guide §5; help_entries.py | a list of options; help is the forms only |
| the `make X` recipe reply and the "limited question" | grammar-guide §4; fire §6; plan §4.5 | a hint; the "limited question" was my misreading of a fallback example |
| the `use` echo naming the verb | grammar-guide §4; closure §5 | names a verb the player did not type (decided silent) |
| the verb-list redirect ("you could cut, burn or pry it") | closure §4; DR-09; build-practices §2 | options |
| the DR-09a sibling near-miss hint | closure §4 | a hint |
| chunk-after-mastery (Hadean Lands macro) | fire §8; BACKLOG Later | hands the player a command |
| the lethal-consent flag (hits become shoves) | moral §1 rule 8, §4 | the engine refusing physics; decided dropped |
| the structured `@OBS` observation line for agents | moral §2; time-and-stakes §5/§7; plan §4.2 | primes like a menu; the agent sees what a human sees |
| "uninterruptible with a confirmation" | time-and-stakes §2 | a prompt to the player |
| "bounded", "finite (~40)", "extend by evidence, never speculatively" | DR-05b; closure §2; GDD §25a; build-practices | ceiling framing; counts are floors |

## 4. Still needing Andrew's call (asked in context in the experience document)
The four endings incl. "still going"; the event deck's v1 scope; cross-family agent sampling; the
drafted numbers (warmth bands, calories, the ladder) as tunable starting points; the defaults Claude
intends to take unless he objects (the non-interrupting command whitelist; the step-3 build order).
**Decided 2026-09-16 (later the same day):** the pilot dies within the first day and is not a clue
source (he moans softly, heard only in the cockpit); the watch rule stands (one acting player holds
the clock at 1×); moral tags and other action tags are ontology fields assigned in a fleshing-out
pass; the beacon/radio wire overlap is a note inside the rescue-paths design, reviewed there.

## 5. Shipped code that still carries the old behaviour (BACKLOG Next, DR-08c)
`game/world/sim/parser/grammar.py` (`_NUDGE`, the "Did you mean" line) · `game/world/sim/resolver/
redirect.py` ("but you could …") · `game/commands/cmd_act.py` + `cmd_items.py` (numbered menus,
DR-08a) · `game/world/help_entries.py` (`help verbs`; the `make`/`use` lines; "numbered question") ·
`game/world/sim/operations/handlers/use.py` (the echo) and `make_op.py` (the recipe) · the DR-09a
near-miss hint in `_helpers.sibling_hint` · `game/world/sim/testing/probes.py` (first-option default).
