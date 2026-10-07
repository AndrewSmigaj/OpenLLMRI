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
        names a character command set (Winter Survival's, the institute's) gets it, and a room that
        picks one per character (a staged scenario: its player, or a watcher) picks it; anywhere
        else, the stock set. Evennia calls this before every command lookup; the switch is never
        stored."""
        room = self.location
        pick = getattr(room, "character_cmdset_for", None)
        wanted = ((pick(self) if pick is not None else getattr(room, "character_cmdset", None))
                  or settings.CMDSET_CHARACTER)
        if not self.cmdset.has(wanted, must_be_default=True):
            self.cmdset.add_default(wanted, persistent=False)

    def at_post_puppet(self, **kwargs):
        """Logging in inside an institute room tells the app where the character is, as arriving
        there does (typeclasses/institute/rooms.py)."""
        super().at_post_puppet(**kwargs)
        context = getattr(self.location, "app_context", None)
        if context is not None:
            self.msg(room_entered=[context(self)])

    def at_pre_unpuppet(self, **kwargs):
        """A watcher leaving the game stops watching first, so the room it watched never hears it
        leave: a scenario's player, an agent, would read that line (typeclasses/watching.py)."""
        from typeclasses.watching import stop_watching
        stop_watching(self)
        super().at_pre_unpuppet(**kwargs)

    def at_post_move(self, source_location, move_type="move", **kwargs):
        """A move made with look=False (loading or ending a scenario) shows nothing on arrival: the
        runner or the command decides what the player reads next. Every move still runs the rooms'
        enter and leave hooks. Any other move looks around, as stock Evennia does."""
        if kwargs.get("look", True):
            super().at_post_move(source_location, move_type=move_type, **kwargs)

    def return_appearance(self, looker, **kwargs):
        """A character crosses areas, so the area it stands in decides how it looks: a room that
        renders characters (Winter Survival's: worn layers, the warmth self-view) does; anywhere
        else it is stock Evennia."""
        render = getattr(self.location, "render_character", None)
        if render is not None:
            return render(self, looker, **kwargs)
        return super().return_appearance(looker, **kwargs)
