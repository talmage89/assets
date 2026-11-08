# Manufactured home communities — dense parks and look-dev checkpoint

An original, script-built family for an American town of 1995–2015. Alder
Court is a compact older through-street community; Meadow Bend is a roomier
1990s loop with double-wides, a clubhouse and a playground. The home, lot,
addition and street grammar is reusable independently of either example.

**This stops before final documentation.** One new manufactured-finish set
is GPU-baked at 4096 and shipped at 2048. It combines with the native house,
ground and prop sets; seeded mesh colors carry broad exposure and upkeep.
The delivery remains exterior-only, without interiors or collision meshes.
No `docs/` images or final gallery are produced at this gate. Image critiques
and their remaining weaknesses are recorded in [REVIEW.md](REVIEW.md).

The latest completion gate is **rejected**: sparse rust and a level street
camera have improved, but the older hero still looks too clean and the lawn
clumps expose their cards. Current 1440 px evidence is in
`renders/finish-pass4/`; same-camera crops are in `renders/finish-fixes/`.
The final view set, gallery and docs remain withheld.

`make` regenerates the ignored checkpoint evidence. `build/metrics.md`
contains the complete six-home, 69-lot, module and park budget tables;
render receipts keep presentation cars, vegetation and town separate.

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
| SingleWide-120 | 1972 | 12 × 60 | 3.6576 × 18.2880 | 31,387 | 4 | 2.332 |
| SingleWide-147 | 1984 | 14 × 70 | 4.2672 × 21.3360 | 28,675 | 5 | 1.968 |
| SingleWide-168 | 1984 | 16 × 80 | 4.8768 × 24.3840 | 34,219 | 5 | 2.375 |
| DoubleWide-245 | 1996 | 24 × 52 | 7.3152 × 15.8496 | 28,130 | 5 | 2.103 |
| DoubleWide-228 | 1996 | 28 × 60 | 8.5344 × 18.2880 | 30,737 | 5 | 2.282 |
| DoubleWide-326 | 1996 | 32 × 64 | 9.7536 × 19.5072 | 32,676 | 5 | 2.458 |

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
  Fine skirt and siding ribs use the manufactured normal sheet; tracks,
  openings, loose panels and silhouette bends remain geometry.

## Modules and native reuse

| New component | Principal dimensions / construction | Triangles | Materials |
| --- | --- | ---: | ---: |
| Deck | 3.6576 × 2.1336 m proof module; 3.048/4.2672 m width variants; cupped boards, beams, joists, 88.9 mm posts | 1,696 | 2 |
| Carport | 6.7056 × 3.3528 m; 2.42–2.68 m roof, hollow 76.2 mm posts, folded 0.8 mm pans, independently supported | 2,828 | 1 |
| UtilityService | Meter, breaker, conduit, water valve and sewer cleanout; three actual connection sockets | 508 | 2 |
| PropaneBottles | Two unbranded 100 lb class cylinders; 378 mm diameter, 1.206 m above pad per Manchester specification | 796 | 1 |
| Condenser | 0.98 m pad, housing, grille and short line set | 744 | 1 |
| WindowAC | 0.58 × 0.55 × 0.38 m housing with support brackets | 212 | 1 |
| SatelliteDish | Spun concave pan, mounting post and feed arm | 276 | 1 |
| AddedRoom | 3.2 × 2.4 m, independent piers, 2.95–3.20 m roof, real sash opening and removable skirt | 672 | 4 |
| Household | Two pots, procedural leaves and small ride-on toy | 432 | 1 |
| EntranceSign | 2.9 m fictional sign on timber posts; open-license lettering | 685 | 2 |
| SupportFrame | Unskirted single-wide chassis/pier inspection assembly | 4,036 | 2 |
| Modules sheet | Add-ons with labels; inspection assembly, not one prop budget | 11,491 | 4 |
| HomeForms sheet | All six bodies and labels; inspection assembly | 187,770 | 6 |

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

| Park | Homes | Ground envelope, m | Lot, ft / sq ft | Street | Placed / unique triangles | Materials | glTF + BIN, MiB |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| 101 / Alder Court, 1968 plan | 36 | 149.304 × 107.7824 | 32 × 110 / 3,520 | 20 ft / 6.096 m through lanes | 2,561,040 / 992,616 | 32 | 70.250 |
| 202 / Meadow Bend, 1994 plan | 33 | 133.4544 × 173.6192 | 56 × 95 / 5,320 | 24 ft / 7.3152 m rounded loop | 2,263,954 / 941,240 | 36 | 66.311 |

