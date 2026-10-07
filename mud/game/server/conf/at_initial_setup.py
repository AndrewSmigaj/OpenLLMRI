"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""


def at_initial_setup():
    """A new database gets the institute (the hub, the polysemy lab, the simulator); `make institute`
    does the same for an existing one. Evennia ignores tracebacks here, so a failure is logged."""
    from evennia.utils import logger
    try:
        from world.institute.build import build
        build()
    except Exception:
        logger.log_trace("at_initial_setup: building the institute failed; run `make institute`")
