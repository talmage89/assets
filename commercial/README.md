# Commercial / seeded corner gas stations

**Exported surface and age checkpoint, awaiting lead review.** Four original
1995–2010 American corner stations, maintained at about fifteen years in service.
The accepted plans, dimensions, circulation, brands, moving parts and sockets
are retained. This round adds construction refinements, shared baked PBR maps,
causal wear, a visible retail fit-out and day/dusk lighting states.

Every vertex, graphic and material field is scripted. No photograph supplies
mesh or texture pixels. [REFERENCE.md](REFERENCE.md) separates published sizes,
authored choices and camera-fit limits; [REVIEW.md](REVIEW.md) records rejected
passes. [TEXTURES.md](TEXTURES.md) gives the allocation and image-sharing rules.
Reference rights and direct files are in [refs/SOURCES.md](refs/SOURCES.md).
No unfinished portfolio JPGs are committed; review images remain rebuild outputs.

## Plans and real dimensions

| Seed | Lot, ft | Store, ft / area | Canopy | Corner / walls / brand / sign |
| --- | --- | --- | --- | --- |
| 101 | 150 × 150 | 60 × 50 / 3,000 sq ft | 3 islands, parallel | SW / split CMU / Rillway / corner monument |
| 102 | 140 × 150 | 56 × 48 / 2,688 sq ft | 2 islands, perpendicular | SE / brick / Latchline / frontage pylon |
| 103 | 160 × 160 | 64 × 48 / 3,072 sq ft | 4 islands, parallel | NW / smooth CMU / Latchline / frontage monument |
| 104 | 160 × 160 | 66 × 50 / 3,300 sq ft | 3 islands at 30° | NE / EIFS / Rillway / corner pylon |

| Construction | Authored real size / measured proof |
| --- | --- |
| Canopy | 14 ft 6 in / 4.4196 m nominal soffit; 3 ft 3 in / .9906 m fascia; 14 in / .3556 m clad columns |
| Islands | 25 ft / 7.62 m centers; 4 × 18 ft / 1.2192 × 5.4864 m; 6 in rise; 21 ft / 6.4008 m clear between curbs |
| Cairn M3 dispenser | 1.10 m cabinet width, .62 m electronics depth, 1.19 m crown, 2.24 m crown height; 30 mm OD hoses |
| Store | 203.2 mm wall shell; 2.75 m glazing head; 3.9624 m roof datum; 4.8768 m parapet; .1524 m slab |
| Public interface | 24 ft clear openings, 5 ft transition wings, native 6 ft apron, 5 ft walk and 15 ft curb-return radius |
| Accessible approach | 132 in vehicle bay + 60 in aisle; a 6 ft 1:12 run and 6 ft level landing in the 12 ft store walk |
| Tank vents | 12 ft / 3.6576 m before caps; original fill/monitor covers use the cited API colors and symbols |

Published municipal/manufacturer comparators and original decisions are cited
in REFERENCE. These are asset dimensions and sampled construction checks,
not structural, ADA, fuel-system or civil-engineering certification.
Meters, Blender +Z up and canonical −Y frontage; a quarter-turn selects the
street corner. Props retain footprint/ground origins, and operating leaves
retain their physical hinges. glTF maps Blender Z to Y up.

## Construction and age

Storefront bays now have masonry pilasters, precast feet/caps, a projecting
folded-metal entry canopy and, on CMU stores, split-face wainscot returns with
a water table. Coping has folds, hems and standing joints. Wall packs, service
lighting, sealed electric meters, disconnect/conduit and a connected gas set
complete the rear/sides. The electrical set clears the cooler. Monument signs
use the store's masonry and a cap; price cabinets have extruded frames.
Canopy columns have folded wraps, a skirt/drip, closure seam and brand band.

The lower hose U has more longitudinal stations and smooth circumferential
normals. The former stray wire/reel proxy is removed: the crown bulkhead and
holstered swivel support the stored hose. No deployable retractor mechanism or
runtime hose deformation is claimed. The nozzle has compound cast sections,
an open guard, grip socket, swivel and curved spout.

The glass reveals gondola shelves, six generated product-front variants,
a cooler-door wall, checkout counter/register and ceiling lights. This is a
representative visible retail volume, not a playable shop plan. Maintained
beds instance the original Boxwood family over generated angular bark chips.

Wear is placed at its causes: engine drips at every fueling face and parking
position; swept tire contact at driveway turns; a repaired service trench and
sealed branching cracks; joint deposits; worn stall paint; gum by the entry;
base/hand-working grime; low bollard scuffs and exposed-steel corrosion; runoff
below coping/fascia joints; low masonry salts/dirt; and south-facing paint fading.
Manufactured grain remains in textures, with broad age in stock vertex tint.
There is no whole-surface dirt noise wash, arbitrary wall peeling or blanket
warm tint on the paving. The maintained age remains an artistic checkpoint.

