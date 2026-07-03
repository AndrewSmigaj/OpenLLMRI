# Documentation Map — start here

Where everything lives, what's authoritative, and where new docs go.

## Tiers

**Authoritative — the design of record (trust these):**
- [`../VISION.md`](../VISION.md) — the anchor: what we build + the locked non-negotiables.
- [`scenarios/whiteout/GDD.md`](scenarios/whiteout/GDD.md) — the game design (FINAL).
- [`architecture/`](architecture/) — the architecture. `implementation-architecture.md` is the spine
  (its **DR-01…DR-23 decision register is our ADR log**); `overview.md` / `perception-model.md` /
  `presentation.md` / `tick-and-scheduler.md` / `llm-integration.md` / `testing.md` are focused views
  kept consistent with it.
- [`scenarios/whiteout/roadmap.md`](scenarios/whiteout/roadmap.md) — the **strategic** phased build order
  (P0–P7) with exit gates.
- [`guides/`](guides/) — authoring guides (objects, actions, workflows, validation).
- `game/world/sim/contracts.py` — the frozen contract dataclasses (here the **code** is the source of truth).

**Living / operational (changes often):**
- [`../BACKLOG.md`](../BACKLOG.md) — the single **Now / Next / Later** list: what's active, next, and parked.
  The tactical board (the strategic arc is `roadmap.md`).
- [`../README.md`](../README.md) — repo entry point + quickstart.
- [`../CLAUDE.md`](../CLAUDE.md) — orientation + rules for Claude Code.
- [`process.md`](process.md) — **how we work** (the design→document→implement loop).

**Scratchpad / exploratory — NOT authoritative (thinking-in-progress):**
- [`investigation/`](investigation/) — brainstorms, lenses, research probes.
- [`proposals/`](proposals/) — proposals under consideration.
- `~/.claude/plans/` — plan-mode working files.

**Archived (history, not current):**
- `scenarios/whiteout/design.md` — the original seed, superseded by the GDD (not authoritative).

## The rule
Scratchpads are for iterating. **Nothing gets implemented until the decision is promoted into the
authoritative docs.** The flow is in [`process.md`](process.md).

## Where a new doc goes
- A **decision** (especially hard-to-reverse / an invariant) → an entry in the DR register
  (`architecture/implementation-architecture.md`), or a standalone ADR in `architecture/adr/`.
- A **feature with real trade-offs** → a short design doc under `architecture/` (or the scenario) —
  after iterating in a scratchpad.
- A **task / idea** → [`../BACKLOG.md`](../BACKLOG.md) (Now/Next/Later).
- **Exploration** → [`investigation/`](investigation/).
