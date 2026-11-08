# Parking garage form review

This log separates preparatory construction review from rendered critique.
Only the exported glTF is allowed to supply the checkpoint geometry. No final
look-dev, manufactured concrete bake or service-age pass is claimed here.

## Preparatory construction review

Color/value first: choose neutral mineral form albedos rather than a white clay
override. Concrete is .34/.325/.29 linear, deck .27/.265/.245, with deep cavities
and a fixed low sun; exposure is not used to make the concrete match a photo.
The final form views still need direct visual review before acceptance.

The PCI reading rejected flange-height light placement: hanging straps now
put the diffusers near the tee-stem underside. The first PT framing attempt
ran its beams along the wrong axis; real transverse 60ft beams now support the
slab between 36ft stations. Ramp girders break at their grade transitions.

The first end decks were thick solid covers. The municipal landings now use
the same tee soffits as the parking bays. Roof ramp columns stop at the last
actual deck; internal and terminal guards protect differences in elevation.
The highest route ends on the flat aisle instead of entering a nonexistent
next ramp. End bays grew to 36ft for tangent turn arcs and lane offsets.

Accessible reservations initially consumed less row width than their shared
aisles needed. The generator now removes the correct full block of ordinary
stalls. The larger garage reserves eight spaces/two vans and the smaller
four/one. Hatching follows the actual 1% plane rather than sinking below it.

Tower doors originally faced opposite directions, and a nominal front stair
door opened under a half landing. Both upper-floor functions now face the
garage landing, with genuine apertures. A separate side exit meets the lower
stair landing at grade. Ticket screens face the driver's side and cabinets
and gearboxes sit on actual concrete control islands. The FULL display has a
back plate and bracket rather than floating beside the entry.

Native context is original library geometry: continuing Main Street rows,
commercial shops, proper alpha-card trees, native luminaires and three car
body types. Cars occupy the per-level stall reservations rather than a single
token car on the street. Nothing in another family is edited.

Three photographic comparisons use recorded neutral patches before fitting.
The Z22 pale sign border, Pleasant Hill shaded enclosure and Harmon sunlit
spandrel are approximate neutrals, not gray cards. Interior fitting uses four
column face anchors and the approximate 33mm EXIF equivalent; the corbel's
outline remains an independent visual comparison. Larger buildings and
different camera processing limit exact claims. The Alewife atrium/roof are
secondary references, not forced matches to a different architecture.

## Pass 1 — six exported Eevee form views

Opened both heroes, both overheads and both aisles in renders/pass1-eevee/. These
images precede the final construction corrections; their views.json records
source hashes. Color/value first: the frame is pale and blue, and the aisle
has almost no contact shadow. The log reports an overflowing Eevee shadow
pool, so these views cannot establish concrete value or cavity darkness.
The next set uses Cycles, with unchanged scalar material albedos and an
explicit clear procedural sky. No weathering is added at this checkpoint.

The municipal hero cuts off the near tower and its roof pole. Move the eye
farther across the intersection while keeping 1.65m height and 35mm lens.
The commercial overhead exposes an unfilled rear portion of its larger
parcel. Add continuous owned parcel ground and a rear landscape strip;
existing library streets continue beyond it. This is a site-construction
error, not an acceptable background crop.

The context hatch/SUV glass and tires also exported as white fallback factors;
this is separate from the shadow failure. Explicit stock quick finishes now
replace their unsupported procedural graph at site assembly, keeping every
original vertex. The sedan retains its native baked PBR.

The 60ft precast span reads in the aisle and its twin-stem rhythm is visible.
The compact garage has transverse downstand beams rather than disguised
tees. Parking density reads as a weekday. The next views must resolve car
contact, end-turn barriers, bearing seats, doorway swings and the stair's
waist construction under real shadows. The first pass is rejected for
presentation and remains a diagnostic, not a deliverable gallery.

## Pass 2 — Cycles town views and three fitted pairs

Opened all six renders in renders/pass2/ and all three pairs archived in
renders/pass2-matches/. Color/value first: contact shadows finally seat the
cars, but sky fill overwhelms the directional key. Concrete reads cool and
the daylight looks too flat. Retain the quick mineral albedos, reduce sky
fill, strengthen the low sun and give it a warm daylight spectrum. The
interior fixtures are too amber; change their presentation lights to neutral
fluorescent white. Parked sedans must have their brake/signature lamps off.

The black municipal hero is a failed camera, inside an opposing storefront.
The Pleasant Hill fit also put its eye below ground, and the commercial fit
overlapped a parked car. These are rejected comparisons, regardless of their
small projection residuals. Add exterior eye-height priors and record any
local context-car clearance used for a photographic viewpoint. Compare the
interior column at the ramp's low-end landing, where both neighboring decks
are near the same height; the mid-ramp column is a poor match to the flat
photographic background.

