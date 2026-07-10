# Presentation v3 — composition with a budget (plan + self-assessment)

> **Status: SCRATCHPAD — Andrew reviews before anything is built (2026-07-09).** Written after
> his mid-cabin transcript critique. Contains: the retrospective on why three presentation
> passes still produced lists, the v3 design, an honest assessment of what it can and cannot
> achieve, and the new authoring scaffolding (the prose style guide) that guides all future
> text — mine included.

---

## 0. Retrospective — what actually went wrong, three times

| Attempt | What it did | Why prose still came out listy |
|---|---|---|
| DR-23 v1 | killed "You see:", added salience buckets + frames | the algorithm is *bucket → sort → comma-join*. It decorates lists; it never composes sentences |
| P3 banding | per-band, per-direction graded groups | multiplied the enumeration: every band×direction became another frame+list |
| P3.5 + polish | articles, counts, noun-phrases at distance | cosmetic repairs to a fundamentally enumerative pipeline |

**Root causes (each maps to a v3 change):**
1. **I built a renderer, not a writer.** Real prose groups by *meaning*, varies sentence shape,
   uses connective logic, and — above all — **omits**. The composer has no omission and no
   sentence planning; with no budget, every item demands a slot, so a list is the only possible
   output. *(→ the prose budget + masses)*
2. **One phrase form served every context.** Scene phrases written as standalone clauses got
   jammed into comma lists → "a sectional chart, folded to this valley, the pilot". *(→ the
   three-form phrase model)*
3. **Frames are content-blind.** "litter everywhere:" wrapping a bolted bin; twin "four shapes"
   sentences. *(→ authored per-zone frames/glimpses; merged far-sentence)*
4. **People rendered as list items.** The pilot between a chart and a thermos. *(→ persons
   always get their own sentence — a hard rule, mechanically enforced)*
5. **Nothing ever READ the output.** Tests assert substrings; no artifact existed for a human
   or an agent to read whole. Prose regressions were invisible to the entire verification
   apparatus. *(→ `make render-scenes` + the review DoD)*
6. **My own authoring had no global style rules.** Each phrase was optimized in isolation —
   locally vivid, globally cacophonous. *(→ the prose style guide: rules first, then words)*

## 1. The philosophy amendment (DR-23 v3)

From *weighting* to **composition with a budget**:

> A `look` is a GLANCE — a few seconds of attention rendered as 4–7 sentences an author could
> have written. **Everything present is addressable; NOT everything is mentioned.** Whatever
> isn't named is inside a mentioned MASS ("the scattered kit") or a mentioned container — one
> `search` away. Nameability survives; enumeration dies.

This *unifies* with DR-24: an aggregate mass is an implicit container. Same reveal philosophy,
no new machinery of thought: the scene mentions the mass; inspection itemizes it.

## 2. The design

### 2a. Three-form phrases (content schema, additive)
Every appearance entry may carry:
- `scene` — a full lead **sentence** (used only when the item is one of the named few in YOUR
  zone). Any punctuation allowed.
- `item` — a short noun phrase, **no internal commas**, ≤6 words ("the latched forward bin").
  Used in the same-zone named-items sentence and adjacent lines. Default: articled name.
- `glance` — ≤3 words ("a bin"). Used at NEAR band. Default: articled head noun.
The composer NEVER puts a `scene` form inside a list. (Root causes 2+3.)

### 2b. The prose budget + masses
- **Same zone**: persons first (own sentences, never listed — hard rule), then up to **K=3**
  prominent/lead `scene` sentences, then ONE items-sentence (semicolon-joined `item` forms,
  ≤4 items), then ONE authored **mass sentence** folding everything else: each zone authors
  masses in `zones.py` (e.g. mid_cabin → `{"kit": {"name": "the scattered kit", "sentence":
  "The rest is scattered kit — gear thrown wherever the impact wanted it."}}`); objects opt in
  via `mass: "kit"` (default: ordinary/subtle fold, prominent/persons never fold).
  A mass is an addressable pseudo-noun (`mass:mid_cabin:kit`, like zone nouns — precedent
  exists): `search the scattered kit` **itemizes its members** (pure disclosure — members are
  already in the pool/visible; no state change, fully deterministic).
