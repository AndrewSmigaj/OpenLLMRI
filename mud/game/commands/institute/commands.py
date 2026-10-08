"""game.commands.institute.commands — the simulator room's menu over the scenario library.

`simulator` lists the library's sets, or one set's scenarios; `simulate` loads a scenario, or enters a
world. Loading a staged scenario calls the same function as the backend's control channel
(typeclasses.staged.instances.load_scenario). `agent` asks the backend to run the model on scenarios
from the library: the backend owns the GPU and runs one agent at a time. In a lab, `lens` lists,
shows and builds the lab capture's lenses through the backend.
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


def _request(path: str, payload: dict | None):
    """POST JSON to the backend (GET when there's no payload) and return its reply; a refusal
    raises with the backend's reason."""
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(backend_url() + path, data=data, headers={"Content-Type": "application/json"},
                                     method="GET" if data is None else "POST")
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


def ask_backend(path: str, payload: dict | None, on_reply, on_error) -> None:
    """Call the backend off the server's thread (a GET when `payload` is None); the callbacks run
    back on it."""
    from twisted.internet.threads import deferToThread
    deferred = deferToThread(_request, path, payload)
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


LENS_POLL_S = 3  # seconds between checks on a build
LENS_POLL_LIMIT = 400  # checks before giving up on following it (20 minutes)


def open_in_app(character, session: str, lens: str, legacy: bool, workspace: str = "layers") -> None:
    """Show a lens in this character's app (the app's `app_command`, DESIGN.md E7)."""
    view = {"session": session, "lens": lens, "legacy": legacy, "workspace": workspace}
    character.msg(app_command=[{"verb": "show", "view": view}])


def follow_build(character, job_id: str, session: str, name: str, polls: int = 0) -> None:
    """Check a build until it ends; then tell the builder, and open the lens in their app."""
    from evennia.utils.utils import delay

    def seen(job: dict) -> None:
        state = job.get("state")
        if state == "done":
            character.msg(f"Lens |w{name}|n is built.")
            open_in_app(character, session, name, legacy=False)
        elif state in ("failed", "cancelled", "interrupted"):
            character.msg(f"The build of {name} {state}. {job.get('error') or ''}".strip())
        elif polls >= LENS_POLL_LIMIT:
            character.msg(f"Still building {name}; |wlens list|n shows it once it's done.")
        else:
            delay(LENS_POLL_S, follow_build, character, job_id, session, name, polls + 1)

    ask_backend(f"/api/jobs/{job_id}", None, seen,
                lambda reason: character.msg(f"Lost track of the build of {name}: {reason}"))


def _lens_line(lens: dict) -> str:
    """One lens in `lens list`."""
    if lens.get("legacy"):
        return f"  |w{lens['name']}|n  a legacy schema"
    if lens.get("kind") == "mass_mean":
        return f"  |w{lens['name']}|n  a mass-mean axis"
    ks = sorted(set(lens.get("k_per_layer") or []))
    k = f"k {ks[0]}" if len(ks) == 1 else (f"k {ks[0]} to {ks[-1]}" if ks else "k ?")
    marks = [m for m, on in (("validated", lens.get("validation")), ("saved", lens.get("state") == "saved")) if on]
    return f"  |w{lens['name']}|n  {k}" + (f", {', '.join(marks)}" if marks else "")


def build_settings(text: str, defaults: dict) -> dict:
    """`k=5 n=15 dims=6 as <name>` over the lab's defaults, as the backend's build takes them."""
    settings = {"k": int(defaults.get("k", 5)), "n_neighbors": int(defaults.get("n_neighbors", 15)),
                "dimensions": int(defaults.get("dimensions", 6))}
    words, name = text.split(), None
    if "as" in words:
        at = words.index("as")
        if at + 1 >= len(words):
            raise ValueError("Name the lens after |was|n.")
        name, words = words[at + 1], words[:at] + words[at + 2:]
    keys = {"k": "k", "n": "n_neighbors", "dims": "dimensions"}
    for word in words:
        key, eq, value = word.partition("=")
        if not eq or key not in keys or not value.isdigit():
            raise ValueError(f"I don't understand {word!r}: use k=, n=, dims= and |was <name>|n.")
        settings[keys[key]] = int(value)
    dims = "" if settings["dimensions"] == 6 else f"-d{settings['dimensions']}"
    settings["name"] = name or f"lab-k{settings['k']}-n{settings['n_neighbors']}{dims}"
    return settings


class CmdLens(Command):
    """The lab's lenses, through the backend.

    Usage:
      lens                                        what the lab shows
      lens list                                   the lab capture's lenses
      lens show <name>                            open one in your app
      lens build [k=] [n=] [dims=] [as <name>]    build one in the background (researchers)

    A build's defaults come from the lab's preset: k, the UMAP neighbours (n) and its dimensions
    (dims). Your app opens the lens when it's built.
    """
    key = "lens"
    locks = "cmd:all()"

    def func(self):
        room = self.caller.location
        preset = room.preset() if hasattr(room, "preset") else {}
        session = preset.get("session_id")
        if not session:
            self.caller.msg("This room shows no capture.")
            return
        verb, _, rest = self.args.strip().partition(" ")
        if not verb:
            self.caller.msg(f"This lab shows {preset.get('clustering_schema') or 'a capture'} of {session}. "
                            "|wlens list|n, |wlens show <name>|n, |wlens build [k=] [n=] [dims=] [as <name>]|n")
        elif verb == "list":
            self._listed(session, self._list)
        elif verb == "show" and rest.strip():
            self._listed(session, lambda lenses: self._show(session, rest.strip(), lenses))
        elif verb == "build":
            self._build(session, preset, rest.strip())
        else:
            self.caller.msg("Usage: |wlens|n, |wlens list|n, |wlens show <name>|n or "
                            "|wlens build [k=] [n=] [dims=] [as <name>]|n")

    def _listed(self, session: str, then) -> None:
        caller = self.caller
        ask_backend(f"/api/sessions/{session}/lenses", None, then,
                    lambda reason: caller.msg(f"The backend didn't answer: {reason}"))

    def _list(self, lenses: list) -> None:
        lines = [_lens_line(lens) for lens in lenses]
        self.caller.msg("\n".join(["The lab capture's lenses:", *lines]) if lines else "No lenses on this capture yet.")

    def _show(self, session: str, name: str, lenses: list) -> None:
        found = next((lens for lens in lenses if lens.get("name") == name), None)
        if found is None:
            self.caller.msg(f"No lens {name!r} here: |wlens list|n shows them.")
            return
        open_in_app(self.caller, session, name, bool(found.get("legacy")),
                    workspace="build" if found.get("kind") == "mass_mean" else "layers")
        self.caller.msg(f"Opening {name} in your app.")

    def _build(self, session: str, preset: dict, rest: str) -> None:
        caller = self.caller
        if role_of(caller) != "researcher":
            caller.msg("Only researchers can build lenses. |wlens show <name>|n opens one.")
            return
        try:
            settings = build_settings(rest, preset.get("lens_defaults") or {})
        except ValueError as err:
            caller.msg(str(err))
            return
        name = settings["name"]
        payload = {"verb": "build", "by": f"mud:{caller.key}", "lens": {"session_id": session, **settings}}

        def started(reply: dict) -> None:
            caller.msg(f"Building |w{name}|n in the background; your app opens it when it's built.")
            follow_build(caller, reply["job_id"], reply.get("session_id") or session, name)

        caller.msg(f"Asking the backend to build {name} (k {settings['k']}, n {settings['n_neighbors']}, "
                   f"dims {settings['dimensions']})...")
        ask_backend("/api/commands", payload, started, lambda reason: caller.msg(f"The backend didn't build it: {reason}"))
