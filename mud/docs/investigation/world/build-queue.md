# The world build queue — the loop's shared state

> **Status: SCRATCHPAD / OPERATIONAL — 2026-07.** This is the resumable backbone for the overnight
> `/loop` that builds the whole valley. Every firing reads THIS file, does a bounded chunk, ticks the
> boxes, commits, and stops. Because state lives here + in git, the job survives any token-limit reset:
> the next firing (or a `claude --resume`) just continues from the first unchecked box. **59 zones:
> 9 built (retouch), 50 to build.**

## The bounded-firing rule (this is what makes spacing work)
Each loop firing does **ONLY the next 2 unchecked rooms**, then STOPS. Never "start the whole list."
Doing a small bounded chunk per firing is the entire point — it keeps each burst under the rolling
5-hour token budget so the work spreads across the night instead of exhausting one window and dying.

## Per-room pipeline (Andrew's order: build first, then everything else)
For each room, in this order:
1. **BUILD** it in code, in the space model: `zones.py` entry (pos / edges / terrain / exposure /
   survey line) · objects + their spaces & appearance prose (tell/hide calibration: show functional
   flavor, hide anything that shortcuts a puzzle) · any new materials/operations it needs · wired
   into `build.py`, `appearance.py`, `spaces.py`.
2. **CENSUS** → the room's official doc (`docs/scenarios/whiteout/rooms/<zone>.md`): *if this were the
   real world, not a MUD* — every entity (physical objects AND elusive things: air, wind, light,
   sound, cold, smell, damp…), then for each entity every action/relation you could apply (monadic
   and polyadic — ontology verbs), each with a candidate MUD command. Thorough, not the gist.
3. **GAP** — compare the census against what got built; list recommended adds/changes to pass the
   "does this virtual room reflect a real-world ontology" bar; apply the clear wins now, log the rest.
4. **VERIFY + COMMIT** — `make validate` (§44 hard gate) + `make test-host`; commit the room + its doc
   together; tick its box here.

## Phase 0 — FOUNDATION (paced across firings; the 50 rooms are GATED on ALL of these)
Chunked so each /loop firing does ONE box, then STOPS. Do NOT start any outdoor room until every
Phase-0 box below is ticked. (Boxes refined from the original 3 on 2026-07 so the loop resumes at the
first unchecked box instead of redoing partial work.)

- [x] **A · Engine core** — `world/sim/space/spaces.py` (frozen `Space` + `load_spaces`) +
  `scenarios/whiteout/spaces.py` (per-zone `SPACE_TABLE`: the plane + its immediate outside) +
  `presentation.compose_scene()` rewrite (group by `state['space']`/appearance home, survey order,
  empty-space omission, anchors as sentences, `_and_join`, `cap`→overflow, spaceless fallback) +
  `rooms.py` effective-zone stamp + appearance `space`/`anchor` on the plane's objects + the stale
  "weighting, never hiding" docstrings cleaned (superseded by DR-24). Pure suite (170) + 4 gates green.
  *(NOT yet: placement/look-at of dropped items = box B; live read + integration = box F.)*
