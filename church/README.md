# Town churches — form and construction checkpoint

Two fictional American congregations in a 2010 town: a 1908 brick Gothic
church one block from Main Street, and a 1963 glulam A-frame church on a
residential arterial. Both are assembled from original scripted modules and
exported as glTF with shared external images. This delivery stops at the
requested construction checkpoint. The photographic finish is not approved.

Seed 101 has a six-bay nave, corner bell tower and spire, rose, deep paired
portal, later brick hall and a 1996 side ramp. Its rear lot is full for Sunday
morning, with four more cars on the streets. Seed 202 has seven A bents,
low masonry walls, glazed ends, steel campanile, fellowship/education wings,
garden, covered drop-off and a lightly occupied weekday lot. Their plans,
circulation and neighbors differ. There is no playable interior.
The three annex-side lancets retain their arch heads above lower infill,
so the later hall roof clears actual glazing instead of cutting through it.

## Dimensions and evidence

The designs are originals, not reconstructions. [REFERENCE.md](REFERENCE.md)
distinguishes authored dimensions from evidence. [SOURCES.md](refs/SOURCES.md)
records every downloaded reference, author, rights and use.

- HABS IL-1223 sheets 3/5/9/11/14 establish measured plan/section discipline,
  wall gauge, recessed portals and window construction. The entry detail's
  graphic scale puts its door height at approximately 2.0–2.1m; our replacement
  leaves are 2.134m high with a wider paired opening. Neither the HABS church's
  complete plan nor its identity is copied.
- The Roanoke First Baptist National Register nomination describes an
  1898–1900 six-bay brick church with slate, tower and later hall. PHMC's
  Gothic and Romanesque guides distinguish lancets/buttresses from round
  arches and heavy masonry.
- The 1961 Chapel for the Children nomination documents 9ft brick sidewalls,
  glulam, glazed roof ends, flat wings and a garden. Connecticut's Shepherd
  of the Sea nomination supplies the principal A-frame/arrival-drive photo.
  DAHP supplies the postwar type guide. The abandoned 2024 photograph is
  used for form, not the maintained age target.
- HABS MD-1298-1 and TN-145-5 supply street and window comparisons. A credited
  Wikimedia 2009 church photograph supplies period glazing/roof/planting
  condition. No photograph is projected, traced or used in a texture.

| Dimension | Historic 101 | Mid-century 202 |
| --- | ---: | ---: |
| Nave outside width × length | 13.106 × 25.603m | 17.678 × 29.870m |
| Clear-width design target | 12.192m / 40ft | 17.069m / 56ft |
| Bay count / pitch | 6 / 4.2672m | 7 / 4.2672m |
| Masonry gauge | .4572m | .3048m |
| Sidewall / pitch | 8.2296m / 48° | 2.7432m / 57° |
| Nave ridge | 15.508m | 16.354m |
| Tower cross top | 28.95m | 15.10m |
| Entrance level | .6096m | .1524m |
| Stair rise / tread | .1524 / .3302m | one entrance level change |
| Fitted door leaf width × height | .984 × 2.1336m | .984 × 2.1336m |
| Side lancet width / stem / crown | 1.40 / 3.10 / 1.212m | panelized gable |
| Glulam section | — | .620 × .240m |
| Ramp rise / run | .6096 / 7.9248m | curb ramp .1474 / 2m |
| Stall width × depth | 2.7432 × 5.4864m | same |

The historic ramp's fresh imported surfaces measure .609600m rise, 1:13.0000
grade and 1.552000m between grasp-height rail vertices. Landings are authored
at 1.8288m length; this is not a measured compliance certificate. ADA 1991
guides the fictional 1996 retrofit. IBC assembly provisions motivate outward
doors, panic hardware and separated exits; no interior egress calculation is
claimed. A filled ramp base reaches below grade rather than spanning in air.

## Generator

`src/plan.py:church()` is the pure grammar; `src/build.py` constructs and
packages it in Blender. Seeded plans and placement offsets are written to
`build/plan-101.json` and `build/plan-202.json`.

| Parameter | Values |
| --- | --- |
| `seed` | integer, deterministic occupancy, placement and variation |
| `style` | `gothic`, `romanesque`, `aframe`, `chapel` |
| `bays` | 3–18 at 4.2672m pitch |
| `width` | 5–42m outside masonry |
| `pitch` | 25–65 degrees |
| `tower` | `corner`, `center`, `freestanding`, `none` |
| `top` | `spire`, `belfry`, `cross` |
| `wings` | comma-separated `hall`, `education`, `transepts`; empty for none |

