# `world/scenarios/_template/` — copy this to start a new scenario

```
cp -r world/scenarios/_template world/scenarios/<name>
```

Then fill `manifest.py` (PURE data — packet lists + metadata) and `build.py` (the Evennia loader). Add
`materials/`, `operations/`, `objects/`, `responses/`, `rescue.def` as you author. The repo is meant to
host many scenarios (GDD §3.1); Whiteout is the first. See
[`world/scenarios/README.md`](../README.md) and [`docs/guides/`](../../../../docs/guides/).
