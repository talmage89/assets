# Form and construction review

This is the requested gate before look-dev. All images are from imported
checkpoint GLBs with simple materials. There are no baked final textures and
no claim of finished weathering, final UVs, or final game readiness.
Photographs never enter any Blender shader.

## Pass 1 — 5 November 2026, rejected

Opened every first-pass image in renders/pass1/201 and renders/pass1/204,
including both approach/above views, the hero and all six details. Compared
against the 2009 North Carolina LED/hanger photo, 2006 Maryland approach and
2014 New Jersey intersection. The Canadian 2008 photo is supplementary
construction context only; it does not establish US layout rules.

Color/value first: the quick yellow is plausible ochre but too uniform; steel
reads as generic gray. Both lack the service-age cues in the photos. These are
deliberate quick materials at this gate, and must not be mistaken for accepted
look-dev. Sky fill was too weak: shadowed hardware disappeared. Increase diffuse
sky without lifting black paint or clipping emission. For subsequent photo
pairs, balance each photo on a documented bare-asphalt patch; asphalt is a
provisional neutral, not a calibrated gray card.

Form failures and actions:

- The center of every LED array had an artificial black hole. The curved opaque
  cover crossed its own LED card. Move its surface behind the dots.
- The vehicle heads looked folded rather than cast under raking light.
  Preserve compound shoulder sections, smooth manufacturing radii and remove
  rear/covered faces. The four/five-section variants exceeded 1,500 triangles;
  simplify hidden rims, latch heads and visor attachment edges.
- Approach paint was mirrored across the roadway: fix the canonical inbound
  side, stop bars, turn arrows and loop locations. Keep US right-hand traffic.
- The nearest car blocked too much of the approach. Move it to the stop line.
- Pedestrian hood depth/oblique camera hid the hand. Review front-on as well
  as oblique, keeping the real hood rather than shortening it for a picture.
- The cabinet leaf opened into the cabinet in the first definition. Reverse
  its range. A surface check then found the hinge barrel entering the jamb:
  put the hinge axis forward of the return and model fixed hinge knuckles.
- Span heads were crowded, with insufficient longitudinal setback for one
  primary face. Re-space the pairs by the approaches they face. Add catenary
  drop ties; retain measured 15 mm service cable and restrained slack coils.
- The native curb, gutter, walk and ramp proportions read well, but inspect
  the verge/approach seams with ray tests. The new road is 33 ft, not a scaled
  residential 24 ft road. Black void-like patches need diagnosis before approval.

The FDOT S1 foundation is deliberately heavier than the decorative New Jersey
example. It is a regional construction choice, not an attempt to duplicate that
product. The Waycroft housing uses its own three-station shoulder, latch layout
and blank maker plate; the Cress button uses its own speaker/arrow surround.
No manufacturer badge or molded proprietary marking is reproduced.

## Pass 2 — 5 November 2026, rejected and corrected

Opened all 17 images in renders/pass2, comparing the same surfaces and
construction to the period photos. Color/value first: more diffuse daylight
reveals the forms without lifting black paint. Off modules are much darker,
and the bright red now fills its lens. Dusk was still effectively black;
replace the below-horizon daylight approximation with explicit cool procedural
ambient illumination and retain restrained visible emission.

The LED occlusion and head budgets were corrected. The smoothed compound
shoulders now read as cast sections; the visor edges still expose the game
mesh in close views, a known low-detail compromise for this checkpoint.

The black verge strips were real missing surfaces, not shadow or asphalt color.
Native glTF roots used quaternion rotation mode, so assigned Euler yaw was
ignored. Correct the placement mode; add actual surface ray checks across all
four approaches. No ground delivery is modified by this fix.

Reviewed route geometry more strictly. Move the big mast footings onto the
curved planting strips, clear of the full 5 ft ramp. Push-button tactile arrows
must point along their crossing; rotate the APS independently of the pedestrian
head. Place a 30 × 48 in clear standing rectangle beside each ramp, connected
to the public walk. Set the button axis from the actual top of that landing.
Add real R10 mounting spacers rather than floating instruction plates.

Source-surface inspection found detail construction errors: missing anchor
bores, a 5 mm gap below the camera rain hood, and poorly placed hinge leaves.
Cut the plate bores, make the nut covers hollow and mechanically retained,
lower the hood to its support and separate the stationary and operating hinge
leaves along their common pin axis. Sweep the cabinet and head pivots rather
than relying on their exported transforms.

The closer span heads now have adequate separation and primary-face setback.
Their catenary drops, slack loops and lower restraints read as assembled
hardware. The painted/galvanized mast styles and four/five/three-section
treatments are distinct. Originality remains intact: only standardized signal
conventions and engineering construction are shared with the references.

Final checkpoint evidence will be in renders/checkpoint and renders/matches.
The remaining material age, baked wear and optical cover response belong to the
requested later look-dev stage. No final docs images are committed here.


## Pass 3 — 5 November 2026, export and assembly corrections

Opened the full 19-image third suite and both initial photo pairs. Color/value
first: the source looked dark when switched off, but the imported GLB still
showed bright colored dots. The shader's multiply node had been lost in export.
Replace it with an actual dark generated BaseColor image, shared by lit/off
materials, and a separate bright emission image. Verify the embedded texels as
well as the source material: off dots must not masquerade as powered indications.
The corrected dusk ambient reveals the supports while keeping black cavities.

