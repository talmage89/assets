# Photo-directed review

The material target is the real used pavement and concrete in `refs/arlington.jpg`
(WxTrinity, CC0) and `refs/ramp.jpg` (Mds08011, CC BY 4.0). Photos are never
material inputs. The calibrated views use approximate nominal geometry, not a
survey: the Ohio assumed-width road fit is 0.41 px RMS; the warning/concrete
fit is 15.16 px RMS. Blender's independent projection agrees within .002 px.
Those are framing statistics and do not certify dimensions or realism.

## Pass 1 — exported Eevee assembly, construction and finish failures

Viewed all four first previews: hero, block, curb and ramp. Compared with both
used-street photographs. The pavement was much too pale and looked like a
new concrete road; the curbs looked machined because planar UVs stretched the
broom grain down the nose; the gutters and walks were overly pristine. A
numerical inspection found a color-space error in the new flat baker. Fixed
source sRGB decoding / linear bake target / single sRGB encoding and added a
constant-color GPU fixture plus per-tile source/bake mean checks. Unfolded the
curb profile in its radial direction, while retaining phase at corner/straight
ports. The reference's irregular flow-line sediment informed placed, interrupted
alpha deposits rather than a brown all-over band.

## Pass 2 — exported Eevee assembly, depth and modular continuity

Viewed hero, block, curb and ramp again after corrected tile baking. Color
separation was much better, and curb grain no longer stretched. The prominent
CG tells were coplanar overlap of repairs with tire-polish cards, virtually
invisible concrete joints, an overly regular repair rhythm, and flat corner
walk slabs. Separated decal layers, colored the recessed joint floors through
the shared trim (no overlay or additional material), and added radial corner
control joints. Replaced the intersection wedge fan with radial strips so its
shared arm edges carry the same crown samples. Road port normals now use the
analytic interior derivative. Source/export/import normal quantization remains
explicitly bounded rather than called bit-identical.

Further independent delivery checks found that glTF corner color attributes
were named differently on import and that exporting unused colors caused a
second trim-material variant. The assembler now recreates the referenced
float point-color layer and recomputes the continuous world field. Only
material-used vertex colors export. This restores the three-material family
and prevents a per-module tint restart.

## Pass 3 — Cycles, source fields, exported materials and physical interfaces

Inspected both calibrated source/photo pairs and exported-GLB/photo pairs, then
all final eye-height, block, repetition, detail, drive-cut, scale, turnaround,
Eevee and tile-board views. Both stages retain the same framing calibration.
The final pairs are under `renders/review-source/` and `renders/review-glb/`.
The four-source/corner arrangement deliberately differs from the photographed
San Diego corner: the comparison judges materials, not a copied plan.

The early Cycles views washed out the color and made the wheel paths look too
strong. Lowered the procedural daylight exposure, made wheel polish subtler
and more matte, removed exaggerated paint micro-relief, and kept chipped paint
in alpha/color. Added measured, normal-represented asphalt edge fretting;
pores and aggregate in cement; soil-edge damp marks; and stronger, interrupted
flow-line deposits. Warning tops have a foot-traffic mask. The result keeps
wear visible in the hero, without painting the entire tile brown.

The first full delivery review also exposed presentation-only facets under
ramps. Matched the grade's sampling to the imported ramp surface and removed
a height discontinuity at its ends; repeated near-equal coordinates had made
flat ground acquire 45-degree smoothed normals. Closed the backdrop beyond the
sample ends, and raised the orthographic side camera so its lower rays do not
start beneath the ground. Those fixes change no delivered geometry.

Independent construction checks caught an actual curb/ramp mismatch while
expanding the earlier port-only checks. Both now share flare stations and
height functions, and the ramp UV chart tapers the curb-profile unfolding to
the sidewalk's world chart. All 312 checks pass, including smooth seams,
internal intersection joins, road/pan contacts and curb/ramp contacts. Expected
material/grade changes are explicitly separated from smooth-normal tests.

Sediment cards originally interpolated across 3 mm joint recesses and could
cut below the paving. Fitted every profile/joint station before export and
sampled a 15-point barycentric grid plus centroid on every trim triangle.
107,360 probes now pass, with .555–10.000 mm measured support distance and no
sampled penetration. This is actual imported-surface sampling, not a comparison
with a declared offset constant or merely scene/export agreement.

## Final assessment and reproducibility

The tile boards and unadorned color mosaics honestly show a 3×3 repeat. No hard
repeat seam is visible; the large top view still reveals that repairs come
from a limited variant library. Seeded weighted selection and continuous world
tint reduce the rhythm without a custom shader. World positions, normals,
UVs and module bounds survive stock glTF export/import; there are three shared
materials and nine shared images in both library and assembly.

