# Commercial / gas-station form review

This gate stops before look development. Review pictures are ignored outputs,
not committed portfolio art. All station images use the exported diagnostic GLB
with its own quick materials. Reference photographs are inspection inputs only.
No photo is projected, traced or used as a texture. No acceptance of age,
manufactured masonry, baked wear or final material response is implied here.

## Photograph protocol and limits

The Pennsylvania canopy photograph is dated May 2006 and the California
operating-dispenser photograph August 2009. Louisiana 2008 and the undated
Colorado view add regional construction and site comparisons. Attribution and
rights are in refs/SOURCES.md. The first three preview rounds below were visual
comparisons, not calibrated pairs; the later pair review uses kit/photo_match.py.

Before comparing hue, `prepare_refs.py` balances PA on sunlit forecourt concrete
at native pixels (150,1400)–(250,1450), assumed neutral gray. Linear RGB gains
are .8890 / .9682 / 1.1872. The warm soffit was rejected as a neutral because it
would force an excessive blue correction. CA uses the light background store
wall at (1050,110)–(1190,180), gains .9903 / .9903 / 1.0200. These assumptions
remove a cast, not the effects of light, exposure, camera response or material.
`build/reference-balance.json` records original/copy hashes and exact ROIs.

The PA fit uses four column/soffit and column/island points across a 50 ft span;
it solves 79.37 mm, RMS 1.66 native pixels. The CA fit uses four lower access-panel
corners; it solves 44.00 mm, RMS .28 native pixels. Kit independently projects
those landmarks through Blender before rendering. These are sparse structural
fits: neither independently measures a whole site or proves the chosen width.
PA has two column rows, broad cladding, a rounded roof and surface fixtures;
our original station has one row, slender square finishes, a flat fascia and
flush fixtures. CA's active hose and our holstered hose are different states.
These held-out differences stay visible; a low residual cannot certify them.

## Pass 1 — reject the presentation and opening failures

Evidence: `renders/pass1/`, including its contact sheet; compared visually with
the dated photographs. These preliminary images have superseded source hashes.

**Color/value first.** The reference's shaded dispenser surround is dark neutral,
with very dark nozzle recesses; the preview's big light panels and glass were
too uniformly bright. The photo's pale sunlit concrete is not evidence for a
pale dispenser, slate-blue black plastic or tan concrete. Separate dark interior
and rubber values were retained, neutral concrete reduced, and glass/backings
were reworked. This is a form palette correction, not a final albedo solution.

**Rejects.** Lettering disappeared through the UV consolidation. Front glazing
read as frosted slabs. The public corner had a seam. The retail entry needed a
real opening rather than a door over a wall; the paired leaves needed an exterior
hinge and an unobstructed threshold. Small props had closed bucket/rim shapes
that could not actually hold the washer tool.

**Changes.** Normalize UV layers, create true storefront/entry apertures and a
shallow dark foyer, correct glazing depth, join the corner return, hollow the
trash/washer rim and bucket, and attach the squeegee to their support. Keep the
canopy at the researched clear height rather than lowering it to fill a frame.

## Pass 2 — reject text orientation and nonworking assemblies

Evidence: `renders/pass2/`; visual comparison to PA soffit/column/pump scale and
CA cabinet/reader/nozzle construction.

**Color/value first.** Dark controls now separate from the cabinet, and cavities
are legible. The gray soffit can remain darker than the sunlit reference because
of light direction; changing it to blue or a chalk-white wash would conceal the
problem. Keep warm metal and concrete neutral rather than compensating for the
reference's white balance with material color.

**Rejects.** Some letters were garbled or rotated: having an image and a UV layer
was insufficient. The hose tether did not meet its actual curve station. Fixed
entry rails crossed a moving leaf. Ice/cage/yard parts had to clear their real
surroundings, not simply export with correct pivot names. The air coil had no
credible supply attachment.

**Changes.** Assign raster text UVs by vertex identity, consolidate only after
letter generation, tie the retractor cord to the true hose point, remove the
false entry rail, reposition exterior hinges, and use real ring openings. Add
a supply hose and support hook to the air machine. Use 5° solid-surface sweeps,
including closed poses, with no allowed-contact exceptions.

## Pass 3 — reject floating graphics and the false cylinder profile

Evidence: `renders/pass3/`, opened hero, dispenser, canopy, entry, sign, rear and
motion views. Comparison again starts with the neutral-balanced period photos.

**Color/value first.** The aubergine remains a dark colored field; the copper
mark is warm without turning the whole station tan. The upper nozzle pocket
must stay dark. The model is still much too smooth/clean to represent fifteen
years of service. That remains explicitly unaccepted at this pre-look-dev gate.

**Rejects.** Floating small captions cast detached shadows. The price sign's
lower text crowded the base. A reversed `(height,radius)` lathe profile produced
false cylinder geometry inside the cage and failed gate sweeps. These are
construction defects even when hidden in a whole-station shot. The first site
interface lowered the gutter pan with the depressed curb, so its nominal
entrance width did not prove compatibility with ground.

**Changes.** Support lettering on actual faces. Correct the original cylinder
profile, move gate hinges clear of jambs, put the island base on the concrete
pad, and set RTU feet on the actual roof membrane. Load the ground family's
native profile and transition function instead of approximating it; preserve
pan elevation while depressing only the curb, use native corner stationing,
and give the public walk its true crossfall. Add distinct private-paving,
curb-flowline, apron and sidewalk sockets with measured frame checks against
the delivered Ground GLB.

## Pass 4 — whole-site and calibrated-pair rejection

Evidence: initial `renders/checkpoint/` set, archived under `build/pass4/` before
replacement; four above/street views, seven main construction views, open entry,
same-scale context and the two kit-calibrated pairs. Every initial view was
opened on a sheet; the dispenser, entry, sign and context were also inspected
at full size. Final files at those paths are the later pass.

**Color/value first.** The quick palette has deep storefront/nozzle cavities and
a dark colored fascia. PA's concrete contains warm exposure and dust after
neutral balance; matching that with a global yellow concrete tint would be
wrong. CA's nearly neutral black surround shows broad specular response, whereas
ours still has simplified scalar roughness. Accept these differences only as
surface work remaining; the form gate does not accept a clean CG surface as a
used station.

**Rejects from the whole site.** Overhead cameras clipped the front property
corner and price sign. The small white retail descriptor lacked contrast on
its light concrete belt. The premium digits and price legal line overlapped.
The same-scale pickup hid behind the canopy; the orthographic presentation's
bottom rays also passed below the distant grade. The house's sunken driveway
needed an opening in that presentation grade, not a blanket plane over it.

**Changes.** Widen above-view field of view, give the caption a dark neutral
state, separate all price rows from the legal line, show the pickup broadside
in the front forecourt and raise the scale camera. Cut only the presentation
grade around the split's exported driveway bounds. Preserve and hash the house
export, external buffer/maps and pickup; no context enters the station GLB.
Street camera Z is set from the actual road datum; a ray measures 1.6800 m
from that surface rather than claiming the camera's absolute elevation is eye
height. The current source remains at the same dimensional design.

## Pass 5 — reject the ramp landing and photo-light cast

Evidence: complete 19-view set in `build/pass5/`, including the two calibrated
pairs and their landmark overlays. All required views were opened on the sheets;
price sign, scale context and both pairs/overlays were opened separately.

**Color/value first.** Correcting the generic match exposure and increasing sky
fill brought the shaded surfaces closer in value, but the PA soffit and CA
concrete acquired too much blue. The high sky fill also desaturated the brand
fields. This is a lighting rejection: do not bake blue into black trim, tint the
concrete warm, or alter the fictional brand to counter it. Test a procedural
neutral ambient field for the photo comparisons, leaving the ordinary street
preview's sky lighting alone. There is no downloaded environment map.

**Form judgment against the photographs.** The cabinet width, hydraulic base,
control reach and 30 mm hose read at real scale. The nozzle is supported by a
holster and a separate spout pocket, and the retractor does not substitute a taut
line for the hanging fuel hose. CA shows an active U, ours a stored U; the state
difference cannot prove exact deployed length. Our compound nozzle is still
coarse under the extreme camera crop. PA's 50 ft structural span and clear height
align, but its larger clad columns, two rows and rounded roof are visibly another
construction system. The source's deep single-row cantilever places the fascia
outside this crop; that pair cannot validate our fascia ratio. Published
14 ft 6 in / 3 ft / 25 ft details plus the independent whole-station and edge
views support those choices. No claim of an entire matched station is made.

**Rejects.** The initial accessible ramp ran the whole 7 ft walk and had no level
top landing. That is a construction miss despite its correct stall/sign colors.
The price captions are now clear and the pickup is visible at the house's scale;
those earlier defects are resolved, not reasons to accept this remaining ramp.

**Change.** Make the store walk 12 ft deep: a genuine 6 ft 1:12 run and a 6 ft
level landing, wholly beyond the level stall/access aisle. Shift the parking row
with it, and adjust the perpendicular-canopy pickup route. Rerun all four routes
with occupied store parking, actual ramp/landing surface probes, door sweeps and
export checks. This is a dimensional approach proof, not an ADA permit audit.

## Pass 6 — neutral light, whole-property framing and construction audit

Evidence: `build/neutral-preview/` tests, followed by the calibrated pairs;
whole-station, family and detail sheets were inspected again. Earlier sheet
versions are superseded by the current GLBs and current 19-view set.

**Color/value first.** A neutral procedural ambient field removes the excessive
blue sky cast from the pair views without tinting any asset material. A .4-strength
neutral-light test was too dark: sampled roof patches read approximately
(.35,.35,.33) against (.47,.42,.38) and (.53,.48,.42) in PA. The final comparison
uses .7 neutral ambient and −.15 exposure; PA also changes sun direction. The
reference soffit remains warmer from its finish and service dirt. Do not erase
that material difference through global yellow concrete. Main street views keep
the original procedural sky and darker cavities. This lighting test is not
accepted final look development.

**Rejects and changes.** A manual wider overhead lens still clipped the rotated
tank pad. Fit every actual exported station vertex inside 4% camera margins and
record those bounds. The pump initially had brand colors but lacked the fuel
name/mark and separate per-grade price windows. Add them on both faces; remove
unreadable keypad microbevels so the worst pump stays below 6,000 triangles.

Closed black scupper proxies were not genuine wall openings. Add holes through
the rear wall, lined sleeves, open tapered conductor heads and hollow downpipes.
Straps wrap around the pipe rather than crossing its bore; the outlet clears
the splash block. Probe the actual passages. The front/rear masonry was centered
on the footprint boundary and overhung its slab. Set its outer faces on the
nominal footprint, align coping to the real wall centers and independently ray
measure all four outside wall planes. Seat the original cage cylinders on the
shelf surfaces rather than leaving a 7.5 mm gap.

Finally, isolated shrub pads did not fulfill the landscape-strip program, and
all signs used the same corner placement. Replace the pads with continuous
edged rear/east beds. Give seeds 102/103 south/west frontage sign placements,
with seed 103's broad face rotated toward its street. Add sign foundations to
the occupied-parking/island route obstacles and retain all four viable routes.

## Pass 7 — accepted form checkpoint, stop before surfaces

Evidence: current `renders/checkpoint/{family,details,contact,circulation}.jpg`,
the underlying nineteen Cycles PNGs, both `renders/matches/*-pair.jpg` images
and their calibration overlays. All views were opened on sheets; hero,
dispenser, pair images and circulation were also inspected separately. Current
source/image/recipe hashes are checked in `build/view-check.json`.

