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

## Final pass 1 — accepted checkpoint re-examined, 5 November 2026

Color and value first: opened the native checkpoint hero, dusk, open cabinet,
four-town sheet, seven-pair sheet and full neutral-balanced head photograph.
The yellow's small old exposed-paint patch is .882/.584/.169 against
.933/.557/.055 in the photo. Those strips have different visor shadows; the
photo clips red, and the earlier comparison does not prove a matched hue.
Broader yellow segmentation gives different results and must not be substituted
for same-surface samples. Increase yellow's green relative to red modestly and
reduce blue, then judge the same matched-light strips again. The cabinet lacks
metallic highlights and the blue-hour view has almost no lighting hierarchy.

CG tells: empty foreground/sky dominate the hero; repeated identical tree
silhouettes make an avenue pattern; every approach looks clean despite its
signal. Unpowered covers show no recognizable curved sky highlight and their
arrays vanish. The interior door gasket was actually a solid black panel,
concealing the aluminum inner skin. Correct it to four perimeter strips, retain
hardware and rack, and add the small police door and folded inner stiffeners.
Rebuild shared trims without changing their resolutions or family memory.

The revised arterial surface keeps Ground's canonical maps intact and places
absorbed oil on the road itself. FHWA 2006 Traffic Detector Handbook Volume II,
chapter 5/appendix J inform 6 ft square chamfered loops, sealed lead-ins and
roadside pull boxes. Wheel-path aggregate has its own scalar roughness, while
paint breaks in value where tires cross. The module's local station grid adds
geometry only where those broad changes need support; report this separately
from the unchanged head budgets. All final pavement views must load the actual
exported ArterialSites module, not the procedural construction scene.

The exported pavement audit found the original MixRGB paint/seal factors were
not serialized by Blender: paint and seal collapsed to the same shader.
Corrected to direct stock COLOR_0 colors, re-exported and independently probed
134 actual imported surface points. All fifteen signal deliveries also pass
raw normals/UV/image checks and source-to-reimport measurements. This proves
those data paths, not appearance. The wearing-course additions bring the four
full road assemblies to 6243/4050/6448/2770 triangles; each consists of multiple
approach pieces plus corners, walks and medians. No image is added.

A better yellow comparison uses the right-hand flat paint beside each lens,
away from the unequal visor shadows. For the red section, balanced photo
RGB is 1.000/.729/.114, hue 41.7 degrees; accepted render .920/.616/.216,
hue 34.1 degrees. The photo clips red, but the 7.6 degree shift toward orange
is clear. Two further right-side strips corroborate it. Preserve all three
rectangles and their clipping fractions in the final measurement receipt.
The revised Maryland neutral was checked as a native crop: an initial
rectangle hit asphalt; the corrected 1640,1730–1660,1770 rectangle is bare
near-curb concrete, clear of leaves and joints. Record the actual gains.

## Final pass 2 — native exported previews rejected selectively, 5 November 2026

Color and value first: opened all three 1200 px Eevee camera drafts, the revised
Cinderbrook draft and all six 1200 px Cycles material/paving/dusk previews.
Yellow now reads yellow rather than orange; compare its documented flat strips
under the retained photo lighting before accepting the numerical match. The
cabinet is clearly metal and its light reveals the controller and rack. Its
inner panel needs real contact with the leaf and pocket: remove tiny floating
standoffs rather than reporting their intended placement as a contact.

CG tells: cover reflection curvature is exaggerated, producing a large golden
reflection of the visor below the sky patch. Reduce the analytic curvature and
clear-coat contribution while keeping the arrays faintly visible and the lit
strength unchanged. The dusk preview has warm pools and visor bounce, but its
sky is still flat. Pixel samples confirm the world normal's inverted Z sign
clamped the gradient to its horizon value. Use absolute altitude and compare
native sky samples again. The pavement close-up misses the detector cuts and
includes a foreground car: retarget all three approach loops and omit only
presentation vehicles from that inspection view.

The tighter Aldervale hero improves occupancy but cannot place its remote
cabinet in the foreground. Cinderbrook's wider corner view includes the cabinet,
pedestrian post, queued cars and full arms. Its first draft clips hardware;
reject it. The farther-back view fits the equipment, but a foreground
presentation street-lamp stem blocks the composition. Leave a documented gap
in that context placement; never hide or move shipped traffic equipment.

