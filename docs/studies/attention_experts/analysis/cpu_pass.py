"""gpt-oss-20b run on the CPU, one decoder layer at a time, over one capture's prompts, keeping each
earlier position's part of attention's output at the read token (read-only; the proposal in
docs/design/design.md#attention; docs/research/attention_and_experts.md, "Attention, word by word").

Captures keep each layer's state at the read token only, but attention at a layer reads every
earlier position's state, so splitting attention by word needs the states at the other positions
as well. This script works them out. It reads one layer's weights at a time from the model's files,
uses them for every prompt and drops them, which needs about 5 GB at most, no GPU and no loaded
model. Attention, the norms and the routers are stored in BF16; the experts are MXFP4, dequantized
with transformers' own converter. The arithmetic runs in float32 and follows transformers 5.4's
modeling_gpt_oss.py step by step: the norm before attention, attention with RoPE, the learned sinks
and a 128-token window on even layers, the norm before the router, the router's four experts and
their softmax, and the experts' clamped gate.

At the read token i, attention's output at a layer is exactly
    attn_i = sum over j <= i of c_ij, plus o_proj's bias,
    c_ij = W_O [a_1ij v_1j ; ... ; a_64ij v_64j],
where a_hij is head h's weight on position j (each head's learned sink takes a share first, so the
weights over real positions add up to less than one) and v_hj is j's value for that head's group.
Kept for every item, layer and source position j <= i:
- the amount, ||c_ij||;
- its share of attention's output, c_ij . attn_i / ||attn_i||^2;
- the heads' mean weight on j, the mean of a_hij over the 64 heads;
- what c_ij adds to each of the 32 scores of that layer's router: s_i (w_e * g) . c_ij, with s_i the
  router norm's scale at i, so that the parts of every source, the state the layer started from,
  o_proj's bias and the router's own bias add up to each score exactly.
Per item and layer it also keeps the sink's mean share over the heads, and, for every position up to
the read token, the amount it drew from each earlier position and the length of its state before
the layer (so what " tank" drew from "the" can be traced to what "the" drew from earlier words).

Checks (results/cpu_pass_<capture>.json): at every layer, the read token's recomputed state against
the captured one (relative error), its first four experts against the captured ones, and that the
parts add up to attention's output and to the router's scores.

Usage, from the repo root (the tank capture for now: its prompts are the sentences alone, with no
chat template, so they can be rebuilt exactly):
  .venv/bin/python docs/studies/attention_experts/analysis/cpu_pass.py tank
The per-source arrays go to data/lake/<session>/studies/attention_cpu_pass.npz (the lake is not in
git; about 40 MB for the tank capture).
"""
from __future__ import annotations

import json
import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pyarrow.parquet as pq
import torch
from common import LAKE, MODEL, load_capture, write_results

THREADS = 4  # half the machine's cores: it is shared
CHUNK = 64  # prompts per batch
F32 = torch.float32
torch.set_num_threads(THREADS)


