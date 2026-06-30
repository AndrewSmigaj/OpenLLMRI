# The lineage of deep-world-model text worlds — and why LLMs change the equation

A research report testing a specific thesis the user raised:

> *Structured-command, "do-anything-in-a-modeled-world" text systems were attempted for decades (parser
> interactive fiction, old chatbots, simulationist MUDs) but stayed extremely limited because the world's
> **ontology and content had to be hand-authored** — there were no LLMs to build it out. Now, with LLMs,
> actually fleshing out that ontology is feasible.*

**Verdict in one line:** the thesis is **substantially correct**, with one important refinement — the
unlock is at **build/authoring time, and only when paired with deterministic validation** ("generate-
then-validate"); the systems that let the LLM *run* the world at runtime (AI Dungeon) fall apart. That
refinement is not a footnote against Whiteout — it *is* Whiteout's design.

This report is the readable synthesis. The full cited detail lives in three section files:
[`_lineage/c1-pre-llm.md`](_lineage/c1-pre-llm.md) (the historical lineage),
[`_lineage/c2-bottleneck.md`](_lineage/c2-bottleneck.md) (the ontology/commonsense bottleneck), and
[`_lineage/c3-llm-unlock.md`](_lineage/c3-llm-unlock.md) (the LLM unlock). It complements
[`prior-art.md`](prior-art.md), which reads these same systems for *design lessons*; here the question is
*historical* — was the vision attempted, what limited it, and has the limit really lifted?

> **Verification note (the anchors were spot-checked, because agents can be wrong).** The two load-
> bearing claims were re-verified against the live web, not taken on the research agents' word: **Cyc**
> (founded July 1984 at MCC; an estimated 1,000–3,000 person-years; ~$60M and 600 person-years by the
> early 2000s; ~24.5M hand-authored assertions by 2017 — [Wikipedia](https://en.wikipedia.org/wiki/Cyc),
> [Britannica](https://www.britannica.com/topic/CYC)) and **West et al. 2022, "Symbolic Knowledge
> Distillation"** ("*for the first time, a human-authored commonsense knowledge graph is surpassed by the
> automatically distilled variant in all three criteria: quantity, quality, and diversity*" — NAACL 2022,
> [ACL Anthology](https://aclanthology.org/2022.naacl-main.341/), [arXiv](https://arxiv.org/abs/2110.07178)).
> Both confirmed. The section files' other figures are consistent with these and with general knowledge.

---

## 1. The dream is sixty years old, and it kept hitting the same wall

The vision Whiteout chases is not new. It has arrived, in recognizable form, roughly once a decade since
the 1960s — and it has been bounded by the same thing every time.

Two systems bracket the whole field. **ELIZA** (Weizenbaum, 1966) had the *appearance* of understanding
with **no world model at all** — keyword pattern-matching, no objects, no state. It was the cheapest way
to look intelligent, and Weizenbaum spent the next decade horrified at how readily people mistook fluency
for comprehension ([Wikipedia: ELIZA](https://en.wikipedia.org/wiki/ELIZA)). **SHRDLU** (Winograd, 1972)
was its photographic negative: genuine, grounded understanding — you could say *"find a block taller than
the one you're holding and put it in the box,"* and it would parse, reason, and do it — but in a world so
small that *"the entire set of objects and locations could be described by including as few as 50 words"*
([Wikipedia: SHRDLU](https://en.wikipedia.org/wiki/SHRDLU)). Winograd himself later disowned the approach,
calling such demos *"Potemkin villages… things which, for the things they actually did in the demo, looked
good, but when you looked behind that there wasn't enough structure to make it really work more generally"*
([metadevo](https://metadevo.com/potemkin-villages/)). **The 50 words were the budget.** Depth and "do
anything" were never the bottleneck; *coverage* was.

Everything after lives in the gap between those poles — keeping SHRDLU's depth while escaping its
smallness — and the entire field converged on the *same architecture* to try:

- **Adventure / Scott Adams (1976–78):** the verb-noun parser over a hand-coded table of rooms, objects,
  and flags. Adams's key move — split a reusable *interpreter* from a swappable *world database*
  ([6502disassembly](https://6502disassembly.com/a2-scott-adams/)) — is the strategy the next 40 years
  repeat: separate engine from content so content can be authored as data.
- **Infocom / the Z-machine / ZIL (1979–89):** the world model becomes a first-class **object tree** with
  attributes and properties, a generic parser operating over it, and a portable VM
  ([inform-fiction.org](https://inform-fiction.org/zmachine/standards/z1point1/appd.html)). A beautiful
  general engine — married to a world whose every room, property, and *response* was hand-written in ZIL.
- **MUDs (MUD1 1978 → LPMud 1989 / DikuMUD 1991):** persistent, multiplayer worlds. LPMud's whole reason
  for existing was the authoring problem — Pensjö *"did not want to have sole responsibility for creating…
  the game world,"* so LPC soft-code let many players build rooms ([Wikipedia: LPMud](https://en.wikipedia.org/wiki/LPMud)).
  This *multiplied authors*; it did not remove authoring.
- **Inform & TADS (1993 → Inform 7, 2006):** the high-water mark of the hand-authored world model —
  kinds, relations, a default physics of containment/light/reachability, and Inform 7's declarative
  **rulebooks** ([Inform 7 docs](https://ganelson.github.io/inform-website/book/WI_19_2.html)). A
  magnificent grammar for *describing* a world, with zero help *populating* one.
- **Simulationist IF — "model a physics, not scripts":** Emily Short's *Metamorphoses* (2000) and
  *Savoir-Faire* (2002) gave every object a size/shape/material so *general verbs* act on anything by its
  properties; Plotkin's *Hadean Lands* (2014) is the cathedral. This school **proved the dream is real** —
  players really do improvise sensible actions the author never scripted — and, crucially, its
  practitioners *measured the bill out loud.*

That last point is the heart of it. The people who got closest **named the wall themselves.** Emily Short:
*"There is no such thing as a generic world simulator,"* a deep model is *"time consuming to write,"* and
*"most of my development time… has gone into working and reworking the content data, rather than refining
the process"* — so deep simulation *"makes most sense… in a small tight game environment"*
([emshort.blog](https://emshort.blog/2018/07/10/mailbag-world-simulation-plug-ins/),
[older essay](https://emshort.blog/how-to-play/writing-if/my-articles/issues-in-simulation-older/)).
Plotkin spent **four years** building one tightly-curated alchemical world
([zarfhome](https://zarfhome.com/press/hadean_lands.html)).

**The recurring conclusion across the whole lineage: the engine was never the wall — hand-authored content
was.** Every system separated a reusable engine from a world-as-data; the engine generalized *behavior*;
nothing generalized *content*. World size tracked exactly one variable — human authoring hours.

## 2. The wall had a name in AI, too: the knowledge-acquisition bottleneck

The IF/MUD lineage is the *applied* half of the story. The *foundational* half — the symbolic-AI attempt
to give machines a deep model of the everyday world — hit the identical wall, and named it.

The 1970s knowledge-representation program (Minsky's **frames**, 1974; Schank & Abelson's **scripts**,
1977) bet that understanding requires large, structured, hand-encoded world knowledge — and then ran into
how much knowledge that is. The poster child is **Cyc** (Lenat, from July 1984 at MCC): an explicit,
decades-long bet that *commonsense itself could be hand-coded.* The numbers are the argument. Lenat's own
early estimate was **1,000–3,000 person-years**; by the early 2000s Cyc had consumed **~$60M and ~600
person-years**; by 2017 it held **~24.5 million hand-authored assertions** over ~1.5M terms
([Wikipedia: Cyc](https://en.wikipedia.org/wiki/Cyc), [Britannica](https://www.britannica.com/topic/CYC)).
For all that, it is widely regarded as having proven the *opposite* of its thesis: that hand-authoring
broad, grounded commonsense doesn't scale to general intelligence. Naive- and qualitative-physics efforts
(Hayes's *Naive Physics Manifesto*, 1979/85; Forbus's QPT and de Kleer & Brown, 1984) hit the same ceiling
and retreated to small formalized domains.

The field even tried to *cheapen* the authoring, in a clean progression of strategies — and each was
cheaper but still sparse, noisy, and incomplete:

| Strategy | Example | Result |
|---|---|---|
| Hand-code by experts | **Cyc** (1984→) | ~24.5M assertions, ~person-millennia; never "complete" |
| Crowd-harvest from the public | **Open Mind / ConceptNet** (1999→) | large but noisy (ConceptNet 5.5 ≈ 21M edges) |
| Crowdsource templated if-then | **ATOMIC** (2019) | ~877k triples; quality up, still bounded by human effort |

Edward Feigenbaum had a name for this in the 1970s: the **knowledge-acquisition bottleneck.** For ~50
years the limiter on "a system that can do anything sensible in a modeled world" was not algorithms — it
was the cost and incompleteness of authoring the world's knowledge by hand. (Full detail + citations:
[`_lineage/c2-bottleneck.md`](_lineage/c2-bottleneck.md).)

## 3. What LLMs actually change

LLMs change *precisely the input that every system above could never cheapen* — and the evidence is now
concrete, not hopeful.

- **LLMs encode much of the commonsense the symbolic era tried to hand-author.** **COMET** (Bosselut et
  al., 2019) showed a language model can *generate* high-quality commonsense triples. The decisive result
  is **West et al., "Symbolic Knowledge Distillation" (NAACL 2022):** a **machine-authored** commonsense
  knowledge graph (ATOMIC-10x) that **surpassed the human-authored one in quantity, quality, *and*
  diversity — the first time that happened** ([ACL Anthology](https://aclanthology.org/2022.naacl-main.341/)).
  That is the Cyc bottleneck, measured and beaten, at *draft* time.
- **The winning pattern is "LLM authors a *checkable* artifact."** LLMs are weak as direct planners but
  strong as *domain authors*: LLM→**PDDL** world models (Guan et al., NeurIPS 2023; "LLM+P"; NL2Plan's
  validated pipeline) have the model write a formal world/operator definition that a deterministic
  planner/validator then runs. The LLM proposes the ontology; a symbolic engine disposes.
- **Generate-then-validate is non-negotiable.** LLM output is *plausible but not reliably correct*; a
  deterministic checker (a solver, a type-checker, a critic) must gate every artifact — which is exactly
  what West et al.'s critic model does, and exactly what makes the distilled KG trustworthy. **LIGHT**
  (Facebook AI) is the game-world precedent for model-assisted (not model-as-authority) authoring.
- **The bounding anti-pattern is documented: don't let the LLM *be* the world at runtime.** **AI Dungeon**
  — an LLM running the world live with no deterministic ground truth — produces the now-canonical failure
  mode: vanished items, forgotten and resurrected characters, contradictions, because state scrolls out of
  the context window. The unlock is **build-time authoring**, not a runtime world-engine.

(Full detail + citations: [`_lineage/c3-llm-unlock.md`](_lineage/c3-llm-unlock.md).)

## 4. Verdict on the thesis

**Substantially correct, with one refinement.**

- ✅ **"These systems were attempted decades ago."** Yes — repeatedly, in recognizable form, since SHRDLU
  (1972), with the same do-anything-in-a-modeled-world ambition.
- ✅ **"They stayed limited because the ontology/content was hand-authored."** Yes, and *demonstrably so*:
  the field converged on the right engine architecture every time, and the binding constraint was always
  human authoring hours — named explicitly by Winograd ("Potemkin villages"), Emily Short ("no generic
  world simulator… content eats the budget"), and, in AI proper, by Cyc's person-millennia and
  Feigenbaum's "knowledge-acquisition bottleneck."
- ✅ **"LLMs now make building that ontology feasible."** Yes — and this is no longer speculative: a
  machine-authored commonsense KB has *already* beaten the hand-built one on quality and scale (West 2022),
  and the LLM-authors-a-checkable-artifact pattern is established practice.
- ⚠️ **The refinement (the part the thesis understates):** the unlock is **at build time, and only with
  deterministic validation.** LLMs cheapen *authoring*, but they shift the burden to **verification,
  grounding, and coverage**, and they catastrophically fail if asked to *run* the world live. "Now we can
  do it" means *"now we can densely author a validated ontology offline,"* **not** *"now an AI can improvise
  the world at runtime."* The two are different projects; the second is AI Dungeon, and it doesn't work.

So the honest version of the thesis is stronger and sharper than the original: *the 50-year wall was
hand-authoring the world's ontology; LLMs are the first tool that moves that wall — provided a
deterministic engine remains the source of truth and the validator of everything the LLM writes.*

## 5. What this means for Whiteout

This lineage is not just *context* for Whiteout — it is a near-exact description of Whiteout's design,
arrived at independently, which is the strongest validation the architecture could get:

- **Keep every pre-LLM lesson** (the lineage earned them): engine owns state; behavior is data, not
  scripts; *model a physics, not puzzle solutions* (the simulationist creed); separate a reusable engine
  from a world-as-data. Whiteout's deterministic operation×material engine *is* the Inform/TADS/
  simulationist-IF world model, modernized.
- **Add the one new input the lineage never had:** the LLM authoring the ontology — materials, operations,
  objects, responses — **at density**, offline. This is precisely the per-object/per-property/per-response
  cost that capped every prior system, and it is the cost West et al. proved is now movable.
- **Avoid the one trap the lineage exposes:** never let the LLM run the world at runtime (Whiteout's hard
  constraint — fully deterministic runtime, LLM at build time only). AI Dungeon is the cautionary tale;
  Whiteout's "all interactions pre-built" rule is the correct response to it.
- **Honor the refinement as a hard requirement:** generate-then-validate. Whiteout's conservation ledger +
  §44 validator + fuzz oracle are exactly the "deterministic disposer" the research says is non-negotiable
  — the thing that turns LLM-drafted content from *plausible* into *trustworthy*.

Whiteout is, in effect, the system this 60-year lineage was always reaching for: SHRDLU's grounded depth,
the simulationist physics, the engine/content split — at a *coverage* the prior eras could never afford,
because for the first time the ontology can be authored densely and then validated. The bet the lineage
says is sound: **the engine was never the wall; the content was; and the content wall is the one that just
came down — carefully, at build time, behind a validator.**

---
### Sources
Lineage detail: [`_lineage/c1-pre-llm.md`](_lineage/c1-pre-llm.md). Bottleneck detail:
[`_lineage/c2-bottleneck.md`](_lineage/c2-bottleneck.md). LLM-unlock detail:
[`_lineage/c3-llm-unlock.md`](_lineage/c3-llm-unlock.md). Design-lesson companion: [`prior-art.md`](prior-art.md).
Anchor verifications: [Cyc (Wikipedia)](https://en.wikipedia.org/wiki/Cyc) ·
[CYC (Britannica)](https://www.britannica.com/topic/CYC) ·
[Symbolic Knowledge Distillation, West et al. 2022 (NAACL)](https://aclanthology.org/2022.naacl-main.341/).
