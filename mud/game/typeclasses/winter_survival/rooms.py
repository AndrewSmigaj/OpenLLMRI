"""game.typeclasses.winter_survival.rooms — the Winter Survival room. Shell.

Everything that makes a room Winter Survival's lives here: the scene-as-prose survey (DR-23), the
zone bands (DR-13a), how a character standing in it looks, and which commands it has. A character
crosses areas, so it asks the room it stands in (typeclasses.characters); a plain room (the
institute's kind) leaves it stock Evennia.
"""
from typeclasses.rooms import Room


class WinterSurvivalRoom(Room):
    """A room in Winter Survival."""

    # The commands a character has while standing here (Character.at_cmdset_get switches to it).
    character_cmdset = "commands.winter_survival.cmdset.WinterSurvivalCharacterCmdSet"

    def render_character(self, character, looker, **kwargs):
        """DR-23/DR-25: the unified renderer for characters too — describe() weaves worn layers
        ('The pilot wears a flight jacket'); looking at YOURSELF appends the shared warmth
        summary, so `look at me` ≡ `examine me` byte-for-byte (one pure helper behind both).
        Characters cross areas: typeclasses.characters asks the room they stand in."""
        from typeclasses.winter_survival.worldview import to_entity_state
        from world.scenarios.winter_survival import content
        from world.sim import presentation
        from world.sim.systems import warmth
        me = to_entity_state(character)
        if looker is character:
            worn = [to_entity_state(o) for o in character.contents
                    if (o.db.state or {}).get("worn_by")]
            return warmth.self_view(me, worn, content.MATERIALS)   # the ONE self-view helper
        return presentation.describe(me)

    def _looker_zone(self, looker):
        from typeclasses.winter_survival.worldview import zone_of
        from world.sim.space import zones as zonemap
        if not (self.db.default_zone and zonemap.loaded()):
            return None
        return zone_of(looker, self)

    def get_display_things(self, looker, **kwargs):
        """DR-23 scene-as-prose (+ DR-13a bands): composed, salience-weighted prose; in a zoned
        scene, same-zone things render fully and farther bands fade into direction-framed graded
        lines (OUT_OF_SIGHT absent). An unzoned room = the one-zone world, unchanged."""
        from typeclasses.winter_survival.worldview import to_entity_state, zone_of
        from world.sim import presentation
        from world.sim.space import perception
        things = self.filter_visible(self.contents_get(content_type="object"), looker, **kwargs)
        if not things:
            return ""
        ents = [to_entity_state(o) for o in things]
        for ent, obj in zip(ents, things):
            z = zone_of(obj, self)               # stamp the EFFECTIVE zone → space grouping needs it
            if z:                                # (mirrors EvenniaWorldView.get; unzoned stays None)
                ent.state["zone"] = z
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
        from typeclasses.winter_survival.worldview import zone_of
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