Native curb modules show perpendicular fingers into the road. Their imported
quaternion rotation mode ignored the assigned Euler yaw. Set the local clone
root's mode explicitly before placing it. The rear commercial parcel now has
continuous ground instead of a black gap. The two plans and their occupancy
read distinctly, and the interior shows tees versus transverse PT beams.

The actual motion sweeps exposed one arm overlapping the other gearbox and
an outward stair leaf touching a projecting corbel. Put the exit controls on
the exiting driver's side, provide three real islands, and move the cores
350mm farther from the front corbel line. Extend the private side landing so
pedestrians can pass beyond the open leaf. These are assembly fixes, not
allow-list exceptions. No new exception was added to the motion checker.

## Pass 3 — corrected lighting, placement and photographic viewpoints

Opened the six renders in renders/pass3/ and the three current pairs, archived
as renders/pass3-matches/. Color/value first: the facade now has warm direct
light, cool cast shadow and dark openings. There is no white clay wash. The
photo-pair concrete remains plainer than the used references: board marks,
connector runoff, staining and patched spalls belong to the requested next
phase. Blue column paint is an authored wayfinding choice; compare bare
concrete above it, not the blue film against the photograph's gray column.

The municipal hero still has a foreground shop concealing its far end. Move
the camera to the public sidewalk in front of that frontage, retaining a
1.65m eye and 35mm lens. Its next view must include the full garage and roof
poles. The commercial hero shows its smaller mass, shared court and occupied
stalls; the overhead shows a narrow speed ramp rather than a recolored second
60ft parking bay. Native curbs now align with the streets.

The interior pair now exposes the real tee webs, L-girder ledges, corbels and
their seats. The broad forms agree with the PCI vocabulary and photograph;
the original garage has different paint, fluorescent fixtures and a ramped
second bay. The exterior pairs show the intended repeated openings. Their
architectural differences, cropped larger reference and camera residuals are
retained rather than presented as a surveyed replica. All exterior fitted
eyes are now above ground. Only context cars at a photographic viewpoint may
be hidden; those names are recorded in its render receipt. Garage geometry
is retained in full.

All 60 module/placed pivot sweeps pass after the physical fixes. The remaining
route check exposed a numerical issue: BVH epsilon produced ghost hits on
long thin joint faces. A source-scene diagnostic with epsilon disabled agrees
with direct imported triangle planes. Source routes now use exact upward
planes and small edge probes; the independent check uses float64 barycentric
intersection at the original XY, with a 10µm boundary tolerance. It must still
reject a real gap. Overlapping tee seal and pour-cover tops use the upper
surface. Full validation and the detailed render set follow this pass.


## Pass 4 — complete seventeen-view construction set

Opened all sixteen site views and the original module-grid render, archived
in renders/pass4/. Color/value first: warm direct facade light, cool shade
and deep covered parking remain intact. The municipal hero now includes the
whole frame and roof poles; the commercial hero frames its separate court
and smaller mass. Weekday occupancy reads on every level. The roofs and
interiors remain deliberately plain form materials, not an aged finish.

The complete view set reveals presentation misses that the six-view rounds
could not expose. The entry cuts the right gantry post; pull back and use
35mm. The tower view shows the core's opaque inner side and crops the larger
roof: view the western core from its exterior glass side. The ramp view is
a blank end landing with its inclined approach mostly off frame; stand in
the actual ramp aisle before its high-end transition and look into the turn.
The human reference is too dark against a dark car; use a lighter neutral
silhouette without changing its 1.80m geometry.

The single physical module grid is rejected. Twenty-five equal-spaced cells
cannot show a small drain and an eighteen-meter bay at a useful common scale;
its horizontal captions are unreadable. Replace it with separate fitted
Cycles views of each independent module export, then compose those panels
with readable names and measured triangle counts. No model or source-scene
substitution is allowed in the fitted views.

Expanded aisle sampling initially landed inside the solid terminal guard
wall, reporting its 1.10m top as overhead headroom. The sampled aisle now
keeps its original one-meter end-wall setbacks while adding actual downward
triangle section midpoints between them. This is a sampling-domain correction,
not a lowered clearance threshold or a geometry exception. It still requires
7ft over the sampled aisle, and the actual entry/van routes are checked
separately. The corrected complete checks and fitted views follow.


Opened the three complete photographic pairs in renders/pass4-matches/ as
well. Bare concrete above the painted column remains within the intended
mineral value family, while the reference's pores, edge softness, runoff and
old repairs are absent as expected before look-dev. The type comparisons
retain different architectural dimensions and their recorded residuals.

