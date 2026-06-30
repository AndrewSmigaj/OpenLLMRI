# Adding a Scenario

This repo (`MUDExperiments`) is a reusable **simulation engine** that hosts
**many scenarios**. Whiteout is the first one. This guide shows how to add
another under `game/world/scenarios/<name>/` and load it.

> The engine (`world/sim/**`) is scenario-agnostic. A scenario is *content*:
> authored scenes, zones, objects, action tweaks and workflows, plus a build
> loader that writes them into Evennia. See
> [../architecture/overview.md](../architecture/overview.md).

## Layout

```
game/world/scenarios/<name>/
  __init__.py
  manifest.py        # name, version, starting scene/zone, world-clock defaults
  scenes.py          # Scenes (each becomes one Evennia Room) — design §10
  zones.py           # Zone coordinates/terrain within each scene — §12
  objects/           # ObjectPackets (one module per major object) — §43.1
  workflows/         # WorkflowPackets — §43.3
  build.py           # the loader: build() — instantiates everything into Evennia
```

Action *families* are usually engine-level (`world/sim/actions/families/`) and
shared across scenarios; only scenario-specific authored overrides (the §26
AUTHORED tier) live under the scenario.

## What each piece does

- **manifest.py** — identity + defaults: `starting_scene`, starting zone, and the
  world-clock seed (`day`/`hour`/`minute`/`weather`/`temperature_c`, §9.2).
- **scenes.py** — each Scene is **one Evennia Room** ([ADR-0004](../architecture/adr/0004-zone-as-attribute-perception.md)).
  Declare them and the exits between them (scene transitions use Evennia
  rooms/exits/`move_to`).
- **zones.py** — `Zone(id, scene, x, y, elevation, terrain_tags)` entries
  ([`world/sim/space/zones.py`](../../game/world/sim/space/zones.py)); these drive
  distance bands and direction phrasing (§11–12). A zone is a **position
  Attribute**, not a room.
- **objects/** — author each object as an `ObjectPacket`
  ([authoring-objects.md](authoring-objects.md)).
- **workflows/** — author each critical goal as a `WorkflowPacket` with ≥3 paths
  ([authoring-workflows.md](authoring-workflows.md)).
- **build.py** — exposes `build()`. It reads the packets and creates the Evennia
  Rooms/Objects, sets zone and material Attributes, and places objects in their
  authored scene/zone. This is the **imperative shell** side; the packets it reads
  are pure data.

## The build loader contract

`load-scenario` calls exactly this:

```
make load-scenario SCENARIO=<name>
# -> docker compose run --rm --entrypoint evennia evennia shell \
#       -c "from world.scenarios.<name>.build import build; build()"
```

So `build.py` must define a top-level **`build()`** that is **idempotent** (safe
to re-run; don't duplicate rooms/objects). `--entrypoint` is required because the
image word-splits arguments and would otherwise break the quoted `-c`
([docker-workflow.md](docker-workflow.md)).

`SCENARIO` defaults to `smoketest` in the Makefile; pass `SCENARIO=<name>` to load
yours.

## Steps to add one

1. `mkdir game/world/scenarios/<name>/` and create the layout above.
2. Write `manifest.py`, `scenes.py`, `zones.py`.
3. Author objects and workflows from their packets and guides.
4. Implement `build()` in `build.py`.
5. **Validate the content** (no server needed):
   `make validate SCENARIO=<name>` ([validation-rules.md](validation-rules.md)).
6. **Load and play:** `make load-scenario SCENARIO=<name>`, then `make up` and
   `telnet localhost 4000`.
7. Document it from [`../scenarios/_TEMPLATE.md`](../scenarios/_TEMPLATE.md) under
   `docs/scenarios/<name>/`.

## Related

- [docker-workflow.md](docker-workflow.md) — build/load/run commands.
- [authoring-objects.md](authoring-objects.md) · [authoring-workflows.md](authoring-workflows.md)
- [../scenarios/_TEMPLATE.md](../scenarios/_TEMPLATE.md) — per-scenario doc template.
