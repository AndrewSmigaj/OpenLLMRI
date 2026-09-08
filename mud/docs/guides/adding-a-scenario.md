# Adding a Scenario

This repo (`MUDExperiments`) is a reusable **simulation engine** that hosts **many scenarios**. Whiteout is
the first. This guide shows how to add another under `game/world/scenarios/<name>/` and load it.

> The engine (`world/sim/**`) is scenario-agnostic. A scenario is *content*: tables of zones, spaces,
> objects, materials, prose and responses, plus probes and a build loader. See
> [../architecture/overview.md](../architecture/overview.md).

## Layout (as of the closure loop, 2026-09-07)
```
game/world/scenarios/<name>/
  __init__.py
  manifest.py          # name, version, starting zone, world-clock defaults
  zones.py             # ZONE_TABLE: positions, edges (walk/see/muffle), terrain, survey prose — §12
  spaces.py            # SPACE_TABLE: the named areas inside each zone (frames, caps, default) — scene spaces
  objects.py           # OBJECT_TABLE: every object as a row (materials, mass, state, parts, zone | in)
  materials/table.py   # MATERIAL_TABLE: ordinal property vectors + tags (the quality anchor, DR-04)
  appearance.py        # APPEARANCE: scene phrases, examine prose, read text, per-form generics
  responses/           # RESPONSES: the narration templates (<op>.<outcome>)
  authored.py          # AUTHORED: tier-1 per-object rules for puzzle-critical things (radio, ELT…)
  probes/              # PROBES: typed command chains with expected outcomes + BASELINE (DR-18a)
  build.py             # build(): the generic loader — creates the room + walks OBJECT_TABLE into Evennia
```
Verbs are engine-level (`world/sim/operations/handlers/`) and shared across scenarios (DR-05b).

## What each piece does
- **manifest.py** — identity + defaults.
- **zones.py / spaces.py** — the perceptual space (DR-13a) and the scene composition (scene spaces). A zone
  is a position Attribute inside one Evennia Room, not a room.
- **objects.py** — the objects ([authoring-objects.md](authoring-objects.md)). The same table feeds the
  Evennia loader and the pure `PureWorld` used by probes and fuzz.
- **materials/table.py** — the materials the operations read.
- **appearance.py / responses/** — the voice. Tune freely.
- **authored.py** — the exceptions: `AUTHORED = {sim_id: rule}` where `rule(attempt, world, materials)`
  returns an `ActionResult` or `None` (falls through to the normal tiers).
- **probes/** — the scenario's executable coverage (`make probes`).
- **build.py** — `build()` must be **idempotent**; it creates the Room, sets its `default_zone`/`seed`,
  and calls the shared loader over `OBJECT_TABLE`.

## The build loader contract
```
make load-scenario SCENARIO=<name>
# -> docker compose run --rm --entrypoint evennia evennia shell \
#       -c "from world.scenarios.<name>.build import build; build()"
```
`--entrypoint` is required because the image word-splits arguments
([docker-workflow.md](docker-workflow.md)). `SCENARIO` defaults to `smoketest`.

## Steps to add one
1. `mkdir game/world/scenarios/<name>/` and create the layout above.
2. Write `manifest.py`, `zones.py`, `spaces.py`, `materials/table.py`.
3. Author `objects.py` rows and `appearance.py` entries; add responses for any new outcome.
4. Write probes for what the scenario promises (cite the design doc / census row for each).
5. **Validate** (no server needed): `make validate SCENARIO=<name>`; `make probes`.
6. **Render and READ**: `make render-scenes` → `docs/review/render-<date>.md`.
7. **Load and play:** `make load-scenario SCENARIO=<name>`, then `make up` and `telnet localhost 4000`.
8. Document it from [`../scenarios/_TEMPLATE.md`](../scenarios/_TEMPLATE.md) under `docs/scenarios/<name>/`.

## Related
[docker-workflow.md](docker-workflow.md) · [authoring-objects.md](authoring-objects.md) ·
[authoring-actions.md](authoring-actions.md) · [validation-rules.md](validation-rules.md)
