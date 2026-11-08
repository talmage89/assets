# C75 form and construction checkpoint

This is the requested stop before look development. Quick surfaces are baked
and judged on the export later in this log; this is not final game-ready acceptance.

## Pass 1 — reject holes, floating nose construction and an invalid exit layout

Color/value first: the yellow reads as yellow rather than ivory, and the tires
and underside keep dark values. The source daylight makes the empty opposing
windows far too pale compared with the service photographs. No albedo inference
is made from the blue shade in those photos. For comparisons the front photo's
background snow, side photo's unmarked dry asphalt and rear photo's pale gray curb are
assumed neutral; these are approximate white balances, not gray cards.

Opened all four `renders/pass1/` images (hero, front, side, rear) and the three
Commons service photographs. The first source fails construction: white voids
around the emergency-door top sash, missing greenhouse end closures, no
firewall under the windshield and an unsupported-looking hood/fender/cowl
transition. The rear is an unconvincing blank slab. The front lamps are flat
white rectangles; the grille's recessed web is sound but its tall rectangular
mouth and separate corner housings still look assembled from blocks. The
windshield is too shallow. The bus overall proportions and 13-bay rhythm read
well, but the near-empty bright cabin and thin seat profiles weaken it.

The dimensions review also rejects the side exit over the rear axle, a step
above the period first-step recommendation, narrow rub rails, and a rearward
hinged side exit. Correct these before any delivery claim. Move the exit ahead
of the axle, give it a forward hinge, use four 210mm rises, 104mm pressed rails,
close the physical body joints and rear sash, add rear corner glazing, deepen
the windshield and raise the padded back crowns. Round exposed rims with the
car's graded-ring method; hidden barrel rings were wasting about 6k triangles.

The original front must keep its own identity. Do not reproduce any photo's
grille or badge, and do not use a successful mesh audit to excuse a weak image.

## Pass 2 — reject the cowl shield, obstructed lettering and an exterior “interior” camera

Color/value first: the second source keeps a useful yellow/black hierarchy,
but its empty-window reflections are still brighter than the used photographs.
The immediate checkpoint issue is form, not a coating adjustment. Opened all
five `renders/pass2/` images at native size: hero, front detail, entrance,
interior and rear. The new rear glazing and closed sash remove the blank rear
and white void. The actual dark entrance recess reads well and shows the
steps and continuous grab rail.

Reject the added fender-to-cowl plate: a beveled extruded arrow is still a
flat shield. Replace it with a sampled compound sheet that changes transverse
section into the cowl. The wider seat-level rail obscures the district text;
move the print into the actual clear belt field. Rear lamps intersect the
new rail returns; separate their real circles. The “interior” camera is looking
along the exterior, not through the opening. Aim it through the entrance at
the driver, and add a separate honest aisle view. Keep these camera purposes
separate. Correct opening signs so both entrance leaves, the rear exit and the
crossing arm actually swing outward; the roof lids already rise correctly.

The wheel lips now read round at this distance. The nose remains more rectilinear
than the comparison buses and the front lights need a sealed curved cover.
Add that cover and keep its actual backing testable. These shortcomings must
be judged again on the baked export, not assumed fixed from source geometry.

## Construction audit between image passes

The first delivery magenta test found a real wedge between the raked
windshield seal and side post. A finite formed corner wrap now connects those
surfaces. The independent bumper mask initially used solid bounding boxes,
which falsely included open space behind the swept C-section corners; it now
uses the actual manufactured section, keeping its open rear. This is a mask
correction, not permission to conceal body gaps.

Contact checks also exposed unsupported looking mechanisms and floor height.
The doors and hatches now have hollow sleeves, pins and structural mounting
feet; bumpers have rail brackets, the exhaust has curved hangers and the
cabin floor has eight transverse 2mm C-section bearers seated on the chassis.
A three-point exhaust hanger hairpin folded its shading fans; the curved hook
removes that cause rather than suppressing the car-family mesh audit.