**Color/value first.** The hero's projected architecture/equipment mask has
Y′ p1 about .058, p50 .369, p95 .624 and p99 .780; white-clip fraction is zero.
It retains deep store/nozzle cavities and a dark colored fascia. The paired
views now have neutral shade rather than blue concrete. The used photographs
still have visibly more local dirt, finish variation and roughness response.
That difference remains unaccepted for the future material stage; no noise
wash or blanket brightening is an acceptable substitute.

**Form judgment.** The 14 ft 6 in canopy reads at service height, with a strong
3 ft 3 in fascia, real flush-light holes, column guards and connected drains.
Combined islands leave 21 ft between curbs. The dispensers now read as formed
hydraulic/electronics cabinets with two operating faces, supported nozzles,
properly thick slack hoses, per-grade prices and fuel-brand identification.
Sale totals derive from the same unit-price constants as the cabinet and sign.
The store's walls fit their slab, divided aluminum frontage has real apertures,
and outward leaves work over the level landing. Rear services and selected
coolers keep the back from being a blank extruded box. Scupper passages and
hollow conductors are construction rather than black marks on masonry.
The final hero also exposed coplanar overlaps in the presentation road skins:
dark rectangles were false self-shadow, not asphalt wear. A single disjoint
union surface removes them. The station GLB remains byte-identical through
this staging correction.

The four corner orientations, canopy axes/counts, store colors/sizes, cooler
presence and corner/frontage signs read as different stations. Continuous
planting strips bound the nonstreet edges. Each has a forward-only pickup body
route through a fueling lane and the other street opening, with store parking
occupied and sign foundations included. The tightest SAT gaps are .225 / .310 /
.225 / .286 m; these are demonstrated paths, not comfortable two-way traffic
or a tanker certification. The extended pure-plan regression passes the same
pickup envelopes on 1,000 seeds; source solids/imports are checked on four.
Above views include every exported vertex within
measured margins; street eyes are measured 1.6800 m above their road surfaces.

**Independent checks.** Four outside-plane rays measure each store's actual
nominal width/depth. Roof, nominal soffit, island envelopes, hose surfaces,
ramp rise and level landing are probed on source geometry. Eleven assemblies
per seed pass 948 total sampled 5° poses without penetration beyond 1 mm or
allowed-contact exceptions. Raw GLB normals/counts and fresh-import positions/
node frames separately prove serialization. The default factory-startup repeat
is byte-identical. The owner's read-only .3122 × .4680 m cylinder envelope fits
the declared horizontal bay and ray-measured .6650 m shelf height; it was never
joined, saved or exported. The ground profile audit compares actual delivered
curb vertices to actual station surfaces, not constants on both sides.

**Remaining weaknesses and next gate.**

- All masonry, paving and equipment still have quick smooth scalar finishes.
  No manufactured relief, causal fifteen-year wear or final baked response is
  accepted. The spare shrubs and presentation roads are also form work.
- The small cooler condenser inherits the large RTU's fan/grille proportions;
  give that size a properly fitted fan layout during detail refinement. Tiny
  pipe/cylinder fittings and the extreme-close nozzle remain coarse.
- PA's clad two-row canopy and CA's active hose are different designs/states.
  The sparse camera fits do not prove an entire matched station, fascia profile
  or deployed-hose motion. The source canopy's fascia is outside the PA crop;
  its separate edge view and published dimensional comparators carry that check.
- Raised brand marks are temporary. Final guarded decals, geometry-independent
  brand swaps, shared ground-image URIs, draw calls, UV density/overlap policy,
  bake transfer and final GPU uploads remain unverified.
- Nozzle detachment frames and hand sockets exist; runtime hose deformation is
  not implemented. There is no tanker, opposing-traffic or structural-load audit.

The form gate is ready for lead review. Stop here: no look-dev bake, final docs
JPGs, portfolio claim or strip-mall construction has been started.

## Pass 8 — first exported surface rejection

Evidence: `renders/form-fixes/` and `renders/look-pass1/`, inspected individually
at their full 1200/1440-pixel width. The nine look images use the freshly
imported `build/look/station-101.glb`, including its embedded GPU-baked maps.

**Color/value first.** The neutral CMU retains its gray, but its per-unit firing
range is far too strong: the wall becomes a checkerboard at street distance.
Reduce unit variation from .84–1.15 to .95–1.05, leaving mortar and manufactured
face relief in the normal. The brand panels retain their aubergine; the marks,
grade numbers, safety captions and price digits do not retain their intended
colors. Inspecting the source Tint and raw GLB shows an actual export loss:
the source contains the copper/red/black values, while those primitives export
white COLOR_0. Emission also cannot depend on COLOR_0 in standard glTF. Put the
original inks directly in the shared graphics cells; use a uniform amber LED
emission state. Do not recolor the entire scene to hide this failure.

**Construction review.** The first full-height pilasters cut across the store
wordmark. Terminate the bay piers at the storefront head, retaining the precast
base/capital and sheltered entrance. The sign cap partly hides its legal line;
separate that line from the last price row and reduce its type. The hose loop
now reads round at the dispenser close-up, without the former stray wire. All
four revised source assemblies pass their motion sweeps and ground-interface
measurements. Source/instance counts and raw unique-mesh counts are distinct.

**Reject the first wear transfer.** Large elliptical oil splats look painted,
despite being placed under engines. Replace them with smaller overlapping,
ragged drips and reduce coverage; keep their real parking/fueling locations.
Repeated coping marks are too black and graphic: lower their alpha, soften
their tails and retain their seam heads. The bark is stretched over an entire
long bed and reads as planks. Add local bed charts at physical chip scale.
The boxwood itself retains the stock family's leaf silhouette and shared maps.

**Presentation.** The new ground geometry/materials remove the smooth green
proxy and give the street its true crown, but the first hero still spends too
much of the frame on road and sky. Keep normal lenses and verticals; refine
the composition, add neighboring context, and judge again. No surface or age
acceptance follows from the successful flat bakes or source checks.

## Pass 9 — reject the comparison light and the remaining generic surfaces

Evidence: all ten `renders/look-pass2/` views and all four exported
`renders/look-matches/*-pair.jpg` comparisons, opened individually at full size.

**Color/value first.** Copper marks, red safety text, black octane numerals,
blue ice lettering and amber prices now survive the export. The restrained
CMU unit range removes the checkerboard. The matched sun/sky pairs still put
the neutral soffit, white steel and concrete too far into cool shade compared
with the photographs. Preserve the real gray albedos; adjust the procedural
sky's chroma/cloud fill and the comparison exposure, keeping the explicit sun
and directional shadows. Each sky's solar elevation/azimuth must agree with
its sun vector. The first Texas neutral candidate was sky, not a metal roof:
reject it before measuring and use the visible aluminum entry jamb at
(1240,1070)–(1245,1150). Its measured linear gains are 1.0282/1.0071/.9666.

**Material/age judgment.** The oil is better localized but still contains
recognizable long elliptical fingers. Replace the shape generator with a
granular irregular accumulation core and small satellite drips. The bark now
has physical local charts rather than stretched long lines, though its
pattern is still more orderly than real shredded mulch. The low CMU dirt and
salt survive, while coping deposits are appropriately quieter after reducing
coverage. Add retained sediment beside the actual fuel-pad joints. No blanket
road-film field or all-over wall noise is accepted.

**Form and delivery.** The equipment's whole finished palette is now shared;
each dispenser uses 5,000 triangles before the final cast-body refinement.
The source and external glTF surface/motion checks pass on four seeds. Raw
UV/normal/guard and fresh-import checks also pass, with canonical ground and
shrub image reuse. The meter remains a blank silver disc in the close-up:
give it its sealed glass, LCD/readout and disconnect handle. The nozzle cast
sections can use a few more radial stations within the 6k cap. Leave the
accepted hose diameter, loop and cabinet proportions alone.

**Presentation.** The 40 mm, 2.65:1 framing study gives the architectural span
about 70% of the frame width, from the actual opposite sidewalk. That viewpoint
puts the monument over the entry; use the other street's opposite sidewalk
for the hero/dusk while retaining a clear island. Add own-library neighboring
houses and trees, without exporting context. The new physical emitters finally
light the canopy's pad and store interior at dusk; the first almost-black
night preview is rejected, not promoted as a successful emissive test.

## Pass 10 — neutral values, real shader inputs and final chart scale

Evidence: all seven `renders/look-pass3/` views at full size, the four
`renders/look-matches-pass3/` pairs and fixed material patches. The first
EIFS patch fell outside the rendered wall (transparent pixels); reject that
invalid sample and place its fixed rectangle on the actual upper wall before
comparing it. These statistics measure display appearance, never albedo.

**Color/value first.** Neutralizing only the procedural sky's chroma removes
the previous blue cast without warming any concrete map. In the fixed pairs,
soffit Y′ is .427 versus .417, concrete .636 versus .795, dark surround .213
versus .135, and EIFS .717 versus .663. The soffit and EIFS medians are close;
the concrete and dark surround are not. Photo/model R:G:B for the soffit is
1.114:1:.867 / 1.009:1:.954, and concrete is 1:1:.995 /
1.012:1:.975. The warmer aged photographic soffit is retained as a finish
difference rather than used to tint all neutral paving.

The concrete patch was suspected to be in canopy shade. An independent camera
ray/solar ray probe rejects that explanation: its region has zero blocked sun
samples. Tune the sun/sky ratio for the photograph's high-contrast sunlight;
leave the accepted ground-family maps byte-identical. The cabinet is a different
make/finish, but its brighter dark surround remains a visible limitation to
address or explicitly retain, not a passing match hidden by the fit error.

**Full-size rejects.** The new lamp states make daylight fixtures appropriately
off while the store is lit; dusk still uses the exported authored strengths.
The meter now has its sealed front and readable display. The hose and the
slightly finer nozzle castings retain their original dimensions. The hero's
new sidewalk clears the entry, with the monument at its right, and shows the
island. Neighboring original houses and trees improve context. Their lawn
looked dark because the imported shader requested a vertex color missing on
the new presentation skin. Supply that actual shader input; do not replace the
ground material with a guessed green. Narrow the joint deposit halo from
160 to 70 mm, avoiding a broad artificial band. The mulch still reads as flowing
grain: replace it with independently oriented angular chips at the same chart
scale. No triangle or image allocation is added by those material fixes.


## Pass 11 — reject blocked evidence and stamped turning marks

Evidence: the final-size sign, rear, services, fueling pavement, landscape and
night views, plus every seed's street and overhead view, opened individually.
These are intermediate checkpoint images; their replacements must pass the
current export and presentation hash audit.

**Color/value first.** The neutral soffit is now .434 versus .417 in the fixed
PA patch; EIFS is .694 versus .663, and the darker molded surround .159 versus
.135. The PA concrete remains .636 versus .795. A rejected high-sun study
raised the concrete to .816 but also drove the soffit to .647, so it is not a
credible whole-frame solution. Retain the ground family's real material and
report the twenty-percent paving gap. The cabinet's remaining eighteen-percent
appearance gap is also not a passing match. These are display Y′ medians,
not recovered material reflectances.

