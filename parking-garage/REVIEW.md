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
