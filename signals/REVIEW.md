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

### LOD critique 5: span wires at native size

Opened both whole construction views and the contact, then all seven
unscaled native original/LOD/difference pages under
`build/lod-rollout/signals/span-native/`. These cover every horizontal span
of the three comparison frames, including near/far poles, wires and heads.
Color/value, powered indications, messenger/tether runs and pole coverage
remain consistent. The six aiming heads and eighteen lens controls remain
separate. Close construction still exposes coarse fittings and head rims.
The .4 request gives 7764/17456 triangles (44.48%), above 6982. Every image
gate passes: worst mean .00483, local .04677, alpha .01852 and IoU .02893.

The first full check was interrupted with observed exit 143 after geometry
passed and before the independent normal audit finished; no own Blender
remained. That interruption is preserved, not called a pass. The directly
monitored full retry passes both checks; exact receipt is
`build/lod-rollout/signals/span-set-pass1-check-retry.json`. Config, outputs,
checks, payload hashes and native images are archived in `span-set-pass1/`
before a lower .25 request is tested at the same .25 switch. No tool or image
gate changed. New geometry uses 25 draws versus the original 27, with the
original three materials/maps; these are measured color-pass submissions.

### LOD critique 6: native pass, original trim check fails

Opened every native page in `build/lod-rollout/signals/span-native-pass2/`,
both new construction views and the combined reporter contact. The 5692-triangle
span meets 6982 at the unchanged .25 / 31.18m switch. Pole/wire coverage and
indications hold; close views still expose coarse fittings. Worst mean .00590,
p95 .03138, local .04875, alpha .02462 and silhouette loss .03856 pass.
`span-set-final-check.json` records exit 0, including the independent field audit.
Twenty-four aiming/lens control nodes retain their serialized state routing.

**Stop: no signals adoption.** The required original `make check` afterwards
returns 2: its unchanged delivery checker also scans the additive directory,
and catches actual newly crossed manufacturing trim cells. An independent raw
accessor audit, `build/lod-rollout/signals/trim-domain-audit.json`, measures:

| Trial | Newly crossed trim triangles | Outside-domain vertices | Maximum UV |
| --- | ---: | ---: | ---: |
| Cabinet 1482 | 12 | 1 | 1.0003411 |
| MastArm 3199 | 30 | 4 | 1.0040153 |
| SpanSet 5692 | 121 | 1 | 1.0516849 |

The three immutable sources have zero such faults. Screen comparisons and the
generic correspondence audit passing do not override this construction-specific
failure. No checker, threshold, source, UV or frozen tool is changed. All three
final configs, payload hashes, raw checks and every image are archived in
`build/lod-rollout/signals/{cabinet,mast-arm,span-set}-final/`. Their trial payloads
are removed from `export/lod/` so the original-only check can run independently;
`make lod` reproduces the rejected trials. Tables describe those trials, not
approved chains. This defect ends the family at its time box; all remaining
heads, posts and town assemblies stay LOD0 pending their own proof.

Final receipts: `original-before.json` exits 0; `original-after.json` exits 2
on the new trim faults; `original-after-isolated.json` exits 0 after archiving
the rejected additions. Exact original commands retain `-o build/delivery.json`
and `-o ../ground/export/ArterialSites.glb`. The unchanged delivery check then
audits all fifteen original containers. Tool freeze revision `55b6288`, all
103 literal hashes match in `freeze-check.txt`. The rollout's immutable receipt
still has all 1200 original delivery/texture/docs files unchanged. Repository
check: 2551 source files, zero errors. The reporter generated all three tables
with `--write-readmes`; `report/contact.jpg` was inspected. Its generic PASS
labels do not include, and cannot overrule, the failed original trim check.
No live jobs or tool edits remain for this family.

## Archived rejected LOD reports — round 1

These reports are rejected evidence, not delivered chains.

## LOD rollout checkpoint: blocked