`make clean` followed by `make` rebuilt the complete pipeline; `make check`
passes. All 251 mesh fingerprints repeat exactly. GPU tile differences remain
within 1/255 (worst byte RMSE .00351); the final atlas repeats exactly, including
RGBA alpha. Final documentation contains only original GLB-rendered JPGs;
reference pairs and intermediate renders remain ignored. Docs are committed
only after this final review.

Weakest: the broad concrete/asphalt aging remains more regular and cleaner
than the photographed street, particularly the less-trafficked ramp shoulders.
The 2K shared maps soften microscopic material variation. Normal-only warning
domes have no raised silhouette or individual cast shadows. The level surface
skins need terrain/grade integration; the neutral presentation ground is not
a lawn, and the depressed curb awaits its driveway apron. These are stated
limits rather than hidden geometry or a claim of a surveyed/certified street.

## Lead-directed visual revision / 01 concrete

Reopened both original exported pairs next to their photographs. The earlier
assessment was too lenient: beige concrete, painted-looking road, repeated wear,
soft curb and smeared flow-line cards are obvious. Engineering is retained.

`visual-01-concrete-glb/{road_material,warning_material}-pair.jpg`: removed the
warm cement bias and dark color flecks; pores remain very shallow relief and
transverse broom strokes live only in normals. Both exported pairs were viewed.
Gray is better, but the ramp is still too light and the first curing field looks
like airbrushed clouds, stronger and smaller than the photo's broad weathering.
Reduced the cloud contrast, doubled its physical scale, and lowered paste value
for the second concrete comparison. Road remains flat and striped at this point.

`visual-01b-concrete-glb/`: viewed both new pairs. The pink and granite flecks
are gone; broad gray weathering is quieter and value is closer. It remains too
smoothly lit beside the sunlit photograph; reserve that judgment for the daylight
pass. Warning orange and gutter stamps are deliberately still visible failures.

## 02 exposed asphalt aggregate

Changed the original mineral field to two populations: roughly 8–14 mm exposed
stone and 3–5 mm fines, with up to about 2 mm generated relief. The previous
6 mm primary population collapsed to two delivery texels. Larger grains now
carry correlated color/normal/roughness, plus soft sub-meter-to-meter mix variation.

`visual-02-aggregate-glb/`: viewed both pairs. Foreground road now has exposed
mineral structure instead of smooth paint, and it resolves toward an even
texture with distance. The ramp pair shows that the larger-scale aggregate is
strong at close range; daylight will be the final test of its relief. The dark
four-line tire pattern is now the most conspicuous remaining road failure.

## 03 remove tire stripes

Removed all four full-length polish cards and the narrow world-tint tire masks.
Retained only broad, low-amplitude continuous mix/exposure tint and edge wear;
there is no replacement dark travel-lane line. Parked-car oil is handled next.

`visual-03-no-stripes-glb/`: viewed both pairs. The road no longer has four
unmotivated dark rails. It reads as continuous mineral paving; the identical
transverse seal and oil group now stand out plainly and are removed next.

## 04 irregular service events

The assembly uses sixteen clean road bases, one sealed variant and one patch
variant. Removed the variant's travel-lane oil package. A separate fixed seed
places a small minority of meandering, differently oriented cracks and sparse
engine drips at curbside parking positions; many bays have neither. Sidewalk
cracks also use sparse seeded selection instead of a seven-panel cadence.
All new cards fit the imported road surfaces and share the existing atlas.

`visual-04-placement-glb/` and corrected-winding `visual-04b-placement-glb/`:
viewed both pairs at each checkpoint. No paired oil cluster or straight tar
stripe occupies the foreground lane; an isolated irregular split appears at
middle distance. Corrected the new strip's winding before continuing. The
assembly now has genuinely empty bays; the final block/top views will judge
the full distribution. Gutter stamps remain the worst close-up artifact.

## 05 flow-line sediment

Replaced the wide wavy stamp with a roughly 2–5 cm dark damp/grit core near the
curb lip, a faint taper into the pan, washouts, sparse mineral grit and a few
script-drawn needles/leaves. The supporting cards are narrower and nearly
continuous along the low line, interrupted locally rather than isolated blobs.
They still follow every actual imported joint/flare station.

`visual-05-flow-line-glb/`: viewed both pairs. The smeared stamps are gone,
but the replacement is too faint and narrow in the photographed framing;
losing the defect is not enough. Widened the damp/grit core to about 4 cm and
increased its density/value contrast, retaining broken low spots and debris.
The first build also caught a ray on an open corner endpoint; probes now sit
just inside the tangent ends, without changing delivered snap geometry.

`visual-05b-flow-line-glb/`: viewed both pairs. The low-line core is denser,
without the old stretched waves or rectangular patch edges. Its fine grit is
still subtle in this broad ramp framing; inspect it in the dedicated curb
close-up under the final side sun. It remains confined to the gutter low line.

## 06 pavement paint and federal yellow

