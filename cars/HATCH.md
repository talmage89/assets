# Alder H120 — form round 2

An original compact five-door hatchback in the 2018–2022 class. This checkpoint
contains the outer body, glazing, wheels, real panel gaps, recessed lamps and
fascia openings. It stops before interior, hinges/struts, underbody detail,
paint, UVs, baking and hatch GLB delivery.

![Front clay, generated locally](renders/hatch-round2/front_three_quarter.jpg)
![Rear clay, generated locally](renders/hatch-round2/rear_three_quarter.jpg)

The package compares Toyota Corolla and Hyundai i30/Elantra GT, with a gently
falling rear roof, short rear overhang, raked backlight and nearly upright lower gate.
Small fixed quarter panes follow the Hyundai's visibility/construction choice.
The bumper holds the plate pocket. Long rising lamps, horizontal grille blades
and the existing family form wheels carry Alder's design language. No maker's
body, badge, lamp graphic or mesh is copied.

## Measured package

[REFERENCE.md](REFERENCE.md#alder-h120-compact-five-door-hatchback-source-form-checkpoint)
contains the manufacturer comparison and photographic uncertainty;
[refs/SOURCES.md](refs/SOURCES.md) registers all thirteen references.
Measurements below come from actual game-mesh bounds, cuts and rays.

| Measurement | H120 measured | Basis / target |
| --- | ---: | --- |
| Length | 4361.2 mm | 4360; Toyota 4370, Hyundai 4340 |
| Body width | 1794.4 mm | 1795; Toyota 1790, Hyundai 1795 |
| Height | 1450.6 mm | 1450; Toyota 1435, Hyundai 1455 |
| Wheelbase | 2650.0 mm | Toyota 2640, Hyundai 2650 |
| Front / rear track | 1550.0 / 1560.0 mm | Original upper-wheel package; Hyundai N Line 1549 / 1563 |
| Front / rear overhang | 926.7 / 784.4 mm | Original 925 / 785; Toyota 935 / 795 |
| Width across mirrors | 2039.3 mm | Hyundai UK 2039 |
| Tire top to arch, all four | 40.0 mm | Brief 30–50 |
| Arch edge minus tire outboard | +2.5 mm front / −2.5 mm rear | Extrema comparison; nearly flush |
| Sampled front/rear door gaps | 4.499–4.506 mm | 4.5 mm |

The chosen tire is **225/40R18**, nominal diameter 637.2 mm. The form proxy is
a circular 629.2 mm tire at 314.6 mm hub height, rather than a deformed loaded
contact patch. Minimum ground clearance is **not yet measured**: 140 mm is the
later underbody target. There is only a temporary recessed cavity closure.

## Profile, sections, face and rear

| Measured feature | Result |
| --- | ---: |
| Hood leading center height | 739.7 mm |
| Windshield rake from vertical | 60.48° |
| Roof center drop over y = 0.15…1.40 m | 40.6 mm / 1.86° |
| Backlight rake from vertical | 46.58° |
| Lower gate rake, z = 0.72…0.84 m | 13.67° from vertical |
| Spoiler overhang beyond upper glass samples | 106.9 mm |
| Side-glass tumblehome at B-pillar | 22.97° |
| Above-arch fender swell relative to same-height door | 30.0 mm front / 29.8 mm rear peak |
| Hood-side to fender crown at y = −1.60 / −1.30 / −1.14 m | 22.94 / 22.99 / 16.71 mm |
| Headlamp centerline along surface | 669 mm each |
| Headlamp maximum sampled height | 98.2 mm |
| Headlamp outer-end rise | 162.9 mm |
| Grille / lower intake normal recess depth | 56.0–57.5 / 51.0–53.1 mm |
| Corner-pocket depth | 46.1–46.9 mm |
| Plan setback at x = 800 mm, front / rear | About 231 / 147 mm at bumper height |
| Rear-glass top / base width | 1192 / 1409 mm |
| Projected D-pillar band | 146 mm |
| Split taillamp height at quarter corner | 125.5 mm; gate tapers inward |
| Plate-pocket mouth / bed, width × height | 319 × 166 / 317 × 159 mm |
| Plate-pocket depth | 21.0–21.5 mm |
| Mirror housing, outboard × height × depth | 228 × 136 × 128 mm |
| Mirror housing bottom height | 994.7 mm |
| Front leading tangent height | 686.0 mm |
| Taillamp height at inner gate tip | 51.7 mm |
| Diffuser lower-edge height range | 217.33–218.29 mm |
| Lower bumper turn-under height | 144.1 mm |

The mirror cap centers are at **x = ±905.6, y = −618.1, z = 1062.8 mm**;
front is −Y. Their bottom is near the beltline and the broad sail mounts behind
the A-pillar base on each front door. Surface intersections verify the sail/door
and shoe/housing contacts. The cap stays 64.2 mm below the central body profile
at its nearest approach; the rear glass plane is y = −551 mm.

The liftgate cut crosses below the split lamps and above the bumper at about
645 mm. The transverse stamped band and recessed garnish reserve a central
badge location; the garnish bed is 6.0–7.1 mm behind the skin. The bumper's soft upper
crease is controlled below that cut, around 580–625 mm. Measured normal turns
over 60 mm are 4.34°, 1.03° and 4.86° at
x = 300, 500 and 700 mm. The bumper remains convex on a broad corner plan.
Its lower 144 mm turns under to the diffuser, with reflectors and an exhaust
cutout. The plate remains in the bumper, following Hyundai, with a lamp at
its top. Mouth dimensions now start on the actual paint skin, without the
locator's 2.5–4 mm standoff; this corrects round 1's depth reporting. Depth
rays use the regenerated uncut parent normal, since the nearest surviving
paint at a hole can belong to an adjacent panel.

Rear-glass widths are horizontal cuts 35 mm below the glass top and 45 mm above
its lowest point. The projected pillar band compares upper-quarter and glass
widths; it is not a structural metal thickness. Photograph estimates are
1192 versus 1114/1149 mm at the top and 1409 versus 1232/1385 mm at the base,
with ±30 mm photographic uncertainty. The glass follows the broader Hyundai
base; it deliberately does not duplicate the narrower Corolla opening.

The three requested door sections are measured at y = −0.335, +0.255 and
+0.755 m. Normal turns use the actual rendered parent corner-normal field;
positions use intersections with the game mesh.

| Section feature | Mid-front door | B-pillar | Mid-rear door |
| --- | ---: | ---: | ---: |
| Shoulder height | 885 mm | 893 mm | 899 mm |
| Upper-door inward lean | 20.17–20.62° | 20.19–20.62° | 20.22–20.64° |
| Lean 40 mm below shoulder | 4.59° | 4.56° | 4.56° |
| Lower-door lean | 16.40° | 15.84° | 15.26° |
| Lower crease normal turn over 80 mm | 10.56° | 10.06° | 9.83° |
| Located soft crease height | 459 mm | 482 mm | 502 mm |
| Concave run, 50 mm chord depth | 1.76 mm | 1.85 mm | 1.81 mm |
| Shoulder to lower door-edge inset | 79.3 mm | 74.4 mm | 70.4 mm |
| Further tuck to recessed sill | 43.4 mm | 49.4 mm | 51.9 mm |

## Construction and allocation

One connected all-quad sheet covers hood, fenders, side, roof, backlight,
liftgate and end fascias. Its regular cage is refined before fitting the
**control vertices** to original analytic sections and the bowed plan.
Catmull–Clark evaluation follows the fit. The fitted control net has 117,425
vertices, 116,736 quads, one connected component and valence-four interior
vertices. The evaluated surface is not fitted point-by-point afterward.

The game surface samples the parent's parameter chart, with denser sampling
at end turns. Panel and aperture cuts are projected onto the fair parent;
gaps are offset afterward. Original parent normals survive separation.
Steel gauge is 0.9 mm, glass 4.8 mm, fascia 3–4 mm. Fixed roof-rail/quarter
joins have no invented shut line. Arch flanges turn inward 18 mm. Recesses
have separate returns and beds, with coarse grille blades inside real holes.

**46,881 game triangles**, down **6,503** from round 1. The high source has
**124,632 triangles**. Removing 14,327 buried reverse-skin triangles creates
the main saving; denser front aperture sampling, the supported spoiler and
new rear feature spend part of it. The last front review added 220 triangles
around the inner lamp corners and restored 768 triangles to the visible
grille, intake, plate and garnish beds, eliminating decimation dents. Fixed
stampings retain every outer face and
visible gauge return. Their inner boundaries are deliberately open and carry
an audited face-role attribute. Moving closures and glass retain their backs.
This is not reported as an entirely closed-solid game assembly.

| Part group | Game triangles |
| --- | ---: |
| Body skins, roof and closures | 11,413 |
| Front/rear fascia skins | 10,450 |
| Four door skins | 3,932 |
| Pillars and appliques | 1,350 |
| Glazing | 1,504 |
| Arch flanges | 784 |
| Wheelwell liners | 1,168 |
| Apertures, returns, beds and grille blades | 5,268 |
| Mirrors | 1,608 |
| Roof spoiler | 1,184 |
| Four tires | 4,224 |
| Four wheels | 3,984 |
| Temporary cavity closure | 12 |
| **Total** | **46,881** |

Per-mesh and per-parent counts are in `build/hatch/form-check.json`. Moving
assemblies remain provisional; their hinges and clearance sweeps are deferred.

The finished-car allocation is **59,381 triangles plus 500 contingency**:
8,000 interior (seats 3,500; dash 1,500; controls 500; door cards 1,200; cargo
1,300), 2,500 underneath and 2,000 for optics, handles, wipers, grille detail,
hinges and struts. That leaves another 119 under the **60,000** ceiling.
These are future allowances, not built parts. Flat interior panels will use
large quads; hidden seat/frame faces and surfaces below interior liners will
be omitted. Keep silhouette and optical edges dense. The present form target
is checked at 47,000 to protect that reserve.

Five temporary clay materials, **zero image textures**, no hatch GLB. Generated
game/high files are 1,038,633 / 2,606,391 bytes; none is committed. The
later delivery remains one shared-family-compatible 2048² BaseColor / OpenGL
Normal / ORM allocation; no texture-memory claim is made for an unbuilt atlas.

## Rebuild and evidence

From the repository root:

```sh
make -C cars BODY=hatch
make -C cars BODY=hatch check
python3 -m py_compile cars/src/hatch_*.py
```

The default target fetches registered image/PDF references, builds both source
densities, checks them, renders the 26 native views and generates the
53-image review contact sheet. `WIDTH`, `SAMPLES` and `PASS` are optional;
defaults are 1600 px, 40 samples and `hatch-round2`. Profile comparisons render
at the photographs’ native 2100 px width. Cycles work uses the
kit GPU lock. Orthographic form views use Workbench. Every render records the
source SHA-256; review rejects mixed source revisions. Failed Make targets
are removed rather than cached as successful reports.

The source checks cover dimensions, budget, closed positive moving solids, audited
fixed-skin boundaries and normals; actual aperture clearance/depth; door sections and crown heights;
five longitudinal body-section stations plus three each across hood and roof;
camera projection agreement; and repository rules. Curvature is a finite
normal-slope derivative, with raw reversals and construction-line zones kept
in the report. These checks do not prove fairness between stations. UV,
bake, motion, export and re-import are explicitly pending at this gate.
Independent factory-empty regeneration matches all **133 objects / 120 meshes**
exactly, including vertices, polygons, corner normals, material slots, transforms
and parents (`build/hatch/determinism.json`).

Evidence under `renders/hatch-round2/`:

- `contact.jpg`: complete 53-image sheet.
- `front_three_quarter.jpg`, `rear_three_quarter.jpg`, `side_raking.jpg`.
- `side-dimensions.jpg`, `front-dimensions.jpg`, `rear-dimensions.jpg`,
  `top-dimensions.jpg`, and `front-rear.jpg`.
- `side-perspective-corolla.jpg`, `side-perspective-hyundai.jpg`, with regional
  deviations in `side-perspective.json`; original-method overlays remain.
- `side-rounds-*.jpg`: original checkpoint beside the current matched overlay.
  `side-methods-*.jpg`: both methods on the same current geometry.
- `stripes_horizontal.jpg`, `stripes_vertical.jpg`, both rear and side
  directions, and `stripes_hood_driver.jpg`.
- `curvature-body.jpg`, `curvature-hood-roof.jpg`, corresponding uncut-parent
  plots under `parent/`, five transverse cuts and the 1 mm-offset centerline.
- `corolla_front`, `corolla_rear`, `hyundai_front`, `hyundai_rear`:
  `-pair.jpg` striped pairs, `_clay-pair.jpg` neutral pairs and calibration
  overlays. Chassis-anchor RMS is 3.59 / 2.95 / 5.02 / 7.81 px respectively.
  `corolla_side` and `hyundai_side` add the two profile pairs.
- `rear-reference-*.jpg`, `rear-comparison-*.jpg`, marked glazing dimensions
  and `tonal-range.json`.

## Pickup preservation and shared changes

The baseline was rebuilt from `34c6d1f` in an archive under this worktree's
`build/hatch-baseline/`. Its ordinary pickup export completed. A fresh current
default pickup build was then compared with the baseline game source using
`src/compare_pickup.py`; the current exporter also re-exported the baseline
finalized source with its unchanged baked maps.

**472 source objects / 454 meshes match exactly**: vertices, polygons, corner
normals, transforms, parents and material slots. **All 150 GLB accessors,
embedded maps and delivery graph match**. Both GLBs are **11,530,720 bytes**, SHA-256
`58661d0c2e11c2050e10677e12fabdf61570a3d25dc53837b485fee5c55a85ea`.
The report is `build/hatch/pickup-round2-preservation.json`. This proves fresh source
generation and serialization compatibility; it does not claim a second GPU
bake produced identical pixels.

Round 2 changes no shared code, sedan module or kit file. Round 1’s only
shared code changes were the isolated `BODY=hatch` Make dispatch and
optional per-body tire segmentation in `wheels.py`. H120 uses 48 game tire
segments; pickup and sedan retain their existing 64-game/96-high defaults.
Those changes have separate commits. No sedan module or kit file changed.

## Perspective overlays and remaining form limits

The two profile cameras now use the kit pinhole solver, with near-wheel
centers and tread contacts. No body-outline point enters the fit. Chassis RMS
at native 2100 px is **4.30 px Corolla / 4.31 px Hyundai**, with estimated
70.8 mm lenses. Four coplanar anchors leave depth and lens weakly constrained;
the explicit 65 mm prior and 45–100 mm bounds remain part of the estimate.
Errors below are screen separations converted at the body center plane, not
recovered 3D surface errors; manual pick uncertainty is about ±16 mm.

| Region | Corolla max, mm | Hyundai max, mm | Chosen comparison |
| --- | ---: | ---: | --- |
| Nose | 6.8 | 9.0 | Both |
| Hood | 36.5 | 24.9 | Both |
| Windshield header | 38.7 | 18.1 | Both |
| Roof | 34.2 | 45.2 | Corolla |
| Spoiler | 9.1 | 180.7 | Corolla |
| Backlight | 20.5 | 151.4 | Corolla |
| Gate | 41.0 | 142.3 | Corolla |
| Front bumper | 45.6 | 4.5 | Hyundai |
| Rear bumper | 47.8 | 31.6 | Hyundai |

The Corolla governs the roof, spoiler, backlight and gate; Hyundai governs
the lower bumpers. The two photographed upper tails disagree by substantially
more than 40 mm. The H120 does not meet both outlines there, and the camera
fit is not adjusted to conceal that difference. `side-rounds-*.jpg` places
the original checkpoint’s orthographic overlay beside this round’s perspective
overlay. `side-methods-*.jpg` isolates the two projection methods on the new
geometry. `side-perspective.json` retains every pick and deviation.

The broad D-pillar transition remains the weakest reflection area. Thin
aperture rims still show small angular marks, the mirror shoe is heavy, and
the straight rear garnish is generic. Side-window and door-cut corners remain
more regular than the references.
Fine lamp optics, transparent glass, interior and paint are absent by design
at this form gate. Final visual critique is in [REVIEW.md](REVIEW.md).
Nothing is needed from the lead to rebuild this checkpoint.