The original 632mm row pitch combined with overly thick padded backs failed
the 2010 NSTSP inspection's 24-inch space between seat/barrier faces. Rebuilt
to 670mm pitch with finite 40–56mm padded backs, shifted the seat grid behind
the front barrier, and retained the 75 places and the unobstructed side exit.
The measurement now intersects the actual backs at horizontal stations;
center-to-center pitch is not reported as clear space. The wider window bays
reach the real rear post, replacing the oversized rear quarter closure.
District lettering moves aft of the side exit so it cannot hang across an
open door. Rail fasteners are two physically located normal-baked rows on each
pressed rail, with no extra mesh rivets.

The next full-face delivery audit rejected eight shading-normal faces on the
new windshield wraps. Their analytic derivative crossed the helper's oblique
hemisphere hint near the top, so a per-vertex direction test reversed normals
within one consistently wound sheet. A constant front-facing hint removes that reversal. Six corner normals still
failed on the coarse chords/hidden returns. Tested the wrap alone through the
same modifier/triangulation path: nine vertical stations and lapped, closed
sheet gauge pass both sides, with zero bad face/corner normals. Exchanging
the hidden return ribbons for these samples preserves its 104 triangles per
side. The same car-family full-face
check now also runs on every source part before baking; export checks remain
independent fresh imports. No winding or normal threshold was relaxed.

## Pass 3 — exported gallery rejects the nose, mirror backs and false poses

Color/value first: the exported lane hero keeps a recognizable warm yellow
and deep black tire/underbody values; shadow-side windows show the high seat
backs. The roof's pale broad reflection and nearly invisible fasteners are
still CG tells compared with the balanced service photographs. These are
preliminary coatings and atlas detail, not a reason to alter the yellow
albedo toward a photograph's blue shade.

Opened every full-size image in `renders/pass3-export/`: all fifteen Cycles
views, including the complete turnaround, entrance, cabin, warning, roof,
scale and fleet. The body proportions, 13 window bays, dual wheels and
seating scale read well. The front grille web is seated, but the four yellow
bars around it remain visibly separate blocks. Replace them with one closed
molded nose, following both the actual hood section and the mouth contour.
The floating small maker plate is removed; identity remains fictional in the
root metadata. The wheel lips are round at this distance and the lamps have
no exported face shards, although their optical graphics remain basic.

Reject the chrome crossview eggs and forward-facing side mirror faces. A
front photograph shows the housings' black backs; the reflective surfaces
look rearward toward the driver. Give the crossviews a shallow black housing,
rear convex face and rim without adding triangles.

The entrance and roof proofs still show closed parts: imported nodes retain
quaternion rotation mode, so setting Euler values did nothing. Apply poses
through their actual world hinge matrices and record measured rotation
deltas. The aisle view is too dark to judge its construction; use its real
dome emission and an indoor camera exposure, recorded in provenance. The
rear close-up will show the exit open while the turnaround keeps it closed.

The new magenta diagnostic separates real defects from the test die: add an
aft backed reveal at the side exit, close the floor-to-wall joint, extend the
corner post to meet the entrance jamb, and close the cap underside. The die
must follow the curved/raked windshield and preserve open space beneath the
floor. A solid prism wrongly filled the space between mirror brackets and
windshield, and wheel-arch rays beneath the floor. No pixel-count tolerance
is introduced; the resolved leak target remains zero.

Three seeds do read as one fleet. Their lettering is distinct and correctly
oriented; variation in age remains subtle at full fleet framing. The emergency
labels are too blurred in the close-up. Increase those small charts' atlas
priority before the next export. Fine rivet and wear readability remains a
known limitation to judge again in the final paired checkpoint.

The corner repair also exposed the entrance's hinge geometry: its original
axes lay in the leaf plane. A wider post would intersect that sweep. Move the
axes 34mm outboard, use hollow sleeves around fixed pins and fork feet, and
seat those feet on full jambs tied to the stepwell walls. This is the same
bearing construction already used at the other exits, at eight sides for
these small knuckles. Removing subpixel bevels from the 50 sash latches
recovers more triangles than the real hinges cost. Motion checks now run
before atlas finalization/baking so a mechanism failure cannot waste a bake.

