#!/bin/sh
# Foreground startup for the evennia container (invoked by docker-compose `command`).
# Kept as a single script because the image entrypoint word-splits its arguments,
# which would mangle a quoted `bash -c "migrate && start"`.
set -e

# Clear stale pid files left by an unclean shutdown.
rm -f server/*.pid 2>/dev/null || true

# Apply DB migrations (idempotent), then run in the foreground logging to stdout.
evennia migrate --noinput
exec evennia start -l
