# Propane Defense Harrow 56

An original scripted **belt-fed 5.56×45 light machine gun** visual game asset.
Fixed molded stock, folding/extending bipod, folding barrel carrying handle,
200-round detachable box and a curved train of individual display rounds/links.
Maker, model, serial and marking masks are fictional. Every mesh comes from
our Blender scripts; reference images are comparison material only.

**Form checkpoint, before look-dev.** This folder deliberately uses the kit's
checkpoint graph. Current GLBs carry seven quick inspection materials and no
textures. They are not final deliveries. No baked wear, UV acceptance, lossless
texture subsets or final docs JPGs are claimed.

Open [the contact sheet](renders/checkpoint/contact-sheet.jpg), the exact eye view at
[aimed.png](renders/checkpoint/aimed.png), [sections](renders/checkpoint/sections.jpg),
[dimensioned orthographic views](renders/checkpoint/orthographic-dimensions.jpg), the five pairs under `pairs/`,
and the real-duration strips/playbacks under `strips/`. All main stills and
strips load `build/lmg.glb`; five standalone views load their own GLBs.
[REVIEW.md](REVIEW.md) records the image critiques and remaining weaknesses.

## Dimensions and construction

The authored overall target is **1,040 mm**, with a **465 mm barrel exterior
span**, against the published fixed-stock class and long-barrel option.
The **7.5 kg** empty target is nominal: this visual mesh is not a mass model.
Photographic variants differ in stock, handguard, sights and barrel furniture;
our own forms do not reproduce a particular product.
[Sources, credits and licenses](refs/SOURCES.md) distinguish manufacturer data,
period published data and exterior photographic evidence.

Actual bounds and sight-ray results are generated in `build/measurements.json`;
actual imported triangle intersections and dimensions are in
`build/sections.json`. Section views cover receiver/tray, receiver/trigger,
two handguard stations, two stock stations, three grip heights, box, cover
and guard. A folded sheet shell has a visible open interior and finite wall;
its rails and exterior rivets remain separate inspectable source parts.

| Actual source surface measurement | Millimeters |
| --- | ---: |
| Overall length / reference target | 1,040.000 / about 1,040 |
| Barrel exterior span / selected published option | 465.000 / 465 |
| Loaded, stowed envelope, width × height | 169.242 × 283.000 |
| Receiver shell, width × length × height | 48.000 × 293.000 × 67.000 |
| Cover, width × length × height | 60.000 × 293.999 × 21.000 |
| Handguard, width × length × height | 65.322 × 243.940 × 65.243 |
| Box shell, width × depth × height | 127.752 × 120.752 × 130.000 |

The latter five are original design dimensions, measured from the mesh; the
references do not publish those individual dimensions. The 1,040 mm target is
1.9 mm longer than the cited period 1,038.1 mm envelope. No inferred mass is
reported as a measurement.

The same report measures first-person relationships on the posed surfaces:
cover overhang **6.00 mm per side**; rear aperture center **31.00 mm above the
cover crown**; front post tip **71.00 mm above barrel center**; rear rim to
post **558.50 mm**; carrying-grip inboard edge **34.00 mm outboard of the
sight plane**; charging paddle **27.00 mm beyond the receiver wall**;
handguard front **33.03 mm behind the barrel collar**; and box lid **13.00 mm
below the receiver floor**. These are original form relationships, separate
from the eight surface seating measurements and the unobstructed sight ray.

Stock, grip and handguard use supported changing-section subdivision cages.
The dense molds are retained in the hidden `High_Sources` collection for the
later normal bake. The game forms are reduced from those surfaces; they are
not flat side-profile extrusions. The lower handguard is an open finite-wall
U. The guard is a broad band. The trigger's concave front faces +Y and its
blunt lower toe curls forward. The cover has a finite shell, left feed opening,
rear release tabs, underside display pawls and a separately owned tray.

The barrel/gas group has exterior collars, a windowed sight tower, open hood,
centered front post, a slotted flash-hider envelope, regulator and heat shield.
The carrying handle stays outboard of the optical ray when folded. Channel
bipod legs carry separate telescoping extensions, detent witnesses and feet.
The box is a finite-wall bin with lid, hinge, mouth and suspension/latch seats.

This is an **inert exterior visual asset**. Bolt/operating-rod displays are
simple animation owners. There is no operative chamber, bolt locking system,
firing pin, sear or gas port. Hidden chamber occupancy has a bone but no render
mesh. Ammunition has solid decorative bases and no working primer geometry.
Links are original decorative cuffs/webs, not validated mechanical interlocks.
Checks establish visual fit, state and export continuity, not weapon function.

## Frame, rig and clips

Meters, palm origin; Blender **+Y forward, +Z up, +X right**; glTF **−Z
forward, +Y up**. Root is identity throughout. Whole-instance movement belongs
to the game. [Interface supplement 1.8.0](INTERFACE.md) is additive; existing
family meanings and the parallel 1.7 binding are unchanged.

Capabilities: belt feed, detachable box, open bolt, nonreciprocating handle,
bipod, automatic only, no empty hold-open. There are **64 bones, 12 sockets
and 19 clips**. Source pivots are declared together in [src/build.py](src/build.py).
The two bipod splay shoes have explicitly bounded visual seating; all other
cross-owner pairs use the ordinary 0.2 mm penetration limit.

