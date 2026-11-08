# Manufactured communities / form gate

The historical checkpoint reviews below are retained. The delivery reviews at
the end judge the five remaining corrections; their visual gate is still open.

This is the form and construction checkpoint. Home finishes are explicit quick
materials; there is no new family bake, finished wear pass, final gallery or
game-readiness claim. Every review render imports the external glTF package.
Native props retain their existing library textures. Photographs remain local
comparison inputs, never materials or committed gallery images.

## Pass 1 — reject the empty common area and cropped component views

Inspected all eight Cycles export frames in `renders/checkpoint/pass1/` at
their native 1000 px: both park heroes/obliques, both home heroes, deck and
carport. Compared the form directly with the 2009 used single-wide, 2007
older-community photograph, 1974 DOCUMERICA row and 2015 oblique aerial in
`refs/`. The first contact is `renders/checkpoint/pass1/contact.jpg`.

**Color and value first.** The photographs' nominal white storm-door frame
(2009), porch fascia (2007), white metal roofs (1974 film) and aluminum pans
(2015) are the neutral assumptions. The 1974 scan has a red cast and cannot
set siding hue directly. The current quick siding is restrained, but the
canopy and skirting are too uniformly clean. Sun shadows are deep and long;
the cavity beneath the carport is appropriately dark. The flat wide lawn
looks like a dark felt sheet, and the dark oblique views make the undeveloped
ground dominate. Do not correct that by raising global exposure. Home
manufacture, uneven upkeep, fade, seam rust and splash remain the later look
gate; these images cannot prove finished albedos or weather.

Form/construction objections:

- The newer loop surrounds a broad empty center. It has the clubhouse,
  laundry and native swing equipment, but no convincing circulation or
  visitor parking. The 2015 reference interlocks its access, awnings, cars
  and yards much more tightly.
- Native cars occupy many lots, but the leading vehicles are mostly silver
  or white. The modulo choices correlate across opposite rows. Paint must
  be distributed independently, including dark blue, charcoal and black.
- A foreground utility pole overwhelms the older street view. Keep the
  1.68 m eye/40 mm camera and move its position within the street.
- The home heroes cut off a roof end; the deck cuts off the stair toe, and
  the carport cuts off its near post. These are failed inspection views.
  Check projected asset bounds, rather than assuming a plausible camera
  distance includes the whole module.
- The back doors have no landings. Each occupied lot needs an independent
  small back stair and a real walking route from the parking approach.
- The initial mesh review found buried mailbox posts, an unnecessary grade
  tread and tiny cap/shim gaps. Correct the actual geometry before any
  support claims. A closed skirt cannot substitute for access construction:
  give the back skirt a genuine opening and separate lift-out panel.
- Uniform tree spacing and the single opposite-street row make the town
  look staged from above. Stagger the native yard trees within their lots,
  vary their age scale, and continue the neighborhood at the side boundaries.
- The dumpster's rear fence needs actual supporting posts and side returns.

Implemented for pass 2: common paths, three occupied visitor bays and
planting reservations; back steps and lot walks; independent paint schedule;
older hero shifted within the clear street; a bounds-based framing loop;
correct mailbox/step/pier contacts; real lift-out skirt opening; visible
under-home service connections; staggered tree placements and side-street
neighbors; posted U-shaped dumpster enclosure. Quick native shed source
meshes also consolidate by fixed root and actual door pivots instead of
exporting each stud as a draw call. No sibling delivery is modified.

The old 40 ft frontage and 110 ft depth give 4,400 sq ft lots, within HUD's
2000 surveyed 4,000–5,000 sq ft range. The newer 64 × 120 ft lots are an
authored, deliberately generous 7,680 sq ft; they are above that common
range. Its low gross density and broad common core remain a concern to
judge again from the next oblique. The 20/24 ft private streets are compared
with the cited municipal dimensions, not described as approved civil plans.

## Pass 2 — construction contacts, additions and the town boundary

