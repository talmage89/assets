# Main Street construction review

This is a form checkpoint. The blank quick-color walls, smooth cornice paint,
missing brick normals and unworn pavement are deliberate unfinished surfaces;
this document does not certify final material realism or baked delivery.

## Pass 1 — first Midwest shell, Workbench (imported checkpoint GLB)

Evidence: `renders/workbench/contact.jpg`, all five constituent views inspected,
against `build/references.jpg` (three actual HABS photographs and measured plan).
Value first: the reference has deep windows and a clearly brighter trim than
masonry. The placeholder colors preserve that hierarchy; Workbench cannot
judge transmitted daylight, material albedo or the final tonal range. The two
monochrome photographs offer no hue evidence; the color photo's neutral is its
sidewalk/white sash, not blue shadow. No color was sampled into an asset.

The seven lots read as a commercial row, with a useful one-story interruption.
The tall display floor, tight window cadence, recessed sash and substantial
cornice projection work. Three form faults need correction: the transom band
collides with masonry above the storefront opening; the corner's lower return
is an implausibly long blank bank wall; the northeastern bay-window flag has
no geometry yet. Fix the band levels, add public-side display openings, and
build the bay as an actual projecting three-plane assembly with supports.
Rear platforms and stairs exist, but the flights need a closer physical check.
The repeated HVAC boxes and very consistent sash treatment remain visible CG
tells that variation/detail work must address before look-dev acceptance.

## Pass 2 — all four towns and independent motion audit

Evidence: `renders/pass2/contact.jpg` (all twelve images inspected) and the
first imported-door sweep. Color/value still uses the first pass's explicit
neutral references; Workbench is useful for form but too dark for a material
approval. The western one-story skyline, denser northeastern row with a real
bay, and southern posted galleries distinguish the towns. They share more
window detail than the photos do; that is a remaining grammar limitation.

The across/overhead/rear cameras crop the end buildings: widen those views.
The motion check found real problems that the pictures concealed: a retail
floor was 34 mm too high, the stair leaf overlapped its cast pier, and service
and corner hinges sat too far out in thick masonry reveals. Lower the shop
floor to grade, narrow/center the stair leaf within its clear opening, inset
the retail leaf behind its glazing returns, and put the other two hinges
behind their thick reveals. No collision exemptions or looser tolerances.
The repeated roof equipment is still too regular; vary its position/count and
add brick chimney masses before the next form review.

## Pass 3 — source photo pairs, regional overview and door corrections

Evidence: all twelve `renders/pass3/` views and the three Workbench preview
pairs in `renders/match-preview/`, inspected individually. The same neutral
references apply; these preview materials are darker and more uniform than
the photographed masonry and are not a look-dev result. The black and white
images constrain proportions/value only. The photographed painted window
is balanced against its pale sash and sidewalk; the low-resolution color
preview is unsuitable for a precise albedo claim.

The photographed cast front has shallower sash recesses and more shaped
cornice brackets than our first model. Italianate fronts now use 105 mm sash
inset, cream hood molds and profiled pressed-metal brackets; thick brick
Romanesque reveals remain 190 mm. The photographed upper floors have more
varied sash/hood condition; filled openings and causal weather remain next-gate
work. The bay window's supported projection reads well. The western skyline
is suitably low, while the northeastern and gallery blocks read denser.

The first whole-row cameras still clipped a corner in overhead views. They
now fit actual imported architecture bounds with explicit margins. The
Mulberry match compares the continuous street wall, not the exact landmark
building: our chamfer, roof and fire-escape location intentionally differ.
The Foster match compares one retail frontage, not the original two-store
building. The color-window crop is a weak calibration at grazing incidence;
its residual and lens bound are disclosed, not hidden by an overlay.

Further sweeps found a 4 mm threshold overlap, a dropped infill ceiling that
hit the door head, and the corner leaf opening into an interior display-room
partition. Thresholds, ceiling and corner-lobby partitions are corrected.
No tolerance change or collision exemption was used.

A further construction review of the rear found that the early diagonal
flights did not meet the next landing on three-story buildings. Replaced them
with stacked parallel flights along the rear wall, deeper end landings and a return walk and
an open stair lane. This preserves headroom over the flight, joins each flight end
to an actual lower landing, and gives the first flight feet on grade. Wall
braces now reach their anchor plates. The earlier attractive overview was
not sufficient evidence that the stairs could be used.

## Fine motion verification while the GPU queue was occupied

One-degree sampling found a 2.3 mm corner-leaf collision at 24° that five-degree
sampling missed. Moving the first side display opening farther from the
chamfer preserves a clear lobby. A separate 58° result was a ray-parity false
positive: oriented-triangle winding was −.004 in air, versus about 1 inside
the actual masonry. The downtown audit now uses that membership test while
retaining the kit's BVH/edge intervals, nearest distances and 1 mm tolerance.
Positive and negative fixtures cover abutting/overlapping members, hollow
frame air and a fully contained collision. All 89 doors pass at 101 positions
each with zero measured penetration. No shared kit behavior changes.

## Pass 4 — Cycles form review of exported quick-material blocks