class Weights:
    """Tensors by name from the model's safetensors files."""

    def __init__(self) -> None:
        self.index = json.loads((MODEL / "model.safetensors.index.json").read_text(encoding="utf-8"))["weight_map"]

    def raw(self, name: str) -> torch.Tensor:
        from safetensors import safe_open

        with safe_open(str(MODEL / self.index[name]), framework="pt") as f:  # type: ignore[no-untyped-call]
            return f.get_tensor(name)

    def half(self, name: str) -> torch.Tensor:
        """A BF16 tensor as the model loads it (fp16), in float32."""
        return self.raw(name).to(torch.float16).to(F32)

    def embedding_rows(self, ids: List[int]) -> Dict[int, torch.Tensor]:
        from safetensors import safe_open

        name = "model.embed_tokens.weight"
        rows = {}
        with safe_open(str(MODEL / self.index[name]), framework="pt") as f:  # type: ignore[no-untyped-call]
            table = f.get_slice(name)
            for token in sorted(set(ids)):
                rows[token] = table[token:token + 1].to(torch.float16).to(F32)[0]
        return rows

    def experts(self, layer: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        from transformers.integrations.mxfp4 import convert_moe_packed_tensors

        p = f"model.layers.{layer}.mlp.experts."
        gate_up = convert_moe_packed_tensors(self.raw(p + "gate_up_proj_blocks"), self.raw(p + "gate_up_proj_scales"))
        down = convert_moe_packed_tensors(self.raw(p + "down_proj_blocks"), self.raw(p + "down_proj_scales"))
        return gate_up, self.half(p + "gate_up_proj_bias"), down, self.half(p + "down_proj_bias")


def prompts(name: str, cap: Any) -> Tuple[List[List[int]], List[int]]:
    """Each item's token ids and read position, checked against the capture's record."""
    from tokenizers import Tokenizer

    if name != "tank":
        raise SystemExit("only the tank capture's prompts can be rebuilt here: its items are the sentences alone")
    tokenizer = Tokenizer.from_file(str(MODEL / "tokenizer.json"))
    columns = ["probe_id", "input_text", "target_token_position", "total_tokens", "target_token_id"]
    rows = {r["probe_id"]: r for r in pq.read_table(LAKE / cap.session / "tokens.parquet", columns=columns).to_pylist()}
    ids, reads = [], []
    for item in cap.items:
        r = rows[item["probe_id"]]
        tokens = tokenizer.encode(r["input_text"], add_special_tokens=False).ids
        read = int(r["target_token_position"])
        if len(tokens) != int(r["total_tokens"]) or tokens[read] != int(r["target_token_id"]):
            raise SystemExit(f"{item['probe_id']}: the rebuilt prompt doesn't match the capture's record")
        ids.append(tokens)
        reads.append(read)
    return ids, reads


def rms(x: torch.Tensor, gain: torch.Tensor, eps: float) -> Tuple[torch.Tensor, torch.Tensor]:
    scale = torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps)
    return gain * (x * scale), scale


