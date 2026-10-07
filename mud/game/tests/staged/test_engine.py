"""Tier-1 pure tests for the staged engine (world.staged): a small multi-stage fixture, not a study set."""
import pytest
import yaml

from world.staged import engine
from world.staged.engine import Completed, StageEntered
from world.staged.scenario import ScenarioError, normalize, parse

FIXTURE = """\
name: fixture_stranger
scene_id: fixture
condition: friend
ground_truth: friend
target_words: ["stranger"]
rooms:
  - name: Test Room
    description: A plain test room.
    objects:
      - name: bench
        examine: A wooden bench.
    inventory:
      - name: map
        examine: A folded map.
    npcs:
      - name: stranger
        short_desc: A stranger waits by the door.
        examine: The stranger looks tired.
    states:
      initial:
        planning_prompt: What will you do about the stranger?
        labels: {intent: unknown}
        actions:
          - id: 1
            command: "greet stranger"
            text: Greet the stranger
            type: friend
            correct: true
            effects:
              - message: You greet the stranger.
              - npc_react: The stranger nods.
              - set_flag: greeted
              - update_description: {target: stranger, description: The stranger is smiling.}
            transitions_to: reveal
          - id: 2
            command: "leave"
            text: Walk away
            type: enemy
            correct: false
            effects:
              - message: You walk away.
              - complete: {outcome: enemy, action_id: 2}
      reveal:
        planning_prompt: The stranger pulls a knife. What now?
        labels: {ground_truth: foe, intent: hostile}
        actions:
          - id: 3
            command: "shove stranger"
            text: Shove the stranger away
            type: enemy
            correct: true
            requires: greeted
            effects:
              - message: You shove the stranger.
              - complete: {outcome: enemy, action_id: 3}
          - id: 4
            command: "give map to stranger"
            text: Give your map
            type: friend
            correct: false
            requires: never_set
            effects:
              - complete: {outcome: friend, action_id: 4}
"""


def scenario(text=FIXTURE):
    return parse(yaml.safe_load(text), "fixture_set/fixture_stranger")


def test_typed_text_is_compared_without_articles_case_or_trailing_punctuation():
    assert normalize("  Give the map to   the Person. ") == "give map to person"
    assert normalize("shove a stranger!") == "shove stranger"


def test_a_scenario_walks_its_stages_with_their_labels():
    sc = scenario()
    play, entered = engine.begin(sc)
    assert entered == StageEntered("initial", {"scene_id": "fixture", "condition": "friend",
                                               "ground_truth": "friend", "intent": "unknown"})

    step = engine.attempt(sc, play, "Greet the stranger.")
    assert step.matched and step.lines == ("You greet the stranger.", "The stranger nods.")
    assert step.events == (StageEntered("reveal", {"scene_id": "fixture", "condition": "friend",
                                                   "ground_truth": "foe", "intent": "hostile"}),)
    play = step.play
    assert play.stage == "reveal" and "greeted" in play.flags
    assert engine.examine(sc, play, "the stranger") == "The stranger is smiling."

    end = engine.attempt(sc, play, "shove the stranger")
    assert end.matched and end.play.done
    assert end.lines == ("You shove the stranger.", engine.COMPLETE_MARKER)
    [done] = end.events
    assert done == Completed(action_id=3, outcome="enemy", action_type="enemy", correct=True,
                             labels={"scene_id": "fixture", "condition": "friend",
                                     "ground_truth": "foe", "intent": "hostile"})
    assert engine.available(sc, end.play) == () and not engine.attempt(sc, end.play, "leave").matched


def test_text_that_is_no_open_action_leaves_the_play_unchanged():
    sc = scenario()
    play, _ = engine.begin(sc)
    for typed in ("dance", "shove stranger", "give map to stranger"):    # unknown, other stage
        step = engine.attempt(sc, play, typed)
        assert not step.matched and step.play == play and step.lines == ()


def test_an_action_whose_flag_is_unset_is_not_open():
    sc = scenario()
    play = engine.attempt(sc, engine.begin(sc)[0], "greet stranger").play
    assert [a.id for a in engine.available(sc, play)] == [3]
    assert not engine.attempt(sc, play, "give map to stranger").matched


def test_a_terminal_action_completes_without_entering_a_stage():
    sc = scenario()
    end = engine.attempt(sc, engine.begin(sc)[0], "leave")
    assert [type(e) for e in end.events] == [Completed] and end.events[0].labels["intent"] == "unknown"


def test_what_the_player_reads():
    sc = scenario()
    play, _ = engine.begin(sc)
    assert engine.look(sc, play) == ("A plain test room.\nA stranger waits by the door.\n"
                                     "You see: bench.")
    assert engine.inventory(sc) == "You are carrying: map."
    assert engine.actions_list(sc, play) == ("What will you do about the stranger?\n"
                                             "greet stranger — Greet the stranger\nleave — Walk away")
    assert engine.examine(sc, play, "map") == "A folded map."
    assert engine.examine(sc, play, "unicorn") is None


@pytest.mark.parametrize("change, problem", [
    (("    states:\n      initial:", "    states:\n      start:"), "needs a 'initial' stage"),
    (("- message: You walk away.", "- shout: You walk away."), "unknown effect 'shout'"),
    (("          - id: 2\n", "          - id: 1\n"), "action ids repeat"),
    (("transitions_to: reveal", "transitions_to: nowhere"), "no such stage"),
    (("target_words: [\"stranger\"]", "target_words: []"), "non-empty list"),
])
def test_a_malformed_scenario_fails_at_load_with_the_reason(change, problem):
    with pytest.raises(ScenarioError, match=problem):
        scenario(FIXTURE.replace(*change))


def test_a_scenario_that_never_completes_is_rejected():
    no_end = "\n".join(line for line in FIXTURE.splitlines() if "complete:" not in line)
    with pytest.raises(ScenarioError, match="no action completes"):
        scenario(no_end)


def test_an_empty_unreachable_stage_is_a_warning_not_an_error():
    sc = scenario(FIXTURE.replace("    states:\n", "    states:\n      instance: {}\n"))
    assert any("'instance' can't be reached" in w for w in sc.warnings)
