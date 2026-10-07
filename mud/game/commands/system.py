"""game.commands.system — what runs for input that matches no command, several commands, or nothing.

Without these, Evennia answers such input with a built-in reply that runs no command, so it never
ends with the prompt, and a client waiting for the prompt (the backend's agent) would wait forever.
As commands they answer as Evennia's built-in replies do, and end with the prompt. The account and
the login screen carry them (commands/default_cmdsets.py), so they apply everywhere; Winter Survival's
own CmdNoMatch (its grammar help) replaces SystemNoMatch inside its rooms.
"""
from django.utils.translation import gettext as _
from evennia.commands.cmdhandler import CMD_NOMATCH
from evennia.commands.default.syscommands import SystemMultimatch, SystemNoInput  # noqa: F401
from evennia.utils import utils

from commands.command import Command


class SystemNoMatch(Command):
    """Input that matches no command. The reply is Evennia's built-in one, word for word."""

    key = CMD_NOMATCH
    locks = "cmd:all()"

    def func(self):
        raw = self.args                 # Evennia hands a no-match command the input as typed
        text = _("Command '{command}' is not available.").format(command=raw)
        suggestions = utils.string_suggestions(
            raw, self.cmdset.get_all_cmd_keys_and_aliases(self.caller), cutoff=0.7, maxnum=3)
        if suggestions:
            text += _(" Maybe you meant {command}?").format(
                command=utils.list_to_string(suggestions, endsep=_("or"), addquote=True))
        else:
            text += _(' Type "help" for help.')
        self.msg(text)
