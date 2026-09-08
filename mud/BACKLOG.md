# Backlog — Now / Next / Later

The single living list of what we're doing, next, and parked. One tactical board; the **strategic** phase
arc (P0–P7) lives in [`docs/scenarios/whiteout/roadmap.md`](docs/scenarios/whiteout/roadmap.md), and the
**closure loop** that now drives P2 lives in
[`docs/architecture/ontology-closure.md`](docs/architecture/ontology-closure.md) (DR-26). Work **one Now
item at a time**; deferred-but-designed items are two-line stubs linking to their design.

## Now  (work-in-progress limit: 1)
- **Andrew reviews the seven design passes** (`docs/investigation/design/`, each with a lens pass):
  rescue graph · time & stakes · moral & social layer · living rooms · fire & shaping · phrasing
  corpus · grammar guide. Nothing in them is implemented until promoted. *(Steps 1–2b of the closure
  loop SHIPPED 2026-09-07: closure, the harness, parser tolerance — commits f1f8e23…13e7a9e; probes
  261/388 at the ratchet; taught-agent phrasings parse 79–83%.)*

## Next
- **Step 3 — time & stakes** (after its two docs are promoted): the activity scheduler on the heartbeat
  (attended actions with start/tick/interrupt/complete; unattended processes), the fire ladder, minimal
  integer warmth / hunger / injury on the clock, the warmth floor, wet/dry + temperature written by ops.
  DR-27.
- **Steps 4–5 — the overnight loop** (`build-queue.md` Phase C, `/loop 30m`, one probe cluster per firing):
  tier-4 generic physics; the verb gaps the censuses and the agent samples voted for (spin, strike, tape,
  press, arrange, fill, blow, sit, listen, smell, feel, adjust, wave, fix, scrape, cover/block, push/pull/
  drag, throw, unscrew, warm); scenery + elusive pseudo-nouns.
- **The valley (world design) — implements as data** once steps 1–5 land: the 50 outdoor zones from
  [`docs/investigation/world/`](docs/investigation/world/) become `OBJECT_TABLE` / zone / space rows,
  rendered and READ, not hand-built in Python. Outdoor rooms are traversal terrain; the systems are the
  content. (The Phase-1 gate in `build-queue.md` waits behind Phase C.)
- **Mudlet integration write-up** — research done; the write-up + a proposed Whiteout Mudlet setup pending
  ([`docs/client/mudlet-research.md`](docs/client/mudlet-research.md)).

## Later  (the big boulders — see `roadmap.md` P5–P7 for the strategic detail)
- **Chunk-after-mastery** — a procedure done once becomes a single long activity (`make fire with bow
  drill`); the Hadean Lands mechanic; offered never imposed. After the base fire paths work.
- **The pure-world play harness** (`tools/play.py`) — an LLM brain drives parse → resolve → apply in
  `PureWorld`, logging trajectory JSONL + gaps (an external player, ADR-0005); then the telnet bot harness
  with the `@OBS` line (plain text — OOB needs a GMCP handshake a bare socket never does).
- **Rescue content** (P5) — the radio/ELT state machines, the hatchet repair, the match-drying loop, flare
  ignition, the extinguisher — the tier-1 authored seam is wired in step 2; content lands from the rescue
  graph.
- **Randomness / dice** — parked; deterministic, variety from route economics; revisit at P5.
- **Status / time updates + colors** — surface the clock + survivor status (ties to Mudlet/GMCP).
- **Presentation v2/v3 leftovers** — masses, three-form phrases, glimpse lines, DR-24b look-under (the
  living-rooms pass decides which survive after Andrew reads a render).
- **Containment/clothing v2** — liquid containers (drink-from / pour-into / fill), capacity, `give`, sit/
  posture, layering curves, leading-count taking, cutting a filled container spills.
- **Scattered-wreck v2** — the cargo-net re-skin (a data-row edit now), the V. HOLT cabin as a Scene, wing
  fuel drains; the satcom is omitted.
- **Lenses skill rework** — right-size the libraries (the `certainty` skill, now promoted, covers the
  pre-implementation gate).
- **break derived-id collision (latent)** — `_shatter` ids are `derived_id(parent, f"{piece_word}{i}")`;
  breaking two parts of one entity would collide. Give break the part-scoped shape when touched next.
- The rest of the phased arc — survival + rescue (P5), instanced co-op (P6), weather + ending (P7).
