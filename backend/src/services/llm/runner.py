"""Runs an analyst: one `claude -p` call (DESIGN.md E8), on the Claude subscription.

The prompt goes on stdin, from an empty working folder, with no tools, no customizations
(`--safe-mode`: no CLAUDE.md, skills, hooks or plugins), no saved session, and nobody to answer
permission prompts. The environment is an allowlist without ANTHROPIC_API_KEY, so the CLI uses
the subscription's login, not the API key the backend's .env sets. The answer is the JSON that
`--json-schema` asks for, read from the result's `structured_output`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol

ENV_ALLOWED = ("PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "TERM", "TMPDIR",
               "XDG_CONFIG_HOME", "XDG_RUNTIME_DIR", "CLAUDE_CONFIG_DIR")
TIMEOUT_S = 300.0


@dataclass
class RunResult:
    output: Optional[Dict[str, Any]]  # the structured answer; None when the run failed
    model: str = ""
    error: Optional[str] = None
    seconds: float = 0.0
    safety_stops: int = 0
    session_id: str = ""


class Runner(Protocol):
    def run(self, prompt: str, schema: Dict[str, Any]) -> RunResult: ...


def analyst_env() -> Dict[str, str]:
    """The environment a run gets: an allowlist, so no API key reaches it."""
    return {key: os.environ[key] for key in ENV_ALLOWED if key in os.environ}


class ClaudeRunner:
    """Real runs through the `claude` CLI; `model` picks one (the CLI's default otherwise)."""

    def __init__(self, model: Optional[str] = None, timeout: float = TIMEOUT_S) -> None:
        self.model, self.timeout = model, timeout

    def command(self, schema: Dict[str, Any]) -> List[str]:
        binary = shutil.which("claude", path=analyst_env().get("PATH")) or "claude"
        command = [binary, "-p", "--output-format", "json", "--json-schema", json.dumps(schema),
                   "--tools", "", "--safe-mode", "--no-session-persistence", "--permission-prompts", "none"]
        return command + (["--model", self.model] if self.model else [])

    def run(self, prompt: str, schema: Dict[str, Any]) -> RunResult:
        started = time.time()
        with tempfile.TemporaryDirectory(prefix="analyst-") as folder:
            try:
                done = subprocess.run(self.command(schema), input=prompt, capture_output=True, text=True,
                                      cwd=folder, env=analyst_env(), timeout=self.timeout)
            except subprocess.TimeoutExpired:
                return RunResult(None, error=f"no answer within {self.timeout:.0f} s", seconds=time.time() - started)
            except OSError as e:
                return RunResult(None, error=f"couldn't start claude: {e}", seconds=time.time() - started)
        return parse_result(done.returncode, done.stdout, done.stderr, time.time() - started)


def parse_result(code: int, stdout: str, stderr: str, seconds: float) -> RunResult:
    """A run's JSON result: the structured answer, or why there is none."""
    try:
        record = json.loads(stdout)
    except json.JSONDecodeError:
        tail = " ".join((stderr or stdout).split())[-300:]
        return RunResult(None, error=f"claude exited {code} without a JSON result: {tail}", seconds=seconds)
    model = next(iter(record.get("modelUsage") or {}), "")
    stops = int(record.get("safety_stops") or 0)
    session = str(record.get("session_id") or "")
    output = record.get("structured_output")
    if record.get("is_error") or record.get("subtype") != "success" or not isinstance(output, dict):
        reason = str(record.get("result") or record.get("subtype") or "no structured answer")
        return RunResult(None, model=model, error=reason[:300], seconds=seconds, safety_stops=stops, session_id=session)
    return RunResult(output, model=model, seconds=seconds, safety_stops=stops, session_id=session)


@dataclass
class FakeRunner:
    """For tests: answers from a function of the prompt and schema, and keeps every prompt."""

    answer: Callable[[str, Dict[str, Any]], Optional[Dict[str, Any]]]
    model: str = "fake-model"
    prompts: List[str] = field(default_factory=list)

    def run(self, prompt: str, schema: Dict[str, Any]) -> RunResult:
        self.prompts.append(prompt)
        output = self.answer(prompt, schema)
        return RunResult(output, model=self.model, error=None if output is not None else "the fake declined")
