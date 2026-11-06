# LOD reduction checkpoint

The immutable reference is the delivered asset, with its shipped maps and glTF
material behavior. This work does not redesign the accepted assets or change
their original documentation images. [LOD.md](LOD.md) records the production
sources, engine integration and pixel-based acceptance. A triangle target does
not waive the original RGB/alpha/local image limits.

## Input receipt

The starting commit is `3c7140a`. Its previous chains were 59,838→59,238 for the
pickup, 58,232→57,243 for Colonial 27, 19,912→19,690 for the grill,
18,258→14,732 for the selected station modules, 872→748 for the cone, and
23,680→2 for the tree. Those proved serialization and texture savings, but did
not justify the tool's geometry reduction. Their micrometer component/UV vetoes
are replaced on the new opt-in screen path, not relaxed globally for existing
asset builders.

`build/lod-baseline/existing.json` covers 59 original delivery, shipped-map and
documentation-image files. `build/lod-v2/receipt.json` separately covers 45
canonical glTF/GLB/BIN/image dependencies. Each chain also retains its immutable
`export/lod/baseline.json`. Final receipt results are recorded below.

The station selects `Canopy` (including islands) and `Dispenser_1`. Its original
container remains complete and byte-identical. LOD0 triangle/material/draw
counts describe those selected modules; resource bytes describe the full
station. Extraction savings are not simplification savings.

## Critique pass 1 — reduced geometry

Color and value first: LOD0 remains the color reference, including dark cavities,
black rubber/enamel and architectural paint. New geometry alone is insufficient:
re-triangulated vertex weathering and old chart seams changed its appearance.
New charts now evaluate the delivered PBR shader and vertex tint once, with
moving source/target pairs isolated during projection. Geometric adjacency is
restored before unwrap; treating every split glTF corner as an island had wasted
most of the atlas. Normals serialized into glTF are the actual bake cage frame.

The first complete revised chains and images are archived under
`build/lod-v2/pass1/<asset>/` and `pass2/<asset>/`. Full-size review rejected:

- The cone's 15% candidate changed its collar/base shading at the 108-pixel
  switch: worst p95 .0824 and local mean .0881 exceeded .08. Its far switch is
  retried at 97 pixels; LOD0 is untouched.
- The grill's lid highlights and thermometer popped locally even though global
  means were low. A stricter near geometric preset is tested. The early far
  envelope filled the hose loop; a subsequent surface volume preserved the loop
  but folded thin returns and produced false cutout holes. Both were rejected.
- The pickup lost headlamp response and showed a white windshield triangle.
  This is an appearance-transfer failure, not a reason to claim its counts pass.
- The house's new charts initially smeared the tiling phase; the far windows
  became white without spatial transmission. UV routing/packing and a separate
  transmission map address those distinct faults.
- The station showed bright rectangular graphics. Its source uses UV0 for
  BaseColor/alpha and a constant UV1 emission swatch. All source UV indices are
  now pinned explicitly, and translucent graphics bake over their real backing.
- Equal-area leaf compensation overfilled the maple crown. The first LOD2 also
  retained too much wood and spent its remaining budget on a giant card. That
  fallback now fails explicitly. Wood reduces first; card selection is spatially
  stratified, with sublinear enlargement. The fixed impostor jointly fits
  opacity and color to 32 own renders rather than superimposing four full trees.

These images spend substantial error budget; none is accepted merely because
its triangle count is lower. The original switch gates remain the arbiter.

## Critique pass 2 — closure, projection and construction

The volume trial's color/value broke into bright patches and dark holes on the
grill's support frame. Native-size LOD2 means .033–.037 and LOD3 means
.035–.045 were unacceptable. The memory cap also forced its volume resolution
coarser than the requested subpixel grid. That implementation was removed.

The replacement closes construction envelopes. Thin panels get closed shells;
concave filaments retain coarse native geometry. Thin attached trim may go,
while sampled attachment distinguishes it from a free support. Enclosed parts
are omitted. Every remaining shell must be closed/manifold with no slivers.
This is one mesh/material/draw at the proxy level, although intersecting closed
components can remain inside it. It is not a minimal boolean union.

A separate fixture now proves that bounded projection repair evaluates original
shader UV/color/normal fields, including batching, and refuses surfaces outside
the distance allowance. Exact texel-center coverage distinguishes padding from
real misses. Another fixture uses UV1 emission and a half-transparent graphic
over its own backing, and a procedural normal map: a constant-blue stand-in
cannot pass it.

The first envelope grill removed all zero-alpha interior misses and lowered
LOD2 mean RGB to .010–.0175. Its front/55° p95/local changes still failed;
its 900-triangle last level still caved the lid visibly. Those full-size images
are archived at `build/lod-v2/envelope-before-lid/`. Broad curved shells now use
outer envelopes, while closed concave tubes retain their own surface. The near
preset is tightened rather than waiving the local highlight gate.

The camera-facing tree alternative also needed an absolute controller: rotating
about the asset origin moved an asymmetric crown's center, and repeated calls
accumulated rotation and atlas offsets. The reference controller now rotates
around the actual card center and assigns absolute UVs. The fixture checks both
center preservation and repeated calls.

## Critique pass 3 — wrong surface hits

