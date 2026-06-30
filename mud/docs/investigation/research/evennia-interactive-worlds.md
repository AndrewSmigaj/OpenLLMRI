# Evennia for Deeply Interactive, Systemic Worlds — Feasibility Research

**Subject:** "Whiteout" — a systemic survival MUD on Evennia 6.0 (Python 3.13, Django 6, PostgreSQL).
**Question:** How idiomatic — vs. how much *fighting-the-framework* — is each subsystem Whiteout needs?
**Method:** Official Evennia docs (`https://www.evennia.com/docs/latest/` / `https://docs.evennia.com`), the Evennia GitHub source, and reputable community sources (Griatch's dev blog, the Evennia Google Group, MU Soapbox). Citations inline.

---

## 0. Executive framing

Evennia is a single-process server built on the **Twisted** reactor with **Django** as the ORM, split into a **Portal** (protocol/connection layer) and a **Server** (all game logic), communicating over AMP, designed to run on one machine ([Portal-And-Server](https://www.evennia.com/docs/latest/Components/Portal-And-Server.html)). Three architectural facts dominate every decision below:

1. **The reactor is single-threaded and must never be blocked** — one slow command or tick freezes *all* players ([Async-Process](https://www.evennia.com/docs/latest/Concepts/Async-Process.html)).
2. **Game objects are typeclassed Django proxy models cached in memory by the idmapper** — repeated reads are as cheap as Python attribute access, but every touched object stays resident in RAM until reload/flush ([Typeclasses](https://www.evennia.com/docs/latest/Components/Typeclasses.html)).
3. **Attributes are pickled blobs you cannot query by value; Tags are the indexed, queryable primitive** ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html), [Tags](https://www.evennia.com/docs/latest/Components/Tags.html)).

The headline result: **5 of 7 Whiteout subsystems are idiomatic or near-idiomatic** (perception rendering, tick/clock, per-observer routing, ontology-payload-in-Attributes, and the LLM async seam — the last has a *ready-made reference implementation in core*). The two friction points are **a primary natural-language parser** (Evennia's command matcher pre-empts free text) and **content density at scale** (single-process ceiling + per-tick DB-write amplification). Notably, Whiteout's "single scene room" design *reduces* the worst attribute-query/reachability tax, because reachability is computed over a small in-memory `room.contents` set rather than via cross-DB queries.

---

## 1. Custom perception rendering — `return_appearance` + `get_display_*` hooks

### How the Evennia 6 appearance pipeline works

The `look` command triggers a fixed call chain ([Objects](https://www.evennia.com/docs/latest/Components/Objects.html), [API: evennia.objects.objects](https://www.evennia.com/docs/latest/api/evennia.objects.objects.html)):

```
look <target> → caller.at_look(target) → target.return_appearance(looker, **kwargs)
```

`return_appearance(looker, **kwargs)` is "the main callback used by `look` for the object to describe itself." It fills a template string from a set of component hooks. The **real default template** (from the API; the prose page shows a simplified version) is:

```python
appearance_template = "\n{header}\n|c{name}{extra_name_info}|n\n{desc}\n{exits}\n{characters}\n{things}\n{footer}\n    "
```

Each `{slot}` is produced by a hook, **all of which receive `looker` and arbitrary `**kwargs` and return a string**:

| Slot | Hook | Default |
|---|---|---|
| `{name}` | `get_display_name(looker=None, **kwargs)` | `self.name` (viewer-aware) |
| `{desc}` | `get_display_desc(looker, **kwargs)` | `self.db.desc` |
| `{header}` / `{footer}` | `get_display_header/footer(looker, **kwargs)` | empty |
| `{exits}` | `get_display_exits(looker, **kwargs)` | formatted exit list |
| `{characters}` | `get_display_characters(looker, **kwargs)` | formatted character list |
| `{things}` | `get_display_things(looker, **kwargs)` | formatted object list |
| (whole string) | `format_appearance(appearance, looker, **kwargs)` | final whitespace processing |

These hooks live on **`DefaultObject`** in `evennia.objects.objects`. The recommended override point is the empty **`ObjectParent`** mixin in your game template (`typeclasses/objects.py`), which `Object/Character/Room/Exit` all inherit — put cross-cutting overrides there, not on `DefaultObject`.

### Per-looker / distance / weather-graded descriptions — idiomatic?

**GREEN. This is the designed extension point.** Every hook receives `looker`, and the docs state outright that objects can "look different depending on who is looking at them." A graded perception render is simply:

```python
class ObjectParent:
    def get_display_desc(self, looker, **kwargs):
        score = perception_score(looker, self)        # distance, light, weather, skill
        if score < FOG_THRESHOLD:
            return "a vague shape in the whiteout"
        if score < CLEAR_THRESHOLD:
            return self.db.desc_obscured or self.db.desc
        return self.db.desc
```

The **Extended Room** contrib (`evennia.contrib.grid.extended_room`) is the in-repo proof of this pattern: it stores multiple descriptions keyed by room-state and embeds `$state(roomstate, text)` FuncParser tags, auto-resolving by season (`get_season()`) and time-of-day (`get_time_of_day()`), and exposes `add_room_state()/remove_room_state()` for arbitrary states like *stormy*, *flooded*, *dark* ([Contrib-Extended-Room](https://www.evennia.com/docs/latest/Contribs/Contrib-Extended-Room.html)). It overrides the desc-retrieval path so the appearance pipeline picks up the resolved text automatically. The Beginner Tutorial demonstrates the same hook-override style for items/NPCs ([Beginner-Tutorial-Objects](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part3/Beginner-Tutorial-Objects.html)).

**The one caveat that matters for Whiteout:** `return_appearance` returns a *single string to a single looker* — it is pull-based (the looker typed `look`). It is **not** a broadcast. Graded *ambient* perception ("you half-hear someone moving in the storm") belongs to §4's per-observer push, not here. So perception splits cleanly: **pull-render = `get_display_*` (GREEN, trivial); push-render = custom propagator (§4).**

---

## 2. Tick / clock engine — `TickerHandler` vs. global Scripts

Evennia offers two timing mechanisms; for a multiplayer heartbeat you use **both, for different jobs**.

### TickerHandler (`evennia.TICKER_HANDLER`) — fan-out to many subscribers

```python
TICKER_HANDLER.add(interval, callback, idstring="", persistent=True, *args, **kwargs)
TICKER_HANDLER.remove(interval, callback, idstring="", persistent=True)
```

A **subscription/pool** model: instead of one timer per object, all subscribers on interval *N* share **one clock**. "The time-keeping mechanism is only set up once for all objects," making it "highly optimized in resource usage" ([TickerHandler](https://www.evennia.com/docs/latest/Components/TickerHandler.html)). Key gotchas:

- **Identity key = `(callback, interval, persistent, idstring)`** — `*args/**kwargs` are *not* part of the key. Subscribe the same callback+interval twice with different args and the second silently overwrites the first unless you give distinct `idstring` values.
- **Persistence:** `persistent=True` (default) survives full shutdown; on shutdown each ticker's timer is saved and resumes from that point. `persistent=False` survives a `@reload` but comes back **stopped** after a shutdown — a classic "my timers vanished" bug.
- **Explicit doc warning:** *"You should never use a ticker to catch changes."* Don't poll many objects for state that rarely changed.

Canonical use is the **Weather tutorial** — a ticker fans a random echo out to all subscribed rooms ([Tutorial-Weather-Effects](https://www.evennia.com/docs/latest/Howtos/Tutorial-Weather-Effects.html)):

```python
TICKER_HANDLER.add(60 * 60, self.at_weather_update)   # every game-hour, all weather rooms
```

### Global Script — one authoritative world clock

A Script is a persisted typeclass carrying its own timer ([Scripts](https://www.evennia.com/docs/latest/Components/Scripts.html)):

```python
class GameTickScript(DefaultScript):
    def at_script_creation(self):
        self.key = "game_heartbeat"
        self.interval = 60          # seconds
        self.persistent = True      # timer survives @reload/reboot
        self.start_delay = True
    def at_repeat(self):
        advance_world_clock()       # weather, temperature, world events
```

`interval`, `repeats` (0 = infinite), `start_delay`, and `persistent` (default `True`) control the timer; hooks are `at_repeat()`, `at_start/at_stop/at_pause`, and `is_valid()` (returning `False` stops it). Register it once as a **global** script via `settings.GLOBAL_SCRIPTS` so Evennia auto-creates/maintains a single instance accessible through the `GLOBAL_SCRIPTS` container.

### Recommendation & pitfalls

**GREEN.** Use **one Global Script as the master clock** + **TickerHandler for object fan-out** (decay, weather echoes). Pitfalls, all documented or structural:

1. **Drift.** Both reschedule `interval` *from the moment the tick ran*, not against the wall clock — drift accumulates and reload resumes from a saved offset. **Never count ticks to track in-game time.** Store an epoch timestamp and *recompute* the calendar (`hour = f(time.time() - start)`); let the tick only *advance/recompute*.
2. **DB writes per tick** are the real scaling trap (§8). A fast ticker writing `obj.db.x` across many objects is the worst case. Keep hot per-tick state on `.ndb` and prefer lazy/computed values (e.g. the traits `.rate`, §7).
3. **Wrong tool / polling** — heed the "never use a ticker to catch changes" rule; prefer event hooks for rare state changes.
4. **idstring collisions** (above).

---

## 3. Natural-language / custom parsing — CmdSets, `CMD_NOMATCH`, custom parser

### How input is matched

On every line, `cmdhandler()` gathers cmdsets from three sources (objects in the caller's location incl. exits; the caller's own cmdset; account/session cmdsets), merges them by priority/merge-rule, and hands the merged set to the parser ([Commands](https://www.evennia.com/docs/latest/Components/Commands.html), [API: cmdhandler](https://www.evennia.com/docs/latest/api/evennia.commands.cmdhandler.html)). The parser (`evennia.commands.cmdparser`, [source](https://www.evennia.com/docs/latest/_modules/evennia/commands/cmdparser.html)) matches each command's `key` + `aliases` against the **start** of the raw input, supports **abbreviation/prefix matching** (`n`→`north`), strips `CMD_IGNORE_PREFIXES` (default `"@&/+"`), and ranks candidates by `cmdlen` (chars matched) and `mratio` (fraction of input covered).

### System commands (syscmdkeys) and routing free text

`evennia.syscmdkeys` exposes magic command keys ([Commands](https://www.evennia.com/docs/latest/Components/Commands.html), [syscommands source](https://www.evennia.com/docs/latest/_modules/evennia/commands/default/syscommands.html)):

- `CMD_NOMATCH` — no command matched (default replies *"Huh? (Type 'help' …)"*)
- `CMD_NOINPUT` — bare return
- `CMD_MULTIMATCH` — several matched
- `CMD_NOPERM`, `CMD_CHANNEL` (input matched a channel name), `CMD_LOGINSTART` (new connection)

Route unrecognized prose to a custom interpreter by overriding `CMD_NOMATCH`:

```python
from evennia import syscmdkeys, Command

class CmdNLFallback(Command):
    key = syscmdkeys.CMD_NOMATCH          # the magic key
    def func(self):
        text = self.raw_string.strip()    # NOTE: use raw_string, not args, for free text
        self.caller.msg(nl_interpreter(self.caller, text))
# add CmdNLFallback() to CharacterCmdSet.at_cmdset_creation
```

### Command lifecycle (for a custom `parse()`)

Order: `at_pre_cmd()` (return truthy to **abort**) → `parse()` → `func()` → `at_post_cmd()`. Runtime attributes: `self.args` (input minus the matched command word), `self.raw_string` (full unstripped input), `self.cmdstring` (the matched key — **not** `cmdname`), plus `self.caller`/`self.session`/`self.obj`. The docs sell the `parse()/func()` split for sharing one parser across a verb family: define `class NLCommand(Command)` with a smart `parse()` and subclass per verb. To replace the matcher wholesale, set `settings.COMMAND_PARSER`.

### Assessment

**YELLOW.** A `CMD_NOMATCH` fallback for "interpret leftover prose" is explicitly sanctioned and clean. But three things fight a *primary* NL loop:

1. **The prefix-matcher pre-empts free text.** Any sentence beginning with a word that abbreviates an existing command (`s` → `south`, `l` → `look`) is consumed before `CMD_NOMATCH` ever fires. `CMD_CHANNEL` and `2-ball` multimatch numbering also sit ahead of it.
2. **`CMD_NOMATCH` is all-or-nothing** — it only sees `raw_string`, only when *zero* commands matched. It's a fallback, not a per-token NLP layer.
3. For a true NL game loop you'll either keep the command set tiny + disable abbreviation, route everything through **one dominant NL `Command` with a rich `parse()`**, or replace `settings.COMMAND_PARSER` (heaviest, but stops fighting the matcher).

> Note: the standalone `Components/Command-Parser.html` page is **404 in `latest`**; that content now lives in `Commands.html` + the `cmdhandler`/`cmdparser` API/module pages.

---

## 4. Message routing beyond a single broadcast

### `msg_contents` is already a per-observer loop

```python
DefaultObject.msg_contents(text=None, exclude=None, from_obj=None,
                           mapping=None, raise_funcparse_errors=False, **kwargs)
```

It iterates `self.contents` (minus `exclude`) and, **for each receiver, re-parses `text` through the FuncParser with that receiver as the perspective, then calls `receiver.msg()`** ([API: objects](https://www.evennia.com/docs/latest/api/evennia.objects.objects.html), [Change-Message-Per-Receiver](https://www.evennia.com/docs/latest/Concepts/Change-Message-Per-Receiver.html)). So per-receiver variation is produced by inline funcs, not by you sending one literal string.

### Actor-stance inline funcs (`ACTOR_STANCE_CALLABLES`)

`$you([key])`/`$You([key])`, `$conj(verb[, key])`, `$pron(pronoun[, …][, key])`, `$obj(key)` ([FuncParser](https://www.evennia.com/docs/latest/Components/FuncParser.html)). `msg_contents` supplies the required `caller`/`receiver`/`mapping` kwargs automatically:

```python
room.msg_contents("$You() $conj(pick) up the gun, whistling to $pron(yourself).",
                  from_obj=caller, mapping={"gun": gun_object})
# actor sees: "You pick up the gun, whistling to yourself."
# others see: "Tom picks up the gun, whistling to himself."
```

`get_display_name(looker=receiver)` is evaluated per receiver, so **viewer-aware naming is free**. `at_say(message, msg_self=, msg_location=, receivers=, msg_receivers=, …)` and `CmdPose` give speech/pose hooks routed through the same machinery ([API: general](https://www.evennia.com/docs/latest/api/evennia.commands.default.general.html)).

### The rpsystem contrib is the reference per-observer propagator

`evennia.contrib.rpg.rpsystem` ([Contrib-RPSystem](https://www.evennia.com/docs/latest/Contribs/Contrib-RPSystem.html), [API](https://www.evennia.com/docs/latest/api/evennia.contrib.rpg.rpsystem.rpsystem.html)) implements exactly "genuinely different string per observer based on what that observer knows":

```python
send_emote(sender, receivers, emote, msg_type='pose', anonymous_add='first', **kwargs)
parse_sdescs_and_recogs(sender, candidates, string, search_mode=False, …)
```

`send_emote` parses `/sdesc`-style refs into markers once, then **loops over `receivers` building a personalized string for each** — substituting each observer's own **recog** (personal nickname) with **sdesc** ("a tall man") as fallback, then calling `receiver.msg()` individually. This is the template for graded perception: each observer sees a string scaled to *what they can perceive/recognize*.

### Building Whiteout's graded-perception propagator

Three tiers, increasing in cost — **all are accepted Evennia practice**:

1. **Pure `msg_contents` + actor-stance funcs** (GREEN) — enough when the only per-observer difference is grammar (you/name, verb conjugation, pronouns) and recog/sdesc naming.
2. **A custom FuncParser callable** (GREEN, cleanest for content) — register e.g. `$perceive(...)` that receives `receiver` and returns *different content* per observer; keep using `msg_contents`. This is how rpsystem/extended_room extend the system.
3. **Explicit per-observer loop** (YELLOW, most flexible) — required when the difference is *visibility/audibility itself*, not grammar: a sound only some hear, a mover only some see, fully suppressed for others. `for obs in room.contents: obs.msg(render_for(obs, event))`. This is exactly what `send_emote` does internally, so it is **not fighting the framework**.

**The only anti-pattern is cramming perception-gated content into a single funcparser template string.** For Whiteout's single-scene graded model, expect a bespoke propagator in the spirit of `send_emote`: compute each co-located observer's visibility/audibility/reachability and emit a tailored-or-suppressed line. **GREEN overall (a proven pattern exists), with the honest note that the graded propagator is custom code you write once.**

---

## 5. State at scale — Attributes, AttributeProperty, idmapper

### Attributes API & storage

```python
obj.db.foo = [1, 2, 3]                                  # category=None shortcut
obj.attributes.add("neck", item, category="clothing")   # categorized
neck = obj.attributes.get("neck", category="clothing")
strength = AttributeProperty(10, category="stat")       # class-level, Django-Field-like
sleepy   = AttributeProperty(False, autocreate=False)   # no DB row until first write
```

Values are **pickled** into the `db_attributes` table (`db_value`); each Attribute is a row, M2M-linked to objects ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html)). Mutable collections return `_SaverList`/`_SaverDict`/`_SaverSet` wrappers that **write through to the DB on in-place mutation**; call `.deserialize()` to detach a plain copy (then you must re-save). DB objects inside Attributes are stored as `(classname, dbid, date)` refs.

### idmapper / SharedMemoryModel cache

Evennia uses the **idmapper** to cache typeclasses (Django proxy models) in memory: unlike vanilla Django (new instance per query), it returns the **same instance**, so on-object handlers, properties, and `.ndb` survive for the life of the server (cleared on reload) ([Typeclasses](https://www.evennia.com/docs/latest/Components/Typeclasses.html), [idmapper source](https://www.evennia.com/docs/latest/_modules/evennia/utils/idmapper/models.html)). This is why repeated lookups are dict hits and cached Attribute reads are "as fast as reading any Python property." API: `cache_instance`, `get_cached_instance`, `flush_cache()` (fires `at_idmapper_flush()` per object), `conditional_flush()` (above a memory threshold). The cache holds **strong refs** — the speed win and the memory cost are the same coin: every touched object stays resident.

### The query problem and the Tags answer

**You cannot query Attributes by value.** Values are pickled strings, so `db_attributes__db_value__lt=4` does **not** work; you can only filter `db_key` + exact `db_value`, with no index on the blob → table scans. **Tags are the queryable primitive** ([Tags](https://www.evennia.com/docs/latest/Components/Tags.html)): *"Tags are more efficient than Attributes since on the database-side, Tags are shared between all objects with that particular tag."* A Tag carries no value (existence is the signal), enabling fast set membership and batch ops:

```python
obj.tags.add("steel", category="material")
obj.tags.add("outdoors", category="zone")
evennia.search_tag("steel", category="material")   # indexed QuerySet
```

**Zones/regions are the documented Tag use case** (a weather script over all `outdoors`-tagged rooms).

### Assessment — ontology in Attributes

**YELLOW (mixed, and resolvable).**

- Storing a rich object/material/action ontology as the **per-object payload** of a thing you already hold a handle to is **idiomatic** — Attributes pickle arbitrary nested Python and read from cache cheaply; use `AttributeProperty` + categories for typed fields.
- It turns adversarial the moment you **query across** the ontology ("find all flammable steel objects," "everything in zone 7"): every such lookup scans pickled blobs. This is the **"zone-as-attribute reachability tax"** — encoding spatial/grouping membership as an Attribute makes each reachability/region query O(N) where Tags give indexed O(matches).
- **Fix:** model the ontology's *searchable axes* (material, zone, affordance class, flammable/etc.) as **Tags with categories**; keep free-form descriptive blobs in Attributes on the same object. Use `.ndb` for transient/derived per-tick state to avoid DB churn.

> **Whiteout-specific relief:** because Whiteout uses a **single "scene" room**, intra-scene reachability is computed over `room.contents` (small N, already in the idmapper cache, iterated in Python) — this **sidesteps the worst of the cross-DB attribute-query tax**. The tax bites mainly if/when you need *global* queries across many scenes; mirror those axes as Tags from day one.

---

## 6. External async — the LLM seam without blocking the reactor

### The rule

Evennia is a single-threaded Twisted reactor; blocking it freezes *every* player: *"If one user … runs a command containing that long_running_function, all other players are effectively forced to wait until it finishes"* ([Async-Process](https://www.evennia.com/docs/latest/Concepts/Async-Process.html)). Any slow external call (LLM/HTTP) must run off the reactor and deliver results via a callback.

### The toolbox

- **`evennia.utils.delay(timedelay, callback, *args, persistent=False, **kwargs)`** — non-blocking scheduling (e.g. a "thinking…" filler). For *when*, not for offloading work.
- **`evennia.utils.utils.run_async(func, *args, at_return=, at_err=, …)`** — runs a callable off-reactor. **Verified from current source ([utils.py](https://github.com/evennia/evennia/blob/main/evennia/utils/utils.py)) it uses `twisted.internet.threads.deferToThread` + `addCallback`/`addErrback`** — i.e. a real thread-pool thread. (The `latest` doc page's claim that it "runs in the same thread" is **stale vs. `main`**.) Because of the GIL, this parallelizes **I/O-bound** work (network releases the GIL) but **not** CPU-bound Python. So it's the right wrapper for a *blocking* `requests.post` to an LLM, the wrong tool for heavy local computation.
- **Native Twisted async HTTP** — `twisted.web.client.Agent` (or `treq`, a requests-like layer over it). The HTTP I/O is driven by the reactor itself, no worker thread, returns a `Deferred`. **Most idiomatic** in Evennia.
- **`@interactive`** decorator — pause a command with `yield` for sequenced flows.

Thread-safety: code inside a `deferToThread` thread must **not** touch the reactor — do `caller.msg(...)` in the `at_return` callback (which runs back on the reactor thread).

### The LLM contrib *is the reference implementation* (load-bearing)

`evennia.contrib.rpg.llm` ships an `LLMClient` + `LLMNPC` typeclass + a `talk` command (`CmdLLMTalk`), with per-player conversation memory and a "thinking" message after `thinking_timeout` ([Contrib-Llm](https://www.evennia.com/docs/latest/Contribs/Contrib-Llm.html), [client source](https://github.com/evennia/evennia/blob/main/evennia/contrib/rpg/llm/llm_client.py)). README: *"All these calls are asynchronous, meaning a slow response will not block Evennia."* The mechanism is **native Twisted — NOT `treq`, NOT `deferToThread`**:

```python
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.web.client import Agent, HTTPConnectionPool
from twisted.web.http_headers import Headers

class LLMClient:
    def __init__(self, ...):
        self._conn_pool = HTTPConnectionPool(reactor)
        self.agent = Agent(reactor, pool=self._conn_pool)

    @inlineCallbacks
    def get_response(self, prompt):
        status_code, response = yield self._get_response_from_llm_server(prompt)
        # ...returns the text; NPC then msg()'s the player when the Deferred resolves

    def _get_response_from_llm_server(self, prompt):
        d = self.agent.request(
            b"POST", bytes(self.hostname + self.pathname, "utf-8"),
            headers=Headers(self.headers),
            bodyProducer=StringProducer(json.dumps(request_body)),  # IBodyProducer
        )
        d.addCallbacks(self._handle_llm_response_body, self._handle_llm_error)
        return d
```

Config knobs: `LLM_HOST` (`http://127.0.0.1:5000`), `LLM_PATH` (`/api/v1/generate`), `LLM_HEADERS`, `LLM_PROMPT_KEYNAME`, `LLM_REQUEST_BODY` (`max_new_tokens`, `temperature`), `LLM_PROMPT_PREFIX`; tested against **text-generation-webui**, with an (untested) OpenAI option. `thinking_timeout`/`thinking_messages` are `AttributeProperty`s on `LLMNPC`.

### Assessment

**GREEN — there is literally a core reference to copy.** Mirror the contrib: an `Agent`/`treq`-based async client returning a `Deferred`, consumed with `@inlineCallbacks`, delivering via `caller.msg()` in the callback, with `utils.delay` for a "thinking…" filler. If you must use a blocking vendor SDK (the Anthropic/OpenAI Python client), isolate it behind `run_async(lambda: client.messages.create(...), at_return=deliver)` — documented and fine for I/O-bound calls, at the cost of one thread-pool slot per in-flight request. **Anti-patterns:** calling a synchronous SDK directly in `func()` (freezes all players), or spinning your own `threading.Thread` and touching `msg`/ORM from it.

---

## 7. Existing contribs & examples — reuse vs. build

Master list (53 contribs, 8 categories): [Contribs-Overview](https://www.evennia.com/docs/latest/Contribs/Contribs-Overview.html). Install via `from evennia.contrib.<category> import <name>`; you can copy a contrib folder into your game dir to fork it.

| Contrib | Path | What it gives | Reuse for Whiteout |
|---|---|---|---|
| **rpsystem** | `contrib/rpg/rpsystem` | sdesc, recog, `/me` `/sdesc` emote refs, pose, masks, **per-listener language obscuration**, whisper | **Use as the perception/identity backbone.** Intrusive: requires inheriting `ContribRPCharacter/Object/Room` + adding `RPSystemCmdSet` — adopt early. Extend sdesc to reflect wounds/worn state. ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-RPSystem.html)) |
| **extended_room** | `contrib/grid/extended_room` | season/time-of-day/state descriptions, `$state()` tags, virtual **details** | **Use as-is**; extend custom-states for weather/temperature/flooding/darkness. ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-Extended-Room.html)) |
| **traits** | `contrib/rpg/traits` | Static/Counter/**Gauge** with min/max + **`.rate`** (change/sec); `obj.traits.x` | **Use as-is for hunger/thirst/stamina/warmth.** `.rate` makes drains **lazy/computed-on-read → no per-tick DB write** (key perf win, §8). ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-Traits.html)) |
| **crafting** | `contrib/game_systems/crafting` | `CraftingRecipe` (tag-matched ingredients + tools → output prototypes), `craft()`, `pre/craft/post` hooks, `CRAFT_RECIPE_MODULES` | **Use as base**; add skill-checks/time/quality/yield-variance in the hooks (none by default). ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-Crafting.html)) |
| **clothing** | `contrib/game_systems/clothing` | wearable slots, layering/coverage, per-wear style | **Use as-is**; extend item attrs for cold-protection/armor/encumbrance. ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-Clothing.html)) |
| **unixcommand** | `contrib/base_systems/unixcommand` | `argparse`-style `--option`/positional parsing | Use for complex builder/admin commands (not the NL loop). ([doc](https://www.evennia.com/docs/latest/Contribs/Contrib-Unixcommand.html)) |
| **prototypes / spawner** (core, not contrib) | `evennia.prototypes` | data-driven object templates: `prototype_parent` inheritance, `$protfuncs` (`$random`, `$choice`…), `@spawn`, `olc` menu | **Backbone for a data-driven systemic world** (item/mob/resource templates). Use as-is. ([doc](https://www.evennia.com/docs/latest/Components/Prototypes.html)) |
| **EvAdventure / Beginner Tutorial** | `contrib/tutorials/evadventure` | Knave/OSR full game: rules engine, menu chargen, turn-based combat, NPC **AI state machine**, dungeon gen, quests, equipment, shops | **Reference/copy-adapt, not drop-in** (WIP). Mine the rules engine + AI state machine + combat loop patterns. ([Beginner-Tutorial-Overview](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.html)) |

**Notable real systemic games:** **Arx — After the Reckoning** ("a MUSH but with more coded systems") is the best open-source example of deep systemic Evennia code ([github.com/Arx-Game/arxcode](https://github.com/Arx-Game/arxcode); Evennia has an official tutorial for running its game dir, [Tutorial-Using-Arxcode](https://www.evennia.com/docs/latest/Howtos/Tutorial-Using-Arxcode.html)). **Ainneve** is the official community demo game ([github.com/evennia/ainneve](https://github.com/evennia/ainneve)). Live games: [games.evennia.com](http://games.evennia.com/).

**Net for Whiteout:** rpsystem + extended_room + traits + crafting + clothing + prototypes cover a large fraction of the *systemic surface* off the shelf. What you must **build**: the graded-perception propagator (§4), the NL parser (§3), and the integration glue (perception scoring, the survival tick logic, the LLM seam wiring).

---

## 8. Scaling limits

### Concurrent players (Dummyrunner benchmark, Griatch)

The canonical stress test uses Evennia's **Dummyrunner** — bots that log in and hammer commands ([Profiling](https://www.evennia.com/docs/latest/Coding/Profiling.html), [dummyrunner API](https://www.evennia.com/docs/latest/api/evennia.server.profiling.dummyrunner.html)):

- **Laptop:** ~**50–75** dummy players comfortable; 75–100 → longer login lag + occasional ~1s hiccups.
- **Desktop:** 1–75 unaffected; ~**150 easy, up to ~250 "on a good day."**
- In one documented run, **50 bots** doing `look` every ~2s used **~45% CPU**; **100 bots → ~100% CPU**.
- **Critical caveat:** the Dummyrunner is a *worst case* — bots fire far more commands/sec than humans (and build constantly). The docs warn it "taxes the server much more than real users." Real games carry **more headcount but fewer commands/sec**.

### Architecture limits

- **Single machine, single-threaded reactor per process** ([Portal-And-Server](https://www.evennia.com/docs/latest/Components/Portal-And-Server.html), [Evennia in pictures](https://evennia.blogspot.com/2016/05/evennia-in-pictures.html)). The Portal holds sockets so the Server can reload without disconnecting players, but **there is no native multi-machine / horizontal scaling** — vertical optimization is the path.
- **Django's ORM is blocking**, which conflicts with the async reactor. Griatch's experiments found offloading DB writes with `deferToThread` was **slower** (GIL), and multi-process pooling was slower under write load — conclusion **"caching is king"**: favor reads, cache hot data ([Combining Twisted and Django](http://evennia.blogspot.com/2012/08/combining-twisted-and-django.html)).

### DB / Attribute write load

- Attribute values are **pickled** (cost grows with structure) and **aggressively read-cached** by the idmapper; in-place list/dict mutations auto-save. Writes "are generally not a bottleneck … unless reading **and** writing many times per second" ([Attributes](https://www.evennia.com/docs/latest/Components/Attributes.html)). Use `.ndb` for transient/per-tick state.
- **The real per-tick trap:** a fast ticker writing Attributes across many objects. **Mitigation specific to survival meters:** drive hunger/thirst/stamina with **traits `.rate`** (timestamp-based, computed lazily on read) so drains require **no per-tick DB write** at all.

### Database backend

- **SQLite3** (default): often *faster* single-process, scales to **millions of objects**, but **not safe with multiple concurrent processes/threads** (errors under a game + separate web process) ([Choosing-a-Database](https://www.evennia.com/docs/latest/Setup/Choosing-a-Database.html)).
- **PostgreSQL** (Django-recommended for production): slower per-op but scales better with a large DB and/or a separate web process. **Whiteout already uses Postgres — the correct production choice.**

### Honest assessment

Game logic is **single-process/single-thread**, so the practical ceiling is **low hundreds of concurrent players on one strong server** — and *lower* for a systemic survival sim with heavy per-action computation unless carefully optimized (Arx demonstrates a large, heavily-coded game on this architecture). Headroom levers, in priority order: **(1) never block the reactor** (cheap commands/ticks, async offload); **(2) minimize per-tick DB writes** (`.ndb`, lazy traits `.rate`, caching, Tags over value-queries); **(3) Postgres**; **(4) no polling tickers.**

---

## Feasibility verdict

| Subsystem | Verdict | Idiomatic approach | Main risk |
|---|---|---|---|
| **Perception rendering** (per-looker, distance/weather-graded) | 🟢 **GREEN** | Override `get_display_desc/name/...(looker)` on `ObjectParent`; branch on a perception score; extended_room's `$state()` pattern for ambient states | Only the *pull* (`look`) path; graded *ambient* events need §4's propagator. `return_appearance` is one-looker-at-a-time, not a broadcast |
| **Tick / clock engine** | 🟢 **GREEN** | One **Global Script** master clock (derive time from a stored epoch) + **TickerHandler** for object fan-out | **Drift** (never count ticks for time) and **per-tick DB writes** (use `.ndb` + lazy traits) |
| **NL parsing** (free-text command entry) | 🟡 **YELLOW** | `CMD_NOMATCH` for leftover prose; for a *primary* loop, one dominant NL `Command` with a rich `parse()` or a custom `settings.COMMAND_PARSER` | Evennia's prefix/abbreviation matcher **pre-empts** free text; `CMD_NOMATCH` is all-or-nothing. Fighting the matcher unless NL is the primary parser |
| **Per-observer routing** (different text per observer) | 🟢 **GREEN** | `msg_contents` + actor-stance funcs for grammar/naming (free); custom FuncParser callable or explicit per-observer loop (à la rpsystem `send_emote`) for graded content | The graded-visibility propagator is **bespoke code** you write once; anti-pattern is cramming perception gating into one template string |
| **Ontology in Attributes** | 🟡 **YELLOW** | Per-object payload in Attributes (`AttributeProperty` + categories, idmapper-cached); searchable axes (material/zone/affordance) as **Tags** | **Zone-as-attribute reachability tax** — Attributes are unqueryable by value (O(N) scans). *Mitigated* for Whiteout: intra-scene reachability is over in-memory `room.contents` |
| **External LLM async** | 🟢 **GREEN** | Copy the core `evennia.contrib.rpg.llm` client: `twisted.web.client.Agent` + `@inlineCallbacks` + `Deferred`; deliver via `caller.msg()` in callback; `utils.delay` for filler | Must **never block the reactor** — no synchronous SDK in `func()`; isolate any blocking SDK behind `run_async(..., at_return=)` (1 thread/call) |
| **Content density** (deep ontology, many objects, many ticks) | 🟡 **YELLOW** | prototypes/spawner for data-driven objects; Tags for queryable axes; `.ndb` + lazy traits for hot state; Postgres | **Single-process ceiling (~low hundreds concurrent)** + **per-tick write amplification** + **idmapper RAM cost** (touched objects stay resident). No horizontal scaling |

**Bottom line:** Evennia is a *good* fit for Whiteout. Perception rendering, the tick engine, per-observer routing, and the LLM seam are idiomatic — the LLM async pattern even ships as a copyable core contrib, and the actor-stance/rpsystem machinery is purpose-built for "different observers see different things." The two areas where you'll work *with grain against the framework* are a **primary natural-language parser** (Evennia assumes command-keyword input) and **scale** (single-process; mind per-tick DB writes and memory). Both are managed, not blocking: a dedicated NL command/parser and a discipline of "Tags for queries, `.ndb`/lazy traits for hot state, never block the reactor" keep the design firmly on the rails.

---

### Primary sources

- Objects / appearance pipeline — https://www.evennia.com/docs/latest/Components/Objects.html · https://www.evennia.com/docs/latest/api/evennia.objects.objects.html
- TickerHandler — https://www.evennia.com/docs/latest/Components/TickerHandler.html · Scripts — https://www.evennia.com/docs/latest/Components/Scripts.html · Weather tutorial — https://www.evennia.com/docs/latest/Howtos/Tutorial-Weather-Effects.html
- Commands / syscmdkeys — https://www.evennia.com/docs/latest/Components/Commands.html · cmdhandler — https://www.evennia.com/docs/latest/api/evennia.commands.cmdhandler.html · cmdparser source — https://www.evennia.com/docs/latest/_modules/evennia/commands/cmdparser.html
- FuncParser — https://www.evennia.com/docs/latest/Components/FuncParser.html · Change-message-per-receiver — https://www.evennia.com/docs/latest/Concepts/Change-Message-Per-Receiver.html
- Attributes — https://www.evennia.com/docs/latest/Components/Attributes.html · Tags — https://www.evennia.com/docs/latest/Components/Tags.html · Typeclasses/idmapper — https://www.evennia.com/docs/latest/Components/Typeclasses.html
- Async-Process — https://www.evennia.com/docs/latest/Concepts/Async-Process.html · LLM contrib — https://www.evennia.com/docs/latest/Contribs/Contrib-Llm.html · client source — https://github.com/evennia/evennia/blob/main/evennia/contrib/rpg/llm/llm_client.py
- Contribs overview — https://www.evennia.com/docs/latest/Contribs/Contribs-Overview.html · rpsystem — https://www.evennia.com/docs/latest/Contribs/Contrib-RPSystem.html · extended_room — https://www.evennia.com/docs/latest/Contribs/Contrib-Extended-Room.html · traits — https://www.evennia.com/docs/latest/Contribs/Contrib-Traits.html · crafting — https://www.evennia.com/docs/latest/Contribs/Contrib-Crafting.html · clothing — https://www.evennia.com/docs/latest/Contribs/Contrib-Clothing.html · prototypes — https://www.evennia.com/docs/latest/Components/Prototypes.html
- Portal-And-Server — https://www.evennia.com/docs/latest/Components/Portal-And-Server.html · Profiling/Dummyrunner — https://www.evennia.com/docs/latest/Coding/Profiling.html · Choosing-a-Database — https://www.evennia.com/docs/latest/Setup/Choosing-a-Database.html · "Combining Twisted and Django" — http://evennia.blogspot.com/2012/08/combining-twisted-and-django.html
- Arx (open source) — https://github.com/Arx-Game/arxcode · Ainneve — https://github.com/evennia/ainneve
