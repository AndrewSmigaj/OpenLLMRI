"""game.typeclasses.staged.instances — loading and ending staged scenarios. Shell.

One fresh StagedRoom per load. The previous instance is deleted at the next load, or when the player
ends the scenario — never inside the action that ends it, so no move text reaches the reply to that
action. Moves are silent and run no move hooks (no arrival look): the runner and the simulator decide
what the player reads next. The simulator's command and the backend's control channel
(server/conf/inputfuncs.py) both call these functions.
"""
from __future__ import annotations

from evennia import create_object

from typeclasses.staged.rooms import StagedRoom
from world.staged import engine, library

_ROOM = "typeclasses.staged.rooms.StagedRoom"


def load_scenario(character, key: str) -> tuple[StagedRoom, engine.StageEntered]:
    """Put `character` in a fresh instance of the scenario `key` ("<set_id>/<file>"). Raises
    ScenarioError, before anything changes, if the key or the file is bad."""
    loaded = library.load(key)
    old = character.location if isinstance(character.location, StagedRoom) else None
    room = create_object(_ROOM, key=loaded.scenario.room_name,
                         attributes=[("scenario_key", key)])
    room.ndb.loaded = loaded
    entered = room.start()
    if old is None:
        character.db.staged_return = character.location     # where `end` takes the player back
    character.move_to(room, quiet=True, move_hooks=False)
    if old is not None:
        old.delete()
    room.report(character, entered)
    return room, entered


def end_scenario(character) -> bool:
    """Take `character` back to where it came from and delete the instance. False if it isn't in one."""
    room = character.location
    if not isinstance(room, StagedRoom):
        return False
    back = character.db.staged_return or character.home
    character.move_to(back, quiet=True, move_hooks=False)
    character.attributes.remove("staged_return")
    room.delete()
    return True
