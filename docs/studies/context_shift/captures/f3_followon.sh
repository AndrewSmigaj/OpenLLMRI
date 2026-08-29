#!/usr/bin/env bash
# Follow-on chain: waits for backfill+fr_ckpt+s3 chains, then D6, behavior, Q1b, D7.
set -u
cd "$(git rev-parse --show-toplevel)"
PY=.venv/bin/python
C=docs/studies/context_shift/captures
okcount() { [ -f "$1" ] && grep -c "	ok$" "$1" || echo 0; }
echo "[followon] waiting for phase-1 chains (36/144/12)..."
while true; do
    A=$(okcount $C/backfill_log.tsv); B=$(okcount $C/fr_ckpt_log.tsv); S=$(okcount $C/fr_s3_d4_log.tsv)
    echo "[followon] backfill $A/36  fr_ckpt $B/144  s3 $S/12"
    [ "$A" -ge 36 ] && [ "$B" -ge 144 ] && [ "$S" -ge 12 ] && break
    sleep 120
done
echo "[followon] phase 1 complete -> D6"
$PY $C/run_chain.py data/sentence_sets/polysemy/context_shift_d6/d6_manifest_tank.json $C/d6_tank_log.tsv 1
$PY $C/run_chain.py data/sentence_sets/role_framing/context_shift_d6_fr/d6_manifest_fr.json $C/d6_fr_log.tsv 1
echo "[followon] D6 done -> behavior"
$PY $C/behavior_chain.py data/sentence_sets/polysemy/context_shift_behavior/behavior_manifest_tank.json $C/behavior_tank_log.tsv tank
$PY $C/behavior_chain.py data/sentence_sets/role_framing/context_shift_behavior_fr/behavior_manifest_fr.json $C/behavior_fr_log.tsv fr
echo "[followon] behavior done -> Q1b (string sign-off: verbatim in approved plan)"
curl -s -X POST http://localhost:8000/api/probes/sentence-experiment -H 'Content-Type: application/json' --max-time 3600 \
  -d '{"sentence_set_name": "tank_q1b_calibration_v1", "generate_output": false}' \
  | $PY -c "import sys,json; d=json.load(sys.stdin); print('q1b_calibration', d.get('session_id'), d.get('total_probes'))" \
  | tee -a $C/q1b_calibration_log.txt
$PY $C/run_chain.py data/sentence_sets/polysemy/context_shift_q1b/q1b_manifest.json $C/q1b_runs_log.tsv 40
echo "[followon] Q1b done -> D7"
$PY $C/run_chain.py data/sentence_sets/polysemy/context_shift_d7/d7_manifest.json $C/d7_log.tsv 1
echo "[followon] ALL CHAINS COMPLETE"
df -h /mnt/c | tail -1
