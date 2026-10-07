"""game.commands.staged.cmdset — the commands a character has in a staged scenario's room.

The player has the stock character commands, with look, examine and inventory reading the scenario,
and `actions` listing what is open now. The scenario's own actions are not commands: the room claims
a typed line that is one of them before any command runs (commands.command.AreaInputMixin), so an
action wins over a command that shares its verb (give, help, …).

A watcher has only what reads the scenario: look, examine, actions, help and `unwatch`. Nothing that
speaks or acts: anything said in the room would reach the player's observation, an agent's prompt.
"""
from evennia import CmdSet, default_cmds

from commands.default_cmdsets import CharacterCmdSet


class StagedCharacterCmdSet(CharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        from commands.staged.commands import (CmdActions, CmdLeave, CmdStagedExamine,
                                              CmdStagedInventory, CmdStagedLook)
        self.add(CmdStagedLook())
        self.add(CmdStagedExamine())
        self.add(CmdStagedInventory())
        self.add(CmdActions())
        self.add(CmdLeave())


class StagedObserverCmdSet(CmdSet):
    key = "StagedObserver"

    def at_cmdset_creation(self):
        from commands.staged.commands import CmdActions, CmdStagedExamine, CmdStagedLook
        from commands.watching import CmdUnwatch
        self.add(CmdStagedLook())
        self.add(CmdStagedExamine())
        self.add(CmdActions())
        self.add(CmdUnwatch())
        self.add(default_cmds.CmdHelp())