A further direct probe of the exported stair path (stored in
`build/walk-surface.json`) found the last tread short of the driver floor.
Vertical rays at x −0.36 to −0.29m saw no surface, while the nearby exposed
chassis rail was only 0.994m high. Add the missing top landing and its closed
riser, extend the stepwell walls into the floor joint, and measure the join
through twelve vertical probes on both source and fresh import. The probes
compare against an actual floor hit, not the target floor-height constant.
Two initial wall contacts only touched a beveled floor edge; a 2mm lap gives
a real intersecting joint, rather than increasing the distance tolerance.
The riser foot reaches the last tread's flat area instead of hovering over
its bevel. This costs 24 interior triangles and leaves the exterior unchanged.

The full-size front/detail images also show small triangular fins at the
fender's lower front end. Equal angular endpoints on different-radius rings
staggered those cuts in both height and depth. Give every ring the same
430mm rear and 750mm front trim heights, preserving the annular roll and
triangle count. The source remains a closed compound molding; no silhouette
fragments are painted over or removed from an image.

The same exported walking-surface scan also found the frame crown at 0.994m,
10mm above the fourth tread. Lower the original-estimate chassis rail 20mm
and extend its floor bearers to retain their measured contact. Its crown is
now below the tread surface, with the rubber/steel tread stack covering it.
The check now probes nine positions on each of the four actual treads as
well as the twelve landing positions, so a serialized-but-obstructed stair
cannot pass. This preserves every triangle and the body package dimensions.


## Pass 4 — complete export evidence, reject underlit photographic comparisons

Color/value first: opened all fifteen native-size Cycles gallery images, the
Eevee hero, all six source/export photographic pairs, the three baked 2048 maps
and the six-view blocker/envelope/leak contact sheets. Reopened the original
Commons photographs. Snow, dry asphalt and the rear gray curb remain the
recorded approximate neutral references. The overcast front/rear comparisons
are visibly darker than those balanced photographs in both source and export.
That is an illumination/exposure mismatch, not evidence to brighten the
yellow albedo. The first attempted correction changed the renderer's default
from −0.30 to +0.80, retaining the same camera and procedural diffuse sky. Archive
the rejected pairs under `renders/pass4-matches/` and
`renders/pass4-source-matches/`.

The finished lane hero has deep tire, grille, stair and underside shadows;
its bus-only display luma p5/median/p95 is 0.0118/0.2745/0.6793, p99 0.8076,
and no bus pixel clips any channel. These measurements exclude the campus
and sky; they support the image critique, not an albedo claim. The roof
still has a broad pale reflection. That remains a preliminary coating issue.

The nose is now joined and the grille is a recessed open web with a real
backing; there are no separated yellow bars or face shards. The cowl
transition still reads broad and more upright than the period photographs.
Its transverse sections are curved, but the large bright shoulder remains
visually dominant. This is the weakest form/styling area to judge at this
checkpoint, rather than a claim of a matched manufacturer's front. The
fender end fins are gone and wheel lips remain circular.

The open entrance shows four treads, the top landing and grab rail; its two
leaves clear their jambs. The through-door view shows the driver's seat,
steering wheel and controls, while the separate aisle view reveals every
row and ceiling lights. The warning view contains the full deployed crossing
loop, readable STOP and lit red lamps. The rear exit and both roof lids
open. Measured render receipts give 95° entrance leaves, 90° arms, 100° rear
exit and 65° roof lids. Adult/child mesh heights are 1.79999995/1.09999990m.
The review script now rejects stale hashes, incorrect poses or wrong scale
figures instead of relying on shot names.

The first Eevee fallback loses much of the cabin behind bright panes; it used
fewer samples and lacked the car renderer's ray tracing setting. Enable that
same ray tracing setting and its 192-sample minimum, retaining the imported
car thin-sheet glass helper. These bus panes have closed finite thickness:
their rear surface also needs to pass transparently in this sheet approximation,
so an unrefracted ray does not receive a second Fresnel/internal-reflection
response. Add that render-only adapter after the unchanged car helper;
Cycles and delivery geometry remain physical. Archive the first preview in
`renders/pass4-eevee/`.

Body seams, sash depth and four pressed rail courses read at this distance.
Tiny normal-baked rivets and emergency lettering are still softer than the
photographs. The three districts and fleet numbers differ correctly, but
their preliminary wear differences are subtle. Lamps retain basic optical
graphics and the seat vinyl is too uniform. These are explicit limits of
this pre-look-dev checkpoint. No material or geometry change accompanies
the comparison-light and Eevee presentation correction.

