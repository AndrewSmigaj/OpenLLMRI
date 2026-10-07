"""world.sim — Whiteout's pure functional core (the "interaction system").

Deterministic, dependency-light Python. Imports NO Evennia/Django and touches no DB; it speaks the
dataclasses in `contracts.py`. The Evennia shell marshals state in, runs these pure functions, and
applies the returned Effects (the only writer). See this package's README.md and
docs/architecture/implementation-architecture.md (DR-01…DR-22).
"""
