# Ditchlight street skateboard

![Season board, Cycles render of the exported GLB](docs/hero.jpg)
![New, season and beat, top and underside](docs/ages.jpg)

| | |
| --- | --- |
| ![Grip, trucks, wheels and seven-ply edges](docs/details.jpg) | ![Turnaround, 1.8 m scale and Eevee](docs/inspection.jpg) |

![Three original fictional graphics](docs/graphics.jpg)

An original street skateboard for a 1995–2015 American town, generated entirely
by Blender 5.2 scripts. The gallery uses exported GLBs with baked maps; the
last graphic sheet is original script-drawn artwork. No reference pixels or
external models enter the asset. [REVIEW.md](REVIEW.md) records the image critiques
and remaining limits; [LOOKDEV.md](LOOKDEV.md) maps the full-size local evidence.

`make` rebuilds the seven-ply pressed deck, eight through-holes and recessed
Allen hardware, sculpted cast trucks, bushings and cup washers, profiled wheels
and visible 608 race/shield faces. Entirely buried nylon inserts, spacer bodies
and outboard speed rings remain in the manufacturing source and are omitted
from the game mesh. Every vertex, material, graphic and texel comes from these
scripts. Dense sculpts and temporary projection helpers do not ship.

## Dimensions and sources

[REFERENCE.md](REFERENCE.md) separates published values from original estimates;
[refs/SOURCES.md](refs/SOURCES.md) records photographs, drawings, authors and
licenses. The 2014 Skate One catalog's shape 127 supplies the default envelope.
Nose/front is Blender −Y; +Z is up; origin is the grounded wheel footprint center.
glTF is +Y up, +Z forward. One Blender unit is one meter.

| Dimension | Reference / generated default |
| --- | --- |
| Width × plan length | 8 × 32.125 in / 203.2 × 815.975 mm |
| Inner mounting-row wheelbase | 14.375 in / 365.125 mm; not axle spacing |
| Nose / tail, outer bolt row to tip | 6.875 / 6.625 in / 174.625 / 168.275 mm |
| Hole pattern per truck | 1.625 × 2.125 in / 41.275 × 53.975 mm; 5 mm bores |
| Veneers / finished maple | 7 nominal 1/16 in veneers; estimated 10.5 mm after pressing/sanding |
| Layup / grip | L/L/C/L/C/L/L; estimated 0.55 mm grip sheet |
| Mold concave | .30 in / 7.62 mm nominal rail rise at 8 in; actual tangent-region gauge in `build/new/construction.json` |
| Nose / tail kick | 18° mold class; continuous 80 mm transitions, slightly curved kicks |
| Truck mounting face → axle | 55 mm; matched 203.2 mm axle width, 137 mm cast hanger |
| Baseplate | Original estimated 58 × 80 mm casting; measured bounds/sections retained |
| Wheels | 54 × 32 mm; 15 mm nominal cylindrical riding band, rounded shoulders |
| Bearings | 608: 8 mm bore × 22 mm OD × 7 mm width; ISO 15 boundary dimensions |
| Hardware | One-inch 10-32 countersunk bolts, 3/8 in mounting-nut flats; 1/2 in axle / 9/16 in kingpin wrench classes |

The mold class comes from Action Sports Technology; the period catalog lists
54 × 32 mm V1 wheels. Roarockit supplies the veneer/layup baseline. NSK supplies
the 608 dimensions: **608 is a designation, not a standard called “ISO 608.”**
Manufacturer anatomy photographs and 2002 Dwindle patent sections establish the
truck's assembly; no proprietary dimensioned casting drawing was available.
Internal casting dimensions, kingpin inclination and travel are original
photo-informed estimates, not a recovered truck design.

The deck is a welded closed shell with seven exposed veneer bands and no buried
stacked internal faces. Castings fuse curved lofts, rounded volumes and tapered
arms, then retain dense sources and reduced game surfaces. Bores, flared bushing
recesses, annular seats and machined nut lands are real geometry. Small edge
bevels, drive machining, cast grain, wood fibers and axle threads transfer to
the normal bake. Actual triangle-plane sections
of the dense/game castings and the re-imported deck expose their construction.
Hard urethane has a riding band and geometric ground line, rather than a car
tire's flattened footprint.

## Counts and materials

