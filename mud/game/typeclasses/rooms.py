"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    def get_display_things(self, looker, **kwargs):
        """DR-23 scene-as-prose: replace the stock 'You see: a, b, c' contents list with composed,
        salience-weighted prose (pure `presentation.compose_scene` over marshalled EntityStates).
        Everything present is still mentioned — weighting, never hiding."""
        from typeclasses.worldview import to_entity_state
        from world.sim import presentation
        things = self.filter_visible(self.contents_get(content_type="object"), looker, **kwargs)
        if not things:
            return ""
        return presentation.compose_scene([to_entity_state(o) for o in things])
