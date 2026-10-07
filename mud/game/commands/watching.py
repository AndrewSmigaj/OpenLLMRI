"""game.commands.watching — `watch` a character and follow it; `unwatch` to stop (typeclasses.watching)."""
from commands.command import Command


class CmdWatch(Command):
    """Follow a character as a watcher: you go where it goes, into each scenario it plays.

    Usage:
      watch <name>

    In a scenario's room you can look, examine and list its actions, and you read what the player
    types; you can't act or speak there. |wunwatch|n takes you back.
    """
    key = "watch"
    locks = "cmd:all()"

    def func(self):
        from evennia import ObjectDB

        from typeclasses.characters import Character
        from typeclasses.watching import start_watching
        name = self.args.strip()
        if not name:
            self.caller.msg("Watch whom? |wwatch <name>|n")
            return
        found = [o for o in ObjectDB.objects.filter(db_key__iexact=name)
                 if o.is_typeclass(Character, exact=False)]
        if not found:
            self.caller.msg(f"There is no one called '{name}'.")
            return
        target = found[0]
        problem = start_watching(self.caller, target)
        if problem:
            self.caller.msg(problem)
        elif target.location is None:
            self.caller.msg(f"You are watching {target.key}. It isn't in the world now: you'll follow "
                            f"it into the next scenario it loads. |wunwatch|n to stop.")
        else:
            self.caller.msg(f"You are watching {target.key}. |wunwatch|n to stop.")


class CmdUnwatch(Command):
    """Stop watching, and go back to where you started.

    Usage:
      unwatch
    """
    key = "unwatch"
    locks = "cmd:all()"

    def func(self):
        from typeclasses.watching import stop_watching
        if not stop_watching(self.caller):
            self.caller.msg("You aren't watching anyone.")
