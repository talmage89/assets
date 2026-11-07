# Rill playground / baked look-dev checkpoint

Original American municipal and school equipment for 1995–2015, generated in
Blender 5.2. This checkpoint includes UVs, three shared baked texture sets and
three installed sites. It stops before a final gallery or `docs/` images.

The family retains the accepted 48-inch connected post grid, 127mm posts,
2/4/6ft decks, 1:12 ramp, pivots and sockets. Its 40 modules remain, with an
additional arch swing frame for the later installations. Every new vertex and
texel is script-generated; photos and published plans are viewing references.
The library's existing Ground, trees, shrubs, houses, streets, cars and poles
provide context. Their canonical deliveries remain byte-identical.

## Dimensions and construction

| Part | Realized dimension / reference |
| --- | --- |
| Posts | 127mm OD, nominal .120in wall; fresh-import wall measurement in `build/check.json`. Manufacturer installation packet's 5in steel posts. |
| Grid and decks | 1.2192m post centers; 1.0922m deck skin between them. Original wider module, rather than the cited maker's 42in grid. Deck heights .6096 / 1.2192 / 1.8288m. |
| Deck manufacture | .105in / 2.667mm standing skin, 89mm downturned tray, return hems, underside stiffener and folded corner seats on smooth split cast collars. Perforations use shared alpha coverage; risers and cheeks are closed geometry. |
| Barriers | 965.2mm / 38in top rail above the deck. Clear infill gaps below 88.9mm. CPSC 2010 Table 4; exposed lower decks also receive barriers. |
| Stairs | Eight 152.4mm rises, 243.75mm runs, 900mm width; closed press-braked sides and risers, punched trays, returned 28.6mm grip rails supported on the actual rail line. CPSC Table 6. |
| Transfer | 16/24in platforms, closed cheeks, punched stepping surfaces and child grip rail. Original compatible assembly based on catalog construction. |
| Slides | 2/4/6ft entries; .22m exit, at least 279.4mm flat runout, compound transverse troughs and supported entry/exit. Straight, wave, spiral and nominal 780mm barrel / 744mm vertical bore tube. CPSC §5.3.6 and dated 2011 maker sheet. |
| Climbers | Arch, 5/7-rung ladders, sloped chain net, compound rock panel; 28.6–32mm gripping rungs. Rings and horizontal ladder at 2.05m; actual hand/foot sockets. |
| Fire pole | 42mm OD, supported 48in entry; measured 494.5mm horizontal reach to the actual deck edge and at least 1.60m above it. CPSC §5.3.2.6. |
| Swings | Two 3.35m bays; 2.4384m beam center, 2.3084m bearing axis, 127mm beam, 89mm legs. A frame in 1996, bent arch supports in 2005/2013. Molded 560mm belt with encapsulated chain inserts; full bucket belt/bowl and leg openings. |
| Chains | 6mm wire, alternating 45mm pitch; true links near hangers, crossed alpha cards below. Shared metal normal chart calibrated to the actual 36mm × 720mm card repeat. |
| Ramp | Six 1.2192m segments rise .6096m in 7.3152m; actual imported 1:12 slope. 1.2714m nominal clear width; 1.8288m turning deck gives 1.7018m between posts. Dual 660/900mm rails and edge curb. The downstream narrower spine does not make every event accessible. |
| Surfacing | One continuous containment per site, holding every reserved zone; later boundaries curve around their union. Local 65–75mm kicked EWF depressions; two-color EPDM in 2013. Actual entrance/floor continuity is sampled in the raw export. |

Numerical anchors come from CPSC Publication 325 (2010), the manufacturer's dated
component sheets and period catalogs. [The source register](refs/SOURCES.md)
records authors, dates and direct URLs. Only the public scopes of ASTM F1487-11,
F1292-09 and F2075-10 were available. These visual assets have no tested impact
attenuation or installation certification.

## Layouts, periods and age

