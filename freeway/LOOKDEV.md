# Freeway revision checkpoint

The accepted civil plans, diamond/ramp geometry, cross section, driving paths,
chaining sockets and Ground image inputs are retained. This round adds the
places, traffic, construction and baked appearance. No docs images or README
gallery are delivered. All inspection images below are ignored rebuild outputs.

## The requested fixes

| Fix | Result and native-size evidence |
| --- | --- |
| Town instead of lawn | Alder Junction has two complete native gas parcels, a strip center, 663 plan-envelope houses, seven parallel streets on each side, cross streets, garden/ROW trees, lights and sagging utility conductors. Cedar Hollow has 216 houses facing away from its walls, backyard divisions and streets ending at the fence. [Diamond before/after](renders/fixes/town-diamond.jpg), [backyards before/after](renders/fixes/town-backyards.jpg). |
| Traffic | 196 actors in 101 and 84 in 202: all three native bodies, five factory colors, moving mainline/ramp/arterial/bridge traffic, stopped terminal queues and parked commercial cars. Seeded headways are 1.7–3.1s at 25–29m/s. Near actors keep full native geometry; distant actors use explicit local distance meshes. [101 before/after](renders/fixes/traffic-diamond.jpg), [202 before/after](renders/fixes/sun-curved.jpg), [terminal controls](renders/lookdev/101/terminal_controls.png). |
| Bridge construction | Seven Type IV I-girders per span: 54in deep, 20in top flange, 26in bottom flange, 8in web. Camber, haunches, end/intermediate diaphragms, elastomeric pads, sole plates, pedestals, cap chamfers and overhang drip grooves are modeled. Assembled beams are 23.82m long to contain the complete bearing footprints; the reusable example remains 23.49m. [Before/after](renders/fixes/girders.jpg), [pier/girders](renders/lookdev/101/pier_girders.png), [bearing pair](renders/look-matches/bearing_2008-pair.jpg). |
| Seated terminals and controls | Pavement boundaries receive ground-intersecting granular/curbed returns. The terminal has stop bars, through and left-turn arrows, WRONG WAY, DO NOT ENTER, entrance guides and fictional Route 47 trailblazers. The existing clear walks cross the bridge. Native commercial driveway openings receive graded arterial aprons. [Before/after](renders/fixes/terminal.jpg), [controls](renders/lookdev/101/terminal_controls.png). |
| Right-of-way | Mowed/unmowed bands, toe ditches, inlets, concrete cut flumes, ROW fabric, rooted volunteers and brush; larger native trees beyond the mowing line. [Before/after](renders/fixes/cut-slopes.jpg), [sound wall](renders/fixes/sound-wall.jpg). |
| Raking sun and values | Procedural low sun at about 17 degrees, with long structural shadows and deep bridge shade. Concrete maps retain actual albedo rather than compensating for lighting. [101 hero](renders/lookdev/101/hero.png), [202 hero](renders/lookdev/202/hero.png), [202 before/after](renders/fixes/sun-curved.jpg). |
| Readable modules | Seventeen separately framed 1000px views, two columns, names, dimensions and triangle labels. [2000px sheet](renders/lookdev/modules.png), [before/after sheets](renders/fixes/modules.jpg), [individual views](renders/lookdev/modules/). |

The eight spatial before/after pairs retain the original camera positions and
targets, at 1400px per view. The module presentation uses larger cells. Camera
receipts are in [renders/fixes/cameras.json](renders/fixes/cameras.json).
Unobstructed overheads accompany the annotated views:
[Alder Junction](renders/lookdev/101/above_clean.png) and
[Cedar Hollow](renders/lookdev/202/above_clean.png).

## Costs measured from the serialized glTF

Instance-expanded triangles count every placed mesh. Unique mesh counts below
show reuse; neither is a claim about runtime frame rate. Materials are glTF
states, and primitives are unique-mesh primitives, not measured engine draws.