Inspected all eleven pass-2 frames: four park views, two home heroes, deck,
carport, and all three calibrated photographic pairs. These are fresh glTF
imports at 1,100 px / 20 samples, in `renders/checkpoint/pass2/`.

**Color and value first.** Each pair records a neutral patch rectangle and
its RGB balancing gains in `matches/comparison-cameras.json`: the 2009
storm-door frame, 2007 porch fascia and 2015 sunlit aluminum pan. The source
photographs have substantially more local variation and darker window
interiors. The quick materials are still too uniform; the carport needs a
metal response and the deck needs grain and localized graying. Those are
look-dev work, not a reason to lift the exposure. The clear-sky park shots
retain deep under-canopy shadows and un-clipped siding. Ground interiors
remain too smooth even with the native irregular grass fringe.

The three pairs are **type comparisons**, not reconstructions of the
photographed property. The original single-wide differs in window plan,
end treatment and overall proportions; its 84.5 px calibration residual is
too high for a dimensional validation. The addition's 17.1 px and carport's
9.4 px fits are useful for roof/support relationships. The carport solver
reaches its 100 mm lens bound: aerial crop perspective is not tightly
identified. No pair establishes exact dimensions of an unmeasured photo.

Corrections before pass 3:

- Added room: its empty rectangular window and exposed concrete stilts read
  as a placeholder. Add inset dark backing, hung sash rails, sill, corner
  returns and removable lower panels. Retain independent support and a
  real sloping wall closure under its roof.
- Carport: the folded surface was a single skin without a visible gauge;
  close it at 0.8 mm and seat rafters against its underside. Confine sag to
  a pan between supports rather than deforming the supported frame.
- Underfloor section: seat 2x6 joists above the chassis, plywood above the
  joists and opposed wedges between hardwood caps and rail flanges. Route
  tie-downs from actual rail clips to anchors inside the skirt footprint.
  Add an export close-up of the exposed piers and straps.
- Door hardware: actual mesh sweeps caught hinge ears striking the moving
  sleeves near the jambs. Recess the main door axes and separate the hollow
  moving sleeves from fixed pins and ears. All six variants now pass three
  independent sweeps, sampled every 2 degrees, without penetrations.
- Older approach: the leading pickup and pole obscure too much home form.
  Use a smaller native hatch at that lot and put poles at lot boundaries,
  outside driveway approaches; keep the 1.68 m / 40 mm street camera.
- Newer oblique: the two shorter central homes, common walks and occupied
  visitor parking make the loop more credible. It remains a spacious edge
  park rather than matching the very dense Florida aerial. Side neighbors
  still need actual public approaches, now continued with native Ground
  road modules. No gray presentation plinth is introduced.

Serialization checks are separate from these judgements. Raw mesh/normal/
UV and fresh-import checks cannot prove a photographic finish. The door
sweeps prove sampled home-door clearance; they do not certify the complete
park, native shed/gate mechanisms, structural capacity or civil design.

## Pass 3 — reject daylight seams and unsupported deck framing

Inspected every image in the complete 1,440 px / 32 sample export batch:
30 inspection frames and three photographic pairs in
`renders/checkpoint/pass3/`. This includes both four-view turnarounds,
posed entries, scale shots, exposed supports, the module sheets and all
requested detail views. The three neutral patches and calibration caveats
from pass 2 remain in force; the source pixels never become texture inputs.

**Color and value first.** The clear afternoon has readable light/shadow
separation and no washed-out white home bodies. The shaded entrance signs
are too dark for a marketing image, but their separately lit module view
proves legible lettering and adequate contrast. No exposure change is made
to hide shade. The window response still sparkles, and uniform metal and
wood remain visibly provisional. The added-room pair now has an actual
sash, sill and enclosed skirt, but its blank siding and bright blinds are
still much simpler than the used photographed addition. Weather and finish
remain outside this gate.

Reject these physical defects before stopping:

- End-on views reveal sky through skirt butt seams. Real interlocking
  panels overlap: close the open seams without adding triangles. Keep the
  intentional missing panel and the separate back access opening.
