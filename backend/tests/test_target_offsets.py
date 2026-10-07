"""Where a captured target word sits in the stored text. The offset is read from the token position,
so it places the occurrence that was captured even when the word also appears earlier (in the
developer prompt) or inside a longer word."""
from pathlib import Path

import pytest

from services.probes.probe_processor import ProbeProcessor

VOCAB = ["<|start|>", "Examine", " person", ".", " The", " personal", " effects", "<|end|>",
         " A", " waits"]
# <|start|>Examine person. The personal effects.<|end|> A person waits
IDS = [0, 1, 2, 3, 4, 5, 6, 3, 7, 8, 2, 9]
TEXT = "Examine person. The personal effects. A person waits"
MODEL = Path(__file__).resolve().parents[2] / "data" / "models" / "gpt-oss-20b"


class FakeTokenizer:
    def decode(self, ids, skip_special_tokens=True):
        return "".join(VOCAB[i] for i in ids
                       if not (skip_special_tokens and VOCAB[i].startswith("<|")))

    def encode(self, text, add_special_tokens=False):
        return [VOCAB.index(text)] if text in VOCAB else [0, 0]


def test_the_offset_is_the_occurrence_that_was_captured():
    p = ProbeProcessor(FakeTokenizer(), None, [])
    positions = [pos for pos, _ in p.find_all_word_token_positions(IDS, "person")]
    assert positions == [2, 10]
    offsets = [p.target_char_offset(IDS, pos, "person", TEXT) for pos in positions]
    assert offsets == [TEXT.index("person"), TEXT.rindex("person")]
    # Counting the word's occurrences in the text would have put the second one in "personal".
    assert TEXT.find("person", offsets[0] + 1) == TEXT.index("personal")


def test_a_text_that_does_not_line_up_gives_no_offset():
    p = ProbeProcessor(FakeTokenizer(), None, [])
    assert p.target_char_offset(IDS, 10, "person", "a different text altogether") is None


@pytest.mark.skipif(not (MODEL / "tokenizer.json").exists(), reason="needs the local gpt-oss tokenizer")
def test_with_the_real_tokenizer_every_offset_lands_on_its_word():
    from transformers import AutoTokenizer

    from services.agent.actions import harmony_token_ids
    tok = AutoTokenizer.from_pretrained(MODEL)
    messages = [
        {"role": "developer", "content": "Your first command MUST be `examine person`. Be personal."},
        {"role": "user", "content": "A bus stop. A person is here, waiting.\n"
                                    "What will you do about the person?"},
    ]
    ids = harmony_token_ids(tok, messages, True, "2026-04-22")
    text = tok.decode(ids, skip_special_tokens=True)
    p = ProbeProcessor(tok, None, [])
    positions = [pos for pos, _ in p.find_all_word_token_positions(ids, "person")]
    offsets = [p.target_char_offset(ids, pos, "person", text) for pos in positions]
    assert len(offsets) >= 3 and all(o is not None for o in offsets)
    assert all(text[o:o + len("person")].lower() == "person" for o in offsets)
    assert offsets == sorted(offsets) and offsets[-1] == text.rindex("person")


@pytest.mark.skipif(not (MODEL / "tokenizer.json").exists(), reason="needs the local gpt-oss tokenizer")
def test_with_the_real_tokenizer_a_pinned_render_matches_the_direct_template():
    # Rendering as text and re-encoding gives the same tokens as tokenizing in the template, so
    # pinning the date changes only the date.
    from datetime import date

    from transformers import AutoTokenizer

    from services.agent.actions import MODEL_IDENTITY, harmony_token_ids
    tok = AutoTokenizer.from_pretrained(MODEL)
    messages = [{"role": "developer", "content": "Examine the person."},
                {"role": "user", "content": "A person is here."},
                {"role": "assistant", "content": "examine person"},
                {"role": "user", "content": "They look tired."}]
    direct = tok.apply_chat_template(messages, add_generation_prompt=True, tokenize=True,
                                     return_dict=True, model_identity=MODEL_IDENTITY)["input_ids"]
    assert harmony_token_ids(tok, messages, True, date.today().isoformat()) == list(direct)