The first calibrated comparisons were unusable: imported houses hid the matched
hardware. Keep the full fitted photographs and camera evidence, omit neighborhood
context for these comparison renders, and crop both sides identically around the
selected construction. Camera agreement verifies projection, not a shape match.
The New Jersey decorative curved arm remains different from our chosen FDOT
straight/cambered steel design. Do not claim this pair proves product identity.

Surface-based pivot sampling found a cable crossing the housing and neighboring
backplate contact. Route the service arch above the head, lower the cast head
85 mm below its coupler and limit X movement to ±4°; keep Z aiming at ±15°.
The indexed stem and flexible tether termination are intentional connections,
excluded explicitly. Cabinet sampling found rain-lip/jamb contact; narrow the
leaf, lower its top and place the hinge axis ahead of the folded return.
Its −110…0° sweep now checks 23 source-surface poses, with the compressed gasket
excluded and a documented 1.5 mm closed-fit tolerance.

Ground pads had sod cards piercing them. Trim only the placed verge copies and
lower that sod 3 mm. Preserve the native Ground files. Lower the pad to a
6.35 mm maximum transition at the walk and derive the 42 in button datum from
its actual top. Seed 202 now demonstrates four mast-mounted pedestrian heads,
four full pedestals and four separate short button posts rather than repeating
one mounting arrangement everywhere.

## Pass 4 — 5 November 2026, final form checkpoint

Opened all 19 final PNGs in renders/checkpoint: four above/driver pairs, the
201 hero, lit and dark head, connection, base, pedestrian head, button, closed
and open cabinet, dusk and the 204 span hanger. Compared construction against
the period approach photos and the close LED/hanger photo. The period photos
were balanced on the documented asphalt patches in refs/SOURCES.md; neither
is a calibrated color target. Color/value first: yellow remains flat ochre,
zinc remains generic gray and paint lacks age. The dark/lit export separation
is now clear and cavity shadow survives. These quick materials are acceptable
for reading form only. They are not an accepted 10–20 year maintained finish.

A final reading of the FDOT drawing exposed a datum error: 25 ft is measured
from plate bottom, not from the start of steel above it. Correct that datum,
the 3 ft top-to-arm offset and the 16/14 in across-flat dimensions of the
12-sided steel sections. The plate-to-pier gap is now one 1¾ in anchor diameter.
Replace the buried flat handhole plate with a bent 11-gauge cover following
the actual two pole facets. Replace the solid connection wedges with a hollow
four-wall transition box, and check its actual contact with shaft and flange.
This increases a mast by only 36 triangles. The base close-up now exposes
leveling hardware, a plausible cover and real plate bores rather than relying
on a dimension label.

Mounting/placement: actual minimum clearance bounds are 5.879 / 6.132 / 6.132 /
5.369 m for 201–204, above the adopted 5.334 m limit. Primary faces are separated
by 8 ft and their measured longitudinal positions lie within the MUTCD range.
The 25/30/36 ft reaches change the support silhouette while keeping the same
lane-facing head positions. Standing rectangles remain clear of the full-width
ramps; the APS arrow points along each crossing. The 28 ground rays find no
missing approach surfaces. These are visual/construction checks, not a civil
accessibility certification or structural calculation.

The fictional Waycroft cases, Cress buttons and Morrow cabinet retain original
shoulders, latch positions, speaker surround and blank maker plates. Standard
indications and ordinary steel fabrication do not reproduce a manufacturer's
branding. The Rill fixture is the library's own unchanged exported head.

Remaining form weaknesses at this gate: visor/loop silhouettes expose their
low polygon count in close-ups; the cable service arches and span coils are
more regular than field installation; small clamps and optical covers are
simplified. The cabinet interior is an empty dark rack blank. Repeated trucks,
few house prototypes and the sparse horizon weaken the presentation. Regional
photo differences leave the New Jersey fit a weaker comparison than Maryland.
No photograph-like surface polish, final atlas, weathering or final delivery
checks are claimed. Stop here as requested; do not begin look-dev.


Final pair review: the 2014 New Jersey crop has a 37.10 px landmark RMS in the
3264 px source frame (estimated 75.08 mm camera). Its pole proportions are
useful but overlapping background heads and the curved reference arm limit it.
The 2006 Maryland crop has a 2.71 px RMS in 2592 px (estimated 41.85 mm).
The difference in hanging arrangement and the reference's much less regular
service cable remain visible. Independent Blender projection disagreement is
0.00735 / 0.00269 px; this validates the camera conversion only. Opened both
full match renders, both calibration overlays, both pairs and all four review
sheets. Hero full-frame display Y p1/p50/p99 is .0031/.5878/.9283, with zero
white-clipped pixels; sky/context are included, so this is not an albedo test.

Validation completed: make WIDTH=1200 SAMPLES=24 and make check exit 0. Actual
source-surface construction checks pass for all four seeds, independently of
raw GLB and fresh-import comparisons (maximum vertex roundtrip error 2.16 µm).
Exact recipe replay produced 15 byte-identical GLBs totaling 12,170,008 bytes.
All 295 baseline delivery hashes are unchanged. Repository check has zero
errors. Evidence lives in build/{checks,construction,repeat,preservation,
hero-range}.json and build/{make-report,check-final}.log. No kit files changed.
