# Foundation shrubs

Two original scripted summer foundation shrubs: a sheared hybrid boxwood and
a blooming bigleaf hydrangea. **Source look-dev checkpoint, before bake.**
Corrections and development are recorded in [REVIEW.md](REVIEW.md). No finished
GLB, baked wood atlas or final delivery validation is claimed.

[Combined contact sheet](renders/family-checkpoint/contact.jpg) ·
[Boxwood three-quarter](renders/checkpoint/three_quarter.png) ·
[Hydrangea three-quarter](renders/hydrangea-checkpoint/three_quarter.png) ·
[Reference evidence](REFERENCE.md) · [Sources and rights](refs/SOURCES.md).

| Source specimen | Boxwood | Bigleaf hydrangea |
| --- | --- | --- |
| Design size | About 0.9 m high × 1.0 m across | About 1.2 m high × 1.4 m across |
| Triangles / cap | **5,588 / 6,000** | **5,222 / 6,000** |
| Retained alpha X × Y width | 1.035 × 1.004 m | 1.433 × 1.425 m |
| Retained foliage bottom / top | 0.060 / 0.867 m | 0.053 / 1.177 m |
| Meshes / materials | 2 / 2 | 2 / 2 |
| Packed source scene | 3,689,574 bytes | 3,624,058 bytes |
| Rooted basal stems / daughters | 24 / 32 | 22 / 18 |
| Construction | Short 6–10-leaf sprigs; low, uneven clipped dome | Opposite cupped serrate blades; arching stems; 17 mopheads |

Blender −Y faces front. Both origins sit at the footprint center on grade;
woody ends meet the receiving ground. There is no separate soil polygon.
No pivots, moving parts or armature. Source vertices carry normalized `Wind`
RGBA: height sway, hierarchy, stable phase and flutter. Root sway and wood
flutter are zero; the intended export attribute remains `_WIND`.

The boxwood has dense fine sprig grain, varied leaf projection and small
highlights, replacing the rejected broad gray sheen. It is widest at the low
skirt, with thinner brown-green foliage on its shaded +Y side. Low interior
sprays screen the basal fan without a solid foliage ball.

The hydrangea has 372 individually curved outer leaves, 102 two-plane interior
branchlet clusters and 17 complete heads, six nodding. Interior branchlets
reuse six original opposite blades per card. Their individual petiole
attachments are not independently represented. Outer petiole starts and
daughter bases are measured inside actual parent wood. Outer blades are
authored 10.9–14.7 cm before projection; heads are measured from retained alpha
support rather than configured radii.

## Shared texture set

Both species use one 2048² BaseColor-alpha, OpenGL +Y Normal and ORM set,
generated analytically at 4096 and filtered with the kit. Eight boxwood tiles
occupy the lower half; the upper half holds wood, serrate leaf/branchlet and
four dusty blue/lavender/pink floret tiles. Every pixel comes from original
equations and seeded variation. Reference images never enter atlas generation.

Full-mip BC7 BaseColor-alpha, BC5 normals and 8-bpp ORM require **16 MiB total**,
shared across the family and all instances. Uncompressed RGBA8 + RGB8 + RGB8
with full mip chains would take about 53.3 MiB. Geometry and engine overhead
are additional. Each plant has two source materials: wood and foliage/sepals.
Procedural wood look-dev still needs its final atlas bake; these PNGs are
analytic source textures, not evidence of a completed GPU bake.
The current BaseColor / Normal / ORM PNGs occupy 1,004,448 / 2,218,978 /
179,482 bytes on disk; PNG file sizes are unrelated to the GPU allocation.

## Evidence and rebuild

[Boxwood Green Velvet pair](renders/checkpoint/match_green_velvet-pair.jpg) ·
[Second boxwood pair](renders/checkpoint/match_clipped-pair.jpg) ·
[Hydrangea house pair](renders/hydrangea-checkpoint/hyd_match_house-pair.jpg) ·
[Hydrangea bed pair](renders/hydrangea-checkpoint/hyd_match_bed-pair.jpg).

