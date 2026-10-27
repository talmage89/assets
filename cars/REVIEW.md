# Alder C150 / body-form review gate

**Stopped before detail, materials, wear, UVs, bake and export.** This is a
reviewable source checkpoint, not a finished or game-ready delivery claim.
The primary evidence is [the contact sheet](renders/checkpoint/contact.jpg),
[front pair](renders/checkpoint/match_front-pair.jpg),
[rear pair](renders/checkpoint/match_rear-pair.jpg), and the
[striped side](renders/checkpoint/stripes_side.jpg).

Every rendered view was opened, individually or in a sheet of every view of its
pass. The comparisons are against the credited photographs, not memory. All
meshes and shader/light data are original scripts; photos are comparison only.

## Second checkpoint — lead rejection and replacement form

The lead rejected the first checkpoint as a melted 1980s truck. That judgment
is correct. The previous self-review was too lenient: the dimensional checks
passed while the body language, greenhouse and striped reflections did not.
The historical passes below are retained as a record, not as approval.

### Revision pass A — replace the surface method

Color/value first: compare neutral clay with the white reference without
pretending their different albedos are a match. Keep tires, glazing and cavities
dark; do not raise exposure to erase the shape defects.

Removed the additive sine/Gaussian hood/side sculpting. The replacement uses
explicit section stations, near-planar ruled quad patches, short tangent
fillets and a separate supported shoulder strip. The raised hood center has
flat fields and crisp transitions. Initial sampling made inverted shoulder
rows at the hood cap; those spiked badly and were rejected, then corrected.
Broad door and hood reflections now run without the former sweeping lumps.
This is not subdivision modeling; the patches evaluate authored sections
with exact derivatives. The resulting stripes, rather than the method's name,
are the criterion.

### Revision pass B — compare the greenhouse against a true profile

Color/value first: a 50% blue silhouette is deliberately diagnostic, not paint
look development. The photograph stays visible under it.

Added the credited 145-inch-wheelbase / 5.5-foot crew-cab profile. Its wheel
centers alone set the overlay's scale and placement. Measured the straight
A-pillar segment at 34.4 +/-1.5 degrees above horizontal. Replaced the old
near-upright windshield with a straight 35.2-degree outer pillar, added side
glass tumblehome, narrowed and crowned the roof, and connected its front and
rear edges to headers. No separate roof-rail plate remains.

The overlay exposed an excessively high hood leading edge; lowered that edge
40 mm while retaining the raised center. The source roof and bed remain higher
and more square than the photo. The published photo caption is 4x2 and our
envelope is 4x4, so the overlay exposes that difference rather than fitting it
away. This caption caveat does not excuse the remaining blunt roof corners or
high hood/front profile.

### Revision pass C — construction and reflection failures

Color/value first: the procedural stripe dome retains dark cavities and soft
highlight rolloff. Pale clay alone had concealed these defects.

Removed the black rectangular liner plates below the arches. Liners now end
inside the upper openings. Replaced arch displacement on a rectangular body
grid with annular quad patches: a flat inner lip, supported radial transition,
and a taper into the rocker. Concentrated angular stations at the ends rather
than increasing all panel grids. Added capped bed rails, the tailgate's top
lip and upright rear lamp envelopes. Rebuilt the nose around original tall
grille/headlamp form volumes. The front bumper corners now sweep back 180 mm,
with an upper return and matching valance, reducing their former detached
side silhouette; the rear step shelf tucks under the tailgate.

The stripes also exposed a sheet-gauge shading fault: normals encoded before
closing the sheet could be distorted when its smoothing fans changed. Reseed
the authored skin normals after gauge evaluation; leave hidden gauge faces
flat. An independent broad-panel slope comparison now samples 2,736 corners,
with maximum normal disagreement 0.0198 degrees. This checks the shading
against the mathematical surface; it does not certify artistic fairness.

The annular flares still compress and curl the stripes where they die into the
rocker. Increasing their angular sampling from 48 to 64 did not materially
improve that shape, so reverted the extra triangles. **Those ends remain the
weakest surface; they are not declared fair or approved.**

### Revision pass D — calibrated pairs and final critique

Color/value first: do not compare gray clay brightness directly with white
factory paint. This gate judges form; final paint depth, clear coat, tint and
causal wear remain entirely unapproved. The cavity/tire values remain dark,
and the final orthographic foreground statistics are saved in
`renders/checkpoint/tonal-check.json`.

