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
