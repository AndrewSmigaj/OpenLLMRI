#!/usr/bin/env bash
set -u
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
LOG="$ROOT/docs/studies/context_shift/captures/tank_ckpt_log.tsv"
[ -f "$LOG" ] || printf "set\tsession\tpositions\tstatus\n" > "$LOG"
COUNT=0
$PY -c "
import json
m=json.load(open('$ROOT/data/sentence_sets/polysemy/context_shift_ckpts/ckpt_manifest.json'))
for e in m: print(e['name'] + '\t' + e['substring'].replace('\"','\\\\\"'))
" | while IFS=$'\t' read -r SET SUB; do
    if grep -q "^${SET}	" "$LOG"; then continue; fi
    RESP=$(curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
        -H 'Content-Type: application/json' --max-time 600 \
        -d "{\"sentence_set_name\": \"${SET}\", \"generate_output\": false, \"capture_static_substring\": \"${SUB}\"}")
    SID=$(printf '%s' "$RESP" | $PY -c "import sys,json
try: print(json.load(sys.stdin).get('session_id','ERR'))
except: print('ERR')")
    NP=$($PY -c "
import pandas as pd
try:
    r=pd.read_parquet('$ROOT/data/lake/${SID}/residual_streams.parquet', columns=['token_position'])
    print(r.token_position.nunique())
except: print(0)" | tail -1)
    STATUS=$([ "$NP" -gt "10" ] && echo ok || echo err)
    printf "%s\t%s\t%s\t%s\n" "$SET" "$SID" "$NP" "$STATUS" >> "$LOG"
    echo "[$SET] $SID pos=$NP $STATUS"
done
echo "=== ckpt chain complete ==="; wc -l "$LOG"; df -h /mnt/c | tail -1