The range export places a white frame chapel, a smaller Romanesque church,
the Gothic church and the A-frame beside one another. The white chapel uses
the native house siding. Wider/longer naves are supported by the grammar;
arbitrary parameter combinations have not received the two sites' complete
circulation review. Town parcel layouts are authored for seeds 101 and 202.
An additional standalone smoke build used 12 bays, 24.384m width, 50° roof,
center-front crenellated tower and hall/education wings: 99,814 triangles.
Its raw geometry/normals/resources pass; it has not received a site or
photo review. Its receipt is `build/grammar-smoke/check.json`.

For a custom standalone church, start in this directory and use a separate
directory under `build/`:

```sh
church_root="$(pwd)"
mkdir -p build/custom
cd build/custom
python3 "$church_root/src/textures.py"
blender -b -t 4 --factory-startup --python-exit-code 1 \
  --python "$church_root/src/build.py" -- --seeds 909 --style gothic \
  --bays 12 --width 24.384 --pitch 50 --tower center --top belfry \
  --wings hall,education --no-sites --no-modules --out build/variant.blend
```

## Packages and interaction

`export/Church-{101,202}.gltf` contains each building. The corresponding
`ChurchSite-*.gltf` adds roads, sidewalks, lots, signs, town hosts, cars and
plants. `export/modules/*.gltf` contains the reusable pieces; `Range.gltf`
shows the grammar. Their `.bin` files contain geometry only. Images use
relative shared URIs within the library; move the resource dependencies
with the packages. `build/glb/` contains embedded inspection copies.

Origins are centered on each complete building's horizontal footprint at
grade; the nave offset is recorded in node extras. Blender is meters, +Z up,
front −Y. glTF is +Y up, front +Z. Moving parts retain their local pivots:

- Door leaves: local Z, left −90..0°, right 0..90°, opening outward. Named
  `Door_Left`/`Door_Right` beneath each entrance frame.
- Bell/yoke/wheel: local X, ±30°, at the axle, independently of the tower.
- Each sign character: `socket_kind=sign_letter`, with row, column and glyph.
  `build/letters.json` gives atlas rectangles for A–Z, 0–9, `&-:.`.
- Stall empties: `socket_kind=parked_car`, center, width/depth, occupied and
  accessible flags. 101 has 17 stalls/17 cars plus four street cars; 202 has
  31 stalls/seven cars. Native car colors vary without new texture sets.
- Walk empties contain ordered `points`; the drop-off empty contains driving
  points, `interpolation=CATMULL_ROM` and 7m lane width. Extras point arrays
  remain in authored Blender axes; convert them when using a glTF engine.
  Axis labels in extras also use Blender axes: Z becomes glTF Y; X stays X.

`Church_stained` retains the authored emissive color map with strength zero
by day; the dusk preview sets strength 4.5. A game can drive that material's
emissive intensity. The protective storm sheet is separate and non-emissive.

## Geometry and resources

All counts are expanded instance triangles unless explicitly described as
unique. A site budget includes its church, paving, signs, street equipment
and reduced town buildings; cars and vegetation are reported separately.
`build/check.json` is the independent raw-glTF ledger; `build/metrics.json`
is the source/export ledger.

| Expanded triangles | Downtown 101 | Mid-century 202 |
| --- | ---: | ---: |
| Complete church | 62,694 | 24,324 |
| Paving, roads and site equipment | 109,210 | 112,062 |
| Context buildings | 69,767 | 64,666 |
| **Budgeted site, excluding cars/plants** | **241,671** | **201,052** |
| Native cars | 1,292,361 (21) | 434,193 (7) |
| Native trees/shrubs | 184,108 (6 + 7) | 260,864 (8 + 12) |
| Entire expanded inspection scene | 1,718,140 | 896,109 |

Both static parcels meet 250k, the historic church meets 40–120k and its
tower meets 15k. Car/tree instances retain shared mesh data; their expanded
totals are not charged to the site ceiling. The A-frame's low triangle count
is intentional and is called out below.

