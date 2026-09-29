# 19 — Multiplayer and instances

> **Status: reviewed with Andrew 2026-09-28.** Andrew answered its open questions on 2026-09-27.
> **Architecture counterpart:** [`perception-model.md`](../architecture/perception-model.md) (the
> shipped seeing and hearing across zones) ·
> [`implementation-architecture.md`](../architecture/implementation-architecture.md) §6 (DR-13,
> DR-13a), §7 (DR-14, DR-15, DR-15a), §13 (DR-22) ·
> [`adr/0004-zone-as-attribute-perception.md`](../architecture/adr/0004-zone-as-attribute-perception.md).
> **Sources:** [`GDD.md`](../scenarios/whiteout/GDD.md) §9/§16; [`VISION.md`](../../VISION.md).

---

## 2. Decisions

### Andrew's decisions

- **Overlapping perception, not one shared room** (recorded 2026-06/07; ADR-0004). Location,
  visibility, audibility, reachability, direction and detail are separate concerns, never collapsed
  into "the room". The architecture records overlapping perception as the deferred item that is
  nevertheless critical (§14). Seeing others in nearby zones and being able to talk to them is the
  part of multiplayer that matters to him.
- **Instanced, synchronous co-op** (GDD §9/§16, DR-15): a party plays one crash together, online at
  the same time, acting concurrently.
- **A run is one sitting of two or three hours**, about a week of game time, which the players can
  pause and return to later — a game played in sessions, not an ongoing world (2026-09-17,
  2026-09-27; DR-15b).
- **The party** (2026-09-27): up to five play — the four adults and the kid, one survivor each. A seat
  nobody plays is a dead character whose clothes and pockets can be searched. AI agents may play seats
  if the players want them.
- **Three run modes, one rule set** (2026-09-16): runs are for friends, for humans and agents
  together, and for agents only, all on the same rules.
- **An agent sees exactly what a human sees** (2026-09-16); structure goes to the log only, so a mixed
  run needs no second channel (document [20](20-the-agent-player-and-research.md)).
- **Agents may play non-human characters** (2026-09-17) — still players from the engine's side. The
  bear, some of the bigger animals and a few birds act, on the engine's behaviour rules or played by a
  lightweight model (2026-09-26, 2026-09-27; document 23).
- **The clock** (2026-09-17, 2026-09-27): it runs continuously at 15 game-minutes per real minute; a
  fast forward, proposed and agreed by the players, runs it at about 150×; awake players can stay in
  it and type a command to slow it; a player waking or any event that is not ambient drops it back to
  15×, and ambient events do not. Sleeping players can chat out of character. The numbers are tuned by
  playtesting.
- **An agent acts at the speed of typing its command; a slow model is simply slow** (2026-09-26,
  2026-09-27). In a run with humans the clock does not wait for a model.
- **A missing player's character goes catatonic** — sits down and stares off; the other players can
  keep them alive if they want, and the character can die (2026-09-27). The party is warned when a
  member is missing (2026-09-17).
- **Ghosts** (2026-09-17, 2026-09-27): a dead player is a ghost and moves freely. Ghosts hear one
  another; the living do not hear ghosts. Anyone, living or dead, can use the out-of-character chat.
- **No gate on violence** (2026-09-16, 2026-09-26): a strike wounds in every kind of run — friends,
  humans with agents, agents only — and there is a combat system like a MUD's. Multiplayer never turns
  a hit into a shove.
- **The whole valley is in the first complete run** (2026-09-16): all fifty outdoor zones, so a party
  can be spread across the valley, not just across a crash site. Walking out is not an ending
  (2026-09-17).
- **Co-op has first-class interdependence** (GDD §16): acts that genuinely need two people, so co-op is
  a shared story, not parallel solitaire.

### Proposals (Claude)

- The **instance lifecycle** (accepted 2026-09-28; its details held for the implementation plan) — spawn from a prototype set, tag every object with a `run_id`, persist
  in Postgres during play, reset by deleting the run's tagged objects, and a reaper Script (DR-15's
  mechanism). This mirrors Evennia's EvAdventure dungeon contrib; it is an idiomatic pattern, not an
  invented one. A paused run is never reaped (§4.1).
