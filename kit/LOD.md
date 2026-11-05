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

## Policy

Switch fractions are vertical projected extent at 1080p and a 60° **vertical**
FOV. Equivalent centered distance is `height / (2 * fraction * tan(30°))`.
This distance concerns the bound's center, not its nearest surface, and is an
estimate for a three-dimensional object viewed in perspective. Wider objects
need a bound/FOV-aware controller. There is no universal cull distance.

| Kind | Additional levels: triangle target as fraction of LOD0 @ screen height | Far texture policy |
| --- | --- | --- |
| Small repeated cone | .60 @ .25 (270px), .30 @ .10 (108px) | 512 original / near; 256 far |
| Moving hero grill | .60 @ .30 (324px), .30 @ .12 (130px), .15 @ .045 (49px) | 2048 near, 1024 middle, 512 far |
| Moving C150 pickup | .55 @ .25, .25 @ .10, .12 @ .04 (43px) | 2048 / 1024 / 512 |
| Colonial / canopy and dispenser | .60 @ .30, .30 @ .12, .15 @ .045 | Same canonical external tiles/trim at every level |
| Red maple | .70 @ .30, .40 @ .12, render-derived far impostor @ .02 (22px) | Original alpha atlas near; independent far impostor |

These are requested targets, not permission to damage an asset. The report
records achieved counts and all rejected reductions. UV splits, thin walls,
separate construction and existing low-density silhouettes can prevent a ratio.
Do not advertise a failed target as an achieved count.

All moving objects, pivots, sockets, rig weights, skin data and animation
accessors retain their names and hierarchy at every ordinary level. No far
merge is authorized in the pilots. Skinned primitives are retained verbatim;
static geometry under separate moving parents can simplify. Alpha card
primitives remain intact before the explicit final foliage impostor. Keep all
levels in the same pose during switching; a rest-only check does not establish
motion clearance after simplification.

## Texture bytes and GPU memory

New levels externalize embedded original PNG bytes **once**, using
content-addressed filenames, rather than embedding the same 2K maps in each
new GLB. LOD0 retains its existing embedded copy. Thus a cold download of the
whole chain still pays for that one duplication; downloading only a distant
level can skip the original GLB and larger maps. Engines need a content-aware
cache to share the embedded LOD0 allocation with an external copy. URI sharing
alone suffices among the additional levels. Geometry-only reduction never
reduces texture residency by itself.

Far opaque maps use linear-light BaseColor, vector-filtered/normalized normals,
RMS roughness and linear AO/metallic/independent data alpha. No UV repacking or
new bake occurs. Smaller images add their actual PNG bytes to disk. A three-map
8bpp set with full mip chains is approximately 16 / 4 / 1 / .25 MiB at
2048 / 1024 / 512 / 256. Reports compute exact 4×4 block allocations per mip,
and distinguish that estimate from PNG storage and RGBA8 engine residency.

Buildings retain maps: reducing shared tiling images for one distant building
adds parallel allocations if near buildings already use the originals. Let the
engine's texture streaming lower resident mips where supported. Ordinary PNG
glTF does not itself enforce GPU compression, streaming or unloads. Loading all
levels/maps at startup can increase residency. Far-level savings require lazy
loading/releasing resources or an engine streaming policy.

## Simplification and checks

The tool starts from **delivered accessors**, reconstructing each primitive in
Blender instead of loading source high geometry or running the asset exporter.
This retains unknown material extensions, multiple UVs, linear Wind, vertex
weathering, skin and all node metadata that an importer/exporter round trip
could drop. Blender's deterministic native collapse operates on split charts;
native planar dissolve is a fallback. Attribute fields travel through the
modifier as linear corner data. UVs and normals are then reprojected from the
delivered triangle field at the actual simplified positions; native corner
values disambiguate coincident chart sides. Normal vectors are renormalized. The LOD-only
serializer compacts referenced geometry, retaining all material and node JSON.
Every output is then freshly imported by Blender for rendering and checking.

Candidates are sampled at vertices, edge midpoints and centroids against the
source surface, with a reverse source-vertex distance check. A .35 projected
pixel surface tolerance is used at the proposed switch. UV field deviation is
bounded separately, with chart ambiguities resolved among equally close source
triangles. Open boundary paths are compared in both directions. New degenerate,
near-zero-aspect triangles, nonmanifold edges and winding/normal disagreements
reject a reduction. Existing defects are reported relative to LOD0, never
silently repaired. These are sampled geometric bounds, not an exact Hausdorff
proof, and do not replace image judgment.

Renders compare LOD0 and each level, and adjacent levels, at the same switch
camera/light, from three azimuths. Full 1920×1080 images remain on disk; strips
are native-pixel crops, with a separate framed close-up per level. Difference
images amplify absolute display RGB by six. Metrics composite on neutral gray
and use the union of asset alpha support, preventing empty background from
diluting error. Default limits: mean absolute RGB ≤.02, p95 maximum-channel
difference ≤.08, mean alpha difference ≤.05, for both original and adjacent
comparisons. These tolerate small subpixel edge filtering while rejecting
broad value/coverage changes. They are review gates, not a universal perceptual
guarantee. Close inspection and several view angles are still necessary.

`check-lod` verifies persisted original SHA256s, configuration and package
hashes/statistics, names/full transforms/extras/hierarchy/materials, topology
against LOD0, finite unit normals, fresh re-import counts and all rendered
evidence hashes. It never regenerates evidence to hide a stale failure.

Unsupported compressed mesh extensions, morph targets, sparse accessors and
network/data URIs fail explicitly. A future library sweep must inventory these,
review each ratio and shader, run motion/pose checks for interactive assets,
and accept rendered switches per asset. Do not run the pilot settings blindly.