The small police door is a separate hinged leaf over a real access aperture
through both skins, with perimeter gasket, lock and pins. Cabinet cost is now
2964 triangles, below 3000. Actual per-approach road counts are 1903 max for
Aldervale, 794 for Cinderbrook, 1993 for Wrenfield and 772 for Morrow Glen,
within the 2000 modular-piece limit; full road totals include all approaches.

## Final pass 3 — clean exported outdoor audit, 5 November 2026

Color and value first: inspected every native outdoor image as it arrived.
The case coating is now a stronger yellow, gray zinc stays separate from it,
and recesses remain deep. The cabinet's natural metal, gasket, louvers,
police-door seam/lock/pins, inner stiffeners and rack are visible; its service
light lifts the former dark void. The molded cover now has a restrained sky
reflection and visible unpowered packages. Its package layout is still more
regular than the photograph, and repeated cabinet trim grain is conspicuous.

The pavement detail shows three full 1.8288 m detector rectangles, relieved
corners, sealed lead-ins and wheel-path wear. Stop/crosswalk paint darkens where
tires cross; fine binder chipping is simpler than the photograph. The old
pavement camera missed the cuts and is retained only as rejected evidence.
Four road plans remain unchanged; tree species, size, rotation and gaps vary.

The 35 mm Cinderbrook hero now fits complete arms against the upper sky, with
cabinet and pedestrian post near the camera and cars at the bars. It has less
empty road/sky than the accepted Aldervale camera. Raking light defines the
steel and nearby surfaces. The dusk gradient now varies with altitude and
warm street-light pools break the former uniform blue. Its green indications
read clearly, but the presentation cars' original 80-strength lights compete
with them. Reduce those imported car materials' preview strengths to 1.6 at
dusk and .8 by day, preserving the car files and the accepted signal strength.

Another CG tell in the close views is a blue band beyond the 350 m ground
edge. Extend only the presentation underlay to 10 km in each direction; the
100 m delivered arterial modules stay intact. The near Cinderbrook street-light
gap must be real context placement rather than hidden lamp geometry with a
live light. Omit the two closest presentation lamp instances for that seed.
Re-render affected outdoor evidence and pairs and verify all recipe/bundle
receipts before docs. Gallery parts are unaffected by these scene corrections.

## Final pass 4 — gallery lighting and material-value audit

Color and value first: the first gallery views were rejected. The studio light
matrices had been read before a dependency-graph update, producing bright bars
through the parts. Update the transforms before recording them, then keep the
studio exposure low enough to retain coated-case color and aluminum highlights.
The correctly lit cabinet exposed broad repeated grain, especially on the small
police leaf. Replace it with fine mill variation and two unequal narrow runoff
tracks beneath exposed edges; sheltered inner skins sample clean aluminum.
Keep the grounded cabinet at ground zero so its buried conduits do not lift
the concrete base into the air.

The inherited equipment-fit pavement camera actually sampled concrete, so its
asphalt numbers were rejected. A separate nominal 42 mm curbside comparison
now has three actual imported road hits and three clear sun paths. No fitted
equipment residual is attributed to this new camera. Under the inherited
Maryland light, the first wearing-course tint gave Y′ .296/.271/.274 against
photo .401/.435/.406. It was too dark. Lift dry aggregate from .60 to .95
vertex tint while retaining localized oil and wheel-path masks; verify again
before publishing the final values. Ground's canonical maps remain byte-identical.

CG tells still to judge in the rebuilt finals: regular LED packages, shared
trim weathering, simplified asphalt mineral breakup and paint abrasion, and
the intentionally coarse distant town. These are appearance limitations, not
claims resolved by the geometry checks.

The .95 tint confirmation gives Y′ .355/.331/.333; native contrast
p85–p15/p85 is .088/.123/.117 versus photo .088/.130/.120. The
nominal comparison also needs a documented half-stop exposure correction:
clear near white paint was .669 versus .889 in the balanced photo. That
correction applies only to this estimated ground-view camera, with its
rectangles and limitations recorded in pavement-camera.json. Re-measure the
actual final image; the presentation cameras keep their own exposures.

## Final pass 5 — delivered images, 6 November 2026

Color and value first: inspected all 25 native checkpoint/optics images, the
seven fitted equipment pairs plus the nominal pavement pair on both source
and export, and the native part turnarounds as they completed. The balanced
pavement photo medians are .401/.435/.406; final imported road .440/.417/.418.
All three render samples hit asphalt or polished aggregate and have clear sun
paths. Near white paint, rather than an asphalt ROI, informed the separate
nominal camera's half-stop field-exposure correction. Original geography and
uncalibrated JPEG response prevent a physical albedo inference.

