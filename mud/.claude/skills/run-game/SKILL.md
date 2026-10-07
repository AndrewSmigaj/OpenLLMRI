---
name: run-game
description: Bring the Whiteout MUD up, load a scenario, and connect for co-op play/smoke-testing. Use whenever the task is to run / boot / restart the server, load a world, get into the game, or read the logs. Orchestrates the existing `make` targets + the load-scenario/restart-server commands; it does not reinvent them.
allowed-tools: Read, Bash, Grep, Glob
---

# Run the game — boot, load a world, connect for co-op

Everything runs in Docker through the Makefile (see [CLAUDE.md](../../../CLAUDE.md) for the full
table). This skill is the **decision tree + gotchas** for operating the live server so a run comes up
clean the first time. It never bypasses the Makefile.

## When to use
"run/boot/start the game", "load the scenario", "restart the server", "get me into the world",
"check the logs", "smoke-test the slice", or setting up two sessions for co-op.

## Bring-up (decision tree)
First decide whether the stack is already running:

```sh
docker compose ps            # is `whiteout-evennia` up?
```

**Already up** → skip to *Load a scenario*.

**Cold / first time on this machine** → run these in order; each must succeed before the next:

```sh
cp -n .env.example .env      # 1. env for compose (git-ignored); skip if .env exists
make build                   # 2. build the pinned image (docker/evennia/Dockerfile)
make migrate                 # 3. create the Postgres schema
make accounts                # 4. admin (Account #1) + bot account (idempotent; uses host pexpect)
make up-d                    # 5. start the server detached (telnet 4000 / web 4001 / ws 4002)
```

Confirm it booted cleanly (don't stream forever):

```sh
docker compose logs --tail=40 evennia    # look for the Evennia startup banner, no tracebacks
```

## Load a scenario
```sh
make load-scenario SCENARIO=whiteout     # runs world.scenarios.whiteout.build:build()
```
Report which scenario loaded and surface any traceback. If it fails because the stack/DB isn't up,
run *Bring-up* first. (This is exactly the `/load-scenario` command.)

## Connect for co-op
The game speaks **telnet on `localhost:4000`** (or the web client on `:4001`). For a co-op smoke you
want two characters in the same room:

1. Connect a client, log in as the admin account (from `.env`: `EVENNIA_SUPERUSER`).
2. Put your character in the crash cabin: `@tel crash cabin` (Evennia builder command).
3. Connect a **second** session as the bot/second account (`AGENT_ACCOUNT`), `@tel` it to the same
   room. Now each player perceives the other via the propagator.

## Live smoke (the enriched slice — 14 verbs, 16 objects)
Once two characters are in the cabin, exercise the systemic world. The verbs: **examine, cut, tear, pry,
break, bend, burn, light, melt, pour, tie, wrap, drink, eat** (each with synonyms, e.g. `saw`/`rip`/`smash`).

```
examine seat                              # parts WITH ids (cover/cushion/belt/bolt) + ident "11B"
cut the cover off the seat with the multitool   # frees the stitched cover -> a 200g loose-fabric object
tear the manual                           # paper tears into strips (no tool); tough things redirect -> cut
break the bottle                          # glass shatters into 3 shards (mass conserved); metal is too tough
bend the wire                             # ductile -> takes a shape; steel is too stiff
light the tinder with the lighter         # starts a fire (lit=True) — distinct from burn
melt the ice                              # off the fire you just lit -> water (ice grams -> water grams)
pour the canteen on the fire              # water douses it (lit=False); pouring on a thing wets it
tie the paracord to the seat              # cordage -> a knot; wrap the blanket around the pilot -> warmth
drink the water   /   eat the chocolate   # the survival payoff
examine the wire                          # shows the state you set: "bent out of true", "tied off", "alight"...
```
Correct behavior: the actor gets first-person narration; the **other** character sees the propagated
event; state (Attributes) changes and mass conserves; `examine` reflects what you did; unknown verbs teach
the grammar (not "Huh?"). Emergent chains are the point — *light the tinder → melt snow off it → drink*.

## Restart / logs / shell
```sh
make restart                              # reload the running server (the /restart-server command)
docker compose logs -f evennia            # follow logs (Ctrl-C to stop)
make shell                                # Evennia/Django shell for inspection
```

## Gotchas (do NOT relearn these the hard way)
- **Superuser needs a pty.** Evennia's `createsuperuser` loops without a TTY — `make accounts` drives
  it over pexpect on the host. Don't call `evennia createsuperuser` in the container.
- **The image entrypoint word-splits args.** Make targets with quoted args use `--entrypoint`; follow
  that pattern, don't hand it `bash -c "... && ..."`.
- **Everything is Docker** except the torch bot-agent (`agent/`), which is host-only (GPU/weights).
- **Never** `docker compose down -v` (deny-listed — wipes the DB volume). To intentionally reset the
  world, use `make reset-db` and say so. **Never** `git push` (deny-listed).

## Graceful degradation (current state)
`make agent` (bot harness) and `make bake` / `make validate` are stubs until later roadmap phases —
they print a pointer instead of doing work. `make load-scenario SCENARIO=whiteout` and the smoke above
are live as of P1.
