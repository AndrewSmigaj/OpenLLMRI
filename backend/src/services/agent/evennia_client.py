"""
Async WebSocket client for Evennia.

Speaks the same JSON protocol as the React frontend (useEvennia.ts):
  Send: ["text", ["command"], {}]
  Recv: ["text", ["..."], {}] / ["prompt", [">"], {}]

and the MUD's control channel (docs/architecture/one-mud.md §6):
  Send: ["scenario", [], {"cmd": "status" | "load" | "end", ...}]
  Recv: ["scenario", [{ok, error, logged_in, character, room, ...}], {}]
  Recv: ["stage_entered", [{...}], {}] / ["scenario_complete", [{...}], {}]

Handles auth, ANSI stripping, and message accumulation.
"""

import asyncio
import html
import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple, cast

import websockets

logger = logging.getLogger(__name__)

# ANSI escape sequences (cursor control, colors, bell)
_ANSI_RE = re.compile(r'\033\[[0-9;]*[mKHJ]|\007')
# Evennia markup codes: |c, |n, |w, |[R, etc. (same pattern as frontend evenniaAnsi.ts)
_EVENNIA_MARKUP_RE = re.compile(r'\|\[[a-zA-Z]|\|[rgybmcwxRGYBMCWXnuis*^]')


_DBREF_RE = re.compile(r'\(#\d+\)')

# The scenario events the runner records; other out-of-band messages (room_entered, …) are ignored.
SCENARIO_EVENTS = ("stage_entered", "scenario_complete")


def _payload(args: List[Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """A structured message carries its payload as the first argument."""
    return args[0] if args and isinstance(args[0], dict) else dict(kwargs)


def clean_evennia_text(text: str) -> str:
    """Clean Evennia WebSocket text for model consumption.

    Decodes HTML entities, strips Evennia color codes, strips ANSI escapes,
    strips Evennia dbrefs like (#20).
    """
    text = html.unescape(text)
    text = _EVENNIA_MARKUP_RE.sub('', text)
    text = _ANSI_RE.sub('', text)
    text = _DBREF_RE.sub('', text)
    return text


class EvenniaClient:
    """Async WebSocket client for Evennia, matching the frontend protocol."""

    def __init__(self, url: str = "ws://localhost:4002"):
        self.url = url
        self.ws: Optional[websockets.ClientConnection] = None
        self._text_buffer: asyncio.Queue[Optional[str]] = asyncio.Queue()
        self._scenario_replies: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self._events: List[Tuple[str, Dict[str, Any]]] = []
        self._reader_task: Optional[asyncio.Task[None]] = None

    async def connect(self) -> None:
        """Connect to Evennia and set raw mode."""
        self.ws = await websockets.connect(self.url)
        # Request raw ANSI mode (same as frontend)
        await self.ws.send(json.dumps(["client_options", [], {"raw": True}]))
        # Start background reader
        self._reader_task = asyncio.create_task(self._read_loop())
        logger.info(f"Connected to Evennia at {self.url}")

    async def _read_loop(self) -> None:
        """Read messages, route text to buffer, track special messages."""
        try:
            async for raw_msg in cast("websockets.ClientConnection", self.ws):
                try:
                    msg = json.loads(raw_msg)
                    cmdname, args = msg[0], msg[1] if len(msg) > 1 else []
                    kwargs = msg[2] if len(msg) > 2 and isinstance(msg[2], dict) else {}

                    if cmdname == "text":
                        text = "".join(str(a) for a in args)
                        await self._text_buffer.put(text)
                    elif cmdname == "prompt":
                        await self._text_buffer.put(None)  # sentinel for prompt
                    elif cmdname == "scenario":
                        await self._scenario_replies.put(_payload(args, kwargs))
                    elif cmdname in SCENARIO_EVENTS:
                        self._events.append((cmdname, _payload(args, kwargs)))
                    # other OOB messages (room_entered, room_left, logged_in, …) are ignored
                except (json.JSONDecodeError, IndexError):
                    # Non-JSON or malformed — treat as raw text
                    await self._text_buffer.put(str(raw_msg))
        except websockets.ConnectionClosed:
            logger.info("Evennia WebSocket connection closed")
        except asyncio.CancelledError:
            pass

    async def authenticate(self, username: str, password: str) -> str:
        """Log in to Evennia and confirm it on the control channel: `status` must report a
        logged-in session playing a character. Raises RuntimeError otherwise."""
        await self.send_command(f"connect {username} {password}")
        welcome = await self.read_until_prompt(timeout=10.0)
        status = await self.scenario("status", timeout=10.0)
        if not status.get("logged_in") or not status.get("character"):
            raise RuntimeError(
                f"Evennia login failed for {username!r}: the MUD reports logged_in="
                f"{status.get('logged_in')}, character={status.get('character')!r}. Check "
                "EVENNIA_AGENT_USER / EVENNIA_AGENT_PASS in the root .env, and that `make accounts` "
                "in mud/ has created the account."
            )
        logger.info(f"Authenticated as {username}, playing {status['character']}")
        return welcome

    async def scenario(self, cmd: str, timeout: float = 30.0, **kwargs: Any) -> Dict[str, Any]:
        """Send a control-channel command (status, load, end) and return the MUD's reply."""
        if self.ws is None:
            raise RuntimeError("not connected")
        await self.ws.send(json.dumps(["scenario", [], {"cmd": cmd, **kwargs}]))
        return await asyncio.wait_for(self._scenario_replies.get(), timeout=timeout)

    def drain_events(self) -> List[Tuple[str, Dict[str, Any]]]:
        """The scenario events received since the last call (stage_entered, scenario_complete)."""
        events, self._events = self._events, []
        return events

    async def send_command(self, text: str) -> None:
        """Send a text command to Evennia."""
        if self.ws:
            await self.ws.send(json.dumps(["text", [text], {}]))

    async def read_until_prompt(self, timeout: float = 30.0) -> str:
        """Read text messages until a prompt arrives or timeout.

        Evennia sends text fragments followed by a prompt message.
        Accumulates all text, returns concatenated result with ANSI stripped.
        """
        accumulated = []
        try:
            deadline = asyncio.get_event_loop().time() + timeout
            while True:
                remaining = deadline - asyncio.get_event_loop().time()
                if remaining <= 0:
                    logger.warning("read_until_prompt timed out")
                    break
                item = await asyncio.wait_for(self._text_buffer.get(), timeout=remaining)
                if item is None:  # prompt sentinel
                    break
                accumulated.append(item)
        except asyncio.TimeoutError:
            logger.warning("read_until_prompt timed out waiting for text")

        return clean_evennia_text("".join(accumulated))

    async def disconnect(self) -> None:
        """Send quit and close the WebSocket connection."""
        if self.ws:
            try:
                await self.send_command("quit")
                await asyncio.sleep(0.3)
            except Exception:
                pass
        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass
            self._reader_task = None
        if self.ws:
            await self.ws.close()
            self.ws = None
        logger.info("Disconnected from Evennia")