No signal kind has an adopted chain. The following measured tables describe
rejected cabinet, mast and span trials. Their generic `check-lod` image,
geometry and normal checks pass, but the unchanged original `make check`
rejects newly crossed manufacturing trim cells and out-of-domain UVs in all
three. No limit is relaxed. See [the two-stage review and raw counts](REVIEW.md).
`make lod LOD_THREADS=4` reproduces these diagnostic trials; do not deploy them.
Their final payloads/checks/images are archived under
`build/lod-rollout/signals/{cabinet,mast-arm,span-set}-final/`; the rejected
outputs are removed from `export/lod/` after proof. Comparisons also remain in
`renders/lod/{cabinet,mast-arm,span-set}/`.

The family time box ends here. Untested standalone `Head_five` (1500), `Head_fya`
(1340), `Head_protected` (964), `Head_three` (1060), `PedHead` (464), `Pedestal`
(1564), `PushButton` (408) and `PushButtonPost` (1044 triangles) remain LOD0.
The four town containers also remain LOD0: 201 (47200), 202 (42408), 203 (51520)
and 204 (31504). These are deferred, not approved by another kind's trial.

Full available-container accounting, including those originals and the three
archived trials, is `build/lod-rollout/signals/full-family-costs.{json,md}`:
219943 stored triangles, 43 source-specific material resources, 973 primitive
placements, 15249449 physical payload bytes and 27.6957 MiB resident. The five
original image resources occupy 17.5001 MiB once; new images 0, added trial mesh
buffers .5431 MiB. Only the selected level of a placed kind is drawn; those
973 stored placements are alternatives, not simultaneous draws. Active draws
range from 1 to 228 across original containers/trial levels. Trial-specific
stored and drawn costs follow below.

<!-- LOD checkpoint mast-arm: begin -->
## Mast arm LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/mast-arm/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 8,174 / — | 4 / 15 | 411,715 | 3,633,325 | 4,045,040 | 17.500 + 0.3765 | near |
| LOD1 | 3,199 / 3,270 | 4 / 15 | 201,795 | 3,633,325 | 3,835,120 | 17.500 + 0.1756 | 25.0% / 27.15 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **18.052 MiB**, versus LOD0 alone **17.877 MiB**. Unique textures 17.500 MiB = 17.500 MiB original + 0.000 MiB proxy/impostor; all meshes 0.5521 MiB. Increase over LOD0 0.176 MiB = 0.000 MiB far maps + 0.1756 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/mast-arm/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/mast-arm/check.json` and `export/lod/mast-arm/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 1 × 512×256, 1 × 1024×1024, 3 × 2048×2048; LOD1: 1 × 512×256, 1 × 1024×1024, 3 × 2048×2048.

LOD1 separate moving meshes: `Mast_0__Head0__Fixed`, `Mast_0__Head0__S00_red`, `Mast_0__Head0__S01_yellow`, `Mast_0__Head0__S02_green`, `Mast_0__Head1__Fixed`, `Mast_0__Head1__S00_red`, `Mast_0__Head1__S01_yellow`, `Mast_0__Head1__S02_green`, `Mast_0__Head2__Fixed`, `Mast_0__Head2__S00_red_arrow`, `Mast_0__Head2__S01_yellow_arrow`, `Mast_0__Head2__S02_yellow_arrow`, `Mast_0__Head2__S03_green_arrow`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 11,373 | 4 | 30 | 4,246,835 | 18.0523 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 15 to 15 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint mast-arm: end -->

<!-- LOD checkpoint cabinet: begin -->
## Controller cabinet LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/cabinet/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 2,964 / — | 1 / 3 | 180,579 | 3,539,302 | 3,719,881 | 16.000 + 0.1681 | near |
| LOD1 | 1,482 / 445 | 1 / 3 | 101,118 | 3,539,302 | 3,640,420 | 16.000 + 0.0924 | 9.0% / 19.36 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **16.261 MiB**, versus LOD0 alone **16.168 MiB**. Unique textures 16.000 MiB = 16.000 MiB original + 0.000 MiB proxy/impostor; all meshes 0.2605 MiB. Increase over LOD0 0.092 MiB = 0.000 MiB far maps + 0.0924 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/cabinet/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/cabinet/check.json` and `export/lod/cabinet/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 3 × 2048×2048; LOD1: 3 × 2048×2048.

