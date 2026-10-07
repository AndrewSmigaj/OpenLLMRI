"""game.typeclasses.winter_survival.objects — the Winter Survival object. Shell.

Every object built for Winter Survival or minted by its single writer (apply) is one of these: it
renders through the pure presentation layer, honours the zone bands, refuses to drop while worn, and
lands in the dropper's zone and space.
"""
from typeclasses.objects import Object


class WinterSurvivalObject(Object):
    """A thing in Winter Survival."""

    def return_appearance(self, looker, **kwargs):
        """DR-23 unified renderer: `look at X` shows exactly what `examine X` shows — the pure
        `presentation.describe` over this object's marshalled EntityState. DR-13a: beyond the
        looker's zone this is the §17 too-far answer instead (look at ≡ examine holds — the
        taught-grammar path gets the same line from the resolver's reach gate)."""
        from typeclasses.winter_survival.worldview import to_entity_state, zone_of
        from world.sim import narrator, presentation
        from world.sim.space import direction, perception, zones as zonemap
        room = getattr(looker, "location", None)
        if room is not None and room.db.default_zone and zonemap.loaded() \
                and getattr(self, "location", None) is room:
            lzone, ozone = zone_of(looker, room), zone_of(self, room)
            if lzone and ozone and lzone != ozone:
                res = perception.perceive(lzone, ozone)
                if not res.visible:
                    return "You don't see that here."
                return narrator.narrate("reach.too_far",
                                        {"target": self.key,
                                         "direction": direction.phrase(lzone, ozone) or "some way off",
                                         "verb": "inspect"})
        return presentation.describe(to_entity_state(self))

    def at_pre_drop(self, dropper, **kwargs):
        """DR-25: worn things don't fall off — take them off first (read-only refusal)."""
        if (self.db.state or {}).get("worn_by"):
            dropper.msg("You're wearing it — take it off first.")
            return False
        return super().at_pre_drop(dropper, **kwargs)

    def at_drop(self, dropper, **kwargs):
        """DR-13a zone sync + scene-space landing: a dropped object lands in the dropper's zone and
        its default space — through the single writer (stock get/drop move via Evennia containment,
        not Effects, so without this a dropped thing would keep a stale zone / no space). An explicit
        `drop X on <space>` overrides the space afterwards in CmdDrop."""
        super().at_drop(dropper, **kwargs)
        room = getattr(dropper, "location", None)
        if room is None or not room.db.default_zone:
            return                                     # unzoned world: nothing to sync
        from typeclasses.winter_survival.apply import apply as apply_effects
        from typeclasses.winter_survival.worldview import EvenniaWorldView, zone_of
        from world.sim import effects
        from world.sim.space import spaces as spacemap
        world = EvenniaWorldView(room, dropper, seed=(room.db.seed or 0))
        zone = zone_of(dropper, room)
        sim_id = self.db.sim_id or self.key
        fx = [effects.move_zone(sim_id, zone)]
        default = spacemap.default_space(zone)
        if default is not None:
            fx.append(effects.set_attr(sim_id, "space", default.id))
        apply_effects(fx, world)
