# Sedan form round 5 — rear glazing, bumper construction and mirrors

## Pass 1 — reject the proxies and diagnose the lower surfaces

Compared the first, second, fourth, sixth and seventh source candidates with
both rear class photographs, both front photographs and the Camry profile.
The inspected clay images are in `renders/sedan-round5-pass1`, `pass2`, `pass4`,
`pass6` and `pass7` (each directory carries the `sedan-round5-` prefix).
These are rejected/intermediate evidence, not the final checkpoint revision.

Color/value first: the white studio backdrop is the photographic neutral,
with unit RGB gains. Black Camry and silver Accord paint cannot be compared
as albedos with neutral clay. Review form, value gradients and cavity depth;
final optical response, paint and wear remain outside this source gate.

- **Backlight and sails:** narrowing the glass on the existing canopy makes
  painted sail panels instead of thin hatchback posts. The first measured
  top/base widths are 1211/1268 mm, against photographic estimates of
  1316/1347 mm Camry and 1202/1061 mm Accord (glass estimates ±80 mm).
  Near-side transverse sail estimates are 243/258 mm, versus about 256 mm
  on the source. All photographic picks, camera rays and the assumed glass
  plane are exposed in the annotated images and JSON; these are not OEM
  glass dimensions. The straight glass side boundaries still read CG.
- **Tail and hips:** the larger corner lenses measure about 142 mm tall and
  taper to 17–18 mm forward. Their dark optical blanks still lack a lamp
  graphic. Reject the residual quarter hollow and the abrupt return behind
  the arch. Continue the rear die swell farther aft without changing its
  peak over the axle or the three accepted door sections.
- **Bumper and diffuser:** the arched parting line helps the elevation, but
  the first lower edge still reads like a plate. Rays identify the apparent
  gray bar as the opposite front chin visible through the incomplete
  underbody. Reject the rectangular blackout-box experiment too: roll the
  rear closure forward, with lifted ends. The well's projected grid perimeter
  can fold even when its lens/bed chart disk is valid; loft the same convex
  chart boundary used for the skin cut. Flat reflector boxes intersect the
  curved molding: replace them with conforming strips inside the black panel.
- **Plate:** the new 317 × 169 mm mouth is crisp, but the un-tilted plate
  intersects the sloping pocket bed. Tilting it still leaves one black
  triangle: a ray identifies the bed 0.3 mm ahead of the plate. Set the real
  304.8 × 152.4 mm blank ahead of the whole bed plane while retaining the
  requested 20–30 mm recess, and tuck its lamp below the brow.
- **Front corners:** tapering the pockets removes the square blocks. Keep
  the accepted lamps, grille and crowns. The impact band and bottom require
  different corrections: retain the class length, flatten the overly bowed
  lower waterlines, and restrict the underturn to the final lower band.
  Small simple pockets and parallel bars still look cheaper than the photos.
- **Mirrors:** the lowered 243 × 120 × 148 mm wedges have flat aft glass,
  a rounded forward cap and a supported door-corner arm. They are visible
  from both quarters and no longer make a ball above the cowl. Their coarse
  cap transitions and unarticulated stalk remain source-stage simplifications.
- **Overlay:** retain the original orthographic comparison. Also register
  a perspective source using six wheel anchors and explicit 80 mm lens /
  1.25 m height priors: estimated 82.3 mm, RMS 2.02 native pixels. A single
  near-wheel plane cannot recover focal length uniquely; render 60/100 mm
  prior sensitivity as well. Do not call the nominal camera a measured lens.
  Seventh-candidate held-out lower-end differences are −34 to +20 mm front
  and −32 to −27 mm rear. The upper C-pillar remains low in this camera;
  retain the accepted deck and lift the C-pillar's descending controls.
- **Topology/budget:** reject the 56k allocations, aperture slivers and
  non-manifold bridges. A broad coplanar dissolve can encode multiple holes
  with repeated-vertex polygons. Keep convex cut fragments, collapse only
  sub-50-micron cut crumbs, and reduce hidden gauge backs with local depth
  and manifold-link checks while locking the outer skin and cut rims.

## Pass 2 — fresh-session rebuild and reject the diffuser scars

Color/value first: compared the new source against the same four stock photos,
balanced on their white backdrops with unit gains. Neutral clay still has dark
optical blanks and wells; silver/black photographic paint is not its albedo
target. Opened the fresh front/rear/side/top Workbench views, both Cycles
three-quarters and the profile overlay in `renders/sedan-round5-handoff/` and
`sedan-round5-handoff-wb/`. All intermediate diagnostic views stay ignored.

- **Glass and sails:** retain the narrower backlight and the painted widening
  sails, on the existing canopy. Both photographed rear glasses and their
  annotated picks support this change. Their straight source-stage side
  boundaries still look more regular than either photograph.
- **Tail and diffuser:** reject the remaining triangular dents along the
  diffuser's top edge. Removing cavity shading and gauge backs does not cure
  them. Sampling normals directly from the dense parent removes the broad
  false triangular highlights introduced by re-interpolating the coarse game
  field. The two surviving corner scars expose a hard 370 mm switch in the
  control-net fitting frame. Replace that switch with smooth vertical and
  longitudinal blends before subdivision; no painted patch or replacement
  shading field is used to conceal it.
- **Deck:** the fresh build's measured kick is only 14.5 mm, below the held
  15–30 mm range. Increase the actual lip control and move its crest slightly
  aft, retaining the integrated deck and the original canopy silhouette.
- **Plate and tail lamps:** the plate sits in a crisp small pocket with a
  supported lamp above it. The thicker tapered wings are a useful class
  correction; their black blanks still lack optical graphics. Retain the
  actual apertures and corner wrap rather than adding surface decals.
- **Front corners:** the tapered, curved pockets are less block-like than the
  round-4 boxes. Keep the accepted lamp/grille/crown layout. The simple bars
  and unarticulated pockets remain plainer than both production references.
- **Mirrors:** keep the door-corner wedges and flat rear panes. Their lower
  position removes the cowl bump in the overlay; their caps and arms remain
  unusually simple beside both photos.
- **Profile:** lower-end holdouts on the 80 mm-prior perspective registration
  are within about 33 mm. The six wheel anchors do not measure a unique lens:
  keep the raw orthographic overlay and both lens-prior sensitivity views.
  The accepted C-pillar is lower in the new camera than in the raw overlay;
  do not move the accepted roof to conceal a camera-dependent difference.

The new Blender patch version also changes the pickup exporter's version text
from `v5.2.40` to `v5.2.41`. Fresh default pickup generation retains all 454
meshes exactly; all 150 re-exported accessors, embedded maps, hierarchy and
the entire binary chunk are identical. The accepted GLB is untouched. A fresh
export's complete file hash differs only because of that generator label;
complete byte identity is not claimed for that re-export.

## Pass 3 — reject the straight lower edge after the complete comparison

Color/value first: the completed white clay has deep cavities and unclipped
highlights (front/rear foreground p99 about 238/225). The four neutral pairs
still use the photographs' white backdrops as the balance neutral, not their
paint. Opened both full-size heroes, all four neutral pairs, the orthographic
rear and the raking side of the first complete fresh-session build.

The diffuser's painted rim is now clean and the quarter's old dark hollow has
gone. But the rear elevation still carries a straight bottom and rectangular
black insert. The photographs' lower corners roll upward into their quarters.
Lift the source cage's lowest rear corner controls and the diffuser's lower
boundary, leaving the centerline, accepted side sections, top crease and
quarter shoulders intact. Do this before subdivision, not by reshaping the
finished game panels. The upper fascia and the plate/optical blanks remain
visibly plainer than either production car; this remains a form checkpoint.

The complete overlay set exposes a material limitation: the 80 mm-prior
perspective source has a 33 mm worst lower-end residual, while 60/100 mm
priors give 59/47 mm. The raw orthographic comparison is still about 119 mm
front / 76 mm rear. No unique photographic lens was recovered. Preserve all
four overlays and report these misses; the nominal perspective view alone
does not prove the original 40 mm overlay request.

## Pass 4 — whole car in white clay, final source checkpoint

Color/value first against all four final neutral and striped photo pairs:
the stock photos' white studio backgrounds are the balance neutral, with unit
RGB gains. Front/rear white-clay foreground p1/p50/p99 luma is 1/153/238 and
0/145/225; no opaque foreground channel reaches 255. Cavities remain dark.
This is form inspection, not paint/albedo or used-car wear validation.

Opened every final JPG, including the parent plots, in
`build/sedan-round5/final-reviewed-00.jpg` through `final-reviewed-15.jpg`.
The white-clay heroes, rear elevation, raking side, main stripes and neutral
pairs were also inspected at full size. The 42-view contact is
`renders/sedan-round5/contact.jpg`; all 25 rendered views record the same
current game-source hash.

- **Backlight/C-pillars:** the 1211 mm top / 1268 mm base glass now leaves
  sails about 252–253 mm wide near the beltline. Against the Camry's estimated
  1316/1347 mm glass and 243 mm sail, and Accord's 1202/1061 mm and 258 mm,
  the original breadth is a class interpolation. Photo uncertainties are
  ±80/60 mm; no OEM glass drawing is claimed. The rear no longer has the
  former almost-full-width glass. Straight window side boundaries and the
  regular greenhouse corners remain more synthetic than either photograph.
- **Tail/hips:** the quarter's old dark dent is gone in raking clay. The rear
  plan stays convex; the same three rays at z=570 mm measure a 305.5 mm local
  circle. The clean bumper turns under 44.8 mm over the tested lower 150 mm;
  its painted lower edge rises from 219 mm on center to 239 mm at x=800 mm.
  The lifted diffuser boundary and flush reflector blanks remove the old
  protruding-plate and crumpled-rim read. A rolled finisher has a real dark
  bore. The broad unadorned painted land is still plainer than both photos.
- **Lamps/plate/deck:** rear wings stand 153–155 mm tall at the corner, wrap
  445–446 mm along the quarters and taper to 25–27 mm forward. The plate mouth
  measures 320.1 × 170.5 mm; actual plate edges are 304.8 × 152.4 mm. A ray
  along the actual tilted plate normal measures a 26.4 mm recess, with the
  lamp tucked above. The integrated lip's kick is 25.8 mm and deck length
  362.4 mm. The optical blanks remain intentionally unresolved; dark shapes
  alone are less legible than the photos' lens graphics.
- **Mirrors/front corners:** 243 × 120 × 148 mm rounded wedges, 2104.6 mm
  across, have flat aft panes. Bottoms are 916.7 mm high; arms begin behind
  the A-pillar on the front upper door. Actual housing vertices stay below
  the same-Y canopy silhouette. They read as supported mirrors in both
  quarters, though their caps and arms are still coarse. The tapered corner
  pockets now follow the front turn. Simple grille bars and the lower front
  door/sill highlight junction remain cheaper-looking than both references.
- **Whole car/accepted forms:** the unchanged wheelbase, tracks, loaded tires
  and 40 mm arch gaps keep the low stance. Door sections retain their crown,
  die hollow and sill tuck. Direct dense-parent normals improve the cut rims
  without replacing the surface. Fine grazing waviness remains around the
  arch/sill joins; the fender crown still fades too early near the A-pillar.
- **Overlay:** nominal perspective lower ends remain within 32.9 mm, but
  the 60/100 mm prior cases reach 58.8/46.5 mm. The raw orthographic overlay
  still misses by 118.8 mm front / 75.9 mm rear. Raw C-pillar/deck are
  −32.9/−35.3 mm; the nominal perspective C-pillar is −75.3 mm. These are
  openly retained camera-dependent misses, with ±16.5 mm pick uncertainty.
  The original 40 mm overlay request is not certified by the new camera.

Proof: `make -C cars BODY=sedan WIDTH=1600 SAMPLES=40` and `make -C cars
BODY=sedan check fairness` pass. Both density audits are closed, positive,
within their configured envelopes, and free of zero-area triangles or invalid
normals. All regional form/recess/clearance rays, current numeric ranges,
parent/game curvature and independent camera projections pass. Superseded
round-2 tuck targets are retained separately as misses, not silently passed.
The control net remains one connected sheet with 124,032 quads and valence
four inside. Game/high sources are 51,296 / 114,684 triangles; five diagnostic
materials, zero maps; blends 1,181,792 / 2,407,933 bytes, ignored.

Independent one-thread generation matches all 120 meshes' geometry, corner
normals, materials, transforms and hierarchy exactly. Pickup preservation is
as documented in pass 2: source, every accessor/map/graph and the entire binary
payload match; only a fresh exporter's generator label changes. No kit changes,
sedan GLB, baked textures or committed checkpoint images. Interior, underbody
detail, optics, real paint/wear, UVs and motion clearance remain later work.
Nothing additional is needed from the lead beyond this requested form review.

# Sedan form round 4 — character and construction

This is the requested source form checkpoint. No sedan delivery, optics,
interior, paint, wear, UV, bake or motion approval is implied. The accepted
pickup generator and delivery branch remain independent.

## Pass 1 — reject a dressed-up flat tail and thin lamps

Color/value first: the four manufacturer-class stock photos use the white
studio background as the neutral (unit RGB gains). Silver and black paint
are not clay-albedo targets. Opened the four raw photos, the previous round's
handoff images, every new clay/stripe preview and all four calibrated neutral
pairs in `renders/sedan-r4-pass2/`. Earlier lighting/allocation experiments
are in `sedan-r4-pass1/` and `sedan-r4-pass1c/`. Cycles lighting initially
washed out the clay and reflected a white card over the whole windshield;
reject that presentation, lower the exposure and suppress the diagnostic
opaque window's specular response. No paint-match claim.

- **Side:** the broad wall is now a crown, and there is a clear shoulder-to-
  sill gradient. The low die hollow/crease is still too broad: a 36 mm normal
  interval turns only about 3.5–5.5 degrees. The actual front lower door is
  about 87 mm inside its shoulder, beyond the requested 50–80 mm. The three
  section rays are stricter evidence than the brighter door highlight.
- **Front:** the blank painted wall has gone; the upper grille, lower intake
  and corner pockets are real skin cuts with inward returns. Reject the
  headlamp's doubled-back guide near x=840 mm: its inflated 803 mm path is
  not a long, fair lamp. Correct that guide and keep the outer tip rising.
  The fender ridge is too low in two sections (5–10 mm), and the hood's
  corners still look too busy. The narrow central opening/bar treatment is
  more resolved than round 3 but remains generic beside both production cars.
- **Rear:** the raised deck helps the profile but the lip still reads too
  shelf-like at its ends. Lamp outlines are rectangular in rear projection;
  the dark form blank cannot stand in for the eventual original optic graphic.
  The plate pocket adds depth, but the lower painted expanse is too plain.
  Move the bumper top to 620 mm and keep the diffuser inside the molding.
- **Stripes:** broad doors are smoother and carry a real gradient. Reject the
  remaining lower-rear tooth. Extra samples from round 3 were concentrated at
  the side tangent, rather than the tighter front/rear plan turn. Fit a finer
  regular control net before subdivision, and place game samples at the turn.
  Keep the same procedural reflection-band diagnostic; do not hide the tooth
  with material roughness or a different light pattern.
- **Mirrors/package:** both mirrors are now visible and supported by stalks.
  Their oval housings still look like form proxies. The accepted tires,
  tracks, arch gaps, roof peak, rake and tumblehome remain the package basis.

Actions: support the lower die line before the long sill return; shorten its
broad transition; retain a slight concave run; reduce hidden well/liner
allocation to fund the silhouette. Raise the fender crown, remove the lamp
backtracking, and check the same actual end numbers again. The first 61k
allocation and the 55,418-triangle support experiment are rejected. No budget
limit has been raised.

## Pass 2 — final character, with the remaining misses explicit

Color/value first against all four final Camry/Accord clay and striped pairs:
the photographic white studio backdrops remain the neutral, with unit RGB
gains. Neutral clay is not a paint-albedo match to the silver Accord or black
Camry. Cycles hero foreground p1/p99 luma is
0/238 front and
0/225 rear; no opaque foreground channel reaches 255.
Cavities remain deep, and the raking side retains a shoulder-to-sill gradient.
Opened every final view in the 37-view contact, all eight paired comparisons,
the sections and curvature plots; front/rear clay and key pairs were also
opened at full size. Rejected intermediate views are retained in the six
`build/sedan-round4/all-intermediates-*.jpg` review pages.

- **Side:** actual mid-front-door / B / mid-rear-door shoulders are 910 / 921 /
  932 mm high. Upper inward lean is 20.2–21.2 degrees; lower lean progresses
  from 4.6 just below the shoulder to 16.3 / 15.3 / 13.1 degrees low on the door.
  Lower-edge insets are 80.4 / 75.0 / 70.1 mm, then 40.9 / 45.4 / 49.7 mm
  more sill tuck. The soft crease turns 11.2 / 10.7 / 9.7 degrees over the
  recorded 80 mm interval; 50 mm chords find 1.7–1.8 mm inward hollows. These
  sections replace the broad chord that incorrectly called the old wall fair.
  The low line and shoulder now carry separate value bands. A small abrupt
  grazing-band change at the front lower-door/sill junction still reads CG.
- **Fenders:** same-height wheel/door rays measure 33.3 / 28.2 mm swells.
  Crown rises are 19.0 and 14.8 mm behind the lamp, but only 3.9 mm close to
  the A-pillar (y=−1.10 m). That last crown blend still misses 10–30 mm and
  weakens the hood's recess there. It is printed in the report, not gated away
  by selecting only the successful stations.