**Evidence defects, fixed at their causes.** The added oak completely occludes
the rear camera. Move that presentation tree beyond the camera; do not accept
a foliage image as proof of rear services. The first extended neighboring lawn
also crossed the public road and left black slivers beside it. Replace those
rectangles with disjoint regions excluding the actual road/walk envelopes;
continue native curb, walk and verge beyond the station's own interfaces.
The driveway wear reads as eleven stamped dashes rather than continuous tire
contact. Replace each path with one tapered swept strip whose UV follows its
length. This retains exactly the same triangle count and shared sheet.

**Determinism defect.** The repeat build exposed unordered import of the two
stock Boxwood meshes. Sort their names before instancing. The corrected export
then repeats byte-identically, and a brand-swap build preserves oriented
positions/normals, all 196 node frames and the same 24 embedded image payloads.
Repeat both checks again after the tire-strip change.

**Retained weaknesses.** The bark is angular and correctly scaled but flat in
raking close-up. Shelves carry simple repeated package fronts. Even with the
real public ground modules and two neighboring houses, this remains a sparse
context, especially from above. Do not call these images portfolio finals.


## Pass 12 — exported checkpoint, final full-size critique

Evidence: all twenty final station/family Cycles PNGs at 1600px, all five
matched render PNGs, their pairs and fixed-value crops, all seven historical
before PNGs and their before/after sheets, opened individually. The combined
contact and separate family/detail/pair/form sheets accompany them. Current
source/buffer/map, image, camera-recipe and context hashes pass for 25 views.

**Color/value first.** Final fixed appearance patches are:

| Surface | Export Y′ | Neutral-balanced photo Y′ | Difference |
| --- | ---: | ---: | ---: |
| soffit | 0.434 | 0.417 | +4.2% |
| concrete | 0.636 | 0.795 | -20.0% |
| dark cabinet | 0.159 | 0.135 | +17.9% |
| eifs | 0.692 | 0.663 | +4.4% |
| asphalt | 0.544 | 0.466 | +16.8% |

The PA soffit remains less warm: R:G:B is 1.009:1:.946 against
1.114:1:.867. Neutral concrete remains 1.012:1:.975 versus 1:1:.995.
EIFS is 1.020:1:.958 versus 1.036:1:.917. The asphalt is slightly cooler,
.978:1:1.029 versus 1.025:1:1. These display measurements include illumination,
response and finish differences. The concrete, asphalt and dark-surround gaps
remain material visual weaknesses; no exact photometric match is claimed.
CMU retains a gray body without the rejected checkerboard, brick reads red
rather than purple, roofs remain gray, and brand panels retain their ink hues.
Hero geometry-mask Y′ p1/p50/p95/p99 is .086/.464/.637/.802; only .025% of
masked pixels clip all three channels. The mask includes poles, so its 94.6%
width is not reported as the building/canopy span. The architecture occupies
roughly three quarters of the horizontal frame by visual inspection.

**Supplementary asphalt evidence.** The original four pairs gave too little
asphalt. Add a fifth, against the used 2009 VA station. Reject the first view:
its unconstrained camera falls to .88 m and looks across lawn. Use adjacent
column stations and a 1.65 m eye prior. Picks made on a 1920px inspection
image must be converted to the native 3888px grid; the initial unconverted
crop/neutral is rejected. Corrected neutral gains are .9663/.9663/1.0750 on
sunlit gray aggregate between shadow bands. A roughly 37° procedural sun
follows the long winter shadows. The final 59.1 mm camera has 19.26 native-px
RMS (about 9.5 inspection pixels), markedly weaker than the primary fits;
this is a paving surface comparison, not proof of an identical plan. Reject
and trim the first asphalt value rectangle's few foliage pixels before the
final statistics above. No photograph enters the authored materials.

**Construction judgment.** Stock boxwood has a real leaf silhouette and sits
in bark beds. The lower hose U is smooth at full size and the stray tether is
gone. Storefront piers, split-face returns, entry shelter and coping folds
read as assembled construction; the services are visible and supported.
The sign has its matching masonry, cap and framed cabinet. The column wrap
has a skirt, seam and band. Front glass reveals stocked shelving, the cooler
wall, counter and ceiling lights. The rear tree no longer obstructs evidence.
The road/curb/walk lawn joins have no black slivers. Continuous tire paths
remove the stamped-dash tell. All four corners remain complete and fitted
inside the overhead views.

**Age and presentation judgment.** Engine deposits, low masonry moisture,
threshold gum, base corrosion, repairs and tire turns are local and keep the
surface's own color. The strongest repair/turning marks survive the full
street frame. Coping streaks and hand/base grime remain quieter there than in
close-ups. Dusk lights the pad from the actual exported luminaire faces and
shows the prices, brand panels and visible shop; it is dark outside that pool.
Normal-lens street eyes are measured at 1.60 m on the opposite sidewalk,
with level verticals. The hero's entry clears the monument.

**Still CG.** Plain gray roof fields, regular masonry/soffit manufacture,
flat bark relief, repeated package fronts and simplified nozzle/guard details
remain legible at close range. Asphalt aggregate is more evenly distributed
than the photograph's patches and abrasions; the PA concrete lacks its broad
worn variation and is too dark. The five pairs are not photographic matches.
Context is sparse beyond the public streets. This is the requested look/age
checkpoint, with no portfolio-final claim or committed docs images.

**Proof at stop.** Full `make WIDTH=1600 SAMPLES=48` passes: 1,000 plans and
eight rejected negative controls, four construction/import checks, 948 sampled
moving poses, four raw-delivery chart/normal/density/import audits, canonical
image reuse and 25 current exported views. `make repeat` is byte-identical
(73,894,428 bytes); both brands retain geometry, 196 frames and 24 embedded
image payloads. The source manufacture fields also repeat byte for byte.
No kit source changes. See README for exact per-part/export/map budgets.


## Pass 13 — direct sun, real fixture openings and the first surface export

**Color/value first.** The accepted hero's neutralized sky fill overwhelmed
its sun. Compare all six `renders/delivery-light-study/` images at full size:
the first clear-sky study (sun 6, sky .025, EV .25) has actual canopy/store
cast shadows. Retain a procedural sky's blue; do not desaturate it into an
ambient overcast. The first surface pairs put concrete at .847 against .795,
soffit .608 against .417, and cabinet .166 against .135. Reject the excess
fill from the newly exposed emitters before changing black paint again.
The original broad splash mask also incorrectly darkened entire horizontal
concrete slabs. Replace that with physical slab/traffic fields and a dedicated
cement, sand and broom finish, with sealant following real joints.

**Full-size inspection.** Open every image in `renders/delivery-pass1/` and
both the main and detailed first pair renders. The lot now differs from the
street and its checker repeat is reduced, but neighboring road modules still
show the same broad ground-family pattern. Normalize that repeated low
frequency on copied presentation meshes as well; preserve all ground files.
The original LED frame was a solid box covering its lens. A real four-sided
frame fixes that obstruction. Two remaining black openings expose a reused
loop variable that duplicates fixture positions; fix it and audit every
opening in the actual reimport. Broad absorbed oil replaces the old isolated
ink splat. The new mulch has overlapping shredded fibers instead of paver
cells; the base rust follows curved paint-loss scars rather than a flat card.

**Delivery.** The exported station uses ten materials (eleven with distinct
smooth/split CMU), replacing eighteen/nineteen. Trim uses the equipment atlas.
Wear, original ink and all lights share one alpha material, one emissive map
and a second UV selector; unlit surfaces select a zero-emission swatch.
The new dedicated concrete and emission maps fit within 29 MiB after removing
the redundant trim triple. Independent raw import/chart/image checks pass.

## Pass 14 — reject the night exposure and invalid material patches

**Color/value first.** All eight `renders/delivery-pass2/` views and five
`renders/delivery-pairs2/` exports/pairs were opened individually. Under the
clear matched sun, concrete is .765 against .795, asphalt .379 against .466,
soffit .501 against .417, dark cabinet .076 against .135, and ray-verified
EIFS .596 against .663. Keep the concrete. Ease the station asphalt correction
from .43 to .59, restore a physically plausible charcoal finish now that the
old ambient wash is gone, and use a warmer off-white soffit finish. The Texas
awning shadow implies a stronger front-normal sun component than the first
estimate; revise that vector, rather than warm all the surfaces globally.

The former EIFS ROI includes the concrete facade belt and its cast shadow.
An independent pixel-to-surface ray identifies those materials and stations.
Reject that measurement and fix a new rectangle on actual sunlit EIFS above
the 4.12 m belt, retaining the original photographic comparison patch.

**Reject the first blue-hour frame.** Its sky has the right blue, but its
exposure is still too low. Inspect all three `renders/dusk-study/` frames:
choose sky .4 and EV 2.2, exposing for the canopy while retaining darker
surrounding ground. Add low-level panel emission to the actual store/price
brand backings. Keep lamps in their native atlas and reduce their excessive
radiances; this does not add a material. All frame openings now show white
lenses. Reduce unnecessary bevel topology on their aluminum frame sections
so even the four-island canopy stays below 18k.

**Fine audit fixes.** Replace the cast nozzle's striped polished normal with
fine cast-metal grain. Increase runoff only under the actual folded joints,
and retain the absorbed gray-brown oil's many overlapping drops. Street-road
normalization uses copied mesh colors and canonical ground images. House and
ground preservation receipts still match all 150 original delivery files.
No docs have been committed.

## Pass 15 — reject repeated streaks, pink panels and elevation occlusion

**Color/value first.** Open all 31 first final-attempt views individually at
native resolution, plus all five assembled pairs. Matched-light medians are
soffit .419/.417, concrete .765/.795, cabinet .084/.135, EIFS .664/.663 and
asphalt .424/.466 (export/photo). Keep the soffit and corrected Texas solar
vector. Increase the dedicated cement's reflectance modestly and ease the
station asphalt multiplier to .72, retaining darker actual travel/engine
centers. The photograph's cabinet is charcoal, rather than the near-black
1.3% reflectance finish; raise that finish to about 3.5% reflectance.

The new broad sign-back emission lightens aubergine toward pink in daylight.
Reduce its radiance from 1.6 to .4, retaining the original ink and native
powered state. Dusk now has a blue sky above dark ground, readable interior,
white diffusers and a forecourt pool; keep sky .4 / EV 2.2.

**Full-size faults and their causes.** Coping runoff reads as repeated dark
daggers: reduce the shared grime opacity, vary seam-specific deposit length,
width and handedness, and soften the broad wall deposit. A physical scupper
probe also finds that a non-solid runoff plane bridges an opening. Cut the
actual aperture out of the overlay and preserve its complete UV chart; do not
exempt the probe. Fine broom/sand survives the bake without a tan wash, and
oil is now an absorbed standing band rather than an isolated ink splat.

The overhead's asphalt still exposes broad periodic modulation between the
coarse vertex samples. Increase only the station's correction sampling to
.55 m (copied presentation roads .50 m); keep the canonical ground PNGs.
Bark fibers have no paver grid but look too flat from the low close-up. Darken
the fibers, widen their irregular ribbons, and add sparse larger 3–8 mm raised
pieces with open bottoms, sharing the existing equipment material. Fine
fibers remain in normals. Stock shrub bark/leaves retain their geometry/maps
under one native mask material, without new botanical pixels.

The front/side/back orthographic attempts include neighboring houses that
occlude the station, with excess vertical space. Hide presentation context
for those elevations/top, fit the public-interface width and use a wide
architectural elevation aspect. Retain actual context for street/details.
Eevee lacks diffuse sky/bounce under its roof despite ray tracing; bake a
local irradiance volume for its presentation, using the same sun/sky and
native exported materials. No additional export material or engine-specific
replacement shader is introduced.

