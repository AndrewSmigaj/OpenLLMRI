"""game.commands.institute.commands — the simulator room's menu over the scenario library.

`simulator` lists the library's sets, or one set's scenarios; `simulate` loads a scenario, or enters a
world. Loading a staged scenario calls the same function as the backend's control channel
(typeclasses.staged.instances.load_scenario).
"""
from __future__ import annotations

import importlib

from commands.command import Command
from typeclasses.institute.rooms import role_of
from world.staged import library
from world.staged.scenario import ScenarioError

USAGE = "Type |wsimulator <set>|n for a set's scenarios, |wsimulate <set>[/<subset>] [<scenario>]|n to load one."


def _spec(text: str) -> tuple[str, str | None, str | None]:
    """'<set>[/<subset>] [<scenario>]' → (set, subset, scenario)."""
    words = text.split()
    set_id, _, subset = words[0].partition("/")
    return set_id, subset or None, words[1] if len(words) > 1 else None


def world_start_room(sset):
    """The room a player enters a world set in: its MUD package's build.start_room()."""
    return importlib.import_module(f"world.scenarios.{sset.manifest['world']}.build").start_room()


class CmdSimulator(Command):
    """List the scenario library's sets, or the scenarios in one of them.

    Usage:
      simulator
      simulator <set>[/<subset>]
    """
    key = "simulator"
    locks = "cmd:all()"

    def func(self):
        if not self.args.strip():
            self.caller.msg(self._sets())
            return
        set_id, subset, _ = _spec(self.args)
        try:
            sset = library.load_set(set_id)
            if sset.kind != "staged":
                self.caller.msg(f"{sset.ref} is a {sset.kind}: |wsimulate {sset.id}|n enters it.")
                return
            keys = sset.keys(subset)
        except ScenarioError as err:
            self.caller.msg(str(err))
            return
        where = f"{sset.ref}/{subset}" if subset else sset.ref
        lines = [f"{where}: {len(keys)} scenarios"] + [f"  {k.partition('/')[2]}" for k in keys]
        self.caller.msg("\n".join(lines))

    @staticmethod
    def _sets() -> str:
        lines = ["The scenario library:"]
        for s in library.list_sets():
            size = f"{len(s.keys())} scenarios" if s.kind == "staged" else ""
            lines.append(f"  {s.ref:<28} {s.kind:<10} {size:<14} {s.manifest.get('title', '')}".rstrip())
            subsets = s.manifest.get("subsets") or {}
            if subsets:
                lines.append("      subsets: " + ", ".join(f"{n} ({len(v)})" for n, v in subsets.items()))
        lines.append(USAGE)
        return "\n".join(lines)


class CmdSimulate(Command):
    """Load a scenario from the library and go there, or enter a world. For researchers.

    Usage:
      simulate <set>                 the set's first scenario, or the world
      simulate <set>/<subset>        the subset's first scenario
      simulate <set> <scenario>      one scenario, by its file name

    In a staged scenario, |wleave|n brings you back here.
    """
    key = "simulate"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        if role_of(caller) != "researcher":
            caller.msg("Only researchers can load scenarios. |wsimulator|n shows what the library holds.")
            return
        if not self.args.strip():
            caller.msg(USAGE)
            return
        set_id, subset, name = _spec(self.args)
        try:
            sset = library.load_set(set_id)
            if sset.kind == "staged":
                self._staged(sset, subset, name)
            elif sset.kind == "world" and not (subset or name):
                caller.move_to(world_start_room(sset), move_type="teleport")
            elif sset.kind == "world":
                caller.msg(f"{sset.ref} is a world: |wsimulate {sset.id}|n enters it.")
            else:
                caller.msg(f"{sset.ref}: {sset.kind} sets can't be played yet.")
        except ScenarioError as err:
            caller.msg(str(err))

    def _staged(self, sset, subset, name):
        from typeclasses.staged.instances import load_scenario
        keys = sset.keys(subset)
        if not keys:
            raise ScenarioError(f"{sset.ref}: no scenarios")
        key = keys[0] if name is None else f"{sset.id}/{name}"
        if key not in keys:
            raise ScenarioError(f"{sset.ref}{'/' + subset if subset else ''}: no scenario {name!r}")
        room, _ = load_scenario(self.caller, key)
        self.caller.msg(room.return_appearance(self.caller))