A native front crop located the near grill's worst 8×8 error on the left edge
of the silver control panel. The new black triangle was a projection ray
sampling the neighboring dark frame. Tightening the geometric preset increased
LOD1 from 8,478 to 10,164 triangles but left the local error at .160. That trial
was rejected as an ineffective fix, and the usual .75-pixel preset was restored.
`build/lod-v2/patches.png` shows the enlarged diagnostic crops; the native
`grill-merged` comparison remains the actual scale used for judgment.

The bake now measures its source-hit world position. A hit more than .1 pixel
from the nearest matching outward surface is re-evaluated there, within the
level's local geometric allowance. This catches opaque neighboring hits as well
as empty rays. Work streams in 8,192-point batches with small patch atlases,
not one full-resolution image per batch. Transparent foreground and backing
are repaired separately before straight-alpha compositing, including emission
and clearcoat. The GPU fixture proves a half-opacity red graphic over its brown
backing, UV1 emission independent of UV0, normal-map variation and spatial coat
weight. The separate repair fixture proves sidedness, repeated-call stability,
batching and rejection beyond the physical distance limit. Peak fixture RSS
stayed below 1 GiB. Those tests establish transfer correctness; the following
pilot renders still determine visual acceptance.

## Critique pass 4 — seams, material membership and fixed-card artifacts

The next full-size review found two distinct car defects: open assembly seams
at door material interfaces, and HDR light leaking onto non-emitting surfaces.
A tiny open material patch is not an expendable closed bolt. Pruning now keeps
open patches, and native collapse weights the geometric material borders while
allowing the old UV/normal seams inside them to reduce. The independent geometry
probe measured no new open assembly edges at 26,276 near triangles. A face-on
panel also stays when its depth alone is subpixel. Separate regressions exercise
both cases. The next source-hit trial was tightened to .01 switch pixel, because even a thin neighboring surface can have an entirely different HDR shader. New near atlases retain the source materials' emission membership;
reconstructed common-material shells still use spatial emission.

The house's middle envelope initially failed on 12 sliver triangles despite
having no boundary or nonmanifold edges. Dissolving near-coincident edges and
retriangulating coplanar neighborhoods yields a clean 8,724-triangle shell in
the geometry probe. A closed-box fixture checks that sliver repair does not
open a shell. These geometry probes do not replace the final baked renders.

At 128 samples the cone's previous far candidate still measured p95 .0828
against the .08 limit; its same-source seed variation was only .0118. Original
charts kept the bands straight but rejected every useful candidate with large
chart-crossing UV errors. That diagnostic was not adopted as an 872-triangle
"reduced" level. A stricter far structural preset is tested instead. The grill's
1800-triangle / 38-pixel trial likewise still measured p95 .0941 at 128 samples,
with seed variation .0157. Its switch is retried at 32 pixels; the limits stay.

The tree's 960-pixel construction views showed the enlarged near cards keep a
full crown. The fixed impostor had isolated colored flecks outside it and an
obvious planar construction from above. Its fit now constrains alpha to a
multi-view visual hull and colors to observed source radiance. The regression
rejects invented bright exterior pixels. Foliage comparisons use 128 samples
on both reference and level to reduce alpha-path noise; opaque comparisons
retain 24. Prelit fixed planes still cannot reproduce changing sun, wind or
all elevated views. The camera-facing alternative remains a separate file.

## Critique pass 5 — prove the shading direction

The added oblique-cage regression exposed a real normal-transfer defect. An
object-space self bake returned the geometric normal even with a non-axis-aligned
normal explicitly linked into the original Principled shader. Unit length and
variation across box faces had passed earlier tests, but did not prove the
source normal-map field was transported. The new test reconstructs world
shading direction from the exported tangent frame and requires the known
original direction within 0.0001 per channel.

Both the initial atlas projection and bounded repair now evaluate the original
shader's linked normal input, or its geometric shading normal when unlinked,
as an encoded world-direction field. Every covered texel converts that field
into the actual exported cage's tangent frame. The corrected oblique test and
all 29 kit modules pass. This is a material correction; the earlier pilot
images remain rejected evidence, and all six final chains are rebuilt with it.

## Critique pass 6 — atlas filtering and compound shells

The complete normal-field batch is retained under `build/lod-v2/pre-layout/`.
The grill passed at 8,462 / 3,156 / 1,800 triangles, and the cone at 348 / 268.
The car and house still failed real image limits, so those counts were not
accepted merely because their geometry was closed.

The car's original paint and lamp UV densities measured about 161 and 219
texels/meter; the new uniform allocation gave both about 67. Its near atlas
used only .163 UV area versus .433 in the original. Native front/side crops
showed blurred lamp patterns, bright seams and wheel-arch reflection halos.
The new layout weights charts by delivered UV/image density, cuts them at
normal-frame discontinuities, then packs all parts with gutters derived from
the sampled mip. A separate clearcoat-normal field restores the original
geometry normal independently of its base normal map; reusing the base bump
or a flat new cage for that glossy layer changes the reflection. Non-emitting
materials retain their original emission membership even in multi-material
middle shells. The one-material proxy uses spatial emission.

The house's middle atlas had 280,852 empty interior texels out of 1,207,851.
Its large roof hole was geometric: vertex connectivity joined touching closed
construction through nonmanifold assembly edges. One roof group had 1,834 faces
and 216 such edges. Convexifying that compound group bridged real roof valleys
beyond the projection allowance. Construction now follows manifold edge
adjacency before explicitly merging coplanar neighbors. Concave capped shells
retain their footprint. A closed/open-bottom L-shaped building fixture checks
that the valley remains and closure adds no boundary or nonmanifold edge.

