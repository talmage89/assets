# Rill playground / form and construction checkpoint

Original American municipal/school equipment for 1995–2015, generated in Blender
5.2. This delivery stops before UV atlases, high-to-low baking, material wear,
final look-dev and README gallery approval. No final docs images are committed.

The family has 40 independently exported modules, a connected 48-inch post grid,
a wider accessible turning platform, and three installed sites. Every vertex and
the two small diagnostic images are original script output. The library's own
Ground, trees, shrub, fence, street light, bench and litter construction is reused.
Existing deliveries are read-only. `REVIEW.md` records four construction passes;
`refs/SOURCES.md` records period photographs, drawings and standards consulted.

## Dimensions and source anchors

| Construction | Realized dimension / source |
| --- | --- |
| Round posts | **127 mm OD**, **3.05 mm wall measured after fresh import**, galvanized steel, capped and riveted. Maker installation packet's 5 inch / .120 inch specification (the nominal .120 is 3.048 mm). |
| Post/deck grid | Original **1.2192 m / 48 inch** module; **1.0922 m** steel deck between post centers. This is an original wider module, not a replica of the cited manufacturer's 42-inch grid. |
| Platforms | **.6096 / 1.2192 / 1.8288 m** (2/4/6 ft); **2.667 mm** 12-gauge standing skin, open underside, 89 mm downturned tray, return hems, stiffener and corner clamp hangers. Maker's .105 inch steel and 5/16 inch perforation anchors; diagnostic pits are temporary texture, not claimed physical holes. |
| Barriers | **965.2 mm / 38 inch** rail center above deck; lower clear gap **50.7 mm nominal**, infill at less than 88.9 mm clear. CPSC 2010 Table 4: school-age barrier at platforms above 48 inches, top at least 38 inches. Original kit uses barriers on lower exposed edges too. |
| Steps | Eight **152.4 mm** rises, **243.75 mm** runs, **900 mm** width, closed risers, stringers and returned 28.6 mm grip rails. CPSC Table 6 access ranges; proportions are original estimates within that guidance. |
| Slides | .6096/1.2192/1.8288 m entries; **.22 m** exits, integral side walls, compound transverse trough and longitudinal run, sitting hood, saddle/exit supports. Flat runout exceeds **279.4 mm / 11 inch**. Straight, wave, 270° spiral and **780 mm** nominal barrel / **744 mm** vertical bore tube. CPSC §§5.3.6.2–6; dated 2011 manufacturer wave-slide sheet supplies construction reference. |
| Climbing | Arch, 5-rung (48-inch) and 7-rung (72-inch) vertical ladders, sloped chain net, compound rock panel; **28.6–32 mm** gripping rungs. Rings and horizontal ladder at **2.05 m**. Hand/foot sockets on actual rung/hold coordinates. |
| Fire pole | **42 mm OD**, a dedicated supported 48-inch entry, at least **1.60 m** above that interface; **494.5 mm** measured horizontal entry distance. CPSC §5.3.2.6 anchors. |
| Swings | Independent two-bay A frame, **2.4384 m** beam center, **2.3084 m** bearing axis, **3.35 m per bay**, 89 mm legs, 127 mm beam, .51 m hanger pitch, two seats per bay; belt and bucket in separate bays. 6 mm true upper chain links plus original alpha strips on the long run. CPSC Table 7 and §5.3.8. |
| Accessible route | Six **1.2192 m** ramp sections rise **.6096 m** in **7.3152 m**, actual imported slope **1:12**; 1.2714 m nominal clear width. **1.8288 m** head platform gives **1.7018 m** between posts; dual 660/900 mm rails and edge curb. Ground and head landings are separate modules. The narrower downstream deck spine does not claim every event is wheelchair accessible. |
| Surfacing | EWF geometry with localized 65–75 mm kicked depressions; 150 mm timber borders and access neck. 2013 uses two-color poured-rubber geometry. F2075-10 covers fiber characteristics; F1292-09 covers impact attenuation. Rendered surfaces have no physical impact-test claim. |

CPSC 2010 supplies the numerical layout/access guidance. Only the public scopes
of ASTM F1487-11, F1292-09 and F2075-10 were read; the full paywalled texts were
not obtained. These original visual assets are not an installation design or a
certified safety product.

