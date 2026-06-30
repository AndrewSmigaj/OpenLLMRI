# C1 — The pre-LLM lineage of "do-anything in a deep world model" text systems

A historical narrative, not a lessons list. The sibling doc
[`../prior-art.md`](../prior-art.md) reads these same systems for *transferable design
lessons*; this file does the **history** — who built what, when, what the "world model"
actually was — and tracks one recurring fact across six decades: the vision of *a text
world you can do anything sensible in* kept arriving, and kept hitting the same wall.

**Thesis this evidence feeds:** these systems chased "do anything in a modeled world"
decades ago but **stayed small because the world's ontology and content had to be authored
by hand**. Every room, object, property, rule, and response was a person typing it. The
world model could be deep, but it could only be as *big* as a team's hand-authoring budget.
LLMs change the input cost of that authoring; nothing in this lineage changed it. Read the
narrative below as a long accumulation of evidence for exactly where the ceiling sat.

A note on framing: two opposite failure modes bracket the whole story. ELIZA (§1) had the
*appearance* of understanding with **no world model at all**. SHRDLU (§2) had a **genuinely
deep world model** but a world the size of a tabletop. Everything after them lives in the
gap between those poles — trying to keep SHRDLU's depth while escaping its smallness, and
mostly failing on the smallness.

---

## 1. ELIZA (Weizenbaum, 1964–1966) — the illusion of understanding with no world model

