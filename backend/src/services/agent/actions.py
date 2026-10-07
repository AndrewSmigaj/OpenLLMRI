"""Where an agent's actions come from.

- ModelActions: the model plays. Each turn it renders the conversation in the harmony chat template
  with the session's pinned date, generates with the capture hooks off, keeps the channel markers so
  the channels parse, and captures the residual stream at the target words with one forward pass
  over prompt + generation.
- ScriptedActions: fixed commands for each scenario run; no model, no GPU, no capture. It drives the
  same loop (the bootstrap, the turn order, the control channel), so scenarios can be checked
  without the GPU.
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Protocol, Sequence, cast

from services.agent.harmony_parser import parse_harmony_channels

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

    from services.agent.scenario_library import LibraryScenario
    from services.probes.integrated_capture_service import IntegratedCaptureService

MODEL_IDENTITY = "You are an agent exploring a world."
MAX_NEW_TOKENS = 800
_DATE_LINE = re.compile(r"Current date: \d{4}-\d{2}-\d{2}")


@dataclass
class Turn:
    """What an action source sees on one tick."""
    session_id: str
    scenario: "LibraryScenario"
    tick: int
    messages: List[Dict[str, str]]      # the conversation so far; the last is the game text
    target_words: List[str]


@dataclass
class Act:
    """One tick's action, with what the model wrote and what the capture recorded."""
    action: str
    analysis: str = ""
    generated_text: str = ""
    target_positions: Dict[str, List[int]] = field(default_factory=dict)
    probes_written: int = 0
    total_tokens: int = 0


class ActionSource(Protocol):
    def begin(self, scenario: "LibraryScenario") -> None:
        """A scenario run starts."""

    async def act(self, turn: Turn) -> Optional[Act]:
        """The next action, or None when there is nothing left to do."""


def harmony_token_ids(tokenizer: "PreTrainedTokenizerBase", messages: List[Dict[str, str]],
                      add_generation_prompt: bool, pin_date: str) -> List[int]:
    """The conversation in the harmony chat template with its "Current date:" line pinned, so a
    run on another day sends the same tokens. Rendered as text and re-encoded, as the sentence
    experiments pin their date (api/routers/probes.py)."""
    text = cast(str, tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=add_generation_prompt,
        model_identity=MODEL_IDENTITY,
    ))
    text = _DATE_LINE.sub(f"Current date: {pin_date}", text)
    return cast(List[int], tokenizer.encode(text, add_special_tokens=False))


class ModelActions:
    """The model plays, and every turn is captured."""

    def __init__(self, service: "IntegratedCaptureService", pin_date: str):
        self.service = service
        self.pin_date = pin_date

    def begin(self, scenario: "LibraryScenario") -> None:
        pass

    async def act(self, turn: Turn) -> Act:
        tokenizer = self.service.orchestrator.tokenizer
        prompt_ids = harmony_token_ids(tokenizer, turn.messages, True, self.pin_date)

        # Generate with the hooks off. The channel markers are special tokens: keep them, or the
        # parser finds no channels and the whole output would be sent to the MUD as the action.
        generated_text, gen_ids = await asyncio.to_thread(
            self.service.generate, prompt_ids, MAX_NEW_TOKENS, skip_special_tokens=False,
        )
        channels = parse_harmony_channels(generated_text)

        # Capture at every target word of this turn, in the latest game text and in the
        # generation (positions past the prompt are labelled "generation" by capture_step).
        full_ids = prompt_ids + gen_ids
        turn_start = (len(harmony_token_ids(tokenizer, turn.messages[:-1], False, self.pin_date))
                      if len(turn.messages) > 1 else 0)
        records, _ = await asyncio.to_thread(
            self.service.capture_step,
            turn.session_id, full_ids, turn.target_words,
            target_position_window=(turn_start, len(full_ids)),
            target_occurrence="all",
            prompt_token_count=len(prompt_ids),
            metadata={
                "label": turn.scenario.condition or turn.scenario.key,
                "turn_id": turn.tick,
                "scenario_id": turn.scenario.key,
                "generated_text": generated_text,
                "capture_type": "prompt",  # capture_step relabels generation positions
            },
        )
        return Act(
            action=channels["action"] or "look",
            analysis=channels["analysis"],
            generated_text=generated_text,
            target_positions={w: [r.target_token_position for r in records if r.target_word == w]
                              for w in turn.target_words},
            probes_written=len(records),
            total_tokens=len(full_ids),
        )


class ScriptedActions:
    """Plays fixed commands: one list per scenario run, in the order the runs happen."""

    def __init__(self, scripts: Sequence[Sequence[str]]):
        self._scripts = [list(s) for s in scripts]
        self._current: List[str] = []

    def begin(self, scenario: "LibraryScenario") -> None:
        self._current = self._scripts.pop(0) if self._scripts else []

    async def act(self, turn: Turn) -> Optional[Act]:
        return Act(action=self._current.pop(0)) if self._current else None
