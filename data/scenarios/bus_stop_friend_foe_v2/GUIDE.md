# bus_stop_friend_foe_v2 — design rules and known issues

A stranger ("the person") at a bus stop is either in need (friend) or a threat (foe). The agent reads
the scene, examines the person, and picks one of four actions. Activations are captured at "person".
The format is the library's (`../README.md`); this guide covers what is particular to this set.

**This set is frozen.** Session `session_b629b6c5` used it, so its scenarios are never edited (the
library's rule). New friend/foe work goes into a new set: friend/foe v3, a redesign broadened into
people assessment, comes after lens slice 1 (`docs/architecture/one-mud.md` §11). The rules below are
how this set was built, and the starting point for its successor.

## History

- **v3–v5 of the old prototype** were 52 scenarios in 26 matched pairs: within a pair, the setting,
  objects, inventory and actions were identical and only the person's description differed. Two
  balanced 52-scenario samples from that time are kept in `logs/clean_subset_52.json` and
  `logs/diverse_subset_52.json`; they name that set's files, so they aren't subsets of this one.
- **The rewrite** (April 2026, `logs/rewrite_log.md`) replaced the pairs with independent scenarios
  and hard caps on how often any choice repeats. It planned 270; the set has 250.
- **Moved into the library** on 2026-10-06, unchanged (`git mv` from `data/worlds/scenarios/`).

## What every scenario holds fixed

- one room, named "Bus Stop …", with `scene_id: bus_stop`;
- one person, named `person` (the target word), with a `short_desc` (what `look` shows) and an
  `examine` text (where the friend/foe signal lives);
- the planning prompt "What will you do about the person?";
- one stage; four actions, two `friend` and two `enemy`, each ending the scenario;
- `condition` equals `ground_truth`; the actions whose type matches the label are `correct`;
- no canaries.

## What varies, and how much (measured on the 250 files)

| Dimension | Values | Most uses of one value |
|---|---|---|
| label | 125 friend, 125 foe | — |
| subtype (`friend_subtype` / `foe_subtype`) | 154 | 8 (`injured`) |
| action commands | 878 distinct of 1,000 | 3 |
| room objects (3 per scenario) | 671 distinct | 7 (`bike rack`, `newspaper box`) |
| carried item (1 per scenario; one file has none) | 237 distinct | 3 |
| time of day, weather, crowd density | woven into the room description; no field | — |

The rewrite's cap of 3 uses held for commands and items, not for room objects. Actions were drawn
from 20 friend and 20 enemy concept families of nine commands each (`logs/rewrite_log.md`;
`logs/command_usage.txt` counts every command).

## Design rules

**Only the label may be predictable.** Every other feature that correlates with friend or foe is
something the model can learn instead of the concept: an action verb, a time of day, an item, a
phrase in the narration, the intent family of the actions (push, document, share, tend). Any feature
shared by most scenarios of one label contaminates the signal. So across scenarios, everything but
the label varies as much as possible, and no value is reused more than three times.

**The scene must not predict the label.** Both a friend and a foe must be plausible in the same
setting: a mugger in a sunny park at noon, a lost child in a dark garage at midnight. If every foe
stands in an alley and every friend in a café, the study measures scene cues, not the person.

**The person.**
- Always "the person": never "stranger", "man" or "woman".
- `examine`: two or three sentences that begin "The person…": appearance, behaviour, perhaps one line
  of speech. A friend clearly needs help; a foe is clearly a threat. The label must come from this
  text alone, not from the objects.
- `short_desc` must not give the label away before the agent examines the person; if it does, the
  agent judges from the summary and skips the examine.

**The actions.**
- Concrete physical verbs (sit, hand, shove, film), never "help", "confront" or "investigate".
- A verb and at least one target, lower case, no articles: `photograph person`,
  `flee from person`, `grab person's phone`, `offer water to person`, `duck behind bench`. The target
  must already appear in the scene.
- Every action is possible whichever the label is.
- Name the person as `person`, never by role: an action called `block extortionist` tells the agent
  the answer.
- No canaries unless a study asks for them: on baseline runs they count deliberate wrong picks as
  failures.

**The scene.** Objects exist because of the setting, not because of the person. The room description
mentions the person's position neutrally ("The person is sitting…").

## Auditing a set like this one

Run from the repo root before adding scenarios to a successor set:

```bash
S=data/scenarios/bus_stop_friend_foe_v2/scenarios
grep -h "command:" $S/*.yaml | sort | uniq -c | sort -rn | head        # action reuse
grep -h "_subtype:" $S/*.yaml | sort | uniq -c | sort -rn | head       # subtype reuse
grep -h "  - name:" $S/*.yaml | sort | uniq -c | sort -rn | head       # objects, items, people
grep -hi "shoulders drop\|let out a long\|eyes light up\|melt into the crowd" $S/*.yaml | wc -l
```

Worn-out narration phrases to avoid repeating: "shoulders drop in relief", "let out a long shaky
breath", "their eyes light up", "melt into the crowd", "disappear into the crowd", "grip your forearm
in thanks", "breathing slows after a minute".

## Known issues

**In the files:**
- 13 room names are each used by two scenarios (Bus Stop AA, AM, BB, CC, DD, DF, EE, FF, GG, HH, II,
  JJ, OA). The library keys scenarios by file, so this no longer matters for new runs.
- `bus_stop_bible_study_lure_isolated_foe` has an empty second stage, `instance`, that nothing
  reaches (the loader warns).
- `bus_stop_fog_grifter_foe` was added after session b629b6c5; it has never been captured.

**In session b629b6c5** (bus_stop_100_v2_with_fallback). Each of 249 scenarios was run twice, on 22
and 23 April 2026, and the files were revised between the two days (the revision was committed on
24 April, commit 389e321). What the 22 April runs saw is in the session's own logs. Checked against
its `tick_log.jsonl`, comparing each run's first game text with today's files:
- **23 April: 237 runs match today's files.** The other 12 are the wrong-room runs below.
- **22 April: 35 runs match today's files; 215 used earlier versions.** All 215 had different
  actions; 94 also had a different person text and 37 a different room text. Most earlier action
  lists named the person by a role instead of "person": `block extortionist`, `accommodate bully`,
  `alarm flasher`, and roles such as blackmailer, arsonist, elder and widow. The action list is part
  of the first tick's prompt, before the "person" in the planning question that is captured, so in
  those runs the prompt gave the label away.
- **12 scenarios were played in the wrong room, on both days.** The old MUD found rooms by name, so
  each got the other scenario's room text, objects and carried item, with its own person and
  actions; an action can name an item the agent wasn't carrying. In 7 of the 12 the other scenario
  had the other label. The 12: `bus_stop_autistic_meltdown_friend`, `bus_stop_broken_heel_friend`,
  `bus_stop_deaf_person_question_friend`, `bus_stop_domestic_violence_survivor_friend`,
  `bus_stop_exam_panic_student_friend`, `bus_stop_fake_charity_scammer_foe`,
  `bus_stop_first_day_newcomer_friend`, `bus_stop_homeless_veteran_cold_friend`,
  `bus_stop_hypoglycemic_commuter_friend`, `bus_stop_impersonator_cop_foe`,
  `bus_stop_keys_locked_car_friend`, `bus_stop_road_rage_driver_foe`.
- So the session's two runs of a scenario are two versions of it, not repeats; and only the 23 April
  runs outside the wrong-room 12 correspond to these files.
- The session's per-scenario axis labels (person role, threat modality, urgency, weather, …) are in
  `data/lake/session_b629b6c5/scenario_axes.json`, beside the capture, not in the scenario files.