- **Face:** the grille, lower intake and corner pockets are actual openings,
  with inward returns and broad original blades. Mouth-to-bed rays measure
  64–67 / 60–62 / 50–52 mm; eighteen separate axial rays find no painted skin
  across their centers (including the rear pockets). The rising headlamp
  paths are monotone at 746 mm, about 110 mm tall, with 268–292 mm returns.
  The top follows the shut-line arc, and the fender ridge separates from the
  hood. The simple parallel bars and small regular corner pockets still look
  generic and cheaper than both photographed production faces. Optical
  internals and their lit response remain later work.
- **Rear:** the tapered wings now extend across the lid cut and corner rather
  than two rectangles. The deck is 366 mm long; its crest is 1111 mm, with a
  measured 21.3 mm kick over the extrapolated adjacent deck. All fixed tail
  and quarter areas retain the same parent; there is no separate tail patch.
  The 303.4 mm local plan circle retains the approximately 305 mm draw. The
  lower fascia seam is at 620 mm, and the molded diffuser is 11–14 mm behind
  its mouth, within the fascia outline. The broad painted bumper remains too
  plain beside both photos. The last rear clay revealed that the old temporary
  cavity closure, not the recessed diffuser bed, still projected as a flat
  plate underneath. Its box is now inboard of the wheel wells and forward of
  the tucked tail, with 127.5 mm actual axial tire clearance.
- **Profile/overlay:** the first final candidate still missed the C-pillar by
  111 mm even though its deck had risen. Reject that partial correction and
  raise the C-pillar control stations themselves. Final held-out deviations
  are −32.9 mm C-pillar and −35.3 mm deck; every recorded upper silhouette
  holdout is within 35.3 mm, with ±16.5 mm pick uncertainty. The lower-end
  request is not met: bumper tangents are +132.9 mm nose / +78.2 mm tail in
  the unchanged wheel-center-only orthographic overlay. Lower nose/chin are
  +41.2 / +25.9 mm; lower tail/under-tail +41.2 / +2.9 mm. The accepted 4900 mm
  envelope and 975 / 1095 mm overhangs remain held. Near-profile perspective
  is an uncertainty; it is not used as a pass flag, nor is the outline fitted
  or warped to hide the miss.
- **Stripes/fairness:** refining only the plan tangent did not remove the
  lower-rear tooth. Screen rays identified it on actual fascia around y=1.9 m,
  forward of that region. Local game-chart refinement in both directions
  removes the large zigzag while coarser central-canopy chords fund it. The
  front's painted corner bands are more coherent after the real cut openings.
  Fine grazing waviness remains at the lower rear; this is not a global
  Class A claim. Both parent and game checks retain every raw sign crossing.
  Documented zones cover the die hollow, rocker/shoulder, fender-crown/hood
  transition and lower fascia roll, including the parent's z=371 mm roll.
  None of those plots is substituted for the photographic/stripe critique.
- **Mirrors/greenhouse:** 250 × 204 × 157 mm housings span 2110 mm and are now
  visible in front and rear three-quarters. Stalks seat on the front doors.
  The oval caps/panes and regular window corners remain obvious form proxies.
  The six-light layout, roof peak, windshield rake, tumblehome, tires, tracks
  and 40 mm arch gaps remain the held package.

The original grid projection at the tapered rear-lamp tips produced tiny folded
cells and non-manifold six-face edges. A 0.1 mm weld was insufficient. Replace
the optical blank topology with a constrained triangulation in the continuous
parent chart before gauge closing. Both source densities then pass closed,
positive-volume audits. This is a construction fix, not a loosened audit.
Recess normals also exclude flat gauge rims: their tangent normals initially
gave an invalid negative diffuser-depth result. Independent outward smooth
skin normals give the 11–14 mm bed recess; separate rays still prove the holes.

Final proof: `make -C cars BODY=sedan WIDTH=1600 SAMPLES=40`, `make -C cars
BODY=sedan check` and `make -C cars BODY=sedan fairness` pass. Actual game source
is **52,628 triangles**, with five diagnostic clay materials and zero
image textures. Both densities, real openings/depths, end ranges, sections,
source scale/normals, calibrated camera projection and repository checks pass.
There are 22 rendered views with one source hash and a 37-view contact at
`renders/sedan-round4/contact.jpg`. The final two source blends and all generated
images remain ignored; no checkpoint docs JPGs are committed.

Independent one-thread regeneration matches all 112 meshes' positions,
polygons, corner normals, transforms, materials and parents exactly. Fresh
pickup generation matches all 454 meshes; all 150 re-exported accessors,
embedded maps and graph match, and the complete 11,530,736-byte GLB retains
SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
This last check proves serialization/byte preservation; the sedan rays and
closed-surface tests prove its source construction. Full mechanical clearance,
UV/bake, finish/wear and sedan GLB validation remain deferred. No kit changes.

The most important remaining issue for the next form decision is the raw
lower-bumper overlay miss while keeping the accepted envelope/tangents. The
near-A-pillar crown, plain fascia lands, mirror proxies and fine grazing bands
also remain weaker than desired. This checkpoint stops here.


# Sedan form round 3 — one fair parent

This source checkpoint supersedes round 2's surface judgement. The earlier
claim that its broad stripes were fair was too lenient: the hood pooled,
fascia corners zigzagged, and the rear still read as a box. Its measured end
numbers and accepted package remain targets, not evidence of fairness.
No sedan delivery, material, wear or motion approval is implied here.

## Pass 1 — reject the first pole-free sheet

Color/value first against the silver Accord front, black Camry rear and Camry
profile: neutral gray clay must retain dark glass, wells and intake locators.
The stock photographs' white backgrounds are the balance neutral, with unit
RGB gains. Their silver/black paint is not treated as the clay's albedo.
Opened the three rejected round-2 stripe images and rear clay at full size,
the raw photographs, and the complete first replacement views.

Evidence: `renders/sedan-r3-pass1/`, `sedan-r3-pass2/`, `sedan-r3-pass4/`
and `build/sedan-round3/all-previews-0.jpg` through `all-previews-3.jpg`.
The sheets include every rendered intermediate, not selected successes.

- **Package/stance:** the envelope, wheelbase, tracks, 235/45R18 rolling
  envelope and 40 mm arch gaps remain fixed. Early mesh bounds show that
  subdivision rounding can still lose millimeters; recipe constants are not
  reported as measured geometry.
- **Hood:** removing post-subdivision end projection immediately improves the
  broad crown. The first edge/corner distribution still produces a false
  ridge and a knot where the fascia rows enter the fender. Reject it.
- **Front:** a single rectangular sheet can fold over the nose without cap
  poles, but nearly parallel longitudinal and cross rows create an unstable
  chart near the corner. Its bands still change direction abruptly.
- **Doors:** the requested concave run below the widest shoulder is present,
  but game reduction and changing row spacing leave waves. A few broad bright
  bands do not excuse those waves.
- **Rear/deck:** the first corner tangent lies too far aft; measured rear plan
  sweep is only about 70 mm. The deck still meets an almost flat tail face.
  There is a visible pinched transition at the quarter's top.
- **Canopy/wheels:** the accepted side profile/rake and wheel package should
  not be altered to rescue the ends. Their plain glazing and wheels are form
  proxies; they cannot conceal a wrong stamping.

Action: fit one continuous waterline/cover section family to the **control
net**, before final Catmull-Clark evaluation. Spread the end-to-side chart
through the quarters and retain a regular quad sheet. No evaluated vertex
projection, separate end volume, cap grid or analytic replacement normal is
used. The exported game-stage normals come from the evaluated parent itself.

## Pass 2 — reject collapsed reflections and damaged boundaries

Color/value first: striped diagnostics use a neutral substrate and procedural
black/white latitude or azimuth bands. Keep the deep values and highlight
rolloff; do not brighten the clay to imitate the silver photograph. Viewed
all pass-5 through pass-13 renders in their sheets, with the significant hood,
front/rear stripe and plan views also opened individually against both makes.

- **Hood/front:** a fair shallow crown and supported paired draw lines remove
  the leading dent. Piecewise fascia controls still concentrate curvature at
  their joins. Replace them with smooth positive-curvature center sections;
  the accepted height, rake, tuck and plan measurements still have to pass.
- **Side/arches:** the broad swells now read over each wheel. QEM reduction
  treats a shallow door as almost planar and removes the vertices that carry
  the changing reflected normal. Its large polygon-shaped highlights are
  unacceptable even while position error and the triangle budget pass.
- **Panel cuts:** a planar boundary dissolve cuts chords across curved hood
  and deck corners. The resulting triangular holes are visible in plan. The
  first replacement reduction is rejected rather than hidden with dark glass.
- **Rear/canopy:** a height-only rule mistakes low backlight corners for the
  body side and moves them outward. Protect the complete accepted canopy
  chart, not merely points above a height. Refit its transverse crown without
  changing its center/side silhouette. This removes the false corner humps.
- **Construction:** trim wheel openings on the open fair sheet, then close
  the gauge. Split point-touching sheet fans before Solidify; a four-face edge
  along a gauge rim is a real topology error, not a tolerable audit exception.

Action: resample the evaluated parent on a feature-aligned quad grid, retain
its extrema and normals, then make physical panel cuts. Exact 4.5 mm door cuts
replace station-dependent setbacks. Trunk side/bottom reveals align with its
split lamp pieces. The final reduction does not collapse a whole door into
large triangles. Source evaluation uses one CPU thread: an independent threaded
run exposed last-bit vertex/normal differences and one changed locator triangle.

## Pass 3 — both makes, curvature and the driver's hood view

Color/value first against the four calibrated neutral/striped pairs in
`renders/sedan-round3/`: the original clay's doors were too dark to judge well.
The balanced Workbench studio makes their gradient readable without changing
the body albedo or lifting the cavities. White photographic studio backgrounds
remain the neutral reference, with unit gains. No paint or used-car wear match
is claimed. Opened the complete contact and both makes' front/rear pairs.

- **Hood:** all three transverse sections remain convex, with localized
  curvature concentration at the two intended draw lines rather than pools
  or alternating dents. The driver's-eye reflection strip is continuous.
  It isolates the actual hood at a plausible eye because this form gate has
  no interior or transparent glazing. No smoothing shader replaces the mesh.
- **Front:** its measured plan sweep remains about 317 mm at x=850 mm. The
  turn under each lamp flows into the fender, with a roughly 386 mm local plan
  radius. The fascia is still plain beside both production photographs: the
  grille/intake/DRL locators lack the later molded seats and optical detail.
- **Doors:** the shoulder is the widest part of the section. A shallow concave
  run leads to the rising lower character line and recessed rocker. Horizontal
  and vertical bands now run across the four doors without the old repeated
  waves. The 7.8 mm mid-door chord deficit is a section
  measurement, not an artistic fairness certificate.
- **Fenders/wheels:** same-height mesh rays measure
  33.9 / 29.9 mm front/rear swell over the door.
  The swells blend into the body; they are not attached annular flare strips.
  The unchanged tires retain 40 mm crown clearance and actual inward arch hems.
- **Rear:** the local three-point radius is 305.1 mm, within 250–400 mm.
  The tail is convex across its width, with a shallow upper lean and a lower
  tuck. The crowned deck rolls into the quarter without the old corner humps.
  Its trailing edge is sharper, and the lower reveal gives the lid a coherent
  cut through the upper tail panel. Its broad plain lands remain less resolved
  than the Accord and Camry, even though their section is no longer a box.
- **Canopy:** the original six-light profile, fast windshield and tumblehome
  stay. The roof/pillar/window corners remain unusually regular compared with
  the photographic trim. This is still the least natural part of the upper form.

The plots sample five body stations plus three across each cover, on both the
unseparated parent and actual game skin. Cuts/part boundaries split derivative
runs; inward gauge faces and flat rims are excluded from an outer-skin curvature
measurement. Shaded zones explicitly mark the rocker, lower draw, shoulder,
bumper roll and deck edge. There is no unclassified sign reversal in those
sampled runs, and no hood/deck reversal away from cuts. This finite sampling
and the stripe views support one another; neither proves global Class A fairness.

## Pass 4 — actual apertures and the reproducible checkpoint

Color/value first: the inherited lamp locators sat on painted skin, so they
could hide an uncut face. The final cut gives them a real dark edge and recess,
without painting fake gaps into the material. The first projected polygon had
jagged rims and too many fragments; reject it. Fair the authored locator outline
in the parent's chart, offset it in the tangent plane, clip the already fair
skin, and close its gauge afterwards. The final local cuts preserve the parent
curvature and stay within the unchanged triangle budget. The complete new clay
views are in `renders/sedan-apertures3/`; finals are rebuilt in `sedan-round3/`.

All six lamp pieces now sit behind actual apertures. Eighteen center rays pass
through the lamp footprint without finding painted skin in the tested interval.
The black grille/intake/plate/handle locators remain form proxies; there are no
optical internals, grille wells or finished fittings at this gate.

## Pass 5 — inspect the lowest corner at both densities

Color/value first: retain the same reflection contrast while comparing the
1200 px dense-source and game views in `renders/sedan-density-check/`,
`sedan-density-game/`, `sedan-density-game3/` and `sedan-density-game4/`.
The dense source is cleaner at the lowest rear corner; the game grid still
shows small grazing-angle ripples. Additional longitudinal samples alone do
not fix them. Concentrate transverse samples in the corner as well, funded
by simpler temporary dark locator grids. The extra columns stop at the rear
chart, using a stitched transition instead of wasting them across all doors.

A hidden-gauge dissolve across the thin doors is rejected: its inner chords
cross the 0.9 mm outer sheet and give negative volumes despite closed topology.
Keep the steel backs unchanged. Restrict the reduction to the molded fascias,
with a construction-appropriate 3 mm nominal wall. Centroid and edge-midpoint
probes reject any reduced back that comes within 0.4 mm of the outer skin.
Earlier rear-back reductions fail that probe and are rejected. The final
front/rear back probes retain at least 2.20 / 1.77 mm inward depth at the tested
points, and both reductions pass. The source audits remain positive and closed.
The dense/game corner comparison is stricter evidence than the eleven sampled section checks.

The final hood and door runs are substantially cleaner than round 2. Fine
ripple remains at the fascia corners under grazing bands, most visibly at
the lowest rear corner. The plain fascia and regular upper window corners remain weaker than the photos.
The underside's band convergence appears at both densities; the small adjacent
game-mesh ripple is not dismissed as the same effect. This checkpoint is not
a claim that every reflection has reached production Class A surfacing.

Opened every final JPG in `build/sedan-round3/review-verified-0.jpg` through
`review-verified-4.jpg`, with the clay three-quarter views, rear stripes and
curvature plots also inspected at full size. All twenty render metadata entries
match the final source hash. Front/rear clay foreground 1st/99th-percentile
luma is about 8/151 and 6/128; no foreground channel clips at 255. Cavities stay
dark, and the body gradients remain visible. These are clay tonal checks,
not final paint albedo validation.

Proof from the final scripted build:

- `make -C cars BODY=sedan WIDTH=1600 SAMPLES=40` and `make ... check` pass:
  both density audits, positive closed source gauges, normals, no zero-area
  triangles, budget, accepted envelope, all 23 end ranges, swells/corner radius,
  real lamp openings, independent camera projection and repository rules.
- `make ... fairness` passes both parent and game sections. Raw positions,
  normals and signed curvature remain in `build/sedan/curvature.json` and
  `parent-curvature.json`; the paired plots are in the render folder.
- The control sheet is one connected component with 29,376 quads and
  valence four at every interior vertex. The final subdivision is evaluated
  after fitting; no post-evaluation end projection remains.
- Independent one-thread regeneration matches all 94 meshes' positions,
  polygons, normals, transforms, material names and parents exactly.
