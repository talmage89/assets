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

The look1–look5 draft images are retained outside the clean build at
`../build/signals-preclean/renders/`. The accepted form images used in native
before/after panels are at `../build/signals-before/checkpoint/`. Final
checkpoint and comparison paths below are regenerated by make.

## Look pass 1 — rejected, 5 November 2026

Color and value first: opened the imported-part head, connection, base and open
cabinet at 1000 native pixels in renders/look1/201. Compared the yellow/black
head to span-2009, galvanized construction to the FDOT details, and the lit
indication to span-2009 and gadsden-2025. The red overexposes toward white;
zinc shows stretched vertical manufacture variation. Neither is acceptable.
Reduce emission, increase actual LED fill, remove excess low-frequency zinc
contrast, and check a color-preserving display transform against the photos.

The cabinet rack is present but some flat panels lose their generated graphics.
Inspection of the actual exported UVs found PrintUV and UVMap layers joining
with zero-filled charts. Normalize chart names before consolidation. Visors
also retained a source black material after atlas assignment; assign their
inner and outer faces before mapping. This is an export/material bug, not wear.
The gray rack, repeated under-lip spots and sparse close-view backdrop remain
CG. No acceptance is claimed by this pass. Correct these before evaluating
road layout, the town setting or the full-frame age.

## Look pass 2 — rejected, 5 November 2026

Color and value first: the imported look2 inspections exposed pale yellow,
strong dark grooves and artificial zinc striping. Reduced normal strength,
restrained zinc contrast and color-preserving display mapping are necessary.
The original label charts were lost at consolidation; all charts now use one
UV layer name before joining. The vehicle indication also used the wrong
alpha domain: the LED sheet must carry both visible coverage and emission.
These findings explain the bad image; they do not excuse shipping it.

Door panels need differentiated instrument faces. Brackets, lenses and
apertures must be judged after external export, because the source materials
hid chart and transparency failures. Repeat the close views before relying
on a full intersection render.

## Look pass 3 — rejected, 5 November 2026

Color and value first: opened all twelve renders/look3 views at native size:
201 hero/head/base/open cabinet, the four plan/driver pairs, and the span hanger.
The optics no longer tear into horizontal rows, and the black grooves were
excessive normal response rather than painted dirt. At reduced normal strength
the wear is now too quiet. Enlarge only the under-visor runoff tracks, increase
sun-side chalking while retaining paint hue, and break base oxidation into wet
crevices and unequal cut-edge patches. The span top deposits read from their
perch; retain them. Red still rolls pink at its LED centers: lower the emission
while retaining the denser array, then measure against two sunlit photographs.

The hero now avoids the near mast but a pedestrian head occludes a primary
face. Move the eye to the forward sidewalk arc, keeping a real 1.6 m viewpoint.
All four towns have streets and delivered cars. The T has dark voids on its
missing branch and the boulevard median is invisible: open slab normals were
wrong. Correct the actual upward surfaces and add a low parcel underlay; keep
the corner planting verge distinct from the walk so footings do not block it.

The town head's measured swing failure was real: a short arm's sign overlaps
its first housing. Lower the sign below the head envelope, supported by real
hanger rods, then repeat the full motion sweep. This is a construction change,
not a larger test tolerance. The new straight-arm photograph replaces the
curved New Jersey comparator. The new measured full-frame fits have 2.15 px
mast, 1.83 px span and .46 px close-head RMS; camera agreement is still separate
from regional product differences and appearance.

## Look pass 4 — construction corrected, 5 November 2026

Color and value first: opened look5/201/hero at its native 1200 pixels against
the field photographs. The raking sun now produces deep visor recesses and
retains the yellow paint and dull zinc. The red remains saturated. Moving the
near tree along the street exposes all primary faces against sky; the gas
station and continued street replace the empty green horizon. Pole patina is
still quiet at this full-frame distance, while visor fading reads better.
The backdrop trees and perfectly repeated houses remain visibly procedural.

The stricter actual-head sweep found two defects concealed by the earlier
serialization checks: the near-side backplate tilted into its support, and a
reverse-arm visor entered the mast steel. Increase near-side stand-off and
put the reversed head on the far side of its arm with its bracket/cable entry.
Do not raise tolerances to pass these contacts. Refit the affected photo
camera using the new actual head coordinates. The compact town still has two
physical supports and four distinct serving arms.

Round retaining rims now spend triangles previously wasted on hidden lens
covers; named transparent-state meshes retain their state API. The exported
optic sheet supplies an opaque circular black lens face with emissive dots;
masked coverage avoids sorted transparency. The cabinet has differentiated
fronts and a readable door record. Rebuild from absence and review every final
image before reporting appearance or measurements.

