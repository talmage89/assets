# PD Covey 26 — boxlock side-by-side shotgun

An original script-built 12-gauge field shotgun: 26-inch joined barrels,
double triggers, extractors, right-swinging top lever, automatic tang safety,
straight-hand walnut stock and splinter forend. Fictional maker/model:
**Propane Defense Covey 26**.

**Form round 6, with baked normals; finish/look-dev remains held.** The gun
uses one baked 2048 BaseColor / OpenGL Normal / ORM atlas, from a 4096 GPU
bake of our original dense sources and inspection constants. The forging's
normal projection is evaluated directly from the dense source through the
game mesh's tangent basis. Checkering, grain,
markings, used finishes and final delivery acceptance remain held. No docs
images are committed at this gate.
Generated image paths below are local build outputs, not hosted README images.

## Dimensions and design

| Quantity | Evaluated visual geometry | Published class / design anchor |
| --- | ---: | --- |
| Overall length | 1079.95 mm | brief: about 1080 mm |
| Barrels, rear face to muzzle | 660.40 mm / 26 in | published 26-inch option |
| Overall width / height | 52.20 / 174.34 mm | corrected fence/side envelope; original straight stock |
| Front-trigger length of pull | 369.63 mm / 14.55 in | published 365 mm; original stock is 4.63 mm longer |
| Comb / heel drop | 38.02 / 63.03 mm | published 38 / 63 mm; measured against an actual rib-centerline datum (concave edges rise about 0.22 mm) |
| Cheek station | 35.00 mm behind comb nose | published range 31.75–38.10 mm |
| Eye above actual comb | 42.81 mm | actual surface ray; CPSA coin-rule sight picture, derived below |
| Eye optical pitch | −0.374° | exact line from the socket to the bead |
| Wrist, wood only at Y = −15 mm | 32.20 × 37.89 mm | sharp top/side photographs; absolute reference scale remains uncertain |
| Splinter wood, overall W × D × L | 34.40 × 24.20 × 172.99 mm | plain field photographs; evaluated mesh dimensions, not published part measurements |
| Splinter sections at Y = 211 / 320 mm | 34.16 × 22.54 / 28.24 × 16.16 mm | actual triangle-plane cuts, with barrel channels |
| Ammunition class | 12 gauge, nominal 2¾ in | nominal opened-hull length |
| Unloaded mass | target 3.2 kg, **unmeasured** | field-gun design class; no mass simulation |

