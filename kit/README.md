# Asset toolkit

A compact Blender 5.2 pipeline, proven on [Field 3](../gas-grill/README.md).
Meters, +Z up, −Y front; deterministic scripted geometry, original material
nodes and graphics. The read-only rifle project informed the workflow.

| File | Responsibility |
| --- | --- |
| `model.py` | Profiles, lathes, lofts, hollow sections, parallel-transport tubes, curves, sheet gauges, bevels, booleans, fasteners, welds, pivot parenting and print UVs |
| `materials.py` | Manufactured finishes with wear, heat, contact, edge, cavity, handling, gravity/drip and exposure masks; combustion/carbon and ported tube idioms; explicit bake channels |
| `rig.py` | Connected chains, normalized vertex binding, arc sampling, reset and parallel-transport free-hanging demonstration |
| `finalize.py`, `uv.py` | Static modifier application, triangulation, priority-weighted atlas unwrap/pack; actual polygon-clipped overlaps, coverage and density percentiles |
| `bake.py` | GPU Cycles selected-to-active BaseColor, roughness, metallic, AO and tangent +Y normal; joins only equal coordinate frames to preserve object-space materials |
| `image_io.py`, `downsample.py` | Original 8/16-bit PNG codec; linear-light color filtering, vector-normal filtering/renormalization and roughness RMS filtering |
| `export.py` | One embedded PBR atlas; static assembly consolidation; separate pivots, sockets and skin; expected geometry/weight/rest-transform report |
| `gltf.py`, `verify.py` | Independent raw GLB accessors, normals, textures, weights and inverse-bind checks; fresh Blender import, geometry, pivots, UVs, rig and posed cross-sections |
| `gpu.py`, `with_gpu.sh` | Shared GPU flock; script-enabled OptiX with CUDA fallback; refuse silent CPU fallback |
| `studio.py` | Procedural seamless studio, key/fill/rim/negative fill, AgX, configured cameras, moving parts, neutral 1.8 m silhouette; Workbench/Eevee/Cycles; final mode accepts only GLB |
| `photo_match.py` | Measured-landmark lens/pose fit, independent Blender projection check, same-framing photo pairs and residual overlays |
| `audit.py` | Independent source/game topology, count, scale, normals and pivot audit |
| `repo_check.py`, `install_hook.py` | Git source/type/size/docs constraints, including staged blobs in the worktree-local pre-commit hook |
| `contact.py`, `fetch_refs.py`, `new_asset.py` | Review sheets, image/PDF-only reference retrieval and safe new-asset scaffold |
| `rules.mk` | Parameter invalidation and the shared checkpoint/delivery build graph |

## Asset interface

Provide `src/build.py`, `src/markings.py`, `src/config.py` and a Makefile including
`../kit/rules.mk`. Meshes carry `asset_set`; a rigid assembly root carries
`static_root=True`. Moving empties carry `pivot_axis`/`range_degrees` or
`slide_axis`/`range_m`; attachment empties carry `socket_kind`. Meshes may specify
`export_part` to retain useful removable/diagnostic groups. Child geometry is
rebased to the owning pivot, with applied mesh scale. Rigged parts use `bind()`.

`config.py` supplies `BUDGETS`, `BOUNDS` and `SHOTS`. Optional `UV_PRIORITY`
(prefix → relative density), `UV_DEFAULT_PRIORITY`, `BAKE_DROP_MESHES`,
`REQUIRED_NODES` and `EXCLUDED_NODES` configure delivery without asset names in
the kit. Original high print sheets can be projected onto solid low backing;
their names belong in `BAKE_DROP_MESHES` to avoid coplanar low duplicates.

An asset stays on checkpoint builds until its Makefile opts into
`FINAL_PIPELINE := 1`. Then `make` builds refs, high/game sources, UVs, 4096 bake,
2048 delivery textures, GLB, imported-GLB studio, docs and checks. An asset's
`src/review.py --final` creates its sheets/docs. Optional `src/check_fit.py`
handles an explicitly authorized external fit reference; the generic model,
baker and exporter never load external assets. `TANK_REFERENCE` is empty by
default. The pilot passes its owner-authorized local path explicitly.

```sh
python3 kit/new_asset.py ammo-can --name AmmoCan
make -C gas-grill
make -C gas-grill check
make -C gas-grill preview
make -C gas-grill match PASS=photo-review WIDTH=1200 SAMPLES=48
make -C gas-grill WEAR=0.65 PASS=dirtier WIDTH=1000 SAMPLES=32 render
make -C gas-grill hook-install
make -C gas-grill clean
```

Requires installed Blender 5.2, Python/Pillow/NumPy, Noto/DejaVu fonts and flock.
Small assets may set `SHIP_SIZE`, `UV_TARGET_DENSITY` and `UV_MARGIN` in their Makefile, with delivered pixels/m limits in config `UV_DENSITY_BANDS` (`p5_min`, `median_min`, `median_max`, `p95_max`); the existing 2048/grill defaults remain unchanged.
No downloaded code, packages or lighting. `rules.mk` sets TMPDIR inside the
worktree. Every Cycles invocation goes through the GPU wrapper. Source/game
geometry checks remain separate from delivery verification; a look-dev audit
cannot certify a GLB.

## Materials and texture policy

`surface()` layers manufacturing, heat, handling, abrasion/chips, rust, grease
and gravity dust. `wear=0` retains manufacturing while removing use-related
layers. Handling/cooking/heat ellipses and `heat_height` are local meters.
`painted_cast()` adds outdoor enamel over sand-cast iron, exposure chalking, ground splash, and sparse rusted chips along configured ledges, circular cap rims and edges; bolt deposits use the same gravity tracks.
`deposits` are `(x,z,width,length)` gravity tracks, optionally with a local face
direction. Cavities use short-range AO; edge proximity compares beveled and
geometric normals. Stable pivot-local coordinates keep weathering attached to
moving parts. Wheel-radial scuffs are separate from hose rubber.

`OUT_base`, `OUT_rough`, `OUT_metal` and meter-valued `OUT_height` expose the bake
interface; other `OUT_*` sockets expose inspection masks. Original print shaders
retain their substrate channels. Reference images never enter material nodes.

The pilot exercises one atlas. The shipped material uses sRGB BaseColor,
OpenGL +Y Normal and non-color ORM (R AO / G roughness / B metallic). High source
microstructure and small bevels transfer through the tangent-normal bake.
A 16-bit 4096 normal intermediate avoids quantization before 2048 filtering.
Delivery settings participate in build invalidation; static export consolidation preserves each assembly's `asset_set` tag.
Atlas priority and subpixel overlap tolerance are reported, never called exact
uniform density or zero overlap. Independent normals, normalized weights and
world bind transforms are checked in the GLB itself.

## Studio and photo matching

Source preview mode loads a modeling blend; `--stage final` accepts only an
exported GLB. Final output metadata records that source and its SHA-256. Imported bone-display
helpers are removed from the render scene. The pilot poses a lid and a hose;
rig rest-frame metadata makes the demonstration robust to glTF bone-axis
conversion. No animation clips are required for engine-controlled parts.

`photo_matches.py` lists image crops, measured 3D/pixel anchors and an initial
camera estimate. `make match` fits position, angle, roll and focal length, then
renders same-framing pairs. The independent Blender projection check must agree
within 0.05 pixels; photographic residuals remain separate. Estimated lenses
are not claimed EXIF. Photos are measurement/comparison only; derived pairs
stay ignored and never become textures or committed docs.

Future tiling/trim and alpha-card policies can extend the material/export
interface. No speculative road, house or foliage generator is included.