| Seed | Published plan relationship | Original installation |
| --- | --- | --- |
| 101 / 1996 | Eastview Tot Lot Renovation, construction sheet 2, 10 July 1995: connected composite/swing containment, ramp, walk, edge seating and shade. Bradley's 2009 school plan additionally informs blacktop/building edges. | L-shaped three-deck structure, two red pyramid roofs, blue posts and yellow rails/events; adjoining swing bay within one timber enclosure. School blacktop and a building-edge socket beyond. |
| 202 / 2005 | Lively Park master-plan diagram, August 2005 in the plan approved 7 October: playground beside picnic space, parking, circulation and retained trees. | Four-deck stepped structure, lower roof bay, spiral/wave events; evergreen, tan and burgundy; arch swings and one rounded flexible border. |
| 303 / 2013 | Simon Playground Renovation L1.0, 28 February 2013: curved soft-surface play area, accessible approach, looping circulation, lawn and shade. | Low inclusive spine with broad turning bay and ramp, upper tube event and shade; teal, lime, orange and sand; arch swings and continuous EPDM. |

These are original compact compositions using plan relationships, not traced
sites. The Eastview plan specifies curved curb/play sand; this school variant
uses straight timber/EWF. Lively's recreation center and pool are omitted.
The 2005 Miracle catalog's printed page 145 explicitly groups Hunter Green,
Sand and Burgundy together and shows the primary and brighter alternatives.
The 2009 Columbia Cascade catalog supplies the additional named color range. Selection of
primary colors for 1996 is a period-compatible inference, not a located 1996
catalog. Native plan/layout evidence is in `renders/comparisons/layout-*.jpg`.

The hundreds select a period scaffold, repeating every 300. Other seed digits
select a connected loop/side bay, roof location/count, compatible events and
mirroring. Review seeds pin the three authored examples. Alternate plan choices
are deterministic; only the three review installations receive the full exported
construction, motion and rendering checks at this checkpoint.

1996 has sun-side chalking/fade, selected maintenance repaints, exposed plastisol
at entry/nosing foot lanes, chipped collars, base oxide, chalky scratched plastic
and compacted fiber. 2005 retains darker evergreen/burgundy, moderate contact wear
and used EWF. 2013 keeps stronger newer colors, limited contact wear and EPDM.
Age is carried by shared charts and causal per-instance tint/chart masks; it
does not allocate another texture set per installation. Fictional MEADOWWORKS
plates and carved initials are original artwork.

## Measured exported costs

| Seed / installation | Equipment triangles | Entire site triangles¹ | Protective area m² | Material states | glTF + BIN bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 101 / 1996 | 35,064 | 109,931 | 404.8 | 14 | 9,115,556 |
| 202 / 2005 | 40,884 | 113,874 | 359.6 | 14 | 9,232,364 |
| 303 / 2013 | 57,442 | 107,126 | 501.3 | 12 | 8,166,003 |

¹ Includes the local surfacing/walk, furniture, fence/light, shrub and trees.
All three remain below 120k. The additional residential streets, houses, parked
cars and distant grove are presentation-only imports and are excluded from that
installed-site budget. Native zone plans show the actual containment. Protective
envelopes conservatively reserve 6ft beyond equipment and twice the swing beam
height fore/aft; checks measure real surface contact and swing clearance.

## Modules / measured exported triangles

| Module | Triangles |
| --- | ---: |
| RampHeadBridge | 92 |
| Deck72 | 1,940 |
| Barrier72 | 1,760 |
| NeckGuard | 140 |
| Deck | 1,772 |
| Barrier | 1,592 |
| InfillPanel | 1,420 |
| HipRoof | 460 |
| Shade | 440 |
| Stairs48 | 1,700 |
| Transfer24 | 868 |
| RampSegment | 852 |
| RampLanding | 44 |
| InterdeckSteps | 276 |
| RoofRiser | 64 |
| SlideStraight24 | 3,860 |
| SlideStraight48 | 3,812 |
| SlideWave48 | 3,812 |
| SlideWave72 | 3,812 |
| SlideSpiral72 | 3,908 |
| SlideTube48 | 3,880 |
| Arch48 | 1,012 |
| Ladder72 | 436 |
| VerticalLadder48 | 372 |
| ChainNet48 | 1,664 |
| RockWall48 | 966 |
| FirePole | 868 |
| OverheadLadder | 680 |
| OverheadRings | 1,688 |
| PanelWheel | 1,832 |
| PanelTic | 1,922 |
| PanelPeriscope | 1,676 |
| SwingArchFrame | 1,312 |
| SwingFrame | 496 |
| SwingBelt | 1,428 |
| SwingBucket | 1,652 |
| SpringRider | 1,300 |
| Roundabout | 736 |
| Post1730 | 390 |
| Post2339 | 390 |
| Post2949 | 390 |

