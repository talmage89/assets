# Neighborhood elementary schools — form / construction checkpoint

Three original American public-school plans, built procedurally in Blender
5.2 and presented as maintained campuses in the 1995–2015 town. This delivery
stops before school look-dev, weathering, bakes and final documentation images.
The classroom additions and replaced sash already express different decades.

Review the exported Cycles [contact sheet](renders/checkpoint/contact.jpg),
the [three photographic pairs](renders/matches/contact.jpg),
[form critique](REVIEW.md), [dimension rationale](REFERENCE.md) and
[source register](refs/SOURCES.md). Review images are ignored rebuild outputs;
there is deliberately no committed final `docs/` gallery at this gate.

| Seed / fictional school | Original plan and growth | Classrooms | Building triangles | Whole site triangles |
| --- | --- | --- | ---: | ---: |
| 101 / Cedar Fork | 1956 single-loaded fingers off a spine; 1963 multipurpose/service block; 1984 cross wing | 12 | 67,816 | 281,151 |
| 102 / Briar Court | 1964 four-room courtyard pods with covered links and low gables; 1988 rear row | 11 | 72,504 | 286,861 |
| 103 / North Vale | 1976 compact media/common core and perimeter classrooms; 1991 rear addition | 12 | 55,792 | 265,468 |

Counts include all placed instances, door hardware, original lettering and
site context. Each building has six materials. Whole sites have 30 materials
and 358 / 370 / 356 placed draw primitives before engine instancing/batching.
The most detailed building is within the 60–150k allowance; the simpler compact
school uses fewer triangles rather than adding invisible detail to reach 60k.
Every site remains below 300k, with two complete mature trees and two cars.

## Dimensions and construction

The measured source-wall clear classroom is **30 × 32 ft / 9.144 × 9.7536 m**,
960 sq ft, with a 30 ft + 6 in structural pitch. Classroom ceilings are 10 ft
above the 6 in floor. Source horizontal planes distinguish the floor at
0.1524 m from the ceiling at 3.2004 m. Single-loaded corridors are 8 ft clear;
the main spine is 10 ft clear. The California classroom comparator, archived
1996 Idaho school rules and BIA 2007 handbook are detailed in REFERENCE.md.

| Seed | Masonry block envelope, m | Full building export bounds, m |
| --- | --- | --- |
| 101 | 83.500 × 60.367 | 86.935 × 61.350 × 8.389 |
| 102 | 70.000 × 67.363 | 71.435 × 68.346 × 8.177 |
| 103 | 74.363 × 57.726 | 75.933 × 58.616 × 8.328 |

Export bounds include projections, covered walks and boiler stacks. Earlier
classroom decks are at 3.81 m; additions at 4.12–4.27 m, the media core at
4.88 m, multipurpose roofs at 6.706–7.315 m. The slab, masonry, sash and roof
are separate construction layers. There are real openings with masonry
returns, 50 mm sash frames, mullions/transoms, steel lintels, projecting sills,
later infill panels, hollow-metal door frames, vision lights, pulls, kick
plates, interior panic bars and closers. Fine mortar and fabrication detail
belong in the next material/normal-map stage.

Flat roofs have gauged membranes/slabs, folded coping and drip legs, cap joints,
scuppers, downspouts, splash blocks and equipment on curbs. The gym's upper
wall remains closed above adjoining low roofs. The courtyard pods have
low-slope gables and deep eaves. Covered steel decks bear on 4 in columns;
the courtyard link's end bears on the later addition above its doorway.

## Generator and delivery

`src/plans.py` is a Blender-independent bounded grammar. `school(seed,
plan_type=None, bays=None)` selects `finger`, `courtyard` or `compact`, with
three/four-bay original wings, original/addition eras, sash replacement,
palette and an archetype-specific parcel arrangement. Arbitrary seeds also
vary bay count, chronology and colors within those bounds. The three review
seeds deliberately use three different circulation graphs and parcels.
They are not an unrestricted site-packing or architectural-program solver.