Attached-trim removal now measures the backing construction's complete area,
rather than the area of one triangle in a dense body panel. Sampling actual
face interiors also prevents a post touching floor and body at its ends from
being mistaken for fully attached trim. New fixtures prove both cases. Smooth
cages retain hard edges at 35 degrees, and UV cuts separate discontinuous
normal frames so texture filtering does not mix unrelated tangent coordinates.

At 128 samples the tree's LOD1 passed all views and its camera-facing alternative
passed. LOD2 still exceeded alpha MAE at .061–.070: its total coverage was about
5% higher than LOD0, rather than too sparse. That also caused the adjacent jump
to the crossed impostor, whose direct comparison already passed. The next
trial reduces card enlargement from exponent .37 to .34, keeping the 20%
triangle count. All image limits remain unchanged.

The full 29-module suite passes after these changes, including UV density
weighting, hard-frame cuts, dense backing, free supports, concave closure and
independent base/coat world-normal transport. New serial pilot renders below
determine acceptance. GPU locks release between pilots. Shader repair keeps
its validated .1-pixel source-hit criterion and processes 16,384 samples in the
same 128-square patch image previously half-filled by 8,192; this reduces
per-batch overhead with a small mesh-memory increase.

## Critique pass 7 — finite atlas budget and noise floor

The first density-weighted grill trial failed loudly before export: 647 charts
with a 16-pixel gutter consumed the far 512 atlas. The middle level also split
almost every triangle for immaterial differences in interpolated corner normals.
Cuts now distinguish frame changes above one degree, while the 35-degree hard
cage edges remain. Gutter growth is limited by chart count and atlas size; the
report marks a capped request instead of pretending it protects every mip. A
128-chart regression requires positive atlas area and exercises that cap. The
same full image gates decide whether a capped layout is usable.

The station needed a noise-floor measurement before its previous failures could
be assigned entirely to geometry. Two original LOD0 renders at different seeds
measured mean .0202 / p95 .1137 / worst local .2295 at 24 samples: identical
geometry already fails all three limits. At 128 samples the local difference
was .1104. At 512 it measured mean .00535 / p95 .02745 / local .06330. A 2,048
sample checkpoint is selected for more local headroom, with a matching seed
probe before that pilot. The original lighting, indirect clamp, cameras and all
limits remain unchanged; denoising stays off. Other opaque pilots retain 24
samples and foliage 128 unless their own evidence requires otherwise.

## Critique pass 8 — native-size density checkpoint

Opened all nine current grill comparison strips and all four construction views
at their native size. LOD1 keeps the enamel value, curved highlights, wheel
openings and frame; all views pass. At LOD2 the control-panel and shelf-edge
highlights become broader and fragmented; its worst local RGB difference is
.100, above .08. The last shell keeps the open frame and hose loop, but loses
small feet/rails: silhouette loss reaches .063 and an adjacent p95 reaches
.090. These are failed image checks, even though the shell is closed and its
normal/winding checks pass. The construction close-up exposes coarse wheel
spokes, simplified knob skirts and softened labels; it is explicitly a distant
shell rather than a close-view replacement.

Opened all six current cone comparison strips and all three construction views.
The 348/268 chain preserves its orange/white values and the footprint at its
switches; every image gate passes. The enlarged construction view reveals
faceted bottom folds, blurred stripe edges and a coarse top opening, so the
remaining 131-triangle target needs an actual trial rather than an assumption
that those details can be removed. The accepted 268 count is preserved while
trying smaller candidates.

The complete previous station strips and dispenser close-ups were also opened.
The 24-sample noise is conspicuous under the lit canopy, while labels lose
sharpness and the middle fascia has a local triangular artifact. At the last
level the fixed rest-pose dispenser shell contains its surroundings in the same
material; the detail camera therefore shows neighboring island construction.
The full checkpoint is being regenerated with density-aware charts and the
measured sample override; it will be judged again, rather than inheriting an
acceptance from that noisy batch.

## Critique pass 9 — exterior correspondence and shell orientation

The density checkpoint improved the pickup's lamps, but its close view exposed
gray lining on the blue roof. A new two-layer shader fixture failed the old
nearest-surface repair: a hidden, same-facing lining was closer to the reduced
cage than the paint. Repair now tries the outward visible layer within the same
two-pixel allowance before its nearest compatible fallback. Source triangle
UVs also must not be extrapolated into unrelated atlas charts by a large repair
footprint. A one-pixel coarse target over a small blue chart next to red texels
checks that bound. Tiny evaluation patches are centered locally to avoid losing
precision after projection groups have been separated. Both shader fixtures
and the independent base/coat direction tests pass.

Those repairs alone did not fix the roof. Raw geometry then exposed 25 inward
closed components in the previous pickup shell, including its roof. Consistent
edge winding and agreement between a face and its shading normal do not prove
outward orientation. The builder now orients each closed island by signed
volume and removes collapsed zero-volume remnants after reduction. An inverted
cube and a flattened closed tetrahedron exercise both operations. The checker
independently measures island volumes from serialized triangles. With this fix,
three exposed roof samples carry the correct original paint RGB 29/55/76 rather
than lining RGB 124/126/124. The diagnostic close view still exposes crossing
construction skins elsewhere, so a voxel-union last shell is being evaluated
before committing the final pilot checkpoint. These diagnostics remain failed
image evidence; a passing unit fixture is not visual acceptance.