- The **band table and the hop math** (see-edge hops, 0–4, no see-path → out of sight), the **speech
  ranges** (whisper/say/call/shout), the **muffle cost**, and the **weather band-steps**. These are
  built and in code, but the specific bands, ranges and steps are proposals until read.
- The **reachable/visible split** and the "too far to {verb} from here" answer.
- **Interdependence as one general rule** — an act's needs met by what the actors present bring
  together (§4.7).
- The **typing pace** in numbers; what the party can do for a
  catatonic member (§4.6).
- The **acting animals perceive by the same bands**, and scent is a channel still to be designed
  (§4.4).
- No shared status readout of other players (§4.8).

---

## 3. In one paragraph

You and the others who walked away from the same broken aeroplane are in one run, on one clock, at the
same time. You are not standing in a shared box: you are in the mid cabin, someone is up in the cockpit
with the pilot's body, someone has already gone out to the tail. You can *see* them from where you are —
clearly if they are next door, as a shape moving on the far shore four zones off — and you can talk to
them: a whisper carries to the person beside you, a shout carries across the crash site, and the wind
and the falling snow eat the difference. What you cannot do is *reach* them, or the orange case you can
plainly see by the bulkhead; for that you walk over. The clock runs for everybody at once, so while you
are prying at a jammed door your friend's fire is burning down and the cold in the cabin is climbing on
the same minutes you are spending. When you all agree to fast-forward — to sleep, or to wait out the
dark — the hours run past; whoever stays awake watches them go and can slow the clock with a command,
and someone waking or something that matters drops it back to its normal pace. If one of you does not
agree, the clock keeps its normal pace for everyone. The run is yours alone — your own copy of the
valley, no strangers walking through it — and it covers about a week of game time in one sitting of two
or three hours, which you can pause and come back to.

---

## 4. The design

### 4.1 A run is an instance

A **run** is one party's private copy of the world: a fresh world-state spawned from a prototype set
and tagged with a `run_id` (DR-15). Two parties playing Whiteout at the same time are in two
unconnected valleys. Solo is a one-player instance — the same code path, a party of one.

The lifecycle (**proposal**, DR-15):

| stage | what happens |
|---|---|
| create | spawn the prototype set; tag every object with the run's `run_id`; seed the run's RNG (DR-12) |
| persist | the run lives in Postgres while it is played, and while it is paused, until the party returns (DR-15b) |
| reset | delete the run's tagged objects (`search_object_by_tag`) at the end |
| GC | a reaper Script sweeps a run that has ended — rescued or dead — or been discarded, and any objects whose run no longer exists |

A paused run is never reaped: a pause is the party's choice to come back, a state of the run rather
than an absence of sessions, so the reaper needs no timeout (2026-09-28). How the instance machinery
is built is the implementation plan's. *Implementation note carried from the architecture: `search_object_by_tag` lives under
`evennia.search` / `evennia.utils.search`, and the reference instancing usage is
`evennia/contrib/tutorials/evadventure/dungeon.py`.*

### 4.2 The party, the seats and the run modes

**Up to five play** — the four adults and the kid, one survivor each; the seats and what each
survivor carries are document [16](16-players-and-kit.md). **A seat nobody plays is a dead
character**, whose clothes and pockets can be searched. **AI agents may play seats** if the players
want them (Andrew, 2026-09-27).

Friends only · humans and agents together · agents only. **One rule set.** Nothing in the engine asks
which mode it is in: an agent connects to a player account over telnet and issues the commands a
human issues (ADR-0005), and sees what a human sees. The consequences of "same rules" are concrete:
violence resolves with real physics in every mode; the clock and the fast forward apply to agents
exactly as to people; a research run is a run. An agent may play a survivor or a non-human character —
the bear, one of the bigger animals, a bird — from outside, through the same grammar (Andrew,
2026-09-17, 2026-09-26), and the person on the other end of the radio is played by a weak language
model (document [14](14-rescue-paths.md) §3.3); the engine does not know which character is played by
whom.

### 4.3 Seeing across zones

A Scene (the crash site) is **one room**; where you stand inside it is a **zone**
([ADR-0004](../architecture/adr/0004-zone-as-attribute-perception.md)). What you perceive is computed
from your zone toward the thing perceived, and graded into a band:

| band | what you get |
|---|---|
| same zone | detailed |
| adjacent zone | clear |
| near | summarized |
| distant | vague |
| barely visible | a shape or a motion |
| audible only | sound, no sight |
| out of sight | nothing at all — no message |

