# A6 — Evennia architecture research (the four load-bearing Evennia-specifics)

Deep-dives the four Evennia-mechanism questions that `review/30-certainty.md` flagged as
"reasoned, not evidenced" for DR-07, DR-10, DR-14, DR-15. Each answer gives the **finding**, a
**CONFIRM / IMPROVE / CHALLENGE** verdict, a **recommended pattern**, and a **confidence delta**.

**Method / provenance.** Findings are taken from the official docs (`evennia.com/docs/latest`),
the Django 6 docs, the in-repo EvAdventure *dungeon* contrib (the canonical instancing example),
and — for the load-bearing mechanics — by reading the actual Evennia source. I pulled the current
PyPI release (`evennia 4.5.0`, which is what `docs/latest` documents) and read
`evennia/typeclasses/attributes.py`, `evennia/typeclasses/tags.py`, `evennia/utils/idmapper/models.py`,
`evennia/scripts/scripts.py`, `evennia/server/service.py`, and
`evennia/contrib/tutorials/evadventure/dungeon.py`. Source line references below are to those files.

> **Version caveat (minor, worth a re-check).** Our stack doc says "Evennia 6.0.0"; the current
> PyPI/`docs-latest` line is the 4.x series. The Attribute / Tag / Script / idmapper internals cited
> here are core and have been stable across majors, so the conclusions hold; but if we really are on
> a different major than 4.5, spot-re-verify the two source-level claims (cache-on-rollback in Q1, the
> reload pause/restore path in Q2) against that tree.

---

## Q1 — Transactions + the write choke-point (DR-10 / DR-07)

### How Attributes and Tags map to Django models / the DB
- An **Attribute** is a real Django row (`AttributeDB`), attached to its host via an M2M
  through-table; its payload lives in a `PickledObjectField` (`db_value`) — values are **pickled**
  before storage, with an optional unpickled `db_strvalue` string field. So Attribute values are
  *not queryable by value* with ORM comparisons (`__gt`/`__lt` etc. operate on pickled strings).
  ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html))