Re-picked the photographed hubs and soft tire contacts at enlarged resolution.
Two outer hub centers, two visible tread-contact centroids and an opposite-side
contact now constrain each camera. The opposite-side point fixes the previous
near-coplanar camera-height ambiguity. Final RMS: **5.69 px front / 5.11 px rear**
in original reference pixels, versus the former ~74 px. Symmetric transparent
comparison margins keep the original design's square corners in frame. All
five residuals and world/pixel coordinates remain in `matched-cameras.json`;
no landmark was silently removed from the displayed RMS.

This is explicitly a five-chassis-anchor fit. The requested few-pixel fit of
roof corners, mirror and bumper corners has **not** been achieved. Their exact
3D correspondence to this original design is uncertain; forcing those estimates
into the solve would hide rather than resolve the shape differences. The
independent side overlay is the stronger proportion evidence. The stock images'
published 4x2 caption and different wheels also limit ride-height comparisons.

Final art-direction critique against both pairs and the side overlay:

- The rake, narrower roof, upright sides and continuous shoulder read much
  closer to a late-2010s crew cab than the rejected shell.
- Hood and broad door bands are straight and continuous; the nose and bed no
  longer use soft global corner displacements. The arch ends and the windshield header still pinch/curl the
  reflections and deserve another surface correction before final acceptance.
- The front face and bumper are still too slab-like beside the photograph.
  Lamp/grille proportions are now established, but the corners lack the
  convincing transition between front face, fender top and body side.
- Roof/backlight corners and rear door outlines remain more rectangular than
  the class reference. The roof is attached, but its edge still reads hard.
- The hood leading silhouette remains higher and blunter than the side photo.
  The 4x2/4x4 mismatch explains some height, not all of this shape.
- The rear box/tailgate is especially plain. Its capped construction is present;
  subtle stamped shape is weaker than in the reference. Do not conceal this by
  adding badges, handles or texture detail.
- Tire-to-arch crown clearance is now 90.30 mm instead of 119.81 mm. Tire fill is
  more convincing, while parked deformation and simple wheels remain proxies.
- Underbody is intentionally open at this gate. This makes the low photo pairs
  less grounded than the real truck; no suspension/frame detail was added to
  camouflage the body critique.

**Stop at form review again.** This is an improved review candidate, not a claim
that all of the lead's fairness and camera requirements are satisfied. No
interior, brakes, final lights/glass/paint, wear, UVs, bakes or export were added.

### Current proof

`make -C cars clean` followed by `make -C cars WIDTH=1600` rebuilt the form
checkpoint from scripts. `make -C cars check` passes source geometry, dimensions,
normal slopes, budget, repository rules and Blender camera projection checks.
Projection agreement under 0.001 px proves calibrator/Blender consistency,
not photo or body accuracy. Per-object and per-category counts are in
`build/form-check.json`; the README lists the current 59,740-triangle total.
Six diagnostic materials, no texture images or GLB. High/game source files
are approximately 1.03 MB / 0.53 MB; they are ignored, not committed.

Opened every final rendered view in the contact sheet, and separately opened
the stripes, photo pairs, calibration plots and side overlay. Orthographic
foreground p5/p50/p95 values (0–255) are side 24/129/158, front 10/53/137 and
top 30/129/151, with zero bright-clipped pixels in all three masks. These are
clay diagnostics, not a final paint/hero tonal approval.

Latest evidence: [all views](renders/checkpoint/contact.jpg),
[side overlay](renders/checkpoint/side-overlay.jpg),
[rake measurement](renders/checkpoint/side-rake.jpg),
[front pair](renders/checkpoint/match_front-pair.jpg),
[rear pair](renders/checkpoint/match_rear-pair.jpg),
[front stripes](renders/checkpoint/stripes_front.jpg),
[side stripes](renders/checkpoint/stripes_side.jpg).

No kit files changed in this revision. A later generalization could move
post-gauge normal restoration into the shared panel helper, after testing
additional open/closed surfaces. No tool installation or new permission is
needed. The lead's next decision remains the body form; detail stays stopped.

## Historical first checkpoint (superseded)

## Pass 1 — reject the first envelope

Color/value first: the dark clay on transparent black was difficult to judge;
black tires and window wells merged into the viewer background. This is a
clay diagnostic problem, not a paint-albedo approval. Added neutral comparison
composites and more legible Workbench exposure while retaining dark tires.

`renders/form-01/`: the windshield leaned too far back, the roof looked like
separate flat strips, the hood-to-nose joint had a broad opening, and bumper
returns were missing. The rectangular upper window corners were an obvious
procedural tell. The initial 103,200-triangle source also spent too much on
redundant sheet grids. **Rejected.**

## Pass 2 — correct cab proportions and budget

Color/value first: retain charcoal tires and a darker glazing block against a
neutral body; do not brighten the whole asset to conceal the cavities.