**Build discipline.** First clean checks passed after the scupper correction;
byte repeat passed (65,507,692 bytes), brand swap retained 177 frames and 22
image payloads. The final provenance gate rejected the first hero after a
renderer cleanup occurred while its long render process was starting. No
docs were published. Rebuild all commercial generated directories from empty
with the corrected, fixed recipe, then repeat the checks and full-size audit.

## Pass 16 — final exported audit and delivery

**Color/value first.** Final matched-sun display Y′ medians (export / balanced
used photo): soffit .439/.417 (+5.3%); concrete .777/.795 (−2.3%); charcoal
cabinet .133/.135 (−1.2%); EIFS .667/.663 (+.5%); asphalt .461/.466 (−1.0%).
Neutrals are PA sunlit concrete, CA light background wall, TX exposed aluminum
jamb and VA sunlit gray aggregate; each linear gain/ROI is retained. These
are appearance measurements under shadow-estimated sun/sky, not albedos or
surveyed solar positions. The full RGB ratios and p10/p90 remain in values.json.

The former wide cabinet ROI also contains its rubber hose. Actual ray hits
identify Equipment cells 1 and 3; reject that mixed .107 measurement, rather
than brighten the hose to match cabinet paint. Narrow the patch to the cabinet
beside the hose. A new independent gate verifies nine actual surface/finish
rays in each of the five final patches (45 total), their image hashes and
current ROI definitions. The prior EIFS belt/shadow contamination is also
covered by that gate.

**Native-size inspection.** Open each of the 17 main Cycles views, all eight
seed views, five raw photo-camera renders, the five composed pairs and the
Eevee image. Also inspect their value patches, eight before/after crops,
contact/comparison sheets and all five final docs JPGs at native size. Keep
the clearer cast-shadow separation, light gray cement, charcoal asphalt,
white LED lenses, gray-brown absorbed standing bands, yellow paint and
cause-local chips. The cast nozzle's grain no longer tears its highlights.
Runoff is softer and varies by actual coping joint, without painting across
the scuppers. Sparse raised bark pieces add small shadows above the fine
fiber normal. Orthographic elevations/top now exclude occluding neighboring
houses. The documentation views sheet and photo-pair sheet use compact
layouts without the former large empty rows. The runoff comparison now
actually crops the coping beneath the canopy, rather than the entry sign.

Hero store/canopy vertices span 74.9% of the frame. Actual sidewalk ray eye:
1.60000005 m; lens 40 mm; verticals vertical. Conservative projected
architecture/equipment-mask Y′ p1/p50/p95/p99: .074/.476/.749/.844. White clip:
.27%, concentrated in powered lenses/ink rather than broad painted surfaces.
Dusk retains a brighter blue sky, readable storefront glow and lit forecourt,
with the canopy diffusers/pool controlling exposure. Eevee's irradiance cache
restores diffuse light below the canopy; the same exported materials remain.

**Proof.** A clean rebuild from empty commercial build/maps/export/renders
completed: `make WIDTH=1600 SAMPLES=48`, return 0. The final default command
also passes after adding the patch-surface gate. `make check` passes the
1,000-plan/negative-control tests, actual source surface and sampled moving
leaf sweeps, independent raw glTF charts/normals/counts, fresh-import surfaces,
all 48 actual LED-lens openings, and same-scene image reuse. `make repeat`
returns byte-identical 66,790,984-byte default GLB; brand swap retains oriented
geometry, 177 node frames and 22 original PNG payloads. No GPU bake-repeat
claim is made by that geometry/export repeat. Repository check: zero errors.
House/ground preservation: all 150 pre-existing delivery/map files unchanged.
No kit source changed. Current provenance verifies 30 Cycles views + one Eevee.

**Cost.** Nine materials per station, ten with distinct smooth/split CMU;
store six/seven, canopy four, dispenser two. Native graphics/wear/emission
share a material and UV emission selector; one glass; opaque trim/equipment
share a sheet. Original boxwood wood/leaves share one locally joined mesh
and native mask. Default: 212,154 placed triangles / 111,570 unique, including
106,172 placed shrub triangles (one 5,588-triangle mesh); 112 placed material
primitives before renderer batching. Store 34,308, canopy 13,046, pump 5,160,
sign 1,516, site 23,180. Extra paving vertices carry the station's repeat/traffic
correction and raised larger bark pieces; none violates a part budget. All
per-seed parts/materials/bytes are in README and delivery receipts. New maps:
18 / 29 MiB, down from 39⅔ MiB by removing redundant trim maps; complete
landscaped family 77 MiB with existing maps. GPU figures assume 8-bpp block
compression and full mips, not measured engine residency.

**Remaining CG tells.** Six repeated product fronts and regular joinery are
visible close up. Fine bark still relies on normal relief, while only the
larger pieces have geometry. The setting remains sparsely developed. Some
original ground aggregate rhythm survives at extreme overhead distance;
the broad tile field is an upstream finding, with all ground bytes preserved.
Eevee shadows/glass differ from the Cycles judgments. The sparse VA photo fit
and unknown photo responses limit precision. These limits are exposed rather
than calling the station indistinguishable from a photograph.

**Docs last.** Five final gas-prefixed JPGs, each ≤1600 px wide / 200,000 bytes;
no motion GIF. Commit only after the above audit, in a separate final commit.


## Pass 17 — hero takeover; reject the first wear trial

**Color/value first.** The accepted source colors and neutral-balanced reference
copies are retained. Initial hero shows the same pale store front/side, little
canopy shadow, and nearly invisible foreground deposits. Save all original
finals and pairs outside the commercial clean directory before changing them.
The fixed PA floor mask measures 19.0% visible markings at a 4% Y′ deficit
against its clean p85, versus 31.5% in the photograph. VA asphalt measures
23.4% versus 59.2%. This is projected sunlit floor area, excluding structures,
large shadows and PA covers; the thresholds include aggregate and residual
seams, not chemical oil identification or surveyed square meters. The masks
and both 4% and 8% deficit thresholds are exposed by src/hero_review.py.
PA is balanced on sunlit concrete; VA on gray sunlit aggregate, with the
existing linear gains and neutral ROIs retained.

The first stronger PA trial reaches 29.5% coverage but its selected deposits
have 21.6% median contrast versus the photo's 6.8%. Reject it: droplets were
stretched in the long footprint direction, and the result is dark smear-like
bands. Correct each droplet for the footprint's physical aspect; use more
round overlapping drops, a lighter absorbed background and fewer strong
cores. The wider standing footprint can remain while its vertex multiplier
is reduced; gray-brown absorbed marks preserve the concrete's own value.
Tire contacts follow operating lanes and the two actual driveways. No
manufactured finish is rebaked for this change: only analytic coverage/ink
within the existing graphics sheet changes; its powered pixels are identical.

The first raking-sun hero has convincing canopy shadow and front/side
separation but too little sky fill. Raise procedural sky from .022 to .035
and sun from 5 to 6, retaining the cross-camera direction. Runoff originates
below folded canopy divisions and existing coping joints. Reject the strongest
opacity to avoid repeated black daggers. Native camera height stays 1.6 m.

Presentation uses a continuous neighborhood block of the actual ground
modules, with original Cape/ranch/split houses, pin oak/maple trees and street
lights. A template-copy error in the old two-house context allowed copies to
inherit an earlier placement's transform; the expanded context snapshots
original bases before any placement. All context remains outside delivery.
Accepted detail and dusk views keep their existing context and light recipe.
The period_canopy pair already had the estimated direct sun; transparent
composition made its sky white. Render its procedural sky opaque. Top keeps
the ground visible while hiding neighboring buildings, closing its black edges.

The second oil trial reaches 31.8% coverage but 13.5% selected contrast;
spread the footprint to 3.0 × 6.5 m and lower its standing/core coverage again.
Keep the carbon contact dark while reducing its opacity; asphalt traffic
continues around the pad instead of ending just inside the two driveways.
A closer 35 mm hero trial enlarges the monument over the storefront: reject
it and restore the accepted 40 mm camera exactly. Before/after hero crops
therefore retain matching native-pixel framing. Only the graphics BaseColor
changed during look iteration; all 17 other commercial shipped images,
including emission, stayed byte-identical before the required clean replay.

Start the final replay with empty commercial build/, textures/, export/ and
renders/, keeping references, immutable library deliveries, original evidence
and tracked docs. Use make WIDTH=1600 SAMPLES=48 WRITE_DOCS=0 so automatic
docs generation waits until every rendered final has been visually judged.


## Pass 18 — native-size final audit; exposed approaches and street ends

**Color/value first.** Keep the accepted 40 mm / 1.6 m hero framing and all
manufactured colors. The cross-camera sun gives the front a brighter value
than the side and throws the canopy shadow leftward across the forecourt.
Keep .035 procedural sky fill: .022 made the shaded masonry too dark.

At native size the first final attempt's wheel contacts taper into pointed,
regular skid-like marks in top/scale. Reject them: retain actual tire width,
vary their center paths by island/wheel, and fade coverage at both ends.
The drip field still ends too far inside the canopy to read from the street.
Extend its local footprint to 3.0 × 9.0 m, move its center .70 m toward the
approach, keep round droplets and deepen individual old absorbed cores
without restoring the rejected opaque standing smear. All six fueling faces
retain their own deterministic clusters. The field stays within the pad.

The neighborhood fixes the hero's field horizon, but the first aerial shows
two black strips beyond road ends. Lawn exclusions reached 250 m while road
modules stopped at 190 m. Extend native street runs to the same 250 m
coverage; keep ground visible at the top view's edges. No station or library
construction is changed. A process time limit interrupted the first clean
render attempt; use a detached local runner for the complete clean replay.
Stop the second attempt to correct these visible faults before any docs.

**Final measured color/value.** PA sunlit cement and VA gray aggregate remain
the photographic neutrals, with the existing linear balancing gains retained.
The strict surface gate finds that the original concrete control now samples
the longer oil footprint (actual coverage alpha 0–80/255 at the nine rays),
so it no longer measures bare cement. A ray grid locates bare sunlit cement
ahead of those marks. Move only that control ROI to (.22,.84,.37,.88); all
45 independent surface/finish rays pass, without ignoring transparent quads
or relaxing the expected material. Export/photo Y′ medians: soffit
.423/.417; concrete .777/.795; cabinet .128/.135; EIFS .667/.663; asphalt
.447/.466. Manufacturing colors and shader responses were not retuned.

Fixed sunlit-pavement masks, at least 4% below each region's clean p85 Y′:

| Pair | Before coverage / contrast | After | Balanced photograph |
| --- | --- | --- | --- |
| PA forecourt | 19.0% / 11.9% | 37.2% / 9.0% | 31.5% / 6.8% |
| VA asphalt | 23.4% / 4.9% | 63.3% / 10.5% | 59.2% / 9.1% |

At the separate 8% deficit threshold, PA coverage is 13.4 → 22.2%, photo
12.5%; selected contrast 15.0 → 11.5%, photo 12.2%. VA coverage is .7 →
44.2%, photo 35.4%; contrast 8.5 → 12.3%, photo 12.2%. These are projected
appearance proxies, including aggregate and residual seams, not square
meters or chemical oil segmentation. The original plans differ. The final
field is somewhat more extensively marked than the photograph, while the
stronger deposits' contrast is close. Masks, image hashes, exclusions and
neutral gains are in renders/hero-review/wear-measurements.json.

