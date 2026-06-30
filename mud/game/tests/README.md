# `game/tests/` — test scaffold (no tests yet)

Two tiers (see [`docs/architecture/testing.md`](../../docs/architecture/testing.md)):

- **`tests/sim/`** — fast **pure** unit tests over `world.sim.*`. No database, no
  Evennia boot (that's the whole point of the functional-core boundary). Run with
  `make test`. Config is in [`../pytest.ini`](../pytest.ini) (`-p no:django` keeps
  Django dormant). Empty until the engine exists.
- **`tests/integration/`** — Evennia integration tests (typeclasses/commands) that
  need the framework + a test DB. Run with `make test-int` via Evennia's own test
  runner. Empty until there's shell code to test.

There are no tests yet — the engine and scenarios they would cover are not built
(see [`docs/scenarios/whiteout/roadmap.md`](../../docs/scenarios/whiteout/roadmap.md)).