- [x] **B · Placement** — `drop` space-picker (explicit `drop X on/in <space>` → default space via
  `at_drop` → an "ask" listing the zone's spaces when a named place is unknown), writing `state['space']`
  via a `set_attr` Effect; and `look at <space>` (id/alias + overflow-word match, rendered uncapped).
  All shell-side (cmd_items + objects.at_drop) calling pure resolvers (`spaces.resolve_space`,
  `presentation.look_space`) — no parser / examine-op / put-op changes, no new EffectKind. Pure suite
  (172) + integration (67) green. *(Explicit place + a multimatch menu falls back to the default space
  on the numbered pick — the re-issue drops the "on <space>" clause; acceptable, logged.)*
- [x] **C · Authored the plane's spaces + prose** to the tell/hide rule and READ the rendered scenes
  (cockpit · mid_cabin · rear_cabin · outside_nose · fuselage_top · outside_tail, via a scratch render
  harness). Retuned ~14 scene phrases so every non-anchor phrase is a NOUN PHRASE carrying CHARACTER
  not position (the frame owns position): stripped baked-in positions, killed comma collisions, fixed
  "blanket spilled from a bin" (history→character). The read surfaced three composer bugs, now fixed:
  aggregates render INSIDE the frame ("…are a jerry can and two quarts of engine oil"), a lone
  aggregate takes "are", and a real pluralizer ("branches", not "branchs"). Census/gap **moved to box
  E** (it was duplicated across C/D/E). Pure (172) + integration (67) green.
  *(Deferred — cross-zone BANDED lines only, NOT same-zone prose: "an oxygen masks" (a plural-named
  single object, mis-articled) and "a dry grass"; fold into box D, which authors those zones, or box F.)*
- [x] **D · The rest of the crash cluster** — authored a ground space per exterior zone (debris_trail
  the_scar · tail_section the_snow · treeline under_spruces), the notable containers as full-sentence
  anchors (survival duffel + mail sack; tail cone + freight crate; the spruce), the scatter in the
  frame. Fixed a real content bug (treeline dry grass read "jammed in a seat rail" — a cabin phrase
  outdoors) and folded in the deferred banded nits: a `mass` flag bares plural/mass names ("oxygen
  masks", "dry grass") in the far view, and band-0 "clear" now collapses ANY anchor to its bare name
  (a full-sentence anchor was dropping into a comma list a zone away). All 9 crash rooms now render in
  the space model. Census/gap → box E. Pure (173) + int (67) green.
- **E · Census + gap sweep** — each crash room gets its official `docs/scenarios/whiteout/rooms/<zone>.md`:
  the real-world ontology census (every entity incl. the elusive — air / cold / light / sound / smell;
  every action & relation with a candidate MUD command, monadic + polyadic) → gap-analysis vs the built
  room → clear+safe wins applied, the rest logged as recommendations. **~1–2 rooms per firing**; cockpit
  first as the exemplar template.
  - [x] cockpit — `rooms/cockpit.md`; 13 built entities + elusive census; gaps logged (top recs:
    `smell`/`listen` sense verbs, glass-shard blade from the windscreen, strip-the-body, scenery nouns)
  - [ ] mid_cabin
  - [ ] rear_cabin
  - [ ] outside_nose
  - [ ] fuselage_top
  - [ ] outside_tail
  - [ ] debris_trail
  - [ ] tail_section
  - [ ] treeline
- [ ] **F · Verify live + integration** — boot, `look` each of the 9, READ the prose against the
  tell/hide rule; `make verify` (gates + pure + integration) fully green.

### GATE — Phase 1 unlocked?  ⛔ NOT YET
Andrew flips this to ✅ after reviewing the foundation. While ⛔, firings do nothing but re-verify.
*(Andrew: set this to ✅ when the engine + the 9 rooms' voice look right.)*

## Phase 1 — the 50 outdoor rooms (2 per firing, in build order)

### S2 — Muskeg
- [ ] tussock_flat
- [ ] labrador_thicket
- [ ] tamarack_island
- [ ] drifted_channel
- [ ] lake_gate_willows

### S3 — Lake
- [ ] shore_apron
- [ ] ice_flat
- [ ] pressure_ridge
- [ ] inlet_mouth
- [ ] outlet_narrows
- [ ] far_shore_burn

### S4 — North Wood
- [ ] forest_edge
- [ ] big_spruce_hollow
- [ ] deadfall_tangle
- [ ] grouse_thicket
- [ ] hare_runs
- [ ] tree_well_hollow

### S5 — Strike Path
- [ ] shear_line
- [ ] wing_in_the_trees
- [ ] gear_gouge
- [ ] bench_saddle

### S6 — Ridge
- [ ] krummholz_band
- [ ] boulder_field
- [ ] the_knob
- [ ] lee_cornice

### S7 — Birch Stand
- [ ] aspen_fringe
- [ ] birch_grove
- [ ] chaga_tree
- [ ] game_trail_crossing

### S8 — Creek
- [ ] outlet_riffle
- [ ] gravel_bar_willows
- [ ] overflow_bend
- [ ] logjam_crossing
- [ ] confluence_pool

### S9 — Beaver Pond
- [ ] dam_crossing
- [ ] pond_flat
- [ ] the_lodge
- [ ] food_cache_margin
- [ ] drowned_set

### S10 — Trapline
- [ ] blaze_gateway
- [ ] spruce_tunnel
- [ ] marten_set_tree
- [ ] cabin_gate

### S11 — Holt's Homestead
- [ ] dooryard
- [ ] porch
- [ ] cabin_interior
- [ ] loft
- [ ] cache
- [ ] woodshed
- [ ] water_hole_path
