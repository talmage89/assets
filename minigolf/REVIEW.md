# Miniature golf — construction and look-dev critique

Passes 1–4 record the earlier form gate. Revision passes below continue through
baked look development and judge the delivered GLBs. Final docs remain outside
this checkpoint. Photographs never enter a material or supply a vertex.

## Pass 1 — imported glTF, `renders/pass1/`

**Color/value first.** The first swatch rendering is too cool and too evenly
filled. Carpet reads blue-green and the rock is a pale gray. The 2007 photo's
white lighthouse paint is the neutral; the 2011 small-course photo's clear
concrete walk is the neutral. These are quick values, not measured final
albedo. Increase raking sun relative to sky, and make the carpet distinctly
putting green without washing gray over it.

Viewed every generated image at native resolution: classic and adventure
oblique overviews, then hero. Harsh failures:

- The two places are too similar: regular narrow rectangles on six straight
  lanes with a pond swapped in. Adventure needs shaped greens, grading,
  staggered axes, and a stronger central planted/water identity.
- The hero camera looks into an oversized foreground boulder. Most of the
  water is hidden; the course/hut and road become a background strip.
- Border rock is overbuilt: some adventure holes reach 9,876 triangles. Reduce
  repeated edge stones, retain geometry in playing surface, cups and features.
- The elevated carpet/slab has no compacted support down to grade at the high
  ends; actual support is needed, not a serialization comparison.
- Side approaches cross continuous borders. Leave real approach openings.
- The footbridge's joists were rotated with the wrong cross-section axis and
  did not reach the deck underside. Use actual 2×6 stock and measure contacts.

Revisions: more organic adventure widths/ends and yaw, continuous 2.5% rising
site grade, a graded planted base below every slab, edge openings at both tee
and cup, smaller stone population, a revised water-facing camera, and corrected
joist/deck/abutment seats. Builder sections establish the 4-inch slab and
published tee-pad stock; the period photos establish density and construction
language, not a copied plan.

## Pass 2 — imported glTF, `renders/pass2/`

**Color/value first.** Cavities now go dark and shadows are directional, but
the quick carpet is still too cyan and the original angular rocks throw an
unconvincing pattern of triangular highlights. Reduce blue in the green
swatches and use a continuous smooth normal field between stone bedding
breaks. Final fiber, stone color and weathering remain outside this gate.

Viewed all six renders at native size: classic ground, adventure ground,
adventure above, hero, windmill, waterfall. Rejections:

- The rectangular cut in the planted grade does not exactly meet the radial
  bank: a black slit appears at the pond's north side in the overview. Match
  the actual rectangle boundaries with asymmetric north/south radial extents.
- The windmill close view clips its sails and views it from behind because
  the hole faces the opposite way. Place its camera in the hole's own frame.
- The hub is solid and intersects its shaft. This is a construction failure,
  even if the blades clear the tower. Bore it and test the real surfaces.
- The lighthouse is excessively slender relative to the 2007 roadside form.
  Widen its tapered shaft, gallery and lantern while retaining the chosen
  4.73 m overall height and a real ball tunnel.
- The castle is too plain at course distance. Add original conical turret
  caps; move the operating gate ahead of the masonry and give it guides.
- The hut's door extends through a jamb and below the finished slab. Correct
  its physical opening, hinge, threshold and two hinge bearings.
- The bridge landings need ramps down to the promenade. The planted grade
  also buries some of the presentation shrubs; place their roots on grade.

Revisions above are geometric. Kit motion collision and fresh cup rays judge
construction independently of glTF serialization. The cup test deliberately
samples its recessed floor off center: the center is an actual drain opening.
The initial camera fits also exposed an invalid 10 m lighthouse camera and
below-grade castle camera; enforce a 1.65 m eye prior and retain the resulting
residuals rather than using camera pose to conceal a different design.

Additional construction audit before pass 3: the first parking court reserved
only 2.25 m behind the stalls. Replace it with measured 7.3152 m aisle and
5.4864 m stalls, remove three central positions for the hut, and connect two
native curb-cut driveways. End the fence runs exactly on their last posts,
with shared corners and rails supported on post faces. Raise the upper-hole
tee signs and scorecard shelves with the playing grade. These were form
failures, not defects to camouflage with a material. The hut hinge audit
also found the fixed pin inside the leaf edge; set the leaf clear of its bored
barrels and connect it with actual offset straps. Re-test the actual surfaces.

## Pass 3 — full-size Cycles gate, `renders/pass3/`

**Color/value first.** The carpet now reads green. White fixture paint keeps
its value while the hut recess and underside cavities go dark. The quick
palette remains flat, and the border stone is too uniform in color; these
are explicit look-dev work. The final hero exposes a pond, lighthouse, hut,
road and town with a lateral shadow, rather than hiding the water behind a
foreground rock. The added north tree line removes the empty horizon in the
opposite player-height views. Source period neutrals are recorded in
`build/reference-balance.json`; the initial clipped lighthouse paint ROI was
rejected and replaced with unclipped concrete.

Opened all twelve 1440 px Cycles images at native size: hero, both courses
above/from ground, tee, cup, border, waterfall, windmill with the measured
1.8 m figure, human bridge and clubhouse. Rejections caught only by images:

- The cup opening has a straight chord: an annular fan reaches too far from
  its outer corner and clips across the circle. A liner-diameter ray proves
  the liner, not the whole clear opening. Partition the fan at the corner
  angle bisectors; add 24 rays just inside the mouth to catch any obstruction.
- The walk skins face downward, so inward solidification extrudes upward.
  Their tops sit above neighboring carpet. Reverse the authored winding,
  explicitly enforce up-facing top normals and assert it before export.
- The stream's rectangular excavation is wider/longer than its liner skin.
  Fill its two sloping banks and terminal bank against the actual channel.
- The interior sorting trays and the external putter rack lack supports.
  Add the supported worktop, rack uprights and a real front slab apron;
  seat the rack heads on its lower rail. Constrain the hut's door to 90°,
  where it clears the deeper inner worktop, and sweep that documented range.