| Group | Axis / authored visual range |
| --- | --- |
| FeedCover / rear latch | X, 0–−96° / +Z release |
| Bolt and operating rod | −Y, 80 mm; rear at ready, forward empty |
| ChargingHandle | −Y, 80 mm, independent of firing |
| Trigger / safety | X, −12° / X, 5 mm push-button |
| CarryHandle | Y, 0–−65° |
| Bipod fold / splay / extension | X, 85° / local Z, ±18° / local −Y, 65 mm |
| Magazine / BoxLid | full detachable frame / Y, 100° |
| ShoulderRest | X, 65° in Inspect |
| BeltLink00…18 / BeltRound00…18 | planar guide / parallel +Y cartridge axes |

Idle, IdleEmpty, IdleSafe, Fire, Burst, CeaseFire, FireLast, Reload,
ReloadEmpty, Charge, BipodDeploy, BipodFold, SafetyOn, SafetyOff, CarryRaise,
CarryFold, BoxOpen, Inspect and BeltEnd have complete poses and explicit holds.
Ammunition visibility is STEP. The bolt is rearward in ready; FireLast ends
forward and empty; a ceased burst returns rearward. Empty reload exchanges
boxes and then charges. Ordinary reload lifts the belt before the box leaves.
These are authored visual timings; a game owns rates, effects and bookkeeping.

`Socket_Magazine` retains the complete box spawn frame. The charging-handle,
box-mouth and cover-hand sockets ride their owners. The six base static
references keep their original paths. `Socket_Eye` is exactly on the aperture
and post line; the aimed camera adds no presentation offset. Eye relief is
currently a provisional artistic estimate, **not a measured cheek weld**.
The downloaded aiming candidates are unsuitable for that measurement; see
REVIEW. The source ray test separately establishes a clear sightline.

The belt uses one cartridge and one link mesh, rigidly bone-parented as shared
instances. Blender's linked mesh deform groups cannot encode different owners;
ordinary skinned binding incorrectly made every copy follow the final bone.
The retained instance approach is tested on actual deformed meshes after import.
`src/belt.py` solves equal center chords, masks the remaining end and supplies
an optional cyclic owner helper for gameplay. Engine integration must occlude
the box-end recycling region. Baked-clip interpolation error is measured
separately; the guide is an authored hanging curve, not a gravity simulation.

## Budget and delivery gate

The ceiling is **48,000 evaluated scene triangles**, including the visible
belt and staged effect owners. `build/triangles.json` measures the current
allocation and each standalone. The unique raw GLB mesh count is lower because
cartridges/links are instanced; do not mistake that for the rendered count.
`build/serialization.json` records actual bytes, clip durations, material count,
source/import affine errors, evaluated surface errors and imported clearance.

| Checkpoint GLB | Scene triangles | Bytes |
| --- | ---: | ---: |
| Gun, staged belt and effect owners | **47,760** | **3,529,940** |
| Loaded box | 5,564 | 146,136 |
| Empty box | 2,668 | 65,116 |
| Cartridge | 896 | 23,204 |
| Fired case | 704 | 18,776 |
| Link | 276 | 11,196 |

The gun stores 34,728 unique raw mesh triangles, seven inspection materials
and zero textures. This higher temporary material count is confined to the
unbaked checkpoint. `make check` passes: no nonmanifold meshes; 802 source and
1,538 fresh-import motion samples with zero violations under the declared
bounds; eight visible surface seats; 155 affine comparisons and five evaluated
surface poses. Maximum source/import position error is 0.000167 mm. Maximum
sampled belt spacing error is 0.0873 mm. These checks establish the reported
visual fit and serialization, with the limits recorded in REVIEW.

Final delivery, after the form gate, is planned through the kit's existing
UV/bake/export path: one 4096 bake downsampled to a **2048 BaseColor / OpenGL
Normal / ORM** set, about **16 MiB** with compressed full mip chains. Loaded
and empty boxes will request lossless 1024 subsets, cartridge/case/link 512,
using `texture_size` and the shared detachable sampling checks. Packing will
fail rather than lower density. These textures have not been generated.

`src/markings.py` prepares original **PROPANE DEFENSE / HARROW 56 /
PD-H56-029014** and **PD / 56 / 29** headstamp masks with Noto Sans. They
are pending a normal bake, not embedded in this unbaked checkpoint. Planned
wear remains site-driven: matte-gray cover/receiver rubs, handled carrying
handle, carbon confined to muzzle/regulator/ports, scraped feet, scuffed box
corners and rubbed shoulder rest. No finish approval is requested here.

## Rebuild

Requires the repository's installed Blender 5.2, Python/Pillow/NumPy, Noto
Sans, GNU make and flock. No packages, models, textures or HDRIs are downloaded.
All scratch stays in `build/`; Cycles uses the kit's shared GPU lock.

```sh
make -C guns/lmg                  # complete form checkpoint, then stop
make -C guns/lmg check            # source and fresh-import motion/serialization
make -C guns/lmg sections pairs strips extra
make -C guns/lmg dimensions evidence review-all
python3 guns/lmg/src/test_belt.py # branch-pop/count/owner-continuity regressions
```

Generated source, GLBs, renders, textures and downloaded references remain
ignored. Nothing in `kit/`, existing common modules or other guns changes.
New [common/ammo556_visual.py](../common/ammo556_visual.py) supplies only
inert original visual silhouettes; [common/interface_v1_8.py](../common/interface_v1_8.py)
checks the additive belt states and capabilities. Future finished docs will be committed only
after acceptance, as the repository contract requires.