**The band math (shipped; the numbers are proposals):** the band is the **see-edge hop count** through
the zone graph — 0 hops same zone, up to 4 hops barely visible, no see-path at all means out of sight
— shifted by weather in band-steps. A wall is simply an **absent see-edge**; that is the whole
occlusion model today. Weather is a stubbed parameter (`"clear"`) until the weather arc threads real
state; the band-steps it will apply are in §4.4.

So "you can see two or three zones away" is the practical shape of it: the party stays visible to each
other across the crash site, and someone far enough off is a shape, not a person. **Sight works within
a Scene** (Andrew, 2026-09-28) — a connected group of places; you do not automatically see into another
Scene. Where the land is really open — across the lake, down the burn — something big such as the bear
can be seen far off; bushes, dense trees and weather block it, decided case by case by common sense.

**Traveling between Scenes** (Andrew, 2026-09-28). A Scene is a connected group of places — a
multi-place zone, bigger or smaller — and going to another one is a journey, not a step: you head off
in its direction and the world gives an estimate (*"You head off toward the birch grove; you reckon it
will take about twenty minutes."*). The walk is an attended activity with its own emotes, and on a
long one you may pass things along the way. You can stop walking, and then you are between Scenes —
*"You are between the birch grove and the plane"* — with whatever is near you, and no room description
beyond that. Moving from place to place inside a Scene takes time too, with the right emotes.

Direction is phrased from the bearing between zones plus the elevation difference — the eight compass
points with *upslope* / *downslope*: *"to the southeast and upslope"*.

### 4.4 Hearing and talking across zones

Speech is a **loudness**, and loudness is a reach in zone-hops (shipped; the mapping is a proposal):

| mode | reach | its synonyms (a floor) |
|---|---|---|
| whisper | the same zone | murmur, mutter, breathe |
| say | adjacent | speak, tell, talk |
| call | near | call out, holler |
| shout | distant | yell, bellow, scream |

Four levels, each with its synonyms written in the same pass (Andrew, 2026-09-28; document 04 §3.7).

Weather shifts the reach in band-steps — steady snow −1 down to whiteout −3 — clamped so the same
zone always hears you; this week the worst is the day-6 flurry at its heaviest (document 13 §4.2). A
**muffled** edge (sound passes, damped) costs 2 hops instead of 1. Non-speech events use the identical
scale: quiet work carries a zone, shattering glass carries three. This is why the weather is a social
pressure and not just a temperature: as the day-6 flurry closes in, the party's voices stop reaching
each other before their bodies do.

**The acting animals** (2026-09-28). The bear, the bigger animals and the
few birds that act perceive and are perceived through these same bands: a survivor sees the bear as a
shape four zones off, and the bear hears a shout the way a person does. One channel the bands do not
carry yet is **scent**. A real bear finds meat, a body and a camp by smell, downwind and far past
sight; smoke and cooking carry on the wind for people too. Scent travels with the wind and lingers
where sound does not, so it is not a loudness — it is its own propagation, owned by a scent-and-wind
design (`PLAN.md` A10), to be written with document 23's animals and document 13's wind.

Every game message goes through the **propagator** rather than being broadcast to the room: for each
observer the shell computes the band toward the event's source and renders *that band's* line — the
full third-person line, then a direction-framed line, then *"…is working at something"*, then
*"A shape shifts {direction}"*, then sound only, then silence. Nobody is told what they could not
have perceived. **Within the zone, every act reaches everyone present as the full line** — the game
does not know which way anyone is facing; the one covert act is a deliberate `steal` (Andrew,
2026-09-27; document 15 rule 5).

### 4.5 Seeing is not reaching

Reachability is a separate answer: you can see the orange case by the bulkhead and be unable to touch
it. An attempt on something visible-but-far gets the physics of why, not a refusal — *"You can see the
{target} {direction}, but it is too far away to {verb} from here."* — and it is excluded from the
wall-sensor, because it is an answer, not a gap. The parser still *matches* distant nouns, so a far
thing gets an honest "too far", never "you don't see that here".

This is the **reachability tax**, the accepted price of one room per Scene: it is paid at one central
gate in the resolver plus the item-command pre-flight and the appearance hook, not by a mixin on every
command.

### 4.6 One clock for everyone

The clock runs continuously at **15 game-minutes per real minute**, the same for everyone; no player
can stall it or yank it forward for the others (DR-14; Andrew, 2026-09-17). A long action occupies its
actor while the shared clock keeps running for everybody — long actions never skip time for other
people (GDD §9.1). Two players acting at once is safe by construction: Evennia's single-threaded
reactor serializes commands, so shared-object mutation cannot race (DR-22).

- **Fast forward** (Andrew, 2026-09-17, 2026-09-27). Proposed and agreed by the players, it runs the
  clock at about **150×**. Awake players can stay in it, seeing events go by faster, and type a
  command to slow it when they want to act. A player waking, or any event that is not ambient, drops
  it back to 15×; ambient events do not. A player who does not agree keeps the normal pace for
  everyone. Being awake is being on watch, and sleeping players can chat out of character to pass the
  time (document [06](06-time-sleep-and-the-clock.md)).
- **An agent acts at the speed of typing its command** (Andrew, 2026-09-26, 2026-09-27): a command
  reaches the world no sooner than an average typist could have typed it, and a slow model is
  simply slow — the clock never waits for it. An agent agrees to a
  fast forward or does not, like anyone. The average
  typist manages about 52 words a minute (Dhakal et al., CHI 2018, 168,000 typists) — some seven real
  seconds for `cut cover off seat with shard`, nearly two game-minutes at the normal pace. Every
  physical act takes its honest game duration and occupies its actor (one activity per actor,
  document 06), so a fast model does no more work per game-minute than a person; the typing pace takes
  away only reaction, the one advantage no person can match. **Agents playing alone run at the models' speed** (Andrew, 2026-09-28): a run with no humans in it does not wait on world speed or typing speed — it goes as fast or as slow as the models work, so more runs get in. *(Proposed by Claude, for Andrew's check:)* the clock in such a run is driven logically: every act still takes its honest game time, and each command is charged the game time an average typist would have taken to type it, so the same moves make the same game whether the model is fast or slow, and a run replays exactly. In an agent-only run the typing charge is what gives
  every step an honest cost on the clock.