Paint is now solid, slightly cool white with crisp geometric edges and faint
aggregate relief. Four fragments share the existing atlas region: clean and
locally worn-through paint, selected at tire crossings instead of white noise
across every bar. The stop bar has two wear zones at wheel crossings.
Warning color now derives from the published 33538 XYZ values (source/conversion
recorded in SOURCES.md), replacing the old ochre-orange guess. Dome-top traffic
wear stays localized and the surrounding yellow stays saturated.

`visual-06-markings-glb/`: viewed both pairs. The visible clean bar is solid
white with a crisp edge; other bars retain localized holes. Yellow has moved
away from orange but AgX/soft illumination still lifts it toward pale peach,
and the concrete is still softly modeled. Do not accept this as the final
color judgment: daylight and display transform need examination in pass 08.

## 07 barrier-curb profile

Retained the same pan, rise, back width and snap locations. Replaced the
76.2 mm rounded nose with 13 mm toe/top tool radii, a planar 1:12 battered
face and a flat top. Analytic profile normals retain that planar face and
small-radius edges; they no longer average across the long face/top. Concrete
roughness is about .9, so the remaining blue face cast is illumination, not a
low-roughness clearcoat. REFERENCE.md separates this requested profile from
the Auburn envelope dimensions rather than falsely citing it as that drawing.

`visual-07-curb-glb/`: viewed both pairs. The raised barrier now reads as a
flat top and a planar face, with the highlight confined to the small tool
radius. The earlier blue face is still exaggerated by the lighting. Ramp
materials remain too smooth/flatly illuminated, and yellow is too pastel.

## 08 side daylight and final art-direction checkpoint

Replaced the broad area fill with an explicit .53° sun at 38° elevation,
from the southwest side. Procedural sky remains, with reduced haze/fill and no
second solar disk. Render-only grade is plain neutral gray. Switched from
AgX to Khronos PBR Neutral to retain yellow saturation. Hero camera remains
1.7 m above actual road grade, tilted to include roughly 2.5–5 m foreground
pavement. No shader, texture or stage geometry is substituted for the GLB.

`visual-08-daylight-glb/`: viewed both pairs and hero/curb/joint/block. Rejected:
the first explicit-sun setup is too dark and blue, with weak direct illumination.
The neutral transform preserves yellow saturation, but cannot compensate for
underlighting. Increased the neutral direct sun, lowered sky fill, and disabled
the light's legacy node override so its energy is explicit. The block also
confirms that repairs are sparse and irregular, rather than a per-bay package.

`visual-08b-daylight-glb/`: viewed both pairs and hero/curb/joint. Neutral direct
sun now gives useful gray value and saturated yellow; the barrier face/top is
clear. Rejected the remaining close-up finish: concrete has too little relief,
coarse asphalt color resembles tessellated scales, and gutter grains stretch
into fine longitudinal streaks. The 10 mm paint offset also casts a sticker-like
shadow. These are visual defects despite the existing support checks passing.

## 09 close-range finish refinement under accepted daylight

Concrete broom pitch is now about 5 mm (rather than sub-Nyquist 2 mm), with
.22 mm peak-to-peak generated relief, faint cement grain and quieter curing
clouds. Reduced gray value slightly toward the photo. Asphalt now exposes
separate 6–13 mm stone islands through pale binder, with less coarse color
contrast and about 1.4 mm primary relief, retaining smaller fines. Gutter grit
is sampled at equal physical spacing in both directions before atlas packing;
its core spans roughly 4–6 cm and stays at the actual pan toe. Paint offset is
3 mm, above the 2 mm edge-fretting layer, instead of a visibly floating 10 mm.

`visual-09-finish-glb/`: viewed both pairs, then 1440 px hero/curb/joint.
Asphalt now reads as a finer mineral mix rather than tessellated scales; nearest
2–5 m carries texture and the distance resolves evenly. The gutter has visible
toe grit with a narrow interrupted footprint. Paint no longer floats visibly.
The close joint reveals a new failure: regular sine broom plus lattice grain
aliases into a woven/waffle pattern. Rejected that finish even though the broader
pair hides it. Replace it with irregularly loaded bristles and jittered cement
grain, with lower relief. Keep color/value and the accepted daylight fixed.

## 10 irregular broom, no woven alias

A periodic one-dimensional random bristle profile replaces the single sine;
slight lateral drift follows a broom pull. Jittered mineral microstructure
replaces regular lattice-height grain. Broom relief is now .14 mm peak-to-peak,
faint enough for used concrete. Both exported photo pairs are rebuilt again.

`visual-10-broom-glb/`: viewed both pairs and the 1440 px joint/curb close-ups.
The woven alias is gone. Concrete now has quiet cement grain, faint irregular
transverse finish and broad cool-gray value changes, without granite flecks.
The toe line carries damp/grit rather than the original smeared stamps. Accepted
this finish for the final assembled renders; final top/block views must still
show the limited tile coverage honestly. No new validation features were added.


## Visual revision / final delivery review