The first correction's receipts exposed a missed override: the camera tool's
saved shot default was actually −0.80, overriding both renderer constants.
Correct `photo_matches.py` itself to request +0.80 front/rear and −0.25 side,
verify the solved cameras again, and assert the actual recorded exposures in
`review.py`. A separate six-comparison GPU target now refreshes changed
calibrations without repeating the verified gallery, bake or export. The
Eevee correction did work: the finite-pane adapter restores visible cabin
and stair depth, with some preview dithering still visible.

## Pass 5 — final calibrated source/export comparison and checkpoint stop

Color/value first: inspected all six corrected photographic pairs. Their
actual receipts now read +0.80000001 front/rear and −0.25 side. The yellow
has a useful warm body value under the side sun, but the cloudy front/rear
surfaces and broad roof reflection remain paler and less saturated than the
balanced service photographs. The black rails, tires and cavities retain
dark values. This is not final appearance acceptance: coating response,
glass/environment reflection and used-surface calibration come first in
look development. No albedo is inferred from the photographs' unbalanced
blue shade. The neutral assumptions remain snow, dry asphalt and gray curb.

Reopened every final gallery view, the corrected Eevee image, the sixteen-view
contact sheet and four-view turnaround. Body proportions, window rhythm,
seat height, dual-wheel spacing and underbody clearance read as the specified
class. The front is original and still more upright and blocky than the
reference examples; its broad cowl shoulder remains the form weakness.
The shared grille web, backed joints, round wheel lips, finite lens covers
and black mirror backs survive export. No face shards, mirrored lettering
or resolved metal-panel leaks recur.

The source/export pairs expose real bake loss: the main lettering survives,
but emergency labels have softer edges, fine fasteners and wear become
subtle, and the export's coat highlights are broader than the source's.
Roof joints are weak even in the source comparison. At only 36.89% imported
atlas coverage and 70.25px/m median density, packing/chart reuse should be
improved before investing in fine surface work; extra geometry is not the
answer. The wheels are conspicuously clean next to the used photographs.
Warning-lamp optics, dashboard detail and vinyl scuffs also remain preliminary.
Fleet numbers/districts distinguish the three exports, while their age
variation needs to become more visible during look development.

The open-door, aisle, rear-exit, hatch and arm views establish functional
construction. The source measures 146 support contacts and 48 unobstructed
walking probes; 508 poses across sixteen mechanisms pass. The fresh imports
independently pass the car-family all-face audit and zero-overlap UV check,
and match the exporter in 169,903 bidirectional vertex samples per seed with
zero vertex/pivot displacement. Serialization does not replace those physical
checks. All six direct magenta views have zero resolved leaks. The native
school fits one bus, while its 12m socket spacing would overlap two parked
bumpers by 192mm; placement guidance is documented without editing the school.

`make -C school-bus` completes the exported Cycles gallery, source/export
comparisons, Eevee view and evidence validation. Every image is from scripts;
the gallery is the actual external glTF with its baked maps. This is the
requested form/construction checkpoint stop. No final docs image or final
look-dev approval is claimed.

## Round 2 — source form pass 1, rejected open-shell cuts

Color/value first: the archived exported checkpoint is too pale beside the
neutral-balanced service photographs. Passenger panes read gray-white, the
ochre enamel loses orange saturation, and the door reveals expose yellow
instead of a pale interior lining. Workbench is used below only for geometry;
its opaque glass and unlit print sheets cannot establish a material match.

Read the old hero, front detail, side, entrance interior, aisle and all three
photo pairs at full size. The old exports/cameras are retained under
`renders/round2-before/` and the worktree's ignored `build/bus-round2/`.
The two different maker photographs show a continuous hood/fender molding,
recessed optics, dark radiator depth and a smooth cowl transition. Their front
designs are references for construction only; neither contour is copied.