A source audit found that appending accessible spaces after the other levels
could reuse a regular ground-floor painted number. Assign sequential numbers
per level, including those late reservations, and publish the number on each
stall socket. The parameter sweep now checks per-level label uniqueness and
the shared graphics page's supported range for all 45 valid programs. This
changes UV choices and metadata, not capacity, occupancy or structural form.


## Pass 5 — fitted modules and targeted camera review

Opened all 25 individual module renders and their composed sheet, plus the
revised municipal entry, tower, scale and ramp views. Archived in renders/pass5/.
Color/value first: the fitted concrete panels retain a mineral mid-value,
dark steel and contact shadows. The fluorescent inspection panel has a bright
pool; it is an energized fixture demonstration, not a concrete albedo sample.
Every small device is now large enough to inspect and the captions are readable.
The tower reveals its real stairs behind glass and includes its full roof.
The entry now contains both gantry posts and the two control lanes.

The new ramp camera still looks across occupied stalls on its way into the
turn. Reject it. Put the eye on the actual serialized turn's tangent point
and look back down the ramp aisle; the sightline must stay in circulation.
The human silhouette is now discernible beside the car without changing scale.
Numbers on the front row also need their UV corners rotated to face the aisle.

The end-bay panel prompted a construction audit: shortening its L girders
scaled the column-end setback as well as the span. Preserve the fixed .82m
total end allowance when changing bay length. Add fresh-import cap-surface
samples for all three precast mating assemblies so a girder end embedded in
a column is rejected. Monolithic PT beam/column intersections are intentional.

The complete imported-garage checks pass before these last two UV/module
corrections: sampled aisle minima 2.6932 / 2.5898m; van-route minima 2.4892m;
1,056 tee seat samples within 1µm; wheel-stop vertices within 1.1µm; all 60
moving-part sweeps clear. These are measured surfaces and discrete samples,
not constants or a continuous full-vehicle collision certification. Repeat
and the final corrected exported views remain to be accepted.


## Pass 6 — complete views and independent mating checks

Opened the complete site view set from the latest exports and reviewed all
25 fitted module panels. Color/value first: facade highlights retain
headroom in the display range; covered parking and corbels have deep shadow.
The clear-sky heroes retain the low sun rather than an overcast fill. The
municipal ramp view now looks down its inclined parking aisle from the actual
turn. The compact view needs its target nearer the ramp mouth to avoid looking
through the corner column; the overhead remains the clearest complete ramp
plan. Street context continues past the garage, although distant landscaping
and repeated background storefronts are still schematic.

The new socket check first selected triangle centroids as though they were
pad centers. Select the actual small face footprints instead; the average of
their underside triangles measures the pad-pair midpoint. The check then
accepted the flat assemblies and rejected the RampBay's front L girder inside
a corbel. Its grade had been applied before a 180° yaw, reversing the slope.
Compute grade in the placed frame, preserve flat column feet, and extend the
shaft vertically while inclining only the bearing seats. Socket positions and
normals must follow the same warp. Bearing frames now use pad undersides,
not stem undersides, and the PT beam endpoints use its actual 60ft span.

The EndBay default is now three tees / 36ft, matching the delivered turn bays.
It remains below the modular triangle cap (968 triangles). The two whole
garage mesh counts are unchanged. These corrections affect mating geometry
and metadata rather than increasing visual detail or beginning look-dev.
The render process in the preceding attempt received SIGTERM during the
module panels; preserve that failure log and regenerate the interrupted set.
Final acceptance requires the corrected mating tests and independent rebuild.


## Pass 7 — corrected exported checkpoint set

Opened all sixteen final site views, all twenty-five fitted module renders,
the module sheet and complete contact sheet. Also opened the three final
calibrated renders, their photographic pairs and comparison contact sheet.
These use the public external-image glTF deliveries, not the authoring blends.
Color/value first: both street heroes retain warm raking light and dark
openings. Full-frame display-Y p1/p99 is .0031/.7726 municipal and
.0185/.7749 commercial; neither has white-clipped pixels. The frame includes
sky/town, so these are exposure diagnostics rather than measured albedos.

The complete frame and roof poles fit the eye-height 35mm heroes. Cars and
fixtures read through the openings, and the overheads show different parking
programs and ramp types. The municipal turn view exposes the inclined aisle;
the compact turn view remains a partial landing/ramp-mouth view, with the
corner column visible, while its overhead supplies the clearest whole route.
The entry contains both gate controls, the clearance gantry and its posts.
Tower glazing reveals the stair flights and the ground exit meets the walk.
The scale views retain the actual 1.80m reference beside a native car.