The three yellow photo hues are 41.7/39.8/40.9 degrees, against final
39.4/40.6/40.9; accepted checkpoint 34.1/34.8/34.9. Corresponding final Y′
.698/.716/.723 compares with photo .743/.704/.733. The stainless-latch neutral
is provisional and the first photo strip clips red in about 96% of its pixels.
These flat strips are a better comparison than the unequal under-visor shadows.

Cinderbrook's 35 mm sidewalk hero places full arms high in frame, cars at bars,
near service equipment and the town behind. Its Y′ p1/p50/p99 is
.004/.400/.937, with .000391% near-white pixels. The gradient dusk sky, actual
street-light pools and small indication flux lights give the lit lenses their
place in the frame. Off covers show sky and packages. Lit R95/sky-R is
1.969 at 30 m and 1.610 at 100 m, versus accepted 1.958/1.616: the accepted
emission remains 6.0. This is image contrast, not candela.

The clean mill finish, narrow runoff and protected inner skin pass the native
cabinet close-up and all four studio views. Gasket, folded stiffeners, access
aperture, police leaf, lock/pins and warm service light read clearly. Its plinth
now rests at floor height with buried conduits. The first standalone button
gallery was rejected because its instruction sign floated without a post; use
the delivered PushButtonPost assembly for that turnaround. The native phase
frames correctly show through green with FYA on/off, steady yellow on S01, then
red/red-arrow. Their shared display stand supports both hangers. The scale
silhouette's actual vertex height is 1.79999995 m. The Eevee view is inspected.

Remaining CG tells: LED packages and cloud reflections are more regular than
the photographed optics; shared trim weathering repeats; paint abrasion and
long wheel paths are too orderly close up; tall pole texture is coarse. Tree
species, scale, rotation, gaps and placement now vary, but the distant flat town
remains simplified. These limitations are retained honestly within the accepted
geometry/texture budgets. No kit changes or neighboring delivery edits.

Native before/after evidence: renders/final-fixes/{hero,asphalt,yellow,
dark_lenses,dusk,cabinet_exterior,cabinet_interior,trees}.jpg. Each side is
1600 native pixels wide; hero/dusk explicitly compare revised authored cameras
and installations. The other detail comparisons retain their cameras.

## Final pass 6 — compact delivery review, 6 November 2026

Color and value first: rejected the first GIF palette because the small green
indication became gray against a palette dominated by case yellow and the
background. Reserve actual sampled green/red/yellow indication colors before
quantizing. The final 256-color GIF is inspected after encoding: green, FYA
on/off, steady yellow and red retain their colors; all six frame durations
are verified. It is 800 × 600 and 306,462 bytes. Quantization banding remains
visible, an honest GIF limitation; native PNG frames retain full color.

The mounted button's four native views now pass: the instruction sign and
button are supported on the actual exported post. Inspected the final contact
sheet and all five compact docs JPGs. Tall overview JPGs are capped at 1600 px
height as well as width; the native evidence remains intact. Each JPG is under
200,000 bytes (largest 199,369). The towns sheet names each town and seed.

Build proof: signals build/, textures/ and export/ plus the authored arterial
GLB were absent at the clean build start. Bake, model, arterial, export, all
checks and the 50-view final stage completed with exit 0. The final mounted
button presentation and bounded docs completed afterward. make, make check,
make repeat and the repository check exit 0. Replay reproduces 15 GLBs exactly,
64,916,952 bytes; this is model/state/image replay, not an exact GPU rebake
claim. All 295 protected delivery hashes remain unchanged. No main merge,
kit changes or top-level README edit.

Final receipts: ../build/signals-delivery-{clean,make,mounted-button,docs}.log;
../build/signals-delivery-final-{make,check,repeat,repo}.log; build/{checks,
construction,layout-check,arterial-check,delivery-check,budget-report,
preservation,repeat-check,final-values,hero-range}.json and build/gif-audit/.
The shared PNGs total 3,633,325 bytes; fifteen external glTF/bin deliveries
with one map copy total 14,628,534 bytes. Map sizes and compressed family
memory remain 2048/1024/512 × 256 and 17.5 MiB. Per-part/per-intersection
triangles, material counts, bytes and first-use memory are in README and the
generated budget report. Nothing is needed from the lead to complete this
delivery. The appearance limitations in pass 5 remain.

## LOD rollout, 2026-11-09

Frozen tool/recipe revision `55b6288`; literal receipt:
`build/lod-rollout/signals/freeze.sha256`. The original `make check` passes
with `-o build/delivery.json -o ../ground/export/ArterialSites.glb`; exact
command/exit/resource receipt is `build/lod-rollout/signals/original-before.json`.