- The pitched gable is a triangle starting too low at its eave corners.
  It leaves a narrow daylight slit beneath each rake. Extend the closure
  from the wall top to the actual underside at several roof stations.
  Add a ray probe at the previously open location.
- A placement audit identifies two short-home lots where a carport post
  reaches the deck rail. Shift the carport 0.5 m toward the drive, including
  its car socket and pad. Check actual exported deck/carport meshes on every
  applicable lot, rather than relying on module dimensions.
- Carport pads and drive approaches overlap coplanarly. Partition their
  union and extend the approaches the remaining 96 mm to the street edge.
- Deck joists and nominal beams occupy the same vertical layer. Put the
  double beams below the joists, seat them on shortened posts, add actual
  outer rim boards and butt the joists inside those rims. Extend guard
  posts down to joist depth. Probe the exported beam/joist/post bearing
  elevations before claiming contact.
- The resource inventory exposed a second car marker beneath each carport,
  in addition to the component's own marker. Remove the lot replacement,
  attach seeded occupancy to the component socket and assert minimum car
  marker spacing. The central infill also displaced the intended mail area:
  move that cluster beside the common walk. Extend the static checks to
  every pair of neighboring lot assemblies and each common facility.

The park forms now differ clearly: narrow older single-wide rows with
mature crowns, tarps, missing panels and added rooms versus broad newer
double-wide lots around a rounded loop, central homes and common facilities.
Cars populate the private approaches in several native body styles and
factory paints. Neighboring houses have public streets beyond all four
park edges. Nevertheless, the lawns are too continuous and the new park's
2.819 homes/acre is too sparse to stand in for a typical dense park. Keep
that limitation explicit. The final pass checks these construction fixes;
it does not start the causal material/wear gate.

## Pass 4 — verify the corrected exports and stop at the form gate

Inspected all **30 Cycles inspection images and three matched pairs** in
`renders/checkpoint/pass4/`, at their native resolution. The complete
contact and both turnaround sheets are generated from these frames. Each
render's current glTF and external image hashes pass verification in
`source-verification.json`. No source blend supplies the rendered home.

**Color and value first.** Reused neutral-patch balancing is unchanged and
recorded beside the three pairs. The street heroes retain readable light
siding, charcoal roofs, deep canopy/window cavities and colored parked
cars. Neither hero has pixels above the near-clip threshold of 0.985;
their max-channel p5/p95 values are 0.059/0.812 and 0.055/0.804. Those are
display-image statistics, not measured surface albedos. The obliques and
shaded signs are dark, and the lawns still read too evenly. Do not mistake
these quick finishes for the later photographic material gate.

The end views no longer leak sky through the panel seams or below the
pitched rakes. Gable infill reaches the roof underside; the skirts retain
their intentional missing panel and separate back access. The final deck
view shows the rim/joist layer above the double beams and short bearing
posts. Independent rays measure beam bottom/top at 0.491200/0.675400 m,
post top at 0.491200 and joist bottom at 0.675400. The inspected bearing
surfaces agree within 0.1 mm. The exposed frame views show real main rails,
dry-stacked CMU webs, caps, opposed wedges and clipped tie straps.

Both exports pass 177 rest-pose checks between separate lots and common
facilities, plus 16 deck/carport checks, with no triangle intersections.
Car markers are no closer than 6.539 m in the old park or 2.743 m in the
new; occupied carports use their component socket exactly once. The mail
cluster now stands beside the common walk. All 18 standalone home hinges
pass 936 sampled poses at 2° intervals / 1 mm tolerance. This still does
not certify native shed/gate motion against all neighboring props, moving
vehicles, structural loads, accessibility or civil approvals.

The older street reads as a small established community with a different
roof mix, mature trees and accumulated additions. The newer loop reads as
a roomier neighborhood with smaller trees, central facilities and newer
homes. The streets lead into a continuing town rather than a gray stage.
The world beyond the park remains repetitive: two native house types and
regular public approaches are context, not a finished town composition.

