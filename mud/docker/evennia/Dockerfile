# Whiteout MUD — Evennia image.
#
# The MUD (Evennia server + web client) runs entirely in this container.
# The torch bot-agent does NOT run here — it runs on the host where the model
# weights and GPU live (see agent/README.md for the host carve-out).
#
# We extend the official image only to add:
#   - psycopg2-binary  : the Postgres driver (the base image targets SQLite)
#   - pytest/pytest-django : the dev test runners for the pure sim/ layer
#
# Everything is PINNED for reproducibility: the base is pinned BY DIGEST, so the whole
# stack — OS, python, evennia, django — is frozen identically across machines and over
# time (local dev, CI, and any fresh clone all build the same bytes). The digest below is
# evennia 6.0.0 · django 6.0.6 · python 3.13.14. To intentionally bump the base: pull the
# new evennia/evennia image, read its digest (`docker images --digests`), rebuild, verify
# the tests pass, then update this line + the versions noted in this comment.
FROM evennia/evennia@sha256:4ad1a81e5bedf5c9c95d2a42af8385c20466bd865a050480e0854388d6f47555

RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.12 \
    pytest==9.1.1 \
    pytest-django==4.12.0

# The game directory is bind-mounted at runtime to /usr/src/game
# (see docker-compose.yml). This is also the default WORKDIR of the base image.
WORKDIR /usr/src/game