The new and season boards have **13,888 triangles**. Beat adds 40 triangles
for two attached maple splinters: **13,928**, within the accepted 14k allowance.
The denser deck and 64-sided wheels take the silhouette budget; buried hardware
and bearing faces pay for it. Each visible bolt head/drive is 56 triangles.

| Part group | New / season triangles |
| --- | ---: |
| Deck and grip shell | 4,128 |
| Eight mounting fastener assemblies | 768 |
| Two cast baseplates | 1,074 |
| Two sculpted hangers | 1,422 |
| Bushings | 640 |
| Kingpins, pivot cups and washers | 800 |
| Exposed steel axle ends | 144 |
| Four urethane wheels | 4,096 |
| Eight visible bearing race/shield pairs | 640 |
| Exposed inboard speed rings | 80 |
| Axle nuts | 96 |
| **Whole board** | **13,888** |

Each state has one **2048 BaseColor / OpenGL +Y Normal / ORM** set, baked at
4096. Three response classes share its images: common opaque surfaces,
clear-coated maple/ink, and satin urethane with modest transmission. There is
no extra hardware atlas. One resident state costs about **16 MiB compressed
with mip chains**; all three age atlases cost about **48 MiB**. Actual GLB/map bytes and UV densities are recorded in
`renders/final/budgets.json` and `build/<state>/verify.json`.

| Age | GLB bytes, including maps | Three PNGs, bytes | Triangles |
| --- | ---: | ---: | ---: |
| New | 8,587,240 | 7,643,164 | 13,888 |
| Season | 9,412,400 | 8,477,544 | 13,888 |
| Beat | 9,461,080 | 8,531,219 | 13,928 |

Each GLB has seven mesh nodes and twelve material primitives. The three atlas
images are embedded once per GLB and are also written separately for engine
import; the two columns above are alternative packaging costs. Compressed
memory is an estimate for engine block compression, not PNG disk size or a
measured engine allocation. UV overlap, outside and degenerate triangles are
zero; median density is 2,032 / 2,067 / 2,026 px/m for new / season / beat.

[TEXTURES.md](TEXTURES.md) documents causal aging and the three original
Ditchlight / Kilnline / Static Orchard sheet designs. Wheel marks are Kilnline;
truck marks are Crossway. The default Ditchlight board is exported in all three
ages. New has fresh carbide grip and clean ink. Season has transverse belly slides
through clear coat and ink to white base and maple, tip/rail chips, front-bolt
and tail-pocket shoe dirt, underside hanger grinds, and yellow sidewalls around
dark coned tread. Beat adds a razor tail, lifted veneers, shoe-goo repair, torn
nose grip, faded wheel print and one real flat spot on the front-left wheel.
There is no center grip label. The flat is parked above ground; it causes a
bump when rolled, as a damaged wheel does.

Seed 0 is 8 in / 32.125 in, with 54 mm wheels. Seeds 1/2/3 use 7.75/8.25/8.5 in
widths, matching axles, 51/53/56 mm wheels and original envelopes in the brief's
ranges. Seed 3 adds 3.175 mm risers. The solid pad is retained in the source;
the game omits its clamped top/bottom and hidden hole walls. Alternate sizes
remain construction variants, not additional look-dev approvals.

## Moving parts and sockets

No armature or clips. The game controls separate pivots. Each wheel's local X
is its axle and rotates continuously. Wheel meshes and shields ride the wheel;
steel axle, spacers and locknuts ride the hanger. Static bushings are a visible
compliance proxy, not a rubber deformation simulation. Internal ball/cage
motion and separate inner-race motion are not simulated.

| Node | Frame / range |
| --- | --- |
| `Hanger_Front`, `Hanger_Rear` | Local Z, −12…+12°; pivots at cup centers, axis through bushing-seat center |
| `Wheel_Front_L/R`, `Wheel_Rear_L/R` | Local X, continuous 360° spin |
| `Socket_Foot_Front`, `Socket_Foot_Rear` | Grip contact; shoe-length direction across deck |
| `Socket_Hand_Carry` | Left rail midspan; local +Z points inward |
| `Socket_Rest_Ground` | Footprint ground center, identity |
| `Socket_Rest_Wall` | Surface-derived wall contact frame; see alignment below |