- **Adjacent zones**: ONE line per direction — the zone's authored `glimpse` ("Aft, the rear
  cabin: seats, drifted snow, dark gear.") plus at most 2 prominent `glance` forms. Never lists.
- **NEAR**: one "you can make out …" sentence, ≤3 glances + "and more".
- **DISTANT/BARELY**: ONE merged sentence across all directions ("Farther out, shapes in the
  snow to the north and northeast.").
- **Characters woven, not labeled**: "Agent-1 is picking through the wreckage beside you." at
  prose position; the `With you:` line dies. Cross-zone characters keep their graded sentence.
- **Opener dedup**: in zoned scenes the room-wide desc line dies; each zone's survey IS the
  opener (the cabin flavor migrates into the interior zones' authored looks — content edit).

### 2c. Micro-hiding (DR-24b — "look under the seat", reveal-by-removal)
- **Positional stow**: a contained child may carry `where: "under" | "behind"`. Such children
  are NOT revealed by a plain search of the fixture — only by `search/look under X` (the parser
  already yields `relation="under"` leading; the search op gains relations `("under",
  "behind")`; `look under X` reaches it through CmdLook's existing sim fallback; examine with
  those relations delegates to the positional search). Honest empty answers teach the verb
  ("Nothing under 11B but frost and a dropped bolt-washer." — authored per fixture or default).
- **Reveal-by-removal**: a child with `where: "in_<part_id>"` surfaces when that PART is
  removed (the `apply()` REMOVE_PART branch clears the flag and drops it to the floor at the
  actor's zone). Removing the seat cover can shake loose what was tucked inside it.
- **v1 content** (small, story-forward, curve-respecting): under 11B → a worn **penknife**
  (edge 0.4 — a backup blade, weaker than the duffel multitool so the intended path holds);
  under 12C → **a child's mitten** (pairs with the mail-sack letter — story, not loot) and a
  pencil stub; tucked in 11B's cover (falls out when it's cut free) → a **boarding pass** with
  a read entry (a name and a destination — quiet worldbuilding, possible arc thread).

### 2d. Composer rewrite (`presentation.py`)
`compose_scene` becomes a staged sentence planner (pure, deterministic):
classify (persons / prominent / named / mass-folded) → plan sentences (opener; person
sentences; ≤K prominent `scene`s; one semicolon-disciplined items-sentence; one mass sentence;
adjacent glimpse lines; one merged far sentence) → join. All *sentences* that carry voice are
authored content (zone looks, glimpses, mass lines, scene leads); the machine only selects and
places them — its sole assembled sentence is the items-sentence, under comma discipline.

### 2e. Scaffolding (the force multipliers)
- **`make render-scenes`** → `tools/render_scenes.py` via the evennia shell: builds a scratch
  scene, walks every zone, dumps every `look` + every object's `examine`/`read` to ONE
  generated artifact (proposed: `docs/scenarios/whiteout/scene-render.md`, marked GENERATED —
  placement/gate-exclusion settled at implementation). Prose is reviewed by READING and by
  diff, never only by substring asserts.
- **`tools/lints/check_prose.py`** (joins `make validate`): every built object has an
  appearance entry; `item` forms contain no commas and ≤6 words; per-zone named-count within
  budget; duplicate display names have differentiated forms; persons never carry `mass`.
- **`docs/guides/prose-style.md`** — the writer's rubric (below), used by me and any agent
  BEFORE authoring text, and as the checklist for prose review of the render artifact.
- **Process DoD amendment**: any content or presentation change requires `make render-scenes`
  and reading the diff before commit.

### 2f. Tests
Tier-1: composer stages (budget cap; persons never listed; scene-forms never in lists; far
merge; mass fold + pseudo-noun; three-form fallbacks). Tier-2: the mid-cabin look has ≤7
sentences and no "With you:"; the pilot never appears comma-flanked; `search the scattered
kit` itemizes; `look under the seat` reveals the penknife; cutting 11B's cover drops the
boarding pass; opener no longer doubles. Golden-render: a committed snapshot of the mid-cabin
look asserting SHAPE (sentence count, no forbidden patterns), not exact wording.

### 2g. Build order (proposed commits)
1. Render tool + style guide + prose lint (review loop FIRST — everything after gets reviewed
   through it).
2. Composer rewrite + three-form schema + budget/masses/glimpses + opener dedup + woven
   characters (+ the content pass: item/glance forms, zone glimpses, mass definitions,
   interior-zone flavor migration).
3. DR-24b micro-hiding (+ its three content finds) + doc appends (DR-23 v3 amendment, DR-24b)
   + BACKLOG.

## 3. Assessment of this plan (the honest part)

**Will it produce high-quality, coherent, detailed descriptions?** It removes every mechanical
cause of the current failures: the comma catastrophe cannot recur (form separation + semicolon
discipline), people cannot be list items (hard rule), the budget forces omission, frames become
authored and content-aware, and the far bands collapse to one sentence. The look becomes 4–7
sentences of which **all but one are authored by a writer** — the machine only chooses and
places. That is the correct division of labor.

**The honest ceiling**: a rule-following composer produces *clean, varied, correct* prose — not
*inspired* prose. v3's bet is that inspiration lives in the authored parts (zone looks, scene
leads, mass sentences, glimpses), and the plan deliberately maximizes their share of every
look. If a look still reads flat after v3, the fix is better *writing* in those authored
fields — reviewable in the render artifact — not more composer machinery. Deeper approaches
(build-time LLM prose baking per §41, generate-then-validate) remain available later and would
slot into exactly these authored fields.

**Does it deepen search gameplay?** Four independent depth layers after v3: containers
(open/pry), masses (search the clutter), positional (under/behind), and removal-reveals — on
top of zones/reach. The scene gets *quieter on the surface and deeper underneath*, which is
precisely the directive.

**Risks, named**: (1) a player's *dropped* item may fold into a mass and "vanish" from the
look — accepted v1 (it's findable by searching the mass; a recency exemption is a clean later
tweak); (2) masses need careful membership or the mass sentence lies — the lint checks
membership, the render review checks truth; (3) the composer rewrite touches every Tier-2
look assertion — budgeted as part of commit 2; (4) golden-render tests must pin SHAPE not
wording, or they'll fight Andrew's tuning.

**Certainty**: parser `relation="under"` leading-position already works (shipped in P3.2,
tested); zone-pseudo-noun precedent covers mass nouns; REMOVE_PART is a single apply branch;
the render tool follows the existing shell-script pattern. The genuinely new risk is composer
regressions — covered by the render-review loop landing FIRST (build order 1).

## 4. The prose style guide (draft — becomes `docs/guides/prose-style.md`)

**The glance rule.** A look is a glance. 4–7 sentences. If you want to say more, hide more.
**The three forms.** Every object authors `scene` (a sentence), `item` (≤6 words, NO commas),
`glance` (≤3 words). Never let a sentence-form into a list.
**People are never items.** A person gets a sentence or nothing. The dead get their tone.
**One frame, and it must fit.** A frame word must match what it wraps (bins are not litter).
Never two mechanical frames in a row; merge or vary.
**Semicolons between phrase-items; commas only inside them.**
**Say it once.** If the zone survey says it, the room desc may not. If a phrase names a
container ("spilled from an overhead bin"), check the container isn't standing in the same
sentence.
**Twins must differ.** Second identical name renders as "another …" or gets a differentiator.
**Distance simplifies grammar, not just detail.** Full sentence → short phrase → head noun →
"shapes" → silence.
**Write for the ear.** Read every look aloud once (the render artifact exists for exactly
this). If you inhale twice in one sentence, split it.
**The mass must be true.** A mass sentence describes what actually folds into it — check the
render, not your intention.
**Author the failure lines too.** "Nothing under 11B but frost" teaches the verb; silence
teaches nothing.

## 5. What I change about how *I* work (the scaffolding on me)

1. **Style guide before words**: any session where I author or edit game text starts by
   reading `prose-style.md`; agent prompts for content work must include it (or its rules
   verbatim) — the way hard sim rules are already restated in every agent brief.
2. **Render, then read**: no content/presentation commit without reading the render diff —
   into the process DoD, not just good intentions.
3. **Review prose as prose**: when checking my own output, read the full artifact aloud-style
   looking for the guide's specific failure patterns — never only grep for expected substrings.
   (Substring asserts caught zero of the six bugs Andrew found by reading.)
