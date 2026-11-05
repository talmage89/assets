# LOD pilot review

This checkpoint preserves the actual delivered files as its reference. It does
not redesign their construction, wear or lighting response. Engine integration
and source links are in [LOD.md](LOD.md). The image comparisons use freshly
imported additional glTF levels against the original exported GLB/glTF and its
baked maps, under identical procedural light/camera settings.

## Input receipt and scope

The cone and C150 GLBs existed in this worktree. Four other pilot exports were
absent and were rebuilt locally from their scripts before establishing their
immutable-input baselines. No other worktree was used. The receipt in
`build/lod-baseline/existing.json` covers all 59 delivery/ship-map/docs files that
were present at the start, including the existing hatchback delivery. All retain
their original SHA256s. Each LOD chain separately records every original GLB or
glTF/BIN/image dependency in `export/lod/baseline.json`.

The existing cone input is 355,384 bytes; its earlier README delivery figure is
499,956. The C150 input is 11,530,720 bytes rather than its older 11,530,736-byte
README figure. These were not substituted or regenerated to match prose.
The accepted tables below measure the actual inputs. Rebuilt missing exports
can differ from older documentation in PNG or exporter-provenance bytes.

The station pilot selects the complete `Canopy` hierarchy, including islands,
and `Dispenser_1`. Its LOD0 remains the complete station delivery; only the
comparison's visible geometry is filtered. New levels omit unselected geometry
and unused materials/images while retaining the original frames. Its LOD0 byte
and resource totals therefore describe the full station container; its triangle
count describes the selected modules. Extraction savings must not be confused
with simplification savings.

The commercial legacy preservation receipt was first captured during these
trials and accidentally included eight new `houses/export/lod/` files. Its
original version is archived under `build/lod-baseline/`; all 50 original
house/ground resources were verified unchanged before excluding only those
new LOD trial entries. The unmodified commercial `make check` then passed.

## Pass 1 — geometry and field preservation

The first cone collapse candidates lost about 12.7 mm of surface and moved UVs
by more than half an atlas. They were rejected, not accepted because they hit a
triangle ratio. A split glTF vertex cannot be treated as a freely weldable
point attribute: material/UV/normal discontinuities must remain corner data.

Native collapse also interpolated UVs independently of its chosen vertex
position: an affine planar fixture exposed errors up to .3125. The tool now
reprojects the original delivered fields at the actual output positions, and
uses native corner fields only to identify seam sides. The affine fixture now
reduces while retaining both UV layers and its linear Wind field.

Acceptance is per connected construction component. A bad screw or thin return
cannot invalidate an otherwise sound body reduction. Conversely, closed thin
walls and all-seam parts must still pass surface, boundary, UV, sliver and winding
checks; a ratio never overrides them. An all-seam component now gets a real
candidate trial instead of being retained without trying. Open material
boundaries are held within 3 µm, rather than allowing a subpixel physical crack.
Zero-area UV counts are compared per layer, so an intentional constant UV1
emission swatch cannot hide a new UV0 degeneracy.

The raw tangent audit found interpolation drift up to .0178 in the tangent/normal
dot product. Blender recomputes tangents during import, so pictures alone could
miss that game-importer difference. New projected tangents are now orthogonalized
against the transported normal, normalized, and retain their handedness. The
independent audit gates dot error at .001 and tangent-length error at .0002.
Eight zero-length tangents on the original grill grease tray and four on the
station are inherited byte-for-byte. They are reported separately from new
basis errors; the fixture rejects an added zero tangent or moving an inherited
invalid corner. This is an existing delivery weakness, not a repaired LOD0.

## Pass 2 — native-size appearance critique

Color/value came first: the comparisons retain LOD0's dark cavities, black
rubber/enamel and neutral architectural paint. No source albedo or age was
changed. The 512/1024 far maps visibly soften the cone's collar edges, the
pickup's plate, and the grill's fine markings in deliberately enlarged close
views. At their switches those details are already small; original/adjacent
native-pixel comparisons are the acceptance views.

- **Cone:** the hollow slim silhouette and base outline survive. The original
  radial faceting remains visible in the construction close-ups. Do not spend
  more triangles merely to conceal that accepted LOD0 property.
- **Grill:** an early reduction made a new bright lid reflection even though its
  global mean difference passed. That was a real pop. Moving/socket geometry is
  now retained, and an 8×8 local difference gate supplements global statistics.
  The lid reflection is stable again; the hose keeps its slack shape and true
  thickness. The distant maps soften small fittings rather than whitening the
  whole object.