The independent mating check accepts all three corrected precast assemblies:
48 girder-cap face samples clear the columns; 18 socket-to-pad midpoint
measurements are within .000001m, and their bearing-plane orientations agree.
Both full garages pass surface support, van route/bar clearance, tee seating,
wheel-stop contact, aperture sampling, normals and UV-collapse checks. All
60 declared motion sweeps pass. The parameter sweep accepts 45 programs and
rejects 33 short ramps plus four invalid inputs. Existing delivery hashes
remain unchanged for all 554 protected files.

The pairs retain honest differences. Bare concrete has the intended neutral
mineral family, but its pores, softened arrises, board/form marks, runoff,
repairs and roughness variation are absent. Controls remain simple folded
cabinet forms without final panel graphics. The native quick Ground arrow
cell repeats; placement-owned repaint/age variation remains to be made.
Distant context and repeated native storefronts are schematic. The public
ACI source is a preview, not the complete paid guide. No bake-loss, final
UV-density, weathering or draw-call certification is claimed at this gate.

All form/construction and image evidence is ready. The independent geometry,
original graphics and manifest byte comparison is the final outstanding
receipt before this checkpoint is reported.


The first independent byte comparison matched the modules, garage deliveries,
graphics and manifests, but found two changed bytes in each complete-site BIN.
Both identify the same native PinOak bark tangent component, alternating
between -.9714 and -.9715 at a four-decimal export rounding boundary. Use the
existing kit guard with an exact position/normal/UV signature, restoring the
accepted tangent from the immutable native PinOak input. Do not use the earlier
site output as an input, round unrelated values or relax the repeat comparison.
Both guarded site payloads match the earlier independently rebuilt native result.

Regenerated all checkpoint views and the three photographic comparisons from
the guarded exports. Their receipts now hash external BINs as well as glTF
JSON. All 41 source-view and three photographic-render receipts match current
inputs and PNG hashes. Programmatically opened every regenerated PNG; maximum
display-byte deviation from the individually reviewed pre-guard renders is one
level, with unchanged framing and construction. The independent full byte
comparison is being rerun with the guarded exporter.


Final acceptance receipt: `make -k WIDTH=1200 SAMPLES=24 all repeat` completed
with exit status 0. The independent rebuild matches all 70 checked files,
91,258,230 bytes, exactly: module/garage/site glTF and BIN files, the three
original graphics PNGs and seven manifests. Native context caches are immutable
inputs; stochastic renders and future baked maps are outside this comparison.
The construction, motion, parameter and site-resource receipts all pass.
`python3 src/dependencies.py` reconfirms all 554 protected existing files;
`python3 ../kit/repo_check.py` reports 2,081 source files and zero errors.
The stale exploratory failure marker is removed; earlier failed logs remain.

Stop here for the requested form/construction checkpoint. The next work is
look-dev and cause-driven service age, followed by the real bake/export review;
this checkpoint is not the completed game-ready/material delivery.

## Revision form pass 1 — towers, daylight and the loose pairs

Color/value first: opened all eight 1000px exports in `renders/form-pass1/`.
The .65 procedural sky / 3.0 sun ratio is too blue and too diffuse outside;
reject it for the low-sun hero. The soffit is substantially more legible
than the baseline, but the view straight across the stems suppresses depth.
Keep that camera as `retained_aisle`, add an angled aisle/tee view, reduce
sky to .22, restore the 4.5 sun, and keep seven diffuse bounces plus actual
downward fixture pools and unoccluded upward practical light. The section
remains the accepted 24in tee, 4in flange and 6ft stem centers; no clearance
is sacrificed to exaggerate a shadow.

The glazed return, panel joints, lift slot and machine-room hood break the
core prism. Flights still disappear in reflection in the dark core: add
fixtures at exported stair sockets. Name/level plaques are blank because
their backing projects 2mm ahead of the print: recess it. The commercial
trial camera makes the building smaller and adds more foreground; reject
it and retain the accepted location. Far-walk meters do not read at this
angle. Add a native tree and meters at the actual crossing, with a soil well.

Re-measured Harmon from its original 4000x3000 photo. The previous anchors
at x1565/3280 did not identify the same floors. The new crop identifies
four successive ceiling/column stations on each of two adjacent columns.
A five-level specimen from the existing generator fits at 13.22 native px
RMS; the accepted three-level town garage is unchanged. The precast photo
has a deeper lower haunch apex; the specimen lowers that apex to 1.48988m
while retaining the beam seats and tee section. Its four shaft/haunch
anchors fit at 15.81 native px. Pleasant Hill remains 14.9px. These are
comparison variants, not changes to the accepted town plans. The precast
neutral is now bare column concrete left of the sign, rather than paper.
Source pixels enter only local white-balanced comparison images.