| Seed / package | Expanded triangles | Unique mesh triangles | Material states | Primitives | glTF + BIN bytes | Image residency, MiB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 freeway | 264,660 | 247,040 | 29 | 1,785 | 20,959,281 | 106.25 |
| 101 town | 5,180,146 | 793,134 | 61 | 373 | 58,116,871 | 143.00 |
| 101 traffic | 3,702,680 | 1,007,007 | 52 | 903 | 54,520,137 | 64.00 |
| 202 freeway | 161,542 | 161,542 | 16 | 1,613 | 14,449,592 | 88.25 |
| 202 town | 2,737,356 | 112,964 | 33 | 33 | 8,745,608 | 77.00 |
| 202 traffic | 1,219,222 | 495,249 | 41 | 581 | 27,697,936 | 64.00 |

Image estimates assume 8bpp block compression and full mips. Package image
totals overlap. The deduplicated whole-scene unions are **265.25 MiB for 101**
and **213.25 MiB for 202**; both scenes together still use 265.25 MiB / 87 unique
images / 127,298,572 PNG bytes. Town and traffic are explicit optional packages,
not hidden inside the freeway budget. The full context is much more expensive
than the civil kit and should use engine instancing/streaming and canonical
family LODs in a game.

| Module | Triangles | Material states |
| --- | ---: | ---: |
| CableBay | 126 | 2 |
| Cantilever | 1,922 | 4 |
| DavitLight | 228 | 4 |
| GoreAttenuator | 302 | 4 |
| GorePaving36 | 20 | 2 |
| GuardrailEnd | 404 | 4 |
| MedianF | 76 | 1 |
| Overpass | 22,556 | 9 |
| PierBent | 676 | 1 |
| PrestressedGirder24 | 796 | 1 |
| RampBranch | 548 | 3 |
| RoadBankTransition | 1,504 | 5 |
| RoadCurve | 1,504 | 5 |
| RoadStraight | 1,600 | 7 |
| SignTruss | 3,190 | 4 |
| SoundPanel | 144 | 2 |
| WBeam | 188 | 3 |

## Appearance and shared resources

[TEXTURES.md](TEXTURES.md) describes all source fields and causes. Four new
triples total **40 MiB**, shared across seeds: Concrete 2048 / 16 MiB, Signs
2048 / 16 MiB, Zinc 1024 / 4 MiB and Maintenance 1024 / 4 MiB. Their combined
PNG size is 18,150,190 bytes. Ground's four canonical triples remain unchanged.
The existing 256px fence recipe and native context images remain shared.

Concrete slab history follows joints; wheel polish and engine-line deposits
follow lane coordinates; repairs, the later overlay and shoulder sealant stay
on the appropriate paving. Repaint ghosts, missing raised markers and gore
tire traces have seeded placement. Concrete deposits begin at joints, drains,
scuppers and bearings. Column patches conform to the cylinder. Steel ages at
connections/exposure, selected ramp-rail bays bend, and adjacent replacement
bays retain brighter zinc. Signs have guarded original legends and aged
sheeting. Weeds, tires and litter accumulate at drainage/fence/barrier traps.

BaseColor is sRGB; normal is OpenGL +Y; ORM is linear R occlusion, G roughness,
B metallic. All new manufacture fields bake at 4096 before kit filtering.
RGBA maintenance coverage is baked separately from RGB and restored before
premultiplied filtering. No photograph enters any material generator.

Actual median linear map luminance is .2702 for bridge concrete, .2542 for
Ground concrete and .1407 for asphalt. Zinc's median metallic reflectance is
.3166. Whole-hero display luminance at the 1st/50th/99th percentiles is
.0109/.4712/.8644 (101) and .0434/.4093/.8597 (202). RGB channels at or above
.99 occupy .001089% and .000454% respectively; this includes sky and cars.
The pavement ROI's 95th-percentile display luminance is .499/.425. These are
rendered display measurements, not calibrated photographic reflectance or a
claim that every bright pixel is concrete. Actual ROI bounds and values are
in `src/quality_receipts.py` and `build/tones-look.json`.

## Photo comparisons

All four comparisons use the kit's feature fit and projection verification.
White balance uses a named field neutral, without exposure correction. Camera
lenses are estimates; small landmark residuals do not establish a surveyed
replica. [Reference credits and source limits](refs/SOURCES.md).