- The rear shelf must meet its wall; the service vault must follow the site's
  grade. Give the intake its visible rigid connection into the pond bank.

The castle, covered bridge, lighthouse, windmill and wreck remain deliberately
small original roadside fixtures, compared with different historic designs.
Camera fits are not shape-reproduction certificates. Full-image EXIF and
crop-equivalent focal priors are recorded; all comparisons keep the original
asset scale and a stated 1.65 m eye prior. Their residuals remain visible.

## Pass 4 — corrected exported construction and final form audit

**Color/value first.** All fifteen current Cycles frames were opened at native
1440 px, including the three isolated matched-camera imports. The hero has
whole-frame display Y′ p1/p5/p50/p95/p99 of
**.0028 / .0297 / .3735 / .7816 / .8090**, with **zero white clipping**.
This includes sky and foliage; it is a tonal diagnostic, not an albedo claim.
The hut's recess, beneath the bridge and inside the cup have genuinely dark
cavities. The green no longer reads cyan. Finish calibration remains pending.

The cup now has a complete circular mouth. Twenty-four near-rim rays for each
of 36 cups see a floor at least 99.60 mm below the lip; the center remains an
open drain. The walk tops now point up and the actual imported side-walk probes
measure .065000 m / .302500 m at the two proof locations. Raised-approach
white sheets no longer sit over carpet. Counter trays sit on the supported
inner worktop, the rack sits on its enlarged concrete apron, and putter blades
rest on its lower rail. The door's 90° stop clears this deeper worktop.

A local bank patch did not close the underlying geometric mismatch between
an oval liner and a separate channel. Rebuilt those as **one original concave
basin outline**, shared with the terrain excavation. Its middle liner, floor
and water line correspond around the open mouth and stream terminus. Deleted
buried terrain faces after the exact Boolean. Six imported rays from pond to
stream now measure Z=−.170000 m and no intervening terrain. The bridge ramp
landings follow actual site grade. The rectangular black bank slit is gone.
The procedural context ground extends beyond the camera horizon; a clipped
finite-plane black band is removed without downloaded sky/lighting.

Photo audit: all three side-by-side pairs and their source renders reviewed.
The 2007 lighthouse, 2011 Michigan green and 2011 California castle are
**different original forms**, not replicas. Native-crop landmark RMS is
11.21 / 17.11 / 33.95 pixels. The castle is the weakest fit: terrain-obscured
base correspondences and different turret proportions leave visible roll and
scale residuals. Its pair is a silhouette/construction comparator, not an
exact camera survey. Estimated cropped-frame lenses are 411.8 / 110 / 180 mm;
the hero remains a separate 40 mm eye-height view. Procedural sun direction,
height and sky are estimated per photograph, with neutral-gain ROIs recorded.
No comparison is described as finished-material or inverse-albedo calibration.

Final construction proof:

- Classic **123,712** triangles; adventure **174,304**. Holes **4,144–5,512** /
  **5,640–7,108**. Every fixture is below 15k; the wreck is largest at 6,428.
- Actual imported cup inner diameters match 107.95 mm within 1 mm; source slab
  edges measure 101.6 mm. Tee pads measure the published 36-inch width.
- Both rotors show zero measured fixed-surface penetration at 5° samples.
  Minimum sampled carpet gaps are 28.56 / 15.87 mm: clear of carpet, while
  the lowest blades cross the 42.7 mm ball envelope. Both portcullises and
  90° entry leaves show zero penetration over 21 sampled poses.
- Bridge deck/joist gap is 0; joist/abutment gap is about −0.0000075 mm.
  These are source contact measurements; fresh export probes independently
  confirm the deck and sockets.
- Actual imported parking aisle / stalls: 7.315199 / 5.486401 m. The two
  driveway openings use native Ground construction. No civil/accessibility
  or vehicle-dynamics certification is claimed.
- 250 seeded plans plus the two explicit proofs have no overlaps between
  their conservative green/border convex envelopes. This is a bounded
  sampled planning check, separate from physical surface collision.
- `make WIDTH=1440 SAMPLES=32`, `make repeat check check-renders`, repository
  check, source/import construction and the fifteen-frame image receipt pass.
  Seven delivered glTF/BIN/PNG files repeat byte-for-byte. All **208** existing
  delivery/docs files remain byte-identical. No kit file changed.

Remaining weaknesses at this gate: the six-column routing is still regular;
rockwork and falling-water silhouette are coarse and clearly procedural in
close views; the castle photo fit is approximate; distant house/shop context
is economical massing and repeats. Carpet fiber, seams/patches, visible use,
repainting, algae/mineral staining, final water response and shared finished
UV/maps are deliberately deferred to look-dev. No final docs JPGs are committed.
The assets stop here for the requested form/construction review.

## Revision pass 5 — source form, broad photographs and two published plans

**Color/value first.** The archived checkpoint's pale uniform rocks and clean,
flat carpet remain rejected. The 2011/2007 course photographs are balanced on
unclipped sunlit concrete (the existing `build/reference-balance.json` receipt).
The new source palette targets buff rock, dark green polypropylene, gray
weathered wood and repainted fixtures. Workbench does not certify those values,
texture response, water, or wear: its gray foliage is a preview limitation.

Opened all six requested archived frames at original resolution before design,
then both 1200 px course overviews and every ground/detail Workbench diagnostic.
Rejections and resulting construction changes:

- The first compressed six-column arrangement was still visibly a grid. Reject
  it. Adventure now has a perimeter circuit around the water and an inner
  sequence; holes 15 and 18 span the stream/pond on girders and abutments. The
  classic gets a common concrete court, rather than lawns between islands.
- Middletown's layout/grading sheets show interlocking greens and roughly 66–73
  ft contours. Oak Island's packet page 40 gives a second independent winding
  water-crossing plan; its memo states 18,590 sq ft. The new adventure planning
  enclosure is 1,840 m² (9.78 holes / 1000 m²), between the two published scale
  comparators. This is an enclosure density, not a claim that green coverage
  or every route length duplicates either site. `src/routing.py` samples the
  actual authored outlines and levels; source/import tests remain separate.
