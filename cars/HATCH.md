# Alder H120 — form round 3

An original compact five-door hatchback in the 2018–2022 class. This is the
requested **source-form checkpoint**, before interior, underbody detail,
hinges/struts, paint, UVs, baking or hatch GLB delivery.

![Front clay](renders/hatch-round3/front_three_quarter.jpg)
![Rear clay](renders/hatch-round3/rear_three_quarter.jpg)

Round three sharpens the side's shoulder and rising lower crease, crowns the
wheel areas, draws the gate inward between the lamps, and gives its lower hem
a shadow over the bumper. The black lower bumper and tall reflectors follow
the Corolla's construction. Crowned, tapered door mirrors replace the blocky
caps. A curved grille surround approaches the inner lamp ends. The package,
greenhouse, spoiler, door-mounted mirror positions, gate cut and plate pocket
remain at their accepted locations.

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
accuracy. Regional deviations in `renders/hatch-round3/side-perspective.json`
are projected millimeters at the body center plane, with about ±16 mm manual
pick uncertainty; they are not recovered 3D surface errors. Both makes' errors
remain visible in the overlays.

| Region, maximum absolute projected deviation | Corolla | Hyundai |
| --- | ---: | ---: |
| Hood | 38.7 mm | 27.1 mm |
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
the Corolla gate increases from 41.0 to 45.6 mm, hood from 36.5 to 38.7 mm,
and nose from 6.8 to 22.8 mm. The last change is approximately the manual-pick
uncertainty. These are disclosed changes, not a claim of exact silhouette
preservation. The larger Hyundai upper-rear differences remain intentional:
that region follows the shorter Corolla greenhouse.

## Side sculpture

The game mesh samples the shoulder on both sides of its narrow normal turn.
The lower hollow now lies above a sharper rising crease and dies out behind
the rear wheel, instead of carrying a second ripple into the molded bumper.

| Measured normal turn | Front door | B-pillar | Rear door |
| --- | ---: | ---: | ---: |
| Shoulder, over 30 mm vertical span | 23.79° | 23.89° | 23.87° |
| Lower crease, over 30 mm vertical span | 12.78° | 15.67° | 16.20° |
| Lower 30 mm window center height | 473 mm | 484 mm | 503 mm |
| Concave run, 50 mm chord depth | 3.67 mm | 3.82 mm | 3.88 mm |

Shoulder surface chords are about 30.2 mm; lower chords are 30.8–31.9 mm.
Angles interpolate the actual authored game corner normals used in rendering.
Positions and distances come from mesh rays. The report retains every endpoint,
normal and search interval. The older 80 mm lower-crease test also remains,
now measuring 16.49° / 17.37° / 16.73°; its longer window locates a different
maximum and must not be confused with the narrower measurement.

Above the wheels, outward swell relative to a same-height door is
**31.7 / 31.8 mm** front/rear. The crown's normal turns **13.62° / 9.60° over
70 mm**, with 70.1 / 70.3 mm surface chords. Hood-edge-to-front-fender rises are
23.0 / 20.4 / 15.5 mm at y = −1.60 / −1.30 / −1.14 m. Both stripe directions
expose the shoulder, lower hollow and wheel-area roll.
The lower crease is clearer in the neutral photo pairs. The improvement in the
unchanged low-sun raking view is modest: it still lacks the photographs' richer
light-to-shadow turn. The measurements do not settle that visual weakness.

## Rear, mirrors and face

The lower gate is sculpted in both plan and section. At x = 0 / 250 / 500 mm,
its lower hem stands **32.31 / 31.76 / 32.51 mm** behind the bumper surface
sampled at z = 610 mm. This is actual mesh-to-mesh projection, not the control
parameter. Between z = 760 and 880 mm, the central concave run lies **24.18 mm**
inside its chord; at x = 250 mm the depth is **14.46 mm**, diminishing toward the
convex lamp corners. In plan at z = 835 mm, the center is **16.63 mm** inside
the chord between x = ±450 mm.

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

Round three corrects the ordering of the front fender control rows and samples
sharp turns more closely. Aperture clipping and triangulation happen in the
flat parameter chart. Constrained retriangulation removes interior clipping
fragments while preserving original sample positions and true boundaries.
Coverage probes retain narrow fragments where necessary; residual numerical
coverage error is bounded in physical meters, at 20 microns. Parent normals
survive separation. Lenses preserve one consistent chart winding and receive
an explicit 1.5 mm gauge along the parent normals; all six have positive volume
and zero edges with inconsistent winding. Paint/black boundaries are split
after aperture cutting.

Steel gauge is 0.9 mm, glass 4.8 mm, fascia 3–4 mm, and arch flanges turn inward
18 mm. Fixed stampings omit only buried reverse tessellation, retaining outer
faces and visible returns with audited inner boundaries. **Moving closures,
including all four doors, retain their backs.** The game assembly is not
reported as an entirely closed solid.