Remaining weaknesses to carry forward: the new park's unusually low gross
density; broad smooth turf; uniform unweathered home surfaces; bright,
occasionally noisy quick glazing; schematic dumpster and pot foliage; no
interiors; exterior-only HVAC/service details. The single-wide photograph
fit remains loose and the aerial carport lens remains bounded, as disclosed
in pass 2. Fine siding relief should move into the eventual normal sheet
where it does not affect silhouette. Causal fade/rust/algae/splash, unique
lot marks, final shader consolidation and baked UV density/packing are
not attempted. No full cold rebake of all reused libraries was performed.

`make` completed the form graph; `make check` passed 21 packages, 1,000
deterministic plans, raw mesh/UV/normal checks and all clearance probes.
`make repeat` regenerated 64 package/image/metadata files byte-identically
with cached native inputs. All 492 pre-existing delivery/image hashes are
unchanged. There are no kit changes and no committed render images.
Stop here for the owner's construction/layout review.

## Look-dev restart — inspect the rejection before changing the scene

Inspected both pass-4 park heroes and obliques, SingleWide-120 and
DoubleWide-228 heroes, and the matched contact at native resolution.

**Color and value first.** The old clear-sky images are cool and too dark
across the lawns and shaded end walls. Dark cavities are useful, but a whole
dark lawn is not photographic contrast. The reference neutrals remain the
white 2009 storm-door frame, 2007 addition fascia and 2015 aluminum pan.
Their balancing assumptions must accompany the complete-park comparisons.

The sparse plots, broad continuous pads, missing inspection-home steps and
empty end elevations fail before material detail. The first revision uses
four rows and linked seeded home/add-on meshes. Tightening the older frontage
to 32 ft at 110 ft depth gives 3520 sqft lots and 36 homes / 9.053 homes per
acre. HUD's 2000 guide, Appendix D pp. 63–66, reports 3500 sqft in some
surveyed communities, frontage down to 20 ft and 10–20 ft separations. This
is the wider survey range, not the earlier modal 40–50 ft comparator or an
assertion that a fictional 1968 park was approved under a later ordinance.
The newer 56 × 95 ft lots give 33 homes / 5.764 homes per acre.

The revised calibration uses five visible 2009 wall corners rather than an
obscured floor corner and a misidentified ridge point. The complete older
street uses the addition's six construction corners. The aerial uses ten
pan/post anchors on two adjacent lots. The camera estimates are 9.59 / 17.00 /
16.56 native pixels RMS. These fit the named anchors, not every home in the
photographs; the aerial reaches its 100mm crop-lens bound. The used-lot fit
infers a low camera, without a height prior; it is not an eye-height hero.

This entry records the rejected baseline and source decisions. The three
new exported-material image critiques follow after the shared GPU bake.

## Look-dev pass 1 — dense exported parks, failed daylight and occluded fits

**Color and value first.** Viewed every one of the 13 exported-GLB PNGs in
`renders/checkpoint/look1` at native 1000px width, and all three composed
photo pairs. The neutral door-frame, addition fascia and aluminum-pan
assumptions remain explicit in their receipts. The street heroes are too
blue and dark, and the elevated views underexpose the roofs and turf.
The full-frame inspection homes are readable but too clean; the old skirt
has almost no legible splash at this distance. Increasing blue sky fill
did not make photographic daylight. Rebalance direct sun against the sky,
reduce the sky's saturation, and check sun visibility through actual trees.
Do not correct this lighting error by making the material albedos white.

The four rows, closely spaced end walls and mature interior trees now read
as a park rather than a hamlet. The older canopy is too continuous: a tree
on every lot blankets the lanes and the aerial comparison. Keep mature
trees between homes, but allow the gaps an actual uneven canopy has. The
curbless asphalt fringe has regular 0.8m teeth, an obvious CG silhouette.
Reduce their depth and irregularize their spacing. Turf still reads flat
and uniform; its worn-route mask is partly hidden by the concrete walk.

