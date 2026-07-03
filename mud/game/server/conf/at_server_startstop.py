"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_init()
at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """
    pass


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    # Whiteout: load the content registries (narration templates + DR-23 appearance) at START —
    # NOT lazily at first command import. The login auto-look renders the room before any command
    # has ever run on a fresh server; with empty registries it degrades to bare fallbacks
    # ("Scattered around: ... a the pilot") — the bug Andrew hit 2026-07-03.
    from world.scenarios.whiteout import content
    content.load()
    # Whiteout: ensure the world-clock heartbeat exists (persistent; DR-14).
    from evennia import create_script, search_script
    if not search_script("whiteout_heartbeat"):
        create_script("typeclasses.heartbeat.HeartbeatScript")


def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
