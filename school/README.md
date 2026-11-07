# Neighborhood elementary schools — look-dev checkpoint

Three original public-school campuses, generated entirely by Blender 5.2
scripts for a 1995–2015 American town. Their accepted classroom grammar and
construction are retained; this checkpoint revises the parcels, circulation,
glazing, roofs and grounds, and binds finished shared PBR maps. Work stops
before a documentation gallery. There are no `docs/` images.

Review [the exported views](renders/lookdev/contact.jpg),
[the three photographic pairs](renders/look-matches/contact.jpg),
[the unchanged-camera comparisons](renders/before-after/contact.jpg),
[the full checkpoint report](LOOKDEV.md), [the critique](REVIEW.md), [reference rationale](REFERENCE.md) and
[source register](refs/SOURCES.md). Images are ignored rebuild outputs.

| Seed / fictional school | Plan and decades | Parcel / entry | Building triangles | Static campus triangles |
| --- | --- | --- | ---: | ---: |
| 101 / Cedar Fork | 1956 fingers; 1963 gym/service block; 1984 cross wing | Mid-block / south | 70,055 | 275,916 |
| 102 / Briar Court | 1964 four-room courtyard pods; 1988 rear row | Corner, two frontages / east | 70,585 | 281,641 |
| 103 / North Vale | 1976 compact media core; 1991 addition | Backing onto a park / north | 57,452 | 258,005 |

Counts include placed instances in the respective exports. Each building has
six materials; each static campus has 22. Native cars, neighboring houses,
continuing streets, utility poles and distant trees are presentation instances
outside the campus package and its budget. Cars retain their native source
geometry and materials. Their period is left to the lead. They are separate
scene actors even where parked inside the school parcel.

## Dimensions and construction

All 35 classrooms retain **30 × 32 ft / 9.144 × 9.7536 m** clear wall dimensions,
960 sq ft, and 10 ft ceilings. Structural pitch is 30 ft + 6 in; the floor
surface is 0.1524 m, ceiling 3.2004 m, single-loaded corridors 8 ft clear and
spines 10 ft clear. Source-wall rays measure the room size independently of
export comparison. References and the limits of those measurements are in
REFERENCE.md.

| Seed | Building export bounds, m | Classrooms |
| --- | --- | ---: |
| 101 | 86.935 × 61.350 × 8.228 | 12 |
| 102 | 87.530 × 68.346 × 8.177 | 11 |
| 103 | 75.933 × 58.616 × 8.328 | 12 |

Bounds include roof projections, covered walks and boiler stacks. Earlier
classroom decks are at 3.81 m; later wings 4.12–4.27 m, the media core 4.88 m
and gyms 6.706–7.315 m. The court school's gym/kitchen/office group is recomposed
on the other side of its pods without changing the accepted room graph.

Early wings have broad steel-sash walls, hopper bays, low spandrels and deep
sunshades; finger corridors have clerestories. The courtyard originals begin
at a low sill, while replaced upper panels and smaller inserted sash remain
visible. The compact school's original windows are narrow; its later addition
has a wider yard-facing bay. Openings have returns, lintels, projecting sills,
frames and actual separate glass, not a texture painted over a solid wall.

Roofs vary between longitudinal low-slope gables, shallow sheds, flat ballast
and framed clerestory monitors. Equipment count and size follow the wing's
age and use. Curbs have sloping bottoms measured against the actual pitched
roof surfaces. Coping, scuppers, downspouts and splash blocks remain modeled.
Drains stand on clear masonry piers, away from operating door leaves.

## Parcels and grounds

Each parcel is 210 × 184 m / 9.548 acres. Open one-way bus lanes run along a
straight loading curb joined directly to the entry plaza; parent traffic uses
another curb and the staff-lot approach. Aprons meet the library's crowned
streets through lowered curb openings. The curb is 6 in, loading pavement
24 ft, and general walks 5 ft. The entry plaza grades down from the curb to
the building floor. Bus loading and waiting places are sockets; no bus mesh
is invented.

The period LAUSD plans/aerials and CDE elementary-site diagram inform the
relationship of wings, yard, play area and field; these are original sites,
not replicas. The corner school has two frontage connections; the mid-block
school returns both routes to one street; the compact school backs onto a
wooded park. REFERENCE.md identifies the actual inspected figures and each
inference. McDowell's written nomination supplements the frontage/tree
reference; its absent scanned site diagram is not claimed as evidence.

The large asphalt yards meet classroom wings and carry basketball, four-square,
hopscotch, an illustrative hand-authored state map and a perimeter running
track. Hoops and tetherball poles stand at their edges. A 70 × 50 ft fenced
playground reservation and socket sit beside each yard; the practice field
and backstop lie beyond. Five mature native trees, four foundation shrubs,
a monument or marquee, racks, bench, lights and yard fences dress each parcel.
Portables on 101/102 retain their landings, rails and supported ramps.

## Shared maps, UVs and age

There is **no new school texture set**. The original library scripts supply
baked BaseColor, OpenGL Normal and ORM maps. Existing files remain unchanged.
Missing buff/tan brick maps are baked from the unchanged houses recipe at
4096 and shipped at its native 512; shared commercial maps are built by that
family's own rules. Meter-scaled tile UVs intentionally repeat; equipment
uses guarded trim cells. No unique bake or lightmap UV packing is claimed.