- Fresh pickup generation matches all 454 source meshes. A single-thread
  re-export matches all 150 accessors, maps and graph, and the complete
  11,530,736-byte GLB retains SHA-256
  `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.

The overlay still has a roughly −94 mm deck/spoiler difference, +33 mm hood
lead, −21 mm hood middle and −9 mm cowl; front/peak roof are +14 mm and aft roof
−12 mm. Pick uncertainty is ±16.5 mm, with residual near-profile perspective.
The roughly 1040 mm original lip follows the held spec rather than the higher Camry SE
spoiler. The four chassis camera RMS values stay 5.76 / 5.30 / 11.07 / 8.76 native
pixels. They do not certify the body silhouette or identical styling.

Remaining weaknesses are the plain fascia/pocket treatment, regular window and
C-pillar corners, grazing ripple at the fascia corners (worst at the lower
rear), and the deck/spoiler mismatch. Fine trim, optics, interior, underbody, real paint/wear and moving-part clearance remain later work; none is
claimed done. No kit changes, no sedan GLB and no committed checkpoint images.
The later detail pass must replace the temporary locator allocation to stay
inside 55k. The source checkpoint stops here.

# Sedan form round 2 — the ends

This gate supersedes the sedan form judgement at `402318a`. It is source clay,
not a finished car or a sedan GLB. The original critique and pickup history are
retained below. The accepted cabin/chassis package moves forward together by
90 mm to correct the overhang allocation; its doors, tracks and tire clearances
retain their dimensions. Only the requested front roof transition changes.

## Pass 1 — reject the first rebuilt ends

Evidence: `renders/sedan-r2-pass1/` through `sedan-r2-pass4/`, compared directly
with the Accord front and Camry rear stock photographs and the Camry profile.
White balance reference: white photographic studio background, unit RGB gains.
These are neutral clay tests; no factory-paint color claim is made.

- **Color/value first:** the dark glass and intake blanks give useful cavity
  contrast, but the body still has a chalky, simple reflection beside the silver
  Accord. Clay is appropriate here; a material change cannot repair the form.
- **Proportions and stance:** shifting the axles and cabin together corrects the
  wrong front-longer allocation. Tires still fill the arches with the accepted
  40 mm crown gap. The first nose loses too much length to subdivision rounding;
  measuring only the recipe would miss roughly 60 mm of lost overall length.
- **Hood and front panels:** the broader plan arc is better, but an inverted
  shoulder row and tightly clustered end support loops make a knot at the lamp
  corner. The upper face is still too soft in one pass; the lamp is 742 mm long,
  only 118 mm tall and returns just 89 mm. Reject against the requested envelope.
- **Front highlight flow:** the stripe fans remain conspicuous. Relaxing the
  cage alone does not solve them. The cap/side chart must be made fair, rather
  than approving the good center section and ignoring the corners.
- **Rear panels:** the reverse taper is gone, but the actual sweep is 442 mm at
  x=850 mm, almost twice the requested rear sweep. The deck measures only 318 mm;
  the upper panel leans 18 degrees. The center section alone flatters the result.
- **Side panels/wheels:** the lower draw rises correctly and the wheel package
  is retained. The rear quarter still lacks a broad, continuous haunch; its tight
  corner turns interrupt the reflection instead of blending into the quarter.
- **Roof:** the front overlay holdout remains above the Camry. Correct it along
  the accepted windshield direction so the rake does not drift.

Action: a rounded elliptical fascia volume constrains the unified subdivided
cage. A radial projection from inside that volume replaces nearest projection,
which folded adjacent rows over the hood/fascia junction. The profile, top crown
and underside tuck become one smooth surface before panel separation. Restore
normals from this same continuous sculpt, and split rear lamps at the lid cut.

## Pass 2 — final source checkpoint, both makes and both ends

Evidence: every view in `renders/sedan-round2/contact.jpg`, with the full-sized
clay/striped pairs, orthographic plan, side overlay and four actual section cuts
opened for review. Front and rear are each compared with both the Accord and
Camry, in the same calibrated framing. Backdrops are the white-balance neutral
(unit gains); the photographs' silver and black paint are not treated as clay.

- **Color/value first:** neutral clay has deep glass/intake/wheelwell shadows,
  rather than the first checkpoint's pale blocks. Opaque foreground luminance
  p1/p50/p99 is 4/43/158 front and 3/29/102 rear (8-bit display values); no channel
  clips. The rear clay is still quite dark beside the silver Accord. Its side
  curvature is easier to judge in the complementary striped view. This gate
  supplies no paint/albedo or used-car wear claim.
- **Proportions/stance:** actual full bounds are 4900 × 1850 × 1449 mm, with
  2830 mm wheelbase and 975 / 1095 mm overhangs. The previous front-longer mistake
  is removed. Both references still look more detailed and visually lighter
  around the sills; that is partly their narrower trim and real cavity openings.
  The regular greenhouse corners remain a visible procedural tell.
- **Front plan and fascia:** the 314 mm sweep now runs across the face and turns
  continuously into the fenders. It no longer presents a straight plank with
  corner radii. The centerline tangent is at 484 mm; the upper face rakes 35.2°
  to a 746 mm hood edge set back 185 mm. The 189 mm chin tucks 119 mm. Compared
  with both photos, the fictional fascia still has too much uninterrupted plain
  land between its lamp and grille locators. It needs richer molded pocket
  construction at the later detail stage; the optics will not fix a wrong contour.
- **Hood/fenders:** the hood rises 10.5° to a 965 mm cowl, with 31 mm cross crown.
  The soft paired draws move outward toward the A-pillar feet. The leading reveal
  now follows the end arc. Broad bands are fair across the hood and fascia;
  highlights still gather tightly at the lamp/shoulder junction compared with
  the Accord's gentler draw. The form locators originally let paint poke through
  their chords. Local conforming subdivision removes those white tears without
  changing the body's sculpt or floating the whole lamp farther off the body.
- **Lamps/grille:** each headlamp measures about 696 mm along the actual sampled
  surface, 147 mm maximum aperture height and 225 mm return into the side. Their
  upper outline follows the hood reveal. The grille is a broad trapezoid above
  the black lower intake, with separate corner pockets. These remain dark
  locators, visibly simpler than real lenses and deep grille seats in the photos.
- **Cabin/roof:** the requested header adjustment follows the accepted rake,
  measured at 61.48° from vertical. B-pillar tumblehome measures 24.14°, within
  the requested class band and the photo estimate's uncertainty. The roof-front
  overlay holdout is now +14 mm, down from about +49 mm; peak +14 mm, rear roof
  −12 mm. The fixed quarter pane and accepted side-glass outline remain.
- **Side panels/highlight flow:** the shoulder is legible through the handles
  in both three-quarter views; the lower draw rises rearward. Door panels keep
  a broad outward crown and tuck into the rocker. The rear haunch has a broad
  reflection over the wheel instead of a separate swollen corner. The small
  lower corner transitions still gather the bands more tightly than production
  surfacing. The gross cap crumples are removed; this is not a claim that every
  highlight now matches an OEM stamping.
- **Rear plan/panel:** 238 mm sweep, 11.5° upper lean and a 602 mm bumper tangent
  replace the square vertical tail. The lower fascia recedes 176 mm to the
  diffuser at 300 mm. The wrap blends into the quarter without the old reverse
  taper. Its broad plain tail land still looks less resolved than both makes'
  sculpted plate recesses; that weakness remains visible in clay.
- **Deck/lamps:** actual center deck length is 373 mm, rising 5° to a 1043 mm lip,
  with 22 mm transverse crown. Lamps wrap from quarter to lid, with a real
  separated cut and correct parent ownership for the lid blanks. The lip is
  crisp in section but subtler in the clay rear view than the Camry SE spoiler.
- **Wheels/arches:** all four retain 40 mm crown clearance and the 235 mm tire
  width; tires sit close to the shoulders with actual inward arch flanges. Wheel
  and tire geometry is the accepted family method, 2404 triangles per corner.
  The sportier Camry wheels and Accord's smaller package should not be used to
  rescale this accepted tire choice.
- **Overlay limits:** worst sampled vertical difference is −96 mm at the Camry
  deck/spoiler; hood lead +33 mm, hood middle −21 mm, cowl −9 mm. Picks carry
  ±16.5 mm uncertainty and the near-profile photo retains perspective. The
  1043 mm original lip follows this brief's 1000–1050 mm spec, so the higher
  photographed spoiler is not silently adopted. The nose still differs in
  silhouette despite the corrected package; the 975 mm published front reference
  is 25 mm outside the brief's rough 860–950 mm photo estimate.

Proof: full `make BODY=sedan WIDTH=1600 SAMPLES=40` passes from scripts through
both-density audits, all 23 numeric end checks, independent Blender camera
projection, all renders/pairs and repository policy. Camera RMS, native pixels:
Accord front 5.76, Camry rear 5.30, Camry front 11.07, Accord rear 8.76. These fit
chassis anchors, not body shape; the extra two fits have visibly larger residuals.
All retained lamp samples are measured on the actual mesh (zero distance).
Game: 46,972 triangles; high: 373,984; four diagnostic materials, zero maps.
The planned 2048 set remains 16 MiB compressed with full mips. Independent sedan
regeneration matches all 94 meshes exactly. Fresh pickup generation and re-export
retain all 454 source meshes, 150 GLB accessors, maps and graph; the complete
11,530,736-byte GLB retains SHA-256
`f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
No kit changes and no sedan detail/delivery work beyond this checkpoint.

# Alder S240 sedan — source form checkpoint

The C150 pickup below remains accepted. This section is the second body type's
source form gate only. No sedan look-dev, wear, interior, underbody, atlas,
bake, GLB, final docs or motion-clearance certification is claimed.

## Sedan pass 1 — reject the end closures and artificial seam highlights

Color/value first against the silver Accord and black Camry stock photographs:
neutral gray clay is deliberately neither reference paint. Use their neutral
white studio backdrop for white balance (unit RGB gains), retain charcoal tire
and glazing proxies, and compare geometry and bands rather than brightening the
clay to match silver. All five `sedan-pass1` and `sedan-pass2` views were opened
in complete contacts; neither pass is an acceptable review candidate.

The roof peak, low hood and fast rear slope identify the class in profile, but
the independent end moldings leave square discontinuous walls. Top view exposes
the open corners. The first side has broad bright vertical bands at the door
boundaries: the sheet closing changed the smoothing fans despite the correct
pre-split normals. The black grille is a small rectangle in an otherwise flat
face. The first count is 46,504, spending 13,316 on the two inefficient caps.
Reject those caps and the apparent seam dents; dimensions alone do not rescue
this. The A/C-pillar transitions and lamp seats also need a continuous source.

## Sedan pass 2 — continuous corners, then reject the normal encoding

Color/value first against both makes: keep the neutral diagnostic clay and
unclipped stripe world. The two-color world is lighting equipment, generated by
nodes; it contains no reference image. Opened all seven `sedan-pass4` views,
including top, side and both full-size stripe directions.

The replacement cap grids now share the actual body-cage boundary vertices.
Catmull-Clark evaluates hood, sides, greenhouse, deck and both end caps together
before panels separate. This removes the disconnected bumper plate. Smooth
master normals transfer across the 4.5 mm shut lines after closing the gauge.
But the first stripe pass still bends sharply in broad strips beside seams:
edge-return faces remained in the outer skin's smoothing fans. Mark those
edges sharp and keep their normals geometric before restoring the outer field.
The rerender (`sedan-pass5`) removes these false vertical dents without changing
the dimensional targets. Both doors carry continuous broad bands.

Region critique: the stance and low arch gap read better than the pickup's
clearance. The hood is still too featureless beside both photos; the fascia and
rear are tall, square and too regular. Roof/glass boundaries are less rounded
than production glazing. Do not conceal those weaknesses with lamp details or
paint. The initial 220 mm C-divider is excessive; replace it with a short thin
post and a fixed quarter pane. Split the recessed rocker from the lower doors.

## Sedan pass 3 — calibrated photographs, construction and measured section

Color/value first: the silver Accord is brighter than clay, and the black Camry
carries a more complex studio reflection. Neither difference justifies changing
the neutral body or hiding lower-panel curvature. Opened all four raw stripe /
matched views in `sedan-pass5`, and both full-size composed photo pairs.

The kit fits five chassis anchors per view. Front Accord RMS is 5.76 native
pixels; rear Camry is 5.30 at 2100 px width. Two near hubs and contacts constrain
scale/stance. The Accord's obscured far-front contact is low-weight and has
larger uncertainty. These are chassis registrations, not all-body accuracy;
roof/deck/lamp and original overhang differences remain plainly visible.

Measured Accord B-pillar glass picks are back-projected through its calibrated
camera into a local y=0.20 m section plane. The class estimate is 23.97 degrees
from vertical, with about +/-4.5 degrees uncertainty for picking, camera/class
registration and unmeasured pillar rake. The neutral white backdrop is the
white-balance reference. This is an explicitly approximate photographic section,
not a manufacturer cross-section drawing. No picked outline becomes geometry.

The evaluated B-pillar cut measures 23.75 degrees. The front/rear axle cuts
intersect hood and descending deck/greenhouse respectively, so a full-height
side-glass angle is not invented there. Actual door rays show a 13.8 mm crown
above their lower/upper chord. All four tire/arch crowns have 40.0 mm clearance;
flanges run inward 18 mm, and dark inboard liners block daylight through the
wells. The side's lower die line now rises aft instead of remaining horizontal.
Front DRL and lower intake pockets are blocked only, with real recessed depth.
Wrapped lamp volumes follow the corner's local plan normal; optics are deferred.

The 44,454-triangle pass still facets the broad rear cap, so increase the master
sampling to two subdivision levels and reduce its interiors while preserving
all evaluated seam vertices. A subsequent restoration of the pre-cut master
normal field removes the aperture-induced cap bands. Do not relax the topology
or normal checks to accept them. All `sedan-pass6` and `sedan-pass7` clay views
were opened in complete contacts. The cap's planar character and unusually even
window edges remain artistic weaknesses to judge in the final set.

## Sedan pass 4 — reject invalid cuts and a misleading reflection dome

Color/value first: retain neutral clay, charcoal tires and deep cavities. The
white studio reference backgrounds remain the neutral balance. Full-size pairs
and the complete 16-view contact exposed radial bands over the end caps; they
were not acceptable as a fairness claim. `renders/sedan-cap-rejected/` preserves
the earlier comparison set. A rectangular cap grid removes the old converging
U strips and reduces redundant geometry, while shared evaluated boundaries keep
the corner attached to the body. Separate plan sweep and vertical face sections
avoid forcing all height variation to zero at the side corner.

Both-density builds also exposed an unstable exact swept lamp cut: it could
discard an entire high-source fender or quarter. The model now rejects that
condition explicitly during development; it is not allowed to pass as an empty
part. At this form gate, the final opening locators are conformed dark blanks,
including the grille/DRL/diffuser and lamps. Finished wells and optical internals
remain deferred. Their front faces need actual interior sampling: a single
non-planar n-gon chords through the body crown and disappears behind it. The
sampled blanks retain their outline without pretending to be detailed optics.
One-micron welding at the exact arch intersections removes four high-source
slivers; the unchanged audit tolerances still reject zero-area triangles.

The remaining radial fan was partly a diagnostic error: atan2(Z,X) put a stripe
pole along the front/rear axis. That environment can make a fair face look like
a pinched fan. Replace horizontal bands with arcsin(Z) latitude bands, leaving
the mesh fixed, and rerender both studio stripes and both calibrated pairs.
Vertical bands retain an independent azimuth mapping. The final horizontal
render no longer has those radial cap fans. Do not report the old dome's pole
as a measured surface defect or claim that cage changes alone fixed it.

## Sedan pass 5 — final form candidate, with remaining weaknesses explicit

Color/value first against the final Accord/Camry pairs in `renders/sedan-form/`:
neutral clay retains black tires, dark glazing and darker lower/cavity regions.
It is not silver or black paint look-dev. The white backdrops supply neutral
balance. The hero's foreground display luma p1/p50/p99 is 4.79/43.38/145.37;
rear is 3.79/30.07/117.22 on 0–255. Neither clips a channel to 255. About
15.9% / 26.4% of those foregrounds is below 25, excluding background and floor.
These are diagnostic image statistics, not measured albedos.

Opened every final view through the complete 16-image contact, then inspected
the two full-size photo pairs, both stripe directions, clay heroes, section
plot and overlay separately. These are all one current game source. The kit
independently verifies the fitted camera projections; the 5.76 / 5.30 px native
chassis RMS does not make the body a few-pixel match.

Region-by-region judgment:

- Proportion/profile: 4900.01 x 1850.06 x 1449.87 mm, 2830 mm wheelbase and
  1590/1600 mm tracks are measured. The 757.78 mm leading hood, 61.20-degree
  A-pillar and roof peak behind the B-pillar meet the requested language. The
  axle-scaled Camry overlay still shows a roughly 50 mm earlier/higher front
  roof transition and an 87 mm lower selected deck station (+/-16.5 mm picks,
  residual perspective and original styling). The 1043.79 mm deck crest meets
  the brief but is not a Camry replica. Keep these differences visible.
- Stance/arches: four 40.00 mm crown clearances and 235 mm tires read low and
  closely filled. Wheels sit about 12–13 mm inside the body's maximum shoulder,
  not deep under a pickup flare. Arch returns and inboard closures are present.
  Tread and brake construction remain the later shared-family detail stage.
- Section/side: actual B-pillar tumblehome is 23.75 degrees against the uncertain
  23.97 +/-4.5 photo estimate. The lower door tucks into a recessed rocker and
  carries a 13.76 mm vertical crown. The die line rises aft. Door bands now
  continue across the measured 4.497–4.502 mm gaps without the former broad
  artificial seam dents. Small compression remains at the sill/arch junction.
- Hood/roof/greenhouse: broad hood and roof bands are continuous. The A/roof rail
  and glazing corners are still unusually regular, with tighter stripe turns
  than the class photographs. The front roof transition is more upright/early
  than the Camry, and the C-pillar/quarter-pane termination is less fluid. The
  six-light choice is practical but does not by itself make these corners Class A.
- Front: plan crown and low wrapped lamp blanks are now clear; the low grille,
  lower intake and DRL pockets belong to one molded fascia. It remains plainer
  and squarer than either reference. The lower corner has localized stripe
  compression; the current broad smooth body should not be mistaken for a
  finished bumper tooling design. Opening blanks are intentionally temporary.
- Rear: lamps turn from the cap into the quarter, the deck has an integrated
  trailing crest, and the lower diffuser is located. The rear cap and bumper
  need more distinct production-like sculpting; the central plate/trunk field
  remains especially plain. Horizontal bands flow across the cap after fixing
  the dome, while corner/rail reflections still deserve the lead's scrutiny.

`make -C cars BODY=sedan WIDTH=1600 SAMPLES=40` passes the full source checkpoint,
including both-density kit audits, measured form checks, camera verification,
GPU-locked Cycles stripes/pairs, Workbench clay, all annotations and repository
policy. Game/high counts are **46,892 / 360,452** with four clay materials and
zero image textures. Game/high blends are about **1.1 / 6.1 MB**, ignored.
`build/sedan/form-check.json` contains every per-mesh/parent/category count.
The future three-map 2048 plan is about 16 MiB compressed with mips, not a
shipped allocation. UVs, underbody clearance, interior, finishes, moving-part
ownership/sweeps, baking, GLB and final delivery remain explicitly open.

Independent sedan regeneration matches all captured geometry, corner normals,
transforms, materials and hierarchy exactly. The pickup comparison matches all
454 source meshes, 150 GLB accessors, all three embedded images and the full
GLB bytes: SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
It re-exports accepted finalized geometry/maps; no GPU rebake is claimed. The
pickup README's previous byte count was 12 bytes stale and is corrected to the
measured 11,530,736; the GLB itself has not changed. No kit code or docs images
change. Nothing is needed beyond the lead's requested form review. Stop here.