| Resource receipt | Downtown 101 | Mid-century 202 |
| --- | ---: | ---: |
| Whole building envelope, including below-grade base | 28.323 × 33.132 × 29.110m | 51.759 × 47.444 × 16.559m |
| Building glTF + geometry BIN | 7,971,659 bytes | 3,192,523 bytes |
| Embedded building inspection GLB | 50,650,448 bytes | 48,704,496 bytes |
| Site glTF + geometry BIN | 34,874,590 bytes | 29,678,770 bytes |
| Referenced site image PNG bytes, once each | 113,808,818 | 113,374,174 |
| Referenced site map allocation, including actors | 246.833MiB | 240.167MiB |
| Site material definitions / mesh primitives | 79 / 619 | 72 / 500 |

| Independently exported piece | Triangles |
| --- | ---: |
| Belfry bay | 572 |
| Bell including shell, yoke, axle, wheel | 2,552 |
| Memorial bench | 60 |
| Laminated A bent with concrete shoes | 48 |
| Steel bent shoe/bolts | 456 |
| Stepped buttress | 144 |
| Drop-off canopy | 156 |
| Classroom bay | 226 |
| Operating door pair/frame/hinges | 1,560 |
| Drainage | 648 |
| Education wing assembly | 5,012 |
| Accessible exit bay assembly | 1,872 |
| Bike rack/cornerstone | 360 |
| Rose gable assembly | 4,184 |
| Glazed A gable assembly | 2,132 |
| Connecting hyphen | 124 |
| Low sidewall | 568 |
| Parish hall assembly | 4,024 |
| Recessed portal | 1,268 |
| Rail run | 1,052 |
| Filled ramp and two rail runs | 2,176 |
| Rear exit landing, treads and rails | 748 |
| Roof assembly example | 540 |
| Rose | 1,342 |
| Rear services | 856 |
| Changeable sign with glyphs | 162 |
| Entry landing/steps | 60 |
| Historic tower including bell/top | 12,456 |
| Pierced wall bay including window | 1,894 |
| Storm-covered lancet | 813 |

Assembly rows include their children; do not add the rows together. Individual
wall/window/buttress/roof/rail pieces meet the modular ceiling. Whole wings,
gables and the ramp contain several pieces. The bell fits the small-prop
3k ceiling. Simple silhouettes are deliberately below indicative lower
triangle targets. The A-frame church is below the requested 40k lower band:
its repeated structural sections and mapped lead do not warrant padding.

| Shared set | Shipped allocation | Estimated compressed GPU memory |
| --- | --- | ---: |
| DowntownMasonry | 2048² BC/Normal/ORM | 16MiB |
| DowntownFinish | 2048² BC/Normal/ORM | 16MiB |
| DowntownMineralRoof (mineral trim chart) | 1024² BC/Normal/ORM | 4MiB |
| RanchRoof | 1024² BC/Normal/ORM | 4MiB |
| HouseSiding (chapel range) | existing 1024² triple | 4MiB |
| Ground Concrete / Asphalt / Lawn | existing 2048² triples | 16MiB each |
| GroundTrim | existing 2048² triple | 16MiB |
| **New ChurchCraft** | **1024² BC/Normal/ORM** | **4MiB** |
| **New ChurchGlass** | **1024² BC/Normal/ORM** | **4MiB** |
| **New ChurchLetters** | **1024×512 RGBA** | **.667MiB** |

The new allocation is **8.667MiB shared across the family**: a timber/slate/
bell-bronze strip set because those materials were absent from the reused
architectural atlases; art glass because the library lacked it; a replaceable
letter atlas because a game must spell new messages. Their texels are analytic
Python/NumPy/Pillow output. Existing sets retain their original baked images.
BC is sRGB, normals are OpenGL +Y, ORM is occlusion/roughness/metallic.
Memory estimates assume 8bpp block compression with full mip chains; PNG disk
size is not GPU allocation. Maps are deduplicated by content across packages.

The standalone buildings reference 76.667/80.667MiB of existing plus new maps;
they share most of it with the town. Body materials number 12, including solid
glass and shadow proxies. Fine grain/lead lives in maps, with causal vertex
tint at wall bases, repaired patches and runoff. UV charts intentionally
tile/reuse; this is not a unique lightmap unwrap or a no-overlap claim.
The module hierarchy is retained for this checkpoint: 303/232 source glTF
primitives before static batching. Those are mesh-definition counts;
expanded site draw calls can be higher. Draw-call reduction remains later work.

## Rebuild and checks

From this directory, with Blender 5.2, Python/NumPy/Pillow and Poppler already
installed:

```sh
make                 # references, model, checks, export renders, comparisons
make check           # raw geometry/resources/repository + fresh Blender import
make repeat          # independent deterministic own-geometry/map payloads
```