The first supported subdivision mold has a lower nose and integrated fenders,
but its wheelhouse Boolean was applied to an open sheet. The native 1000 px
Workbench views in `renders/round2-front-step1/` expose yellow cutter surfaces
across the wheels. Reject this result. Apply the 6 mm laminate before the cuts,
then check actual closed geometry again. The 84,230-triangle trial also exceeds
the 70k exterior allocation; reduce concealed wheel sections and internal disc
detail while retaining 96 tire and 128 exposed rim-lip stations.

The side camera's six-point fit mixed a different bus body's overhang/eave
geometry with chassis registration. Refit visible hubs and ground contacts,
as in the sedan review: 8.37 native-pixel RMS at 48.73 mm, versus 82.8 px and
21.7 mm before. The discarded eave picks remain body holdouts; this is a
camera improvement, not a claim of matching the reference bus's proportions.

## Round 2 — form pass 2, compound mold and cabin construction

Color/value first: the source Eevee preview is warmer than the old ochre,
and gray lining replaces the yellow dash surround and stepwell. Its 32-sample
software glass remains bright and dithered; reject it as evidence of the final
window read. Physical Cycles transmission and the exported atlas still need
their own review. The source preview also exposes a gray exterior wall at the
entrance; retain yellow outside and paint only the actual inner wall gray.
The two balanced exterior paint patches measure 249/195/89 and 178/130/59
sRGB (snow / near white parking stripe). Their different illumination is
visible: these are appearance samples, not estimates of calibrated albedo.

Opened both makers' photographs again, all five Workbench front/side iterations,
the five actual mesh section plots and the three completed software Eevee
views. The rear shoulder initially crossed the falling crown, producing a
trough. A monotonic rear transition now reaches the windshield sill. The mold
is one supported subdivision cage, with a 6 mm laminate before wheel/pocket
cuts and a separate level-3 source for normal transfer. Wheelhouse liners sit
inside the laminate lip. Source section curves are in
`renders/round2-front-step3/sections.png`; updated final sections follow export.

The first optical construction had 128 cover/reflector triangle crossings on
each side. Apply the same bowed die to the buckets, reflector bowls and bulbs,
then test again: zero crossings, with the unchanged car face/corner/area gates
passing. The amber lenses occupy real openings. The new grille has a recessed
return, open cross webs and a closed dark radiator bed. No maker's front is
copied. Tiny optical facets and the economical grille remain review points.

The seats have crowned cushions, broad rounded back tops, sewn welt geometry
on the entrance rows and material seams/scuffs on the rest. Gray lining,
rubber coving, barrier legs and modesty-panel supports meet the actual floor.
The first tread stays 354 mm high, with a shallow folded pan, yellow nosings
and a recessed courtesy light. The source now measures 86,488 triangles:
69,224 exterior / 17,264 interior, including 25,632 in six wheels. The car
full-face audit and all 153 actual static-support contacts pass. Existing
16-mechanism sweeps still pass at all 508 poses. These are construction checks,
not exported serialization or appearance approval.

Software Workbench identifies its renderer as llvmpipe; no shared GPU is used
for those quick geometry views. The software Eevee batch received SIGTERM
after three completed views, before the aisle image. Its retained images are
`renders/round2-source-pass2/`; Cycles look probes and final exported views
remain required. No documentation image has been written.

## Round 2 — look pass 3, rejected light probes and dense-source repair

Color/value first: the four native 1000 px source Cycles probes under
`renders/round2-source-cycles/` still show white sky through the far side
panes and a dark aisle. Gray lining and saturated yellow alone do not fix
that lighting/context problem. Reject these as the final look. The next
probe retains camera refraction but uses colored parallel-pane shadow
transmission, the documented Cycles glass/transparent-shadow optimization.
A charcoal studio wall supplies real context behind the orthographic side
view. A second aisle camera at adult eye height supplements, rather than
replaces, the original low camera required for before/after evidence.

The first dense normal bake is rejected. Its independent ray audit showed
99.996% fallback area: a later optical Boolean collapsed the dense source
to a cutter-sized solid. The production mesh was unaffected. Retain the
level-3 smooth fiberglass mold before the routed lamp openings; their
narrow perpendicular cut returns retain exact mesh normals. Add a hard
density/coverage gate to the normal transfer. The actual five section cuts
are regenerated under `renders/round2-front-final/`. No acceptance is
inferred from having run the bake.