## Look pass 5 — rejected, 5 November 2026

Color and value first: inspected the twenty-one native exported checkpoint
views and all six photo pairs, plus the five completed source comparisons.
The source comparison was stopped after the same color miss was established.
The balanced North Carolina photo's yellow samples are about .996/.675/.094
in display RGB; the old exported yellow is .686/.561/.106. The photo clips
much of its red channel, so these are appearance limits rather than albedo.
Warm the paint, raise only the matched direct sun, and retain the hero's deep
visor interiors. The old equal solid dots read as a graphic. Replace them
with fewer original radial packages/hot cores, then remeasure full-sun states.
The dark lenses also need their unpowered packages visible at close distance.

The complete cabinet reads as serviceable equipment; graphics and door paper
survive delivery. No missing UV layers or broken normal projection remains.
Runoff on the cases is too quiet because its masks taper to zero at the very
bottom, where the lens leaves visible paint. Let narrow unequal trails reach
that real lower edge; enlarge only the perch deposits. Keep rust at wet metal
edges and anchors. Tall-pole density remains a compromise.

The overhead exposes neighboring corner houses overlapping across street
rows. Reserve measured prefab bounds rather than filling each row blindly.
The large-return channelizing piece also needs one actual lane of clear road
around it. Use a 35 ft arterial return, a smaller rounded splitter and measure
the retained island vertices against the circular gutter edge. Other 15–25 ft
returns need no channelization. Move the hero eye onto the resulting walk.
Dusk lights must use the imported LightEmitter sockets, not a guessed height
above the post; record those socket/light positions. The blue sky must remain
brighter than the ground.

## Look pass 6 — calibration improved, 5 November 2026

Color and value first: opened look6's native hero/head and full camera-frame
head_201, then the revised setting's hero/above/dusk and both optical fixtures.
The painted flat patch below red moved from .675/.545/.118 to
.871/.584/.176, toward the photo's .933/.557/.055. Yellow is now warm gold,
while the circular indication has hot cores and dimmer package edges. The
photo clips red and its cover reflects white clouds; our clear-cover response
still differs. Do not claim a perfect photographic match or candela calibration.

The native 30/100 m fixtures read lit and dark without bloom: red R95 / sky R
is 1.958 / 1.616, against 1.783 and 1.308 in the two balanced sunlit photos.
Mean indication Y / sky Y is .478 / .442 (photos .312 / .561). Distances come
from actual imported lens centers. These are display contrasts, not physical
luminous intensity. Keep the measured indication strength.

The revised setting removes roof intersections and reserves the commercial
lot; its backdrop remains repetitive. All primary hero heads read against sky.
The eye is measured at 1.6000 m above the actual corner walk. Fixture sockets
now place 48 presentation lights below their actual glass. Complete the final
clean rebuild, source/game pairs and native before/after panels before reporting.
No docs images are approved or committed by this pass.

## Look pass 7 — whole installation and resource audit, 5 November 2026

Color and value first: opened both native 1600-pixel Oregon-array preview
renders and the photograph, plus the memory-limited hero/dusk previews. The
render keeps the yellow coating and gray zinc distinct under direct sun;
the reference uses black cases, so it calibrates zinc and construction, while
the North Carolina pair remains the yellow age comparator. The dark visor
interiors stay deep. Clear-cover reflections and regional hardware still differ.
The Oregon neutral was checked visually: the first proposed rectangle hit a
house window. Replaced it with the unlettered gray reverse of a roadside sign,
recorded and annotated before measuring. It remains a provisional field neutral.

The earlier Gadsden camera fit only one face, while the complete reference
installation had a different head count. Reject it for mast-array proof. The
period Oregon replacement has the same single straight arm, two through faces
and four-section FYA. Fit all ten centers and six diameter vertices measured
from the actual meshes. Constrained sidewalk/driver fits give 5.952 / 6.631 px
RMS at 1600 pixels; this proves the whole array's projection, not the street
geography. Cinderbrook keeps a separate black-head comparison. The final set
now has seven pairs across all four seeds.

After the external memory stop, use one Blender process at a time, fresh per
seed, two CPU threads and the shared GPU lock. Cap only presentation images;
signal maps retain full delivery resolution and source comparisons retain
4096 fields. Render native photo crops directly instead of allocating an
entire multi-megapixel frame for each small detail. The source Cinderbrook
comparison fell from 6481.9 to 3911.5 MiB kernel peak RSS. The two full Oregon
preview frames peaked at 4111.0 MiB. Repeated neighborhood planting remains
conspicuous, but no library export is modified by this presentation cap.