| Reference | Native fit RMS | Balanced neutral | Shipped / source-field pair |
| --- | ---: | --- | --- |
| Daily freeway / 2008 | 6.98px | Pavement ROI (370,1460)–(470,1510) | [shipped](renders/look-matches/guide_2008-pair.jpg) / [4096 fields](renders/source-matches/guide_2008-pair.jpg) |
| FHWA bridge / 2008 | 5.31px | Clean cap ROI (1100,1410)–(1140,1470) | [shipped](renders/look-matches/bearing_2008-pair.jpg) / [4096 fields](renders/source-matches/bearing_2008-pair.jpg) |
| USGS diamond / 2002 | 1.67px | Neutral roof ROI (430,42)–(455,60) | [shipped](renders/look-matches/diamond_2002-pair.jpg) / [4096 fields](renders/source-matches/diamond_2002-pair.jpg) |
| Daily traffic / 2007 | 1.49px | Gray asphalt ROI (1675,1490)–(1689,1510) | [shipped](renders/look-matches/traffic_2007-pair.jpg) / [4096 fields](renders/source-matches/traffic_2007-pair.jpg) |

The guide photograph has more lanes, the bridge has a pile bent and SCC beams,
the real diamond's west arterial curves, and the 2007 road has additional
outer/auxiliary lanes without this sound-wall enclosure. These compare original
types, construction, values and age. The source-field pairs retain exported
geometry and replace only the four new manufacture fields with 4096 color/ORM
and physical source height, clearly labeled in metadata.

## Verification and remaining limits

`make` completed successfully, including fresh glTF import, the construction,
resource and preservation checks, all checkpoint renders and final review.
Inspected 45 raw Cycles views: 19 scene views, 17 modules, scale, four shipped
photo views and four source-field views. The final review validates image,
bundle and recipe hashes and all eight complete matched camera/light records.
`python3 -m kit.repo_check` passed: 2,036 source candidates, zero errors.

`make check` separates fresh-import construction/contact measurements from
raw serialization/resource checks. Edge sampling measures 3,552 points in 101
and 8,256 in 202: no positive soil gap, at most 25.4mm intentional burial.
Three actual girder sections measure .6604/.2032/.508m flange/web widths.
168 bearing footprint probes have −.760 to +.755mm pad/girder camber difference;
sole plates contact pedestals at zero measured gap. Every Cedar Hollow house
envelope stays at least 2.50m outside the actual curved ROW fence envelope.
Fresh-import actor roots serialize with zero measured position error. The
504 identifiable wheel meshes in 101 and 144 in 202 measure −7.1 to +9.1mm
against actual paving. These probes do not certify every distant merged wheel
or the swept interactions of a running traffic simulation. Measured bridge
clearance over six lane probes is 5.771–5.901m.

`make repeat` independently rebuilds 24 geometry buffers byte for byte and
regenerates all 13 CPU source fields exactly. `make check-texture-repeat`
passed a fresh GPU bake and delivery filter: maximum difference 1/255,
worst RMSE .002359 byte, and coverage alpha byte-exact (kit limits: 2-byte
maximum / .02-byte RMSE). Detailed numerical receipts
live in `build/` rather than being represented as constants in a check.

Textured triangles have finite, noncollapsed UVs. Meter tiling and guarded
chart reuse deliberately overlap. Collapsed UVs counted on native untextured
scalar materials are unused; this is not a unique-lightmap certificate.
The session preservation gate checks 1,089 pre-existing other-family delivery
files byte for byte. No kit source or other-family delivery was changed.

The remaining CG cues are the regular lots and repeated house/foliage shapes,
simplified context interfaces, crisp cast-concrete edges, limited variation in
bridge patina and overly clean barrier/cap surfaces. Zinc's crystalline pattern
is still exaggerated at close gore/repair distance. Broad Ground asphalt
variation and shallow alpha rib/wire parallax also remain visible. Static
traffic is a seeded snapshot, not a traffic simulation. The
town uses explicit distance envelopes, not complete architectural houses.
The large context and material/draw-state counts need engine integration work;
no runtime performance result is claimed. No lead action or extra tool is
needed for this checkpoint. A future generic native-context LOD/instancing
reporter would help the kit; this family introduces no shared-kit change.
