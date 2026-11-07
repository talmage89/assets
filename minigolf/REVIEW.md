# Miniature golf — construction checkpoint critique

This is the form gate. Quick swatches and original diagnostic graphics are
exported; manufactured materials, final normals, seams/patch wear, repainted
chips, wet mineral/algae masks and final docs are deferred as requested.
Photographs never enter a material or supply a vertex.

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
