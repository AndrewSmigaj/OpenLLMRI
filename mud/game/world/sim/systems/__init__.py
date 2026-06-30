"""world.sim.systems — stateful subsystems behind the operation interface (DR-14/16, §31-39).

The running real-time clock + activity scheduler (P4), the survival systems (P5), rescue + the radio
FSM (P5), and weather (P7). All pure; each is plain Python registering like any operation. See
systems/README.md.
"""
