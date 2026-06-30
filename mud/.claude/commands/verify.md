---
description: Full verification — compose config + pure tests + §44 validate, plus a quick live smoke.
---

Run the full verification pass for Whiteout and summarize pass/fail. The optional scenario
name is in `$ARGUMENTS` (default `smoketest`).

1. **Static + unit gate** — run the Makefile verify target (compose config check + pure
   `world.sim` tests + §44 content validate):

   ```sh
   make verify SCENARIO=${ARGUMENTS:-smoketest}
   ```

2. **Live smoke** — make sure the stack is actually up, then probe it:
   - If nothing is running, boot it: `make up-d` (run `make migrate` first if the DB is
     fresh, and `make load-scenario SCENARIO=${ARGUMENTS:-smoketest}`).
   - Confirm the telnet port answers, e.g.:

     ```sh
     (echo; sleep 1) | timeout 5 telnet localhost 4000 || true
     ```

   - If the scripted bot harness is available, run a short scripted-bot smoke against the
     running server:

     ```sh
     make agent
     ```

     (host python; scripted brain, `localhost:4000`). Keep it brief.

3. **Summarize** each stage as PASS / FAIL: compose config, pure tests, validate, telnet
   reachable, bot smoke. Quote the key error lines for any failure and point at the likely
   cause. Do not push, do not destroy the DB volume.
