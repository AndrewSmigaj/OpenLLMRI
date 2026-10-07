"""game.commands.staged.commands — look, examine, inventory and actions in a staged scenario's room,
and `leave` for builders testing a scenario (an agent can't type its way out of one: the backend's
runner ends scenarios through the control channel)."""
from commands.command import Command


def _room(caller):
    from typeclasses.staged.rooms import StagedRoom
    room = caller.location
    return room if isinstance(room, StagedRoom) else None


class _Shown:
    """A staged command the player types is shown to watchers in the room, as an action is."""

    def at_post_cmd(self):
        room = _room(self.caller)
        if room is not None and room.is_player(self.caller):
            room.show_observers(self.caller, self.raw_string.strip())
        super().at_post_cmd()


class CmdStagedLook(_Shown, Command):
    """Look around, or at something or someone.

    Usage:
      look
      look <thing>
    """
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"

    def func(self):
        room = _room(self.caller)
        target = self.args.strip()
        if target.lower().startswith("at "):
            target = target[3:].strip()
        if room is None:
            self.caller.msg("You are nowhere in particular.")
        elif not target:
            self.caller.msg(room.return_appearance(self.caller))
        else:
            self.caller.msg(room.examine_text(target) or "You don't see that here.")


class CmdStagedExamine(_Shown, Command):
    """Examine something or someone closely.

    Usage:
      examine <thing>
    """
    key = "examine"
    aliases = ["ex", "exa"]
    locks = "cmd:all()"

    def func(self):
        room = _room(self.caller)
        target = self.args.strip()
        if room is None:
            self.caller.msg("You are nowhere in particular.")
        elif not target:
            self.caller.msg("Examine what?")
        else:
            self.caller.msg(room.examine_text(target) or "You don't see that here.")


class CmdStagedInventory(_Shown, Command):
    """See what you are carrying.

    Usage:
      inventory
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"

    def func(self):
        room = _room(self.caller)
        self.caller.msg(room.inventory_text() if room else "You are not carrying anything.")


class CmdActions(_Shown, Command):
    """List what you can do here. Type the command on the left of the dash.

    Usage:
      actions
    """
    key = "actions"
    locks = "cmd:all()"

    def func(self):
        room = _room(self.caller)
        self.caller.msg(room.actions_text() if room else "There is nothing to do here.")


class CmdLeave(Command):
    """End the scenario and go back to where you were (builders testing scenarios).

    Usage:
      leave
    """
    key = "leave"
    locks = "cmd:perm(Builder)"

    def func(self):
        from typeclasses.staged.instances import end_scenario
        if end_scenario(self.caller):
            self.caller.msg(self.caller.location.return_appearance(self.caller))
        else:
            self.caller.msg("You are not in a scenario.")
