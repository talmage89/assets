# Downtown / American Main Street — construction checkpoint

An original seeded family of narrow brick commercial buildings built about
1880–1930 and altered over time: shops at the sidewalk, apartments or offices
above, party walls, deep lots and an alley. Four seven-building block faces
contain 28 individually placeable buildings. This delivery stops at the
**form and construction gate**. It has quick colors and one original sign
sheet; it has no final material bake, finished trim UVs, weathering or night
lighting. Do not treat the checkpoint exports as final game deliveries.

The four regional grammars are a Midwestern two-story Italianate/masonry row,
a lower western commercial street with mid-century infill, a denser
northeastern three-story row with a projecting bay, and a southern row with
supported cast-iron galleries. Seeded variation changes the lot order, widths,
depths, heights, window cadence, cornices, original/replacement storefronts,
tenants, awnings, roofs and rear services within each regional vocabulary.

Generated images: [eye-height hero](renders/checkpoint/midwest/hero.png),
[all checkpoint views](renders/checkpoint/contact.jpg), and
[three reference pairs](renders/matches/contact.jpg). These files are generated
by `make`, remain ignored, and are not final documentation JPGs.
[REVIEW.md](REVIEW.md) records the rejected forms and corrections.

## Dimensions and construction

[REFERENCE.md](REFERENCE.md) distinguishes published measurements from authored
dimensions. [refs/SOURCES.md](refs/SOURCES.md) records every photograph, drawing,
manual, author, rights statement and use. The National Register bank nomination
anchors a documented 25 × 100 ft commercial footprint; the NPS storefront,
window and masonry briefs define the construction vocabulary. HABS photographs
and the Norwalk measured plan guide proportion and street grain. The 1904
cornice catalog supplies real stock height/projection ranges. We did not copy
a building or a manufacturer's ornament.

| Feature | Authored range / dimension |
| --- | --- |
| Interior / corner lots | 20–30 / 32–40 ft wide; 80–140 ft deep |
| Main ground / upper floor modules | 14–16 / 11–12 ft; infill ground floor 13 ft |
| Parapet | 2.5–3.5 ft above roof datum |
| Wall gauge | 440 mm front, 340 mm exposed/rear, 220 mm each party half |
| Display bulkhead | 510 mm original, 320 mm replacement aluminum |
| Retail entry | 1.04 m return depth; leaf 70 mm behind returns, 900 mm nominal leaf |
| Main transom band | 620 mm high, separate from sign-band girder |
| Upper front / rear openings | Up to 1.02 × 1.96 / 1.02 × 1.63 m |
| Sash inset | 105 mm Italianate front, 190 mm masonry/rear |
| Segmental arch rise / sill | 220 / 120 mm |
| Corner chamfer | 1.45 m back on both outer edges, actual diagonal wall |
| Gallery | 2.70 m deep; 120 mm columns, supported deck and falling canopy |
| Fire escape | Up to 5.60 m walk, 2.45 m return projection, 1.067 m guard, 880 mm flights |
| Sidewalk | 12 / 14 / 16 ft curb to building, by region |

The facade has real wall holes and reveals. Angled display returns meet a
recessed terrazzo entry; storefront piers, plinths and girder carry the upper
wall. Separate stair doors survive storefront tenant changes. Upper sashes
have different planes, meeting rails, stools, sills and segmental/flat heads.
A seeded upper opening retains its old hood and sill around later brick infill.
Some hoods and cornices are formed-metal assemblies with profiled brackets,
ledges and dentils; other fronts have corbelled brick. The northeastern bay
has three glazed planes, a roof and visible brackets.

Corner fronts have diagonal entrances and display openings on their public
side. The rear has actual service openings, supported escape platforms,
bar grating, inclined flights, wall anchors, scuppers, strapped downspouts,
meters, conduit loops and occasional shed additions. Roofs fall toward the
rear; parapets, coping, skylights, varied equipment and chimney masses remain
geometry. Ghost lettering and a demolished-neighbor roof scar occur on the
exposed end wall. Current lettering is fictional, generated with installed
open DejaVu fonts. No reference pixel enters a texture.

Shop rooms are shallow, economical volumes: diner booths/counter/stools,
hardware/antiques shelves, barber chairs and mirrors, vacant kraft paper,
and bank/hotel counters. Upper openings have dark rooms, curtains, partial
blinds and an occasional window air conditioner. These are exterior shells
with shallow visible rooms, not playable complete floor plans.

## Generator, placement and doors

`src/plan.py` is pure Python. Inputs are integer `seed`, one of `midwest`,
`western`, `northeast`, `southern`, and a bounded lot count of 4–12. `load()`
also accepts an authored JSON plan. Regional constants describe permitted lot
widths/depths, story/style distributions, masonry palette, walk width and
parking type. First and last lots are wider corners; one infill is reserved
in the Midwestern/western grammar. The same seed gives identical geometry
and sign pixels; budgets are measured on actual generated meshes.

