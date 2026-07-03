# Clothing & Warmth (DR-25)

> **Status: SPEC OF RECORD (2026-07-03; Andrew's directive — "you should be able to wear
> everything").** Clothing is a SYSTEM, not flavor: worn items produce a warmth score that the
> P5 cold clock will consume. v1 ships the score and its surfacing; exposure/damage is P5.

## The model

- **Wearability is DERIVED, never whitelisted** (`systems/warmth.py::wearable`): any entity whose
  materials carry a fabric/flexible/soft/insulating tag, ≤ 4 kg, not a fixture/liquid/edible —
  the blanket wears as a cloak, a freed seat cover wraps, socks and gloves and a spare shirt all
  wear. Physical refusals for the rest ("it doesn't bend around a body").
- **Worn representation**: `state["worn_by"] = wearer` on the item; the item STAYS in the
  wearer's inventory (the Evennia clothing-contrib pattern, concept only). `wear` auto-takes from
  the floor (SET_ATTR then TRANSFER — transfer LAST, the DR-24 rollback rule); `remove/doff/shed`
  (and "take X off", routed from the take handler) clears the flag and keeps it in hand; worn
  things refuse `drop` and `put` until shed; a DEAD wearer can be stripped (take's dignity line);
  a living one refuses.
- **The warmth score** (`systems/warmth.py`): each worn item contributes
  `round(insulation × min(mass_g, 3000))` "insulation-grams" — an INTENSIVE material property
  scaled by EXTENSIVE mass, then summed. This is not ordinal-summing (DR-04/DR-11 hold): a 100 g
  wool strip warms less than a 700 g wool blanket. Bands: bare to the wind → thinly covered →
  adequately dressed → well bundled → swaddled. Thresholds are tunable constants.
- **Layering**: unlimited and linear in v1 ("wear everything") — diminishing returns / coverage
  slots are a recorded tuning surface (BACKLOG), revisited when P5 makes warmth bite.
- **Surfacing**: `inventory` splits carried/worn and ends with the warmth band; `examine me` /
  `look at me` append the SAME `worn_summary` (one pure helper → byte-identical); examining
  anyone weaves what they wear ("The pilot wears a flight jacket") — which is itself a discovery
  clue (a worn jacket suggests pockets; frisk him).

## P5 hand-off

`clothing_warmth` becomes one input of the §32 exposure model beside fire, windbreak, shelter and
huddling; the no-materials warmth floor stays the survivability guarantee. A `status` command
joins then.
