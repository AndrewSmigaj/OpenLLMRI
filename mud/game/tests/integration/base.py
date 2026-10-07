"""The Tier-2 test base for Winter Survival.

Evennia's EvenniaTest builds room1/room2 and obj1/obj2 from the shared typeclasses, which are plain
Evennia (the institute's kind of room). Winter Survival's behaviour lives in its own room and object
classes, so its tests build those instead.
"""
from evennia.utils.test_resources import EvenniaTest

WS_ROOM = "typeclasses.winter_survival.rooms.WinterSurvivalRoom"
WS_OBJECT = "typeclasses.winter_survival.objects.WinterSurvivalObject"


class WinterSurvivalTest(EvenniaTest):
    """EvenniaTest whose rooms and objects are Winter Survival's."""
    room_typeclass = WS_ROOM
    object_typeclass = WS_OBJECT
