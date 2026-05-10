#!/usr/bin/env bash
# Suicide letter paper protocol WITH generate_output=true.
# Fires the 12 missing sessions: ord 4..9 x {block_ba, block_ab}.
#
# DELIBERATE ABSENCES:
#   - NO curl --max-time. The server holds the connection for the whole
#     capture (typically 30-75 min for cumulative gen-256 across 40 probes).
#     Prior runs used --max-time 3600 and orderings that ran longer than
#     1h had curl killed while the server kept going, producing ghost ERR
#     rows in the log and concurrent-busy errors on subsequent fires.
#   - NO nohup, NO trailing &. This script is launched via a single
#     foreground bash invocation under run_in_background=true; we let
#     curl block sequentially through all 12 fires.
#
# LOG: docs/scratchpad/paper_protocol_with_gen_log.tsv
# Idempotent: skips any (ord, dir) pair already recorded with status=ok
# (or ok_smoke / ok_recovered).

set -u

LOG=docs/scratchpad/paper_protocol_with_gen_log.tsv
[ -f "$LOG" ] || printf "ord\tdir\trun_id\tnew_session\tprobes\tregime_boundary\tstatus\n" > "$LOG"

fire() {
    local ORD=$1
    local DIR=$2
    if grep -qE "^${ORD}	${DIR}	[^E]" "$LOG"; then
        echo "[skip] ord${ORD}_${DIR} (already complete)"
        return
    fi
    echo "[fire] ord${ORD}_${DIR} ($(date '+%H:%M:%S'))"
    local START=$(date +%s)
    local RESP
    RESP=$(curl -s -X POST http://localhost:8000/api/experiments/temporal-capture \
        -H 'Content-Type: application/json' \
        -d "{
            \"session_id\": \"session_9358c2a1\",
            \"clustering_schema\": \"suicide_letter_basin_k3_n15\",
            \"basin_layer\": 23,
            \"basin_a_cluster_id\": 1,
            \"basin_b_cluster_id\": 0,
            \"sentences_per_block\": 20,
            \"sequence_config\": \"${DIR}\",
            \"generate_output\": true,
            \"run_label\": \"paper_gen_suicide_ord${ORD}_${DIR}\"
        }")
    local END=$(date +%s)
    local RUN_ID NEW_SID PROBES REGIME STATUS
    RUN_ID=$(printf '%s' "$RESP" | .venv/bin/python -c 'import sys,json
try: d=json.loads(sys.stdin.read()); print(d.get("temporal_run_id","ERR"))
except: print("ERR")')
    NEW_SID=$(printf '%s' "$RESP" | .venv/bin/python -c 'import sys,json
try: d=json.loads(sys.stdin.read()); print(d.get("new_session_id","ERR"))
except: print("ERR")')
    PROBES=$(printf '%s' "$RESP" | .venv/bin/python -c 'import sys,json
try: d=json.loads(sys.stdin.read()); print(d.get("sequence_positions","?"))
except: print("?")')
    REGIME=$(printf '%s' "$RESP" | .venv/bin/python -c 'import sys,json
try: d=json.loads(sys.stdin.read()); print(d.get("regime_boundary","?"))
except: print("?")')
    if [ "$RUN_ID" = "ERR" ] || [ -z "$RUN_ID" ]; then
        STATUS="err"
        echo "  FAILED in $((END-START))s: ${RESP:0:300}"
    else
        STATUS="ok"
        local ELAPSED=$((END-START))
        echo "  done in ${ELAPSED}s ($((ELAPSED/60))m) run=${RUN_ID} session=${NEW_SID}"
    fi
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$ORD" "$DIR" "$RUN_ID" "$NEW_SID" "$PROBES" "$REGIME" "$STATUS" >> "$LOG"
}

# 12 missing sessions: ord 4..9 alternating directions
for ord in 4 5 6 7 8 9; do
    fire "$ord" block_ba
    fire "$ord" block_ab
done

echo "Suicide-letter paper protocol with generation complete: $(date '+%H:%M:%S')"