The inspection homes have their era roofs, end banks, lights, both stairs,
eaves/shutters/entry covers and deep frames. The new close entry cameras
sit behind the rail, obscuring the doors; move onto the actual porch at
standing eye height. Timber has transverse, oversized wave grain because
the native trim's grain direction is mapped across the long member. Fix
the UV direction/scale rather than modifying the native texture. The blind
stacks repeat at the same height on every window of a given home.

The low numerical pair errors do NOT establish useful comparisons. The
2009 camera sees a neighboring car/home in front of its intended subject;
the 2007 camera is immediately against the neighboring home's wall. Both
are rejected despite their 9.59/17.00px anchor residuals. Compare exposed
end-of-row homes/additions in the complete park, with visibility checked
on the actual imported triangles. The aerial does show the occupied park,
but is too tree-covered and dark against its sunny reference. Its 100mm
bound remains disclosed. No new image in this pass is accepted as final.

A source construction audit also found a 25mm gap below the new canopy
posts and tools that leaned short of the wall. Prepared corrections seat
the posts in the cupped deck, lean tools against the wall, drape the cover
over its actual support footprint, and map severity to the upkeep label
(the former seed-index order made `kept` dirtier than `patched`). These
await the next model build and imported-surface bearing measurements.

## Look-dev pass 2 — useful daylight, still insufficient surface history

**Color and value first.** Viewed all 18 PNGs at native 1100px width and all
four complete-park photo pairs. The blue cast is resolved and the street
heroes retain deep shade without clipping. Their p95 values are .835/.859,
with zero near-clip pixels. The elevated views still read too dim, at
p95 .592/.608; the roof and lawn exposure needs another adjustment. The
2009 pair is now far too pale against its door-frame-balanced reference:
lower its exposure, use the family's blue-gray paint on that later infill,
and retain the white skirt's contrast. The clear-sky heroes look overcast
because desaturating their fill also desaturated the visible sky. Keep the
neutral fill while restoring a procedural blue sky in view/reflections.

The finer irregular road fringe no longer reads as regularly spaced teeth.
The end banks, proud glass/meeting rails, different blind openings and era
roof construction are clearer. Entry cameras now see the actual door and
storm hardware over the rail; the deck's timber fibers follow the members.
Imported bearing rays on the three double-wides measure canopy post bottoms
at .877m and board tops at .88197–.88312m, giving 4.97–6.12mm engagement.
These are surface measurements, separate from the serialization checks.

Still CG: almost uninterrupted felt-like lawns, clean white skirt feet,
identically gray rolled roofs, and a hard white/metal finish boundary partway
up the carport posts. Next corrections add actual compacted routes on some
older lots, an aged cracked-concrete/gravel corner apron, stronger caused
splash, maintenance-dependent roof coatings and a continuous zinc finish
with seeded foot corrosion. The corner car/cart must clear the end window.
Town cars need road-shoulder placement; rear tree ranks must clear buildings,
and another block of varied ranches should close the older elevated view.

The second street fit is rejected: I selected lot 18 without checking its
room flag. It has no addition, so the fitted imaginary box is meaningless.
The next calibration binds lot 36's actual exported AddedRoom node, asserts
its existence, and checks the imported mesh group. The 2009 subject is now
visible but two of five anchors are hidden by its cart/car; moving them into
the corner hardstanding removes that obstruction. Aerial visibility is 9/10;
the newer lane's four anchors are clear, but its road-depth stations remain
inferred, and it only supplements the three construction comparisons.

All construction, UV/resource and motion checks pass for this model state.
The new town corrections were prepared after its context module loaded and
are reserved for pass 3; they are not claimed as present in these images.

## Look-dev pass 3 — full checkpoint and historical comparison

**Color and value first.** Viewed all 44 exported-GLB frames at native
1440px, the balanced photo pairs and their contact. The four park hero /
above p95 values are .784/.769 and .804/.718, with less than .001% near
clipping. Blue sky and neutral surface fill now coexist; white skirting
stays distinct from the faded siding, and openings retain deep shade.
The neutral references remain the 2009 door frame, 2007 white fascia,
2015 aluminum pan and 2024 white PVC post, balanced in linear RGB.

