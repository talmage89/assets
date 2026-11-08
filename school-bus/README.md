# Morrow C75 school bus — round 2 look checkpoint

An original late-2000s American Type C conventional, with a 75-child seating
layout and three fictional district/fleet seeds. Built entirely by scripts
in Blender 5.2. This round develops the compound fiberglass front, cabin,
glass, enamel and service wear, then checks the external-image glTF under
Cycles. It stops before final documentation images and a README gallery.

The body has split-sash windows, four pressed rub rails, sheet seams and
normal-baked fasteners, roof caps, two roof hatches, a genuine entrance and
stairwell, rear and left-side emergency exits, dual rear tires, chassis rails,
springs, axles, service doors, exhaust, mud flaps, brackets, mirrors, stop arm
and crossing gate. Twenty-five padded three-place benches, an aisle, driver
station, controls, steering wheel, barrier, ceiling and lamps provide actual
interior parallax. Nothing is a photographic card or downloaded asset.

[Measurement basis and cited standards](REFERENCE.md) ·
[Photo/source register](refs/SOURCES.md) · [Critique log](REVIEW.md)

The original package targets **12.192m bumper length, 2.4384m steel body
width, 3.2004m roof and 6.9342m wheelbase**. Mirrors, rub rails, strobe and
other equipment extend that nominal envelope. Actual surface measurements,
triangle allocation and delivery bytes are rebuilt into `build/model-check.json`
and `build/delivery-101.json`; they are reported separately from design targets.

| Datum | Measured surface / pivot result | Basis |
| --- | ---: | --- |
| Bumper length | 12.192000 m / 40 ft | Brief; within AM-VIS-0710 conventional range |
| Steel body width | 2.438400 m / 96 in | Original package; AM-VIS-0710 lists 96 in exterior |
| Steel roof height | 3.200400 m / 10 ft 6 in | Brief's original package |
| Wheelbase | 6.934200 m / 273 in | AM-VIS-0710 72/77-place package |
| Full rest equipment envelope, W × L × H | 3.350 × 12.3005 × 3.330 m | Actual mirrors, lamps/arms and strobe included |
| Cushions / aisle | 0.990600 m each / 0.323400 m clear | 39-inch three-child benches; actual mesh bounds |
| Seat row pitch / minimum clear back spacing | 0.670 m / 0.614 m | Actual horizontal sections; 2010 NSTSP 24-inch recommendation |
| First tread / three tread rises / landing rise | 0.354 m / 0.210 m / 0.196 m | Actual walking faces; NSTSP step recommendation |

The rub-rail crowns reach 2.500 m wide, beyond the nominal 96-inch steel
body. Thus the rail envelope is 61.6mm wider than that published nominal
exterior width; this checkpoint makes that packaging difference explicit.
Track, overhangs and the cowl/door/window layout are original estimates,
not measurements attributed to a maker. See [REFERENCE.md](REFERENCE.md) for
the period 2010/2015 NSTSP and 2012 CFR FMVSS 111, 131, 217 and 220–222 basis.

## Geometry allocation

| Allocation | Triangles |
| --- | ---: |
| Body, glazing, lamps and chassis, excluding wheels | 43,658 |
| Six tires, steel wheels, hubs and lugs | 25,632 |
| Exterior subtotal | **69,290** / 70,000 |
| Interior | 17,264 |
| Total, each seed | **86,554** / 90,000 |

Fine sheet fasteners, roof laps, tread, corrosion and scratches are baked
fields. Geometry carries the six tire silhouettes, graded wheel lips,
compound hood/fender sections, window construction, actual openings and
mechanisms. The per-source-mesh and per-pivot counts are in
`build/model-check.json`; fresh imported mesh counts are in each
`build/delivery-<seed>.json`.

The hood/fenders share a supported subdivision cage and a 6 mm laminate.
The dense level-3 mold supplies baked curvature; routed lamp-opening returns
keep their exact mesh normals. Bowed clear covers sit ahead of formed
reflectors inside hollow buckets. Actual transverse section cuts and optical
intersection checks accompany the front renders. Concealed wheel detail pays
for the front and rounded, crowned cabin upholstery without exceeding either
triangle allocation. Gray inner lining, rubber coves and folded step pans
replace the exterior-yellow cabin surfaces.

The same total by exported group (carriers exclude their wheel children):

| Group | Count × triangles | Subtotal |
| --- | ---: | ---: |
| Static `SchoolBusMesh`, including cabin | 1 × 57,282 | 57,282 |
| Entrance leaves | 2 × 472 | 944 |
| Rear emergency door | 1 × 734 | 734 |
| Side emergency door | 1 × 550 | 550 |
| Roof hatches | 2 × 228 | 456 |
| Steering carriers | 2 × 92 | 184 |
| Front wheels | 2 × 4,656 | 9,312 |
| Rear outer wheels | 2 × 4,656 | 9,312 |
| Rear inner wheels | 2 × 3,504 | 7,008 |
| Stop arm | 1 × 616 | 616 |
| Crossing arm | 1 × 156 | 156 |
| Total | 17 mesh groups | **86,554** |

