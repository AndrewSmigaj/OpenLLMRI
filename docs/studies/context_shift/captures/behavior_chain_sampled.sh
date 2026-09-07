#!/usr/bin/env bash
# Sampled-decoding arm (7 September 2026): the behavior cells under
# do_sample=True, temperature 1.0, top_p 1.0, no top-k truncation, 2,048-token cap,
# template date pinned to each cell's original capture day. Draw n uses seed
# 20260906 + n. Order: fiction/real draws 1, 2, 3 (204 cells each, transition and
# no-shift), then tank draw 1 (108 cells). Resumable: each pass skips cells already
# in its log. Run from the repository root; the backend must be READY.
set -u
ROOT=$(git rev-parse --show-toplevel); cd "$ROOT"
PY="$ROOT/.venv/bin/python"
CH="docs/studies/context_shift/captures/behavior_chain_v2.py"
FR="data/sentence_sets/role_framing/context_shift_behavior_fr/behavior_manifest_fr.json"
TANK="data/sentence_sets/polysemy/context_shift_behavior/behavior_manifest_tank.json"
LOGDIR="docs/studies/context_shift/captures"
for n in 1 2 3; do
  echo "=== fiction/real draw $n (seed $((20260906 + n))) $(date) ==="
  "$PY" "$CH" "$FR" "$LOGDIR/behavior_fr_s${n}_log.tsv" fr \
      --sample --temperature 1.0 --top-p 1.0 --seed $((20260906 + n)) --suffix "_s${n}"
done
echo "=== tank draw 1 (seed 20260907) $(date) ==="
"$PY" "$CH" "$TANK" "$LOGDIR/behavior_tank_s1_log.tsv" tank \
    --sample --temperature 1.0 --top-p 1.0 --seed 20260907 --suffix "_s1"
echo "=== sampled arm complete $(date) ==="
