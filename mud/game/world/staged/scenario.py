"""world.staged.scenario — a staged scenario as data. PURE (stdlib + PyYAML-parsed dicts).

Parses one scenario file of the library (data/scenarios/<set>/scenarios/<file>.yaml; the format is
data/scenarios/README.md) into frozen dataclasses and validates it, so a malformed file fails when it
loads, with a message naming the file and the field, never halfway through a run.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Top-level fields that are structure, not labels; every other scalar top-level field is a label.
STRUCTURE = {"name", "rooms", "target_words", "npcs"}
START = "initial"
EFFECTS = {"message", "npc_react", "complete", "set_flag", "remove_flag", "update_description"}

_ARTICLES = re.compile(r"\b(the|a|an)\s+", re.IGNORECASE)
_TRAILING = re.compile(r"[\s.!?;:,]+$")


class ScenarioError(ValueError):
    """A scenario file that does not follow the format."""


def normalize(text: str) -> str:
    """How typed text and action commands are compared: lower case, articles stripped, spaces
    collapsed, trailing punctuation dropped. 'Give the map to the person.' == 'give map to person'."""
    text = _ARTICLES.sub("", text.strip().lower())
    return _TRAILING.sub("", " ".join(text.split()))


@dataclass(frozen=True)
class Thing:
    """An object in the room, an item the player carries, or a person."""
    name: str
    examine: str
    short_desc: str = ""


@dataclass(frozen=True)
class Effect:
    kind: str           # one of EFFECTS
    value: Any


@dataclass(frozen=True)
class Action:
    id: int
    command: str        # normalized
    text: str
    type: str
    correct: bool | None
    canary: bool
    requires: str | None
    effects: tuple[Effect, ...]
    transitions_to: str | None


@dataclass(frozen=True)
class Stage:
    name: str
    planning_prompt: str
    labels: dict[str, Any]          # the ground truth while the scenario is in this stage
    actions: tuple[Action, ...]


@dataclass(frozen=True)
class Scenario:
    key: str                        # set_id/file — never the room name
    name: str
    labels: dict[str, Any]          # scenario-level ground truth (condition, ground_truth, …)
    target_words: tuple[str, ...]
    room_name: str
    description: str
    objects: tuple[Thing, ...]
    inventory: tuple[Thing, ...]
    people: tuple[Thing, ...]
    stages: dict[str, Stage] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    @property
    def start(self) -> Stage:
        return self.stages[START]


def _fail(key: str, where: str, problem: str) -> ScenarioError:
    return ScenarioError(f"{key}: {where}: {problem}")


def _things(key: str, raw: Any, where: str) -> tuple[Thing, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise _fail(key, where, "must be a list")
    out = []
    for i, t in enumerate(raw):
        if not isinstance(t, dict) or not t.get("name"):
            raise _fail(key, f"{where}[{i}]", "needs a name")
        out.append(Thing(name=str(t["name"]), examine=str(t.get("examine", "")).strip(),
                         short_desc=str(t.get("short_desc", "")).strip()))
    return tuple(out)


def _effect(key: str, raw: Any, where: str) -> Effect:
    if not isinstance(raw, dict) or len(raw) != 1:
        raise _fail(key, where, "an effect is a mapping with exactly one kind")
    kind, value = next(iter(raw.items()))
    if kind not in EFFECTS:
        raise _fail(key, where, f"unknown effect {kind!r} (known: {', '.join(sorted(EFFECTS))})")
    if kind == "complete" and not (isinstance(value, dict) and value.get("outcome")):
        raise _fail(key, where, "complete needs an outcome")
    if kind == "update_description" and not (isinstance(value, dict) and value.get("target")
                                             and "description" in value):
        raise _fail(key, where, "update_description needs a target and a description")
    return Effect(kind=kind, value=value)


def _action(key: str, raw: Any, where: str) -> Action:
    if not isinstance(raw, dict):
        raise _fail(key, where, "an action is a mapping")
    for f in ("id", "command", "type"):
        if raw.get(f) in (None, ""):
            raise _fail(key, where, f"needs {f}")
    if not isinstance(raw["id"], int):
        raise _fail(key, where, "id must be an integer")
    effects = raw.get("effects") or []
    if not isinstance(effects, list):
        raise _fail(key, where, "effects must be a list")
    return Action(
        id=raw["id"], command=normalize(str(raw["command"])), text=str(raw.get("text", "")),
        type=str(raw["type"]), correct=raw.get("correct"), canary=bool(raw.get("canary", False)),
        requires=raw.get("requires"),
        effects=tuple(_effect(key, e, f"{where}.effects[{i}]") for i, e in enumerate(effects)),
        transitions_to=raw.get("transitions_to"))


def parse(data: Any, key: str) -> Scenario:
    """Parse and validate one scenario file's contents. Raises ScenarioError."""
    if not isinstance(data, dict):
        raise _fail(key, "file", "must be a mapping")
    rooms = data.get("rooms")
    if not isinstance(rooms, list) or len(rooms) != 1:
        raise _fail(key, "rooms", "a staged scenario has exactly one room")
    room = rooms[0]
    if not isinstance(room, dict) or not room.get("name"):
        raise _fail(key, "rooms[0]", "needs a name")
    target_words = data.get("target_words")
    if not isinstance(target_words, list) or not target_words:
        raise _fail(key, "target_words", "must be a non-empty list")
    labels = {k: v for k, v in data.items()
              if k not in STRUCTURE and isinstance(v, (str, int, float, bool))}

    raw_stages = room.get("states") or {}
    if not isinstance(raw_stages, dict) or START not in raw_stages:
        raise _fail(key, "rooms[0].states", f"needs a {START!r} stage")
    stages: dict[str, Stage] = {}
    for name, raw in raw_stages.items():
        raw = raw or {}
        where = f"states.{name}"
        stage_labels = raw.get("labels") or {}
        if not isinstance(stage_labels, dict):
            raise _fail(key, f"{where}.labels", "must be a mapping")
        actions = tuple(_action(key, a, f"{where}.actions[{i}]")
                        for i, a in enumerate(raw.get("actions") or []))
        ids = [a.id for a in actions]
        if len(ids) != len(set(ids)):
            raise _fail(key, where, "action ids repeat")
        commands = [a.command for a in actions]
        if len(commands) != len(set(commands)):
            raise _fail(key, where, "two actions have the same command")
        stages[name] = Stage(name=name, planning_prompt=str(raw.get("planning_prompt", "")),
                             labels={**labels, **stage_labels}, actions=actions)

    warnings = []
    reachable = {START} | {a.transitions_to for s in stages.values() for a in s.actions
                           if a.transitions_to}
    for s in stages.values():
        for a in s.actions:
            if a.transitions_to and a.transitions_to not in stages:
                raise _fail(key, f"states.{s.name}", f"transitions_to {a.transitions_to!r}: no such stage")
        if s.name not in reachable:
            warnings.append(f"stage {s.name!r} can't be reached")
        if not s.actions and not any(e.kind == "complete" for x in stages.values()
                                     for a in x.actions for e in a.effects):
            warnings.append(f"stage {s.name!r} has no actions and nothing completes")
    if not any(e.kind == "complete" for s in stages.values() for a in s.actions for e in a.effects):
        raise _fail(key, "states", "no action completes the scenario")

    return Scenario(
        key=key, name=str(data.get("name") or key), labels=labels,
        target_words=tuple(str(w) for w in target_words), room_name=str(room["name"]),
        description=str(room.get("description", "")).strip(),
        objects=_things(key, room.get("objects"), "rooms[0].objects"),
        inventory=_things(key, room.get("inventory"), "rooms[0].inventory"),
        people=_things(key, room.get("npcs"), "rooms[0].npcs"),
        stages=stages, warnings=tuple(warnings))
