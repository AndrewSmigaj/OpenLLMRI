"""game.commands.institute.cmdset — the commands a character has in the simulator room: the stock
character commands, plus `simulator` (browse the scenario library) and `simulate` (load from it)."""
from commands.default_cmdsets import CharacterCmdSet


class SimulatorCharacterCmdSet(CharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        from commands.institute.commands import CmdSimulate, CmdSimulator
        self.add(CmdSimulator())
        self.add(CmdSimulate())
