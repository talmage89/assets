# Freeway — look-dev checkpoint

Two original procedural freeway places in a town of 2012: a maintained 1970s
concrete diamond under an arterial, and a curved asphalt corridor with a wide
median and residential sound walls. The accepted alignments, lane section,
ramp geometry and driving/chaining sockets are retained. **This round stops
before a README gallery or docs images.**

[LOOKDEV.md](LOOKDEV.md) maps each requested fix to its views and measured costs.
[REVIEW.md](REVIEW.md) records the native critiques and remaining CG cues;
[REFERENCE.md](REFERENCE.md) gives real dimensions and source limits;
[TEXTURES.md](TEXTURES.md) describes the four shared PBR sets and caused age.
The inspection images remain rebuildable, ignored artifacts.

## Places and delivery

| Seed / place | Freeway triangles | Town context triangles | Traffic triangles / actors | Freeway glTF + BIN |
| --- | ---: | ---: | ---: | ---: |
| 101 / Alder Junction | 264,660 | 5,180,146 | 3,702,680 / 196 | 20,959,281 B |
| 202 / Cedar Hollow | 161,542 | 2,737,356 | 1,219,222 / 84 | 14,449,592 B |

`export/Freeway-{101,202}.gltf` contains the civil asset and its roadside.
`Town-<seed>.gltf` and `Traffic-<seed>.gltf` are separate context packages; every
inspection view imports all three. The freeway's own count remains below
400k. Native foliage and near cars dominate the larger context counts. Those
are instance-expanded totals; `build/look-audit.json` also reports unique mesh
triangles, material states, primitives, geometry bytes and image memory.

Alder Junction has two native gas parcels and a strip center at the arterial,
663 native-plan house shells, seven parallel streets on each side,
backyards, utility conductors, public lights and native trees. The strip's
public street wraps behind its parcel; graded aprons use the commercial
family's actual driveway openings. Cedar Hollow has a differently arranged
residential grid of 216 houses behind the walls, with roofs/trees above them and cross
streets ending at the right of way. Context uses the existing explicit house
plan-envelope adapter and canonical materials. It is a visual town context,
not a complete civil/architectural town delivery.

Traffic uses all three native bodies and five original factory colors. Near
vehicles retain their full geometry, including actors within 36m of the stock
close-up cameras; distant bodies retain coherent local LOD normals and native
BaseColor/ORM. The native paint-coverage data is decoded
into local stock-PBR RGB variants. Afternoon flow uses seeded 25–29m/s speeds
and 1.7–3.1s headways; ramp and arterial queues have stopped actors. Ramp cars
follow grade and bank; daytime flowing lamps are off and queues retain brakes.
The snapshot is static. Use the canonical cars for working gameplay pivots.

Keep repository-relative external image URIs, or remap them into an engine's
shared texture cache. Original library deliveries remain read-only and are
hash-checked. No image is embedded per seed, downloaded into a material, or
copied from a photograph.

## Dimensions and construction

| Feature | Dimension / basis |
| --- | --- |
| Mainline | Two 12ft / 3.6576m lanes each way; 10ft right and 4ft left shoulders; 2% tangent crossfall |
| Diamond | 1,600m excerpt; 8ft median; terminal axes X ±78m; 366m parallel speed-change lane plus 91.44m taper |
| Curved corridor | 1,000m excerpt; 1,400m radius; 4% bank; 30ft median and 14ft precast sound walls |
| Paving / paint | 15ft concrete joints; 6in lines; 10ft dashes on a 40ft cycle; physical 16×7in rumble envelopes at 12in pitch |
| Median / rail | 32in F barrier, actual drain openings; 31in W-beam top, 12-gauge sheet, 6ft 3in post pitch and real blockouts |
| Overpass | Two 24m spans; 70ft / 21.336m deck; five 11ft lanes; 5ft clear walks retained |
| Girders | Seven per span, Type IV: 54in depth, 20in top, 26in bottom, 8in web, actual chamfers/haunches and 18mm camber |
| Supports | Three 1.2m columns; 19.8×2.3×1.1m chamfered cap; elastomeric pads, sole plates, .88×.78m pedestals and widened abutment ledges |
| Girder length | 23.49m reusable example; 23.82m in the bridge so the complete pads stay under the flange |
| Structure / lighting | 34m four-chord triangulated guide truss; 12m davit mounting height |

FHWA/AASHTO cross-section guidance, 2003/2009 MUTCD and period DOT plans inform
these dimensions. The corrected Type IV section is from TxDOT report
0-4751-1 vol.2, Figure A.1.4.1. [SOURCES.md](refs/SOURCES.md) records the primary
references, dates, authors and rights. These are original visual constructions,
not load-rated bridges or certified crash hardware.

