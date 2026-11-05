# Neighborhood strip centers — form checkpoint

Four original maintained small-shop centers using the commercial family's
construction. **This is the requested form gate, before strip look development.**
Diagnostic GLBs use quick finishes and one original tenant sheet. Manufactured
masonry, causal 15–25-year wear, final baking and portfolio docs are deferred.
[Sources and tenant originality](STRIP_REFERENCE.md) and the strip section of
[REVIEW.md](REVIEW.md) accompany the images.

## Plans and dimensions

| Seed / center | Lot, ft | Building | Front / walls | Spaces |
| --- | --- | --- | --- | ---: |
| 201 / Alder Rill Shops | 336 × 244 | 240 × 70 ft; 16,800 sq ft; ten 24 ft bays, nine leases | Flat metal covered walk; split CMU; end towers | 101 |
| 202 / Crossbend Court | 324 × 238 | 220 × 64 ft; 14,080 sq ft; ten 22 ft bays, nine leases | Mansard; brick; center tower | 97 |
| 203 / Lowbank Commons | 348 × 250 | 242 × 76 ft; 18,392 sq ft; eleven 22 ft bays, nine leases | Segmental arcade; EIFS; end towers | 109 |
| 204 / Willow Span Shops | 396 × 244 | L: seven 24 × 64 ft main bays, two return bays, 64 ft square elbow; 17,920 sq ft | Flat canopy; smooth CMU; elbow entry | 90 |

Dimensions are authored against the brief and cited comparators, not recovered
from surveyed properties. Standard parking is **9 × 18 ft**, around two
**24 ft** double-loaded aisles. **9 ft** planted islands bookend and break up
the rows. Six **11 ft** accessible spaces share three exclusive **5 ft** aisles,
dispersed along the walk. Their recessed **6 ft / 1:12** ramps stay within the
**10 ft** walk and retain a **4 ft** level landing. Actual surface rays check
that column bases do not intrude. The two **24 ft** entrances use native
five-foot transition wings and six-foot aprons on the ground six-inch grid.
Side drives connect to a **24 ft** rear drive. The L's front aisle continues
through a reserved cross aisle with a turn flare.

Floor is **.1524 m**; membrane datum **4.2672 m**; parapet **5.1816 m**; tower
top **6.72 m**. Storefront head/transom/sill are **2.75 / 2.20 / .27 m**.
Flat/arcade soffit is **3.3075 m**, mansard soffit **3.0925 m**. Source rays
measure these independently of the GLB roundtrip.

The parking dimensions come from Brookfield's published nonresidential site
standards; the count/van dimensions come from the US Access Board. The retail
ratio comparator is Commercial Point's **3 spaces / 1,000 sq ft** shopping
center baseline. The four actual ratios are **6.01 / 6.89 / 5.93 / 5.02**.
These exceed that comparator; they are not a mixed-use demand study or a
claim of local approval. [STRIP_REFERENCE.md](STRIP_REFERENCE.md) links each
authority, states its limits and separates authored sizes from photo picks.

## Parameters

`strip_plan.generate(seed, overrides)` produces a pure-Python plan before
Blender builds anything. Four bounded archetypes select row/L, bay count,
width/depth, lot, canopy/arcade/mansard, towers and wall finish. Other seeds
shuffle all eight trades plus vacancy and vary depth/color within the same
tested archetypes. Driveway stations follow the lot width on the ground
six-inch grid; parking counts and access groups regenerate from the available
frontage. This is deliberately a bounded grammar, not arbitrary parcel design.

A JSON passed as `STRIP_PLAN=build/my-plan.json` can override `lot_ft`,
`bays`, `bay_ft`, `depth_ft`, `shape`, `style`, `wall`, `color` and `towers`.
Dimension/circulation validation rejects unsupported plans. `TENANTS` holds
the original names, sign style and colors; the atlas supplies fixed-size cells
so a tenant changes through UV selection. Proof seeds are 201–204.

## Construction and reuse

Each bay owns its slab, aluminum storefront, lit shallow room, covered-walk
share, roof membrane, rooftop unit, vents, rear wall, scupper/downpipe, gas
meter and disconnect. Adjacent bays combine at an end; their shared demising
wall and room finish are removed. Fixed construction joins per module.
Rear-wall pieces retain their own reusable mesh roots inside each bay.
End caps, towers, roof ladder, meter bank, pylon, paving, poles and dumpster
yard remain separate. The L closes a real elbow/storage volume and miters
its walk/canopy; it is not two overlapping rows of shop boxes.

The common meter bank occupies the rear of the right end wall, clear of the
left dumpster yard and rear rain leaders/gas gear. Mounting feet fit the
projecting base; an actual-surface check tests the bank against every other
mesh and probes its outboard working space.