| Building surface | Shared set | Shipped size | GPU MiB, three maps |
| --- | --- | --- | ---: |
| Brick | CommercialBrick (101), RanchBrick buff/tan (102/103) | 512 | 1 |
| Painted block | CommercialCMU | 1024 | 4 |
| Sills / concrete | CommercialConcrete | 1024 | 4 |
| Painted trim / metal | CommercialEquipment | 2048 | 16 |
| Granular roof cover | CommercialConcrete, rescaled mineral grain | 1024 | 0 additional |
| Glass | Stock transmissive PBR | No images | 0 |

Each building references 12 images / **25 MiB**; sills and roofs share the
same mineral maps at different physical scales. A static campus references
33 shared images / **113 MiB**, including ground, two tree atlases, fence and
the existing shrub atlas. All six exports together reference **37 unique
images / 114.33 MiB**, 74,509,897 bytes of PNGs. Memory assumes 8 bpp block
compression with full mip chains, not uncompressed Blender residency. Buff/tan
normal and ORM maps deduplicate against their canonical matching images.

Brick density is about 420 px/m, concrete 672 px/m and painted block 420 px/m.
Trim density varies with the guarded uniform swatches; exact area-weighted
percentiles and all intentional tile reuse are in `build/delivery-audit.json`.
Every standalone building has zero collapsed UV triangles. Fine manufacture
comes from shared baked maps; school-specific splash, runoff and column-base
oxidation use placement-owned corner color. Small earlier-coat chips and
patched mortar strips are attached geometry. Drain masks follow the actual
scupper station; soil shortcuts, asphalt trench repairs and faded game lines
follow use rather than a uniform dirt overlay.

## Generator, pivots and delivery

`src/plans.py` retains the bounded, Blender-independent room grammar.
`school(seed, plan_type=None, bays=None)` selects a finger, courtyard or compact
plan, bay count, construction decades, replacements and district colors.
`siteplan.py` selects its parcel relationships and heading; `buildings.py`
constructs the walls/roofs and `siteworks.py` the grounds. This is a bounded
archetype generator, not an unrestricted architectural-program solver.

`export/School-<seed>.gltf` is the standalone building; `Campus-<seed>.gltf`
adds the static parcel. Each has a binary, metadata JSON and repository-relative
shared image URIs. Preserve those URIs or remap to a shared image cache.
Geometry plus glTF is 9,667,423 / 9,800,951 / 7,891,876 bytes per building and
21,176,867 / 21,741,690 / 18,650,644 bytes per campus, excluding shared images.
No images are embedded. Native foliage retains alpha and `_WIND` data.

Building origin is the center of its block envelope on the ground. Construction
uses Blender +Z up, front −Y. Campus yaw turns the entry toward its selected
frontage; glTF converts to +Y up. Exterior leaves retain hinge empties named
`School_<seed>__<block>_Door_<opening>_<leaf>` with Blender local Z ranges
−90–0° for the left leaf and 0–90° for its paired right leaf. Portable leaves
follow the same convention. Dumpster gates have ±110° hinges. Flag rotation
is ±60° on Z and the halyard lowers 6.2 m. No armature or animation clip.
Named entry, footprint, walk, loading, service, blacktop, playground, ballfield
and portable-approach sockets remain available.

## Rebuild and checks

```sh
make                 # references, dependencies, six exports, checks, Cycles, pairs and sheets
make check           # construction, UVs, raw glTF, fresh import, preservation and repository rules
make repeat          # independent export rebuild and byte comparison
make render          # exported Cycles views at 1400 px / 32 samples
make matches         # three neutral-balanced calibrated photographic pairs
make clean           # removes school build/export/textures/renders
```

All Blender jobs are serial. Cycles uses the shared kit GPU lock. Context is
rebuilt locally from native scripts; it never modifies canonical deliveries.
No kit changes are required. `renders/lookdev/<seed>/` holds hero, above, plan,
rear, window wall, entry, gym, door, roof, scale, blacktop and four original-camera
views. `renders/look-matches/` holds Walls gym, McDowell ribbon and Emerald
covered-walk pairs. Two photographs show schools in daily use. Fits compare
measured features of original designs; they are not replicas or recovered
EXIF cameras. Balance patches and fit residuals are recorded in `build/`.

Physical checks measure source room walls, sweep leaves against their casings
and neighbors, measure leaf clearance above completed campus surfaces, seat
equipment curbs on roof faces, intersect drive paving and program reservations,
and sample actual entrance surfaces. Fresh-import counts, bounds and pivots
prove serialization separately. Raw UV/normal/geometry checks, shared-image
allocation, 300 grammar seeds and preservation of all 772 prior delivery files outside this family
are independent receipts. None certifies complete interiors, vehicle swept
paths, continuous collision, engineering or occupancy/egress compliance.

The remaining visual weaknesses and the latest acceptance status are recorded
in REVIEW.md. This checkpoint stops before final documentation photographs.
