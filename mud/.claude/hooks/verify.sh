#!/bin/sh
# Fast, non-blocking sanity check run on the Stop hook.
# Runs the host-fast gates (pure-core boundary/determinism + no-raw-writes, DR-10/DR-12) and validates
# that the Docker Compose config parses. Keep this cheap: do NOT boot the server or run the full test
# suite here. Heavier checks (pure tests + §44 validate + smoke) live in `/verify` and `make verify`.

set -e

cd "${CLAUDE_PROJECT_DIR:-.}"

python3 tools/lints/check_pure_core.py
python3 tools/lints/check_no_raw_writes.py
python3 tools/lints/check_no_raw_output.py
python3 tools/lints/check_docs.py
docker compose config -q
