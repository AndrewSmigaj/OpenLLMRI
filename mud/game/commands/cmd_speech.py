"""game.commands.cmd_speech — zone-aware speech (DR-13a, §15). Shell.

say / whisper / call / shout become SPEECH Events routed through the band-aware propagator:
words carry per §15 (whisper → same zone, say → adjacent, call → near, shout → distant); beyond
word range but within earshot the voice blurs; out of earshot, silence. Stock room-wide say would
break the fiction in a zoned Scene. v1 keeps whisper untargeted (a quiet say); the stock targeted
`whisper <player> = <text>` form is deferred (BACKLOG).
"""
from __future__ import annotations

from commands.command import Command
from typeclasses.propagator import propagate
from world.sim.contracts import Event, EventKind
from world.sim.space import sound

_MODES = ("say", "whisper", "call", "shout")


class CmdSpeak(Command):
    """Speak to those around you.

    Usage:
      say <words>        — carries to the next zone
      whisper <words>    — only your own zone hears
      call <words>       — carries a couple of zones
      shout <words>      — carries across the site
    """
    key = "say"
    aliases = ["whisper", "call", "shout", "'"]
    locks = "cmd:all()"
    help_category = "Communication"

    def func(self):
        caller = self.caller
        text = (self.args or "").strip()
        if not text:
            caller.msg("Say what?")
            return
        mode = self.cmdstring if self.cmdstring in _MODES else "say"
        caller.msg(f'You {mode}, "{text}"')
        room = caller.location
        if room is None:
            return
        ev = Event(EventKind.SPEECH, caller.db.sim_id or caller.key,
                   loudness=sound.SPEECH_LOUDNESS[mode], data={"text": text, "mode": mode})
        propagate(room, [ev], caller)
