# Ditchlight street skateboard — form checkpoint

An original scripted street skateboard for a 1995–2015 American town. This is
the **form and construction checkpoint, before look-dev**. The exported GLB
uses temporary material factors. Graphics, age, UVs, baked maps and final docs
are deliberately deferred. No existing delivery, toolkit file or top-level
index is changed.

`make` generates a seven-ply popsicle deck, trimmed grip edge, actual eight-hole
mounting pattern and countersunk Allen heads, two compound cast trucks, bushings,
pivot cups, kingpins, washers, locknuts, four urethane wheels, eight shielded 608
bearings, spacers and speed rings. Every vertex is authored by these scripts.
The dense source castings remain separate and excluded from the GLB.

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
| Mold concave | .30 in / 7.62 mm nominal rail rise at 8 in; actual near-edge gauge in `build/check.json` |
| Nose / tail kick | 18° / 18°; measured from actual centerline ray hits |
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
bevels and surface grain wait for the normal bake. Actual triangle-plane sections
of the dense/game castings and the re-imported deck expose their construction.
Hard urethane has a riding band and geometric ground line, rather than a car
tire's flattened footprint.

## Counts and texture plan

The default is **11,662 triangles**, below the 12,000 ceiling. The inspection GLB
retains 95 named meshes and 16 temporary factor materials, **zero images**.
It is **397,852 bytes**; its SHA-256 is in `build/skateboard.json` and `build/check.json`.
The final atlas/consolidation will reduce this inspection split to rigid groups;
these temporary draw calls are not claimed as a finished game delivery.

| Part group | Default triangles |
| --- | ---: |
| Deck and grip shell | 1,924 |
| Eight mounting fastener assemblies | 1,216 |
| Two cast baseplates | 1,050 |
| Two sculpted hangers | 1,400 |
| Bushings | 480 |
| Kingpins, pivot cups and washers | 872 |
| Steel axles | 64 |
| Four urethane wheels | 3,136 |
| Eight bearings and shields | 896 |
| Bearing spacers and speed rings | 384 |
| Axle nuts and nylon inserts | 240 |
| **Whole board** | **11,662** |

[TEXTURES.md](TEXTURES.md) plans one 4096 bake, shipped as one 2048 BaseColor /
OpenGL +Y Normal / ORM set, about **16 MiB compressed with full mip chains**.
One delivered material; no extra hardware atlas. Fictional deck/wheel/truck
marks, three original graphic designs and grip stickers are planned there.
`new`, `season` and `beat` are registered states but intentionally have no
visual age effect yet; that next stage includes localized geometric damage.

Seed 0 is 8 in / 32.125 in, 54 mm wheels. Seeds 1/2/3 use 7.75/8.25/8.5 in
widths, matching axles, 51/53/56 mm wheels and original deck envelopes in the
brief's ranges. Seed 3 adds 3.175 mm risers. The alternate seeds measure **11,602 / 11,582 / 11,940 triangles**; their GLBs
are **397,368 / 396,040 / 409,512 bytes**. `make check-variants` measures all
three alternatives, including deck → pad → plate supports on the riser seed.

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

Default cup centers are `(0, ±234.55, 73)` mm. World steering axes are approximately
`(0, +.80961, −.58697)` front and `(0, −.80961, −.58697)` rear: **35.94° to
the deck plane**, measured from actual pivot matrices. The kingpin itself is
20° from vertical toward its axle. To demonstrate a coordinated carve, apply
front `+angle` and rear `−angle`, so both wheel banks agree and their steering
yaws oppose. This conservative ±12° range is an authoring estimate, not a
manufacturer stop specification.

For a wall at world Y=0, outward normal +Y, align `Socket_Rest_Wall` to a target
rotated −90° around X, at Z=`wall_alignment_height_m` from its extras. The whole
board then leans 78° with its measured lowest surfaces on floor Z=0 and wall
Y=0. `build/check.json` names the actual contact meshes; the dedicated render
uses the same complete socket alignment. Moving the target carries the board.

## Rebuild and verification

Installed Blender 5.2, Python/Pillow/NumPy, GNU make, Noto Sans and flock.
Only cited photos/PDFs are downloaded; no packages, models, materials or lighting.
All Cycles work holds the kit GPU lock and uses OptiX/CUDA when available.

```sh
make                         # refs, model/GLB, checks, Cycles, photo pairs, sheets
make check                   # construction, normals, motion, fresh import, sections, repo rules
make repeat                  # independent factory-startup rebuild; exact GLB bytes
make check-variants           # all three alternate dimensions and riser supports
make variant-renders         # alternate GLB heroes, plus widest seed's side
make PASS=another WIDTH=1200 SAMPLES=32
make clean                   # generated build/renders only; references stay cached
make                         # rebuild from scripts
```

Checks separate **physical construction** from **serialization**. Actual surfaces
measure thickness, concave, kick angles, through holes, bushing-seat thickness,
static nut clearance, supports and wall/floor contacts. Kit BVH/solid-parity
sweeps test both hangers every 1° and all four wheels every 15° through 360°.
Only the two urethane bushings and retained rubber pivot interface are allowed
compliant contacts; metal interference is rejected. Sweeps are sampled checks,
not continuous collision detection. Fresh GLB import separately verifies all
meshes, counts, bounds, normals and complete pivot/socket matrices.

| Generated local path | Contents |
| --- | --- |
| `build/skateboard.glb` | Form-checkpoint glTF binary; temporary factors, no textures |
| `build/skateboard.blend` | Original game parts and retained dense castings |
| `build/check.json` | Measured construction, motion, normals, wall rest and GLB preservation |
| `build/sections.json` | Actual dense/game triangle-plane intersections |
| `build/cameras.json`, `build/photo-balance.json` | Fits, residuals and neutral assumptions |
| `renders/checkpoint/hero.png` | Three-quarter Cycles hero on concrete in raking sun |
| `renders/checkpoint/contact.jpg` | All requested Cycles views, wall rest and scale |
| `renders/checkpoint/matched-pairs.jpg` | Three period complete-board comparisons |
| `renders/checkpoint/cast-sections.jpg` | Three sections through each dense/game casting |
| `renders/checkpoint/steering.jpg` | Coordinated −12 / 0 / +12° demonstration |
| `renders/checkpoint/` | Top, bottom, side, front, concave, truck/inner truck, wheel/bearing, tail/grip edges, scale, wall rest |
| `renders/checkpoint/values.json` | Display-value tonal ranges; not recovered albedo |

[REVIEW.md](REVIEW.md) records the critique rounds and unresolved limits. The
mini close-up fit is approximate; complete-board photo dimensions are unknown,
so they are normalized to the default class. Macro views still expose 28-sided
wheel silhouettes and some reduced-casting facets. These and the unchamfered
small hardware need the next normal-map/finish stage. No photoreal final,
causal wear, graphic or texture-delivery approval is implied by this checkpoint.
Original scripts and quick materials are ours; photographic credits stay in the
reference register. No docs images are committed before final approval.
