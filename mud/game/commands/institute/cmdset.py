"""game.commands.institute.cmdset — the commands a character has in the institute.

Every institute room: the stock character commands, plus `watch` and `unwatch` (follow a character
into the scenarios it plays). The simulator adds `simulator` (browse the scenario library),
`simulate` (load from it) and `agent` (run the model on scenarios, through the backend)."""
from commands.default_cmdsets import CharacterCmdSet


class InstituteCharacterCmdSet(CharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        from commands.watching import CmdUnwatch, CmdWatch
        self.add(CmdWatch())
        self.add(CmdUnwatch())


class SimulatorCharacterCmdSet(InstituteCharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        from commands.institute.commands import CmdAgent, CmdSimulate, CmdSimulator
        self.add(CmdSimulator())
        self.add(CmdSimulate())
        self.add(CmdAgent())