`renders/form-02/`: steepened the windshield and extended the roof forward,
adjusted roof crown/rail heights, and brought the nose toward the hood. Reduced
game patch sampling without changing the tire circumference sampling. Source
audits passed at 56,292 triangles. The side proportions now read as a crew
cab/short bed, but the arch swelling was too soft and the doors too slab-like.
The first estimated camera fits were loose and sometimes cropped the body;
those were useful critiques, not precise shape certification.

## Pass 3 — expose highlight flow

Color/value first: the Eevee trial did not produce a strong enough striped
reflection to judge the surface. Replaced it with a procedural stripe dome in
Cycles, with the direct studio lights disabled. Actual 24-sample OptiX views
ran under `kit/with_gpu.sh`; no environment image was downloaded.

`renders/form-03/`: reduced the arch swell, added restrained waist/lower panel
sculpting, brought the front fascia to its intended reveal, and raised the rear
bumper toward the gate. Stripes exposed uneven interpolation around the arch
grid and overly square glass/sash corners. Inner floors and glass did not need
the same sampling as visible painted sheets.

## Pass 4 — round glazing and close construction gaps

Color/value first: the new reflection contrast made unintended hard facets
more visible; do not confuse high contrast with good surface quality.

`renders/form-04/`: built rounded stamped sash rings and actual glass openings,
removed the artificial horizontal gap within each door, added bed rear corner
returns and formed bumper upper returns. Reduced redundant inner/glass grids;
the result is 51,996 triangles. This pass exposed a regression: the thin glass
rim polluted the smooth face normals, making an X-shaped highlight; analytic
normal encoding on the body also needed correction. **Shading rejected.**

## Pass 5 — rear cab taper and normal precision

Color/value first: broad glass highlights were still triangulated; this is a
normal problem, not a reason to hide the glass in near-black material.

`renders/form-05/`: tapered the rear cab wall/roof back from the lower cab,
made the side window surface planar, and subtracted tangent coordinates in
Python double precision before converting to mathutils vectors. The tire/arch
relationship remains about 120 mm above the tire crown. The geometry was sound,
but the generated gauge rims still affected the glass face's shading.

## Pass 6 — fix the actual smoothing fans

Color/value first: the flat side-glass faces must reflect as flat faces; their
X highlight was not acceptable even at this coarse stage.

`renders/form-06/`: mark sharp edges on the actual closed result for ordinary
meshes. Establish the panel smoothing fans before setting custom split normals.
This removes the X from the glass and the artificial rectangular normal patches.
A separate kit fixture checks the attached analytic panel against the exact
normal of a paraboloid, manifold gauge/positive volume, and actual tire bounds.
That regression fixture passes. No triangle increase was used for the fix.

## Pass 7 — simplify the broad skin curvature

Color/value first: keep the reflection bands distinct, with dark cavities and
unclipped highlights. Body shade must not become a pale wash.

`renders/form-07/`: replaced the multi-station side crown with a smooth sine
section and a C1-connected upper cab taper. Softened the two styling features.
The bands now flow cleanly across the two lower doors; the broad bed crown no
longer shows the previous multi-station waviness. Wheel-arch highlights still
turn more abruptly than I would like near the end corners.

## Pass 8 — sweep the nose corners and prepare the review

Color/value first: the white reference is brighter than the neutral clay by
design; compare silhouettes and shading gradients, not its paint brightness.
The clay tires and wheel wells remain dark. Final orthographic foreground
luminance p5/median/p95 (0–255) is approximately side **22/102/126**, front
**14/89/145**, top **27/130/154**. No foreground channel reaches 250. This is
checkpoint exposure evidence only; real paint albedo/clearcoat is still pending.

`renders/form-08/` and `renders/checkpoint/`: the first nose was too square in
plan. Swept its corners back, carried the sweep into the hood/shoulder and front
bumper, and kept the published bumper envelope. Lowered the two general clay
cameras so stance is easier to read. The latest pair uses the less obstructed
April 2019 front/rear photographs; the older black truck and Ram remain useful
cross-design references. Added target dimension sheets and measured-source
reports rather than presenting input constants as measurements.

Final image inspection also caught background daylight through the arch gaps.
Added the missing inboard liner closures (544 triangles across all four wells),
so the cavities read dark through geometry. The final count is **52,540**; this
did not change the silhouette or need extra texture memory.

The final kit photo-match fits have **73.94 px RMS at 5130 px** and
**77.73 px RMS at 4886 px**, about 1.44% and 1.59% of image width. The
independent Blender projection agrees with the fitter within 0.003 px. Those
are different facts: the projection check proves the camera implementation;
the 74–78 px residuals disclose approximate landmark/shape matching. The
estimated camera heights are lower than ideal and are not claimed EXIF poses.