Command: `make -C ground WIDTH=1600 SAMPLES=96 PASS=review` — passed, including
the existing `make check`. Opened every final render: Cycles hero, block,
repetition/top, curb, joint, ramp, depressed curb, scale, front, side and back;
Eevee hero; both exported 3×3 tile boards; both final source/photo pairs and both
final GLB/photo pairs. Also opened the complete contact sheet and all three
compressed docs JPGs. Source and delivery finishes retain the same color and
material direction; the 2K set softens the tiniest concrete grain as expected.

Final exported pairs:
- `renders/review-glb/road_material-pair.jpg`
- `renders/review-glb/warning_material-pair.jpg`

Final contact: `renders/final/contact.jpg`. The final images use the current
exported assembly; per-image metadata records its hash and lighting. Docs:
hero 185,202 bytes, overview 187,539 bytes, details 180,228 bytes, all ≤1600 px
wide. No reference images are committed or used as material inputs.

Current delivery: library 4,162 triangles / 29,049,628 bytes; demonstration
31,772 triangles / 31,487,792 bytes; three shared materials, nine 2048² maps,
48 MiB compressed with mipmaps (192 MiB if uploaded as RGBA8). All 312 existing
seam/interface checks pass, max position error 3.842 µm and max smooth-normal
angle .065°. Existing support sampling passes at 127,520 points, closest-surface
clearance 1.228–7.998 mm. No check code or shared kit code changed in this pass.

Remaining limits: the large unadorned top view still reveals some repeated tile
weathering. The normal-only warning domes retain a flat silhouette and no
individual cast shadows. The reference has more accumulated organic litter
than this reusable gutter strip. Concrete macro weathering remains smoother
than the photograph's long service history. The neutral grade is presentation
only; no driveway surface, lawn, storm drain or manhole was added.


## Street completion / pass 01 — color and value first

Opened the inherited final GLB pairs. Rejected the blue-gray concrete and
all-over curing clouds. First correction (`p2-01-value-glb`) raised the paste
from .425 to .635 sRGB and removed most low-frequency color modulation without
changing the daylight. Opened both new pairs: rejected the new concrete as too
white, still slightly lavender, and too pristine against the used gray photo.
The flow line is visible again, but the photo has a stronger, grittier toe.

Second correction uses .545 neutral paste with a small blue-channel reduction
to cancel the remaining cool material/sky bias, quiet cement grain, and causal
edge/soil deposits. Seals now have 65–80 mm feathered coverage, .48 roughness,
.8 mm normal relief and 3 mm card clearance rather than 6 mm; the transverse
variant's card width was narrowed so it also stays below 100 mm. Open cracks
retain millimetric openings. Lighting is unchanged throughout this pass.

Opened both `p2-01b-value-glb` pairs. Base concrete is now light neutral gray,
clearly separated from the asphalt; the blue/lavender paste and cloud pattern
are gone. The sunlit slab is still a little brighter and much cleaner than the
photo, and the shaded far curb remains blue from its sky-facing orientation.
Accepted the base value for continuing construction; later passes must add
localized joint/edge patina rather than reintroducing broad tile noise. The
flow band is darker but still lacks the photograph's dense organic grit. Seal
width/relief no longer reads as an open canyon; it remains visibly repaired.

## Street completion / pass 02 — exported assembly, color and construction

Viewed every image in `p2-02-preview`: hero, dressed, block, repetition,
curb, ramp, driveway, inlet, manhole and lawn. Also opened all three Cycles
checkpoints (`p2-02-cycles`: inlet, lawn, dressed) against Lawton's used inlet /
grass photo, the Ohio street and Daderot's iron photos. Rejected the result.
The concrete is still a little pale and pristine; lawn green is plausible but
thin patches form an obvious repeating camouflage pattern, and the sparse
strokes look like straw on a carpet. Edging improves silhouettes but has an
obvious regular shadow rhythm. Iron is too black/blue with large orange patches,
and its stretched UVs exaggerate the noise. A mistaken pad half-width also
filled the whole lid instead of leaving individual raised grip lands. Driveway
flares shade in triangles, and tire scuffs look like sharp ruled lines. The
initial dressed shot hides the mailbox/light behind the camera and overlaps
the cart with the hydrant. These are visual failures despite working geometry.

Existing checks caught UV collapse on a 3 m joint-floor span and two crown
clipping slivers that collapse in float32. Fixed the new joint mapping and
removed sub-numerical crown wedges; did not loosen their tolerances. Raised
turf blade density and quieted thin-patch coverage; added standard alpha MASK
for foliage sharing the same trim images, while sediment retains BLEND.
Reduced oxide/steel contrast and metallic response on oxidized iron, restored
waffle grip pads, smoothed the real apron grade, softened tire scuffs, added
parked-engine drips and moved long seals away from the lane center. Reframed the
hero farther back at the same player height and separated the context props.

