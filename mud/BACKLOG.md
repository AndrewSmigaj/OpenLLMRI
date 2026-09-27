# Backlog — the Now slice of [`PLAN.md`](PLAN.md)

**The single tracked task list for the whole project is [`PLAN.md`](PLAN.md)** — every task, its status,
the design document that owns it, and what it waits on. This file shows only what is being worked now
and what comes next; the task ids are PLAN's. The current decisions, all in one place, are `PLAN.md`
§5. Work **one Now item at a time**.

**The rule** (PLAN §1): nothing is built and no agent runs a world-building loop until every document in
`docs/design/` is finalized. Phase B, the machine that runs the loops, is built in parallel because it
touches no design.

## Now  (work-in-progress limit: 1)
- **The sittings resume at document 10**, checking the answers Claude proposed in each document (marked
  *proposed by Claude, for Andrew's check*), one document at a time. Document 15's rules are decided.

## Next  (in this order — PLAN §0)
2. **The sittings resume in index order** (A1.10–A1.23, `docs/design/README.md`): each document's
   answers proposed by Claude are checked with Andrew, and every document is finalized at the close
   (A2–A8).
3. **A10** — the design documents for the systems the review found missing (combat, heat, hunting,
   trapping and fishing, food state and spoilage, animal behaviour, scent, light and darkness, weather,
   snow and ice on the ground, the body's physiology, two people acting on one thing, the tutorial
   rooms); then **A11** — the GDD's vision, broadened.

## In parallel — Phase B, the machine (ready to start; touches no design)
- **B1** the agent roster pinned to models, the hooks consolidated · **B3** `README.md` rewritten ·
  **B4** anchors and quickstart config · **B5** stale text in the code READMEs, the architecture views
  and the tooling · **B6** hygiene (`tools/bake.py`, `tools/coverage.py`, `seed.md` and the rest) ·
  **B9** the ontology store's full schema (document 05 §4.5) · **B12** the loop scaffold and queue ·
  **B14** the shipped narration and binding bugs.
- Waiting inside Phase B: B2 and B7 on B1; B8 (publish) on B3 and B4; B10 on B9; B11 on B10; B13 (the
  clarification-only feedback in code, DR-08c) on document 04's finalization.
