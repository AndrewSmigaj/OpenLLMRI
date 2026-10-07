"""Tier-2 integration: one MUD, many areas.

Winter Survival's behaviour lives in its own room and object classes. A character crosses areas,
so the room it stands in decides its commands and how it looks: inside Winter Survival's rooms it has
the six commands; in a plain room, the institute's kind, stock Evennia only. Every input, a command,
an unknown word or nothing at all, ends with a prompt: the marker a client reads as "this command's
output is complete".
"""
from unittest import mock

from django.conf import settings
from evennia import create_object
from evennia.utils.test_resources import EvenniaTest
from evennia.utils.utils import class_from_module

from tests.integration.base import WS_OBJECT, WS_ROOM

GRAMMAR_HELP = "i don't know how to do that"     # Winter Survival's answer to an unknown word
THE_SIX = {"CmdAction", "CmdNoMatch", "CmdDrop", "CmdLook", "CmdInventory", "CmdSpeak"}
WS_COMMANDS = "commands.winter_survival"          # the package of Winter Survival's commands


def _texts(m):
    out = []
    for c in m.call_args_list:
        t = c.args[0] if c.args else c.kwargs.get("text")
        if isinstance(t, tuple):
            t = t[0]
        if t is not None:
            out.append(str(t))
    return " ".join(out).lower()


def _prompted(m):
    return any("prompt" in c.kwargs for c in m.call_args_list)


class TestAreas(EvenniaTest):
    """room1 and room2 are plain rooms (the institute's kind); self.ws is a Winter Survival room."""

    def setUp(self):
        super().setUp()
        from world.scenarios.winter_survival import content
        content.load()
        self.ws = create_object(WS_ROOM, key="crash cabin")

    def _run(self, line):
        with mock.patch.object(self.char1, "msg") as m:
            self.char1.execute_cmd(line)
        return m

    def _commands(self):
        """(Winter Survival's command names, all command names) the character has where it stands.
        Stock Evennia has its own CmdLook/CmdDrop/CmdInventory, so ours are told apart by module."""
        self.char1.at_cmdset_get()
        cmds = self.char1.cmdset.current.commands
        ours = {type(c).__name__ for c in cmds if type(c).__module__.startswith(WS_COMMANDS)}
        return ours, {type(c).__name__ for c in cmds}

    def test_a_plain_room_offers_stock_commands_only(self):
        said = _texts(self._run("xyzzy the frobnicator"))
        assert GRAMMAR_HELP not in said, "Winter Survival's grammar help must not answer outside its rooms"
        assert "command 'xyzzy the frobnicator' is not available." in said, "Evennia's own reply"
        ours, names = self._commands()
        assert not ours and "CmdGet" in names

    def test_a_character_in_a_winter_survival_room_has_its_six_commands(self):
        self.char1.move_to(self.ws, quiet=True)
        ours, names = self._commands()
        assert ours == THE_SIX
        assert "CmdGet" not in names, "the taught `take` owns get/grab (DR-24)"
        assert self.char1.cmdset.cmdset_stack[0].path.startswith(WS_COMMANDS)
        assert GRAMMAR_HELP in _texts(self._run("xyzzy the frobnicator"))

    def test_a_plain_room_shows_its_description(self):
        self.room1.db.desc = "A bright, quiet hall."
        assert "a bright, quiet hall." in _texts(self._run("look"))

    def test_walking_between_areas_switches_the_commands(self):
        assert GRAMMAR_HELP not in _texts(self._run("xyzzy"))
        self.char1.move_to(self.ws, quiet=True)
        assert GRAMMAR_HELP in _texts(self._run("xyzzy"))
        self.char1.move_to(self.room1, quiet=True)
        assert GRAMMAR_HELP not in _texts(self._run("xyzzy"))

    def test_a_character_looks_the_way_its_area_renders_it(self):
        self.char1.move_to(self.ws, quiet=True)
        assert "bare to the wind" in _texts(self._run("look me")), "Winter Survival's warmth self-view"
        self.char1.move_to(self.room1, quiet=True)
        assert "bare to the wind" not in _texts(self._run("look me")), "stock Evennia outside it"

    def test_objects_built_or_minted_in_winter_survival_are_its_objects(self):
        from typeclasses.winter_survival.objects import WinterSurvivalObject
        from typeclasses.winter_survival.rooms import WinterSurvivalRoom
        from world.scenarios.winter_survival.build import build
        room = build()
        assert isinstance(room, WinterSurvivalRoom)
        built, frontier = [], list(room.contents)
        while frontier:                                   # most loot is nested: walk the tree
            o = frontier.pop()
            built.append(o)
            frontier.extend(o.contents)
        assert built and all(isinstance(o, WinterSurvivalObject) for o in built)

        create_object(WS_OBJECT, key="whisky bottle", location=self.ws, aliases=["bottle"],
                      attributes=[("sim_id", "bottle"), ("materials", ["glass"]),
                                  ("mass_g", 500), ("state", {})])
        self.char1.move_to(self.ws, quiet=True)
        self._run("break the bottle")
        shards = [o for o in self.ws.contents if str(o.db.sim_id).startswith("bottle:shard")]
        assert len(shards) == 3 and all(isinstance(o, WinterSurvivalObject) for o in shards)

    def test_every_command_ends_with_a_prompt(self):
        # By behaviour: a stock command, a stock emote, an unknown word and empty input, in both
        # kinds of room.
        for room in (self.room1, self.ws):
            self.char1.move_to(room, quiet=True)
            for line in ("look", "emote waves", "xyzzy", ""):
                assert _prompted(self._run(line)), f"{line!r} in {room.key} sent no prompt"
        # By structure: every command a character (in either kind of room), an account, a session,
        # an exit or the login screen offers inherits the prompt.
        from commands.command import PromptMixin
        exit_ = create_object(settings.BASE_EXIT_TYPECLASS, key="north", location=self.room1,
                              destination=self.room2)
        exit_.at_cmdset_get()
        sets = [self.account.cmdset.current, self.session.cmdset.current, exit_.cmdset.current,
                class_from_module(settings.CMDSET_UNLOGGEDIN)()]
        for room in (self.room1, self.ws):
            self.char1.move_to(room, quiet=True)
            self.char1.at_cmdset_get()
            sets.append(self.char1.cmdset.current)
        missing = sorted({type(c).__name__ for s in sets for c in s.commands
                          if not isinstance(c, PromptMixin)})
        assert not missing, f"commands that send no prompt: {missing}"
