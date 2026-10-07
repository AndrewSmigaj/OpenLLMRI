"""Pluggable bot "brains" for the Winter Survival harness.

A brain is a pure policy: ``observation (str) -> next MUD command (str)``. It only
*chooses* commands; the deterministic engine owns all world state (design §41). See
``base.Brain`` for the contract.
"""
