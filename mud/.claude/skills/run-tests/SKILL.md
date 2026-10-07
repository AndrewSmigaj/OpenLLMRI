---
name: run-tests
description: Run and interpret the Whiteout checks — the pure-unit (Tier-1) and Evennia-integration (Tier-2) tests, the 4 structural gates, and the solvability fuzz — and know WHICH to run WHEN. Use whenever the task is to test, verify, check for regressions, or add a test. The authoritative policy lives in docs/architecture/testing.md.
allowed-tools: Read, Bash, Grep, Glob
---

# Run the tests — the layered check strategy + when to run what

Whiteout's checks come in layers, fast→slow. The functional-core boundary (`world/sim` imports no
Evennia) is what makes the fast layers possible. The full policy + rationale is in
[docs/architecture/testing.md](../../../docs/architecture/testing.md); this skill is how to *drive*
and *read* it.

## The layers
| Layer | Command | Proves | Lives in |
|---|---|---|---|
| **Gates** (4, host-fast) | `make lint` | boundary/determinism + one-writer + one-output-path + doc-consistency | `tools/lints/*.py` |
| **Tier-1 pure** (unit) | `make test-host` (host) / `make test` (Docker) | the operation×material engine, ledger, resolver, parser, clock — pure functions | `game/tests/sim/test_*.py` |
| **Tier-2 Evennia** (integration) | `make test-int` | the shell: Attribute↔`EntityState` marshalling, commands, the propagator, the heartbeat Script | `game/tests/integration/test_*.py` |
| **Solvability fuzz** | `make fuzz` (or `python3 tools/fuzz.py whiteout`) | every attempt resolves + every effect conserves mass; seeded-replay is byte-identical | `tools/fuzz.py` |

Golden-master narration snapshots live inside Tier-1 (assert authored responses stay stable).

## When to run what (the policy)
| Moment | Run | Why |
|---|---|---|
| Editing (inner loop) | `make test-host` | gates + Tier-1 pure on the host in ~seconds; no Docker |
| On Stop (already wired) | `.claude/hooks/verify.sh` | auto: the 4 gates + `docker compose config -q` |
| Before each local commit | `.githooks/pre-commit` | the 4 gates — **enable once:** `git config core.hooksPath .githooks` |
| Before a push / full local pass | `make verify` | gates + compose config + Tier-1 (Docker) |
| "Did I break the shell?" | `make test-int` | Tier-2 Evennia (throwaway test DB) |
| Every GitHub push | auto (`.github/workflows/ci.yml`) | all of the above, in the cloud, green ✓ / red ✗ per commit |

Default inner loop is **`make test-host`**. Run **`make test-int`** whenever you touched anything under
`game/typeclasses/`, `game/commands/`, or the scenario `build.py` (the shell). The GitHub run is the
backstop — it runs everything regardless.

## Reading a failure
- **Gate fail** (`make lint`) — a structural violation: `world/sim` imported Evennia, a raw `obj.db.x=`
  outside `apply()`, a raw `.msg`/`msg_contents` outside the propagator, or a forbidden doc pattern. The
  gate prints the file:line + the rule. Fix the code, not the gate.
- **Tier-1 fail** — a pure-logic or contract regression. It reproduces host-side in milliseconds; the
  assertion names the operation/material. This is where most real bugs surface.
- **Tier-2 fail** — a shell regression (marshalling, command wiring, propagation, the Script). If a
  Tier-1 concept only fails here, a rule may have leaked into the shell — move it back into `world/sim`.
- **Fuzz fail** — an UNRESOLVED attempt (fell through with no physical answer) or a CONSERVATION
  violation (mass not balanced). Feed unresolved attempts to the `solvability-fuzz` skill's report flow.

## Adding a test
- **Tier-1 (pure)** — build the contract dataclasses by hand (`EntityState`, `Part`, `ActionAttempt`)
  and a tiny fake world exposing `get(id)` / `reachable(actor)` / `in_zone(z)`; call the pure function
  and assert on the returned `ActionResult`/`Effect`. See `game/tests/sim/test_fuzz.py` for the
  `FakeWorld` shape. The **`sim-test-writer`** agent authors these from the §45 list.
- **Tier-2 (integration)** — subclass `EvenniaTest`, build minimal inline fixtures in `setUp()` (a room
  + a test object with `sim_id`/`parts`/`mass_g`), drive `char.execute_cmd(...)`, and assert on a
  **mocked** `.msg` (`mock.patch.object(char, "msg")`). Mirror `game/tests/integration/test_slice.py`
  — including the co-op assertion (char2 hears char1) and an atomic-rollback case.

Keep Tier-1 the bulk (it's where the game's logic lives); reserve Tier-2 for what genuinely needs the
database and the server.
