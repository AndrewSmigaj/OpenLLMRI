# Whiteout MUD — Evennia image.
#
# The MUD (Evennia server + web client) runs entirely in this container.
# The torch bot-agent does NOT run here — it runs on the host where the model
# weights and GPU live (see agent/README.md for the host carve-out).
#
# We extend the official image only to add:
#   - psycopg2-binary  : the Postgres driver (the base image targets SQLite)
#   - pytest/pytest-django : the dev test runners for the pure sim/ layer
FROM evennia/evennia:latest

RUN pip install --no-cache-dir \
    psycopg2-binary \
    pytest \
    pytest-django

# The game directory is bind-mounted at runtime to /usr/src/game
# (see docker-compose.yml). This is also the default WORKDIR of the base image.
WORKDIR /usr/src/game