The preliminary four-point side result in pass 1 fails its body holdouts
(132.7 / 370.4 native px). It is superseded, not accepted. The old reference
has a shorter rear overhang. Replace it with a photographed used 77-place
long body, balanced on the white trailer panel behind the nose. Eight
landmarks cover hubs, ground contacts and both upper/lower body ends:
23.62 native px RMS at 26.84 mm (16.40 px at 1400 px width), versus the
original 82.8 native px. Different makers' body/hood details remain visible;
the accepted 40 ft body is unchanged.

The completed pass-3 probes still have a dark aisle. Direct sunlight now
reaches the seats, but the low exterior sky strength is unsuitable for this
interior exposure. Use a broad bright procedural daylight sky for the two
aisle views, retaining the real glazing and omitting interior fill lamps.
The adult-height view also exposes yellow window-post returns: paint the
inside faces and glass reveals gray while retaining each outward yellow face.

The independent-build audit initially compared raw loop arrays, which can
rotate/reorder between BMesh conversions. Comparing corresponding oriented
triangles shows identical vertices and topology. Remaining smooth-normal
differences are float accumulation rounding (about 1e-7), not a different
form. The audit now measures this difference explicitly against 1e-6 and
requires exact geometry, bindings, transforms and functional metadata. Mesh
updates after mirror deformation and final triangulation are explicit.

## Round 2 — exported look pass 4, reject the remaining pale read

Color/value first: all eight 1000 px exported probes and all four source
and four exported photo pairs have been opened. The balanced used side
photograph is more orange and saturated than the render. In the low-eye
hero the side panes still reflect/transmit a bright, empty horizon; the
higher fleet camera sees the dark cabin and its panes read black. This is
a context/angle contribution, not evidence that the export lacks
transmission: its delivered Glass has transmission 1 and IOR 1.52.
Both source and export show the miss, so it is not hidden by a source-only
shader correction. Reject the current hero/window/paint read.

The brighter procedural daylight sky makes the aisle readable. The adult
view shows rounded padded tops and crowned cushions; the original low
camera remains for the exact before/after. The source's gray post reveals
have now reached the refreshed atlas/export. The 4k rebake checks 5,165,308
interior texels per channel with zero missing texels/reversed normals; the
dense hood transfer retains 99.885% area coverage under its stricter 1%
fallback gate. Source/export geometry, optical and lane checks still pass.

The first school hero has a native building, actual loading curb and three
queued exports, but clips the left mirror, hides the canopy and barely
shows the third bus. Move back and aim farther along the queue. Add only
read-only instances of the native campus tree meshes beside the loop,
without editing any original geometry/material/image. Their dark horizon
should replace the empty sky seen by the glass. Studio photo comparisons
use explicit original charcoal horizon flags to approximate the service
photographs' enclosed tree/bus surroundings. These are recorded scene
conditions, not photographic texture plates. Test the existing paint
against a modest green-channel palette reduction before changing its
baked base. The current lower splash/chips are still too subtle at hero
distance; strengthen cause-specific coverage after the color decision.

## Round 2 — look pass 5, context and palette calibration

Color/value first: opened all eight native context/palette trial renders.
The modest palette change (green factor .78) gives the desired orange-yellow
under the same hero light. Adopt linear enamel (.95,.332,.004), with matching
249/156/13 sRGB graphic substrates. Source deposition colors remain separate.
The used-photo field measures 223/130/1 after neutral balance; the earlier
render field is 185/147/59 (hues 34.86° / 41.90°). These are photographed
appearances under different illumination, not laboratory albedo samples.
The very dark first horizon flags reduce the render field to 139/102/0,
and the warmer candidate to 138/89/0. Reject that exposure as too dark.
Use lighter charcoal horizon reflectance and a 2.0 EV photographic exposure
for the next controlled source/export pairs. The hero keeps its low-sun
exterior exposure.

Native foliage improves the upper-pane read, but the mature crowns leave
a bright low horizon under them. Add original procedural understory only
where five actual native ground rays reject roads, walks and roofs. Reuse
native tree meshes without editing their data and place them on measured
ground. Remove the speculative north-side tree belt, which could overlap
the school buildings. The studio flags remain explicit visible geometry.

