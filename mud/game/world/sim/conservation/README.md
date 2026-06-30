# `world/sim/conservation/` — the conservation ledger (DR-11, §24)

The flagship runtime invariant. `check(pre, effects)` runs **inside the shell's `apply()`, before
commit**, and rejects any transform whose post-state doesn't balance the pre-state.

- **Mass is real integer grams and balances EXACTLY** (no float tolerance — integer-quantized to kill
  drift). The only "tolerance" is the **accountable environment sink** absorbing *legitimate* losses
  (smoke to air, heat lost); the sink tracks its total per channel and **may only grow**.
- **Energy is a GATE, not a balanced channel** (enough heat to ignite/melt? enough force to bend?) —
  qualitative-physics says ordinal energy can't be conserved unambiguously, so we don't try.
- A rejection is a **bug** (unphysical authored content), not a player failure: it's logged and fails
  the build.

Built in roadmap **P1** (with the slice). Property-tested every phase thereafter.
