# Probe 1 — paper / Wizard-of-Oz playtest of the first 30 minutes

**Goal:** calibrate **FUN (Q2)** by hand-simulating the opening of a run from the design + proposal —
me playing engine + narrator, a plausible 2-player party acting — then auditing where it's *tension*
vs *tedium* (GD2, GD4, GD10, GD18). This is a thought-experiment, not a verdict; it surfaces felt
problems a spec read misses.

Players: **Mara** (rear cabin), **Andrew** (front, near the pilot). Single instanced run, ~1 in-game
day. Transcript is illustrative — what the engine *should* produce.

---

## Minute 0–3 — wake, orient (the Toy test, GD2)
```
> look
You're strapped into a window seat in the rear of a broken cabin. Snow ticks against a
cracked pane above you. The belt is stiff with frost across your lap. An overhead bin hangs
open, spilling a torn backpack. Across the aisle, Mara slumps in her harness, not yet moving.
> unbuckle
Your fingers are clumsy with cold. The frozen latch resists, then gives. You're free.
> lick the latch
Cold. Bad idea — your tongue stings and nearly sticks. You pull back. (Lesson learned, cheaply.)
> wear the seat cover
You can't wear it while it's stitched to the seat. You could cut or tear it loose first.
```
**Audit:** This is the make-or-break. Three pokes (unbuckle / lick / wear) each got a *physical,
slightly witty* answer — that's the Toy working (GD2 GREEN *if* the responses are this good). The
"lick the latch" beat is the whole game's voice (GD25). **Risk:** if any of these returned "You can't
do that" or a flat "Nothing happens," the magic dies instantly. The opening 60 seconds must be
hand-polished, not generated. **Finding: the first-3-minutes responses are the single highest-ROI
content in the game and must be authored/curated, not left to generic derivation.**

## Minute 3–8 — the pilot, the first real choice (GD7)
```
> go forward
You climb over a collapsed seat frame into the front cabin. The pilot is slumped at the
cockpit threshold, breathing wet and shallow. A trickle of blood has frozen on his temple.
> talk to pilot
His eyes flutter. "...north... we were north of the route..." Then his head rolls aside.
> search pilot     (Andrew's choice: tend, question, or loot?)
```
**Audit:** The tend-vs-question-vs-loot fork (design §19) is a genuine meaningful choice (GD7 GREEN)
**only if** the three options have real, different payoffs and the pilot's lucidity is a depleting
resource the player can *feel* spending. **Risk (GD7→YELLOW):** if "tend" is always strictly best
(more clues, no downside), the choice collapses. Needs a real cost to tending (time, exposure while
you kneel in the wind) to make loot/question viable. **Finding: the pilot needs an explicit
opportunity cost on tending, or the choice is dominant-strategy fake.**

## Minute 8–18 — first fire / first long task (the tedium test, GD4/GD18)
```
> cut the seatbelt with the multitool
You saw at the frozen webbing. The nylon resists; your cold hands slow you.
  ...a few fibers part. (2 / 11 min)
> [Mara, meanwhile] gather shavings from the torn backpack lining
...
```
**Audit:** Here is the **tedium cliff**. An 11-minute saw task: with the proposal's **event-driven
clock**, the world doesn't drain while Mara also acts, and the task isn't 11 real minutes — but the
*player* still issues "continue" a few times and reads near-identical tick text. **Two concrete
saves needed:** (1) tick messages must **escalate stakes**, not count ("the wind kicks up; your
fingers won't fully close — keep going?"), and (2) **action-chunking** (Hadean Lands lesson): once
you've sawed webbing successfully, future identical cuts collapse to one command with a single
resolved result. **Without both, this minute-range is where players bounce (GD4 → YELLOW/high).**
Co-op helps (GD16): Mara prepping tinder while Andrew saws is a *shared* rhythm, not parallel
solitaire — but only if the game shows them each other's progress (perception routing).

## Minute 18–30 — fire catches, weather turns (interest curve, GD10)
```
The shavings catch. A thread of flame climbs, then gutters in a draft from the cracked pane.
> hold the seat cover up to block the draft
You hold it between the wind and the flame. It helps for a moment, then snaps sideways and
nearly smothers the fire. Stretched over the seat backs it might work as a screen.
Andrew (to the south): "Got a flame — losing it to the wind!"
[The snow thickens. Visibility drops. Somewhere outside, a low drone — a plane? — fades.]
```
**Audit:** Strong beat. The shirt/cover-windbreak failure is the design's signature moment (GD25),
the weather turn raises the curve (GD10 GREEN), and the **distant unseen plane** is exactly the
mid-run re-spike the brainstorm called for. The cross-zone shout ("losing it to the wind") is a
cooperation/perception payoff (GD16). **Risk:** the interest curve depends on these scripted-ish
beats landing on time; emergent play could miss them. **Finding: seed 2–3 timed "beats" (the
distant plane, the pilot's last lucid line) so the curve doesn't sag if players wander.**

---

## Calibration result (for the certainty doc)
- **Where the fun clearly is (high confidence):** the Toy opening, the resolution-not-success
  failures, the windbreak moment, the weather/plane beats, co-op fire-building. The *voice* is
  delightful **if** the responses are well-authored.
- **Where the fun is at risk (the two cliffs):**
  1. **The long-task tedium cliff (min 8–18).** Mitigated only if tick messages escalate stakes AND
     action-chunking ships. This is the #1 fun risk — **GD4, severity high.**
  2. **Dominant-strategy collapse of the pilot choice** unless tending has a real cost — **GD7,
     severity med.**
- **Dependency:** the opening minutes and the failure responses must be **hand-curated**, not
  generic-derived — quality of prose *is* the product here (GD13/GD25).
- **Estimated FUN confidence:** *conditional.* The design **can** be very fun (the beats are there),
  but fun is **not** guaranteed by the systems — it rests on (a) escalating tick feedback +
  action-chunking and (b) curated opening/failure prose. Without those two, the deep simulation reads
  as a chore. → feeds Q2 as "moderate confidence, conditional on two specific mitigations."