The [published class specifications](https://www.ugartecheashotguns.com/shotguns/specifications/)
offer the boxlock, double triggers, extractors, 26-inch barrels and splinter
forend together. Their 38/63 mm comb/heel-drop baseline informs the original
stock. A straight hand keeps the field silhouette lean and permits shifting
the hand between triggers. The slightly longer measured pull is a disclosed
original-design difference. Installed fonts will be found through `kit/fonts.py`
when original markings are added; no real markings or engraving are copied.

The [primary cheek-station instructions](https://www.brownells.com/userdocs/learn/076-200-548_Pull___Drop_Gauge.pdf)
place the cheekbone 1¼–1½ inches behind the comb nose. The accepted station
remains 35 mm behind the nose, at Y=−123 mm. The
[CPSA handbook](https://www.cpsa.co.uk/userfiles/files/CTSH.pdf), printed p. 4-2,
checks a sporting sight picture with a pound coin on the rib 200 mm ahead
of the standing breech: the bead's center just clears the coin. The historical
[round pound is 3.15 mm thick](https://www.royalmint.com/collect/collector-resources/designs-and-specifications/one-pound-coin-designs/).
Extending that line from the actual rib surface and bead back to the accepted
cheek station gives eye Z=60.500 mm, 3.612 mm above the extended rib and
42.811 mm above the actual comb. The local comb drop there is 39.199 mm;
the accepted comb-nose drop remains 38.02 mm. This derives a fitted visual
sight picture; it does not claim an anatomical measurement of a human.

The local primary side-by-side manual supplies its illustrated exterior parts,
double-trigger order, forend iron and controls. Direct sources, photographic
authors/licenses and reference limitations are in `refs/SOURCES.md`.
Photo landmarks calibrate cameras only; no photo enters modeling or materials.

## Construction and frame

Meters, palm origin, Blender +Y toward the muzzle / +Z up / +X right;
glTF −Z forward / +Y up. Whole-instance stance and recoil are external;
internal Root stays identity. Preserve imported materials.

The wood comes from three-dimensional subdivision cages with changing width,
comb, cheeks, belly, wrist and end tapers. Dense originals remain in
`High_Sources`; the game copies are reduced after carving the seats/channels.
The forend has two barrel channels, a bottom-rib channel, iron pocket, inset
latch and curved knuckle cups. The stock has real tang inlets and a pitched
butt plate. Neither furniture piece is a side-profile extrusion.

The action is one closed forging with explicitly planar ground sides and
R6 side returns and one supported subdivision control net for the
upper head, filled to Z55.59 mm, with bore-concentric front arcs and a standing breech
with visible pin bushings. The table has a narrow visual lug passage over
a closed lower floor. A single ground side plane continues from the head to
the bar. The rounded underside and its flush trigger plate share an 8 mm lower
arris and sweep into the concentric knuckle; the hinge pin ends are thin flush
circles in the same steel. Rounded-end 6 mm slots clear the 5.4 mm trigger roots
by 0.30 mm on each side. Two hollow barrel skins meet on
cut joined flats at the breech, without overlapping outer walls, and have chamber-side rim recesses,
walls at the muzzle, joined solid top and bottom ribs, lower lumps/hook and a
two-pad extractor. A swept guard band and separate rear tang surround two tapered flat trigger
blades. Their working faces are concave toward the muzzle and their tips curl
forward. The top lever has a round 11.2 mm boss and a long, narrow tapered tail lying
close above the strap. Its thumbpiece is about 7.1 mm wide and 1.9 mm thick.
The guard is a 12.4 × 1.63 mm flat band with a swept front return and wrist tang.
The safety retains its compound thumb surface. Dense forging and thumbpiece
sources supply this round's normal bake. Checkering remains held.

This is exterior visual construction. Hidden hammers are state only. There is
no working lockwork, ballistics, pressure design or manufacturing model. Motion
angles, guide travel and running gaps are authored visual estimates.

| Moving assembly | Pivot / local axis, Blender mm | Visual range |
| --- | --- | --- |
| Barrels and forend | (0,170,19), X | 0 to −42° |
| Extractor | (0,115,44), rides Barrels | Y 0 to −10 mm |
| Top lever | (0,94,53), Z | 0 to +25°, toward the right |
| Front / rear trigger | (2.6,64,4) / (−2.6,31,4), X | 0 to −13° |
| Tang safety | guide at (0,5,23) | Y 0 to −5 mm, safe rearward |
| Visible locking shoes | (0,130,13), Y | 0 to −24 mm, withdrawn before opening |

The rear trigger root moved rearward by 12 mm to fit the photographed blade
spacing and revised guard. Its owner, pull direction, angle and left-barrel
assignment are unchanged. The front trigger and accepted pull are unchanged.

The forend rides Barrels, with its own named rigid owner and the same hinge
axis. Its cups bear on the concentric knuckle throughout the sampled swing.
The latch is an inset fixed presentation part; forend removal is not a clip.

## Rig, states and sockets

[Guns interface 1.7.0](INTERFACE.md) adds break action, two stable chamber IDs,
double triggers, automatic safety and no magazine. It reuses 1.4.0's
`loaded` / `fired` / `empty` states and 1.1.0's shell-guide frame. Right is
chamber 0 and the front trigger; left is chamber 1 and the rear trigger.
Each hammer is `cocked` or `rest` in the manifest.

Nineteen clips cover Idle, right Fire, FireLeft, Open/OpenLoaded, manual Unload,
Reload of two, ReloadSingle, Close, Safety/SafetyOn, Inspect, and seven explicit
state holds. `Fire → FireLeft → Open → Unload → Reload → Close → Safety`
returns to ready. Fired hulls stay in their chambers until the hand pulls them
axially clear. Incoming shells transfer visibility at the same seated pose.
Display children use STEP occupancy; guide bones never scale to zero.

No hand mesh ships. The held hulls/shells and complete guide frames provide
consumer hand-IK targets. An interrupted clip retains its exact frame and
state and resumes there; no jump to a closed Idle is promised.
Real-time WebPs and uniform 15-Hz frame strips accompany every clip.

Seven legacy socket names remain. Magazine/mag-well nodes are explicitly
inactive. SupportHand follows Forend; Shell and ShellL follow the nonscaling
right/left insertion guides; ChamberR/L follow Extractor; MuzzleR/L follow
their actual barrels. Eye sits at (0,−123,60.500) mm and points down 0.374° to
the brass bead; the exact 45 mm lens camera renders against gray. The supplement gives
spawn, visibility and event meanings.

## Budget and generated files

<!-- CHECKPOINT_STATS -->

| Inspection output | Triangles | GLB bytes |
| --- | ---: | ---: |
| Gun, all staged alternatives | 38,822 | 12,495,908 |
| Shell | 752 | 26,476 |
| Hull | 480 | 18,160 |

54 named rigid meshes, 17 bones, 19 clips, 14 sockets; 1 atlas material and **three 2048 texture images** (4096 GPU source bake).
<!-- /CHECKPOINT_STATS -->

All hidden ammunition alternatives count against the 39k round-six gun budget.
The shell module is new in `guns/common/shell12_visual.py`; no pump source or
output is imported. It preserves the pump's original exterior proportions:
22.4 mm rim, approximately 20.1 mm hull, 57.5 mm loaded length and 69.8 mm fired
length. Connected hidden joins make each shell a closed manifold skin.

| Local generated path | Contents |
| --- | --- |
| `build/sxs.blend`, `build/sxs.glb` | Native source and unbaked diagnostic export; not the rendered delivery |
| `build/shell.glb`, `build/hull.glb` | Separate head-centered exterior ammunition, +Y toward mouth |
| `export/sxs.glb` | Baked 2048 gun, named rigid parts, rig, clips and sockets |
| `build/delivery/finalized.blend`, `high.blend`, `uv.json` | Kit UV target, dense bake sources and atlas measurements |
| `build/baked/4k/`, `build/baked/precise4k/`, `textures/` | Original GPU bake, dense forging normal projection at 4096, delivered three-map 2048 set |
| `build/baked/precise4k/projection-report.json` | Measured source-plane fits, per-region projection distances, coverage and input/output hashes |
| `build/delivery/projection-ownership.json` | Independent check that constant albedos project from their own parts |
| `renders/checkpoint/pairs/aimed-pair.jpg`, `open-player-pair.jpg`, `open-breech-pair.jpg` | Exact player views beside rear/action photographs and calibrated comparisons |
| `renders/checkpoint/reflections/` | All five striped cameras in two directions; source/export sheets, before/after comparisons and native open-head crops |
| `build/fairness.json` | Dense-source topology, geometric normal-angle maxima with coordinates, and separate intended-edge measurements |
| `renders/checkpoint/head-raking-comparison.jpg` | Both lighting sides: original dense source beside the baked export |
| `renders/checkpoint/landmarks/` | Annotated right/top/bottom rakes with measured landmark arrows |
| `build/check.json`, `import-check.json` | Separate source/import topology, intended-state, contact and half-frame clearance reports |
| `build/serialization.json`, `repeat.json` | Baked-export affine/surface/atlas proof and independent native rebuild proof |
| `renders/checkpoint/contact-sheet.jpg`, `hero-gray.jpg` | Current Cycles inspection views from the exported GLB |
| `renders/checkpoint/dimensions.jpg`, `sections/sections.jpg` | Measured orthographic and triangle-plane sections |
| `renders/checkpoint/photo-pairs.jpg` | Twelve calibrated baked-export comparisons, native residual arrows and photo-outline overlays |
| `renders/checkpoint/clips.jpg`, `opening.jpg`, `strips/` | All clips, wide opening and correctly timed WebPs |
| `renders/checkpoint/ammunition.jpg` | Standalone shell and hull inspection |

The current gun embeds one three-map **2048** set and uses one material.
BaseColor and ORM are RGB8; the tangent normal remains RGB16 after the
kit's vector box filter. An 8-bit trial stepped the narrow mirror bands, so
this round retains the original bake precision without adding texels or maps.
The embedded normal PNG is 7,289,858 bytes; the GLB is 12,495,908 bytes.
A deterministic 4096 projection computes the forging's normals from its
original dense triangles in the actual game mesh's Mikk tangent basis.
Construction ownership keeps roof, lip, floor and end-cap projections separate.
Two planes fitted to the dense source supply 99 ground-side triangles;
source-plane RMS residuals are 0.000318/0.000290 mm, maximum 0.003410 mm.
The operation covers 555,222 interior texels. Maximum nearest-source distances
are 0.0973 mm on the roof, 0.0229 mm on the lip, 0.0053 mm on the floor,
0.0269 mm on the rear cap and 0.5374 mm on the remaining reduced forging.
It replaces selected-to-active directional noise without altering geometry
or material constants. All other parts retain their GPU normal bake.
The action uses exact pixel-center occupancy for its gutter; a conservative
mask protects every other part's occupied atlas area.
A consumer that block-compresses the maps uses about 16 MiB including mipmaps;
uncompressed RGB16 normal storage costs more and is importer-dependent.
At this form gate, 54 named rigid meshes remain for independent surface/contact
diagnostics. Consolidating
the delivery skin belongs to final acceptance. The accepted standalone shell
and hull stay in their unchanged diagnostic GLBs; their own small baked sets
remain part of the later finish delivery, rather than claiming they share the
gun's atlas.

The exterior gauges below use actual exported triangles, not nominal parameters.
Photo-scale estimates and their uncertainty are in `refs/SOURCES.md`.

| Quantity | Measured export | Photo / geometry relation |
| --- | ---: | --- |
| Right / left fence crown | 57.348 / 57.339 mm Z | barrel top 57.350 mm; reduction deviation at most 0.011 mm |
| Fence pair width | 51.895 mm | joined tubes at breech 51.900 mm |
| Front arc fitted radius, right / left | 13.358 / 13.316 mm | accepted R13.35 front arcs; extrapolated from the exposed sections |
| Largest arc-center offset from actual bore axis, right / left | 0.027 / 0.019 mm | outward front-arc fits; axes from actual chamber skin |
| Axial return length, right / left | 18.71 / 18.70 mm | photo 18–20 mm, about ±2 mm; equivalent reference-curve fit to the subdivision return |
| Drop behind right / left fence return | 7.603 / 7.603 mm | photo 5.6 ±3 mm |
| Drop at right / left side wood line | 12.958 / 12.950 mm | photo 12.5 ±3 mm |
| Drop at center wood line | 10.960 mm | photo 8.5 ±3.5 mm; lever occludes actual center |
| Center fill, outside lever recess | 55.5897–55.5904 mm Z | owner-specified 55.59 mm; actual rib-floor probe 55.585 mm |
| Side return radius, right / left | 5.893 / 5.896 mm | photo 4.5–7.5 mm, at least ±2 mm |
| Fence/head equivalent local radius, right / left | 7.182 / 7.182 mm | photo 4–8 mm, at least ±2 mm; Y96.5–102, X±12.6 mm |
| Upper head/strap equivalent radius, right / left | 7.017 / 6.976 mm | photo 4–8 mm, at least ±2 mm; Y92–94, X±10 mm |
| Inner return behind outer, right / left | 9.00 / 8.80 mm | photo 11.5 ±3 mm; 0.10 mm height-departure landmarks |
| Boss radial running clearance | 0.288–0.304 mm | R5.90 fore wall around R5.60 boss; fore semicircle at Z49 |
| Recess upper lip radius | 0.576 mm | photo roughly 0.25–0.75 mm, at least ±0.25 mm; circle fit error 0.008 mm |
| Minimum lever-swing gap | 0.157 mm | 0–25°, 0.5° steps; 51 angles, vertex/face and edge/edge surface distances, zero penetration |
| Largest head/bar side step | 0.000194 mm | one side plane |
| Largest plate/bar step | 0.00294 mm | both skins extrapolated to common seam station |
| Lower-edge radius | 7.981–8.009 mm | photo 7–9 mm, at least ±2 mm |
| Front / rear slot width | 6.000 / 6.000 mm | blades 5.400 mm; 0.300 mm clearance each side |

The center outline now follows Z55.59; the former Z49.72 notch is superseded.
The head uses the regular Catmull–Clark limit of one 35 × 18 quad control
net (324 independent height controls with symmetry). Supported front and side
loops retain the accepted circles and R6 return; physical curvature variation
and monotone slopes remove secondary humps. The integral R0.60 recess lip
shares its boundary vertices with the roof. It has no tangent Boolean join.
The rear relief stays below the accepted lever through its 0–25° swing. Compare the actual cuts at 3, 8 and 15 mm behind the face,
both bore-axis cuts, and `head-raking-comparison.jpg`.

The reflection test uses two perpendicular sets of procedurally generated
parallel bright bands at roughness 0.045, without denoising. Its five cameras
are the open player, top, exact aimed and both side rakes. The exported
normal map remains connected. `reflections/source-export-transverse.jpg`
and `source-export-longitudinal.jpg` show native head crops for every view;
`before-after-source-*.jpg` and `before-after-export-*.jpg` compare round five
with round six under the same cameras and bands. `open-head-before-after.jpg`
contains the ordinary player's native 450 × 300 crops. The audit verifies
current source/export hashes, normal-map retention and matching cameras,
resolution, band environment and diagnostic roughness.

Round-six preservation against `7d0ee67` finds 102 of 104 entries identical:
only the action and its stock inlet differ. All moving meshes, rig,
clips and sockets retain their prior geometry and keys. The inlet follows the
new rear head surface; the original lever and strap are identical. No material constants
changed. `REVIEW.md` records the image critiques and photographic limits.

## Rebuild and inspect

Requires installed Blender 5.2, Python/Pillow/NumPy, GNU make, fontconfig and
flock. No packages, add-ons, models, textures or lighting are downloaded.
`make refs` fetches only the registered photographs/PDF. Scratch stays in
this worktree's `build/`; every Cycles invocation uses the shared GPU lock.

```sh
make -C guns/sxs                    # model, kit UV/bake/export, checks and baked evidence
make -C guns/sxs check              # source/import, contacts, half-frame sweep, repeat
make -C guns/sxs model              # native source and unbaked diagnostic GLBs
make -C guns/sxs export             # one baked 2048 gun atlas through the kit
make -C guns/sxs sections match     # section cuts and calibrated photo pairs
make -C guns/sxs strips             # real-duration playback and wide opening
make -C guns/sxs render review      # current inspection stills and complete evidence
make -C guns/sxs reflections        # two band directions, five cameras, source/export
make -C guns/sxs fairness           # dense adjacent geometric face-normal angles
```

Build checks prove budgets, geometry, state, support and serialization within
their reported sampling. They do not establish photographic form or finish.
`REVIEW.md` records the image critiques, region acceptance and remaining limits.
The model uses canonical face order and dense original surface normals for
repeatable rebuilds. Most parts retain the 1 µm coordinate grid; the action
uses 10 nm so its short roof/lip boundary intervals stay planar.
This round changes only `guns/sxs/`; no kit or common module changed. The
first checkpoint introduced the shared exterior shell generator and additive
1.7.0 schema validator, which retain their accepted structure.

The original procedural rifle informs the build/rig/render workflow. All asset
vertices, bake sources and inspection materials are generated by our scripts. Reference
credits are in `refs/SOURCES.md`; eventual fictional text uses an installed
open-license font. Nothing is pushed.
