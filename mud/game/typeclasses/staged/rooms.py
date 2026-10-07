"""game.typeclasses.staged.rooms — a room playing one staged scenario. Shell.

One fresh instance per load (typeclasses.staged.instances). The scenario's data (world.staged) is the
room's description, its people and objects, the player's scenario inventory and the actions open in
each stage. A typed line that is one of the open actions is claimed before any command runs
(commands.command.AreaInputMixin): the actor reads the action's lines, others in the room read the
typed line, and the stage changes or the scenario completes. Each stage entered and the completion are
also sent as structured messages for the backend's runner:
  ["stage_entered", [{scenario, set, file_hash, stage, labels}], {}]
  ["scenario_complete", [{scenario, set, file_hash, action_id, outcome, action_type, correct,
                          labels}], {}]
"""
from __future__ import annotations

from typing import Any

from typeclasses.rooms import Room
from world.staged import engine, library


class StagedRoom(Room):
    """A room playing one staged scenario (db.scenario_key = "<set_id>/<file>")."""

    # The commands a character has while standing here (Character.at_cmdset_get switches to it).
    character_cmdset = "commands.staged.cmdset.StagedCharacterCmdSet"

    # --- the scenario and its play state -------------------------------------------------------

    @property
    def loaded(self) -> library.Loaded:
        if self.ndb.loaded is None:
            self.ndb.loaded = library.load(self.db.scenario_key)
        return self.ndb.loaded

    @property
    def scenario(self):
        return self.loaded.scenario

    def play(self) -> engine.Play:
        p = self.db.play or {}
        return engine.Play(stage=p["stage"], flags=frozenset(p.get("flags", ())),
                           descriptions=tuple(tuple(d) for d in p.get("descriptions", ())),
                           done=bool(p.get("done")))

    def _save(self, play: engine.Play) -> None:
        self.db.play = {"stage": play.stage, "flags": sorted(play.flags),
                        "descriptions": [list(d) for d in play.descriptions], "done": play.done}

    def start(self) -> engine.StageEntered:
        play, entered = engine.begin(self.scenario)
        self._save(play)
        return entered

    # --- what the player reads -----------------------------------------------------------------

    def return_appearance(self, looker, **kwargs):
        return f"|c{self.key}|n\n{engine.look(self.scenario, self.play())}"

    def examine_text(self, name: str) -> str | None:
        return engine.examine(self.scenario, self.play(), name)

    def inventory_text(self) -> str:
        return engine.inventory(self.scenario)

    def actions_text(self) -> str:
        return engine.actions_list(self.scenario, self.play())

    # --- a typed line that is one of the open actions ------------------------------------------

    def claim_input(self, caller, raw_string: str) -> bool:
        typed = (raw_string or "").strip()
        step = engine.attempt(self.scenario, self.play(), typed)
        if not step.matched:
            return False
        self._save(step.play)
        if step.lines:
            caller.msg("\n".join(step.lines))
        self.msg_contents(f"{caller.get_display_name(caller)}: {typed}", exclude=[caller])
        for event in step.events:
            self.report(caller, event)
        return True

    def report(self, caller, event: engine.StageEntered | engine.Completed) -> None:
        about: dict[str, Any] = {"scenario": self.db.scenario_key, "set": self.loaded.set.ref,
                                 "file_hash": self.loaded.file_hash}
        if isinstance(event, engine.StageEntered):
            caller.msg(stage_entered=[{**about, "stage": event.stage, "labels": event.labels}])
        else:
            caller.msg(scenario_complete=[{
                **about, "action_id": event.action_id, "outcome": event.outcome,
                "action_type": event.action_type, "correct": event.correct,
                "canary": event.canary, "labels": event.labels}])