- Initial continuous rock had equally flat horizontal rings and still looked
  like stacked discs. Reject it. Bed elevations now vary around each outcrop;
  the mass is fractured and softly carved. The waterfall's first three sheets
  were inside that mass: cut a spill channel and place three receiving ledges
  behind exposed weirs. The new camera stays outside the crossing slab.
- High greens must rise with their local grade, rather than use one height per
  lane. Use actual station positions in the height function. The quarry stair
  and ledge show the terrain change from the ground. Fine bumps/ramps retain
  the accepted concrete/carpet/cup construction and topology density.
- Windmill sails now have heavy stocks, leading boards, bars and diagonal
  bracing; the tower has overlapping siding, windows and service door. The
  lighthouse's real tunnel passes through masonry supporting its shaft. The
  castle is a deep six-metre gatehouse with a keep, buttresses and corbels.
- The clubhouse gains siding, open framed side windows, a sliding service sash,
  canvas awning, price/menu boards, restroom marking, a porch light, stock and
  putter racks. Sash bearings and slide clearance need the imported audit.
- The new horizon uses actual library house, strip-mall, station, car, utility
  pole and street-light construction. Native maple/oak and boxwood/hydrangea
  replace massing substitutes; deterministic rotations/sizes and planted
  masses replace the string of identical shrubs. This is presentation context,
  accounted separately from the delivered lane/fixture geometry.

The added Henderson photographs are visual references for buff shotcrete and
wet/dry staining after use. Their gravel, irregular planted margins and broken
water are substantially richer than the current source. Keep that difference
visible in the next critique; a geometry audit cannot close it.

Final material, matched-light and imported-GLB critique passes are still pending
at this entry. No image here is represented as an approved look-dev result.

## Revision pass 6 — first baked GLB checkpoint, rejected

**Color/value first.** Opened all five 1000 px, 16-sample Cycles images in
`renders/look-pass1/` at their original size, then the used Henderson falls
photograph again. Dark carpet reads as polypropylene, but backlit gray rock
and nearly black service joinery do not match the reference's warm, readable
dry stone and ordinary weathered lumber. The waterfall is too dark and blue;
its sheets read as plastic. The first sun/sky balance hides too much form.

- Reject the lumber mapping. The staged post GLB's charts do not agree with
  the delivered atlas: large black gaps and hardware stripes appear on every
  beam. Use clean interior gate-board/end-grain pixels of the unchanged
  canonical atlas, with its real longitudinal grain direction.
- Increase procedural sky fill modestly and exposure by .35 stop; use a
  raking front sun for the waterfall. Preserve cavity shadows and check the
  revised values before changing dry-stone albedo, already a buff linear
  .36/.285/.19. Reduce the exaggerated black fracture graphic.
- Raise the water's transmitted color and transmission; halve its normal
  amplitude. Replace polygonal foam clumps with thin broken receiving rings,
  and add tapered aeration streaks attached to the actual falling sheets.
- Reject both first hero framings: the classic clips the castle and barely
  includes water; the adventure looks across a crossing toward the road and
  hides most of the pond. Move them at the same real eye height and 40 mm.
- The classic court's uninterrupted plane is too smooth and scaleless. Add
  narrow, dirt-darkened expansion joints at actual three-metre slab spacing.
- The source support checks now measure <1 mm deck contacts and <.22 mm end
  bearing contacts. Fresh GLB tests caught and corrected a reused cup-height
  variable and sidewalks that followed playing bumps instead of the site grade.
  These corrections are construction evidence, not visual approval.

All first-pass images remain local. No final docs image is committed.

## Revision pass 7 — second imported checkpoint, rejected where noted

**Color/value first.** Opened the two revised hero images and tee detail at
1000 px. The warm lit rock and expanded sky fill read more clearly; the
weathered lumber is still almost black. Sampling the real shared atlas proves
why: the chosen color region's tangent normal points inward (blue near zero).
The previous UV-coordinate correction alone did not solve its response.
Select a clean board region with positive-Z normals and add an independent
hemisphere check on the exact reused pixel rectangles. Do not edit the source
family's textures. Its shipping maps remain byte-identical.

The classic court's expansion joints give useful scale. The windmill and
covered bridge read as constructed roadside fixtures, and the price/name
signs and planted boxwood/hydrangea read from player distance. Native boxwood
geometry seeds 811 and 829 now share the canonical leaf/wood materials and
maps, rather than adding texture sets. Growth, sizes and planting locations
are deterministic; no imported reference pixels or downloaded assets.

Reject the adventure hero again: its crossing green still covers almost all
of the pond. Test north, west and south bank cameras, each 1.65 m above an
actual down-ray hit on the imported course, with a 35 mm lens. The first
three frames survived; the following batch received SIGTERM before the cup
frame, with no cause established. Resume smaller batches and inspect every
result; do not treat an interrupted render as an approved checkpoint.

The widest native photo residuals are 28.85 px / 2816 px lighthouse, 18.02 /
2892 px green and 33.16 / 4000 px castle, at 35.0 / 42.7 / 56.8 mm. Castle
comparison now uses the classic course to avoid the adventure clubhouse's
occlusion. These are homologous design landmarks with disclosed error;
full-course visibility and the actual pairs still require visual judgment.

## Revision pass 8 — camera probes and water/rock rejection

**Color/value first.** Opened all three 1000 px north/west/south camera probes.
The dry rock now reads warm buff rather than blue-gray, and the real lumber
chart has corrected its black response. The pond is too mirror-like and the
wet stone too close to its dry value. Keep the dry albedo; increase the
water's ripple-scale normal, darken the physically wet spill-zone mask and
retain mineral/roughness variation at the damp base.

Choose the north-bank hero: its open water, castle, clubhouse and commercial
road all appear together. West hides most fixtures, south looks through the
crossing's rail and deck. Both new heroes measure their 1.65 m eye from an
actual imported support down ray, rather than claiming a height constant.
The classic camera moves closer so pavement does not dominate the frame.

