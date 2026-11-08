# Manufactured home communities — form and construction checkpoint

An original, script-built family for an American town of 1995–2015. Alder
Court is a compact older through-street community; Meadow Bend is a spacious
1990s loop with double-wides, a clubhouse and a playground. The home, lot,
addition and street grammar is reusable independently of either example.

**This stops before look-dev.** Home materials are quick vertex colors with
one shared 8 × 8 white image. Native library props retain their images where
available. There is no manufactured-home bake, finished wear, final gallery,
collision delivery, interior or game-ready claim. No `docs/` images are
committed. Four critique rounds are recorded in [REVIEW.md](REVIEW.md).

Local checkpoint images, rebuilt by `make`:

- [Alder Court street hero](renders/checkpoint/pass4/Park-101/hero.png) and
  [oblique](renders/checkpoint/pass4/Park-101/above.png).
- [Meadow Bend street hero](renders/checkpoint/pass4/Park-202/hero.png) and
  [oblique](renders/checkpoint/pass4/Park-202/above.png).
- [Complete contact sheet](renders/checkpoint/pass4/contact.jpg),
  [photo comparison sheet](renders/checkpoint/pass4/matched-contact.jpg),
  [single-wide turnaround](renders/checkpoint/pass4/SingleWide-120/turnaround.jpg)
  and [double-wide turnaround](renders/checkpoint/pass4/DoubleWide-228/turnaround.jpg).
- [Home forms](renders/checkpoint/pass4/HomeForms/detail.png),
  [add-on sheet](renders/checkpoint/pass4/Modules/detail.png),
  [exposed piers](renders/checkpoint/pass4/SupportFrame/piers.png),
  [deck](renders/checkpoint/pass4/Deck/detail.png),
  [carport](renders/checkpoint/pass4/Carport/detail.png),
  [service pedestal and risers](renders/checkpoint/pass4/UtilityService/detail.png),
  [entrance sign](renders/checkpoint/pass4/EntranceSign/detail.png) and
  [human/car scale](renders/checkpoint/pass4/SingleWide-120/scale.png).

## Scale and construction

All dimensions are meters. Long home axis is Blender X, grade is Z = 0 and
the primary side entry faces −Y. Each component origin is centered at grade;
door origins are on their actual hinge pins. Exports use glTF Y up.

