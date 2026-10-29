# Standalone detachable texture delivery

All seventeen standalone GLBs carry their own small baked texture sets. The six
main gun GLBs are byte-identical to exports built before this change at branch
point `6bce9cfc0245d03e04c00490d96aed66f8f3fbd0`. Canonical PNGs and
finalized source blends also retain their exact SHA-256 hashes. No docs JPG was
regenerated or changed. Baseline builds used each gun’s `make export`; this
avoided the `all` target’s docs regeneration. Every baseline bake used the shared
GPU lock. Exports were preserved under `build/detachables/baseline/<gun>/`.

## Texture policy

`DETACHABLES` entries opt into `texture_size=512` or `1024`. Static ammunition
variants use the equivalent `EXPORT_TEXTURE_SIZE`. Export-only configuration
keeps these choices outside bake dependencies. The kit copies shipped pixels
without rebaking or resampling, and translates nonrotated/nonmirrored charts by
integer pixels with a positive uniform UV scale. Material factors/extensions,
including the SMG’s opaque alpha specular data, survive unchanged. The original
canonical-map delivery and its existing kit regression remain unchanged.

Charts retain their bilinear sampling footprint plus two pixels of dilation.
**Standalone samplers use LINEAR base-level filtering without mipmaps, with
CLAMP_TO_EDGE.** No finite gutter can isolate islands through a mip chain ending
at 1×1, and glTF has no maximum-LOD field. Importers must honor the sampler;
forcing generated mipmaps requires an engine-specific LOD/padding policy.
At 8-bpp compression per map, the three base levels cost about 0.75 MiB at 512
or 3 MiB at 1024. The ten 1024 and seven 512 sets total about **35.25 MiB**;
seventeen independent full 2048 allocations with mipmaps would cost 272 MiB.

## Measured standalone outputs

Density below is the surface-area-weighted median, in pixels per meter.
Each item uses one material and three embedded maps. Triangle counts and exact
oriented positions/normals, origins and material settings are unchanged.

| Gun | Standalone | Triangles | Old GLB bytes | New GLB bytes | Map size | Atlas density → own set |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| pistol | `case.glb` | 384 | 5,204,740 | 239,544 | 512 | 7,571.67 → 7,571.67 |
| pistol | `magazine_empty.glb` | 4,416 | 5,362,360 | 945,428 | 1024 | 3,972.74 → 3,972.74 |
| pistol | `magazine_loaded.glb` | 5,256 | 5,396,292 | 1,105,768 | 1024 | 3,972.74 → 3,972.74 |
| shotgun | `hull.glb` | 394 | 8,244,008 | 345,992 | 512 | 3,532.51 → 3,532.51 |
| shotgun | `shell.glb` | 600 | 8,260,472 | 362,344 | 1024 | 5,103.97 → 5,103.97 |
| bolt | `case.glb` | 768 | 6,753,080 | 196,596 | 512 | 4,083.00 → 4,083.00 |
| bolt | `magazine_empty.glb` | 3,716 | 6,928,816 | 1,151,616 | 1024 | 2,680.07 → 2,680.07 |
| bolt | `magazine_loaded.glb` | 4,976 | 6,997,748 | 1,373,476 | 1024 | 2,680.07 → 2,680.07 |
| smg | `cartridge.glb` | 688 | 7,359,568 | 141,404 | 512 | 7,076.69 → 7,076.69 |
| smg | `case.glb` | 688 | 7,360,256 | 161,256 | 512 | 6,295.72 → 6,295.72 |
| smg | `magazine_empty.glb` | 4,048 | 7,476,900 | 1,137,960 | 1024 | 2,376.67 → 2,376.67 |
| smg | `magazine_loaded.glb` | 5,792 | 7,549,888 | 1,267,700 | 1024 | 2,374.26 → 2,374.26 |
| revolver | `cartridge.glb` | 520 | 6,307,544 | 58,568 | 512 | 2,938.81 → 2,938.81 |
| revolver | `case.glb` | 456 | 6,304,652 | 64,264 | 512 | 2,938.83 → 2,938.83 |
| revolver | `speedloader_loaded.glb` | 5,398 | 6,513,196 | 548,644 | 1024 | 2,755.17 → 2,755.17 |
| lever | `cartridge.glb` | 1,598 | 7,216,192 | 595,532 | 1024 | 4,942.85 → 4,942.85 |
| lever | `case.glb` | 1,326 | 7,197,348 | 651,064 | 1024 | 5,749.64 → 5,749.64 |

Total standalone GLB bytes: **116,433,060 → 10,347,156** (91.11% smaller).

The smallest supported size fitting the unchanged, guarded chart rectangles is
chosen. All 512 items fit that size. Each 1024 item exceeds the 512 rectangle
area budget, except the live shotgun shell, which has a 538-pixel-long guarded
chart that cannot fit without rotation or density loss. Exact layout dimensions
and density percentiles are in each `build/delivery/detachables/<name>/layout.json`.

## Preservation proof

