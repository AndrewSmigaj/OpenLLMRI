"""game.typeclasses.watching — following a character, as an observer. Shell.

`watch <name>` (commands/watching.py) takes the watcher to where the character is and keeps it there:
each scenario instance the character loads or leaves, its watchers are moved along with it
(typeclasses.staged.instances). In a scenario's room a watcher reads but can't act or speak: only the
scenario's player has its typed lines claimed, and anything said in the room would reach the player's
observation, an agent's prompt (StagedRoom.character_cmdset_for). `unwatch` takes the watcher back to
where it started watching.
"""
from __future__ import annotations


def _followable(location) -> bool:
    """Watchers follow into the institute and into staged scenarios. A world's rooms give a
    character the world's own commands, so following into one waits for a world observer mode."""
    from typeclasses.institute.rooms import InstituteRoom
    from typeclasses.staged.rooms import StagedRoom
    return isinstance(location, (InstituteRoom, StagedRoom))


def start_watching(watcher, target) -> str | None:
    """Follow `target`: to where it is now, or, if it isn't in the world (an agent before its run,
    logged out), into the next scenario it loads. Returns why not, or None."""
    if target == watcher:
        return "You can't watch yourself."
    if target.location is not None and not _followable(target.location):
        return f"{target.key} is somewhere watchers can't follow yet."
    if watcher.db.watching is not None:
        stop_watching(watcher, go_back=False)
    else:
        watcher.db.watch_return = watcher.location
    watcher.db.watching = target
    target.db.watchers = [w for w in (target.db.watchers or []) if w and w != watcher] + [watcher]
    if target.location is not None and watcher.location != target.location:
        watcher.move_to(target.location, quiet=True, move_type="watch")
    return None


def stop_watching(watcher, go_back: bool = True) -> bool:
    """Stop following; by default, go back to where watching started. False if not watching."""
    target = watcher.db.watching
    if target is None:
        return False
    if target.db.watchers:
        target.db.watchers = [w for w in target.db.watchers if w and w != watcher]
    watcher.attributes.remove("watching")
    back = watcher.db.watch_return or watcher.home
    if go_back:
        watcher.attributes.remove("watch_return")
        if watcher.location != back:
            watcher.move_to(back, quiet=True, move_type="watch")
    return True


def carry_watchers(character, destination) -> None:
    """Move `character`'s watchers to `destination` with it (a scenario load or end)."""
    watchers = [w for w in (character.db.watchers or []) if w and w.db.watching == character]
    character.db.watchers = watchers
    for watcher in watchers:
        if watcher.location != destination:
            watcher.move_to(destination, quiet=True, move_type="watch")