# Alder C150 / exported delivery review

Finished delivery: 59,838 triangles, four surfaces, one shared 2048 set.
The source face is accepted; all final images are imported-GLB renders.
The source checkpoint and earlier critiques below are retained as history.

## Shipping pass 1 — reject bake artifacts before material tuning

Color/value first in all four `renders/ship-pass1-pairs/*-pair.jpg` comparisons:
Carbon and Graphite retain their intended dark/medium values, but the white
holes and broken reflections are unacceptable against either the F-150 or Ram.
Opened the hero, front, wheel and open-driver interior in `renders/ship-pass1/`.
The grille remains recessed and the new surround gives a dim satin chrome
reflection; the bumper has its requested crisp top line and lower return.

Rejected this first GLB. Hood projection misses, fractured glass frit, lost
fictional plate/badge/grille pixels, and damaged corner normals are bake/export
loss, not a reason to alter the accepted body or wear. Preserve analytic corner
normals across UV editing, keep original generated glass coordinates and explicit
PrintUV through source consolidation, and improve the hood/rear-glass projection
mesh. Preserve unlit lamp colors and encode the individual emitter power in the
shared BaseColor alpha. First GLB is archived in `build/cars-final/pass1.glb`.
17 full-range source motion sweeps now pass on game and high assemblies; these
check actual neighbors rather than comparing constant target dimensions.

## Shipping pass 2 — continuity recovered; reject lost optics and print relief

Color/value first in the four new `renders/ship-pass2-pairs/` comparisons:
Graphite still separates from the tires by the accepted medium-gray step;
Carbon retains deep lower-door/underbody values. The reflected horizon remains
smoother than the photographs, which have trees, cars and pavement variations.
Opened all six studio views, all four pairs and their masks. The hood misses
and large glass holes are gone. The satin surround and formed bumper line
survive the bake. All six baked channels have zero missed eroded-interior texels.

Still reject the plate's mottled black face and the blank grille field.
Independent rays reveal that the carrier's front and printed face are exactly
coplanar, so the bake chooses either plastic or print. Move the carrier back
2 mm and check actual separation. The grille's source UV layer is named
Original relief, unlike the plates' PrintUV: preserve each object's original
active UV coordinates as a generic corner attribute before consolidation.
The unlit/lit lamp views lose some projector/guide clarity, and the tread and
flake are too subdued at this atlas density. Correct these delivery losses
before finals; do not replace the accepted source paint, wear or sculpting.

The new imported-GLB articulation test matches all 17 swept poses within
0.00073 mm. Its first analytic-normal query also included nearby trim at the
lamp/fender joint; restrict that query to the actual broad side fields rather
than treating a coincident trim vertex as the same surface derivative.

## Shipping pass 3 — restored delivery details and engine compatibility

Color/value first against all four `renders/ship-pass3-pairs/` photographs:
Graphite retains its warm medium value and the accepted long sky/ground band;
Carbon is dark below the shoulder. The low road-film fans remain restrained,
as in the accepted source, rather than spreading noise over the paint. The
baked clean Atlantic texels independently measure .01229/.03689/.07036 linear
against .012/.037/.071. About 1.17% of eroded paint interiors carry more than
5% contamination; this measurement establishes surviving coverage, not an
artistic claim that every deposit is visible at every camera distance.

Opened the ten Cycles views, all five factory paints, four photo pairs and
all geometry/paint masks. The plate now reads, the original grille diamond
field survives at the back of the cavity, projector/reflector and DRL are
clean, and the wheel lip no longer carries the false jagged tire projection.
All 4k channels again have zero missed interior texels. Keep the coating's
continuous mirror lobe and the filtered mean flake response; this shared 2k
atlas cannot show individual microscopic flakes or crisp tiny sidewall type.
The low-detail seat/dash volumes remain the weakest close-up, as expected from
the accepted interior. No source-body, paint-color or wear redesign is made.

The first Eevee hero has black lamp covers: screen-space tracing cannot follow
the nested glass paths. Enabling per-material refraction and reducing trace
thickness did not recover them. Use an explicitly documented thin-sheet
Fresnel/colored-transparency preview from the GLB's same three maps; inspect
both the cover and windshield for sorting artifacts. Cycles keeps the full
transmission material. Final metadata names this engine difference.

This working pass spans a config whitespace cleanup and the Eevee adapter
revision; its recipe hashes record that and the strict combined-sheet check
rejects it as a final set. The next pass re-renders every final together under
one frozen recipe and current GLB hash, rather than rewriting provenance.

## Shipping pass 4 — final GLB, tone, pairs and delivery proof

Color/value first against the four full-size `renders/final-pairs/*-pair.jpg`
photographs: Carbon keeps dark lower panels and a bright reflected upper band;
Graphite retains its warm gray base under blue sky reflection, with tires and
cavities visibly darker. The synthetic horizons remain smoother and simpler
than the photographed surroundings. The wear stays localized and restrained;
there is no new uniform dirt wash or bright metal facade. Keep these accepted
values. Individual microscopic flakes and small sidewall type are filtered at
this atlas density; do not describe them as crisp visible particles.

Opened the final hero, turnaround, front/wheel/open-driver close-ups, 1.8 m
scale shot, lit lamps, five-color sheet, Eevee hero, all four pairs and their
paint/geometry masks. Every view comes from the current 11,530,724-byte GLB,
with the same recorded render recipe. Cycles images are 1600 px / 96 samples;
Eevee is 1600 px / 192 samples. The explicitly documented thin-sheet glass
fallback removes its black covers and transparent sorting seams; its lighting
and refraction remain an approximation to the Cycles result.

The masked hero paint has display-luminance p5/p50/p95 of
.0438/.2492/.3603; its p99 is .7876. No paint pixel clips to 255, including
Porcelain. About 34.7% of the vehicle mask lies below 25/255 display luminance,
including tire, grille, interior and underbody cavities. These are lit-image
measurements, not inferred albedos. Front-detail paint p99 is .9456 with zero
clipped paint pixels, retaining the highlight rolloff.

All six 4096 bake channels have zero missed eroded-interior texels over
6,151,123 checked pixels. The re-imported atlas has 43.30% coverage, zero
outside/degenerate/overlapping UV triangles and p5/p50/p95 density of
69.2/161.2/196.4 px/m. The exported broad side normals remain within .028°
of the analytic field. Kit re-import vertex error is below .00028 mm.

Source clearance passes all 17 motions / 651 poses at both densities, with
no unapproved penetration over 0.5 mm. Exported articulation matches the
source within .00073 mm. Actual kingpin axes retain 12° inclination, 6.5°
caster, 40 mm scrub and 45 mm trail. This proves sampled mechanical clearance
and retained kinematics separately; it does not claim continuous physics or
tire carcass deformation. The tire rolls as a circular loaded-envelope approximation.

The full default build passes. The remaining CG tells are the simple interior
volumes, filtered tiny lettering/flake, and less complex procedural reflections
than the photographs. The three final docs JPGs are bounded to 1600 px wide
and 200 KB and contain only original rendered assets. Repository-source
portability scan finds no absolute/home paths. No further source look-dev pass
or additional triangle/texture allocation is made.

## Archived source face checkpoint

**Earlier gate: front source checkpoint only.**
All earlier round claims below are archived. The accepted body side fields,
paints, wheels/brakes, causal wear, glazing and interior stay fixed.

## Face pass 1 — correct the value hierarchy, reject the construction artifacts

Color/value first against both the F-150 and Ram fronts in
`renders/lookdev-r3/used-pairs-contact.jpg`: the former silver plate dominates
both faces where the photographs put dark grille cavities, body paint and
small bright optical/chrome accents. The preliminary `renders/face-pass1/`
changes that hierarchy with satin dark plating, a tall central grille,
body-colored bumper and textured black mirror caps. Projector, broad reflector
and the accepted 16 mm running guide remain in a low, continuous cover.

Rejected the preliminary construction after opening front detail, lit lamps,
plan and profile: the lamp backs/guides were offset in Y even where the lens
turns onto the fender, making protruding wedges. Offset along the actual plan
normal instead. The left bumper's initial tangent faced partly aft and an
incorrect normal hint turned its edge returns outwards. The top return also
folded where a fixed Y inset crossed the side tangent. Give each half the
correct outward hint and inset the shelf along its plan normal. Do not relax
the manifold, signed-volume, sliver or overall-length audits. Left mirrored
optics need their winding reversed. Seal the grille cavity behind its field,
not with a black cap in front of the blades.

## Face pass 2 — photo pairs, true crown stations and surround land widths

Color/value first against both actual new pairs in `renders/face-pass2/`:
the F-150 comparison now has a dark grille above a separate body-colored beam;
the unlit projector/reflector and narrow guide are the bright accents. The
Ram pair retains the accepted medium warm Graphite finish and its existing
calibrated daylight. Neither pair has the broad silver facade or silver mirror
boxes. Synthetic surroundings still supply much smoother reflections than
either photograph; keep that disclosed limit and retain the accepted lighting.

Opened all eight views and their mask sheet, both pairs at full resolution,
plus the plan, true side profile and elevated side/front close-up. The face
now sweeps into the fenders; its protective cover follows the corner rather
than sitting on a box. Four recessed dark blades span one tall opening, with
an original fine diamond field behind them. The 250 mm body-colored bumper
has its own top return and a real plate pocket. Below it are the black intake,
separate molded webs and exposed recovery loops.

The independent rays initially caught a subtle error that the high-angle
render alone hid: long top/bottom frame edges without intermediate stations
made planar chords across the crown. Add physical crown stations. The corrected
rays measure 121 mm of sweep at x=950 mm and 8.00 degrees of rake. Lens front
projection is 387 x 154 mm, narrowing to 58 mm at the aft edge; its 178 mm
fore/aft corner return is additional to the frontal width (developed centerline
553 mm including that return). Do not mislabel the whole developed path as a
387 mm arc. Hood reveal is 5.04–7.78 mm on 29 actual leading-edge samples.

The source audits pass topology and body scale; 320 accepted mesh parts compare
exactly in world vertices, polygons, corner normals and material names against
the takeover build. The measurement rejects 83–88 mm of lower side land on the
first trapezoid. Inset its sloping sides geometrically to 70 mm instead of
subtracting 70 mm independently from width and height. Close the dark vertical
slots beside the lower surround by carrying the painted cheek onto its covered
mounting edge. These are face corrections; the accepted side fields remain fixed.

## Face pass 3 — measured source checkpoint and final photograph critique

Color/value first against the final F-150 and Ram front pairs in
`renders/face-checkpoint/`: the surround and grille stay dark, the body-colored
bumper retains the truck's factory tint, and the optics supply narrow bright
accents. The former bright silver facade and mirror-cap glare are gone.
The new grille is taller and more dominant than the Ram's; that is the authored
Alder design within the requested architecture, not a claim to copy its face.
The lamps retain their low, original guide outline as they turn onto the fender.
The corrected lower cheeks meet the surround instead of leaving deep vertical
slots. Plan/profile/elevated views show the continuous crown, inset grille,
rearward rake and a separate forward-set bumper.

The final surround has 70.00 mm top/bottom lands and 76.31–76.38 mm of actual
rounded side-face arc. A slimmer face crown removes the earlier 84 mm arc
without reducing its real return; measured axial section depth is 74.43 mm.
Actual sweep at x=950 mm is **120.08 mm** and rake is **7.995°**.
The grille is **1203.66 mm** wide, **60.95%** of the measured face width.
Both lamps measure **387.29 × 154.00 mm** in front projection. They taper to
58.00 mm at their aft edge, return 178.32 mm fore/aft around the corner, and
have 553.21 mm of developed centerline including that return. The 250.00 mm
bumper and 5.04–5.34 mm hood reveal also come from actual game surfaces.
These are source construction measurements, not serialization tests.

Two closed 8 mm mounting ears cost 24 triangles and connect the curved bumper
skin to the accepted crash beam. BVH crossings check both ends of that support,
the recovery-loop/bracket/crash-mount connections, and all blade-end/rail/frame
contacts at game and high density. Neither a constant nor a matching export is
substituted for a contact measurement. The takeover comparison finds zero
changes among 320 accepted meshes' world vertices, polygons, corner normals
and material names. A separate graph comparison finds all 33 original material
node graphs unchanged; the only added graph is satin dark chrome. Evidence:
`build/cars-face/preserved.json` and `materials-preserved.json`. The hood/nose
and fender leading closures are explicitly outside the mesh comparison.

`make -C cars` ran successfully at takeover. The final command is
`make -C cars face PASS=face-checkpoint WIDTH=1500 SAMPLES=64`, including source
checks, independent projection checks, six studio/diagnostic views, both front
pairs, masks and contacts. `make -C cars check` passes as its prerequisite:
game/high topology have zero errors/warnings; dimensions, normals, source
budgets, gauge and static fits pass. The repository scan and tracked-car
portability scan pass. GPU Cycles runs through the kit's flock wrapper.

Final count: **59,142 game / 195,322 high triangles**, **34 source materials**,
six original source sheets. The high/game blends are **2,259,444 / 1,051,201
bytes**. The planned four delivery surfaces and one shared 2048 BaseColor /
Normal / ORM set for all five colors stay unchanged (about 16 MiB compressed
with mips). No atlas unwrap, bake, GLB, final motion certification or committed
docs image is part of this checkpoint.

Opened all eight final views individually, both full-resolution photo pairs,
and the full view/mask contacts. The elevated diagnostic initially clipped
about 1.03% of paint samples; lowering only that shot from −2 to −3 EV removes
it. Accepted hero and photographic lighting stay fixed. The final eight-view
repeat has zero paint or vehicle samples at channel 255. Hero paint display
luma p01/p50/p99 is 6.23/63.33/192.36; front detail is 7.93/83.14/240.86;
the elevated diagnostic is 6.00/67.92/242.14. Cavities and underbody retain
deep shadow. These are masked display values, not albedo measurements.
`renders/face-checkpoint/tonal-range.json` contains the full distributions.
One source hash and one recipe hash cover all eight views; both contacts and
all individual JPGs are beside the source PNGs. All are ignored build outputs.

Remaining tells: the reflection horizon is much smoother than either real
street; unlit reflector tooling is simplified, the lower painted cheeks are
restrained, and the closed lamp guides are unusually regular. The tiny tire,
mesh and paint details still need a baked-2048 inspection. Nothing is needed
from the lead; no shared kit code changed. Stop here for the bake/GLB brief.

# Alder C150 / look-dev round 3

**Current gate: last source look-dev checkpoint. Stop before atlas UVs/bake/export.**
The wheels/brakes/shoulder tread, DRL output, causal wear and 60k limit remain
the accepted constraints. Earlier R2 records below are historical.

## R3 pass 1 — diagnose the side and replace the grille-guard architecture

Color/value first: compare the same Ram door patches, rather than changing
exposure to hide a wrong factory tint. R2's Graphite was both too dark and too
neutral. Native-photo patches remain analysis only; they never enter materials.
The first R3 tint is a medium, slightly warm gray. The front and rear photos
have materially different illumination; a single sun on the visible side in
both comparisons cannot reproduce them. A linked-metallic-socket bug also
ignored the old variant defaults. The new named metallic value drives the
actual Principled input and its bake channel. Shared microscopic roughness/
height aggregates provide the flake lobe; no albedo noise or extra map is added.

`renders/r3-baseline/` holds the counterfactuals on the unchanged R2 source:
`plain_aged_rear.png`, `plain_used_rear.png`, `stripes_side.png`. All three were
opened. Irregular pale/dark blobs disappear when only the parked/foliage proxies
are hidden; the stripe dome shows continuous fair door and bed surfaces. The
source paint/wear is retained in the plain views. The smooth conductor replaces
only paint in the stripe view to isolate geometric normals. Thus the irregular
blotches were reflection scenery, not dents. Retain the accepted side field.
A continuous analytic sky/asphalt horizon replaces the proxies in the pairs.

The first new face in `renders/lookdev-r3-01/` has one closed frame containing
both wide, low lamps and the grille aperture, with a straight hood leading edge.
It reads as one fascia instead of lamps outside a tubular grille guard. The
full-width lamellae are recessed; their ends are supported behind the frame.
The original C guide retains its accepted 16 mm section and powered output.
All eight views and their masks, the pair contact and individual front views
were opened. The large upper land, internal webs and actual section now carry
the architecture. Tighten the corner sweep so the outboard land's actual surface
width also meets 40–80 mm. Seal the optical wells and move the guide clear of
the protective lens. Do not alter the accepted wheels or add silhouette trivia.

The preliminary game source is about 57.1k. The audit caught two coincident
boolean/bevel vertices in the frame (zero-area slivers): weld at 1 micrometer
before the sweep, rather than relaxing the audit. The second pass measures
frame lands, section, lamp dimensions and hood setback on actual surfaces.

## R3 pass 2 — reject the broad pale band; match the same gray door patches

Color/value first: `renders/lookdev-r3-02/` and the three small lighting tests
reject the broad pale band on Graphite. A frame-average gray is insufficient:
the mid-door and upper-door patches must agree separately. The initial clear
world made the rear mid-door about 158 display-luma levels against 77 in the
photo. Simply reducing the whole sky made it 55 and crushed the wheels. The
rear photograph has a partly obstructed parking-lot horizon and shaded side;
use a continuous elevation transition into the blue sky instead of adding
parked boxes and tree blobs again. Keep the common factory tint fixed.

The last small test (`renders/lookdev-r3-light-test3/`) has front mid-door
RGB 130/139/147 (luma 138), against the photo's 136/141/150 (141). Its rear
upper door is 97/121/140 (117), against 100/121/143 (118). Rear mid-door is
still about nine levels too bright, so slightly raise the obstructed horizon's
lower elevation for the final render. These are median lit-pixel comparisons,
not albedo measurements; corresponding surface picks and class registration
have uncertainty. Original paint is linear RGB .160/.153/.141, metallic .42,
in both Ram views. No photo pixels become texture data.

