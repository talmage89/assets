# Neighborhood strip centers — look checkpoint

Four original maintained small-shop centers, approximately 15–25 years in
service. This is the requested look checkpoint, not final portfolio delivery.
[Reference limits and originality](STRIP_REFERENCE.md), [maps](TEXTURES.md),
and four look critique passes in [REVIEW.md](REVIEW.md) accompany it.
Checkpoint renders remain ignored under `renders/strip/`; no unfinished docs
images are committed.

Main was merged in `40de911`, including the gas delivery and delivered hatch.
Gas source and committed delivery images, houses and Ground remain identical
to main. A receipt also verifies the 43 delivery/doc files present before
this work. No kit code changed.

## Plans, construction and form fixes

| Seed / center | Lot, ft | Building | Site and construction | Spaces |
| --- | --- | --- | --- | ---: |
| 201 / Alder Rill Shops | 336 × 244 | 240 × 70 ft; 16,800 sq ft | Centered deep lot, four rows, flat walk, split CMU, end towers; southwest pylon | 101 |
| 202 / Crossbend Court | 390 × 210 | 220 × 64 ft; 14,080 sq ft | Wide shallow lot, row pushed 24 ft east, three rows, mansard/brick, central tower; southeast pylon | 93 |
| 203 / Lowbank Commons | 348 × 260 | 242 × 76 ft; 18,392 sq ft | West-biased row, staggered islands, differing driveway stations, arcade/EIFS; west pylon | 105 |
| 204 / Willow Span Shops | 396 × 244 | L; 17,920 sq ft | Two-street corner, south entry/east exit, flat walk/smooth CMU, elbow tower; east pylon | 91 |

End caps select wrap glazing and a side tenant sign, or a signed solid side.
The L's short return also wraps; it no longer ends in a blank closure.
Wrapped frames occupy real wall openings and reveal the same tenant room.
Each service door has a 1.7 × 1.6 m concrete stoop and two 114.3 mm loading
bollards. These additions retain the accepted bay widths, building heights,
walk styles, rear services, tenants, pylon and moving parts.

The grammar is bounded parcel design, not arbitrary site planning.
`strip_plan.generate(seed, overrides)` resolves dimensions and circulation
before modeling. `STRIP_PLAN=build/my-plan.json` supplies overrides; unsupported
geometry is rejected. Other seeds vary the same tested archetypes.

Standard parking is **9 × 18 ft**, around **24 ft** double-loaded aisles.
**9 ft** islands break the rows. Six **11 ft** accessible spaces share three
exclusive **5 ft** aisles. The **6 ft / 1:12** recessed ramps retain a **4 ft**
level landing within the **10 ft** walk. Actual surface rays check columns,
ramps and native street interfaces. Entrances are **24 ft**, with native
five-foot transition wings and six-foot aprons on Ground's six-inch grid.
The corner's cross aisle continues to its east exit.

Floor is **.1524 m**, membrane datum **4.2672 m**, parapet **5.1816 m**,
tower top **6.72 m**. Storefront head/transom/sill are **2.75 / 2.20 / .27 m**.
Flat/arcade soffit is **3.3075 m**, mansard soffit **3.0925 m**.
Sizes are authored against the cited standards/comparators, not recovered
from surveyed properties. Parking ratios are **6.01 / 6.61 / 5.71 / 5.08**
per 1,000 sq ft; they exceed the cited 3/1,000 baseline but are not a local
approval or demand study. STRIP_REFERENCE states each authority's limits.

## Surfaces, signs and occupied rooms

Manufacture shares the gas station's exact CMU, brick, EIFS, concrete,
membrane and equipment maps. Ground asphalt/lawn and Boxwood remain unchanged;
the mansard uses the existing house shingles. New strip art is only one
**2048² RGBA color + 1024² RGB emission** sheet: **6⅔ MiB** compressed with
full mips. Original signs, notices, address numbers, wear charts, powered
fixtures, faded south-facing pylon alternatives and the removed tenant's
letter ghost share it. Furniture uses the equipment atlas, without a new
interior sheet. All alternatives total **81 MiB**, or **97 MiB** with existing
shingles; actual referenced memory is **79⅓ / 92⅓ / 76 / 79⅓ MiB** by seed.
These estimates are separate from file bytes.

The original trades remain Vellum Nails, Hemwick Dry Cleaners, Notch Oven
Pizza, Copperfold Laundry, Pintrace Phone Repair, Drowsefield Mattress,
Tallied Oak Tax, Snipwell Hair Studio and vacancy. UV0 selects ink/coverage;
UV1 selects radiance or zero. The exported material lights the signs,
pylon, canopy fixtures and interior fixtures in both Cycles and Eevee.
Presentation light sources support the exported fixture emission at dusk.

