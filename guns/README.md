# Guns

Original scripted visual game assets, each in its own independently rebuildable
folder. Shared procedural geometry, rigging, baking and delivery use `kit/`.

| Gun | Status | Asset |
| --- | --- | --- |
| PD C9 compact 9 mm pistol | Final: baked PBR, rig/clips and standalone magazines/case | [pistol/](pistol/README.md) |

## Shared conventions

[Guns Interface 1.0.0](INTERFACE.md) is the accepted consumer contract. Meters,
grip origin, Blender +Y forward / +Z up / +X right; glTF −Z forward / +Y up.
Whole-instance motion is external; internal Root stays identity. Six attachment
sockets stay at scene root, while Socket_Magazine rides its complete bone frame.
Each gun owns its capabilities, clip schedules and semantic event/state manifest.

`common/` contains the guns-only presentation renderer, timed strip generator,
interface schema/frame checks and photographic camera configuration helpers.
They accept each gun's manifest and shot table; pistol anatomy, poses, landmarks,
contact policy and construction checks remain in `pistol/src/`. Reusable asset
primitives belong in `kit/`, rather than in a second weapons toolkit.

## Rebuild and add a gun

```sh
make -C guns                # all immediate gun folders
make -C guns check          # all gun checks
make -C guns/pistol         # pistol alone
make -C guns/pistol check
```

Add `<gun>/Makefile`, `README.md`, `REVIEW.md`, `src/`, `refs/SOURCES.md` and,
only after final acceptance, `docs/`. Use `../../kit/checkpoint_rules.mk`
until look-dev and final delivery are authorized; the pistol then calls the kit
finalize/bake/downsample/export stages through its rig-specific delivery graph. The family Makefile discovers
immediate child Makefiles automatically. A gun must work from its own directory,
without another gun's sources or outputs. Provide an asset-owned renderer entry
point and shot/manifest modules when using `common/render.py` or `common/strips.py`.
Use `common/interface_checks.py` for the common contract; independently check
that gun's intended states, contacts and motion. Keep measured photo landmarks
in the gun and import `common/photo_matches.py` for units/calibrated shot loading.

All builds use the kit GPU lock and worktree-local scratch directory. Generated
blends, GLBs, textures, renders and downloaded references remain ignored. See
[the repository contract](../AGENTS.md) and [kit documentation](../kit/README.md).