The Cycles checkpoint confirms the edging marks are actual blade/card shadow
rhythms, not merely an Eevee sorting artifact. Replaced fractional foliage with
an explicit stock MASK state (same atlas, no added images), and will judge the
new silhouettes again. The first iron finish is also rejected in Cycles: it
looks painted in camouflage. Oxidation now stays much closer to the substrate
value. The new lawn wrap test and continuation of the existing modular seam
sampler are necessary for the third tiling set; no general check framework or
kit feature is added.

## Street completion / pass 03 — calibrated materials and repeat

Opened all four `p2-03-material-glb` pairs and all seven `p2-03-cycles` renders.
Color/value first: concrete is now neutral/light rather than blue-gray. It is
still cleaner and less eroded than the used ramp photo. The lawn's green fits
the used-street reference better after raising blade coverage; the big brown
camouflage repeat has receded. Iron value is improved but broad rust and UV
streaks still look like a painted coating. Rejected the separate grate bars,
the dense checker lid and the picket-like edging. The new inlet photo fit is
1.41 px RMS; the cover comparison is 33.34 px RMS and is only a material/framing
aid, not a dimensional measurement. The two original fits are unchanged.

The broader street is coherent, but plain slabs still look too perfect; the
inlet has visible rectangular construction artifacts; a box-shaped shadow at
the lawn boundary exposes mismatched grades. Changed the grate to one plate
with round-corner holes, made foliage shorter/curved and irregularly spaced,
added actual 1.5–4 mm sediment grains to the toe graphic, and joined the yard
filler grades. Tire traces were softened and parked-engine drips now sit on
the rear drive slab. No lighting change masks the material corrections.

## Street completion / pass 04 — construction tells in the exported pictures

Opened all four `p2-04-fit-glb` pairs and all six `p2-04-cycles` renders.
Color/value: concrete remains a little cleaner and brighter than the photo,
but is light neutral gray and clearly lighter than asphalt. The flow line has
visible gritty interruptions instead of just a cloudy stamp. The lawn is a
muted summer green with straw/clover; its flat middle still needs engine grass
scatter at close range. Rejected remaining iron smoothness, overly dense grip
pattern and large dark text plaques. Replaced the lid's dense normal-only grid
with sparse, real 3 mm grip lands, and cast letters directly into the iron.
Continuous object-level iron UVs replace per-face resets that looked striped.

The assembly's large black lawn seams were real grade discontinuities, plus
an incompletely rebuilt corner: the asset Makefile appended MODEL_DEPS after
the shared target had already expanded it. Added an explicit prerequisite for
the new modeling module. The old core tests are unchanged; new lawn joins use
the same tolerance, with clipped shared intervals where a corner joins only
part of a longer yard edge. Actual yard geometry and tangents were corrected.
Joined each casting's fixed parts; only the service lid and lift-out grate
remain separate. The inlet body's curb UV projection is explicitly preserved
through that consolidation. Superseded previews remain ignored.

## Street completion / pass 05 — casting value and causal patina

Opened all four `p2-09-preflight-glb` pairs and all eight `p2-09-cycles` views,
plus the streetside camera trial. Rejected two remaining misses. Consolidation
had inherited the basin floor's .22 tint scale, darkening the entire inlet
concrete; reset the fixed body's tint to one, keeping the same albedo and light.
The cover now has real grip shadows, but its broad rust islands still look like
camouflage. Removed them. Oxidation on the cover now follows the seat and the
bases of raised lands; exposed grate/hood iron has a brown oxide finish with
contact-brightened edges and fine cast grain. Foundry lettering no longer lays
a complete rectangular coating over the hood. These are surface corrections,
not relaxed checks. The linear-light lawn prefilter brought source/bake color
MAE from .01022 to .00512 without changing the original .008 acceptance gate.

The original core plus new lawn/apron joins pass 458 seam/interface tests.
New inlet sediment sheets now clip the actual imported pan triangles: the
coarser draped grid had three interior points nearly touching the depressed
pan. The original 3 mm offset and support thresholds stay unchanged. The
casting clearances come from imported vertex bounds and ray hits, not constants.

Opened all four `p2-10-iron-glb` pairs and all six corrected `p2-10b-cycles`
views. The inlet concrete now matches the rest of the curb; iron no longer
has broad camouflage patches, and real cover grip shadows survive export.
Accepted the material direction, retaining the stated limits: iron and cement
are smoother/cleaner than the photographed castings and pavement; grass is
flat inside its fringes; and tile repeat remains apparent from overhead.
A prior preview job (`p2-10-cycles`) had read the previous GLB before the new
export finished. Its metadata caught that stale input; viewed its contact,
then reran after export completion and confirmed the corrected input hash.
Those ignored previews are not final evidence.

Private driveway panels now retain square 10 ft bays rather than inheriting
all the walk's longitudinal scores, which had created implausibly narrow
private strips. The apron still continues the walk scoring, and the walk has
expansion joints at the separate drive pour. The final clean build will judge
that last small geometry change and all final views at delivery resolution.

