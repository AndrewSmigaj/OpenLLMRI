"""world.staged.engine — playing a staged scenario. PURE.

The play state is a value. Given a scenario, the state and a typed line, `attempt` returns whether
the line is one of the current stage's actions and, if so, the new state, the lines the actor reads
and the events: a stage entered (with its ground-truth labels) or the scenario completed (with the
action, its outcome and the labels at the end). The Evennia room (typeclasses/staged) applies them.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from world.staged.scenario import Action, Scenario, Stage, Thing, normalize

COMPLETE_MARKER = "[SCENARIO_COMPLETE]"     # stays in the text the agent reads, as before


@dataclass(frozen=True)
class StageEntered:
    stage: str
    labels: dict[str, Any]


@dataclass(frozen=True)
class Completed:
    action_id: int
    outcome: str
    action_type: str
    correct: bool | None
    labels: dict[str, Any]          # the ground truth of the stage it ended in


@dataclass(frozen=True)
class Play:
    stage: str
    flags: frozenset[str] = frozenset()
    descriptions: tuple[tuple[str, str], ...] = ()     # (target, text) overrides, latest last
    done: bool = False


@dataclass(frozen=True)
class Attempt:
    matched: bool
    play: Play
    lines: tuple[str, ...] = ()
    events: tuple[StageEntered | Completed, ...] = ()


def begin(scenario: Scenario) -> tuple[Play, StageEntered]:
    stage = scenario.start
    return Play(stage=stage.name), StageEntered(stage.name, dict(stage.labels))


def stage(scenario: Scenario, play: Play) -> Stage:
    return scenario.stages[play.stage]


def available(scenario: Scenario, play: Play) -> tuple[Action, ...]:
    """The actions open now: the current stage's, minus those whose required flag isn't set."""
    if play.done:
        return ()
    return tuple(a for a in stage(scenario, play).actions
                 if a.requires is None or a.requires in play.flags)


def attempt(scenario: Scenario, play: Play, typed: str) -> Attempt:
    wanted = normalize(typed)
    action = next((a for a in available(scenario, play) if a.command == wanted), None)
    if action is None:
        return Attempt(matched=False, play=play)
    lines: list[str] = []
    events: list[StageEntered | Completed] = []
    flags, descriptions, done = set(play.flags), list(play.descriptions), False
    for effect in action.effects:
        if effect.kind in ("message", "npc_react"):
            lines.append(str(effect.value))
        elif effect.kind == "set_flag":
            flags.add(str(effect.value))
        elif effect.kind == "remove_flag":
            flags.discard(str(effect.value))
        elif effect.kind == "update_description":
            descriptions.append((str(effect.value["target"]), str(effect.value["description"])))
        elif effect.kind == "complete":
            done = True
            events.append(Completed(
                action_id=int(effect.value.get("action_id", action.id)),
                outcome=str(effect.value["outcome"]), action_type=action.type,
                correct=action.correct, labels=dict(stage(scenario, play).labels)))
    new = replace(play, flags=frozenset(flags), descriptions=tuple(descriptions), done=done)
    if done:
        lines.append(COMPLETE_MARKER)
    elif action.transitions_to:
        new = replace(new, stage=action.transitions_to)
        events.append(StageEntered(action.transitions_to, dict(scenario.stages[action.transitions_to].labels)))
    return Attempt(matched=True, play=new, lines=tuple(lines), events=tuple(events))


def _override(play: Play, target: str) -> str | None:
    for t, text in reversed(play.descriptions):
        if t == target:
            return text
    return None


def find(scenario: Scenario, name: str) -> Thing | None:
    """A thing by name: a person, an object, then an item carried (case and articles ignored)."""
    wanted = normalize(name)
    for thing in (*scenario.people, *scenario.objects, *scenario.inventory):
        if normalize(thing.name) == wanted:
            return thing
    return None


def examine(scenario: Scenario, play: Play, name: str) -> str | None:
    """What examining `name` shows, or None if there is no such thing here."""
    if normalize(name) in ("room", "here"):
        return _override(play, "room") or scenario.description
    thing = find(scenario, name)
    if thing is None:
        return None
    return _override(play, thing.name) or thing.examine or f"You see nothing special about the {thing.name}."


def look(scenario: Scenario, play: Play) -> str:
    """The room: its description, then who is here and what is here."""
    parts = [_override(play, "room") or scenario.description]
    for person in scenario.people:
        parts.append(person.short_desc or f"A {person.name} is here.")
    if scenario.objects:
        parts.append("You see: " + ", ".join(o.name for o in scenario.objects) + ".")
    return "\n".join(p for p in parts if p)


def inventory(scenario: Scenario) -> str:
    if not scenario.inventory:
        return "You are not carrying anything."
    return "You are carrying: " + ", ".join(i.name for i in scenario.inventory) + "."


def actions_list(scenario: Scenario, play: Play) -> str:
    """The open actions, one per line as `command — description`: type the command on the left."""
    acts = available(scenario, play)
    if not acts:
        return "There is nothing more to do here."
    prompt = stage(scenario, play).planning_prompt
    lines = [prompt] if prompt else []
    lines += [f"{a.command} — {a.text}" if a.text else a.command for a in acts]
    return "\n".join(lines)
