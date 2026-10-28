# PD Bracken L20 lever-action carbine

An original **Propane Defense** .30-30 visual game asset in the class of the
20-inch, straight-grip, top-ejecting hunting carbine. All geometry comes from
our Blender 5.2 scripts. It has a six-round tube, right-side loading cover,
exposed hammer, semi-buckhorn sight, beaded front blade and curved steel butt
plate. Its contours and fictional **PD / 30-30** ammunition headstamp are ours.

**Form and motion checkpoint, before look-dev.** Constant inspection materials
stand in for blued steel, oiled walnut and ammunition metals. No wood grain,
finish wear, atlas, UV/bake acceptance, final delivery or docs photographs are
claimed at this gate. The dense sculpt is retained for the later bake.

Generated inspection files stay ignored. Start with
`renders/checkpoint/contact-sheet.jpg`, `dimensions.jpg`, `sections.jpg`,
`regions.jpg`, `photo-pairs.jpg`, `source-pairs.jpg`, `clips.jpg` and
`clips-detail.jpg`.
Round-two evidence adds `lever-stroke.jpg`, `hammer-trigger-pairs.jpg`,
`aimed-pixels.jpg`, three orthographic lever poses, a butt-plate profile,
an underside wrist view and close raking views of both receiver flanks.
`renders/checkpoint/views/` contains native stills; `pairs/` and `source-pairs/`
contain calibrated exported/dense comparisons; `strips/` contains each clip's
frame strip and real-duration animated WebP. `detail-strips/` adds eleven
closer action views at the same real timings. [REVIEW.md](REVIEW.md) records the
image critiques, region acceptance and remaining differences.

## Scale and references

| Quantity | Measured / designed | Basis |
| --- | --- | --- |
| Barrel, breech face to crown | 508.00 mm / 20 in | Published carbine class; actual mesh bounds |
| Overall length | 965.20 mm / 38 in | Published class and independent Smithsonian measurement |
| Length of pull at finger-height face | About 340.74 mm | Actual trigger/butt surface rays; original stock, about 3 mm shorter than published 13.5-inch class |
| Closed gun width / height | About 42.55 / 183.76 mm | Evaluated visible mesh bounds |
| Capacity | Six in tube, one chambered | Explicit individual rounds, follower and count states |
| Cartridge case / overall length | 51.80 / 64.77 mm | Published C.I.P. external envelope |
| Cartridge rim / body / neck diameter | 12.85 / 10.71 / 8.38 mm | C.I.P.; exterior-only visual geometry |
| Eye behind rear sight / above actual comb | 368.00 / 39.02 mm | Authored ergonomic placement, measured again on actual surfaces |
| Notch width | 3.60 mm | Original sight geometry |
| Target mass | About 3.1 kg | Class planning target; **not a measured mass** |

The macro headstamp planes sit 0.025 mm behind the case head, so the standalone
GLB bounds include that extra depth: 64.795 / 51.825 mm. The tabulated lengths
refer to the physical case-head frame and bullet/mouth surfaces.

The eye location is an ergonomic estimate, not a published eye-relief value.
The NPS shouldered lever-rifle photograph supports a cheek weld behind open
sights qualitatively; it depicts a different, longer rifle. The manual's
shouldering/sight instructions and our actual comb ray support the placement,
without turning that estimate into a sourced dimension. The exact Eye frame
looks through the notch at the bead with a 70° horizontal FOV, zero shift, opaque
gray backdrop and every gun part visible. Surface rays check obstruction and
the projected bead top against the notch shoulders.

Published specifications, parts diagrams, manuals, direct reference URLs,
authors and licenses are in [refs/SOURCES.md](refs/SOURCES.md). Modern
angle-eject/rebounding-hammer diagrams inform names and construction; their
different action semantics are not attributed to this older class. Commons
photos of the class provide right, left and open-action comparisons. Photo
neutral patches and linear white-balance corrections are rebuilt by
`src/white_balance.py`; reflective screw/pin facets are imperfect neutrals.
No reference pixel is used in modeling, a material or a texture.