- A **Tag** is likewise a Django row (`TagDB`) joined by an M2M through-table; tags *are* indexed and
  queryable (`search_object_by_tag`, `ObjectDB.objects.get_by_tag`). This is exactly why DR-07 mirrors
  the queryable axes (material/zone/affordance) as Tags. ([Tags](https://www.evennia.com/docs/latest/Components/Tags.html))
- Both `AttributeDB` and the typeclassed hosts subclass `SharedMemoryModel` (the **idmapper**), an
  in-memory instance cache so repeated lookups return the *same* Python object.
  ([idmapper.models](https://www.evennia.com/docs/latest/_modules/evennia/utils/idmapper/models.html))

### Do writes go through the ORM (so `transaction.atomic` works)?
Yes — every write is an ordinary `Model.save()` / M2M `.add()`:
- `obj.db.x = v` → `DbHolder.__setattr__` → `AttributeHandler.add()` → either
  `do_update_attribute()` → `attr.save(update_fields=["db_strvalue","db_value"])` **or**
  `do_create_attribute()` → `new_attr.save()` then `...m2m...add(new_attr)`
  (`attributes.py`, `add` ≈ L1243, `do_create_attribute` ≈ L1063, `do_update_attribute` ≈ L1083).
- `obj.tags.add(...)` → `TagHandler.add()` → `getattr(self.obj, m2m_field).add(tagobj)`
  (`tags.py`, `add` ≈ L487/L521).

Because these are all standard Django ORM calls, wrapping them in
`with django.db.transaction.atomic():` **does give DB-level all-or-nothing commit/rollback** for the
Attribute write *and* its Tag-mirror write together. Django defers the commit to block exit and rolls
back on any exception, with savepoints for nested blocks.
([Django transactions](https://docs.djangoproject.com/en/6.0/topics/db/transactions/))
**The DB half of DR-10 is sound.**

### The sharp edge: a rolled-back transaction leaves a STALE in-memory value
This is the real finding and it is **not** in the docs — it's in the source. The write path updates
the **in-memory cache eagerly and there is no rollback hook**:
- `AttributeHandler.add()` writes to the DB *and* immediately calls `_set_cache(...)`; the cached
  `Attribute` object's `db_value` now holds the new (pickled) value in process memory
  (`attributes.py` L1078–L1080; `_set_cache` ≈ L650).
- Mutable Attribute values are returned as `_SaverDict`/`_SaverList`, which **write themselves back to
  the DB on in-place mutation** — another eager write with the same caching.
  ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html))
- The idmapper cache is only force-flushed on `post_migrate` (migrations) — the per-request
  `request_finished.connect(flush_cache)` line is **commented out** (`idmapper/models.py` L549–L550).
  There is **no automatic cache invalidation when a Django transaction rolls back.**

Consequence: if an `atomic()` block writes Attributes/Tags and then **raises**, the DB reverts but the
**process keeps the rolled-back value in memory** until that object's handler cache is reset (or the
Server process restarts — see Q2; `@reload` discards the whole cache because it reboots the Server
process). A naive "just wrap `apply()` in `atomic()`" would, on a mid-batch failure, leave a torn
*in-memory* world even though the DB is clean. **This challenges the naive version of DR-10.**

### Why this is small for us, and the clean fix
1. **Our ledger runs before any write.** DR-11's `ledger.check()` simulates the post-state in memory
   and rejects *pre-commit* — so a rejected action never writes at all, and never needs a rollback.
   The only path that actually hits `atomic()`-rollback is an *unexpected* DB error mid-batch (rare).
2. **For that rare path, invalidate the touched objects' caches on rollback.** Evennia exposes the
   tools: `obj.attributes.reset_cache()` / `obj.tags.reset_cache()` (clear the handler caches;
   `attributes.py` L694, `tags.py` L478) and, at the model level, `refresh_from_db()` /
   `flush_instance_cache(force=True)` (`idmapper/models.py` L366, L347). Pattern:

   ```python
   def apply(result):
       touched = effects_targets(result.effects)
       try:
           with transaction.atomic():
               ledger.check(pre, result.effects)          # raises -> no writes happened
               for eff in result.effects:
                   eff.write()                            # obj.db.x = ... ; obj.tags.add(...)
       except Exception:
           for o in touched:                              # belt-and-suspenders: untear memory
               o.attributes.reset_cache(); o.tags.reset_cache()
           raise
   ```
   Because the ledger gate precedes the writes, the `except` branch is essentially never hit in normal
   play; it exists so an integrity error can't desync cache from DB. Document this as a hard
   requirement of `apply()` (and assert it in a Tier-2 test: force a mid-batch raise, assert the
   Attribute reads back its pre-value).

### Is the single choke-point + lint realistic?
**Yes, very.** All mutation funnels through a handful of *syntactically detectable* call shapes:
`*.db.<x> = `, `*.ndb.<x> = `, `*.attributes.add(/.batch_add(`, `*.tags.add(/.batch_add(`,
`*.attributes.remove`, `*.db.<list>[..] = ` (the SaverList mutation case). An AST/grep `engine-reviewer`
rule that allows these only inside `typeclasses/…/apply` (and bans them in `world/sim`, `commands`,
`systems`) is straightforward — `obj.db.x =` is the documented public write API, so there's no hidden
back door to miss. One nuance to encode: in-place mutation of a fetched `_SaverDict`/`_SaverList`
*also* writes, so the lint should also flag subscript/`.append`/`.update` on values read out of `.db`
(or, simpler, require Effects to *replace* containers rather than mutate fetched ones).

### Verdict, pattern, delta
- **Verdict: IMPROVE** (the decision is right; research adds one mandatory mechanism it was missing).
  DB-atomicity over Attributes+Tags is confirmed; the choke-point+lint is confirmed feasible; the
  *new* requirement is **cache-invalidation-on-rollback** (and treating SaverList in-place mutation as
  a write the lint must catch).
- **Recommended pattern:** ledger-check-before-write inside `atomic()`; on any exception, `reset_cache()`
  the touched objects' attribute+tag handlers before re-raising; Effects replace containers rather than
  mutate fetched SaverLists; lint bans `.db=`/`.ndb=`/`.attributes.add`/`.tags.add` and SaverList
  in-place writes outside `apply()`.
- **Confidence delta (DR-10): +2 (→ ~82).** Net small-positive: the core works and the lint is more
  clearly feasible than assumed (raise), partially offset by discovering a real correctness footgun
  (the rollback-cache desync) that must be coded and tested (lower). It is fully mitigable, so not a
  net negative.
- **Confidence delta (DR-07): +3 (→ ~85).** Confirmed idiomatic: Attributes are pickled and
  *not* value-queryable, so mirroring queryable axes to Tags is the documented Evennia answer, and the
  same-transaction Attribute+Tag write is supported. No change to the decision.

---

## Q2 — Activity persistence across `@reload` (DR-14)

### What survives what
- **`@reload` is a warm reboot of the *Server* process** (the Portal — and thus player connections —
  stays up). Persistent DB state is untouched; the in-memory Server is rebuilt from the DB.
  ([Start-Stop-Reload](https://github.com/evennia/evennia/wiki/Start-Stop-Reload),
  [Running Evennia](https://www.evennia.com/docs/latest/Setup/Running-Evennia.html))
- **`.db` / Attributes persist; `.ndb` does not.** "Everything stored to ndb (NonDataBase) is
  guaranteed to be cleared when a server is shut down." `.db` is the `AttributeDB` row (Postgres) and
  survives reload/reset/shutdown alike. ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html))
- **`@reset` / `@shutdown`** additionally run shutdown hooks and wipe all non-persistent state
  (non-persistent scripts, `.ndb`, cmdsets). Persistent DB data still survives; what's lost is exactly
  the in-memory stuff. So the DR-14 rule "**persist the Activity in Attributes, never on `.ndb`**" is
  correct and is the whole ballgame. ([system commands](https://www.evennia.com/docs/latest/api/evennia.commands.default.system.html))

### Scripts and TickerHandler across reload
- **Persistent Scripts resume automatically.** `persistent=True` (the default) "means the timer will
  survive a server reload/reboot." In source, the reload path pauses each active script
  (`s._pause_task(auto_pause=True)`) and calls `at_server_reload()` before the Server reboots
  (`server/service.py` L509–L515); on restart the script is reinstated and `at_start` fires.
  ([Scripts](https://www.evennia.com/docs/latest/Components/Scripts.html))
- **TickerHandler subscriptions survive a *reload*** (and a shutdown only if their `persistent` flag is
  set). On restart the server calls `TICKER_HANDLER.restore(...)` (`server/service.py` L641).
  ([TickerHandler](https://www.evennia.com/docs/latest/Components/TickerHandler.html)) Caveat: a ticker
  subscription must reference a **typeclassed object + method name** so it can be re-pickled/restored;
  a bare closure won't survive — fine for us (the heartbeat is a global Script).
- **Timer bookkeeping across reload is approximate.** Evennia tracks elapsed-within-interval across
  pause/reload, but it is not a guaranteed-exact wall clock; a long `@reload` can shift the next fire.
  ([Scripts](https://www.evennia.com/docs/latest/Components/Scripts.html)) For correctness you should
  **not derive Activity progress from the timer's elapsed bookkeeping.**

### Idiomatic storage for in-progress timed Activities
Store the Activity as **its own data** in persistent Attributes — the actor, action, accumulated
progress, and a **logical deadline / remaining-work counter** — and let the global heartbeat Script
*advance* that data each tick. On `at_start` after reload, recompute "what's left" from the persisted
Activity rather than trusting the timer. This is doubly clean for Whiteout because DR-14's *recommended*
clock is **event-driven / logical-tick**, not wall-clock: progress is measured in logical ticks the
heartbeat applies, which are fully deterministic and reload-invariant. (Evennia's own duration-command
howto stores progress on the object and re-derives, rather than trusting in-flight timers —
[Command-Duration howto](https://www.evennia.com/docs/latest/Howtos/Howto-Command-Duration.html).)

### Verdict, delta
- **Verdict: CONFIRM (with one refinement).** Persistent state in Attributes + a persistent global
  heartbeat Script survives `@reload` and resumes; `.ndb` is correctly excluded. Refinement: persist
  the Activity's *progress/deadline* and recompute on `at_start`; don't lean on the Script timer's
  elapsed estimate for game-correct progress.
- **Confidence delta (DR-14): +8 (→ ~83).** Strong raise — the mechanism is exactly as DR-14 assumed
  and is documented + source-confirmed; the only adjustment (store progress, recompute on resume) is
  cheap and already aligned with the deterministic-clock choice.

---

## Q3 — Instancing on Evennia (DR-15)

### There is an official, in-repo pattern that is ~identical to DR-15
The EvAdventure **dungeon** contrib implements per-party instanced zones almost exactly as DR-15
specifies. ([dungeon API](https://www.evennia.com/docs/latest/api/evennia.contrib.tutorials.evadventure.dungeon.html),
[source](https://github.com/evennia/evennia/blob/main/evennia/contrib/tutorials/evadventure/dungeon.py))
Reading the source:
- **Each instance is a `Script` + a Tag namespace.** An `EvAdventureDungeonBranch` script *is* the
  run; rooms are tagged with the branch key under category `"dungeon_room"`, characters under
  `"dungeon_character"`, and each room also stores a `dungeon_branch` Attribute pointing back at the
  script. (Directly mirrors DR-15's "tag everything with a `run_id`.")
- **Objects are created on demand** with `create.create_object(...)` inside `new_room()` (triggered by
  `EvAdventureDungeonExit.at_traverse()`).
- **Teardown deletes by tag.** `EvAdventureDungeonBranch.delete()` does
  `search.search_object_by_tag(self.key, category="dungeon_room")` (and `…dungeon_character`),
  relocates the characters, deletes every tagged room, then removes the branch script. (This is exactly
  DR-15's "reset by deleting the run's tagged objects.")
- **A reaper Script GCs abandoned instances.** `EvAdventureDungeonBranchDeleter` runs on an interval
  (default hourly), iterates the branch scripts, compares each `last_updated` against a max-life
  threshold, and calls `branch.delete()` on the expired ones. (Exactly DR-15's "GC'd by a reaper
  Script if abandoned.")

So **DR-15's four-part lifecycle (tag-with-run_id → create-on-start → delete-tagged-on-end →
reaper-GC) is the documented, framework-endorsed idiom**, not a guess. It is also shipped in a real
production game: **Arx** runs generated/instanced content (its *Shardhaven* generated dungeons), which
demonstrates the tag-based approach scales in anger ([arxcode](https://github.com/Arx-Game/arxcode)).

### Two improvements over the naive version
1. **Spawn the zone from a prototype set, not ad-hoc `create_object` calls.** Whiteout clones a *fixed*
   authored zone per run (unlike the dungeon's procedural rooms). Use `evennia.prototypes.spawner.spawn`
   with a "run prototype set" so a party-start mints the whole tagged room/object graph in one
   declarative call — idiomatic, and it keeps the authored zone as data.
   ([Prototypes/spawner](https://www.evennia.com/docs/latest/Components/Prototypes.html))
2. **Make the reaper query orphans by Tag, not only by live-run iteration.** The contrib's
   `delete()` is the happy path; if a run Script dies or a crash interrupts teardown, you can get
   *orphaned* rooms/objects still carrying a `run_id` tag whose run no longer exists. The reaper should
   *also* sweep `ObjectDB.objects.get_by_tag(category="run")` for tags whose run-Script is gone and
   delete those, so cleanup is robust to partial failures. (DR-06's debris cap/merge is the other
   bound, keeping per-run object counts down.)

### Pitfalls (and that they're benign here)
- **Orphaned objects** — handled by the tag-sweeping reaper above; this is the main one.
- **dbref churn** — Evennia dbrefs are monotonic and **not reused**, so churning thousands of per-run
  objects makes dbref *numbers* climb with "holes." This is cosmetic: don't key anything on dbref
  density or contiguity, and don't display dbrefs as run-stable ids (use the seeded logical ids from
  DR-12). No functional problem.
- **Postgres dead tuples** — mass deletes leave dead rows for autovacuum to reclaim; with bounded
  party sizes and DR-06's debris caps the volume is small. Fine.
- **Idmapper RAM** — instanced rooms/objects sit in the idmapper while resident; bounded per active run,
  and freed on delete (`pre_delete` flushes the instance, `idmapper/models.py` L564). Fine.

### Verdict, pattern, delta
- **Verdict: CONFIRM (strong) + minor IMPROVE.** DR-15 matches an official contrib and a shipped game
  almost line-for-line. Improvements: spawn the zone from a **prototype set**; have the **reaper sweep
  orphans by tag** (not just iterate live runs).
- **Recommended pattern:** one `RunInstance` Script per party = the run identity; `run_id` as a **Tag**
  (category `"run"`) on every room/object/character; spawn the authored zone via prototypes at party
  start; teardown = `search_object_by_tag(run_id, "run").delete()`; a global reaper Script (interval ~
  minutes for abandoned-run timeout) deletes runs with no connected sessions past a TTL *and* sweeps
  tag-orphans.
- **Confidence delta (DR-15): +15 (→ ~83).** Largest raise of the four — what was the weakest
  "reasoned, unverified" decision (C=68) turns out to be the framework's own endorsed pattern with a
  reference implementation we can lift directly.

---

## Q4 — Per-action object load / WorldView snapshot (bonus, DR-13/perf)

**Short verdict: cheap — CONFIRM.** Two cache layers make per-action snapshotting effectively
memory-bound:
- **`room.contents` returns idmapper-cached typeclass instances.** Once an object has been loaded, the
  idmapper hands back the same Python object — no DB round-trip per access
  ([idmapper.models](https://www.evennia.com/docs/latest/_modules/evennia/utils/idmapper/models.html)).
- **Attribute reads are served from the AttributeHandler's aggressive cache.** "Reading from an already
  cached Attribute is as fast as reading any Python property." The first attribute access on an object
  triggers one query that loads *all* its attributes (`_cache_complete`), and everything after is a
  dict hit ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html);
  `attributes.py` `_load_cache`/`get_all_attributes` ≈ L529/L914).

**The one gotcha: cold first-touch is N+1.** For a freshly loaded room, the *first* snapshot pays ~one
query per object to warm its attribute cache (object N → N attribute-load queries); subsequent
snapshots are warm. Mitigations if cold-start ever shows up in profiling: prefetch attributes in bulk,
and keep object counts bounded (DR-06 debris cap/merge + DR-15 per-run scoping + DR-13's zone-scoped
WorldView already do this). For a single-room scene with bounded contents this is negligible — the
read side of `apply`/`resolve` is fine. (Note the cache is for *reads*; the Q1 stale-on-rollback issue
is a write-path concern, unrelated to read cost.)

---

## Summary table

| Decision | Verdict | Recommended change | Confidence delta |
|----------|---------|--------------------|------------------|
| **DR-07** State in Attributes + Tag mirror | **CONFIRM** | None. Attributes are pickled & not value-queryable → Tag-mirroring queryable axes is the documented idiom; same-transaction Attribute+Tag write supported. | **+3 → ~85** |
| **DR-10** One enforced atomic mutation path | **IMPROVE** | Keep ledger-check-before-write inside `transaction.atomic`; **add cache-invalidation on rollback** (`reset_cache()` touched attr/tag handlers in `except`); make Effects *replace* containers (not mutate fetched SaverLists) and have the lint catch SaverList in-place writes too. Lint of `.db=`/`.ndb=`/`.attributes.add`/`.tags.add` confirmed feasible. | **+2 → ~82** (works + lint feasible; offset by a real, mitigable rollback-desync footgun found) |
| **DR-14** Activity persistence across `@reload` | **CONFIRM** | Persist Activity progress/deadline in Attributes (not `.ndb`); on `at_start` recompute remaining work rather than trusting the Script timer's elapsed estimate. Persistent Script + TickerHandler both restore on reload. | **+8 → ~83** |
| **DR-15** Instanced co-op runs | **CONFIRM (strong) + minor IMPROVE** | Matches the official EvAdventure *dungeon* contrib (tag-by-run_id, create-on-start, delete-by-tag, hourly reaper) and Arx Shardhaven. Improve: spawn the authored zone from a **prototype set**; have the reaper **sweep tag-orphans**, not just iterate live runs; treat dbref churn as cosmetic. | **+15 → ~83** |

**Net effect.** All four decisions are sound; none needs reversal. The research **raises** confidence
across the board, most sharply on DR-15 (weakest → framework-endorsed with a reference implementation).
The single substantive *new* requirement is DR-10's cache-invalidation-on-rollback — a small, testable
addition to `apply()`, not a redesign.

### Sources
- Evennia Attributes — https://www.evennia.com/docs/latest/Components/Attributes.html
- Evennia Tags — https://www.evennia.com/docs/latest/Components/Tags.html
- Evennia attributes source — https://www.evennia.com/docs/latest/_modules/evennia/typeclasses/attributes.html
- Evennia idmapper source — https://www.evennia.com/docs/latest/_modules/evennia/utils/idmapper/models.html
- Evennia Scripts — https://www.evennia.com/docs/latest/Components/Scripts.html
- Evennia TickerHandler — https://www.evennia.com/docs/latest/Components/TickerHandler.html
- Start-Stop-Reload — https://github.com/evennia/evennia/wiki/Start-Stop-Reload · https://www.evennia.com/docs/latest/Setup/Running-Evennia.html
- Command-Duration howto — https://www.evennia.com/docs/latest/Howtos/Howto-Command-Duration.html
- EvAdventure dungeon (instancing) — https://www.evennia.com/docs/latest/api/evennia.contrib.tutorials.evadventure.dungeon.html · https://github.com/evennia/evennia/blob/main/evennia/contrib/tutorials/evadventure/dungeon.py
- Prototypes / spawner — https://www.evennia.com/docs/latest/Components/Prototypes.html
- Arx (arxcode) — https://github.com/Arx-Game/arxcode
- Django 6 transactions — https://docs.djangoproject.com/en/6.0/topics/db/transactions/
</content>
</invoke>