Every retained piece stays at or below the accepted 1,954-triangle maximum;
slides stay at or below 3,916. Small mating pieces intentionally remain below
300. Independent pieces use one to three material states. Installed equipment
uses separate opaque and masked states sharing the same images; context adds
its own library states. The state count is not a count of unique texture sets.

## Baked textures and memory

Original 4096² manufacture fields pass through locked Cycles flat baking and
kit filtering. Nine shipped PNGs form three shared stock glTF PBR sets:

| Set | Shipped size | GPU MiB with full mips at 8bpp/map | Contents |
| --- | --- | ---: | --- |
| PlayMetal | 1024² | 4 | Powder coat/orange peel, cast collars, zinc, plastisol perforation/wear, chain coverage, recessed pin drive, fictional plate and timber. |
| PlayPlastic | 1024² | 4 | Rotomolded chalk, directional bed scratches, mold seams/flashing, scuffed seats and carved initials; era tint through corner colors. |
| PlaySurface | 2048² | 16 | Loose 12–45mm fibers, aged fiber, EPDM and contact-worn EPDM; actual depressions and separate carryout chips. |
| **Family total** | | **24** | Shared across every piece and seed. |

Each has sRGB BaseColor, OpenGL +Y Normal and linear ORM (R occlusion,
G roughness, B metallic). Deck/chain alpha occupies the metal BaseColor.
`textures/bake/*-bake.json` records 4096 bakes; shipped reports record map bytes.
The nine family PNGs total 21,295,675 bytes on disk; that compressed file size
is separate from the estimated GPU allocation.

Manufacture charts intentionally repeat and overlap within assigned cells,
with eight delivered-pixel gutters and splits at physical repeat boundaries.
This is a trim/tiling allocation, not a unique zero-overlap unwrap. The UV audit
reports density percentiles and rejects collapsed UV triangles. Large molded
parts have lower density than fine fasteners. Normal unit lengths, external
image resolution and references are checked from the actual shipped buffers.

Reused Ground, tree and shrub 2048² sets cost 16MiB each; the 1024² fence
set costs 4MiB. Ground Concrete adds another shared 16MiB. The actual exported
sites reference 84MiB (101/202) or 68MiB (303) of library sets in addition to the
new 24MiB: 108 / 108 / 92MiB if every referenced set is uncached. All three
installations together share the same 108MiB resource union. Presentation streets/houses/cars have their own
existing resources. These are separate from the approved new family allocation.
Canonical images are referenced or externalized once, never duplicated per seed
as new family sets. An engine should cache resources across the glTFs.

## Pivots, sockets and engine use

Meters, Blender +Z up / -Y front; glTF +Y up / +Z front. Ground posts, frames,
riders and spinner use footprint origins. Decks use their top connection plane;
slides their entrance projection on grade; ramp segments their upper connection
plane; swing modules the beam axis. Those mating-origin exceptions are deliberate.

| Moving assembly | Local axis / range | Pivot |
| --- | --- | --- |
| Each swing pendulum | X / -55…55° | Bearing axis, 130 mm below beam center; chains and seat follow it. |
| Spring rider | X / -14…14°; optional Y / -12…12° | Spring's upper mount; spring is fixed, rigid tilt is a game approximation. |
| Roundabout | Z / continuous, author range -180…180° | Central bearing at 270 mm above surfacing. |
| Steering wheel | Y / continuous | Wheel hub. |
| Nine tic-tac-toe drums | X / continuous | Separate horizontal spindle axes. |
| Periscope | Z / -90…90° | Molded base swivel. |

The table uses Blender axes; glTF maps X to X, Y to -Z and Z to +Y.

`socket_kind` empties expose slide entry/exit, seat, transfer platform, ladder/net/
rock hand and foot locations, ring grips, deck/post centers and ramp joints.
Seeded sites use the first composite deck center as their grade origin;
placement coordinates and use-zone envelopes remain explicit in the manifest.
No armature, animation clip or physics implementation is shipped at this gate.
Explicit tangents are omitted at this checkpoint: importers derive tangent space
from the preserved normals and UVs. This avoids a nondeterministic rounding
boundary in Blender's recalculated reused-tree tangent.
The kit's surface-based motion sweep samples swing rotations at 11° steps against
the actual imported frame/neighbor seats, with only their own hanger articulation
excepted. This is sampled clearance, not a continuous physics proof. Other motion
pivots are retained and inspected; spring deformation remains the documented
rigid gameplay approximation.

## Rebuild and review

