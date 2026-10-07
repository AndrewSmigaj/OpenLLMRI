#!/usr/bin/env python3
"""Planted-violation tests for the four gates: each still catches what it is for, and only inside its
scope (DR-29: the shell gates scan Winter Survival's own packages; the doc gate scans the docs git
tracks). Each test builds a small MUD tree in a temporary folder and runs a gate against it.
Stdlib only; `make lint` runs it after the gates.
"""
from __future__ import annotations

import contextlib
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_docs           # noqa: E402
import check_no_raw_output  # noqa: E402
import check_no_raw_writes  # noqa: E402
import check_pure_core      # noqa: E402

RAW_WRITE = "def f(obj):\n    obj.db.state = {}\n"
RAW_OUTPUT = "def f(room):\n    room.msg_contents('hello')\n"


class GateTest(unittest.TestCase):
    def tree(self, files: dict) -> pathlib.Path:
        """A temporary MUD root holding {relative path: text}."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        return root

    def run_gate(self, gate, root: pathlib.Path) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return gate.main(root)


class TestPureCore(GateTest):
    def test_catches_evennia_in_the_core(self):
        root = self.tree({"game/world/sim/rules.py": "import evennia\n"})
        self.assertEqual(self.run_gate(check_pure_core, root), 1)

    def test_catches_a_wall_clock_in_the_core(self):
        root = self.tree({"game/world/sim/rules.py": "from time import time\n"})
        self.assertEqual(self.run_gate(check_pure_core, root), 1)

    def test_the_shell_may_import_evennia(self):
        root = self.tree({"game/world/sim/rules.py": "X = 1\n",
                          "game/typeclasses/rooms.py": "import evennia\n"})
        self.assertEqual(self.run_gate(check_pure_core, root), 0)


class TestNoRawWrites(GateTest):
    def test_catches_a_raw_write_in_winter_survivals_shell(self):
        for rel in ("game/typeclasses/winter_survival/rooms.py",
                    "game/commands/winter_survival/cmd_act.py"):
            with self.subTest(rel=rel):
                self.assertEqual(self.run_gate(check_no_raw_writes, self.tree({rel: RAW_WRITE})), 1)

    def test_the_single_writer_is_allowed(self):
        root = self.tree({"game/typeclasses/winter_survival/apply.py": RAW_WRITE})
        self.assertEqual(self.run_gate(check_no_raw_writes, root), 0)

    def test_shared_and_other_areas_code_is_out_of_scope(self):
        root = self.tree({"game/typeclasses/rooms.py": RAW_WRITE,
                          "game/typeclasses/institute/lab.py": RAW_WRITE})
        self.assertEqual(self.run_gate(check_no_raw_writes, root), 0)


class TestNoRawOutput(GateTest):
    def test_catches_msg_contents_in_winter_survivals_shell(self):
        for rel in ("game/typeclasses/winter_survival/objects.py",
                    "game/commands/winter_survival/cmd_speech.py"):
            with self.subTest(rel=rel):
                self.assertEqual(self.run_gate(check_no_raw_output, self.tree({rel: RAW_OUTPUT})), 1)

    def test_shared_and_other_areas_code_is_out_of_scope(self):
        root = self.tree({"game/commands/system.py": RAW_OUTPUT,
                          "game/commands/institute/lab.py": RAW_OUTPUT})
        self.assertEqual(self.run_gate(check_no_raw_output, root), 0)


class TestDocs(GateTest):
    def git_tree(self, tracked: dict, untracked: dict) -> pathlib.Path:
        root = self.tree({**tracked, **untracked})
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "add", *tracked], check=True)
        return root

    def test_catches_a_regression_in_a_tracked_doc(self):
        root = self.git_tree({"docs/notes.md": "Objects weigh mass_kg.\n"}, {})
        self.assertEqual(self.run_gate(check_docs, root), 1)

    def test_an_untracked_file_is_not_a_doc(self):
        root = self.git_tree({"docs/notes.md": "Objects weigh mass_g.\n"},
                             {".pytest_cache/README.md": "Objects weigh mass_kg.\n"})
        self.assertEqual(self.run_gate(check_docs, root), 0)

    def test_the_allow_words_still_excuse_history(self):
        root = self.git_tree({"docs/notes.md": "The retired mass_kg field is gone.\n"}, {})
        self.assertEqual(self.run_gate(check_docs, root), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