Counts include home bodies, decks, carports, native props, facilities,
private ground/roads, small edge plants and service infrastructure. Cars,
large trees and shrubs are
**placement sockets**, not meshes duplicated into the park packages. Render
provenance reports their actual instantiated triangles separately from the
park, neighboring buildings and public streets. Unique totals count each
distinct exported mesh once; placed totals count every instance. Eight
seeded home profiles per park, with two solar orientations, share linked
mesh data; repeated carports, ACs, dishes and other add-ons also share data.

Presentation context is measured after importing the native assets, with
placed and unique totals for cars, vegetation, town architecture and public
streets in `build/metrics.md` and each pass's `provenance.json`. Factory
paint, parking offsets and angles vary independently of native body choice. A game can populate or
cull the exported sockets without loading this presentation neighborhood.

The older 3,520 sq ft lots use the narrower end of
[HUD's 2000 builder guide](https://inspectapedia.com/Manufactured_Homes/HUD-Home-Builders-Guide-to-Manufactured-Housing.pdf),
Appendix D pp. 63–66: some surveyed communities allowed 3,500 sq ft and
frontages down to 20 ft, although 40–50 ft was more common. Its 10–20 ft
home-separation range informs this compact plan. The modern survey is a
construction comparator, without a claim of historical local approval.
The 20 ft older lane and 24 ft newer road comparators remain unchanged.
Fresh raw-mesh home-envelope separations are **4.246–4.616 m** in Alder
Court and **6.172–10.418 m** in Meadow Bend, including awnings and eaves.
These are measured physical gaps, not statutory setbacks.

Both parks use four rows. Alder Court has two connected through lanes;
Meadow Bend has a loop and three reserved common lots. Gross densities,
including common land, are **9.053 / 5.764 homes per acre** for old/new.
The complete per-lot tables in `build/metrics.md` name every template,
occupant seed, era, dimensions, home cost, placed lot cost and unique lot
cost. They exclude cars and large vegetation while including fixed native
props, small edge plants and local flatwork. Current lot ranges:

| Park | Lot placed triangles | Referenced geometry buffer bytes | Shared PNG bytes | Shared GPU MiB |
| --- | ---: | ---: | ---: | ---: |
| Alder Court | 48,385–80,143 | 3,166,874–5,320,994 | 33,544,097–52,832,240 | 88–112 |
| Meadow Bend | 46,107–76,470 | 3,157,100–5,077,048 | 45,561,332–64,849,475 | 104–128 |

Each lot references shared meshes and maps inside its park. These are subtree
resources, not standalone lot file sizes or allocations to sum across lots.
The six inspection homes bind 32 / 48 / 48 / 52 / 52 / 52 MiB respectively;
the static parks bind 160 / 176.042 MiB. Cache shared images once.

Office, clubhouse and laundry assemblies, their entry decks, signs, cluster
mail, dumpster enclosure, visitor parking, common walks and playground are
included in whole-park counts. Native pole sockets support sagging overhead
conductors; individual lot service connections route below grade to risers.
The schematic dumpster and pot foliage remain simpler than the home and
deck construction. Component budgets are measured in each park's JSON
`assemblies` table rather than repeated here as stale constants.

## Generator and game connections

`src/plans.py` has no Blender dependency. `home(seed, era, width_ft,
length_ft)` accepts eras `1972`, `1984`, `1996`, widths 12/14/16 or
24/28/32 ft and the bounded length choices 52/56/60/64/70/76/80 ft.
The seed chooses siding, color, roof, porch width, carport, independent
room, AC type, propane, dish, missing panel, tarp, sag and upkeep label.
Upkeep and exposure drive finish color and caused weather. `park(seed,
kind, rows)` uses `old`/`new` and 8–10 lots per row, default nine. Home
profiles are reused through linked mesh instances; occupant dressing and
plant placement have independent deterministic random streams.
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

The exported parks also pass **1,365 static assembly-pair checks** between
separate lots and common facilities, plus deck/carport mesh checks.
These are rest-pose mesh/marker checks, not swept vehicle clearance. The
placement audit moves sheds behind the tightly packed older homes and
keeps their utilities clear of neighboring rear landings and fences.

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

The static image union across both park packages is **176.042 MiB**,
estimated at 8 bits/texel block compression with full mipmaps: 124.042 MiB
of native Ground/fence/patio/grill/mailbox/cart/chain-link/playground maps,
36 MiB of Houses Siding/Shingles/Trim, and the new 16 MiB Manufactured set.
The parks share these images; canonical URI caching avoids a second
allocation. Cars, large trees and town context add native resources whose
render dependencies are recorded separately. PNG disk size, uncompressed
runtime allocation and this block-compression estimate differ.

The **one new shared set** contains 2048 BaseColor (sRGB), OpenGL +Y Normal
and ORM (occlusion/roughness/metallic), **6,429,664 PNG bytes** in total.
Our scripts create every field, bake it at 4096 using Cycles GPU, then
downsample to shipping resolution. Atlas cells encode ribbed metal siding,
rolled roofing, skirt, chassis steel, pier concrete, aluminum carport and
hardware. Sparse fastener runoff, sheltered damp, grade splash and the garden's
four clipped-blade variants occupy guarded cells in that same set. Coverage
is analytic: GPU-bake RGB/normal/ORM first, then pack the original alpha field
without premultiplying paint color. No reference pixels enter the atlas.
Broad seeded exposure and caused wear multiply these fields via
standard glTF `COLOR_0`; they are not projected photographs. Repeated
meter-scale UVs intentionally overlap within their material cells, with
guard texels. This is a shared tiling atlas, not a unique lightmap unwrap.
Homes use four or five materials including inherited shingles, siding,
wood and glazing. The older homes add one blended weather state using the
same atlas; it adds no maps. Whole-park native material counts are larger. The
unbatched primitive counts and unique mesh counts remain explicit in
`build/metrics.md`; linked mesh reuse does not itself promise one draw call.

## Rebuild and proof

Blender 5.2 and the repository's existing Python tools are required. No
packages, scripts or binaries are downloaded. From this folder:

```sh
make                         # references, models, checks, locked Cycles set, pairs, contacts
make check                   # raw export, sampled dimensions, re-import, home door sweeps, repo rules
make repeat                  # regenerate packages and compare bytes with cached native inputs
make check-texture-repeat    # regenerate fields, locked GPU rebake, kit tolerance + exact coverage
make model OLD_SEED=303 NEW_SEED=404 ROWS=9
make render PASS=preview WIDTH=1000 SAMPLES=16
make check-preservation
```

Alternate seeds rebuild the grammar. The photo-calibrated cameras and
published comparisons target the supplied 101/202 examples.

Historical before/after evidence uses the supplied earlier checkpoint cache:
`make baseline` freezes its six packages before `make repeat` replaces that
cache. When present, `build/baseline/export/` enables the additional renders
and identical-camera/light comparison sheets automatically. The historical
geometry and image payloads are SHA-checked; only image URIs relocate.
This optional historical input is separate from rebuilding the current
family from scripts. No previous asset package is substituted for a current
delivery, and the comparisons remain ignored review images.

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
| `build/preserved*.json` | SHA-256 baselines for 1,212 pre-existing delivery/image files; all unchanged |
| `build/look-check.json` | Atlas-cell containment, finite UVs, image resources, density and instance audits |
| `build/metrics.md` | Every home, lot and module; unique/placed park and presentation counts; image memory |
| `renders/checkpoint/<pass>/provenance.json` | Fresh embedded GLB imports, source/image hashes, cameras, light and actual context triangles |
| `renders/checkpoint/<pass>/sources/` | Exact embedded GLBs used by that pass, retaining its original baked images |
| `renders/checkpoint/<pass>/tonal-report.json` | Percentiles and near-clip fractions; supports visual judgement, not albedo certification |
| `renders/checkpoint/<pass>/source-verification.json` | Archived GLB and referenced image SHA-256 receipts |
| `renders/checkpoint/<pass>/matches/` | Three construction pairs plus a supplementary newer-lane pair; neutral balance, anchor overlays and residuals |

Heroes are perspective views from 1.68 m at 40 mm under a procedural clear
sky and 18° raking sun. The complete set also includes turnarounds,
skirting, opened entry, exposed frame/piers, module details, scale references
and both park obliques. Comparisons use the 2009 used home, 2015 aerial and
2024 straight-lane Commons photographs. The 2007 photo remains an age reference;
its curved apron could not fit a level older-lane camera below 20 px RMS.
The replacement inside Alder Court uses zero pitch/roll and lens rise;
its road depths are inferred. RMS is **18.43 / 11.53 / 16.65 / 8.53 native
pixels** for the used home, older lane, aerial and newer lane. The single-lot camera is inferred
low without a height prior; the aerial reaches its 100 mm crop-lens bound.
Neither fit proves that this fictional park reproduces a photographed site.
Neutral patches are identified and balanced in linear RGB before comparing
values. The final critique records what still reads as CG.

There are no interiors. This checkpoint does not claim structural/civil
certification, unique lightmap packing, full-site motion clearance or final
draw-call batching. Native shed/pole/playground adapters, household plants
and the schematic dumpster remain less developed than the homes. No kit,
top-level README or final docs images are changed.
