"""game.commands.staged.cmdset — the commands a character has in a staged scenario's room.

The stock character commands, with look, examine and inventory reading the scenario, and `actions`
listing what is open now. The scenario's own actions are not commands: the room claims a typed line
that is one of them before any command runs (commands.command.AreaInputMixin), so an action wins over a
command that shares its verb (give, help, …).
"""
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
