# Alder H120 — form checkpoint

An original compact five-door hatchback in the 2018–2022 class. This checkpoint
contains the outer body, glazing, wheels, real panel gaps, recessed lamps and
fascia openings. It stops before interior, hinges/struts, underbody detail,
paint, UVs, baking and hatch GLB delivery.

![Front clay, generated locally](renders/hatch-checkpoint/front_three_quarter.jpg)
![Rear clay, generated locally](renders/hatch-checkpoint/rear_three_quarter.jpg)

The package compares Toyota Corolla and Hyundai i30/Elantra GT, with a level
roof, short rear overhang, steep backlight and nearly upright lower gate.
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
| Length | 4361.0 mm | 4360; Toyota 4370, Hyundai 4340 |
| Body width | 1794.4 mm | 1795; Toyota 1790, Hyundai 1795 |
| Height | 1450.6 mm | 1450; Toyota 1435, Hyundai 1455 |
| Wheelbase | 2650.0 mm | Toyota 2640, Hyundai 2650 |
| Front / rear track | 1550.0 / 1560.0 mm | Original upper-wheel package; Hyundai N Line 1549 / 1563 |
| Front / rear overhang | 925.8 / 785.2 mm | Original 925 / 785; Toyota 935 / 795 |
| Width across mirrors | 2039.0 mm | Hyundai UK 2039 |
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
| Hood leading center height | 732.5 mm |
| Windshield rake from vertical | 60.48° |
| Roof center drop over y = 0.15…1.40 m | 23.3 mm / 1.07° |
| Backlight rake from vertical | 44.03° |
| Lower gate rake, z = 0.72…0.92 m | 9.32° from vertical |
| Spoiler overhang beyond upper glass samples | 98.7 mm |
| Side-glass tumblehome at B-pillar | 22.97° |
| Above-arch fender swell relative to same-height door | 29.6 mm front / 29.0 mm rear peak |
| Hood-side to fender crown at y = −1.60 / −1.30 / −1.10 m | 14.95 / 21.61 / 10.12 mm |
| Headlamp centerline along surface | 691.1 mm each |
| Headlamp maximum sampled height | 89.6 / 92.8 mm |
| Headlamp outer-end rise | About 139 mm |
| Grille / lower intake normal recess depth | 60–62 / 55–57 mm |
| Corner-pocket depth | 49.8–50.8 mm |
| Plan setback at x = 800 mm, front / rear | About 229 / 231 mm at bumper height |
| Rear-glass top / base width | 1173 / 1411 mm |
| Projected D-pillar band | 145 mm |
| Split taillamp height at quarter corner | 124–129 mm |
| Plate-pocket mouth / bed, width × height | 317 × 167 / 314 × 159 mm |
| Plate-pocket depth | 25.0–25.4 mm |
| Mirror housing, outboard × height × depth | 234 × 141 × 126 mm |
| Mirror housing bottom height | 981 mm |

Rear-glass widths are horizontal cuts 35 mm below the glass top and 45 mm above
its lowest point. The projected pillar band compares upper-quarter and glass
widths; it is not a structural metal thickness. Photograph estimates are
1173 versus 1114/1149 mm at the top and 1411 versus 1232/1385 mm at the base,
with ±30 mm photographic uncertainty. The glass follows the broader Hyundai
base; it deliberately does not duplicate the narrower Corolla opening.

The three requested door sections are measured at y = −0.335, +0.255 and
+0.755 m. Normal turns use the actual rendered parent corner-normal field;
positions use intersections with the game mesh.

| Section feature | Mid-front door | B-pillar | Mid-rear door |
| --- | ---: | ---: | ---: |
| Shoulder height | 885 mm | 893 mm | 899 mm |
| Upper-door inward lean | 20.18–20.62° | 20.20–20.63° | 20.22–20.64° |
| Lean 40 mm below shoulder | 4.60° | 4.56° | 4.56° |
| Lower-door lean | 16.40° | 15.84° | 15.26° |
| Lower crease normal turn over 80 mm | 10.56° | 10.06° | 9.83° |
| Located soft crease height | 459 mm | 482 mm | 502 mm |
| Concave run, 50 mm chord depth | 1.74 mm | 1.85 mm | 1.81 mm |
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

**53,384 game triangles**, within 55,000, but above the approximately 45k aim.
The high source has **122,232 triangles**. This allocation prioritizes rear
corner and glazing reflection continuity; it leaves only 1,616 triangles of
the final ceiling. Hidden gauge backs and fixed-body draw calls need further
optimization before the later interior/detail stage.

