"""Tier-2: PureWorld ↔ Evennia parity (DR-18a). The pure in-memory world built from OBJECT_TABLE
must match the Evennia world the loader builds from the SAME table — object for object — and stay
matched after the same effect set is applied by the shell's single writer and by PureWorld.apply().
This is what lets probes/fuzz/render run on the pure core and mean something about the live game."""
from evennia.utils.test_resources import EvenniaTest


def _evennia_snapshot(room):
    """id → (name, materials, mass, parts, sorted state minus zone, parent sim_id) — the same shape
    as PureWorld.snapshot() — for every object under the room (recursive)."""
    from typeclasses.worldview import to_entity_state
    out = {}
    pool = list(room.contents)
    while pool:
        o = pool.pop(0)
        if not o.db.sim_id:
            continue
        e = to_entity_state(o)
        st = {k: v for k, v in (o.db.state or {}).items() if k != "zone"}
        parent = o.location.db.sim_id if (o.location is not None and o.location is not room) else None
        out[e.id] = (e.name, tuple(e.materials), int(e.mass_g),
                     tuple((p.id, p.material, p.mass_g, p.attachment) for p in e.parts),
                     tuple(sorted((k, repr(v)) for k, v in st.items())), parent)
        pool.extend(o.contents)
    return out


class TestApplyParity(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.scenarios.whiteout import content
        from world.scenarios.whiteout.build import build
        content.load()
        self.scene = build()

    def _pure(self, actor_zone=None):
        from world.scenarios.whiteout.objects import OBJECT_TABLE
        from world.sim.testing.pure_world import PureWorld
        return PureWorld.from_table(OBJECT_TABLE, actor_zone=actor_zone)

    def test_loader_and_table_build_the_same_world(self):
        ev = _evennia_snapshot(self.scene)
        pw = self._pure().snapshot()
        pw.pop("me", None)
        assert set(ev) == set(pw), (set(ev) ^ set(pw))
        for sid in ev:
            assert ev[sid] == pw[sid], (sid, ev[sid], pw[sid])

    def test_same_effects_same_world_after_apply(self):
        from typeclasses.apply import apply, get_sink
        from typeclasses.worldview import EvenniaWorldView
        from world.scenarios.whiteout import content
        from world.sim.contracts import ActionAttempt, NounRef
        from world.sim.resolver import resolve
        # the actor stands in the rear cabin on both sides
        self.char1.move_to(self.scene, quiet=True)
        self.char1.db.sim_id = "me"
        self.char1.db.state = {"zone": "rear_cabin"}
        pure = self._pure(actor_zone="rear_cabin")
        for attempt in (ActionAttempt(actor="me", verb="break", X=NounRef("bottle"), raw="break bottle"),
                        ActionAttempt(actor="me", verb="cut", X=NounRef("seat2", "cover"),
                                      tool=NounRef("bottle:shard0:loose"), raw="cut cover off 12c with shard")):
            world = EvenniaWorldView(self.scene, self.char1, seed=1)
            r_ev = resolve(attempt, world, content.MATERIALS)
            r_pw = resolve(attempt, pure, content.MATERIALS)
            assert r_ev.resolution == r_pw.resolution and r_ev.tier == r_pw.tier, (r_ev.tier, r_pw.tier)
            assert r_ev.effects == r_pw.effects
            if r_ev.effects:
                apply(list(r_ev.effects), world, sink=get_sink(self.scene))
                pure.apply(r_ev.effects)
            ev = _evennia_snapshot(self.scene)
            ev.pop("me", None)                       # the actor is not part of the object parity
            pw = pure.snapshot()
            pw.pop("me", None)
            assert set(ev) == set(pw), (set(ev) ^ set(pw))
            for sid in ev:
                assert ev[sid] == pw[sid], (sid, ev[sid], pw[sid])