Joseph Weizenbaum wrote ELIZA at MIT between roughly 1964 and 1966, running on an IBM 7094
under the CTSS time-sharing system in a list-processing language (MAD-SLIP); its famous
persona was the **DOCTOR** script, a parody Rogerian psychotherapist
(https://en.wikipedia.org/wiki/ELIZA). Mechanically it did one thing: it scanned the user's
typed sentence for keywords, ranked them, and reflected the input back through canned
decomposition/reassembly templates ("I am X" → "How long have you been X?"). There was no
memory of the conversation as *facts*, no objects, no state — Weizenbaum built it with **no
internal model of meaning or "universe of discourse"** whatsoever
(https://en.wikipedia.org/wiki/ELIZA).

That is precisely why ELIZA matters here as the cautionary *opposite* of a world model. It
is the cheapest possible way to *look* intelligent: model nothing, mirror everything. And it
worked unnervingly well — Weizenbaum's own line is that ELIZA shows "how easy it is to
create and maintain the illusion of understanding" while in fact understanding nothing
(https://en.wikipedia.org/wiki/ELIZA). His secretary, who had watched him build the thing,
reportedly asked him to leave the room so she could talk to it privately
(https://www.history.com/articles/ai-first-chatbot-eliza-artificial-intelligence-precursor-llms).

**Weizenbaum's later misgivings** are the whole point of including ELIZA in a world-model
lineage. He was disturbed enough that he spent the next decade arguing *against* the
conflation of fluent output with comprehension, writing in *Computer Power and Human Reason:
From Judgment to Calculation* (1976) that "I had not realized... that extremely short
exposures to a relatively simple computer program could induce powerful delusional thinking
in quite normal people" (https://en.wikipedia.org/wiki/ELIZA;
https://link.springer.com/article/10.1007/s00146-018-0825-9). ELIZA's reception pushed him
to attack the "powerful delusional thinking" about machine intelligence he saw spreading
among experts and the public alike
(https://link.springer.com/article/10.1007/s00146-018-0825-9).

**What kept it small — and why "small" is the wrong word here.** ELIZA didn't hit an
authoring wall because it never tried to climb one. It has no world to author. The lesson it
plants at the head of this lineage is the inverse warning: surface fluency is free, but a
system with no ground-truth state cannot *do* anything in a world — it can only talk as if
it could. Everything that follows is the much harder project of building the state that
ELIZA conspicuously lacked, and discovering that *that* is what doesn't scale.

---

## 2. SHRDLU (Winograd, 1968–1972) — a deep world model the size of a tabletop

Terry Winograd built SHRDLU at MIT between 1968 and 1970, with the canonical write-up
appearing in his 1972 *Cognitive Psychology* monograph
(https://en.wikipedia.org/wiki/SHRDLU). It is the photographic negative of ELIZA: where
ELIZA faked understanding with no world, SHRDLU achieved real, grounded understanding of a
*tiny* world. You conversed with it in ordinary English — "find a block which is taller than
the one you are holding and put it into the box" — and it parsed the request, reasoned about
the scene, resolved pronouns, executed the move in a simulated **blocks world**, and could
explain *why* it did what it did. The simulated environment held blocks, cones, balls,
pyramids, a table, and a box, and Winograd built it so deliberately bounded that "the entire
set of objects and locations could be described by including as few as 50 words"
(https://en.wikipedia.org/wiki/SHRDLU). That is the deep-world-model dream in miniature: a
program you can give an open-ended instruction and have it *do the sensible thing*.

**What kept it small.** Everything SHRDLU knew was hand-coded to that microworld; its
competence was an artifact of the world being exhaustively, manually modeled, and it **did
not generalize past the demo**. Winograd himself disowned the demo-driven approach in
retrospect. In a 1991 interview he admitted the famous dialogue was "very carefully worked
through, line by line," that a question even slightly outside it had only "some probability"
of a sensible answer, and — decisively — "there was no attempt to get it to the point where
you could actually hand it to somebody and they could use it to move blocks around"
(https://en.wikipedia.org/wiki/SHRDLU; https://metadevo.com/potemkin-villages/). He named
the pathology directly: "Pressure was for something you could demo... I think AI suffered
from that a lot, because it led to 'Potemkin villages', things which — for the things they
actually did in the demo looked good, but when you looked behind that there wasn't enough
structure to make it really work more generally" (https://metadevo.com/potemkin-villages/).
The system was so brittle that by 1974 it had succumbed to software rot and a researcher
could no longer get it to respond sensibly (https://en.wikipedia.org/wiki/SHRDLU). Winograd
spent his later career, notably in *Understanding Computers and Cognition* (Winograd &
Flores, 1986), arguing that this whole style of hand-built symbolic microworld was a
conceptual dead end (https://en.wikipedia.org/wiki/SHRDLU).

This is the **key anchor of the whole lineage**. SHRDLU proves that a text system *can* let
you do anything sensible in a modeled world — provided the world is small enough for one
person to model completely by hand. Interpretability and "do-anything" were never the
bottleneck; **coverage** was. The block of 50 words was the budget. Every later system in
this document is, in effect, an attempt to buy a bigger block of words, and every later
system pays for it the same way SHRDLU did: by hand.

---

## 3. Colossal Cave Adventure (1975–77) & Adventureland (1978) — the parser game is born, the world is a hand-coded table

The microworld idea escaped the lab and became a *game* with Will Crowther's **Adventure**
(ADVENT / Colossal Cave), written around 1975–76 in FORTRAN on a PDP-10 at Bolt, Beranek &
Newman (https://jerz.setonhill.edu/if/canon/Adventure.htm). Crowther, a caver and the
network engineer who had helped build the ARPANET, modeled it on the real Mammoth Cave
system in Kentucky — he was literally keeping a computer map of the cave
(https://jerz.setonhill.edu/if/canon/Adventure.htm). Don Woods discovered it at Stanford and
in 1977 roughly quadrupled it, from Crowther's ~700 lines to ~3,200, adding the dwarves, the
pirate, the magic, and the 350-point scoring
(https://en.wikipedia.org/wiki/Colossal_Cave_Adventure).

The interaction model that would dominate text games for fifteen years arrives fully formed
here: the **two-word verb–noun parser**. You typed `GET LAMP`, `GO WEST`, `KILL DRAGON`; the
game looked at "only the first five letters of each word" and matched against a fixed
vocabulary (https://jerz.setonhill.edu/if/canon/Adventure.htm). Crucially, the *world model
underneath* is a hand-coded data structure: a numbered set of rooms (locations) with text
descriptions and exit tables, a set of movable objects, and a pile of integer flags and
counters tracking state (lamp on/off, dwarf encountered, dam blown). The "anything you can
do" is exactly the finite cross-product of the verb list and the object list that Crowther
and Woods sat down and enumerated.

Scott Adams took the same model to the home micro with **Adventureland** in 1978 — plausibly
the first text adventure on a personal computer — and the smallness becomes explicit and
quantified, because now the constraint is a cassette-loaded 16K TRS-80
(https://ifdb.org/viewgame?id=dy4ok8sdlut6ddj7). Adams's parser recognizes only two-word
VERB-NOUN commands and only the first three letters of each word
(https://6502disassembly.com/a2-scott-adams/). His real innovation was an architectural one
aimed squarely at the size problem: he split the *engine* from the *world*, writing a small
interpreter that read a compact, data-driven **adventure database** of rooms, items,
vocabulary, and condition/action rules — so the same interpreter could run many games by
swapping the data (https://6502disassembly.com/a2-scott-adams/;
https://ifdb.org/viewgame?id=dy4ok8sdlut6ddj7).

**What kept it small.** Two walls, stacked. First the obvious one — memory: a world that
must fit, descriptions and all, in 16–60K of core is a world of dozens of rooms, not
thousands (https://en.wikipedia.org/wiki/Colossal_Cave_Adventure;
https://ifdb.org/viewgame?id=dy4ok8sdlut6ddj7). But the deeper, more durable wall is the one
that outlived the memory limits: **every room, object, verb response, and state flag was a
line a human wrote.** Adams's data-driven engine is the first clear statement of the
strategy that recurs for the next forty years — *separate the engine from the content so the
content can be authored as data* — and it is exactly the right move, and it does not
dissolve the wall. It just relocates it. The interpreter is reusable; the database is still
hand-typed, room by room, condition by condition.

---

## 4. Infocom / ZIL / the Z-machine (1977–1989) — the world model becomes a first-class object tree

Zork began as a hobby project by Tim Anderson, Marc Blank, Bruce Daniels, and Dave Lebling
at the MIT Dynamic Modeling Group around 1977, written in MDL (a Lisp dialect nicknamed
"Muddle"); the team founded Infocom in June 1979 to sell it
(https://www.inform-fiction.org/manual/html/s46.html; https://en.wikipedia.org/wiki/Z-machine).
The technical leap that makes Infocom matter to this lineage is the **Z-machine**, designed
by Joel Berez and Marc Blank in autumn 1979: a portable virtual machine whose Version 1
already "contained essentially all of the main architecture: the header, the memory divided
into three, the variables and stack, **the object tree**, the dictionary, the instruction
format" (https://inform-fiction.org/zmachine/standards/z1point1/appd.html).

That object tree is the headline. For the first time the **world model is a first-class data
structure in the runtime**: every room, creature, and item is an object node in a
containment tree, each carrying a set of boolean *attributes* (flags like takeable,
openable, lit) and numbered *properties* (descriptions, capacities, pointers), and the
parser and verbs operate generically over that tree
(https://inform-fiction.org/zmachine/standards/z1point1/appd.html;
https://en.wikipedia.org/wiki/Z-machine). The parser itself was far richer than the
two-word ancestors — Infocom games understood multi-object commands, prepositions, and
"all" — and games were authored in a purpose-built high-level language, **ZIL** (Zork
Implementation Language), distilled from MDL, compiled by ZILCH and assembled by ZAP into
Z-code that ran on any machine with an interpreter
(https://inform-fiction.org/zmachine/standards/z1point1/appd.html;
https://en.wikipedia.org/wiki/Z-machine). Write once, run on the Apple II, the IBM PC, the
TRS-80, the C64 — the Z-machine is why Infocom could ship one game to a fragmented hardware
market and dominate the early-80s charts
(https://inform-fiction.org/zmachine/standards/z1point1/appd.html).

**What kept it small.** The Z-machine solved *portability* and gave authoring a clean,
reusable substrate — an engine, a virtual machine, a generic object/attribute/property model
and a generic parser. None of that solves *content*. Each Infocom title was still a bounded,
hand-built world: a team designed every room, wrote every object's properties, and — the
expensive part — hand-authored every *response*, because the prized Infocom feel came from
specially-written reactions to things players might plausibly try. The world model was now a
first-class citizen of the runtime, yet its *extent* was still exactly what a human had typed
in ZIL. The wall didn't move; it just got a much nicer tool sitting in front of it. This is
the cleanest pre-LLM statement of the whole problem: a beautiful general engine, married to a
world whose every detail is hand-written, ships as a tight, finite, curated game.

---

## 5. The MUD lineage (1978 → 1990s) — persistent multiplayer worlds, still authored object by object

In parallel, the world model went *multiplayer and persistent*. Roy Trubshaw and Richard
Bartle built **MUD1** ("Essex MUD") at the University of Essex in 1978 on a PDP-10 — the
first Multi-User Dungeon, named in tribute to the *Dungeon* variant of Zork
(https://en.wikipedia.org/wiki/MUD1). Trubshaw wrote it first in PDP-10 assembly (MACRO-10),
rewriting it in BCPL in 1980 to save memory, and — the part that matters here — he built a
domain-specific **Multi-User Dungeon Definition Language (MUDDL)** so the world could be
declared as data; Bartle then "contributed much work on the game database, introducing many
of the locations and puzzles" (https://en.wikipedia.org/wiki/MUD1). Same pattern as Adams:
engine vs. content, world-as-authored-database. Same wall: the locations and puzzles are
Bartle's, typed out one at a time.

The two great codebase families of the late 80s/early 90s split precisely on *how much of
the world authoring they tried to delegate*, and the split is the most instructive thing in
this section:

- **LPMud** (Lars Pensjö, 1989) was born from an explicit refusal to be the sole author.
  Pensjö "wanted to create a world... but did not want to have sole responsibility for
  creating and maintaining the game world," so he split the system into a C *driver* (a
  virtual machine) and a *mudlib* written in a new, friendly, object-oriented soft-code
  language, **LPC** — designed so "people with minimal programming skills" could log in and
  add rooms, weapons, and monsters, concentrating on "building a room" rather than on
  programming logic (https://en.wikipedia.org/wiki/LPMud). This is the most direct pre-LLM
  attack on the authoring bottleneck: *make the world programmable from inside the world, by
  many hands, in soft-code.* It worked well enough to make LPMud one of the dominant MUD
  forms of the early 90s (https://en.wikipedia.org/wiki/LPMud).
- **DikuMUD** (DIKU, University of Copenhagen, 1990–91; Hammer, Madsen, Nyboe, Seifert,
  Stærfeldt) went the other way: it "hard-coded its virtual world," with areas, zones, rooms,
  objects, and mobiles defined as hand-authored static text data files rather than live
  soft-code (https://en.wikipedia.org/wiki/DikuMUD). It was easier to run and balance, became
  the template for the entire combat-MUD genre (Circle, Merc, ROM, SMAUG), and its lineage
  fed straight into EverQuest, Ultima Online, and World of Warcraft
  (https://en.wikipedia.org/wiki/DikuMUD).

From there the simulationist branch pushed *depth* hard — DartMUD (1991) and Discworld MUD
modeled materials, refining chains, heat that must be sustained, liquids and containers and
decay (covered for its design lessons in [`../prior-art.md`](../prior-art.md) §2). The
ambition was unmistakably "do anything sensible with the stuff of the world."

**What kept it small.** LPMud's soft-code is the single most important pre-LLM idea for the
content-scaling problem: it *multiplied the number of authors* by letting players become
builders. But multiplying authors is not the same as removing authoring — it is throwing
more human hours at the same per-object, per-room, per-response cost. Every LPC room is still
hand-written; every Diku area is still a person filling out object records; every
simulationist material on DartMUD is hand-specified. Persistence and multiplayer raised the
*value* of a big world (now many people inhabit it) without lowering the *unit cost* of
authoring one. MUDs got large only by accumulating volunteer-years, and they stayed bounded —
and uneven — by exactly the rate at which humans could type new world into them.

---

## 6. Inform & TADS (1987 → 2006) — the modern world-model engines, and the ambition of a general physics

When the IF *industry* collapsed in the late 80s, the *craft* moved to amateurs, and they
built proper authoring systems. Mike Roberts released **TADS** (Text Adventure Development
System) in 1987, with the influential TADS 2 arriving in 1992; Graham Nelson released
**Inform** in 1993, compiling down to — fittingly — Infocom's own Z-machine, which let
hobbyists run their games on the existing interpreter ecosystem
(https://www.inform-fiction.org/manual/html/s46.html;
https://en.wikipedia.org/wiki/Graham_Nelson). Both took the Infocom object model and
generalized it into a reusable library: a standard world model of rooms, things, containers,
supporters, doors, and actors, with a default physics of containment, light, reachability,
and movement that the author inherits for free and then extends. TADS 3 went further still,
shipping a built-in *multi-sensory* model where sight, sound, and smell propagate through a
connection graph (https://www.inform-fiction.org/manual/html/s46.html;
http://brasslantern.org/writers/iftheory/tads3andi7.html).

The clearest statement of the *ambition* — a general world model, not a bag of scripts — is
**Inform 7** (Graham Nelson, 2006). Inform 7 replaced procedural code with a declarative,
natural-language design language built on two big ideas: a built-in "Standard Rules" ontology
of *kinds* with spatial relations and actions, and **rulebooks** — control flow expressed as
ordered lists of rules consulted until one decides, rather than imperative branches
(https://ganelson.github.io/inform-website/book/WI_19_2.html;
https://en.wikipedia.org/wiki/Graham_Nelson). Nelson's own framing, from his white paper
*Natural Language, Semantic Analysis and Interactive Fiction*, is that IF is fundamentally a
**simulated world** that the design language exists to describe, and he notes the genre's
perennial tension between "recreating an experienced world" and dropping in "a really neat
puzzle" — "there is a Crowther and a Woods in every designer"
(https://www.cs.tufts.edu/comp/150FP/archive/graham-nelson/WhitePaper.pdf;
https://www.inform-fiction.org/manual/html/s46.html). The design dream is explicit: a world
where behavior is *additive and data-driven*, where any new object or relation slots into the
shared rule pipeline, where the author specifies a general physics and the engine applies it
uniformly.

**What kept it small.** Inform 7 is arguably the high-water mark of the hand-authored world
model — relations, rulebooks, kinds, a clean Check→Carry-Out→Report pipeline — and that is
exactly what exposes the ceiling so clearly. The engine generalizes *behavior*; it cannot
generalize *content*. Every kind, every object, every relation, every rule, and every
bespoke response is still a sentence the author writes. Inform gives you a magnificent
grammar for describing a world and zero help populating one. A general world model with no
general way to *fill* it is still, at ship time, precisely as large as one author's patience —
which is why even celebrated Inform works are a few dozen rooms deep. The tool got as good as
hand-authoring can get; the input was still hands.

---

## 7. Simulationist IF — "implement the physics, not the script," and the bill that comes due

The most philosophically pointed corner of this lineage is the **simulationist** school,
whose explicit creed is: don't script puzzle solutions, *model a physics* and let players
improvise solutions you never anticipated. Its standard-bearer is Emily Short.

**Metamorphoses** (2000) began, in Short's own words, as "just a test-space for my materials
library" — a sandbox to check whether wood, metal, glass, water, and so on "behaved as they
were supposed to do," with general categories for size (a 1–4 scale of human-manipulable
sizes) and shape (planar, rodlike, etc.) so that *general verbs* could act on any object by
its properties rather than by bespoke per-object code
(https://emshort.blog/how-to-play/writing-if/my-articles/making-of-metamorphoses-older/;
https://ifdb.org/viewgame?id=j61yaux1cqbptxyb). **Savoir-Faire** (2002) extended the same
object model — every object with size, shape, and material — and layered on the *Lavori
d'Aracne*, a "magical link" by which two sufficiently-similar objects are joined so "anything
that happens to one happens to both," turning the consistency of the underlying simulation
*into the puzzle mechanic itself* (https://ifdb.org/viewgame?id=p0cizeb3kiwzlm2p). The design
goal across both is that the player "becomes increasingly skilled at applying the rules of
the game-world" rather than guessing isolated puzzle solutions — a coherent physics you can
*reason inside* (https://emshort.blog/how-to-play/writing-if/my-articles/issues-in-simulation-older/).
Andrew Plotkin's **Hadean Lands** (Kickstarter 2010, released 2014) is the genre's
cathedral: a marooned alchemist's apprentice operating a deep, rule-governed alchemy — a
synthesized "physics" of elements, reagents, and rituals — where you experiment freely and,
once a ritual is mastered, the engine's goal-tracker lets you re-invoke "dozens of steps"
with a single command (https://emshort.blog/2014/10/30/hadean-lands-andrew-plotkin/;
https://zarfhome.com/press/hadean_lands.html).

**What kept it small — and here the authors say it themselves.** This school is the most
explicit pre-LLM evidence for the thesis, because its practitioners documented the bill.
Short is blunt that a fully general physical simulation "could get intensely fiddly to play,"
is "hard to write... because there would be a lot of form-filling," and would be "memory-
intensive and time consuming to write... especially if one started to account for things
like shape" — which is *why* she deliberately reduced her model to coarse size/shape
categories and concluded such systems "make most sense... in a small tight game environment"
(https://emshort.blog/how-to-play/writing-if/my-articles/issues-in-simulation-older/). Years
later she generalized it into a flat principle: "There is no such thing as a *generic* world
simulator. Any simulation is making decisions about what to model and what to ignore, what
level of abstraction to use, what kinds of state are interesting to preserve" — and, from
hard experience, "most of my development time... has gone into working and reworking the
content data, rather than refining the *process* of generation"
(https://emshort.blog/2018/07/10/mailbag-world-simulation-plug-ins/). Plotkin's number tells
the same story from the other side: **four years** building the puzzles and the custom IF
technology for one tightly-curated alchemical world
(https://zarfhome.com/press/hadean_lands.html), a body of underlying logic far larger than
its ~73,000 words of printed text (https://ifdb.org/viewgame?id=u58d0mlbfwcorfi).

So the simulationist school *proved the dream is real* — model a physics, and players really
do improvise sensible actions the author never scripted. And in proving it, it measured the
wall exactly: a believable physics demands that *every material's properties, every general
rule's interactions, and every state worth preserving be decided and authored by a human*,
and that cost is so steep that the genre's masterpieces are deliberately, necessarily
*small, tight, curated* worlds. The depth is hand-made. There was, before LLMs, no other way
to make it.

---

## The common thread

1. **The vision is old and stable.** From SHRDLU's blocks (1972) to Hadean Lands' alchemy
   (2014), the recurring dream is identical: *a text world you can do anything sensible in*,
   where a general engine resolves open-ended intent against a modeled reality
   (https://en.wikipedia.org/wiki/SHRDLU;
   https://emshort.blog/2014/10/30/hadean-lands-andrew-plotkin/). The ambition never needed
   LLMs and never went away.

2. **Two poles, and the gap between them is the whole field.** ELIZA had fluency with **no
   world model**; SHRDLU had a **deep world model** the size of a tabletop, "as few as 50
   words" (https://en.wikipedia.org/wiki/ELIZA; https://en.wikipedia.org/wiki/SHRDLU).
   Sixty years of work is the attempt to keep SHRDLU's grounded depth at ELIZA's apparent
   breadth — and the breadth is what kept failing.

3. **The bottleneck was never the engine — it was hand-authored content.** Every system
   converged on the same good architecture: separate a reusable engine from a world-as-data
   (Adams's database, Infocom's object tree + ZIL, MUDDL/LPC/Diku areas, Inform's
   kinds/rulebooks) (https://6502disassembly.com/a2-scott-adams/;
   https://inform-fiction.org/zmachine/standards/z1point1/appd.html;
   https://en.wikipedia.org/wiki/LPMud; https://ganelson.github.io/inform-website/book/WI_19_2.html).
   The engine generalized *behavior*; nothing generalized *content*. Each room, object,
   property, rule, and response stayed a line a person typed.

4. **Every attempt to scale authoring relocated the wall instead of removing it.** Data-
   driven interpreters (Adams), portable VMs (the Z-machine), soft-code crowdsourcing
   (LPMud's LPC), and declarative rulebooks (Inform 7) each *lowered the cost or multiplied
   the authors* of hand-authoring — but the unit was still "a human writes one more piece of
   world" (https://en.wikipedia.org/wiki/LPMud;
   https://ganelson.github.io/inform-website/book/WI_19_2.html). The asymptote didn't move.

5. **The practitioners named the ceiling out loud.** Winograd: demos that look good but
   lack "enough structure to make it really work more generally" — "Potemkin villages"
   (https://metadevo.com/potemkin-villages/). Short: "no such thing as a *generic* world
   simulator," a deep model is "time consuming to write," and content data — not the engine —
   eats the development budget, so deep simulation "makes most sense... in a small tight game
   environment" (https://emshort.blog/2018/07/10/mailbag-world-simulation-plug-ins/;
   https://emshort.blog/how-to-play/writing-if/my-articles/issues-in-simulation-older/). The
   wall was understood, not merely hit.

6. **Therefore worlds stayed small and curated — and that is exactly the lever LLMs move.**
   Across the lineage, world size tracked one variable: human authoring hours. The depth was
   always achievable by hand; the *extent* never was. The thesis this lineage tests is that
   LLMs change precisely the input these systems could never cheapen — the per-object,
   per-property, per-rule, per-response authoring of the world's ontology and content — while
   leaving every other lesson (engine owns state; behavior is data; model a physics, not
   scripts) intact and now, for the first time, fillable at density.