```sh
make -C playground                       # refs, textures, model, check, render, match, review
make -C playground check                 # fresh import, dimensions, UVs, maps, actual contacts
make -C playground match                 # three white-balanced daily-use photo pairs
make -C playground source-match          # additional live-source photo comparisons
make -C playground before-match          # preserved prior export, same calibrated cameras
make -C playground compare               # 1200px fixed-camera panels and plan evidence
make -C playground repeat                # byte-identical model/export repeat; no bake rerun
make -C playground WIDTH=1200 SAMPLES=24 render
```

Blender runs serially through `src/serial_blender.sh` and the kit's shared GPU
lock, including modeling and import checks. Rendering imports exported glTF
and baked PNGs. Scratch stays in `build/`. Python requires the repository's
existing NumPy/Pillow/Matplotlib; plan evidence uses installed Poppler.
Existing library deliveries are read-only and are not rebuilt here.
No kit code or top-level index is changed.

Review products remain ignored local files:

- `renders/lookdev/{101,202,303}/{hero,above}.png`: 40mm, 1.65m heroes in raking
  sun; above views with use zones and access.
- `renders/lookdev/`: clamp/deck, stair and transfer; slide bed/exit/tube junction;
  hanger/hollow, belt/bucket, arch frame, net climber, rubber wear and scale.
- `contact.jpg`, `matched-contact.jpg`, `pieces-labeled.jpg` and actual imported
  `molded-cross-sections.jpg` within that folder.
- `renders/comparisons/`: native same-camera before/after panels and plan evidence.
- `build/check.json`, `lookdev-check.json`, `hero-values.json`, `cameras.json`
  and `repeat.json`: independently reproducible measurements.

The photo fits retain original design differences. Roswell's deck and the 2005
stair are matched on whole installed sites, not on pieces floating in a void.
Adair's frame is now compared with the arch variant; its original full-frame
70mm EXIF constrains the fit. Roswell's compact-camera EXIF constrains the
horizontal equivalent to 36.0–36.8mm. The stair photograph has no available EXIF;
its camera stays level, with a bounded 12–40mm full-image horizontal lens.

| Pair | RMS / maximum error in native crop pixels | RMS / crop width | Fitted full-photo horizontal equivalent |
| --- | ---: | ---: | ---: |
| Used deck, 2009 | 29.23 / 57.41 | 4.48% | 36.8mm |
| Used swings, 2009 | 20.42 / 32.98 | 2.39% | 71.0mm |
| Used stair, 2005 | 12.69 / 18.04 | 7.05% | 12.0mm; zero roll |

The virtual lenses for the tight crops are longer; both values appear on the
pair footers. Fits sit near lens bounds and retain original construction
differences, so these are useful comparisons, not surveyed replicas. The deck
variant's catalog forest green remains darker than the photograph's Kelly green.
The shaded pairs use stronger procedural sky fill than the raking-sun heroes,
with unchanged exposure and material albedos. Additional live-source pairs use
the same cameras and lighting as the exported comparisons. Their live analytic
assemblies use original 4096 color/ORM fields and the calibrated 4096 normals
before filtering; they isolate filtering/serialization loss. There is no
separate high-poly projection step in this manufacture-field pipeline.
Residuals and neutral
white-balance controls remain explicit in `build/cameras.json`: shaded concrete,
a small white cap and a galvanized stair cheek; none is a calibrated gray card.
Photos never enter mesh generation or a shader.

Remaining look-dev limits are identifiable chain cards close up, repeated collar
chipping, regular slide-bed scars, some half-meter edges in EPDM contact wear,
and recognizable library foliage cards. EWF is flatter and cooler in the shaded
pairs than the loose warm chips in the photographs. Age reads most strongly
through roof fade, contact lanes, the installation palette and its surfacing;
small base and handling marks remain less evident in the full-site views.

Lettering uses installed DejaVu Sans; review captions use Noto Sans, located
through `kit.fonts`. No downloaded visual asset enters a shader.

## Limits at this gate

[REVIEW.md](REVIEW.md) records the native image critiques and remaining CG tells.
Crossed chain cards remain a game compromise; distant small chips use normal and
color relief rather than loose geometry everywhere. Repeated manufacture charts
and library context can still be recognized in close inspection. Photo fits
compare compatible original construction, not surveyed replicas, and do not
prove absolute reflectance. Sampled swing clearance is not continuous dynamics.
No final README gallery or `docs/` images are produced in this round.
