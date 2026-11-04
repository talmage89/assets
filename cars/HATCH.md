# Alder H120 — form round 4

An original compact five-door hatchback in the 2018–2022 class. This is the
requested **source-form checkpoint**, before interior, underbody detail,
hinges/struts, paint, UVs, baking or hatch GLB delivery.

![Front clay](renders/hatch-round4/front_three_quarter.jpg)
![Rear clay](renders/hatch-round4/rear_three_quarter.jpg)

Round four repairs the hood/cowl control-sheet folds and the game triangles
that crossed the lamp-end crowns. The gate gains a narrow upper crease while
retaining its measured hollow and lower lip. A neutral clearcoated gloss clay
under an original procedural sky and dark ground makes the accepted side lines
read through reflected value. The package, main greenhouse, mirrors, gate cut, plate pocket, lamp sizes and
pickup remain preserved. The repaired cowl includes a localized change to the
lowest windshield corners, measured below.

[Gloss front](renders/hatch-round4/gloss_front_three_quarter.jpg),
[gloss rear](renders/hatch-round4/gloss_rear_three_quarter.jpg), and
[round-four contact sheet](renders/hatch-round4/round4-contact.jpg).

## Measured package and references

[REFERENCE.md](REFERENCE.md#alder-h120-compact-five-door-hatchback-source-form-checkpoint)
and [refs/SOURCES.md](refs/SOURCES.md) identify the manufacturer dimensions and
all thirteen photographs/drawings. Photographs are for measurement and review;
none enters the geometry or supplies a texel.

| Measurement | Actual game mesh | Basis |
| --- | ---: | --- |
| Length × body width × height | 4363.0 × 1796.5 × 1450.6 mm | Original 4360 × 1795 × 1450 package, ±4 mm |
| Wheelbase | 2650.0 mm | Corolla 2640; Hyundai 2650 |
| Front / rear track | 1550.0 / 1560.0 mm | Accepted wheel package |
| Front / rear overhang | 927.0 / 785.9 mm | Accepted 925 / 785 targets |
| Width across mirrors | 2039.3 mm | Hyundai UK sheet: 2039 |
| Tire-to-arch vertical gap | 40.0 mm, all four | Accepted 30–50 range |
| Windshield / backlight rake | 60.48° / 46.58° from vertical | Accepted greenhouse |
| Rear-glass top / base width | 1192 / 1409 mm | Horizontal cuts; broader Hyundai base |
| Spoiler overhang | 106.9 mm | Beyond upper glass samples |

Tires remain 225/40R18 proxies: 629.2 mm modeled circular diameter at
314.6 mm hub height, rather than a loaded contact deformation. Ground clearance
is not certified; 140 mm remains the future underbody target. The present
floor is a small recessed cavity closure.

The six calibrated cameras are unchanged. Profile fits use wheel centers and
tread contacts, never body-outline points: **4.298 px Corolla / 4.312 px Hyundai
RMS** at native 2100 px width. The Corolla governs the upper rear profile and
Hyundai the lower bumpers. Four coplanar anchors and the lens prior limit depth
accuracy. Regional deviations in `renders/hatch-round4/side-perspective.json`
are projected millimeters at the body center plane, with about ±16 mm manual
pick uncertainty; they are not recovered 3D surface errors. Both makes' errors
remain visible in the overlays.

| Region, maximum absolute projected deviation | Corolla | Hyundai |
| --- | ---: | ---: |
| Hood | 36.5 mm | 24.9 mm |
| Windshield header | 38.7 mm | 18.1 mm |
| Roof | 34.2 mm | 45.2 mm |
| Spoiler | 9.1 mm | 180.7 mm |
| Backlight | 20.5 mm | 151.4 mm |
| Gate | 45.6 mm | 126.5 mm |
| Nose | 22.8 mm | 9.0 mm |
| Front bumper | 45.6 mm | 4.5 mm |
| Rear bumper | 45.6 mm | 31.6 mm |

The selected Corolla roof/spoiler/backlight and Hyundai lower-bumper maxima
retain their round-two values. Small deviations elsewhere are not identical:
the Corolla gate remains at 45.6 mm versus round two's 41.0 mm, and the nose
remains at 22.8 mm versus 6.8 mm. The hood returns to 36.5 mm from round three's
38.7 mm; the Hyundai hood improves from 27.1 to 24.9 mm. The last change is smaller than the manual-pick
uncertainty. These are disclosed changes, not a claim of exact silhouette
preservation. The larger Hyundai upper-rear differences remain intentional:
that region follows the shorter Corolla greenhouse.

## Side sculpture

The game mesh samples the shoulder on both sides of its narrow normal turn.
The lower hollow lies above a sharper rising crease. Round four adds 2–3 mm
of draw between the wheel openings, after the gloss pairs showed its value
change was too weak. That extra draw fades into the wheel openings; the
accepted molded-end relief remains. The original hollow dies out behind
the rear wheel before it can emboss a second ripple into the bumper.

| Measured normal turn | Front door | B-pillar | Rear door |
| --- | ---: | ---: | ---: |
| Shoulder, over 30 mm vertical span | 23.79° | 23.89° | 23.87° |
| Lower crease, over 30 mm vertical span | 16.52° | 21.84° | 24.72° |
| Lower 30 mm window center height | 473 mm | 484 mm | 503 mm |
| Concave run, 50 mm chord depth | 4.67 mm | 5.20 mm | 5.49 mm |

Shoulder surface chords are about 30.2 mm; lower chords are 30.8–32.3 mm.
Angles interpolate the actual authored game corner normals used in rendering.
Positions and distances come from mesh rays. The report retains every endpoint,
normal and search interval. The older 80 mm lower-crease test also remains,
now measuring 20.78° / 24.30° / 24.58°; its longer window locates a different
maximum and must not be confused with the narrower measurement.

Above the wheels, outward swell relative to a same-height door is
**31.7 / 31.8 mm** front/rear. The crown's normal turns **12.46° / 9.60° over
70 mm**, with 70.0 / 70.3 mm surface chords. Hood-edge-to-front-fender rises are
22.9 / 24.2 / 11.6 mm at y = −1.60 / −1.30 / −1.14 m. Both stripe directions
expose the shoulder, lower hollow and wheel-area roll.
The unchanged low-sun raking view lights both sides of a horizontal crease
similarly. The new gloss side and calibrated pairs instead show a bright
shoulder over a darker door, the rising lower reflection break and the wheel
crowns. These reflections, alongside the stripes, provide the visual check.

## Rear, mirrors and face

The lower gate is sculpted in both plan and section. At x = 0 / 250 / 500 mm,
its lower hem stands **33.37 / 32.90 / 32.55 mm** behind the bumper surface
sampled at z = 610 mm. This is actual mesh-to-mesh projection, not the control
parameter. Between z = 760 and 880 mm, the central concave run lies **24.00 mm**
inside its chord; at x = 250 mm the depth is **14.09 mm**, diminishing toward the
convex lamp corners. In plan at z = 835 mm, the center is **15.61 mm** inside
the chord between x = ±450 mm.

The upper crease turns the rendered game normals **34.51 / 32.99 / 16.42°**
at x = 0 / 250 / 450 mm across a **30 mm vertical span**. Corresponding surface
chords are 32.22 / 30.81 / 30.62 mm; the sampled centers are z = 895 / 892 /
889 mm. These are rays and interpolated game normals, not the die parameters.
The central vertical, off-center vertical and central plan depths differ from
round three by only −0.18 / −0.37 / −1.02 mm. The top ridge and retained hem
bound the recess, rather than leaving an unbounded soft indentation.

The gate shut line remains at about z = 645 mm. The bumper's central painted
band spans **570–644 mm**; painted corners extend down to about 226 mm. Black
occupies the lower center around the plate, following the Corolla. Its measured
width is **1454 / 1384 / 1270 mm** at z = 350 / 450 / 550 mm. Reflector envelopes
are about **19 × 198 mm in rear projection**, with the original 24 × 200 mm guide
following the curved corner. The reference estimates and uncertainty are in
REFERENCE.md. The unpainted rear stripe view exposes the entire bumper, including
surfaces otherwise hidden by the dark material.

The split taillamp corners remain about **125 mm** tall. Each lens and its cut
now use the same projected outline, with curved boundary samples in the lens
instead of long chords cutting through the body. The bumper plate mouth is
**319 × 166 mm**, its bed is **21.0–21.5 mm** recessed, and its overhead lamp
remains separate.

Mirrors retain **228 × 136 × 128 mm** outboard/height/depth envelopes and the
**2039.3 mm** overall span. A crowned top, rounded outboard end and tapered
front join a slim triangular door sail. Three actual silhouette vertices give
an outboard radius of **57.9 mm** in front projection. The rear pane remains
flat at y = −551 mm. Actual surface intersections verify sail/door and
shoe/housing support; this is parked contact evidence, not a motion sweep.

The upper grille has a narrow molded surround following the fascia's plan
curve. Its bed is **66.0–67.5 mm** behind the actual parent skin; the blades
follow that curved bed. The closest inner-lens-to-frame spacing is **15.0 mm**
on each side. The lower intake remains **51.0–53.1 mm** deep. Hood and lamp
corner reflections are supplied in both stripe directions.

## Construction and triangle allocation

The accepted one-sheet construction remains: 117,425 fitted control vertices,
116,736 quads, one connected component and valence-four interior vertices.
Original analytic sections fit the control net; Catmull–Clark evaluation
precedes every panel or aperture cut. The evaluated surface is not refitted.

The old hood/cowl sheet folded because swept transverse controls crossed
when the crown descended, compounded by a 20 mm fitting-weight handoff. Local
unswept rows and a 120 mm handoff remove those folds without refitting the
evaluated parent. Independent regeneration checks 38,034 parent faces near the
lamps and 52,552 at the cowl: none exceeds the 75° orientation diagnostic.
The original cowl had 1,049 suspect faces. The largest current deviations
from the intended section normal are 4.06° / 37.92° in those respective zones.

A separate fault lived only in the game mesh: thin chart-space triangles
became reversed physical chords at the lamp tips. Hood triangulation now uses
physical XY; fenders and rear turns use locally injective radial coordinates.
The front projection origin is below the crown's concave inner slope. Cut
boundaries, the gate lip and feature-aligned shoulder edges remain constrained.
The final hood/fender check finds no reversed triangles in the diagnosed region.
Two further small reversed fragments at the front arch and grille edge were
resolved by sampling the same parent more closely.

Local refinement resolves both normal height and reflected-normal change.
Redundant interior samples are retired only when replacement centroid and
edge-midpoint probes lie within 0.3 mm of the parent and interpolate its normals
within 1.5°. No fixed reduction ratio flattens a panel. Original cut intersections
may be retired only where the chart boundary remains collinear and its physical
chord misses by under 0.3 mm. The method reallocates triangles to tight turns;
retained vertices remain on the original evaluated sheet. It does not smooth
or replace the parent's shape after cutting. The normal transfer itself was
independently checked and was not the cause of the hood folds.

Direct round-three surface comparisons disclose the scope of that cowl repair.
The roof differs by at most 0.00014 mm and backlight by 0.0028 mm in two-way
vertex-to-mesh probes. Windshield and adjoining pillar surfaces above z = 980 mm
agree within 0.00015 mm. The lowest windshield tips around z = 943 mm move by
up to **29.49 mm**, and adjacent lower pillar corners by **26.52 mm**, where the
old sheet folded. This is a local change to the accepted glazing boundary;
the windshield's main surface, rake and header are preserved. Mirror housings,
spoiler and wheels match exactly; mirror-sail surface differences are below
0.00014 mm. Raw comparisons are in `build/hatch/round4-preserved-surfaces.json`
and `round4-preserved-main-glass.json`.


Steel gauge is 0.9 mm, glass 4.8 mm, fascia 3–4 mm, and arch flanges turn inward
18 mm. Fixed stampings omit only buried reverse tessellation, retaining outer
faces and visible returns with audited inner boundaries. **Moving closures,
including all four doors, retain their backs.** The game assembly is not
reported as an entirely closed solid.

| Part group | Game triangles |
| --- | ---: |
| Body skins, roof and closures | 12,717 |
| Front/rear fascia skins | 8,722 |
| Four door skins | 4,428 |
| Pillars and appliques | 1,374 |
| Glazing | 1,512 |
| Arch flanges | 784 |
| Wheelwell liners | 1,168 |
| Openings, returns, beds and grille | 5,612 |
| Mirrors | 1,016 |
| Roof spoiler | 1,184 |
| Four tires | 4,224 |
| Four wheels | 3,984 |
| Temporary cavity closure | 12 |
| **Total** | **46,737** |

The round-four comparison budget is **46,843 for form / 59,343 planned total**.
The current form leaves 106 triangles unspent. Keep 8,000 for the cabin (seats
3,500; dash 1,500; controls 500; door cards 1,200; cargo 1,300), 2,500 underneath,
and 2,000 for optics, handles, wipers, grille detail, hinges and struts.
Form plus those unchanged allowances is **59,237**; the separate 500-triangle
contingency still fits below 60,000. Allowances are not built parts.

Five temporary clay materials, **zero image textures**, no hatch GLB.
The game source is **1,084,081 bytes**. The high source has **110,922 triangles**
and occupies **2,303,895 bytes**. Both are temporary source artifacts. Later delivery still targets the family's 2048² BaseColor /
OpenGL Normal / ORM allocation; this form has no baked-texture memory claim.

Doors remain separate around vertical hinge pivots: left 0…72°, right −72…0°.
Hood and liftgate retain X-axis provisional pivots, −65…0° and −95…0° respectively.
Wheel assemblies retain axle pivots. These are intended ranges; hinge hardware,
travel clearances and moving fit are deferred, not certified by parked checks.

## Rebuild and review

```sh
make -C cars BODY=hatch
make -C cars BODY=hatch check
python3 -m py_compile cars/src/hatch_*.py
```

Defaults are `PASS=hatch-round4`, `WIDTH=1600`, `SAMPLES=40`; original profile
comparisons remain at native 2100 px. Cycles uses the kit GPU lock. The original
matte clay and stripe renderer is unchanged. Historical round-three comparisons
are rebuilt from local revision `da466e3` under `build/` when absent; no other
worktree is touched. A full-history clone is needed for historical comparisons.

The gloss uses scene-linear gray 0.18, roughness 0.22, coat weight 1 and coat
roughness 0.075. Blender's procedural sky supplies the upper hemisphere; a
200 m dark diffuse ground plane supplies lower-hemisphere reflections. No HDRI
or photograph is used for lighting. The ground is camera-invisible to retain
the existing pair framing, but remains visible in reflections. Both revisions
use exactly the same environment, exposure and cameras. The side now shows a
light shoulder above a darker wall, a rising lower reflection break and rolling
wheel-crown highlights. This is diagnostic clay, not production paint look-dev.

Five whole-game-body mean-curvature maps use signed cotangent mean curvature
with mixed Voronoi areas. The colors use an asinh scale at ±40 inverse meters;
raw values are retained, without spatial smoothing or outlier removal. Gray
marks incomplete cut-edge neighborhoods and unmeasured inserts. Analytic plane,
cylinder and sphere checks verify units and sign; maximum errors are 0,
0.000030 and 0.001018 inverse meters. The raw discrete map remains sensitive to
thin cut-adjacent triangles; the same-camera stripes and gloss must be read
beside it, not replaced by a threshold pass.

The build produces both source densities, package/topology audits, aperture and
contact measurements, round-two/three preservation checks, round-four crease
and depth measurements, an independently regenerated parent orientation check,
eleven game/parent section-curvature stations, camera verification and repository
checks. Independent regeneration matches all **132 objects / 119 meshes** exactly,
including geometry, normals, materials and transforms
(`build/hatch/round4-determinism.json`).

Evidence in `renders/hatch-round4/` includes:

- `contact.jpg`: the existing matte/stripe/photo review set.
- `round4-contact.jpg`: the new gloss/maps and round-three comparisons.
- `curvature-stripes-*.jpg`: five whole-body maps beside matching reflections.
- `gloss_*-pair.jpg`: six calibrated comparisons against both makes; plus gloss
  side, front/rear three-quarter and rear views.
- `round3-round4-*.jpg`: unchanged-camera comparisons, including every pair.
- Original matte heroes, raking side, orthographic views, both stripe directions,
  perspective profiles, measured sections and all earlier construction proofs.
- `mean-curvature.json`, `gloss-tonal-range.json`, `round3-round4.json` and
  `round4-shots.json`: raw values, tone, cameras and source hashes.

Every current native view and game measurement names source SHA-256
`62deb6c290f859e3fb930965bcc32a23b5dd1b0d344bcbd87f2de0e9a4c4d4d5`.
These are source renders. UV, bake, motion, export and re-import checks remain
outside this requested checkpoint.

## Pickup preservation and limits

A fresh default pickup build matches **472 objects / 454 meshes** from the
accepted baseline. Re-exporting its unchanged finalized source and maps matches
all **150 GLB accessors**, embedded images, delivery graph and full file bytes.
Both GLBs are **11,530,720 bytes**, SHA-256
`58661d0c2e11c2050e10677e12fabdf61570a3d25dc53837b485fee5c55a85ea`.
See `build/hatch/pickup-round4-preservation.json`. This proves source generation
and serialization compatibility; it does not claim a second identical GPU bake.
No shared family implementation, sedan module or kit file changed in round four.

The narrow hood crowns and gate are substantially calmer in gloss. The raw
maps and tight stripes still show small irregularities near cut boundaries,
the rear shoulder termination and the crowded D-pillar transition. The regular
window corners and door cuts, empty optics, opaque glass and absent cabin still
make the car read as CG. The broad horizontal grille bars look older than either
reference. [REVIEW.md](REVIEW.md) records the region and whole-car critiques.
Stop here for the requested form checkpoint; no detail or look phase was started.