The bridge has top/bottom flanges and web, cambered haunches, end/intermediate
diaphragms, bearing plinths, abutments/wingwalls, approach slabs, deck overhang,
a real underside drip groove, walk parapets, fence and connected drains.
Paving boundaries have granular shoulders or curb returns sampled against
actual soil. Ditches/inlets, cut flumes, mowing limits, ROW fencing, volunteers
and trapped litter complete the corridor. Added terminal controls include stop
bars, through/left-turn arrows, WRONG WAY / DO NOT ENTER, entrance guides and
fictional Lark Route 47 trailblazers. DejaVu Sans Condensed Bold is the open-font
FHWA substitute; no Interstate shield or real brand is used.

## Reusable pieces

Fresh raw-accessor counts. Material states differ from placed draw calls.

| Module | Triangles | Materials |
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

The complete bridge includes its girders and bent; do not add those examples
again. All ordinary pieces stay below 2k, structures below 8k, the bridge below
50k. Flat paving and small barriers intentionally use fewer than 300 triangles.

## Shared materials and memory

Ground Asphalt, Concrete, Lawn and GroundTrim remain canonical. New
FreewayConcrete and FreewaySigns are 2048 triples (16 MiB each);
FreewayZinc and FreewayMaintenance are 1024 triples (4 MiB each): **40 MiB new**,
shared across seeds and modules. The sign triple replaces the old temporary
single sheet. The small fence field reuses the original chain-link recipe.
`TEXTURES.md` separates the manufacturing fields, caused placement layers and
native context resources. Estimates assume 8bpp block compression and full
mips; PNG bytes and Blender's uncompressed residency are different quantities.

All twelve new maps are generated/baked at 4096, then filtered with the kit.
BaseColor is sRGB, Normal is OpenGL +Y, ORM is linear occlusion/roughness/metallic.
Tiling UVs and guarded chart reuse intentionally overlap. Independent audits
check finite UVs and noncollapsed textured triangles, measured density percentiles, normal lengths,
resource identities and actual serialized triangle counts. No unique-lightmap
UV certification is implied.

## Coordinates, sockets and rebuild

Meters; Blender +Z up, canonical front −Y, station +Y, arterial +X. Scene origin
is station zero at the alignment datum. glTF converts `(x,y,z)` to `(x,z,−y)`.
Individual module exports retain chaining frames; the library sheet has display
placements to reset before assembly. Sign faces remain replaceable panel roots,
lights expose emitter sockets, and bridge/girder ends expose W/E frames.
Road and rail S/N frames use local +Y forward; bridge W/E frames follow +X.

The immutable `Plan` carries seed, civil type, length, median, radius, grade,
bank and terminal offset. Its exact center/frame functions drive every mainline
surface and path. Four lane and four ramp curves remain in the diamond source;
four lane curves remain in the curved source. glTF path empties retain sampled
Blender/glTF coordinates in extras because glTF has no curve primitive.
Those samples are already in the authored path-root frame. The path empty's
translation marks its start; do not add that translation to the samples again.
No new freeway animation or armature is needed.

```sh
make                         # fields/bakes, exports, checks, all checkpoint views/pairs
make check                   # fresh import, raw PBR/UV, real contacts and preservation
make repeat                  # exact buffers and independently generated CPU fields
make check-texture-repeat    # fresh GPU bake; kit 2/255 max and .02-byte RMSE limits
make render sheet scale      # exported Cycles views, large labeled pieces, human/car scale
make matches source-pairs    # four balanced-photo pairs, shipped and 4096 source fields
make evidence                # native before/after views from identical cameras
```

Blender runs serially and GPU work uses the shared kit lock. Scratch files stay
inside build/. No kit code changed. `make` stops at this look-dev checkpoint.
The scene views, sheet, scale and both photo sets share one serial GPU lease.
The isolated accepted-source archive can reconstruct missing before views from
commit 3681a2c without touching another worktree.

`renders/lookdev/` holds the 1400px Cycles scene views, 1000px individual pieces,
2000px labeled sheet, scale and contact. `renders/look-matches/` holds the four
shipped-PBR comparisons, with `renders/source-matches/` for source-field bake-loss
inspection. `renders/fixes/` contains native before/after pairs and camera receipts.
`build/check.json`, `edge-audit.json`, `bridge-audit.json`, `look-audit.json`,
`context-audit.json`, `albedos.json`, `tones-look.json` and repeat receipts separate construction,
serialization, resource, appearance and reproducibility evidence.

The scene remains more orderly than the photographed town: repeated house and
foliage silhouettes, regular lots, simplified context interfaces, crisp concrete
edges and overly clean barrier/cap surfaces remain visible. Zinc's crystalline
pattern is still exaggerated in the close gore/repair views. Ground's broad asphalt
variation and fine alpha rib/wire parallax also show at close range. Photo fits
compare original types: lane counts, bridge construction, season and cities
differ. No photographic equivalence or traffic/civil certification is claimed.