LOD1 separate moving meshes: `Controller__Door__Fixed`, `Controller__PoliceDoor__Fixed`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 4,446 | 1 | 6 | 3,820,999 | 16.2606 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 3 to 3 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint cabinet: end -->

<!-- LOD checkpoint span-set: begin -->
## Span wire assembly LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/span-set/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 17,456 / — | 3 / 27 | 770,206 | 3,595,708 | 4,365,914 | 17.333 + 0.7065 | near |
| LOD1 | 5,692 / 6,982 | 3 / 25 | 318,002 | 3,595,708 | 3,913,710 | 17.333 + 0.2751 | 25.0% / 31.18 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **18.315 MiB**, versus LOD0 alone **18.040 MiB**. Unique textures 17.333 MiB = 17.333 MiB original + 0.000 MiB proxy/impostor; all meshes 0.9816 MiB. Increase over LOD0 0.275 MiB = 0.000 MiB far maps + 0.2751 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/span-set/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/span-set/check.json` and `export/lod/span-set/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 1 × 1024×1024, 3 × 2048×2048; LOD1: 1 × 1024×1024, 3 × 2048×2048.

LOD1 separate moving meshes: `SpanWire__Head0__Fixed`, `SpanWire__Head0__S00_red`, `SpanWire__Head0__S01_yellow`, `SpanWire__Head0__S02_green`, `SpanWire__Head1__Fixed`, `SpanWire__Head1__S00_red`, `SpanWire__Head1__S01_yellow`, `SpanWire__Head1__S02_green`, `SpanWire__Head2__Fixed`, `SpanWire__Head2__S00_red`, `SpanWire__Head2__S01_yellow`, `SpanWire__Head2__S02_green`, `SpanWire__Head3__Fixed`, `SpanWire__Head3__S00_red`, `SpanWire__Head3__S01_yellow`, `SpanWire__Head3__S02_green`, `SpanWire__Head4__Fixed`, `SpanWire__Head4__S00_red`, `SpanWire__Head4__S01_yellow`, `SpanWire__Head4__S02_green`, `SpanWire__Head5__Fixed`, `SpanWire__Head5__S00_red`, `SpanWire__Head5__S01_yellow`, `SpanWire__Head5__S02_green`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 23,148 | 3 | 52 | 4,683,916 | 18.3150 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 25 to 27 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint span-set: end -->

## Fixed-region adoptions, 2026-11-09

Frozen tool `cc6cfee`, literal hashes in `build/lod-uv/freeze.sha256`.
All original deliveries already exist here. The original frozen-input
`make check` passes before work (`build/lod-uv/signals-original-before.json`).
The immutable ledger covers all 52 original signal delivery/map/docs files.
These proofs compare unchanged delivered LOD0 under identical lighting; no
photographic balance or new realism approval is inferred.

### Cabinet critique 1 — native color and small powered fixture

Opened all three .09 / 19.362 m native strips and their difference panes.
Cabinet gray, zinc, dark vent slots and the separate service-light center
retain their source values. The new row is 2676/2964 triangles against 445,
1194 more than the rejected 1482 trial. Worst mean .0000983, local .00404,
alpha .000913 and silhouette loss .000986 pass unchanged limits. No new
intermediate image is referenced. The saving is modest: 288 triangles.

### Cabinet critique 2 — held doors, original trim-domain gate

Opened both construction views and contact, revisiting door rims, hinges,
the access aperture, louvers and lamp at native size. Source panel construction
and values agree; small original bevels remain visibly coarse close up. Both
door mesh hierarchies and canonical pivots survive. The independent source-field,
UV-area, tangent and re-import checks pass. Most importantly the family's own
unchanged `make check` includes `export/lod/cabinet/Cabinet_LOD1.gltf` and now
passes: the old 12 trim crossings and outside-domain vertex are gone. Every
original byte remains unchanged. This frequent part's small extra .1594 MiB
buffer buys a 9.72% triangle saving without a private atlas; the 445 goal is
explicitly missed and no optimality or engine timing claim is made. Rest checks
and original sampled motion are separate; keep LOD0 during door interaction.
Final native evidence: `renders/lod/cabinet/`; archived proof:
`build/lod-uv/archive/signals/cabinet-final/`.

