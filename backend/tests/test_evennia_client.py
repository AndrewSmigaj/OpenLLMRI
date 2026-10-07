"""EvenniaClient against a fake MUD on a local websocket: raw mode on connect, text gathered until the
prompt and cleaned for the model, other out-of-band messages ignored, the timeout, the control channel
and its scenario events, and the login confirmed on the control channel."""
import json

import pytest
from websockets.asyncio.server import serve

from services.agent.evennia_client import EvenniaClient, clean_evennia_text

PROMPT = ["prompt", [">"], {}]


class FakeMud:
    """Answers each ["text", [command], {}] with scripted frames and records every frame received.
    A frame is a [cmdname, args, kwargs] list, or a plain string sent as-is (not JSON)."""

    def __init__(self, replies, control=None):
        self.replies = replies
        self.control = control or {}          # control-channel cmd → its reply payload
        self.received = []

    async def handler(self, ws):
        async for raw in ws:
            msg = json.loads(raw)
            self.received.append(msg)
            if msg[0] == "text":
                frames = self.replies.get(msg[1][0], [["text", ["ok"], {}], PROMPT])
                for frame in frames:
                    await ws.send(frame if isinstance(frame, str) else json.dumps(frame))
            elif msg[0] == "scenario":
                reply = self.control.get(msg[2]["cmd"], {"ok": False, "error": "unknown"})
                await ws.send(json.dumps(["scenario", [reply], {}]))


@pytest.fixture
async def mud_session():
    """Start a fake MUD with given replies and a client connected to it; clean both up."""
    opened = []

    async def start(replies, control=None):
        fake = FakeMud(replies, control)
        server = await serve(fake.handler, "127.0.0.1", 0)
        port = next(iter(server.sockets)).getsockname()[1]
        client = EvenniaClient(f"ws://127.0.0.1:{port}")
        await client.connect()
        opened.append((server, client))
        return fake, client

    yield start
    for server, client in opened:
        await client.disconnect()
        server.close()
        await server.wait_closed()


async def test_connect_asks_for_raw_mode_first(mud_session):
    fake, client = await mud_session({})
    await client.send_command("look")
    await client.read_until_prompt(timeout=2)
    assert fake.received[0] == ["client_options", [], {"raw": True}]
    assert fake.received[1] == ["text", ["look"], {}]


async def test_text_is_gathered_until_the_prompt_and_cleaned(mud_session):
    fake, client = await mud_session({"look": [
        ["text", ["|wA |cbus stop|n (#12)"], {}],
        ["text", [" &lt;here&gt;\x1b[0m"], {}],
        PROMPT,
        ["text", ["after the prompt"], {}],
    ]})
    await client.send_command("look")
    assert await client.read_until_prompt(timeout=2) == "A bus stop  <here>"


async def test_other_out_of_band_messages_are_ignored(mud_session):
    fake, client = await mud_session({"north": [
        ["room_entered", [], {"room_type": "lab", "role": "researcher"}],
        ["text", ["You go north."], {}],
        PROMPT,
    ]})
    await client.send_command("north")
    assert await client.read_until_prompt(timeout=2) == "You go north."


async def test_a_frame_that_is_not_json_is_kept_as_text(mud_session):
    fake, client = await mud_session({"look": ["a raw banner", PROMPT]})
    await client.send_command("look")
    assert await client.read_until_prompt(timeout=2) == "a raw banner"


async def test_without_a_prompt_it_times_out_with_what_arrived(mud_session):
    fake, client = await mud_session({"wait": [["text", ["partial"], {}]]})
    await client.send_command("wait")
    assert await client.read_until_prompt(timeout=0.3) == "partial"


async def test_login_is_confirmed_on_the_control_channel(mud_session):
    fake, client = await mud_session(
        {"connect agent-1 secret": [["text", ["You become Scout."], {}], PROMPT]},
        control={"status": {"ok": True, "logged_in": True, "character": "Scout"}})
    assert await client.authenticate("agent-1", "secret") == "You become Scout."
    assert fake.received[-1] == ["scenario", [], {"cmd": "status"}]


async def test_login_fails_when_the_mud_reports_no_character(mud_session):
    fake, client = await mud_session(
        {"connect agent-1 wrong": [["text", ["Incorrect login."], {}], PROMPT]},
        control={"status": {"ok": True, "logged_in": False, "character": None}})
    with pytest.raises(RuntimeError, match="login failed"):
        await client.authenticate("agent-1", "wrong")


async def test_the_control_channel_returns_the_mud_reply(mud_session):
    loaded = {"ok": True, "scenario": "set/file", "set": "set@1", "stage": "initial"}
    fake, client = await mud_session({}, control={"load": loaded})
    assert await client.scenario("load", key="set/file", timeout=2) == loaded
    assert fake.received[-1] == ["scenario", [], {"cmd": "load", "key": "set/file"}]


async def test_scenario_events_are_kept_for_the_runner(mud_session):
    done = {"action_id": 1, "outcome": "friend"}
    fake, client = await mud_session({"help person": [
        ["text", ["You help them."], {}],
        ["stage_entered", [{"stage": "after"}], {}],
        ["room_left", [{"room_type": "hub"}], {}],
        ["scenario_complete", [done], {}],
        PROMPT,
    ]})
    await client.send_command("help person")
    assert await client.read_until_prompt(timeout=2) == "You help them."
    assert client.drain_events() == [("stage_entered", {"stage": "after"}),
                                     ("scenario_complete", done)]
    assert client.drain_events() == []


def test_clean_text_for_the_model():
    assert clean_evennia_text("|rDanger|n &amp; \x1b[1mbold\x1b[0m door(#7)") == "Danger & bold door"