The four proof plans use seeds 411, 512, 613 and 714. `src/build.py -- --seed N
--region western --count 8 --out build/custom.blend` generates another block
and retains its individual glTFs. This replaces that region's diagnostic block;
run `make -B model` to restore the four default proof blocks afterward. Supply
those arguments after the normal headless Blender invocation, not to Python.

Each building exports one stock `.gltf` plus `.bin`; all image references
resolve to `export/textures/T_DowntownFormSigns_BaseColor.png`. Keep that shared
folder and cache by canonical URI. A block face is its list of placed building
instances in `build/blocks/<region>/block.json`; the assembled `.glb` beside it
is a diagnostic export. Origin is the ground center of the rectangular lot
footprint. Blender +Z is up, frontage −Y; glTF is +Y up, +Z forward. Mesh scales
are applied. Front placement aligns the `FrontLine` socket to the sidewalk.

| Node suffix | Function |
| --- | --- |
| `Socket_PartyLeft`, `Socket_PartyRight` | Lot-line X planes; different lot depths intentionally have different midpoint Y |
| `Socket_FrontLine`, `Socket_RearAlley` | Building/sidewalk and alley interfaces |
| `Socket_*DoorThreshold` | Actual door threshold; stores nominal leaf width |
| `Socket_BladeBracket` | Wall support for the projecting sign |
| `Socket_AwningLeft`, `Socket_AwningRight` | Paired frame attachments |
| `StoreDoor`, `StairDoor`, `ServiceDoor` | Separate leaf meshes below actual hinge pivots |
| `CornerDoor`, `GalleryDoor` | Present only when the construction requires them |

All door pivots rotate about local Blender +Z (glTF +Y) through 0–100° inward.
The upper gallery doors meet the deck. No armature or animation clip is needed.
The sampled sweep checks every actual leaf against the fixed triangles at 5°
increments, not a constant clearance claim or just serialization.

## Geometry and resource budget

Six quick material states maximum per building; static construction is joined
inside each root, with separate moving leaves. Fine brick coursing, stamped
ornament, surface damage and small wear belong in shared normal/color maps,
not individual brick meshes. Some small fronts fall below 8k because adding
faces would not improve their silhouette.

| Block / seed | Frontage | Building triangles | Checkpoint GLB bytes |
| --- | ---: | ---: | ---: |
| Midwest / 411 | 60.655 m | 67,814 | 8,859,048 |
| Western / 512 | 58.826 m | 48,686 | 6,469,164 |
| Northeast / 613 | 56.083 m | 104,680 | 13,590,240 |
| Southern / 714 | 65.227 m | 80,856 | 10,521,920 |

Actual individual geometry (gltf + bin MiB excludes the shared image):

| Building | Lot | Stories | Parapet height m | Triangles | Geometry MiB |
| --- | --- | ---: | ---: | ---: | ---: |
| Midwest_411_01 | 32 × 100 ft | 2 | 8.687 | 11,518 | 1.417 |
| Midwest_411_02 | 27 × 110 ft | 2 | 8.992 | 11,650 | 1.440 |
| Midwest_411_03 | 22 × 90 ft | 2 | 9.296 | 7,422 | 0.914 |
| Midwest_411_04 | 27 × 90 ft | 1 | 4.877 | 3,256 | 0.415 |
| Midwest_411_05 | 25 × 90 ft | 2 | 8.534 | 11,026 | 1.353 |
| Midwest_411_06 | 30 × 90 ft | 2 | 8.382 | 8,738 | 1.068 |
| Midwest_411_07 | 36 × 90 ft | 2 | 9.296 | 14,204 | 1.741 |
| Western_512_01 | 36 × 100 ft | 2 | 8.382 | 15,636 | 1.915 |
| Western_512_02 | 25 × 100 ft | 1 | 5.029 | 4,636 | 0.593 |
| Western_512_03 | 28 × 100 ft | 1 | 5.334 | 3,314 | 0.422 |
| Western_512_04 | 24 × 100 ft | 1 | 4.724 | 3,196 | 0.409 |
| Western_512_05 | 24 × 90 ft | 1 | 5.944 | 4,550 | 0.581 |
| Western_512_06 | 20 × 80 ft | 1 | 5.639 | 3,508 | 0.446 |
| Western_512_07 | 36 × 80 ft | 2 | 8.992 | 13,846 | 1.697 |
| Northeast_613_01 | 36 × 120 ft | 3 | 12.497 | 23,528 | 2.895 |
| Northeast_613_02 | 20 × 120 ft | 2 | 8.839 | 10,602 | 1.307 |
| Northeast_613_03 | 20 × 120 ft | 3 | 13.259 | 9,362 | 1.156 |
| Northeast_613_04 | 26 × 100 ft | 3 | 12.497 | 13,278 | 1.629 |
| Northeast_613_05 | 20 × 100 ft | 3 | 12.497 | 12,344 | 1.516 |
| Northeast_613_06 | 26 × 140 ft | 3 | 13.259 | 11,990 | 1.485 |
| Northeast_613_07 | 36 × 140 ft | 3 | 12.649 | 23,576 | 2.868 |
| Southern_714_01 | 36 × 120 ft | 2 | 8.992 | 15,934 | 1.955 |
| Southern_714_02 | 30 × 90 ft | 2 | 8.992 | 13,374 | 1.639 |
| Southern_714_03 | 25 × 120 ft | 2 | 9.296 | 9,284 | 1.140 |
| Southern_714_04 | 23 × 120 ft | 2 | 8.992 | 6,018 | 0.750 |
| Southern_714_05 | 30 × 90 ft | 2 | 8.687 | 9,028 | 1.123 |
| Southern_714_06 | 30 × 100 ft | 3 | 11.735 | 9,166 | 1.130 |
| Southern_714_07 | 40 × 90 ft | 2 | 8.992 | 18,052 | 2.201 |