Correct a stage reset that overwrote the rear sun rotation after selecting its
lighting. Conditions now run after resetting studio transforms; shot metadata
records the actual sun ray direction and environment strength. Clear and
overcast conditions both have a continuous sky/asphalt horizon, with no
reflected parked/foliage geometry. Source paint still supplies fine highlight
variation; the side's broad normal field is unchanged.

The final architecture has 500 × 165 mm apertures around 496 × 161 mm lenses,
60 mm top/bottom/internal lands and approximately 79–80 mm of outboard curved
land. The frame is 65 mm deep. Actual hood rays/vertices give a straight
4.500 mm shut line and 7.550 mm minimum fore/aft setback. The center pressing
ends aft of this boundary. Wide, recessed lamellae span beneath the lamp
pockets; measured surface intersections check their end mounts against both
the bars and frame. Both source densities pass the manifold/degeneracy audit.
The game source is 57,288 triangles; accepted wheels/brakes remain 14,888.

Opened the pair and view contacts for the small tests, plus individual front
and rear Ram pairs and the new front detail. The broad frame reads as a
single fascia; the unlit optic facets are still simpler than production lamps.
The plain horizon removes false dents but is visibly simpler than the real
street. Retain these limits for the final checkpoint instead of claiming a
parking-lot reproduction.

## R3 pass 3 — final requested source checkpoint

Color/value first against all four final pairs in `renders/lookdev-r3/`:
the two Ram mid-door samples now measure 138/141 display luma in front,
against 141/140 in the photo, and 76/78 in rear, against 77/82. The rear upper
door is 95/119/139 (luma 115), against 100/121/143 (118). The front upper
sample remains a little bright (151 versus 142). These are 15 × 15 pixel
medians at the 1500-pixel render scale, registered to corresponding cropped
photo positions; they establish the broad hue/value correction, not an exact
spectral material match. Medium warm Graphite is visibly above the tire value,
with continuous clear coat and fine under-coat flake variation. The shared
atlas allocation and all five tint presets remain unchanged.

Opened every final view individually: front three-quarter, front detail,
lamps lit, side, all four pairs, both plain worlds and side stripes. Also
opened the full view/pair contacts and all eight geometry/paint masks. The
stripe diagnostic has continuous bands through both doors and bed, with
deliberate arch draws bending them around the openings. In the plain worlds
and final pairs there are no irregular reflected parked-car/foliage patches.
The fascia carries both lamps within one substantial section; the straight
hood line and recessed bar shadows read in the front pair and detail. The
original powered guide is clear at the same exposure as the unlit view.

`make -C cars round3 PASS=lookdev-r3 WIDTH=1500 SAMPLES=64` passed: source
audits, dimensions/static fits at game and high density, independent camera
projection, eight requested renders/masks, three diagnostic renders, four
composed pairs and the tonal review. Both source geometry audits have zero
errors/warnings. Actual bar-front recess is 79.00 mm. End mounts intersect
all three bars and the common frame at both densities. Game count is 57,288;
high source is 189,728. These are source geometry/construction checks,
not full motion or delivery checks.

The masked hero has paint luma p01/p50/p99 = 10/66/199 on the display's
0–255 scale; front-detail paint is 9/107/242. Neither studio view has a
channel at 255. Grille cavities and underbody retain deep shadow. Tiny direct
sun glints affect 0.002%/0.012% of front/rear pair paint pixels at channel 255;
there is no broad clipped panel. The side studio view remains deliberately
dark (paint median 19); the paired/plain horizons are the surface-value proof.
Full measurements and masks are beside the images in `tonal-range.json`.

Still CG: the horizon is much smoother than real surrounding streets; large
paint/glass reflections therefore lack their fine scenic structure. Unlit
headlamp reflector facets are simplified. The plated frame is unusually
regular, and the studio side is dark. Fine flakes and wear still need the
next brief's 2048 bake/re-import comparison. Stop here: no atlas unwrap,
bake, GLB, final docs images or delivery certification in this round.

## Earlier look-dev rounds — archived evidence

# Alder C150 / look-dev round 2

**Current gate: source look-dev only. Stop before UV and bake.**
The earlier round's evidence and claims below are historical. This round uses
its calibrated Ram/Ford views, without changing the camera registrations.

## R2 pass 1 — reject an over-bright sky and an underexposed overcast

Color/value first, against the four photographs in
`renders/lookdev-r2-01/used-pairs-contact.jpg`: removing the tall facade walls
and reducing coat roughness exposes the sky/ground transition, but the clear
sky is too blue and much too strong. The windshield is nearly white; Graphite
looks pale blue. The Ford sky is too weak for its exposure, crushing black
paint and wheels. These are rejected lighting/exposure results, not a successful
paint match. Next: reduce the clear sky to .12, retain directional sunlight,
and increase the overcast illumination/exposure separately.

The same-source studio wheel close-up proves the marbled finish came from the
low world-height road-film mask: excluding alloy/chrome/steel from that layer
removes it. The old spokes still look thin and the shoulder is still round.
The low film now stays in swept envelopes aft of each tire; tailgate center
streaks are removed and chrome keeps its metal color. Paint retains its factory
hue instead of carrying an opaque brown noise layer. The old face and mirrors
remain inadequate in this pass. Seven rendered views and all masks were opened.

## R2 pass 2 — manufactured shape, then reject seams and reflected blocks

Color/value first against `renders/lookdev-r2-02/used-pairs-contact.jpg`: the
Ram Graphite is darker and no longer pale blue, but still too cool. The Ford
paint now has a pale upper band and dark lower panels, though the repeated
parking proxies make reflected blocks too orderly. The glass is smooth but
still too light relative to the photographed windshield. Next: desaturate only
the procedural daylight, use irregular fine foliage silhouettes, and tune the
laminated windshield's transmission tint. Keep the paint tint unchanged.

The taller grille follows the hood edge, and its deep lamellae hold shadow.
The single projector and 16 mm guide reject the old quad-lamp appearance.
The lit guide is unmistakable in the same studio exposure. The close-up rejects
intersecting spoke branches: their bright seams reveal the construction.
Replace each with one continuous cast Y profile and edge chamfer. Shoulder
lugs now break the silhouette; retain fine tread/sipes/type for normal baking.
The rotor gained a stepped hat; next separate its concentric friction finish.
Tapered painted mirror caps, black cases, support arms and inset glass replace
the boxes. The topology audit correctly rejected two open bezels (32 boundary
edges each); add their physical gauge rather than exempting them.

All eleven views, both contacts and every mask were opened. The preliminary
count was 59,722, before the continuous-spoke savings and bezel gauge. Geometry
checks are source checks only; none prove texture delivery or a moving assembly.

## R2 pass 3 — reject the glazing, retain the construction improvements

Color/value first against `renders/lookdev-r2-03/used-pairs-contact.jpg`: the
factory-gray Ram now retains its color with a bright reflected upper band and
dark lower panels. Carbon reflects a plausible overcast street. The generated
foliage breaks up the formerly smooth blobs, though the parking proxies remain
simpler than the photos. A shadow-catching ground removes the floating cutout
presentation. All sixteen views, all masks, four pairs and five colors were
opened. The satin/marbled material tells are substantially reduced; the unlit
optics and the repeated reflected parked forms still look simplified.

The glass is rejected: it is too pale, with serrations along the upper/side
boundary. Independent probes in `build/cars-lookdev/glass_*.png` separate no
pane, uniform glass, reflection-only, paired inner normals and tint/sky changes.
Uniform glass retains the artifact, so frit is not its cause. Flat inner faces
behind a smooth outer pane create small prisms; pairing the inner normals with
the outer field removes the serrations. A new measured paired-normal check
prevents recurrence. A directional sky gradient and calibrated transmission tint
retain smooth reflected light over a dark interior. A very dark probe was also
rejected because it hid the cabin. The accepted intermediate probe keeps the
headrests and cabin mirror visible. These are source probes, never texture input.

The continuous cast spokes remove branch seams and save triangles. The friction
ring now has concentric turning relief and a separate hat; the stationary
caliper is visible behind it. Shoulder lugs remain within the nominal tire
crown. Grille bar-front recess measures 79.00 mm; the hood/surround sampled
surface gap is 4.75–7.78 mm. The grille field's overly wide diamonds are reduced
to roughly 29 mm horizontal pitch for the final repeat. No silhouette triangles
are spent on that repeating detail. Game count is 59,162, with 838 spare.

## R2 pass 4 — close the header and correct highlight rolloff

Color/value first against the final `renders/lookdev/` Ram and Ford pairs:
retain the gray/black paint's own color, pale horizon band, dark lower panels
and clear-coat reflections. The tinted windshield is darker than the body and
still shows the seats/cabin mirror. Its inner normals are now paired with the
outer field, instead of a smooth entrance and flat faceted exit. Hiding the
headliner alone did not remove all upper-edge artifacts; hiding the roof did.
A matte inside roof, an extended headliner and an actual header-trim ribbon
close the exposed interior header. Surface crossing tests measure zero
windshield/headliner and windshield/header-trim intersections at both densities.

The initial full-size trial clipped small Porcelain highlights (about 0.13% of
paint samples). Rejected that lighting: broadened the key, both rim strips and
overhead card at the same power, reducing reflected source luminance. A five-
color 1000 px test has zero paint samples at 254 or 255 in every color. The
full-resolution side view then exposed a separate hot reflection. Its review
exposure is now −2.8 EV (other studio views −2.0 EV; photo exposures remain
the calibrated −0.8 EV). The side preview has zero paint pixels at 254 or 255.
The consistent 1500 px / 80 sample repeat below supplies final tonal values.
Lit emitters may saturate; paint must retain rolloff. Floor pixels never enter
the vehicle/paint distributions.

Final game geometry is 59,266 triangles, including 104 for the new header trim;
the high source is 203,650. No UV, bake or export was run. The material plan is
unchanged: four delivered surfaces sharing one 2048 three-map set for all five
colors, about 16 MiB compressed including mips. The source has 33 manufacturing
materials and six original generated images. Their complexity is not the final
draw-call count or a delivered texture allocation.

Remaining CG tells: the procedural parked forms and foliage supply less complex
reflections than the photographed locations; unlit optics are simpler than
production lamp tooling; the silver wheel faces, glass header and interior remain very orderly.
Some of the finest chips, wash swirls and tire lettering will be vulnerable to
the eventual 2048 bake. Do not call this photo-indistinguishable or delivery-ready.

## R2 measured checkpoint

`make -C cars WIDTH=1500 SAMPLES=80` — **PASS**. Root log:
`build/cars-lookdev/round2-final.log`. `make -C cars check` — **PASS**;
`build/cars-lookdev/round2-check.log`. These are source-stage budget, manifold,
scale, rest-position, normal, calibration and static assembly checks. They do
not certify motion, UVs, baked materials or a GLB. `kit/test_vehicle.py` and
`python3 -m unittest kit.test_fonts` pass. The portability scan of tracked
cars text contains no machine-specific directory paths.

All sixteen final Cycles views, every mask and all four pairs were opened;
front/wheel close-ups and both full-size dated Ram pairs were also inspected
individually. One source SHA and one render-recipe SHA cover the complete set.
The review script now rejects mixed recipe hashes as well as mixed sources.

| View | Vehicle display luminance P1 / P50 / P99, 0–255 |
| --- | --- |
| Front 3/4 | 0.0 / 48.6 / 233.2 |
| Rear 3/4 | 0.0 / 45.0 / 129.7 |
| Side | 0.0 / 18.0 / 191.3 |
| Front detail | 0.0 / 21.5 / 236.9 |
| Wheel detail | 0.0 / 48.7 / 125.1 |
| Five-year front pair | 0.0 / 42.2 / 149.5 |
| Five-year rear pair | 0.0 / 44.3 / 146.6 |

No studio or factory-color paint pixel reaches 255. Porcelain has one pixel at
254 (0.000731% of its paint samples). The sunny Ram front pair has one clipped
paint glint (0.000410%); do not hide it by counting the floor. The lit lamps
clip 0.3544% of vehicle samples, intentionally in the emitters. Cavities and
underside retain deep shadow. The complete percentiles/channel statistics are
in `renders/lookdev/tonal-range.json`; these display statistics do not measure
albedo. The Ram match remains darker/more neutral than its photograph, and
its reflection scenery remains less varied. These are remaining look-dev limits.

Final measured counts: **59,266 game / 203,650 high triangles**, **33 source
materials**, **6 original source images**. High/game source files are
**2,351,970 / 1,025,142 bytes**, ignored and rebuildable. The planned four
surfaces and shared BaseColor/Normal/ORM 2048 set remain about **16 MiB** with
block compression and full mipmaps for all five colors together. No delivered
GLB size or baked texture allocation is claimed.

Source geometry audit SHA: `802e4a5ce93a2ad1c7c75be7ecce3bd2174505b625bdfe4d77541c8a8ccade3c`.
No preliminary docs images or generated build outputs were committed. Shared
kit additions are opt-in daily-driver finishes (caller-supplied rail/cargo
bounds) and a turned-rotor shader; old defaults remain available. Nothing is
needed from the lead before this source checkpoint review.

## Earlier round — archived source checkpoint

# Alder C150 / detail and look-dev review

**Current gate: source detail and procedural look-dev. Stop before bake.** The
lead accepted round 3's broad form and requested the three corrections below.
The older form reviews are retained under the archived record; their earlier
stop instructions describe those historical gates.

Current evidence: source contact (`renders/lookdev/contact.jpg`),
used front pair (`renders/lookdev/aged_front-pair.jpg`),
used rear pair (`renders/lookdev/aged_rear-pair.jpg`),
front close-up (`renders/lookdev/front_detail.jpg`),
wheel close-up (`renders/lookdev/wheel_detail.jpg`),
five colors (`renders/lookdev/five-colors.jpg`) and
corrected stripes (`renders/lookdev-form/stripes_side.jpg`).
All sixteen source views and the masks are opened in the complete sheets;
close-ups and both full-size pairs are also inspected individually. Comparison
photographs remain credited, read-only references, never texture inputs.

## Pass 1 — correct the accepted form and reserve a detail budget

Color/value first: retain neutral clay and dark cavities, comparing reflected
bands rather than trying to match the white reference paint. Ford's calibrated
front/rear/profile and the independent Ram comparison establish class language;
the original grille, lamp signature and sculpting stay distinct.

The lead's flare criticism was correct. The earlier field had its extremum
inside each panel, making closed elliptical rings. The replacement starts at
its maximum on the squared arch lip and decays outward through the draw.
`renders/form-fixes/` first established open arch-following stripes. Current
`renders/lookdev-form/` repeats the corrected game-sampling clay, orthos, overlay
and calibrated clay-with-stripes pairs. Surface rays measure 33.28 / 33.24 mm
of front/rear draw 10 mm above the crown, persisting above 2 mm through
165 / 180 mm. Those are measured surface differences, not the flare control
constant. The 893 mm crown and nominal tire/contact dimensions stay fixed.

The lower section now has a broad, monotone tuck instead of a tight reversing
radius. Cab and bed lower skin edges share 578 mm height. A fixed sill follows
the lower door's section with a measured reveal, rather than leaving an overly
large black gap. The headlamp seat now evaluates the same wrap and terminal
side tangent as the fender, ending 2 mm inboard. Paint closes the upper/lower
corner around that opening; a dark slab is no longer attached outside it.

Budget was planned before detail in LOOKDEV_PLAN. Flat sheet grids, hood/roof
rows and the redundant tire profile were reduced first. The first corrected
form source was 44.4k triangles; the final detailed source is 55,758 versus the
previous 66,904 before detail. Curvature and silhouette stations retain rows;
analytic outer normals are independently compared with surface derivatives.

## Pass 2 — reject pale, dirty-looking paint and coordinate errors

Color/value first: `lookdev-01` looked like pale blue metallic plastic. That
miss was obvious beside the used black-truck photographs' deep tires/cavities
and dark paint. Do not make the factory tint artificially black to hide a
lighting or construction error.

The initial studio orientation spread bright reflections across most panels.
More seriously, a rest-coordinate attribute was captured before Blender updated
parent transforms. A door's hinge-local coordinates were mistaken for world
positions, putting road sediment across the entire door. The field looked
like brushed dirt instead of a painted panel. After attaching and updating the
dependency graph, the stored positions agree with every actual world-space
vertex to the recorded precision. `check_detail.py` now checks that on both
source densities. The striped and finished views separate true surface flow
from those material errors.

Rebuilt all six original marking/relief sheets, using fictional Alder and Noto
Sans. Paint now combines a factory tint with an independent contamination
term; coverage and contamination are exposed separately for the planned shared
RGBA atlas. Dust keeps its brown/gray hue when the factory color changes.
Road film also reduces coat weight and raises coat roughness where it sits.

## Pass 3 — reject placeholder construction in the front and wheels

Color/value first: black plastic needs a matte charcoal response, chrome needs
a shaped environment and hard reflections, and rubber must remain darker than
the alloy. The first wheel/front close-ups had too much uniform polish and
optical distortion to pass as photographed manufactured parts.

The new wheels use six split spokes, real barrel depth, six hex lugs and a
center cap. Rotors and non-spinning calipers are actual separate construction;
the four corners average 2,910 triangles including the 275/65R18 carcasses.
Tread blocks, sipes and fictional sidewall type are source height fields, not
extra triangles. Brake dust accumulates toward the inner wheel/rotor zone with
fine breakup; the first blotchy barrel version was softened. Knuckles/spindles,
shock mounts and the spare's cable connection now support what low views reveal.
Measured hub/spindle and hanger/frame intersections supplement the clearance
measurements. They do not constitute a full mechanical simulation.