## Final construction and presentation review

The removable cover now includes its full 38.1 mm gauge and underside, plus a
real frame seating ledge. That geometry is needed when it lifts, rather than
being a hidden static detail. Two imported-surface ray hits measure its rest
contact; radial clearance is measured above the intended seat contact. The
square private driveway bays retain their own pour joints.

A ray inspection located the remaining long black border in the render-only
backdrop: its rim station exactly at CORE took the low branch, interpolating
below the delivered yard along the sample boundary. Corrected that equality;
asset meshes, UVs, lighting and material values are unaffected.

## Street completion / pass 06 — final-resolution chamber inspection

Opened the clean 1600 px hero, street, driveway, lawn, cover and inlet views,
all four exported photo pairs and the full contact. Color/value now stays light
and neutral across the concrete, including the inlet body; the curb's shaded
face retains a sky contribution. The broad curing clouds and central black
road canyon are gone. The used-photo comparisons still show cleaner concrete,
more uniform oxide and a much thinner grass interior than a real site.

Rejected bright white/green slivers visible through the grate. Traced rays
through the far slot row: the chamber had a floor and longitudinal walls but
no end returns, so those rays escaped to the walk and turf. Added the two
visible chamber returns, and two rays in the existing
casting measurement verify those imported surfaces. This addresses an actual
picture defect; the existing seam, overlay and material tolerances remain
unchanged. A targeted Cycles/Eevee inlet comparison precedes final regeneration.


The targeted comparison also exposed transparent sorting on the opaque iron
in Eevee. Added an OPAQUE iron state sharing the same trim images; foundry
lettering retains BLEND and grass retains MASK. Six family material states now
share the same twelve images and 64 MiB estimated compressed memory. The
remaining bright slot streaks traced to direct sunlight on the pale floor,
not escaping geometry. Its settled-sediment tint now survives consolidation.
The chamber ends follow the actual depressed curb section, closing the exposed
triangular pan shoulder; their vertical UVs unfold along Y separately from the
longitudinal curb chart. The existing UV-area gate caught the first planar
projection error; that gate and every prior seam tolerance are unchanged.

Opened `p2-12-opaque-cycles/{curb,inlet}.png`, its Eevee inlet,
`p2-13-basin-cycles/curb.png`, its Eevee inlet, and both final targeted
`p2-14-shoulder` renders. Accepted the closed concrete shoulder, settled dark
floor and solid iron. Eevee retains a stronger blue sky contribution inside
unlit recesses; it no longer breaks the casting into transparent fragments.
The final clean rebuild uses this corrected geometry and material state.

The complete clean build passed. Before freezing the delivery, corrected the
new end-return fit: a 900 mm grate in a 900 mm chamber had zero end clearance.
The cast plate is now 890 mm long inside that authored 900 mm opening, retaining
5 mm per end throughout a vertical lift. The existing imported casting check
now measures that gap as well as the separate 9.5 mm hood separation. Dimensions
and authored/reference distinctions were updated; no texture or budget changed.

Completed that fit with a real cast perimeter seat rather than leaving the
smaller plate unsupported. The opening is 900 × 385 mm, the plate 890 × 375 mm,
35 mm thick; the fixed frame supports its underside at -59 mm. Imported ray
pairs measure contact on both bearing rails. Front and end clearances are 5 mm,
with a separate 14.5 mm gap to the hood, invariant during vertical removal above
the intended seat contact. Stopped the superseded final-render job when this
construction fix was identified; the completed prior clean build remains in
`build/p2-delivery-clean-build.log`, and final regenerated proof uses the new GLB.

The imported UV/area gate caught coincident Boolean/bevel vertices after the
plate dimensions changed. Welded sub-micron doubles and dissolved zero-length
edges before applying the atlas UVs; no faces were hidden or checks relaxed.
The corrected library and assembly pass all 458 interfaces, original numeric
material gates, support sampling and measured grate/cover seating and removal.


## Street completion / pass 07 — final exported delivery

Color/value first: the concrete is light neutral gray, clearly lighter than
asphalt under the unchanged sun/sky. It no longer has the original beige-pink
or dark blue-gray albedo. Separate pours are quiet; the gutter's dark low band
remains visible. The photo still has more organic erosion, settled debris and
small local stains than the generated cement. The exposed iron has the right
brown/gray family but a more uniform oxide and smoother cast edges. These
remain visible shortcomings, not outcomes proved by engineering checks.

Opened every final shot in six readable inspection sheets, including all
17 Cycles views, Eevee, the three GLB-rendered 3×3 boards and raw color mosaics;
also opened the full-resolution curb view, all eight final/source photo pairs,
the complete contact and all three delivery JPGs. The final GLB hash is
`5f7315ff5fb50c0806dc8954a4697231158b3e2be03b18a50edcaea4667a2f08`. Source/GLB grain changes are visible in the pairs:
the delivered fine relief is softer, while color remains stable. The grass
fringes break the concrete silhouette, but the interior remains flat and its
repeat is apparent overhead. Engine grass scatter remains necessary for a
close, fully inhabited neighborhood; normal-only warning domes and the empty
horizon also read as CG.