### Mast arm critique 1 — native values and coverage

Opened all three native .25 / 27.151 m strips, both construction views and
contact. Yellow cases, dark visors, red indications, gray support and green
street-name values agree with LOD0. Arm/pole width, three head coverage and
letter shapes hold. The source coarse fasteners and head construction remain
visible close up. This row is 7196/8174 triangles against 3270, adding 3997
triangles over the rejected 3199 trial. All original image gates pass; no
palette, image, powered-surface or acceptance setting changes.

### Mast arm critique 2 — original trim gate and state routing

Revisited the native arm/head joints, street name and lens outlines after
the field audit. No new seam, missing member or changed indication appears.
The family's own `make check` now includes both new files and passes its
unchanged manufacturing-cell/domain/UV-area checks: the old 30 crossings and
four out-of-domain vertices are gone. Re-import, normals and tangents pass too.
The asset state audit measures ten original lens nodes, preserving every
state flag, lit/off material name and world frame; receipt is
`build/lod-mast-arm-state.json`. It is now part of public `check-lod`.
Saving 978 triangles is modest (11.96%); the 3270 goal remains unmet. Fields,
names and rest appearance are proved, not flexible-cable motion or engine
phase timing. Original 52-file receipt is unchanged. Final evidence:
`build/lod-uv/archive/signals/mast-arm-final/`, native `renders/lod/mast-arm/`.

### Span set critique 1 — native color, wires and indications

Opened all three .25 / 31.177 m native strips, construction views and contact;
reopened the wide 0/55-degree strips at original pixel size. Yellow cases,
red/green indications and gray supports retain source values. The six heads,
upper span and lower tether remain; the 145-degree view is nearly end-on and
cannot prove the whole span. The 13754/17456 result misses 6982, costing 8062
more triangles than the rejected 5692 trial. All unchanged image gates pass.
Two independent native-image samplings address thin members: top-wire alpha
coverage ratios are 1.00026/1.00009; 1298/2082 thin-run bands including the
lower tether give .99847/.99854. Raw source/level pixel samples are in
`build/lod-uv/signals-span-{wire-coverage,all-thin-bands}.json`. These measure
sampled image coverage, not every diameter or continuous cable motion.

### Span set critique 2 — trim domains and state routing

Revisited the hanging joints and head outlines against the unchanged source.
Close-up construction retains the source's coarse macro detail; no new exposed
trim patch or missing hanger appears. The family's own `make check` includes
the new span file and passes: the old 121 crossings and outside-domain vertex
are gone. Serialized boundary, UV-area, tangent, normals and re-import gates
pass. The state audit measures 18 source lens nodes with identical flags,
material memberships and world frames (`build/lod-span-set-state.json`).
This does not certify engine phase timing or flexible-wire deflection.
The saving is 3702 triangles (21.21%), with 25 active primitive placements
instead of 27 and no new texture. The original 52-file receipt is unchanged.
Final native evidence: `renders/lod/span-set/`; archived recipe and checks:
`build/lod-uv/archive/signals/span-set-final/`.

### Signal family closeout

Public `make check-lod LOD_THREADS=4` passes all three chains and state audits
(`build/lod-uv/signals-public-final.json`). The original frozen-input check
passes after the span trial; all 52 original files are byte-identical.
Full 15-container accounting, including every unadopted part/town, is in
`build/lod-uv/signals-full-costs.json`: 233196 stored triangles, 43 canonical
per-container material references, 973 stored placements and 15838625 distinct
payload bytes. Maps remain 17.5001 MiB; new meshes add 1.1049 MiB, taking full
family residency from 27.1526 to 28.2575 MiB. Original town containers draw up
to 228 primitives; adopted cabinet/mast/span draw 3/15/25, with only one level
active per instance. Stored placements are not simultaneous draws.
The combined report/contact is `build/lod-uv/signals-final-report/`.
