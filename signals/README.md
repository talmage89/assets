# Waycroft / traffic signals — form checkpoint

Four original signalized intersections for an American town of 1995–2015.
This is the requested construction gate before look-dev: quick materials,
original graphics and imported checkpoint GLBs. It is not a baked final delivery.
No docs images are committed until the family is finished.

The family includes tapered mast arms and anchored poles, three-section
12-inch heads, a four-section FYA, five-section doghouse and protected-arrow
heads, black/yellow-bordered backplates, street-name signs, detection cameras,
pedestrian heads and accessible buttons, a two-pole span set, controller
cabinet, electric service and pull boxes. Real joints, visors, cast shoulders,
anchor holes, hollow nut covers, hinge hardware and slack service cables are
built in geometry where they affect construction or silhouette.

[REFERENCE.md](REFERENCE.md) records dimensions and distinguishes published
standards from authored choices. [REVIEW.md](REVIEW.md) records rejected passes
and remaining limits. [refs/SOURCES.md](refs/SOURCES.md) credits every source.

| Seed / town | Support and heads |
| --- | --- |
| 201 / Aldervale | Galvanized 36 ft reach; yellow tunnel visors; 2 in yellow border; FYA |
| 202 / Cinderbrook | Dark green 30 ft reach; black cap visors; five section; near-side head; pole-mounted pedestrian heads and separate button posts; lit street name |
| 203 / Wrenfield | Bronze 25 ft reach; yellow cap visors; protected arrows; Rill luminaire head |
| 204 / Morrow Glen | Black steel strain poles; diagonal catenary/messenger/tether set; eight free-standing heads |

Each mast carries two primary through faces 8 ft apart and a left-turn face
over the central turn lane. Opposing approaches share phases. Pedestrian walk,
hand and two seven-segment countdown digits have independently named parts.
The cabinet corner, finishes, head style, arm reach, left treatment and detection
presentation follow the seed. These four layouts demonstrate distinct municipal
equipment choices; they are not four engineered traffic plans.

| Feature | Dimension / choice |
| --- | --- |
| Vehicle indication | 304.8 mm / 12 in |
| Head section pitch / front width | 370 / 354 mm |
| Tunnel / cap visor reach | 245 / 205 mm |
| Steel pole | 7.62 m / 25 ft from plate bottom; 16 → 12.53 in across flats |
| Base plate / foundation | 762 × 63.5 mm circular plate; 1.2192 m round pier |
| Anchors | Six 44.45 mm rods; 584.2 mm circle |
| Arm | 7.62 / 9.144 / 10.9728 m pole-center reach; 2° camber |
| Street-name frame | 2.134 × .4572 m; equal name-face geometry |
| Pedestrian case / pedestal | 444.5 × 419.1 × 180 mm; 101.6 mm pole |
| Accessible button / standing space | 1.0668 m above actual landing; 762 × 1219.2 mm clear rectangle |
| Cabinet shell | 910 × 720 × 1660 mm; 3 mm aluminum, 200 mm plinth |

Meters, Blender +Z up, −Y frontage; glTF +Y up and +Z forward. Reusable assemblies
have ground-footprint origins. Head origins are their upper indexed hanger;
pedestrian head origins are case centers; the attachment-only APS origin is its
pole frame, with its button above it. Ground sockets preserve these placement
frames. Cabinet door uses local Z, −110…0°. Head frames provide Z ±15° aiming
and X ±4° limited movement. Source-surface sampled clearances distinguish
construction from the independent source/GLB serialization check. Service cable
is static geometry; a game adding wind motion must update its attachment ends.

## Rebuild and inspect

Run make WIDTH=1200 SAMPLES=24 in this folder. It fetches photos/PDFs, builds
the four sources and GLBs plus standalone parts, checks geometry and construction,
renders 19 Cycles views, fits two period photos and composes review sheets.
Every Cycles call holds the shared kit GPU lock. No kit source is changed.

- make check: budgets, named lenses, scale/clearance, source/import geometry,
  actual component contacts, sampled pivots and repository/preservation rules.
- make matches: calibrated period comparison views and side-by-side pairs.
- make -C ../ground arterial: separately build the new ground checkpoint library.

Generated outputs:

