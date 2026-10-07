---
description: Restart the Whiteout server and tail logs briefly to confirm it came back.
---

Restart the running Evennia server, then check it recovered.

1. Restart:

   ```sh
   make -C mud restart
   ```

   `make -C mud restart` reloads the running server (`evennia reload`), falling back to restarting
   the container. If that fails or the stack isn't running, fall back to a full cycle:

   ```sh
   make -C mud down && make -C mud up-d
   ```

2. Tail the logs briefly to confirm a clean boot (don't follow indefinitely):

   ```sh
   docker logs --tail 40 llmri-mud-evennia
   ```

Report whether the server is back up and surface any errors/tracebacks in the tail. Stop
after the brief tail — do not stream logs continuously.
