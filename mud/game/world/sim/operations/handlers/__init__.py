"""world.sim.operations.handlers — the operation handler functions (functions-first, DR-05).

Each handler is a pure `resolve_<op>(attempt, world, materials) -> ActionResult | None`:
returns an ActionResult if the operation applies (SUCCESS / PARTIAL / an informative REDIRECT),
or None if it does not apply to this target (so the resolver tries the next tier).
"""
