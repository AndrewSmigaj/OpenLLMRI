# C3 — The "LLM Unlock": Why a Deep World Ontology Is Now Buildable, and How People Actually Build One

**Thesis under test:** *The old hand-authored-ontology bottleneck is now removed by LLMs.*

**Honest verdict up front:** Largely true **for build-time authoring**, and only **if the LLM is paired with a deterministic validator**. The unlock is real but bounded — it is an unlock at *authoring/build time*, not a license to let the LLM *be* the world engine at runtime. Everything below argues that boundary carefully and cites the evidence on both sides.

---

## 0. What the bottleneck was

For forty years the dominant obstacle to symbolic AI was the **knowledge-acquisition bottleneck**: every commonsense fact a system "knew" had to be hand-authored by experts. The canonical example is **Cyc** (Lenat, begun 1984), whose explicit purpose was framed as overcoming "brittleness and knowledge acquisition bottlenecks" by hand-coding a projected ~100 million commonsense assertions over decades of human labor ([Lenat, *CYC: Using Common Sense Knowledge to Overcome Brittleness and Knowledge Acquisition Bottlenecks*, AI Magazine 1985](https://onlinelibrary.wiley.com/doi/abs/10.1609/aimag.v6i4.510); [Britannica: CYC](https://www.britannica.com/topic/CYC)). The same bottleneck shows up in interactive-fiction and game terms as: someone has to author every object, every property, every legal interaction, and every rule by hand. That hand-authoring cost is precisely what the "LLM unlock" claims to dissolve.

The claim of this section is narrow and testable: **LLMs substantially relieve that bottleneck at *generation* time** — they can *propose* the ontology, the entities, the relations, and the rules — provided a deterministic process then *validates* what they produce.

---

## 1. LLMs as commonsense / ontology generators

### 1.1 COMET — the proof-of-concept that an LM can *generate* a commonsense KG

The pivotal early result is **COMET (COMmonsEnse Transformers)** ([Bosselut et al., ACL 2019](https://aclanthology.org/P19-1470/); [arXiv:1906.05317](https://arxiv.org/abs/1906.05317)). Trained on seed tuples from two hand-built commonsense knowledge graphs — **ATOMIC** (inferential if-then social knowledge) and **ConceptNet** — COMET learns to *generate* new commonsense tuples in natural language rather than retrieve them. Human raters judged its novel generations as high quality, with top-1 precision of **77.5% on ATOMIC** and **91.7% on ConceptNet**, approaching human performance on these resources ([Bosselut et al. 2019](https://aclanthology.org/P19-1470/); [code](https://github.com/atcbosselut/comet-commonsense)).

The conceptual significance: the *implicit* knowledge inside a pretrained LM can be *transferred into explicit, structured commonsense* — i.e., the knowledge the symbolic era tried to type in by hand was already latent in the model and could be emitted on demand. COMET is the first concrete demonstration that the acquisition step can be *generated*, not just curated.

### 1.2 Symbolic Knowledge Distillation — machine-authored KG *beats* the human one

COMET still trained on a human seed. The stronger result came three years later. In **Symbolic Knowledge Distillation** ([West et al., NAACL 2022](https://aclanthology.org/2022.naacl-main.341.pdf); [arXiv:2110.07178](https://arxiv.org/abs/2110.07178)), GPT-3 is prompted with head events and relations to *author an entire commonsense knowledge graph from scratch* — **ATOMIC10x** — filtered by a learned **critic model**. The headline finding directly attacks the bottleneck: *"for the first time, a human-authored commonsense knowledge graph is surpassed by the automatically distilled variant in all three criteria: quantity, quality, and diversity,"* and the model trained on it (COMET-distil) surpasses the GPT-3 teacher's commonsense despite being ~100× smaller ([West et al. 2022](https://aclanthology.org/2022.naacl-main.341.pdf)). This is the strongest single piece of evidence for the thesis: a machine-generated ontology can exceed a famous hand-built one on the metrics that matter — **and note the critic/filter step is load-bearing**, foreshadowing §3.

### 1.3 The pattern generalizes: LLM-driven KG / ontology construction

This has since become a research subfield. A 2025 survey, *LLM-empowered knowledge graph construction* ([arXiv:2510.20345](https://arxiv.org/abs/2510.20345)), reviews how LLMs are now used across the classic KG pipeline — **ontology engineering, knowledge extraction, and knowledge fusion** — generating triples, axioms, and class hierarchies. Crucially, the survey frames the standard practice honestly: approaches *"treat the LLM as a source of knowledge to be validated,"* because *"LLMs hallucinate, confabulate, and produce plausible but incorrect formalizations"* ([survey, arXiv:2510.20345](https://arxiv.org/html/2510.20345v1)). That is the field's own statement of the §3 caveat.

**Takeaway for §1:** The knowledge-acquisition bottleneck is *substantially relieved at generation time*. What used to be years of expert typing can now be a generation pass — but the output is a *draft to be checked*, not a verified KB.

---

## 2. LLMs generating *symbolic* world models / game logic / planning domains

The deeper unlock for *interactive worlds* is not free-text commonsense but **formal, checkable artifacts**: an LLM authoring a planning domain, a rule set, or an action ontology that a deterministic engine can then run and verify.

### 2.1 LLM → PDDL world models (Guan et al., NeurIPS 2023)

The cleanest statement of the paradigm is **Guan et al., *Leveraging Pre-trained LLMs to Construct and Utilize World Models for Model-based Task Planning*** ([NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/f9f54762cbb4fe4dbffdd4f792c31221-Abstract-Conference.html); [arXiv:2305.14909](https://arxiv.org/abs/2305.14909); [code](https://github.com/GuanSuns/LLMs-World-Models-for-Planning)). Their explicit motivation is that **LLMs are poor *direct* planners** — they cite "limited correctness of plans, strong reliance on feedback from interactions with simulators or even the actual environment, and inefficiency in utilizing human feedback." Their alternative: have the LLM *construct an explicit world model in PDDL*, then hand that model to a sound, domain-independent classical planner. The LLM is **not** the planner; it is an *interface* that (a) drafts the PDDL and (b) translates PDDL ↔ natural language so that **PDDL validators (VAL) and humans** can supply corrective feedback. The key efficiency argument: you correct the *domain model once* rather than correcting every individual plan. Results: GPT-4 produced high-quality PDDL for **over 40 actions** and the corrected models solved **48 challenging planning tasks** across IPC and a Household domain harder than ALFWorld ([Guan et al. 2023](https://arxiv.org/abs/2305.14909)).

### 2.2 LLM+P — NL problem in, formal solve, NL answer out

**LLM+P** ([Liu et al. 2023, arXiv:2304.11477](https://arxiv.org/abs/2304.11477); [code](https://github.com/Cranial-XIX/llm-pddl)) is the minimal version of the pattern: it takes a natural-language planning problem, uses the LLM to translate it into **PDDL**, lets a **classical planner** find a correct/optimal plan, then translates the plan back to natural language. The reported result is stark: LLM+P returns optimal solutions for most problems, while the LLM *alone fails to produce even feasible plans* for most ([Liu et al. 2023](https://arxiv.org/abs/2304.11477)). The LLM supplies *translation and modeling*; the deterministic solver supplies *correctness*.

### 2.3 NL2Plan — full pipeline with validation baked in

**NL2Plan** ([Gestrin et al. 2024, arXiv:2405.04215](https://arxiv.org/abs/2405.04215); [HTML](https://arxiv.org/html/2405.04215v2)) is the most "productized" version and is essentially a blueprint for the build-time pattern. From a *minimal* natural-language description it generates a complete PDDL domain + problem via a **six-step decomposition**: (1) type extraction, (2) type-hierarchy construction, (3) action extraction, (4) action construction, (5) problem extraction, (6) planning. Two things matter for the thesis:

- **Every artifact is validated.** Syntactic checks use a suite of tools (VAL, cpddl, a custom validator); **semantic** checks use LLM or human feedback; a feedback substep runs at most once per step to avoid infinite loops; the final plan is checked against the original task ([NL2Plan, arXiv:2405.04215](https://arxiv.org/html/2405.04215v2)).
- **Decomposition + validation beats one-shot generation.** NL2Plan substantially outperforms directly asking an LLM to emit PDDL (even with a validator), solving far more tasks with zero manual edits; the stepwise structure keeps the LLM from "forgetting" necessary actions ([NL2Plan, arXiv:2405.04215](https://arxiv.org/abs/2405.04215)). Related work, *Large Language Models as Planning Domain Generators* ([arXiv:2405.06650](https://huggingface.co/papers/2405.06650)), studies the same generation task at scale.

**Pattern of §2:** the LLM *authors a formal, checkable artifact* (PDDL domain, rule schema, ontology) and a *deterministic engine* (classical planner / validator) consumes it. The formality is the whole point: it is what makes machine verification — and therefore trust — possible.

---

## 3. The deterministic-engine + LLM-authored-content pattern: **generate-then-validate**

The unifying architecture across §2 — and the actual answer to "how do people build these systems today" — is **"LLM proposes, validator disposes."** The LLM *generates or proposes* content; a deterministic checker *validates* it before it is trusted or shipped.

- In Guan et al., the disposer is **VAL plus a human reviewing NL-rendered PDDL** ([arXiv:2305.14909](https://arxiv.org/abs/2305.14909)).
- In NL2Plan, the disposers are **VAL/cpddl/custom syntactic validators, a classical planner (solvability as a correctness signal), and LLM/human semantic feedback** ([arXiv:2405.04215](https://arxiv.org/html/2405.04215v2)).
- In Symbolic Knowledge Distillation, the disposer is a **learned critic model** that filters GPT-3's generated tuples ([West et al. 2022](https://aclanthology.org/2022.naacl-main.341.pdf)).
- In LLM-driven KG construction generally, the survey states the field treats LLM output as *"knowledge to be validated"* ([arXiv:2510.20345](https://arxiv.org/html/2510.20345v1)).

### 3.1 LIGHT — model-assisted authoring of an interactive world

The game/world-building precedent is **LIGHT** (Facebook AI Research). The original platform, *Learning to Speak and Act in a Fantasy Text Adventure Game* ([Urbanek et al. 2019](https://ai.meta.com/research/publications/learning-to-speak-and-act-in-a-fantasy-text-adventure-game/); [project](https://parl.ai/projects/light/)), is a *crowd-authored* world: **663 locations, 3,462 objects, 1,755 character types, and 11,000 episodes** of grounded talk-and-act interaction. The follow-up, ***Generating Interactive Worlds with Text*** ([Fan, Urbanek et al. 2019, arXiv:1911.09194](https://arxiv.org/abs/1911.09194)), is exactly the model-assisted-authoring story: neural models *"compositionally arrange locations, characters, and objects into a coherent whole,"* can generate new content, and explicitly let *"humans … interactively aid in worldbuilding."* Human evaluators preferred worlds built this way over other ML world-construction baselines, though automatic world-building scores were modest (reported in the low tens of percent), underscoring that the model is an *assistant whose output is curated*, not an autonomous authority.

### 3.2 Why validation is *essential*, not optional

The reason the validator is non-negotiable is that LLM output is *plausible-but-not-necessarily-correct by construction*. Lenat & Marcus put it bluntly in *Getting from Generative AI to Trustworthy AI: What LLMs might learn from Cyc* ([arXiv:2308.04445](https://arxiv.org/abs/2308.04445)): LLMs are *"trained to produce outputs that are plausible, but not necessarily correct,"* and their results are *"both unpredictable and uninterpretable"* and *"lacking in aspects of reasoning."* Their prescription is hybridization — LLM generation *grounded in formal verification and explicit representation*, where reasoning steps and provenance are auditable. That is generate-then-validate stated as a thesis. The KG survey echoes it: hallucination and confabulation are *expected*, so the formal checker is what converts a confident draft into a trustworthy artifact ([arXiv:2510.20345](https://arxiv.org/html/2510.20345v1)).

---

## 4. The bounding anti-pattern: **LLM-as-runtime-world**

The boundary of the unlock is sharp, and it is best illustrated by what happens when you *cross* it: letting the LLM **be** the live world engine, with no deterministic ground truth for state.

The canonical case is **AI Dungeon**. Its *own* FAQ explains the structural failure: the model only sees a fixed **context window** of recent text, so *"the AI loses its ability to look back and reference certain parts of the story,"* and the FAQ admits mitigations are *"not guaranteed to work 100% of the time"* ([AI Dungeon FAQ: "Why does the AI forget or mix things up?"](https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up)). The documented, reproducible failure modes are exactly the ones a world-engine must never have: characters whose names the AI suddenly can't remember, plot threads that *vanish*, an NPC who was a sworn enemy last scene now greeting you as a stranger ([Tavernbound: *Why AI Dungeon Keeps Forgetting Your Story*](https://tavernbound.com/blog/why-ai-dungeon-forgets-your-story)); the engine *"can ignore your commands, throw away key plot points it has already set up, or even forget entire characters and locations,"* and when asked to fill space it will *"make up whatever it wants … even if it is irrelevant, contradictory"* ([TV Tropes: AI Dungeon 2](https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/AIDungeon2)). The same failure is documented academically for LLM game masters: in a study of solo role-play, *"the GM often provided incoherent responses or forgot that the player had just picked up an item"* ([*Static Vs. Agentic Game Master AI for Facilitating Solo Role-Playing Experiences*, arXiv:2502.19519](https://arxiv.org/abs/2502.19519)).

These are not prompt-tuning bugs; they are the *signature* of having no deterministic state of record. Items vanish and characters resurrect because the "world state" is just re-derived from a sliding text window every turn. AI Dungeon's countermeasures — **Memory Bank / Plot Essentials / Story Cards** — are an attempt to *bolt a small persistent state store onto the side* of the LLM ([AI Dungeon FAQ](https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up)), which is the tacit admission that *some* deterministic ground truth is required. This is the crucial boundary: **the unlock is at build/authoring time; it is not a license to make the LLM the runtime world-engine.**

---

## 5. State of the art: how a deep interactive world from an LLM-built ontology is actually built today

Synthesizing §§1–4, the current best practice for "deep interactive world from an LLM-built ontology" is a **two-phase, offline-authoring / online-deterministic** split:

1. **Author offline with the LLM (generation).** Use the LLM to *propose* the ontology and content — entity/type taxonomy, properties, relations, action schemas, rules, and content (the LIGHT and KG-construction story: [arXiv:1911.09194](https://arxiv.org/abs/1911.09194); [arXiv:2510.20345](https://arxiv.org/abs/2510.20345)). **Decompose** the authoring into typed steps rather than one-shotting it; stepwise generation is materially more robust (the NL2Plan finding: [arXiv:2405.04215](https://arxiv.org/abs/2405.04215)).
2. **Validate / bake (the disposer).** Pass every generated artifact through a **deterministic checker**: a formal validator (VAL/cpddl), a type/consistency checker, and — the strongest signal available for interactive domains — an actual **solver/simulation** that confirms the world is well-formed and the intended goals are reachable (Guan, NL2Plan, LLM+P: [arXiv:2305.14909](https://arxiv.org/abs/2305.14909), [arXiv:2405.04215](https://arxiv.org/abs/2405.04215), [arXiv:2304.11477](https://arxiv.org/abs/2304.11477)). Use the LLM's PDDL↔NL translation to make **human review cheap** where semantic judgment is needed (Guan: [arXiv:2305.14909](https://arxiv.org/abs/2305.14909)). Optionally add a **learned critic/filter** to prune low-quality generations at scale (West et al.: [arXiv:2110.07178](https://arxiv.org/abs/2110.07178)).
3. **Run on a deterministic engine (runtime).** Ship the *validated* ontology into a deterministic engine that owns world state and is the single source of truth at runtime. The LLM may still surface text or propose actions, but the engine — not the LLM — *arbitrates state*, precisely to avoid the §4 AI Dungeon failure modes.

### What is genuinely solved vs. still hard

**Genuinely unlocked (the thesis holds):**
- **Authoring throughput / draft coverage.** Producing a first-draft ontology of broad commonsense breadth is now cheap — and a machine-authored KG has *beaten* a celebrated hand-built one on quantity/quality/diversity ([West et al. 2022](https://aclanthology.org/2022.naacl-main.341.pdf)).
- **NL ↔ formal translation.** Turning informal intent into a formal, checkable artifact, and rendering formal artifacts back to readable NL for review, is reliable enough to build on ([Guan 2023](https://arxiv.org/abs/2305.14909); [Liu 2023](https://arxiv.org/abs/2304.11477)).

**Still hard (the caveats that keep it from being a blank check):**
- **Grounding.** Generated symbols must correspond to the engine's *actual* mechanics; the LLM can emit a plausible predicate that the engine cannot honor.
- **Coverage / completeness verification.** A validator can confirm an artifact is *well-formed and solvable*, but proving the ontology *covers all situations the world will encounter* remains open — this is the residual of the old bottleneck, displaced from authoring to *verification*.
- **Global consistency.** Large generated artifacts can be locally valid yet globally contradictory; hallucination/confabulation is intrinsic, so checking scales with the artifact ([arXiv:2510.20345](https://arxiv.org/html/2510.20345v1); [Lenat & Marcus 2023](https://arxiv.org/abs/2308.04445)).
- **No runtime authority.** The LLM cannot be the live arbiter of world state without reintroducing incoherence ([AI Dungeon FAQ](https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up); [arXiv:2502.19519](https://arxiv.org/abs/2502.19519)).

---

## 6. Summary

- **What the LLM genuinely unlocks:** the *generation* step of ontology/world-model building. COMET showed an LM can emit commonsense KGs ([Bosselut 2019](https://aclanthology.org/P19-1470/)); Symbolic Knowledge Distillation showed a *machine-authored* KG can surpass the human one in quantity, quality, and diversity ([West 2022](https://aclanthology.org/2022.naacl-main.341.pdf)). The decades-long hand-authoring cost (Cyc-style; [Lenat 1985](https://onlinelibrary.wiley.com/doi/abs/10.1609/aimag.v6i4.510)) is largely removed at draft time.
- **The winning architecture is formal-artifact authoring:** the LLM writes a *checkable* object — PDDL domain, rule schema, typed ontology — and a deterministic engine consumes it (LLM+P, Guan, NL2Plan: [2304.11477](https://arxiv.org/abs/2304.11477), [2305.14909](https://arxiv.org/abs/2305.14909), [2405.04215](https://arxiv.org/abs/2405.04215)). Notably, LLMs are weak *direct* planners but strong *domain authors*.
- **The essential caveat is generate-then-validate:** LLM output is plausible-but-not-necessarily-correct, so every artifact must pass a deterministic disposer — validator, solver, type checker, or critic — before it is trusted ([Lenat & Marcus 2023](https://arxiv.org/abs/2308.04445); [KG survey 2510.20345](https://arxiv.org/abs/2510.20345)). Stepwise generation + per-step validation beats one-shot prompting ([NL2Plan](https://arxiv.org/abs/2405.04215)).
- **The unlock is build-time, not runtime:** the LLM authors and proposes *offline*; a deterministic engine owns state and arbitrates *online*. Human review is made cheap via NL↔formal translation ([Guan 2023](https://arxiv.org/abs/2305.14909); model-assisted LIGHT authoring: [1911.09194](https://arxiv.org/abs/1911.09194)).
- **The bounding anti-pattern is LLM-as-runtime-world:** AI Dungeon and LLM game-masters demonstrate the failure of no deterministic ground truth — vanished items, forgotten/resurrected characters, contradictions — driven by the context window, not fixable by prompting ([AI Dungeon FAQ](https://help.aidungeon.com/faq/why-does-the-ai-forget-or-mix-things-up); [Tavernbound](https://tavernbound.com/blog/why-ai-dungeon-forgets-your-story); [arXiv:2502.19519](https://arxiv.org/abs/2502.19519)).
- **Verdict — is the bottleneck actually removed?** *Largely yes, for build-time authoring, **IF** paired with deterministic validation* — the LLM dissolves the authoring cost but not the verification burden, which shifts from "typing the knowledge" to "checking, grounding, and proving coverage of the generated knowledge." It is a genuine unlock, not a blank check.
