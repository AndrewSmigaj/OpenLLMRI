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
- **Presentation v1 SHIPPED** (2026-07-03, DR-23 — [`docs/architecture/presentation.md`](docs/architecture/presentation.md)):
  scene-as-prose `look`, salience weighting, unified look-at/examine renderer, full appearance
  content for the crash cabin (Andrew tunes the voice in `appearance.py`). **v2 leftovers → Later.**
- **P3 zones/perception SHIPPED** (2026-07-03, DR-13a, pulled ahead of P2 —
  [`docs/architecture/perception-model.md`](docs/architecture/perception-model.md)): the 7-zone
  crash site (`zones.py` content — Andrew tunes geography + survey prose), go/approach movement,
  the §14 fading look, band-routed events, the §17 reach gate, zone-aware say/whisper/call/shout.
  **Building out the plane is now authored zone content**, not plumbing.
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
- **Perception polish (post-P3)** — `look <direction>` / `scan`; targeted `whisper <player> =`;
  move durations + auto-pathing (P4, the `duration_minutes` seam is plumbed); planar-distance
  banding + finer occlusion; real weather banding (P7 — the `weather=` parameter is the seam).
- **A shippable Mudlet client package** — mapper feed, GUI gauges, auto-install.
- **Fragment affordances** — minted fragments carry no tool capabilities: a glass shard has no `edge`
  state (`_shatter` sets only material/mass/provenance), so "cut X with shard" counts as bare hands;
  the DR-05a `{material}_scrap` objects have the same gap. The improvised-glass-knife loop wants a
  material→affordance rule for derived objects — a small design decision first, then trivial to
  implement. *(Found during the 2026-07 slice-fix certainty audit.)*
- **break derived-id collision (latent)** — `_shatter` ids are `derived_id(parent, f"{piece_word}{i}")`,
  so breaking two different parts of one entity would collide sim_ids; the DR-05a scrap ids are
  part-scoped and immune. Give break the part-scoped shape when touched next.
- **Presentation v2** — the deferred DR-23 answers: state-conditioned ROOM desc (fire-lit cabin reads
  differently), authored hiding (waits for/with P3 perception), per-part examine prose, richer
  connective frames. Design decisions recorded in `docs/architecture/presentation.md`.
- **Lenses skill rework** — right-size the lens libraries (currently overkill for routine checks; the
  `certainty` skill — draft in [`docs/proposals/certainty-skill-draft.md`](docs/proposals/certainty-skill-draft.md) —
  covers the pre-implementation gate).
- The rest of the phased arc — ontology breadth (P2), scheduler (P4), survival + rescue (P5), instanced
  co-op (P6), weather + ending (P7). See `roadmap.md`.
