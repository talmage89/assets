# Downtown / American Main Street

An original scripted family of 28 individually placeable commercial buildings,
arranged as four seeded seven-lot block faces. Built about 1880–1930 and altered
over time: recessed shops, separate stair entries, apartments and offices,
party walls, deep lots and service alleys. Accepted dimensions, lot rhythm,
regional grammars and storefront organization are retained. The family uses shared baked surfaces, articulated cast and pressed ornament,
and four town presentations.

Generated evidence stays ignored; no docs images are published at this gate:
[eye-height hero](renders/checkpoint/midwest/hero.png),
[dusk](renders/checkpoint/midwest/dusk.png),
[all views](renders/checkpoint/contact.jpg),
[matched-light pairs](renders/matches/contact.jpg),
[focused storefront pair](renders/matches/foster_storefront-pair.jpg),
[before/after fixes](renders/fixes/), and
[source-field comparisons](renders/source-matches/).
[REVIEW.md](REVIEW.md) records the full-size critiques, including rejected fits.

## Dimensions and construction

[REFERENCE.md](REFERENCE.md) separates published measurements from authored
choices; [refs/SOURCES.md](refs/SOURCES.md) gives image/PDF credits and uses.
The Lawrence County Bank nomination anchors a 25 × 100 ft commercial lot;
NPS briefs establish storefront, sash and masonry construction. HABS photographs
and the Norwalk plan guide proportion and urban grain. The 1904 cornice catalog
supplies stock height/projection ranges. These are original buildings rather
than surveyed copies of the references.

| Feature | Authored dimension |
| --- | --- |
| Interior / corner widths | 20–30 / 32–40 ft; depths 80–140 ft |
| Ground / upper floor modules | 14–16 / 11–12 ft; infill ground floor 13 ft |
| Parapet | 2.5–3.5 ft above roof |
| Wall gauges | 440 mm front, 340 mm exposed/rear, 220 mm each party half |
| Bulkheads | 510 mm original, 320 mm aluminum replacement |
| Retail entry | 1.04 m return; leaf 70 mm farther back; 900 mm nominal leaf |
| Transom | Separate 620 mm band above display sash |
| Upper front / rear openings | Up to 1.02 × 1.96–2.20 / 1.02 × 1.63 m |
| Sash inset | 105 mm Italianate front; 190 mm other masonry/rear |
| Corner chamfer | 1.80 m setback on both outer edges |
| Bank lobby | 300 mm landing, two measured 150 mm risers; retail entry at grade |
| Metal cornice | 825 mm profile height; 610 mm standard / 708 mm heavy-corner projection |
| Gallery | 2.70 m projection; 120 mm columns; 1.06 m guard |
| Fire escape | Up to 5.60 m walk, 2.45 m return; 880 mm flights; 1.067 m guard |
| Walks | 12 / 14 / 16 ft by region; 152.4 mm curb datum |

Walls have actual apertures and reveals. Original iron storefronts have
tapered column/pilaster shafts, bases and capitals; replacement aluminum fronts
remain plain. Profiled hood molds carry ears, keys and consoles, with peaked
hoods on the original Italianate iron fronts. Washed stone sills have a 170 mm
body plus a 60 mm lower molding and include drip undercuts; lintels have drafted
faces. Pressed-metal cornices carry paired
scroll brackets, modillions, dentils, recessed frieze fields and a reserved
central date panel. Other fronts have corbelled brick and belt profiles.
Geometry carries the silhouette; tooling and pressed fine relief use normals.

Canvas sags across frame bays and ends in a scalloped hanging valance. The
bank/hotel corners have 45° cut entries with a separate transom,
stone bearing piers, a base/water table and a 10 m stone public return, heavier fronts and name
stones. Rear variation includes different-depth hollow ells, sloping additions,
back porches/stairs, changing sash, stepped parapets and retained fire escapes.
Downspouts are strapped to walls; conduit bends and loops follow their supports.
Shop and upper rooms are shallow visible volumes with fixtures, shelves,
curtains and blinds, rather than complete playable interiors.

## Placement and motion

`src/plan.py` takes an integer seed, a region (`midwest`, `western`,
`northeast`, `southern`) and 4–12 lots; `load()` also accepts an authored plan.
The proof seeds are 411 / 512 / 613 / 714. A custom build uses the usual
headless Blender command followed by `-- --seed N --region western --count 8
--out build/custom.blend`. It replaces that region's diagnostic block;
`make -B model` restores the four proof blocks.

