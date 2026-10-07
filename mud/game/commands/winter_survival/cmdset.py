"""game.commands.winter_survival.cmdset — the commands a character has inside Winter Survival.

A character crosses areas, so the room it stands in decides its commands: Winter Survival's rooms
name this set (WinterSurvivalRoom.character_cmdset) and the character makes it its default while it
is there (Character.at_cmdset_get); anywhere else it has the stock set.

This is a whole character command set (the stock one plus Winter Survival's six), not a set laid
over the stock one, because Evennia's merge treats two commands as duplicates only when their KEYS
match: a merged-in CmdAction carrying the get/examine aliases would leave the stock get and the
builder examine standing beside it. Adding the six to a copy of the stock set removes those at
add-time, exactly as when this set was the game's only character set.
"""
from commands.default_cmdsets import CharacterCmdSet


class WinterSurvivalCharacterCmdSet(CharacterCmdSet):
    """The stock character commands with Winter Survival's six: the taught grammar, the
    unmatched-input nudge, the menu-aware drop/look/inventory and zone-aware speech."""

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        # The taught-grammar action command (keyed on every operation verb) + the unmatched-input
        # nudge. (CmdAction's `examine` intentionally overloads the builder examine.)
        from commands.winter_survival.cmd_act import CmdAction, CmdNoMatch
        self.add(CmdAction())
        self.add(CmdNoMatch())
        # Stock drop/look share the DR-08a numbered disambiguation menu (same-key add after super()
        # replaces the stock commands); look also strips 'at' (look at X ≡ examine X, DR-23). GET IS
        # GONE: the taught `take` op owns get/grab (DR-24) — CmdAction (added above) replaced stock
        # CmdGet at add-time, and adding a get-aliased command AFTER it would delete the ENTIRE
        # taught set (Evennia de-dupes by key/alias INTERSECTION — the matchset trap; see
        # containment.md).
        from commands.winter_survival.cmd_items import CmdDrop, CmdInventory, CmdLook
        self.add(CmdDrop())
        self.add(CmdLook())
        self.add(CmdInventory())     # DR-25: carried/worn split + the warmth band
        # Zone-aware speech — say/whisper/call/shout as SPEECH events through the band-routing
        # propagator (DR-13a, §15); replaces the stock room-wide say.
        from commands.winter_survival.cmd_speech import CmdSpeak
        self.add(CmdSpeak())