- **Pausing** (Andrew, 2026-09-17, 2026-09-27, 2026-09-28). The players can pause the run and return to
  it later. **The run pauses when someone in the party types `pause game`** — it does not pause
  by itself when players leave. The clock stops because the run is paused, which is not a hole in the
  running clock. The command is `pause game`, not `pause` — pausing is also something a person might do
  in the world (2026-09-28). When someone leaves, the out-of-character chat says so and offers the command:
  *"Mara disconnected — type `pause game` to pause it if you want."* **If everyone disconnects, the
  run pauses itself**, so nobody comes back to a party gone catatonic (2026-09-28).
- **A missing player** (Andrew, 2026-09-27). If a player is missing, their character goes catatonic:
  sits down and stares off. The party is warned (2026-09-17). The others can keep the character alive
  if they want, and it can die. The body is in the world
  like anyone's — core and extremity heat, wetness, hunger, thirst and wounds keep changing by the same
  systems — so the party can carry them in, cover them, huddle with them and feed them, and the player
  returns to whatever state the body is in.

### 4.7 Interdependence

Co-op needs **first-class interdependence** — acts that genuinely *require* two people, so co-op is a
shared story rather than parallel solitaire (GDD §16). The roadmap's P6 exit gate is an interdependence
that genuinely requires cooperation — a real gate, not a checkbox. The sources name three:

- **The antenna hold.** One survivor holds the improvised antenna up high while another works the
  radio; the signal is better the higher the antenna goes (document 14 §3.2), so "held up, out there,
  in this wind" is a real term, not a scripted two-player prompt.
- **The landmark relay.** A scout who can see a landmark relays it to the person at the radio — the
  landmarks the voice on the other end asks for (document 14 §3.3).
- **The carry** of an injured survivor.

They are the positive end of the moral layer's axis, not a separate system: the same witnessing and
logging that make betrayal legible make the hold and the relay legible (document
[15](15-moral-and-social-layer.md)).