The wider campus-101 view holds all three buses and the mirrors, but its
canopy is occluded by the contiguous queue. Campus 102 has a long canopy
extending ahead of the lead nose; use that native lane for the hero, keep
the accepted campus-101 socket proof separately, and audit all three body
envelopes as well as all eighteen tires. The rear bus follows the real east
transition rather than extending straight over its curb. Final exposure,
framing and support results remain to be inspected.

Strengthen only causal coverage: irregular lower splash height, wheel wakes,
opaque primer exposed by leading chips, skirt-edge salt/rust, roof runoff
and rear soot, with duller rail crowns and bumper corrosion. The previous
chip mask faded primer into yellow; wear now changes its coverage. Give
the entrance treads and first two bench rows more of the existing atlas so
wear/ribs survive downsampling. Triangle and texture allocations do not grow.

### Export leak checkpoint before the full gallery

The new six-view direct test rejected the first final batch: 1,480 side
pixels and 13 top pixels. Archived actual/mask images and ray locations are
in `renders/round2-leak-failure/`. Side rays hit fictitious cutter-end walls
at X=-0.760m inside the test die's wheel opening. The independent filled die
now uses a through arch, as its rear arch already did. This changes the
expected empty space, rather than masking a delivery hole.

The top failure was real: the optical routing tool extended behind its
cassette and pierced the swept fender. Shorten that cut to the nose wall.
All 24 downward probes at the failed region now hit the actual hood, and
all-face normals and optical intersections still pass. The repair adds 66
triangles (hood 6,198; total 86,554, exterior 69,290). Rebuild the UV/bake and
all delivery proofs; previous 86,488-triangle receipts are superseded.

## Round 2 — exported look pass 6, finish the visible age and exposure

Color/value first: opened all eighteen 1400px Cycles gallery views, four
source and four delivery pairs, the Eevee view and historical hero. The new
school hero has saturated orange-yellow, dark cabin panes with local
reflections, a visible canopy/curb and three queued buses. Its bus-only
pixels have 31.45% below 25/255 display luma; paint median/p99 are .543/.642,
with no clipped RGB channels. These measurements support the image review;
they are not albedo values or an appearance pass by themselves.

The used side field is now 195/137/21 versus the neutral-balanced photo's
223/130/1. The render's nominally neutral plate is also cool, so replace
the residual blue sky contribution in photographic views with neutral
overcast light before changing the baked yellow again. A blanket 2 EV
overexposes the rear comparison: both source and export are pale and their
glass reflects white. Use an individual photographic exposure for each
view, preserving all solved camera geometry and recording those settings.

The integrated hood, recessed lamps/grille, gray lining, crowned seats and
shallow step are substantial improvements in the same-camera comparisons.
The adult-height aisle shows the padded tops, but the original low-eye
aisle is still too dark; raise its photographic exposure about one stop.
The front/side/rear orthographic rays see below the finite ground plane.
Extend a real studio wall below that plane and use it behind all three
views, without changing their cameras.

Reject the age read at this stage: lower dirt is visible in the close-up
but too faint in the hero, and roof runoff disappears beneath the coating
highlight. Increase the existing localized coverage, use opaque sparse
leading-edge chips at a less extreme noise threshold, and dull the source
coating over the same masks stored in delivery alpha. Strengthen hatch and
marker runoff, skirt salt/rust, bumper corrosion, rear soot, rail chalk and
seat contact scuffs. Keep all changes on their causal surfaces, within the
same geometry and shared atlas. The service photos show duller low panels
and wheels, not a uniform noise wash. Archive this rejected set in
`renders/round2-export-pass6/` and repeat the source/export judgement.

## Round 2 — source look pass 7, narrow the runoff and carry coating response

Color/value first: opened all seven new source probes and all eight pairs
under neutral overcast light. The used-side field is 191/117/0 against
223/130/1: its hue is now close, but value is low. Increase photographic
exposures moderately, without changing the yellow again. The added rear
reflection horizon fixes its white panes; its trial .8 EV is now too dark.
Restore a normal daylight exposure for that view. These trials remain in
`renders/round2-look-pass7/`; their delivery panels still use the prior atlas.