The probes make two remaining form errors unmistakable. Reject the tall,
pointed cheeks: smooth taper still reads as a pair of eggs despite ledges.
Replace their radial profile with broad fractured crowns, superelliptic
plan faces and alternating overhang/recess beds, using fewer angular
stations to retain the budget. Reject the white froth rings: they read as
CAD washers. Replace them with small irregular, disconnected foam fragments
and randomized thin entrainment streaks attached to the flow. Separate
pond ripple and falling-water normal regions inside the same existing atlas
and material; no texture allocation or material-state increase.

The fully rebuilt export passes source contacts, all 36 cups, sampled motion,
normal/tangent checks, authored UV boundaries, the exact reused lumber-normal
hemispheres, three precision regression cases and repository rules. This
proves the build. The next imported images and full-course photo pairs judge
whether the latest rock/water corrections read well enough.

## Revision pass 9 — complete six-frame third checkpoint

**Color/value first.** Opened both heroes, waterfall, cup, fixture and clubhouse
at 1100 px. The repaired lumber reads gray weathered timber. The dry ledged
rock is warm and has better broad faces, but its fine response remains softer
than the used-falls photograph. Its shaded white fence panel is now explicitly
neutral-balanced in `build/reference-balance.json`; that photo has mixed
sun/shade light, so raw brightness is not an albedo measurement. Pond
reflections remain too straight: the encoded ripple normal's measured standard
deviation is only about .01. Increase its height field before accepting it.

- Keep the north-bank composition and the broadened outcrop crowns; neither
  depends on moving/rescaling a fixture for the hero. Keep all fixture meshes
  in the real course in the photo comparisons.
- Move the cup camera around the marker: the old camera aligns almost exactly
  with its off-cup pole and hides the liner. The dimensions and cup topology
  remain unchanged.
- The service sash works, but the counter stock disappears into shade. Add a
  real fluorescent housing/tubes and an exported emitter socket, with a
  corresponding studio area light. Tighten the window detail camera.
- Replace the leaves' obvious elliptical scatter with seeded sheltered eddy
  clusters and individually turned leaf shapes. Keep the leaf count and sizes.
- Give the downstream stream two actual 35/45 mm level drops and receiving
  pools, rather than calling two stones on one water plane a fall. Lower the
  associated froth to the real surface; retain the .40 m main-pool depth.
- Cut planted islands out of the classic court, give them actual soil/edging,
  and share their footprints with native planting placement. Move its entry
  planting clear of the parking stalls and head walk; filter foliage envelopes
  against greens, fixtures, lane-side walks and the adventure circuit. The
  classic pond moves 1.7 m within its central landscape corridor, clear of the
  right-hand lane's walk. Neither playing-lane dimensions nor sockets change.
- Correct the native road modules' outward-facing curb/sidewalk transforms,
  support its yards/verges at their true levels and apply its nominal crown
  height/roll to road cars. No library delivery is changed; these are placement
  corrections and are not represented as independent wheel-contact tests.

All six frames completed when rendered in fresh serial processes. Keep that
batch approach and validate every final receipt and comparison before report.

## Revision pass 10 — full 20-frame attempt, routing and water rejected

**Color/value first.** Opened all twenty 1440 px / 32-sample GLB frames,
including both dusk views and every close-up. Painted fixtures, warm buff rock
and weathered timber hold their color, with dark interiors and unclipped broad
highlights. The supposed green pond is a major failure: a context lawn plane
raised to support the roadside yards covers the water. Cut the entire course
parcel out of that presentation terrain, then independently ray-test the
terrain above the imported water. Do not compensate with a bluer material.
The dusk light pools are too faint; increase the installed flood output and
retain enough dusk sky to read the surrounding ground.

The classic aerial still reads as a gridded installation on one gray sheet.
Reject it. Fan the opposed pairs into angled clusters, use a shared mulched
bed, and connect their outside banks with curved walks selected against the
actual green/border and fixture footprints. Retain every seeded green's
length, width, feature and carpet topology. The compact bed measures 1,221 m²
from its sampled polygon, excluding the perimeter strips. It is denser than
the 1,727 / 2,044 m² full published enclosures; those differing area definitions
are disclosed rather than calling the course parcel a measured play area.
Check 250 seeds of both kinds; classic walks additionally undergo narrow-phase
plan-space strip tests. A castle's broad front and narrow rear keep use their
actual compound footprint, not a full-width rectangle behind the turrets.

The border detail exposes a texture-scale error: each actual brick carries a
miniature masonry wall. Sample a plain clay region for individual border
bricks while retaining the full masonry chart on arches. Smooth the actual
cup-liner rim without adding triangles. Bench legs need a real buried pad;
add it and measure their source-surface contact rather than reporting a
placement constant. Additional native boxwood growth seeds and hydrangeas
fill safe spaces in the shared classic bed; foliage is excluded from greens,
fixtures and the routed walks.

These twenty images remain diagnostic until their corrected replacements and
course-setting photo pairs have been opened and judged. No docs image or
README gallery is generated.

The additional evaluated-source audit found two lane-side walks cutting the
western outcrop and mountain, plus the public upper ledge inside the rock
shell. Route the four inner longitudinal walks outside their greens, connect
them to the circuit and lower crossing, and add framed bank approaches to the
upper crossing. Carve the public stair/ledge's real clearance into the rock.
Check the actual top triangles against all four quarry formations within the
adventure course; do not accidentally compare the co-located classic authoring
scene. Connection selection and green clearance are also exercised on all
250 adventure seeds. These are additional bounded checks, not a general
pedestrian-routing or accessibility certification.

Keep the accepted hole/fixture geometry while recovering site cost: omit
buried walk bottoms, omit the distant fence's 2 mm bevel strips, and reduce
counter-stock balls to the silhouette resolution they need. The native town
and plant placements now have companion `export/Minigolf-*-context.json`
instance recipes; they remain separate from core course geometry and share
library maps. The actual assembled image inventory is counted separately.

## Revision pass 11 — four 1000 px imported-course previews

