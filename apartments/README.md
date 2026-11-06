# Rill Court / garden apartments and townhouse rows

Original American rental housing for a town set around 2005, with the 2002
garage row shown around 2015. **Form and construction checkpoint; look-dev is
not started.** `make` builds four apartment complexes, their four standalone
buildings, and four townhouse rows with quick materials and external-image glTF.

Local images are generated into `renders/`; no checkpoint images are committed
as final `docs/` photographs. Open `renders/review/heroes.jpg`,
`renders/review/complex-family.jpg`, `renders/review/row-family.jpg`,
`renders/review/construction-details.jpg`, `renders/review/photo-pairs.jpg`,
`renders/review/unit-plans.jpg` and `renders/review/contact-sheet.jpg` after building.

## Buildings and generation

| Seed | Original plan / construction | Units |
| --- | --- | ---: |
| 301 | 12 | 71,957 | 1,114,215 | 9.97 / 37.46 |
| 302 | 16 | 111,608 | 1,109,190 | 15.53 / 41.56 |
| 303 | 24 | 141,138 | 1,157,365 | 19.47 / 48.10 |
| 304 | 8 | 55,134 | 1,061,128 | 7.69 / 30.94 |
| 401 | 6 | 44,246 | 163,732 | 8.85 |
| 402 | 6 | 44,502 | 163,988 | 8.91 |
| 403 | 6 | 51,462 | 247,472 | 13.07 |
| 404 | 4 | 29,386 | 125,024 | 6.84 |

`src/plans.py` supplies `garden(seed, **overrides)`, `row(seed, **overrides)`
and `complex_plan(seed)`, without Blender. Profile selection is deterministic;
other seeds vary bounded unit widths or row counts, replacement windows/doors,
curtains, blinds and occupancy. Controls include era, floors, access, skin,
roof, straight/L/offset shape, unit width/depth and palette for apartments;
count, width/depth, roof, garage and fire-wall option for rows. Unsupported
counts and unknown controls fail. This is a bounded grammar, not an arbitrary
parcel solver or a complete interior-plan generator.

Every garden wing has four units per floor: two front/two rear off a common
stair hall, or four along a gallery. Actual circulation slabs leave the
stairwell open and provide landings and a side bypass. Schematic room
reservations distinguish compact two-bedroom core units from one-bedroom
gallery units. Window backings provide cheap interior depth; furnished,
walkable interiors are outside this checkpoint.

The L and offset forms are separate framed fire compartments connected by
supported low open links. Their independent roof envelopes clear one another. Ten-foot wall gaps leave
measured conservative service-passage bounds of 1.295 m (L) and 1.564 m
(offset) after adjacent balcony/HVAC projections and the meter banks.
Townhouse fronts step in depth and finished-floor level; foundation fill,
stoops and sloping garage approaches reach those levels. Front gables use the
houses' analytic roof-plane clipping to meet the main roof.

## Dimensions, parts and sockets

[REFERENCE.md](REFERENCE.md) separates published dimensions from authored choices;
[refs/SOURCES.md](refs/SOURCES.md) records image/PDF authors, rights and uses.
The 1977 NBS study's 20 × 32 ft townhouse anchors the compact row. DAHP's
c.1970–1978 photographs and Sacramento's 1960/1962 apartment survey establish
the period forms. HUD/FHA publications establish regulatory context; no
historical permit compliance is claimed.

Floors are 2.7432 m apart. Common stairs use sixteen 171.45 mm rises per story,
279.4 mm goings, 1.1176 m flights and 1.2192 m landings. Guards are 1.0668 m;
separate stair grasp rails are 914.4 mm high and 38.1 mm diameter. Typical
windows are 1.524 × 1.2192 m; entry leaves nominally .9144 × 2.032 m; patio
sliders 1.8288 × 2.032 m. Balconies project 1.524 m on concrete slabs with
steel posts. Shared parking stalls are 2.7432 × 5.4864 m, beside an approximately
8.2 m native crowned road; main walks are 1.524 m.