**Final native-size judgment.** Open all 17 main Cycles images, all eight
seed views, five raw photo-camera views and the Eevee hero. Inspect their
contact sheet and the five native-pixel hero before/after crops. Keep the
accepted 40 mm camera and measured 1.6 m sidewalk eye. The hero's lateral sun
produces a canopy shadow across the slab, brighter storefront and darker
side/cavities; neighboring original houses, trees and street lights now
replace its field horizon. Longitudinal wheel contacts fade softly, fueling
deposits spread into the exposed approach and fascia/coping runoff remains
at its construction joints. The unchanged close-up lighting retains the
accepted entry, sign and dispenser look. Dusk retains its accepted lighting
and composition. The period canopy has its actual procedural sky rather
than a white transparency composite, under its retained photo-estimated sun.
Top-edge Y′ minimum/p1/median are .057/.337/.379: no black void border.

Hero conservative projected architecture/equipment-mask Y′ p1/median/p95/p99
is .041/.266/.631/.776; white clipping .26%, principally powered lenses/ink.
This is a display range, not albedo or a visibility-buffer measurement.

**Final proof and cost.** Rebuild every commercial source, map, export and
render from initially empty generated directories with
`make WIDTH=1600 SAMPLES=48 WRITE_DOCS=0`. Complete the replay after correcting
the measurement control described above; final make returns 0 and validates
30 Cycles views plus one Eevee, all from current external glTF/maps.
`make check` returns 0; `make repeat` returns 0 with a byte-identical
66,729,400-byte default GLB and unchanged geometry/frames/shared images under
the brand swap. The repository check returns zero errors. House/ground
preservation verifies all 150 existing delivery/map files. No main merge,
kit change, library alteration or shared construction-interface change.

Default triangles: 212,662 placed / 112,078 unique. Store 34,308 and dispenser
5,160 are unchanged; canopy 13,098 includes 52 runoff triangles; ServiceWear
712 includes 456 added wheel-contact triangles. Nine materials (ten on seed
103), 18 new maps at the accepted 512/1024/2048 sizes, 29 MiB new / 75⅓ MiB
default total. Default external glTF/BIN 13,186,355 bytes, plus 53,541,730
referenced PNG bytes; new shared PNGs occupy 10,059,586 bytes.

**Remaining CG tells.** Very close paving exposes softness in the shared
1024 ink atlas; the effect is calibrated and readable at street distance
but is not high-resolution grime at macro range. Regular construction, six
repeated product fronts and repeated neighborhood prototypes remain. Eevee
has harder shadow/alpha and glass differences from Cycles. Fine bark and
some ground aggregate rhythm remain the accepted limitations. No extra
texture allocation is introduced to conceal those limits.

**Docs last.** After the above full-size judgments, regenerate the affected
five gas-prefixed JPGs from the current exported finals. Amend the existing
head docs commit, so history contains one version of these five images.

---

## Neighborhood strip center — form checkpoint

This section concerns only `strip_*.py` and `build/strip/`. The station's
accepted construction and its separate look work are unchanged. All strip
images import diagnostic GLBs with quick finishes and original graphics.
No surface bake, final age, masonry relief or portfolio acceptance is implied.
The Texas and California photographs are credited in refs/SOURCES.md;
STRIP_REFERENCE.md separates authored dimensions from their sparse camera fits.

### Strip pass 1 — reject expense, framing and type

Evidence: `renders/strip/pass1/{hero,storefront,walk,pylon,rear}.png`, all
opened individually. References: the used Texas shop row and California low
center, also opened, with their neutral assumptions documented for later fits.

**Color/value first.** Shaded glazing is appropriately dark, rather than pale
blue/frosted panels. The first sky is too gray, and the smooth quick masonry
cannot stand in for a used split-face block wall. Keep the material distinction
honest: do not turn all concrete tan to copy the Texas photograph's paving.
The form palette needs directional sunlight and shadow separation; no claim
of material matching is made.

**Rejects.** The unoptimized ten-bay building costs 92,196 triangles. Repeated
tiny bevels consume that budget without changing player-distance silhouette.
The hero clips the left return, and the near storefront camera cannot see
the sign above the deep canopy. The first sign cells have the wrong aspect
ratio, stretching their letters. Pale channel-letter inks on white pylon
substrates are nearly unreadable.

**Changes.** Retain silhouette radii, remove sub-4 mm edge breaks from the
game construction, and reserve them for trim normals. Keep the same physical
storefront depth/head/transom. Recompose with a fixed 40 mm level camera;
move the detail camera far enough back to clear the shelter. Give fascia
art its real narrow aspect, darken the channel-panel substrate and put all
captions/addresses on the same new sheet.

### Strip pass 2 — reject a merely passing plan

Evidence: `renders/strip/pass2-camera/`, `renders/strip/pass2-L/`, the plan
diagrams and the actual surface/motion reports. Every rendered view was opened.

**Color/value first.** Sun/sky now creates a deep covered-walk band and
recognizable cast column shadows. Asphalt stays dark gray; concrete stays
neutral. The used photos still have much more material variation and wear.
These remain future look work, not a reason to add a noise wash to this gate.

**Rejects.** The L initially duplicates its corner walk and canopy, has an
unsupported coping segment inside the elbow, and leaves the front parking
aisle without a good exit. Counts alone also place some accessible aisles
under columns or beyond the end of the building's actual walk. The first
full motion check catches a real water-table collision across every entry
bottom rail. After cutting that trim, it catches a second smaller collision:
the door-hours notice was fixed in space while the leaf moved through it.
The perimeter planting exclusions are holes until they receive actual skins.

**Changes.** Miter the return canopy/walk, remove the internal floating cap,
and reserve a cross aisle and turn flare outside the entire wing walk.
Include covered walks, occupied vehicles, islands, sign and yard in pickup
routes. Shorten upper L rows to keep the cross aisle usable. Select dispersed
accessible groups that clear column/tower plinths and reach the real walk;
probe the full ramp/landing width on actual source surfaces. Cut the entry
opening to floor height and interrupt the water table at the jambs. Parent
the notice to the leaf at its actual glass surface. Fill the perimeter beds.

**Independent proof.** Four occupied-lot pickup route sets and representative
car park/back-out paths pass. The source/native-curb comparison, ramp rays
and raw/fresh GLB import are separate from the kinematic plan proof. Full
5-degree entry/service/gate/lid sweeps have no contact exemptions.

### Strip pass 3 — reject hidden signs and weak evidence

Evidence: the first full 1600 px set, archived at
`build/strip/review-pass3/`, and both used-photo pairs at
`build/strip/review-pass3-matches/`. All sixteen main/family PNGs and both pairs
were opened individually, including the original reference photos.

**Color/value first.** The architecture mask has deep glazing and zero white
clipping, with a dark-gray lot and neutral concrete. The rear and service
views are too dark to inspect; use a rear-directed sun for those diagnostic
views. Do not lighten the exported black door or metal to hide poor evidence.
Both pairs make the remaining surface gap plain: our quick wall/roof/paving
fields lack the photographs' manufacture and service history.

**Rejects.** Entry towers obscure the first/last tenant wordmarks, echoing a
failure already rejected on the station. Combined end leases repeat identical
signs on each structural bay. A raceway crosses a subtitle. The overhead
camera fits extents without centering them, wasting much of its frame on
grass. Scale context is present in ordinary shots, and the house's first
placement/grade hides its driveway; moving it must also keep it out of the
station's footprint. Native near-side street continuations leave short gaps
at the ends of the commercial frontage. A newly added tower-art rectangle
also exposes a UV-transfer error: pixel coordinates were not normalized.

**Changes.** Put affected tenant names on the tower's own face, use one sign
per combined lease, keep a common physical graphic carrier, and move its
raceway above the lettering. Add appropriately proportioned tower art to the
same sheet and reject any out-of-range ink rectangle before export. Center
and fit the above views using positive-depth imported bounds. Load the
station/house/pickup only for the scale shot, keep their footprints separate,
and cut presentation lawn around the split's actual descending drive. Clip
native ground modules along their length at the property endpoints, retaining
their cross section. No ground/shrub/house/car source or delivery is modified.

**Photo critique.** The roughly 10 native-pixel fits compare a few framing
stations, not entire surveyed centers. The Texas fascia/shelter and California
metal mansard are different systems from our full covered walk and shingle
alternative. Glazing divisions and period proportions are useful comparators;
roof materials, exact bay width, local finish and light response are not
accepted matches. Their neutral ROIs/gains remain disclosed. This gate must
stop before trying to manufacture the missing used surfaces.

### Strip pass 4 — fixed services, end closures and final form audit

Evidence: all sixteen PNGs under `renders/strip/checkpoint/`, the three current
`renders/strip/matches/*-pair.jpg` comparisons, and the assembled contact
sheet were opened. Family rows run 201, 202, 203, 204. The provenance audit
hashes all nineteen current exported views, their renderer and native context.

**Color/value first.** Retain the same assumed photo neutrals: Texas white
vehicle hatch, California sunlit gray sidewalk, with the generated gains/ROIs
in `build/strip/references/balance.json`. The final hero's conservative
architecture mask has Y′ p1 **.0149**, median **.2476**, p99 **.6322**, and
**zero white clipping**. Covered glazing and column shadows stay deep, concrete
reads neutral and asphalt dark gray. This checks the image's tonal range,
not real albedos: the quick wall, roof, paving and service surfaces still lack
the used photographs' manufacture, localized dirt and variation. Those flat
fields remain conspicuously CG and are explicitly outside this form gate.

**Rejects and fixes.** A well-lit service close-up exposed a fixed collision
that moving-door sweeps could not detect: the original long meter bank crosses
the first rain leader and service gear. Its first end-wall location also puts
the dumpster yard in front of its access. Put the bank at the rear of the
right end wall, with feet shaped to the wainscot/water table and risers meeting
grade. Test its actual consolidated skin against every other source mesh,
including the yard. Finite rays now test the full width of a 1.2 m outboard
working corridor. The close-up then reveals a duplicated last-bay partition
on the end-cap skin and an inward-facing right wall pack. Remove the redundant
partition/finish and mirror the pack outward. The final service image has no
striped coplanar panel, hidden meter faces or unsupported mounting feet.
Rear-wall construction also retains its own reusable mesh root per bay.
The mansard audit also catches columns inheriting the flat canopy's 3.46 m
shaft top and protruding through the slope. Lower the shafts to 3.10 m and
seat their capitals under the lower soffit. All ten actual shaft tops now
measure 3.0999999 m, with the same triangle count.

**Form judgment.** The 22/24 ft modules read as small tenants, with combined
end leases and one name per lease. The 2.75 m storefront head and shallow
transom keep the glass commercial in scale. Ten-foot walks have a useful
column setback and continuous shelter; the mansard and arcade change the
silhouette rather than just recoloring the flat front. Raised towers and
coping interrupt the long parapet. Sign band, tower faces and pylon are
readable, and original names/treatments remain distinct from the reviewed
national chains. Cheap lit furnishing gives the windows room depth, though
the repeated notices, flat rear partitions and rigid garment shapes remain
weak at close range. End and rear walls are purposefully service construction,
but their scalar finishes still look like blank blocks.