All five optional context props build/check unchanged. Their placement keeps
walks and ramps open, the mailbox at road-relative height and the cart behind
the curb. No obvious fit failure is visible in this dressed view. The hydrant's
bright white bonnet looks cleaner than the aged pavement; small street-name
text is soft at this framing. No prop source or export was edited.

Proof commands and outcomes:

- `make -C ground clean`, then `make -C ground WIDTH=1600 SAMPLES=96 PASS=review`:
  complete source/4K bake/2K export/render/check pass, log
  `build/p2-delivery-clean-build.log`.
- Final grate seating/clearance correction followed by the same complete
  `make` command: pass, log `build/p2-delivery-final.log`; its `make check`
  stage passes all 458 seams/interfaces, raw GLB/re-import/scale,
  UV/normals/density, tile wrapping/source-color, overlay support and repository
  gates. Repository check reports 377 source files, zero errors.
- 125,408 imported overlay samples measure 1.228–7.998 mm
  clearance, with no sampled penetration. Actual casting seat contacts and
  lift clearances are in `build/delivery-check.json`, distinct from serialization.
- Library: 11,178 triangles, 54,006,888 bytes. Assembly:
  69,268 triangles, 59,650,776 bytes. Inlet 2,552,
  manhole 1,452; all lawn pieces ≤516 triangles.
- Six material states, twelve unique 2048² maps, four shared sets: approximately
  64 MiB with BC7/BC5 plus mipmaps, or 256 MiB uncompressed RGBA8. The checked
  five-prop dressing adds about 20 MiB compressed, 84 MiB total.
- Final evidence: `renders/final/{dressed,hero,streetside,repetition}.png`,
  `renders/final/contact.jpg`, `renders/final-eevee/hero.png`,
  `renders/tiles/tile_{asphalt,concrete,lawn}.png`, and the four pairs in each
  `renders/review-{glb,source}/` directory. Full filenames are catalogued in README.
- Docs: hero 190,606 bytes, overview 186,376, details 190,858; all 1600 px wide.
  Only these final JPGs are committed in this run. Inherited docs history is
  retained: squashing earlier agents' commits across the main merge would
  rewrite history outside this run.

No new shared kit functionality was added; the main merge retained both additive
README sections. No tool installation or lead action is needed. The central
remaining art weakness is still surface age/irregularity at close range, despite
the corrected color, construction, localized wear and new street coverage.

## Iron rebuild / pass 01 — inherited delivery rejected

Opened the inherited `renders/final/inlet.png` and `manhole.png`, Lawton's
combination inlet, both Daderot cover photographs and the newly cited used
ConstructionMentor inlet. Color/value first: the old inlet is brown overall,
with virtually no distinction between exposed iron and retained oxide. It
reads as wood. The lid's light gray field and continuous orange perimeter also
look synthetic. The cap's rectangular overhang, lawn-crossing fringe and
punched plate make the construction failure apparent at ordinary street range.

Rebuilt only the inlet casting/pan junction; accepted ground modules and their
material functions remain unchanged. The returned curb plate now follows the
existing rounded/battered section and terminates at its back edge. The throat
is below a 70 mm face-plate edge. One connected grate has 25 mm transverse cast
bars, 9.6 mm slot necks, small cast edge breaks and a perimeter bearing seat.
Both iron castings retain the existing trim atlas and material states.

## Iron rebuild / pass 02 — first exported checkpoint rejected

Opened both 1000 px / 32 sample `renders/iron-01` Cycles close-ups. Color/value
is much darker, but the cap is too blue-black/glossy, its front has stretched
horizontal rust streaks, and the perfectly continuous rusty lid ring is too
regular. Grass still appears over the top: the wide crossed fringe planes can
straddle an exclusion band without either vertex landing in it. Changed that
local inlet exclusion to triangle-bound intersection. Other strips and the
lawn skin stay untouched. Raised top roughness, warmed the charcoal base and
reduced the sheltered-face oxide contrast; broke up the lid seat oxide.

The independent check rejected coincident cheek/chamber end triangles. Replaced
overlapping closed solids with a continuous returned plate, full end-cheek
sweeps and only their exposed inner faces; the concrete chamber stops below
the iron. A frame-edge station now brings the depressed pan exactly to the
flush rim rather than leaving a high shoulder at the grate's outer corners.
Added imported ray measurements for curb-profile agreement, cap height/back,
slot widths and bar widths. Existing seam/material/support tolerances remain.

## Iron rebuild / pass 03 — calibrated color and casting response

