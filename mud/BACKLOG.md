# Backlog — Now / Next / Later

The single living list of what we're doing, next, and parked. One tactical board; the **strategic** phase
arc (P0–P7) lives in [`docs/scenarios/whiteout/roadmap.md`](docs/scenarios/whiteout/roadmap.md), and the
**closure loop** that now drives P2 lives in
[`docs/architecture/ontology-closure.md`](docs/architecture/ontology-closure.md) (DR-26). Work **one Now
item at a time**; deferred-but-designed items are two-line stubs linking to their design.

## Now  (work-in-progress limit: 1)
- **The design review — a conversation over `docs/design/`, one document at a time, in the index
  order** (`docs/design/README.md`); nothing is built and no agent runs a world-building loop until
  every document is finalized. Read `docs/investigation/design/00-provenance-audit.md` first (what is
  his, what Claude added, what was removed on 2026-09-16). The nine passes of 2026-09-07 are merged
  into `docs/design/` (`docs/investigation/design/`, each with a lens pass):
  rescue graph · time & stakes (now incl. sleep + the consensus clock, DR-14a) · events & escalation
  (the week-long run, the escalation ladder, the event menu — DR-15a) · moral & social layer · living
  rooms · fire & shaping · players & kit (the 206's honest interior: cargo net, hat shelf, 4 seats) ·
  phrasing corpus · grammar guide. Nothing in them is implemented until promoted — EXCEPT what Andrew
  decided outright on 2026-09-07 and is SHIPPED: the closure loop steps 1–2b, and **the crash draw**
  (slots, pockets, luggage, clothing v2 — commit 18bac60; probes 290/417; taught phrasings 79–83%).

## Next
- **Clarification-only feedback — the code catches up with DR-08c (Andrew, 2026-09-16; VISION.md
  "Never a menu"):** remove the verb suggestions from the parser nudge (`parser/grammar.py` `_NUDGE`
  and the "Did you mean" line) and from the tier-5 redirect (`resolver/redirect.py`, "but you could …");
  replace the numbered disambiguation menus (`cmd_act.py`, `cmd_items.py`, DR-08a) with `Which X do
  you mean?` and nothing more; `help grammar` becomes the forms with one example each; delete `help
  verbs`; `make X` and bare `use X` become clarifications, `use X on Y` resolves silently; drop the
  DR-09a sibling near-miss hint; probe steps name nouns unambiguously (the runner no longer picks the
  first option); **every unknown-word parse failure is logged to `gaps.jsonl`** so the next pass adds
  the synonym; run the agent phrasing samples early, after each synonym batch. Opus 5 implementer via
  the loop; the probe baseline must not drop (re-authored probes are not drops).
- **Step 3 — time & stakes** (after its docs are promoted): the activity scheduler on the heartbeat
  (attended actions with start/tick/interrupt/complete; unattended processes), **sleep / wait + the 20×
  consensus advance with event interrupts (DR-14a)**, the fire ladder, integer warmth (the clothing v2
  exposure fraction is its input) / hunger / injury on the clock, the warmth floor, wet/dry + temperature
  written by ops, **the escalation calendar + the seeded event deck (DR-15a; events-and-escalation.md)**.
  DR-27.
- **The 206's honest interior** (players-and-kit.md §5, on approval): cargo net + hat shelf + jammed
  cargo door replace the two bins; four seats 1A/1B/2A/2B + the right seat, each with different damage
  and finds; look-under (DR-24b). A content pass with a render read.
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