| Path | Contents |
| --- | --- |
| build/Signals-201…204.blend / .glb / .json | Equipment-only source, imported game checkpoint and measured budgets |
| build/parts/*.glb | MastArm, Pedestal, PushButtonPost, Cabinet, PushButton, PedHead, three/FYA/five/protected heads and SpanSet |
| renders/checkpoint/201/hero.png | Sidewalk eye height, 40 mm; original library ground, houses, trees and vehicles |
| renders/checkpoint/<seed>/{above,driver}.png | All four intersections; driver camera 1.18 m high, 42 mm |
| renders/checkpoint/201/{head_lit,head_dark,connection,base,pedestrian,button,cabinet,cabinet_open,dusk}.png | Construction, state and dusk evidence |
| renders/checkpoint/204/span_hanger.png | Balanced hanger, catenary tie, cable coils and tether |
| renders/checkpoint/{contact,four-towns,construction,photo-pairs}.jpg | Complete review sheets |
| renders/matches/{trenton,maryland}-pair.jpg | Imported GLB against balanced 2014 NJ / 2006 MD photograph |
| build/{checks,construction,ground-placement,preservation,hero-range}.json | Independent numerical evidence and provenance |

Validated with make WIDTH=1200 SAMPLES=24 and make check (both exit 0).
All four source-surface construction checks pass. The independent fresh-import
comparison has at most 2.16 µm vertex error. Replaying the four-seed recipe
produced 15 byte-identical GLBs (12,170,008 bytes total). The baseline receipt
confirms 295 existing delivery files are unchanged; repository check has zero
errors. The check scope excludes final UV packing, bake and look-dev approval.

The environment uses installed Blender/Python/Pillow/NumPy, fontconfig and
flock. No downloaded code, models, materials or HDRIs are used.

## Lens states for a game

Every lens is a separate mesh with signal_lens, signal_kind and powered extras.
Names are stable: Mast_0__Head0__S00_red, S01_yellow, S02_green; an FYA head
has S00_red_arrow, S01_yellow_arrow, S02_yellow_arrow and S03_green_arrow.
S02 additionally carries flashing_yellow_arrow. No animations or timing logic
are imposed on a game.

Switch a lens between the two shared materials SharedLens_Off and
SharedLens_Lit; both retain the same UV tile and dark BaseColor image. The lit material adds a separate generated bright emission image and
emission. The game must keep other sections dark and control legal phase
timing. Flash FYA S02 by toggling that lens; S01 is the steady yellow arrow.
Pedestrian meshes end in __hand, __walk and
__Countdown_{Tens,Ones}_{A…G}. Set those seven segment parts with the ordinary
0–9 segment table; suppress countdown during walk/steady don't-walk as needed.
The checkpoint shows walk in one direction and hand/countdown in the other.
Materials are shared: swap per-mesh references, do not change a shared material
globally to power an individual lens.

## Measured checkpoint budgets

| Reusable part | Triangles |
| --- | ---: |
| Three-section head, all variants | 940–1,036 |
| Four-section FYA | 1,308 |
| Five-section doghouse | 1,460 |
| Protected-arrow head | 940 |
| Complete mast assembly, seed 201 / 202 / 203 | 9,038 / 10,374 / 9,794 |
| Pedestal with head / button-only post | 1,562 / 1,042 |
| Push-button attachment / pedestrian head | 406 / 464 |
| Cabinet including service and moving leaf | 2,160 |
| Complete span-wire set with poles and eight heads | 20,152 |
| Flush pull box | 232 |

Whole equipment totals include every support, head, lens, station, cabinet,
pull box and standing pad. They exclude ground and presentation houses/trees/cars.

| Seed | Equipment triangles | Checkpoint GLB bytes |
| --- | ---: | ---: |
| 201 | 53,060 | 2,365,668 |
| 202 | 56,324 | 2,491,980 |
| 203 | 56,084 | 4,029,256 |
| 204 | 37,060 | 1,478,600 |

The prototype palette uses 13–26 materials across the seeds; final shared-map consolidation is pending. The native Rill maps account for the larger seed 203 file. This is intentionally a form checkpoint, not final draw-call/UV validation.

## Planned final texture allocation

One shared 2048² BaseColor/OpenGL Normal/ORM family atlas, one 1024² emissive
sheet and a 512 × 256 street-name sheet: approximately 17.5 MiB compressed
with full mipmaps (16 + 1⅓ + ⅙ MiB). The 2048 atlas is justified by the pole,
cabinet, pedestrian and several head styles sharing it. Most small fittings
will use baked normal detail. The optional Rill head keeps its native 1024 maps
in this checkpoint; its final charts are planned inside the family atlas without
changing the street-light delivery. Three surface types are planned: opaque family,
LED optics and names. Runtime lit/off instances share those same images.

This checkpoint still uses a quick palette and generated print sheets; it has
not performed UV packing, 4096 baking, downsampling or texture-memory validation.
The prototype GLBs' bytes and material counts are reported by build/checks.json,
not represented as final texture cost.

## Additive ground work

ground/src/arterial.py builds ArterialCheckpoint.glb separately: three 11 ft
lanes and a matching intersection, double yellow/dashes, left/through arrows,
24 in stop bars, high visibility crossings and sealed detector loops. Native
curbs, corners, sidewalks, ramps and lawn are placed unscaled. The script reuses
native asphalt maps. All pre-existing deliveries are protected by a SHA-256
receipt; no ground, street-light, street-sign or context asset is rebuilt.

The remaining weakness is the quick material response: no accepted 10–20 year
chalking, base rust, zinc patina, bird deposits, streaks or maintenance stickers
has been developed or baked. The cabinet rack is a blank; small optical and
mounting details remain simplified. The neighborhood repeats a few prototypes
and the distant setting is sparse. Photo fits compare construction in different
regional installations and cannot establish exact albedo or civil compliance.
Work stops at this checkpoint.