## Critique pass 10 — union shell and powered lenses

The separate construction envelopes could cross after independent collapse.
The last level now optionally unions them on a switch-relative voxel grid before
the shared budget collapse. The pickup probe used half-pixel cells and a
.3-pixel outward allowance to retain thin source skins during the union. Its
roof stays blue and the crossing lining triangles disappear. The 2,800-triangle
prototype peaked at about 1.4 GiB child RSS, including its atlas and renders.
The grill's thinner open frame uses quarter-pixel cells and .15-pixel allowance.
Both are starting geometry allowances; the same image gates still decide.
A fixture checks the union's count, closure and positive island volumes.

The first union made the pickup's headlights dark: a surface-emission bake sees
a transmissive lens, whereas LOD0 shows an emitter behind it. An additional
source pass removes transmissive faces for emitted-color projection and repairs
that layer within the same distance allowance. Its radiance is tinted by the
front glass field and added only on transmissive receiver texels. The serialized
atlas fixture reconstructs the expected HDR radiance behind a lens, verifies
opaque materials remain non-emitting, and checks the middle-level glass material
retains that receiver map. The original source hashes remain unchanged.
The current pickup probe has lit lamps and no broad gray roof patch; it still
fails the front mean/p95 and localized light/reflection gates. Those failures
remain explicit. Identical-LOD0 seed comparisons are being measured before the
final sample counts are selected, followed by fresh serial pilot evidence.

## Critique pass 11 — calibrate the comparison noise

Opened all source-seed comparison strips at native size. The original pickup
at the near switch differs from itself by worst local .197 at 24 samples,
.085 at 128 and .042 at 512. Far source comparisons fall to local .012–.018
at 512. Its final comparisons therefore use 512 samples on both sides. The
original grill's middle view measured local .051 / p95 .029 at 24 and local
.016 / p95 .012 at 128; the far p95 falls from .043 to .016. It uses 128 to
leave more of the unchanged budget for actual LOD error. Empty background is
excluded from these measurements, as it is for the geometry comparisons.
The visible noise concentrates in powered lamps, glass and specular edges;
these sample overrides do not change light, exposure, denoising or limits.

## Critique pass 12 — re-imported shader and empty frame coverage

The next controlled fixture evaluated the actual imported Normal Map outputs,
rather than reconstructing them with the baker's own inverse. A flat original
with known base bump and an independent coat direction was transferred to a
cage with varying corner normals. The old conversion produced a diagonal streak:
texel centers shared by two triangles were converted from world to tangent
space twice. Its maximum errors were 94 degrees for base and 118 for coat.
Covered texels are now converted once. The remaining systematic error exposed
an incorrect assumption that the interpolated frame was orthonormal. The
Cycles implementation normalizes the interpolated normal but retains the Mikk
tangent's interpolated length; the inverse now solves that complete frame.
Both re-imported fields measure p95 .265 degrees and maximum below .364 after
8-bit PNG storage. All four actual shader-field images were opened at native
size: the diagonal disappears, and the fields match the constant source inside
their chart. The new regression checks the shader, independently of the inverse.

The house's white gable also required a construction safeguard. Coplanarity
and touching bounds alone allow rake/frame rails to merge into a convex panel
across their opening. Planar merges now require at least 80% projected coverage,
or at most two square pixels of missing coverage. A hollow four-rail fixture
must remain four shells, while adjacent siding boards still merge. The grill's
union has a separate bounded post-union deflation trial: expanding thin shells
helps the union, but retaining all that expansion thickens its distant frame.
These construction corrections keep the original image and silhouette limits.

A control that retained the original charts and optical materials passed its
image gates, but kept 58,236 pickup and 57,709 house triangles at LOD1. It is
archived under `build/lod-v2/native-near-probe/`, and is not the delivered chain.
That repeats the original failure in purpose; a correct appearance transfer,
rather than reverting to those chart constraints, is necessary for useful
reduction on these assemblies.

## Critique pass 13 — reject ineffective silhouette adjustments

Opened all six union/deflation grill comparisons and both 960-pixel construction
views at native scale (`build/lod-v2/grill-erosion-probe/native-strips.png` and
`native-close.png`). The 996-triangle .1-pixel deflation has good RGB differences
(mean .012–.016, p95 .051–.063), but silhouette loss .065–.073 and adjacent
loss up to .076 fail .05. The 994-triangle .12 trial worsens the side/rear outline
to .086–.090. The close-ups expose distorted hose elbows and coarse wheel/knob
shapes. Neither trial is promoted. The closed envelope path without a voxel
union is tested separately before selecting a count fallback.

Opened every tree card-size/switch trial at native scale, packed without
resampling in `build/lod-v2/tree-card-trial/native-0.png` and `native-1.png`.
Exponents .30 and .26 at the 3.5% switch still change alpha by .056–.068.
Moving the .30 trial to 2.8% reduces that to .051–.060; even at 2.2%, the side
and rear remain .055/.053, and the rear transition to the fixed impostor stays
.053. The crown does not vanish, but its fine coverage shimmers differently.
Those are failed trials, rather than evidence for moving the switch. The
current round-robin crown-cell selection also overrepresents sparsely occupied
cells; a separate density-proportional allocation trial tests that cause.

## Critique pass 14 — fresh pickup, house and grill checkpoint

