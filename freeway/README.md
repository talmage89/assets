# Freeway — form and construction checkpoint

An original procedural freeway family for a town in 2012, with a maintained
1970s concrete diamond interchange and a separate curved asphalt corridor.
**This delivery stops before look-dev.** The construction, alignment, exported
geometry and inspection images are ready for review; quick materials are not
the finished weathered asset. Nothing in `kit/` or an existing family is changed.

## The two places

| Seed | Plan | Exported triangles | Materials, including context | Geometry files |
| --- | --- | ---: | ---: | --- |
| 101, Alder Junction | 1,600 m depressed concrete freeway, four ramps, signalized arterial on a two-span overpass | 388,894 | 69 | 1,823,042 B glTF + 21,355,668 B buffer |
| 202, Cedar Hollow | 1,000 m raised asphalt curve, wide cable median, houses behind sound walls | 348,638 | 52 | 1,800,038 B glTF + 10,907,356 B buffer |

Both include six vehicles, ROW fencing, drainage, lighting, houses, trees and
utility lines. The diamond also has a native commercial store exterior and a Ground-tiled
parking parcel.
The nearest H120 retains the original car geometry. Distant traffic uses local
context reductions with coherent geometric normals and native BaseColor/ORM;
their full-mesh normal bake is omitted. Houses are explicitly distance proxies
generated from the
house family's delivered roof planes, wall sections and clipped opening plans,
with its canonical material tiles and simple fixtures. They are not changes to
the house deliveries. Trees retain native geometry. Signal and utility form
geometry calls the existing families' construction functions.

Traffic copies are static inspection fixtures. Use the canonical car deliveries
for their working door, steering and wheel pivots.

## Dimensions and construction

[REFERENCE.md](REFERENCE.md) gives the detailed dimension basis and separates
standard dimensions from authored design choices. [The source register](refs/SOURCES.md)
records URLs, authors, rights and uses. AASHTO recommendations were researched
through its public excerpt and official FHWA explanations; the full copyrighted
Green Book and Roadside Design Guide were unavailable.

