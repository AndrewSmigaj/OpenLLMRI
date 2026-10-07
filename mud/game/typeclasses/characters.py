"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from django.conf import settings
from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def at_cmdset_get(self, **kwargs):
        """A character crosses areas, so the room it stands in decides its commands: a room that
        names a character command set (Winter Survival's) gets it; anywhere else, the stock set.
        Evennia calls this before every command lookup; the switch is never stored."""
        wanted = getattr(self.location, "character_cmdset", None) or settings.CMDSET_CHARACTER
        if not self.cmdset.has(wanted, must_be_default=True):
            self.cmdset.add_default(wanted, persistent=False)

    def return_appearance(self, looker, **kwargs):
        """A character crosses areas, so the area it stands in decides how it looks: a room that
        renders characters (Winter Survival's: worn layers, the warmth self-view) does; anywhere
        else it is stock Evennia."""
        render = getattr(self.location, "render_character", None)
        if render is not None:
            return render(self, looker, **kwargs)
        return super().return_appearance(looker, **kwargs)