## Shared PBR and loading

`export/CommercialGas-<seed>.gltf` plus its `.bin` is the stock delivery layout.
`export/textures/` holds **17 new shared images / 39⅔ MiB** assuming 8-bpp
BC7/BC5 and full mipmaps. CMU is 1024; brick, EIFS and roof 512; trim and
shared equipment 2048; both brands' ink sheet 1024. EIFS/roof omit redundant
ORM maps. Glass and the operational emissive states add no images.

Manufacture is generated and GPU Cycles flat-baked at 4096, then filtered in
linear color, vector-normal and roughness-RMS space. Typography/marks are
original 4096 raster art with coverage-aware filtering. The original baked
fields repeat byte for byte. This is a tiled-material bake, not a unique
whole-station projection bake.

Ground asphalt/concrete use their existing canonical images (**32 MiB**),
with native 6.096/3.048 m repeats. Stock public lawn adds its existing **16 MiB**;
Boxwood uses the shrubs family's existing **16 MiB**, once for every instance.
The full wall-alternative + paving/lawn/shrub allocation is **103⅔ MiB**.
A neighborhood already loading ground and shrubs adds only the commercial
**39⅔ MiB**. PNG bytes are not GPU memory. Keep canonical URI/image identities
when loading; the same-scene importer reuse check proves that sharing here.

Each shrub instances two stock meshes; the repeated plants do not upload
nineteen independent botanical atlases or geometries. Neighboring houses,
trees and streets in the presentation are loaded from their own exports and
are excluded from station delivery. Their hashes are recorded.

The exported lamps retain their authored night-capable emission strengths.
Day presentation switches exterior luminaires off, keeps the interior and
prices on, and scales logo-panel emission to .10. Dusk restores their strengths.
Both states use the same exported geometry, inks and PBR maps, with procedural
sun/sky only. Ink colors are stored in the sheet because glTF emission does
not multiply COLOR_0. No replacement source look shader is used for judgments.

## Measured budgets

Counts include real operating leaves, hoses, cylinders, utility gear and wear
ribbons. Each dispenser is **5,160 triangles**, below 6k. Paving, landscaping
and presentation are accounted separately.

| Seed | Store | Canopy + islands | Price sign | Station without plants | Placed stock plants | Whole placed station |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 34,306 | 12,806 | 1,516 | 86,066 | 106,172 | 192,238 |
| 102 | 30,058 | 9,626 | 1,044 | 71,684 | 106,172 | 177,856 |
| 103 | 34,526 | 16,106 | 1,516 | 96,100 | 111,760 | 207,860 |
| 104 | 32,054 | 12,806 | 1,044 | 83,556 | 106,172 | 189,728 |

Default seed's other parts: paving 3,634; separate service-wear ribbons 256;
tank pad 1,164; vents 376; trash/washer 1,116 each; ice cabinet 1,776;
propane cage/cylinders/doors 4,474; dumpster yard/container/gates/lids 3,224;
air/water 1,570; store bollard 256 each; accessible sign 416; light pole 348 each.
The store and canopy are within 45k/18k. The price sign stays below the preferred
2k lower end because its construction does not need filler geometry.

`build/delivery.json` and `build/delivery-check.json` record exact per-seed
geometry bytes, embedded-GLB bytes, unique mesh triangles, material primitives,
shared PNG bytes, UV density and import errors. Placed shrub triangles are not
unique GPU geometry: seed 101's unique mesh total is 91,654 triangles.
The large embedded build GLBs duplicate no images internally but include the
existing ground/shrub PNG payloads; external deliveries share those resources.


| Seed | glTF + geometry BIN bytes | Embedded build GLB bytes | Materials |
| --- | ---: | ---: | ---: |
| 101 | 10,714,116 | 73,894,428 | 18 |
| 102 | 9,241,258 | 70,055,664 | 18 |
| 103 | 11,696,735 | 74,876,996 | 19 |
| 104 | 10,586,865 | 71,201,832 | 18 |

The 17 new PNGs occupy 12,295,219 bytes on disk.
The material counts include separate tiled construction finishes, ground,
foliage, glass, transparent wear, graphics and operational lamp states; they
are not a claim of one draw call for a whole station.

## Parts, pivots and generator

Fixed construction consolidates per reusable module: store, canopy/islands,
each dispenser, sign, site paving, tank pad/vents, trash/washer, ice cabinet,
propane cage, air/water, dumpster yard, bollards, signs and poles. Botanical
meshes remain instanced. There is no armature.

