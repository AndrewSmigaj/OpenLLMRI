# Documentation Map — start here

Where everything lives, what's authoritative, and where new docs go.

## Tiers

**Authoritative — the design of record (trust these):**
- [`../VISION.md`](../VISION.md) — the anchor: what we build + the core decisions.
- [`design/`](design/) — **the design of record, one document per system**, in review order; the index,
  the review procedure and the template are in [`design/README.md`](design/README.md). A system's design
  (the what and why, Winter Survival content included) lives here; its mechanism (the how) lives in
  `architecture/`. Each document's banner says whether it is a draft, reviewed, or finalized.
- [`scenarios/winter_survival/GDD.md`](scenarios/winter_survival/GDD.md) — the umbrella: pitch, vision, cross-cutting rules, and the chapter index into `design/`.
- [`architecture/`](architecture/) — the architecture. `implementation-architecture.md` is the spine
  (its **DR-01…DR-23 decision register is our ADR log**); `overview.md` / `perception-model.md` /
  `presentation.md` / `tick-and-scheduler.md` / `llm-integration.md` / `testing.md` /
  **`ontology-closure.md`** (forms, derived capabilities, tier-4 physics, the probe corpus) are focused
  views kept consistent with it.
- [`guides/`](guides/) — authoring guides (objects, actions, workflows, validation).
- `game/world/sim/contracts.py` — the frozen contract dataclasses (here the **code** is the source of truth).

**Living / operational (changes often):**
- [`../PLAN.md`](../PLAN.md) — **the program: every task, tracked** — phases, statuses, the design document that
  owns each task, what it waits on, the decisions Andrew must make, and the rule that lets the loops' additions
  flow back into the design and into new tasks. **The single task list.**
- [`../BACKLOG.md`](../BACKLOG.md) — the Now slice of `PLAN.md`.
- [`../README.md`](../README.md) — repo entry point + quickstart.
- [`../CLAUDE.md`](../CLAUDE.md) — orientation + rules for Claude Code.
- [`process.md`](process.md) — **how we work** (the design→document→implement loop).

**Scratchpad / exploratory — NOT authoritative (thinking-in-progress):**
- `~/.claude/plans/` and the session scratchpad — working files, never the design of record.

## The rule
Scratchpads are for iterating. **Nothing gets implemented until the decision is promoted into the
authoritative docs.** The flow is in [`process.md`](process.md).

## Where a new doc goes
- A **decision** (especially hard-to-reverse / an invariant) → an entry in the DR register
  (`architecture/implementation-architecture.md`), or a standalone ADR in `architecture/adr/`.
- A **feature with real trade-offs** → a short design doc under `architecture/` (or the scenario) —
  after iterating in a scratchpad.
- A **task / idea** → [`../BACKLOG.md`](../BACKLOG.md) (Now/Next/Later).
- **Exploration** → the session scratchpad; what survives is promoted into `docs/design/`.
