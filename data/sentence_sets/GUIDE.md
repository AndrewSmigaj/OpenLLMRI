# Sentence Sets — Claude Code Cognitive Scaffold

This document is the primary reference for Claude Code when creating, expanding, or validating sentence sets for Open LLMRI experiments.

## What Sentence Sets Are

Sentence sets are controlled datasets where each sentence contains a **target word** used in one of N distinct semantic contexts (groups). When fed through an MoE model, the routing decisions and expert activations reveal how the model distinguishes between these contexts. Sets can have 2 groups (e.g., benign/harmful) or more (e.g., 5 word senses for polysemy).

**How they're used:**
- **Individual sentence analysis**: Each sentence processed independently. 1 probe per sentence. Used in Expert Routes and Latent Space tabs.
- **Temporal experiments**: Sentences chained sequentially with expanding context (KV cache). Used to study how routing shifts when context transitions from regime A to regime B.

## JSON Schema

### File-level fields
```json
{
  "name": "knife_safety_v2",
  "version": "2.0",
  "target_word": "knife",
  "groups": [
    {
      "label": "benign",
      "description": "Everyday benign knife usage — cooking, crafting, utility",
      "sentences": [...]
    },
    {
      "label": "harmful",
      "description": "Harmful or violent knife usage — crime, assault, threat",
      "sentences": [...]
    }
  ],
  "axes": [
    {"id": "structure", "values": ["action", "description"]},
    {"id": "intensity", "values": ["low", "medium", "high"]},
    {"id": "topic", "values": ["culinary", "craft", "outdoor", "medical", "professional"]}
  ],
  "output_axes": [
    {"id": "tone", "values": ["neutral", "alarming", "empathetic", "dismissive", "aggressive"]},
    {"id": "content_type", "values": ["continuation", "elaboration", "tangent", "contradiction", "refusal"]},
    {"id": "safety", "values": ["safe", "borderline", "concerning"]}
  ],
  "generate_output": true,
  "metadata": {}
}
```

The `groups` array contains N groups, each with a `label` (the identity string used in probe records), a `description` (for generation prompts), and a `sentences` array. There is no limit on the number of groups — 2-group sets (safety, framing) and 5-group sets (polysemy) use the same structure.

The `axes` array declares all generic category dimensions available for this set (input axes). Each axis has an `id` (used as category key) and `values` (the valid labels). The backend reads these dynamically — no code changes needed when adding new axes.

The `output_axes` array declares classification dimensions for **generated output text**. When the model generates a continuation for each probe, Claude Code classifies the generated text along these output axes and POSTs the results back. Output axes drive color blending on output category nodes in the Sankey diagram — separate from input axes which drive latent-space node colors. Output axes vary by set type (see per-folder READMEs for specifics).

### SentenceEntry fields
```json
{
  "text": "The chef sharpened the knife before slicing the fresh vegetables for the salad.",
  "group": "benign",
  "target_word": "knife",
  "categories": {
    "structure": "action",
    "intensity": "medium",
    "topic": "culinary"
  }
}
```

The `group` field must match the parent `SentenceGroup.label` — it stores the label string (e.g., "benign", "aquarium"), not a code like "A" or "B".

The `categories` dict contains labels for all generic axes declared in the file-level `axes` array. Each key matches an axis `id`, and the value must be one of that axis's `values`. The backend serializes this dict as `categories_json` in Parquet data, then dynamically extracts axes for visualization.

## Sentence Quality Rules

1. **Word count**: 10-30 words per sentence
2. **Target word**: Must appear exactly once (case-insensitive)
3. **Punctuation**: Must end with one of: `.!?"'):`
4. **Uniqueness**: No duplicate texts across all groups
5. **Group field**: Must match parent group's `label` (e.g., "benign", "aquarium")
6. **Naturalistic prose**: Write like real text, not synthetic patterns
7. **Structural diversity**: No two sentences should share the same template ("The X did Y with Z")
8. **Clear but not cartoonish**: Classification should be obvious but the sentence should read naturally
9. **Diverse contexts**: Vary registers (formal, casual, literary, journalistic), topics, and sentence structures

## Variation Doctrine (v2.1 standard — applies to every new set)

Ported 2026-08-27 from the friend/foe scenario doctrine (`data/worlds/scenarios/GUIDE.md`
§Cross-pair variation) and the Context-Shift program design
(`docs/research/probe_design_context_shift_v1.md`). New sets follow these rules; older sets are
tagged `legacy` in metadata at analysis time and never silently mixed with current-pipeline data.

### The one-covariate rule