**Color/value first.** Opened classic above/hero and adventure hero/dusk at
native size. Neutral balancing remains on the cited concrete / castle wall
and shaded white fence ROIs. Carpet keeps a useful green range and fixture
paint has shadow depth. Reject the water's broad alternating silver/blue
stripes: these are regular reflected-sky bands caused by two oversized sine
waves, not evidence for a darker or bluer albedo. Replace them with six crossed
wavelets at shorter wavelengths. The shared mulch bed still reads too smooth
and gray in shade; add original bark-chip color/relief and retain a measured
two-metre UV repeat across clipped bed cells, inside the existing atlas.

The angled classic pairs, shared bed and wraparound walks remove the previous
rectangular lawn plots and gridded paved sheet. The water is finally exposed
in both courses. Reject the classic hero's foreground lamp post, which bisects
the pond: move the camera along the upper bank at the same measured eye height,
keeping 40 mm. The adventure foreground remains too softly shaded to describe
the ledges; use a northwest raking sun that reaches those actual faces rather
than raising their albedo. Keep the improved warm night-play pools and dark
water cavities. Native ranch and cape construction now vary the background
house row; all external family deliveries remain untouched.

The source form checks now pass: four quarry formations against 96 actual
playing/walking top surfaces give zero triangle intersections; six raised
assemblies have girder-to-deck maximum gaps below 1 mm. Both framed bank
approaches have sampled radii above 3.53 m over 250 seeds, preventing the
previous inner-girder fold. These are construction receipts. The revised
ripples, chip scale and camera/light changes still need imported-image judgment.

## Revision pass 12 — four 1100 px imported previews

**Color/value first.** Opened both heroes, waterfall and border at native size.
The crossed ripples break the metallic stripes and the classic bed now reads
as bark mulch. The warm gray timber/brick remain distinct; the border's actual
bricks no longer carry a miniature wall pattern. The north-bank foreground
rock is still too pale and smooth, with weak wet/dry separation compared with
the neutral-balanced used-falls photograph. Reduce the buff rock albedo by
about one fifth, keep its hue, strengthen the flow-localized damp mask and
allocate a wet roughness region inside the same atlas/material. Do not apply
a repeating bottom-edge wet band to a tiled stone texture.

The waterfall close-up exposes too much of the stainless weir bodies. Replace
the rounded spill shelves with broad cast crowns and undercut toes covering
the bodies, leave only thin spill lips, and add actual receiving pool skins.
The drops must land at the next pool's datum, then the main pond's datum.
Retain the total fall height. Recompute rock smoothing on the evaluated mesh
rather than carrying old sharp-edge flags through subdivision/decimation;
retain two-metre stone detail repeats with clipped cells. This spends a few
faces on UV scale rather than another map or material state.

The classic hero is now clear of the lamp pole and shows the water, lighthouse,
clubhouse, price window, plantings and commercial road at the required 40 mm
and measured eye height. Keep its camera. Keep the new adventure raking sun;
the source rock/material corrections above still need fresh GLB judgment.
A front-facing lighthouse camera initialization reduces its photo fit from
28.85 to 11.29 native pixels at 42.4 mm; its complete setting and actual
visibility must still be judged in the rendered pair, not inferred from RMS.

## Revision pass 13 — latest rock/flow close-up, rejected where noted

**Color/value first.** Opened the 1100 px waterfall in `renders/look-pass6/`.
The dry buff and localized wet region separate better, but the curtain is still
too opaque and the foam reads as long white strings. The thin falling sheet
must transmit much more light than the pond's colored depth: give its existing
atlas region a near-neutral clear-water color, retain the shared water state,
and smooth/reduce the curtain's geometric wrinkling. Its upstream-facing
normals are corrected to downstream air and checked on actual source faces.
Break the foam into shorter tapered fragments without increasing its faces.

The large black squiggle on the coping is a UV-scale failure, not a real
fracture. Give the continuous pond coping the same physical stone repeat,
use shorter angular fracture segments and make all stone/mulch fields periodic
inside their eight-texel guards. The camera still lets the raised green hide
the lower fall; move the detail camera to its north side and retain enough
vertical field for all three drops. A separate wider fixed camera contains
both the old and relocated waterfall in their before/after pair.

Correct the course-area comparison as well: the shared-bed outline and an
entire fenced play compound are different quantities. Tighten the adventure
fence around the routed course, move its side benches/lights inside, and keep
the original property/parking dimensions. The final enclosure area is to be
measured from post-mesh centroids, with actual carpet vertices checked inside.
Report both enclosure and routed-bed/window definitions against the published
plans, rather than mixing them. No hole dimensions or fixture triangles change.

The castle annotation audit found a misplaced left roof point and inferred
base points hidden by the photograph's fence. Replace them with four visible
front-gate roof tips/eave centers. The resulting 55.9 mm / 4.39 px fit is a
framing estimate from those explicit features, not a claim that our original
compact gatehouse replicates the photograph's sprawling castle. The lighthouse
front initialization similarly avoids its earlier grazing-view local minimum.
Complete-course visibility still requires the rendered pairs.


## Revision pass 14 — full-size spill close-up, rejected

**Color/value first.** Opened the 1440 px imported waterfall and the used
Henderson falls photograph at native resolution. The tan dry stone has useful
shadow depth, but the falling water is a silver-blue plastic curtain and the
receiving foam is an obvious white square lattice. The camera now exposes all
three drops; that makes these defects impossible to dismiss as distant detail.
The neutral used for the photograph remains its shaded white fence, with mixed
sun/shade exposure explicitly unresolved.

An open transmission plane has no exit interface. Replace it with 1.5 mm
closed liquid ribbons that narrow and wander under acceleration, and lower the
falling-water region's roughness from .12 to .025. Transmission becomes 1 for
the shared water state. Keep the colored-depth pond region. Replace the foam
quad lattice with sparse irregular 1.5–5.5 mm bubble flecks and short trails
attached to the actual ribbons. Build a continuous stepped stone body behind
the existing spill shelves; the empty cut recess made the shelves read as
separate plates. These are corrective changes, not yet visual acceptance.
`renders/look-pass7/waterfall.png` preserves the rejected image locally.


