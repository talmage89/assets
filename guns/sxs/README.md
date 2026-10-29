# PD Covey 26 — boxlock side-by-side shotgun

An original script-built 12-gauge field shotgun: 26-inch joined barrels,
double triggers, extractors, right-swinging top lever, automatic tang safety,
straight-hand walnut stock and splinter forend. Fictional maker/model:
**Propane Defense Covey 26**.

**Form and motion checkpoint, before look-dev.** The GLBs use constant
inspection materials. UVs, normal-map checkering, markings, used finishes,
baking and final delivery remain held. No docs images are committed at this gate.
Generated image paths below are local build outputs, not hosted README images.

## Dimensions and design

| Quantity | Evaluated visual geometry | Published class / design anchor |
| --- | ---: | --- |
| Overall length | 1079.95 mm | brief: about 1080 mm |
| Barrels, rear face to muzzle | 660.40 mm / 26 in | published 26-inch option |
| Overall width / height | 54.80 / 175.79 mm | original twin-barrel/straight-stock envelope |
| Front-trigger length of pull | 369.63 mm / 14.55 in | published 365 mm; original stock is 4.63 mm longer |
| Comb / heel drop | 38.02 / 63.03 mm | published 38 / 63 mm; measured against an actual rib-centerline datum (concave edges rise about 0.22 mm) |
| Cheek station | 35.00 mm behind comb nose | published range 31.75–38.10 mm |
| Eye above actual comb | 42.81 mm | actual surface ray; CPSA coin-rule sight picture, derived below |
| Eye optical pitch | −0.374° | exact line from the socket to the bead |
| Wrist, wood only at Y = −15 mm | 32.17 × 37.88 mm | sharp top/side photographs; absolute reference scale remains uncertain |
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
shoulders, spherical fence domes, a short upper head and a standing breech
with visible pin bushings. The table has a narrow visual lug passage over
a closed lower floor. The rounded underside sweeps into the concentric knuckle;
the hinge pin ends are small flush circles. Two hollow barrel skins meet on
cut joined flats at the breech, without overlapping outer walls, and have chamber-side rim recesses,
walls at the muzzle, joined solid top and bottom ribs, lower lumps/hook and a
two-pad extractor. A swept guard band and separate rear tang surround two tapered flat trigger
blades. Their working faces are concave toward the muzzle and their tips curl
forward. The top lever has a round 11.2 mm boss and a long, narrow tapered tail lying
close above the strap. Its thumbpiece is about 7.1 mm wide and 1.9 mm thick.
The guard is a 12.4 × 1.63 mm flat band with a swept front return and wrist tang.
The safety retains its compound thumb surface. Dense forging and thumbpiece
sources are retained for the later edge/checkering normal bake.

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
| Gun, all staged alternatives | 37,728 | 1,765,484 |
| Shell | 752 | 26,476 |
| Hull | 480 | 18,160 |

54 named rigid meshes, 17 bones, 19 clips, 14 sockets; 9 temporary inspection materials and **zero texture images**.
<!-- /CHECKPOINT_STATS -->

All hidden ammunition alternatives count against the 38k round-three gun budget.
The shell module is new in `guns/common/shell12_visual.py`; no pump source or
output is imported. It preserves the pump's original exterior proportions:
22.4 mm rim, approximately 20.1 mm hull, 57.5 mm loaded length and 69.8 mm fired
length. Connected hidden joins make each shell a closed manifold skin.

| Local generated path | Contents |
| --- | --- |
| `build/sxs.blend`, `build/sxs.glb` | Named form assembly, rigid rig, clips and sockets |
| `build/shell.glb`, `build/hull.glb` | Separate head-centered exterior ammunition, +Y toward mouth |
| `build/sculpt.blend` | Dense furniture/control cages on the same rig for comparison |
| `build/check.json`, `import-check.json` | Separate source/import topology, intended-state, contact and half-frame clearance reports |
| `build/serialization.json`, `repeat.json` | Round-trip affine/surface proof and independent rebuild proof |
| `renders/checkpoint/contact-sheet.jpg`, `hero-gray.jpg` | Current Cycles inspection views from the exported GLB |
| `renders/checkpoint/dimensions.jpg`, `sections/sections.jpg` | Measured orthographic and triangle-plane sections |
| `renders/checkpoint/photo-pairs.jpg`, `source-photo-pairs.jpg` | Eleven export/source comparisons, native residual arrows and photo-outline overlays |
| `renders/checkpoint/clips.jpg`, `opening.jpg`, `strips/` | All clips, wide opening and correctly timed WebPs |
| `renders/checkpoint/ammunition.jpg` | Standalone shell and hull inspection |

Planned final delivery: one 2048 BaseColor/OpenGL Normal/ORM gun set, about
16 MiB with block compression and mipmaps. Standalone shell and hull get
independent 512 sets, about 1 MiB each, rather than embedding the gun atlas.
The gun's internal display shells may occupy its atlas; the standalone maps
derive from the same original finish fields. This is a plan, not a shipped
texture-memory or baked-delivery claim.

## Rebuild and inspect

Requires installed Blender 5.2, Python/Pillow/NumPy, GNU make, fontconfig and
flock. No packages, add-ons, models, textures or lighting are downloaded.
`make refs` fetches only the registered photographs/PDF. Scratch stays in
this worktree's `build/`; every Cycles invocation uses the shared GPU lock.

```sh
make -C guns/sxs                    # complete form checkpoint; stops before look-dev
make -C guns/sxs check              # source/import, contacts, half-frame sweep, repeat
make -C guns/sxs model              # all four grouped inspection outputs
make -C guns/sxs sections match     # section cuts and calibrated photo pairs
make -C guns/sxs strips             # real-duration playback and wide opening
make -C guns/sxs render review      # current inspection stills and complete evidence
```

Build checks prove budgets, geometry, state, support and serialization within
their reported sampling. They do not establish photographic form or finish.
`REVIEW.md` records the image critiques, region acceptance and remaining limits.
The model uses a 1 µm coordinate grid before reduction, canonical face order,
and dense original surface normals to make independent rebuilds repeatable.
This round changes only `guns/sxs/`; no kit or common module changed. The
first checkpoint introduced the shared exterior shell generator and additive
1.7.0 schema validator, which retain their accepted structure.

The original procedural rifle informs the build/rig/render workflow. All asset
vertices and inspection materials are generated by our scripts. Reference
credits are in `refs/SOURCES.md`; eventual fictional text uses an installed
open-license font. Nothing is pushed.
