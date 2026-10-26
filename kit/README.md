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
No downloaded code, packages or lighting. `rules.mk` sets TMPDIR inside the
worktree. Every Cycles invocation goes through the GPU wrapper. Source/game
geometry checks remain separate from delivery verification; a look-dev audit
cannot certify a GLB.

## Materials and texture policy

`surface()` layers manufacturing, heat, handling, abrasion/chips, rust, grease
and gravity dust. `wear=0` retains manufacturing while removing use-related
layers. Handling/cooking/heat ellipses and `heat_height` are local meters.
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

## Optional asset policy and moving assemblies

These additions preserve legacy calls and defaults. New assets should declare
policy in their own `src/config.py` / settings module; do not edit kit internals.
The grill's values live in `gas-grill/src/settings.py` and `src/config.py`.

- Pass `attach(..., asset_set='YourSet')`; `inherit_asset_set=True` instead reads the parent's tag. The legacy default remains `Grill` for existing callers. `bind(..., export_part='CableMesh', modifier_name='Cable skin')` supplies a skin's export name. `EXPORT_SKIN_NAMES={armature_name: mesh_name}` optionally overrides it at export. There is no name-based test for a hose in assembly ownership.
- `RIG_POSES={armature_name: {'angles': [...], 'lateral': ..., 'twist_step': ..., 'initial_z': (...)}}` configures the studio and verification demonstration. The angle list can have any chain length. `dangling()` also accepts those optional keywords directly; omitted values retain the pilot pose.
- `VERIFY_POLICY` sets `density_reference_size`, `density_p5_min`, `density_median_min/max` and `density_p95_max`. Its optional `tube` dictionary supplies `rest_points_property`, `radius_m`, radial/plane matching tolerances, minimum ring vertices/count, minimum posed radius, attachment travel and root tolerance. `tubes={armature_name: {...}}` supports different chains within one asset. Existing acceptance bands remain defaults.
- `combustion(..., geometry={...})` supplies burner lanes and widths, hood spread/thermal/oil heights, bowl drain center/radii/heights and drip sources, channel apex and streak locations. `ported_burner()` accepts tube/port heights, pitch/start/end, port/soot radii and thermal band dimensions. `surface(..., rust_regions={...})` sets low-height, weld and upper-height regions. All values use the part's rest frame in meters; the legacy finish presets remain available.
- `BAKE_SIZE`, `TEX_SIZE` and `UV_TARGET_DENSITY` are optional Make variables, defaulting to 4096, 2048 and 850. For example a repeated prop can set `TEX_SIZE := 1024` and its own density bands. Rebuild with `make clean && make` when changing atlas sizes/density. `MARKINGS_DEPS` adds shared settings dependencies to graphic generation.
- `FIT_CHECK_ARGS` optionally appends arguments to an asset's own `src/check_fit.py`; it is empty by default. The grill uses `--parts-source build/finalized.blend` for component-level clearance measurements.

Example motion/projection policy:

```python
MOTIONS = [dict(node='Door', axis='Z', range=[0, 100], step=2,
                tolerance_m=.0005, allow=[
                    dict(moving='Door hinge sleeve', fixed='Door hinge pin',
                         reason='Pin in the sleeve bore')])]
BAKE_POLICY = dict(isolate_moving=True, moving_roots=['Door'],
                   cage_m=.003, ray_distance_m=.012, ao_distance_m=.035)
```

`make check-motion` (included in `make check`) sweeps configured rotations in
degrees or `kind='translation'` ranges/steps in meters, on both game and high
source. It tests tagged solid meshes, excluding declared boundary-only sheets.
BVH crossings select candidate surfaces; vertices and edge intervals use nearest
surface distance and three-ray solid parity to measure penetration. The report
lists sampled values, tolerance, violations and intended-contact allow-list
reasons. Missing `MOTIONS` means no sweep. Sampling is explicit, not a continuous
collision guarantee; choose a step small enough for the narrowest obstruction.
Wheel axial separation can additionally prove clearance for every angle.

With `BAKE_POLICY.isolate_moving=True`, low/high geometry is matched by owning
root and translated into separated projection groups. Each lid, door, wheel or
slider therefore receives only its own source projection and local AO. Static
geometry stays assembled; independent rest-position shadow copies preserve its
contact AO. Shadow copies cannot share mutable mesh data with joined sources.
The bake report records groups, offsets and shadow-copy counts. Omitting this
policy keeps the original assembled bake. Custom procedural materials should
use rest/object coordinates, as this library does; raw world-space masks need
rest-coordinate attributes when using translated isolation.

`SHOTS` entries may add `parts={node: {'translation': (x,y,z)}}` or
`rotation_degrees`; the studio resets these transforms between views. This
supports a withdrawn slider or alternate door pose without special node names.
The legacy `lid` shot angle can target another node/axis using the optional Make
variable `STUDIO_ARGS := --lid-node YourHatch --lid-axis Z`; defaults remain
`Lid` / X. Optional fit shots already accept their own `fit_socket` node name.

`compare_textures.py` compares two delivery folders numerically, in RGB byte
units. The grill accepts maximum channel delta **2/255** and byte-domain RMSE
**0.02** per map; geometry remains exactly reproducible. GPU texture bytes are
not promised bit-identical. `make check-texture-repeat` is an opt-in full rebake
and comparison; normal checks never force that expense on other assets.
`blender -b --factory-startup --python-exit-code 1 --python kit/test_policy.py`
runs small solid/hollow collision and non-grill naming/rig compatibility fixtures.