An additional shadow audit sampled the same exposed yellow strip and the strip
below the visor. The source photo's left side is shaded while the draft's left
side was lit: the close-pair sun had its lateral direction reversed. Correct
the incident rays to come from the camera's right, keeping the sky direction
coupled. Record zinc value and both painted strips in lens-measurements.json;
the under-visor contrast includes cast shadow and cannot be called dirt alone.
This changes comparison illumination, not the delivered BaseColor.

## Look pass 8 — exported checkpoint audit, 5 November 2026

Color and value first: opened all 21 current exported Cycles views at native
resolution, the seven game photo renders and their pairs, all seven source
renders, four review sheets and eleven native before/after panels. Inspection
paths are recorded in build/image-review.json. Yellow remains gold instead of
olive, dull zinc remains gray and black backplates retain deep recesses. The
sampled zinc display Y is .665 against the balanced Oregon photo's .667. Its
microstructure is still smoother than the photograph. The exposed yellow
sample is .882/.584/.169 against .933/.557/.055; photo clipping and the
optical product prevent interpreting these as inverse albedo estimates.

The small left strip below the visor remains a mismatch: Y relative to the
exposed paint is 1.083 in the render and .490 in the photograph. The differently
shaped doors and visors cast different shadows there; this does not demonstrate
matched dirt coverage. Broader lower-edge runoff is present, but the clear-cover
reflections, optical package response and fine retained grime remain weaker
than the photograph. Shared trims repeat some marks. Pole patina is quieter
than case fading at the hero's full-frame distance. Those limits are retained
in the report rather than called photographic agreement.

The native audit caught two presentation defects after the mast array refit:
the head's higher mount clipped its backplate in the old close camera, and the
raised street sign concealed the arm flange. Target the actual exported head
pivot, and view the flange from behind the sign. The corrected images show the
complete head and the bolted connection. Lower Maryland's comparison sun to
about 17 degrees, with its rays toward the camera's left, to follow the long
field shadows. Re-render source and exported pairs under identical settings.
The original reference street geography and seasonal foliage still differ.

The four top/driver pairs now expose different civil plans, lane-derived arms,
two diagonal poles at the compact crossing, the boulevard's median noses and
turn bays, and the T's closed side. Houses no longer intersect adjacent rows.
The gas station, three car bodies and continued town streets are presentation
only. The span has a messenger clamp, extension/adjuster, lashed lead and one
short gravity entry loop; no decorative rings remain. The rack, load-switch
bank, conflict monitor, detector inputs, power/breakers, harness and door pocket
are present. Cabinet fronts are intentionally simple texture-carried forms.

Hero display Y p1/p50/p99 is .0146/.5710/.9342; white fraction is .00656%,
including the sky and presentation lights. This is a full-frame range check,
not a material albedo test. Blue-hour sky is brighter than the ground; the
street emitters use actual imported light sockets and house windows are lit.
The true 30/100 m fixtures retain red R95/sky-R ratios 1.958/1.616 versus
1.783/1.308 in the two balanced sunlit photos. Dark ratios are .067/.290.
These are display-domain contrasts, not candela measurements.

Build proof: all generated signal output directories and ArterialSites.glb
were absent before the clean build. Its bake/model/arterial/check stages
passed. The framing audit interrupted only the render stage; after the camera
corrections make completed, followed by the corrected pair stage. Final make,
make check, make repeat and the repository check all exit 0. Exact model replay
matches 15 GLBs totaling 65,237,392 bytes. Independent shipped-map comparison
is exact for BaseColor, Normal, emissive and names; four ORM channel values
differ by 1/255, within the kit's channel tolerance. No exact GPU rebake claim.

Raw external glTF checks pass for all 15 deliveries: one shared five-map image
folder, valid guarded trim domains, finite unit normals, nonzero UV area and
measured density. Independent source-surface clearance/motion and lane/view
checks pass. All 295 protected delivery hashes are unchanged. The delivered
family totals 14,607,229 bytes including one map copy, at an estimated 17.5 MiB
block-compressed with full mips. No kit changes or docs images are committed.
Final kernel peaks are about 4.95 GiB for the bake and 4.83 GiB for the largest
checkpoint process; each seed runs in a fresh serial Blender process.

Evidence: ../build/signals-final-make.log (clean stages),
../build/signals-final-make-resumed.log (completed checkpoint),
../build/signals-final-pair-light.log (corrected comparisons),
../build/signals-verify-{make,check,repeat,repo}.log; build/{checks,construction,
layout-check,delivery-check,budget-report,preservation,repeat-check,
texture-repeat,lens-measurements,hero-range}.json. The repetitive town context,
coarse tall-pole detail, shared wear and simplified optics remain the clearest
CG tells. This is the requested review checkpoint, without docs images.