## Revision form pass 2 — reject the floating end decks

Color/value first: opened every full-size view in `renders/form-pass2/`
and all three matched pairs. The .22 sky / 4.5 sun balance restores the warm
facade and gives the open levels useful daylight. The pale source deck is
still too uniform; the later material pass must separate its traffic-darkened
upper face from the pale concrete soffit. The column concrete, rather than
the paper sign, is the interior photo's neutral. No material acceptance yet.

The deeper 30in sections make stems and their shadows legible, but the above
view reveals a construction error: the replacement ramp tees applied the
ramp rise at the east end platforms as well as inside the ramp limits.
Reject the set. Limit the replacement rise to central ramp stations, and
retain the actual old topping, connector and pad triangles. Re-run upward
clearance rays on the imported result, rather than treating serialization
identity as a construction test.

The street tree blocks the tower and name; move it onto the opposite
cross-street walk with a real soil well. Mount diagonal warning stripes on
the actual column face with a steel backing, rather than detached planes.
Close the unintended rear tower wall gap and transom slit, correct the
street-facing signs' winding, and add legible floor numerals. The tower
landing camera must show the lift doors and stair door as well as the stairs.
The new buildings close the former empty street horizon; a wider hero frame
reduces the excessive foreground road without moving its eye-height camera.

The precast fit is numerically close but its ramp and cables disagree with
the photo's flat middle seat. Build a two-bay flat calibration assembly from
the same columns, inverted-T girders and tees, with parked native cars. The
Harmon anchors now identify the correct successive floor undersides, but
the five-level specimen ends too soon above them. A six-level, 24-station
comparison version fits the native crop at 5.67px RMS. This private comparison
option does not expand the public generator's accepted 3–5 level program.
Both comparisons are explicitly construction specimens; the accepted town
garages are still four and three levels.

The pre-bake motion audit then found the new lift architraves occupying the
sliding pockets and the revised side pier overlapping the closed street
leaf. Move the fixed architraves in front of the leaf's sliding plane and
shorten the pier to the original aperture; retain every pivot and range.
The regenerated modules and placed assemblies pass all 60 sampled sweeps.
Pigment overlays are explicitly open boundary surfaces, excluded from solid
ray-parity containment; the underlying structural surfaces remain tested.

The prebound UV audit also exposed numerical slivers at band intersections.
Remove subpixel UV/geometry fragments rather than relaxing the imported UV
check. Small manufactured faces translate their texture phase without being
split; large core panels trade transverse density for zero extra geometry.
Tower3 / Tower / Tower5 remain 4,324 / 5,928 / 7,532 triangles. Actual bake
and material acceptance are still pending the next photographic review.

## Revision form pass 3 — fixed platforms and readable cores

Color/value first: opened all 23 full-size scene views in
`renders/form-pass3/`, each comparison PNG and all three side-by-side pairs.
Against the bare-concrete-balanced interior photo, the source floor remains
too clean and bright, with regular luminaire pools. The photo has a darker,
reflective traffic surface, broad side daylight, mottled soffits and deep
local beam shade. Keep the pale cement soffit distinct from the darkened
upper deck finish; reduce the regular pools during the baked review. The
exterior has a useful sun/shade range, but clean panels still read as CG.

The overhead confirms that replacement tees no longer rise above the east
platform. The angled tee view shows deep paired stems and their seats; the
retained aisle provides an honest comparison to the original camera. The
front tower now exposes switchback flights and landing guards through its
return, a glazed lift slot, separate panels, coping and machine-room vent.
Level numerals and opening-hours plaques read correctly. The landing view
shows both real door apertures and the call panel; exterior pull hardware
remains a useful small construction refinement for the next pass.

The new crossing tree leaves the core visible, and the original foreground
camera now sees meters, a planted walk and a queue vehicle. The panorama
reduces the excessive road. Town blocks close the hero's former street end.
Ground Lawn maps, world-XY UVs and the School's maintained-turf tint replace
the quick lawn material; the large commercial lawn still reads too smooth
at this distance. The cyan route appears only on the separate plan view.

The flat two-bay interior specimen is materially closer to the photographed
construction than the ramp: actual inverted-T seats, paired tees and parked
cars. Its haunch landmarks remain 15.81px. Pleasant Hill remains 14.92px.
The Harmon lower-stack landmarks are 5.67px, but the pair reveals that a
six-level specimen stops above them too soon: the photo continues for two
more floors. Extend only this private comparison to eight levels and re-render
it before judging the bake. The scalar landmark fit alone did not prove the
upper massing. The accepted town programs remain four and three levels.