## Construction

The stock and forend are changing compound subdivision cages, with independent
width, belly, comb, toe and channel curvature. Dense originals live in
`build/sculpt.blend`; their reduced game copies receive the same machined
inlets. Flush upper/lower tongues follow the wood's actual surface; a buried
fork joins both receiver cheeks below the bolt race. The slotted retention
screw has a continuous shank through bores in both tangs and the wrist.
Actual section cuts compare both at three wrist, three butt and three
forend stations. The crescent plate has curved faces across its entire
surface, seated on the wooden butt, with its shoulder socket on that surface.

The receiver is hollow, with rounded machined corners, top opening, bottom
linkage aperture, side gate, screw countersinks, guide lands and lock seats.
The barrel has an exterior taper, crown, bore and chamber counterbore. The
magazine is a hollow tube. Both 1.3 mm-gauge bands are fitted to section cuts of
our actual wood/barrel/tube surfaces. The sights have a barrel dovetail, spring
leaf, separate stepped elevator and supported front ramp/blade/bead.

The lever is one continuous forging, with a sweeping web and a long,
straight-sided finger opening. Its measured opening is 104 × 29 mm; its
bar is 2.2 × 8.2 mm. It pivots on a dropping link with a real pin/bore bearing.
The curved hammer body and returning spur carry a crowned thumb table with
1.0 mm checkering in the inspection mesh. The
trigger is a 6 mm wide, 3.7 mm deep radiused blade: its front concavity faces the muzzle and its
toe returns forward. It is checked against sharp side and oblique photographs.

The bolt, forked locking-block display, cradle carrier, sear support and feed
handoffs are deliberately incomplete visual internals. They establish supported
poses, exposed construction and game animation. They do not reproduce a
working mechanism. The forked lock's gate-side relief is an original visual
accommodation; the source photos do not establish its hidden shape. Springs
inside the opaque tube and concealed fire-control internals are omitted.

## Rig and consumer binding

The additive [interface 1.5.0 supplement](INTERFACE.md) retains base 1.0.0 and
reuses 1.1.0 tube-loading and interruption meanings. `build/interface.json`
contains capabilities, 37 clip schedules, events and count states. Fire and
manual cycling are separate. Every tube round, the follower, the displayed
carrier/chamber/insertion rounds and the fired case has an individual bone.
All 26 bones are rigid-weighted; all ten sockets retain complete frames.
Root stays identity; the consumer supplies whole-instance motion and hand IK.

| Part | Pivot or travel | Authored range |
| --- | --- | --- |
| Lever | X axis at (0, 124, −1) mm, on moving Link | 0–80° global; local angle compensates Link |
| Lower link | X at (0, 195, 5) mm | 0–20° |
| Bolt | Y translation | 90 mm rearward |
| Locking block | Z translation | 30 mm downward |
| Carrier | X at (0, 85, 7) mm | 0–20° |
| Hammer | X at (0, 70, 30) mm | Fired 0°, half-cock 12°, full-cock 44°, bolt-overtravel 90° |
| Trigger | X at (0, 83, 0) mm | 0 to −12° |
| Loading cover | Z at (15.2, 122, 20) mm | 0–28° inward |
| Follower / tube rounds | Y | 64.77 mm pitch, count-dependent |

These are visual animation ranges, not published mechanism measurements.
The carrier and fired-case motion bones remain nonscaling; their separate
display children alone hide, preserving orientation across a GLB handoff.
The operating hand socket follows the compound lever/link motion. Clearance
uses a fixed palm and four lever-riding finger envelopes through every clip;
it proves clearance of those explicit volumes, not every possible human hand.

