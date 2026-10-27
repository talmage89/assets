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

Current evidence: [source contact](renders/lookdev/contact.jpg),
[used front pair](renders/lookdev/aged_front-pair.jpg),
[used rear pair](renders/lookdev/aged_rear-pair.jpg),
[front close-up](renders/lookdev/front_detail.jpg),
[wheel close-up](renders/lookdev/wheel_detail.jpg),
[five colors](renders/lookdev/five-colors.jpg) and
[corrected stripes](renders/lookdev-form/stripes_side.jpg).
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
The primary evidence is [the contact sheet](renders/checkpoint/contact.jpg),
[front pair](renders/checkpoint/match_front-pair.jpg),
[rear pair](renders/checkpoint/match_rear-pair.jpg), and the
[striped side](renders/checkpoint/stripes_side.jpg).

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

Latest evidence: [all views](renders/checkpoint/contact.jpg),
[side overlay](renders/checkpoint/side-overlay.jpg),
[rake measurement](renders/checkpoint/side-rake.jpg),
[front pair](renders/checkpoint/match_front-pair.jpg),
[rear pair](renders/checkpoint/match_rear-pair.jpg),
[front stripes](renders/checkpoint/stripes_front.jpg),
[side stripes](renders/checkpoint/stripes_side.jpg).

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