## Export and runtime use

`export/C75-101.gltf`, `C75-102.gltf` and `C75-103.gltf` each have a matching
`.bin`. Retain their relative `shared/` image paths or remap them through a
content cache. All three reference **one shared 2048² BaseColor / OpenGL +Y
Normal / ORM atlas**, including interior, tires and glass. The source fields
are GPU-baked at 4096 and channel-filtered to 2048. This is approximately
**16 MiB** with full mips and three 8bpp block-compressed maps; PNG bytes and
mesh buffers are separate. Four car-family surfaces distinguish paint,
opaque fittings/interior, transmissive glass and switchable lamps. Paint needs
its clearcoat response separately from rubber/vinyl; glass and switchable
emission account for the other two bindings. All four sample the same images.
The standard glTF clearcoat roughness also reads ORM green, so deposited dirt
does not retain the clean coating's narrow highlight. This reuses the existing
texture and UVs; it adds no image or material.

The car family does not ship a standalone tire/glass image set. This checkpoint
imports its original tire, glass, paint and lamp generators and atlas methods;
the accepted car files and deliveries are unchanged. Six truck tires share the
same manufacturing field. Fleet lettering occupies guarded charts in this
same atlas. The age variants additionally use a small, physically restricted
lower-body vertex-color layer; they do not allocate extra textures.

Fresh imported delivery sizes, in bytes:

| Payload | Seed 101 | Seed 102 | Seed 103 |
| --- | ---: | ---: | ---: |
| glTF | 53,344 | 53,345 | 53,344 |
| BIN | 9,182,716 | 9,182,716 | 9,182,716 |

The shared images total **5,626,289 bytes**: BaseColor 1,499,157,
Normal 1,611,875 and ORM 2,515,257. PNG storage size is distinct from the
16 MiB GPU estimate. All three seeds contain their own six district, fleet
and plate planes. Imported UV coverage is 35.35%, with p5/median/p95 density
35.86/65.63/120.93 px/m and zero overlaps or out-of-bounds triangles. The source
pack covers 37.09%, including all three guarded lettering regions. Entrance
treads and the first two bench rows receive extra priority in this same atlas.
Fine fasteners remain softer than the source; this is a conservative many-chart
pack, not an optimal utilization claim.

| Seed | Fleet | District | Age / wear |
| --- | --- | --- | --- |
| 101 | 218 | Cedar Vale Schools | 3 years / .46 |
| 102 | 307 | North Creek District | 4 years / .67 |
| 103 | 164 | Oak Hollow Schools | 5 years / .84 |

Meters, Blender +Z up and −Y front; glTF +Y up and +Z front. The origin is the
center of the bumper footprint at grade. Retain the hierarchy and material
bindings. There is no armature or baked animation. Local authoring axes below
become glTF Y for Blender Z; X stays X. Ranges are from closed/rest.

| Pivot | Axis / degrees | Construction |
| --- | --- | --- |
| `Entrance_front`, `Entrance_rear` | Z, 0…98 / −98…0 | Outward leaves on opposite jambs; axes 34mm outboard of leaf planes |
| `Emergency_rear` | Z, 0…105 | Rear exit, true vertical hinge |
| `Emergency_side` | Z, −105…0 | Forward edge hinge, left side |
| `Roof_hatch_front`, `Roof_hatch_rear` | X, −80…0 | Actual roof openings, rear hinges |
| `Stop_arm` | Z, −90…0 | Driver-side vertical pivot |
| `Crossing_arm` | Z, −90…0 | Entrance-side bumper pivot, forward deployment |
| `Steer_FL`, `Steer_FR` | Z, ±40 | Front steering carriers |
| Six `Wheel_*` nodes | X, full revolution | Dual rear tires turn separately, on coaxial spindles |

`Socket_Driver`, `Socket_Door`, 25 bench sockets and 75 passenger-place
sockets are separate empties. Their actual positions and all pivots are in
the model report. The circular tire is a mean loaded envelope, preserving
ground contact while turning; it does not simulate carcass deformation.

Lamps default **off** in stock glTF. The car-family BaseColor-alpha convention
stores source power divided by 80. [lamp_states.py](src/lamp_states.py) reads
only delivered images and exposes red, amber, headlight, dome and strobe
uniforms. The warning proof selects red and strobe with amber off. Flash timing
belongs to the game. No additional emission image is required.

## Rebuild and evidence

```sh
make -C school-bus             # complete checkpoint, serial Blender jobs
make -C school-bus check       # source, motion, UV, imported meshes, magenta, preservation
make -C school-bus export      # all three glTF/BIN files and shared images
make -C school-bus render      # exported gallery, source/export photo pairs and Eevee
```