The gun, live cartridge and fired case export through the kit's weapon GLB
path. At this gate the gun preserves named parts for independent surface
audits. Its seven constant material classes are inspection-only; the final
atlas will consolidate them. The standalone cartridge/case have head-centered
origins and +Y toward the mouth. At the eject event, the ejection socket equals
the fired-case head frame; consumers can replace the demonstration case with
the standalone. See the supplement for ownership and interruption details.

## Checkpoint budget

| Output | Triangles | Constant materials | GLB bytes |
| --- | ---: | ---: | ---: |
| Gun, including every ammunition display and hidden tube slot | 39,926 | 7 | 2,856,292 |
| Standalone live cartridge | 1,598 | 5 | 61,728 |
| Standalone fired case | 1,326 | 3 | 50,124 |

The gun is inside the brief's 30–40k ceiling. Its 116 named inspection meshes
remain separate for surface audits; this is not the final draw-call layout.
There are **zero texture images** at this gate. The final one-atlas target and
its memory budget remain unchanged. The same static exterior generated twice
has identical vertices/normals, oriented triangles, skin, sockets and animation
accessors. Blender can reorder identical bead triangles in the GLB; the live
cartridge and fired case also reproduce byte-for-byte. `make repeat` checks
the exact accessor data and oriented topology, recording both file hashes.

## Checks and rebuild

```sh
make -C guns/lever              # the complete requested checkpoint
make -C guns/lever check        # construction, states, all motion, fresh import
make -C guns/lever render       # exported GLB inspection stills
make -C guns/lever review       # sections, photo pairs, timed clips and sheets
make -C guns/lever repeat       # independent rebuild and exact geometry/clip comparison
make -C guns/lever check-topology # imported solids across normal/attribute seams
```

`make refs` fetches registered images/PDFs; `make model` builds the named
source, retained sculpt, gun/cartridge/case GLBs and manifests. All Cycles work
uses the shared kit GPU lock. Scratch files stay under this worktree's build.
`make clean` removes generated output so the checkpoint can be rebuilt.

`build/check.json` reports real mesh dimensions, manifold solids, required
surface contacts, sight/comb rays, trigger concavity, intended event/count
states and half-frame clearance sweeps. `build/serialization.json` repeats
construction, state and motion checks after a fresh GLB import, checks raw
normals/weights/durations and compares full affine transforms at half frames.
The independent construction tests establish the model's stated contacts;
source/import agreement separately establishes serialization. Eight probes test
the outer tang bearing lands, and each connected tang component must reach the
receiver. The sculpted wood also transfers its smooth normal field directly
to the reduced vertices; this adds no textures or triangles. Raw GLB normal
seams duplicate corner vertices, so the imported geometry record lists their
unwelded edges. `build/topology.json` separately proves all 116 geometric solids
closed after check-only welding at 0.01 micrometers; the delivered normals and
meshes are untouched.

`build/provenance.json` ties every final inspection still and clip sample to
the current source GLB/sculpt hash and verifies all encoded clip durations.
UV overlap, density and bake transfer belong to the next stage, since no UVs
or textures exist at this checkpoint. Final intent is one 2048 BaseColor /
OpenGL Normal / ORM set, baked at 4096; about 16 MiB with block compression.

## Next finish pass

The hunting-use finish is planned, not implemented: bright gray receiver
corner and bottom rubs; plum/brown thinning confined to exposed blued flats;
smooth polished lever contact arcs; thin bright loading-cover lips; rubbed
band shoulders and muzzle rim; crushed dark dings at the stock heel/toe and
forend edges; and darker hand oil around the wrist. Walnut fiber must curve
with its carved volume. Each effect will be judged on a white-balanced used
reference pair of the baked export at hero scale before final acceptance.

No kit code or other gun is changed in round two. The shared .30-30 generator
`ammo_3030.py` now assigns independent analytic normals to the straight body,
shoulder and neck, removing the false dent-like highlight without adding faces.
`interface_v1_5.py` and the accepted bone/clip data are unchanged. Only the butt
socket's position follows the revised plate, as documented in the supplement.