Opened all nine fresh pickup strips at native pixel scale, including the split
270-pixel near views, and all four construction renders. Counts are
26,276/11,710/2,800. The roof still has dark near patches and bright middle
seams; lamp detail changes locally, while the far lamps broaden. Geometry,
winding, import and normal checks pass, but every image view fails. Near local
RGB reaches .428, middle .491 against the preceding level, and far .231.
The far front also fails mean .0267 / p95 .133. None is labeled accepted.
Reusing the rebaked BaseColor for emission is a separate diagnostic: LOD0's
lamp material samples the same original image for both and has no vertex tint.
It improves front/side local error to .191/.357, but still fails. The canonical
chain retains its reproducible baked fields while that result is investigated.

Opened every fresh house comparison and all four construction renders. The
coverage guard removes the filled white garage gable. LOD2 is 8,690 triangles
and its front mean/p95 improve from .0254/.169 to .0144/.0715. LOD1 still shows
triangular garage-door shading, and all levels change eave/window detail.
Near local errors .220–.297 fail; middle local/adjacent errors reach .144.
The 1,798-triangle shell passes the rear but fails front/side color and p95
(.0304/.1137 at the front). All silhouettes and independent raw/normal checks
pass. Native pages are under `build/lod-v2/review-final/{cars,houses}/`.

Opened every fresh grill comparison and construction render, plus both no-union
goal trials. LOD1/2 pass at 8,462/3,096 triangles. The union's last silhouette
is too thick. The 986-triangle closed-envelope goal still fails the original
.05 alpha gate (front .0737, rear .0640); its .075–.109 IoU loss also fails.
The 1,796-triangle envelope keeps the outline better: all original RGB/alpha
gates pass, with alpha .0376–.0462, while IoU .0524–.0678 exceeds the initial
new .05 opaque cutoff. That cutoff effectively tightened the original alpha
budget for this thin antialiased frame. LOD0-only support measurements give
mean alpha .684/.720/.705 and equivalent IoU limits .073/.069/.071. The grill
uses .073, following the existing foliage opacity calibration, while retaining
every original RGB/alpha/local gate. The chosen no-union fallback is rebuilt
and checked again; its 1,000-triangle goal remains explicitly missed.

## Critique pass 15 — tree density and a measured switch adjustment

Opened all fresh 512-sample tree comparisons and construction views, every
density trial, and the original-tree seed pairs at native size. At the middle
side view, original-to-original alpha noise falls from .0137 at 128 samples to
.0053 at 512; the far rear falls from .0170 to .0071. That noise does not explain
the balanced-card level's .056–.064 alpha change. More samples improve the
measurement, but are not a geometric fix.

Round-robin occupied-cell selection overrepresents sparse outer crown cells.
Proportional quotas with stable largest remainders retain the original spatial
mass. At exponent .40, all neighboring-level and far transitions pass, but the
original 3.5% switch narrowly fails front mean .0202 and side alpha .0524.
The tested 3.2% switch (34.56 rather than 37.8 pixels) passes every original
RGB/alpha/local gate and the overlap gate, against both LOD0 and the preceding
level, at exactly 4,736 triangles. Its source alpha errors are .0464/.0489/.0451.
The transition to the fixed impostor also passes. The tested method is promoted
as an optional density selection; LOD1 keeps its passing balanced selection.
The regression uses a dense/sparse 90/10 leaf population, verifies that mass,
exact count, original UV/Wind fields and deterministic output. The complete
kit suite and six manifests are refreshed after promotion.

The large-card construction keeps a full crown; it is still visibly card-based
up close. The fixed eight-triangle impostor is an obvious planar star from the
25-degree construction camera, while the camera-facing alternative looks more
tree-like there. Both remain distant representations with frozen lighting and
wind; elevated cameras and changing sun need separate engine review.

## Critique pass 16 — retained material correspondence and near coat frames

At native size the pickup's isolated-material front/side/rear pairs now retain
headlight emitters rather than projecting their exterior lenses onto them.
Mean RGB falls to .0041/.0026/.0025; local errors .1815/.0850/.0770 still reject
two views. The construction close-up still shows angular roof reflections. A
new cage changes the implicit clearcoat direction even when the base normal
field transfers correctly, so the independent coat direction is now transferred
at near levels too. This costs another atlas; it is not a texture-memory saving.

Opened all three station material-isolation pairs in native crops, both
construction close-ups, and the original-to-original 2048-sample seed pair.
Separating retained graphics from equipment prevents decals projecting into
opaque backing; the station side mean falls from .122 to .013. The letters
still spread into soft white patches and the gold fascia stripe blooms. The
new atlas has finite capacity and too many padded charts, with large differences
from the source's intentional graphics density. These are actual failures,
not sampling noise (.00258 mean in the source-only control). Keep the image
gates and report the remaining failed levels.

Opened the cone's 146- and 128-triangle native three-view strips and close-ups.
The cheaper cones have a visibly polygonal stem/foot and smeared stripe edges;
front p95 .0880/.1024 exceeds .08. [The 146-triangle trial](../build/lod-v2/cone-0.15-current/trial-0.15.png) shows the change at native size. Restore the passing 268-triangle middle level
at the unchanged switch; its 15% target remains explicitly missed.

The promoted near-material test uses two overlapping materials inside one
moving node, compacted source material indices, and independently samples the
serialized backing/sign colors and opacity. The near clearcoat test measures
the actual re-imported shader against the original field on a varying-normal
cage, separately from the proxy test. All original deliveries remain read-only.