Direct reuse: `building.storefront`, `glazed_leaf`, `wall_with_openings`,
`rooftop_unit`; family geometry/coping/utility vocabulary; `siteworks.strip`,
`curb_run`, `flat`; the unchanged ground profile/transition adapter; family
light poles and operating dumpster enclosure; stock Boxwood's two meshes and
three maps. No gas-station module or canonical output is changed. No kit
feature is added. Main remains unmerged pending the lead's instruction.

New `strip_*.py` modules supply plans, bay/end/tower wrappers, mansard/arcade,
meter bank, tenant furnishing, parking/cross aisle, pylon, sign sheet, checks
and presentation. Sub-4 mm edge breaks belong in the future trim normal;
larger cabinet, casting, masonry-base and upholstery radii remain geometry.

The original occupants are **Vellum Nails, Hemwick Dry Cleaners, Notch Oven
Pizza, Copperfold Laundry, Pintrace Phone Repair, Drowsefield Mattress,
Tallied Oak Tax, Snipwell Hair Studio**, plus **For Lease**. Their names,
letter/raceway, box and panel treatments differ from national chains as
recorded in STRIP_REFERENCE. All sign/window quads retain identical topology
when UV selection changes tenant. Names, hours, addresses and parking captions
share one sheet. Door-mounted notices travel with their leaves.

Visible rooms have salon/manicure chairs and desks, garment racks, a pizza
counter/oven/tables, washers/folding tables, repair/tax desks and mattress
displays. These are economical shallow fit-outs, not playable interiors.
Vacancy has an empty unlit backing.

## Budgets and memory

| Seed | Building | Bay range | Pylon | Center without plants | Whole placed center | Unique-mesh triangles | GLB bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 201 | 54,738 | 3,602–6,432 | 3,104 | 77,036 | 278,204 | 82,624 | 10,925,644 |
| 202 | 52,812 | 3,610–6,458 | 3,104 | 74,770 | 275,938 | 80,358 | 10,861,500 |
| 203 | 59,256 | 3,690–6,538 | 3,104 | 82,274 | 283,442 | 87,862 | 11,372,236 |
| 204 | 47,664 | 3,496–6,462 | 3,104 | 69,118 | 270,286 | 74,706 | 10,444,704 |

Every proof stays below **80k building / 7k bay / 5k pylon**. Counts include
moving leaves. Exact per-part and frame measurements are retained in
`build/strip/strip-<seed>.json` and `build/strip/checks.json`.

Default bays 01–10 are **4,712 / 4,946 / 5,118 / 4,690 / 3,602 / 4,702 /
4,638 / 4,682 / 6,332 / 6,432** triangles. Larger end leases retain one RTU
per original structural bay, as a combined tenancy in an existing center can.

For example, bay 01's **4,712** comprises **3,508** fixed front/room/walk/roof,
**866** fixed rear-service construction, **314** entry leaf and **24** rear
steel leaf. Rear pieces and both leaves retain their own meshes/pivots.

The default's end caps are 312 triangles each; towers 406 each; ladder 760;
meter bank 2,688; paving/stripes/curbs 16,070; six poles 316 each; operating
dumpster yard 1,228. Landscape
has **36 stock shrubs**, **5,588 unique mesh triangles / 201,168 placed**.
Whole-center placement cost is deliberately reported separately from unique
geometry. Street, station, house and pickup context never enter its export.

There are **18 quick material states**, including the two stock shrub states.
This is a diagnostic palette, not the final draw-call allocation. Shared trim,
equipment, masonry, graphics, glass and lamp consolidation awaits the family's
gas-station material delivery and the next gate.

Current maps: **one new 2048² RGBA sign sheet**, about **5⅓ MiB** with BC7 and
full mips, plus the unchanged shrubs' **16 MiB** triple reused once. Scalar
finishes/glass add no images. Native ground context reuses its three existing
2048 triples (**48 MiB**). PNG/GLB bytes are not GPU memory.

The planned look shares Commercial CMU/brick/EIFS/roof, trim and equipment.
Signs are the sole proposed new set; no interior sheet is needed. The whole
existing commercial allocation plus signs is **45 MiB**, or **109 MiB** with
required ground/lawn/shrubs and all wall alternatives loaded. Mansards reuse
the houses' unchanged shingle triple (**16 MiB existing**, shared with houses).
See [TEXTURES.md](TEXTURES.md) for the allocation assumptions.

## Parts and frames

Meters, Blender +Z up / frontage −Y; glTF maps `(x,y,z)` to `(x,z,−y)`.
`StripCenter_<seed>` is at the site footprint center at grade. Bay modules use
front-center construction anchors and left/right repeat sockets. Pylon and
loose props retain their ground-footprint origins.

