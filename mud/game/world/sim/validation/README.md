# `world/sim/validation/` — content-lint (DR-17, §44)

The §44 checklist as a **hard gate** (load / CI / `make validate`). It checks *authored content*, not
runtime behavior:

- ≥3 solution paths for critical goals; ≥3 clue paths for critical facts (no single-point softlock);
- timed actions have tick feedback **and** are interruptible (or explicitly marked otherwise);
- derived objects have capabilities or explicit non-uses; perception routing on major activity;
- the **global-softlock check** (a party can't spend/burn into an unwinnable world-state);
- the **conservation ledger balances** every authored transform.

Pure; returns findings (empty = clean). Built in roadmap **P2** (with a load-time hook landing earlier).