| Part group | Game triangles |
| --- | ---: |
| Body skins, roof and closures | 15,252 |
| Front/rear fascia skins | 13,900 |
| Four door skins | 4,132 |
| Pillars and appliques | 2,152 |
| Glazing | 1,448 |
| Arch flanges | 784 |
| Wheelwell liners | 1,168 |
| Apertures, returns, beds and grille blades | 4,028 |
| Mirrors | 2,032 |
| Roof spoiler | 268 |
| Four tires | 4,224 |
| Four wheels | 3,984 |
| Temporary cavity closure | 12 |
| **Total** | **53,384** |

Per-mesh counts for all 118 meshes and per-parent sums are in
`build/hatch/form-check.json`. The hood has 560 triangles; liftgate group 1,988;
front door groups 1,964 each including mirrors; rear door skins 1,132/1,104;
each wheel/tire group 2,052. Grouping is provisional: full moving assemblies,
window attachments and clearance sweeps belong to the next stage.

Five temporary clay materials, **zero image textures**, no hatch GLB.
Generated game/high `.blend` files are 1,235,540 / 2,545,831 bytes. None is
committed. Later delivery remains one shared-family-compatible 2048²
BaseColor / OpenGL Normal / ORM allocation; no texture-memory claim is made
for an unbuilt atlas.

## Rebuild and evidence

From the repository root:

```sh
make -C cars BODY=hatch
make -C cars BODY=hatch check
python3 -m py_compile cars/src/hatch_*.py
```

The default target fetches registered image/PDF references, builds both source
densities, checks them, renders the 22 requested views and generates the
41-image review contact sheet. `WIDTH`, `SAMPLES` and `PASS` are optional;
defaults are 1600 px, 40 samples and `hatch-checkpoint`. Cycles work uses the
kit GPU lock. Orthographic form views use Workbench. Every render records the
source SHA-256; review rejects mixed source revisions. Failed Make targets
are removed rather than cached as successful reports.

The source checks cover dimensions, budget, closed positive solids and
normals; actual aperture clearance/depth; door sections and crown heights;
five longitudinal body-section stations plus three each across hood and roof;
camera projection agreement; and repository rules. Curvature is a finite
normal-slope derivative, with raw reversals and construction-line zones kept
in the report. These checks do not prove fairness between stations. UV,
bake, motion, export and re-import are explicitly pending at this gate.
Independent factory-empty regeneration matches all **131 objects / 118 meshes**
exactly, including vertices, polygons, corner normals, material slots, transforms
and parents (`build/hatch/determinism.json`).

Evidence under `renders/hatch-checkpoint/`:

- `contact.jpg`: complete 41-image sheet.
- `front_three_quarter.jpg`, `rear_three_quarter.jpg`, `side_raking.jpg`.
- `side-dimensions.jpg`, `front-dimensions.jpg`, `rear-dimensions.jpg`,
  `top-dimensions.jpg`, and `front-rear.jpg`.
- `side-overlay-corolla.jpg`, `side-overlay-hyundai.jpg`, and raw JSON errors.
- `stripes_horizontal.jpg`, `stripes_vertical.jpg`, both rear and side
  directions, and `stripes_hood_driver.jpg`.
- `curvature-body.jpg`, `curvature-hood-roof.jpg`, corresponding uncut-parent
  plots under `parent/`, five transverse cuts and the 1 mm-offset centerline.
- `corolla_front`, `corolla_rear`, `hyundai_front`, `hyundai_rear`:
  `-pair.jpg` striped pairs, `_clay-pair.jpg` neutral pairs and calibration
  overlays. Chassis-anchor RMS is 3.59 / 2.95 / 5.02 / 7.81 px respectively.
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
The report is `build/hatch/pickup-preservation.json`. This proves fresh source
generation and serialization compatibility; it does not claim a second GPU
bake produced identical pixels.

The only shared code changes are the isolated `BODY=hatch` Make dispatch and
optional per-body tire segmentation in `wheels.py`. H120 uses 48 game tire
segments; pickup and sedan retain their existing 64-game/96-high defaults.
Those changes have separate commits. No sedan module or kit file changed.

## Remaining form limits

The raw orthographic/photo overlays do not meet the requested 40 mm envelope
at every point: worst sampled deviations are **157.5 mm at the Corolla
backlight and 113.3 mm at the Hyundai chin**. Finite photographic perspective
and the intentionally different rear profile are visible; no outline fitting
hides them. Exact
final deviations and the fourth region-by-region critique are recorded in
[REVIEW.md](REVIEW.md).

The broad D-pillar turn and lower bumper corners remain the weakest reflection
areas. Door cuts and spoiler ends are more regular than the photographed cars,
and the end-fascia/lamp transitions still need further refinement. The body
reads as a compact hatch, but this is a form-review handoff, not final surface
or production approval. Nothing is needed from the lead to rebuild it.
