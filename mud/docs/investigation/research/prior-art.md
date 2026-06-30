# Prior art — a systemic-world teardown for Whiteout

A multi-source web-research review of work relevant to building a text world where *as much
as possible can be done with everything*: a deterministic engine that owns state, an
objects→parts→materials model with conservation, ~20 composable operation categories, an
explicit perception model, and LLMs used to flesh out the ontology and interpret unbounded
intent. The brief throughout is **transferable lessons**, not summaries. Each sub-topic ends
with an explicit `Lesson for Whiteout`. The closing **Synthesis** distills the 6–8 most
load-bearing principles and a documented-failure-modes list.

The three killer risks this evidence is read against: **(R1)** the "do-anything" promise
hitting a wall; **(R2)** the ontology/content not being authorable at density; **(R3)** keeping
a deep world *fun*, not tedious.

---

## 1. Immersive sims / systemic games — how "everything interacts" was actually delivered or failed

### A. Breath of the Wild — multiplicative design and the chemistry engine
At GDC 2017, technical director Takuhiro Dohta framed BotW as a deliberate split between two
engines: a physics engine ("a rule-based movement calculator") and a parallel **chemistry
engine**, "a rule-based state calculator" governing non-constant elements like fire, water and
ice (https://www.thumbsticks.com/gdc-17-breath-of-the-wild-science-lies/). The chemistry engine
runs on just three rules: elements can change a material's state (leaves burn and disappear),
elements can change each other's state (water extinguishes fire), but plain materials cannot
change each other. Dohta's headline claim is the leverage of that minimalism: "The model is an
extremely simple one but allows for the expression of all sorts of events" (same source). The
elemental grid (fire/water/ice/wind/electricity over material tags like wood and metal) is just
these few rules applied uniformly to thousands of objects — which is what produces combinatorial
emergence instead of hand-built puzzles.

This is the **multiplicative vs additive** distinction (credited to director Hidemaro
Fujibayashi): additive design adds one bespoke interaction per object, so content scales
linearly; multiplicative design makes every object obey the same shared verbs, so each new
object *multiplies* against all existing ones — "physics and chemistry allow for intuitive (and
seemingly endless) solutions, such as fanning a bomb to propel it or cutting down a tree to
cross a gap" (https://www.engadget.com/2017-03-12-breath-of-the-wild-gdc-talk.html). The rules
are anchored to real-world expectation (metal conducts lightning, fire burns wood, wind pushes),
so players learn affordances by intuition, not tutorials. Dohta also stressed these are
deliberately "clever lies" tuned for control and responsiveness, not textbook accuracy, and the
team validated the whole interaction system first in a **top-down 2D NES-style prototype** so
they could "test out the real thing, rather than an approximation" before committing to 3D —
proving the systemic core lived in the rules, not the rendering
(https://www.gamedeveloper.com/design/video-designing-i-zelda-breath-of-the-wild-i-s-unconventional-mechanics).

`Lesson for Whiteout:` Keep the operation set small and uniform, and anchor each operation to
real-world intuition so players predict outcomes without being taught; prove the full
operation×material *interaction matrix* in the cheapest representation you have (text) before
investing in content density — this is exactly the brainstorm's "vertical ontology slice first."

### B. Prey (2017) / Deus Ex / System Shock — the imsim lineage, and where it leaks
The immersive-sim pillar (traceable through Looking Glass to Warren Spector, who coined
"immersive simulation") is "a consistent series of rules and systems… [that] can be exploited by
the player to complete objectives in unique and unpredictable ways," producing "emergent
gameplay beyond what has been explicitly designed" (https://en.wikipedia.org/wiki/Immersive_sim).
The "0451" lineage (System Shock → Deus Ex → Dishonored → Prey; Harvey Smith, Raphael
Colantonio) defines quality as multi-use **systemic verbs**, not single-purpose actions: Prey's
GLOO Cannon paralyzes enemies, builds climbable platforms to off-limits areas, caps electrical
hazards, and snuffs fires — one verb, many uses. The **Recycler/Fabricator** loop makes matter
conserved and fungible: objects break into raw material types that re-fabricate into other items,
with diegetic visual feedback so the player "witnesses every step" rather than using an abstract
menu (https://www.narrativedesign.net/p/prey-2017-game-design-lessons). Mimics (enemies disguised
as ordinary props) weaponize the systemic promise itself: because *any* object is potentially
interactive, paranoia becomes gameplay.

But the systemic promise visibly **leaks** wherever designers fall back to authored,
non-systemic content. The same analysis flags Prey's hacking and weapon-upgrade screens as
"bland, frustrating" menu abstractions that break the emergent loop, and progression stays gated
by authored neuromod availability and narrative pacing
(https://www.narrativedesign.net/p/prey-2017-game-design-lessons). The genre's standing tension,
per Harvey Smith, is that systemic richness is expensive to build against modest sales — the wall
is economic as much as technical (https://en.wikipedia.org/wiki/Immersive_sim).

`Lesson for Whiteout:` Favor few verbs that each do many things (one join/separate-matter
operation should serve traversal, defense, and crafting), and make conservation-of-matter
diegetic and legible (Prey's recycler is the model for Whiteout §24); but expect the seam to show
wherever you bolt on a non-systemic exception — keep authored packets rare (radio/beacon/pilot
only) and dressed as world-fiction, never as a menu.

### C. Dwarf Fortress / Caves of Qud — depth and its documented cost
Dwarf Fortress is the maximal case. Every material has raw-defined `MELTING_POINT`,
`BOILING_POINT`, `IGNITE_POINT` and specific-heat tokens, and heat propagates each tick (an item
shifts toward ambient by the difference divided by its specific heat), so phase changes,
magma-safety, water freezing/evaporating, and notorious accidents (acidic blood tracked on cloth
shoes melting a dwarf's feet) all *emerge* from one consistent material-property simulation
rather than scripts (https://dwarffortresswiki.org/index.php/Temperature). Caves of Qud gets
similar emergence from a uniform entity-component model — Jason Grinblat's example of dropping a
Brain component onto a table yielding "a walking, talking table" shows how component-uniformity,
not bespoke content, generates surprise, and Wander mode lets the world "play out emergently as
if you weren't there"
(https://www.gamedeveloper.com/design/tapping-into-the-potential-of-procedural-generation-in-caves-of-qud).

The **cost is heavily documented**. DF's temperature math is "a known cause of lag," to the point
the game lets you disable it for FPS, and large fortresses inevitably hit "FPS death" where the
simulation outgrows the CPU (https://dwarffortresswiki.org/index.php/Temperature). Qud's depth
imposes an interface/learning cliff: reviewers call it "impenetrable," with hundreds of shortcuts
and learning-through-death that is "exhaustingly time consuming," only partly mitigated by the
1.0 UI overhaul (https://www.gaming.net/reviews/caves-of-qud-review/).

`Lesson for Whiteout:` A uniform property-and-component model buys vast emergence cheaply, but
budget explicitly for the two failure modes these games hit — *simulation cost* (cap tick-rate
and active-object scope per room; instanced ~one-day runs make this tractable) and the
*perception/UI burden* (Whiteout's explicit perception model must surface affordances legibly, or
depth reads as tedium — see §1 cross-cutting and the Koster point in §2).

### Cross-cutting (immersive sims) — what holds, how players discover, where the wall appears
Consistency holds when a *small* rule set is applied *uniformly* to all objects and grounded in
intuition (BotW's three chemistry rules; DF's per-material properties; Qud's components) —
uniformity, not quantity, makes a system feel trustworthy and learnable. Players discover
affordances by **transfer**: once a rule is learned on one object they assume it everywhere, so
real-world-aligned rules need no tutorial, and "everything is interactive" can itself become
content (Prey's mimics). The **wall** — the edge of the simulation (R1) — appears at two
predictable seams: (1) authored, non-systemic exceptions that break the spell, and (2) the cost
ceilings of depth (DF's FPS death, Qud's UI cliff). Good games hide it by dressing gates as
fiction, scoping the simulation tightly enough to stay performant, and investing in legibility so
the player perceives the systemic affordances rather than drowning in them.

---

## 2. Deep MUDs — depth vs tedium, and multiplayer survival pacing

### A. Discworld MUD — skills and deep crafting
Discworld organizes hundreds of skills into seven/eight top-level groups (adventuring, covert,
crafts, faith, fighting, magic, people) that branch into sub- and sub-subskills, each carrying a
numeric "bonus" that drives every skillcheck (https://dwwiki.mooo.com/wiki/Skills). The
anti-grind heart is the **TaskMaster ("TM")** system: simply *using* a skill gives a chance to
advance it for free, and that chance peaks at roughly a 50% pass probability — so the optimal way
to improve is to keep attempting tasks at the *edge of your competence*, not to repeat trivial
ones (https://dwwiki.mooo.com/wiki/Skills). Crafting is genuinely deep: smithing/finesmithing is
multi-step (forge from a pattern, with a chosen metal, on a workbench), and final quality is set
mostly by the first couple of steps plus your specific subskill bonus, while the material
(white/black/rose gold, electrum, platinum, silver, bronze…) sets price and *which* skill applies
(https://dwwiki.mooo.com/wiki/Crafts.smithing). Output feeds player-run craft shops. Notably,
*amount* of metal often doesn't change value — *quality* does — which keeps players chasing
better, not more.

`Lesson for Whiteout:` Tie skill/competence growth to attempts made at ~50% difficulty (reward
operating at the frontier, not repetition), and make crafted quality depend on early decisive
decisions and the right specialized operation rather than raw material *quantity*, so depth reads
as mastery rather than throughput.

### B. Armageddon MUD — survival stakes and permadeath
Armageddon (1990–2024) was a roleplay-*enforced* desert sim where thirst is coded survival
pressure: persistent "you are very thirsty" messages, and characters literally die without water
— which pushes players into the game's real stories (dangerous journeys, theft, swearing fealty
to water-controlling clans) rather than making thirst a meter to top off
(https://www.cabinetmagazine.org/issues/64/lucas.php). Permadeath is the narrative gravity: loss
is described as a draft burning in your hands, which makes every decision consequential and
sustains a culture where ~98% of play is in-character
(https://en.wikipedia.org/wiki/Armageddon_(MUD)). The transferable insight: survival mechanics
felt meaningful *because they were levers into emergent social/political story*, not because they
were realistic. The crafting system shows the opposite edge — players found it arbitrary and
grindy: branching trees lock you into a path, recipes are deliberately obscure, and skilling up
can take "like 5 years RL" of repetition to branch
(https://armageddonmud.boards.net/thread/13/crafting-skills-megathread).

`Lesson for Whiteout:` Make survival pressure *route players toward each other and toward stories*
(scarcity solved socially), and let consequences be heavy enough to matter — but avoid
Armageddon's crafting trap of opaque, lock-in, repetition-gated progression; the survival loop
earns its weight, the chores must not.

### C. Material / crafting / simulation depth across text MUDs
DartMUD (1991) is the cited gold standard for simulationist crafting and player-run economy: raw
skills (farming, fishing) yield materials, intermediate skills (metallurgy, milling) refine them,
and finishing skills (smithing, chandlery) produce goods — a forge needs the right ores, ingots
and fuel, must be pumped to temperature, and must *retain heat* over time
(https://mud.fandom.com/wiki/DartMUD). Discworld itself runs surprisingly deep "physics": vessels
hold liquids with sip/taste/drink/fill/empty/splash verbs, perishables decay to dust, special
containers slow rot, and you can evaporate seawater in a salt pan to harvest salt
(https://dwwiki.mooo.com/wiki/Liquid_containers, https://dwwiki.mooo.com/wiki/Decay) — directly
relevant to a conservation-of-matter model. On depth-vs-tedium, Raph Koster's framing is
decisive: fun is the dopamine of *learning/mastery*, and an activity becomes "grind" precisely
when the pattern is fully learned and nothing new remains — same challenge, no new insight
(https://www.raphkoster.com/2005/12/16/do-levels-suck/).

`Lesson for Whiteout:` Simulation depth (heat that must be sustained, liquids/containers, decay,
refine-chains) is engaging only while it keeps *teaching* — so gate matter-conservation systems
behind *decisions* (what to combine, how to route heat/wetness) and **auto-abstract or batch any
step whose pattern players have fully mastered** before it curdles into busywork (this is the MUD
evidence for Hadean Lands' action-chunking in §3C).

### Cross-cutting (deep MUDs) — pacing and teaching a verb-rich space
(1) *Depth becomes busywork the moment it stops teaching* (Koster) — Whiteout's ~20 operations
stay fun while their *combinations* yield new outcomes, and turn dangerous when a known recipe
must be re-typed. (2) *Multiplayer survival pacing*: Armageddon kept thirst meaningful by making
it social/political, not by tightening the meter; routine maintenance should be delegable,
batchable, or solved through other players, with scarcity/permadeath reserved for genuinely
story-bearing moments. (3) *Teaching the command space*: Discworld's verb-noun grammar with
per-command and per-object/location help (`help here`, `help <object>`) progressively reveals the
verb space (https://dwwiki.mooo.com/wiki/Skills) — a model where Whiteout's LLM intent-parser
absorbs unbounded phrasing while contextual help teaches the underlying operation vocabulary.

---

## 3. Parser interactive fiction + world models

### A. Inform 7 — declarative rulebooks + relations as an "everything interacts" model
Inform 7 ships a mandatory "Standard Rules" extension defining the baseline ontology and physics:
kinds (room, thing, container, supporter, person, door), spatial relations, and the actions that
manipulate them (https://ganelson.github.io/inform-website/book/WI_19_2.html). Control flow is
not imperative code but **rulebooks** — "a list of rules to be followed in sequence until one of
them makes a decision," each with a default outcome
(https://inform-7-handbook.readthedocs.io/en/latest/chapter_4_actions/rulebooks_&_stop_the_action/).
Every action runs a fixed pipeline — **Before → Instead → Check → Carry Out → After → Report** —
with a clean division of labor: Check blocks illegal actions and *says why*; Carry Out actually
mutates world state and "must not block… and should not say anything"; Report narrates
(https://ganelson.github.io/inform-website/book/WI_12_9.html). **Relations** are the second
pillar: "Relations are what sentences express… yes/no questions about pairs of things," so the
verb is decoupled from the relation it expresses, and authors can mint arbitrary new relations
between any kinds (https://ganelson.github.io/inform-website/book/WI_13_3.html). The power for
"everything can interact" is that behavior is *additive and data-driven*: any new object,
condition or relation slots into the same shared pipeline without rewriting the engine, and
conflicts resolve by rule ordering/specificity rather than nested conditionals.

`Lesson for Whiteout:` Model each of the ~20 operation categories as a fixed
Check→CarryOut→Report pipeline over relations — conservation lives in Check (veto + reason),
state mutation in CarryOut, perception in Report — and let LLM-authored content add *rules and
relations, never new control flow*. This is what keeps a combinatorial interaction space
authorable (R2) and maps directly onto the brainstorm's three resolution modes.

### B. TADS 3 — the sense-passing model
TADS 3's library is class/inheritance-heavy and is best known for a built-in *multi-sensory*
simulation: senses (sight, sound, smell) propagate through a connection graph, with first-class
"sensory emanations" — objects representing a smell or a sound that exist and travel
independently of their source — and fine control over *how* sense data passes between locations
(a noise audible through a door but a smell not) (http://brasslantern.org/writers/iftheory/tads3andi7.html).
Inform's default model is leaner and containment-centric, pushing rich perception into author
code.

`Lesson for Whiteout:` Since Whiteout already promises an explicit perception model (the
brainstorm's best idea), treat percepts (a smell, a sound, a heat signature) as **first-class
engine objects that propagate along a sense graph separate from the matter graph** — TADS shows
this is what makes a survival world feel physically present, and that it must be engine-owned and
deterministic, not author-improvised per object.

### C. Hadean Lands — the ritual planner/compiler against crafting tedium
Andrew Plotkin's alchemy game has the player perform multi-step rituals; its key innovation is
*action chunking*: once a ritual succeeds, the engine memorizes the whole process so the player
gains meta-commands like `CREATE HEALING POTION` that "auto-executed the steps — sometimes dozens
of steps — required," and any previously-solved puzzle re-solves with one command, the
goal-tracker even routing/gathering prerequisites
(https://emshort.blog/2014/10/30/hadean-lands-andrew-plotkin/). The reviewer is explicit that
"if it weren't for the action-chunking feature, this would make the game maddeningly repetitive,"
and that automation *shifts the challenge from execution to strategy* — optimizing which rituals
to run given scarce ingredients (same source).

`Lesson for Whiteout:` The first time a player discovers a crafting chain it is a puzzle; every
time after it must collapse to **one intent-level command the engine replans against current
world state** (substituting equivalent materials, re-gathering inputs). Auto-chunk *known*
procedures so tedium evaporates while novelty and scarcity stay the real game — the single most
important concrete antidote to R3.

### D. Versu / Praxis — declarative social state + permissible actions as affordances
Versu (Richard Evans & Emily Short) models characters as autonomous, utility-driven agents over a
shared world state written in *Praxis*, a logic DSL whose world is "a set of sentences in…
exclusion logic" (https://emshort.blog/2013/02/14/introducing-versu/). Crucially, social
practices are first-class objects implemented as reactive joint plans that "never control the
agents directly; they merely provide suggestions" — i.e. *affordances* — and each agent
independently chooses via utility. Short's example: a character "fell silent" when an
uncomfortable party entered, with no special-case authoring, because permissibility fell out of
the declared social state. The transferable core is the clean split between *state* (declarative
facts) and *available actions* (affordances computed from that state).

`Lesson for Whiteout:` Compute the set of *permissible operations* as affordances derived from
declared world state (material, temperature, adjacency, tool-presence) rather than hard-coding
interactions; the LLM then maps player intent onto this **generated affordance set**, which both
bounds the do-anything promise (R1) and gives a legible menu of what is actually possible right
now.

### E. Curveship — separating world-events from how they're told
Nick Montfort's Curveship cleanly splits the *storyworld* (a simulator of actors, items, rooms,
events) from *narrative discourse* (the telling), via a Simulator→Teller architecture: the
Simulator emits first-order event representations and the Teller renders them under a chosen
"spin" — temporal order, focalization/narrator, person, tense — so the same events narrate many
ways (https://nickm.com/curveship/).

`Lesson for Whiteout:` Keep the deterministic engine's event log as neutral, structured fact, and
make the LLM purely a *Teller* that renders those events into prose per player's perception and
perspective. This separation lets you re-narrate identical state for different observers,
regenerate text without touching world state, and audit the engine independently of the prose
(it operationalizes the brainstorm's "narration must never imply unmade state").

### Cross-cutting (parser IF) — intent legibility, mis-parse, disambiguation
Plotkin separates two parser stages: *matching* (a yes/no filter keeping objects that share the
player's typed words) and *disambiguation* (a ranked score that picks the best candidate or asks
"Which do you mean?"), noting that by disambiguation "the parser has forgotten which specific
words the player used" — a flaw that makes naively adding synonyms backfire
(https://blog.zarfhome.com/2024/01/parser-if-disambiguation). Inform mitigates this with liberal
`Understand` rules mapping many synonyms/adjectives (including conditional understandings like
"cracked" only when the vase is broken), `Does the player mean` rules that *rank* candidates so
the parser silently picks the most likely instead of nagging, and a customizable
"asking which do you mean" activity that fires only on genuine ambiguity and produces readable
prompts (https://ganelson.github.io/inform-website/book/WI_18_31.html). The community lesson on
guess-the-verb is to be generous with synonyms, normalize equivalents (get/take), drop filler
words, and emit *guiding* error messages rather than flat rejection
(https://emshort.blog/2010/06/07/so-do-we-need-this-parser-thing-anyway/).

`Lesson for Whiteout:` Never hard-reject unparsed intent. Score candidate `(operation, target)`
interpretations, auto-resolve when one clearly dominates, ask a *targeted* clarifying question
("the red key or the blue key?") only when scores tie (the brainstorm's intent-confirmation
affordance), and when intent has no engine realization, **fail informatively by surfacing the
nearest available affordances** ("you can't weld snow, but you could melt or compress it") —
turning the do-anything wall into a legible redirect (R1) and preserving "no `You can't do that.`
ever ships."

---

## 4. ML / LLM text worlds — using LLMs without losing determinism or hallucinating state

### A. Microsoft TextWorld — logic-based state, language as a view
TextWorld is a sandbox where text games "emerge from a set of underlying world mechanics," and
the *engine*, not any neural net, owns state (https://arxiv.org/abs/1806.11532). Internally it is
logic-based: world state is a set of first-order **facts/predicates** (`on(apple, table)`,
`closed(door)`), actions are rules with preconditions and effects, and a **knowledge base** of
types/predicates/rules drives both generation and a built-in solver. Games are generated by
sampling a world graph then **chaining rules backward from a goal** to guarantee a winnable quest
of controllable length; surface text renders separately (it can compile to Inform 7), so language
is a *view* over symbolic state (https://github.com/microsoft/TextWorld).

`Lesson for Whiteout:` Model the deterministic core exactly this way — typed objects + predicate
facts + precondition/effect operation rules — treating the ~20 operation categories as the rule
schema; generate/validate scenarios by *chaining operations* so solvability is provable (the
brainstorm's fuzz harness), and keep prose a pure render of facts.

### B. ScienceWorld — small action set, rich property simulation
ScienceWorld is a hand-authored deterministic symbolic simulator of ~10 rooms and up to ~200
object types, with **25 high-level actions** that expand to ~200k legal action-object pairs
(https://arxiv.org/abs/2203.07540). Objects carry physical *properties* (temperature, state of
matter, conductivity) and the engine runs simplified **thermodynamics (heat transfer,
melting/boiling/freezing), electrical circuits, chemistry and biology** to update them
deterministically each tick (https://www.emergentmind.com/topics/scienceworld-benchmark) — almost
exactly Whiteout's change-temperature/wetness/shape operations with conservation-style updates.
The paper's headline finding — strong LLMs can *recite* that copper conducts but fail to *run the
experiment* — is itself the case for a real engine.

`Lesson for Whiteout:` A small, fixed set of property-mutating processes (heat, wetness, phase
change) hand-coded as deterministic update functions buys enormous emergent depth; you don't need
*many* operations, you need *composable* ones over rich object properties (R1/R2).

### C. Jericho — engine-computed "what's actually possible here"
Jericho wraps real Z-machine IF and exposes two engine-owned primitives agents can't fake: a
**world-object tree** (the parsed hierarchy of rooms/objects/inventory) and a
**valid/admissible-action** detector that fills templates with in-scope objects, executes each
against the engine, and keeps only those that *actually changed* the world-object tree
(https://github.com/microsoft/jericho). It also leans on determinism (fixed seeds) plus load/save
to enable search/planning (https://ojs.aaai.org/index.php/AAAI/article/view/6297/6153).

`Lesson for Whiteout:` Expose an engine-computed affordance list derived by *trial-applying*
candidate operations to current state. This grounds the LLM intent-parser (it picks from real
affordances rather than inventing them) and is a direct antidote to the do-anything wall (R1) —
the wall becomes a graceful, engine-honest "no valid operation" instead of a hallucinated
success. This is the implementation of the brainstorm's Versu-style permissible-action set.

### D. ALFWorld — two aligned views (abstract reasoning, concrete execution)
ALFWorld's core idea is **two aligned views of one world**: an abstract TextWorld (high-level text
actions, PDDL-style state) and a concrete embodied ALFRED simulator, kept in correspondence so a
policy learned in the cheap abstract world transfers to the expensive concrete one
(https://arxiv.org/abs/2010.03768). Reasoning happens in the abstract symbolic layer; execution
is grounded in the detailed layer.

`Lesson for Whiteout:` Deliberately separate an **abstract operation/ontology layer** (where the
LLM plans and players express intent) from the **concrete material/part/conservation layer**
(where the engine resolves physics). Author and reason at the abstract level; let the engine
"compile" abstract operations down to concrete material-state changes — the alignment is what lets
you scale content without re-deriving physics each time.

### E. LIGHT — density via crowdsourcing + structured affordances
LIGHT is the density proof-point: a crowdsourced fantasy world of **663 locations, 3462 objects,
1755 characters** plus 11k interaction episodes, all in natural language but with each object
carrying structured **attributes/affordances** (gettable, wieldable, edible, container…) a game
engine enforces independently of the dialogue models
(https://aclanthology.org/D19-1062.pdf). A follow-up used models to *propose* new
locations/characters/objects that humans curated — model-assisted authoring, not model-as-
authority (https://parl.ai/projects/light/).

`Lesson for Whiteout:` The "ontology authorable at density" risk (R2) is beatable by making the
LLM a *content proposer* that emits structured, schema-constrained object/part/material entries a
validator and human curator accept — the engine still owns the typed attributes; the LLM fills
the long tail.

### F. Stanford Generative Agents (Smallville) — borrow the loop, fear the cost
Park et al. give believable NPCs via a **memory stream** (timestamped observations scored by
recency/importance/relevance), periodic **reflection** (synthesizing higher-level facts), and
recursive **planning** (https://hai.stanford.edu/news/computational-agents-exhibit-believable-humanlike-behavior).
Transferable: the retrieval-scored memory and reflect/plan loop. Fragile/expensive: it is
token-hungry and slow (many LLM calls per agent per tick), and coherence still drifts because
memory is free-text, not ground truth.

`Lesson for Whiteout:` Borrow the memory-stream/reflection pattern only for NPC *characterization
and chatter*, and keep NPC-relevant *facts* in the deterministic store; budget aggressively
(cache, summarize, act on ticks) or per-agent LLM cost and latency will sink a multiplayer MUD.

### G. AI Dungeon — the canonical LLM-as-world-model failure
AI Dungeon is the canonical collapse: there is **no persistent ground truth**, only a fixed
context window (historically ~4k tokens for free tiers). When events scroll off the top, "most of
the time it's just making it up," producing contradictions, resurrected dead characters and
vanished items (https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up). The fixes
are bolt-on retrieval (Memory Bank / Plot Essentials) that *re-inject* summaries — a patch, not
state ownership (https://help.aidungeon.com/faq/the-memory-system).

`Lesson for Whiteout:` This is precisely the architecture *not* to build. State lives in the
engine; the LLM is never the source of truth for what exists. Anything the LLM "remembers" must be
reconstructable from the deterministic store, or it will drift.

### H. LLMs as / over world models (2023–2025) — author the model, don't step it
Three concrete data points. (1) *Can Language Models Serve as Text-Based World Simulators?*
(Wang et al., ACL 2024) measured GPT-4 directly at ~**59.9%** on whole-state dynamic transitions,
dropping to **49.7%** on environment-driven (non-action) dynamics, with errors concentrated in
arithmetic, physics and common sense — and error compounds over steps, so direct LLM simulation
is unreliable (https://aclanthology.org/2024.acl-short.1/). (2) *RAP* repurposes the LLM as a
world model inside MCTS planning — useful for *reasoning*, but still neural-state and best for
closed puzzles (https://arxiv.org/abs/2305.14992). (3) Guan et al. (NeurIPS 2023) is the winning
pattern: the **LLM writes PDDL** (a symbolic world model), validators + a human correct it once,
then a sound **symbolic planner** runs the loop — "keeping the LLM out of the planning loop"
yields correctness guarantees
(https://proceedings.neurips.cc/paper_files/paper/2023/hash/f9f54762cbb4fe4dbffdd4f792c31221-Abstract-Conference.html);
NL2Plan and "LLMs as Planning Domain Generators" extend this
(https://arxiv.org/abs/2405.06650).

`Lesson for Whiteout:` Never let the LLM *step* the simulation. Use it to *author the symbolic
model* (operation schemas, object/material definitions in your formal format) under validation,
and to *parse intent* and *narrate* — the deterministic engine does every state transition.

### Cross-cutting (ML/LLM) — LLM at the edges, hard symbolic authority at the core
The consistent winning shape across A, C, D and H: a **symbolic state authority** (typed facts +
precondition/effect rules) is the *only* thing allowed to mutate state, with LLMs confined to
three edges — (1) **content authoring**: emit schema-constrained ontology entries a
validator/human accepts before they enter the world (LIGHT, Guan); (2) **intent parsing**: map
unbounded player text onto the *engine-computed set of valid operations* (Jericho's
admissible-action handler), so "do anything" degrades to an honest "no operation matches" rather
than a fabricated outcome; (3) **narration**: render engine facts into prose, reading state but
never writing it (Curveship's Teller). Determinism is preserved because the LLM proposes and the
engine disposes; hallucinated state is impossible because every player-visible fact must be
reconstructable from the symbolic store (the AI Dungeon anti-pattern). This *is* the brainstorm's
three resolution modes — hard mechanics / soft-judge-on-rails-with-clamp-and-cache / pure prose.

---

## 5. Commonsense / qualitative-physics ontologies — designing the operation × material engine

### A. Gibson's affordances — index by action, not object class
Gibson coined "affordance" for what the environment *offers* an agent — action possibilities that
exist relationally, in the fit between an agent's capabilities and a thing's physical properties,
not in the object or the mind alone (https://en.wikipedia.org/wiki/Affordance). His canonical
examples (a rock affords sitting *to a human but not a fish*) make the point that the same matter
offers different verbs to different agents in different states. Don Norman ported this into design
but sharpened a distinction Whiteout must respect: what matters operationally is the *perceived*
affordance, which can diverge from the real one, yielding *hidden* affordances (real but unseen)
and *false* affordances (perceived but absent) (https://jnd.org/affordances-and-design/).

`Lesson for Whiteout:` Index the ontology by affordances (operation availability) computed from
*material properties + agent capability*, not by object class — and split the model in two: the
engine's *real* affordances (what conservation/material state actually permits) versus the
*perceived* affordances the perception model and LLM narrate. The gap between them is your puzzle
and your do-anything honesty boundary: surface hidden affordances on inspection; never narrate
false ones (R1/R3).

### B. Forbus's Qualitative Process Theory — the closest formal analog
QPT is the canonical formalism for reasoning about physical change *without numbers*. Its central
claim: "Every change in the physical system is directly or indirectly caused by processes"
(https://www.qrg.northwestern.edu/ideas/qptidea.htm), where a process has five slots —
individuals, preconditions, quantity conditions, relations, and *influences* — and only processes
carry direct influences on quantities. Quantities live in a *quantity space* of ordinal
inequalities, and *qualitative proportionalities* chain them. The companion tradition, de Kleer &
Brown's "A Qualitative Physics Based on Confluences" (AI 24, 1984), models each variable as just
+, −, or 0 and links them via confluences capturing competing tendencies
(https://dekleer.org/Publications/Scanned%20AIJ.pdf). This is almost exactly Whiteout's
"operations change material quantities": Whiteout's operations *are* QPT processes, its material
properties *are* the quantities.

`Lesson for Whiteout:` Model each of the ~20 operations as a QPT-style process with explicit
preconditions, quantity conditions, and *influences* on material properties; represent properties
*qualitatively* (a quantity space like cold<cool<warm<hot, with named thresholds — exactly DF's
freezing/ignition points) rather than raw floats, so the **LLM reasons about direction and
ordering of change (which it does well) while the deterministic engine owns the numeric
bookkeeping and conservation** (this resolves the brainstorm's LLM↔determinism seam at the
representation level).

### C. SHRDLU / blocks world — the cautionary closed microworld
Winograd's SHRDLU conversed in English to manipulate a blocks world whose *entire* object/location
set could be described in ~50 words (https://en.wikipedia.org/wiki/SHRDLU). Language stayed
interpretable *precisely because* the domain was tiny and fully modeled. It did not scale — rules
were hardcoded to the microworld — and Winograd later disowned the demo-driven approach as
building "Potemkin villages" lacking "enough structure to make it really work more generally"
(https://en.wikipedia.org/wiki/SHRDLU). The lesson is not "microworlds fail" but "language is
interpretable *only* over a closed, fully-modeled domain."

`Lesson for Whiteout:` A bounded, exhaustively-modeled material/operation ontology is the
*enabling* constraint, not a limitation — keep the operation vocabulary small and total (the ~20
verbs) so player intent always resolves onto something the engine models; bound the verbs, let
materials/objects be the open axis. The failure mode to avoid is letting the LLM imply affordances
the closed engine can't honor (the do-anything wall, R1).

### D. ConceptNet & ATOMIC — seed the ontology, never trust it as ground truth
ConceptNet 5.5 is a multilingual graph whose edges are exactly the relations Whiteout needs —
`UsedFor`, `CapableOf`, `MadeOf`, `HasProperty`, `PartOf`, `ReceivesAction`, `AtLocation`
(https://arxiv.org/pdf/1612.03975) — a natural seed for object→material→affordance triples. ATOMIC
adds 877k *if-then* inferential triples (https://arxiv.org/abs/1811.00146), a precondition→effect
shape mirroring operation schemas. But the weaknesses are severe for grounding a deterministic
engine: ConceptNet is *sparse* (over half its concepts have a single assertion) and *noisy*
(~15.5% of assertions judged false/vague), lacks word-sense disambiguation, and has no grounding
(https://arxiv.org/abs/2011.14084). Separately, COMET shows a fine-tuned LM can *generate*
commonsense triples humans rate highly (approaching human quality on ATOMIC/ConceptNet)
(https://arxiv.org/abs/1906.05317) — evidence an LLM can densely populate an affordance/property
ontology that hand-authoring and KB-mining cannot reach.

`Lesson for Whiteout:` Mine ConceptNet/ATOMIC to *bootstrap candidate* affordances and material
properties (great for breadth and human-plausible verbs), but never trust them as ground truth —
every seeded property/affordance must be validated against the conservation-and-property engine
before it's canonical, and the sparse long tail must be *generated* (COMET-style) and gated by
validation, not retrieved (R2).

### E. Operation-over-property formalisms — the action schema
STRIPS/PDDL is the canonical "operation" formalism: an action = parameters + *preconditions*
(atoms that must hold) + *effects* (add/delete literals), with the domain (general actions/types)
cleanly separated from the problem instance (objects, initial state, goal)
(https://www.primaryobjects.com/2015/11/06/artificial-intelligence-planning-with-strips-a-gentle-introduction/).
This maps one-to-one onto Whiteout: each of the 20 operations is an action schema; material-
property predicates/quantities are its preconditions and effects; conservation is a global
invariant on the effect set. For the *property tables*, Dwarf Fortress is the proven game-scale
precedent — materials are defined in raw files by numeric, threshold-style tokens (melting/boiling/
ignition point, specific heat) the simulation reads uniformly
(https://dwarffortresswiki.org/index.php/DF2014:Material_science).

`Lesson for Whiteout:` Make every operation a declarative precondition/effect schema over a
*fixed property schema* (like DF's material tokens), so operations are **data, not code**, and the
LLM authors *table rows* (property values, thresholds) against a fixed column set rather than
free-form behavior — the engine, not the LLM, applies effects and enforces conservation (R2 +
determinism).

### Cross-cutting (qualitative physics) — designing the engine and having the LLM fill it
Three convergent lessons. (1) *Fix the verbs and the schema; open only the data.* SHRDLU and PDDL
both show interpretability comes from a closed, total operation vocabulary over a fixed predicate/
property schema; the LLM's job is filling rows, never inventing operations or effects. (2) *Make
the LLM reason qualitatively, the engine quantitatively.* QPT/confluences show physical change is
reliably expressible as direction-of-change over ordinal quantity spaces — exactly the regime LLMs
handle well — while the deterministic engine owns the numbers and conservation. (3) *Generate,
then validate.* COMET-style generation can populate density that hand-authoring and ConceptNet-
mining cannot — but only into a *constrained schema* and gated by validation against engine
invariants.

---

## 6. Synthesis — the most transferable lessons for Whiteout

Each lesson is one sentence of **principle** + one of **application**.

1. **Few uniform verbs beat many bespoke interactions.** *Principle:* combinatorial richness comes
   from a *small* operation set applied *uniformly* to many objects (BotW's three chemistry rules;
   ScienceWorld's 25 actions → 200k pairs), not from per-object content. *Application:* treat the
   ~20 operation×material rules as the actual engine and authored object-packets as the rare
   exception — exactly the brainstorm's inversion.

2. **Symbolic engine owns state; the LLM lives only at three edges.** *Principle:* the proven
   architecture (TextWorld, Jericho, Guan et al.) is a symbolic state authority that alone mutates
   state, with the LLM confined to authoring, intent-parsing, and narration. *Application:*
   implement the three resolution modes — hard mechanics (engine only) / soft adjudication
   (LLM-judge-on-rails, clamp + cache) / pure prose — and make every LLM output a *proposal* the
   engine can veto.

3. **Compute affordances from state; parse intent against them.** *Principle:* permissible actions
   should be *derived* from declared world state (Versu) and verified by trial-application
   (Jericho), giving an engine-honest "what's possible here." *Application:* the LLM maps unbounded
   player text onto this generated affordance set, so the do-anything wall degrades into a legible
   "no operation matches — but you could melt or compress it," and `You can't do that.` never ships.

4. **Reason qualitatively, bookkeep quantitatively.** *Principle:* QPT and the
   LLM-as-simulator failures (GPT-4 at ~60% transition accuracy, errors in arithmetic/physics)
   show LLMs are reliable about *direction/ordering* of change but not numbers. *Application:*
   represent material properties as ordinal quantity spaces with named thresholds; the LLM reasons
   over them, the engine does conservation arithmetic.

5. **Operations are data (precondition/effect schemas over a fixed property schema).** *Principle:*
   the STRIPS/PDDL + DF-raws pattern makes behavior declarative table-rows, not code.
   *Application:* the LLM authors object/material rows and operation schemas against a fixed column
   set, validated at ingest — the only way the ontology becomes authorable at density (R2).

6. **Auto-chunk mastered procedures; keep only the novel decision.** *Principle:* depth is fun only
   while it teaches (Koster); a known multi-step chain re-typed is grind. *Application:* adopt
   Hadean Lands' action-chunking — the first solve of a crafting chain is a puzzle, every repeat
   collapses to one intent-command the engine *replans* against current state and scarcity.

7. **Make perception (and percepts) first-class and engine-owned.** *Principle:* TADS' sense-
   passing and Curveship's Simulator→Teller split show perception belongs in the deterministic core
   while prose is a pure render. *Application:* propagate sound/smell/heat percepts along a sense
   graph separate from the matter graph; the LLM narrates per-observer state and never invents
   facts — the runtime assertion that narration references only post-effect state.

8. **Tie survival pressure to stories and to other players, not to meters.** *Principle:*
   Armageddon's thirst mattered because it forced social/political play, not because it was
   realistic. *Application:* make scarcity solvable socially, reserve heavy/irreversible
   consequences for story-bearing moments, prefer degradation over hard loss, and batch/delegate
   routine maintenance so survival stays dramatic rather than a chore.

9. **Generate the long tail, then validate against invariants.** *Principle:* LIGHT and COMET show
   models can densely *propose* a structured ontology that hand-authoring can't reach, but
   model-as-authority drifts. *Application:* the LLM proposes schema-constrained
   object/material/affordance entries; a validator (conservation, property-schema, fuzz-solvability)
   and optional human curator accept them before they're canonical — the brainstorm's
   resolve-then-crystallize loop with a wall-sensor feeding the queue.

### What to avoid — documented failure modes
- **AI Dungeon incoherence (LLM-as-world-model).** No persistent ground truth → contradictions,
  resurrected NPCs, vanished items when context scrolls off
  (https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up). *Never* let the LLM be
  the source of truth; every player-visible fact must be reconstructable from the engine store.
- **Direct LLM simulation of physics.** GPT-4 lands ~60% on state transitions and error compounds
  over steps (https://aclanthology.org/2024.acl-short.1/) — never let the LLM *step* the
  simulation; have it *author the model* under validation.
- **"Systemic theater" / the leaking promise.** Imsims break the spell exactly where they bolt on
  non-systemic minigames or hard gates (Prey's menu hacking)
  (https://www.narrativedesign.net/p/prey-2017-game-design-lessons) — keep authored exceptions rare
  and dressed as fiction.
- **Simulation-depth FPS death & UI cliff.** DF's temperature sim is a known cause of lag and
  fortresses hit "FPS death" (https://dwarffortresswiki.org/index.php/Temperature); Qud reads as
  "impenetrable" (https://www.gaming.net/reviews/caves-of-qud-review/) — cap tick-rate/active-object
  scope (instanced ~one-day runs) and invest in perception legibility.
- **Crafting as opaque, lock-in, repetition-gated grind.** Armageddon's crafting was found arbitrary
  and years-long to branch (https://armageddonmud.boards.net/thread/13/crafting-skills-megathread) —
  reward attempts at the competence frontier (Discworld's TM), not raw repetition.
- **Closed-microworld brittleness (SHRDLU).** Language interpretation collapses past the toy domain
  when rules are hardcoded (https://en.wikipedia.org/wiki/SHRDLU) — bound the *verbs* and keep them
  total; let objects/materials be the open axis the LLM populates.
- **Synonym-stuffing breaking the parser.** Naively piling on synonyms backfires because
  disambiguation forgets the typed words (https://blog.zarfhome.com/2024/01/parser-if-disambiguation)
  — score `(operation, target)` candidates, auto-resolve the dominant one, and ask a *targeted*
  clarifying question only on genuine ties.
- **Per-agent LLM cost/latency in multiplayer.** Generative Agents are token-hungry and slow
  (https://hai.stanford.edu/news/computational-agents-exhibit-believable-humanlike-behavior) — use
  the memory/reflection loop only for NPC flavor, keep facts in the engine, and budget caching hard.
