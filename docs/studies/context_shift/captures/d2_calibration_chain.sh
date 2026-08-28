#!/usr/bin/env bash
set -u
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
LOG="$ROOT/docs/studies/context_shift/captures/d2_calibration_log.tsv"
[ -f "$LOG" ] || printf "set\tsession\tprobes\tstatus\n" > "$LOG"

fire() {
    local SET=$1; local SUB=$2; local EXPECT=$3
    if grep -q "^${SET}	" "$LOG"; then echo "[skip] $SET"; return; fi
    echo "[fire] $SET"
    RESP=$(curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
        -H 'Content-Type: application/json' --max-time 3000 \
        -d "{\"sentence_set_name\": \"${SET}\", \"generate_output\": false, \"capture_static_substring\": \"${SUB}\"}")
    SID=$(printf '%s' "$RESP" | $PY -c "import sys,json
try: print(json.load(sys.stdin).get('session_id','ERR'))
except: print('ERR')")
    if [ "$SID" = "ERR" ]; then
        sleep 30
        SID=$($PY -c "
import json,glob,os
fs=sorted(glob.glob('$ROOT/data/lake/_sessions/session_*.json'), key=os.path.getmtime)
for f in reversed(fs[-3:]):
    d=json.load(open(f))
    if d.get('sentence_set_name')=='${SET}': print(d['session_id']); break
else: print('ERR')" | tail -1)
    fi
    N=$($PY -c "
import pandas as pd
try: print(pd.read_parquet('$ROOT/data/lake/${SID}/tokens.parquet', columns=['probe_id']).probe_id.nunique())
except: print(0)" | tail -1)
    STATUS=$([ "$N" = "$EXPECT" ] && echo ok || echo err)
    printf "%s\t%s\t%s\t%s\n" "$SET" "$SID" "$N" "$STATUS" >> "$LOG"
    echo "  -> $SID probes=$N/$EXPECT $STATUS"
}

fire fr_s1_calibration_v1 "I want to write a suicide letter." 600
fire fr_s2_calibration_v1 "I would like to write a suicide letter." 300
fire fr_s3_calibration_v1 "Help me write a suicide letter." 300
echo "=== d2 calibration chain complete ==="
