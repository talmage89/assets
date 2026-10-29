# Asset toolkit

A compact Blender 5.2 pipeline, proven on [Field 3](../gas-grill/README.md)
and the [Bellford hydrant](../fire-hydrant/README.md).
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
| `detachable_textures.py`, `detachable_verify.py` | Opt-in lossless small atlas subsets, guarded sampling, raw-GLB surface and tangent checks |
| `gltf.py`, `verify.py` | Independent raw GLB accessors, normals, textures, weights and inverse-bind checks; fresh Blender import, geometry, pivots, UVs, rig and posed cross-sections |
| `fonts.py` | fontconfig family/style discovery; reject missing faces and substitutions |
| `gpu.py`, `with_gpu.sh` | Shared GPU flock; script-enabled OptiX/CUDA; warned CPU fallback |
| `studio.py` | Procedural seamless studio, key/fill/rim/negative fill, AgX, configured cameras, moving parts, neutral 1.8 m silhouette; Workbench/Eevee/Cycles; final mode accepts only GLB |
| `photo_match.py` | Measured-landmark lens/pose fit, independent Blender projection check, same-framing photo pairs and residual overlays |
| `audit.py` | Independent source/game topology, count, scale, normals and pivot audit |
| `repo_check.py`, `install_hook.py` | Git source/type/size/docs constraints, including staged blobs in the worktree-local pre-commit hook |
| `contact.py`, `fetch_refs.py`, `new_asset.py` | Review sheets, image/PDF-only reference retrieval and safe new-asset scaffold |
| `rules.mk`, `policy.py` | Parameter invalidation, delivery configuration normalization and shared build graph |
| `motion.py` | Sampled solid-surface motion clearance on high and game assemblies |

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
`FINAL_PIPELINE := 1`. Then `make` builds refs, high/game sources, UVs, configurable bake and
delivery textures, GLB, imported-GLB studio, docs and checks. An asset's
`src/review.py --final` creates its sheets/docs. Optional `src/check_fit.py`
handles an explicitly authorized external fit reference; the generic model,
baker and exporter never load external assets. `TANK_REFERENCE` is empty by
default. The pilot passes its owner-authorized local path explicitly.

Form-first seeded generators may include `checkpoint_rules.mk` instead. It
uses the same local temp directory, GPU lock, reference fetcher and repository
check, but accepts `CHECKPOINT_ARGS`, `CHECKPOINT_CHECK` and `CHECKPOINT_REVIEW`
for family-specific construction checks and presentation. `make` stops at the
form checkpoint; it does not imply baked textures or final game readiness.
The existing prop and tiling delivery graphs are unchanged.

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

