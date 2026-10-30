# Guns

Original scripted visual game assets, each in its own independently rebuildable
folder. Shared procedural geometry, rigging, baking and delivery use `kit/`.

| Gun | Status | Asset |
| --- | --- | --- |
| PD C9 compact 9 mm pistol | Final: baked PBR, rig/clips and standalone magazines/case | [pistol/](pistol/README.md) |
| PD Bracken L20 .30-30 lever-action carbine | Final: baked PBR, 37 clips, tube and gate loading, cartridge and case | [lever/](lever/README.md) |
| PD Hearth 12 pump shotgun | Final: baked PBR, rig/clips, live shell and fired hull | [shotgun/](shotgun/README.md) |
| PD Meridian Six .357 revolver | Final: baked PBR, 22 clips with per-chamber state, speedloader, cartridge and case | [revolver/](revolver/README.md) |
| PD Vesper B24 bolt-action precision rifle | Final: baked PBR, nine clips, scope/bipod and standalone magazines/case | [bolt/](bolt/README.md) |
| PD Relay 9 fixed-stock 9 mm submachine gun | Final: baked PBR, 21 clips, magazines, cartridge and case | [smg/](smg/README.md) |
| PD Rill 39 stamped-receiver 7.62×39 rifle | Final: baked PBR, 20 clips, rock-in magazines, cartridge and case | [ak/](ak/README.md) |
| PD Harrow 56 belt-fed 5.56×45 light machine gun | Final: baked PBR, 19 clips, count-aware belt, boxes, cartridge, case and link | [lmg/](lmg/README.md) |

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
The [1.3.0 charging-handle supplement](smg/INTERFACE.md) adds manual handle
locking, a nonreciprocating handle socket and select-fire states.
The [1.4.0 swing-out revolver supplement](revolver/INTERFACE.md) adds per-chamber
cylinder state, a manual swing-out reload and a speedloader.
The [1.5.0 lever-action supplement](lever/INTERFACE.md) adds a manual lever action,
gate loading of the tube and a half-cock hammer.
The [1.6.0 rocking-magazine supplement](ak/INTERFACE.md) adds a rock-in magazine
path and a reciprocating charging-handle binding.
The [1.8.0 belt-feed supplement](lmg/INTERFACE.md) adds open-bolt belt states,
feed-cover and box sockets, count-aware rounds/links and a detachable box.

`common/` contains the guns-only presentation renderer, timed strip generator,
interface schema/frame checks and photographic camera configuration helpers.
Each finished gun also has one real-speed exported-GLB GIF under its hero.
[GIF clips, cameras and delivery sizes](GIFS.md) are listed together.
`make -C guns/<gun> gif` rebuilds it; [the shared tool](common/README.md#one-signature-motion-gif)
accepts a member-owned clip sequence and camera for later guns.
They accept each gun's manifest and shot table; pistol anatomy, poses, landmarks,
contact policy and construction checks remain in `pistol/src/`. Reusable asset
primitives belong in `kit/`, rather than in a second weapons toolkit.

Standalone detachable GLBs now carry their own 512 or 1024 texture subsets,
with full density relative to each gun atlas. The Vesper feed correction
intentionally re-bakes its atlas while retaining the same texture allocation. [Delivery details](DETACHABLES.md) lists sizes,
density, cluster counts, mipmapped sampling and the old/new preservation proof.
All twenty-one across seven guns retain density ratio 1.000 at 512/1024 and
total **13,754,664 bytes** versus 146,735,344 bytes with full atlases
(90.63% smaller). Eight sets are 512 and thirteen are 1024; about 60 MiB
compressed with full mip chains, without inter-file deduplication.
The Harrow adds five full-density subsets: two 1024 boxes and three 512
ammunition/link items, totaling **4,285,960 bytes**. Its
[delivery table](lmg/README.md#budget-detachables-and-validation) records the
individual allocations; the twenty-one-item comparison above retains its
original seven-gun scope.

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