## Look pass 1 — reject the aggregate bump and clean traffic finish

Color/value first: opened all 23 exported views in `renders/look-pass1/`,
the three baked photographic pairs and three original-field pairs. In the
precast pair, the neutral-photo column has display-linear Y .109 versus .181
in the render; the near dark soffit patch is .0079 versus .0175, and the
floor patch is .0696 versus .0787. These are displayed-image comparisons
under unequal lighting, not recovered albedos. The renderer's column is
too yellow/green. Use less yellow cement, neutral practicals, broader side
daylight and lower comparison exposure before judging finer surface detail.
Do not simply darken every concrete surface to match a shaded photo.

The 4096 GPU bake preserves RGB mean to .0000197 and mean absolute error
.00142; OpenGL normals and coverage-aware 2048 filtering are real outputs.
The first attempt caught associated-alpha darkening in the emission input;
bake opaque RGB and restore original coverage before filtering. Source and
baked pairs retain the same large-scale response, but the source's overly
strong height is itself wrong: broad cement clouds and aggregate bump make
the walls look like sponge. Reduce the normal amplitude and macro variation.

Runoff, repaired spots and turning tires are visible in close-ups. Individual
runoff streams merge away too much in the full hero; increase coverage only
on those cap/joint masks. The little repairs still read as round spots at
this scale: use angular cutout patches and vary their extent. Preserve dry
gaps between causes. Decks need a coated traffic response, with roughness
separate from bare soffits, using the same sheet and material rather than
adding a second draw to every structural tile. The fixtures make repeated
white pools on the floor; reduce their downward power and add more sky
and upward bounce. The full-frame wear must improve without a noise wash.

The eight-level Harmon source and baked pair now continue above the measured
stack, but the photograph has a deeper cast edge beam than this town variant.
Add that downstand only to the reference specimen, so its opening/solid ratio
matches the photograph. Keep both actual town programs and their accepted
surfaces unchanged. The three native landmark residuals remain 15.81,
14.92 and 5.67px; the points alone are not a silhouette proof.

Add exterior pull handles to the refined doors, recheck their full motions,
and close the small remaining town gap visible beside the municipal entry.
The large turf plot still needs a more convincing maintained edge. These
are review findings, not claims that the look-dev checkpoint is finished.

## Look pass 2 — neutral cement, stronger cap history, remaining light tells

Color/value first: opened all 18 full-size scene views in `renders/look-pass2/`,
all three baked and three original-field pairs, and the revised form pairs in
`renders/form-pass5-matches/`. The bare-column ROI is now Y .0926 against the
photo's .1093; the dark soffit is .00810 against .00794, and the floor is .0443
against .0696. The green/yellow cast is much smaller. The remaining floor
miss needs more broad side light, not a global albedo/exposure increase that
would spoil the already close soffit. The interior reference looks into an
open landscaped lot, while the specimen still imports opposing town blocks.
Remove those buildings from the comparison only and retain the real towns.

Both heroes have a usable sun/shade range: display-Y p1/p99 is .0053/.8592
municipal and .0269/.8729 commercial, with zero clipped RGB pixels. These
include sky and context. The lower normal amplitude and coated upper-deck
roughness stop the whole asset looking like spongy cement. Cap runoff now
reads in the full hero, but some tails still reveal their rectangular stamp
limits. Taper them out with gravity, and start them on the actual vertical
face at the cap edge. Keep the visible repair patches angular.

The interior is legible throughout the aisle, with proper paired stems,
supports and open sides. The near uplight hotspot still advertises an area
light beside a closed black housing. Make the fixture a real wraparound
diffuser, put the presentation emitter above its exposed lens edge, reduce
its upward power and shift the balance toward sky/floor bounce. This can
retain the fixture's existing triangle count. The new exterior pulls remain
clear through all 60 measured motions.

The Harmon downstand fixes the opening/solid ratio, and its hazier illumination
is closer to the photo. The square town columns still differ from the photo's
round forms. Use a round cast-column variant only in this private specimen;
the measured fronts stay at the same diameter and coordinates. Pleasant Hill
keeps its accepted fit with a lower-sun lighting match. Source and baked
pairs preserve the intended response without a broad color-space shift.

The municipal entry still finds a small flat horizon to its northeast; add
one instanced closing frontage there. The lawns now use the School/Ground
maps and maintained tints, plus a mown edge. Their distant large plots still
read simpler than a photograph. Fine stains, oil and droppings resolve in
close views; the full hero carries the larger cap/joint service history.

## Look pass 3 — reject sun on the neutral column and the commercial framing