- **C150:** doors, hood, mirrors, wheel/steering assemblies and wipers retain
  their delivered geometry and frames. The five-color coverage/emitter alpha
  stays independent during filtering. The stock glTF fallback's very bright
  lamp interiors are already present in LOD0; they are not a new LOD highlight.
- **Colonial 27:** siding/shingle/trim phase, roof outline, window rhythm and
  door openings remain stable. It still reads like the original dense exterior
  shell. The reduction is too modest to call this an efficient far building.
- **Maple:** an eight-view trial failed coverage at 55°/145° (mean alpha error
  .0588/.0680 against a .05 limit). A controller bug also left quaternion-mode
  imported cards facing the wrong direction. The controller now rotates the
  actual world matrix; the fixture tests it. Thirty-two render directions and
  filled transparent RGB reduce angular/filtered-edge changes. Its enlarged
  close view honestly exposes a flat, soft, prelit picture: it is only intended
  for the approximately 22-pixel switch. Two ordinary near trials retained every
  triangle, so their duplicate geometry/maps are omitted from delivery.
- **Canopy/dispenser:** the fascia outline, columns, islands, cabinet edges and
  hose/nozzle construction remain legible in module and dispenser close views.
  The first wide construction view had distracting indirect fireflies from the
  powered canopy lenses at 24 samples. The comparison renderer now clamps only
  indirect radiance to 3, identically for all levels; direct light and visible
  emission retain their original values. No asset material was altered.

## Verification scope and remaining weaknesses

`make check-lod` separates raw topology/field checks, actual fresh-import
measurements, original dependency hashes, and image evidence. Imported vertex
positions and pivot matrices are measurements, not configured dimensions.
The independent normal audit checks geometry normals, UV degeneracy, skin
weights, inverse binds and animation data against LOD0. The render comparisons
judge the combined normal-map/tangent/material appearance.

The original `make check` commands establish source construction and sampled
mechanical clearance. The LOD import/pose-frame tests establish serialization;
they do not constitute a new continuous-time collision proof. Moving geometry
is deliberately retained to protect those engineered fits, and no moving parts
are merged. Static geometry is still an approximation. Engine collision should
continue to use separately chosen collision geometry.

Most requested triangle ratios are not reached. Tiny separate manufactured
parts, atlas boundaries, thin shells, protected moving geometry and already
coarse silhouettes limit generic reduction. The manifests expose each target
and achieved count; rejected attempts remain in the build reports. These
chains prove safe delivery/checking and meaningful far texture savings, not a
large geometry reduction for every asset. Do not apply these ratios blindly to
forty assets or infer a measured game frame rate from these isolated checks.

The maple billboard freezes wind and bakes daylight; a rotating camera, strong
wind, overhead views, changing sun or night can reveal a pop. Its controller
needs an engine implementation and angular/fade tuning. Shared building maps
retain their texture allocation; engine mip streaming is required to lower
residency. Loading every embedded LOD0 plus every additional level/map at startup
can increase memory. Source physics checks, byte preservation and these static
render checks do not replace an actual Godot/Unity/Unreal integration test.

## Pass 3 — accepted checkpoint

The full-size colonial strips exposed faint triangular value bands in the
siding that the global image limits allowed. Normals and UVs were unchanged;
the culprit was re-triangulated, non-affine vertex weathering. The builder now
checks interpolated color/Wind at triangle centroids and edge midpoints too,
with a .01/channel limit. A non-affine painted-plane fixture reproduces and
rejects the fault. The six chains are rebuilt with that guard before acceptance.

Final native-pixel switch strips, original/adjacent views, amplified differences
and construction close views are reviewed after those checked builds. The
compact overview is an index; it does not replace the native-size images.


The final review opened all 25 construction frames (including four dispenser
details), all 45 switch views and their amplified differences, with native pixels
preserved. Oversized construction/strip composites were reopened at original
resolution. The 32 source-rendered maple atlas sectors were also inspected.
Color/value stayed consistent; no new caved silhouette, seam swim, exposed hole
or broad faceting remains in the checked views. The colonial siding bands are
gone. Fine normal-map reflections soften at the grill far switch; the canopy
far columns show small bright-pixel changes. These stay below the local gate,
but deserve engine temporal review. The maple silhouette is still a slightly
different filtered cluster at 22 pixels; angular animation and lighting changes
are outside this acceptance.

The overview is [one sheet of all six pilots](docs/lod-pilots.jpg). Per-pilot
contacts below link to full-size switch strips, original PNGs, differences and
construction close-ups in the same directories.