Meters, split-system condensers/pads, through-wall AC sleeves, sash, sills,
thresholds, gutters, downspouts, vents, lights, numbers, mailboxes and carts
are modeled. Balcony/patio cues include chairs, plants, bicycles, a kettle
grill, a dish and sparse left-up light strings. Trim and weather are quick
color reservations; causal material aging, surface manufacture and dusk
window emission await look-dev.

Blender is meters, +Z up, front −Y. Each building root is centered on its wall
footprint; complex roots are at parcel centers. Footprint polygons and corner
sockets, front/rear walk sockets and each townhouse party wall's center/end
sockets survive export. The party-wall line runs between its two endpoint
sockets. Native context scales are applied into mesh coordinates.

Entry and stair-hall leaves have separate vertical hinge pivots, 0–100° about
Blender Z (glTF Y). Sliders move along their own X track, 0–.7864 m for the
six-foot opening. Garage leaves are four rigid sections per unit, with top
hinge origins and `motion_kind=sectional_track`; `src/garage_motion.py:pose(t)`
uses the existing houses' chord-constrained vertical/curved/horizontal guide,
for normalized opening 0–1. No armature or animation clip is required.
Dumpster lids retain their X hinges, −95–0°. An engine must drive these pivots.

## Shared materials and site

The six building roles match the houses: Siding, Shingles, Veneer, Concrete,
Trim and Glass. **There is no finished baked apartment texture set yet.**
The exported quick palette multiplies vertex colors by one generated 8² white
image, shared by every seed. Source context uses simplified materials and two
1024² original library branchlet color/alpha images, also shared externally.
No photograph or downloaded asset supplies vertices or texels.

The look-dev allocation can reuse HouseSiding (4 MiB), RanchRoof (4 MiB),
HouseVeneer (1 MiB), HouseConcrete (1 MiB), HouseTrim (16 MiB), CapeCedar
(⅓ MiB) and SplitStone (⅔ MiB): **27 MiB of already existing maps**, with no
new apartment set proposed. Roof/veneer alternatives select their applicable
maps within the six roles. This is a plan, not a claim that those maps are
already assigned or that final UV density has passed. Compression estimates
assume 8 bpp/maps with full mips. Loading houses with all 49 MiB already resident
would add no image allocation for that subset when canonical URIs are cached.

`context_build.py` runs original ground, fences, shrubs, trees and pickup
scripts into `apartments/build/context/`. It never rebuilds or writes their
canonical deliveries. Scoped quick-material adapters retain their original
geometry; botanical charts are normalized before static joining. Each native
module is consolidated once and then instanced, avoiding geometry multiplication.

New site construction here comprises the private stalls/paint/stops/islands,
walk branches, carports, cluster mailbox, tapered split-lid dumpster and its
native-fence enclosure, fictional entrance signs, pool bowl/deck/guard and
small swing playground. Amenity walks join the main path; the pool gate has a
separate vertical hinge and opens outward 0–100°. Native lawn regions are clipped around structures,
walks and the pool. Oil reservations follow engine positions. Final paving
and wear should reuse the ground/commercial material conventions.

## Measured checkpoint budgets

Counts below are the current raw glTF **instance** totals. Geometry sizes include
the glTF and BIN, excluding the one shared 808,759-byte PNG inventory. All building
architectures use six materials. Rows include their own patios and entry fittings
in the architecture count; their scene count additionally includes library/site context.

| Apartment seed | Units/building | Building triangles | Whole complex triangles | Building / complex geometry MiB |
| --- | ---: | ---: | ---: | ---: |
| 301 | 12 | 71,957 | 1,114,215 | 9.97 / 37.46 |
| 302 | 16 | 111,608 | 1,109,190 | 15.53 / 41.56 |
| 303 | 24 | 141,138 | 1,157,365 | 19.47 / 48.10 |
| 304 | 8 | 55,134 | 1,061,128 | 7.69 / 30.94 |

| Row seed | Units | Architecture triangles | Row + site/context triangles | Geometry MiB |
| --- | ---: | ---: | ---: | ---: |
| 401 | 6 | 44,246 | 163,732 | 8.85 |
| 402 | 6 | 44,502 | 163,988 | 8.91 |
| 403 | 6 | 51,462 | 247,472 | 13.07 |
| 404 | 4 | 29,386 | 125,024 | 6.84 |

