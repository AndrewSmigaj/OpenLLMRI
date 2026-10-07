"""game.commands.institute.commands — the simulator room's menu over the scenario library.

`simulator` lists the library's sets, or one set's scenarios; `simulate` loads a scenario, or enters a
world. Loading a staged scenario calls the same function as the backend's control channel
(typeclasses.staged.instances.load_scenario). `agent` asks the backend to run the model on scenarios
from the library: the backend owns the GPU and runs one agent at a time.
"""
from __future__ import annotations

import importlib
import json
import os
import time
import urllib.error
import urllib.request

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

    A staged scenario starts by showing what the agent sees at its start: the room, what you carry
    and the choices. Type a choice's command to take it; |wleave|n brings you back here.
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
        # What the agent reads at a scenario's start: the backend's runner types look, inventory and
        # actions first.
        self.caller.msg("\n".join([room.return_appearance(self.caller), room.inventory_text(),
                                   room.actions_text()]))


# --- running the model as an agent, through the backend ------------------------------------------

def backend_url() -> str:
    """The backend's API; from the MUD's container the host is host.docker.internal (compose)."""
    return os.environ.get("BACKEND_URL", "http://host.docker.internal:8000").rstrip("/")


def agent_name() -> str:
    """The character the backend's runner plays (its account is EVENNIA_AGENT_USER)."""
    return os.environ.get("EVENNIA_AGENT_USER") or "agent"


class BackendError(Exception):
    pass


def _post(path: str, payload: dict) -> dict:
    """POST JSON to the backend and return its reply; a refusal raises with the backend's reason."""
    request = urllib.request.Request(backend_url() + path, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as reply:
            return json.loads(reply.read().decode())
    except urllib.error.HTTPError as err:
        try:
            detail = json.loads(err.read().decode()).get("detail", "")
        except (ValueError, AttributeError):
            detail = ""
        raise BackendError(f"{err.code} {detail}".strip()) from err
    except urllib.error.URLError as err:
        raise BackendError(f"can't reach the backend at {backend_url()} ({err.reason})") from err


def ask_backend(path: str, payload: dict, on_reply, on_error) -> None:
    """Call the backend off the server's thread; the callbacks run back on it."""
    from twisted.internet.threads import deferToThread
    deferred = deferToThread(_post, path, payload)
    deferred.addCallbacks(on_reply, lambda failure: on_error(str(failure.value)))


class CmdAgent(Command):
    """Run the model as an agent on scenarios from the library, or stop it. For researchers.

    Usage:
      agent run <set>[/<subset>] [<scenario>]
      agent stop

    The backend plays the scenarios with the model and captures its activations, one agent at a
    time. |wwatch <agent>|n follows it from scenario to scenario.
    """
    key = "agent"
    locks = "cmd:all()"

    def func(self):
        if role_of(self.caller) != "researcher":
            self.caller.msg("Only researchers can run agents. You can |wwatch|n one.")
            return
        verb, _, rest = self.args.strip().partition(" ")
        if verb == "run" and rest.strip():
            self._run(rest.strip())
        elif verb == "stop":
            self._stop(rest.strip())
        else:
            self.caller.msg("Usage: |wagent run <set>[/<subset>] [<scenario>]|n or |wagent stop|n")

    def _run(self, spec: str) -> None:
        caller = self.caller
        set_id, subset, name = _spec(spec)
        try:
            sset = library.load_set(set_id)
            if sset.kind != "staged":
                raise ScenarioError(f"{sset.ref} is a {sset.kind}: agents play staged sets for now")
            keys = sset.keys(subset)
            if name is not None:
                key = f"{sset.id}/{name}"
                if key not in keys:
                    raise ScenarioError(f"{sset.ref}: no scenario {name!r}")
                keys = [key]
            if not keys:
                raise ScenarioError(f"{sset.ref}: no scenarios")
            target_words = list(library.load(keys[0]).scenario.target_words)
        except ScenarioError as err:
            caller.msg(str(err))
            return
        payload = {
            "session_name": f"mud_{sset.id}{'_' + subset if subset else ''}_{time.strftime('%Y%m%d_%H%M%S')}",
            "scenario_id": sset.id, "target_words": target_words, "scenario_list": keys,
            "auto_start": True,
        }

        def started(reply: dict) -> None:
            caller.db.agent_session = reply.get("session_id")
            caller.msg(f"Agent session {reply.get('session_id')} started on {len(keys)} scenario(s). "
                       f"|wwatch {agent_name()}|n follows it.")

        caller.msg(f"Asking the backend to run the agent on {len(keys)} scenario(s)...")
        ask_backend("/api/agent/start", payload, started,
                    lambda reason: caller.msg(f"The backend didn't start it: {reason}"))

    def _stop(self, session_id: str) -> None:
        caller = self.caller
        session_id = session_id or caller.db.agent_session
        if not session_id:
            caller.msg("Which session? |wagent stop <session_id>|n")
            return

        def stopped(reply: dict) -> None:
            caller.attributes.remove("agent_session")
            caller.msg(f"Agent session {session_id} stopped after {reply.get('total_turns')} turns.")

        ask_backend("/api/agent/stop", {"session_id": session_id}, stopped,
                    lambda reason: caller.msg(f"The backend didn't stop it: {reason}"))