| Pilot / local image index | Worst mean RGB | Worst p95 channel | Worst 8×8 mean | Worst alpha MAE | Geometry normal max / p95, degrees |
| --- | ---: | ---: | ---: | ---: | ---: |
| [traffic-cone](../traffic-cone/renders/lod/contact.jpg) | 0.00320 | 0.01569 | 0.01154 | 0.00033 | 0.9237 / 0.0000 |
| [gas-grill](../gas-grill/renders/lod/contact.jpg) | 0.00365 | 0.01569 | 0.02515 | 0.00002 | 8.6289 / 0.0000 |
| [cars](../cars/renders/lod/contact.jpg) | 0.00402 | 0.01569 | 0.05523 | 0.00000 | 2.6761 / 0.0000 |
| [houses](../houses/renders/lod/contact.jpg) | 0.00002 | 0.00000 | 0.00901 | 0.00000 | 0.0000 / 0.0000 |
| [trees](../trees/renders/lod/contact.jpg) | 0.01672 | 0.05202 | 0.02098 | 0.04364 | unlit impostor |
| [commercial](../commercial/renders/lod/contact.jpg) | 0.00834 | 0.06311 | 0.06478 | 0.00434 | 3.2553 / 0.0000 |

Limits are .02 / .08 / .08 / .05 in the four image columns. Values include
both original and adjacent comparisons over asset support, from all three
azimuths. The raw normal audit retains legitimate split-normal alternatives;
its vertex-weighted p95 is zero because most delivered corners remain exact.
It does not mean every point on each simplified triangle has zero error.

## Accepted measurements

Each load row below includes its glTF/BIN and required PNGs, or its complete
embedded GLB. Texture GPU figures assume 8-bpp blocks and full mips, with
raw mesh accessor bytes shown separately. They are estimates before engine
overhead; PNG glTF does not mandate that compression. The whole-chain total
deduplicates shared paths; it deliberately counts both embedded LOD0 images
and the external near copy when both are shipped.

### small prop

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 872 / — | 1 | 47,708 | 307,676 | 355,384 | 1.000 + 0.0434 | near |
| LOD1 | 776 / 523 | 1 | 46,434 | 307,676 | 354,110 | 1.000 + 0.0424 | 25.0% / 2.46 m |
| LOD2 | 748 / 262 | 1 | 43,355 | 101,597 | 144,952 | 0.250 + 0.0395 | 10.0% / 6.16 m |

Distinct payload dependencies for the whole chain: **854,446 bytes**, excluding optional audit JSONs.

### hero grill

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 19,912 / — | 1 | 1,592,875 | 8,784,185 | 10,377,060 | 16.000 + 1.4974 | near |
| LOD1 | 19,740 / 11,947 | 1 | 1,587,424 | 8,784,185 | 10,371,609 | 16.000 + 1.4933 | 30.0% / 3.26 m |
| LOD2 | 19,714 / 5,974 | 1 | 1,585,156 | 2,674,965 | 4,260,121 | 4.000 + 1.4911 | 12.0% / 8.16 m |
| LOD3 | 19,690 / 2,987 | 1 | 1,584,241 | 778,788 | 2,363,029 | 1.000 + 1.4903 | 4.5% / 21.75 m |

Distinct payload dependencies for the whole chain: **27,371,819 bytes**, excluding optional audit JSONs.

### C150 pickup

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 59,838 / — | 4 | 5,428,105 | 6,102,615 | 11,530,720 | 16.000 + 5.1402 | near |
| LOD1 | 59,480 / 32,911 | 4 | 5,415,346 | 6,102,615 | 11,517,961 | 16.000 + 5.1304 | 25.0% / 6.79 m |
| LOD2 | 59,368 / 14,960 | 4 | 5,397,586 | 2,046,431 | 7,444,017 | 4.000 + 5.1135 | 10.0% / 16.98 m |
| LOD3 | 59,238 / 7,181 | 4 | 5,394,499 | 683,641 | 6,078,140 | 1.000 + 5.1106 | 4.0% / 42.45 m |

Distinct payload dependencies for the whole chain: **36,570,838 bytes**, excluding optional audit JSONs.

### colonial seed 27

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 58,232 / — | 6 | 5,085,829 | 16,072,464 | 21,158,293 | 38.000 + 4.8366 | near |
| LOD1 | 58,183 / 34,939 | 6 | 5,083,625 | 16,072,464 | 21,156,089 | 38.000 + 4.8351 | 30.0% / 25.11 m |
| LOD2 | 57,739 / 17,470 | 6 | 5,046,725 | 16,072,464 | 21,119,189 | 38.000 + 4.7999 | 12.0% / 62.78 m |
| LOD3 | 57,243 / 8,735 | 6 | 5,001,821 | 16,072,464 | 21,074,285 | 38.000 + 4.7571 | 4.5% / 167.41 m |

