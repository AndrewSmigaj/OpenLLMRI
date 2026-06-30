# `world/sim/parser/` — the taught command grammar (DR-08, GDD §25a)

A classic IF/MUD parser, **no NL model**. Input is the **taught grammar** `VERB X [RELATION Y] [WITH Z]`
at action granularity:

- **VERB** — the action (synonym table → one canonical operation id).
- **X** — the primary target: a thing **or a part** (`the seat's cover` = `the cover of the seat`).
- **RELATION** — a preposition (`off`, `onto`, `against`, `between`, `into`, `from`…) binding a **second
  object Y**. This slot makes two-object actions first-class.
- **WITH Z** — the optional tool.

`parse()` → `ActionAttempt{actor, verb, X, relation, Y, tool, raw}` or a `ParseError` carrying a help
nudge (never a hard "you can't do that"). **"You can do everything"** = everything that fits this grammar
and is sensible resolves, via the *generative* operation×material engine — not an enumerated command
list. Built in roadmap **P1**.