| Feature | Built dimensions | Primary basis |
| --- | --- | --- |
| Freeway section | 12 ft / 3.6576 m lanes; 10 ft / 3.048 m right, 4 ft / 1.2192 m left shoulders; 2% tangent crossfall | [FHWA reproduction of AASHTO table](https://ops.fhwa.dot.gov/publications/fhwahop16060/ch2.htm) |
| Curved seed | 1,400 m radius, 4% bank, 30 ft / 9.144 m median; alignment datum +1.4 m | Authored alignment; separate partial bank-transition piece |
| Diamond | 8 ft / 2.4384 m median; terminal axes X ±78 m; ramp path 273.908 m, measured maximum grade 4.557%, minimum plan radius 178.690 m | Authored layout compared with USGS's 2002 diamond photograph |
| Speed-change lanes | 12 ft wide; 366 m parallel length and 91.44 m taper | Generous authored geometry informed by [TxDOT ramp guidance](https://www.txdot.gov/manuals/des/rdw/chapter-15-grade-separations-and-interchanges-/15-7-ramps---direct-connectors-.html) |
| Pavement and markings | 15 ft / 4.572 m concrete joints; 6 in / .1524 m lines; 10 ft dashes on 40 ft cycle; 3/12 ft dotted auxiliary boundaries | [2003 MUTCD](https://mutcd.fhwa.dot.gov/pdfs/2003/Ch3.pdf), [2009 MUTCD Part 3](https://mutcd.fhwa.dot.gov/pdfs/2009/part3.pdf), FHWA pavement manuals |
| F barrier | 32 in / .8128 m high; 24 in base, 6 in top; 20 ft / 6.096 m bay; actual 12 × 3 in drainage slot | Period WSDOT F-shape practice; slot is an authored detail |
| W-beam | 31 in steel top; 12 gauge / 2.66 mm sheet; 6 ft 3 in / 1.905 m post spacing; 3.81 m bay plus laps | WSDOT Type 31 construction; generic illustrative terminal |
| Sound wall / ROW | 14 ft / 4.2672 m post-and-panel wall; 6 ft chain-link fence, 10 ft post spacing | GDOT period panel construction; existing fence family's analytic wire field |
| Overpass | Two 24 m spans; 70 ft / 21.336 m deck; five 11 ft lanes; 5 ft / 1.524 m clear sidewalks | Original bridge arrangement, state DOT prestressed-girder construction |
| Load path | Seven 54 in / 1.3716 m Type IV envelope girders per span at 3.048 m centers; 28 elastomeric pads; three 1.2 m columns; 19.8 × 2 × 1.1 m cap | Traditional generic section envelope, not a load-rated bridge design |
| Exported bridge measurements | 5.7707–5.9007 m sampled road-to-girder clearance; maximum bearing contact discrepancy 0.0024 mm | Independent rays against freshly imported actual surfaces |
| Guide structure / light | 34 m truss span, 1.52 m depth, triangulated four-chord construction; 12 m davits | Original illustrative construction informed by DOT photographs/plans |

The bridge includes deck crown, cambered reusable girders, diaphragms,
abutment seats/backwalls, wingwalls, slope paving, approach slabs, parapets,
pedestrian fence, scuppers and connected downpipes. Ramp rail follows the actual
curve and grade; posts stay vertical and splice lengths overlap. The wide
median is a depressed ditch, with cable posts planted at its surface.

Signs use fictional Lark Route 47, destinations and street names. No Interstate
shield is used. Installed **DejaVu Sans Condensed Bold**, found through
`kit/fonts.py`, approximates the unavailable FHWA alphabet. Guide faces, exit
tabs, speed, mile, DO NOT ENTER and gore EXIT graphics are script-generated.
Opposing guides have NORTH / Alder Junction and SOUTH / Cedar Hollow legends.
The curved segment uses a through guide over its own carriageway. Truss legs
follow actual terrain heights; measured concrete-base embedment is .3000 m.
Eight exported approach-pavement/soil samples measure zero gap.

## Reusable pieces and budgets

Fresh external glTF re-import counts, including signs and sockets' associated
visible construction. Empty sockets and driving paths add no triangles.

| Piece | Triangles | Piece | Triangles |
| --- | ---: | --- | ---: |
| RoadStraight, 36.576 m | 856 | RoadCurve, 36.576 m | 760 |
| RoadBankTransition, 36.576 m | 760 | RampBranch | 548 |
| GorePaving36 | 20 | MedianF | 76 |
| WBeam | 188 | GuardrailEnd, 7.62 m | 404 |
| CableBay | 126 | SoundPanel | 132 |
| SignTruss | 3,190 | Cantilever | 1,922 |
| DavitLight | 228 | GoreAttenuator | 302 |
| PrestressedGirder24 | 596 | PierBent | 660 |
| Overpass, complete assembly | 18,124 | **All 17 library examples** | **28,892** |

The bridge assembly includes its girder and bent instances; do not add the
separate examples to its count. Flat paving and simple barriers intentionally
use fewer than 300 triangles. The bridge is below the nominal 20k lower bound
without silhouette subdivision; both scenes remain below 400k. The library
uses 13 quick material roles and 39 meshes, with a 74,001 B glTF and
2,386,696 B buffer. These material roles will be consolidated during look-dev.

## Shared images and memory

Exports are `export/Freeway-{101,202}.gltf`, `export/FreewayModules.gltf` and
`export/modules/*.gltf`, each with an external `.bin`. Optional tangents are
reconstructed by importers; authored normals are retained. Image URIs share
canonical native images across the clone; only GLB-only/temporary graphics need a single
content-addressed copy in `export/shared/`. Keep these relative directories
together when importing. No downloaded image is used in a material.

| Allocation | Size | Estimated compressed GPU memory with mipmaps |
| --- | --- | ---: |
| Reused Ground Asphalt, Concrete, Lawn, GroundTrim | Four existing 2048 triples | 64 MiB |
| Temporary original sign face sheet | One 2048 image | 5.33 MiB |
| Temporary native fence analytic field | Three 256 images | .25 MiB |
| Temporary reused-source signal graphics, diamond only | Three 1024 × 512 images | 2 MiB |
| All scene 101 images, including native town/traffic | 49 unique images, 82,383,259 B PNG data | 150.58 MiB |
| All scene 202 images, including native town/traffic | 36 unique images, 78,367,699 B PNG data | 137.25 MiB |

These estimates assume one byte per texel per map after BC compression, with
mipmaps; PNG sizes are disk storage, not VRAM. Each scene deduplicates by image
hash. The current bridge concrete and metal use scalar quick materials.

The proposed look-dev allocation is a 2048 concrete triple (16 MiB, shared
bridge/barriers/walls), 1024 galvanized-steel triple (4 MiB), 2048 sign-face
triple (16 MiB) and an additive 1024 Ground maintenance/decal extension (4 MiB):
**40 MiB new**, before replacing temporary maps. Existing Ground deliveries stay
unchanged. Final Signals, street-signs, fences and trees atlases should be reused
where applicable. This is a declared allocation, not a finished texture delivery.

## Generator and sockets

`src/plan.py` owns lane/shoulder/joint dimensions and immutable `Plan` values:
seed, kind, town, length, median width, radius, elevation datum (`grade`), bank,
pavement and terminal offset. `Plan.center/frame/xyz` drive the same exact
alignment for pavement, earthwork, rail, furniture, traffic and paths. Ramp
paths use a cubic horizontal ease and a separate vertical curve after the
shared throat. The quick bank-transition example changes −2% to −2.5% over
36.576 m; chain four appropriately parameterized pieces for −2% to −4%.
Only seeds 101 and 202 are audited deliveries; other seeds select deterministic
plan variants and require their own geometry review.

Blender meters, +Z up, +Y station, arterial +X. The scene origin is station zero
at the diamond's freeway datum; the curved seed is raised from that datum.
Road/rail `S` and `N` empties chain modules. Road end frames use local +Y as
the forward tangent. Bridge/girder `W`/`E` frames point along +X. Sign faces are
separate replaceable panel roots with nominal dimensions and `sign_face`
sockets. Davits expose an `engine_light` socket. No animated freeway part is
required at this gate.

Lane centerlines and all four ramp paths are actual curves in the per-scene
`build/Freeway-*.blend`. glTF has no curve primitive: corresponding `drive_path`
empties carry `points_blender_json` and `points_gltf_json`, sampled coordinate
arrays. The glTF array maps `(x,y,z)` to `(x,z,−y)`. Samples are in the authored
path-root coordinate frame; the empty's translation marks the start and must
not be applied to the sample array again. `build/modules.json`,
`build/scene-*.json` and `build/check.json` record parts, bounds and measurements.

## Rebuild and inspection

```sh
cd freeway
make                 # references, missing native inputs, form exports, checks, all Cycles views
make check           # independent re-import, dimensions/contact/budgets and repository rules
make repeat          # second construction, exact comparison of 20 geometry buffers
make preview         # optional fast Eevee hero/aerial previews
```

Blender 5.2 headless, deterministic geometry, installed Python/Pillow/Numpy and
open fonts. All Cycles work runs through the existing kit GPU lock. Missing
native inputs are rebuilt using their original Makefiles; an existing delivery
is never rebuilt. All Freeway-generated data is ignored and rebuildable.

The final inspection set is rendered **from external exports**, not the source
scene, at 1400 px, 32 Cycles GPU samples, procedural raking sun/sky and fixed AgX
exposure. The 17 module views are individually framed. Review images stay
ignored at this checkpoint; no final `docs/` JPGs are committed.

- [Scene contact sheet](renders/checkpoint/contact.jpg): two eye-height 40 mm heroes, close aerials and annotated full alignments, barrier, real ramp guardrail terminal, signs, bridge underside, gore, terminal, sound wall and cable median.
- [Module sheet](renders/checkpoint/modules.png), with [individual views](renders/checkpoint/modules/).
- [Scale shot](renders/checkpoint/scale.png): 1.8 m silhouette and full native H120.
- [Three period photo comparisons](renders/matches/contact.jpg), with individual `*-pair.jpg` files and projection overlays.
- [Six critique passes](REVIEW.md), including rejected geometry and disclosed comparison limits.

Independent audits check normals, nondegenerate geometry, measured crossfall,
widths, barrier openings, rail height, bearing contacts, bridge clearance,
sidewalk clear width, approach and sign-foundation contacts, context-car normal
hemispheres and 24 tire contacts in each scene. Hash preservation
covers 529 preexisting texture/export files. Repeated tile UVs and quick
context materials are intentional; final atlas overlap, density, bake loss,
material-count optimization and motion/swept-vehicle validation are not certified
by this form gate.

The rebuild was exercised after clearing every Freeway-generated build,
export, texture and render output (downloaded references and original native
inputs retained). `make check` passes at the counts above. The final construction
repeat matches all 20 `.bin` files exactly; the four final quick image maps also
match an isolated regeneration. Evidence is in `build/check.json`,
`build/repeat.json`, `build/graphics-repeat.json` and the render metadata.

## Remaining work

Concrete repair/spall relief, bridge joint/drain staining, directional tire
polish, old stripe ghosts, metal corrosion, shoulder debris and fence weeds
remain for a later look-dev phase. Placement-owned patch groups exist,
but no uniform weather wash stands in for caused aging. Ground's tiling sets
are reused; its maintenance/decal extension has only been allocated. The generic
guardrail terminal, attenuator and sign support are plausible visual assemblies,
not certified products. Ramp terminals need a full vehicle swept-path review.
Town context remains sparse and repetitive, with simple house fixtures. Sign
green and material albedos still need calibration against the photographs.
No final photographic material quality is claimed here.

Reference photograph credits: Coolcaesar (2008 freeway, CC BY-SA 3.0/GFDL),
FHWA (2008 bridge, US government public domain/CC BY 2.0), USGS (2002 diamond,
public domain). Photographs are viewed and camera-matched only; they contribute
no vertex or texel. All visible asset geometry and graphics originate in this
repository's scripts.
