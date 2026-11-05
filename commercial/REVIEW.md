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