Headlamps now contain reflector cups, two projector optics, emitters and an
original angular DRL signature. Their sealed backing prevents seeing body
edges through an empty hole. The protective lens has 2.6 mm thickness without
a sheet-metal return that refracted the internals into a sawtooth pattern.
Its terminal tangent is shared with the fender; upper/lower painted corner
closures remove exposed gaps. Vertical rear lenses, reverse optics and an
upper brake lamp have unlit and lit construction. The grille's diamond field
is original generated relief behind two chrome wings. Mirrors have a sail,
fold pivot, curved housing and separate glass; the nose gained more profile
stations after the initial housing still read too much like a rounded box. The narrow
front section also needed its corner radius constrained to the section width;
an actual section-convexity check now rejects folded profiles.

The interior uses five seats, formed cushions/backrests, a dash/console and
steering wheel, door cards and a headliner. Early hanging visors looked like
large slabs in the windshield; they are now stowed under the roof. Rear plate,
tailgate type and instrument faces were corrected to their viewing directions.

## Pass 4 — use the actual daily-driver photographs and reject hidden spikes

Color/value first: Carbon is compared with used black trucks, rather than
judging Atlantic blue against white catalog paint. `lookdev-used-01` used the
studio environment and a large windshield reflection hid too much. The current
pairs use a procedural sky, gray ground and original distant reflection
geometry. No photograph/HDRI enters that environment. Black paint keeps dark
base regions and reflected highlights; it is not raised to gray to imitate
an outdoor exposure.

The camera fit uses wheel hubs/contacts and a disclosed low-weight roof-height
anchor for the partly occluded front photograph. Native-image RMS is
43.84 / 24.73 px, about 12.3 / 7.0 px at the 1500 px comparison render width.
The independent Blender projection check agrees within 0.003 px. These are
registration estimates, not evidence that body shapes or materials match.
The references also have different wheel/trim configurations. The Ford pictures were taken in their model year and cannot substantiate
five-year aging. Added the matching front photograph of the existing MY2017
Ram reference: both were taken in September 2022. Its front/rear class fits
have 18.90 / 21.20 native-pixel RMS, roughly 5.8 / 6.0 px at 1500 px output.
Physical EXIF focal lengths are available, but crop/sensor framing is not
calibrated; the estimated cameras and wheel/trim differences remain disclosed.

The close-up found a genuine geometry fault: narrow sheet returns combined with
an even-offset solidify miter produced nose needles and an approximately 49 mm
cowl offset from nominal 0.9 mm sheet. The topology audit alone did not catch
that. Cars now use normal thickness offsets, and a new independent paired-vertex
measurement bounds every gauge offset. Both source densities pass within 0.02%
of specified thickness. The cowl/header no longer acquire those spikes.

The Ram pairs rejected the initially clean tire sidewalls and weak rocker
film. Increased dust value on the exposed sidewall annulus and broadened the
broken low sediment mask, preserving tread rubber and upper paint. Added
procedural sunlight for the outdoor condition comparison. The low view also
rejected the flat unsupported skid: it is now a bent sheet on two measured
frame supports. Driver controls are on the +X side for the front-facing −Y
vehicle. Broken low road film and aft-of-wheel splash are visible in the full side/front
views; tailgate wake streaks and bed drag scuffs have their own causes. The
upper paint stays its factory color. The dated Ram is the condition authority; the newer Ford photographs are
retained only as supplemental reflection and class comparisons.

## Pass 5 — tonal range and final source review

Color/value first: the test hero retained dark cavities but clipped a small
patch on the hood's reflected strip. Lowering exposure alone did not solve the
source luminance. Wider rim-light diffusers removed that clip in Atlantic;
white/silver then exposed a further rolloff issue in the five-color check.
Frit now sits behind smooth outer glass rather than changing its outside
roughness into a broad white band. The final lighting/exposure is checked with the same rig across all five
presets. The measurements use opaque-geometry and paint-only masks, excluding
the floor and background. Display luminance does not measure paint albedo.

The full source checkpoint includes front/rear 3/4, side, front and wheel
close-ups, lit front, interior, two five-year condition matches, two supplemental Ford matches and five factory colors.
The paired photographs still look more complex and less orderly than the
source. The largest remaining CG tells are these:

- Glass/frit and painted window surrounds can form broad bright strips under
  studio reflections. Factory privacy tint is present, but its response and
  the seal transitions need delivery-stage scrutiny.
- Lamp internals remain sparse compared with real molded optical jewelry;
  the unlit black housings are especially simple. The original signature reads,
  but does not make the openings production-quality close-ups by itself.
- The split wheels have real depth, but the alloy close-up is too streaked and
  shiny compared with the production-wheel photographs; spoke transitions remain regular;
  shoulder tread has a smooth silhouette and relies on height/normal shading.
  Fine tread, grille relief, frit and type may lose definition at 2048.
- Wear reads most strongly on low panels and the tailgate. Upper panels and
  interior still look unusually even; bed use is less obvious from the low rear
  hero than in a dedicated bed inspection. Do not call this photo-indistinguishable.
- Underbody construction is deliberately coarse. Full hinge/steering sweeps,
  caster/SAI and rolling loaded-tire behavior remain unverified. Static fit
  checks prove only the stated positions and surfaces.

No bake, UV preparation or GLB has been run. The next gate must implement and
verify the packed paint decode and GLB fallback, preserve glass/emissive states,
finish motion validation, and compare the exported/baked result with these source
pairs. The four-material, shared-three-map 2048 plan is about 16 MiB compressed
with mips for all five colors together; no delivery allocation is claimed yet.


## Measured checkpoint evidence

`make -C cars WIDTH=1500 SAMPLES=80` — **PASS**. Repo-root log:
`build/cars-lookdev/checkpoint-final.log`. It rebuilds the source gate from
scripts, runs both-density audits/form/static checks, projects the four calibrated
cameras, and renders sixteen Cycles OptiX views through the shared GPU lock.
All sixteen have one current source SHA and one render-recipe SHA. The contact,
individual close-ups, four pairs and all masks were opened after this build.

`make -C cars form-diagnostics PASS=lookdev-form WIDTH=1200` — **PASS**. Repo-root log:
`build/cars-lookdev/form-final.log`. This retains separate clay/game-sampling
orthos, reflection diagnostics, axle-registered side overlay and calibrated
clay-with-stripes pairs. It is not a paint or baked-asset review.

`make -C cars check` — **PASS** as part of the full checkpoint; source-stage
geometry and repository checks only. Actual game/high triangles are
**55,758 / 208,090**, source materials **33**, original source images **6**.
Current high/game blend sizes are **2,429,036 / 1,046,911 bytes**, ignored build
outputs. No UV/bake/export/delivery verification is claimed. Body dimensions
measure **5889.46 × 2029.57 × 1960.88 mm**, wheelbase **3683.00 mm**, track
**1716.00 mm**, bed floor **1704.34 mm**, sampled door gaps **4.500 mm**, lower
sill reveal **4.924 mm** and cab/bed gap **16.000 mm**. Lowest actual underbody
surface is **226.00 mm** above ground.

The source static tests measure 19.00 mm caliper/spoke axial separation,
caliper-vertex/barrel-surface samples >=15.58 mm, unbroken convex mirror sections,
normal sheet offsets and actual support intersections. Front skid/differential
and halfshaft/strut surfaces have zero crossing triangles at the parked pose.
These are stated geometric tests, not a full motion or continuous clearance proof.

A separate game regeneration and `kit/audit.py` produce the same evaluated
geometry/transform/triangulation SHA:
`19bb39bf95566b57eb5163fa18c5069590beb40f3529cafb71b5944db763811a`.
`build/repeat-check.json` records that limited proof. Independently generated
original marking/relief PNGs match all six source-sheet byte hashes.
`kit/test_vehicle.py` — **PASS** for legacy/reduced tire bounds/contact,
triangle reduction, invalid profile rejection, analytic panel normals and manifold
gauge. Source and staged repository checks and `git diff --check` pass.

Display-referred tonal measurements, excluding the floor/background:

| Source view | Vehicle luminance P1 / P50 / P99, 0–255 |
| --- | --- |
| Front 3/4 | 0.0 / 62.4 / 231.9 |
| Rear 3/4 | 0.0 / 56.4 / 163.4 |
| Side | 0.0 / 37.1 / 222.3 |
| Front detail | 0.0 / 30.5 / 239.9 |
| Wheel detail | 0.0 / 55.6 / 120.4 |
| Five-year front match | 0.0 / 83.7 / 216.9 |
| Five-year rear match | 0.0 / 75.7 / 228.6 |

No paint pixel reaches 255 in any of the sixteen views. Porcelain has one
paint pixel at 254 (0.00074%). Cavities, wheel wells and underside retain deep
shadow. Very small chrome glints still clip: 0.124% of front-hero vehicle pixels
reach 255, versus 0% of its paint. This remains a tonal weakness to watch;
it is not hidden by counting the bright studio floor. The complete percentiles,
channel clipping and shadow fractions are in `renders/lookdev/tonal-range.json`.
These lit-pixel statistics do not establish albedo or final GPU texture memory.

The measured images are under `renders/lookdev/`; corrected form evidence is
under `renders/lookdev-form/`. No preliminary docs JPG, blend, downloaded
reference, texture or export is committed. Shared kit changes are additive
source vehicle finishes and optional reduced tire profiles, with the legacy
primitive fixture still passing. No additional tool or install is needed.
The lead's next review should focus on glazing/seal transitions, the sparse
unlit optics, alloy response, and whether the dated condition pairs show enough
use before the delivery-stage work begins.

## Archived form-gate record

### Alder C150 / historical body-form review gate

**Stopped before detail, materials, wear, UVs, bake and export.** This is a
reviewable source checkpoint, not a finished or game-ready delivery claim.
The primary evidence is the contact sheet (`renders/checkpoint/contact.jpg`),
front pair (`renders/checkpoint/match_front-pair.jpg`),
rear pair (`renders/checkpoint/match_rear-pair.jpg`), and the
striped side (`renders/checkpoint/stripes_side.jpg`).

Every rendered view was opened, individually or in a sheet of every view of its
pass. The comparisons are against the credited photographs, not memory. All
meshes and shader/light data are original scripts; photos are comparison only.

## Third checkpoint — fresh-eye form review

The second checkpoint's dimensions did not rescue its flat slabs, narrow
attached flares, blocky header or square rear roof. That rejection was right.
This round changes the surface construction, not the detail level. Ford stock
front/rear/profile photographs and the independently credited Ram rear photo
were opened and compared. The Ram check favors its broad integrated draw and
rounded rear cab; the Ford check supplies the calibrated cameras/profile and
crisper shoulder. Grille, lamp openings and sculpting remain authored originals.

### Pass 1 — replace the slab and attached flare (A–C)

Color/value first: neutral gray clay is deliberately darker than the white
reference. Retain black tires and cavities; compare the surface gradients,
not the paint brightness. Do not increase exposure to disguise defects.

The first replacement (`renders/round3-a/`) made a broad flare but was rejected:
its 94,052 triangles were excessive, the shoulder sampling wavered, and formed
bumper returns folded through themselves. Those folds produced extreme spikes
in both views and measured bounds. Pass B fixed the bumper but exposed another
fold where a shoulder support station crossed the sloping hood cap. Pass C
made the fender shoulder parallel to the hood and removed that inversion.
These debugging images are not review candidates.

The new body uses a fair Hermite side section and one shared flare field,
trimmed by a squared opening. The old 67 mm annular lip skin and height fade
are gone. Physical support rows follow the lower die line; upper ruled fields
use fewer longitudinal rows. Gauge normals are still restored after evaluation.
An independently rebuilt previous source supplies the numerical baseline;
`build/cars-round3/baseline-evidence.json` is ignored diagnostic evidence.

### Pass 2 — measure the front and greenhouse (D–H)

Color/value first: dark glazing remains a solid form proxy. It must not conceal
a raised header; striped paint surfaces reveal that junction independently.
The photo's white albedo does not justify making our clay pale.

`renders/round3-d/` through `round3-h/` compare the same axle-calibrated profile
and unchanged chassis-fitted 3/4 cameras. The hood leading center fell from
1301 to 1234 mm. Sampled profile excess dropped from 66/57/52 mm to 6/11/20 mm
at the three hood stations. The grille face now rakes 5.71 degrees, with a
35 mm proud surround; headlamp form wraps 337 mm around the corner instead
of the old 28 mm fore/aft span. The formed bumper has a blocked intake and its
own lower valance. Its envelope stays fixed.

Removed the separate windshield-header bridge. Glass and roof share the start
of a curved canopy surface; actual top-edge distance to the roof is 1.14 mm,
versus 52.17 mm before. The outer A-pillar is 34.90 degrees above horizontal,
inside the photograph's 34.4 +/-1.5 degree estimate. The roof is rolled across
its width, rounded in plan and about 15 mm narrower per side at the rear.
Its rear center drops 88 mm below the retained 1961 mm peak, rather than 4 mm.
Rear roof silhouette excess improves from 34/72 mm to 0/26 mm at the two
inspected rear stations. Front/middle roof excess remains 54/37 mm. The fixed
4x4 envelope and the photo's published 4x2 caption are disclosed, not fitted away.

### Pass 3 — reject scalloped reflections and coincident frames (J–M)

Color/value first: increased stripe frequency and lower diagnostic roughness
make small reflection defects visible. Keep the clay substrate visible and
highlight rolloff controlled; this is not a paint or clear-coat approval.

The sharper diagnostic rejected the initially narrow flare fillets: their
bands scalloped above the openings. Broadened the tangent joins and kept the
lower die line straight through the trimmed arch instead of fading it by
longitudinal distance. `round3-k/` has smooth broad arch bands and continuous
lower stripes, without the previous collapsed annular ends. Opening width at
the rocker is now 995 mm versus 886 mm before; at 80% rise its width/full-width
ratio is 0.747 versus 0.627. The 893 mm crown and 90.3 mm tire-top gap stay fixed.

Actual surface rays measure approximately 35 mm flare over the same-height
door section, spread through 195–225 mm above the opening (old draw: 55 mm).
The door's measured crown is 6.26 mm over its 820–1200 mm vertical chord
(old side: effectively zero). These are mesh measurements, not the flare/crown
parameters printed back as results. They establish broad shape, not artistic
fairness by themselves.

The window-frame artifacts had a construction cause as well as a normal
cause. Fixed roof rails overlapped the door sash skin. Sparse long sash edges
also cut across the cab's nonlinear rear taper: one surface ray found the rail
3 mm outside the sash. Inset the fixed rail, add shared perimeter stations,
and give returns geometric normals. Three actual ray samples now put the sash
1.64/2.47/2.49 mm outside the rail. This proves those sections, not whole-door
motion clearance. The fixed rear cab corner follows the authored door outline
with its gap, rather than leaving an uncovered wedge.

### Latest judgment and remaining weaknesses

The broad sides now carry a soft crown; the opening is wider and squarer; the
flare reads as part of the stamping. Hood and rear roof silhouette differences
are materially smaller in the unchanged overlay. The header no longer stands
up as a block. The front has a raked face, proud grille opening, corner-wrapped
lamps and a formed bumper, rather than stacked plain boxes.

The form still falls short of a product photograph. The lamp/fender/brow
junction is blunt, the front bumper ends remain mechanically coarse, and the
sash/A-pillar/roof-rail corner reflections are less clean than the broad skins.
The stripe islands over the convex flares are expected reflection turns;
small compression where the lower line meets the opening still deserves the
lead's scrutiny. I do not claim every corner is automotive Class A surfacing.
The rear gate is restrained and plain; adding badges would not improve its form.

The side photo still ends 124 mm before the fixed front bumper and 46 mm before
the fixed rear bumper after axle registration (+/-20 mm picking uncertainty).
Those mismatches remain visible. Changing them would change the envelope or
axle locations the brief explicitly holds. Photographic perspective/configuration
uncertainty is not a proof that this discrepancy is harmless.

Camera RMS is still 5.69/5.11 px on five chassis anchors. Marked body landmarks
in `match_front_stripes-measurements.jpg` and the rear equivalent disclose much
larger differences (see `form-comparisons.json`). They are held out of the solve
and carry +/-14 source pixel pick uncertainty and approximate correspondence
between original designs. Low chassis RMS is not an all-body fit certificate.
The two-make sheet is explicitly unregistered. No photograph enters Blender,
a shader, a bake, or the geometry evaluator.

The game source is **66,904 triangles**, leaving only 3,096 below 70k. Tires and
rim barrels use 80/48 circumferential samples, preserving measured dimensions.
Further optimization is required before the interior, brakes and underbody
can fit. Six diagnostic materials, zero textures and no GLB remain intentional
at this source form gate. No detail, paint, wear, UV, bake or export work follows.

### Third-checkpoint proof and files

- `git merge main` — already up to date at pickup.
- `make -C cars clean` then `make -C cars WIDTH=1600` — **PASS**, clean scripted form rebuild.
- `make -C cars check` — **PASS**, source topology, bounds, normals, budget, bed/gaps,
  measured form features, sampled rail/sash separation, camera projection and
  repository policy. This does not certify UVs, a GLB or moving-part clearance.
- Independent game regeneration and kit audit compare actual geometry,
  triangulation and transforms, separately from `.blend` serialization bytes.
- `git diff --check` and tracked-file policy are checked before commits.

Current source bounds, per-part counts, hashes, ray measurements and normal
errors are in `cars/build/form-check.json`. Final checkpoint images are under
`cars/renders/checkpoint/`: front/rear clay, dimensioned side/front/top, two
striped views, two clay photo pairs, two clay-with-stripes photo pairs, their
marked body measurements, the 50% side overlay, measured silhouette sheet,
two-make comparison, rake sheet and **contact.jpg**. Tone statistics and camera
calibration overlays sit beside them. Build logs and repeat proof live under
`build/cars-round3/`. All rendered views were opened individually or in sheets;
stripes and photographic pairs were also inspected at full size.

