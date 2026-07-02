# Backlog — Now / Next / Later

The single living list of what we're doing, next, and parked. One tactical board; the **strategic** phase
arc (P0–P7) lives in [`docs/scenarios/whiteout/roadmap.md`](docs/scenarios/whiteout/roadmap.md). Work **one
Now item at a time**; deferred-but-designed items are two-line stubs linking to their design.

## Now  (work-in-progress limit: 1)
- **Finish the item-interaction slice** — get the verbs / materials / transforms into "a format we like"
  (iterate until it feels right). Shipped so far: disambiguation + naming + bare-hands (M1–M3,
  DR-08a) · stock get/drop numbered menus (DR-08a append) · **attachment honesty** — destructive
  extraction + explain-why/near-miss redirects (DR-05a/DR-09a, 2026-07-02). Next sub-item is
  Andrew's call — natural candidate: **fragment affordances** (Later, below).

## Next
- **Presentation / perception evolution** — scene-as-prose room look + state-conditioned object appearance +
  salience weighting + the unified look-at/examine renderer. Orthogonal to item-interaction. **Design
  redrafted**: [`docs/investigation/presentation.md`](docs/investigation/presentation.md)
  (scratchpad) — awaiting Andrew's review; promote to an authoritative doc, then implement.
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
- **Fragment affordances** — minted fragments carry no tool capabilities: a glass shard has no `edge`
  state (`_shatter` sets only material/mass/provenance), so "cut X with shard" counts as bare hands;
  the DR-05a `{material}_scrap` objects have the same gap. The improvised-glass-knife loop wants a
  material→affordance rule for derived objects — a small design decision first, then trivial to
  implement. *(Found during the 2026-07 slice-fix certainty audit.)*
- **break derived-id collision (latent)** — `_shatter` ids are `derived_id(parent, f"{piece_word}{i}")`,
  so breaking two different parts of one entity would collide sim_ids; the DR-05a scrap ids are
  part-scoped and immune. Give break the part-scoped shape when touched next.
- **Lenses skill rework** — right-size the lens libraries (currently overkill for routine checks; the
  `certainty` skill — draft in [`docs/proposals/certainty-skill-draft.md`](docs/proposals/certainty-skill-draft.md) —
  covers the pre-implementation gate).
- The rest of the phased arc — ontology breadth (P2), scheduler (P4), survival + rescue (P5), instanced
  co-op (P6), weather + ending (P7). See `roadmap.md`.