**Parking and assembly.** Both entrances, both occupied aisles and the rear
loop pass the pickup paths. The L uses its reserved cross aisle outside the
covered return. Representative car parking/back-out passes with neighbors
occupied; this does not certify every stall or simultaneous traffic. All four
plans retain six unobstructed van-sized spaces and exclusive aisles. Actual
ramp/landing rays clear column bases. All **2,040** sampled door/gate/lid poses
have zero measured penetration without contact exemptions. The bank has zero
measured interference, about **85 mm** cabinet standoff, **.49–.50 mm** foot
assembly gaps, and **324** clear working-area rays per seed. Its end-wall
working space is measured separately from GLB serialization.

**Gate limits.** The scale shot keeps the station, split-level and pickup at
their native meter scale on separate footprints. Overhead views reveal the
Ground family's repeated road-repair patch; flag that shared pattern rather
than modifying Ground here. Rear service landings are less developed than
the accessible front walk. Period research adds a third pair: the Virginia
brochure states 1989 construction / 2015 renovation; Texas has a published
secondary-record date of 2002. California remains an older auxiliary. The
Virginia fit uses one clear pane at only 1164 px native width and .30 px RMS;
its hipped pavilions differ from our flat towers. The tiny white fascia-trim
neutral is disclosed. A first yellowish pavement ROI turned the photograph
too blue and was rejected; no material was tuned to that cast. All three
fits remain unsurveyed type comparisons. Final masonry/shingles, weathering, sign optics,
material consolidation and baking are still pending. Stop at the requested
form checkpoint; no portfolio docs images are committed.

## Strip look pass 1 — reject cropped hero, uniform runoff and rust stamps

**Color/value first.** Opened all five 1200 px Cycles exports in
`renders/strip/look-pass1/`, plus the original Texas storefront, the used rear
photograph and both native Westlakes front/lot photographs. The procedural
raking sun gives deep storefront cavities and a distinct walk shadow. The
CMU reads neutral gray rather than the former warm scalar slab; concrete and
asphalt are distinct. The first hero's conservative architecture union has
Y′ p1 .0126, median .2143, p99 .7678. Its .124% white clipping includes active
emissive diffusers; this is not a zero-clipping claim or recovered albedo.
Paving is still too even at full frame to accept without the matched pairs.

**Rejects and changes.** The eye is now inside the lot, but the nearest tower
clips the top of the panoramic frame. Give the hero more vertical field and
raise the camera shift, retaining 40 mm and an actual 1.6 m ground offset.
Parked vehicles belong in the site views; hide them for diagnostic close-ups
so the pizza room can be judged. The coping wash repeats the same pointed
shape, and wet door-bottom rust looks like an orange stamp. Reduce wash
opacity, vary its width, length and mirror selection. Generate hem-rooted
corrosion coverage in the strip's existing free chart, retaining a dark
oxide color and irregular paint-loss boundary. Increase threshold deposits
and the tracked-grit strip rather than tinting the whole walk dirty.

**Construction evidence.** The revised plans pass 1,000 plans / seven invalid
controls and all four occupied-lot route sets. The first motion run correctly
rejects a gate deposit authored on the wrong signed side of its pivot; it
extended outside the right leaf. Place deposits separately on the seventeen
actual slat faces. The corrected default passes every moving-part sweep,
service-landing ray, ramp/column, meter-support and native-curb probe, as well
as fresh GLB geometry/frame import. The three available raw surfaced exports
pass map-byte, material-count, UV-area and unit-normal checks. No delivered
station, house or ground file has been edited.

## Strip look pass 2 — construction reads; reject traffic tape and tight framing

**Color/value first.** Opened every 1400 px image in `renders/strip/look-pass2/`:
hero, storefront, walk, rear, stalls, dusk and endcap. Cross-check against the
native used Texas and Westlakes photos, and the 600 px used rear. The walk's
shadow is deep without blue-tinting the black framing. The rear's gray door
paint and hem-rooted dark oxide retain their colors; the bright concrete stoop
is distinct from the asphalt. Blue hour has a brighter sky than ground, lit
signs and shops, and a light pool under the walk. The palette still needs the
held-out paving measurements; no exact albedo match is claimed.

**Rejects and changes.** The upper nearest tower now fits, but the neighboring
pole crosses it and its cap is still tight. Move the eye four meters down the
side drive and use 35 mm, retaining a level 1.6 m view with a shifted lens.
Hide the presentation cars for all diagnostic details; their absence now
exposes the pizza oven, work counter and tables. The stalls have accumulated
soft drips instead of an isolated ink splat, but long tire contacts look like
fresh painted stripes. Soften that shared strip chart and retain the broader
vertex-sampled polished paths. Replace pointed coping wash with several
unequal soft gravity rivulets. Keep grime/gum localized to entries.

The wrapped left end now has continuous room depth through both glazed faces
and carries the same tenant's side sign. Audit all four plans for the same
fix: the L's short closure was still a solid wall, even though its end-treatment
parameter said wrap. Give that closure the return tenant's glazing and side
sign too. The former 7,000-triangle maximum leaves no useful margin for the
last tracked-grit quad; reduce only the bollard cap's radial segmentation,
retaining its measured diameter and silhouette, rather than dropping real
construction or exceeding the bay budget.

## Strip look pass 3 — reject weak evidence, soft ink and unsupported fit-out

**Color/value first.** Opened all nineteen 1600 px main/family views and all
six native comparison renders; archived this iteration in
`build/strip-look/pass3-images/` and `pass3-pairs/`. Also inspected native
photo grids before accepting measurement patches. Reject the original
Westlakes-lot neutral: it sampled blue tree-shadow asphalt, with linear gains
1.348 / .987 / .803, turning sunlit ground orange. The replacement is the
sunlit concrete curb top, native (80,492)–(108,495), with gains about
.993 / .982 / 1.026. Keep its tiny native size disclosed. The first walk
rectangle also crossed glass and a sunlit curb; reject its statistics. A
fixed shaded-concrete patch now gives Y′ .217 / .231 before the final light
revision, rather than pretending the mixed .100 / .249 patches measured
concrete.

The period-lot photograph casts the shelter's shadow toward the lot. Reverse
the estimated sun's front-normal component and match its brighter camera
exposure; leave the family's asphalt albedo intact. The initial asphalt proxy
has 4%-threshold variation coverage / median contrast 56.8% / 6.9%, against
45.8% / 7.3% in the balanced photo. At 8% it is 19.5% / 10.1% against
18.3% / 10.6%. These count projected visible variation, including aggregate
and repair texture; they are not chemical oil segmentation or surveyed area.
Retain the annotated masks and both thresholds. The rear photo is overcast:
use neutralized procedural sky illumination, rather than allowing blue fill
to turn its gray steel blue. All outdoor pairs retain the procedural sky.

**Native-size rejects and fixes.** The narrow tower cell is visibly softer
than adjacent masonry. Reallocate unused address/window pixels within the
same 2048 sheet to 488×150 tower faces; put addresses in compact guarded
cells and preserve the nine tenant styles. No extra map or memory. The
full imported neighborhood still has a gap beyond the far end; stagger a
second library block behind the first. The above views expose a missing
public corner quadrant inherited from the station's context assumptions.
Restore the native corner curb, walk and planted sector, leaving Ground's
files untouched. Locally join the boxwood's two skins under its existing
mask, as the station does: one primitive per plant, unchanged stock vertices
and pixels. The mansard needs a tenth material for its separate existing
house shingles; the other three seeds stay at nine.

**Construction rejects and fixes.** The new tracked-grit quad floated across
an accessible ramp; the actual pedestrian surface rays reject it. Keep broad
entry grime on the level landing and exclude gum from the sloped lane.
An actual material-patch ray also exposes downward open-sheet winding on a
sealant strip. Restore authored sheet fronts, preserving UVs by vertex
identity; do not hide this with a two-sided opaque material. Finally, simple
fit-out proxies had unsupported chair bases, oven, desks and conveyor rail.
Seat the chair bases, add oven/table/desk feet and monitor stands, and make
a closed racetrack conveyor with external supports, cantilevers and hanging
connections. Source probes now measure each tagged foot against its actual
finished floor: 73 default contacts within 1 mm, before consolidation. These
are source-contact measurements, separate from reimport serialization.

The complete four-seed construction, motion, raw-UV/map and reimport checks
pass after these corrections. All final images must be rerendered against
stable current GLBs; the renderer now rejects source or recipe edits during
a render instead of attributing an earlier loaded scene to later file bytes.

## Strip look pass 4 — final exported checkpoint and measured misses

**Color/value first.** Inspected the final nineteen main/family Cycles views,
the six calibrated native comparison renders and six pair composites, the
Eevee view and all four annotated measurement masks. The hero's architecture
mask has Y′ p1/p50/p95/p99 of .012/.210/.605/.768 and .118% white clipping,
mostly powered diffusers; deep walk/interior shadows remain intact. The
35 mm camera is inside the lot at a measured 1.6 m eye. Raking sunlight
separates the split faces and coping; it does not imitate overcast exposure.
The distant frontage is legible, with parked delivered cars and a street
horizon. The tower's reallocated ink is visibly sharper at native size.

Photo exposures are camera settings independent of the hero and material
albedos. The retained Westlakes neutrals precede every measurement. With
period-lot exposure 1.75 and walk .30, fixed asphalt median Y′ is .657
against .675 in the balanced photograph; shaded walk is .219 against .232.
At 4% below each patch's clean p85, asphalt variation covers 24.9% at 5.1%
median contrast, against 46.0% at 7.3%. At 8%, it is .91% / 9.0%, against
18.34% / 10.6%. This is a remaining lack of broad pavement variation despite
the improved value match. Do not describe the result as identical aging.
The shaded walk measures 46.9% / 9.6%, against 58.3% / 6.2%; at 8%,
28.6% / 13.7%, against 18.4% / 9.6%. Its remaining marks are too contrasty.
The native walk patch is only about 20×4 pixels. These are projected
variation estimates including aggregate/repairs, not chemically separated
oil or surveyed area. Eighteen independent exported-surface rays pass at the
fixed rectangles, rejecting the earlier glass/curb and reversed-sheet errors.

**Construction and presentation judgment.** All four sites are rendered above
and from the street, with the shallow east-shifted row, west-biased arcade's
staggered islands and corner L visibly differing from the centered lot.
The left end shares its room through real wrapped openings; the short L
return now wraps too. Rear stoops and loading bollards make the service
entries usable. Lit signs, window rooms, canopy fixtures and the pylon survive
export and read at dusk; Eevee's cached indirect view is darker under the
walk than Cycles but retains the same materials. Salon/cleaner/pizza fittings
now have actual supports; the measured source floor contacts are distinct
from the reimport-position check.

**Remaining CG tells at this gate.** Identical structural bay rhythms,
simplified interior appliances/furniture, very orderly rear services and
restrained large-area aging still reveal the generator. Door-hem corrosion
is still an alpha simplification. Small notices/pylon lettering soften;
canopy and wall runoff reads more clearly in detail than in the full hero.
The corrected native asphalt repeat is less obvious but the photographic
patch remains more varied. The library neighborhood is occupied yet sparse,
with recognizable repeated house/tree forms. This is a look checkpoint,
not a claim of final photographic equivalence.

**Proof.** `make strip-check` passes all four current sources: 1,000 plans,
seven rejected invalid controls, occupied-lot route/parking proofs, actual
construction and motion checks, raw map/UV/normal validation and fresh import.
The repository check reports 1,546 source files / zero errors. Independent
`make strip-repeat` produces a byte-identical 66,825,832-byte default GLB.
`make strip-values` passes all eighteen surface rays. Three seeds retain nine
material states; the mansard requires ten for its existing separate shingles.
The default has 246 actual material primitives, not nine draw calls. New strip
maps cost 6⅔ MiB; its actual referenced set costs 79⅓ MiB. No kit changes.
The preservation receipt verifies all 43 initially present delivery/doc files;
gas source/docs and houses/Ground tracked files remain identical to main.