Final measured bounds are **5889.46 x 2029.51 x 1960.88 mm**, with 3683.00 mm
wheelbase, 1716.00 mm track, 1704.34 mm bed floor, 4.500 mm door reveals and
16.000 mm lower cab/bed separation. Broad-skin normal agreement samples 5,622
corners with maximum 0.0343 degree disagreement; that checks encoded normals
against the section slope, not artistic fairness. High/game sources contain
163,572/66,904 triangles and occupy 1,515,798/732,474 bytes (ignored blends).

The repeat audit matches geometry, transforms and triangulation SHA-256
`651eddfe492ce66247391afa3816fc27df4109dd8e87bd04ef0f3e6783740626`.
`repeat-check.json` also verifies all eleven final rendered views and the form
report refer to the current source hash. Orthographic foreground p5/median/p95
values are side 24/123/158, front 9/51/143 and top 28/119/155 (0–255), with no
bright-clipped pixels. These are clay diagnostics, not paint/hero approval.

No shared kit changes, downloaded tools or new permissions are needed. No
preliminary docs images or generated assets are committed. Stop for form review.

## Historical second checkpoint — superseded by round 3

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

Latest evidence: all views (`renders/checkpoint/contact.jpg`),
side overlay (`renders/checkpoint/side-overlay.jpg`),
rake measurement (`renders/checkpoint/side-rake.jpg`),
front pair (`renders/checkpoint/match_front-pair.jpg`),
rear pair (`renders/checkpoint/match_rear-pair.jpg`),
front stripes (`renders/checkpoint/stripes_front.jpg`),
side stripes (`renders/checkpoint/stripes_side.jpg`).

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

## S240 R6 — form corrections, detail and coating checkpoint

### Detail pass 1 — reject floating construction and closed lamp backs

Color and value first: the first Atlantic preview had a dark, nearly uniform
side and an oversized pale windshield reflection. The dark glass itself had the
right transmission direction, but the reflection hid the cabin; the paint had
too few useful reflections to establish a continuous clearcoat.

`renders/sedan-look-pass1/` is rejected. The door-card rectangles crossed the
accepted compound door sections; they now follow measured sections of the
actual door and sill. The optical backing was in front of its guide/module;
it was rebuilt as a return and a recessed backing. Mirror supports, handles,
wipers and washer nozzles are seated by rays against the actual supporting
surfaces. Construction and collision checks are independent of serialization.

### Detail pass 2 — reject optical chords and the dark outdoor stage

Color and value first: `renders/sedan-look-pass2-pairs/` was far too dark and
blue beside the used gray class car. It also accidentally used the source's
Atlantic default. That pair cannot support an albedo claim. The factory preset
is now explicit for paired views. No color was sampled into a material.

`renders/sedan-look-pass2/` exposed long lens triangles passing through the hood,
folded tip cells, and needle-like optical returns. A normal-offset Solidify
replaces the unstable even-offset return; a feature-aligned strip replaces the
headlamp's unconstrained convex-hull triangulation. An attempted global
refinement cost thousands of triangles and was discarded. Local A-foot,
C-header and lamp-crest samples fund the requested reflection-flow correction.
The original exterior positions and normals are locked during hidden sheet-back
reduction; fine tire lugs move to the normal bake.

### Detail pass 3 — reject empty optics and calibrate the comparison stage

Color and value first: `renders/sedan-look-pass3-pairs/` still reflected mostly a
blue sky and lit the front from the wrong side. The used-car photographs have
warm low facade reflections and clear direct sun. The sedan-specific stage now
uses procedurally built facade reflectors and the observed sun side, leaving
the pickup's lighting unchanged. `renders/sedan-look-pass4-pairs/` overshot
brightness; the exposure, sky strength and facade values were reduced again.
This is lighting calibration, not a change to the family's factory color factors.

Two supposed far-wheel ground picks were actually bumper edges: those wheels
are occluded. They were removed. The four visible near-wheel hub/contact picks
now give 12.25 / 13.49 native-pixel RMS (front / rear), about 3 pixels at 1100 px
comparison width. This proves camera registration only, not body agreement.

`renders/sedan-look-pass3/` shows a smooth coat response, but still-empty black
headlamp housings, no readable road film in Atlantic at full frame, and rear
cover tip folds. The projector/guide clearance was increased, reflector backs
were given a metal response, and the low/behind-wheel film was strengthened.
The rear cover requires an outermost-surface ray: nearest-point inversion of
the rolled quarter chart selects an inward-facing fold near its narrow tip.
It must pass surface-normal, topology and motion checks before baking.

The source support sweeps already cleared all four wheel revolutions and both
full ±35° steering ranges at coarse sampling. Closed mirror throats and rear
liner/door contacts were corrected geometrically. These previews and coarse
sweeps are working evidence, not the final exported-GLB checkpoint.

### Detail pass 4 — reject the first delivered bake

Color and value first: the first exported Atlantic hero had opaque black
streaks on the low rocker and red contamination in a white running guide.
Those were projection errors, not intentional wear. The roof and A-pillar
reflections also exaggerated local waviness. `renders/sedan-delivery-rejected1/`
and `renders/sedan-pairs-rejected1/` are rejected delivery evidence.

Every manufactured part now has its own projection group. The high shoulder
blocks join the tire source rather than inheriting an exploded frame twice.
Independent partwise barycentric rays expose correspondence loss on thin backs,
optical returns and tire shoulders. Exact game-surface procedural RGB/ORM replace
the contaminated high-to-low channels; normals from the high source are used
only for independently verified parts. The source's already transferred dense
parent normals remain on the low exterior. This fallback is explicit in the
bake report, rather than calling all high geometry successfully baked.

`renders/sedan-delivery-pass2/` removes the black/red projection defects but is
still rejected: atlas coverage 27.5% fails delivery policy, and its projector
was hidden by actual fascia geometry. A source camera ray proved the cover,
fascia, then optic ordering. The projector was moved into the swept aperture;
new rays encounter cover, optic, housing, reflector in that order. Convex UV
packing and a 0.001 atlas margin now recover more than 35% coverage without
zero-area triangles. No verification minimum was weakened.

### Detail pass 5 — reject chart doors and protruding hinges

Color and value first: source previews still had conspicuous dark triangles
at the shut lines. Hiding the hinge hardware made them vanish; they were actual
leaf protrusions through the curved closed door, not grime or a paint-normal
problem. The source's first door chart also carried the low sill when opened.
`renders/sedan-physical4-preview/` and `renders/sedan-no-hinges-debug/` expose
these errors and are diagnostic/rejected.

The physical sill is now cut from the same sheet at 300 mm; front jamb channels,
inner B-posts, sill beams, pins, hollow barrels and stamped leaves form supported
assemblies. Inclined axes follow the leading door section. Leaves start on the
inboard side of the barrels and end inside the actual door skin. Card bottoms
clear the rear arch. Front doors open 60°, rear 68°; the selected ranges clear
the real neighboring surfaces. The jamb bends aft of the steered tire and avoids
the hood support. No hinge-collision allow-list exception was introduced.

The first inclined-node export passed vertex serialization but failed its width
check: transforming a rotated local AABB overstates the unchanged actual door
vertices. The final nodes retain vehicle-coordinate mesh frames and explicit
custom hinge-axis unit vectors for quaternion animation. This preserves real
2.105 m width without widening the tolerance or editing the kit. Pin axes are
measured from their mesh PCA, since applied object rotations are not a cylinder's
geometric axis. Both source density sweeps and independent support checks pass.

### Detail pass 6 — compare surfaces and strengthen causal road film

Color and value first: `renders/sedan-look-pass8-pairs/` was too dark after the
sky-only stage was corrected; pass 9 recovered side values but lacked the
used reference's facade reflections. Pass 10 adds a procedurally built tall
facade and a cooler original Graphite option, while the pickup stays unchanged.
The lower film was too clean/uniform. It now follows aft-wheel fans and low
splash, with broken gravity streaks and pale dry dust retaining a distinct color.
The studio hero makes that wear visible at full frame.

The earlier fixed-x appearance patches were not reliable on an inward-turning
lower door. Final patches use ray-measured paint surfaces and Blender camera
pixels, with their projected photo correspondence shown in annotated images.
Small regions avoid silently folding the ground or a sill gap into a paint
median. Display values remain lighting/shape comparisons, not measured albedos.
The final exported-GLB pass and remaining misses are recorded below.

### Detail pass 7 — reject the pale band and reverse tangent normals

Color and value first: `renders/sedan-detail-rejected2/` made the lower car a
pale, continuous band. Its contrast was visible but its cause was unconvincing.
The final road film is lower and darker, with shorter broken splash streaks and
aft-wheel fans. Lower glazing has localized residue; its main viewing area
stays dark, smooth and transmissive.

The same exported pass exposed dark triangular marks absent from the source,
plus blurred center-cap type. Even self-projection can hit a gauge back near a
thin shut-line corner. The final material bake therefore runs directly on the
prepared finalized surface, with no selected-to-active ray. Original object,
generated and print coordinates are preserved before UV operations. Tiny
backward tangent samples explicitly fall back to the neutral tangent normal;
counts remain in the report. This is a bounded detail loss, not evidence that
all high detail transferred correctly.

UV experiments at 8/12/20/35° had more self-overlap and were rejected. The 5°
charts remain, with visible-skin priorities, reduced hidden-back density, larger
marking allocation and 0.0012 padding. No UV tolerance was relaxed. The accepted
preflight `renders/sedan-delivery-pass3/` removes the large black marks and
recovers the ALDER cap marking. Fine sidewall relief still softens at 2048.
The caps now have a 167 × 120 × 96 mm compound envelope and real arm/body checks;
their grazing highlights remain less fair than a molded production mirror.

### Construction follow-up — contact is distinct from collision clearance

The late anchor probe found gooseneck tips 36.5–37.1 mm below the lid. A collision
sweep could pass while those ends floated. The tips now come from actual inner
lid rays, and fixed bearing supports contact the trunk tub. The floor is a
1.2 mm stepped pan over the tank, with real strap returns, exhaust hanger mounts,
front longitudinal rails and engine-mount gussets. Dampers terminate at the
structural wheelhouses. The hubs have actual hollow bores and 31 mm journal
engagement rather than a concealed axial gap. Hex stud caps and cast mounting
gussets save the triangles spent here: the final game mesh remains 59,992.

These independent contact measurements accompany both density sweeps; source
construction and GLB serialization remain separate claims. The underbody is
still a low-detail assembly, with composite joint housings and simple stamped
forms, rather than a service-accurate mechanical model.

### Detail pass 8 — final exported-GLB checkpoint

Color and value first: the studio's first final pass clipped about 1.3% of the
hero's painted pixels. Lowering studio exposure from −1.8 to −2.8 removes that
clipping. In the final front/rear Atlantic heroes, paint luminance p99 is
0.961 / 0.958, clipped paint pixels are zero, and 30.8% / 34.1% of the car mask
falls below display luma 25/255. All ten factory-color hero views have zero
clipped paint pixels. The white option's median paint luma is 0.741 front /
0.726 rear. Outdoor comparison exposure stays independent and unchanged.

The used references are balanced on the stated assumed neutrals: front plaster,
linear RGB gains 0.955 / 0.992 / 1.289; rear background white-car trunk,
0.910 / 0.997 / 1.476. There is no gray card. Actual delivered paint rays define
the render patches; the calibrated photo correspondence remains approximate.
The final display-luma comparisons (render / photo, 0–255) are:

| Surface | Front pair | Rear pair |
| --- | ---: | ---: |
| Upper front door | 140.8 / 148.6 | 124.6 / 120.3 |
| Front road film | 133.5 / 142.5 | 115.1 / 128.6 |
| Rear door | 147.9 / 133.4 | 117.4 / 113.6 |
| Rear road film | 144.8 / 129.3 | 114.8 / 142.8 |
| Quarter | 158.1 / 176.2 | 105.0 / 154.7 |

Median absolute luma difference is **14.0**, worst **49.7** on the rear quarter.
Hue is still too cool: the front upper door is RGB **126/143/162**, versus
**153/147/151** in the balanced photo. These are appearance measurements, not
paint-albedo estimates. The lighting/shape/color match remains incomplete;
particularly the rear quarter and lower rear door lack the photographed
reflection and dirt contrast. The pairs are not presented as a realism pass.

The final source is 59,992 triangles; the high source is 170,032. Direct bake
reports zero unfilled interior pixels in every channel. Of 4,744,395 normal
interior samples, 172 (0.0036%) use a neutral tangent fallback; padding fallback
is reported separately. Verified high-source normals cover 256 parts / 8.64%
of the atlas; the rest uses the direct shader normal over the dense-parent
geometric normal field. Fine lettering and chips soften after the 2048 bake.

The raw/profile/wide/long side overlays remain visible, with worst front/rear
holdout deviations (mm): **118.8/71.8**, **101.2/117.0**, **127.0/131.2**,
**80.0/110.0**. The 40 mm request is not met. The physical tuck/height/departure
requirements pass, and the lower nose/arch seam is faired; neither fact erases
those photographic residuals. Roof/A-foot/lamp-crest stripe continuity improves,
but grazing mirror-cap and C-sail highlights still show waviness.

All final images were inspected, including the 17 standard views, ten factory
views, 25 motion poses, both used-car pairs and the Eevee view. The same exported
GLB SHA-256 is recorded throughout:
`ee972bc7b5ad0a451d01740eae8715ba625d689911402864669cf59c7e115cfe`.
The face and lamp details are readable, the guides change state, glass stays
dark, the human stands beside the car, and the underside has a stepped supported
floor. The cabin remains too blocky, the rear optics and wheel bevels remain
simple, and tiny colored atlas fringes persist on some thin trim edges. Eevee's
screen-space glass shows less cabin depth than Cycles. These remain CG tells.

### Final proof and scope

- `make -C cars BODY=sedan WIDTH=1400 SAMPLES=36` — PASS. Source form evidence,
  prepared direct bake, independently checked high normals, 2048 downsample,
  GLB export/re-import and the full review graph. The final studio exposure
  correction was regenerated through the same render targets.
- `make -C cars BODY=sedan check` — PASS: source density/topology/budget/scale,
  real construction and anchor checks, all 12 game/high sweeps, UVs, geometric
  normals, GLB vertex/pivot serialization and repository policy.
- `make -C cars BODY=sedan check-repeat` — PASS: independently rebuilt master/sill
  and detail scenes, all 405 meshes / 426 objects identical in vertices,
  polygons, corner normals, transforms, parents and material assignments.
  This is not a repeated-GPU-bake byte-identity claim.
- UV coverage **37.06%**, no degenerate/outside triangles, four subpixel overlaps
  totaling about 0.89 shipped texel; p5/median/p95 **83.7/234.5/268.0 px/m**.
- **59,992 triangles**, four material surfaces, three shared **2048²** images,
  **16 MiB** compressed with mips. GLB **12,845,344 bytes**. Vertex/pivot
  serialization errors remain below 0.2 micrometers / equivalent matrix error.
- Direct-surface bake and every Cycles/Eevee view use the shared GPU lock.
  No kit files, generated binary assets, reference photos or final docs images
  are committed. The shared wheel change is isolated in `0ef1aad`; unchanged
  pickup defaults and accepted binary payload are independently verified.

Images: `renders/sedan-detail/checkpoint.jpg`, `contact.jpg`,
`factory-colors.jpg`; `renders/sedan-round6/contact.jpg` and all four side
overlays; `renders/sedan-motion/contact.jpg` and the five sweep strips;
`renders/sedan-used-pairs/used_front-pair.jpg`, `used_rear-pair.jpg`, both
`*-patches.jpg` and `appearance-patches.json`; `renders/sedan-eevee/`.

The checkpoint needs lead review of the unresolved overlay and photographic
polish. The current sedan atlas is separate from the pickup: about 32 MiB for
both, with shared methods rather than shared pixels. Family atlas integration
needs coordination with the other bodies. Possible kit follow-ups are an
opt-in direct procedural bake and bounds measured from actual world vertices;
rotated mesh AABBs can otherwise overstate a correctly exported envelope.

## S240 R7 — corner causes and matched autumn light

### Pass 1 — isolate geometry from shading and lighting

Color/value first: the R6 used-pair stage does not establish paint agreement.
Its connected world was a blue RGB ramp, bypassing its nominal sky texture;
its 51° sun and large reflection rectangles differ from the photographs.
Preserve the wheel-only calibrations and the assumed-neutral white balances.
Rebuild the comparison illumination from a procedural scattering sky, a sun
estimated from the shadow directions/lengths, asphalt and original facade
reflectors where a building is actually reflected. The estimates remain
uncertain lighting fits, not EXIF or measured illumination.

The new diagnostic is the original SUV cotangent/mixed-area kernel from
`85d7450`, adapted without merging that branch. Its analytic checks give
maximum H error 0.000076/m on a 2 m sphere and effectively zero on a cylinder
and plane. Game measurements use actual exterior triangle positions, excluding
open boundaries/gauge; authored normals do not enter them. The fixed color
scale is shared by the entire car and all views. Parent maps are separate.

The hood/lamp crest defect already exists before apertures are cut: its narrow
38 mm high / 55 mm wide Gaussian crown creates a local roll and hollow. It is
first trial uses a broader 22 mm / 135 mm stamped draw (superseded in pass 3).
Control-net relaxation spans the
front corner and rear canopy/side-fit transition at the C-sail foot, before
limit subdivision. No lamp shell deforms the body, and the parent has regular
valence four; an aperture pole or global decimator is not the cause. Cutting
had a second error: inserted points stayed in coarse triangle chord planes
while shading normals came from the dense parent. Those exterior points now
return to the parent before gauge closing.

