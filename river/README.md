# River / county road crossings

**Form and construction checkpoint; quick PBR, before final look-dev.**
An original scripted river reach and a parameterized prestressed-girder road
bridge, assembled into two different American town settings in 2010.
No final texture bake or gallery JPGs are delivered in this round.

Local exported Cycles views: [downtown hero](renders/checkpoint/101/hero.png),
[edge hero](renders/checkpoint/202/hero.png),
[complete contact](renders/checkpoint/contact.jpg),
[photo comparisons](renders/checkpoint-matches/contact.jpg).
All presentation imports external-image glTF. Embedded GLBs are inspection
mirrors under `build/embedded/`, never the scene's high-detail source.

## Places and dimensions

| Seed | 101 / Cedar Run downtown | 202 / county edge |
| --- | --- | --- |
| Reach / nominal normal-flow width | 300m / 100ft, 30.480m | 300m / 120ft, 36.576m |
| Bridge / construction year | Three 60ft spans, 54.864m / 1974 | Two 80ft spans, 48.768m / 1968 |
| Out-to-out width | 39ft / 11.8872m | 35ft / 10.668m |
| Main supports | Three-column bents | Rounded-nose wall pier |
| Place | Low floodable riverwalk, floodwall and brick Main Street backs | Natural banks, gravel bar, launch/fishing access, fields and houses |

Normal width varies along the reach, and the bar narrows the low-flow surface.
Runs are about 1.05m deep, the riffle about .37m, the outer pool about 2.2m.
Bankfull and normal water are separate; the natural floodplain is about 2.15m
above water. Published sources and authored choices are separated in
[REFERENCE.md](REFERENCE.md); all viewed/downloaded rights and exact uses are
in [SOURCES.md](refs/SOURCES.md).

Five original **AASHTO Type III** girders per span use the FDOT 20130 section:
45in depth, 16in top, 22in bottom and 7in web. They have modest camber,
haunches, diaphragms, concrete plinths, elastomer pads and steel sole plates.
Abutments have seats, backwalls and wingwalls; approach slabs carry the road
onto fill. Deck panels carry a 2% crown, two 11ft lanes, raised walks, 32in
parapets, expansion gaps/seals, drains and supported utility conduits.
The W-beam approaches retain sheet gauge, blockouts, posts and generic terminals.
Plaques name a fictional county crossing. This is visual construction, not a
load-rated bridge or a hydraulic design.

## Generator and game interface

`src/plan.py` is Blender independent. `generate(seed, **changes)` returns an
immutable `Plan`: kind, reach length, channel width, bend amplitude/phase,
bar and riffle stations, span count (2–4), span length (12–27m), deck width,
deck elevation, pier type and construction year. The two defaults change the
channel and site plans, rather than recoloring one composition.

Meters, +Z up; river flow +Y; bridge station +X. glTF converts positions to
`(x,z,-y)`. Whole-crossing roots are at the crossing center on normal-water
datum. Module exports are locally centered and can be placed independently.
The inspection library arranges them on a sheet; reset its display transforms
before placing those roots into a new bridge.

- Girder `W/E` bearing sockets mark each end.
- `Lane_*`, `Sidewalk_*`, `RiverbankTrail` and `FlowCenterline` retain sampled
  paths in `points_blender_m` / `points_gltf_m` extras. Samples are local to
  the identity path root; do not add its translation again.
- `_FLOW` on the water is a float3 custom vertex attribute: Blender-frame
  horizontal velocity X/Y in m/s, then depth in m. It is data, not albedo.
  Convert velocity `(vx,vy)` to glTF `(vx,0,-vy)` in an engine shader. The river
  normal repeats over 2m. There is no frozen flow animation.
- `FishingSpot` / `BoatLaunch` are gameplay sockets on the rural bank.

Load `export/RiverCrossing-101.gltf` or `RiverCrossing-202.gltf` with its BIN
and preserve relative image URIs. `export/RiverModules.gltf` and the seven
`export/pieces/*.gltf` provide reusable construction. Context/traffic/native
vegetation are named and costed separately for removal, batching and engine LOD.

## Materials and checkpoint cost