Each source checkpoint has Cycles daylight three-quarter, side, 1 m close-up,
1.8 m human scale, base, shaded-side and structure views, plus its two pairs.
The combined sheet includes all eighteen renders. Structure views intentionally
isolate wood. Outputs under `build/`, `textures/` and `renders/` are ignored
rebuild products; no final docs JPGs have been committed.

```sh
make -C shrubs                         # both source checkpoints; before bake
make -C shrubs check                   # geometry, botany, cameras and repository
make -C shrubs preview                 # quick boxwood Eevee study
make -C shrubs render match contact PASS=study WIDTH=1100 SAMPLES=32
make -C shrubs hydrangea-render hydrangea-match hydrangea-contact HYD_PASS=hyd-study
make -C shrubs family-contact           # combine default checkpoint evidence
```

Requires installed Blender 5.2, Python/NumPy/Pillow, fontconfig and flock. All
Cycles jobs use the kit GPU lock and procedural daylight. `make refs` restores
ignored photos/PDFs with URLs and rights recorded in `refs/SOURCES.md`.

`make check` covers source triangle/material budgets, bounds, closed positive
wood solids, actual attachments, unit normals, finite normalized Wind, alpha
support/density, independent source/game geometry agreement, calibrated camera
projections and repository rules. The combined sheet verifies every source hash
and rejects clipped pair silhouettes. Actual node/default/link/image signatures
must agree across both plants, enforcing two family material definitions.
It does not prove final UV packing,
bake projection, GLB serialization, engine draw calls or post-export appearance.
Intersecting stem sweeps retain hidden attachment caps pending finalization.

## Shared kit and limits

Earlier maple extractions remain `kit/foliage.py` and `kit/photo_frame.py`,
with maple wrappers preserving original defaults. This revision adds only
`Cards.add_grid` to `kit/botany.py`: physical normals and Wind on curved card
grids, covered by the botanical fixture. `kit/rules.mk` is unchanged. Earlier
full source regression preserved maple geometry, normals, UVs, Wind and analytic
atlas bytes; no maple GPU rebake/export was repeated for this additive method.

The boxwood remains more regular than the photograph, and repeated sprays show
at 1 m. Hydrangea outer blades and sepal shapes remain too uniform; close views
expose card intersections and simpler surfaces than real plants. Its broad
foliage/flower values differ substantially from the darker house reference,
although the selected deep pocket is much closer. The brighter bed photo has
a different exposure and overlapping plants, not a calibrated albedo target.
These are reviewable look-dev sources, not finished portfolio assets.

## Matched display-value measurements

The marked regions and complete measurements are in each render directory's
`measured-values.json` and `*-value-patches.jpg`. Y here is a weighted display
RGB value on 0–1, not linear luminance or measured reflectance. Boxwood uses a
lit-front patch; hydrangea uses broad leaf/flower populations plus shaded patches.
Photos differ in exposure, light and specimen. The leaf mask includes gray-green
highlights so it cannot hide a broad pale sheen by discarding low saturation.

| Region | Model median Y | Photo median Y |
| --- | ---: | ---: |
| Green Velvet lit foliage | 0.351 | 0.361 |
| Second clipped boxwood lit foliage | 0.361 | 0.291 |
| Hydrangea house foliage | 0.254 | 0.101 |
| Hydrangea house heads | 0.574 | 0.372 |
| Hydrangea bed foliage | 0.237 | 0.376 |
| Hydrangea bed heads | 0.549 | 0.526 |

Green Velvet's brighter-half median is 0.469 / 0.440 (model/photo), saturation
0.629 / 0.571, hue 108.9° / 102.4°. The source still has brighter highlights and
slightly cooler green. Hydrangea's house shaded patch is 0.083 / 0.075, but its
whole mass has too little of that deep shade. The bright bed's shaded patch is
0.181 / 0.126. These residuals remain visible in the pairs.
