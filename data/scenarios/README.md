# The scenario library

Scenarios are datasets, like sentence sets: a set is designed for a study by varying some things and
holding others fixed. Other studies reuse a set, or build their own. The MUD plays them and the
backend's agent runner records what the model did and what it saw. Both read this one folder (the
MUD's container mounts it read-only as `SCENARIO_LIBRARY`).

Related: `docs/architecture/one-mud.md` §5 (why the library looks like this), the staged engine
`mud/game/world/staged/` (the code that reads it), `data/sentence_sets/GUIDE.md` (sentence-set
design rules, ported from the friend/foe set's).

## Layout

```
data/scenarios/
  README.md                this file: the library and the staged-scenario format
  <set_id>/
    set.yaml               the set's manifest
    GUIDE.md               the set's own design rules and known issues
    logs/                  authoring logs, audits, superseded lists
    scenarios/*.yaml       one file per scenario (staged sets)
  _parked/                 files kept for reference that no set uses (folders starting with _ are skipped)
```

- **A scenario's key is `<set_id>/<file stem>`**, e.g.
  `bus_stop_friend_foe_v2/bus_stop_autistic_meltdown_friend`. Never the room name: room names can
  repeat inside a set.
- **A study cites a set as `<set_id>@<version>`.** Every run records the set reference, the scenario
  key and the scenario file's sha256.
- **A set that a finished study used is never edited.** Changes go into a new version, or a new set.

## set.yaml

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | the folder's name |
| `version` | yes | bumped on any change to the set's scenarios |
| `kind` | yes | `staged` (multiple-choice scenarios played by the staged engine), `world` (a free-form world played by its own engine) or `mini-world` (a world configuration: a starting situation, designed axes and exit conditions) |
| `title` | no | a short name for menus |
| `purpose` | yes | the question the set serves |
| `axes` | yes for staged sets | what the set varies on purpose: the label(s) under study and everything varied so it can't stand in for them |
| `invariants` | yes for staged sets | what every scenario holds fixed (target words, planning prompt, shape) |
| `subsets` | no | named lists of file stems, e.g. a balanced sample; the loader rejects a name that isn't a file |
| `provenance` | yes | how and when the set was made |
| `used_by` | yes | the studies and sessions that used it (empty until one does) |
| `world` | `world` sets | the world's package in the MUD, `mud/game/world/scenarios/<world>/`; its `build.start_room()` gives the room a player enters |

## The staged-scenario format

A staged scenario is one room, one or more people and objects, and a set of **stages**. Each stage
offers actions; typing one applies its effects: a message, a change to what the player sees, the next
stage, or the end with an outcome. Each stage can declare its own ground-truth labels, so a scenario can
shift partway (a reveal at stage 3 turns a friend into a foe).

```yaml
name: bus_stop_autistic_meltdown_friend   # the file stem
scene_id: bus_stop                        # every other scalar top-level field is a label:
condition: friend                         #   recorded with each stage the run enters
ground_truth: friend
friend_subtype: autistic_sensory_overload
target_words: ["person"]                  # where the backend captures activations

rooms:
  - name: Bus Stop II                     # exactly one room
    description: |                        # what `look` shows
      A bus stop near a construction detour on a sunny weekday afternoon...
    inventory:                            # what the player carries
      - name: foam earplugs
        examine: A clean sealed packet of yellow foam earplugs.
    objects:                              # what is in the room
      - name: traffic cone
        examine: A folded traffic cone left on the curb. Scuffed.
    npcs:                                 # the people
      - name: person
        short_desc: rocking and covering their ears, overloaded by the jackhammer   # follows "A person is here,"
        examine: |
          The person is rocking, hands clamped over their ears...
    states:                               # the stages; the first is always `initial`
      initial:
        planning_prompt: "What will you do about the person?"
        labels: {}                        # optional: labels for this stage, over the top-level ones
        actions:
          - id: 1
            command: "offer earplugs to person"
            text: Silently set the earplug packet within their reach
            type: friend
            correct: true
            effects:
              - message: "You set the packet on the curb beside them and step back..."
              - complete: {outcome: friend, action_id: 1}
```

### Actions

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | an integer, unique within the stage |
| `command` | yes | the text that takes this action, compared after normalizing (below) |
| `text` | no | what `actions` shows beside the command |
| `type` | yes | the action's class, e.g. `friend` or `enemy` |
| `correct` | no | whether it is right for the scenario's label |
| `canary` | no | wrong in every condition; a steering-detection device, only when a study asks for it |
| `requires` | no | a flag that must be set for the action to be open |
| `effects` | yes | what happens, in order |
| `transitions_to` | no | the stage that follows; leave it out when the action ends the scenario |

**Matching.** A typed line takes an open action when the two are equal after normalizing: lower case,
the articles *the*, *a* and *an* removed, spaces collapsed, trailing punctuation dropped. So
"Give the map to the person." takes `give map to person`. There is no verb table: the room claims a
matching line before any command runs, so an action wins over a command that shares its verb. A line
that matches no open action runs as an ordinary command.

**What people see.** The player reads the action's messages. Others in the room see the typed line,
e.g. `Ann: give the map to the person`.

### Effects

| Effect | Example | What it does |
|---|---|---|
| `message` | `message: "You sit down."` | text for the player |
| `npc_react` | `npc_react: "The person says thank you."` | a person's response, for the player |
| `complete` | `complete: {outcome: friend, action_id: 1}` | ends the scenario with an outcome |
| `set_flag` | `set_flag: person_on_ground` | sets a flag for `requires` |
| `remove_flag` | `remove_flag: person_on_ground` | clears it |
| `update_description` | `update_description: {target: person, description: "..."}` | changes what `examine` shows for a person or an object, or what `look` shows when the target is `room` |

The old prototype also had vendors, portable objects, dialogue topics and three more effects
(`reveal_object`, `remove_object`, `move_object`). No set uses them, so the staged engine doesn't
have them; extra fields in a file are ignored.

### Multi-stage patterns

A non-terminal action leaves out `complete` and names the next stage:

```yaml
states:
  initial:
    planning_prompt: "What will you do about the person?"
    actions:
      - id: 4
        command: "shove person"
        type: enemy
        effects:
          - message: "You shove the person. They fall, the bottle shattering."
          - update_description: {target: person, description: "The person is sprawled on the ground."}
          - set_flag: person_on_ground
        transitions_to: after_shove
  after_shove:
    planning_prompt: "The person is on the ground. What now?"
    labels: {ground_truth: friend}        # the reveal: from here on, the truth is different
    actions:
      - id: 5
        command: "help person up"
        type: friend
        requires: person_on_ground        # open only while the flag is set
        effects:
          - message: "You help them to their feet."
          - complete: {outcome: friend, action_id: 5}
```

## Playing and validating

- **Loading** checks the whole file first and names the file and field of any problem: one room, an
  `initial` stage, known effects, unique action ids and commands, transitions to stages that exist,
  and at least one action that completes. A stage nothing can reach is reported as a warning.
- **In the MUD,** each load is a fresh copy of the scenario's room. The player has `look`, `examine`,
  `inventory` and `actions`; the room sends `stage_entered {scenario, set, file_hash, stage, labels}`
  on each stage, and `scenario_complete {…, action_id, outcome, action_type, correct, labels}` with the
  `[SCENARIO_COMPLETE]` marker at the end (`docs/architecture/one-mud.md` §6).
- **People** browse and load sets in the institute's simulator room; the backend's runner loads them
  through the MUD's control channel. Both call the same function.
- **The library's own test** loads every set's manifest and every scenario file, so a broken file fails
  CI (`mud/game/tests/staged/test_library.py`).
