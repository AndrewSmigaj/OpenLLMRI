"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def return_appearance(self, looker, **kwargs):
        """DR-23/DR-25: the unified renderer for characters too — describe() weaves worn layers
        ('The pilot wears a flight jacket'); looking at YOURSELF appends the shared warmth
        summary, so `look at me` ≡ `examine me` byte-for-byte (one pure helper behind both)."""
        from typeclasses.worldview import to_entity_state
        from world.scenarios.whiteout import content
        from world.sim import presentation
        from world.sim.systems import warmth
        base = presentation.describe(to_entity_state(self))
        if looker is self:
            worn = [to_entity_state(o) for o in self.contents
                    if (o.db.state or {}).get("worn_by")]
            return f"{base} {warmth.worn_summary(worn, content.MATERIALS)}"
        return base
