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

    def _looker_zone(self, looker):
        from typeclasses.worldview import zone_of
        from world.sim.space import zones as zonemap
        if not (self.db.default_zone and zonemap.loaded()):
            return None
        return zone_of(looker, self)

    def get_display_things(self, looker, **kwargs):
        """DR-23 scene-as-prose (+ DR-13a bands): composed, salience-weighted prose; in a zoned
        scene, same-zone things render fully and farther bands fade into direction-framed graded
        lines (OUT_OF_SIGHT absent). An unzoned room = the one-zone world, unchanged."""
        from typeclasses.worldview import to_entity_state, zone_of
        from world.sim import presentation
        from world.sim.space import perception
        things = self.filter_visible(self.contents_get(content_type="object"), looker, **kwargs)
        if not things:
            return ""
        ents = [to_entity_state(o) for o in things]
        lzone = self._looker_zone(looker)
        if lzone is None:
            return presentation.compose_scene(ents)
        perceived = {ent.id: perception.perceive(lzone, zone_of(obj, self))
                     for ent, obj in zip(ents, things)}
        return presentation.compose_scene(ents, perceived)

    def get_display_desc(self, looker, **kwargs):
        """DR-13a: a zoned room's survey opens from where you STAND — 'You are in {zone}.' +
        the zone's authored prose — before the scene-wide desc."""
        from world.sim.space import zones as zonemap
        desc = super().get_display_desc(looker, **kwargs)
        lzone = self._looker_zone(looker)
        z = zonemap.get(lzone)
        if z is None:
            return desc
        lead = f"You are in {z.name}." + (f" {z.look}" if z.look else "")
        if "exterior" in z.terrain_tags:
            return lead                    # the cabin's interior desc doesn't follow you outside
        return f"{lead}\n{desc}" if desc else lead

    def get_display_characters(self, looker, **kwargs):
        """DR-13a: same-zone characters render normally; visible farther ones are graded
        ('To the south, Mara is moving about.'); OUT_OF_SIGHT characters don't appear."""
        from typeclasses.worldview import zone_of
        from world.sim.space import perception
        lzone = self._looker_zone(looker)
        if lzone is None:
            return super().get_display_characters(looker, **kwargs)
        chars = self.filter_visible(self.contents_get(content_type="character"), looker, **kwargs)
        here, away = [], []
        for c in chars:
            res = perception.perceive(lzone, zone_of(c, self))
            if res.band.value == "same_zone":
                here.append(c.get_display_name(looker, **kwargs))
            elif res.visible:
                away.append(f"{res.direction_phrase[0].upper()}{res.direction_phrase[1:]}, "
                            f"{c.get_display_name(looker, **kwargs)} is moving about.")
        out = []
        if here:
            out.append("|wWith you:|n " + ", ".join(sorted(here)))
        out.extend(sorted(away))
        return "\n".join(out)