Ground's Asphalt, Concrete, Lawn and GroundTrim are reused without changes.
Native trees and buildings retain their original library images. Bank/bed has
one temporary original 1024 triple; a 512 bank-card image also contains the
tiny plaque legends; water has one original tiling 512 normal. That is
**4⅔ MiB new** at 8bpp with full mips. Final intent is a shared 2048 bank/bed
triple (16MiB), the same card image (⅓MiB) and a 1024 water normal (1⅓MiB).
The freeway has not landed on main; none of its unmerged code/maps is copied.
Future concrete reuse is isolated behind the material role and beam interface.

Cycles uses imported transmission/IOR, the shipped normal and uniform river
absorption extras. Stock glTF cannot carry the Blender volume node graph;
the renderer reconstructs that uniform volume response from those extras.
An engine must implement the same depth absorption and flow. Quick bank
fields and coarse placed maintenance remain provisional, not final baked art.

<!-- measured-costs:start -->
| Piece | Triangles |
| --- | ---: |
| TypeIII_Girder18 | 360 |
| DeckPanel6 | 260 |
| Parapet6 | 52 |
| PierColumns | 340 |
| PierWall | 226 |
| Abutment | 100 |
| GuardrailTerminal | 428 |

Flat panels intentionally stay below 300 triangles; no subdivisions are added for a minimum.

| Assembled mesh type | Downtown count × max triangles | Edge count × max triangles |
| --- | ---: | ---: |
| Abutment | 2 × 100 | 2 × 100 |
| ApproachRail | 4 × 428 | 4 × 428 |
| ApproachSlab | 2 × 12 | 2 × 12 |
| BearingStation | 4 × 396 | 3 × 396 |
| DateAndNamePlaques | 1 × 14 | 1 × 14 |
| Deck | 9 × 285 | 6 × 264 |
| Girder | 15 × 360 | 10 × 360 |
| Parapet | 18 × 52 | 12 × 52 |
| Pier | 2 × 340 | 1 × 226 |
| Span DiaphragmsHaunches | 3 × 204 | 2 × 204 |
| Span DrainConduit | 3 × 1,024 | 2 × 1,024 |

| Seed | Bridge | Bed / banks | Water | Site | Vegetation | Cars | Town / people | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 15,821 | 67,438 | 20,560 | 11,592 | 1,935,154 | 561,418 | 826,816 | 3,438,799 |
| 202 | 10,940 | 60,470 | 20,560 | 760 | 2,664,858 | 388,674 | 719,352 | 3,865,614 |

| Seed | glTF + BIN bytes | Material states / unbatched placed draws |
| --- | ---: | ---: |
| 101 | 41,570,069 | 69 / 2609 |
| 202 | 33,676,544 | 39 / 4721 |

Both crossings share 35 unique image payloads, estimated **148.67 MiB** at 8bpp with full mips. PNG dependency bytes and uncompressed residency differ. These totals include native context; the new river-only allocation is listed above.
<!-- measured-costs:end -->

## Rebuild and evidence

```sh
make                         # native inputs, refs, sources, glTF, check, Cycles, pairs/contact
make check                   # raw attributes, fresh import, actual bearing contacts, preservation
make repeat                  # exact CPU fields / geometry / manifests; excludes blend containers
make render WIDTH=1280 SAMPLES=32
make clean && make           # remove only this family's generated products and rebuild
```

Blender 5.2, installed Python/Pillow/NumPy/fonts and flock are required.
Only missing original library resources are built through their native targets;
existing deliveries are read-only. A serial render batch holds the kit GPU
lock once. All scratch and downloaded references stay in ignored folders.

`build/check.json` separates accessor/import preservation from actual sampled
girder/pad contacts and reach measurements. Tiling UV reuse is intentional;
finite UVs and density are measured, not a unique lightmap/atlas certification.
`build/preservation.json` fingerprints every pre-existing delivery input.
`build/repeat.json` records the exact deterministic rebuild comparison.
The critique log is [REVIEW.md](REVIEW.md). No kit or top-level index change.

All trees are native red maples and pin oaks; no new willow species is made.
Native school context caches retain original house, car, bench and light forms
with quick materials; they are presentation resources, not new canonical
deliveries. Native street-signs supply approach speed signs. Full appearance,
fine causal weathering, collisions/LOD and final game performance remain for
later stages after the lead's form review.