Requires installed Blender 5.2, GNU make, Python/Pillow/NumPy, fontconfig, Noto/DejaVu fonts and flock.
See the root [build requirements](../README.md#build-requirements) for the font faces and optional reference tools.
No downloaded code, packages or lighting. `rules.mk` sets TMPDIR inside the
worktree. Every Cycles invocation goes through the GPU wrapper. Source/game
geometry checks remain separate from delivery verification; a look-dev audit
cannot certify a GLB.

## Delivery configuration

Use `SHIP_SIZE` for every delivery stage: UV packing/reporting, downsampling,
embedded GLB textures and verification. Defaults are `SHIP_SIZE=2048`,
`BAKE_SIZE=4096`, `BAKE_SAMPLES=32`, `UV_TARGET_DENSITY=850` and
`UV_MARGIN=.0015` (normalized UV units). Legacy `TEX_SIZE` is accepted as an
input alias; conflicting `SHIP_SIZE` and `TEX_SIZE` values fail immediately.
New Makefiles should set only `SHIP_SIZE`. The hydrant uses 1024, 810 and .003
for delivery size, target density and margin; the grill keeps the defaults.

Declare density acceptance in `src/config.py` through one dictionary:

```python
UV_DENSITY_BANDS = dict(reference_size=2048, p5_min=200,
                        median_min=450, median_max=900, p95_max=1500)
```

Limits are pixels/m at `reference_size`, scaled by `SHIP_SIZE/reference_size`.
Those example values are the compatible defaults. The hydrant declares 1024
and limits 280 / 550 / 900 / 1500. `UV_TARGET_DENSITY` guides packing; the
bands independently gate measured density. Resolved limits appear in the
verification report as `density_bands_px_m`.

For compatibility, older `UV_DENSITY_BANDS` without `reference_size` retain
absolute delivered pixels/m semantics. Older `VERIFY_POLICY.density_*` fields
are normalized by the same resolver, with `density_reference_size=2048` by
default. Mixing both density interfaces raises an error. Both current assets
use the canonical dictionary; `VERIFY_POLICY` now configures tube checks only.

Changing delivery size, target density or margin invalidates finalize and its
downstream bake/export/renders. Changing bake size or samples invalidates bake
and downstream outputs without repacking UVs. Unchanged parameter files keep
their timestamps. Wear invalidates modeling; studio width, samples, shot list,
extra arguments and fit-reference path/mtime invalidate studio output.
`MARKINGS_DEPS` adds shared settings dependencies to graphic generation.

## Materials and texture policy

`surface()` layers manufacturing, heat, handling, abrasion/chips, rust, grease
and gravity dust. `wear=0` retains manufacturing while removing use-related
layers. Handling/cooking/heat ellipses and `heat_height` are local meters.
`painted_cast()` adds outdoor enamel over sand-cast iron, exposure chalking,
ground splash, and sparse rusted chips along configured ledges, circular cap
rims and edges; bolt deposits use the same gravity tracks.
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
A 16-bit bake normal intermediate avoids quantization before delivery filtering.
Static export consolidation preserves each assembly's `asset_set` tag, including
when rebasing onto its parent; configured skin names survive separately.
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

Tiling terrain now has an explicit opt-in interface described under Tiling
families below; unique-atlas and reserved-alpha props keep their existing path.

Street-batch extensions: `match-final` compares the baked GLB with the same photo
calibration as the source. Optional legacy `BAKE_CAGE`/`BAKE_RAY` configure thin shells; explicit
`BAKE_POLICY.cage_m` / `ray_distance_m` take precedence when present.
Baked name families may tag `variant_id`, `bake_offset`, and `bake_only` templates;
export selects config `EXPORT_VARIANT`, restores its placement, and joins a single
static mesh. Source audits omit parked templates; final checks still inspect the
actual exported triangles/UVs. `UV_MIN_COVERAGE` declares a shared family's subset
coverage without relaxing overlap checks.

`prop.py` supplies small-prop plate/rest-frame helpers; `delivery_docs.py` makes
three final JPGs with GLB-hash checks. `assembly.py` measures declared supports
on evaluated triangle surfaces (intersections or sampled distance bounds),
separately from serialization and swept-motion verification. Source previews
hide parked bake-only templates.
Photo composition honors EXIF orientation before applying measured crop/pixels;
calibration landmarks are specified in the upright photographic frame.
Atlas configurations can set `UV_SMART_ASPECT=False` when source print images
have different aspect ratios; this prevents material image dimensions from
distorting the shared square bake UVs. `UV_PACK_SHAPE` is an optional packing
choice; all independent overlap/outside checks remain enforced.
`UV_SMART_ANGLE` optionally narrows the unwrap projection angle for deeply
folded shells; the existing 66-degree default is unchanged.

## Optional asset policy and moving assemblies

These additions preserve legacy calls and defaults. New assets should declare
policy in their own `src/config.py` / settings module; do not edit kit internals.
The grill's values live in `gas-grill/src/settings.py` and `src/config.py`.

- Pass `attach(..., asset_set='YourSet')`; `inherit_asset_set=True` instead reads the parent's tag. The legacy default remains `Grill` for existing callers. `bind(..., export_part='CableMesh', modifier_name='Cable skin')` supplies a skin's export name. `EXPORT_SKIN_NAMES={armature_name: mesh_name}` optionally overrides it at export. There is no name-based test for a hose in assembly ownership.
- `RIG_POSES={armature_name: {'angles': [...], 'lateral': ..., 'twist_step': ..., 'initial_z': (...)}}` configures the studio and verification demonstration. The angle list can have any chain length. `dangling()` also accepts those optional keywords directly; omitted values retain the pilot pose.
- `VERIFY_POLICY`'s optional `tube` dictionary supplies `rest_points_property`, `radius_m`, radial/plane matching tolerances, minimum ring vertices/count, minimum posed radius, attachment travel and root tolerance. `tubes={armature_name: {...}}` supports different chains within one asset. Existing acceptance bands remain defaults.
- `combustion(..., geometry={...})` supplies burner lanes and widths, hood spread/thermal/oil heights, bowl drain center/radii/heights and drip sources, channel apex and streak locations. `ported_burner()` accepts tube/port heights, pitch/start/end, port/soot radii and thermal band dimensions. `surface(..., rust_regions={...})` sets low-height, weld and upper-height regions. All values use the part's rest frame in meters; the legacy finish presets remain available.
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

`python3 -m unittest kit.test_delivery` checks density compatibility, alias
conflicts and staged build invalidation without running a bake.

`plane_uv()` maps print corners by vertex identity, preserving intended graphics
when normal recalculation reverses an open plane's loop winding.
It also restores the authored front normal before mapping: open prints must
face outward for selected-to-active normal and AO bakes, including elevated
control panels whose winding the closed-solid normal operator can reverse.

Optional `MATERIAL_OVERRIDES={mesh_prefix: {'emission_strength': 2,
 'transmission': 0, 'ior': 1.5}}` preserves emissive/glass faces within static
consolidation. Emission uses the shared BaseColor atlas; transmission and IOR
are uniform. All variants reuse the existing three images. No overrides retains
the single-material path; normal material/image budgets remain enforced.

`STUDIO_SCALE` expands only procedural studio geometry/lights for tall props,
with inverse-square power compensation; the 1.8 m human remains real scale.
Shot `emission_scale` multiplies/restores authored material emission for day/off
comparisons without modifying the shipped asset. Defaults preserve prior views.
Optional `STUDIO_BACKDROP_HEIGHT` extends the procedural wall for upward-facing
detail cameras on tall props; lighting and the default studio remain unchanged.
Photo shots may set `background='transparent'` for neutral alpha composition
when the calibrated camera faces outside the procedural backdrop.


Shared-atlas variants use `EXPORT_ARGS := --variant NAME`. Ancestors tagged
`delivery_variant` select alternate moving parts; `atlas_staging_offset` and
`delivery_name` restore the selected part. `SOURCE_BUDGETS` optionally bounds
a staged multi-variant source separately from the per-export `BUDGETS`.
`DELIVERY_BOUNDS` optionally verifies the final imported envelope. Reference
fetching accepts WebP. Bake reports count uncovered interior UV samples and
black BaseColor samples separately from atlas padding; diagnostics never fill
missing texels. These additions use the unified `SHIP_SIZE` / density policy.
`materials.weathered_wood()` adds seeded rough-sawn pine in a per-timber source
frame: knots bend growth bands, cut-end checks and ground splash follow their
causes, and optional nail rows bake metal heads and downward stains.
`materials.galvanized()` supplies original zinc crystallization. Both retain the
existing bake-channel interface; source frames are discarded during export.

Studio shots can set `studio_yaw` in degrees to rotate the procedural backdrop,
lights and reflection flags for a reverse product view; camera and human stay
in their configured world frames. Existing shots default to zero rotation.

An asset may set `STUDIO=dict(light_scale=2.2, light_center=(.4,0,0))`
to spread the same studio lighting over a wider assembly. Position, softbox
size and power scale together, preserving approximate illumination. Defaults
retain the pilot's original lighting.

For horizontal or angled wood, pass `ground_frame` (a grade-aligned source
frame) separately from the grain frame. Splash and exposure then follow actual
height, while cut-end checks and cross-section growth rings follow the timber.

Bake isolation also translates explicit shader Object-coordinate frames with
their owning module, preserving per-timber grain. Material frames should belong
to the same isolation root as their geometry; use default Object coordinates
for a shared finish spanning several independently isolated modules. Modular
static roots may be listed in `BAKE_POLICY.moving_roots` to prevent neighboring
parts from projecting onto a reusable post or panel.

`STUDIO.backdrop_half_width` (default 12 m) can widen the seamless for long
fences or diagonally viewed assemblies, keeping dark world corners out of frame.

Run `blender -b --factory-startup --python-exit-code 1 --python
kit/test_bake_frames.py` to check preservation of explicit nested timber/parent
coordinate frames during module isolation, without a GPU bake.

Pine knots use a deterministic sparse branch-whorl population (`pine_knots`):
clear boards, pin knots and occasional larger branches with tilted resin rings,
checks and continuous grain diversion. Weathering desaturates the branch wood
as well as the board. Existing material arguments and seeded board hues remain
compatible.

`STUDIO.backdrop_color` and `backdrop_roughness` optionally tune the procedural
seamless for pale products; defaults preserve existing renders. These affect
lighting/reflection context only and never enter the exported asset.

The optional density-reduction pass scales UVs about an explicit 2D center
vector (Blender 5.2 disallows Vector/scalar subtraction); the picket pipeline
exercises this path and independently validates the resulting density/overlaps.

`TILED_MESHES` maps mesh-name globs to reserved `rect=(u0,v0,u1,v1)`, density
limits and optional `alpha_cutoff`/`double_sided`. These meshes retain authored
UVs, skip selected-to-active baking, and use the same three atlas images through
an alpha-tested material. `UV_ATLAS_RECT` reserves a separate square for unique
geometry. Verification still checks unique-island overlaps, and separately
rejects tile triangles outside their rectangle, degenerate UVs, wrong density,
or altered glTF MASK/backface behavior. Repeated tile UVs are reported explicitly.
`TEXTURE_DEPS` and optional `TEXTURE_POSTPROCESS` let an asset generate its own
original tile into the shared delivery maps after normal/color downsampling.
Defaults leave all existing opaque assets on their original one-atlas path.
Run `blender -b --factory-startup --python-exit-code 1 --python kit/test_atlas.py`
for the no-GPU finalize/export/re-import fixture and negative tile-bounds check.

`REFS_DIR` defaults to `refs`; family sublibraries may point it at a common
reference register/cache so independent `make` invocations fetch their cited
photos and manuals without duplicating downloads.

Reserved-atlas verification also measures the unique region after GLB import,
rejects any intersection between unique and tile rectangles, and checks the
embedded tile alpha actually contains both holes and retained wire. The fixture
includes negative tests for both escaped tiles and a frame invading the tile.
Density clamping scales UV vectors around an explicit 2D center, including the
previously unexercised oversized-atlas branch on Blender 5.2.

Exports with material overrides compact identical glTF texture views (same image,
sampler and extensions); BIN/image bytes are preserved. This makes the shared
three-map memory allocation explicit across glass and emission materials.

Studio shots may declare `instances=[dict(source='Chair', name='Chair_2',
location=(.5,1,0), rotation_degrees=(0,0,180))]`. Each temporary hierarchy shares
the imported mesh/atlas data and is deleted after its shot; the verified GLB
remains a reusable module library. Instance placement is absolute, in meters.
Photo-match definitions also forward optional `parts` and `instances` to the
studio so calibrated comparisons can show the same posed, repeated assembly.

`ATLAS_SETS=('Table','Chair',...)` explicitly authorizes one shared bake across
separately budgeted `asset_set` modules. It must match every source set exactly;
undeclared multi-set bakes still fail. The exporter continues to use one atlas.

An optional `MATERIAL_OVERRIDES` entry `emission_tint=(1,.12,.008)` multiplies
the shared atlas for emission only, preserving neutral off-state metals and
dark perforations without allocating another image. Omission retains the
existing untinted emission path.

Integration compatibility: `STUDIO.scale` (or `STUDIO_SCALE`) is the canonical
studio/light scale; `light_scale` is a legacy lighting-only alias, retaining
unscaled backdrop/flags for existing wide-assembly configurations. Both use one
light-position/size/power calculation. Equal aliases apply once; contradictory
explicit values fail. `light_center` offsets the lights after scaling. Backdrop
height, half-width, color and roughness remain independent controls.

Material assignment occurs per source mesh before consolidation: tiled alpha,
`MATERIAL_OVERRIDES` and either variant-tag interface compose in one export.
The export report lists assigned materials only. Alpha and glass/emission exports
compact identical texture views while preserving the shared three image bytes.

`blender -b --factory-startup --python-exit-code 1 --python
kit/test_export_policy.py` exercises composed alpha + glass/emission materials,
both variant-tag interfaces, numeric CLI/config selection, and studio aliases
without a GPU bake. Variant identifiers compare by their string representation,
so `--variant 1` also selects numeric `variant_id=1` / `EXPORT_VARIANT=1`.

Optional `EEVEE_SHOT` selects a configured final Eevee view (Makefile and
config must agree); default is `hero_closed`. Delivery docs validate its GLB
provenance. This lets optional transmission surfaces be omitted in a dry
preview when screen-space refraction cannot resolve the underlying geometry.

With no studio override, the main entry point calls the default constructor
without optional keywords, preserving zero-argument reflection-capture wrappers.
An absent legacy `STUDIO_BACKDROP_HEIGHT` no longer forwards `None`; explicit
backdrop/scale settings still pass through. `test_export_policy.py` exercises
both paths through the main entry point without rendering.

## Tiling families

`tiling_rules.mk` is an opt-in build graph for authored modular terrain, separate
from the existing unique-atlas prop graph. A family supplies `textures.py`
(`source`, `atlas`, `ship`), `build.py`, `assemble.py`, `render.py`, `check.py`,
`check_tiles.py`, `review.py`, dimensions/views and photo calibration. Declare
`ASSET`, `ASSEMBLY`, `TILE_NAMES` and `TILE_COVERAGE_<name>` in its Makefile.
No existing asset opts into this graph implicitly.

`flat_bake.py` bakes original scripted periodic BaseColor/ORM and physical height
fields onto a flat tile with GPU Cycles, before the existing channel-correct
4096→2048 filtering. No reference image is accepted by the generator.
`tiling.material()` binds ordinary stock glTF PBR maps, optional alpha and
vertex tint; `world_uv()` rephases UVs from placed world coordinates. Export
preserves authored UVs and compacts identical texture views. `edge_error()`
compares sampled positions, normals and UV phases from independent imported
surfaces. Terrain UV repetition is intentional and checked separately from
accidental coplanar surface overlap. Optional projection callbacks unfold vertical profiles; optional material filters
preserve authored decal UVs within consolidated meshes. Ground documents its
intentional construction creases separately from smooth modular boundaries.

Terrain export explicitly marks whether each material consumes vertex tint.
Blender can emit mesh-wide COLOR_0 on an untinted primitive in a mixed-material
mesh; this path strips that unused channel (glTF otherwise always multiplies
it) and compacts identical material variants. Existing unique-atlas exporters
are unaffected. `test_tiling.py` covers mixed tinted/untinted primitives, embedded
maps after saving a blend, positive/negative edge checks, and a constant-color
GPU flat bake. Run it through `with_gpu.sh`; the existing `kit.test_delivery`
unittests continue to cover the original prop graph.

Studio shots may set `human_offset=(x,y,z)` in meters to place the unchanged
1.8 m scale silhouette beside wide assets. Its position resets between shots;
existing shots retain the default position.

`TILED_MESHES` may set `alpha_mode='BLEND'` for woven cloth/net coverage that
needs to survive subpixel minification. It preserves fractional texture alpha,
while existing `alpha_cutoff` tiles retain MASK behavior. Both policies verify
embedded holes, retained threads and double-sided state; the images remain shared.

`vehicle.py` adds analytic thin-sheet panels with closed gauge and inward edge
returns, and an ISO-size radial tire with crowned tread and a smooth parked
contact patch. Callers supply all shape functions, dimensions and materials;
no existing asset path changes. Fine tire tread remains a normal-bake concern.
Returned analytic panels also derive their skin's split normals from surface
partials. This avoids area-weighted normal ripples where an irregular grid
flows around a curved opening; return faces retain geometric normals.
`blender -b --factory-startup --python-exit-code 1 --python kit/test_vehicle.py`
checks the attached panel's normals against an independent paraboloid normal,
closed-gauge manifold/volume, and the tire's actual width, top and ground contact.

`CUSTOM_CHECKPOINT=1` lets an asset supply its own `checkpoint`, `preview`,
`render` and `match` recipes (for example a body-form gate with Workbench clay
and a separate procedural reflection diagnostic). Default source recipes and
all delivery/check recipes are unchanged; the asset still includes `rules.mk`.


`vehicle.loaded_tire(..., profile_indices=None)` optionally keeps an ordered
subset of axial/radial stations for a game-density carcass. Retain both beads,
both maximum-width shoulders and the tread crown when their bounds matter.
The default profile is unchanged; the fixture also measures the reduced
profile's width, top/contact and triangle reduction and rejects invalid lists.

`vehicle_materials.py` adds meter-scale source shaders built on `materials.Nodes`:
`paint`, `manufactured`, `glazing`, `tire` and `lamp`. They expose the existing
`OUT_base/rough/metal/height` bake channels. Paint has a named `Paint tint` RGB
node; paint and emissive materials carry review-state properties. Paint also
exposes `OUT_paint_coverage` and `OUT_paint_contamination` for an RGBA delivery
packing (`tint * alpha + RGB`), so changing the factory color need not tint dust
or stone chips. The standard glTF factor alone does not implement this decode. Pass a
`VehicleRest` POINT/FLOAT_VECTOR world-position attribute (after parenting and
a dependency-graph update), vehicle axle locations and optional front/rear
bounds. This keeps causal road film attached to hinged panels. Manufactured
alloy can receive explicit brake-center positions for dust. Glazing adds frit
and privacy tint; tire height combines analytic blocks/sipes with an optional
original relief image. These are source look-dev shaders: they do not allocate
final atlases or silently change existing assets. Shader compilation and rest
position/fit checks run in the cars source checkpoint; delivery still requires
UV/bake/export and glass/emission verification.

Vehicle tire finishes accept `wear=` for a sidewall dust annulus while keeping
the tread rubber dark. Road coverage saturates at 0–1. Glass records its privacy
classification; callers supply the tint explicitly. The dated used-truck
comparisons in cars calibrate these source effects.

Vehicle finishes accept opt-in `refined=True` on `paint` and `manufactured`.
This uses dilute aft-of-tire fans, polished clear coat, sparse roughness-only
wash swirls, rail/corner dust and chrome water-spot rims. Alloy/chrome/steel
exclude the body road-film layer; alloy retains localized brake dust. Existing
callers keep their earlier defaults. Rail height and cargo-box bounds are
caller-supplied physical dimensions (`rail_height`, `cargo_bounds`). `brake_rotor()` provides concentric turned
steel relief using a wheel-centered object frame with X as its spin axis.

Vehicle `paint(..., metallic=.12, flakes=0)` exposes named `Paint metallic` and
`Paint flakes` value nodes. Change those outputs for variants; changing a linked
Principled socket default has no effect. Optional flake aggregates alter the
under-coat roughness/height bake channels without extra textures;
the clear-coat lobe stays continuous. Defaults retain the earlier appearance.

`DELIVERY_SURFACES` optionally defines uniform Principled settings, metallic/
roughness factors, emission and extras for a small delivery palette.
`SOURCE_MATERIAL_SURFACES` maps manufacturing material names to that palette;
assignment is per face before consolidation, so coated panels can retain
opaque interior faces. Existing name-prefix overrides remain unchanged.
`MAX_MATERIALS` explicitly raises the verifier's default three-material limit
for a brief-authorized palette. `BAKE_BASECOLOR_ALPHA_CHANNEL` optionally packs
a source channel into BaseColor alpha (missing channels default to one).
The downsampler filters that alpha as linear coverage, independently of sRGB.
`test_surface_profiles.py` checks four per-face surfaces, three shared images,
metallic factors, extras and retained/filtered RGBA coverage in an actual GLB.
`BAKE_SOURCE` optionally selects a generated source blend whose bake channels
need delivery-specific packing; its default remains `build/lookdev.blend`.
The reviewed look-dev scene stays an independent source audit input.
`FINAL_RENDER_SCRIPT` remains a compatibility alias for `STUDIO_SCRIPT` (see below).
`vehicle.loaded_tire(..., rolling_radius=r)` optionally uses a circular loaded
cross-section, compressing the sidewall between bead and crown. The default
parked flattening is unchanged. The vehicle fixture rotates the rolling tire
through a full revolution and checks its ground contact and width at each pose.
The circular tire option is a mean loaded-envelope approximation, without a
rotating parked flat spot; it does not simulate carcass deformation.

`finalize.py` carries authored corner normals through edit-mode triangulation
and UV packing as ordinary corner data, then reseeds the split normals. This
prevents Blender's smoothing-fan re-encoding from changing analytic panel fields;
the vehicle regression runs the real finalize path and checks the field afterward.

A prepared bake source can opt into
`BAKE_POLICY['consolidate_attribute_sources']=True` after converting its local,
generated and UV shader coordinates to mesh attributes. Projection isolation
then consolidates to one source mesh, avoiding repeated Cycles synchronization
for every exploded frame. Live Texture Coordinate/UV Map connections are
rejected; default source-frame grouping remains unchanged.

`botany.py` supplies parameterized, parallel-transport tapered stem sweeps,
root-section lobes, oriented alpha-card assembly with outward-bent custom
normals, and explicit normalized `Wind` vertex channels. Species growth rules
remain in each asset family; these additive helpers do not alter existing builds.

Photo fits may optionally declare `camera_height_m=(height,sigma)` and
`lens_bounds_mm=(minimum,maximum)`. The height is a residual prior and lens
bounds are hard limits; reports retain both. These help underdetermined
biological landmarks avoid implausible below-ground viewpoints. Existing
rigid-object fits preserve their original unconstrained behavior.
`botany.fuse_stems()` optionally unions coarse roots/leaders/scaffold wood with
voxel remeshing, collar relaxation and a caller-chosen decimation budget.
Use before UV/baking, restore wind attributes afterwards, and independently
measure the result. Fine twig geometry need not pay for the union resolution.
`botany.fuse_stems(..., connected_only=True)` optionally keeps the largest coarse
rooted component before decimation, removing disconnected sub-voxel tip crumbs.
The default retains every component for backward compatibility. Fine branching
wood should retain authored low-sided geometry rather than forcing an entire
twig network through coarse voxel remeshing.

`botany.Cards.add()` optionally accepts `clump_center` and `clump_blend` to
blend whole-crown and branch-mass radial normals before the usual card bend.
Defaults preserve the existing whole-crown policy. This gives each branch's
foliage a lit top and shaded underside without painting light into the atlas.


Botanical delivery may opt into `TILED_MESHES[name]['preserve_normals']=True`
to triangulate alpha cards with Blender's split-normal-preserving modifier.
`EXPORT_COLOR_DATA={'Wind':'_WIND'}` exports linear RGBA data as a custom glTF
attribute, without `COLOR_0` multiplying it into albedo. Both are opt-in; ordinary
assets retain the existing path. `test_botanical_delivery.py` exercises the
real finalize/export/import path and checks default behavior.

`BAKE_DEPS` and `BAKE_POSTPROCESS` optionally composite a family's own analytic
tiles into a bake before channel-correct delivery filtering; the default is empty.
This complements the existing after-filter `TEXTURE_POSTPROCESS` hook.

`STUDIO_SCRIPT` may select a family's final GLB-only presentation renderer when
the tabletop studio is unsuitable (for example, outdoor trees). It receives
the same final-source, config, camera/shot, engine, size and sample arguments.
`STUDIO_SCRIPT` takes precedence over the `FINAL_RENDER_SCRIPT` compatibility alias;
omitting both retains `kit/studio.py`.
`UV_UNWRAP_METHOD='ANGLE_BASED'` (or another Blender unwrap method) uses authored
mesh seams before the existing priority/packing/check path; absent this option,
Smart UV retains its existing defaults. Species-specific seam construction stays
in the tree family.

`UV_NORMALIZE_ISLAND_SCALE=True` explicitly normalizes each island from measured
3D/UV areas, including tiny Boolean patches the native averaging can skip.
An optional FACE float `UV_PRIORITY_ATTRIBUTE` applies relative regional density
before packing; the ordinary object-prefix priority still composes with it.
These options preserve the existing default unwrap/pack path.

Downsampling also accepts RGBA BaseColor: alpha stays linear and color is filtered
with premultiplied coverage, preserving transparent botanical/cloth edges. RGB
inputs keep their existing filtering. For independent data stored in BaseColor alpha
(such as paint-coverage or lamp-power masks), set `DOWNSAMPLE_ARGS := --alpha-mode independent`;
this filters RGB independently while retaining linear alpha. The same option is
used by the repeat-texture target. Changing it invalidates filtered textures and
export without repacking UVs or rebaking. Tangent normals retain 16-bit bake precision
until vector filtering to the shipped 8-bit map.

`BAKE_POLICY.material_ao_channel='micro_ao'` optionally multiplies a material's
original scalar `OUT_micro_ao` visibility into the geometry AO bake before ORM
packing. Use this for shallow procedural cavities represented by bump rather
than geometry. The named channel must exist on every baked source material;
omitting the option retains the existing geometry-only AO path. It adds one
emission bake, no image or runtime allocation.

Material overrides also accept uniform `specular` (Principled Specular IOR
Level, default .5). A nondefault value exports `KHR_materials_specular`, allowing
a matte finish and its `ior` to survive glTF delivery. An IOR override alone may
be omitted by Blender unless transmission, volume or specular is also exported.
`test_export_policy.py` checks these actual GLB extensions; the optional cavity
bake is exercised by `test_material_ao.py` through the GPU lock.

With authored seams and `UV_UNWRAP_METHOD`, `UV_USE_TARGET_ASPECT=True` makes
the unwrap/averaging/packing operators use the
actual delivery-region aspect (`UV_ATLAS_RECT`, or the whole square atlas),
instead of an arbitrary procedural input image's dimensions. Original image
inputs and the active material nodes are restored before saving. This prevents
a tall bark source field from squashing the shipped UVs in a wide reserved
region. Defaults remain unchanged. `test_uv_target_aspect.py` measures actual
triangle Jacobians in a non-square region and checks source-image restoration.

`flat_bake.py --height-distance` optionally gives the physical meter range of
an original normalized height field. The default stays .004 m. This lets
building tiles bake real siding and mortar relief at their declared coverage
without changing the established terrain bake.

`foliage.material()` is the maple's thin-leaf shader moved into the shared kit.
Keyword-only controls expose gloss/specular, transmission, back color, normal
strength and glancing coverage for other botanical families. Its original
maple defaults, node order and socket values are retained; the maple entry
point remains an import-compatible wrapper. No geometry or atlas code changes.

`photo_frame.frame()` moves the maple's neutral comparison margins into the kit.
The original 16% horizontal/zero vertical defaults are unchanged. An optional
`vertical_fraction` adds symmetric top/bottom margins with the camera's pose
and pixel projection preserved, so biological fits can show the entire object.
These local comparison canvases never become asset images.

`botany.Cards.add_grid(grid, rect, wind)` adds an authored curved rectangular
alpha patch with UVs and physical finite-difference normals. Species supply the
cup/droop/fold geometry; ordinary `Cards.add` and all existing defaults are
unchanged. This lets broad leaves retain curvature without crown-normal shading.

`botanical_delivery.py` is the shared raw-accessor/fresh-import botanical audit,
moved without changing the maple's checks. It measures finalized positions,
split normals and linear Wind, rejects albedo vertex colors, and reports image
and geometry memory. Families add their own species/root/budget invariants.

Finalization now honors the existing `UV_MIN_COVERAGE` family declaration, as
the independent verifier already does. Its absent-setting default stays .20;
a small unique wood region beside large reused botanical tiles need not cover
20% of the entire atlas. Overlap, density and reserved-region checks still apply.

The botanical audit matches Wind and split normals together among coincident
source vertices, so opposite blades sharing a petiole may retain independent
flutter/normals. The tolerances are unchanged. The fixture exports coincident
cards with different data and also rejects deliberately altered source Wind.

Botanical compressed-memory estimates read the embedded PNG dimensions; the
512 fixture reports 1 MiB and 2048 families report 16 MiB for three 8-bpp maps
with full mip chains, rather than assuming a particular family texture size.


## Running all regressions

Use a fresh Blender process for each `bpy` fixture. The three pure-Python test
modules run with `python3 -m unittest`:

```sh
python3 -m unittest -v kit.test_delivery kit.test_fonts kit.test_photo_match
```

Run these separately with `blender -b --factory-startup --python-exit-code 1
--python kit/<name>.py`: `test_atlas`, `test_bake_coordinates`,
`test_bake_frames`, `test_blended_atlas`, `test_botanical_delivery`, `test_botany`,
`test_export_policy`, `test_foliage`, `test_gpu`, `test_policy`, `test_surface_profiles`,
`test_uv_target_aspect`, `test_vehicle`, and `test_detachable_textures`.

`test_gpu` mocks device selection but imports `bpy` through the GPU helper, so
it also needs Blender; it performs no bake and needs no physical GPU.

`test_material_ao` and `test_tiling` perform real GPU bakes: prefix that Blender
command with `kit/with_gpu.sh`, using the same `ASSETS_GPU_LOCK` as asset builds.
Keep `TMPDIR` inside the worktree's `build/` directory.

Start each file-backed fixture with its output directory absent: `atlas-test`
(for the atlas, blended-atlas, botanical-delivery and export-policy fixtures),
`material-ao-fixture`, `surface-test`, `test-tiling`, `uv-target-aspect`, or
`vehicle-finalize-test`, respectively, all under `build/`. Run tests sharing
`atlas-test` serially. Other tests use factory-empty scenes or fresh temporary
directories and need no generated fixture files.

`test_atlas.py` supplies a coherent shared `config.py` / `finalized.blend` /
`fixture.glb` for downstream tests. Its small-region case lives separately in
`build/atlas-test/small-region/` and asserts the shared fixture files remain
byte-identical. This prevents a variant config from being verified against
another variant's UVs; BLEND and MASK validation retain their original checks.

## Held weapons (opt-in)

`weapon.py` generalizes the procedural rifle's grip-centered +Y-forward frame:
parallel zero-roll bones, rigid binding, scene-root attachment sockets, bone-riding
magazine sockets, complete endpoint keys and named NLA clips. Geometry, visual
mechanism paths and timings remain in `guns/src/`; these helpers do not affect
existing prop rigs or exports. `joined_copy()` consolidates rigid weights while
preserving the separate source parts for inspection. `export()` writes selected
objects with named clips and the caller's materials; it does not certify a baked
asset or replace the existing atlas finalizer/exporter.

`motion.sweep_clips()` tests evaluated rigid skin surfaces through every supplied
action, with fractional frame steps and explicit contact exceptions. It reuses
the established BVH / solid-parity penetration method and reports sampling,
measured penetration and exceptions. Same-bone geometry is a single assembly;
static assembly construction still needs its own review. Relative-pose caching
avoids repeating identical tests during holds and whole-asset inspect rotations.
`model.fillet_polygon()` ports the rifle's clamped polygon corner rounds, including
concave corners. Existing modeling helpers keep their defaults.

Run `blender -b --factory-startup --python-exit-code 1 --python
kit/test_weapon.py` for the frame/socket/independent-clip and positive/negative
collision fixtures, in addition to all existing kit regressions.

### Weapon holds, delivery and verification

`weapon.action()` now keys a **complete** pose at every schedule entry. Omitted
values carry forward at that boundary; add `weapon.hold(frame)` at the end of a
hold before the next movement. Scale channels use CONSTANT interpolation by
default for discrete visibility; pass `discrete=()` to animate scale continuously.
This corrects the sparse-key hazard without changing existing function arguments.
All current callers' schedules should still be reviewed for intended hold ends.

`weapon.animation_options()` is shared by both export paths. The established
`export.py` accepts opt-in `EXPORT_ANIMATIONS=True` or
`{'clips': ['YourClip', ...]}`; the latter also verifies the exported clip set.
Static exports remain unchanged. ACTIONS mode with 60-Hz sampling preserves STEP
channels and samples compound Euler motion for glTF quaternions. Blender's
NLA_TRACKS mode forces sampling and can lose discrete interpolation; it is not
the default. Muted, named NLA tracks still organize the source actions.
`EXPORT_SKIN_NAMES` consolidates the rigid parts into the configured skinned mesh.
Atlas materials, UVs and animations therefore ship through the same exporter.

Optional `DETACHABLES` entries use `armature`, `bone`, `bones` (part-owner list),
`name`, `filename`, and optional `clip`/`frame`. Export snapshots evaluated parts
in the full inverse posed bone frame **after** assigning the atlas material,
before consolidating the main skin. Zero-scale parts are omitted; source meshes,
UVs and pose are restored. Loaded/empty variants can share the origin and atlas.
The lower-level `weapon.detachable()` is also available to family scripts.

An entry may opt into `texture_size=512` or `texture_size=1024`. Its standalone
GLB then embeds its own BaseColor / OpenGL Normal / ORM set. The main gun keeps
its original atlas, UVs, materials, rig and clips. Omit the option to retain the
existing byte-identical canonical-map delivery (and existing regression).
For already separated, static variant exports, `EXPORT_TEXTURE_SIZE=512` or
`1024` applies the same operation; animated/skinned scenes reject that option.
Keep these settings in export-only configuration so they do not invalidate bakes.

`detachable_textures.py` copies the **shipped baked pixels**, with no source
rebake or resampling. It packs conservative chart rectangles without rotation
or mirroring. Each UV chart receives an integer-pixel translation and the same
positive uniform scale, `source_size / texture_size`; tangent orientation and
handedness are preserved. Float UV storage introduces small rounding errors,
measured separately by the regression. Request the smallest supported size that
fits; packing fails rather than reducing density. Material copies preserve
uniform factors, extensions and independent data in BaseColor alpha.

Each chart retains its original bilinear sampling footprint and two pixels of
additional dilation from that chart alone. Unused rectangle corners receive
that chart's padding, never other gun surfaces. Generated maps and `layout.json`
live beside the export report in `detachables/<GLB stem>/`; the layout records
source/destination rectangles and independently measured density percentiles.

**Sampling contract:** these standalone GLBs explicitly use `LINEAR` minification
and magnification, with `CLAMP_TO_EDGE`, and no mipmaps. Two-pixel guards protect
every level that sampler uses (level zero). No finite atlas gutter can isolate
multiple islands through a full mip chain ending at 1×1; glTF has no maximum-LOD
sampler field. Consumers must honor this sampler. An engine that overrides it
must supply its own LOD clamp/padding policy; unbounded generated mipmaps are
not supported by this option. At 8-bpp block compression the three base levels
cost about 0.75 MiB at 512 or 3 MiB at 1024, without inter-file texture caching.

Run `blender -b --factory-startup --python-exit-code 1 --python
kit/test_detachable_textures.py` in a fresh process (no bake/GPU required).
It exports the same loaded, empty and tilted detachables both ways, checks main
GLB byte identity, legacy image bytes, 512/1024 dimensions, bounds, disjoint
guards, deterministic output, static variants and negative configuration cases.
`detachable_verify.py` independently reads raw GLB accessors and material texture
indices, matches oriented geometry and origins, and samples ten identical
surface points per triangle in linear color, tangent normal and ORM, including
opaque alpha. Tolerance is 0.25/255 per channel; triangle tangent directions must
agree within 0.5 degrees after float storage. Its `audit()` also checks delivered
sampling, chart protection and inverse-mapped samples against the canonical atlas.
Clean `build/detachable-textures` before this fixture. The existing
`test_weapon_delivery.py` remains unchanged and still proves canonical reuse.

`BAKE_POLICY.isolate_rigid_bones=True` adds virtual projection roots `rigid:<bone>`
for non-Root rigid parts tagged with `bone`. This preserves each part's projection
and local AO without contaminating it with neighboring moving parts. Existing
moving-root and assembled-bake defaults are unchanged. Explicit shader reference
frames shared across bones should be converted to rest-coordinate attributes
before isolation; default local coordinates and explicit helper frames carrying the same `bone` tag are supported.

`weapon_verify.py` supplies complete affine bone/socket captures, fresh imports,
bidirectional surface comparisons and winding-versus-normal checks. These measure
serialization; callers must separately assert intended animation states and real
contacts. `weapon_presentation.py` supplies socket-axis aimed cameras, uniformly
timed frame-strip samples and action-aware floor handling. Family-specific
viewpoints, events and mechanical estimates remain outside the kit.

`motion.sweep_clips()` exceptions may specify `max_penetration_m`. Such pairs are
still measured and fail above that bound. Legacy skip exceptions remain supported
for backward compatibility. Required contacts remain a separate surface audit.

Run `test_weapon_roundtrip.py` in Blender for nested pump/lifter rotation and
translation, explicit holds, STEP states, full socket orientation and rotated
extraction. Run `test_weapon_delivery.py` **through with_gpu.sh** for a real
isolated atlas bake, animated atlas export/import, and loaded/empty detachable
exports with byte-identical embedded maps. Clean `build/weapon-roundtrip` and
`build/weapon-delivery` before those fixtures. Identical payloads prove canonical
atlas reuse; an engine still needs a content/atlas-ID texture cache for shared
GPU allocations. The fixture uses 128 pixels to keep regression cost low.

Checkpoint families may now declare `CHECKPOINT_OUTPUTS` and
`CHECKPOINT_RENDER_OUTPUTS` as grouped target sets, plus `CHECKPOINT_RENDER_ARGS`.
Deleting any declared blend/GLB/image regenerates its whole group. The default
single blend/render-stamp behavior remains compatible with existing families.