Color/value first: opened all 25 full-size exported scene views, the two
baseline open-door views, and all three baked plus three original-field
pairs, archived in `renders/look-pass3/` and its paired folders. Removing the
comparison's opposing buildings admits the needed floor daylight: floor Y
is .06253 against .06963 in the concrete-balanced photo. But it also admits
direct low sun onto the camera-facing column, lifting it to .26164 against
.10930; the soffit is .01143 against .00794. Reject that column lighting.
Put the comparison sun behind the visible face, as the shaded photograph
requires, before judging material color again. Keep the new broad sky and
open lot. These display-linear readings are not albedo measurements.

The municipal hero has display-linear p1/p99 .00030/.70944, commercial
.00206/.73499, and neither has clipped RGB pixels. The wraps now expose a
real diffuser edge below the uplight, rather than a light beside an opaque
housing. Regular floor pools remain a procedural tell. The deeper paired
stems, actual seats and brighter floor resolve the former tunnel/flat-ceiling
read. The new cab and inner sliding panels make the opened elevator usable;
the surface leaves still lack enclosed pockets and the cab does not travel.

The northeast frontage closes the municipal entry horizon, and the exported
queue tires now meet the actual sloped apron. The commercial hero still puts
the crossing tree and meters outside the frame. Move only its public hero
camera farther across the crossing street, retaining 35mm/1.65m and the old
camera for the direct before/after. Re-render the set with that correction.

Cap runoff is visible in the heroes and tapers off instead of ending at a
rectangular stamp, but close-ups still reveal comb-like stream groups.
Small engine leaks, mineral deposits and roost marks remain detail-scale;
the full hero does not make each independently identifiable. The reference
precast floor is wet and carries broad cleaning/tire swirls; the dry specimen
does not yet reproduce that state. Harmon has the correct round cast forms
and an improved edge/opening ratio, but its surfaces remain more uniform
than the photo. Tight 15.81/14.92/5.67px fits do not erase those look misses.

## Look pass 4 — useful public views, unresolved column illumination

Color/value first: opened all 25 final scene views and all six original-field
and baked pairs, archived as `renders/look-pass4/` and its paired folders.
The sun is now behind the photographed column face. The concrete-balanced
floor median is .06970 against .06963 in the photo; the near dark soffit is
.00955 against .00794. The bare column is still .22498 against .10930.
Checked diagnostic ROI overlays on both full-size images: the column patch
is bare cement in each, not a sign. Reject the remaining column illumination
before changing finer surface detail. Separate sky, sun and practicals on the
same exported specimen to identify the cause rather than tinting that patch.

The public heroes retain deep shade and unclipped sunlit concrete: municipal
display-linear p1/p99 is .00030/.70944, commercial .00126/.72468, zero clipped
RGB pixels in both. The new commercial camera includes its crossing tree and
walk while exposing the flights through the glazed return. The surface car
row still hides much of its entry queue; meters are partly hidden by the tree.
The dedicated entry views make the actual queue/apron contact clear.

Closed 2mm formed pockets now conceal the opened lift leaves. Zero-thickness
pockets failed the solid-parity check despite no triangle crossings; real
skins pass all sixty motions without a new collision exemption. Six-sided
small stair tubes fund that construction, reducing the tallest tower to 7756
triangles. The fixed ground cab is usable and lit, but does not travel.

The independent GPU repeat passes the predeclared tolerance: BaseColor and
ORM are exact; three normal-map pixels differ by one eight-bit code each.
Canonical maps remain frozen. Runoff combs, smooth distant turf, repeated
native actors and detail-scale minor stains remain visible CG tells. The
dry floor still differs from the photograph's wet cleaning/tire swirls.

## Look pass 5 — surrounding construction before color tuning

Color/value first: inspected the isolated sky, practical and sun renders,
the longer-roof probe, all three wet-floor probes, all three camera-side
continuation probes, and both narrower-distribution probes at native size.
The short comparator's sky-only column was Y .17090; practical-only was
.02522 and sun-only .00006. Direct sun was no longer the main error. The
small roof admitted sky from sides that the photographed structure continues
beyond. Extending the eighteen-tee assembly behind the camera lowers the
column to .10235 with the public fixture preset, against photo .10930.
Its floor then falls to .03533 against .06963, and soffit .00414 against
.00794. This is a construction/illumination issue, not a reason to darken
the shared column material.

Retain the surrounded flat assembly and broad wraparound practicals at 1.5
times the public preset. The 960px probe gives column .13066, soffit .00674
and floor .05241. That reduces the former twofold column miss, while leaving
the floor about a quarter darker than the photo. The visible central measured
coordinates and 15.806px native fit do not change. The surrounding roof's
extent outside the crop is inferred; it is not a surveyed full footprint.
The public garages, their lighting and accepted programs are unchanged.

