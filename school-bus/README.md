# Morrow C75 school bus — form and construction checkpoint

An original late-2000s American Type C conventional, with a 75-child seating
layout and three fictional district/fleet seeds. Built entirely by scripts
in Blender 5.2. This delivery stops at the requested **form and construction
checkpoint**: UVs, preliminary baked materials, external-image glTF and
exported Cycles evidence. Final coating/wear development remains separate.

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

## Export and runtime use

`export/C75-101.gltf`, `C75-102.gltf` and `C75-103.gltf` each have a matching
`.bin`. Retain their relative `shared/` image paths or remap them through a
content cache. All three reference **one shared 2048² BaseColor / OpenGL +Y
Normal / ORM atlas**, including interior, tires and glass. The source fields
are GPU-baked at 4096 and channel-filtered to 2048. This is approximately
**16 MiB** with full mips and three 8bpp block-compressed maps; PNG bytes and
mesh buffers are separate. Four car-family surfaces distinguish paint,
opaque fittings/interior, transmissive glass and switchable lamps.

The car family does not ship a standalone tire/glass image set. This checkpoint
imports its original tire, glass, paint and lamp generators and atlas methods;
the accepted car files and deliveries are unchanged. Six truck tires share the
same manufacturing field. Fleet lettering occupies guarded charts in this
same atlas. The age variants additionally use a small, physically restricted
lower-body vertex-color layer; they do not allocate extra textures.

| Seed | Fleet | District | Age / preliminary wear |
| --- | --- | --- | --- |
| 101 | 218 | Cedar Vale Schools | 3 years / .46 |
| 102 | 307 | North Creek District | 5 years / .67 |
| 103 | 164 | Oak Hollow Schools | 7 years / .84 |

Meters, Blender +Z up and −Y front; glTF +Y up and +Z front. The origin is the
center of the bumper footprint at grade. Retain the hierarchy and material
bindings. There is no armature or baked animation. Local authoring axes below
become glTF Y for Blender Z; X stays X. Ranges are from closed/rest.

| Pivot | Axis / degrees | Construction |
| --- | --- | --- |
| `Entrance_front`, `Entrance_rear` | Z, 0…98 / −98…0 | Outward leaves on opposite jambs |
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

Every Cycles bake/render uses the kit's shared GPU lock. Scratch files remain
under this worktree's `build/`. The Makefile includes the shared checkpoint
rules, imports the sedan's chart-repair finalizer and uses its frozen-coordinate
bake preparation. The front grille imports the hatchback's open-web method.
No shared kit or car generator is changed.

| Generated evidence | Contents |
| --- | --- |
| `renders/checkpoint/hero.png` | Eye-height 40mm Cycles view of the export in native school 101's lane |
| `renders/checkpoint/turnaround.jpg` | Front, side, rear, top |
| `renders/checkpoint/front_detail.png` | Hood, recessed grille, sealed lamps and supported mirrors |
| `renders/checkpoint/entrance.png`, `interior.png`, `aisle.png` | Open leaves, steps, driver view through the door, separate cabin view |
| `renders/checkpoint/warning.png` | Deployed arms and red warning state |
| `renders/checkpoint/emergency.png`, `roof.png` | Rear exit and open roof lids |
| `renders/checkpoint/scale.png`, `fleet.png` | 1.8m adult and 1.1m child; three actual seed exports |
| `renders/checkpoint/contact.jpg` | Complete review contact sheet |
| `renders/matches/`, `renders/source-matches/` | Three neutral-balanced Commons photographic pairs at calibrated cameras |
| `renders/seethrough/` | Six imported-delivery magenta tests, envelope masks and counts |
| `renders/eevee/hero.png` | Eevee transmission preview |

The native school sockets reserve 11m buses at 12m centers. This 40ft vehicle
fits the first straight-curb position. Two buses need at least **12.5m center
spacing**; blindly using both original sockets would overlap their bumpers.
The school files are unchanged. Actual lane contact rays are in `build/school-fit.json`.

No checkpoint image is committed as final documentation. Review images and
build products regenerate from scripts. Procedural sun/sky supplies all light;
fonts are installed Noto Sans through `kit/fonts.py` (SIL OFL). The standards
inform visual construction; these meshes are not a vehicle safety certification.
