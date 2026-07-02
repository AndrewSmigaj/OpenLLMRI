# How we work — the loop

Right-sized for a solo dev + Claude Code on an experimental project. **Continuous flow, one thing at a
time** — no sprints, story points, or standups. **Waterfall on *design*, agile on *implementation*.**

## The loop (per work item)
1. **Pick one `Now` item** from [`../BACKLOG.md`](../BACKLOG.md) — work-in-progress limit: one.
2. **Design just enough:**
   - Touches an **invariant / hard-to-reverse** decision → a short **ADR** (Title · Context · Decision ·
     Status · Consequences) in the DR register (`architecture/implementation-architecture.md`) or a
     standalone file in `architecture/adr/`. Append-only — supersede, never rewrite.
   - **Real trade-offs** to weigh → a 1–3 page **design doc** — after iterating in a scratchpad.
   - **Obvious** → write nothing.
3. **Promote the decision into the authoritative docs.** Nothing gets implemented until it's documented there.
4. **Implement behind a seam** — build the extension point now, the concrete feature/content later; tolerate
   duplication until the third use (don't extract the wrong abstraction early). This *is* the
   no-fragile-refactoring rule.
5. **Verify — Definition of Done:** `make verify` (+ the relevant tests) green **and you've seen it run**.
   The four lint gates (`tools/lints/*`) are the automated "sensors" — they enforce the seams mechanically.
6. **Commit small — docs + code in the *same* commit** (so the docs can't drift from the code).
7. **Reconcile the backlog** — anything designed-but-deferred → a two-line `Later` stub linking to its
   design; prune stale items; pick the next `Now`.

## Doc tiers (see [`README.md`](README.md))
Authoritative (design of record) · living (BACKLOG, README, CLAUDE.md) · scratchpad (investigation/,
proposals/, plan files) · archived. **Scratchpads iterate; authoritative docs decide.**

## Working with Claude (keeps the agent on-rails)
- **One concern per session;** state explicitly what's **out of scope**.
- The built-in **Explore and Plan subagents do NOT read `CLAUDE.md`** — restate any rule they must obey in
  their prompt.
- Treat AI output like a junior's pull request: **read and understand it before it ships;** feed gate/test
  failures straight back.
- Durable facts/rules → `CLAUDE.md`; procedures → skills / this doc; guarantees → hooks + gates; ephemeral
  plans → the plan file (never `CLAUDE.md`).