Distinct payload dependencies for the whole chain: **36,290,464 bytes**, excluding optional audit JSONs.

### red maple

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 23,680 / — | 2 | 2,677,996 | 5,198,088 | 7,876,084 | 16.000 + 2.5496 | near |
| LOD1 | 2 / 2 | 1 | 3,036 | 2,394,277 | 2,397,313 | 2.667 + 0.0002 | 2.0% / 542.77 m |

Distinct payload dependencies for the whole chain: **10,273,397 bytes**, excluding optional audit JSONs.

### canopy and dispenser

| Level | Triangles / target | Materials | Geometry bytes | PNG bytes | Total load bytes | GPU textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 18,258 / — | 9 | 13,186,355 | 53,541,760 | 66,728,115 | 75.334 + 12.3445 | near |
| LOD1 | 15,834 / 10,955 | 4 | 1,955,303 | 6,176,884 | 8,132,187 | 23.334 + 1.8160 | 30.0% / 15.70 m |
| LOD2 | 15,134 / 5,477 | 4 | 1,887,698 | 6,176,884 | 8,064,582 | 23.334 + 1.7515 | 12.0% / 39.25 m |
| LOD3 | 14,732 / 2,739 | 4 | 1,848,542 | 6,176,884 | 8,025,426 | 23.334 + 1.7142 | 4.5% / 104.66 m |

Distinct payload dependencies for the whole chain: **72,419,658 bytes**, excluding optional audit JSONs.


### Added disk cost

| Pilot | New payload bytes beyond original delivery | Added PNG bytes |
| --- | ---: | ---: |
| traffic-cone | 499,062 | 409,273 |
| gas-grill | 16,994,759 | 12,237,938 |
| cars | 25,040,118 | 8,832,687 |
| houses | 15,132,171 | 0 |
| trees | 2,397,313 | 2,394,277 |
| commercial | 5,691,543 | 0 |

The additional opaque PNG sets are stored once per size. The original GLBs
keep their embedded maps, so a whole-chain download still duplicates that
original image payload once. The house/station add no shared-image copies.
The station byte saving per cold level includes extracting selected modules
from a full station container; geometric simplification alone saves 19.3%
of the selected source triangles. The house saves only 1.7%, the grill 1.1%,
and the pickup 1.0%. Texture residency savings are the primary practical gain
for the opaque props, provided higher-resolution resources are released.

## Commands and proof

All commands ran in this worktree; logs remain under `build/lod-logs/`.

```sh
make -C traffic-cone check -o export/TrafficCone.glb
make -C gas-grill check
make -C cars check -o export/AlderC150.glb
make -C houses SEEDS=27 check
make -C trees check
make -C commercial check
# Each of the six pilots:
make -C <pilot> lod
make -C <pilot> check-lod
blender -b --factory-startup --python-exit-code 1 --python kit/test_lod.py
python3 -m unittest -v kit.test_delivery
python3 kit/repo_check.py
```

All six original checks and all six additional LOD checks passed. The two
`-o` flags freeze existing GLBs while their original validation recipes run;
they prevent stale local modeling prerequisites from regenerating the reference
delivery. Four initially absent exports were rebuilt with their existing export
targets before their LOD baselines were established.

All 25 `kit/test_*.py` modules passed: the 24 existing modules were run
sequentially with fresh fixture directories, with `test_atlas.py` seeding its
dependent fixtures and `with_gpu.sh` wrapping the GPU fixtures. The new LOD
fixture ran from a fresh `build/lod-test/` after the final field/tangent fixes.
Negative controls reject source changes, wrong normals, flipped faces, new
tangent defects, non-affine color damage and stale checkpoint evidence.
`regressions/results.json`, `test-lod.log` and `stale-checkpoint-control.log`
record these results. The six default/check reachable dependency graphs match
the starting commit exactly (`pilot-make-graphs.json`); the six Make delivery
unit tests also pass. All 59 initially existing delivery/map/docs hashes and
all six per-chain input baselines remain unchanged. The repository check passes.

## Applying this across the library

Inventory each canonical input and pivot/socket metadata; supply an opt-in
config, protect undocumented detachable parts, and choose a shader/render recipe.
Run the tool under the shared GPU lock and review each failed target and all
native switches before accepting it. Most of these targets need asset-specific
proxy construction or a color-preserving remesh/rebake strategy for useful
triangle reductions; generic collapse alone is insufficient on this construction.
Implement resource caches, lazy loading/mip streaming and pose-synchronized
controllers in the consuming engines, plus the maple billboard/fade controller.
Then validate temporal popping, animation clearance and actual game performance.
No library-wide run or engine integration is claimed by this checkpoint.