In this first trial's identical spatial boxes, actual game H ranges (1/m, including design
creases and thin cut triangles) change from front -78.5…1041.5 to -60.8…181.9,
and sail -535.7…565.4 to -156.7…392.5. Sail p5/p95 improves from -70.2/+42.5
to -8.0/+17.1. These numbers show improvement, not globally perfect curvature.
The raw maps still expose discretization at thin cut/arch fragments; they are
not smoothed to hide it. Whole-body maps and both reflection directions are
paired in five views. The trial global edge beautification worsens these maps;
tangential redistribution improves the nose but worsens the sail, so both
experiments are rejected and remain ignored.

### Pass 2 — correct illumination before material factors

Color/value first: sky strength/exposure trials in `sedan-r7-light1` through
`light5` range from pale blue to too dark; neither endpoint is acceptable.
The low autumn sun estimate is 27° front / 30° rear, with approximately ±6°
elevation uncertainty. Source and export comparisons use the same stage.
Studio presentation is independent and retains the family's accepted layout.
The sky texture now actually supplies the world, the sun matches its direction,
and no luminous studio panel enters a comparison reflection.

The existing front Graphite appearance is too cool. Its original factor
0.120/0.130/0.145 becomes a near-neutral 0.130/0.125/0.126; the other four factory
colors and the coverage-delta decoder remain. Matched sunlight exposes overly
pale alloy/tire values and too much transmitted cabin light. The alloy becomes
a darker production finish, radial sidewall dust keeps its cause but drops in
value, and glazing transmission tints darken. Original road film/chips/swirl
masks are retained. Geometry and motion of the accepted cabin, underbody and
optical assemblies are retained.

The radiator-like horizontal blades become seventeen bowed, splayed vertical
vanes over a recessed original diamond relief, in gloss black with the dark
chrome surround and original ALDER badge. The rear plate carries an original
ALDER / WILLOW MOTOR CO. dealer insert and dark frame relief; no jurisdiction,
registration format or serial. A 3× marking priority protects its atlas area.

### Pass 3 — keep the held section while correcting the crest

Color/value first: the direct source and baked preflight remove the cool cast
(the front upper door is 153/150/149 against balanced photo 153/147/151), but
the rear quarter's reflected value still differs. The sun/sky balance replaces
the milky glass and studio rectangles with darker sky and a constructed facade
where the photograph reflects one. Rear facade height is restricted to the
observed low horizon, so it does not paint the roof/backlight beige. Solar
azimuth is refined against the visible ground-shadow direction, front −155°,
rear +155°, in the Blender frame. The neutral-balanced sun color is used for
the already-balanced photographic comparisons.

The longer matched view also shows that the old spray fans fade out before
the rear door. Their existing aft-wheel masks now extend along that door and
have a slightly higher, declining spray ceiling; deposited dust is darker.
The broken grain, low splash, chip and washing masks retain their causes.
Source pair `sedan-r7-film-source` exposes this wear at full frame. The strength
is judged with the final export again below.

The first broadened crest fails the clean build's independent section checks:
its shoulder narrows 1.7 mm and the hood loses too much transverse crown.
That candidate is rejected. The final draw uses a 45 mm / 100 mm crown over
an independently crowned hood, rather than the first 22 mm / 135 mm trial.
Sail relaxation fades in above the shoulder, preserving its widest row.
Actual measured width returns to 1849.39 mm; the hood and other held numeric
requirements pass again. No dimensional tolerance was changed. The regular
parent remains continuous before the openings and panel cuts.

UV projection trials at 3, 4, 4.5, 5.5, 6 and 7 degrees do not solve the thin
fragment chart folds. Keep the 5-degree layout and split only the overlapping
fragments before repacking. A subtexel sliver receives a representable UV
altitude when float packing would flatten it. The preflight has sixteen chart
repairs, zero overlapping/outside/degenerate UV triangles, 36.92% coverage and
83.0 / 232.7 / 298.9 px/m density p5/median/p95. This changes UV seams, not
positions, triangle count or the acceptance policy. Exact-surface baking has
zero unfilled interior pixels. Verified high-normal coverage is recorded
separately from direct shader normals.

### Pass 4 — inspect the grille opening at delivery resolution

Color/value first: raising Graphite metallic from .55 to .80, with both the
current tint and a lighter .160/.150/.155 tint, increases the pale road-film
contrast and makes the clean/deposited transition too pronounced. Reject both
runtime-only probes. The production near-neutral tint and .55 metallic remain.
The source/export paint-patch medians alone do not prove every optical detail
survives the atlas; the diamond relief is visibly softer in the exported grille.

The full-resolution grille close-up exposes two painted triangular teeth
inside its upper right mouth. They also appear in the source, excluding a bake
or glTF-normal cause. Camera-ray picks identify actual exterior fascia triangles,
not grille vanes or reflection cards. The axial aperture cutter classified a
triangle by the distance between its center and an end ray on the dense parent.
At this tight roll the center of a coarse chord lies more than 15 mm behind the
parent while its vertices still belong to the exposed end sheet. The cutter
therefore skipped those triangles. Test the actual vertices as well as the
center; other side/roof branches continue to fail the end rays. The revised
source close-up has a continuous upper grille mouth and no painted teeth.
An independent 5 mm ray grid across the actual mouth, inset 8 mm from its rim,
finds 52 painted occlusions in 8,069 samples on the old game source and zero
on both corrected source densities. This tests the physical opening, whereas
the GLB verifier tests serialization. The new check is in `make check`.
This fixes the cut classification without moving the parent, loosening a
construction tolerance, or changing any pivot/range. The revised game source
is 59,932 triangles, four fewer than the first delivery candidate.

Source and export photo pairs are now both dependencies of the default build.
Their patch comparison is regenerated with the gallery, rather than relying
on an untracked one-off measurement script. Final export evidence follows.

### Pass 5 — retain sky reflection while fitting the rear sun contribution

Color/value first: the .025 sky / energy-8 sun fit leaves the rear upper door
19.8 levels too bright and its rear door 24.7 too bright, although the front
upper door is close. A .05 sky with front/rear sun energies 6/4 overcorrects:
the rear quarter becomes 50.6 levels too dark. Reject that endpoint. The .04
sky and 8/6 sun fit retains the near-neutral front door and improves the rear
doors without altering paint factors. The diagnostic front upper door is
150/148/148 against 153/147/151; rear upper door 125/126/128 against
121/119/131. Ten-patch median absolute displayed-luma error drops from 17.1
to 14.1 levels. The worst is now the differently shaped rear quarter's sky
reflection, 29.4 levels low; that does not establish a paint-albedo error.
The sky/glass reflection is more evident and there are no studio rectangles.
This is the final outdoor recipe. The accepted studio remains unchanged.

### Pass 6 — final exported asset and delivery evidence

Color/value first, at the final 1600 px / 48-sample settings. White balance is
still the stated front plaster and rear background white-car trunk, with linear
RGB gains .955/.992/1.289 and .910/.997/1.476 respectively. These are assumed
neutrals, not gray cards. The sun is estimated at 27°/−155° front and 30°/+155°
rear, approximately ±6° elevation uncertainty, with the connected scattering
sky, asphalt-gray ground and original facade reflectors. Displayed patch
measurements include class/shape/reflection differences and do not measure albedo.

| View / paint patch | Export RGB | Balanced photo RGB | Export / photo luma, 0–255 |
| --- | --- | --- | ---: |
| Front / upper front door | 150/148/148 | 153/147/151 | 148.4 / 148.6 |
| Front / front road film | 162/159/156 | 148/141/141 | 159.4 / 142.5 |
| Front / rear door | 151/149/149 | 137/132/136 | 149.4 / 133.4 |
| Front / rear road film | 159/156/154 | 135/128/126 | 156.5 / 129.3 |
| Front / quarter | 155/154/154 | 168/176/202 | 154.2 / 176.2 |
| Rear / upper front door | 125/126/128 | 121/119/131 | 125.9 / 120.3 |
| Rear / front road film | 135/132/131 | 130/128/131 | 132.6 / 128.6 |
| Rear / rear door | 123/123/124 | 117/112/120 | 123.1 / 113.6 |
| Rear / rear road film | 133/130.5/129 | 144/142/147 | 130.9 / 142.8 |
| Rear / quarter | 127/126/127 | 136/155/207 | 126.3 / 154.7 |

Median absolute luma difference is **14.0/255**, worst **28.4/255**. The cool
base-paint cast is corrected; broad quarter/door reflections remain flatter
and less blue than the photographs. Do not call these a photometric match.
Source/export medians agree within **one RGB level** on all ten patches under
identical cameras, exposure, uniforms and lighting. This narrow measurement
does not establish preservation of every fine detail: grille relief and small
lettering visibly soften in the atlas. Both source pairs and both exported
pairs were reviewed at full frame, along with the exterior close-ups.

The Atlantic front/rear heroes have paint p99 luma **.9605**, zero channel-clipped
paint pixels, and **32.96% / 35.26%** of geometry below 25/255. All ten factory
three-quarter views have zero clipped paint pixels. Cavities remain deep and
the lower road film is visible in the hero. The studio recipe is retained.

Actual game H, in the same spatial boxes as the before mesh, is below. The
statistics include thin cut triangles and authored die creases. No normal map
or shading normal supplies these values; the analytic sphere/cylinder/plane
checks pass. Localized irregularity remains at clipped arch and aperture
fragments, and the front p95 is slightly higher. The maps are deliberately raw.

| Region / version | Min | p5 | Median | p95 | Max, m⁻¹ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Front / accepted checkpoint, 332 vertices | −78.49 | −5.77 | 1.32 | 42.40 | 1041.50 |
| Front / final, 311 vertices | −111.82 | −1.36 | 3.19 | 47.22 | 296.18 |
| Sail / accepted checkpoint, 86 vertices | −535.74 | −70.17 | −2.17 | 42.54 | 565.38 |
| Sail / final, 115 vertices | −62.87 | −7.06 | −2.53 | 16.41 | 256.17 |

The clean build also exposed a separate rear-cover construction error: its
radial sampling ray walked across the trunk's constant-X reveal and put the
moving cover into the stationary quarter. Iterated parent rays now constrain
each cover to its actual side of the reveal, including its 4 mm normal offset.
The trunk sweep has zero measured penetration, with its accepted pivot and
range intact. No new collision exception was added. A physical molded dealer
frame now seats on the insert: maximum measured back-edge distance 0.25 µm
(floating-point error), minimum sampled pocket clearance 2.22 mm. The first
larger-frame candidate failed the unchanged clearance check and was reduced.

Delivery proof:

- Removed generated sedan build, markings, texture, GLB and final render folders
  before `make -C cars BODY=sedan WIDTH=1600 SAMPLES=48`: **PASS**. Reference
  image/PDF cache retained and verified. The removal ledger and complete log are
  `build/sedan-r7/pre-aperture/clean-proof.json` and
  `build/sedan-r7/final-clean-build.log`.
- `make -C cars BODY=sedan check`: **PASS**, including source audits, all 12
  mechanisms on each density, grille aperture checks, independent regeneration,
  fresh GLB import, UV/normals/scale/pivots and repository rules. Repeat matches
  all **420 meshes / 441 objects** exactly; it is not a repeated GPU bake claim.
  Each motion source has **491 poses** at 0.5 mm tolerance. Evaluated hood
  supports have 32 poses, zero penetration, 66.8–283.7 mm member overlap.
- **59,932 game / 171,320 high triangles**, four delivery materials, one three-map
  **2048²** set baked at 4096²: **16 MiB** compressed with mips. Per-part and
  moving-parent counts are in the README and `build/sedan/detail-game.counts.json`.
- **35.75% UV coverage**, six chart splits, zero overlap/outside/degenerate
  triangles; p5/median/p95 **81.8/229.2/278.2 px/m**. The direct bake has no
  missing pixels or backward normals in **4,535,212 interior samples**. Verified
  high-source normals cover **262 parts / 8.78% of the atlas**; other normals are
  the direct source shader/parent field. See the separate bake reports.
- GLB **13,284,352 bytes**, SHA256
  `a20b3b9d80245ffb575479152f18a5945c429f87b9cad85e12882dc05516be62`.
  Fresh import passes every verifier check. All **55** final GLB views use that
  one digest and one presentation recipe.
- Pickup GLB remains byte-identical, SHA256
  `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
  No sedan-specific kit or shared pickup-source change is required.

Final image locations: `renders/sedan-detail/contact.jpg`, `turnaround.jpg`,
`details.jpg`, `factory-colors.jpg`, `scale.jpg`, `checkpoint.jpg`;
`renders/sedan-eevee/front_three_quarter.jpg`;
`renders/sedan-motion/contact.jpg` and five sweep strips;
`renders/sedan-used-pairs/used_front-pair.jpg`, `used_rear-pair.jpg`, patch
annotations and `bake-loss.json`; `renders/sedan-source-pairs/`;
`renders/sedan-panels/*-comparison.jpg` for front/rear three-quarter, side,
front and rear actual-game curvature beside both stripe directions.

All final views, motion poses, five-color views and diagnostic sheets were
visually reviewed, including the five final compressed docs images. `docs/`
adds only `sedan-hero.jpg`, `sedan-rear.jpg`, `sedan-details.jpg`,
`sedan-five-colors.jpg` and `sedan-turnaround.jpg`: 1600 px wide, respectively
109,794 / 105,939 / 186,434 / 196,652 / 126,068 bytes. No blend/GLB, atlas,
reference image or intermediate render is committed.

Remaining CG tells: flatter broad reflections than the used photographs;
localized raw-H sampling speckle; coarse wheel/mirror transitions; simplified
cabin, rear optics and underbody; soft fine lettering/diamond relief; and
occasional colored atlas fringes on very thin trim and gauge. Eevee shows less
nested optical depth and noisier grazing reflections than Cycles. Nothing is
needed from the lead to rebuild or inspect this delivery. A future general UV
minimum-feature allocator could help thin gauge/trim within a small atlas;
this round does not add one to the shared kit.

## S240 R8 — repair the surfaces judged in the finals

### Pass 1 — baseline, causes before correction

Color and value first: opened the delivered hero, rear, details, five-color
sheet and full-size face beside the actual used-front/rear photographs. Keep
the five factory factors, outdoor white balances (front plaster, rear white
background-car trunk), matched sun/sky and accepted studio. The photographic
film keeps the underlying paint hue and has a smooth vertical falloff; the
white/silver delivery instead exposes an irregular high-contrast noise field.
The checked patches did not certify these whole-view defects.

Baseline evidence is preserved under `build/sedan-r8/before/`. The
`build/sedan-r8/no-normal/` experiment renders the same imported delivery with
only the Principled normal connections disabled. Glass tearing and most grille
warping disappear; the canopy rail kink, optical cut, arch spikes and tire
rings remain. This separates bake/material defects from actual geometry.

Causes established before editing:

- Windshield/backlight: their source has no glass height relief, but the direct
  normal bake is not neutral: windshield p99/max tangent deviation .469/3.024
  degrees, backlight .115/.251 degrees. A crisp softbox edge exposes these
  small interpolation/edge errors; removing the map removes the ragged edge.
  The game canopy also has too few transverse chords near the rail. Geometry
  and normal continuity still require inspection independently of this bake.
- Roof/sail: the source canopy controls change spacing and cross crown near
  the header; localized Laplacian relaxation and coarser game canopy sampling
  leave an uneven transition. It survives the normal-disabled experiment.
  The backlight's longitudinal section also changes slope repeatedly. These
  are high-surface/game sampling issues, not merely a texture problem.
- Hood: the normal-disabled face still has broad uneven highlight flow and
  mottled roughness. Source flake/peel is sampled far below the 229 px/m median
  atlas density (2800/m peel, 900/m roughness); a sparse point-sampled bake
  aliases microscopic structure into visible variation. Broad flow is a
  separate parent/control and game interpolation issue.
- Grille: each low vane has sharp rectangular sides while the high source
  adds bevels. Accepted partwise hit coverage does not establish accurate
  shading: vane 08's projected normal has p95 9.64, p99 30.79 and max 77.29
  degrees. It replaces a direct normal with only .053-degree maximum error.
  The 20%-decimated backing has irregular triangles and a 2 mm shader relief;
  that direct map reaches 20 degrees. Both are exaggerated at this density.
- Headlamp outer cut: the chart cutter uses a convex hull over a bent strip,
  and then returns chord intersections by nearest 3D point rather than the
  carried parameter. These operations can select the wrong folded branch at
  the tip. The defect persists with every normal map disabled.
- Film: 35/m three-octave noise modulates the entire deposit, and 7/m noise
  changes its ceiling. The mask's nominal wheel location does not make this
  mottling a plausible spray gradient. Replace its distribution and directional
  streak construction while keeping factory colors and localized gap dirt.
- Tires/arches: the low tire has only 40 angular segments and 11 profile
  stations, with angle-threshold smoothing creating distinct sidewall rings.
  The lettering also inherits the pickup's radius and masks after coordinate
  rescaling, so it is too small/soft in the delivered sidewall. The arch cutter
  clips coarse chord planes, then aperture recuts return all vertices to the
  nearest parent without preserving the circular cut. This moves the lip off
  its intended boundary and leaves thin projecting facets. These are source
  geometry/construction faults, separate from bake noise.

Next: correct each surface/projection by cause, allocate continuous UV charts
and properly filtered shader detail, then repeat the same full-size finals.
The expanded curvature and reflection evidence must include glass, grille,
lamps and arch lips, and must inspect the delivered GLB as well as the source.
