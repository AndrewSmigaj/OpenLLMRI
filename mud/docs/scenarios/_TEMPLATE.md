# <Scenario Name> — Design

> Copy this file to `docs/scenarios/<name>/design.md` and fill it in. It is the
> per-scenario design doc that mirrors the engine's authoring shape. Keep it
> skimmable; cite the engine design as "§N" where a rule is reused, and link the
> guides for *how* to author each piece. The reusable engine lives in
> `game/world/sim/**`; this scenario is content on top of it
> (see [adding a scenario](../../guides/adding-a-scenario.md)).

- **Status:** Draft | In progress | Playable
- **Starting scene / zone:** `<scene>` / `<zone>`
- **World-clock seed:** day/hour, weather, temperature (§9.2)

## 1. Pitch

One or two sentences: the premise and the central survival/dramatic promise.
What does the player do, and what is the §2-style promise (survive by
*understanding the world*, not guessing verbs)?

## 2. Binding decisions

The scenario-specific commitments (the local equivalent of design §3). Examples:
the hazard model, the rescue premise, any deliberate scope limits. Note where you
*reuse* engine defaults vs. override them.

## 3. Scenes & zones

Each **Scene** is one Evennia Room; each **zone** is a position Attribute within
it ([zone-as-attribute](../../architecture/adr/0004-zone-as-attribute-perception.md)).

| Scene (Room) | Zones (positions) | Connects to | Notes / terrain tags |
|---|---|---|---|
| `<scene_id>` | `<zone>, <zone>, ...` | `<scene>` via `<exit>` | trees / ravine / inside, occlusion |

Include rough zone coordinates (x, y, elevation) so direction/distance phrasing
works (§11–12), and which scene transitions use Evennia exits.

## 4. Key objects

The major authored objects, each an `ObjectPacket`
([authoring objects](../../guides/authoring-objects.md)).

| Object | Material(s) | Parts → outputs | Survival uses | Silly/non-survival use |
|---|---|---|---|---|
| `<object_id>` | `<material>` | `<part>` → `<output>` | … | … (§44 requires one) |

Note conservation-relevant transforms (§24) and which object carries an authored
puzzle rule (the §26 AUTHORED tier).

## 5. Workflows

Goal-level workflows, each a `WorkflowPacket`
([authoring workflows](../../guides/authoring-workflows.md)). Remember §44:
**≥ 3 solution paths** per critical goal, **≥ 3 clue paths** per hidden fact,
inspect/access/diagnose/repair/test stages for critical repairs.

| Goal | Success conditions | Alternate paths (≥3) | Clue paths (≥3) | Partial states |
|---|---|---|---|---|
| `<goal>` | … | …; …; … | …; …; … | … |

## 6. Rescue / goal paths

The overlapping ways the scenario can *end* well, as additive confidence (§39) —
no single object required for all endings. List the distinct combinations and any
hard time pressure (§8 weather progression, scripted deadlines).

- `<route A>` — …
- `<route B>` — …
- `<route C>` — …
- `<route D>` — …  *(aim for ≥ 4 distinct combinations; §39)*

## 7. Tests

The acceptance checks (§45) the scenario must pass — success, failure,
conservation, silly and perception cases. These back the `tests` lists on each
packet and run via `make verify` ([validation](../../guides/validation-rules.md),
[testing](../../architecture/testing.md)).

- [ ] …
- [ ] …

## Build & load

- Content lives in `game/world/scenarios/<name>/` with an idempotent `build()`.
- Validate: `make validate SCENARIO=<name>`
- Load: `make load-scenario SCENARIO=<name>`, then `make up` and
  `telnet localhost 4000`.

See [adding a scenario](../../guides/adding-a-scenario.md) and the
[docker workflow](../../guides/docker-workflow.md).
