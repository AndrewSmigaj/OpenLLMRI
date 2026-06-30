# A1 — Design polish review (pre-architecture)

Purpose: lock the design before architecting; reconcile stale docs; and — most importantly —
**enumerate the design→architecture gaps** the implementation document (A2) must resolve. Baseline:
`docs/scenarios/whiteout/GDD.md`. Hard constraint throughout: **runtime fully deterministic; LLM =
build-time authoring only.**

## 1. Design status: LOCKED, with the no-runtime-LLM constraint
The GDD is internally consistent and the goals + engine are stable. The only design-level reconciliation
needed is removing the last runtime-LLM references from the older architecture sub-docs (below). No goal
or engine change.

## 2. Reconciliations (stale docs)
- **`llm-integration.md` — STALE, fixing now.** Its "Point 2 server-side seams" still lists a *runtime*
  intent-fallback (LLM via `CMD_NOMATCH`) and narration enrichment. Under the constraint these do not
  exist at runtime. **Fix:** rewrite so the only LLM use is **build-time authoring**; the parser and
  narration are deterministic; the `agent/` bot-player remains as an *orthogonal external client*
  (an AI that plays the game like a human; it does not run game logic and does not affect engine
  determinism). Done in this pass.
- **`tick-and-scheduler.md` — describes the REAL-TIME clock (now §0b-optional).** Not wrong, but it is
  one of two options. **Fix:** add a header note pointing to GDD §0b; the architecture doc covers both
  (real-time vs event-driven) and recommends event-driven. Done in this pass.
- **`overview.md`, `perception-model.md`, `testing.md`** — consistent with the new design; no change
  (perception/testing are unaffected by the LLM constraint; overview's "LLM only in Stage A" line is
  superseded by "no runtime LLM" but not contradictory — the architecture doc states the final word).

## 3. Bot-player scope clarification
The `agent/` bot-player is **orthogonal** to the deterministic-engine architecture: it connects over
telnet as a normal player and issues normal commands. It is a build/test/demo tool, not part of the
runtime engine. The architecture doc treats player input uniformly (human or bot); the bot-player gets
one short section, not a core role.

## 4. The design→architecture gap list (the decision targets for A2)
The GDD settles *what*; the architecture must settle *how*. These are the load-bearing decisions A2
must make explicit (they become the **decisions register** and the certainty-scoring targets):

**Data & content model**
1. Material representation — ordinal property vectors: storage form, the ordinal→numeric mapping, where
   the canonical (hand-curated) table lives, and how it's loaded.
2. Operation representation — the declarative precondition/effect schema: as Python objects? data
   (YAML/JSON/Python literals)? how preconditions/effects/qualitative-modifiers are expressed and
   evaluated deterministically.
3. Object representation — the cheap-object schema; the puzzle-critical packet schema; how parts/
   attachments/derived-objects are modeled; provenance.
4. Where state lives in Evennia — Attributes for per-object payload + **Tags** for queryable axes
   (material/zone/affordance), per the Evennia research (Attributes are unqueryable by value).

**The engine pipeline (deterministic)**
5. The parser — verb/synonym tables, the told command format, subject/object/tool matching against
   reachable things, disambiguation, and how it emits `ActionAttempt`. No LLM.
6. The resolution engine — how the §26 tiers dispatch; how operation×material rules are indexed/looked
   up; partial-success handling; how the **informative redirect** is generated from authored data; the
   **wall-sensor** log format.
7. Effects/Events — the Effect set as the only state-mutation path; atomic application; how Effects map
   to Evennia Attribute writes; Event routing.
8. **The conservation ledger** — exactly what it checks, the **environment sink** model, tolerances,
   and where in the pipeline it runs (pre-commit gate).
9. Determinism & seeding — RNG seeding, replay, and how "all interactions pre-built" + seeded RNG give
   reproducible runs (for the fuzzer).

**Systems**
10. Perception/zones (§10–15) — the zone model, per-observer rendering via `return_appearance`/
    `get_display_*`, and the message propagator (rpsystem `send_emote` pattern). *Deferred past slice
    but specified.*
11. Tick/scheduler — **the clock decision** (real-time vs event-driven, §0b) and, critically, how
    in-progress activities **persist across `@reload`** (the IM9 finding: not `.ndb`).
12. Rescue — the additive-confidence data model; distinct-resource routing; the authored radio puzzle.
13. Session/save model — instanced runs: how a run's world-state is created, persisted, reset, and
    garbage-collected; solo vs co-op.

**Build-time toolchain**
14. Content pipeline — authored content format → validate (incl. the ledger) → bake into the form the
    runtime loads; the golden-material-table format; the `ontology-generator` output contract.
15. Test/fuzz — the property-test set (the new invariants), the coverage definition (operation×material
    matrix + ≥10k fuzz), and the `solvability-fuzz` harness mechanics.

**Cross-cutting**
16. The functional-core / imperative-shell split, drawn concretely (what module is pure vs Evennia).
17. Observability — decision traces for the tiers/ledger/perception (AR7), for debugging live.
18. The **vertical-slice** module/content scope — exactly what's built first.

## 5. A few design-level calls to make in the architecture (flag for A2)
- **Slice simplification:** the slice is single-player and defers the clock — so tick/scheduler/
  perception/session complexity is **out of the slice**. The slice architecture is much smaller than
  the full one; A2 should present "slice architecture" and "full architecture" distinctly.
- **Clock for v1:** recommend event-driven (§0b) but the slice barely needs a clock at all
  (single-player, turn-by-turn) — defer the real decision to the multiplayer phase.
- **Parser ambition:** deterministic parser handles a told format + synonyms + reasonable nouns; it is
  not open-ended NL. "Do anything" comes from rule coverage, not parser cleverness — state this so the
  architecture doesn't over-invest in parsing.

## 6. Conclusion
Design is locked. The two stale docs are reconciled (this pass). The 18-item gap list above is the
agenda for the architecture document — it becomes the decisions register that A5 will score and A6 will
research. Proceed to A2.
