# `tools/` — build-time + CI tooling (offline; never runtime)

Host-runnable scripts. **None of this runs during play** (the runtime is deterministic, no LLM).

| Script | Purpose | Roadmap |
|---|---|---|
| `bake.py` | compile authored scenario sources → the baked runtime data (validate + ledger, then write the numeric/indexed form) — `make bake` | P2 |
| `fuzz.py` | the solvability-fuzz harness (ScriptedBrain over seeded runs; every attempt resolves / 0 conservation violations / rescue reachable; wall-sensor → authoring queue) — `make fuzz` | P2 |
| `coverage.py` | report op×material matrix completeness + fuzz-corpus stats | P2 |
| `lints/check_pure_core.py` | **gate:** no evennia/django/random/time/datetime/uuid imports under `game/world/sim` (the functional-core boundary + determinism, DR-12) | now |
| `lints/check_no_raw_writes.py` | **gate:** state changes only via `apply()` — no raw `.db/.ndb` writes or `.attributes/.tags.add` in the shell (DR-10) | now |

The two lints are **host-fast** (stdlib only, AST-based — no false positives from comments/docstrings) and
run in `make lint` / `make verify`, the Stop hook (`.claude/hooks/verify.sh`), and the optional pre-commit
hook (`.githooks/pre-commit`; enable with `git config core.hooksPath .githooks`).