| Moving node | Local axis / range |
| --- | --- |
| Entry_Left / Entry_Right | Z, −100…0° / 0…100°; outer jamb barrels |
| ServiceDoor | Z, −100…0°; rear exterior hinge |
| IceDoor_-1 / IceDoor_1 | Z, −100…0°; separate cabinet hinges |
| PropaneDoor_-1 / PropaneDoor_1 | Z, −100…0°; cage front hinges |
| DumpsterGate_-1 / DumpsterGate_1 | Z, −110…0° / 0…110° |
| DumpsterLid_-1 / DumpsterLid_1 | X, −105…0°; rear lid edges |
| Dispenser_<n>_NozzleA/B | Detachable holstered frames, separate hand sockets |

Entry/nozzle hand sockets, `Socket_StoreEntry`, `Socket_StoreWalk`, and separate
private paving, curb-flowline, apron and public-walk driveway frames survive.
The owner's tank may be loaded only by the read-only fit tool; it never enters
the saved station, maps or export. Source and fresh-import checks distinguish
working surface clearances from mere serialization.

`src/plan.py` remains Blender-independent: 2–4 islands, 0/30/90° canopy axes,
quarter-turn corners, bounded stores, four wall styles, two original brands,
monument/pylon and selected cooler boxes. Rillway retains aubergine/copper/ivory
and three unequal piers; Latchline retains graphite/periwinkle/off-white and
offset brackets. The trade-dress comparison is in REFERENCE. Equal graphic
quads allow UV-selected brand changes without different logo geometry.
Retail walls/openings, storefronts, coping, services and fit-out remain reusable
within this family for the later strip mall. No strip mall is built this round.

## Rebuild and review

```sh
make -C commercial WIDTH=1600 SAMPLES=48
make -C commercial check
make -C commercial export
make -C commercial match
make -C commercial before-after
make -C commercial repeat
```

The default command rebuilds original fields/bakes/maps, four sources and
shared-image exports, checks, Cycles checkpoint views, used-photo pairs and
before/after form crops. GPU work holds the shared kit lock; scratch stays under
worktree build/. Missing stock ground, shrubs, house and oak presentation
exports build with their families' own Makefiles; existing exports stay intact.
No kit source changed.

| Output | Evidence |
| --- | --- |
| `renders/look-checkpoint/hero.png` | Opposite sidewalk, 1.60 m eye, 40 mm lens, verticals vertical; entry clear of monument |
| `renders/look-checkpoint/seeds/<seed>/{street,above}.png` | Four corners and whole-property views fitted to actual exported vertices |
| `renders/look-checkpoint/{dispenser,canopy,column,entry,sign,rear,services,asphalt,landscape}.png` | Construction, services, material and causal age close-ups |
| `renders/look-checkpoint/dusk.png` | Exported canopy, prices, brand/store panels and interior lit |
| `renders/look-matches/*-pair.jpg` | Five calibrated used-photo comparisons, explicit procedural sun/sky and neutral balance |
| `renders/look-matches/*-values.jpg` | Fixed display-value and hue patches; differences retained in values.json |
| `renders/form-fixes/*-before-after.jpg` | Seven fixed-camera crops; before rebuilt from our accepted Git version |
| `renders/look-checkpoint/contact.jpg` | Full checkpoint contact sheet |
| `build/checks.json`, `build/motion-*.json` | Surface probes, 948 total sampled 5° door/gate/lid poses, native ground interface |
| `build/plan-check.json` | 1,000 pickup routes with occupied parking; tightest SAT gap .225 m |
| `build/delivery-check.json`, `build/look-view-check.json` | Actual geometry/UV/normal/image reuse; current source/image/context hashes |

Photo cameras fit selected structure, not entire stations: PA 2006 canopy
1.66 px RMS; CA 2009 dispenser .28 px; PA forecourt crop 3.43 px; TX 2004
entry .58 px; supplementary VA 2009 paving 19.26 px with a 1.65 m eye prior.
Sun elevations/directions are estimates from visible shadows;
photos do not supply surveyed solar positions, camera response or albedos.
The five comparisons use four photographs, with two PA crops. Neutral ROIs
and linear gains are in `build/reference-balance.json`.

Fixed display Y′ medians (export / balanced photograph; not albedos):

| Surface | Export | Photo | Relative difference |
| --- | ---: | ---: | ---: |
| soffit | 0.434 | 0.417 | +4.2% |
| concrete | 0.636 | 0.795 | -20.0% |
| dark cabinet | 0.159 | 0.135 | +17.9% |
| eifs | 0.692 | 0.663 | +4.4% |
| asphalt | 0.544 | 0.466 | +16.8% |

Remaining limitations are recorded in REVIEW: the PA concrete remains darker
than its very bright photograph, VA asphalt is brighter than its comparator,
the photographed soffit is warmer, and exact
black-surround/EIFS appearance differs between manufacturers and lighting.
The original station plan, single column row, flat fascia and stored hoses
are not copies of those photographed systems. Repetition, regular construction,
flat bark relief and simple package geometry remain visible close up. The
finest wear is weaker from the opposite sidewalk than in detail views; this is
not presented as a perfect photograph or an accepted portfolio final.
