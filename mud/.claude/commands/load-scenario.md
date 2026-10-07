---
description: Load a Whiteout scenario into the running stack (default smoketest).
---

Load a scenario via the Makefile. The scenario name is in `$ARGUMENTS`; if it is empty,
default to `smoketest`.

Run:

```sh
make load-scenario SCENARIO=${ARGUMENTS:-smoketest}
```

This runs `world.scenarios.<scenario>.build:build()` inside the Evennia container. Report:
which scenario was loaded, whether the build succeeded, and any errors or tracebacks from
the output. If the build fails because the stack/DB isn't up, say so and suggest `make up-d`
(and `make migrate` if migrations are pending) before retrying. Do not boot or modify
anything else.