## Revision pass 15 — four 1440 px imported critical views

**Color/value first.** Opened waterfall, clubhouse, road and sign at original
resolution in `renders/lookdev/`, plus the three balanced period photographs.
The liquid film now refracts the stone, and the square foam has gone, but
regular separated streams look like a metal grille. Keep the exit interface
and replace the parallel bands with a continuous film carrying nonparallel
travelling wrinkles. Receiving shelves are unnaturally black rectangles:
use clear falling-water response for their shallow pools, expose only the
25 mm stainless spill lip, and keep their supported stone body. Extend the
physical damp mask up to the top inflow. These changes remain to be judged.

The service view proves siding, supported awning and racks, but the .12
roughness glazing reads as frosted glass. Set clear glazing to .025. Move both
price/menu boards onto the fixed wall rather than occupying the restroom door
bay; carry the restroom label on the actual door. Face the open sash from the
right so stock trays and both boards can be inspected. Canvas stripes must not
carry painted edge chips: two cloth regions fit inside the same atlas.

The actual native station, strip mall, utilities and cars now replace the toy
boxes. The wide road camera spends too much frame on empty lawn; move it to
the roadside. The pylon lettering is visibly stretched and its beige label
blocks disagree with the opal face. Give each business one composed printed
face within the existing 1024 graphics sheet; preserve glyph aspect in other
labels. The original creek emblem becomes a circle rather than a vertical
pill. No new material or image allocation is required.

The rejected waterfall/window/road images are preserved locally under
`renders/look-pass8/`. All four were rendered from exported baked GLBs; the
next source correction invalidates their delivery hashes for final inventory.


## Revision pass 16 — final-size spill/window and landmark audit

**Color/value first.** Opened the corrected 1440 px spill and frontal counter.
The buff stone retains deep undercuts and the flow-localized damp region;
water has finer broken reflections and the dark artificial film border is
removed. The used-falls photograph is still more irregular and aerated than
these engineered continuous weirs. Retain that as a visible look-dev weakness,
not a claim of photographic equivalence. The flat normal-map diagnosis was
measured: the old falling-water chart varied only between 127/128 in red and
green. Its new advected field survives the delivery filter; evaluated film
rim normals are sharpened after the exit-interface modifier.

The frontal counter now exposes the stock and all price/menu lettering.
The real plywood panel carries the boards; the door carries its own label.
The clearance check caught 14 mm intrusion from the new strike casing and
passed after correction to the actual leaf's offset extent. No hidden collision
threshold was relaxed. A literal .025 scalar roughness override also made the
exporter generate another ORM image: move the value into the existing atlas
and enforce sixteen images / 81⅓ MiB. That allocation check now passes.

The first full-course lighthouse pair correctly failed its visibility gate:
hole 6 obscured two lower anchors from the distant pose. A fresh native-size
photo detail also exposed incorrect gallery landmarks: they were inner points,
not the visible deck edges. The gallery was proportionally too wide. Narrow
it, lengthen the lantern/head relative to the shaft and slightly strengthen
the shaft's taper while retaining 4.73 m height, original tunnel footprint and
3,084 triangles. The measured ratios are recorded in REFERENCE. Mark actual
gallery edges and the painted base just above the coping. The unchanged broad
reference crop now solves at 42.37 mm / 4.36 native-pixel RMS, down from 11.29;
complete-course visibility and image judgment remain pending. No geometry is
hidden or rescaled to obtain the fit.


## Revision pass 17 — first course-setting pair and visible curb picks

**Color/value first.** Opened the 1440 px lighthouse comparison image at full
height. White paint, red bands, buff stone and dark cavities separate, but the
native foliage still has a visible card silhouette and the foreground ramp
occupies too much of the frame. Reject this lower-bank image as the final
comparison even though its five anchor rays are clear. Preserve it locally in
`renders/match-pass1/`. No course structure is hidden for its replacement.

A probe of three upper-crossing framings finds a supported player camera
1.824 m above the actual imported deck, with only the finial's own 25 mm
surface ahead of an anchor. Use the central 800 × 1250 pixel crop of the
2007 course photograph, which retains several holes, water and banks. Its
42 mm source lens is fixed for this on-course viewpoint; RMS is 6.58 native
pixels (about .82% of crop width). The full distant framing and the 50 mm
lower-bank version remain rejected. The source lens is not a measured EXIF
value for the reference crop. The actual rendered composition still needs review.

The classic comparison then failed the visibility test. Its four photograph
marks are visibly concrete curb-top corners, as verified in
`build/green-landmark-detail.png`; the old source points lay on carpet below
them. Move the source picks to the actual curb profile (.2774 m authored top,
80 mm stock centerline offset), retaining every hole vertex. The full-course
pose now solves at 36.8 mm / 13.34 native pixels, and all four independent
opaque rays are unobstructed. The castle framing remains 55.9 mm / 4.39 pixels;
its eave picks describe cap-axis/eave-plane centers inferred from the visible
roof outlines, not surveyed masonry points. All are different original designs.

## Revision pass 18 — complete-course photo pairs at delivery resolution

**Color/value first.** Opened all three current imported-GLB PNGs at original
resolution and all three balanced photograph pairs. A sampled bright carpet
region under the earlier northeast light had linear R/G .290 and B/G .480,
against the photograph's .308/.524; its green value was .171 against .371.
The adjacent neutral curb was also too dark. Correct the matched key/sky
balance rather than making another speculative albedo change. The current
pairs have brighter sunlit carpet, white paint and concrete with retained
dark canopy, tunnel and fence shadows. White balance uses the neutrals and
ROIs recorded in `build/reference-balance.json`; photographic exposure and
processing remain unknown. These are approximate matched-light comparisons.

The setting audit caught a sideways parked pickup blocking the classic view.
Parked cars now face their stall headwalk; moving road cars follow opposing
lanes and the native crowned-road slope. Reuse colonial, ranch and cape house
variants behind the course as well as across the commercial road, and extend
the native maple/oak population with younger understory. Small boxwood in the
narrow classic entry beds now fits the actual bed envelope. No canonical
library delivery is regenerated or modified.