## Installed sites and measured costs

| Seed / installation | Equipment triangles | Entire site triangles¹ | Protected surface m² | glTF + BIN bytes² |
| --- | ---: | ---: | ---: | ---: |
| 101 / 1996 | 32,632 | 107,662 | 306.7 | 8,217,687 |
| 202 / 2005 | 38,484 | 114,338 | 291.2 | 8,837,083 |
| 303 / 2013 | 54,770 | 101,766 | 423.1 | 5,957,824 |

¹ Includes the local surface/walk, reused furniture/fence/light, shrub and trees;
101/202 have two tree species, 303 one large tree to fund its accessible platform.
The large lawn plane is included in counts, but its bounds are presentation
context, not the installed pad's dimensions. All sites stay below 120k.
² Shared external image bytes are separate and loaded once with a resource cache:
41,643,171 bytes / 17 unique maps for 101 and 202; 36,445,093 bytes / 14 maps
for 303. The two new diagnostic images together are 6,785 bytes; the rest are
reused library data, not new per-seed texture allocations.

The composite is a connected installation, not independent towers parked apart.
The hundreds select one of three period scaffolds (1996/2005/2013, repeating
every 300); other seed digits select compatible climbers, slides and overhead
events. Review seeds 101/202/303 pin the authored examples. These are explicit
connected scaffolds, not an unconstrained random park designer. `SEEDS=104,205,307`
builds alternate event selections. Grounded posts are shared
between adjacent decks; height transitions use closed steps. Swing front/back
zones conservatively reserve twice the beam height and do not overlap any other
envelope. The
conservative composite envelope extends 1.8288 m around its actual placed mesh;
its gap to the swing envelope is **254 / 191 / 283 mm** for 101/202/303. This gap
is between protective envelopes, not the equipment surfaces. Timber/rubber
footprints follow their connected union with 180 mm construction margins, removing
unused corners. Slide exits remain inside the protected composite envelope.

1996 is designated faded/repainted with thin kicked fiber, 2005 middle years,
2013 newer/inclusive on rubber. Only the geometry and surfacing type distinguish
these at this gate. Fading, repaint edges, age-specific dirt and polish remain
look-dev work; the quick colors are not evidence that those ages are finished.

## Modules / measured exported triangles

| Module | Triangles |
| --- | ---: |
| RampHeadBridge | 92 |
| Deck72 | 1,856 |
| Barrier72 | 1,792 |
| NeckGuard | 140 |
| Deck | 1,856 |
| Barrier | 1,624 |
| InfillPanel | 1,452 |
| HipRoof | 460 |
| Shade | 440 |
| Stairs48 | 1,260 |
| Transfer24 | 588 |
| RampSegment | 852 |
| RampLanding | 44 |
| InterdeckSteps | 276 |
| RoofRiser | 64 |
| SlideStraight24 | 3,868 |
| SlideStraight48 | 3,820 |
| SlideWave48 | 3,820 |
| SlideWave72 | 3,820 |
| SlideSpiral72 | 3,916 |
| SlideTube48 | 3,856 |
| Arch48 | 1,012 |
| Ladder72 | 436 |
| VerticalLadder48 | 372 |
| ChainNet48 | 1,664 |
| RockWall48 | 966 |
| FirePole | 884 |
| OverheadLadder | 680 |
| OverheadRings | 1,688 |
| PanelWheel | 1,864 |
| PanelTic | 1,954 |
| PanelPeriscope | 1,708 |
| SwingFrame | 496 |
| SwingBelt | 1,084 |
| SwingBucket | 1,432 |
| SpringRider | 1,300 |
| Roundabout | 736 |
| Post1730 | 326 |
| Post2339 | 326 |
| Post2949 | 326 |

Small mating/support pieces below 300 triangles are intentional; adding hidden
faces to reach a lower budget would waste geometry. Deck72 and Barrier72 make
the wider accessible turning bay. Slide/roof limits are 4k; every other module
is under 2k. Source stays parameterized in `src/parts.py` and `src/dimensions.py`.

## Texture allocation and resource sharing

Planned final shared sets, each three maps with full mip chains at 8 bpp per map:

| Set | Shipped size | GPU MiB | Purpose |
| --- | --- | ---: | --- |
| Coated metal / plastisol | 1024² | 4 | Common coating, deck perforation and chain coverage, cast clamps, zinc and rubber; reserve alpha cells instead of a separate chain atlas. |
| Molded plastic | 1024² | 4 | Shared molded finish and contact response; several colors through vertex tint. |
| Protective surfacing | 2048² | 16 | EWF and two EPDM colors, original periodic grain; placed depressions and causal instance variation. |
| **New family total** | | **24** | Excludes existing library sets; allocations do not multiply per seed. |

These are planned allocations, not baked delivery claims. Current quick family
has Frame/Molded/Site/Perforated/Chain review states and only a 128² deck image
plus 64×512 chain image (about **.0625 MiB** compressed with mips). Individual
modules use 1–3 materials; installed contexts use 13 states (101/202) or 11 (303).
They share existing Ground Lawn, tree and shrub 2048² sets (16 MiB each) and
fence's own 1024² analytic checkpoint fabric sheet (4 MiB). Its final GLB
is absent in this checkout, so the unchanged fence script regenerates that
review sheet inside this family's build; it is not claimed as the final fence bake. That is 68 MiB of reused sets for 101/202, 52 MiB for
303, before final playground sets. The tree's existing geometry/engine overhead
is additional. Pin oak images exist embedded in its canonical GLB and are
externalized once here; other available image paths reference canonical family
files. Do not load each glTF into a separate uncached texture allocation.

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
pivots are retained and inspected; a full spring deformation/interaction pass is
still required before final delivery.

## Rebuild and review

```sh
make -C playground                    # refs, model, glTF, checks, Cycles, contact
make -C playground check              # imported geometry/resources/layout/motion
make -C playground match              # balanced period pairs and fit diagnostics
make -C playground repeat             # byte comparison of deterministic exports
make -C playground WIDTH=900 SAMPLES=16 render
```

The section diagnostic additionally needs Matplotlib.
No source `.blend` enters a review render. All Cycles commands use the kit GPU
lock. Scratch stays in `build/`. Missing tree/shrub/Ground prerequisites can be
built by their own Makefiles.
Already present library deliveries are read-only and are never rebuilt here.
No kit changes and no top-level index changes.

Local verification passed all 40 fresh module imports, three whole-site budgets,
17 actual deck-interface contact tests and 132 sampled swing poses. The exact
repeat check compared 104 export/manifest files with zero differences. All 263
protected existing deliveries remained byte-identical. These checks establish
the stated geometry and resource properties, not a final appearance approval.

Local rebuilt review products:

- `renders/checkpoint/{101,202,303}/hero.png` and `above.png`: 40 mm, 1.65 m
  eye-height close heroes; plans show all events with colored use-zone envelopes.
- `renders/checkpoint/pieces.png` and `pieces-labeled.jpg`: reusable family sheet.
- `clamp-deck.png`, `slide-entrance.png`, `slide-exit.png`, `swing-hanger.png`,
  `climber.png`, `molded-sections.png` (three-quarter form), `swing.png` and
  `scale.png`; `molded-cross-sections.jpg` cuts actual imported surfaces at
  three perpendicular stations, independent of the generating profiles.
- `renders/checkpoint/matches/*-pair.jpg`, `matched-contact.jpg` and `contact.jpg`.
- `build/check.json`, `manifest.json`, `cameras.json`, `hero-values.json` and
  `repeat.json`: reproducible measurements, not committed generated claims.

The pairs retain construction differences: Adair uses an arched frame, the
original kit an A frame. Refitting an original compatible design cannot remove
that residual. Cropped focal lengths and full-photo equivalents are both
reported. The source photographs remain outside git and never enter a shader.

## Checkpoint limits

The close chain view still exposes the crossed-card transition and flat link
response. The molded hood/chute junction shows a small intersecting cheek, and
the tube's exit sleeve overlaps its open runout shell; both need a clean joined
high-detail source before the normal bake. The pieces sheet is an inventory:
small hanging seats need the separate swing close view to judge. The new quick
materials, sparse context and hard distant horizon remain visibly synthetic.
Period wear and fiber/EPDM response are intentionally unfinished at this stop.
Photo fits compare compatible construction, not exact replicas; their lighting
and architectural residuals are recorded in the review. No final atlas overlap,
texel-density or bake validation is claimed yet.
