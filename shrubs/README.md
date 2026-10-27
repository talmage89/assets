# Foundation shrubs

Original scripted summer foundation shrubs, built on the shared botanical
kit. **Current stage: boxwood source look-dev checkpoint.** Hydrangea has been
researched but is held until the checkpoint review. No final GLB, baked stem
atlas, delivery verification or final docs JPGs are claimed yet.

The sheared hybrid boxwood has a soft mound about 0.9 m tall × 1.0 m across,
15–25 mm opposite entire leaves, a dense pruning shell, uneven new shoots and
thinner old foliage on its low +Y shaded side. Seven basal leaders share a
rooted woody core. Blender −Y is the front; the origin is at grade.

[Daylight three-quarter](renders/checkpoint/three_quarter.png) ·
[Side](renders/checkpoint/side.png) · [1 m leaf view](renders/checkpoint/close_1m.png) ·
[1.8 m scale](renders/checkpoint/scale.png) · [Contact](renders/checkpoint/contact.jpg) ·
[Full review sheet](renders/checkpoint/review-sheet.jpg) ·
[Green Velvet pair](renders/checkpoint/match_green_velvet-pair.jpg) ·
[Clipped boxwood pair](renders/checkpoint/match_clipped-pair.jpg).
These are ignored local rebuild outputs, not committed final docs images.

[Reference evidence](REFERENCE.md) · [Sources and rights](refs/SOURCES.md) ·
[Critique history](REVIEW.md).

The family reserves one 2048² BaseColor-alpha / OpenGL +Y Normal / ORM set for
both species, generated at 4096 and filtered with the kit. Its eight boxwood
tiles occupy the lower half, stems/soil an upper-left strip and future hydrangea
leaves/flower tiles the remaining upper region. Two materials at most. Full-mip
BC7 BaseColor-alpha, BC5 normals and 8-bpp ORM cost **16 MiB total**, shared
across all instances/species; geometry and engine overhead are additional.

Every source vertex carries normalized `Wind` RGBA: R height sway, G hierarchy,
B stable phase, A leaf flutter. Zero sway/flutter at grade. Wind is data, never
an albedo multiplier; final export is planned as `_WIND`, as on the maple.
No armature or moving parts.

```sh
make -C shrubs                    # current look-dev checkpoint only
make -C shrubs check              # source, camera, botanical and repo checks
make -C shrubs preview            # quick Eevee source views
make -C shrubs render match contact PASS=study WIDTH=1100 SAMPLES=32
```

Installed Blender 5.2, Python/NumPy/Pillow, fontconfig and flock are required.
Every Cycles render uses the shared GPU lock. Downloaded photos/PDFs are ignored
and used only for measuring and local comparisons. All geometry and atlas
pixels are original equations/seeded procedural output. No documentation image
is committed before the asset is final.

## Checkpoint measurements and limits

| Actual source measurement | Result |
| --- | ---: |
| Total / cap | **4,893 / 6,000 triangles** |
| Leaves / wood / soil | 3,794 / 1,082 / 17 triangles |
| Alpha cards | 1,897 |
| Retained foliage X × Y width | **1.021 × 0.981 m** |
| Retained foliage bottom / top | **0.112 / 0.880 m** |
| Complete mesh, including transparent corners | **1.101 × 1.038 × 0.907 m** |
| Source meshes / materials | 3 / 2; soil kept separate for honest wood auditing |
| Packed look-dev scene | 2,276,380 bytes |
| 2048 BaseColor-alpha / Normal / ORM PNGs | 654,733 / 1,290,223 / 134,896 bytes |
| Closed wood: nonmanifold edges / signed volume | 0 / 0.00085624 m³ |
| Actual daughter-base centers inside primary wood | 35/35, all three parity rays agree |
| Base-center distance to actual primary surface | 1.47–6.23 mm inward |
| Authored repeated-card density at 2048 | 3,701–3,910 px/m |

The retained bounds are computed by mapping actual alpha texel-center support
onto each source quad. They are not the configured dimensions or transparent
card bounds. Leaf lengths are authored 15–25 mm before small card scale and
projection variation. Core wood is fused; fine daughters are economical
intersecting closed sweeps. Their basal centers are measured inside the actual
primary surface, but hidden internal attachment caps remain at this checkpoint.
The inner card population screens bright central windows without an opaque
ball. No proof of each leaf sprite's twig attachment is claimed.

`make check` is a **source checkpoint check**, covering budget, scale, solids,
Wind, normals, tile rectangle/density, source/game geometry agreement, calibrated
camera projections and repository rules. It does not certify finalized unique
wood UVs, bake projection, final GLB serialization or engine draw calls. Final
opaque wood/soil consolidation is planned; no GLB exists yet.

Wind R is height-based (wood ×.38, leaves ×1); G is .25 primary/.5 daughter/1
leaf hierarchy; B is a seeded family phase; A is leaf flutter .6–.95 (zero for
wood/soil). The soil is anchored with R/G/A zero. No wind animation is baked.

The full source rebuild regression for extracting the maple code preserves
positions, triangle indices, corner normals, UVs, Wind and all three analytic
atlas PNGs byte for byte. A golden shader snapshot and default comparison-frame
JSON/PNG comparison also agree. This is source/content compatibility evidence;
a full maple GPU rebake/export was not run.

Remaining weaknesses: the mound is more regularly rounded and its leafy sprays
more visibly repeated than the photographs. Close views expose planar leaf
construction and angular little branches. The soil patch remains a simple thin
shape and needs a softer garden-bed transition at final delivery. The primary
reference has more upright fine sprays and richer pruning pockets. The second
reference is a different cultivar at low resolution; its camera fit cannot
establish metric identity. These limitations remain visible for lead review.

Shared kit changes are limited to `foliage.py` (extracted thin-leaf response)
and `photo_frame.py` (extracted comparison framing); their maple wrappers keep
original defaults. `kit/rules.mk` is unchanged. Hydrangea geometry, final baking,
GLB export and final docs remain held at the requested boxwood checkpoint.