The paired 1980s infill now has its end bank, rake/fascia, proud frames,
steps, occupied apron and neighboring carport in frame. A later receipt
audit corrects the initial visual impression: four of five anchors are
clear; the far wall corner is behind its own roof trim. The old-lane
comparison now binds an actual addition, not the
rejected imaginary lot-18 box. The aerial compares two existing carports
in the populated park. Their residuals remain 9.59, 17.00 and 16.56px;
these measure selected construction landmarks, not the complete scene.
The supplementary newer lane fit remains 8.53px with inferred depth.

Still CG against the photographs: the old apron is too smooth despite its
fine cracks; the road's light aggregate is too close to the concrete pads;
the turf interiors remain flat beside the native edge tufts. Carport posts
have a continuous finish now, but its galvanized pattern misstates their
painted-steel construction and hides the foot corrosion. Correct these
with caused repair/crack placements, darker road vertex tint, stronger
existing blade normals and a separate painted-post finish within the
same atlas/material. The corner tool heap should have a supported cover.

The 36/33-home layouts, occupied gaps, mature interior trees, varied ranch
blocks, gas station/strip entrance and field/tree edge are all present.
The eight historical frames import the frozen original deliveries and
legacy context, then use the current camera matrices and physical light.
The matrix/lens/light comparison passes for eight full-size pairs. They
show the actual change in density, construction and surroundings rather
than moving the camera to flatter either state. Leaf-card silhouettes,
the tidy repeated plant pots and broad planar ground still reveal the
procedural scene. These remain explicit limitations for the next pass.

The post-pass visibility audit also rejects the addition fit's usefulness:
only two of six anchors have clear rays through the deck/canopy. Inspecting
the photo again found its right-front roof/floor pixels had been placed on
the window edge. The corrected calibration uses the actual room corners;
the home fit uses outer fascia corners instead of hidden wall corners.
Check these revisions on imported geometry before the next GPU batch.

## Look-dev pass 4 — correct sightlines, rejected ground-wear visibility

**Color and value first.** Viewed all 44 native 1440px frames and the
balanced park comparisons in `renders/checkpoint/look4`. Hero/above p95
is .784/.773 in Alder Court and .804/.718 in Meadow Bend; near-clipping
stays below .001%. The asphalt now separates from pale concrete pads,
while siding remains distinct from white skirting and deep cavity shade.
The photo neutrals are unchanged: storm frame, addition fascia, aluminum
pan and white PVC post, balanced in linear RGB.

The three construction fits now pass imported-triangle visibility for
5/5, 6/6 and 9/9 anchors, with 18.43/16.95/16.65 native-pixel RMS.
The supplementary lane clears 4/4 at 8.53px, with its inferred depth still
disclosed. The incorrect room pixels are corrected, fascia replaces hidden
wall corners and the obscured aerial post foot is excluded. An independent
Blender projection check disagrees with the solver by at most .00674px.
The renderer now rejects an occluded required anchor before rendering.

The added cover is visible and supported, and the carport has continuous
painted posts with localized foot rust. However, the old apron still reads
too smooth against the battered 2009 photograph. Raw exported geometry
reveals a cause: some isolated pavement cards face downward after the
generic volume-normal recalculation. The first settlement-crack card has
glTF normal (0,−1,0), while a repair card faces (0,+1,0). Unit-length checks
passed despite this construction error; one-sided culling hides the crack.
The summer-turf mesh also has downward normals. Of 176 older-park wear
cards, 29 face downward. Preserve authored upward winding for these open terrain skins and add a
positive-up normal/winding audit. No triangle or texture increase is needed.

Still CG: planar turf away from its edge tufts, coarse leaf-card silhouettes,
and wood-like texture on small plant pots. The latter is a finish assignment
error: give terracotta and foliage their nonmetal finish swatches. The newer
aerial also reveals a public-road stub behind the tree line; continue that
road beyond the camera's set. The homes, density and actual fit subjects
remain; this pass is rejected for these surface/context defects rather
than counted as final look approval. All eight historical comparisons pass
their camera/lens/resolution/light equality checks.