The final form batch completed under one inherited shared GPU lock. Inspected
all twelve native before/after renders and six comparison JPGs: four sites,
wrapped end and service landings. Both sides retain original quick finishes
under the same renderer/light; the baseline is `b3a77d8`, the after side is
rebuilt from current form scripts. The comparison metadata hashes both source
sets. Inspected the final family, detail, pair and complete contact sheets.
`python3 src/strip_review.py` passes **26 current exported views**, plus the
twelve form renders' source/recipe/image hashes and six required crops.
The requested checkpoint stops here. No final docs images are committed.

## Strip delivery pass 1 — reject the inherited look (full-size before)

**Color/value first.** Inspected the native 1600-pixel hero, storefront and
blue-hour images, the 1800-pixel-wide six-pair sheet, and the family sheet
before editing. The cool masonry and black extrusions make every seed one
palette. The asphalt has almost no broad service variation. The fixed pair
measurements are 24.9% coverage / 5.1% median contrast versus the photo's
46.0% / 7.3%; walk contrast is 9.6% versus 6.2%. Retain those original masks
and images in `build/strip-final/before/`, without changing the neutrals.

**CG tells rejected.** Empty gray rooms, one identical dark notice per window,
weak interior radiance at dusk, no pole pools, a clean service rear, and four
nearly identical parking grids are substantive misses. The prior checkpoint's
claim that the occupied sites differed enough was too lenient. Transparent
channel-letter face artwork sits 54 mm ahead of its backing and projects an
offset alphabet onto it; the apparent duplicate is a cast shadow, rather
than duplicate text geometry. Close the carrier spacing and make its printed
backplate opaque, retaining separate lit letter pixels in the emission map.

**Changes for the next export.** Use single-frontage shallow and deep parcels,
a west-street endcap with side parking and a corner L; native entrances follow
those frontages. Add trade-specific vinyl, offers, OPEN tubing, blinds, vacancy
paper, menu/cooler/product art in the same 2K sheet. Strengthen the physical
fixture output and ship punctual fixture lights. Warm seeded masonry/fascia
colors, accumulated stall centers, aisle paths, sawcut repairs, rear gas runs,
fixture wash and three welded dumpster forms address the causes of the misses.
No photograph supplies model or texture pixels.

## Strip delivery pass 2 — new exported rooms, reject sign placement and service conflict

**Color/value first.** Inspected all five native 1200-pixel exported views in
`renders/strip/final-pass1/`: storefront, hero, dusk, rear and above. Sandstone
CMU is now warm rather than slate. Powered rooms are markedly brighter, with
OPEN signs and identifiable cleaner/pizza display forms. The bright backing
is still too even and can obscure depth; keep counters, reflective appliances
and graphics distinct rather than treating illumination as sufficient dressing.
The asphalt's stall centers read, but the open travel field remains too regular.
The rear's warm paint is closer to the used photo, but its runoff is too faint.

**CG tells and fixes.** Moving the sign backing forward exposed an assembly
mistake: the ink quad is 1 mm behind it, leaving blank cabinet faces. Move ink
2 mm outward. The original alpha shadow was correctly diagnosed; the corrected
opaque carrier must still be visibly in front. Rear hem corrosion inherited
round blobs from the shared sheet: replace only the strip chart with thin,
unequal edge loss. Increase vertical fixture/scupper runoff, retaining the wall
color. Window posters, translucent vinyl, partial blinds and merchandise now
vary by tenant; simple room fixtures still reveal the economical fit-out.

**Measured assembly rejection.** The complete motion sweep catches the new
containers' lids against service geometry at −100 degrees. Move their pads
300 mm out from the wall and give the lid its physical −95-degree stop; rerun
the actual-surface sweep. Keep the service-loop occupied-lot test, including
the new pad polygons, so visual dressing cannot silently obstruct circulation.
The first delivery consolidation has six fixed-building primitives, with
separate entry/service leaves; the full placed center has 100 primitives
before the final shallower layout. No kit or accepted-family code changed.

## Strip delivery pass 3 — matched-light audit, reject misleading patches and white rooms

**Color/value first.** Inspected all six native pair composites and the native
lot/walk renders, plus the 1600-pixel corrected storefront/hero/dusk/rear.
The sandstone/brass palette separates the default from brick and cream EIFS;
the rear is warm rather than blue-gray. The sign face now has one alphabet.
But the day rooms are too evenly bright compared with the used photos. Reduce
room-fixture radiance and the shipped point-light intensity together, keep
lit ceilings at dusk, darken backing paint, and put colorful merchandise and
supported chairs near the glass. Move the left interior finish inward: the
previous lining was embedded in the exterior end wall and exposed brick inside.
Portrait window offers now include original drawn trade illustrations, not
only three lines of text. Vinyl and posters must not conceal the cooler/menu.

**Measurement rejection.** The changed narrow/deep parcel moves an island
into the old asphalt ROI. The actual surface test hits its vertical concrete
curb; reject that result even though its apparent coverage is closer to the
photo. The original shaded-walk ROI also crosses a new light gradient. Select
unobstructed floor rectangles, verify all eighteen rays, and recompute the
before images in the same rectangles. Standardize comparisons at the original
1440-pixel measurement width and the calibration's exact aspect, since a
one-pixel resize phase materially changes the tiny photo walk patch. Retain
the original 24.9% / 5.1% asphalt and 9.6% walk-contrast report as historical
values, not as interchangeable with the new patches.

The validated common before asphalt patch is 28.2% coverage / 5.25% contrast;
the common before walk is 11.1% / 5.58%. Their changed positions are recorded,
not silently substituted. Strengthen the actual side-drive/rear-drive wheel
bands and stall engine centers; soften/broaden entry deposits while preserving
gum. These are cause-local adjustments, not a global noise overlay.

**Assembly rejection.** All new container lids pass in the default and brick
center. The full four-seed sweep catches the street-edge center's relocated
enclosure against Bay 01's service leaf and the building when its gates open.
Move that enclosure into the large free east buffer, away from the wrapped
front, meter working space and rear doors. Keep the new container pads in the
occupied-lot route obstacles. Matching dimensions or preserving exports alone
would not have detected this conflict.

## Strip delivery pass 4 — full gallery audit before cold rebuild

**Color/value first.** Inspected the 1600-pixel hero, storefront, walk, tower,
end cap, pylon, rear, services, stalls, dusk, scale, all four overheads and
streets, all four turnaround frames and the Eevee hero. The default's
architecture-mask Y′ p1/p50/p95/p99 is .015/.264/.625/.776, with .120% white
clipping, largely fixture lenses. Warm CMU, red brick/sage, cream EIFS and
putty/teal remain distinct; cavities are deep. Window products, illustrated
posters, blinds and notices are now visible; source photos still have more
varied merchandise and less orderly rear services.

The verified common asphalt patch measures 38.9% variation / 5.63% median
contrast, up from 28.2% / 5.25%; photo 46.0% / 7.25%. A final wheel-path
amplitude calibration is warranted before freezing. The common walk reaches
29.0% / 6.30%, versus 58.3% / 6.24% in the balanced photo. Its broad marks are
softer than the inherited 9.6%-contrast patch, although the rectangles are
explicitly different; clean-to-dirty coverage still falls short. Gum remains
visible. These are appearance variations at a 4%-below-p85 threshold, not
chemical stain segmentation. Keep both thresholds and source/mask hashes.

**Native-size rejects.** The four parcels now read differently above: shallow
single-aisle, deep four-row, west street/endcap with side parking, and the
corner L. However, street 201's foreground pylon clips and obscures shops;
street 204 favors the return's blind rear. Move both cameras. The orthographic
turnarounds have neighboring houses in front of the asset; hide presentation
context for those diagnostic elevations while retaining the ground plane.
Dusk has operating rooms and OPEN signs, but strengthen the pole pools. Keep
fixture ranges bounded in the external package. Eevee remains darker through
transmission than Cycles; do not hide that difference with substitute shaders.

**Delivery decision.** Consolidating every fixed site prop is unnecessary and
makes the pylon/poles/containers hard to reuse. Consolidate the building by
material and the site skins together, but retain independent site-prop roots
and meshes; accept their actual primitives and report them. Source modules
remain intact before delivery consolidation. All four construction/motion,
raw-UV/normal/budget and external buffer/image checks pass, and four external
centers plus a repeat reuse thirty image identities. The shared-family
preservation receipt verifies 198 pre-existing delivery/map/doc files.
The final audit and docs follow the cold rebuild, not this preliminary batch.


## Strip delivery pass 5 — cold export, native-pixel final acceptance

**Color/value first.** Opened every cold-built final at native resolution:
hero; storefront, walk, tower, wrapped end, pylon, rear, meters and stalls;
dusk; 1.8 m scale; front/side/back/top; four overheads and four independent
street views; Eevee; all six photo pairs; their masks and the final contact,
family, sites, streets, detail and pair sheets. Opened all eleven native
before/after plates (1,312–1,600 px wide), checking against the immutable
handoff pixels. Warm sandstone/bronze, brick/sage, cream/burgundy and
putty/teal separate the centers. Final architectural Y′ p1/p50/p95/p99 is
.015/.265/.625/.776; .121% white clipping is mostly light lenses. Dusk rooms
and OPEN signs glow, with actual pole pools on the ground. Day rooms remain
more evenly illuminated than photographic shops. Eevee glass is visibly
darker than Cycles; the unaltered Eevee result is retained.

**Final calibrated values.** On the same validated replacement rectangles,
asphalt before → after is 28.24% → 44.99% variation coverage and
5.25% → 5.79% median contrast; balanced photo 46.00% / 7.25%. Walk is
11.07% → 39.68% coverage and 5.58% → 5.70% contrast; photo 58.27% / 6.24%.
Asphalt Y′ .657 vs photo .675; walk .258 vs .232. This is display variation
below the local p85, not an oil classifier. Both thresholds, original photo
rectangles, assumed neutrals and hashes remain in wear-values.json. Eighteen
floor rays pass. The inherited 24.9% asphalt / 9.6%-contrast walk series uses
different render patches and is retained as history, not a claim of a direct
9.6-to-5.7 reduction. The photo walk patch has very few original pixels.

**What still reads as CG in the pairs.** Goods and hanging shirts are simple;
poster typography softens at atlas resolution. Counters/room backings remain
too uniform compared with the crowded photographic windows. Containers and
rear service spacing remain orderly; the source photo has substantially more
varied scars and debris. The asphalt's 8% tail and median contrast are still
weaker than the photo; the walk lacks the photo's broad worn coverage and is
a little bright. Surrounding houses sit in sparse library landscaping. These
are visual limitations, not hidden by serialization or dimension tests.