Axes above are Blender local axes. In glTF, local Z becomes local Y; the
wheel axle remains local X. Default cup centers are `(0, ±234.55, 73)` mm. World steering axes are approximately
`(0, +.80961, −.58697)` front and `(0, −.80961, −.58697)` rear: **35.94° to
the deck plane**, measured from actual pivot matrices. The kingpin itself is
20° from vertical toward its axle. To demonstrate a coordinated carve, apply
front `+angle` and rear `−angle`, so both wheel banks agree and their steering
yaws oppose. This conservative ±12° range is an authoring estimate, not a
manufacturer stop specification.

For a wall at world Y=0, outward normal +Y, align `Socket_Rest_Wall` to a target
rotated −90° around X, at Z=`wall_alignment_height_m` from its extras. The whole
board then leans 78° with its measured lowest surfaces on floor Z=0 and wall
Y=0. `build/<state>/construction.json` names the actual contact meshes; the dedicated render
uses the same complete socket alignment. Moving the target carries the board.

## Rebuild and verification

Installed Blender 5.2, Python/Pillow/NumPy, GNU make, DejaVu/Noto fonts and flock.
Only cited photos/PDFs are fetched. Blender calls run serially in this worktree;
all Blender steps hold the shared kit lock; Cycles uses OptiX/CUDA.
Appearance comparisons reconstruct our tracked scripts at `b0939d8`; the
optional historical form comparison uses `8cc0710`. These commits must be
available in this clone. No other checkout or worktree is accessed.

```sh
make                         # sources → 4096 bake → 2048 GLBs → finals/docs/checks
make check                   # game/dense construction, GLB/UV/maps, repo rules
make repeat                  # byte-identical serialization and original image fields
make repeat-form             # independent raw form rebuild and byte comparison
make check-variants          # alternate dimensions, budgets and riser supports
make clean                   # generated asset outputs; references stay cached
```

Construction checks measure actual surfaces: scale, deck gauge/concave/kicks,
eight bores, bushing seats, metal clearance, ground/wall contacts, bearing
winding, and attached delamination. Game hangers sweep every 1° over ±12°;
wheels spin every 15°. Dense source hangers get their own sweep. Only the
bushings and retained rubber pivot are compliant exceptions. These are sampled
checks, not continuous collision guarantees. Fresh baked-GLB imports separately
verify counts, normals, UV overlap/density, texture dimensions and complete
pivot/socket transforms; they prove serialization rather than construction.

| Local output | Contents |
| --- | --- |
| `export/{new,season,beat}.glb` | Embedded baked game assemblies |
| `textures/<state>/` | One three-map 2048 set |
| `build/<state>/model.blend` | Game form and retained manufacturing sources |
| `build/<state>/{high,finalized}.blend` | Dense finish source and UV-packed game assembly |
| `build/<state>/{construction,high-check,verify}.json` | Separate physical and delivery audits |
| `renders/fixes/` | Nine native-size appearance before/after crops, same cameras |
| `renders/form-fixes/` | Optional historical form comparisons and three deck sections |
| `renders/final/<state>/` | Cycles heroes, tail/truck/bearing/grip close-ups; season turnaround/scale |
| `renders/final/{pairs,source-pairs}/` | Three neutral-balanced photograph comparisons |
| `renders/final/contact.jpg` | All states, details, turnaround, scale and Eevee |
| `renders/final/eevee/hero.png` | Eevee view of the same season GLB |
| `renders/final/graphics-sheet.jpg` | The three original designs |
| `renders/final/{values,budgets}.json` | Measured tones and delivery costs |

The mini-board fit is retired. Current pairs use the 2006 horizontal used board,
the 2010 used complete (including an exact close truck/wheel crop), and the
2005 full-size loose truck. The photographs' unrecorded dimensions and lenses
limit what their residuals prove. Neutral patches and gains are recorded in
`build/photo-balance.json`; reference pixels never enter a material.

Five final JPGs are rebuilt by `make docs`; each is at most 1600 px wide and
200,000 bytes. No animation clip or GIF is required: the separate pivots are
ready for engine controls. `make repeat` checks deterministic serialization
from existing maps and independently regenerates all original source images;
it does not claim a repeated GPU bake.

Credits and photograph licenses are in [refs/SOURCES.md](refs/SOURCES.md).
Installed DejaVu Sans fonts use their open font license. Fictional Ditchlight,
Kilnline, Static Orchard and Crossway graphics are authored here. Lighting is
procedural sun/sky and area lights. No external model, texture or HDRI is used.