Reject the wet-floor probes: their stronger clearcoat/darker cement lowered
the foreground without correcting the column. Reject the 100/120-degree
downward spreads: they made isolated bright pools and a darker foreground,
unlike the photo's broad reflected light. Those variants remain diagnostic
build files only. The photo's wet cleaning/tire swirls and cooler bounced
light remain unreplicated; do not call this a complete material match.

Opened all sixteen 1200–1280px-per-panel fixed-camera comparisons. Daylight
now reaches the public aisle floors and soffits, stair flights read through
the tower returns, and the enclosed lift pockets conceal opened leaves.
The aligned retained aisle still foreshortens the tee depth; the transverse
tee detail and the matched interior are the clearer construction evidence.
Cap runoff still forms comb-like groups and distant turf remains smooth.

## Look pass 6 — final exported checkpoint and its limits

Color/value first: opened all twenty-five 1280px final scene views, the two
baseline open-door views, all six baked/original-field photo pairs, and the
final scene, pair and before/after contact sheets. The concrete-balanced
precast comparison is column Y .13066 versus photo .10930, soffit .00720
versus .00794, floor .05117 versus .06963. The former twofold column error
is reduced to about twenty percent; the floor remains twenty-seven percent
darker and warmer than the wet photograph. This is a remaining look miss.
The public heroes have display-linear p1/p99 .00030/.70944 municipal and
.00126/.72468 commercial, with zero clipped RGB pixels in either image.
Deep shaded bays remain dark while sunlit concrete retains its highlights.

The broad original manufacture fields and filtered bake preserve the same
appearance without a large color-space or roughness shift. The actual tee
stems and seats now read in the transverse underside and matched views.
The aligned retained aisle still foreshortens them. Tower returns reveal
flights and landings; opened leaves fit within closed pockets and reveal a
lit ground cab. That cab remains static, with no vertical travel controller.
Every existing delivery remains protected and the public geometry is unchanged
from the preceding candidate. The one drawn route is confined to its plan.

The Harmon diagnostic's marked projections were also overlaid on its actual
render and photo: the two selected column stacks align, with 5.674px RMS,
but that does not certify the whole facade silhouette. Its periodic columns,
cleaner cement and more uniform ceiling still differ from the photograph.
Pleasant's accepted 14.923px fit remains intact; precast is 15.806px.

The municipal street view is closed by native frontage. Commercial includes
the crossing tree and walk, but surface cars obscure much of its entry queue,
and the tree partly hides the meters. The entry details show the queue.
Runoff combs, smooth distant turf, repeated cars and regular light pools remain
CG tells. Oil, connector rust, salts and roost marks resolve in the detail
views; each is not independently identifiable at full hero framing. The upper
deck's sealer history is still subtle. These are checkpoint limitations, not
claims of a finished photographic match. Stop before the README gallery/docs.

## Delivery pass 7 — checkpoint diagnosis before the final corrections

Color/value first: opened the two 1280px checkpoint heroes, the municipal
aisle, the commercial top deck and the 2400px tower comparison at native size.
The heroes' pale horizon and broad facade fill suppress the difference between
sunlit spandrels, shaded shafts and deep openings. A numeric unclipped range
does not excuse that low local contrast. Retain the accepted interior practical
lighting and photo-pair presets; revise only the public exterior daylight.
Use the facade photograph's bare cement for the new value comparison, rather
than its temporary fence sheet. No photograph contributes texture pixels.

The new eight-way car-color selection will use the original family palette
for its five principal colors, anchored to DuPont's 2010 North American white,
black, silver and red shares. Other shares are explicitly authored, not a
used-fleet measurement. Four native model geometries and independent per-stall
choices should break the identical dark frontage. The commercial surface row
needs a driveway/sight gap at the entry, not a different hero camera.

The age source contains seven regularly spaced rivulets per stamp. Delete
that construction of the coverage field. Wet joints should feed irregular
plumes, with crystalline salts at their margins and terminal deposits. Most
panel fields should remain dry. The aisle needs broad accumulated tire traffic
and larger dispersed engine leaks; the top lane needs visibly abraded sealer.
Retain the actual tee/seat sections, clearances, towers, turf and fitted pairs.

The floor's blue squares lack their surface ISA. Access Board chapter 5
requires stall and access-aisle markings but specifies no marking color.
Use blue diagonal hatches inside the retained clear aisles and a small blue
ISA background in each stall, with a white symbol and the existing elevated
signs. No full stall is a solid blue panel. These changes remain unjudged
until the exported candidate is opened from the unchanged cameras.
