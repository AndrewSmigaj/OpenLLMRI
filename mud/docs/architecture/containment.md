# Containment & Discovery (DR-24)

> **Status: SPEC OF RECORD (2026-07-03; Andrew's directive).** Scenes must read as scenes, not
> manifests. **Containment is the honest hiding**: loot lives INSIDE things and is invisible
> because it is physically contained — no flags, no lists. `open` / `search` / `dig` earn the
> contents. This supersedes the DR-23 "weighting, never hiding" default (amended there).

## The model

- **Containers are explicit content**: `state {"container": True}`, plus `"open": bool` for rigid
  lidded things (bins, the avionics panel, a first-aid kit), `"jammed": True` for pry-first lids,
  `"sealed": True` for caps (the jerry can). Anything with Evennia contents is *searchable*; an
  empty duffel is still a container (it can receive `put`).
- **The reveal rule (ONE rule)**: an object's contents enter the world — the parser pool, the
  scene, reach — iff the object is `open` OR `searched` (or the child is `worn_by` the parent:
  a worn jacket is the visible layer). Recursive **through revealed containers only**: opening
  the bin shows the duffel; the duffel's insides wait for their own search.
- **Deterministic discovery**: search/dig always find exactly what is physically there (no RNG —
  DR-12 holds). The contents ARE the find-text.
- **Marshals, not contracts**: the worldview derives `state["in"]` (physical parent),
  `state["contents"]` (sorted unworn child names), `state["worn"]` (sorted worn child names).
  `EntityState` is untouched; `owner` keeps meaning possession, never location.
- **`EffectKind.TRANSFER`** (additive) is the ONE relocation: `apply()` calls
  `move_to(dest, quiet=True, move_hooks=False)` — hook-free, massless (the ledger passes it like
  MOVE_ZONE); unknown ids raise (the MOVE_ZONE silent-no-op lesson). Zone state needs no
  maintenance — effective zone chains through carriers/containers (DR-13a). *Ordering rule:*
  handlers place TRANSFER effects LAST in their effect tuples (an atomic rollback after a
  `move_to` can desync Evennia's location cache; last-position minimizes the window).

## The grammar

`take/get/grab/collect X [from Y]` · `put/stow X into Y` · `open`/`close` · `search/rummage/frisk`
· `dig` (snow). The from-fold keeps its D6 part semantics and gains a strictly-additive fallback:
when X isn't a *part* of Y, it re-binds as an entity with the container kept in `Y` — so
"take the socks from the duffel" parses whole. Bare "take off X" arrives as `X=None, relation=off,
Y=X` for the wear system (DR-25).

## The get-handover (and the CmdSet matchset trap)

The taught `take` op owns **get** and **grab**. The old stock-subclass `CmdGet` is REMOVED in the
same change — Evennia's `CmdSet.add` de-duplicates by key/alias INTERSECTION, so adding a
same-alias command after the taught command would delete the ENTIRE taught set (verified at the
pinned source; a Tier-2 assert guards that `cut` still resolves after cmdset build). Accepted
loss, recorded: stock leading-count stacking (`get 3 shard`) — take moves one thing per command.

## Known edges

- Menus can offer a contained pick that becomes unreachable if the container closes mid-menu —
  the stale-pick rule answers honestly (DR-08a).
- The reach gate covers contained things for free (effective zone chains); a visible-but-far open
  bin's contents answer "too far", never "you don't see that".
- Liquid containers are NOT modeled (only the jerry can's `sealed` bit gates pouring) — BACKLOG.
