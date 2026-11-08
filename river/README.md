# River / county road crossings

**Form and construction checkpoint; quick PBR, before final look-dev.**
An original scripted river reach and a parameterized prestressed-girder road
bridge, assembled into two different American town settings with period
infrastructure and the library's native vehicle context.
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
Runs are about 1.05m deep, the riffle about .37m, and the outer pool about 2.1m
(the exported vertex-depth maximum is 2.04m).
Bankfull and normal water are separate; the natural floodplain is about 2.15m
above water. Published sources and authored choices are separated in
[REFERENCE.md](REFERENCE.md); all viewed/downloaded rights and exact uses are
in [SOURCES.md](refs/SOURCES.md).

Five **AASHTO Type III** girders per span use the FDOT 20130 section:
45in depth, 16in top, 22in bottom and 7in web. They have modest camber,
haunches, diaphragms, concrete plinths, steel seating plates and elastomer pads.
Their exterior centers are .95m in from the deck edges. The wall cutwater
follows local flow while its cap stays transverse to the road.
Abutments have projecting seats, backwalls and wingwalls; approach slabs carry the road
onto fill. Deck panels carry a 2% crown, two 11ft lanes, raised walks, 32in
parapets, expansion gaps/seals, drains and supported utility conduits.
The W-beam approaches retain sheet gauge, blockouts, posts and generic terminals.
Plaques name a fictional county crossing. This is visual construction, not a
load-rated bridge or a hydraulic design.

## Generator and game interface

`src/plan.py` is Blender independent. `generate(seed, **changes)` returns an
immutable `Plan`: kind, reach length, channel width, bend amplitude/phase,
bar and riffle stations, span count (2–4), span length (12–27m), deck width (10–14m),
deck elevation, pier type and construction year. The two defaults change the
channel and site plans, rather than recoloring one composition.
Their bend amplitudes are −7m / +15m, with different phases and bar/riffle stations.

Meters, +Z up; river flow +Y; bridge station +X. glTF converts positions to
`(x,z,-y)`. Whole-crossing roots are at the crossing center on normal-water
datum. Module exports are locally centered and can be placed independently.
The inspection library arranges them on a sheet; reset its display transforms
before placing those roots into a new bridge.

- Girder `W/E` sockets mark the bearing centers, .26m in from each end;
  their flat seats meet the elastomer pads.
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
Bridge concrete and galvanized parts use the landed freeway family's 2048
Concrete and 1024 Zinc sets: 16MiB + 4MiB at 8bpp with full mips. Those images
are shared external dependencies, not duplicate river allocations.
Native trees and buildings retain their original library images. Bank/bed has
one temporary original 1024 triple; a 512 bank-card image also contains the
tiny plaque legends; water has one original tiling 512 normal. That is
**4⅔ MiB new** at 8bpp with full mips. Final intent is a shared 2048 bank/bed
triple (16MiB), the same card image (⅓MiB) and a 1024 water normal (1⅓MiB).
After freeway landed, `main` was merged at `dcc2132`. The small adapter in
`src/freeway_bridge.py` calls its original girder, three-column bent, F-barrier,
guardrail/terminal and bearing factories in an isolated module namespace.
It substitutes the cited Type III section for freeway's larger Type IV,
adapts cap span/height while preserving round 1.2m columns, and scales the
native bearing layers to this bridge. It does not edit the freeway sources
or canonical deliveries. The local deck, wall pier and abutment retain this
crossing's dimensions and construction.

Cycles uses imported transmission/IOR, the shipped normal and uniform river
absorption/scattering extras. The coefficients in inverse meters are absorption
`(.35, .315, .56)` and scattering `(.105, .1085, .0385)`, with HG anisotropy `.2`.
Stock glTF cannot carry the Blender volume node graph; the renderer reconstructs
one Volume Coefficients node from those extras.
An engine must implement the same depth absorption and flow. Quick bank
fields and coarse placed maintenance remain provisional, not final baked art.
The water continues to ±800m as one closed medium over a submerged bed.
Internal closing planes are removed and their boundary vertices welded so
they cannot refract as artificial dams. The water object's extras distinguish
the 300m core from that presentation extension for engine clipping/streaming.
The measured water triangle count includes the extension; distant terrain,
houses and trees remain separately removable presentation objects.

<!-- measured-costs:start -->
| Piece | Triangles |
| --- | ---: |
| TypeIII_Girder18 | 696 |
| DeckPanel6 | 260 |
| Parapet6 | 52 |
| PierColumns | 712 |
| PierWall | 226 |
| Abutment | 112 |
| GuardrailTerminal | 404 |

Flat panels intentionally stay below 300 triangles; no subdivisions are added for a minimum.

| Assembled mesh type | Downtown count × max triangles | Edge count × max triangles |
| --- | ---: | ---: |
| Abutment | 2 × 112 | 2 × 112 |
| ApproachRail | 4 × 404 | 4 × 404 |
| ApproachSlab | 2 × 12 | 2 × 12 |
| BearingStation | 4 × 396 | 3 × 396 |
| DateAndNamePlaques | 1 × 14 | 1 × 14 |
| Deck | 9 × 285 | 6 × 264 |
| Girder | 15 × 696 | 10 × 696 |
| Parapet | 36 × 28 | 24 × 28 |
| ParapetLightPedestals | 1 × 48 | — |
| Pier | 4 × 676 | 1 × 226 |
| Span DiaphragmsHaunches | 3 × 204 | 2 × 204 |
| Span DrainConduit | 3 × 1,024 | 2 × 1,024 |

| Seed | Bridge | Bed / banks | Water | Site | Vegetation | Cars | Town / people | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 21,581 | 68,434 | 31,480 | 40,452 | 1,648,008 | 561,418 | 1,133,488 | 3,504,861 |
| 202 | 14,228 | 61,670 | 31,480 | 760 | 3,458,188 | 388,674 | 1,020,568 | 4,975,568 |

| Seed | glTF + BIN bytes | Material states / unbatched placed draws |
| --- | ---: | ---: |
| 101 | 51,383,741 | 70 / 3894 |
| 202 | 40,436,559 | 40 / 6091 |

Both crossings share 41 unique image payloads, estimated **168.67 MiB** at 8bpp with full mips. PNG dependency bytes and uncompressed residency differ. These totals include native context; the new river-only allocation is listed above.
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
girder/pad and plinth/support contacts, light-base seating, rail feet in soil,
alley paving over its supporting terrace, walk clearance, building/walk bounds
and reach measurements. Tiling UV reuse is intentional;
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

Heroes use 40mm lenses, eye-height bank/trail cameras and a procedural clear
23° sun at −.4EV. Underside inspections adapt exposure to the shade; every
frame records its camera, exposure and exact glTF/image bundle hash.
The three final comparisons use Raisin's town bridge (2008), the Huron bridge
underside (2013) and a Huron bank/water stretch (2008). White-balance assumptions,
fit residuals and the different structures/seasons remain visible. They are
reference comparisons, not reconstructions or dimensional surveys.