Rooms contain supported salon/manicure chairs and counters, a closed dry
cleaner's overhead conveyor with hanging garments and cantilever supports,
pizza counter/oven/tables, washers and folding tables, desks and mattress
displays. Vacancy retains a bare empty floor and no powered room lights.
These are shallow storefront fit-outs, not playable interiors. Actual source
floor probes measure **73 / 70 / 69 / 63** tagged support contacts, at most
**1 mm** above the finished floor.

Age follows causes: accumulated engine drips occupy stall centers; continuous
wheel paths follow the aisles and turns. Sealed cracks and a repaired utility
trench explain pavement repairs. Old/restriped paint keeps its own pigment.
Entry footfall, gum and grit stay on the walk and avoid sloped ramps. Coping
and canopy joints feed unequal gravity rivulets. Wet masonry retains salts
near grade/rain leaders; service-leaf and gate hems retain corrosion.
The vacant bay has the ghost of fictional removed letters. Deposits have zero
radiance and retain the underlying material's color; there is no uniform
whole-center aging wash.

## Geometry and material cost

| Seed | Building triangles | Bay range | Center without shrubs | Whole placed center | Unique mesh triangles | GLB bytes | States / primitives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 201 | 60,866 | 3,962–6,896 | 88,756 | 289,924 | 94,344 | 66,825,832 | 9 / 246 |
| 202 | 58,662 | 3,948–6,900 | 85,362 | 236,238 | 90,950 | 76,087,580 | 10 / 240 |
| 203 | 66,946 | 4,034–6,986 | 95,906 | 297,074 | 101,494 | 65,225,800 | 9 / 262 |
| 204 | 53,754 | 3,962–6,926 | 82,420 | 283,588 | 88,008 | 65,969,172 | 9 / 231 |

All remain below **80k building / 7k bay / 5k pylon**. The increase from the
accepted form buys the required stoops/bollards, wrapped ends, real interior
supports and vertex samples for material/age variation. Every pylon is 3,104
triangles. The 36 stock shrubs contribute 201,168 placed triangles but only
5,588 unique triangles; seed 202 has 27 shrubs / 150,876 placed triangles.
Presentation cars, streets, houses, trees and street lights do not ship.

The default's external glTF is **289,528 bytes**, its geometry bin
**12,357,964 bytes**, and referenced PNGs **54,175,963 bytes**. Canonical
external image URIs share maps across centers and existing families. The
self-contained GLB is a convenient rendering/inspection copy.

| Default part | Triangles | Materials and reason | Material primitives |
| --- | ---: | --- | ---: |
| Bays 01–10 | 5,164 / 5,842 / 5,710 / 5,202 / 3,962 / 5,214 / 5,102 / 5,146 / 6,796 / 6,896 | Six: masonry, concrete, equipment/trim/furniture, glass, membrane, ink/emission | 15 each, including independent rear/entry/service meshes |
| Left wrapped / right signed end | 954 / 554 | Five / four: wall, slab, trim, ink; wrapped end also glass | 5 / 4 |
| Two towers | 438 each | Four: wall, concrete, trim, ink | 4 each |
| Ladder | 760 | Equipment | 1 |
| Meter bank | 2,688 | Equipment, glass, ink | 3 |
| Paving/islands/paint | 20,150 | Asphalt, concrete, equipment bark/guards, lawn, ink/deposits | 5 |
| Six lot poles | 316 each | Concrete base, equipment pole, powered diffuser | 3 each |
| Operating dumpster yard | 1,440 | Masonry, concrete, equipment, corrosion ink | 9 including moving parts |
| Pylon | 3,104 | Masonry, concrete, equipment, ink/emission | 4 |
| Site wear/repairs | 1,300 | Asphalt repair, equipment sealant, alpha deposits | 3 |
| Landscape | 201,168 placed | One existing masked shrub material | 36 |

Nine material states are not nine draw calls. Modular roots and actual moving
leaves retain their necessary primitives. The mansard has a tenth state for
existing shingles alongside its flat membrane. This is the only exception.
Exact materials/triangles for every seed and part are in
`build/strip-look/delivery.json` and `delivery-check.json`.

## Frames and motion

Meters; Blender +Z up / frontage −Y; glTF maps `(x,y,z)` to `(x,z,−y)`.
`StripCenter_<seed>` is at the footprint center at grade. Bay modules retain
front-center and left/right repeat sockets. No armature or animation clips.

| Node | Pivot / local range |
| --- | --- |
| `Bay_<nn>_Entry` | Exterior hinge, Z −100…0° |
| `Bay_<nn>_ServiceDoor` | Rear-frame exterior hinge, Z −100…0° |
| `Strip_DumpsterGate_-1/1` | Z −110…0° / 0…110° |
| `Strip_DumpsterLid_-1/1` | Rear lid edge, X −105…0° |
| `Bay_<nn>__RepeatLeft/Right` | Structural-bay joint sockets |
| `Socket_{Drive,GroundCurb,GroundApron,GroundWalk}_1/2` | Private/native public-interface frames |