## Look-dev pass 5 — final checkpoint, remaining appearance gap

**Color and value first.** Inspected all 44 native 1440px PNGs in
`renders/checkpoint/look5`, all four full-size balanced photo pairs, the
two contacts and all eight before/after sheets. The comparison neutrals
remain the white storm-door frame, white addition fascia, sunlit aluminum
pan and white PVC post; gains are calculated in linear RGB. Old/new hero
p5 values are .0706/.1451 and p95 .7843/.8039. Their near-clip fractions
are .000944%/.000258%; both obliques have zero near-clipping and p95
.7725/.7176. Cavity shade remains deep, the sunlit siding retains detail,
and asphalt separates from pale concrete. These display-value statistics
support exposure review, not a claim to have measured intrinsic albedo.

The paired 2009 home has the right general siding/skirting separation and
a much better roof/end-window/step silhouette than the old checkpoint.
However, the photograph's battered apron is substantially more mottled,
rough and repaired. Our low cracks and repairs still disappear at this
framing; the lawn is also too uniform in height and hue. The 2007 addition
pair shows the occupied row and supported entry, but its tidy woodwork and
regular planting do not reproduce the photograph's irregular maintenance.
The aerial now shows a dense inhabited park rather than a lone carport;
its roofs, mature interior trees, separate pads and narrow lanes read
clearly. The reference still has stronger hardscape history and more
varied resident alterations. The newer lane retains a flatter lawn and
more repeated vehicles than the supplementary photograph.

The open-surface correction is a real shipping fix: raw exported winding
and normals now point upward for all 22,436/31,482 tagged terrain
triangles. The previous volume-normal recalculation is bypassed for these
skins. In Cycles the visible difference is small; this correction does
not establish that the pavement wear now matches the photograph. Pots
and small foliage use their intended nonmetal finish, and the public
street continues beyond the newer set instead of ending behind the trees.
These changes add no triangles to the shipped parks.

The form comparisons show the 36/33-home neighborhoods, end-on rows,
era-specific roofs, proud windows, steps, native lot furnishings, interior
old-park canopies and closed town context. All eight before/after sheets
pass equal camera/lens/resolution/light checks. The imported construction
anchors remain visible at 18.43/16.95/16.65px RMS; the supplementary road
fit is 8.53px with inferred longitudinal stations. This is landmark
calibration, not a complete photographic scene match or surveyed depth.

Still CG and below the photographic quality goal: the old concrete apron
is too smooth and clean; broad turf stays planar away from the edge tufts;
leaf-card silhouettes and small plants are coarse and repetitive. Only
three native car bodies recur across the parks. The grayed deck has fine
grain and cupping but still reads unusually even in the full-size detail.
Some adapted secondary objects (play equipment, utility pole and waste
enclosure) remain simpler than the homes. Wear is most legible at skirt
feet, on roof coatings and at carport post bases; it does not yet give
every sunny wall and pad the reference's visible history. This handoff
is a look-dev checkpoint, not final art acceptance. No gallery/docs are
made. A further appearance pass should prioritize irregular repair
history and ground relief before finer home detailing.

Final `make`, `make repeat` and `make check-preservation` pass: 21 checked
exports, 1,000 deterministic plans, 1,365 static assembly comparisons,
936 sampled poses of 18 home hinges without violations, 64 byte-identical
regenerated package files, and 1,202 unchanged prior files (492 original).
Repeat uses cached native inputs and does not repeat the GPU bake.
All 44 render source/image receipts pass. These checks prove their stated
geometry, serialization, resource and sampled-motion scopes; they do not
override the visual weaknesses above.

## Delivery pass 1 — reject weak wall/apron age and the drawn road seal

**Color and value first.** Inspected all ten native 1440px frames in
`renders/age-pass1/`, then all four full-size neutral-balanced pairs. The
2009 storm-door frame, 2007 white addition fascia, 2015 bare aluminum pan
and newer PVC post remain the balance assumptions. The older lot still
has much less value variation than the used photograph: its light skirt,
clean apron and smooth siding dominate the few dark marks. The street
heroes keep deep shade and unclipped highlights: old/new max-channel
p5/p95 are .0706/.7804 and .1412/.7961; near-clip fractions are .00000773
and .00000258. These are display statistics, not measured albedos.

