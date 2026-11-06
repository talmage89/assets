# Additional levels of detail

The existing delivered GLB or glTF/BIN and every referenced image remain LOD0.
They are immutable inputs. `make lod` is opt-in; no existing default target or
`make check` depends on it. The builder hashes all original dependency bytes
before/after work and persists a baseline. A changed input fails until a person
reviews it and explicitly removes the obsolete generated LOD directory.

## Delivery convention and engine behavior

Separate `export/lod/<name>_LOD1.gltf` / `.bin`, etc., plus `manifest.json`.
The manifest references the original delivery as level zero. Names inside every
level retain their original meaning; only filenames get `_LOD<n>`. Never import
all levels as visible geometry, or assume the filename automatically builds an
engine LOD controller. No `MSFT_lod` extension is required or emitted.

This deliberately uses core glTF rather than tying delivery to one importer.
These are documentation-based integration instructions, not an engine test.
Sources consulted 2026-11-05:

| Engine / importer | Consumption |
| --- | --- |
| Godot 4 | Its [mesh LOD importer](https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html) already generates mesh LODs from imported glTF, using a pixel-error criterion. For ordinary geometry, loading only original LOD0 remains a good option. To use this authored chain, import the files as separate scenes and set [visibility ranges](https://docs.godotengine.org/en/stable/tutorials/3d/visibility_ranges.html) on each level's GeometryInstance3D nodes, with a small hysteresis margin. Disable automatic mesh reduction on these checked meshes to reproduce these comparisons. Runtime FOV/size-aware selection is preferable to fixed distances. |
| Unity | [glTFast's supported features](https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.14/manual/features.html) do not list `MSFT_lod`; do not assume it supports that vendor extension. [UnityGLTF](https://github.com/KhronosGroup/UnityGLTF#supported-features-and-extensions) does list import/export support. Either can import separate files. Assign the renderers for each level to a [LODGroup](https://docs.unity3d.com/6000.0/Documentation/Manual/class-LODGroup.html); its thresholds use projected height / screen height. Preserve node transforms and apply the same interaction pose to all level hierarchies, or swap mesh resources under canonical pivots. |
| Unreal | [Interchange imports glTF](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-assets-using-interchange-in-unreal-engine). Its [import reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/interchange-import-reference-in-unreal-engine) exposes Import LODs (requires Bake Meshes), LOD Groups, and normal/tangent/UV controls, but that does not establish that the glTF translator recognizes `MSFT_lod` or suffixes as LOD relationships. Import separate scenes/meshes and explicitly assemble corresponding primitive mesh LODs or visibility-switched actor components. Keep articulating parts separate and disable mesh combination/recomputed normals. Unreal screen-size semantics differ from this vertical-height convention: calibrate in its preview rather than blindly copying thresholds. |
| `MSFT_lod` | The [vendor extension specification](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Vendor/MSFT_lod/README.md) describes ordered node/material alternatives and optional `MSFT_screencoverage` extras. Support is optional; core glTF has no universal automatic LOD controller. UnityGLTF supporting it does not imply Godot, glTFast or Interchange do. Making it required would exclude importers; making it optional would silently show LOD0 only. |

## Screen-distance acceptance

The production basis (consulted 2026-11-05) is:

- [meshoptimizer simplification](https://meshoptimizer.org/#simplification) reports
  geometric error and converts it to pixels using distance, vertical FOV and
  viewport height. Its attribute-aware path weights normals, colors and UVs;
  seam restrictions can stall faceted meshes. Its permissive mode and component
  pruning address this construction. Its example normal weight is .5; guidance
  suggests roughly 1 for normalized normals/colors, and density-dependent UV
  weights around 10–100. Position and attribute error share the resulting metric.
  Blindly copying those weights would miscalibrate differently tiled assets: the
  kit uses its own split-wedge, attribute-weighted QEM for shared-map
  intermediate levels, with UV weight 10 and normal weight .5. Position is
  normalized by each construction component's diameter. UV seams are boundaries;
  corresponding wedges on both sides collapse together along the seam. Original chart fields interpolate within their own wedges, with
  normalized normals/tangents. Weighted vertex updates and endpoint alternatives
  share one geometric position across every UV/material side. Normal splits
  within a continuous UV chart retain separate corners when their normal or
  tangent direction differs by more than one degree; redundant numerical splits
  can join. This preserves the frame in which the original normal map was baked.
  Open boundaries,
  alpha graphics, glass and powered source surfaces stay fixed. Independent world/mip bounds and rendered appearance still gate the
  result. No meshoptimizer code is downloaded or used. Blender's native
  simplifier remains the proxy construction tool.
- [Godot mesh LOD](https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html#configuring-mesh-lod-performance-and-quality)
  uses a screen-space error threshold, with a one-pixel default. Its metric
  accounts for FOV/resolution; fixed world-space micrometer constraints do not.
- [Unreal automatic LOD](https://dev.epicgames.com/documentation/en-us/unreal-engine/static-mesh-automatic-lod-generation-in-unreal-engine)
  combines quadratic reduction, triangle presets, PixelError and silhouette
  importance. Its automatic switch computation uses accumulated simplification
  error. Its screen-size convention needs engine-specific calibration.
- [Unreal proxy geometry](https://dev.epicgames.com/documentation/en-us/unreal-engine/proxy-geometry-tool-overview-in-unreal-engine)
  combines multiple meshes/materials into one mesh and a newly baked material.
  Its [proxy settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/proxy-geometry-tool-reference-in-unreal-engine)
  specify pixel screen size and a merge distance that can close doors/windows.
  [World Partition HLOD](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---hierarchical-level-of-detail-in-unreal-engine)
  applies that replacement strategy to groups of actors. Here it is confined
  to the selected asset/modules, with openings judged in the original renders.
  [Simplygon's remesher](https://www.simplygon.com/features/remesher) similarly
  builds watertight proxies for a requested on-screen size, removing internal
  detail and merging appearance. These inform the far-level strategy here.

These are design references, **not an engine performance comparison**. No
Godot/Unity/Unreal runtime benchmark is claimed.

At a centered switch distance `d`, `meters_per_pixel =
2*d*tan(vertical_fov/2)/viewport_height = asset_height/(1080*screen_height)`.
The convention still uses a 60-degree vertical FOV and a 1080-pixel viewport.
Distances describe the center of the original bound. Wide/deep assets can be
larger in perspective; the actual same-camera renders account for that.

The opt-in screen policy normally uses **3/4 pixel for the area-weighted 95th percentile
of sampled structural displacement**, with a **two-pixel maximum** for localized
construction detail, and **1.5 pixels for the diameter of a removable island**.
These are this toolkit's starting choices, not numbers prescribed by the
sources. The subpixel structural limit leaves room for AA; tiny bevels and
fittings can spend a larger local allowance. Every exception is recorded with
its measured maximum and percentile. A failed glossy near view can use a stricter 0.35-pixel preset (with a 0.93-pixel local maximum); the chosen preset is recorded. No fixed 3-micrometer seam veto remains
on this path. Boundaries use the level's structural tolerance. Full component
bounds are never used to measure the distance to an intentionally omitted bolt.

For unchanged charts, UV tolerance is **half a texel of the estimated sampled
mip**. Each source triangle's UV/world area ratio gives texels per meter; multiply by meters
per pixel to estimate the footprint and `log2(max(1,footprint))` for the mip.
The normalized limit is `.5*max(1,footprint)/texture_size`. Bounds remain separate
for each material, UV layer and source triangle; a large low-density part cannot
constrain a small part's finer source charts. Reports retain the
density, mip and normalized bound per UV layer. This is an isotropic estimate;
grazing angles and anisotropic filtering still need rendered inspection.

LOD1 and LOD2 always sample LOD0's unchanged maps and unchanged material
settings. No chart replacement, downsampling or rebake is permitted on these
levels. Component-local field checks reject individual invalid collapses;
UV/normal weighting prioritizes harmless changes. Vertex frame correspondence
uses 3-degree normal / 5-degree tangent limits. Face centers and edge midpoints
use screen-relative limits: normal `clamp(15 / width_pixels, 3, 45)` degrees,
tangent `clamp(25 / width_pixels, 5, 45)` degrees. Width is the triangle's shortest
altitude divided by meters per switch pixel. Broad faces retain tight frame
agreement; tiny faces may simplify. Checking only vertices missed 23-degree normal
errors inside long cone faces; those errors changed the response of its unchanged
normal map. These angular field bounds supplement the pixel/UV bounds and do
not replace the final image checks. If chart preservation stalls
above the target, retain the higher count and report the measured miss beside
its native comparison. Never replace a target miss with a new intermediate atlas.
The source normal field, UV routing, independent BaseColor alpha data and
emission therefore keep their original meaning, including the pickup's custom
lamp-power field. Interactive names, source materials and moving membership stay.

Only the last closed proxy gets new charts, baked **from the immutable delivered
asset**. PBR BaseColor, ORM and source shading normals transfer to its new cage;
spatial emission, transmission and clearcoat get additional small maps when
required. Transparent print layers composite onto their actual backing. A closed
opaque shell owns its geometric coverage: a missed projection ray never cuts a
hole in it. Glass is represented by its transferred transmission field.
Every atlas dimension is at most 512 (the accepted tree impostor is separate).
Misses, bounded repairs, chart coverage and field-normal tests remain reported.
No high-detail modeling scene or external image enters the transfer.

Transmissive lenses receive an additional emitted-color projection from the original geometry behind them, tinted by the front surface. This preserves powered lenses when their internal emitters merge into a shell; opaque near materials retain their original non-emitting membership.
Emission keeps the antialiased direct-ray coverage, without nearest-surface
extrapolation or bake margins that could grow a bright lamp into its surroundings.
Patch repair validates shader coverage independently of alpha, so transparent
lettering pixels can correctly reveal their real backing.

Normal conversion visits each covered texel once, including shared UV diagonals,
and solves the interpolated tangent frame rather than using orthogonal-frame
dot products. Blender's [normal-map evaluation](https://github.com/blender/blender/blob/blender-v5.2-release/intern/cycles/kernel/svm/tex_coord.h) and
[triangle normal interpolation](https://github.com/blender/blender/blob/blender-v5.2-release/intern/cycles/kernel/geom/triangle.h)
define the tested frame. A regression evaluates the actual re-imported base
and coat shader outputs on a varying-normal cage, independently of that inverse.

The final arbiter remains the unchanged image limits, for LOD0 and the preceding
level at each switch (24 opaque / 128 foliage samples by default, with a seed-noise-calibrated `render_samples` override for noisy powered/specular assets; same fixed seed): mean absolute display RGB <= .02; p95 max-channel change
<= .08; alpha MAE <= .05; maximum mean RGB change in any 8x8 patch <= .08.
An additional **soft silhouette IoU loss <= .05** for opaque assets measures
`1 - sum(min(alpha0,alphaN))/sum(max(alpha0,alphaN))`. Empty background never
dilutes any metric. Foliage uses .09 for this new measure: its approximately
.55 mean union opacity makes a .05 alpha MAE correspond to about .09 IoU loss.
The thin open grill frame uses .073: original LOD0 at the far switch has mean
alpha .684/.720/.705 within its support at the three views, so the existing
.05 alpha allowance corresponds to approximately .073/.069/.071 IoU loss.
This source-only calibration follows the same opacity basis as foliage; every
candidate must still pass the original .05 alpha MAE and all RGB/local gates.
The original .05 alpha gate and all RGB/local gates remain unchanged. Three azimuths, amplified differences and independent
construction close-ups remain mandatory. Render failures are not waived to hit
a triangle count, and a target miss remains a target miss in the report.

## Configuration and assembly

Include `../kit/lod_rules.mk` at the end of the asset's Makefile, and supply
`src/lod.json`. Both `make lod` and `make check-lod` remain opt-in. The default
build/check dependency graph is unchanged. Paths resolve against the asset root.

```json
{
  "kind": "hero prop",
  "source": "export/Asset.glb",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.30},
    {"ratio": 0.15, "screen_height": 0.12},
    {"ratio": 0.05, "screen_height": 0.045, "proxy": true,
     "target_triangles": 900, "texture_size": 512}
  ]
}
```

Each level starts from delivered LOD0, avoiding accumulated error. Static parts
merge by material, while moving roots keep separate meshes and original frames.
Original named transform nodes, extras, sockets, skins and clips survive. Complete
attribute wedges preserve UV and normal discontinuities; only redundant numerical
tangent splits are canonicalized to an original representative. Compatible
material primitives simplify jointly with discrete material IDs; they split
back into their original materials afterwards. Open boundaries stay fixed.
A progressive area-error ledger enforces the same 95% structural pixel budget
throughout collapse, before the independent final surface measurement. UV error
uses each source material and UV layer's own sampled-mip bound: an unused
constant UV1 cannot impose its mip-zero bound on a minified UV0.
Small closed construction islands may disappear under the accepted pixel policy.
Powered surfaces also protect neighboring components whose bounds overlap the
powered assembly's bounds expanded by half a switch pixel. This conservative
selection keeps tiny shutters and housings from exposing an entire bright lens
after pruning; it is not a surface-contact measurement. A source-skin guard
casts rays to candidate face centers from six axes and eight corner directions.
If a formerly hidden back face wider than three switch pixels becomes
visible where the source had an outward-facing surface, the original connected
construction is retained. Its measured ray direction, facing cosines and retained
triangle cost are recorded. Visibility includes the other components in the
compatible rigid group; a separate base can cover a body's internal skin.
Thin exposures still face all original image gates. These samples guard visible layer ordering; they
are not an exhaustive self-intersection or swept-clearance certificate.
An additional assembled-edge check compares the combined candidate with its
combined source. Independently valid components can move into a shared edge,
creating a new nonmanifold contact, or separate a previously matched boundary.
Only implicated components return to their original geometry; the check repeats
until edge counts no longer increase. Receipts record the measured counts and
edge coordinates. It uses the existing one-micrometer edge-incidence convention,
not a micrometer surface-displacement budget. Geometric acceptance remains in
switch pixels. Inherited source defects remain distinguishable from new defects.
Skinned near meshes retain their source vertices/weights; foliage uses its own
larger-card path. These are rest/data checks, not swept motion certification.

At the proxy level, all geometry merges in its rest pose. Original transform
nodes remain for placement/socket lookup but no longer animate the proxy. Hold an animatable level while a door, lid or
nozzle is away from the rest pose.
Construction shells follow manifold edge adjacency, so touching trim cannot join a whole compound roof. The new shell closes construction envelopes and simplifies them in
one mesh. Smooth proxy cages keep hard edges at 35 degrees. Skinned tubes and explicit `preserve_concavity` node patterns retain
their closed source surface, including wheel openings before the common collapse/remesh. An optional
`proxy_budget` records a larger construction budget while leaving the original
`target_triangles` goal and target-miss status intact. Broad open panels receive closed outer envelopes; closed concave shells retain their footprint, including roof valleys, and filaments retain their own coarse geometry, preserving a hose loop. Subpixel
closed islands and thin features attached to neighbors may disappear; open material patches and broad face-on panels stay. Free supports
are protected by sampled attachment tests. Fully enclosed construction is
removed. Without remeshing, overlapping closed components can remain; that path does not claim a boolean union or minimal topology. Closing an envelope can fill a recess, so the
render and silhouette gates must catch a visible consequence. Optional `proxy_remesh` unions those construction envelopes on a switch-relative voxel grid before the common collapse, avoiding crossing skins. The pilots start with half-pixel cells and .3-pixel inflation (quarter-pixel / .15 for the open grill frame), all within the structural pixel allowance. The result must
have zero open/nonmanifold edges, one material and one draw call. Its independent
atlas is 512 (256 is also supported). Geometry and maps derive only from LOD0.

Planar groups also require 80% projected source coverage, unless their missing
area is at most two square switch pixels, so frame rails cannot fill a window
or gable opening. `proxy_remesh.deflation_pixels` may recover part of the union's
expansion; it is bounded by both the original inflation and half a voxel.

Build, bake and impostor work use **one Blender process**, four CPU threads by
default (`LOD_THREADS`), and the shared GPU flock only around GPU operations.
Hashing streams in 1 MiB chunks. No nested Blender jobs or library-wide parallel
builds are required. Test fixtures and per-pilot jobs should also run serially.


`protected_nodes` identifies undocumented moving/detachable roots; it keeps
frames and separate near geometry, not byte-exact high-detail topology.
`include_nodes` selects modules from a larger immutable delivery. Static merges
retain source-node provenance so those modules can still be reviewed separately.
The station pilot selects `Canopy` (including islands) and `Dispenser_1`.
Its LOD0 bytes/maps describe the complete original container; triangle counts
describe the selected modules. Extraction savings are distinct from reduction.

## Targets, switches and texture residency

| Kind | LOD1 | LOD2 | Last level | Intermediate / far maps |
| --- | --- | --- | --- | --- |
| Small prop | 40% @ .25 (270px) | 15% @ .09 (97px) | none | LOD0 / none |
| Hero prop | 40% @ .30 (324px) | 15% @ .12 (130px) | 400–1,000 @ .03 (32px) | LOD0 / <=512 |
| Car | 40% @ .25 | 15% @ .10 | 1,500–3,000 @ .04 (43px) | LOD0 / <=512 |
| Building | 40% @ .30 | 15% @ .12 | 500–2,000 @ .045 (49px) | LOD0 tiles/trim / <=512 |
| Tree | 50% @ .08, larger cards | 20% @ .032, larger cards | 8 fixed-card tris @ .015 | LOD0 / fitted RGBA |
| Modular piece | 40% @ .25 | 15% @ .09 | normally none | shared family maps / none |
| Many small props on one set | 40% @ .25 | 15% @ .09 | normally none | shared family maps / none |

Ratios refer to selected LOD0 triangles. Target and achieved counts remain
separate fields. The accepted cone's 268-triangle fallback remains the reference
for its far-level appearance. Do not lower the image gates to hit a target.
Switches above are calibrated starting points. A changed switch needs a failed
old-distance comparison and a passing new-distance comparison, both retained.

`manifest.json:resident` reports the complete fixed chain: unique original maps
**once**, only new proxy/impostor maps, and **all** levels' vertex/index bytes.
It lists LOD0 alone alongside this total, the proxy texture increment and the
additional mesh increment. Any new intermediate image hash fails `check-lod`.
Thus allowable texture residency is exactly LOD0 plus the proxy atlas; mesh
residency necessarily grows by the explicitly reported additional buffers.
These are 8-bpp 4x4-block estimates including every mip, before engine overhead,
not measured driver allocations. A three-map set costs about 16/4/1 MiB at
2048/1024/512. Additional PBR fields count as additional maps.

External building/family maps keep their canonical URIs. Embedded GLB maps are
externalized byte-for-byte once, using content-addressed filenames for the new
standalone core glTF files. This creates no new **image content**. To make GPU
sharing real, the importer must bind intermediate primitives to LOD0's material
resources. `canonical_material_bindings` maps each near material to the original material
index; `resident.canonical_image_bindings` maps each intermediate image to
its original image index and complete SHA-256. A loader that separately allocates
an embedded image and its identical external copy violates this resource policy;
filename equality or identical bytes alone does not establish shared allocation.
For selected modules, map materials by unique source name after compaction.
Keep LOD0's original container intact; extraction savings are reported separately.
Optional camera-facing foliage is an alternative to the fixed impostor, so its
cost is reported separately rather than silently loading both.

## Foliage

Intermediate tree levels use deterministic crown-cell stratification, retaining
fewer whole leaf cards with sublinear size compensation (linear exponents
.39/.40). LOD1 uses balanced occupied-cell selection. LOD2 uses density quotas,
allocated by stable largest remainders, so sparse outer cells do not outweigh
the dense crown. Its switch moves from .035 to .032 after the original alpha
gate rejected .035. Inverse-count area compensation overfilled the crown in the trials.
Every retained card keeps its source UVs, bent normals and Wind corner data.
Branches simplify separately. Enlarged cards intentionally replace the original
positions; coverage, leaf mass and silhouette must pass the switch renders.

The crossed impostor has four fixed planes / eight triangles in a 1024x256 atlas,
with opacity and scene-linear color fitted jointly against 32 own-rendered views, and a core-glTF unlit alpha material. It requires
no camera controller. Its alpha compensates for overlapping planes. Lighting
and wind are frozen; elevated views and changing sun remain limitations.
The camera-facing 32-sector, two-triangle alternative and its reference
`lod_impostor.pose()` controller is delivered alongside the fixed planes. `impostor: "crossed"` builds both;
`impostor: true` builds only the camera-facing alternative. The reference pose
sets absolute rotation/UVs around the bound center, so repeated calls do not drift. Both bake from the original
export and fill transparent RGB from the original rendered colors before mips.

## Verification and evidence

The builder starts from delivered accessors, never the high-detail source. Its
LOD-only serializer preserves unknown JSON, multiple attributes, skin and clips.
Unsupported compression, morph targets, sparse accessors and network/data URIs
fail explicitly. Original dependencies are SHA-256 checked before/after builds,
against the persisted immutable baseline. Changing source bytes cannot silently
refresh that baseline.

Checks retain topology, winding, normal/tangent validity, degenerate UV checks,
fresh Blender re-import counts, actual imported surfaces (20 micrometers) and
pivot matrices (2e-5), configuration/package/recipe hashes and rendered-evidence
hashes. New proxy shells require zero open/nonmanifold edges and positive per-island signed volumes; inward and collapsed shells fail independently of normal-vector agreement. Near shading
normals and rebaked tangent-map normalization are independently audited; proxy
cage normals are intentionally new and its baked shading is judged in images.
Skin influence interpolation normalizes weights; bind/clip preservation is
separate from an animation-clearance claim.

`build/lod/<source stem>/simplification.json` records candidates, omitted features,
UV/mip budgets and assembly policy. `export/lod/manifest.json` lists cold-load
triangles, materials, draw calls, geometry/PNG/package bytes and GPU estimates.
`renders/lod/` holds full 1920x1080 pairs, differences, native four-panel crops
(LOD0 / preceding / new / difference), per-level
960px construction close-ups elevated by 25 degrees and a contact sheet. `metrics.json` records LOD0/adjacent image
and silhouette measurements. Check reports are not game payloads.

The canopy's near cameras clip some of its wide/deep extent under the accepted
vertical-height convention. Full construction overviews show the whole module;
the near switch frames only establish what their camera actually sees. Engine
selection based on actual projected bounds needs separate calibration for this
high-aspect-ratio assembly.

Primitive draw counts are measured glTF submissions for one color pass; they
are not GPU captures of an engine's depth, shadow or refraction passes.

## Family adoption recipe

Adopt LODs only after the family's original delivery and original `make check`
are finished. Work on the family branch, merge current `main`, and keep LOD work
opt-in. Do not edit an accepted source GLB, BIN, material or image to make an LOD
pass. The six-pilot checkpoint and its remaining failures are recorded in
[LOD_REVIEW.md](LOD_REVIEW.md). This recipe is provisional while that checkpoint
has failures; a family is not approved by another family's result.

1. Add `src/lod.json` using the applicable complete example below, replacing the
   source filename and kind label. Paths resolve from the **asset folder**, not
   from `src/`. A family with several kinds adds one config per delivered kind or
   coherent module. Cosmetic variants may share a config only after their node,
   material, UV and image routing has been checked.
2. Add `include ../kit/lod_rules.mk` after the existing rules in its Makefile.
   For a single kind, `make -C family lod` and `make -C family check-lod` suffice.
   To select another config, use `make -C family lod LOD_CONFIG=src/lod-kind.json`
   and the identical override for `check-lod`. The hooks never depend on the
   original model/bake/export targets. Set `LOD_THREADS=4` or less; run one chain
   at a time. The kit handles the shared GPU lock for bake and render work.
3. Build each config, inspect the exported comparisons and close views, correct
   the config/tool as necessary, then run `check-lod`. Do not bypass a failed
   image/normal/topology/memory check. An above-target level may pass its visual
   checks, but must keep `target_met: false` and the achieved/goal counts in the
   report. Keep the established switches until failed evidence justifies a move.
4. After the final build, rerun the original family's `make check`, verify the
   immutable-source receipt, and run `python3 kit/repo_check.py`. When original
   build targets are newer than an immutable delivery, freeze the already
   accepted generated inputs with explicit `make -o path` arguments; record the
   complete command. Never let validation silently regenerate accepted LOD0.
5. Generate measured tables with `python3 kit/lod_report.py family/src/lod.json
   --write-readmes`. Supply several configs to report several kinds. A failed
   checkpoint can be documented with `--allow-failed`; that flag only reports
   failures and never changes any acceptance result. Keep full evidence ignored
   under `renders/` and `build/`; commit scripts/config/README/review only. Existing
   original docs JPGs remain byte-identical.

A car retains doors, hood, tailgate and wheels through LOD2. Authored pivot/slide
extras and animation targets are detected automatically. Add `protected_nodes`
patterns for undocumented moving roots. Each pattern protects the canonical
frame and separate near mesh, while allowing its geometry to reduce. List the
actual moving mesh names and ranges in the family README. Hold LOD0–2 while an
interaction differs from rest; the closed proxy cannot animate those surfaces.

```json
{
  "kind": "car",
  "source": "export/Car.glb",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.25},
    {"ratio": 0.15, "screen_height": 0.10},
    {"ratio": 0.05, "screen_height": 0.04, "proxy": true,
     "target_triangles": 2500, "texture_size": 512,
     "proxy_remesh": {"voxel_pixels": 0.5, "inflation_pixels": 0.3}}
  ]
}
```

A building keeps all original tiling sets, vertex tint, glass and trim-sheet
UVs near. Choose a coherent delivered building; do not merge neighboring
buildings across a placement boundary. The same example covers commercial
buildings. A module selection adds e.g. `"include_nodes": ["Canopy", "Dispenser_1"]`
and `"protected_nodes": ["*Nozzle*"]`. Selection preserves the original full
container as LOD0; its disk/mesh/map cost must still include that full container.

```json
{
  "kind": "building",
  "source": "export/Building.gltf",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.30},
    {"ratio": 0.15, "screen_height": 0.12},
    {"ratio": 0.05, "screen_height": 0.045, "proxy": true,
     "target_triangles": 1800, "texture_size": 512,
     "proxy_remesh": {"voxel_pixels": 0.5, "inflation_pixels": 0.3}}
  ]
}
```

A hero prop retains lids, knobs, wheels, sockets and any skin near. Open frames,
loops and concave castings need special inspection at the last switch. Start
with native closed envelopes; union/remesh only if the native shell's overlap or
construction actually fails. `preserve_concavity` protects named source pieces
such as wheels. Do not add a larger `proxy_budget` without reporting its target
miss and the failed lower-budget comparison.

```json
{
  "kind": "hero prop",
  "source": "export/Prop.glb",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.30},
    {"ratio": 0.15, "screen_height": 0.12},
    {"ratio": 0.05, "screen_height": 0.03, "proxy": true,
     "target_triangles": 1000, "texture_size": 512,
     "preserve_concavity": ["Wheel*"]}
  ]
}
```

A small prop normally stops after LOD2. Keep the source atlas at both levels;
there is no benefit in adding a private texture set to every repeated item.
Do not force an already tiny object to have four rows.

```json
{
  "kind": "small prop",
  "source": "export/SmallProp.glb",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.25},
    {"ratio": 0.15, "screen_height": 0.09}
  ]
}
```

A tree uses whole leaf cards, source bent normals and Wind data. Review each
species' coverage; the maple's enlargement exponents are starting values, not
universal leaf rules. `foliage_shader: "maple"` restores the existing published
maple shader from delivered maps during comparison; use it only for a compatible
source. A new shader/card convention needs an adapter and its own regression.
The fixed eight-triangle impostor is the default far choice; its separately
reported camera-facing alternative is optional and needs the supplied controller.

```json
{
  "kind": "tree",
  "source": "export/Tree.glb",
  "foliage_shader": "maple",
  "silhouette_loss": 0.09,
  "render_samples": 512,
  "levels": [
    {"ratio": 0.5, "screen_height": 0.08, "leaf_cards": true,
     "leaf_scale_exponent": 0.39},
    {"ratio": 0.2, "screen_height": 0.032, "leaf_cards": true,
     "leaf_scale_exponent": 0.4, "leaf_selection": "density"},
    {"ratio": 0.0004, "screen_height": 0.015, "impostor": "crossed"}
  ]
}
```

A modular piece preserves connectors and placement frames. Use the same endpoint
coordinates across neighboring pieces and review their joint at every level.
A whole-family shared source can be selected without copying its atlas. Give
**every config selecting the same container** a unique `name`, `output` and
`renders`; otherwise one module would overwrite another module's checkpoint.
No proxy is prescribed for a 300–2,000-triangle section. If a large assembly later
needs an HLOD, treat it as a separately reviewed building/hero proxy.

```json
{
  "kind": "modular piece",
  "name": "FenceSection",
  "source": "export/FenceFamily.glb",
  "include_nodes": ["Section"],
  "output": "export/lod/section",
  "renders": "renders/lod/section",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.25},
    {"ratio": 0.15, "screen_height": 0.09}
  ]
}
```

For many small props sharing one set, use one config per **independently placed
kind**, all referencing the same delivered family container and canonical maps.
Copy the following for each kind, changing all four kind-specific names/paths.
Do not place the whole family on one LOD controller: a nearby can and a distant
can must select independently. If each original kind already has its own GLB
with byte-identical shared images, use that file as its source instead.

```json
{
  "kind": "shared-set small prop: can",
  "name": "Can",
  "source": "export/SmallProps.glb",
  "include_nodes": ["Can"],
  "output": "export/lod/can",
  "renders": "renders/lod/can",
  "screen_space": true,
  "feature_pixels": 1.5,
  "levels": [
    {"ratio": 0.4, "screen_height": 0.25},
    {"ratio": 0.15, "screen_height": 0.09}
  ]
}
```

Every adoption owes at least **two logged LOD critique passes**. Open every
native three-azimuth strip, its original and preceding-level comparison, every
difference, and every construction/detail view. Begin with color/value, then
check silhouette, holes, hard-edge shading/tangents, normal-map phase, labels,
glass/emission and moving membership. A logo or label larger than a few pixels
must retain its shape; subpixel lettering may disappear without turning into
bright blocks. Trees additionally owe coverage/wind-field inspection; modules
owe endpoint/joint inspection. Record concrete failures, changes and final
measured results in the family's review. A contact sheet is an index, not the
scale for judgment. Keep raw checks distinct from animation clearance and
engine performance claims.

Report this cost table from the actual serialized manifest, not source constants:

| Row | Required measurements |
| --- | --- |
| Each level | Achieved/target triangles; materials; color-pass draws; geometry bytes; referenced PNG bytes and dimensions; total dependency bytes; estimated texture and mesh GPU bytes; switch fraction/pixels/distance; separate moving meshes; visual/raw check result |
| LOD0 alone | Original container bytes; unique original image allocation; original mesh allocation; sum |
| Whole fixed chain | Unique original images once + only proxy/impostor images; every level's mesh; sum; increment over LOD0 split into proxy maps and additional meshes; number of new intermediate images (must be zero) |
| Optional impostor | Replacement far texture/mesh cost and its resulting chain total, separately from the fixed choice |
| Entire shared-map family | Union original/proxy image hashes across kinds once; each distinct original container mesh once and every additional level mesh; per-instance draw/triangle costs kept separate |

For the family union, deduplicate complete `images[].sha256` values and sum their
`compressed_mip_bytes`. Deduplicate a repeated LOD0 container by its resolved
source path and delivery hash before summing `mesh_gpu_bytes`; sum the new mesh
allocations for every kind. Do not sum the per-chain texture totals blindly.
Bind every kind's near materials to the canonical family resources in the engine.
Repeated placements should instance the same selected meshes/materials, rather
than load another copy of the chain. These estimates exclude engine metadata,
shadow/refraction passes and controller cost; measure those in the target game
before making a frame-rate claim.