`src/buildings.py` builds the construction; `siteworks.py` builds the site;
`build.py` publishes standalone `School-<seed>.gltf` and assembled
`Campus-<seed>.gltf`, each with its own binary and shared external image URIs.
Their adjacent JSON files describe parameters, dimensions and budgets.
`build/family.json` collects all six packages.

Preserve the repository-relative image URIs when importing, or remap them to
one shared image cache. No images are embedded. School geometry plus glTF is
approximately 9.68 / 10.23 / 7.87 MiB; site geometry plus glTF is approximately
22.10 / 22.77 / 19.78 MiB, excluding shared images. Exact bytes are in
`build/check.json`. Scene-node instancing retains the library foliage/fences.

School origin is the center of its block envelope on the ground, +Z up and
front −Y. Export transforms are applied; glTF is +Y up, front +Z. Motion-axis
names below refer to Blender coordinates: the vertical Z hinge / halyard axis
becomes glTF Y. Exterior leaves retain named hinge empties
`School_<seed>__<block>_Door_<opening>_<leaf>`:
local Z, 0–90° outward, negative on the first/left leaf and positive on the
paired right leaf. Cylindrical hinge knuckles stay on the jamb axis.
Portable leaves use the same convention. No armature or baked animation.

Named entry, walk and footprint sockets accompany the building. Campus
sockets include Playground (the center of the equipment reservation), bus and
parent entries, service, blacktop, ballfield, portable lower approaches and flag
halyard. The flag pivots around Z (±60°) and can lower 6.2 m on its Z halyard
socket; its authored rest cloth has sag and folds. Dumpster gates use Z hinges
with ±110° ranges. These are integration frames, not animation clips.

## Site reuse and additions

Each authored lot is 210 × 184 m / 9.548 acres. The public street extends the
rendered bounds slightly beyond the lot. Separate bus/parent stadium loops
have 24 ft paving, measured curb/gutter sections, 5 ft outer walks, graded
verges and interrupted entries. Staff lots have 20 / 25 / 23 marked spaces,
including an 11 ft van bay and 5 ft access aisle. A separate service drive
reaches the kitchen, dock bumpers and dumpster enclosure.

Reused unchanged source families: Ground street sections and tiling maps;
chain-link fence fabric/parts; street-furniture bench and bike racks;
street-light fixture; boxwood geometry/analytic atlas; mature maple/oak GLBs
with alpha and Wind data; hatchback geometry. Read-only local adapters rebuild
context under `school/build/`. Parked cars omit brake/lug internals and use a
0.68 local body LOD with uniform form finishes. Canonical deliveries are never
edited. An existing-delivery hash snapshot is checked after construction.
The available car family describes late-2010s vehicles: these parked context
copies are later than the requested town period. They are explicit checkpoint
stand-ins; period-specific vehicle dressing is still needed for final scenes.

New school-specific construction: the two loop geometries, parking/markings,
entry plaza and connected exterior routes, loading signs, flagpole/halyard and
fictional district flag, service dock/enclosure, original basketball hoops and
game lines, practice ballfield/backstop arrangement, and one portable each on
101/102 with true openings and a supported ramp. Portable floor is 0.70 m;
its 6.5712 m run descends 0.5476 m at 1:12, with landings, rails and high-side
guard. A further 2.7432 m approach drops 0.1344 m to site grade. The 70 × 50 ft
fenced playground footprint reserves space and a socket
for `playground/`; no playground equipment is built here.

## Images and memory

School surfaces use six temporary semantic slots and one white 8² image with
vertex colors: negligible image memory, no new school texture set. Planned
look-dev starts with the houses' RanchBrick/HouseTrim, commercial CMU/roof and
apartments' mineral surfaces wherever they serve. This gate neither duplicates
those finished sets nor approves a new institutional set.