Traffic now has blue, charcoal, black, red and tan among the light paints.
However, the newer hero still puts the same pickup body on both foreground
drives: a nine-lot row correlated with the three-body cycle. Offset the body
cycle by row as well as by lot, retaining independently seeded paint.
The three native body geometries necessarily recur across a whole park.

Reject the age and turf gate. The older row remains too clean. Roof runoff
is cut off above window heads and hidden by the awnings; redirect it beside
their ends and let exposed streaks reach lower. Broaden selected neglected
streaks, increase irregular lower-skirt splash, and expose a missing end
panel on patched homes so underfloor darkness reads from the lane.
The apron repairs exist, but their placement hugs the house. Fresh-import
surface and camera rays hit the actual repair skins; projected patch
centers occupy only a small strip beside the cart. Move the caused repair,
crack and former-parking oil history across the existing exposed apron.
Do not change the accepted slab or lane dimensions to match this photo.

The long black seal reads as a drawn zigzag. Smooth its path, vary its
width, interrupt the repaired sections, reduce repeated large oil stamps,
and break the uniform brown shoulder band. Keep the charcoal pavement's
value; add restrained binder/wheel-lane and exposed-margin differences.
Broad lawns remain felt-like. Soil at the skirt is largely hidden, and
the drive-edge scars are too small. Ground the soil skins on the actual
undulating sward, open the mailbox/drive turning scars and add sparse native
grass clumps beyond the slab fringes, without another image set.

The replacement 2007 view now shows the actual old lane and occupied
neighbors. Its 18.737px fit uses four inferred lane stations, rather than
the old six addition corners; it is a weaker construction comparison.
The 29.39mm pose has a conspicuous tilt and substantially more open street
than the photograph. The other three accepted fits are unchanged. No final
gallery or docs image is approved by this pass. First-pass native crops
are in `renders/age-fixes/`; they document the miss as well as the progress.

## Delivery pass 2 — reject polygonal soil and insufficient integrated wall age

**Color and value first.** Inspected all ten 1440px pass-2 frames and all
four balanced pairs in `renders/age-pass2/`. The same four photographic
neutrals apply. The old single-wide remains brighter and much cleaner than
the shaded reference. Its exposed apron now has visible repair history,
but the wall/skirt values remain too uniform. Correct the old wall's
caused color variation and reduce the single-wide pair's exposure by .45
stop to better match its assumed white frame; retain the accepted hero
lighting. Before/after evidence must rerender the old export under that
same matched light, not compare two different exposures.

The opposite foreground drives now use different bodies, and trees have
different crown scales, rotations and horizontal aspects. These choices
are stored in exported sockets. Sparse lawn clumps read as actual blades
in the near row. The smooth, interrupted road seals and smaller oil traces
are better than the first zigzag, with restrained wheel/binder value changes.

Reject the soil treatment. Hard polygon edges at the drive/mailbox scars
and the intermittent shoulder pieces read as paper laid on the ground.
Use a shared vertex-opacity fringe over the same Concrete maps, with a
feathered outer ring and actual sward-conforming elevations. A new material
state is justified; another texture allocation is not. Independently check
that the exported COLOR_0 alpha contains both clear edges and an opaque core,
and enforce the accepted 176.05 MiB ceiling on the complete static image union.

The broad roof-runoff ribbons are still weaker than needed. Carry selected
roof-seam and end-fastener corrosion directly in the wall's color stations,
including the street-facing end beside its window bank. Add protected-eave
damp to the older walls. Keep the missing panels, piers and existing door
clearances; no home/lot plan changes are warranted. The 2007 comparison has
the required lane and neighbors but retains a tilted, inferred-road fit,
which is less convincing than the three accepted construction comparisons.
This pass still withholds the gallery. Crops are provisional, not approval.
