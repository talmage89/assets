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
