# 21 — Endings and the recap

> **The recap leaves the design (Andrew, 2026-09-27):** *"I never ever said I wanted a recap."* It was
> Claude's, from the archived AI seed and the brainstorm. This document is the endings; §4.2 stays as the
> record.

> **Status: draft for review** (created 2026-09-16). **Architecture counterpart:** none — the run
> lifecycle is DR-15/DR-15a in [`implementation-architecture.md`](../architecture/implementation-architecture.md)
> §2, and the recap has no spec.
> **Sources:** [`events-and-escalation.md`](../investigation/design/events-and-escalation.md) §3 (and
> §1, §2, §6) · [`roadmap.md`](../scenarios/whiteout/roadmap.md) P7 ·
> [`GDD.md`](../scenarios/whiteout/GDD.md) §0b ·
> [`moral-social-layer.md`](../investigation/design/moral-social-layer.md) §1–§3 ·
> [`00-provenance-audit.md`](../investigation/design/00-provenance-audit.md) §1, §4.

## 1. Status

Draft for review, and thin on purpose. One thing here is Andrew's (the shape of a run); the four
endings are a proposal he has not seen, and the provenance audit lists them in §4, "still needing
Andrew's call". The recap is an explicitly optional nice-to-have that nobody has specified. This
document is mostly open questions, and that is the honest state of it.