Each building is one stock glTF plus its geometry bin, referring to the same
11 images in `export/textures/`. Keep this directory layout and cache canonical
image URIs. `build/blocks/<region>/block.json` lists placements and costs;
its assembled GLB is diagnostic. Presentation context is excluded from building
deliveries. Origins are ground-level lot centers; frontage is Blender −Y,
up +Z (glTF forward +Z, up +Y). Mesh scales are applied.

| Node suffix | Purpose |
| --- | --- |
| `Socket_PartyLeft`, `Socket_PartyRight` | Lot-line planes |
| `Socket_FrontLine`, `Socket_RearAlley` | Street/alley placement interfaces |
| `Socket_*DoorThreshold` | Actual threshold and nominal leaf width |
| `Socket_BladeBracket` | Projecting-sign wall attachment |
| `Socket_AwningLeft`, `Socket_AwningRight` | Frame attachments |
| `StoreDoor`, `StairDoor`, `ServiceDoor` | Separate leaves under hinge pivots |
| `CornerDoor`, `GalleryDoor`, `EllDoor`, `PorchDoor` | Conditional moving leaves |

All leaves rotate inward 0–100° about local Blender +Z (glTF +Y).
The actual imported surfaces are checked every degree. There are no collision
exemptions or armatures. The kit handles BVH crossings/edge distances; the
building audit uses oriented solid-angle membership for joined solid members,
with both hollow-room and contained-collision fixtures. This is a sampled
geometric test, not structural or building-code certification.

## Assemble a street

Build the family, then load the seven stock glTFs listed in a region's
`build/blocks/<region>/block.json`. Place each root at its `position` (Blender
coordinates). For glTF/Godot coordinates convert `(x,y,z)` to `(x,z,-y)`.
The manifest's different lot depths share one front line: Blender Y=0.
Adjacent party-line planes share X; their socket midpoints differ in depth.
The two 220 mm half-walls remain inside their respective lots.

Load `DowntownStreet_<region>.gltf` at the street origin. It supplies the whole
walk, curb, roadway, tree pits, parking and alley. The road lies 152.4 mm below
the walk. Street-lamp bases and trees use the pit/walk datum; parked cars use
the road datum. Join another block at either end with the requested cross
street and walk widths; the frontage and corner cut are in the manifest.
An opposite block faces the first after a 180° vertical-axis rotation, with
its front line at Blender `Y = -2*walk-road_width`.

The four seven-lot seeds are independent proof towns, not a rule to mix every
style into one street. Choose a region and integer seed for another row.
Individual buildings remain independently placeable, and signs/awnings use
shared sheet regions. Keep the canonical texture directory beside the glTFs;
cache images by resolved URI so a town loads each map once.

## Geometry and resources

<!-- METRICS_START -->
| Block / seed | Frontage m | Building triangles | glTF + bin bytes | Diagnostic GLB bytes |
| --- | ---: | ---: | ---: | ---: |
| midwest / 411 | 60.655 | 95,278 | 13,217,831 | 30,345,532 |
| western / 512 | 58.826 | 69,590 | 9,718,614 | 26,853,232 |
| northeast / 613 | 56.083 | 135,168 | 18,828,210 | 35,956,544 |
| southern / 714 | 65.227 | 121,620 | 16,942,431 | 34,065,328 |