## Critique pass 17 — justify the fixed impostor switch

Retested the fixed eight-triangle maple at the original .02 switch (21.6
nominal pixels), using 512 samples and the promoted density-based middle level.
All three original comparisons pass, but the rear transition from LOD2 has
alpha MAE .0543, above the unchanged .05 gate. The 1.5% fixed-card switch stays;
this is a neighboring-level coverage failure, not a triangle-budget choice.
The native original/middle/fixed crops are at
`build/lod-v2/tree-original-far-switch/native.png`; complete measurements and
full renders sit beside them. The fresh canonical .015 transition is checked
again with the rebuilt middle level.

## Critique pass 18 — native-envelope controls and final tree review

Opened every fresh tree strip and all five construction views at native size.
The .032 density middle level keeps the crown's mass without the earlier outer
cell bias. All original and neighboring checks pass. The fixed impostor still
reads as a vertical planar star from the elevated construction view; its intended
16-pixel distance does not make it suitable for close or elevated presentation.
The camera-facing alternative is smoother there but needs its controller.

The pickup's non-voxel control uses 2,660 triangles. Native strips and the
construction close-up show white windshield/roof patches, angular doors and
lamp changes. Front mean .0679 / p95 .3373 is worse than the current union shell;
all views fail RGB gates despite passing silhouettes. It is rejected and the
2,800-triangle union proxy stays. The measured strips/close view and metrics are
at `build/lod-v2/native-far-final/cars/`. This is evidence against that automatic
fallback, not proof that a hand-built proxy cage cannot do better.

The house's non-voxel control uses 1,744 triangles but darkens the facade and
produces a broken-looking roof/valley patch in the construction view. Native
front mean .0394 / p95 .1530 and all three RGB views fail; its better outline
does not excuse that appearance. Keep the 1,798-triangle union candidate.
The rejected control and its measured native strips/close view are at
`build/lod-v2/native-far-final/houses/`.

The canopy/dispenser non-voxel control uses 1,762 triangles and closely matches
the outline (overlap loss .0035–.0061), but its lettering becomes bright blocks.
Source mean .0371–.0490 and p95 .1647–.2359 fail at every view. Its native strips
and whole-module close view at `build/lod-v2/native-far-final/commercial/` were
opened at full size. It is rejected; a good silhouette alone does not establish
a usable material proxy, and the canonical union candidate stays for the final
checkpoint comparison.

## Critique pass 19 — final pickup images remain rejected

Opened all nine fresh native strips and all four construction views. Retained
material isolation plus the independent coat direction improves the near side
local error from .4278 to .0736, which now passes. Front local .1646 and rear
.0890 still fail .08. The roof still has dark triangular patches in the elevated
close view; the independent coat map is not a complete fix for the real car's
atlas/projection seams. Middle roof edges and headlamps still jump; front mean
.0210 / p95 .0941 and local .431 fail. The far front mean .0267 / p95 .1333
and all far local gates still fail, with lamps broader/brighter and faceted
wheels. All silhouettes pass. Low global near means do not excuse local errors.

The 26,276 / 11,710 / 2,800 chain has actual reduction, but it remains an
unapproved image checkpoint. Its near five-map 2048 set costs 26.7 MiB versus
the original 16 MiB; adding the coat field did not produce a net near residency
saving. The next car recipe needs better chart/correspondence handling and a
verified lamp-power field, rather than looser gates or a claim of better engine
performance. The README records the failed status and exact costs.

## Critique pass 20 — final house images remain rejected

Opened all nine fresh strips and four construction views at native size.
The gable opening and roof valley remain intact in the union candidate, and
all silhouette tests pass. Near garage-door panels still turn into triangular
highlights; eaves, window trim and siding phase change too. Near local errors
.2850/.3113/.1560 reject all views despite low global means. The middle level
is closer but still fails local .1182/.1072/.0833. The far front/side change
broad facade value (mean .0304/.0243, p95 .1137/.0980); the rear passes.
Material isolation did not repair the geometric/atlas response on the garage
panels. It is a real remaining failure, not a reason to spend the image budget
again by increasing its limits. The 25,386 / 8,690 / 1,798 chain remains rejected,
with fresh costs and failure status in its README.

## Critique pass 21 — final passing grill fallback

Opened all nine fresh native strips and all four construction views. Near and
middle parts keep the dark enamel/steel values, cavity depth and lid highlight;
the knob skirts and small construction details reduce without a visible pop at
their switches. The far shell has coarse wheels and a softened badge close up,
but its holes, frame and hose loop read at the actual 32-pixel switch. Every
original and adjacent RGB/alpha/local/overlap check passes, as do raw checks.
The 8,462 / 3,096 / 1,796 chain is a passing visual fallback, with the 1,000-triangle
far goal still explicitly missed. The rejected 986-triangle construction's
[alpha-failure comparison](../build/lod-v2/grill-envelope-goal/native-strips.png) remains the reason for that miss; it is not claimed impossible
for a purpose-built cage to do better. Its native-envelope fallback is one
material/draw with a 512 map set, keeping overlapping closed envelopes rather
than claiming a union. The README and current manifest record those costs.

## Critique pass 22 — final cone and one last goal control