`build/detachables/preservation.json` records the complete old/new comparison.
All six main GLBs match byte for byte, including meshes, rig, clips, sockets,
materials and maps. Independent raw-accessor checks match all standalone
oriented triangles and full origin/node frames, then sample ten common surface
points per triangle: **410,240 surface samples** across all seventeen items.
Linear color (including alpha), normal and ORM agree within 0.25/255; the
largest measured normal-channel error is only **0.015564 byte**. The largest
UV transform error is **0.0001221 delivered pixel**. The maximum triangle tangent
direction discrepancy from float UV storage is **0.423°**, on microscopic charts.
Resolved density and subtexel sliver ratios are recorded separately.

The exporter occasionally flips a final four-decimal tangent digit. Guarded
asset-owned position/normal/UV anchors restore branch-point tangents at nine
corners in five guns; the bolt retains its existing single-corner guard. The
kit utility rejects changed signatures or differences above one rounding step.
No source geometry, UV atlas, rig or baked pixel is changed by those guards.

The SMG’s old finish fingerprint included immutable standalone UV buffers.
Its main-gun fingerprint remains fully enforced. New detachable fingerprints
were measured from the old baseline, retaining exact oriented triangle data and
origins while allowing UV-driven vertex ordering/deduplication; the independent
atlas audit verifies the new mapped look. Its clean check now declares and
builds the five existing neutral-reference photographs it actually uses.

## Old/new renders

All 31 pairs were opened and inspected, from 62 Cycles stills at 1200 pixels
per item / 32 samples through the shared GPU lock. Cameras, shot settings and
final studio recipes match on both sides. Current GLB hashes and identical
shot/stage metadata are checked in `build/detachables/render-provenance.json`.
The revolver renderer selects its final recipe by an `export` path component;
its preserved baseline was staged under that component before final comparison.
The invalid initial form-studio comparisons were discarded.

Gallery: `build/detachables/pairs/index.html`. Full pairs:
`build/detachables/pairs/<gun>/<standalone>/<shot>-pair.jpg`.
Contact pages: `build/detachables/pairs/contact-1.jpg` through `contact-6.jpg`.
Individual originals/new renders and source hashes remain in the adjacent
`old/`, `new/` and `shots.json` files. Review notes:
`build/detachables/visual-review.md`.

No new bleed, marking loss, hue/value shift or normal seam was visible. Worst
full-image RGB byte RMSE is **0.02555**. Existing extreme-macro faceting and
soft headstamps remain; this revision preserves them. No docs image needs a
visual revision, and all tracked docs hashes remain unchanged.

## Checks

All six guns were re-exported through their own `make export`, then checked:

| Command | Result |
| --- | --- |
| `make -C guns/pistol check` | PASS |
| `make -C guns/shotgun check` | PASS |
| `make -C guns/bolt check` | PASS |
| `make -C guns/smg check` | PASS |
| `make -C guns/revolver check` | PASS |
| `make -C guns/lever check` | PASS |

Every `kit/test_*.py` passed from fresh fixture directories; existing scratch
and baselines were preserved outside those fixtures. `Blender` below means
`blender -b --factory-startup --python-exit-code 1 --python kit/<test>.py`;
`GPU` prefixes that with `kit/with_gpu.sh`. Python uses
`python3 -m unittest -v kit.<test>`.

| Kit test | Runner | Result |
| --- | --- | --- |
| `test_atlas` | Blender | PASS |
| `test_bake_coordinates` | Blender | PASS |
| `test_bake_frames` | Blender | PASS |
| `test_blended_atlas` | Blender | PASS |
| `test_botanical_delivery` | Blender | PASS |
| `test_botany` | Blender | PASS |
| `test_delivery` | Python | PASS |
| `test_detachable_textures` | Blender | PASS |
| `test_export_policy` | Blender | PASS |
| `test_fetch_refs` | Python | PASS |
| `test_foliage` | Blender | PASS |
| `test_fonts` | Python | PASS |
| `test_gpu` | Blender | PASS |
| `test_material_ao` | GPU | PASS |
| `test_photo_match` | Python | PASS |
| `test_policy` | Blender | PASS |
| `test_surface_profiles` | Blender | PASS |
| `test_tiling` | GPU | PASS |
| `test_uv_target_aspect` | Blender | PASS |
| `test_vehicle` | Blender | PASS |
| `test_weapon` | Blender | PASS |
| `test_weapon_delivery` | GPU | PASS |
| `test_weapon_roundtrip` | Blender | PASS |

Exact commands and results: `build/detachables/kit-tests.json` and
`build/detachables/gun-checks.json`; logs are in `build/detachables/logs/`.
Repository checks and `git diff --check` pass. Generated GLBs, maps, blends,
references and review images stay ignored.

## Remaining limitation

The sampler contract deliberately excludes mipmaps. Engine importers that
override it need a bounded LOD or a different padding/delivery policy; they
were not tested here. No additional tools or lead action are needed for the
GLB sampling contract delivered in this revision.
