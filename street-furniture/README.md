# Rill / street furniture — form checkpoint

An original 1995–2015 American streetscape family: a bus-stop sign, route and
schedule holder; three-sided aluminum/glass shelter with bench, replaceable
poster and lighting hardware; anchored steel-strap bench; flanged pipe U rack
and row; three coin newspaper cabinets and a chained row; blue collection box;
single and twin mechanical meters; slatted litter and recycling receptacles.
Fictional RILL TRANSIT, TOWN POST, The Rill, Daybreak and Town Weekly graphics
are generated with installed open fonts. Every vertex and texel is scripted.

**This is the requested form/construction checkpoint, before look-dev.** The
exports use quick shared colors and graphics. Baked wear, final UV allocation,
material validation, full motion sweeps and final documentation images remain
for the next stage. No finished-asset claim is made by this checkpoint's checks.

[REFERENCE.md](REFERENCE.md) distinguishes published anchors from original
construction estimates. [REVIEW.md](REVIEW.md) records rejected views and the
photo-based critique. [Source credits](refs/SOURCES.md) identify every cached
photo/PDF and its rights. No reference image enters a material.

The regulatory/warning extension lives in
[street-signs/SET_REFERENCE.md](../street-signs/SET_REFERENCE.md). It uses the
2009 MUTCD / 2012 revisions and SHS supplement. The earlier STOP, street blades,
their atlas and all other existing deliveries retain their original bytes.

| Module | Triangles | Measured W × D × H, m | Materials |
| --- | ---: | --- | ---: |
| BusStop | 574 | .4572 × .1130 × 3.0500 | 2 |
| Shelter, including its bench/slab | 7,730 | 4.2672 × 1.8288 × 2.7420 | 2 |
| ShelterMissingPanel | 7,718 | Same exterior envelope | 2 |
| Bench, center arm and anchors | 3,436 | 1.8550 × .6218 × .8050 | 1 |
| BikeRack | 1,052 | .8684 × .1524 × .9144 | 1 |
| BikeRackRow, four U's | 4,208 | .8684 × 2.8956 × .9144 | 1 |
| NewsDaily | 1,578 | .5905 × .6105 × 1.2442 | 2 |
| NewsPedestal | 1,626 | .5616 × .6055 × 1.1660 | 2 |
| NewsWeekly, impact-dented side | 1,814 | .6016 × .6255 × 1.2860 | 2 |
| NewsRow, three independent cabinets | 5,018 | Member roots at −.72 / 0 / +.72 m | 2 shared |
| CollectionBox | 1,152 | .8814 × .7068 × 1.3303 | 1 |
| MeterSingle | 1,426 | .2140 × .2090 × 1.5200 | 2 |
| MeterTwin | 2,870 | .4880 × .2090 × 1.5550 | 2 |
| Litter | 2,966 | .7000 × .7021 × .9600 | 1 |
| Recycling | 2,966 | Same envelope | 1 |

All individual pieces meet the brief's ceilings. Row counts are the sum of
their members, not a single-rack/box budget. Footprints above include chain
posts, handles, flanges and overhanging covers; nominal sheet/cabinet dimensions
are separately listed against their sources. The newspaper cover adds 6 mm
above its nominal cabinet dimension. Glass adds a second material where needed.

`export/StreetFurniture.gltf` is the inspection library. Every named module
also has its own ground-centered `export/<Module>.gltf` and BIN. All reference
the **same canonical external image in `export/textures/`**. The library lays
modules apart for inspection; replace a module root's transform when placing it.
Rows reuse member mesh/image identities. Presentation houses, Ground and cars
are never included in these exports.

Meters, Blender +Z up / −Y front; glTF +Y up / +Z forward. Each module has a
`*_SidewalkSocket` on Ground's **.1524 m** construction grid and named anchor
sockets. Normal props sit at finished-walk grade; the shelter root is its slab
underside and its integrated bench sits .150 m above that root. These are
placement sockets, not terrain displacement or structural footing models.

Moving nodes preserve their actual pivot frames in the glTF extras:

