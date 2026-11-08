# Manufactured communities / form gate

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
