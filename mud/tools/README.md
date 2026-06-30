# `tools/` — build-time + CI tooling (offline; never runtime)

Host-runnable scripts. **None of this runs during play** (the runtime is deterministic, no LLM).

| Script | Purpose | Roadmap |
|---|---|---|
| `bake.py` | compile authored scenario sources → the baked runtime data (validate + ledger, then write the numeric/indexed form) — `make bake` | P2 |
| `fuzz.py` | the solvability-fuzz harness (ScriptedBrain over seeded runs; every attempt resolves / 0 conservation violations / rescue reachable; wall-sensor → authoring queue) — `make fuzz` | P2 |
| `coverage.py` | report op×material matrix completeness + fuzz-corpus stats | P2 |
| `lints/check_pure_core.py` | **gate:** no evennia/django/random/time/datetime/uuid imports — and no `dbid`/`uuid`/`datetime` field names — under `game/world/sim` (functional-core boundary + determinism, DR-01/DR-12) | now |
| `lints/check_no_raw_writes.py` | **gate:** state changes only via `apply()` — no raw `.db/.ndb` writes, subscript/in-place mutation, or `.attributes/.tags.add` in the shell (DR-10) | now |
| `lints/check_no_raw_output.py` | **gate:** game events reach players only via the message **propagator** — no raw `.msg_contents()` in the shell (the seam that keeps overlapping perception zones a clean drop-in, DR-13) | now |
| `lints/check_docs.py` | **gate:** live docs don't regress to a locked decision (forbids `mass_kg`, `CMD_NOMATCH`, `intent-fallback`, `event-driven`, `Pass N`, `design.md`-as-authoritative) | now |

These four gates are **host-fast** (stdlib only, AST/regex-based — no false positives from comments/
docstrings) and run in `make lint` / `make verify`, the Stop hook (`.claude/hooks/verify.sh`), and the
optional pre-commit hook (`.githooks/pre-commit`; enable with `git config core.hooksPath .githooks`).