| Part group | Game triangles |
| --- | ---: |
| Body skins, roof and closures | 10,118 |
| Front/rear fascia skins | 11,267 |
| Four door skins | 4,692 |
| Pillars and appliques | 1,350 |
| Glazing | 1,504 |
| Arch flanges | 784 |
| Wheelwell liners | 1,168 |
| Openings, returns, beds and grille | 5,540 |
| Mirrors | 1,016 |
| Roof spoiler | 1,184 |
| Four tires | 4,224 |
| Four wheels | 3,984 |
| Temporary cavity closure | 12 |
| **Total** | **46,843** |

The **46,881 form allocation and 59,381 finished plan remain unchanged**.
The current form leaves 38 triangles unspent within that allocation. Keep
8,000 for the cabin (seats 3,500; dash 1,500; controls 500; door cards 1,200;
cargo 1,300), 2,500 underneath, and 2,000 for optics, handles, wipers, grille
detail, hinges and struts. Current form plus those allowances is **59,343**;
the separate 500-triangle contingency still fits below 60,000. Allowances are
not built parts. The high source is **114,174 triangles**.

Five temporary clay materials, **zero image textures**, no hatch GLB.
Generated game/high files are **1,059,996 / 2,427,423 bytes**. Later delivery
still targets the family's 2048² BaseColor / OpenGL Normal / ORM allocation.
The present form has no baked-texture memory claim.

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

Defaults are `PASS=hatch-round3`, `WIDTH=1600`, `SAMPLES=40`; profile comparisons
render at native 2100 px. Cycles uses the kit GPU lock. Orthographic form views
use Workbench. No downloaded lighting or model data is used. Missing round-two comparisons
are reconstructed from local revision `082ca31` under `build/`; no other
checkout is changed. A full-history clone is needed for historical comparisons.

The build produces both source densities, package and topology audits, aperture
and contact measurements, round-two preservation checks, new surface numbers,
eleven game and parent curvature stations, camera verification and repository
checks. Raw curvature reversals and construction zones remain in the reports;
the wheel-crown zone extends from the actual arch crown to the shoulder,
including its intentional lower concave blend. Passing
sampled sections does not prove that every reflection is fair.

The dense-parent normal query uses Blender's native BVH to avoid copying
millions of triangle corners into Python. A 783-ray comparison against the
original corner-field query gave zero positional discrepancy and at most
1.23e−7 normal-vector difference. Independent regeneration matches all
**132 objects / 119 meshes** exactly, including vertices, polygons, normals,
materials, transforms and parents (`build/hatch/determinism.json`).

Evidence in `renders/hatch-round3/` includes:

- `contact.jpg`: the full 54-image review sheet; 27 native renders.
- `round2-round3-contact.jpg` and `round2-round3-*.jpg`: unchanged-camera comparisons,
  including every calibrated pair, with source hashes and camera checks.
- Front/rear clay heroes, `side_raking.jpg`, four orthographic views and dimensions.
- Front, rear and side stripes in both directions, the driver's hood view,
  and `stripes_rear_unpainted.jpg`.
- Six calibrated stripe pairs and six neutral pairs, perspective profiles,
  regional deviations, sections, curvature plots and `tonal-range.json`.

Every native view and game measurement names the final source SHA-256:
`d6901bfc3cb9f97bf78a90580bec2972df16ec06f5356df1b7f2dc3d7fffc3da`.
These are source renders. UV, bake, motion, export and re-import checks remain
outside this requested checkpoint.

## Pickup preservation and limits

A fresh default pickup build matches **472 objects / 454 meshes** from the
accepted baseline. Re-exporting its unchanged finalized source and maps matches
all **150 GLB accessors**, embedded images, delivery graph and full file bytes.
Both GLBs are **11,530,720 bytes**, SHA-256
`58661d0c2e11c2050e10677e12fabdf61570a3d25dc53837b485fee5c55a85ea`.
See `build/hatch/pickup-round3-preservation.json`. This proves source generation
and serialization compatibility; it does not claim a second identical GPU bake.
No shared family implementation, sedan module or kit file changed in round three.

The remaining form weaknesses are an understated side in the low-sun view,
crowded D-pillar reflections, small angular marks at the cowl and extreme lamp
tips, residual lower-corner reflection crowding, and a mirror cap softer than
the Hyundai's molding. The side-window corners and straight door cuts remain more
regular than the photographs. Empty optics, opaque glass, bare wheels and the
missing interior are separate stage omissions. [REVIEW.md](REVIEW.md) records
the region critiques and whole-car assessment. This is a stop at the form gate,
not approval for final delivery.