Opened both `iron-02` close-ups, all four GLB/photo pairs and all four source/photo
pairs. Color/value first: both castings now read charcoal brown-gray rather than
terracotta, with dark cavities. The used inlet has brighter grazing highlights,
more battered edges and substantially more debris than our few-season casting.
The lid reference is heavily sediment-filled; it remains a finish comparison,
not a reason to replace the accepted road or bury the authored lid in gravel.

Rejected stretched front-plate grain and the lid's very black square tops,
which could read as recesses in the overhead pair. Rotated vertical-face UVs so
the long cast face follows the long atlas axis. Reduced the grip tops' metallic
fraction to retain a small diffuse contribution while preserving their darker
polished response; aligned the normal/oxide land masks to the actual complete
cast pads, eliminating partial ghost marks beside the label. No new map or
material state is introduced. Lighting/exposure are unchanged.

The four-point inlet fit has 67.54 px RMS in a 1240 px crop: this wider municipal
casting and its skewed installed frame are not the same proportions as our
narrow-pan original. The lid fit is 15.58 px RMS in 2012 px. Both fit residuals
remain printed on the pairs; neither fit certifies dimensions. Independent
Blender projection verification still uses the kit's 0.05 px threshold.

## Iron rebuild / pass 04 — final exported delivery

Opened all 17 final Cycles views, including the full-resolution inlet and lid,
the dressed hero, the Eevee hero, all three regenerated tile boards, all eight
final/source photographic pairs, the complete contact sheet and all three
compressed docs JPGs. Color/value first: exposed iron is near-black charcoal
brown-gray, with warmer retained oxide in the slots, sheltered walls, pad bases
and broken frame-edge deposits. Grain no longer stretches into front-plate
wood streaks. The upper face and rounded cap follow the adjacent curb, and the
cap is clear of grass. The pan carries the gutter's existing sediment with a
local darkening at the inlet, rather than white stains. The warning lettering
remains shallow and subdued in the top iron.

Accepted this revision at the small casting's intended importance. Remaining
weaknesses: cast edges/patina are more regular and cleaner than the photographs,
and the lid lacks their accumulated grit/debris. The fitted inlet photograph
is a broader, differently installed casting; its 67.54 px residual makes it an
approximate framing/finish comparison. The 15.58 px lid comparison is likewise
not a dimensional survey. Source/delivery pairs show normal detail softening
at 2K; the charcoal palette and localized oxidation survive export. No exposure
or lighting change was used to hide a material mismatch. The final hero retains
dark casting cavities without clipping the neighboring concrete highlights.

Proof:

- `make -C ground export/GroundStreet.glb`: regenerated scripted geometry,
  4096 source fields/bakes, 2048 delivery maps, library and assembly; final log
  `build/iron-revision/build-final.log`.
- `make -C ground WIDTH=1600 SAMPLES=96 PASS=iron-final`: passed the complete
  render/pair/docs/check pipeline; log `build/iron-revision/final-make.log`.
- `make -C ground check`: passed independently; log
  `build/iron-revision/final-check.log`. All 458 interfaces, raw/re-import,
  UV/density, normals, scale, material/wrap and repository checks pass.
- Imported inlet: **2,472 triangles** (down from 2,552). Lid module remains
  **1,452 triangles**. Library **11,098 triangles / 53,627,160 bytes**;
  assembly **69,206 triangles / 59,261,600 bytes**. Six material states and
  twelve shared 2048² images remain; no extra iron images/materials. Shipped
  PNGs total **52,763,768 bytes**; family compressed memory remains ~64 MiB.
- Actual rays measure 25.000 mm bars, 9.600 mm slot necks, a 800.000 × 95.400 mm
  throat and -25.400 mm grate top. Cap top/back both measure 152.400 mm;
  three imported face comparisons agree with the straight curb within .015 µm.
  Grate bearing contacts are within .000008 mm; end/front removal gaps are
  5.000 mm. These prove construction separately from GLB serialization.
- The unchanged support tolerances pass at **126,176** imported overlay
  samples, **1.228–7.998 mm** closest-surface clearance; no sampled penetration.
- Final exported pairs: `renders/iron-final-glb/inlet_material-pair.jpg` and
  `renders/iron-final-glb/manhole_material-pair.jpg`; corresponding pre-bake
  comparisons are in `renders/iron-final-source/`.
- Final close-ups: `renders/final/{inlet,manhole}.png`; dressed hero:
  `renders/final/dressed.png`; contact: `renders/final/contact.jpg`.
  All final street metadata references assembly SHA-256
  `ff3bf9bef92258b12de1acd64ffa42e06b6eb58a4b95ceb3c24246d6b6ab0fc7`.
- Refreshed docs: hero 190,593 bytes, overview 186,393, details 198,301;
  all 1600 px wide. Only these finished JPGs are committed.

Accepted road/curb/walk/ramp/drive/lawn modeling and material functions were not
changed. Only this inlet's crossing fringe cards were excluded and its pan tint
localized. Shared kit code is unchanged. No tool installation or lead action
is needed.