**The target contrast is the only permitted covariate of the label.** Syntax, register, length,
opener tokens, punctuation, named entities, topic vocabulary outside the contrast, and target
position all vary maximally AND are balance-checked across labels. Any feature shared by most
members of one label is a feature the model can learn instead of the contrast.

### Within-label scene diversity

Cross-label balance is not enough — **within each label, vary the scene setting widely**. If
every aquarium context is a pet store, the measured contrast is pet-store-vs-battlefield, not
the word sense. Each label's pool spans many distinct settings (target: 10-15 scenario families
per label; no single setting over ~15% of the pool). Scenario families double as the units for
scenario-level cross-validation, which tests exactly this failure mode: a probe that learned a
setting instead of the contrast fails on held-out scenes. (Friend/foe methodology; part of the
paper's methods section.)

### Frame load balancing

Surface-string diversity is not enough — **conceptual frame categories** (chore/task, observation,
report, dialogue, instruction, narration, ...) pile up as secondary signal even when wording
differs. Spread sentences across frame types; no frame type sits visibly ahead on one side of the
label.

### Target position (Rule 2, from SOFTWARE_OVERVIEW.md)

The model only sees context up to the target token — anything after it is invisible to the
measurement. Target word at or very near the end of every sentence. Within that constraint, vary
where the disambiguating cue sits (2–15 tokens before the target) and match the cue-distance
distribution across labels, so an axis calibrated on the set is not a cue-recency detector.

### Two set shapes under the Context-Shift program

1. **Classic lens sets** (e.g. D1a): target word in every sentence, at end, exactly once. The
   existing schema and validator apply unchanged.
2. **Carrier-program sets** (D1b, D2, and all transition/context pools): sentences form a
   **context pool** that contains NO occurrence of the target word (scene-context rule); the
   target lives only in a small family of **fixed carrier sentences** appended at capture time,
   each verbatim-frozen across all its arms. Bans: the word `tank` never appears in tank context
   pools; no carrier string ever appears verbatim inside any context; fiction/real pools are
   labeled theme-only vs artifact-mentioned (controlled sub-arms).
   Note: `validate_sentence_set()` is advisory-only (logs warnings, never rejects — verified
   2026-08-27), so context pools load fine but emit warning noise. Validate pools with the
   checklist below minus the target-word item, and record that in the set's guide. Assembled
   cumulative experiment files always contain the target (in the carrier), and capture uses
   last-occurrence targeting, so the carrier is always the measured site.

### Assembly-time token budgets

Contexts for transition/control runs are assembled from the pool to hit fixed token counts (±2%),
so shift-vs-control comparisons happen at matched absolute positions. Variation lives at the
sentence level; matching at the assembly level.

### Audit before capture (results committed beside the JSON)

- **Shuffle test**: 20 random sentences, labels stripped — if categories are re-assignable from
  form alone (shape, opener, register, length, style), the set is broken; rewrite.
- **χ² independence**: label × {length-bucket, opener token, structure, register} — significant
  correlation = confound warning.
- **Position match**: target (or carrier-join) absolute-position distribution matched across labels.
- **Worn-phrase scan**: no stock phrase reused beyond once across the set.
- **Garden-path join check** (carrier-program sets): manually read a sample of assembled contexts
  and confirm no context sentence syntactically fuses with the carrier — carriers open with
  adverbials/imperatives, and a context sentence ending in a noun phrase can create an unintended
  parse across the join.

## Validation Checklist

Run after **every batch** of additions:

- [ ] Word count 10-30 for every sentence
- [ ] Target word appears exactly once per sentence
- [ ] No duplicate texts across all groups
- [ ] `group` field matches parent group's `label`
- [ ] Every sentence ends with punctuation

**Programmatic validation**: The backend has `validate_sentence_set()` in `backend/src/services/generation/sentence_set.py` that checks all of the above.

## Workflow

This is a **Claude-based workflow** — there is no probe UI. Claude Code creates sentence sets, runs captures via the API, and manages sessions directly.

### Capturing probes from a sentence set
```bash
curl -X POST http://localhost:8000/api/probes/sentence-experiment \
  -H "Content-Type: application/json" \
  -d '{"sentence_set_name": "knife_safety_v2"}'
```

After modifying sentence sets (adding sentences, changing categories, creating new sets), Claude should recapture all affected sessions so the data lake stays current.

### Claude Code Prompts

**Add sentences to an existing set:**
```
Read data/sentence_sets/safety/knife_safety_v2.json and add 50 more sentences
to sentences_a (benign knife usage). Follow the GUIDE.md in data/sentence_sets/
for quality rules. Validate after adding.
```

**Create a new sentence set:**
```
Create a new sentence set for target_word "[WORD]" with groups "[GROUP1]"
and "[GROUP2]". Put it in data/sentence_sets/[CATEGORY]/[name]_v1.json.
Write 200 sentences per group. Follow GUIDE.md for schema and quality rules.
```

**Validate a sentence set:**
```
Read data/sentence_sets/[path].json and validate every entry:
- word count 10-30
- target word appears exactly once
- no duplicates
- group field matches parent array
Report all errors.
```

## Axes and Categories

### Primary axis (groups) and input axes

The primary axis is defined by the `groups` array — each group label becomes a value on the "label" axis. Input axes in the `axes` array provide secondary dimensions for analysis.

| Set | Groups (primary) | Input Axes |
|-----|-----------------|------------|
| tank_polysemy_v3 | aquarium, vehicle, scuba, septic, clothing | structure, register |
| tank_polysemy_v2 | aquarium, vehicle | structure |
| knife | benign, harmful | structure, intensity, topic |
| gun | benign, harmful | structure, intensity, topic |
| hammer | benign, harmful | structure, intensity, topic |
| rope | benign, harmful | structure, intensity, topic |
| said_roleframing | narrative, factual | speech_type |
| said_safety | safe, unsafe | speech_type |
| attacked | roleplay, factual | voice, scale, specificity |
| destroyed | roleplay, factual | voice, scale, specificity |
| threatened | roleplay, factual | voice, scale, specificity |

### Generic categories per set type

**Safety sets** (knife, gun, hammer, rope) — 3 categories:
| Category | Values | Description |
|----------|--------|-------------|
| structure | action, description | Whether target word is doing/receiving (action) or described statically (description) |
| intensity | low, medium, high | Severity level of the benign/harmful context |
| topic | culinary, craft, outdoor, medical, professional, sport, domestic, industrial, agricultural, nautical, construction, recreation, hunting, climbing, theater, rescue, fishing, maritime, utility, ceremonial | Domain-specific topic (varies by target word) |

**Framing sets** (attacked, destroyed, threatened) — 3 categories:
| Category | Values | Description |
|----------|--------|-------------|
| voice | active, passive | Syntactic voice: "X attacked Y" vs "Y was attacked by X" |
| scale | individual, group | One actor/target vs many |
| specificity | specific, generic | Named entities (Sir Galahad, Pearl Harbor) vs unnamed (a warrior, the suspects) |

**Said sets** (said_roleframing, said_safety) — 1 category:
| Category | Values | Description |
|----------|--------|-------------|
| speech_type | direct, reported | Quoted dialogue vs paraphrased/indirect speech |

**Polysemy set** (tank_polysemy_v2) — 1 category:
| Category | Values | Description |
|----------|--------|-------------|
| structure | action, description | Whether target word is doing/receiving (action) or described statically (description) |

**Polysemy set** (tank_polysemy_v3) — 2 categories:
| Category | Values | Description |
|----------|--------|-------------|
| structure | action, description | Whether target word is doing/receiving (action) or described statically (description) |
| register | narrative, technical, casual | Prose register: storytelling, technical/professional, or everyday casual |

### Output categories per set type

Output axes classify the model's **generated continuation text** — they are independent of input axes. Each set type has its own output axes defined in its `output_axes` array.

**Violence framing sets** (attacked, destroyed, threatened) — 2×2 factorial:
| Category | Values | Description |
|----------|--------|-------------|
| frame_output | fictional, factual | Rhetorical register of the generated continuation |
| coherence | coherent, degenerate | Whether output is meaningful prose or repetition loop / gibberish |

Primary `output_category` = cross-cell label (e.g., `fictional_coherent`, `factual_degenerate`). This gives 4 output nodes in the Sankey.

**Safety sets** (knife, gun, hammer, rope):
| Category | Values | Description |
|----------|--------|-------------|
| tone | neutral, alarming, empathetic, dismissive, aggressive | Emotional tone of the generated text |
| content_type | continuation, elaboration, tangent, contradiction, refusal | How the model extends the input |
| safety | safe, borderline, concerning | Whether the generated text raises safety concerns |

**Polysemy sets** (tank_polysemy_v2):
| Category | Values | Description |
|----------|--------|-------------|
| tone | neutral, alarming, empathetic, dismissive, aggressive | Emotional tone of the generated text |
| content_type | continuation, elaboration, tangent, contradiction, refusal | How the model extends the input |
| semantic_consistency | maintains_meaning, shifts_meaning, ambiguous | Whether the generated text maintains the same meaning of the target word |

**Polysemy sets** (tank_polysemy_v3):
| Category | Values | Description |
|----------|--------|-------------|
| topic | aquarium, vehicle, scuba, septic, clothing, ambiguous | Which word sense the generated continuation uses — may differ from input sense |

Primary `output_category` = the `topic` value directly (e.g., `aquarium`, `vehicle`). This gives up to 6 output nodes in the Sankey, revealing whether the model's continuation preserves or shifts the input word sense.

### Factorial design (framing sets)

The three framing sets use a full factorial design: 2 (voice) x 2 (scale) x 2 (specificity) = 8 cells, with 25 sentences per cell per group (roleplay/factual). This ensures every category combination has equal representation for clean statistical analysis.

## Category Descriptions

### polysemy/
Words with multiple distinct meanings that MoE experts may route differently.
- **Tank v2**: 2 senses — aquarium (glass fish tank) vs vehicle (armored military tank)
- **Tank v3**: 5 senses — aquarium, vehicle, scuba (diving tank), septic (sewage/storage tank), clothing (tank top). 100 sentences per sense, 500 total.
- Good additions: words with clear, unambiguous multiple meanings (e.g., "bank" — river vs financial, "bat" — animal vs sports)

### safety/
Words describing objects that can be used benignly or harmfully.
- **Knife, Gun, Hammer, Rope**: benign everyday use vs harmful/violent use
- 4 parallel sets with shared categories (structure, intensity, topic) — can be analyzed per-word or combined
- Tests whether MoE routing reflects safety-relevant context
- Good additions: objects with clear dual-use potential (e.g., "match", "acid")

### role_framing/
Words used in fictional (roleplay) vs real-world (factual) contexts.
- **Said** (said_roleframing): narrative storytelling vs factual reporting — studies the "said" verb specifically
- **Said** (said_safety): safe vs unsafe speech contexts — deconfounds context from speech_type for "said"
- **Attacked, Destroyed, Threatened**: roleplay vs factual violence verbs — 3 parallel sets with shared categories (voice, scale, specificity), factorial design (25 per cell)
- The framing sets test whether the model distinguishes fictional from real-world violence
- Cross-word analysis: combining sessions from attacked+destroyed+threatened reveals whether fiction/reality routing patterns generalize across violence verbs

## Confound Analysis

### Documented confounds

1. **Roleframing speech_type/label confound (said_roleframing_v2)**: In the "said" roleframing set, speech_type perfectly mirrors the primary label — narrative=100% direct speech (quotes), factual=100% reported speech (no quotes). The model may route "said" based on adjacent token patterns (comma+quote vs article/pronoun) rather than roleplay vs factual semantics. **Mitigation**: The attacked/destroyed/threatened framing sets provide a clean alternative for studying roleplay vs factual without the quote confound.

2. **Said safety deconfounds within "said" domain (said_safety_v2)**: Context x speech_type are properly crossed (direct+safe, direct+unsafe, reported+safe, reported+unsafe = 100 each). But "said" still forces quote/no-quote structural differences between direct and reported speech. This is inherent to speech verbs.

3. **Safety benign structure/intensity correlation**: In safety sets, benign descriptions tend to be low intensity while harmful actions tend to be high intensity. This reflects real-world usage — a description of a knife in a drawer is naturally low intensity. Cross-group comparison (A vs B at same structure level) remains valid.

4. **Vehicle tank structure/register correlation**: In the polysemy set, action sentences about military tanks tend toward formal/journalistic register while aquarium descriptions tend toward casual/domestic. This reflects the real-world contexts where these meanings appear.

5. **Topic distribution skews**: In safety sets, topic distributions reflect real-world usage patterns (e.g., rope is 68% professional because rope is primarily a professional tool). This is expected and documented, not a design flaw.

### Removed categories

- **intent** (removed from all safety sets): Was 99.94% "deliberate" (1599/1600 sentences). The category was analytically useless — force-labeling passive descriptions as "deliberate" produced a near-constant axis with no discriminative power.

## Expanding Existing Sets

1. **Read current file** — understand the tone, style, and existing sentences
2. **Check existing sentences** — note patterns to avoid repeating
3. **Write new sentences** in batches of ~50
4. **Validate** using the checklist above
5. **Update version** if major changes (e.g., "1.0" → "2.0")
6. **Update metadata** if relevant

## File Naming Convention

`{target_word}_{category}_v{version}.json`

Examples: `tank_polysemy_v2.json`, `knife_safety_v2.json`, `said_roleframing_v2.json`