**Delivery proof.** A cold build removed all owned strip models, art, external
packages, calibration and render outputs, retaining canonical shared-library
dependencies; `make -C commercial WIDTH=1600 SAMPLES=40` passed. Then
`make -C commercial check` and `make -C commercial repeat` passed, including
the unchanged gas targets. Strip repeat is byte-identical at 66,392,004
embedded intermediate bytes; gas repeat is byte-identical at 66,729,416 bytes.
The intermediate GLB is not the shipping format. All four external glTF/BIN
packages preserve canonical image URIs; four centers plus a repeated center
reuse thirty decoded image identities. Their common image union is 67,064,433
bytes and the four geometry packages total 51,480,180 bytes. Building/seed
primitives are 56/115, 52/138, 61/139 and 51/133; fixed building surfaces use
6/7/6/6. Whole default was 246, gas default remains 112 (store 11).
Buildings are 60,592 / 53,882 / 67,808 / 54,154 triangles; fitted bays stay
4,034–6,342; pylons stay 3,104. Source construction, UV/normal/budget,
whole-range motion, occupied circulation and external byte/import checks pass.
These prove geometry and serialization separately, not photographic equality.

The protected-family receipt passes all 198 existing delivery/map/doc files;
no kit, houses, Ground, cars or top-level README edits. Repository check
passed with zero errors. Five final JPGs follow this review and receive a
separate last commit; native proof renders and downloaded photographs remain
ignored and rebuildable.


**Final docs inspection.** The first eight-view gallery could not meet 200 KB
without excessive compression, and the size guard rejected it. Retain that
full sheet under renders; use a six-close-up, three-column docs layout and
encode in memory before writing only a compliant JPG. Opened that composition,
the final contact and all five docs JPGs at native size. Hero/sites/streets/
details/dusk are respectively 190,687 / 192,947 / 189,194 / 199,856 / 164,093
bytes; all are 1600 px wide. The final default `make` passes including the
new docs stage. Repository check now covers 1,557 files with zero errors.


**Shipping repeat.** Extended the repeat to convert the independently rebuilt
scene into external glTF/BIN at the canonical relative-URI location, compare
both files byte for byte, and restore the baseline package in all cases.
`make -C commercial repeat` passes again: 12,311,793 external bytes match,
including fixture lights and shared-image URIs, in addition to the 66,392,004
embedded intermediate bytes and unchanged gas repeat. This is delivery
reproducibility, separate from the actual-surface construction checks.


## Strip value round — reject a bright sampling corner and hero-invisible wear

**Color/value first.** Reopened the accepted native period_lot pair, hero,
stalls and walk, and the balanced source photographs. The prior right-corner
photo ROI (Y′ .675) is an unusually bright portion of the wearing course.
Three clearly sunlit native patches measure .605, .626 and .675; these
are display values under the photograph's unknown exposure, not reflectance.
The assumed neutral remains the sunlit gray concrete curb, excluding its joint
and blue tree shadow. The neutral gains and photographic pixels are unchanged.
The old .657 render statistic did not prove the lot's overall value matched.

**Material isolation.** Measured actual exported UV/COLOR_0/PBR samples using
memory-mapped buffers. The shared Ground asphalt image has median sRGB Y′
.411 / linear Y .141. Effective exported linear Y medians are Ground .134,
gas .100 and accepted strip .0905; these are shader-input samples, not scene
pixels or area-weighted surveys. The road ORM's median roughness is .788.
Only the strip's application changes: darker, causally varied COLOR_0 and a
dry scalar roughness, retaining the exact shared color, normal and AO images.
No canonical gas/Ground image is rewritten and no texture allocation is added.

**Rejects while iterating.** Moving the actual comparison camera and its fitted
glazing anchors two bays along removes the foreground island, retaining the
same lens/height and .53 px landmark RMS. That move brings an awning shadow
through the old render ROI; reject its nonsensical 61% contrast. Place the
replacement rectangle wholly on sunlit exported pavement and test its surface
rays. Reframe the accepted export under the same new camera for a comparable
before measure, with the original deposit sheet regenerated from the accepted
script and verified against its original embedded payload. Do not substitute
changed rectangles silently for the inherited 45.0% / 5.8% report.

The first stronger walk chart produced repeated tire-like ribs and 10.3%
contrast; reject it. Use broad, soft footfall deposits with irregular cloud
shapes, preserving gum. Merely lowering asphalt albedo still leaves the hero
looking clean at its grazing view. Actual source and fresh-import eye rays
confirm the repair surfaces are present, correctly above the wearing course,
with their intended vertex colors. Increase their local contrast and exposed
utility-repair footprints, and retain the routed crack shapes. Compare these
at full-frame hero size, separately from the close-up's aggregate statistic.

The outside memory stop interrupted no build owned by this round; git was
clean and the preceding completed build log was intact. Subsequent jobs use
one Blender process, four threads and the shared GPU lock, with streamed
hashes/memory-mapped diagnostics instead of whole large-file reads.


**Cold-build rejection.** The actual ramp probe caught a 22.7 mm obstruction:
the widened flat footfall/traffic quads bridged a sloping access ramp. Trim
their outer edges to the actual level walk, 39 mm inside the ramp knee, rather
than weakening the probe or presenting those quads as physical ramp wear. No
new triangles or changed ramp geometry. Restart the cold build after this fix.


**Grazing-view rejection.** The full native walk image exposes pale oil-shaped
reflections across the sunlit stalls: the separate alpha films use the sign
sheet's material response and catch the sky. Increasing their opacity is the
wrong fix. Remove the asphalt oil/tire overlay meshes, retain absorbed oil and
wheel contact in the actual wearing-course COLOR_0, and sample the true entry
turn paths into that same field. Dark seals and repairs share the asphalt
response. Gum and footfall deposits remain on the shaded walk. Stop the
current gallery and cold-rebuild this corrected export; do not bless the
white-looking oil films because its close-up coverage happens to pass.


**Contrast calibration, color/value still first.** With pale films removed,
the clean course is darker and the hero carries visible dark utility repairs
and routed seals. But the broad sunlit pair patch still measured only 5.86%
contrast, so value correction alone is not accepted as a contrast fix. Two
actual-export trials at fixed camera/light/1440 px give tire strengths
.64 → 55.63% coverage / 7.16% contrast and .72 → 59.90% / 7.99%, against
46.00% / 7.25% in the unchanged photo patch. Freeze .65 and verify at final
1600 px / 40 samples. The extra variation follows wheel travel, not a whole-
lot noise overlay. The higher coverage is disclosed rather than tuning the
threshold or choosing another rectangle to force both numbers to agree.

The final source keeps the accepted RNG draws for each stall's unequal width,
length and rotation, preserving subsequent rear-wear placement. Entry-path
fields explicitly handle west, east and south openings. Removing the thin
asphalt films saves 590–1,022 placed triangles per seed and retains the same
115 / 138 / 139 / 133 material primitives and texture allocation.


## Final value critique — exported 1600 px / 40 sample cold build

**Color/value first.** The common-camera sunlit asphalt patch is Y′ .652 before
and .572 after. The balanced photo's three sunlit native patches are .605,
.626 and .675; the final outlined native render patches are .559, .579 and
.572. The strip has moved from pale gray to a darker wearing course, slightly
below the photograph's patch medians rather than claiming exact photographic
reflectance. The neutral assumption remains the sunlit concrete curb; gains,
photo pixels, lighting and exposure are unchanged. Hero foreground Y′ drops
.486 → .396 in the identical rectangle. The native 1600 px before/after crop
shows dark utility repairs, seals and wheel paths without relying on a zoom.

Actual exported input median linear Y is Ground .134, gas .100, strip .0905
before / .0492 after. The original asphalt base image is unchanged (.411 sRGB
Y′ / .141 linear Y). With the actual exported median tints and native PBR
settings under identical procedural light, diagnostic swatches measure Ground
.757, gas .728, strip .724 before / .643 after. The swatches isolate material
application from the three sites' differing shadows; they are not additional
photo-matched scenes. The strip alone uses roughness .96. The diagnostic
preserves the gas's roughness texture multiplier as well as its texture.

**Contrast and coverage.** At the unchanged 4%-below-p85 threshold, final
asphalt is 56.31% coverage / 7.12% contrast versus the photo's 46.00% / 7.25%.
The inherited accepted-camera result remains 44.99% / 5.79%; the actual accepted
export reframed with the new camera measures 51.07% / 6.32%. These are separate
series, not interchangeable before numbers. Walk, with camera/patch unchanged,
is 39.68% / 5.70% before, 35.18% / 6.61% after, against 58.27% / 6.24% in the
photo. Keep that coverage shortfall visible in the report. Nine actual export
rays per patch validate the floor, and the nine asphalt rays also have clear
asset sun paths. This proves sampling scope, not artistic quality.

**Native image judgement.** Opened all 30 current export views: hero, all
close-ups, turnaround, scale, dusk, four overheads, four streets, six matched
renders and Eevee. Opened all six pair plates, the family/sites/streets/details/
contact/pairs sheets, outlined sunlit patches, before/after hero plate, coverage
masks, four diagnostic swatches and all five final docs JPGs at native size.
The walking-eye oil no longer turns into pale reflective films. Broader soft
traffic dirt and discrete gum read at the doors; the pale clean strip beside
the curb remains plausible. The hero's repairs and black routed seals remain
visible in the whole frame; broad oil centers are quieter where cars occlude
them. The lot pair foreground is open pavement, no planted island.

**What still reads as CG in the pairs.** The photo's mineral aggregate is
coarser and its repair edges more broken. Our repaired rectangles remain too
regular, wheel paths form orderly bands in overhead views, and the photo's
walk has more widespread accumulated dirt. Shipped rooms and signage retain
the accepted simplicity; glazing reflections and repeated construction are
more uniform than the photographs. Eevee's rooms remain darker than Cycles.
Do not call the coverage overrun or the walk shortfall a match merely because
asphalt contrast is now within .14 percentage point of the photo.

**Build and preservation.** Removed the owned strip models, generated art,
exports, calibration and final render outputs before rebuilding serially with
`make -j1 -C commercial WIDTH=1600 SAMPLES=40` (four-thread Blender wrapper).
Canonical dependencies were retained to honor their byte-preservation rule.
The cold make and `make check` pass; the latter covers construction, ramp and
motion probes, UVs, budgets, external export/re-import and repository rules.
The strip repeat passes with both the four-thread wrapper and default Blender.
The protected gas repeat differs with the thread override, so reran the
specified normal `make -j1 -C commercial repeat`: both strip and gas are exactly
byte-identical. No shared code or protected bytes were altered to accommodate
that difference. The gas GLB remains 66,729,416 bytes with its accepted hash.
`python3 kit/repo_check.py`: 1,561 source files, zero errors.
`python3 commercial/src/strip_preserve.py`: 198 existing files byte-identical.
Final source and diagnostics compile; `git diff --check` passes. No kit change.

Building triangles remain 60,592 / 53,882 / 67,808 / 54,154; placed seed totals
are 189,264 / 290,052 / 252,144 / 294,046. Building/seed material primitives
remain 56/115, 52/138, 61/139, 51/133 (gas default 112 seed primitives).
External geometry packages are 12,227,249 / 12,285,134 / 13,895,142 / 12,553,502
bytes. Map dimensions and compressed GPU estimates remain unchanged at
79⅓ / 92⅓ / 76 / 79⅓ MiB; no added map or material allocation.

**Final docs replacement.** Inspected before staging: strip-hero.jpg 185,970,
strip-sites.jpg 196,005, strip-streets.jpg 189,937, strip-details.jpg 197,496,
strip-dusk.jpg 159,908 bytes. All are 1600 px wide and below 200,000 bytes.
Replace these in the owned gallery head by amendment, as requested, so only
one gallery-image version is reachable in branch history. The accepted
parcels, palettes, fitouts, sign construction and occupancy remain in place.
