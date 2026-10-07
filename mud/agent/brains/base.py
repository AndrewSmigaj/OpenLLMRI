"""The single interface every brain implements (design §3.3 / §41).

The bot is a *participant*, not an authored NPC. Design §3.3 forbids autonomous
in-scenario NPCs; this bot sidesteps that by logging into a normal player account
and acting through the exact same commands a human uses. The deterministic engine
still owns every piece of state (design §41) — a brain only decides what command to
issue next:

    observation (str)  ->  next MUD command (str)

Implementations live alongside this file, all behind this one method:
  - ScriptedBrain : deterministic, zero-dependency (fuzz / playtest, design §42 Pass 10)
  - TorchBrain    : the user's OSS-20B weights via torch (the data-collection target)
  - ClaudeBrain   : lets Claude play the MUD, for testing
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Brain(ABC):
    """Abstract policy mapping a single observation to a single MUD command."""

    @abstractmethod
    def act(self, observation: str) -> str:
        """Return the next MUD command line for ``observation``.

        Args:
            observation: Text the MUD sent back — either prose ``look`` output or a
                structured observation string (see ``runner.py``). May be empty.

        Returns:
            One command line, with no trailing newline, e.g. ``"look"``, ``"north"``,
            ``"examine seatbelt"``. The runner sends it to the MUD verbatim.
        """
        raise NotImplementedError