The additional closed-envelope control reaches 130 triangles, but fails the
unchanged switch gates: side p95 .1042 and alpha .0530, rear alpha .0531, plus
overlap loss .060. Its native construction view shows an angular mouth/foot and
shifted bands. [Its native comparison](../build/lod-v2/cone-proxy-goal/native-strips.png)
and close view sit beside its metrics. It is rejected without changing the switch
or limits. The 146/128 native reductions also remain rejected.

Opened all six fresh canonical strips and three construction views. The retained
348 / 268 chain passes raw and original/adjacent image checks at .25/.09. It has
coarse facets and wavering bands in the close construction view, but these remain
below the unchanged gates at its 97-pixel far switch. LOD2's 131-triangle goal is
still a target miss for these automatic methods, not a geometric lower bound.
There is no LOD3. Its README records the passing fallback and exact map costs.

## Critique pass 23 — final canopy/dispenser images remain rejected

Opened all nine fresh strips at native scale (split into nine readable pages)
and all eight whole-module/dispenser construction views. Retained material
isolation reduces the worst near side mean from .122 to .0130, but the lettering
still becomes white blocks, the fascia stripe spreads and small display graphics
smear. Near local errors .6059/.4862/.6243 reject all views. The middle level
changes broad panel/column value too: mean .0280–.0317, p95 .1216–.1294. The far
union has thicker roof/columns and altered dispenser details, with alpha
.0534–.0608 and overlap .0656–.0760. Every far view fails both color and coverage.
These remain real failures after the independent 2048-sample source noise control.

The 8,180 / 2,688 / 1,798 chain is a rejected checkpoint despite substantial
geometry/draw reduction and meeting its middle/far counts. The near framing clips
some canopy ends under the accepted vertical-bound convention; the independent
construction overviews show the complete module. This does not establish the
appearance of portions outside the switch camera. Its two nozzle meshes remain
separate near; all proxy geometry is at rest. The README records measured costs,
selected-container accounting and failed image status.

## Final measurements and remaining failures

These measurements use the final serialized files and freshly hashed comparisons. A failed image gate is a failed checkpoint; its low triangle count is not an approval.

| Pilot | LOD0 | LOD1 achieved / goal | LOD2 achieved / goal | Last proxy achieved / goal | `check-lod` |
| --- | ---: | ---: | ---: | ---: | --- |
| C150 pickup | 59,838 | 26,276 / 23,935 | 11,710 / 8,976 | 2,800 / 2,800 | FAIL: images |
| colonial seed 27 | 58,232 | 25,386 / 23,293 | 8,690 / 8,735 | 1,798 / 1,800 | FAIL: images |
| hero grill | 19,912 | 8,462 / 7,965 | 3,096 / 2,987 | 1,796 / 1,000 | PASS |
| small prop | 872 | 348 / 349 | 268 / 131 | none | PASS |
| red maple | 23,680 | 11,840 / 11,840 | 4,736 / 4,736 | 8 / 8 | PASS |
| canopy and dispenser | 18,258 | 8,180 / 7,303 | 2,688 / 2,739 | 1,798 / 1,800 | FAIL: images |

Exact per-level triangles, materials, draw calls, geometry/PNG/load bytes, map dimensions, texture/mesh GPU estimates and switches are in the six README tables and `build/lod-pilots/report.md`. The latter also lists every exceeded original/adjacent limit and links its native strip. [Six-pilot index](../build/lod-pilots/contact.jpg); this reduced-size sheet indexes evidence and is not the scale used for judgment.

| Pilot | Passing image levels | Failed image levels | Native evidence and construction views |
| --- | --- | --- | --- |
| C150 pickup | none | LOD1, LOD2, LOD3 | [`cars/renders/lod/`](../cars/renders/lod/) |
| colonial seed 27 | none | LOD1, LOD2, LOD3 | [`houses/renders/lod/`](../houses/renders/lod/) |
| hero grill | LOD1, LOD2, LOD3 | none | [`gas-grill/renders/lod/`](../gas-grill/renders/lod/) |
| small prop | LOD1, LOD2 | none | [`traffic-cone/renders/lod/`](../traffic-cone/renders/lod/) |
| red maple | LOD1, LOD2, LOD3, LOD3 camera-facing | none | [`trees/renders/lod/`](../trees/renders/lod/) |
| canopy and dispenser | none | LOD1, LOD2, LOD3 | [`commercial/renders/lod/`](../commercial/renders/lod/) |

Every far opaque shell is one material and one draw call, with an independent 256 or 512 atlas set baked only from its immutable LOD0. All have independently checked closed, consistently oriented, positive-volume construction. The grill fallback keeps separate overlapping closed envelopes; it does not claim a boolean union.

| Far proxy | Triangles | PNG maps | PNG bytes | Texture GPU MiB | Mesh GPU MiB |
| --- | ---: | --- | ---: | ---: | ---: |
| C150 pickup | 2,800 | BaseColor 512×512, ORM 512×512, Normal 512×512, Emission 512×512, Transmission 512×512, Clearcoat 512×512, CoatNormal 512×512 | 394,691 | 2.334 | 0.1563 |
| colonial seed 27 | 1,798 | BaseColor 512×512, ORM 512×512, Normal 512×512, Transmission 512×512 | 397,938 | 1.333 | 0.0880 |
| hero grill | 1,796 | BaseColor 512×512, ORM 512×512, Normal 512×512 | 316,843 | 1.000 | 0.1088 |
| canopy and dispenser | 1,798 | BaseColor 512×512, ORM 512×512, Normal 512×512, Emission 512×512 | 252,054 | 1.333 | 0.0902 |