The brighter aisle reveals curved padded tops, welts, contact scuffs, tape
repairs and gray lining. Leading chips, skirt deposits and bumper corrosion
now read at useful distance. Retain those changes. Roof runoff follows the
correct crossfall, but its broad marks look like painted stripes. Reject
them: narrow and taper each path, break its coverage and keep slight drift.
The studio wall fills the old void, but the ground slab still occludes its
lower portion. Orthographic elevations should use the full-height card
without that horizontal slab; the camera framing stays unchanged.

The delivered coat had uniform .22 roughness despite dirt in the base
roughness map. Use the existing ORM green channel for both lobes through
standard `KHR_materials_clearcoat`, and match that response in the source.
The seed-specific .25/.20/.14 coat factors now have one shared parameter
table. This keeps the four bindings, three images and geometry unchanged.
Rebuild and bake these final shader refinements, then judge the refreshed
delivery rather than the earlier atlas under the new light.

### Fleet-marking regression found during final review

The final fleet view exposed missing district, fleet and plate planes on
seeds 102 and 103. The bake-only cleanup removed these staged variants
before the kit exporter could select them. Preserve objects with a
`variant_id` until that selection; continue removing the independent mold.
The old twelve-triangle difference between seeds was missing construction,
not an optimization. Each corrected delivery measures 86,554 triangles.

An independent check now compares the selected source marking planes,
after their staging offset, against fresh imported positions and UV corners.
It rejected the old seed 102 with all 36 corners missing. All three repaired
deliveries contain six planes and all 36 corners; maximum UV distance is
2.98×10⁻⁸. This proves the intended markings survive, separately from the
existing source/export serialization check. The shared baked images did
not change. Regenerate the complete gallery with the corrected fleet.

## Round 2 — look pass 8, final atlas and same-camera repairs

Color/value first: reviewed the complete eighteen-view Cycles set, eight
source/export photo pairs, Eevee, the historical hero and all seven repair
pairs at native size. This set exposed the alternate-marking regression
above; seed 101's final glTF/BIN remain byte-identical after that repair.
The used-side paint field measures 210/136/33 against the photo's 223/130/1,
after neutral balance on the white trailer behind its nose. This is rendered
appearance under different real surroundings, not a calibrated albedo match.
The snow-balanced first front and stripe-balanced second maker support the
warmer orange-yellow choice. Roof highlights still become peach under the
sky; the main sunlit yellow stays saturated and has no clipped channels.

The school hero fills the frame at 44mm, with the canopy beside the bus,
walk, curb and two queued seeds. Deep shade remains beneath it and inside
the wheel wells. At full frame, lower splash deposits, leading fender chips
and dull skirt edges remain visible after baking. Bus-only display luma
has 30.51% below 25/255; paint median/p99 are .544/.642, with zero clipped
channels. The masks exclude campus and sky. These support visual judgement
and do not establish physical albedo or photorealism by themselves.

The front's crown falls toward the recessed mouth; its shoulder sweeps back
into the cowl without the original yellow plate. Raking-light views and
five actual section cuts show changing transverse curvature. Both makers'
photos remain comparisons of construction, not contours to reproduce.
The clear covers reveal separate reflectors, and the grille has a dark
return behind its surround. Source-to-bake loss is chiefly fine surface
relief, rather than the compound silhouette.

The side match uses the long service body and all eight body/wheel anchors:
23.62 native pixels at 26.84mm, or 16.40px on the 1400px comparison grid.
The upper/lower window values are now dark, with far-pane light and seat
silhouettes; rear overcast reflection remains grayer than the service photo.
Gray lining, coves, modesty panel, rubber floor and yellow nosings separate
the cabin from the shell. Adult-height daylight reveals crowned upholstery,
welts, scuffs and two tape patches; the original low camera is brighter too.
The first step is a shallow folded pan rather than a skirt-height block.

Remaining CG tells: warning and rear lamps have simple optics; controls are
basic; fine fasteners and lettering soften at this atlas density. Runoff is
now narrow and broken, but retains some regularity. The cabin is intended
for exterior views, not close first-person play. Accept this look checkpoint
subject to the corrected fleet render and final proof audit; defer docs.