The 16/24/8-unit garden buildings scale the twelve-unit triangle allowance
proportionally; all remain inside it. Whole complexes have 22 quick materials;
row scenes have 12 (18 with parked vehicles), shared across their instances.
The largest scene is 1,157,365 triangles, including vehicles and vegetation.
Context uses 38,226-triangle parked source pickups, 23,680-triangle mature maples
and 5,588-triangle shrubs. Their static templates retain one geometry instance
per placement, rather than accumulating joined copies.

New site geometry measures 1,200 triangles for the cluster mailbox, 720 per
four-stall carport, 340 for the dumpster/body/lids/pad before its native fences,
and 438 for the swing playground. The pool/deck/fixed fence is 8,150 triangles,
with a separate 320-triangle gate; its long fence is an assembly of repeated
rail spans. Sign bodies are 132 triangles. Lettering is excluded from these
part figures and included in the complete scene totals.

The current fifteen external images comprise two 1024² branchlet color/alpha
images and thirteen 8² diagnostic color/normal/ORM images. Their assumed 8-bpp
allocation with full mips is about **2.668 MiB** for the entire checkpoint family.
They are temporary source-context/diagnostic images, not the future 27 MiB PBR subset.

The check reports **zero** degenerate triangles and metric UV triangles across all twelve scenes; 197 existing delivery/docs files retain their pre-session SHA-256 hashes.
Maximum source/import point error on the buildings and rows is 3.932 micrometers; the largest raw unit-normal error is 1.19e-07. These are serialization facts, separate from the physical checks.

## Rebuild and evidence

```sh
make WIDTH=1200 SAMPLES=32  # entire form checkpoint, checks and Cycles views
make check                 # construction, raw glTF, fresh imports, preservation
make matches               # three fitted exported and source photo pairs
# Another seed in a supported grammar:
blender -b --factory-startup --python-exit-code 1 --python src/build.py -- \
  --only Row-409 --out build/custom.blend
```

Preserve each `.gltf`/`.bin` pair beside the common `export/shared/` directory.
One building uses at most six materials. `export/*.json` records dimensions,
plans, triangle counts, image references, pivots, sockets and file sizes;
`build/family.json` summarizes the full build. Counts for complexes include
every instance, not just unique mesh buffers. Row architecture is reported
separately from its site and library context.

`build/check.json` separates physical source measurements from serialization.
It measures actual pan crowns, uniform riser/going intervals, door/casing
surface intersections every 10°, nine slider positions, linked-wing meter
passage bounds, and 21 garage positions per section with
section/guide/ceiling checks. Raw glTF checks cover finite geometry/metric UVs,
unit normals, instance counts, external resources and material budgets. Fresh
imports check counts, complete pivot/socket frames and bidirectional source
point correspondence for buildings/rows. Complexes reuse those checked forms.
This is not continuous whole-assembly collision certification or final UV/bake
verification. Zero-area geometry and staging UVs are rejected. Final texel density and trim-sheet mapping are deferred.

All Cycles calls use the shared GPU lock. Heroes and family views import the
external glTF; source photo pairs remain independent witnesses. Hero/ground
eyes are placed 1.68 m above an actual downward-ray ground hit. Each image
folder records source hashes and camera/light-stage provenance. The photo
solver's residuals are type-fit errors, not survey accuracy; the garage-row
photo has 38 mm-equivalent EXIF, while its fitted lens differs for this original
plan. Neutral assumptions and critique passes are in [REVIEW.md](REVIEW.md).

Per-asset editable source scenes are `build/<stem>.blend`; `build/family.blend` is the last built scene, while `build/family.json` is the aggregate record.

The checkpoint stops here. The weakest areas are shallow repetitive room
backings, sparse landscaping/tenant dressing, simplified context cars and
unweathered quick surfaces. Unit interiors, fire ratings, local accessible
routes, full motion sweeps, final material charts/bakes and game collision/LODs
remain future work. No kit or existing family file is changed.
