# `world/sim/operations/` — the operation engine (DR-05)

The heart of "everything interacts." An **operation** is a unit of behavior behind **one interface**:

- **Common, stateless** op×material cases (cut/burn/pry/tie/wear…) are the **declarative schema**
  (`Operation` + the closed `Predicate`/`Modifier`/`EffectSpec` language) run by `interpreter.evaluate`.
- **Stateful/complex** logic (the radio FSM, the `systems/*`) is **plain Python** behind the same
  interface and registers identically.

**Build order (DR-05 — the biggest bet):** write the first 2-3 operations as **plain Python functions
first**; extract the interpreter **only once repetition is undeniable**. Few operations × many materials
× the RELATION slot = a vast, *generative* interaction space — not a hand-enumerated list.

**Deterministic specificity dispatch:** most-specific rule wins (authored-special > object >
(operation,material) > generic), ties broken by a declared integer `priority` — never file order. Built
in roadmap **P1/P2**.