| Building | Lot ft | Stories | Front datum m | Triangles | Materials | glTF + bin bytes |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Midwest_411_01 | 32 × 100 | 2 | 8.687 | 15,980 | 6 | 2,237,398 |
| Midwest_411_02 | 27 × 110 | 2 | 8.992 | 13,974 | 6 | 1,936,151 |
| Midwest_411_03 | 22 × 90 | 2 | 9.296 | 11,878 | 6 | 1,646,309 |
| Midwest_411_04 | 27 × 90 | 1 | 4.877 | 4,836 | 5 | 667,370 |
| Midwest_411_05 | 25 × 90 | 2 | 8.534 | 16,322 | 6 | 2,245,499 |
| Midwest_411_06 | 30 × 90 | 2 | 8.382 | 14,762 | 6 | 2,033,663 |
| Midwest_411_07 | 36 × 90 | 2 | 9.296 | 17,526 | 6 | 2,451,441 |
| Western_512_01 | 36 × 100 | 2 | 8.382 | 25,298 | 6 | 3,568,879 |
| Western_512_02 | 25 × 100 | 1 | 5.029 | 6,144 | 6 | 843,873 |
| Western_512_03 | 28 × 100 | 1 | 5.334 | 5,086 | 6 | 697,147 |
| Western_512_04 | 24 × 100 | 1 | 4.724 | 4,788 | 5 | 661,129 |
| Western_512_05 | 24 × 90 | 1 | 5.944 | 5,922 | 6 | 817,531 |
| Western_512_06 | 20 × 80 | 1 | 5.639 | 5,140 | 6 | 721,380 |
| Western_512_07 | 36 × 80 | 2 | 8.992 | 17,212 | 6 | 2,408,675 |
| Northeast_613_01 | 36 × 120 | 3 | 12.497 | 27,978 | 6 | 3,943,152 |
| Northeast_613_02 | 20 × 120 | 2 | 8.839 | 15,652 | 6 | 2,163,844 |
| Northeast_613_03 | 20 × 120 | 3 | 13.259 | 14,354 | 6 | 2,015,854 |
| Northeast_613_04 | 26 × 100 | 3 | 12.497 | 19,300 | 6 | 2,650,705 |
| Northeast_613_05 | 20 × 100 | 3 | 12.497 | 14,944 | 6 | 2,061,249 |
| Northeast_613_06 | 26 × 140 | 3 | 13.259 | 15,170 | 6 | 2,119,268 |
| Northeast_613_07 | 36 × 140 | 3 | 12.649 | 27,770 | 6 | 3,874,138 |
| Southern_714_01 | 36 × 120 | 2 | 8.992 | 25,512 | 6 | 3,621,889 |
| Southern_714_02 | 30 × 90 | 2 | 8.992 | 18,714 | 6 | 2,574,096 |
| Southern_714_03 | 25 × 120 | 2 | 9.296 | 15,238 | 6 | 2,106,825 |
| Southern_714_04 | 23 × 120 | 2 | 8.992 | 9,360 | 6 | 1,303,581 |
| Southern_714_05 | 30 × 90 | 2 | 8.687 | 11,212 | 6 | 1,532,242 |
| Southern_714_06 | 30 × 100 | 3 | 11.735 | 12,058 | 6 | 1,658,946 |
| Southern_714_07 | 40 × 90 | 2 | 8.992 | 29,526 | 6 | 4,144,852 |

| Street piece | Triangles | glTF + bin bytes |
| --- | ---: | ---: |
| midwest | 8,509 | 1,205,085 |
| western | 8,230 | 1,169,061 |
| northeast | 8,378 | 1,187,701 |
| southern | 10,368 | 1,473,146 |

Front datums are authored parapet/cornice levels. Covers rise 45 mm above them;
seeded stepped rear parapets rise up to 480 mm farther. These are plan values,
not reported as independent height measurements.

The 28 buildings total **58,707,086 bytes** of glTF/bin;
four street pieces total **5,034,993 bytes**. Eleven shared
images total **17,162,063 bytes**. The deliverable family is
**80,904,142 bytes**, excluding diagnostic GLBs and presentation context.
<!-- METRICS_END -->

There are five material states on small infills and six on the other buildings.
Static construction is joined by material; moving doors remain separate.
[TEXTURES.md](TEXTURES.md) details the **42⅔ MiB** compressed allocation with
complete mip chains: masonry 2048², mineral/roof 1024², finish 2048², signs
2048² and interior 1024²; eleven images in total. RGBA8 uploads with mips cost
170⅔ MiB. Compression and caching remain engine-import policy. The stock
Blender importer independently verifies reuse of eleven image datablocks
across all 28 buildings, four street pieces and a repeated import.

The houses' existing running-bond brick lacks common-bond header courses and a
neutral painted-brick strip. Downtown therefore adds a shared masonry set;
other families' maps remain byte-identical. Physical coursing, neutral mortar,
kiln variation and guarded chart regions survive stock glTF. Reused tile/trim
charts intentionally overlap; these are not unique lightmap UVs.

Rest-position vertex colors add low splash, sill runoff, scupper damp,
oxide below escape fixing plates, localized repair variation and door/shoe handling, preserving each substrate's
color. Fine finish losses follow folded edges. Ghost paint breaks along
courses/joints and irregular losses; transparent areas expose the real brick.
`--wear 0` disables broad construction weather for a control. All vertices and
texels are generated by our scripts; reference pixels never enter materials.