## Rebuild and checkpoint evidence

```sh
make -C commercial strip WIDTH=1600 SAMPLES=40
make -C commercial strip-check
make -C commercial strip-repeat
```

`strip` adds the look pipeline beside the unchanged gas default. Individual
steps are `strip-model`, `strip-export`, `strip-render`, `strip-match`,
`strip-eevee`, `strip-values`, `strip-fixes`, `strip-review` and
`strip-protected`. Use the same WIDTH/SAMPLES when rerunning render targets.
All Cycles invocations hold the shared GPU lock. Missing context builds
through the library's own scripts, without changing their source/deliveries.

| Path under commercial/ | Evidence |
| --- | --- |
| `build/strip-look/strip-<seed>.{blend,glb,json}` | Four generated sources, exported hierarchies, dimensions and exact counts |
| `export/CommercialStrip-<seed>.{gltf,bin,json}` | Shared-map stock glTF delivery |
| `renders/strip/checkpoint/hero.png` | Raking sun; inside lot, 1.6 m eye, 35 mm, parked delivered pickup/crossover/hatch in several colors |
| `renders/strip/checkpoint/seeds/<seed>/{above,street}.png` | Four parcels in native streets, sidewalks and library neighborhood |
| `renders/strip/checkpoint/{storefront,walk,tower,endcap,pylon,rear,services,stalls}.png` | Unoccluded construction/interior/sign/service/age detail |
| `renders/strip/checkpoint/{dusk,scale}.png` | Powered center; separate 1.8 m silhouette |
| `renders/strip/eevee/hero.png` | Exported materials with Eevee irradiance cache |
| `renders/strip/matches/*-pair.jpg` | Six balanced-photo/procedural-light comparisons: Commerce, Sterling, Westlakes walk/lot; older California and date-unverified rear auxiliaries |
| `renders/strip/form-fixes/*-before-after.jpg` | Four parcel comparisons, end-cap crop, rear landing crop; original quick finishes on both sides |
| `renders/strip/checkpoint/{family,details,contact}.jpg` | Complete review sheets including pairs and form fixes |
| `renders/strip/measurements/` | Fixed annotated coverage/contrast patches and neutral balances |
| `build/strip-look/{checks,delivery-check,value-surface-check,view-check}.json` | Source construction/motion, raw maps/UVs/normals, actual measurement-surface rays, current image/export/context hashes |

The plan proof covers 1,000 seeds, rejects seven invalid controls, and tests
all four occupied-lot routes and representative park/back-out maneuvers.
Construction checks measure surfaces and clearances; fresh-import checks
separately prove serialization. Shared tiling/chart overlaps are intentional;
raw glTF checks reject degenerate UV triangles and nonunit normals and verify
image bytes against the generated/library maps. The independent default
factory-startup build is byte-identical at **66,825,832 bytes**.

## Photographic judgment and remaining limitations

Four look critique passes start with color/value. All main, family, dusk,
Eevee, comparison and form-fix renders are inspected at native size.
Procedural sun/sky follows estimated photo shadows; the overcast rear uses
neutral sky. Photo neutrals and uncertainties are recorded in the generated
balance receipt. They are assumed neutral surfaces, not measured albedos.
Sparse camera fits have roughly .3–10.4 native-pixel residuals; their precision
does not establish unsurveyed dimensions or identical construction.

| Fixed patch | Median Y′, render / photo | 4%-threshold coverage, render / photo | Median contrast, render / photo |
| --- | --- | --- | --- |
| Sunlit repaired asphalt | .657 / .675 | 24.9% / 46.0% | 5.1% / 7.3% |
| Shaded walk | .219 / .232 | 46.9% / 58.3% | 9.6% / 6.2% |

Coverage is projected visible variation relative to each patch's p85, not
chemical oil segmentation or surveyed stain area. Aggregate, repairs, unknown
camera response and residual shadows affect it. Both 4% and 8% thresholds
and masks are retained; nine actual exported-surface rays per rectangle
exclude glass, walls, columns, curbs and wrong floor levels. The native photo
walk patch is only about 20×4 pixels. Asphalt value is close, but its variation
is weaker than the used photograph; the walk's remaining deposits are more
contrasty. These are measured misses, not a claimed appearance pass.

The center still reads CG through regular bay repetition, restrained broad
weathering, simple low-detail rooms and very tidy service construction.
Close tower ink is improved by reallocating pixels within the same sheet;
small notices and distant pylon lettering still soften. Door-bottom rust
remains a simplified alpha treatment. The neighborhood uses delivered library
forms and sparse traffic rather than a fully dressed commercial district.
These limitations remain visible at this checkpoint; no final portfolio/docs
claim is made.