The hero reads native `school/export/Campus-102.gltf` and its relative payloads.
The original single-socket fit proof also reads `Campus-101.gltf`. These are
read-only presentation/check inputs; the bus builder, UV, bake and exporter
do not depend on either. Additional native tree instances share their original
data. Procedural distant understory candidates are rejected by actual ground
rays on roads, walks and roofs. No school payload is edited or re-exported.

Every Cycles bake/render uses the kit's shared GPU lock. Scratch files remain
under this worktree's `build/`. The Makefile includes the shared checkpoint
rules, imports the sedan's chart-repair finalizer and uses its frozen-coordinate
bake preparation. The original grille has a recessed surround and open webs.
No shared kit or car generator is changed.
CPU construction/import/camera audits run before one serial GPU render batch;
photo-pair composition runs after that batch releases the lock. A calibration
change refreshes only the eight photographic comparisons in a separate GPU turn;
the verified gallery stays cached.

| Generated evidence | Contents |
| --- | --- |
| `renders/checkpoint/hero.png` | Eye-height 44mm Cycles view in native school 102's loading lane, with two queued seeds |
| `renders/checkpoint/turnaround.jpg` | Front, side, rear, top |
| `renders/checkpoint/front_detail.png` | Hood, recessed grille, sealed lamps and supported mirrors |
| `renders/checkpoint/entrance.png`, `interior.png`, `aisle.png`, `aisle_daylight.png`, `side_interior.png` | Steps, door and side-pane interior views, original aisle camera and adult-height daylight aisle |
| `renders/checkpoint/warning.png` | Deployed arms and red warning state |
| `renders/checkpoint/emergency.png`, `roof.png` | Rear exit and open roof lids |
| `renders/checkpoint/scale.png`, `fleet.png` | 1.8m adult and 1.1m child; three actual seed exports |
| `renders/checkpoint/contact.jpg` | Complete review contact sheet |
| `renders/matches/`, `renders/source-matches/` | Four neutral-balanced service-photo pairs, including two makers' fronts and a used long body's side |
| `renders/round2-repairs/` | Native same-camera before/after comparisons; originals remain archived |
| `renders/round2-front-final/` | Actual five-station transverse triangle cuts |
| `renders/seethrough/` | Six imported-delivery magenta tests, envelope masks and counts |
| `renders/eevee/hero.png` | Eevee transmission preview |

The legacy school-101 sockets reserve 11m buses at 12m centers; blindly using
both would overlap this 40ft vehicle's bumpers. Parked buses need at least
**12.5m centers**; deployed crossing loops need **14.35m** for a 0.2m game-scene
gap. The school-102 presentation uses 12.6m longitudinal spacing, with the
rear bus angled into the actual east transition. All 18 tires meet native
asphalt, and 27 transformed body-envelope probes stay inside the corridor
(maximum measured offset 3.3282m; corridor half-width 3.6576m). Original socket
and actual staged-fleet proofs are separate: `build/school-fit.json` and
`build/school-stage.json`.

`build/checkpoint-check.json` gathers the independent reports. Construction
checks measure the actual surfaces: 153 supported joints, 48 walking-surface
probes, a 0.614m minimum seat/back clearance, and 508 sampled poses across
16 mechanisms. The only motion exceptions are the two intentional spindle
interfaces. Fresh imports separately verify all 17 mesh groups, zero duplicate
or bad-normal faces, the UV layout and 178,639 bidirectional vertex samples
per seed, with zero vertex/pivot displacement. A separate check measures all
36 marking corners against the intended source variant's positions and UVs.
Those import comparisons prove
serialization; they do not substitute for the construction measurements.
Six direct magenta views report zero resolved leak pixels. All 335 other assets' delivery
and documentation files in the round's preservation manifest retain their
hashes, including the 56 pre-existing native school payloads.

The 4096 bake checks 5,211,610 interior atlas texels per channel, with
zero unfilled base texels, missing alpha or reversed normal hemispheres.
The 6,198-triangle hood receives normals from an independent 86,612-triangle
dense mold: 99.882% measured surface projection coverage, with exact mesh
normals retained on narrow routed returns. Missing projection beyond 1% fails
the bake. Independent builds compare 1,155 objects' exact geometry, canonical
oriented topology, bindings, transforms and metadata; the measured maximum
smooth-normal component rounding is 1.19×10⁻⁷ against a 10⁻⁶ tolerance.
Presentation receipts identify actual delivery hashes, pose deltas and scale
heights; `src/review.py` rejects stale or incorrectly posed evidence.

The remaining CG tells are described in [REVIEW.md](REVIEW.md): simple
warning/taillamp optics and driver controls, softened lettering and fine
fastener relief in the shared atlas, and some regularity in the roof runoff.
The cabin supports exterior views rather than a fully playable interior.
These are look-checkpoint limitations; final documentation remains deferred.

No checkpoint image is committed as final documentation. Review images and
build products regenerate from scripts. Procedural sun/sky supplies all light;
fonts are installed Noto Sans through `kit/fonts.py` (SIL OFL). The standards
inform visual construction; these meshes are not a vehicle safety certification.