The supported upper-crossing lighthouse camera is now accepted as a useful
comparison of the tower and its course setting: 42 mm chosen source lens,
6.58 native-pixel RMS on the declared central reference crop. It is not an
estimate of the photograph's original focal length. The classic fit is
36.8 mm / 13.34 px; the castle is 55.9 mm / 4.39 px. Landmark projection and
core occlusion are checked separately, and the visible context was inspected.
The scenes are original courses, not reconstructions of those photographed:
the classic foreground has more lawn, the lighthouse crop has different water
and hole routing, and the six-metre castle keep is substantially less elaborate
than the sprawling reference. Small residuals do not erase those differences.

Remaining visible CG tells: foliage cards and repeated crown character;
buff rock's broad smooth ledges and repeated surface field; the quiet,
engineered waterfall; sparse ground litter and limited hand-placed garden
irregularity; and the castle's restrained silhouette. The source-built native
town provides real construction at distance, but its house/commercial scalar
finishes are weaker than the course's baked material treatment. Keep these
limitations visible in the checkpoint report.

## Revision pass 19 — final course views, day and dusk

**Color/value first.** Opened all eight final ground/above/hero/dusk PNGs at
their original 1440-pixel width. Compared paint, carpet, foliage and masonry
with the balanced in-season pairs inspected in pass 18. Sunlit white paint
remains below clipping, while cavities, the pond under the bridge and canopy
shadows retain real darkness. Display-luma 1st/50th/99th percentiles are
.006/.288/.892 classic hero and .003/.432/.947 adventure hero. All-channel
white clipping is .000386% and zero, respectively. Dusk clipping is .0303% /
.0232%, localized to operating light sources. These are rendered display
statistics, not material reflectance measurements.

The classic overview proves common beds, angled opposed hole pairs and
connected walks. Adventure ground/above views prove the stair, upper ledge,
sloping banks and two supported water crossings. Both heroes use the imported
GLB and baked textures at an actually measured 1.65 m eye height, with 40/35 mm
lenses. Their receipts distinguish that support measurement from a requested
camera constant. The commercial strip, native cars and clubhouse are visible
across the water; night-play lamps operate in both dusk views.

The adventure hero still gives too much visual weight to the foreground
rock/pier/water rather than the sequence of greens. The central water has a
coarse reflected ripple pattern. Classic coping remains smooth and regular
despite the improved continuous construction, and distant foliage retains
card silhouettes. The course grounds are tidier and less botanically complex
than the period photos. These images are a substantial form/look improvement,
but they are not yet difficult to distinguish from photographs.


## Revision pass 20 — cup-scale nap aliasing, corrected before acceptance

**Color/value first.** Opened the delivered cup, border and waterfall close-ups
at full size. Carpet hue is consistent with the matched season photos, but
the cup view exposes broad normal-map lumps rather than a flat, fibrous mat.
A 5.2 mm tuft is below the delivered lane chart's reliable Nyquist limit.
Keeping the physical pile-height variation in that chart produces false
centimetre-scale shading after filtering. Reduce only its effective normal
relief (.23/.15 loop/noise amplitudes to .035/.018) in the same original field.
Do not invent larger tufts or add texture allocation. Preserve the traffic
flattening, seams, patch, causal vertex tint and every mesh vertex.
The height-derived micro-occlusion also becomes quieter; BaseColor and
roughness are unchanged.

The full render run is stopped after its active frame; no other worker is
interrupted. The revised 4096 bake, 2048 filter, byte-repeat check and final
image inventory must be rerun before acceptance. Earlier final-size images
are useful rejection evidence, but their old GLB hashes are not current proof.
The engineered waterfall remains regular and quiet compared with the used
Henderson reference; that limitation is retained.

The corrected cup render removes the false broad lumps; individual fibers
remain unresolved at the shared lane-chart density. The strict full repeat
then exposes small GPU emission-resampling differences in BaseColor and ORM;
the normal repeats exactly. Keep the byte assertion. Validate those flat
emission bakes against their original fields, then use exact authored
color/ORM pixels for CPU delivery filtering. Preserve the GPU physical normal
bake. `finish_bake.py` records the measured errors and source hashes; TEXTURES
describes this distinction explicitly. The failed receipt is retained in
`build/repeat-gpu-emission-failed.log`, rather than relabelled as a pass.


The next strict repeat isolated one delivered normal channel at pixel
(1294,1280), changing from 129 to 128, plus one earlier parallel mesh-buffer
mismatch. A separate cached mesh rebuild repeated both buffers byte-for-byte.
To remove hardware resampling from the authoritative textures, evaluate
float64 symmetric derivatives of the original height field at the same
eight-metre / .018 m calibration, and retain the GPU bake as an independent
polarity/footprint check. Mean angular difference is 2.79°, with 95% below
9.91°; the sampling kernels are different, not claimed pixel-equivalent.
Source color/ORM remain exact original pixels. Mesh evaluation/export now
uses one CPU thread. The strict 22-file assertion is unchanged; failed logs
remain in `build/repeat-normal-failed.log`. Fresh visual and repeat acceptance
is still required below.


## Revision pass 21 — frozen exported fields and complete course views

**Color/value first.** Opened all 22 final GLB course PNGs at original 1440 px
width, all three current game/photo PNGs and their balanced reference pairs,
and the balanced ten-month-old Henderson falls photograph. White paint,
carpet hues, buff stone and dark cavities remain distinct. Final display-luma
1st/50th/99th percentiles are .00646/.28821/.89223 classic hero and
.00309/.43188/.94735 adventure hero. All-channel white clipping is .000386%
and zero. Dusk clipping is .0304%/.0235%, at operating emitters. These are
whole-frame display statistics, not measured albedo.

The cup no longer has false broad nap lumps. Fibers remain unresolved at the
shared lane-chart density, and the extreme macro exposes rim segmentation.
Seams, patches, traffic fade and fixture paint failure survive in the delivered
images. The waterfall retains wet/dry contrast, but its broad rock bands and
quiet engineered weirs remain much more regular than the photograph. The high
inspection sun exposes the shoreline and supporting piers; deep bridge shade
still weakens the visibility of submerged balls and edge debris.