The maple has two enlarged-card intermediate levels, a fixed four-plane/eight-triangle impostor (1024×256 RGBA) and a separate camera-facing two-triangle/32-sector alternative (2048×1024 RGBA). The fixed version needs no controller. Both freeze lighting and wind. Near levels retain the delivered leaf UVs, bent normals and Wind data.

Near moving frames/names remain on both near levels; the README tables enumerate their separate meshes. The proxy merges their rest geometry. These are rest-pose and data-preservation checks, not swept animation-clearance or game-controller tests. The pickup’s custom lamp-power alpha controller still requires the original LOD0 until that non-glTF field has a dedicated transfer adapter.

Validation:

- All 29 `kit/test_*.py` files passed serially from cleaned fixture folders: ordinary Python unittests for the seven pure-Python files, Blender for the other files, and `kit/with_gpu.sh` for the five GPU fixtures. Logs: `build/lod-v2/regressions/`. The new tests exercise screen/mip acceptance, pruning, material welding, closed proxy appearance, retained material isolation, source immutability, density quotas and actual re-imported base/coat shader directions.
- All six original `make check` targets passed. The checks used the accepted immutable deliveries/build targets as `make -o` inputs, so verification could not trigger a destructive rebuild of LOD0; houses used `SEEDS=27`. Exact commands and exits: `build/lod-v2/original-checks.json`.
- `make -C <pilot> lod` and `make -C <pilot> check-lod` ran serially for every pilot. The table above reports their image failures honestly. All six pass re-imported counts/surfaces/pivots, winding, topology policy, normal/tangent checks and immutable-source receipts.
- `python3 kit/repo_check.py` and `git diff --check` passed. Streaming preservation receipts cover 59 original delivery/map/docs files, 45 canonical dependencies and 155 supplemental delivery resources, with overlap between ledgers; all remain byte-identical. No source delivery, original map or original docs image was rewritten.
- One own Blender process at a time, four CPU threads, shared GPU lock, no parallel builds. Peak process memory and complete per-pilot build/check exits are recorded in `build/lod-v2/material-final-checkpoints.memory.json` and `final-pilot-checkpoints.json`. Waiting for other GPU users is included in elapsed time.

Measured canonical checkpoint costs (GPU queue and diagnostic trials excluded from each pilot row):

| Pilot | Build + render, min | Check, s | Peak child RSS, GiB |
| --- | ---: | ---: | ---: |
| trees | 3.8 | 2.5 | 1.40 |
| cars | 10.9 | 14.5 | 2.36 |
| houses | 16.4 | 17.6 | 2.50 |
| gas-grill | 4.9 | 5.1 | 2.21 |
| traffic-cone | 1.2 | 1.8 | 1.23 |
| commercial | 23.4 | 6.8 | 2.65 |

These pilot timings are planning inputs, not a linear promise for every variant. Species/material layouts and the number of charts drive bake/review cost. Family reuse needs review before sharing an atlas or reduction recipe.

## Applying the tool to the remaining library

A library batch still needs the failed appearance transfers resolved and an
approved recipe per family. The present image checks do not justify a claim
that these chains beat an engine's automatic LODs in visual quality or frame time.

| Family | Work required before a library batch |
| --- | --- |
| Vehicles | Configure canonical moving roots and any skinned cables, review wheel/body silhouettes and glass/lamp/coat transfer per body type, then verify animation poses in the target engine. Reuse configs across cosmetic variants only after checking their atlas/material routing. |
| Houses and commercial modules | Select coherent modules; merge adjacent boards/trim without bridging gaps between buildings; preserve doors near. Review roof/porch recesses and glazed openings per footprint. Seed-specific near atlases can cost more scene memory than shared tile sets; use family atlas sharing or canonical near charts where practical. |
| Hero and small props | Establish feature sizes and moving roots per construction. Most use native reduction; large open assemblies need a tube/void review before the final shell. Do not add a proxy to an already tiny cone merely to complete a standard four-row table. |
| Trees and shrubs | Calibrate card enlargement and switches per crown/species, retain source wind fields near, capture/fix each species' own impostor. Fixed cards need no controller, but frozen wind/light and elevated cameras remain limitations. |
| Modular streets, fences and repeated fixtures | Keep connectors and placement frames, group compatible pieces/materials, and review section endpoints. Assess family texture residency and instancing; a per-piece atlas can defeat existing sharing. |
| Guns and other mechanical assemblies | Audit moving roots/skins and material extensions, retain near interaction behavior, and use far proxies only for world/dropped presentations. A first-person weapon that never gets small on screen has little to gain from this distance chain. |

The rollout needs per-family configs, serial build/bake time, native-size review,
original-byte receipts and target-engine integration. These cold-load and
primitive-count measurements do not establish frame time, engine memory
residency or swept animation clearance. Collision remains separately chosen
geometry. Shared maps save memory only when the scene's resource policy actually
releases or streams larger sets; an object-level cold-load saving is not a
whole-scene residency measurement.

The house's original shared images total 38 MiB under this estimate. For scale,
40 independent 1.33 MiB proxy sets would total about 53 MiB before any near
maps. That is a planning example, not a measured library scene: it shows why a
per-variant cold-load saving cannot establish a family-wide memory improvement.