The [reference register](refs/SOURCES.md) contains direct image/PDF URLs,
authors, rights and specific uses. The historic boundary is
[HUD's June 15, 1976 construction standard](https://www.hud.gov/hud-partners/manufactured-home-resources).
Earlier homes used varying industry/state rules, including ANSI A119.1 and
NFPA 501B; [Minnesota's historical rule](https://www.revisor.mn.gov/rules/1350.0100/)
documents that distinction. These game meshes have no certification label.

[24 CFR 3280, 2015 edition](https://www.govinfo.gov/content/pkg/CFR-2015-title24-vol5/pdf/CFR-2015-title24-vol5-part3280.pdf)
informs permanent-chassis construction and exterior openings.
[Part 3285](https://www.govinfo.gov/content/pkg/CFR-2015-title24-vol5/pdf/CFR-2015-title24-vol5-part3285.pdf)
informs piers, caps, shims, anchors, skirts and access. Its installation rules
postdate the old homes: they are a construction comparator, not a claim
about original 1972 installation practice or engineering adequacy.

| Inspection home | Era | Authored body, ft | Body width × length, m | Triangles | Materials | glTF + BIN, MiB |
| --- | --- | --- | --- | ---: | ---: | ---: |
| SingleWide-120 | 1972 | 12 × 60 | 3.6576 × 18.2880 | 30,627 | 5 | 2.776 |
| SingleWide-147 | 1984 | 14 × 70 | 4.2672 × 21.3360 | 30,555 | 6 | 2.750 |
| SingleWide-168 | 1984 | 16 × 80 | 4.8768 × 24.3840 | 33,927 | 6 | 3.052 |
| DoubleWide-245 | 1996 | 24 × 52 | 7.3152 × 15.8496 | 22,462 | 6 | 2.026 |
| DoubleWide-228 | 1996 | 28 × 60 | 8.5344 × 18.2880 | 24,673 | 6 | 2.222 |
| DoubleWide-326 | 1996 | 32 × 64 | 9.7536 × 19.5072 | 25,388 | 6 | 2.288 |

The body sizes are **original grammar dimensions**, not replicas of named
manufacturer models. Published Champion dimension sheets distinguish a
nominal 16 ft section from an actual 15 ft 2 in body, and nominal 28 × 56 ft
from actual 26 ft 8 in × 52 ft. Those sheets establish dimensional context
only; their plans were not copied. The authored walls use the exact body
dimensions above. Small relief, trim, eaves and flues extend the envelope.
Raw-export footprint spans and ray-measured wall widths are recorded in
`build/check.json`; the latter include up to 26 mm of lap relief.

Construction sections:

- Floor elevation 0.910; 19.05 mm plywood on 38.1 × 139.7 mm joists at no
  more than 406.4 mm centers. The 254 mm steel I rails have 6 mm webs and
  12 × 115 mm flanges. A raw-mesh sample measures the rail underside at
  **0.49725 m**, above Part 3285's 0.3048 m comparator.
- Main rail piers are within 0.5 m of each end and at no more than 2.4384 m
  centers by construction. Two hollow CMU courses, a 38.1 mm hardwood cap
  and opposed wedges bear under each rail. Concrete pads are partly buried.
  Double-wides add marriage-line supports and visible end joint trim.
  Spacing is an authored parameter, not an independently measured load test.
- Galvanized 31.75 × 0.9 mm tie straps connect rail clips to ground-anchor
  tension heads inside the skirt. Hitch tongues and transport wheels are
  absent. This depicts a permanently installed exterior, not a towing rig.
- Eaves are 3.120 m for the 1972 form and 3.350 m for the later forms.
  Older rolled roofs have a 130 mm bow; later single-wides have a 2:12
  profile, double-wides 3:12. Seamed metal and shingle roof options are
  separate from siding choice. Gauged walls have actual openings, jambs,
  sash/storm frames, backing cavities, blinds and corner returns.
- Skirts have vents, lower tracks, a seeded missing panel and a separate
  lift-out panel over an actual opening, about 0.8 m wide × 0.61 m high.
  Fine panel ribs are geometry at this gate; the eventual normal sheet can
  absorb relief that does not affect the silhouette.

## Modules and native reuse

| New component | Principal dimensions / construction | Triangles | Materials |
| --- | --- | ---: | ---: |
| Deck | 3.6576 × 2.1336 m proof module; 3.048/4.2672 m width variants; cupped boards, beams, joists, 88.9 mm posts | 1,576 | 2 |
| Carport | 6.7056 × 3.3528 m; 2.42–2.68 m roof, hollow 76.2 mm posts, folded 0.8 mm pans, independently supported | 2,060 | 2 |
| UtilityService | Meter, breaker, conduit, water valve and sewer cleanout; three actual connection sockets | 508 | 3 |
| PropaneBottles | Two unbranded 100 lb class cylinders; 378 mm diameter, 1.206 m above pad per Manchester specification | 796 | 2 |
| Condenser | 0.98 m pad, housing, grille and short line set | 744 | 2 |
| WindowAC | 0.58 × 0.55 × 0.38 m housing with support brackets | 212 | 1 |
| SatelliteDish | Spun concave pan, mounting post and feed arm | 276 | 1 |
| AddedRoom | 3.2 × 2.4 m, independent piers, 2.95–3.20 m roof, real sash opening and removable skirt | 672 | 5 |
| Household | Two pots, procedural leaves and small ride-on toy | 432 | 3 |
| EntranceSign | 2.9 m fictional sign on timber posts; open-license lettering | 685 | 2 |
| SupportFrame | Unskirted single-wide chassis/pier inspection assembly | 4,036 | 3 |
| Modules sheet | Add-ons with labels; inspection assembly, not one prop budget | 10,603 | 5 |
| HomeForms sheet | All six bodies and labels; inspection assembly | 169,578 | 6 |

The deck top is authored at 0.885 m; a fresh-import ray measures
0.884807 m on a cupped board and 0.147550 m at the low tread. Six equal
147.5 mm rises, five 279.4 mm treads and a 935 mm deck rail are explicit.
Back doors receive smaller independent decks/steps, rotated toward grade.
Independent export rays measure beam bottom/top at 0.491200 / 0.675400 m,
post top at 0.491200 m and joist underside at 0.675400 m: the inspected
bearing surfaces meet within 0.1 mm.

Reused geometry comes from the existing families, without editing their
deliveries: Houses' indexed construction helper and Apartments' native
library importer; Ground's materials, grass-edge generator and public road
modules; chain-link sections/posts/gates and privacy fence enclosures;
mailboxes, trash carts, patio chairs and grills. Shed, Utility and Playground
are built from their native source scripts into local quick-material
adapters because their final packages were absent here. These adapters are
9,700 / 5,944 / 7,508 triangles, respectively; the playground count includes
the four-seat swing assembly and spring toy. The inherited shed exceeds a
standard prop's 8k tier because its native framed interior and working
double doors are preserved. No second shed or pole modeling system is added.

Other reused per-instance costs are 1,264 triangles for the mailbox, 5,556
for the trash cart, 1,648 for the lawn chair and 19,912 for the native hero
grill. A chain-link section is 504; line/terminal posts are 492/876; a
complete gate bay is 3,312 across its separately budgeted leaf, latch and
posts. Their original family materials and pivot structures are retained.

## Two communities

| Park | Residential homes | Ground envelope, m | Main lot, ft / sq ft | Private street | Triangles | Materials | glTF + BIN, MiB |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| 101 / Alder Court, 1968 plan | 10 | 79.152 × 102.960 | 40 × 110 / 4,400 | 20 ft / 6.096 m through lane | 629,000 | 29 | 35.899 |
| 202 / Meadow Bend, 1994 plan | 12 | 123.4672 × 139.536 | 64 × 120 / 7,680 | 24 ft / 7.3152 m rounded loop | 758,960 | 33 | 41.865 |

Counts include home bodies, decks, carports, native props, facilities,
private ground/roads and service infrastructure. Cars and vegetation are
**placement sockets**, not meshes duplicated into the park packages. Render
provenance reports their actual instantiated triangles separately from the
park, neighboring buildings and public streets.

| Render context, counted separately | Alder Court | Meadow Bend |
| --- | ---: | ---: |
| Cars, including 14 on public streets | 1,851,325 triangles / 30 cars | 2,280,409 triangles / 37 cars |
| Trees and shrubs, including town canopy | 913,864 triangles | 1,072,020 triangles |
| Neighboring house architecture | 1,632,416 triangles | 1,632,416 triangles |
| Reused public road modules | 15,420 triangles | 15,420 triangles |

Resident/visitor cars number 16 / 23; factory paint varies independently
of the three body types. These context counts come from imported meshes,
not fixed allowances. A game can populate or cull the exported markers
without loading the whole presentation neighborhood.

The older frontage and lot area match the common 40–50 ft / 4,000–5,000 sq ft
range surveyed in [HUD's 2000 builder guide](https://www.huduser.gov/Publications/PDF/buildergd.pdf).
The [Johnson City code](https://ecode360.com/12624699) supplies a 40 ft
frontage / 20 ft drive comparator; Forsyth County's official UDC supplies
the 24 ft two-way road comparator. These modern dimensions are not a
claim of historical local approval. Homes are set 6.096 m behind the
private pavement edge, with separate parking approaches. Fresh raw-mesh
home separations along the outer rows are **7.279–8.193 m** in Alder Court
and **10.022–12.765 m** in Meadow Bend. These measure home shells, not all
attached structures or statutory setbacks.

Meadow Bend has ten large outer lots and two shorter central 24 × 52 ft
homes. The central lots are 29.6848 m deep. Gross density, including common
ground, is only **4.966 / 2.819 homes per acre** for old/new. The newer park
is deliberately generous but remains much less dense than the photographed
Florida park or HUD's common 6–8 homes/acre survey. This is a visible
weakness to decide at the next gate, not a hidden compliance claim.

Every seeded home and dressed lot is counted independently below. Lot
totals exclude cars/vegetation but include their native fixed props.

| Park / lot | Home seed | Era / body, ft | Home triangles | Dressed lot triangles |
| --- | ---: | --- | ---: | ---: |
| 101 / 1 | 10101 | 1972 / 12 × 60 | 22,421 | 42,981 |
| 101 / 2 | 10102 | 1972 / 12 × 64 | 23,267 | 68,923 |
| 101 / 3 | 10103 | 1984 / 16 × 70 | 32,063 | 58,615 |
| 101 / 4 | 10104 | 1972 / 14 × 52 | 21,438 | 43,746 |
| 101 / 5 | 10105 | 1972 / 12 × 60 | 31,004 | 74,860 |
| 101 / 6 | 10106 | 1972 / 12 × 60 | 23,109 | 48,785 |
| 101 / 7 | 10107 | 1972 / 12 × 64 | 23,789 | 46,461 |
| 101 / 8 | 10108 | 1984 / 16 × 70 | 31,838 | 77,386 |
| 101 / 9 | 10109 | 1972 / 14 × 60 | 22,725 | 46,521 |
| 101 / 10 | 10110 | 1972 / 14 × 64 | 23,441 | 45,993 |
| 202 / 1 | 20201 | 1996 / 24 × 60 | 24,629 | 48,957 |
| 202 / 2 | 20202 | 1996 / 32 × 64 | 24,859 | 47,743 |
| 202 / 3 | 20203 | 1996 / 28 × 60 | 24,263 | 69,871 |
| 202 / 4 | 20204 | 1996 / 28 × 60 | 24,346 | 50,622 |
| 202 / 5 | 20205 | 1984 / 16 × 76 | 22,340 | 43,508 |
| 202 / 6 | 20206 | 1996 / 32 × 56 | 23,841 | 69,309 |
| 202 / 7 | 20207 | 1996 / 24 × 56 | 23,341 | 49,817 |
| 202 / 8 | 20208 | 1996 / 24 × 64 | 25,034 | 48,010 |
| 202 / 9 | 20209 | 1996 / 28 × 60 | 24,141 | 67,665 |
| 202 / 10 | 20210 | 1984 / 14 × 76 | 33,233 | 59,601 |
| 202 / 11 | 20211 | 1996 / 24 × 52 | 22,670 | 45,714 |
| 202 / 12 | 20212 | 1996 / 24 × 52 | 22,816 | 68,088 |

The older office/laundry assemblies cost 23,132 / 20,752 triangles; the newer
clubhouse/laundry assemblies 24,193 / 27,272, including their entry decks.
Their signs, decks, cluster mail,
dumpster enclosure, visitor parking, common walks and playground are
included in whole-park counts. Native pole sockets support sagging overhead
conductors; individual lot service connections route below grade to risers.
New common components cost 752 triangles for cluster mail, 112 for the
schematic dumpster, 448 for each park's two bump/sign assemblies, 2,016 for
the three conductor spans and 228 per lot for under-home service routes.
Meadow Bend's visitor markings add 60. The dumpster and pot foliage remain
simpler than the home and deck construction.

## Generator and game connections

`src/plans.py` has no Blender dependency. `home(seed, era, width_ft,
length_ft)` accepts eras `1972`, `1984`, `1996`, widths 12/14/16 or
24/28/32 ft and the bounded length choices 52/56/60/64/70/76/80 ft.
The seed chooses siding, color, roof, porch width, carport, independent
room, AC type, propane, dish, missing panel, tarp, sag and upkeep label.
The upkeep label is not yet a weather shader. `park(seed, kind, rows)` uses
`old`/`new` and 4–6 lots per outer row. Home seeds are derived per lot;
lengths and plant placement have independent deterministic random streams.
An older through lane and a newer closed loop have different road graphs,
lot widths, home mix, common reservations and building placements.

`homes.py` constructs bodies; `addons.py` constructs the additions;
`site.py` assembles lots and facilities. `build.py` publishes every
standalone component and both parks, plus JSON plans, budgets, pivots and
socket counts. Change the plan or call these functions to lay out one lot
at a time; the example layouts are not a monolithic imported mesh.

Primary and rear doors, storm doors, shed doors and native gates remain
separate at their inherited or authored pivots. Home axes are Blender Z:
front door 0…100°, back −100…0°, storm −105…0°. `make check` sweeps the
six standalone homes at 2° intervals with 1 mm tolerance: 18 motions,
936 tested poses in total. Skirt access is a separate lift-out object.
Native shed/gate motion definitions remain inherited; this checkpoint
does not claim a complete sweep against every dressed lot neighbor.

The exported parks also pass **177 static assembly-pair checks** between
separate lots and common facilities, plus **16 deck/carport mesh checks**.
Car sockets have at least 6.539 m spacing in Alder Court and 2.743 m in
Meadow Bend. These are rest-pose mesh/marker checks, not swept vehicle
clearance. The final placement audit removed duplicate carport sockets and
moved the mail cluster beside the common walk, clear of the central homes.

`socket_kind` extras identify car, occupant, door approach, mailbox,
electric/water/sewer, street connection, planting and drive-path nodes.
Drive nodes contain `path_id`, `next_index`, width, 10 mph speed and closure;
the loop entry also identifies its connection segment. Occupant sockets
sit on decks and at thresholds. Native shed and fence extras survive.

## Images, materials and memory

All 21 packages are glTF + BIN with external images. Native maps are
hash-identified and reference canonical family paths; other shared maps
are written once under `export/shared/`. Copy the package **with its
referenced images**, or remap those URIs through a game's resource loader.
No photograph, downloaded asset or HDRI is used as a material or light.

At this gate, the unique image allocation across both park packages is
**124.042 MiB**, estimated at 8 bits/texel block compression with full
mipmaps. That is existing Ground lawn/asphalt/concrete/trim, privacy fence,
patio and grill 2048 trios (16 MiB each), mailbox/cart/chain-link 1024 trios
(4 MiB each), one native 64 × 512 playground chain card (0.0417 MiB), and
the white 8 × 8 home placeholder (under 0.001 MiB with block padding/mips).
The parks share these resources; the second park does not allocate a
second set. PNG disk size and uncompressed glTF runtime size differ.
Cars, trees and render-only neighboring houses add their own native images.

The later home look-dev should reuse Houses' Siding 1024, Shingles 2048
and Trim 2048 sets (36 MiB already shared with the town). **One new
manufactured-home set**, 2048 BaseColor / OpenGL normal / ORM, is reserved
for ribbed metal roofing/siding, skirt, steel chassis, piers and aluminum
carport. Its incremental compressed allocation is **16 MiB**, independent
of the number of lots. No new baked set has been authored at this gate.
Six quick construction roles currently aid inspection; they are not a
final draw-call optimization or finished material count.

## Rebuild and proof

Blender 5.2 and the repository's existing Python tools are required. No
packages, scripts or binaries are downloaded. From this folder:

```sh
make                         # references, models, checks, locked Cycles set, pairs, contacts
make check                   # raw export, sampled dimensions, re-import, home door sweeps, repo rules
make repeat                  # regenerate packages and compare bytes with cached native inputs
make OLD_SEED=303 NEW_SEED=404 ROWS=6 PASS=alternate
make render PASS=preview WIDTH=1000 SAMPLES=16
make check-preservation
```

`kit/checkpoint_rules.mk` supplies the gate graph; `kit/with_gpu.sh` holds
the shared GPU lock once for the complete render batch. Modeling and
checks use serial Blender processes. References are fetched only as
images/PDFs into ignored `refs/`. Existing accepted native packages are
read-only inputs. Missing native deliveries have a source-only fallback
under `build/library/`, built with their original Makefiles; no sibling
delivery is overwritten. The warm-input path is exercised here; a complete
cold rebake of every native family has not been exercised in this checkpoint.

Evidence is local and rebuildable:

| File | Evidence / limit |
| --- | --- |
| `build/family.json`, `export/*.json` | Every piece/home/lot count, dimensions, materials, images, pivots and sockets |
| `build/check.json` | Raw triangle/normal/finite UV checks, zero collapsed geometry/UV triangles, fresh re-import counts, sampled physical dimensions, 1,000 deterministic plans |
| `build/motion.json` | Sampled actual home-door meshes; no penetrations, no contact exceptions |
| `build/repeat.json` | Byte identity of regenerated glTF/BIN/JSON/local PNGs, using cached native inputs; not a GPU rebake test |
| `build/preserved.json` | SHA-256 baseline for 492 pre-existing delivery/image files; all unchanged |
| `renders/checkpoint/pass4/provenance.json` | Fresh glTF imports, image/export hashes, camera/light settings and actual context triangles |
| `renders/checkpoint/pass4/tonal-report.json` | Image percentiles and near-clip fractions; supports visual judgement, not albedo certification |
| `renders/checkpoint/pass4/source-verification.json` | Every render receipt still matches its current glTF and external image hashes |
| `renders/checkpoint/pass4/matches/` | Three photo pairs, neutral patches, camera overlays and calibration residuals |

Heroes are perspective views from 1.68 m at 40 mm under a procedural clear
sky and 18° raking sun. The complete set also includes turnarounds,
skirting, opened entry, exposed frame/piers, all requested module details,
scale references and both park obliques. Three matched pairs use distinct
2009, 2007 and 2015 Commons photographs. They compare construction types;
the 84.5 px single-wide fit and 100 mm-bound carport lens are disclosed in
the critique, rather than presented as exact photographic replicas.

Remaining weaknesses are the broad new-park grounds and low density,
smooth lawn interiors, repetitive source silhouettes, simplified household
plants and quick window/metal responses. There are no interiors. Causal
sun fade, seam rust, north-wall algae, splash, worn boards and seed-unique
ground marks belong to the next look gate. This checkpoint does not claim
unique baked UV packing/density, structural/civil certification or full-site
motion clearance. No kit or top-level README changes were made.