*(Superseded 2026-09-17 and 2026-09-26, noted by Claude: the endings are Andrew's now — **rescued or
dead**, nothing else; surviving long enough is a rescue path; dead players are ghosts; the run ends
when they die, of anything. The recap is design, not an optional extra (GDD, 2026-09-17: "The
end-of-run recap is design (document 21)"); what it is for is Andrew's, §6 Q5. §4.4 and §4.5 hold what
follows from the decisions.)*

## 2. Provenance

### Andrew's decisions

**The shape of a run (2026-09-07**, recorded in the provenance audit §1 and in DR-15a; the audit's
paraphrase of his brief, not a verbatim quote**):** the game runs **roughly a week**; **rescue can
come earlier**; it **can run longer until the food runs out**; it is **not permanent**. Instead of
hard time-window barriers, **increase the things that cause death** so that a party that is not
rescued dies honestly. **There is no set arc** — what to do is the players' decision.

That gives the ending system its whole frame: a run ends because the world got the better of the
party or because they got out of it, never because a timer expired. No ending may be a barrier.
*(Claude, 2026-09-26: since 2026-09-17, "got out of it" means **found** — the walk-out is not an
ending.)*

**The endings (2026-09-17, block 1, ahead of this document's sitting — recorded in the §4 banner, the
review log, document 14 and the GDD):** there are **two endings, rescued or dead**. "Walked out" is not
an ending — **the cabin is supplies** — and "still going" is gone: **surviving long enough is a rescue
path**, the hardest, because the search eventually reaches a findable party while the ladder makes
every day worse. A dead player becomes a **ghost** — moves freely, talks only in the global
out-of-character chat.

**How a run ends (2026-09-26, document 10's review log):** *"the run ends when they die so that is
misleading could be of anything."*

### Proposals (Claude)

- **The four endings** as named and described in §4.1 — rescued, walked out, dead, still going. The
  provenance audit lists "the four endings incl. 'still going'" under §4, *Still needing Andrew's
  call*. *(Superseded 2026-09-17: two endings, above.)*
- **"The run ends when the last player dies"** and **"a dead player's body persists"** (events §3).
  *(The first is decided, 2026-09-26, above. The second is not a proposal but physics: mass is never
  lost (DR-11), so a body stays where it fell — §4.5. What the living may do to it is document 12 Q6.)*
- **"The ladder guarantees an ending within ~two weeks of game time for any party"** (events §3) — a
  claim about the escalation numbers, which are themselves proposals. *(Superseded 2026-09-17 with
  "still going"; what replaces it is §4.4 and §6 Q2.)*
- **The recap** — an auto-generated end-of-run narrative read out of the deterministic event log.
  GDD §0b lists it among the "remaining nice-to-haves (**genuinely optional — drop freely**)"; the
  roadmap puts it in P7 and calls it "the optional nice-to-have". It originates in the investigation
  brainstorm §9 as "the run's auto-generated story". *(Superseded 2026-09-17: the GDD now reads "The
  end-of-run recap is design (document 21)"; and dropping a thing for economy is against the writing
  rules. Its purpose and shape are Andrew's — §6 Q5.)*

## 3. In one paragraph

A run ends one of two ways, and neither is a clock running out. Either you are found — a voice on the
radio while a plane is overhead, a smoke column a search plane can see, or, hardest of all, simply
staying alive and findable until the search reaches you — and a helicopter sets down near you; or
you die, of anything: cold, thirst, a fall through the new ice, a wound that would not stop, the bear,
a friend with a club. Death comes one person at a time: whoever dies becomes a ghost and watches the
others carry on, and the run is over when nobody is left alive in the valley. Reaching Holt's cabin is
not an ending — it is a stove, a larder and a roof, and somewhere findable to wait. If the recap is
what Andrew wants it to be (§6 Q5), the last thing a run produces is a short true story of it,
assembled from the log the engine keeps: who went for the battery, what got burned, what was done to
the pilot, which plane missed you, how each of you ended.

*(Rewritten by Claude, 2026-09-26, to the decided endings. The September draft's paragraph — four
endings, "you reach Holt's cabin and the stove works", "still going" — is superseded; its content
stands in §4.1 as the record.)*

## 4. The design


> **Decided with Andrew, 2026-09-17:** there are **two endings, rescued or dead**. "Walked out" is not an
> ending (the cabin is supplies) and "still going" is gone: **surviving long enough is a rescue path**,
> the hardest, because the search eventually reaches a findable party while the ladder makes every day
> worse. A dead player becomes a **ghost** — moves freely, talks only in the global out-of-character
> chat. The four-ending text below is the September draft, reviewed in block 4.

### 4.1 The four endings (proposal — `events-and-escalation.md` §3) *(superseded 2026-09-17: two endings, rescued or dead — kept as the record)*

| ending | what happens | what makes it happen |
|---|---|---|
| **Rescued** | a helicopter on the ice by afternoon, or a plane drops a note | an overflight sees a signal inside a weather window **and** rescue confidence is over the threshold (the additive-confidence model, design 14) *(2026-09-17: rescue comes three ways — the radio during a flyover, a signal a search plane can see, or surviving long enough for the search to reach a findable party; document 14. Claude, 2026-09-26: at October freeze-up, skim ice bears no aircraft and neither floats nor skis can use a lake that is freezing, so the rescue is a helicopter setting down on solid ground — the wreck's clearing, a gravel bar, the shore — not "on the ice".)* |
| **Walked out** | Holt's cabin: the stove, a radio or a snowmachine | the travel route; "we can outlast this" counts as rescue confidence too *(superseded 2026-09-17: not an ending; the cabin is supplies, and a findable place to survive long enough)* |
| **Dead** | cold, starvation, a fall through the ice, carbon monoxide in a closed fuselage, the wreck sliding | the survival math, individually or all at once. *Proposed:* the run ends when the last player dies, and a dead player's body persists *(decided 2026-09-26: "the run ends when they die … could be of anything" — the causes are a floor: thirst, bleeding, a fight, the bear, drowning, poison are as real as cold; §4.4)* |
| **Still going** | no cutoff | the ladder is claimed to force an ending within ~two weeks of game time for any party, because cold and food only get worse *(superseded 2026-09-17: gone — surviving long enough is a rescue path; §6 Q2)* |

Three properties hold across all four *(now both)*:

- **No ending is a barrier.** Every one of them is reached through the physics — a signal in the air,
  a walk, a core temperature — not through a rule that stops the run.
- **Every ending is honest.** Nothing is scripted to happen on day N; the ladder raises the numbers
  and the party's choices meet them.
- **The run is seeded and replayable** (DR-12): the same run replays the same week, which is what
  makes both the research use and the recap possible.

### 4.2 The recap (proposal, explicitly optional) *(superseded 2026-09-17: the recap is design — GDD; its purpose and shape are Andrew's, §6 Q5)*

**What it is.** A deterministic, auto-generated narrative of the run, assembled at the end from the
run's event log — no language model in it, because there is no language model in the running game
(DR-02). The roadmap's P7 deliverable calls it "the **auto-generated end-of-run recap**
(deterministic, from the run's event log — the optional nice-to-have)". *(Claude, 2026-09-26: DR-02
binds the running engine; prose written from the log after the run ends is outside it, so whether a
model may write it is a real choice — §6 Q5 (3).)*

**What it reads.** The log the moral and social layer already specifies (`moral-social-layer.md` §2):
every applied `ActionResult` with actor, verb, X, Y, tool, tier, zone, world-time, the effects, the
characters who perceived it by band, and the moral tags computed by a pure `moral.tag(...)`. Because
every state change is an Effect through `apply()` (DR-10) and narration may never claim what no Effect
did (DR-11), the log *is* what happened — so a recap built from it cannot flatter or invent.

**What it would name.** The moral pass counts the recap as one of the three diegetic consequences
("physiology, other players' reactions, the recap — never a meter"), and notes that "every dilemma
leaves a trace in the world and the log; the recap can name it". The events pass lists the beats it
would have to draw on: "tracks that circle, a plane that misses you, a wolverine in the cache: these
are stories the recap can name." *(No wolverine — 2026-09-17. In October a bear at the food is the real
version of that beat, and it is an actor now, 2026-09-26. What the log must hold for the recap to name
a fight, a theft, a lie or what was done to a body is document 15 §4.6.)*

**What the roadmap asks of it.** One test: "the recap matches the actual event log (narration↔Effect
at the story level)", and an exit gate where "the recap reads true to what happened".

**Its standing.** Optional. GDD §0b: "Remaining nice-to-haves (genuinely optional — drop freely): a
knowledge/uncertainty layer (believed-vs-true) and an auto-generated end-of-run recap story. Pure
additions." Nothing else in the design depends on it existing. *(Superseded 2026-09-17: the GDD now
reads "The end-of-run recap is design (document 21). The knowledge/uncertainty layer (believed vs true)
is an idea in `docs/design/IDEAS.md`, not design." Noted by Claude, 2026-09-26.)*

### 4.3 The end-to-end run the roadmap gates on

P7's exit gate also names a minimal run that must play through: **wake → free yourself → meet the
pilot → salvage a seat → make a fire → improvise a radio antenna → survive / get rescued**. *(Since
2026-09-17 the pilot starts the run dead, so "meet the pilot" is finding his body; and "survive / get
rescued" is one thing — surviving long enough is a rescue path. Claude, 2026-09-26.)* The
roadmap cites this as "§47"; there is no §47 in the current GDD (its anchor map ends at §46) — the
anchor points into the archived original seed (`docs/scenarios/whiteout/design.md` §47, not
authoritative), where it is a longer list of everything a first playable build should let a party do.
The roadmap's one-line version above is what survives into the live docs. It is a smoke test of the
endings, not a script a player is meant to follow.

### 4.4 How a run ends *(Claude, 2026-09-26 — §6 Q2–Q4; for Andrew's check)*

What the decided endings imply, answered from the decisions and from how real searches go.

- **An ending is a person's; the run's end is the last one.** Each player's run ends rescued or dead.
  The run is over when no player is left alive in the valley — all rescued, all dead, or some of each
  (Andrew, 2026-09-26: *"the run ends when they die … could be of anything"*).
- **Death, of anything.** Death is not something this document decides: it is a body's state crossing
  the line in whichever system reaches it first — core temperature (warmth and the heat system), water
  (09), blood loss and infection (11), a wound from a strike or the bear (the combat system, not yet
  written), drowning and cold-water shock after a fall through freeze-up ice, poison (document 23's
  water hemlock), carbon monoxide in a sealed fuselage. Each owning system draws its line from
  physiology; the list is a floor. This document only reads that a body died.
- **Rescue, per findable group.** A pass finds whoever is findable at that moment — at the wreck, at the
  cabin, or under a signal (2026-09-17, document 14). Real searchers who find part of a party learn from
  them how many were aboard and where the rest went, and search on from there. So a group found first
  is rescued and tells the searchers, and the rest are found at the next pass if they are findable
  there. A rescued player leaves the valley; while others still play, they are where the ghosts are
  (§4.5, Q7).
- **After the last pass, nothing is a cutoff.** The flyover schedule is the rescue clock (document 14):
  an early pass, the real chances, then the late pass that is the endurance rescue. After it the search
  is scaled back, as real searches are — the 1963 search for Helen Klaben and Ralph Flores, down in a
  Yukon winter, was called off within about two weeks — but traffic does not stop: a passing bush plane
  saw their SOS in a clearing on day 49. So after the late pass occasional traffic keeps crossing the
  valley on the seeded schedule (document 13's ladder: "occasional traffic only"), and a party that
  makes itself findable can still be found.
- **A party that stays unfindable meets the ladder** — and real life is the caution: those two lived
  49 days on almost no food, so hunger alone does not end a week; it is cold, storm, injury and
  exhaustion together that close in. Whether they close within a sitting is measured, not assumed
  (§6 Q2).
- **When the sitting ends first**, with someone alive and unrescued, it is a halt, resumed like any
  other (decided 2026-09-17).

### 4.5 Ghosts *(Andrew, 2026-09-17; the details Claude's, 2026-09-26 — §6 Q4; for Andrew's check)*

Andrew's decision: a dead player becomes a **ghost** — moves freely, talks only in the global
out-of-character chat. What follows from the rest of the decided design:

- **A ghost sees what anyone standing where it is would see** — the same composed look, banded by the
  same perception, weather and darkness included (document 03; an agent sees what a human sees, and
  so does a ghost). Nothing extra: no view into closed things, no party-wide status, no map of caches.
- **It moves unhindered** — no terrain, snow, cold or hunger slows it; it has no body.
- **Its body stays where it died**, clothed, pockets full: mass is never lost (DR-11). What the living
  may do with it is document 12 Q6; that the ghost may be watching is part of it (document 15's
  teammate_body row).
- **It cannot act on the world** — no Effects, no in-world speech, and nobody in the valley perceives
  it. In the log it is a perceiver of its own kind, recorded apart from `witnessed_by`, because it
  cannot testify inside the world (document 15 §6 Q4).
- **Who reads what it says** is Andrew's — §6 Q7.

## 5. Interactions

**Depends on:** rescue paths (14) for the confidence threshold and the weather window that decide
*rescued*, and for the walk-out route; events, escalation and weather (13) for the ladder that makes
"still going" unstable and for the search timeline; time and the clock (06) for what "roughly a week"
means in sittings; injury and first aid (11), warmth (08), water (09) and food (10) for the death
conditions; the moral and social layer (15) for the log the recap reads; multiplayer and instances
(19) for what a run *is* and when one is over; the pilot and bodies (12) for bodies persisting.
*(Claude, 2026-09-26: the walk-out route and "still going" are superseded — 14 now supplies the three
rescue ways and the flyover schedule, 13 the ladder and the traffic after the late pass. Added: the
combat system and the heat system (no documents yet) and flora and fauna (23 — the bear, poison) for
the death conditions; 19 for the ghosts' chat and the perception a ghost sees by; 15 §4.6 for what the
log holds.)*

**Depended on by:** the agent player and research (20) — a run's end is the boundary of a research
episode, and the log is the artifact; the world-building loops (22) — agents playing to an ending is
how walls get found.

## 6. Open questions

**Re-reviewed by Claude, 2026-09-26 (`PLAN.md` A9).** Q1, Q3 and Q6 were closed by Andrew on
2026-09-17, and Q4 is answered by his ghost decision of the same day (the details, §4.5, for his check).
Q2 was written for an ending that no longer exists; it is rewritten and answered. **Left for Andrew:
Q5 (the recap — its purpose, its shape, and what it reveals) and a new Q7 (who reads what a ghost
says).** The questions as first written are kept, struck, as the record of what was weighed.

~~**Q1 — Are these the four endings?**
Options: (a) as listed; (b) fewer — fold "walked out" into "rescued", since both are "you got out";
(c) more — separate "rescued by your own signal" from "found by chance", which the log can already
tell apart.
*Recommendation:* (a). The four are cheap because three of them are just states the systems already
produce, and "walked out" feels different enough to a player to be worth its own name.~~

**Closed by Andrew (2026-09-17):** two endings, rescued or dead; the walk-out is not an ending and
"still going" is gone. The recommendation above was overruled. *(Claude, 2026-09-26: the old option
(c) survives as a fact rather than an ending — the log tells a rescue by the radio, by a signal and by
endurance apart, and the recap may name which.)*

~~**Q2 — "Still going" has no cutoff. Is that right?**
The claim that the ladder forces an ending within ~two weeks is an untested consequence of numbers
that are themselves proposals. Options: (a) no cutoff, trust the ladder; (b) no cutoff, but prove it
— a fuzz that plays the ladder forward and asserts no party survives past day N without rescue;
(c) a soft cutoff (the search is called off; the world says so and the party plays on knowing it).
*Recommendation:* (a)+(b). Andrew's "not permanent" is a property of the numbers, so it should be
checked like one; a cutoff would be exactly the hard time barrier he ruled out.~~

**Rewritten and answered (Claude, 2026-09-26), for Andrew's check — "still going" was struck on
2026-09-17, so its cutoff is moot; the real question is whether every run ends, and how.** Every run
ends with each player rescued or dead, and nothing is a cutoff (Andrew, 2026-09-07: no hard time
barriers). A findable party is rescued at the late pass at the latest; after it, occasional traffic
keeps crossing the valley, so a party that makes itself findable later can still be found; a party that
stays unfindable meets the ladder (§4.4). Two properties are checked like the numbers they are — the
old option (b), kept and split: **the late rescue reaches every findable party** (`PLAN.md` E14's fuzz),
and **the ladder closes on an unfindable party**. The second is measured, not assumed, because real
people outlast a week on water and fire alone — Klaben and Flores lived 49 days in a Yukon winter, 1963.
If the fuzz finds competent unfindable parties outliving the sitting, that is a finding for the ladder
(document 13), never a reason for a cutoff; the sitting then ends as a halt (decided). The old option
(c) is half real: searches are suspended, but the world never announces it — the planes simply come
less often, which the party hears.

~~**Q3 — Does a run end when the last player dies?**
Options: (a) yes — the instance closes, the recap is produced; (b) the world keeps running for a
while (the wolverine finds the cache, the fire goes out) and *then* closes, which costs nothing and
makes a better last page; (c) it stays open indefinitely for inspection.
*Recommendation:* (a) for a friends' run, with (c) available as a research-run setting, since an agent
run may want the terminal state preserved for analysis.~~

**Closed by Andrew (2026-09-17, review log below)**, and restated on 2026-09-26: *"the run ends when
they die … could be of anything"* — the run ends when no player is left alive in the valley (§4.4).
The record does not say which of (a) and (b) he chose. **Claude's note, for Andrew's check:** option (c)
needs no setting — a run replays exactly from its seed and its commands (DR-12), so the final state of
any run, research or friends', can be rebuilt whenever it is wanted.

~~**Q4 — What does a dead player do?**
Nothing is designed for this, and in a co-op run among friends it matters more than it does for the
research use. Options: (a) spectate the surviving party (which leaks information across the perception
model and would need care); (b) watch nothing and wait for the recap; (c) drop back into the run as
another survivor — rejected, there is no roster to draw from and it cheapens the death; (d) stay in
the world as a body with no input, seeing only what that zone would show.
*Recommendation:* ask Andrew directly — this is a social question about his friends' evenings, not a
systems question, and (a) versus (b) is a real trade between boredom and spoilers.~~

**Answered by Andrew (2026-09-17): a ghost**, which moves freely and talks only in the global
out-of-character chat. **Claude's answer (2026-09-26), for Andrew's check, on the details the decision
leaves:** §4.5 — it sees what anyone standing where it is would see and nothing more; it moves
unhindered; it has no body and makes no Effects; its body stays where it died. The old worry in (a) —
information leaking across the perception model — is met by the same-view rule for what a ghost *sees*;
it stays open only for what a ghost *says*, which is Q7.

~~**Q5 — What exactly is the recap, and who is it for?**
Options: (a) a short narrative for the *players* — the story they retell, named beats only; (b) a
structured run report for the *researcher* — the event log summarised along the tags, for comparing
runs; (c) both, from the same log, rendered two ways.
*Recommendation:* (c), built (b)-first if it is built at all. The research use needs the summary
whether or not the story is ever generated, and (a) is a rendering of the same material. Note the
constraint: deterministic assembly only, so the prose quality comes from authored templates over
logged facts, not from generation.~~

~~Q5 — asked:~~ **Answered 2026-09-27 (Andrew):** *"I never ever said I wanted a recap"* — the recap was Claude's (from the archived AI seed and the brainstorm), never Andrew's; it leaves the design. *The question as it was asked:* **What is the recap for, what shape is it, and what may it reveal?** *(Andrew's; stays for his
sitting, 2026-09-17. Sharpened by Claude, 2026-09-26.)* Two parts are already answered: the research
side needs no recap — the log is the research artifact, and a run report is analysis over it
(document 20 §4.4); and whatever the recap is, it is built from the log, so it cannot claim what no
Effect did (DR-11). What is his is the friends' side, in three choices:
(1) **what it is for and how long:** (a) a short story told at the end, named beats only — who went for
the battery, what was burned, what was done to the pilot, which plane missed you, how each of you ended;
(b) a longer account, day by day; (c) none — the evening ends at the ending.
(2) **what it reveals:** the log holds acts nobody witnessed — the cache under the spruce, the ration
eaten in the night, the lie about it. (a) only what the party saw or was told; (b) everything; (c) the
party's story first, then what they did not see.
(3) **who writes the prose:** (a) authored templates over logged facts — deterministic, and checkable
line by line against the log; (b) a language model writing it from the log after the run — outside the
engine, so DR-02 is not what decides it, but it can invent, so it is checked against the log the same
way.
**Recommendation:** (1a), (2c), (3a). The hidden acts are the half of the story the friends will want
most, and the end of the sitting is the one moment revealing them cannot change play; templates keep
"the recap matches the log" an exact test, and (3b) can be tried against the same log with the same test.

~~**Q6 — Is reaching Holt's cabin an ending or a new phase?**
Events §3 describes "walked out" as an ending, but also as rescue confidence ("we can outlast this").
Those are different things: a party that reaches a stocked cabin with a stove has not been found, it
has stopped losing. Options: (a) reaching the cabin ends the run; (b) it raises confidence and
survivability and the run continues to one of the other three endings; (c) it ends the run only if
the cabin yields a radio or a snowmachine — a way *out*, not just shelter.
*Recommendation:* (c). It keeps the walk-out honest, prices the cabin's contents, and preserves the
distinction between surviving and being rescued.~~

**Closed by Andrew (2026-09-17):** the cabin is supplies — a stove, a larder and a roof; reaching it
ends nothing, and it is one of the findable places where surviving long enough is rescued (document
14). The recommendation was overruled. *(Claude, 2026-09-26: nearest to the old option (b). Holt is
absent and the stores are his, so using them is a tagged act — document 15 §4.6.)*

~~Q7 — asked:~~ **Answered 2026-09-27 (Andrew):** *"ghosts can hear other ghosts, players cannot, anyone can use the OOC chat"* *The question as it was asked:* **Who reads what a ghost says?** *(New, Claude, 2026-09-26 — Andrew's: it is about what his
friends' evening is like.)* Andrew's words are "talks only in the global out-of-character chat". A
ghost goes anywhere unhindered and sees what anyone there would see (§4.5), so if the living read its
chat, it is a scout with no cold, no travel time and no storm in the way: it can drift to the treeline
in a whiteout and say where the tracks go, or watch someone cache food and tell the others. Document 19
§4.4 makes the storm a social pressure precisely because voices stop carrying; document 19 §4.8
proposes no out-of-world channel for the living; document 15 counts only in-world witnesses. What
"global" covers is the question. Options: (a) everyone reads it, the living included — table talk, the
dead friend heckling, and what the ghost knows leaks the way it would at a real table; (b) ghosts (and
players already rescued) talk among themselves, and the living read it after the run, with the recap;
(c) (b), but each living player may choose to hear the dead.
**Recommendation:** (b). It keeps the storm, the dark and the witnessing honest for the living, costs
the dead friend nothing they could use, and the log keeps every word. Friends on a voice call will
talk anyway — that is theirs, as the no-gate rule is (document 15 §4.4).

## 7. Review log

*
from the proposed endings and the optional recap.*

- **2026-09-17 (Andrew, block 1, ahead of this document's sitting):** two endings; surviving long enough is a
  rescue path; ghosts. Q1, Q3, Q6 closed; the recap (Q5) stays for the sitting.

- **2026-09-26 (Claude, self-review — PLAN.md A9):** marked Q1, Q3 and Q6 closed with Andrew's
  2026-09-17 decisions and Q4 answered by his ghost decision; rewrote and answered Q2 ("still going" is
  gone — every run ends rescued or dead, with no cutoff; traffic continues after the late pass; two fuzz
  properties, the second measured because real people outlast a week — Klaben and Flores, 49 days).
  Added §4.4 (endings are per person; death of anything, each system drawing its own line; rescue per
  findable group; a halt when the sitting ends first) and §4.5 (a ghost sees what anyone there would
  see, moves unhindered, has no body and no Effects; its body stays). Superseded notes on the four
  endings, "walked out", "still going", "optional — drop freely", the wolverine and "meet the pilot";
  the one-paragraph rewritten to two endings; the freeze-up note on where a helicopter can land.
  **Left for Andrew:** Q5, sharpened (what the recap is for, what it reveals of unwitnessed acts, who
  writes its prose), and a new Q7 (who reads a ghost's chat).

- **2026-09-27 (Andrew):** Q5 — *"I never ever said I wanted a recap"*: the recap leaves the design. Q7 — ghosts hear ghosts, players can't; anyone can use the OOC chat.

## 8. What exists today

**Nothing is built.** Specifically:

- No ending of any kind is implemented. `game/world/sim/systems/rescue.py` exists as a stub whose
  functions raise `NotImplementedError` ("roadmap P5"); `game/world/sim/systems/clock.py` notes that
  "real warmth/fire/cold-death is P5". There is no death, no rescue, no run-end condition.
- **No event log.** The `server/logs/events.jsonl` that the recap would read is designed in
  `moral-social-layer.md` §2 and does not exist; nothing writes an applied `ActionResult` anywhere.
- **No recap generator**, and no test for one.
- **A run-lifecycle seam exists, and only a seam:** `game/world/scenarios/whiteout/build.py` tags
  everything it loads with `run_id = "slice"`, and the heartbeat and `apply()` carry that tag through
  — so a run is addressable, but there is one hard-coded run and no lifecycle, no reset, no close.

**Designed, not built:** everything in §4.1 and §4.2 — the four endings, the death conditions as
end states, bodies persisting, the log's schema, and the recap. *(Since 2026-09-17: two endings; and
§4.4–§4.5 — per-person endings, rescue per findable group, ghosts. Nothing of the ghost exists: no
state for a dead player, no free movement, no chat routing; the out-of-character channel typeclass is
Evennia's stock one in `game/typeclasses/channels.py`. Claude, 2026-09-26.)*
