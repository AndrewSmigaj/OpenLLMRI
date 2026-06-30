---
name: ontology-generator
description: Generate Whiteout ontology content — materials (property vectors), operations (declarative precondition/effect schemas), and cheap objects — from the design schemas, using generate-then-validate so output passes `make validate`. Use when fleshing out the interaction ontology for the crash scene or adding materials/operations/objects. The LLM proposes; the validator disposes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Ontology generator — LLM authors content, the validator gates it

Implements the proposal's "LLM at the authoring edge" (see
`docs/proposals/whiteout-engine-proposal.md` §3–§4) with the **generate-then-validate** discipline
from `docs/investigation/research/prior-art.md` (LIGHT/COMET). The deterministic engine + validator
are the ground truth; this skill never writes runtime state, only content that must pass the gate.

## The inversion you are authoring toward
- **Objects are cheap:** `{materials, parts?, size, mass, tags, state}`. Do NOT author per-object
  affordance lists — behavior derives from operations over materials.
- **Materials are the real content:** ordinal property vectors (cut/tear/bend resistance,
  burnability, ignition difficulty, smoke toxicity, insulation, conductivity, edibility…). Reason
  **qualitatively** (low/med/high, more/less/enough); the engine maps ordinals to numbers.
- **Operations are declarative:** roles, preconditions, qualitative modifiers, effects (with
  conservation), partial-success, and an **informative** failure. ~20 operation categories (design §5).

## Procedure
1. **Read the schemas first:** the relevant authoring guide (`docs/guides/authoring-{objects,actions}.md`),
   the §43 templates, the property schema, and the VISION non-negotiables. Match field names exactly.
2. **Generate qualitatively.** Propose the material vector / operation schema / object as data.
   For materials, use ordinal grades + a one-line justification per property. For operations, write
   precondition/effect/partial/failure in the declarative form; never bake in numbers the engine
   owns.
3. **Guard against hallucinated capabilities.** Every claimed affordance must be *derivable* from a
   material property or an operation precondition. If you can't ground it, drop it (this is the #1
   LLM-authoring failure mode — AR16/IM3).
4. **Validate (the gate).** Run `make validate SCENARIO=<name>` (and, where logic exists, the
   relevant property tests). Treat any failure as a defect to repair, not override.
5. **Repair loop.** Fix → re-validate until green. **Record the repair count** (it is the IM3
   throughput metric — high repair rates mean the schema or prompt needs work, not more generation).
6. **Conserve (design §24).** Any transformation effect must preserve material/mass/temperature/
   wetness/contamination/provenance. The validator enforces it; author as if it will.
7. **Hand invariants to tests.** If you author a new operation, propose its property test (give it to
   the `sim-test-writer` subagent): it resolves, it conserves, partial success keeps progress, failure
   is informative.

## Crystallize mode (runtime tail)
When fed entries from the **wall-sensor log** (attempts that fell through to generic-redirect),
propose the missing operation×material rule constrained to existing operations + the target's state,
validate it, and emit it as a new rule for review — the resolve-then-crystallize loop
(`proposal §3.6`). Same gate; no exceptions.

## Output
Write content into the scenario's `objects/`, `materials/`, or the engine's `operations/`, following
`docs/guides/adding-a-scenario.md`. Report: what was generated, validate result, repair count, and any
capability you dropped for lack of grounding.

## Do NOT
Invent numeric survival math, write runtime/engine state, or add an affordance that no material
property or operation precondition supports. The engine owns mechanics; you author *content that the
engine can run*.
