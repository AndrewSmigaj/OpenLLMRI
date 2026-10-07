"""EvenniaClient against a fake MUD on a local websocket: raw mode on connect, text gathered until the
prompt and cleaned for the model, out-of-band events ignored, the timeout, and the login check."""
import json

import pytest
from websockets.asyncio.server import serve

from services.agent.evennia_client import EvenniaClient, clean_evennia_text

PROMPT = ["prompt", [">"], {}]


class FakeMud:
    """Answers each ["text", [command], {}] with scripted frames and records every frame received.
    A frame is a [cmdname, args, kwargs] list, or a plain string sent as-is (not JSON)."""

    def __init__(self, replies):
        self.replies = replies
        self.received = []

    async def handler(self, ws):
        async for raw in ws:
            msg = json.loads(raw)
            self.received.append(msg)
            if msg[0] == "text":
                frames = self.replies.get(msg[1][0], [["text", ["ok"], {}], PROMPT])
                for frame in frames:
                    await ws.send(frame if isinstance(frame, str) else json.dumps(frame))


@pytest.fixture
async def mud_session():
    """Start a fake MUD with given replies and a client connected to it; clean both up."""
    opened = []

    async def start(replies):
        fake = FakeMud(replies)
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


async def test_out_of_band_events_are_ignored(mud_session):
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


async def test_login_succeeds_when_look_shows_the_world(mud_session):
    fake, client = await mud_session({
        "connect agent-1 secret": [["text", ["You become Scout."], {}], PROMPT],
        "look": [["text", ["Limbo"], {}], PROMPT],
    })
    assert await client.authenticate("agent-1", "secret") == "You become Scout."


async def test_login_is_refused_while_the_welcome_banner_shows(mud_session):
    banner = [["text", ["Welcome to LLMud Institute. Log in with connect <username> <password>"], {}],
              PROMPT]
    fake, client = await mud_session({"connect agent-1 wrong": banner, "look": banner})
    with pytest.raises(RuntimeError, match="authentication failed"):
        await client.authenticate("agent-1", "wrong")


def test_clean_text_for_the_model():
    assert clean_evennia_text("|rDanger|n &amp; \x1b[1mbold\x1b[0m door(#7)") == "Danger & bold door"
