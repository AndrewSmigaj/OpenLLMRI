"""game.typeclasses.institute.rooms — the institute's rooms: the hub, the labs and the simulator.

Plain Evennia rooms that tell the app where a character is. Arriving sends
`room_entered [{room_type, role, …}]` and leaving sends `room_left [{room_type}]`, the messages the
app's toolbar reads (the old prototype's contract). The role is `researcher` for Builder accounts and
`visitor` otherwise. A character that logs in inside an institute room is told too
(Character.at_post_puppet).
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from evennia.utils import logger

from typeclasses.rooms import Room


def lab_presets_root() -> Path:
    """LAB_PRESETS if set (the MUD's container mounts data/labs/ there), else the repo's data/labs."""
    env = os.environ.get("LAB_PRESETS")
    return Path(env) if env else Path(__file__).resolve().parents[4] / "data" / "labs"


def role_of(character) -> str:
    account = character.account
    return "researcher" if account and account.check_permstring("Builder") else "visitor"


class InstituteRoom(Room):
    """An institute room: entering and leaving it tell the app where the character is."""
    room_type = "hub"
    character_cmdset = "commands.institute.cmdset.InstituteCharacterCmdSet"

    def app_context(self, character) -> dict:
        """The `room_entered` payload for `character`."""
        return {"room_type": self.room_type, "role": role_of(character)}

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        super().at_object_receive(moved_obj, source_location, move_type=move_type, **kwargs)
        if moved_obj.account:
            moved_obj.msg(room_entered=[self.app_context(moved_obj)])

    def at_object_leave(self, moved_obj, target_location, move_type="move", **kwargs):
        super().at_object_leave(moved_obj, target_location, move_type=move_type, **kwargs)
        if moved_obj.account:
            moved_obj.msg(room_left=[{"room_type": self.room_type}])


class HubRoom(InstituteRoom):
    """The start room, with exits to the labs and the simulator."""
    room_type = "hub"


class LabRoom(InstituteRoom):
    """A lab that shows one capture. Entering sends its preset (data/labs/<db.preset>.yaml: the
    session, the clustering and the panels' settings), so the app loads that view. `micro_world` is
    the app's name for a room that fixes the session shown: its toolbar locks the session picker."""
    room_type = "micro_world"

    def preset(self) -> dict:
        """The lab's preset file, read on every entry so an edit applies without a rebuild."""
        path = lab_presets_root() / f"{self.db.preset}.yaml"
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as err:
            logger.log_err(f"lab {self.key}: can't read its preset {path}: {err}")
            return {}

    def app_context(self, character) -> dict:
        preset = self.preset()
        return {**super().app_context(character),
                "session_id": preset.get("session_id"),
                "clustering_schema": preset.get("clustering_schema"),
                "viz_preset": preset.get("viz_preset")}


class SimulatorRoom(InstituteRoom):
    """The simulator: `simulator` lists the scenario library's sets, and `simulate` loads one
    (commands/institute/). A menu on purpose, unlike a world's rooms."""
    room_type = "simulator"
    character_cmdset = "commands.institute.cmdset.SimulatorCharacterCmdSet"
