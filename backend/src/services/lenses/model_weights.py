"""The model's own weights, read on the CPU from its safetensors files: no GPU and no loaded model.

The tensors are BF16, which NumPy can't hold, so they are read through safetensors' torch
interface and converted to float32. The unembedding (201,088 rows of 2,880) is read in chunks of
16k rows, about a second each.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, Tuple

import numpy as np

from api.config import PROJECT_ROOT

Array = np.ndarray[Any, Any]

MODEL_DIR = PROJECT_ROOT / "data" / "models" / "gpt-oss-20b"
CHUNK_ROWS = 16384


class ModelWeights:
    """gpt-oss-20b's norms, routers and unembedding, by name from its safetensors index."""

    def __init__(self, folder: Path = MODEL_DIR) -> None:
        self.folder = folder
        self.index = json.loads((folder / "model.safetensors.index.json").read_text(encoding="utf-8"))["weight_map"]
        self.config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
        self.eps = float(self.config.get("rms_norm_eps", 1e-5))

    def tensor(self, name: str) -> Array:
        from safetensors import safe_open

        with safe_open(str(self.folder / self.index[name]), framework="pt") as f:  # type: ignore[no-untyped-call]
            value: Array = f.get_tensor(name).float().numpy()
        return value

    def router(self, layer: int) -> Tuple[Array, Array]:
        """A layer's router: weight [experts, hidden] and bias [experts]."""
        return self.tensor(f"model.layers.{layer}.mlp.router.weight"), self.tensor(f"model.layers.{layer}.mlp.router.bias")

    def pre_router_norm(self, layer: int) -> Array:
        """The RMS-norm gain applied to the residual stream before a layer's router reads it."""
        return self.tensor(f"model.layers.{layer}.post_attention_layernorm.weight")

    def final_norm(self) -> Array:
        return self.tensor("model.norm.weight")

    def unembedding_chunks(self, rows: int = CHUNK_ROWS) -> Iterator[Tuple[int, Array]]:
        """(first token id, rows of the unembedding) in chunks, float32."""
        from safetensors import safe_open

        with safe_open(str(self.folder / self.index["lm_head.weight"]), framework="pt") as f:  # type: ignore[no-untyped-call]
            part = f.get_slice("lm_head.weight")
            total = int(part.get_shape()[0])
            for start in range(0, total, rows):
                yield start, part[start:min(start + rows, total)].float().numpy()

    def decoder(self) -> Any:
        """A function from token id to its text, special tokens (`<|end|>`, `<|channel|>`) included."""
        from tokenizers import Tokenizer

        tokenizer = Tokenizer.from_file(str(self.folder / "tokenizer.json"))
        return lambda token_id: tokenizer.decode([int(token_id)], skip_special_tokens=False)


def rms_norm(hidden: Array, gain: Array, eps: float) -> Array:
    normed: Array = hidden / np.sqrt((hidden ** 2).mean(axis=-1, keepdims=True) + eps) * gain
    return normed