The actual shared site image allocation, estimated at 8 bpp with full mips:

| Reused set | Images | GPU MiB |
| --- | --- | ---: |
| Ground asphalt / concrete / lawn | three 2048² triples | 48 |
| Maple / oak | two 2048² triples | 32 |
| Chain-link | one 1024² triple | 4 |
| Original shrub analytic context atlas | one 1024² triple, shared under school textures/checkpoint | 4 |
| School form witness | one 8² image | <0.001 |

All three campuses together reference the same **22 unique images / 88.0001
MiB**, about 61.4 MiB of PNG files. This is the loaded site cost, not 88 MiB of
new school art. There are no school bakes at this checkpoint.

## Rebuild and evidence

```sh
make                    # refs, missing dependencies, six packages, checks, Cycles, pairs, contact sheets
make check              # physical source checks, raw external glTF, fresh imports, preservation
make repeat             # independent geometry/image re-export and byte comparison
make render             # 27 exported Cycles views, 1400 px / 32 samples
make matches            # three neutral-balanced, feature-calibrated export/photo pairs
make clean              # removes school build, export, textures and renders
```

Missing canonical inputs are built with their original family Make rules,
following the apartment dependency convention; existing inputs are reused.
All Cycles work uses the shared kit GPU lock. Modeling/checks use CPU.
No kit changes are required. Sources, measurements and photo extraction are
scripted; photographs are comparison inputs only.

Per seed, `renders/checkpoint/<seed>/` contains `hero`, `above`, `plan`, `rear`,
`windows`, `entry`, `gym`, `door`, `roof`, plus provenance with export hashes.
Heroes use eye height 1.68 m and a 40 mm lens with raking procedural sunlight.
`renders/matches/` contains Walls gym, McDowell ribbon and Emerald covered-walk
pairs. Fits are feature/type comparisons on original designs, not surveyed
replicas or recovered EXIF cameras. Neutral patches and residuals are in
`build/reference-balance.json` / `build/matched-cameras.json`.

Checks distinguish source construction from serialization: source-wall rays
measure every classroom; 21 poses per exterior leaf test actual casing and
neighbor surfaces; the kit's solid-parity penetration sweep also checks each
closed casing at 0.5 mm tolerance. Portable leaves are checked on campus. Fresh
imports independently compare counts, bounds and pivot/socket frames. Finite
UVs/unit normals and alpha/Wind preservation are checked. Intentional tiling
reuse and provisional collapsed UV charts are reported; final UV density,
normal-map fidelity, lightmap charts and bake acceptance remain future work.
The standalone staging charts have 2,004 / 2,846 / 1,986 zero-area UV triangles;
these are reported diagnostics rather than a finished unwrap acceptance.

The clean school rebuild regenerated all local context from original library
scripts. `make repeat` passes for 34 external geometry/image files. The one
oak tangent which straddles MikkTSpace's four-decimal rounding boundary retains
its read-only canonical value through the kit's guarded repair: exact
position/normal/UV signature and at most one 0.0001 tangent step. No geometry,
normal or UV quantization is used. All 772 pre-existing delivery files remain
byte-identical. Raw checks measure 35 classrooms and 882 exterior-leaf poses;
fresh-import bounds/pivot errors stay below 0.01 mm. Repository checks pass.
Actual trunk-base bounds clear the building footprints. Actual walk polygons
have zero overlap with portable wall footprints, practice-field envelopes,
court play areas or playground reservations beyond their permitted entry
aprons; those are construction checks separate
from the import comparison. A further 3,750 downward source-surface probes
cover the six drive/walk junctions and find no uncovered sample.

The weakest areas are still visible: uniform proxy masonry/roof surfaces,
regular window backings/blinds, schematic interiors and service systems,
sparse landscape dressing and no causal school aging. Full vehicle swept
paths, continuous collisions, structural design and complete occupancy/egress
compliance are not certified. This is the requested form checkpoint.