**The mechanism** (2026-09-28). Interdependence is what the physics
gives when an act's needs exceed one body, so it is built once, as a general rule, and every real case
follows from it. An operation's needs — a capability at a level (`heft`, `leverage`), a free hand, a
body's heat, a position, a line of sight — are met by **what the actors present bring together, read
from each one's concurrent state**; and because an activity's progress lives on the world (document
06), two people can work one job. What that makes real, from how the things actually work:

- **the antenna held up high** outside while another works the radio in the cockpit — aircraft VHF is
  line of sight, so height is range;
- **the landmark relayed** from where it can be seen to the person at the radio, by the speech and
  sight ranges above;
- **the carry** of someone who cannot walk — an adult is more than one person can carry over rough
  ground for any distance;
- **the huddle** — another body's heat is by definition another person (document 08); this one
  *genuinely requires* two, which is the P6 gate met by physics;
- holding the light while another works; hauling someone out through the ice; lifting what one person
  cannot shift; two people spinning one fire drill — and whatever else the loops find. Nothing that one
  person can really do is made to need two (2026-09-28): a log can be cut alone.

Here a little hint in the world's voice is right (2026-09-28): *"It's too heavy for one person to
lift."* The antenna has more to it, as the other systems do — held higher, it hears and is heard
farther, if the party thinks to do it (document 14 §3.2).

None of these is a two-player script, and almost none is the only way: a person alone can lash the
antenna to a pole or drag a travois — every goal has several ways — so cooperation is usually the
better answer rather than the only one, which is what keeps a party of one a real run. Which is built
first is ordering: `PLAN.md` E13 names the antenna hold; the huddle arrives with warmth, earlier in the
build order (document 06).

### 4.8 Talking out of character, and what is not here

- **The out-of-character chat** (Andrew, 2026-09-17, 2026-09-27). Anyone, living or dead, can use it;
  sleeping players chat in it to pass the time. Ghosts hear one another, and the living do not hear
  ghosts (document [21](21-endings.md) §4.5). Speech in the world keeps its physical range
  (§4.4). Evennia's stock channel typeclass is in the scaffold
  ([`game/typeclasses/channels.py`](../../game/typeclasses/channels.py)).
- **No shared status readout of other players** (2026-09-28). You learn how your friend is doing by
  looking at them, being told, or watching them fail. This follows from never-a-menu — a status panel
  is a list of facts nobody perceived.
- **The lobby** (Andrew, 2026-09-28, 2026-09-29): once a player dies or is rescued they are transported to the lobby — a room inside the simulation, not a physical room of the institute. Players there talk to each other in the room itself, so they can talk about the rescue without the out-of-character chat. It has a door that opens into the simulation: through it they move around the world at a quick speed, not the slow pace of the living, watching as ghosts do — seeing everyone, acting on nothing, heard only by other ghosts. (document 21 §4.5).
- **No mode switch** (Andrew, 2026-09-16). The engine does not know whether it is running a friends
  run or a research run: the same rules in all three modes.

---

## 5. Interactions

**This depends on:**

- [06 — time, sleep and the clock](06-time-sleep-and-the-clock.md): the running clock, the fast
  forward, the watch; every multiplayer property above is downstream of it.
- [01 — premise and world](01-premise-and-world.md): the zone map and the valley's edges — which
  zones can see or hear which is authored geography.
- [03 — the player view](03-the-player-view.md): the look is what perception renders; *who is here*
  is a perception answer, not a room roster.
- [13 — events, escalation and weather](13-events-escalation-and-weather.md): weather band-steps are
  the one live input to perception that is still stubbed.
- [14 — rescue](14-rescue-paths.md): the antenna hold and the landmark relay are rescue content.
- [16 — players and kit](16-players-and-kit.md): the seats, and what an unplayed seat's dead
  character carries.

**These depend on this:**

- [20 — the agent player and research](20-the-agent-player-and-research.md): mixed and agent-only
  runs are instances; "the same view as a human" is this document's perception.
- [15 — the moral and social layer](15-moral-and-social-layer.md): every act in the zone is seen by
  everyone there; `steal` is the one covert act; beyond the zone, witnessing is by band.
- [21 — endings](21-endings.md): an ending is a run's ending; the ghosts and the
  out-of-character chat.
- [12 — the pilot and bodies](12-the-pilot-and-bodies.md): who could see what was done to the pilot's
  body, by band.
