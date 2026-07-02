# Backlog — Now / Next / Later

The single living list of what we're doing, next, and parked. One tactical board; the **strategic** phase
arc (P0–P7) lives in [`docs/scenarios/whiteout/roadmap.md`](docs/scenarios/whiteout/roadmap.md). Work **one
Now item at a time**; deferred-but-designed items are two-line stubs linking to their design.

## Now  (work-in-progress limit: 1)
- **Finish the item-interaction slice** — get the verbs / materials / transforms into "a format we like"
  (iterate until it feels right). Active sub-item:
  - **Disambiguation + naming + bare-hands fix** — a numbered menu to pick among identical objects; real
    derived names ("glass shard", not "shard glass"); the pick preserves the whole command; fix the "The
    your bare hands…" narration. *(Live bug; item-interaction, not perception.)*

## Next
- **Presentation / perception evolution** — scene-as-prose room look + state-conditioned object appearance +
  the look-tree + prominence/salience. Orthogonal to item-interaction. The design was iterated in-session
  and **not saved as a doc** — redraft in a scratchpad when picked up, then promote to an authoritative
  design doc.
- **Mudlet integration write-up** — the research pass is done (findings gathered); writing them up into
  [`docs/client/mudlet-research.md`](docs/client/mudlet-research.md) (currently a skeleton) + a brainstorm
  doc with a proposed Whiteout Mudlet setup are pending.

## Later  (the big boulders — see `roadmap.md` P2–P7 for the strategic detail)
- **Randomness / dice-rolling for conditions** — decide whether/where to introduce RNG (runtime is
  deterministic today; the seed seam exists).
- **Status / time updates** — surface the running clock + survivor status to the player (and to clients,
  e.g. GMCP — ties to the Mudlet work).
- **Colors** — subtle greys for "different" + reserved special-state colors (blood, fire); try it and get
  friends' feedback.
- **Build-time authoring pipeline** — draft the appearance/content library, validate, and bake.
- **Multi-zone perception** — the overlapping-zones / perception-bands system (roadmap P3).
- **A shippable Mudlet client package** — mapper feed, GUI gauges, auto-install.
- **Lenses skill rework** — right-size the lens libraries (currently overkill for routine checks; the
  `certainty` skill — draft in [`docs/proposals/certainty-skill-draft.md`](docs/proposals/certainty-skill-draft.md) —
  covers the pre-implementation gate).
- The rest of the phased arc — ontology breadth (P2), scheduler (P4), survival + rescue (P5), instanced
  co-op (P6), weather + ending (P7). See `roadmap.md`.