| Mechanism | Local axis and range | Pivot placement |
| --- | --- | --- |
| NewsDoor | X, 0…75° outward/down | Lower front door pin |
| NewsCoinLid | X, −105…0° | Rear edge of upper coin compartment |
| CollectionServiceDoor | Z, −105…0° | Front left service jamb |
| CollectionPullDownChute | X, 0…50° | Chute lower edge, .925 m above root |
| MeterCoinDoor / Twin0CoinDoor / Twin1CoinDoor | Z, −95…0° | Front left edge of vault leaf |
| LitterLid / RecyclingLid | X, −100…0° | Back rim at (0,.31,.86) m |

Exact local coordinates and measured import bounds are in `build/manifest.json`
and `build/check.json`. These checks verify serialization, counts, normals,
external image sharing, bounds and pivot metadata. They do not substitute for
a sampled physical clearance audit. Source details remain parameterized in
`src/pieces.py`; the seed changes paper headlines, flag states and a missing
shelter pane. The weekly cabinet has one localized handling dent.

Planned final textures, held until the form is reviewed:

| Shared set | Planned runtime allocation, full mips at 8 bpp |
| --- | ---: |
| Furniture 2048² BaseColor / OpenGL Normal / ORM, baked at 4096 | 16 MiB |
| Fictional graphics 1024² RGBA, all papers/labels/posters/flags | 1⅓ MiB |
| Added signs 2048² face sheet | 5⅓ MiB |
| **Both new families together** | **22⅔ MiB** |

The proposed two-material furniture delivery uses one opaque atlas plus a
graphics/glazing state. Reserved graphics/glass cells can use ORM red as the
transmission mask in that second state, which omits the opaque AO binding;
green still supplies roughness. This is a proposed stock-glTF packing to
validate after the gate, not implemented look-dev. No set per seed or per box.
The quick checkpoint currently shares one 2048 color image; glass is scalar.
PNG/BIN disk bytes differ from compressed GPU memory.

Next-stage wear will follow causes: upper exposure/chalking, fold and door-edge
chips, weld/anchor corrosion, low splash, hand/pull and foot contact grime,
limited original stickers/tags and retained pane damage. It must survive the
bake at player distance. Uniform noise dirt is not an acceptable substitute.

```sh
make                          # rebuild form exports, Cycles views, photo pairs, checks/contact
make check                    # raw/import budgets, bounds, pivots, repo and preservation receipt
make match                    # three calibrated used-object comparisons, no texture input
make repeat                   # rebuild both additions; compare every external delivery byte
make -C ../street-signs set-check
```

Requires installed Blender 5.2, Python/Pillow/NumPy, fontconfig/DejaVu and flock.
Cycles uses the shared kit GPU lock and OptiX/CUDA. `renders/checkpoint/`
contains the 1.65 m / 40 mm raking-sun street hero, complete module lineup,
regulatory and warning lineups, face/back/base details, frame/bench, heads,
boxes, collection box, racks, receptacles and pole-band bracket; `contact.jpg` includes all
checkpoint views plus the three photo pairs from `renders/match/`.
Every image receipt hashes its actual external glTF inputs and context.

The main remaining weaknesses are flat quick materials, no finished weathering,
pinched/faceted meter casting around its cuts, approximated meter/coin internals
and the differences between the original
constructions and photographed models. The meter reference is a later card
conversion; the pedestal reference is a free-paper rack, so neither establishes
our mechanism design. Camera-fit residuals are reported openly. No kit change
or new software installation is required.

Checkpoint verification: `make`, `make check`, the sign `set-check`, receipt
validation and `make repeat` pass. Rebuilding both additions reproduces all
86 external delivery files / 8,015,914 bytes exactly. Baseline hashes of 459
preexisting delivery files still match, including the earlier signs.
The furniture library glTF/BIN/PNG are 62,226 / 1,983,288 / 523,460 bytes;
individual modules share that PNG. These are quick checkpoint allocations,
not finished optimized texture or motion-clearance results.

[Street hero](renders/checkpoint/hero.png) · [Full contact sheet](renders/checkpoint/contact.jpg) · [Photo pairs](renders/match/)