- [08 — warmth, clothing and shelter](08-warmth-clothing-and-shelter.md): the huddle is an
  interdependence (§4.7). [11 — injury and first aid](11-injury-and-first-aid.md): the carry, and
  tending a catatonic or injured survivor (§4.6).
- [23 — flora and fauna](23-flora-and-fauna.md): the acting animals perceive and are perceived by
  band; scent is a channel still to be designed (§4.4).

---

## 6. Open questions

None open.

---

## 7. Review log

- **2026-09-17 (Andrew):** a run is one sitting, paused and resumed, not an ongoing world; the party
  is warned when a member is missing; ghosts; agents may play non-human characters.
- **2026-09-26 (Andrew):** in a run with humans a slow model is simply slow; the bear, some bigger
  animals and a few birds act.
- **2026-09-26 (Claude, self-review):** answered for Andrew's check — interdependence as one general
  rule (§4.7); a paused run is never reaped (§4.1); the last player out pauses the run (§4.6); the
  acting animals perceive by band, and scent is a channel to design (§4.4).
- **2026-09-27 (Andrew):** up to five play; an unplayed seat is a dead character whose clothes can be
  searched; agents may play seats; the pace is the speed of typing the command; a missing player's
  character goes catatonic, the others can keep it alive, and it can die; ghosts hear ghosts, the
  living cannot, and anyone can use the out-of-character chat.
- **2026-09-27** — the no-storm week carried in (document 13 §4.2).
- **2026-09-28 (Andrew, the document's sitting):** a run as its own copy of the world, its machinery for
  the implementation plan; the run pauses when someone types `pause game`, and by itself only if
  everyone disconnects; sight works within a Scene, and going to another is a journey with an estimate,
  emotes, things passed, and a stop between two Scenes; four levels of talk with synonyms; the typing
  pace and a missing player's body; working together as one general rule, never making two people
  needed for what one can do, with a small hint when something is too heavy for one. **Reviewed in
  full.**

## 8. What exists today

**Built.**

- The perception layer, shipped: [`game/world/sim/space/`](../../game/world/sim/space/) —
  `zones.py` (the zone graph, `walk`/`see`/`muffle` edges, loaded-once scenario content),
  `perception.py` (the see-edge hop banding and the weather band-step parameter), `sound.py` (speech
  loudness → reach in hops; muffle cost; the same-zone clamp), `direction.py` (bearing plus elevation
  → the compass phrase), `spaces.py`.
- The bands and the perception result are contracts in
  [`game/world/sim/contracts.py`](../../game/world/sim/contracts.py).
- The message propagator: [`game/typeclasses/propagator.py`](../../game/typeclasses/propagator.py),
  driven from [`game/typeclasses/heartbeat.py`](../../game/typeclasses/heartbeat.py); no game output
  bypasses it (a lint enforces it).
- Speech by range: [`game/commands/cmd_speech.py`](../../game/commands/cmd_speech.py), using the pure
  loudness table.
- The reach gate and the "too far to {verb} from here" answer in the resolver, plus the item-command
  pre-flight and the per-observer appearance hook.
- Zone state through the single writer: the `MOVE_ZONE` branch of
  [`game/typeclasses/apply.py`](../../game/typeclasses/apply.py), with the zone tag mirror.
- A **single** run tag: objects are built carrying `("slice", "run_id")`
  ([`game/world/scenarios/whiteout/build.py`](../../game/world/scenarios/whiteout/build.py)) and the
  heartbeat finds its rooms by that tag. This is the seam for instancing — one hard-coded run, not a
  lifecycle.

**Designed, not built.** The instance lifecycle (create / persist / reset / GC) — DR-15 and roadmap
P6. The seats and the dead characters in unplayed ones. Pausing, the catatonic missing player, and the
typing pace. Ghosts and their hearing. Co-op interdependence — the mechanism is proposed (§4.7), no
content exists. Concurrent-action handling on the shared clock beyond what the reactor gives for free.

**Nothing.** No instancing code, no reaper Script, no run creation or teardown, no multi-run support
of any kind. No interdependence content anywhere in `game/`. The weather input to perception is a
stubbed `"clear"` at every call site — the band-steps in §4.4 are implemented but never exercised by
real weather. Movement is single-hop and instant; durations are plumbed but unused. Muffle edges are
implemented and tested but the crash-site map authors none, so no sound is damped anywhere in the
world yet.