def rotate(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    first, second = torch.chunk(x, 2, dim=-1)
    return torch.cat((first * cos - second * sin, second * cos + first * sin), dim=-1)


def experts_forward(x: torch.Tensor, top: torch.Tensor, gates: torch.Tensor, w: Tuple[torch.Tensor, ...],
                    limit: float = 7.0, alpha: float = 1.702) -> torch.Tensor:
    """GptOssExperts.forward for flat tokens [n, hidden] and their four experts and gate weights."""
    gate_up, gate_up_bias, down, down_bias = w
    out = torch.zeros_like(x)
    for expert in torch.unique(top).tolist():
        rows, slot = torch.where(top == expert)
        h = x[rows] @ gate_up[expert].to(F32) + gate_up_bias[expert]
        gate, up = h[..., ::2].clamp(max=limit), h[..., 1::2].clamp(-limit, limit)
        h = (up + 1) * (gate * torch.sigmoid(gate * alpha))
        h = h @ down[expert].to(F32) + down_bias[expert]
        out.index_add_(0, rows, h * gates[rows, slot, None])
    return out


def run(name: str) -> Dict[str, Any]:
    from transformers import GptOssConfig
    from transformers.models.gpt_oss.modeling_gpt_oss import GptOssRotaryEmbedding

    from services.lenses.data import load_routing
    from services.lenses.store import lens_dir, read_manifest

    started = time.time()
    cap = load_capture(name)
    config = GptOssConfig.from_pretrained(str(MODEL))
    eps, heads, groups, dim = config.rms_norm_eps, config.num_attention_heads, config.num_key_value_heads, config.head_dim
    ids, reads = prompts(name, cap)
    site = read_manifest(lens_dir(cap.session, cap.lens)).site.token_position
    captured_routing = load_routing(cap.session, [item["probe_id"] for item in cap.items], site)
    n, longest = len(ids), max(len(t) for t in ids)
    sources = max(reads) + 1
    lengths = torch.tensor([len(t) for t in ids])
    weights = Weights()
    rows = weights.embedding_rows([t for tokens in ids for t in tokens])
    state = torch.zeros(n, longest, config.hidden_size, dtype=F32)
    for b, tokens in enumerate(ids):
        state[b, :len(tokens)] = torch.stack([rows[t] for t in tokens])
    cos, sin = GptOssRotaryEmbedding(config)(state[:1], torch.arange(longest)[None])
    cos, sin = cos[:, None], sin[:, None]  # [1, 1, T, dim / 2]
    q_idx, k_idx = torch.arange(longest)[:, None], torch.arange(longest)[None, :]
    valid = torch.arange(longest)[None, :] < lengths[:, None]  # [N, T]

    shape = (n, len(cap.layers), sources)
    amount, share, weight = np.full(shape, np.nan, np.float32), np.full(shape, np.nan, np.float32), np.full(shape, np.nan, np.float32)
    push = np.full((*shape, config.num_local_experts), np.nan, np.float32)
    carried, sink = np.zeros((n, len(cap.layers), config.num_local_experts), np.float32), np.zeros((n, len(cap.layers)), np.float32)
    maps = np.full((n, len(cap.layers), sources, sources), np.nan, np.float16)  # every position's amounts, up to the read token
    residual = np.full((n, len(cap.layers), sources), np.nan, np.float32)  # each position's state before the layer, its length
    checks: List[Dict[str, Any]] = []
    for li, layer in enumerate(cap.layers):
        t0 = time.time()
        p = f"model.layers.{layer}."
        g_in, g_post = weights.half(p + "input_layernorm.weight"), weights.half(p + "post_attention_layernorm.weight")
        wq, bq = weights.half(p + "self_attn.q_proj.weight"), weights.half(p + "self_attn.q_proj.bias")
        wk, bk = weights.half(p + "self_attn.k_proj.weight"), weights.half(p + "self_attn.k_proj.bias")
        wv, bv = weights.half(p + "self_attn.v_proj.weight"), weights.half(p + "self_attn.v_proj.bias")
        wo, bo = weights.half(p + "self_attn.o_proj.weight"), weights.half(p + "self_attn.o_proj.bias")
        sinks = weights.half(p + "self_attn.sinks")
        wr, br = weights.half(p + "mlp.router.weight"), weights.half(p + "mlp.router.bias")
        expert_weights = weights.experts(layer)
        allowed = k_idx <= q_idx
        if config.layer_types[layer] == "sliding_attention":
            allowed = allowed & (k_idx > q_idx - config.sliding_window)
        mask = torch.where(allowed, 0.0, torch.finfo(F32).min)
        routed = wr * g_post  # [experts, hidden]: the router's view, with the norm's gain
        wo_heads = wo.T.reshape(heads, dim, config.hidden_size)  # each head's slice of the output projection
        sum_error, router_error, rel_error, match_four = [], [], [], []
        new_state = torch.empty_like(state)
        for start in range(0, n, CHUNK):
            h = state[start:start + CHUNK]
            b_n, t_n = h.shape[0], h.shape[1]
            x, _ = rms(h, g_in, eps)
            q = (x @ wq.T + bq).view(b_n, t_n, heads, dim).transpose(1, 2)
            k = (x @ wk.T + bk).view(b_n, t_n, groups, dim).transpose(1, 2)
            v = (x @ wv.T + bv).view(b_n, t_n, groups, dim).transpose(1, 2)
            q, k = rotate(q, cos, sin), rotate(k, cos, sin)
            k, v = k.repeat_interleave(heads // groups, dim=1), v.repeat_interleave(heads // groups, dim=1)
            logits = q @ k.transpose(2, 3) * dim ** -0.5 + mask
            combined = torch.cat([logits, sinks.reshape(1, -1, 1, 1).expand(b_n, -1, t_n, 1)], dim=-1)
            probs = torch.softmax(combined - combined.max(dim=-1, keepdim=True).values, dim=-1)[..., :-1]
            attn = (probs @ v).transpose(1, 2).reshape(b_n, t_n, heads * dim) @ wo.T + bo
            mid = h + attn
            post, scale = rms(mid, g_post, eps)
            scores = post @ wr.T + br
            top_values, top = torch.topk(scores, 4, dim=-1)
            gates = torch.softmax(top_values, dim=-1)
            flat = valid[start:start + b_n]
            moe = torch.zeros_like(mid)
            moe[flat] = experts_forward(post[flat], top[flat], gates[flat], expert_weights)
            new_state[start:start + b_n] = mid + moe
            for local in range(b_n):
                b, i = start + local, reads[start + local]
                a = probs[local, :, i, :i + 1]  # [heads, sources]
                parts = (a[..., None] * v[local, :, :i + 1, :]).permute(1, 0, 2).reshape(i + 1, heads * dim) @ wo.T
                total = attn[local, i]
                sum_error.append(float((parts.sum(0) + bo - total).norm() / total.norm()))
                amount[b, li, :i + 1] = parts.norm(dim=1).numpy()
                share[b, li, :i + 1] = (parts @ total / total.dot(total)).numpy()
                weight[b, li, :i + 1] = a.mean(0).numpy()
                sink[b, li] = float(1 - a.sum(1).mean())
                s = scale[local, i, 0]
                push[b, li, :i + 1] = (s * parts @ routed.T).numpy()
                carried[b, li] = (s * h[local, i] @ routed.T).numpy()
                each = torch.einsum("hjd,hdk->hjk", v[local, :, :i + 1, :], wo_heads)  # [heads, sources, hidden]
                every = torch.einsum("hqj,hjk->qjk", probs[local, :, :i + 1, :i + 1], each)  # [positions, sources, hidden]
                sum_error.append(float((every[i] - parts).norm() / parts.norm()))
                maps[b, li, :i + 1, :i + 1] = every.norm(dim=2).numpy()
                residual[b, li, :i + 1] = h[local, :i + 1].norm(dim=1).numpy()
                rebuilt = carried[b, li] + (s * bo @ routed.T).numpy() + push[b, li, :i + 1].sum(0) + br.numpy()
                router_error.append(float(np.abs(rebuilt - scores[local, i].numpy()).max()))
                stored = torch.from_numpy(cap.outputs[li][b].astype(np.float32))
                rel_error.append(float((new_state[b, i] - stored).norm() / stored.norm()))
                mine = set(top[local, i].tolist())
                theirs = set(np.argsort(-captured_routing[b, layer], kind="stable")[:4].tolist())
                match_four.append(mine == theirs)
        state = new_state
        del expert_weights
        rel = np.array(rel_error)
        checks.append({"layer": layer, "seconds": round(time.time() - t0, 1),
                       "relative_error_median": float(np.median(rel)), "relative_error_p95": float(np.percentile(rel, 95)),
                       "relative_error_max": float(rel.max()), "match_four": float(np.mean(match_four)),
                       "parts_sum_error_max": float(max(sum_error)), "router_parts_error_max": float(max(router_error))})
        print(json.dumps(checks[-1]), flush=True)
    out = LAKE / cap.session / "studies"
    out.mkdir(parents=True, exist_ok=True)
    width = max(len(t) for t in ids)
    token_ids = np.full((n, width), -1, np.int64)
    for b, tokens in enumerate(ids):
        token_ids[b, :len(tokens)] = tokens
    np.savez_compressed(out / "attention_cpu_pass.npz", probe_ids=np.array([item["probe_id"] for item in cap.items]),
                        layers=np.array(cap.layers), reads=np.array(reads), token_ids=token_ids, amount=amount,
                        share=share, weight=weight, push=push, carried=carried, sink=sink, maps=maps, residual=residual)
    payload = {"capture": name, "session": cap.session, "lens": cap.lens, "items": n, "threads": THREADS,
               "seconds": round(time.time() - started, 1), "layers": checks,
               "array_file": str((out / "attention_cpu_pass.npz").relative_to(LAKE.parent.parent))}
    write_results(f"cpu_pass_{name}", payload)
    return payload


if __name__ == "__main__":
    for capture in sys.argv[1:]:
        run(capture)
