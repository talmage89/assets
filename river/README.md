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
Runs are about 1.05m deep, the riffle about .19m, and the outer pool about 2.1m
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
Their bend parameters remain −7m / +15m, with different phases and bar/riffle stations.
Downtown's positive-station bend broadens progressively to 1.95 times its
parameter; its approach/hero reach retains the original centerline.

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
  normal follows current-aligned UVs. Material extras specify continuous
  speed-to-normal/roughness ranges, evaluated from this exported attribute
  by the Cycles adapter and intended engine water shader. Stock glTF retains
  a constant PBR fallback. Sheltered curling wakes are analytic game data,
  rather than a fluid simulation. There is no flow animation.
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
The export renderer reuses freeway's thin-leaf response adapter on the
imported native foliage maps; it does not load high-detail vegetation sources.
After freeway landed, `main` was merged at `dcc2132`. The small adapter in
`src/freeway_bridge.py` calls its original girder, three-column bent, F-barrier,
guardrail/terminal and bearing factories in an isolated module namespace.
It substitutes the cited Type III section for freeway's larger Type IV,
adapts cap span/height while preserving round 1.2m columns, and scales the
native bearing layers to this bridge. Added sole plates, keeper angles,
anchor nuts and pad laminations retain the accepted stack's seat/top datums.
It does not edit the freeway sources
or canonical deliveries. The local deck, wall pier and abutment retain this
crossing's dimensions and construction.

Cycles uses imported transmission/IOR, the shipped normal and uniform river
absorption/scattering extras. The coefficients in inverse meters are absorption
`(.806, .8525, 1.2555)` and scattering `(1.4, 1.6, .7)`, with HG anisotropy `.2`.
Stock glTF cannot carry the Blender volume node graph; the renderer reconstructs
one Volume Coefficients node from those extras.
An engine must implement the same depth absorption and flow. The existing
512 card sheet also carries original soft runoff, salt, repair and paint-over
masks. No new image allocation is added for weather. These checkpoint fields
remain provisional, rather than a final high-source normal bake.
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
| BearingStation | 4 × 3,636 | 3 × 3,636 |
| DateAndNamePlaques | 1 × 14 | 1 × 14 |
| Deck | 9 × 285 | 6 × 264 |
| Girder | 15 × 696 | 10 × 696 |
| Parapet | 36 × 28 | 24 × 28 |
| ParapetLightPedestals | 1 × 48 | — |
| Pier | 4 × 676 | 1 × 226 |
| Span DiaphragmsHaunches | 3 × 204 | 2 × 204 |
| Span DrainConduit | 3 × 1,024 | 2 × 1,024 |
| TextureDrivenBridgeAge | 1 × 1,068 | 1 × 420 |

| Seed | Bridge | Bed / banks | Water | Site | Vegetation | Cars | Town / people | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 32,369 | 54,667 | 35,730 | 55,366 | 5,687,834 | 820,534 | 2,478,730 | 9,165,230 |
| 202 | 21,128 | 50,452 | 35,655 | 798 | 14,928,480 | 388,674 | 1,074,960 | 16,500,147 |

| Seed | glTF + BIN bytes | Material states / unbatched placed draws |
| --- | ---: | ---: |
| 101 | 367,046,626 | 969 / 8208 |
| 202 | 41,053,520 | 53 / 21241 |

Both crossings share 44 unique image payloads, estimated **172.67 MiB** at 8bpp with full mips. PNG dependency bytes and uncompressed residency differ. These totals include native context; the new river-only allocation is listed above.
<!-- measured-costs:end -->

## Rebuild and evidence

```sh
make                         # native inputs, refs, sources, glTF, check, Cycles, pairs/contact
make check                   # raw attributes, fresh import, actual bearing contacts, preservation
make repeat                  # exact geometry/manifests and image identity; excludes blend containers
make render WIDTH=1280 SAMPLES=32
make clean && make           # remove only this family's generated products and rebuild
```

Blender 5.2, installed Python/Pillow/NumPy/fonts and flock are required.
Only missing original library resources are built through their native targets;
existing deliveries are read-only. A serial render batch holds the kit GPU
lock once. All scratch and downloaded references stay in ignored folders.

`build/check.json` separates accessor/import preservation from actual sampled
girder/pad and plinth/support contacts, light-base seating, rail feet in soil,
alley paving over its supporting terrace, walk clearance, building/walk bounds,
crop material continuity across cell diagonals and reach measurements. Tiling UV reuse is intentional;
finite UVs and density are measured, not a unique lightmap/atlas certification.
`build/preservation.json` fingerprints every pre-existing delivery input.
`build/repeat.json` records the exact deterministic rebuild comparison.
The five original CPU images were also regenerated separately with identical
SHA-256 hashes; that receipt is `build/texture-repeat.json`.
The critique log is [REVIEW.md](REVIEW.md). No kit or top-level index change.
The regenerated [checkpoint report](build/checkpoint-report.md) links every
requested fix to its views and lists per-piece/category memory and mesh reuse.
Imported `_GROUND_TIP` attributes mark all buried rail-post ends for actual
surface-contact checks; the rail profile and upper datum remain unchanged.

All trees are native red maples and pin oaks; no new willow species is made.
Native school context caches retain original house, car, bench, light,
boxwood and utility forms
with quick materials; they are presentation resources, not new canonical
deliveries. Native street-signs supply approach speed signs. Full appearance,
fine causal weathering, collisions/LOD and final game performance remain for
later stages after the lead's form review.

The downtown uses 160 distinct native buildings generated in this family's
build directory through downtown's validated JSON-plan interface. Eight long
frontages combine native parameter draws from Midwest, Northeast and Western
styles. End corners have two storeys to stay within the native per-building
caps; interior three-storey elevations remain. Native rear walls, additions,
service doors and fire escapes face the river alleys; dumpsters and rear
parking occupy their working space. Four rows meet the river and four face
them across Main Street. Lots beyond the reach continue the crossing street;
distinct canonical buildings continue the town beyond the core. Rural context
adds dense linked maples and low, broad boxwood clumps,
hay swaths, field wire, occupied yards/drives, roadside ditches and utility
conductors with sag. Hay rows are material assignments on the terrain itself;
the outer continuation starts at its actual boundary. Bank colonies share
sixteen six-triangle meshes.
`build/resources.json` measures stored/placed triangles, mesh instances and
shared images per category and module. Engine instance batching is still
required; the authored scene graph is not a frame-rate claim.

Heroes use 40mm lenses, eye-height bank/trail cameras and a procedural clear
18° warm sun at −.4EV. Underside inspections adapt exposure to the shade; every
frame records its camera, exposure and exact glTF/image bundle hash.
The three comparisons use Raisin's town bridge (2008), FHWA's South Carolina
concrete I-beam underside (2008) and a Huron bank/water stretch (2008). White-balance assumptions,
fit residuals and the different structures/seasons remain visible. They are
reference comparisons, not reconstructions or dimensional surveys.
Same-camera handoff/revised panels, at 1280 pixels per side, are under
`renders/fixes/`; changed inspection cameras use a reconstructed accepted
`9b1c8bc` export and lighting rendered with the identical revised camera.
`build/fix-evidence.json` retains image/camera/bundle
hashes. No docs images or README gallery are added at this checkpoint.
Baseline eye clearances are measured on the imported accepted terrain in
`build/baseline-clearance-101.json` and `baseline-clearance-202.json`.
Both sides of every comparison must also pass the near-black image gate;
the downtown riffle camera clears both versions of its shifted bank.