## Harsh assessment for the lead

- **Stance:** wheelbase, track, tire width and four ground contacts are measured.
  The 120 mm crown gap reads as stock 4x4 clearance. Front and rear have the same
  arch crown clearance; a rear-rake adjustment may help once the class form is
  accepted. The tire load shape is a light parked estimate, not the manufacturer's
  minimum loaded radius and not a spinning tire solution.
- **Proportions:** this is visibly a full-size crew/short-bed pickup in side/top
  views. The broad unpierced nose still reads heavy. Its future grille/lamp
  openings cannot be used to excuse incorrect body mass at this gate.
- **Panel curvature/highlights:** lower doors now share a continuous crown across
  the 4.5 mm seam. Some front shoulder/nose reflection pinching remains, especially
  the fan of bands near the swept front corner. The bed rear corner also turns
  bands sharply. I would not call these production-class highlight surfaces yet.
- **Greenhouse:** the roof/A/C-pillar transitions remain more angular than the
  photographs. Rounded window corners help, but the top rail/C-pillar joint needs
  the lead's attention. There are small exposed junctions at rear-glass edges;
  seals cannot simply conceal unresolved sheet alignment.
- **Wheel fill:** nominal tire diameter is right, with the rims/sidewall bulge
  explicit. Smooth tread and basic spokes deliberately look unfinished; brakes,
  suspension and tread normals have not been added.
- **Construction:** every sheet is a closed solid, but this is an outer form
  assembly, not a mechanically complete truck. Front bumper side closures and
  cabin junctions remain weak. Frame support, actual ground clearance, all hinge
  sweeps, steering axes and loaded-tire rolling behavior are unverified.

These are reasons for the requested **form review**, not hidden completed-asset
exceptions. Do not proceed to detail/bake until the lead has reviewed the form.

## Verification and files

- `make -C cars clean`, removal of the ignored checkpoint image directory, then
  `make -C cars WIDTH=1600` — **PASS**, rebuilding high/game sources, nine views,
  two photo pairs, projection checks, dimension sheets, contact and source checks.
  Root log: `build/cars-clean-rebuild.log`. The final hinge-sign correction and
  camera configuration rebuilt through the same command in
  `build/cars-final-rebuild.log`.
- `make -C cars check` — **PASS**: 52,540 game / 182,636 high triangles; closed
  manifold positive-volume meshes, finite coordinates/normals, no zero-area
  slivers, configured bounds/budget, camera projection, repository rules and
  actual form measurements. UV/bake/GLB checks are explicitly pending.
- `kit/test_vehicle.py` under headless Blender — **PASS**. `python3 -m unittest
  kit.test_delivery` — **PASS**, 4 tests. Root logs: `build/test-vehicle.log`,
  `build/test-delivery-cars.log`.
- An independent regeneration to `cars/build/repeat-game.blend` and another kit
  audit produced the same geometry/transform/triangulation SHA-256 as the game
  source. `build/repeat-check.json` — **PASS**. No texture-repeat claim is made.
- `python3 kit/repo_check.py`, staged repository check, and `git diff --check` —
  **PASS**. No images, meshes, exported assets, downloaded references or final
  docs are committed.

Key actual measurements: **5888.90 × 2031.83 × 1960.88 mm** envelope,
**3683.00 mm** wheelbase, **1716.00 mm** track, **1704.34 mm** bed floor,
**4.500 mm** sampled door gaps and **16.000 mm** lower cab/bed separation.
The hood/tailgate opening sign was corrected to negative local X; their
clearance is still pending. Part/category triangle counts are in README and
`build/form-check.json`; no final GLB or texture set exists. Six temporary clay
materials, zero image textures. The planned five tint presets share one 2048
three-map set, about 16 MiB compressed with mips; that allocation is not shipped.

Main images under `cars/renders/checkpoint/`: `front_three_quarter.jpg`,
`rear_three_quarter.jpg`, `side-dimensions.jpg`, `front-dimensions.jpg`,
`top-dimensions.jpg`, `match_front-pair.jpg`, `match_rear-pair.jpg`,
`stripes_front.jpg`, `stripes_side.jpg`, and **`contact.jpg`**. PNG originals,
calibration overlays, source hashes and tonal statistics are alongside them.

Kit changes are additive: analytic returned sheet panels with correctly encoded
split normals, loaded ISO tires, their geometry/normal fixture, and an opt-in
custom checkpoint recipe switch. Existing asset defaults remain unchanged.
No tools or installs are needed. The lead is needed to review the form, with
particular attention to the greenhouse and front-corner highlight pinching.