Build native library dependencies first if absent: Ground, trees, shrubs,
the two house seeds, three cars, street lights and street signs. The dependency
script reports missing files. It copies the cached Downtown host or builds a
private copy under this family's `build/`, never in an existing delivery.
No kit change is required. A cold reconstruction removed this family's own
`build/`, `export/`, `textures/` and `renders/` before rebuilding; reference
downloads and the independent pre-build library hash receipt were preserved.

`make check` verifies static/tower/church ceilings, finite geometry, unit
normals, nonzero church triangle areas, UV presence/density, external image
paths, fresh-import triangle/bounds agreement and centered origins. It measures
ramp grade/rail clearance, cross seating, canopy post seating/clearance, curb
ramp grade, annex-to-glass clearance and the parcel-side depressed driveway
curb. It checks geometric outward winding on imported gable/roof faces;
unit normals alone did not catch the earlier Eevee culling failure.
Door/bell sweeps use
15° samples, 1mm tolerance and no contact exceptions. Walk centerlines are
tested at +1.1/+1.7m against church construction. These prove sampled surfaces
and serialization, not structural/code certification or complete navigation
volumes. The current independent receipt also confirms 373 pre-existing
delivery/map files remain byte-identical.
The repeat check reproduced 39 building/range/construction-module BIN and
new PNG payloads exactly, totaling 37,368,671 bytes. It excludes the two sites
and site-only sign geometry; native inputs are covered by the immutable
library receipt rather than regenerated by that check.

## Inspection images

These are rebuildable local checkpoint outputs, deliberately ignored by git.
There are no final `docs/` images at this gate.

- [All site views/contact](renders/checkpoint/contact.jpg): both eye-height
  across-street heroes, oblique parcels, doors/steps, day/dusk glass, towers
  from below, education wings/lots, street signs and 1.8m human/car scale.
- [Historic hero](renders/checkpoint/101/hero.png) and
  [mid-century hero](renders/checkpoint/202/hero.png): exported external-image
  glTF, Cycles, 35/38mm, camera height 1.72m, clear procedural sky, low sun
  raking the fronts. No HDRI. The rear-wing inspection uses light from its
  viewed side and records that direction in its receipt.
- [Modules/contact](renders/modules/contact.jpg),
  [four-church range](renders/checkpoint/range.png), and
  [Eevee hero](renders/eevee/101/hero.png).
- [Photo pairs/contact](renders/matches/contact.jpg): three distinct HABS/
  nomination photographs. [Source comparisons](renders/source-matches/contact.jpg)
  use the saved construction scene with the same maps; the principal pairs
  use the actual exported packages. The third pair explicitly isolates the
  exported WallBay to avoid a neighboring buttress hiding the window.

Photo-fit RMS is 30.6px/705px for the historic street, 24.3px/878px for the
A-frame, and 9.4px/170px for the window. The modern/window lens bounds are
active; these are framing comparisons between different original buildings,
not replicas. Independent Blender projection agrees with the calibrator
within .05 source pixel. The modern reference is balanced on its unmarked
gray arrival drive; HABS monochrome does not supply a hue target. Full
critiques, corrections and remaining differences are in [REVIEW.md](REVIEW.md).

The current weak points are clean, even trim and concrete, regular art-glass
patterning, synthetic bell patina, planar parcel lawns, coarse reduced
neighboring roofs and too many unbatched static primitives. Storm glazing has frame depth/stand-off,
vents and separate glass, but its yellowing/haze needs a causal wear pass.
The breathing slots need detailed verification, and Eevee screen reflections
still differ from Cycles despite the native raytrace/slab setup.
Patina, roof repairs/lichen, repointing/efflorescence, runoff, railing rust,
bird deposits, fascia deterioration and site-specific age still need a
later look-dev brief. The current vertex tint and inherited paving
wear are not acceptance of that brief's final aging. No final high-detail
bake, shipping optimization or photographic-finish approval is claimed.

## Credits

All new geometry and texels are original deterministic scripts. Shared
library geometry/maps remain the owner's original work. Reference rights
and source links are in [SOURCES.md](refs/SOURCES.md). Sign/date glyphs use
the installed open-license DejaVu Sans Bold through `kit/fonts.py`.
Names, dates, inscriptions and signs are fictional; only plain crosses are
used. Lighting is procedural. No existing model, scan, texture, HDRI or asset
pack was downloaded or adapted.
