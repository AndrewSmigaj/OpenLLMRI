# Plan — Whiteout implementation-architecture document (overnight effort)

Goal: produce a **rigorous, polished, full-implementation architecture document** for Whiteout, with
its design quality *measured* and then *raised* through deep analysis and research. Each phase is a
separate focused pass — no rushing. Findings are written down as they're produced.

Design baseline (locked): `docs/scenarios/whiteout/GDD.md` (§0a improvements, §0b optional). Hard
constraint: **runtime is fully deterministic; the LLM is a build-time authoring tool only.**

## Deliverables
- **`docs/architecture/implementation-architecture.md`** — THE document (the full implementation
  blueprint). Evolves v1 → v2 (post-lens) → final (post-research).
- Working notes (findings written down): under `docs/architecture/review/`
  - `10-design-polish.md` — the pre-architecture polish review.
  - `20-lens-findings.md` — architectural/coding lens analysis (finding cards).
  - `30-certainty.md` — certainty analysis with the numeric system.
  - `40-research-notes.md` — online + Evennia + reasoning, to raise certainty.
  - `50-final-changes.md` — what the research changed, and the re-scored certainty.

## Phases (each its own task; do in order)
**A1 — Polish review of the design (lock it before architecting).** Re-read the GDD/proposal with the
no-runtime-LLM constraint; reconcile the stale arch sub-docs (`llm-integration.md`,
`tick-and-scheduler.md` describe the old runtime-LLM / real-time clock); list any design gaps the
architecture must resolve. → `10-design-polish.md` (+ targeted GDD/sub-doc fixes).

**A2 — Write the architecture document v1.** The full blueprint: a **decisions register** (every
load-bearing architectural decision, enumerated, so certainty has clean targets) + module/package
structure + the engine internals (data model for materials/operations/objects; the conservation
ledger; the deterministic parser; the §26 resolution tiers; effects/events; perception; tick/
scheduler; rescue; save/load/sessions) + the Evennia integration (typeclasses, cmdsets, scripts,
Attributes/Tags, message routing) + the build-time toolchain + data formats + test/fuzz strategy + the
vertical-slice implementation plan + key interfaces/contracts + text sequence diagrams + file layout.
→ `implementation-architecture.md` v1.

**A3 — Architectural/coding lens analysis (thorough; findings written down).** Apply the architecture +
implementation lens libraries (incl. the code-smell subset) to the v1 doc, via parallel subagents per
group; per-decision finding cards. → `20-lens-findings.md`.

**A4 — Update & polish the architecture document.** Fold every actionable lens finding into the doc.
→ `implementation-architecture.md` v2.

**A5 — Certainty analysis with a numeric system.** Establish a scoring rubric (Confidence 0–100 with
defined bands × Criticality weight × Evidence basis) and **score every decision in the register**;
compute a weighted overall architecture-confidence; rank the weakest decisions. → `30-certainty.md`.

**A6 — Investigate everything to raise certainty.** For each low-confidence / high-criticality decision
from A5: online research, Evennia docs/source dives, reasoned prototypes/thought-experiments — gather
evidence to confirm, improve, or replace the decision. Parallel research agents where useful.
→ `40-research-notes.md`.

**A7 — Final update.** Incorporate the research; revise decisions that need it; **re-score certainty**;
finalize the document. → `implementation-architecture.md` final + `50-final-changes.md`.

## Principles
- Don't rush; each phase is real work with a written artifact.
- The decisions register is the spine — it makes certainty scoring and research targeting clean.
- Evidence > opinion: prefer proven Evennia/CS patterns; cite. Where speculative, say so and lower the
  score.
- Keep the runtime-deterministic / LLM-build-time-only constraint inviolable throughout.
