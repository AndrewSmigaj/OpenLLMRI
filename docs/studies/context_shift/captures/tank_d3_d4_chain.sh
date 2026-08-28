#!/usr/bin/env bash
# Tank D3/D4 capture chain — sentence-experiment route, carrier substring,
# explicit generate_output, per-run row-count assertion, resume-safe TSV log.
set -u
ROOT=$(git rev-parse --show-toplevel)
PY="$ROOT/.venv/bin/python"
LOG="$ROOT/docs/studies/context_shift/captures/tank_d3_d4_log.tsv"
CARRIER="What is the meaning of the word tank?"
[ -f "$LOG" ] || printf "run\tsession\tprobes\trows_ok\tstatus\n" > "$LOG"

RUNS=$($PY -c "
import json
m=json.load(open('$ROOT/data/sentence_sets/polysemy/context_shift_runs/tank_manifest.json'))
print(' '.join(r['name'] for r in m['runs']))")

for RUN in $RUNS; do
    if grep -q "^${RUN}	" "$LOG"; then echo "[skip] $RUN"; continue; fi
    echo "[fire] $RUN"
    RESP=$(curl -s -X POST http://localhost:8000/api/probes/sentence-experiment \
        -H 'Content-Type: application/json' --max-time 900 \
        -d "{\"sentence_set_name\": \"${RUN}\", \"generate_output\": false, \"capture_static_substring\": \"${CARRIER}\"}")
    SID=$(printf '%s' "$RESP" | $PY -c "import sys,json
try: print(json.load(sys.stdin).get('session_id','ERR'))
except: print('ERR')")
    if [ "$SID" = "ERR" ] || [ -z "$SID" ]; then
        # curl may have timed out while server continued — find newest session for this set
        sleep 20
        SID=$($PY -c "
import json,glob,os
fs=sorted(glob.glob('$ROOT/data/lake/_sessions/session_*.json'), key=os.path.getmtime)
for f in reversed(fs[-3:]):
    d=json.load(open(f))
    if d.get('sentence_set_name')=='${RUN}': print(d['session_id']); break
else: print('ERR')" 2>/dev/null | tail -1)
    fi
    CHECK=$($PY -c "
import pandas as pd, sys
try:
    t=pd.read_parquet('$ROOT/data/lake/${SID}/tokens.parquet', columns=['probe_id'])
    r=pd.read_parquet('$ROOT/data/lake/${SID}/residual_streams.parquet', columns=['token_position','probe_id'])
    n=t.probe_id.nunique(); pp=r.groupby('token_position').probe_id.nunique()
    ok = n==40 and len(pp)==10 and (pp==40).all()
    print(f'{n} {\"OK\" if ok else \"MISMATCH\"}')
except Exception as e:
    print(f'0 FAIL')" 2>/dev/null | tail -1)
    PROBES=$(echo $CHECK | cut -d' ' -f1); ROWS=$(echo $CHECK | cut -d' ' -f2)
    STATUS=$([ "$ROWS" = "OK" ] && echo ok || echo err)
    printf "%s\t%s\t%s\t%s\t%s\n" "$RUN" "$SID" "$PROBES" "$ROWS" "$STATUS" >> "$LOG"
    echo "  -> $SID probes=$PROBES rows=$ROWS"
done
echo "=== chain complete ==="; df -h /mnt/c | tail -1
