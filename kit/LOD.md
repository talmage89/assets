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
  kit instead checks world displacement and mip-relative UV drift separately,
  then rebakes fields on new charts when chart preservation prevents reduction. This toolkit uses Blender's native
  simplifier, not downloaded meshoptimizer code.
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
mip**. Average UV/world triangle area gives texels per meter; multiply by meters
per pixel to estimate the footprint and `log2(max(1,footprint))` for the mip.
The normalized limit is `.5*max(1,footprint)/texture_size`. Reports retain the
density, mip and normalized bound per UV layer. This is an isotropic estimate;
grazing angles and anisotropic filtering still need rendered inspection.

When a reduction removes a chart or changes a non-affine vertex-color field,
its old UVs are not represented as preserved. The level gets a new packed atlas
baked **from the immutable delivered asset**, with vertex tint evaluated once.
PBR BaseColor/alpha, roughness, metallic, existing occlusion and tangent normals
are transferred; emission, spatial transmission and clearcoat and an independent coat normal add maps only when needed.
Charts retain relative source UV/image density, with mip-derived gutters and cuts at cage-normal changes above one degree. A chart-count/size cap prevents gutters consuming the atlas; capped requests are reported and still require the same image gates. The linked source shading-normal field is evaluated as world direction and converted into the exported cage's actual tangent frame; a geometric self bake is insufficient. Original UV0/UV1 routing is explicit, and transparent graphics composite over
their real backing. For cage-ray misses, bounded nearest-surface patches evaluate
the original shader on the GPU; they never invent a replacement color. The
local two-pixel geometric allowance bounds that repair. Baked source positions
identify opaque neighboring hits as well as empty rays; hits differing from nearest compatible surface by more than .1 switch pixel are re-evaluated, within the same two-pixel distance allowance; correspondence uses
the target outward hemisphere. Records stream through small patch atlases,
and unresolved misses remain reported. Outward visibility is checked before nearest-surface fallback so a hidden lining cannot displace exterior paint. Evaluation patches stay inside their source triangle rather than extrapolating UVs into adjacent atlas charts; their geometry is centered locally to retain floating-point precision. Exact texel-center coverage separates chart padding from surface. Near-level uniform
clearcoat/transmission settings remain per material. Each independently moving
source/target pair is translated together during projection. This prevents a
door from baking its neighbor. The skin rest frame is handled explicitly.

The rebake evaluates glTF-defined shader fields. Custom meanings stored in an
opaque texture's alpha are not shader opacity and need a separate adapter.
The pickup's original lamp-power alpha is one such field: its metadata survives,
but the current rebaked opacity does not reproduce that controller's data.
Its rest checks use core glTF emission. Keep LOD0 for that custom lamp controller
until its power field is explicitly transferred and its light states are checked.

Transmissive lenses receive an additional emitted-color projection from the original geometry behind them, tinted by the front surface. This preserves powered lenses when their internal emitters merge into a shell; opaque near materials retain their original non-emitting membership.

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
    {"ratio": 0.4, "screen_height": 0.30, "rebake": true, "texture_size": 2048},
    {"ratio": 0.15, "screen_height": 0.12, "rebake": true, "texture_size": 1024},
    {"ratio": 0.05, "screen_height": 0.045, "proxy": true,
     "target_triangles": 900, "texture_size": 512}
  ]
}
```

Each level starts from delivered LOD0, avoiding accumulated simplification error.
Ordinary near atlases isolate each source material within each moving group
before projection. A retained transparent graphic cannot replace its opaque
backing, and a retained lamp emitter cannot sample the lens in front of it.
These temporary partitions are removed after baking; node names, pivots, skins
and clips remain. Shells and proxies use complete-source projection and alpha
compositing instead. Clearcoat gets its own transferred normal direction at
near levels too, because a new cage changes the otherwise implicit coat normal.
If module selection compacts material indices, ordinary near baking requires
unique original material names to recover their correspondence; ambiguous names
fail explicitly rather than sampling another material.
Original named transform nodes, metadata, sockets and pivot frames remain.
Static nodes consolidate by material into a shared mesh before decimation;
complete corner signatures weld, while geometric topology retains chart/hard
normal discontinuities as corner data. Seams may collapse along their line;
charts that cannot survive a useful reduction are rebaked. Interactive nodes
stay separate and simplify too, including normalized barycentric skin weights
on the grill's hose. Original bind matrices and clips remain. This proves data
transport; rest-view renders do not prove swept animation clearance.

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

| Kind | LOD1 | LOD2 | Last level | Map dimensions |
| --- | --- | --- | --- | --- |
| Cone | 40% @ .25 (270px) | 15% @ .09 (97px) | none | 512 / 256 |
| Grill | 40% @ .30 (324px) | 15% @ .12 (130px) | 400-1,000 goal @ .03 (32px) | 2048 / 1024 / 512 |
| C150 | 40% @ .25 | 15% @ .10 | 1,500-3,000 @ .04 (43px) | 2048 / 1024 / 512 |
| House / canopy | 40% @ .30 | 15% @ .12 | 500-2,000 @ .045 | 2048 / 2048 / 512 |
| Maple | 50% @ .08, larger cards | 20% @ .032, larger cards | crossed cards, 8 tris @ .015 | original near atlas; new far RGBA |

Ratios refer to LOD0. Targets and achieved counts are separate fields. Existing
opaque switch sizes stay fixed unless failed rendered evidence justifies a
change. The cone's far .10 switch failed its image gate and moves to .09;
the grill's original far .045 switch moves to .03 after even the farther .035
trial failed. The fixed maple impostor's
original .02 switch fails neighboring-level alpha (.0543 > .05), so it uses
.015. The previously absent maple intermediate levels get their own switches.

New near/far sets are external PNGs, never repeated embedded copies. Original
LOD0 retains every original embedded/external byte. New atlases intentionally
cost additional storage; loading an original embedded GLB plus every alternative
at startup also costs additional residency. The C150 near emission and independent coat-normal atlases add two maps (26.7 MiB versus LOD0's 16 MiB); its middle/far sets still save memory. Reports retain that near cost rather than claiming every row saves texture memory. Lazy loading, resource release and
engine mip streaming are necessary for savings. Canonical building tile maps
remain untouched; rebaked level atlases can be loaded without them when distant.
A three-map 8bpp set with full mips is about 16 / 4 / 1 / .25 MiB at
2048 / 1024 / 512 / 256. Emission, transmission and clearcoat each add a map where required. Reports count exact 4x4
block allocations per mip, distinct from PNG bytes and RGBA8 engine residency.

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