### LOD critique 1: controller cabinet

Opened all three native original/preceding/new/difference strips, both
construction views and contact. Color/value first: metal body, dark vents,
door reveals and concrete retain the original response at 25% / 6.97m.
The service fixture's shaft retains coverage. Close inspection reveals a
simpler louver form and coarser circular lamp, without a native switch fault.
Both `Controller__Door__Fixed` and `Controller__PoliceDoor__Fixed` stay
separate under their original pivots. All image and independent UV/frame,
topology and re-import checks pass. However 2238/2964 triangles retain
75.51%, missing 1186, with unchanged three draws and one material. This is
a cost trial, not yet a selected family level. Complete config, payload,
hashes, comparisons and checks are archived in
`build/lod-rollout/signals/cabinet-pass1/`; the next equipment trial is the mast.

### LOD critique 2: mast target control

Opened every native strip, both construction views and contact for both mast
requests. Color/value and shaft coverage hold at .25 / 27.15m. The initial
3835/8174 level (46.92%) passes all original image and independent field/raw
checks, but misses 3270. All three aiming head frames and separate lens/state
nodes remain; four materials and fifteen draws retain canonical routing.
The lower .15 request reaches 2849, meeting the count, but side-view local
RGB .12776 exceeds .08: visor/housing highlights and thin projected shapes
change. No image limit is altered. The source UV/frame audit still passes;
`make check-lod` returns 2 for images. Source-only noise is not claimed as its
cause. Both configs, payloads, checks and every image are retained in
`build/lod-rollout/signals/mast-arm-pass1/` and `mast-arm-pass2/` before a
middle request is tested. Close views expose coarser visor rims at both
densities; acceptance remains at the native switch.

### LOD critique 3: selected mast density

The .25 optimization request at the unchanged .25 switch reaches 3199
triangles, 39.14% of 8174, meeting the original 3270-triangle/40% goal.
Opened all three fresh native strips, both construction views and contact.
Color/value, shaft coverage, street-name lettering and red indications remain
consistent. Local RGB .02429/.05828/.02545 passes the original .08 bound;
mean/p95 and alpha/IoU pass too. The coarser visor rims remain a close-view
limitation. Fresh `make check-lod` and the independent UV/frame audit pass.
`build/lod-rollout/signals/MastArm-state-routing.json` independently records
all thirteen aiming/lens control nodes with matching control fields and
independent mesh/material bindings. This proves serialized state routing,
not live phase timing, flexible-cable updates or a new swept-motion audit.
The cheaper 2849-triangle visible-failure control remains archived. Measured
selected-level table/contact: `build/lod-rollout/signals/mast-report/`.

### LOD critique 4: select the useful cabinet distance

Omit the weak .25 cabinet row and retain one shared-map level at the existing
far starting point, .09 / 19.36m. Its 1482 triangles retain 50% of 2964,
against the unchanged 445-triangle goal. Opened all three native strips,
both construction views and contact. Gray body/vent values, door reveals and
the small service-post coverage agree at the switch. The closer construction
view exposes a polygonal service lamp, simplified louver and panel corners;
those do not read as faults at .09. All image/field/raw checks pass.

Explicitly tested this exact 1482-triangle export at the old .25 / 6.97m
distance. Opened all three native controls in
`build/lod-rollout/signals/cabinet-original-switch/`: the lamp turns visibly
polygonal and vent response changes. Front/side local errors .15375/.12741
fail .08; the rear passes. These failed old-distance comparisons and passing
new-distance comparisons establish the farther switch without changing gates.

Also opened all three 440-triangle ordinary-collapse goal controls at .09 in
`build/lod-rollout/signals/cabinet-goal-control/`. The lamp turns dark, the
vent loses its response and bright borders appear on the cabinet. Front
mean/p95/local .02873/.15687/.25460 and side p95/local .10196/.16268 fail;
the rear passes. This deliberate unguarded control uses the original maps
and is never a delivery. Its script/receipt record actual source, selected
and candidate dependencies and tool hashes. The selected 1482 is the lowest
reviewed passing count, not a global geometric minimum; `target_met: false`
remains. Both door meshes/pivots are retained, with matching serialized
door controls in `Cabinet-state-routing.json`. No new motion-clearance or
engine-light simulation is claimed. Measured selected tables/contact are
`build/lod-rollout/signals/report/`; the original .25 cost trial remains
archived in `cabinet-pass1/`.