The windmill view includes an actually measured 1.8 m silhouette, sided tower,
framed windows, stocks, bars and boards. The lighthouse has a masonry tunnel
base, glazed lantern and gallery. The six-metre keep is now course-scale, but
its silhouette is substantially simpler than the sprawling reference castle.
The service-window view shows the open sash, price/menu lettering, putter
racks, ball stock, restroom leaf and counter light. Native house/commercial
construction supplies the roadside setting; its source-scalar finishes remain
weaker than the course materials. Foliage cards, repeated crowns, tidy beds
and repeated rock/paint fields still disclose CG. The adventure hero gives
too much weight to foreground rock, pier and water. No photographic
equivalence is claimed.

The reference pairs now have complete course settings and explicit homologous
landmarks: lighthouse 6.58 native px on the declared central crop at a chosen
fixed 42 mm source lens; classic curb 13.34 px at 36.8 mm; castle 4.39 px at
55.9 mm. The lighthouse lens is not inferred reference EXIF. The castle eave
centers are inferred from roof outlines. Different routes, foreground lawn
coverage, architecture and planting remain visible; these residuals describe
landmark framing, not a reconstruction of the photographed place.

A final context audit found the hard-coded 10.4 m roadside conductors missing
the native hardware, with crossarms parallel to the road. Turn the native
poles across the road and use their transformed primary/neutral sockets,
native catenary sampler and cable diameters. The resulting seven poles and
24 spans record actual mesh end-ring centroid errors in the companion JSON.
That checks attachment coordinates; the native builder defines the seat
surfaces. No course mesh, image allocation or protected delivery changes.

The complete strict regeneration now passes all 22 delivery-file hashes and
four original-field hashes, including GPU validation, deterministic field
evaluation, filtering and serial mesh export. No equality threshold was
relaxed. Final source-field and before/after image acceptance follows below.

Opened the three 4096-field PNGs and their photograph pairs at original size.
Compared with the same imported geometry, camera, lighting and fixed seed at
2048, their whole-frame mean absolute display-RGB differences are .000457
(classic green), .002409 (lighthouse) and .000827 (castle); 95th percentiles
are one, two and one 8-bit code values. Unchanged native context occupies much
of each frame, so these are descriptive frame statistics, not a masked
material-error bound. Filtering softens fine relief, but the paint failure,
traffic fade, seams and stone strata survive. No high-poly projection loss is
claimed measured: both versions use identical geometry and original fields.
The source pairs retain the same visible setting/design differences described
above; the source resolution does not make them photographic.

Opened all 26 final before/after PNGs at original resolution, all 13 assembled
pairs, and the four final contact sheets. The actual final PNG hashes in the
local viewing ledger cover all 54 frames without an unseen current image.
The two overviews show common planted beds and curved routes; the adventure
ground views show the water crossings, raised greens, retaining rock, quarry
steps and guards. The form change is substantial, although the overview still
exposes a regular outer circuit and the foreground supports dominate the
adventure hero. The pond inspection confirms the free-form edge and concealed
liner; the dark water still prevents a strong debris/ball read. The fixture
pairs expose the sided windmill, supported lighthouse and enlarged keep
without disguising the simpler castle silhouette. The clubhouse, road and
pylon comparisons confirm the functional counter and library-based setting.
All before/after cameras match exactly in their receipts. The three fixture
before frames stage old geometry at the revised placement, explicitly labeled;
the other before frames import the complete accepted baseline course.

| Requested correction | Full-size local comparison |
| --- | --- |
| 1. Routing, packing and grade | `renders/comparison/classic-above-pair.jpg`, `adventure-above-pair.jpg`, `hero-pair.jpg`, `terrain-pair.jpg` |
| 2. Continuous rock and ledged waterfall | `renders/comparison/waterfall-pair.jpg` |
| 3. Free-form pond and shelves | `renders/comparison/pond-pair.jpg` |
| 4. Readable playing breaks | `renders/comparison/terrain-pair.jpg`; `renders/lookdev/bank.png` |
| 5. Constructed course fixtures | `renders/comparison/fixture-pair.jpg`, `lighthouse-pair.jpg`, `castle-pair.jpg` |
| 6. Roadside service building | `renders/comparison/clubhouse-pair.jpg` |
| 7. Library town and lit pylon | `renders/comparison/road-pair.jpg`, `sign-pair.jpg` |
| 8. Planted species, sizes and seeds | `renders/comparison/planting-pair.jpg` |
| 9. Framed course-setting photo pairs | `renders/look-matches/period_{classic_green,lighthouse,castle}-pair.jpg`; corresponding 4096-field pairs in `renders/source-matches/` |

Final proof: `make WIDTH=1440 SAMPLES=32` exits zero, including the construction,
UV/normal/tangent/memory, 250-seed-per-kind, repository and preservation gates,
then the complete serial locked Cycles inventory. `make repeat` exits zero:
22 delivery files and four original fields repeat byte-for-byte after fresh
generation and GPU validation. `make review` accepts 22 GLB views, three
delivery/photo pairs, three source-field/photo pairs and 13 same-camera pairs.
The independent repository check reports 1,836 source files and zero errors;
preservation reports 208 unchanged files. Local receipts are
`build/final-all-physical.log`, `repeat-final.log`, `repeat.json`,
`render-check.json`, `tonal-review.json`, `field-filter-review.json`,
`check.json`, `look-check.json`, `routing.json` and `preservation.json`.

This is the requested look-dev checkpoint, not final photographic acceptance.
The weakest remaining cues are smooth/repeated rock strata, quiet regular
weirs, dark shaded water, unresolved carpet fibers, cup-rim macro segmentation,
foliage cards/repeated crowns, tidy planting and scalar-finish background
buildings. No docs image or README gallery is added. No kit code changes.
A future general kit addition could make deterministic height-derived delivery
normals and their independent GPU validation a documented shared operation;
this family keeps that implementation local for this checkpoint.
