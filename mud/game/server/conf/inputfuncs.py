"""
Input functions

Input functions are always called from the client (they handle server
input, hence the name).

This module is loaded by being included in the
`settings.INPUT_FUNC_MODULES` tuple.

All *global functions* included in this module are considered
input-handler functions and can be called by the client to handle
input.

An input function must have the following call signature:

    cmdname(session, *args, **kwargs)

Where session will be the active session and *args, **kwargs are extra
incoming arguments and keyword properties.

A special command is the "default" command, which is will be called
when no other cmdname matches. It also receives the non-found cmdname
as argument.

    default(session, cmdname, *args, **kwargs)

"""

# def oob_echo(session, *args, **kwargs):
#     """
#     Example echo function. Echoes args, kwargs sent to it.
#
#     Args:
#         session (Session): The Session to receive the echo.
#         args (list of str): Echo text.
#         kwargs (dict of str, optional): Keyed echo text
#
#     """
#     session.msg(oob=("echo", args, kwargs))
#
#
# def default(session, cmdname, *args, **kwargs):
#     """
#     Handles commands without a matching inputhandler func.
#
#     Args:
#         session (Session): The active Session.
#         cmdname (str): The (unmatched) command name
#         args, kwargs (any): Arguments to function.
#
#     """
#     pass


def scenario(session, *args, **kwargs):
    """The control channel for the backend's runner (any client may use it):

      ["scenario", [], {"cmd": "status"}]
      ["scenario", [], {"cmd": "load", "key": "<set_id>/<file>"}]
      ["scenario", [], {"cmd": "end"}]

    Each is answered with ["scenario", [{ok, error, logged_in, character, room, ...}], {}]; a load
    also answers with the scenario, its set (set_id@version), its file's hash and the first stage,
    and the room sends "stage_entered". The agent can't type its way out of a scenario: only this
    channel (or a builder's `leave`) ends one. Imports stay inside: Evennia treats every global
    function in this module as an input handler.
    """
    from typeclasses.staged.instances import end_scenario, load_scenario
    from world.staged.scenario import ScenarioError

    cmd = kwargs.get("cmd") or (args[0] if args else "")
    character = session.puppet
    reply = {"ok": False, "error": None, "logged_in": bool(session.logged_in),
             "character": character.key if character else None}
    if cmd == "status":
        reply["ok"] = True
    elif character is None:
        reply["error"] = "not playing a character"
    elif cmd == "load":
        try:
            room, entered = load_scenario(character, str(kwargs.get("key", "")))
            reply.update(ok=True, scenario=room.db.scenario_key, set=room.loaded.set.ref,
                         file_hash=room.loaded.file_hash, stage=entered.stage)
        except ScenarioError as err:
            reply["error"] = str(err)
    elif cmd == "end":
        reply["ok"] = end_scenario(character)
        if not reply["ok"]:
            reply["error"] = "not in a scenario"
    else:
        reply["error"] = f"unknown scenario command {cmd!r} (status, load or end)"
    if character is not None and character.location is not None:
        reply["room"] = character.location.key
    session.msg(scenario=[reply])