## Street and setting

Downtown street glTF/bin exports remain separate from buildings and refer to
the same canonical images. They contain full
building-to-curb sidewalks, chamfer returns, open tree pits/grates, curbs,
parking marks, cross-street connections and a service alley with loading aprons.

Presentation adds a different seeded opposite block face, continuing blocks
and corner buildings at the next crossing, houses and trees beyond the alleys,
street trees, lamps, parked pickup/crossover/hatchbacks and tenant belongings.
The library's original generators run only inside `downtown/build/context/`;
no other family's delivery is modified. The cars use their original procedural
paint/glazing and exterior construction, rather than a claimed rebake of their
final deliveries. Context mesh data is instanced. Close-ups retain the town in
glossy rays so the glass reflects a street rather than a bare sky.

The hero is a 1.60 m camera on the opposite sidewalk, 38 mm on a 36 mm sensor,
under a raking procedural sun. Dusk has warm selected rooms/shops and downward soft pools
from the actual street-lamp emitter sockets. Day shops retain their fixtures;
clearer panes show goods behind the street reflections. Day/dusk share the delivered interior
image and `LightUV`; presentation light objects are not exported.

## Rebuild and proof

Requires installed Blender 5.2, Python/Pillow/NumPy, open DejaVu fonts and flock.
No downloaded code, packages, models, textures or HDRIs are used. Every Cycles
bake/render holds the shared kit GPU lock and requests OptiX/CUDA. Make is
serial; all scratch data stays inside ignored build directories.

```sh
make -C downtown clean
make -C downtown                  # 4096 bakes, shipped maps, exports, checks and all evidence
make -C downtown check            # independent fresh-import and construction checks
make -C downtown repeat           # isolated field/bake/model rebuild; compare actual bytes
make -C downtown check-repo
```

The cold checkpoint and separate checks pass: 28 buildings, 107 doors across
10,807 sampled positions, 32 deliveries sharing eleven imported images, and
79 byte-identical files in the independent field/bake/export repeat.
The repository check reports 1598 source files and zero errors.

`build/check.json` separates raw serialization, fresh-import preservation,
physical ray measurements and motion. `build/plan-check.json` checks 4,000
plans, not 4,000 rendered buildings. `build/chart-check.json` measures actual
UV area/density and guarded-region containment. `build/texture-check.json`
checks image sizes, exact canonical bytes and normal lengths;
`build/resource-check.json` proves actual imported image reuse.
`build/render-check.json` checks exported bundle/image/context provenance,
all 26 Cycles views, active photographic pairs and hero camera/tonal range.
`build/repeat.json` records full isolated procedural-field/GPU-bake/export
repeatability. Blend container bytes are not deterministic delivery evidence.

Five fitted pairs include HABS form checks and separate Auburn/Louisiana
color checks. A focused storefront crop retains native exported pixels from
the same Foster fit. Stated neutral patches and channel gains accompany the fits.
They compare original buildings with different facades; camera residuals and
unknown photographic processing limit the claim. A fit proves framing, not
material correctness. `renders/values/` shows measured patches; display values
are exposure diagnostics, not inferred physical albedos.

Remaining limitations and the final full-size verdict are recorded in
[REVIEW.md](REVIEW.md). Simplified cast relief, repeated roof equipment and shallow room backings
still reveal the procedural construction. Eevee's approximate glass is less convincing than Cycles.
There are no collision or LOD meshes,
unique lightmap UVs, or complete interiors in this checkpoint.

## Credits and scope

[Reference credits](refs/SOURCES.md) identify the HABS/Library of Congress
photographers, NPS authors, historic catalogs and district nominations, plus
Michael Walter, Chris Light and Paul Sableman's color photographs. The new
sign-weather reference is Michael J. Auer's NPS Brief 25, including Thomas C.
Jester's photograph. References supply construction, dimensions and comparison;
no photographed pixels enter a material or committed image.

Installed DejaVu Serif/Sans use the open Bitstream Vera/DejaVu license. Tenant,
bank, hotel and foundry names are fictional. Town context uses this library's
original house, tree, street-light and parked-car generators for presentation.
Every delivered vertex and texture pixel is generated by the family scripts.