Evidence: `renders/pass1/contact.jpg`, the 35 mm hero review and all twenty
first complete Cycles gallery views. Color/value first: untextured brick is
much more even than the photographs, as expected at this gate. The pale trim
is separated from red/buff masonry, storefront cavities stay deep, and the
hero's highlights do not clip. The photo's pale sash/sidewalk are the color
comparison neutrals; no photographic pixel has become an asset texture.
Final material/albedo and wear calibration is expressly deferred.

The full row and parked pickup/crossover/hatchback read at eye height. The
first 40 mm composition lost too much of the near row; the 35 mm camera stays
on the opposite walk and shows the corner and the row beyond. The four
skyline rhythms remain distinct; the southern gallery's deck, posts and rails
read as supported construction. The new fire escape has real end landings and
readable flights. Rear shots retain deep shade rather than a pale wash.

The close-ups caught two presentation/construction mistakes: a date stone was
behind brick corbels, and the ghost-sign view cropped its lettering. Reserve a central frieze field
for the date panel, clear of brackets/corbels and aim the side view at the actual sign center.
Show the profiled metal cornice in its close-up, with the brick cornices still
visible in the block elevations. A support pass also corrects furniture feet,
chair columns and roof curbs after the shop floor was lowered to grade.

Remaining form limits are deliberate but visible: the sashes and rear service
layout share too much vocabulary, cornice ornament is coarse, room dressing is
boxy, and the street ends use simple right-angle curbs. The sign is a form
placeholder, not a convincing painted-brick ghost yet. The source vehicle
forms are context, not the accepted baked car deliveries. The final texture,
weather, window vinyl and night-light work belongs to the next gate.


## Pass 5 — taller sash proportions and construction contacts

Evidence: all twenty window-revision Cycles views and all three matched pairs
inspected. Value first: the archival pale sash and sidewalk remain the stated
color neutral; the monochrome pairs constrain value and proportions only.
The quick masonry is still much more uniform than the photographed brick.
Material approval is deferred; the render does preserve dark entrances,
shaded undersides and separated light trim.

The Foster pair exposed overly short upper windows. Increase Italianate
openings to 2.20 m and Romanesque to 2.14 m; keep plain commercial openings at
1.96 m. These fit the existing 11–12 ft floor modules and distinguish styles
without adding window silhouette segments. Re-rendered pairs show a better
tall-sash rhythm. The surveyed facade still has more elaborate hoods and
cornice relief; those differences remain visible and belong in the shared
ornament source rather than extra repeated game-mesh faces.

The corrected side camera exposed a more serious mistake: the old ghost-sign
rectangle crossed a display-window opening. Move it and the demolished-neighbor
outline onto uninterrupted masonry, and assert the sign field clears every
opening. The new close-up verifies the placement. Its opaque painted rectangle
still reads as a printed panel; this is a quick-material placeholder that must
become worn paint integrated with brick at look-dev.

A contact review also found gallery feet above grade, a flat skylight curb
below sloping glazing, and missing short blade-sign hangers. Correct the feet
and canopy column caps, build a four-sided inclined hollow curb whose flashing
intersects the falling roof, add the hangers and seat the masonry tie plates.
Independent rays on the actual exported surfaces now measure gallery feet at
grade, 20 mm curb-base overlap into the roof, and glazing-to-side-rail gaps
below 1 micrometer of mesh precision. Those numbers establish geometric
contact; they do not certify structural capacity or field construction tolerances.


## Pass 6 — final exported checkpoint, Cycles

Evidence: every view in `renders/checkpoint/contact.jpg`, all three pairs in
`renders/matches/contact.jpg`, and the full-resolution final hero inspected.
The audit confirms all 23 views use the current exported GLB hashes, the
Cycles engine and the recorded camera/context. The 35 mm hero is at 1.68 m on
the opposite sidewalk with the pickup, crossover, hatchback, trees and lights.

Value first: the final hero has deep storefront/awning cavities and bright
trim with smooth highlight roll-off. No RGB channel reaches 255; display-luma
5th/50th/95th percentiles are 4.93/68.19/192.90 on the 0–255 PNG scale. These
are display diagnostics, not measured albedo or a final material approval.
The photographic neutral remains the pale sash/sidewalk; monochrome pairs
remain form/value evidence only.

The Midwest infill interrupts an otherwise two-story cadence, the western
row stays low, the northeast has a denser three-story street wall and a bay,
and the southern gallery reads as a supported continuous sidewalk frontage.
Store entries, transoms, separate stair doors, upper openings and cornices
read clearly in their close-ups. The ghost field clears the display windows;
the revised date panel is legible. Rear service volumes and usable escape
landings are visible, though the shaded rear close-up remains deliberately dark.

The remaining CG tells are the flat/unworn masonry, simplified cornice relief,
repeated rear equipment and sash detailing, simple room furniture, and the
printed-looking ghost sign. Source vehicle forms are presentation context.
Archival matches are approximate original-family comparisons: RMS residuals
are 6.85/10.56/5.46 pixels, and the grazing window crop reaches its 100 mm lens
bound. They are not exact reproductions of the pictured facades. Stop here,
before brick/trim look-dev, wear, final UV/bakes and night lighting.