The shared checkpoint sign image is 2048² / 174,836 disk bytes, about 5⅓ MiB
with BC7 and mipmaps. It is loaded once for the family. The proposed final
allocation is **42⅔ MiB** across three shared PBR sets plus sign and interior
sheets, serving six materials maximum; [TEXTURES.md](TEXTURES.md) explains
region packing, physical purposes, texture sizes and memory assumptions.
Those final maps have not been generated or certified.

## Street and presentation

New downtown-only pieces provide full building-to-curb poured sidewalks,
sidewalk returns and triangular paving at chamfered entries, short cross-street connections,
real open tree pits with flush grates, straight six-inch curbs, an opposite
sidewalk, roadway with parallel/60° parking marks, and a rear alley with loading
aprons for different building depths. They use the ground family's 152.4 mm
curb datum. `export/DowntownStreet_<region>.glb` is separate from the building
assets; no ground delivery or shared kit file changes.

The hero is an eye-height 1.68 m view from the opposite sidewalk at 40 mm on
a 36 mm sensor, under a procedural raking sun. Context uses the existing
library's pickup, crossover, hatchback, maple and street-light generators.
Their source forms are generated inside `downtown/build/context/`, imported
for presentation, and excluded from downtown exports. Vehicle context has
quick colors; it does not claim the cars' final baked delivery. Context source
hashes and every camera/source GLB hash are recorded in render provenance.
The whole-block elevations use a wide panorama from the opposite sidewalk;
the overhead/rear cameras fit the actual imported architecture bounds;
the hero keeps its measured eye height and lens.

## Rebuild and evidence

Requires installed Blender 5.2, Python/Pillow/NumPy, DejaVu fonts and flock.
No packages, models, textures, lighting or executable code are downloaded.
Reference downloads are image/PDF inspection material only. All temporary data
stays inside this worktree's ignored build folders. Every Cycles invocation
holds the shared kit GPU lock and requests OptiX/CUDA.

```sh
make -C downtown                 # complete form checkpoint, then stop
make -C downtown check           # 4,000 plans, actual meshes/imports/doors and repository rules
make -C downtown check-repeat    # rebuild and compare exported geometry/image bytes
make -C downtown check-sweep     # 48 additional actual buildings against geometry caps
make -C downtown matches         # three calibrated HABS photo pairs
make -C downtown WIDTH=1000 SAMPLES=16 render
```

`build/check.json` separates raw accessor serialization, fresh-import
preservation, physical ray measurements, party interfaces and motion.
`build/motion/*.json` records 89 doors × 21 sampled positions with no
exemptions. Independent steel-surface rays also measure feet at grade and
3.328–3.605 m minimum sampled vertical clearance between stacked escape flights. `build/plan-check.json` records 4,000 deterministic plan checks;
this is not a claim that 4,000 full buildings were rendered. Additional mesh
sweep and repeat reports live beside it. Staging UVs are checked for finite,
nondegenerate triangles; final trim density and overlap proof are deferred.

Remaining limitations: quick/unworn surfaces; repeated sash and rear equipment
details; simple flat room furniture; coarse cornice ornament; no final brick
coursing, causal damage, window vinyl, night lights, collision
or LOD delivery. Photo calibration is approximate and uses small archival
service images; residuals remain visible. The photographed buildings differ
from these original plans. No source-render or measurement check is presented
as proof of final photorealism.
