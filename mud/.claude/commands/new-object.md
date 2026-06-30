---
description: Scaffold a new ObjectPacket stub under the current scenario's objects/ from the §43.1 template.
---

Scaffold a new authored object for the current scenario. The object name is in
`$ARGUMENTS`.

If `$ARGUMENTS` is empty, ask for an object name and stop.

Steps:

1. **Read the templates first.** Open `docs/scenarios/whiteout/design.md` §43.1 (the Object
   Authoring Packet), the authoring guide in `docs/guides/` (objects), and
   `game/world/sim/contracts.py` for the `ObjectPacket` / `Part` / `Attachment` / `Material`
   field sets. Skim an existing object under the scenario's `objects/` for house style.

2. **Locate the scenario.** Default scenario is `smoketest`; if the working context points
   at another scenario (e.g. `whiteout`), use that. The target dir is
   `game/world/scenarios/<scenario>/objects/`. Create it (and an `__init__.py`) if missing.

3. **Derive ids/filenames** from `$ARGUMENTS`: snake_case the name for the `id` and the
   filename (e.g. "aircraft seat" → `aircraft_seat.py`, `id="aircraft_seat"`). Don't
   overwrite an existing file — pick a non-colliding name and say so.

4. **Write a stub `ObjectPacket`** following §43.1, with the fields present and `TODO`
   placeholders to fill in: `id`, `name`, `aliases`, `category`, `description`, `scene`,
   `zone`, `mass_g`, `parts` (each `Part` with `material`, `attachment`,
   `outputs_when_removed`), `materials`, `affordances`, **both** `survival_uses` and
   `non_survival_uses`, `failure_modes`, and `tests` (success / failure / conservation /
   silly / perception cases per §44 and §45). Rules stay pure — this packet is data; never
   put logic in a typeclass.

5. Report the file path created and list the `TODO`s the author must fill, and remind them
   to run `make validate` once filled.
