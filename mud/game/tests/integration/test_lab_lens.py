"""Tier-2 integration: the polysemy lab's `lens` command. Everyone lists and shows the lab
capture's lenses; researchers build one. A build takes its settings from the lab's preset, is
acknowledged at once, reports the backend's refusals, and opens the lens in the builder's app
when it's built. The backend is stubbed (ask_backend)."""
from unittest import mock

from evennia import create_object
from evennia.utils.test_resources import EvenniaTest

SESSION = "session_1434a9be"  # the polysemy lab's capture (data/labs/polysemy_tank.yaml)
LENSES = [
    {"name": "tank-k5-n15", "kind": "umap", "legacy": False, "k_per_layer": [5] * 24,
     "validation": {"best": {}}, "state": "saved"},
    {"name": "tank_polysemy_k6_n20", "kind": "umap", "legacy": True},
    {"name": "aquarium-axis", "kind": "mass_mean", "legacy": False},
]


def _texts(m):
    out = []
    for c in m.call_args_list:
        t = c.args[0] if c.args else c.kwargs.get("text")
        if isinstance(t, tuple):
            t = t[0]
        if t is not None:
            out.append(str(t))
    return "\n".join(out)


def _shown(m):
    return [c.kwargs["app_command"][0] for c in m.call_args_list if "app_command" in c.kwargs]


class TestLabLens(EvenniaTest):
    def setUp(self):
        super().setUp()
        from world.institute.build import build
        _, self.lab, _ = build(start=create_object("typeclasses.rooms.Room", key="Limbo"))
        self.char1.move_to(self.lab, quiet=True)
        self.calls = []

    def _backend(self, replies):
        """Answer each path by its prefix: a reply, a function of the call, or an error to report."""
        def ask(path, payload, on_reply, on_error):
            self.calls.append((path, payload))
            reply = next((r for prefix, r in replies.items() if path.startswith(prefix)), None)
            if isinstance(reply, Exception):
                on_error(str(reply))
            else:
                on_reply(reply(path, payload) if callable(reply) else reply)
        return mock.patch("commands.institute.commands.ask_backend", ask)

    def _run(self, line, char=None):
        char = char or self.char1
        with mock.patch.object(char, "msg") as m:
            char.execute_cmd(line)
        return m

    def test_visitors_list_and_show_lenses_but_cannot_build(self):
        self.char2.move_to(self.lab, quiet=True)
        with self._backend({"/api/sessions/": LENSES}):
            about = self._run("lens", self.char2)
            listed = self._run("lens list", self.char2)
            shown = self._run("lens show tank-k5-n15", self.char2)
            axis = self._run("lens show aquarium-axis", self.char2)
            built = self._run("lens build k=4", self.char2)
        assert "tank_polysemy_k6_n20 of session_1434a9be" in _texts(about)
        listing = _texts(listed)
        assert "tank-k5-n15|n  k 5, validated, saved" in listing and "a legacy schema" in listing
        assert _shown(shown) == [{"verb": "show", "view": {"session": SESSION, "lens": "tank-k5-n15",
                                                            "legacy": False, "workspace": "layers"}}]
        assert _shown(axis)[0]["view"]["workspace"] == "build"  # a mass-mean axis has no Sankeys
        assert "Only researchers" in _texts(built)
        assert all(path.startswith("/api/sessions/") for path, _ in self.calls)

    def test_a_build_takes_the_presets_defaults_and_opens_the_lens_when_built(self):
        states = iter([{"state": "running"}, {"state": "done"}])
        started = {"job_id": "job_1", "session_id": SESSION, "name": "lab-k4-n15"}
        with self._backend({"/api/commands": started, "/api/jobs/job_1": lambda path, payload: next(states)}), \
                mock.patch("evennia.utils.utils.delay", lambda seconds, fn, *args: fn(*args)):
            m = self._run("lens build k=4")
        path, payload = self.calls[0]
        assert path == "/api/commands" and payload == {
            "verb": "build", "by": f"mud:{self.char1.key}",
            "lens": {"session_id": SESSION, "k": 4, "n_neighbors": 15, "dimensions": 6, "name": "lab-k4-n15"}}
        assert [p for p, _ in self.calls[1:]] == ["/api/jobs/job_1", "/api/jobs/job_1"]  # followed until built
        text = _texts(m)
        assert "Asking the backend to build lab-k4-n15" in text and "in the background" in text and "is built" in text
        assert _shown(m) == [{"verb": "show", "view": {"session": SESSION, "lens": "lab-k4-n15", "legacy": False,
                                                        "workspace": "layers"}}]

    def test_refusals_and_bad_settings_are_reported(self):
        with self._backend({"/api/commands": RuntimeError("409 Lens 'lab-k5-n15' already exists")}):
            refused = self._run("lens build")
        assert "didn't build it: 409 Lens 'lab-k5-n15' already exists" in _texts(refused)
        with self._backend({}):
            bad = self._run("lens build k=five")
            unnamed = self._run("lens build n=20 as")
        assert "I don't understand 'k=five'" in _texts(bad) and "Name the lens" in _texts(unnamed)
        assert [path for path, _ in self.calls] == ["/api/commands"]  # bad settings never reach the backend
        with self._backend({"/api/sessions/": LENSES}):
            m = self._run("lens show nothing")
        assert "No lens 'nothing'" in _texts(m) and not _shown(m)
        failed = iter([{"state": "failed", "error": "a worker crashed"}])
        with self._backend({"/api/commands": {"job_id": "job_2"}, "/api/jobs/": lambda p, q: next(failed)}):
            m = self._run("lens build as my-lens")
        assert "The build of my-lens failed. a worker crashed" in _texts(m) and not _shown(m)
