# Validation Rules — `make validate`

> Rewritten 2026-09-07 (DR-17a / DR-18a). The validator is a **real content lint over the tables**, run
> on the host in milliseconds: `make validate SCENARIO=<name>` → `python3 -m world.sim.validation
> <name>`. It is part of `make verify`, CI, and the overnight loop's gate. A red validate is a stop.

Validation is a gate on **authored data**, not a game system. The engine still enforces conservation and
"everything resolves" at runtime; the lint makes sure the tables are well-formed before they load.

## What it checks (the §44 checklist, made mechanical)
**Objects (`objects.py`)**
- every `materials` id and every part `material` exists in `materials/table.py`
- every part `attachment` is in the taxonomy (`_helpers.CUTTABLE_ATTACH ∪ PRYABLE_ATTACH ∪ {fixed}`)
- `mass_g` and part masses are non-negative integers; `sim_id` is unique
- exactly one of `zone` / `in`; a referenced parent exists; a referenced zone exists
- an appearance entry exists (**warning**; the generic fallback is honest but dull)

**Materials** — every prop is an ordinal word; every tag is known; a `flammable` tag implies
`burnability`, a `brittle` tag implies `rigidity`, etc.

**Zones / spaces** — every zone has a default space; every space frame has the `{be}`/`{items}` slots;
every object's `space` exists in its zone.

**Responses** — every `narrator.narrate("<id>")` call in the handlers has a template; no template writes
an article before `{tool}`.

**Probes** — every probe cites a `source`; `status` is `pass` or `todo`; the zone and the held things
exist; every `status: pass` probe passes (that part runs in `make probes`, CI-enforced) and the
passing count never drops below `probes/BASELINE`.

**Solvability (with the rescue graph)** — every critical goal has ≥3 probe chains; every critical fact
has ≥3 clue paths; no single object appears in every path of a goal.

## Fixing failures
| failure | fix |
|---|---|
| unknown material / attachment | add the material to the table or fix the spelling; name a real attachment |
| no zone and no `in` | place it: a `zone`, or stow it `in` a parent (DR-24) |
| missing template | add `<op>.<outcome>` to the scenario responses |
| appearance missing | add the `sim_id` entry (or rely on the form-keyed generic for a derived thing) |
| probe regressed | fix the engine, never edit the probe's expectation to pass |

## Related
[authoring-objects.md](authoring-objects.md) · [authoring-actions.md](authoring-actions.md) ·
[`../architecture/ontology-closure.md`](../architecture/ontology-closure.md) §6 ·
[`../architecture/testing.md`](../architecture/testing.md)