| Node | Local axis / range |
| --- | --- |
| `Bay_<nn>_Entry` | Physical exterior hinge, Z −100…0°. Handle/threshold sockets retained. |
| `Bay_<nn>_ServiceDoor` | Rear frame's exterior hinge, Z −100…0°; rotated rear parent faces outward. |
| `Strip_DumpsterGate_-1/1` | Z −110…0° / 0…110°. |
| `Strip_DumpsterLid_-1/1` | X −105…0° at rear lid edges. |
| `Bay_<nn>__RepeatLeft/Right` | Structural-bay joint anchors. |
| `Socket_{Drive,GroundCurb,GroundApron,GroundWalk}_1/2` | Private paving and native public-interface frames. |

Transforms are rebased/applied within each module. No armature or animation
clips; the game supplies door controllers, collision, navigation and LODs.

## Rebuild and evidence

```sh
make -C commercial strip WIDTH=1600 SAMPLES=40
make -C commercial strip-check
make -C commercial strip-repeat
make -C commercial strip-model STRIP_SEEDS=201,202,203,204
make -C commercial strip-render
make -C commercial strip-match
```

The additive targets hold the shared GPU lock for every Cycles invocation.
Missing ground/shrubs/pickup build through their own Makefiles. Scripted
station and split-level forms stay under `commercial/build/strip/context/`, preserving
their canonical deliveries. The existing pickup GLB is read-only context.

| Output after rebuild | Evidence |
| --- | --- |
| `build/strip/strip-<seed>.{blend,glb,json}` | Sources, exported module hierarchies, exact counts and frames |
| `build/strip/plan-check.json`, `plan-<seed>.jpg` | 1,000 plans; seven invalid controls rejected; occupied-lot pickup routes and representative park/back-out |
| `build/strip/checks.json`, `motion-<seed>.json` | Actual wall/roof/walk/ramp/native-curb surfaces, pedestrian clearance, moving-part sweeps and raw/fresh GLB import |
| `renders/strip/checkpoint/hero.png` | 1.6 m eye on native opposite sidewalk, 40 mm lens, level verticals |
| `renders/strip/checkpoint/seeds/<seed>/{above,street}.png` | Four centers in native road, curb, sidewalk and lawn |
| `renders/strip/checkpoint/{storefront,walk,tower,pylon,rear,services}.png` | Tenant room/sign, walk, tower, pylon and rear utility construction |
| `renders/strip/checkpoint/scale.png` | Same-scale strip, station form, split-level form and pickup |
| `renders/strip/matches/{commerce,sterling,sunnyvale}-pair.jpg` | Two period comparators plus an older auxiliary; neutral-balanced, kit-fitted exported GLBs |
| `renders/strip/checkpoint/{family,details,contact}.jpg` | Checkpoint sheets; complete contact includes all three fitted pairs |
| `build/strip/view-check.json`, `repeat/check.json` | Current export/image/dependency hashes and independent byte repeat |

The completed verification run passes **1,000 plans**, rejects **seven invalid
controls**, and clears occupied-lot pickup routes plus a representative car's
park/back-out in all four centers. Pickup routes retain at least **1.93 m**
separating gap; the selected parking maneuvers retain at least **.393 m**.
These are sampled geometric proofs, not traffic-capacity or delivery-truck
certification.

All **2,040** sampled moving-part poses pass with zero measured penetration
and no contact exemptions. Every bank clears all other source meshes; its
mounting feet are within **.50 mm** of the wall, cabinet backs measure about
**85 mm** from it, and **324 finite rays per seed** clear a **1.2 m** working
corridor. Ramp/landing surface errors are below **.4 µm**, native-curb surface
gaps below **8 µm**. Fresh GLB import positions differ by at most **12 µm**;
that last number proves serialization, separately from the construction tests.
The image audit covers **19 current exported views**. The default's independent
factory-startup GLB rebuild is byte-identical. Repository rules pass; no kit
code was changed, so a kit-wide regression run is not applicable.

The form gate stops here. Unweathered quick walls/paving, simple furnishings,
sparse surroundings and weak unsurveyed photo fits remain visible limitations.
Virginia's brochure states **1989**; Texas is reported **2002** by a secondary
property record. Both remain unsurveyed; California is an older auxiliary,
excluded from period proof. The native Ground repair pattern is conspicuously
repeated in overhead context; that
shared asset is unchanged here. Rear service leaves have a six-inch step
to the lot; detailed service landings are still weaker than the front access.
The mansard's shingle pattern, final masonry, service wear, sign optics and
shared-image delivery await look development. No unfinished `docs/` art is
committed.
