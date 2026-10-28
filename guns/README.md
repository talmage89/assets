# Guns

Original scripted visual game assets, each in its own independently rebuildable
folder. Shared procedural geometry, rigging, baking and delivery use `kit/`.

| Gun | Status | Asset |
| --- | --- | --- |
| PD C9 compact 9 mm pistol | Final: baked PBR, rig/clips and standalone magazines/case | [pistol/](pistol/README.md) |
| PD Hearth 12 pump shotgun | Final: baked PBR, rig/clips, live shell and fired hull | [shotgun/](shotgun/README.md) |
| PD Meridian Six .357 revolver | Final PBR delivery for review: 22 clips, per-chamber state, cartridge/case and loader | [revolver/](revolver/README.md) |
| PD Vesper B24 bolt-action precision rifle | Final: baked PBR, nine clips, scope/bipod and standalone magazines/case | [bolt/](bolt/README.md) |

## Shared conventions

[Guns Interface 1.0.0](INTERFACE.md) is the accepted consumer contract. Meters,
grip origin, Blender +Y forward / +Z up / +X right; glTF −Z forward / +Y up.
Whole-instance motion is external; internal Root stays identity. Six attachment
sockets stay at scene root, while Socket_Magazine rides its complete bone frame.
Each gun owns its capabilities, clip schedules and semantic event/state manifest.
The [1.1.0 tube-loading supplement](shotgun/INTERFACE.md) adds pump support-hand
and insertion sockets without changing the pistol's 1.0.0 binding.
The [1.2.0 bolt/optic supplement](bolt/INTERFACE.md) adds manual bolt cycling,
bipod states and the optional objective-camera frame.

`common/` contains the guns-only presentation renderer, timed strip generator,
interface schema/frame checks and photographic camera configuration helpers.
They accept each gun's manifest and shot table; pistol anatomy, poses, landmarks,
contact policy and construction checks remain in `pistol/src/`. Reusable asset
primitives belong in `kit/`, rather than in a second weapons toolkit.

### Triggers

The front face is concave and faces the muzzle; the lower tip curls forward.
The back face is convex toward the grip. Each new gun checks its trigger in a
photographic pair, including a side view and a three-quarter close-up.
`common/trigger_review.py` composes comparison-only crops from each gun's own
framing data. `common/revision_check.py` checks changed triggers against an
independently rebuilt baseline: all other named meshes, rig, sockets and clips.

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
