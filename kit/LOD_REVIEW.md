# LOD reduction checkpoint

The immutable reference is the delivered asset, with its shipped maps and glTF
material behavior. This work does not redesign the accepted assets or change
their original documentation images. [LOD.md](LOD.md) records the production
sources, engine integration and pixel-based acceptance. A triangle target does
not waive the original RGB/alpha/local image limits.

Passes 1–23 and their measurement tables record the earlier `f6b0cf9`
checkpoint. The shared-map revision begins at pass 24 below; its final measured
checkpoint supersedes those earlier costs and failure descriptions.

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

## Critique pass 24 — shared-map handoff, native baseline review

Merged current main (`4964db8`) in `52f7f72`, preserving both the strip-mall
rules/docs and station LOD hooks. Opened all 27 failed pickup, colonial and
station native strips, including the two named 55-degree near/middle failures.
Color/value first: the pickup's middle lamps are broader and brighter than the
original lens/reflector; rear roof edges open. The colonial's garage relief turns
into triangular highlights and side siding loses its original value/phase.
The station's lettering is replaced by white blocks and its gold fascia spreads;
the far canopy grows thick while losing coverage. These are real visible transfer
failures. The accepted reductions/proxy construction, switches and image gates
remain the starting basis, not evidence of visual approval for those three.

The original near atlases add image content and resident memory. The new path
keeps original map bytes/material settings, with paired UV/material-seam
collapses and original alpha/emission routing. Whole-chain accounting includes
unique original maps, only far proxy/impostor maps, and every mesh. Actual GPU
sharing requires binding near primitives to the original material resources;
content equality across private importer caches is insufficient. A preservation
ledger covers 408 existing delivery/map/docs files before work.

## Critique pass 25 — reject shortcut UV transfer and insufficient reductions

Tested the accepted cone's 268-triangle pre-atlas cage directly on the original
maps. Opened all six 1080p control renders as native, unscaled source/control
crops at `build/lod-v3/cone-map-control/native-crops.png`. The original orange and
white bands become stretched black/orange ribbons on the cage. Front mean .1000,
p95 .4824 and local .3654 fail; side/rear fail too. This rejects simply removing
the atlas bake from the existing geometry recipe. It does not reject the accepted
268-triangle baked fallback's previous appearance.

Early endpoint-QEM trials preserve source maps but retain too much geometry:
the pickup first held 50,806 near triangles, then 46,776, and the cone retained
722/680. These are rejected reduction trials, not deliveries. Component-local
checks, normalized normal correspondence, paired material wedges and small
seam-junction transport improve the next cone to 578/476, still above its
accepted basis. The shared-map public fixture passes actual build/re-import,
material/image identity, geometry/pivot checks and the independent normal audit.
No passing six-chain checkpoint is claimed yet. Diagnostic build/check logs are
under `build/lod-v3/`; cancelled superseded CPU trials are explicitly recorded.

## Critique pass 26 — distinguish source glare from transferred lamp growth

Opened the native far pickup probes and independent source/material controls at
original resolution (`build/lod-v3/far-probe/cars/` and
`build/lod-v3/glass-control/`). Color/value first: the bright windshield is
already present in the delivered source under this sun, so flattening glass or
removing its normal map would change the accepted look. Disabling emission
removes the broad lamp brightness but leaves the bumper patches. The probe
still fails: front mean .0307, p95 .1458 and local .2585; side local .2351;
rear local .1086. Coverage and outline pass. These probes precede the final
antialiased-emission change and are diagnostic evidence, not the final chain.

Found two transfer defects: repair had treated zero alpha as a failed shader
sample, discarding real transparent print pixels; and point/nearest repairs
could replace filtered emission coverage with full bright source samples.
Independent constant shader coverage now validates transparent patches. Emission
keeps direct antialiased rays without nearest extrapolation or bake margins.
A footprint-aware position guard preserves valid filtered source samples.
Closed opaque proxies derive coverage from their closed shell, rather than
turning projection misses into alpha holes. Regression fixtures for transparent
patches, bounded emitters and actual shader-normal transport pass. Final
switch-distance evidence below must still determine whether the changes suffice.

## Critique pass 27 — shared maps expose construction-order failures

The first complete shared-map pickup was 29,472 / 18,498 / 2,800 triangles.
The completed LOD2 55-degree strip restores the gray internal lens/reflector
instead of the previous white blob and keeps the rear cab roof closed. One early
view opened the previous LOD2 strip while its replacement was still rendering;
only the completed, manifest-matched evidence is used here.

Color/value first: new triangular dark patches appear across the cab roof in the
construction view. They persist with base and coat normal inputs disconnected,
and with a constant gray diffuse paint replacing every paint texture. This rules
out a rebake, a changed map or tangent-space decoding as the cause of that roof
pattern. The source roof construction has intersecting internal skins. Independent
simplification changes their visibility ordering. A broad source-component guard
removes the roof artifacts, but retains too much unrelated construction: 37,400 /
28,854 triangles. Native strips of all nine views and all four close views were
opened for that control. It still fails the local gate: LOD1 front .2797 and rear
.2236; LOD2 rear .1377. Maximum-error crops at native scale locate these errors
inside the headlamp and at the tail-lamp edges, not on the repaired roof.

The narrower guard samples candidate face-center visibility from 14 directions
and restores only constructions that expose a previously hidden back face.
The source roof independently triggers it in `build/lod-v3/visibility-probe.log`.
The lamp failures are caused by reducing/pruning neighboring opaque shutters and
housings while retaining the powered surface. Powered assemblies now retain
neighboring construction selected conservatively by bounds, before pruning.
`build/lod-v3/near-frame-control/` preserves every normal/plain-material control;
`max-patch-*.png` preserves the lamp diagnoses. The next complete checkpoint
must judge these changes; source-normal thresholds and image gates are unchanged.

The normal auditor also had a correspondence error: choosing the smallest UV
residual alone can select an opposing skin when an atlas reuses UVs. It now
chooses the normal among all source correspondences satisfying the same half-mip-
texel bound, while retaining the original 45-degree maximum / 10-degree p95
limits. Image acceptance remains independent of that ambiguity correction.

## Critique pass 28 — face interiors and the unreplaced cone

Color/value first: the original shared-map cone attempt kept its source images,
but changed the light response of the orange and white bands. The independent
vertex audit measured only 2.4 degrees of normal change while interior samples
found about 23 degrees (area-weighted p95 about 18). Explicit tangent decoding
was tested and rejected: it made negligible improvement. The failure was the
interpolated frame inside long triangles, not an image transfer. Face-center and
edge-midpoint frame checks now preserve broad faces tightly and use a bounded
screen-relative allowance on smaller faces. Redundant normal splits can join;
real frame discontinuities retain separate corners.

The completed current cone is 872 / 626 / 436 triangles. All six native strips
and all three construction views were opened at original resolution. Both
levels preserve the original hue, band values and source maps; the far neck and
base remain mildly faceted in the close view, but the switch comparisons pass.
The unchanged six RGB/alpha/local/silhouette gates, normal audit and fresh
re-import check pass (`build/lod-v3/cone-adaptive.log`). This **does not retain
the previously accepted 268-triangle count**: putting those old vertices back
on the original maps corrupts stripe phase. The 436-triangle result is reported
as an unresolved count regression, not as the accepted 268 fallback.

The pickup far-atlas supersampling control rendered a 1024 bake downsampled to
512, preserving linear color, normalized normals and RMS roughness. All three
native strips and its construction view were opened. Front mean improves from
.0315 to .0278 and the worst local patch from .2526 to .1988, still above .02 /
.08. Side and rear local patches also fail. This control is rejected; no
production bake or limit is changed. Evidence: `build/lod-v3/car-ssaa-probe/`.
The powered lens transfer remains weaker than the original multi-layer optics.

## Critique pass 29 — current shared-map exports, first review

Color/value comparisons below use immutable LOD0 under identical procedural
illumination. No photographic white balance is inferred for this transfer test.
Native strips include the original, preceding level, new level and amplified
difference; construction views are judged separately from switch-distance views.

- **Pickup:** all nine current native strips and all four construction views
  opened at original resolution. The near blue paint and deep grille values
  remain consistent. LOD2 retains the actual lamp/lens structure instead of a
  new white patch, and the rear cab roof is closed without the prior dark roof
  triangles. The source windshield already has the large white reflection seen
  in the close view. This is still a failed chain: LOD1 front local RGB is
  .19391 > .08; LOD2 rear .09825 > .08. Native crops locate these on the polished
  grille surround and rear bumper lip, rather than the lamps. Source maps are
  identical, but the remaining geometry/frame change moves a sharp reflection.
  The far proxy retains its shell silhouette but brightens/simplifies the lamps
  and distorts bumper reflections: front mean .03146 / p95 .14863 / local .25261;
  side and rear local .23024 / .10878. All three far views fail. The normal audit
  passes; the raw chain's only error is the failed image gate. Evidence:
  `cars/renders/lod/`, `build/lod-v3/final-patches/cars/`.
- **Cone:** all six current native strips re-opened at original resolution,
  along with the far construction view. Orange/white band values and phase
  match; near errors are effectively invisible, and the far maximum mean is
  .00624. The lower lip and neck show minor faceting in the close view, within
  the switch gates. Image, normal and raw checks pass. The 626 / 436 counts
  remain above their 349 / 131 targets, and 436 does not meet the owner's
  requirement to keep the accepted 268-triangle far level. This count regression
  is unresolved, even though the new shared-map appearance passes.
- **Colonial:** all nine current native strips and all four construction views
  opened at original resolution. Color/value first: LOD1/2 retain the siding
  tone and roof value; the garage panel relief no longer shades as large flat
  triangles. All six intermediate comparisons pass (largest mean .00856).
  Sharing original charts/maps and preserving their frame fixes the reported
  near defect; no intermediate rebake remains to introduce another transfer.
  The far proxy still flattens/changes the garage pattern, softens window trim
  and makes the eave shading irregular. At the actual switch, front mean
  .03006 / p95 .10980 and three-quarter mean .02388 / p95 .09804 fail. The rear
  far view passes. The normal audit passes; the raw chain reports only image failure.
  Coverage is not the limiting metric on this chain. The 31,774 / 21,092 intermediate counts exceed 23,293 / 8,735; the proxy is 1,798.
  Evidence: `houses/renders/lod/`, particularly `LOD1-55-strip.jpg` and
  `LOD3-0-strip.jpg`.
- **Canopy/dispenser:** all nine current native strips, all four full
  construction views and all four dispenser detail views opened at original
  resolution. Color/value first: near purple fascia, gold edge, white print,
  gray soffit and deep dispenser recess retain LOD0's values. RILLWAY remains
  legible in LOD1 and LOD2; all six near comparisons pass (maximum mean about
  .0020 on the final guarded export). The full overviews confirm coverage beyond
  the clipped near cameras.
  The closed/shrunk proxy fixes coverage: alpha MAE .00639 / .00700 / .00979 and
  silhouette loss .00748 / .00898 / .01237 all pass their .05 limits. This does
  not fix the entire far appearance. Its lettering blurs and its small powered
  panels lose/shift bright coverage; all three far RGB views fail (means .02956
  / .02253 / .02356, p95 .16863 / .12941 / .11373, local .13679 / .10809 / .14769).
  The dispenser proxy also looks coarse in close-up; that is not the scale at
  which its acceptance is measured. One merged rest shell cannot isolate the
  dispenser from adjacent supports for a detail shot, so nearby column/island
  geometry appears in that proxy close view. After the assembled-edge guard, counts 9,928 / 7,510 exceed
  7,303 / 2,739; far shell 1,798. Evidence: `commercial/renders/lod/`.
- **Maple:** all twelve native strips (including the camera-facing alternative)
  and all five construction views opened at original resolution. Color/value
  first: the crown stays dark green with the source's shadow depth; its leaf
  mass changes slightly as cards enlarge, rather than washing out. LOD2 front
  mean .0195 is close to .02, but passes at the accepted .032 switch. All image,
  normal and raw checks pass. Both impostors are visibly flat/soft in close-up,
  as expected; the fixed eight-triangle choice is judged at its sixteen-pixel
  switch. The camera-facing choice matches those views more closely and has a
  larger atlas/controller requirement. Foliage construction, switches and source
  maps are unchanged from the accepted basis. Evidence: `trees/renders/lod/`.

### Controlled colonial diagnosis

The retained 25,386-triangle pre-atlas LOD1 cage reproduces the garage diamonds
with LOD0's original maps. Disconnecting base and coat normal maps does not
remove them (local RGB .12069 with maps / .12104 without). Replacing all
materials with constant-gray diffuse still shows the facets; clearing custom
normals and using flat geometric normals also leaves them. Thus the garage
failure is already in the collapsed geometry and its face orientations, before
rebaking; tangent-space textures are not required to produce it. The old cage
also changes the side wall's tone with the original maps, so its geometry/UV/
attribute reduction cannot be treated as an accurate neutral carrier. The
current UV/frame-preserving path keeps both areas consistent with LOD0. These
controls do not isolate every possible contribution of the old wall transfer.

Four native comparison strips (eight renders) were opened at original size.
They use the same 55-degree camera and 25.11 m switch, 128 samples for diagnosis;
they do not replace the final acceptance images. Input hashes prove
that neither LOD0 nor the retained cage was modified. Evidence:
`build/lod-v3/colonial-cause/` and `build/lod-v3/colonial-gray/`.

The grill's 986-triangle trial was also opened in all nine native strips and all
four construction views. Its near color/value and all six intermediate image
comparisons pass. Far RGB passes, but coverage does not: front alpha .07374 /
IoU loss .10852, side .05407 / .07538, rear .06396 / .09074. These exceed .05 /
.073. The trial is retained under `build/lod-v3/grill-986/`; the accepted 1,796-
triangle construction was restored for the final comparison below. No limit is
relaxed to admit the smaller trial.

### Final assembly correction and grill review

The assembled-edge check found two new contacts that component-local tests had
missed. The grill's LOD1 combined nonmanifold incidence increased from one to
two; restoring three implicated thin components costs 24 triangles and returns
that measured incidence to one. Station LOD2 similarly restores 228 triangles.
These source defects remain distinguished from new defects: the grill source
body already has four boundary incidences and one nonmanifold incidence. Its
far proxy is closed, with zero of both. No original delivery was repaired or
re-exported.

All nine final grill strips/differences and all four construction views were
opened at original resolution after this correction. Color/value first: near
black enamel, gray fascia and deep frame shadows match LOD0. The larger frame
keeps its negative spaces and hose loop at the last switch. LOD2 shows knob and
wheel faceting in close-up; LOD3 blurs the badge and has rougher highlights, but
at its 32-pixel switch all three views pass every RGB, alpha, local and IoU
limit. Largest far reference mean is .0128. The completed chain is
19,912 / 11,696 / 8,070 / 1,796; the 1,000-triangle proxy goal is still missed.
The accepted fallback was kept because the 986-triangle trial fails coverage,
not because its target was changed. Raw, normal and image checks now pass.

The station's nine final strips and eight construction/detail views were also
opened again after the 228-triangle correction. Its broad gray roof and soffit
remain complete, near print stays crisp and dark fascia hue is consistent.
Far native maximum-patch crops locate the remaining RGB failures at the fascia
lettering: it becomes a bright soft smear while still spanning several pixels.
The repaired shell therefore passes coverage but remains an appearance failure.
Its final raw audit additionally reports ten new unmatched canopy edges in each
near level: 442 source boundary incidences versus 452 candidate, under the same
one-micrometer convention. Nonmanifold incidences fall from 130 to 100. The
group-local guard is insufficient at contacts across differing attribute groups
and does not include all interactions with pruned components. No broad coverage
hole is apparent in the images, but the raw failure stands. The station is not
an image-only failure and is not structurally approved.

## Critique pass 30 — final switch review and cost decision

Color/value first, again against the unchanged delivered LOD0 under the same
lighting. Reopened the pickup LOD2 55/145-degree views, colonial LOD1 55-degree
view, station LOD2 55-degree view and all three far maximum-patch crops, grill
LOD1/2 55-degree and all three far views, cone LOD2 55-degree view, and maple
LOD2 front / LOD3 55-degree views at original resolution. The previous complete
image reviews remain the basis for the other views; the contact sheet is only
an index.

- **Pickup:** the LOD2 lamp retains its gray lens and actual bright emitter
  shape; the rear cab roof stays closed. Those requested defects are corrected.
  Two other near polished-metal reflection patches still fail, and the far
  lamps/bumper transfer is still unacceptable. Shared maps alone do not preserve
  a sharp reflection after its carrier changes.
- **Colonial:** siding brightness and garage-panel shading stay consistent in
  the current near path. The constant-gray controls establish that the old
  garage fault preceded rebaking and involved collapsed face orientations.
  The current far garage/eaves still change enough to fail two views.
- **Station:** near letters remain readable, the canopy does not lose coverage,
  and the far shell passes alpha/IoU. The far atlas still blurs its large fascia
  text into a brighter patch; all three far RGB views fail. This is not accepted
  as legitimate disappearance of subpixel lettering. The additional near
  assembly-edge failures also remain open.
- **Grill:** near black values and frame gaps remain stable. The 1,796-triangle
  proxy passes at the switch; the 986-triangle proxy does not. Keep the larger
  shell and report the goal miss.
- **Cone:** band phase and orange/white values match. The new 436-triangle far
  level passes appearance, but does not preserve the owner's accepted 268.
- **Maple:** near crown mass and deep green values remain credible; LOD2 front
  mean .0195 narrowly passes .02. The accepted eight-triangle fixed impostor and
  optional camera-facing alternative both pass. Frozen light/wind and elevated
  viewing remain the original impostor limitations.

All intermediate images match LOD0 by complete hash and use its original
materials. No intermediate atlas is referenced. The fixed-chain estimates below
include **every** mesh level, full mip chains and deduplicated canonical images.
They exclude engine metadata and assume the engine actually binds those shared
resources; matching embedded/external PNG bytes does not prove driver reuse.

| Chain | Triangles, LOD0 onward | LOD0 resident MiB | Whole chain MiB | New far maps MiB | Additional mesh MiB |
| --- | --- | ---: | ---: | ---: | ---: |
| Pickup | 59,838 / 41,084 / 36,792 / 2,800 | 21.140 | 30.836 | 2.334 | 7.363 |
| Colonial | 58,232 / 31,774 / 21,092 / 1,798 | 42.837 | 48.918 | 1.333 | 4.747 |
| Station | 18,258 / 9,928 / 7,510 / 1,798 | 87.678 | 91.396 | 1.333 | 2.384 |
| Grill | 19,912 / 11,696 / 8,070 / 1,796 | 17.497 | 20.238 | 1.000 | 1.740 |
| Cone | 872 / 626 / 436 | 1.044 | 1.102 | 0 | .058 |
| Maple | 23,680 / 11,840 / 4,736 / 8 | 18.550 | 21.204 | .333 | 2.321 |

The station row retains the **complete immutable original container's** memory
and byte costs, while triangle/material/draw rows describe the selected modules.
Near extraction savings are not credited as simplification. Replacing the fixed
tree impostor with the optional camera-facing one gives 23.537 MiB for that
alternative chain; both alternatives are not assumed resident together.

The texture residency requirement passes for all six: original images plus only
far maps. If “LOD0 plus the proxy atlas” is read as a cap on the **entire** chain
including additional vertex/index buffers, all six exceed it by the explicitly
shown mesh increment. Those buffers are not hidden in the estimates.

The higher near counts are substantial, not small target excursions:

| Chain | LOD1 achieved / goal / excess | LOD2 achieved / goal / excess |
| --- | --- | --- |
| Pickup | 41,084 / 23,935 / +71.6% | 36,792 / 8,976 / +309.9% |
| Colonial | 31,774 / 23,293 / +36.4% | 21,092 / 8,735 / +141.5% |
| Station | 9,928 / 7,303 / +35.9% | 7,510 / 2,739 / +174.2% |
| Grill | 11,696 / 7,965 / +46.8% | 8,070 / 2,987 / +170.2% |
| Cone | 626 / 349 / +79.4% | 436 / 131 / +232.8% |
| Maple | 11,840 / 11,840 / 0% | 4,736 / 4,736 / 0% |

These counts retain chart/frame/construction agreement instead of spending new
map memory. They do not retain the previous rebaked chains' reduction counts.
The pickup's LOD2 is especially weak as a cost reduction. No image gate or goal
was lowered to call this complete. The seven-kind adoption recipe in `LOD.md`
is complete enough to follow, but remains **provisional** until this checkpoint
has no failed chains. The next useful work is source-field-aware reduction of
the retained near constructions, a whole-mesh guard covering pruning and
incompatible attribute groups, and a sharper far transfer of print/lamp and
garage surfaces, rather than another intermediate rebake.

### Evidence integrity

Final assembled-edge code changed no serialized geometry, maps or rendered
pixels for pickup, colonial, cone or maple. Complete dependency sets and every
rendered image hash were compared before reusing those images; metrics record
the old and new manifest hashes and the full receipt. Station and grill were
rerendered because their geometry changed. Evidence:
`build/lod-v3/render-input-revalidation.json` and
`build/lod-v3/before-aggregate-guard/`. This is input revalidation, not a relaxed
render limit. Fresh final raw and normal checks were run on all six.

The inherited strip-mall historical receipt had also captured the previous
station/house LOD outputs. Its 49 authorized LOD entries were archived and
removed from that original-delivery receipt; all 134 non-LOD digests were first
verified unchanged. The LOD audits retain their own independent immutable-source
baselines, and the session's 408 original delivery/map/doc files still match.
Scope proof: `build/lod-v3/strip-receipt-scope.json`. No original-delivery digest
was refreshed to conceal a change.

Full measured per-level materials, draw calls, geometry/PNG/dependency bytes,
map dimensions, checks and resident totals are generated in
`build/lod-pilots/report.md` / `report.json`. All native images remain in each
pilot's `renders/lod/`; the six-chain index is `build/lod-pilots/contact.jpg`.
No original docs JPG was replaced and no failed checkpoint image is committed.

### Final validation, 2026-11-06

- Merged `main` at `4964db8` in `52f7f72`, retaining signals, utility poles and
  the strip-mall delivery alongside the existing station and LOD hooks.
- Rebuilt all six chains through `kit.lod.build`, serially with four threads:
  five `make -C <pilot> lod-mesh LOD_THREADS=4` jobs and the grill's equivalent
  `build/lod-v3/check-grill-aggregate.py` invocation. Source recipes/payloads
  were frozen before final rendering and tests. Changed station/grill payloads
  were rerendered; the other four chains have complete identical-input receipts.
- Fresh `make -C <pilot> check-lod LOD_THREADS=4`: **grill, cone and maple pass**;
  **pickup, colonial and station fail**, with exact errors above and in the
  generated report. All six normal audits pass. Goal misses remain separate
  from the image/raw results; neither the cone count nor grill proxy goal is met.
- Every original pilot `make check` passes, including the commercial strip and
  four station seeds. Accepted generated inputs were frozen with explicit
  `make -o path` arguments to prevent regeneration. Complete commands and exit
  codes are in `build/lod-v3/original-checks-final.json`; the successful commercial
  rerun is `commercial-original-after-scope.log`. Its initial receipt-scope
  conflict remains recorded, not erased.
- All **30 `kit/test_*.py` files pass** from cleaned fixture/cache directories,
  serially: Blender for bpy fixtures, `python3 -m unittest` for the seven pure
  test files, and `kit/with_gpu.sh` for all five GPU fixtures. Driver:
  `build/lod-v3/regressions.py --phase cpu` then `--phase gpu`. Per-file logs,
  current source hashes and exits are in `build/lod-v3/regressions/`; final phase
  logs are `regressions-final-cpu.log` / `regressions-final-gpu.log`.
- `python3 build/lod-v3/preserve.py --check`: **408 files, zero changed**.
  `python3 kit/repo_check.py`: **1,681 source files, zero errors**.
  `git diff --check`: pass. Existing tracked docs images also match `f6b0cf9`;
  the only docs-image additions are those brought by the main merge.
- `python3 build/lod-v3/final-proof.py`: verifies all those receipts, current
  tool/config/source hashes and every rendered-image hash. Machine-readable
  result: `build/lod-v3/final-proof.json`. Peak child-process RSS across the final
  serial jobs is **2,907,196 KiB (2.77 GiB)**; this is host-process memory, not an
  engine/GPU allocation measurement. Every Cycles operation used the shared lock.

The checkpoint remains **incomplete**. No failed chain or count regression is
approved by the passing regression suite, and the provisional recipe does not
authorize rolling these failures into other families.

## Critique pass 31 — reduction handoff and constraint diagnosis

The new brief accepts the shared maps, moving rules, existing lamp/roof/garage/
siding/near-lettering fixes, the 1,796-triangle grill proxy, 436-triangle cone
LOD2 and the maple chain. Those approvals supersede the unresolved cone-count
wording in pass 30. Original deliveries remain the immutable color/value
reference; this comparison does not infer photographic white balance.

Opened every ten failing native strips linked by the handoff report, at full
size: pickup LOD1 front, LOD2 rear and all three LOD3 views; colonial LOD3 front
and three-quarter; station all three LOD3 views. The pickup's thin grille and
rear-bumper reflections move while paint value remains consistent. Its proxy
brightens/broadens the front lamps. The colonial proxy changes the garage/eave
response and softens trim. The station proxy retains broad coverage but spreads
its fascia lettering into a brighter soft patch. These are remaining faults,
not approved merely because the silhouette or global mean passes.

The source constraint inventory distinguishes constraints from persistent pins.
Of the pickup's 30,971 geometric vertices, 26,151 touch UV seams, 23,112 touch
hard-normal splits and 396 touch material borders; only 64 are on open part
boundaries. There are 13,298 vertices in moving meshes. Powered/glass/alpha
protection pins 4,022 vertices; the old boundary rule adds 64. The colonial has
31,492 geometric vertices, 28,191 UV-seam vertices, 28,185 hard-normal vertices,
12 material-border vertices, 1,074 open-border vertices and 452 moving vertices.
Its protected surfaces pin 552 vertices. These categories overlap. Calling
every seam a locked vertex would misdescribe the implementation; the separate
initial-offer comparison records which vertices actually lack a mapping/weighted
collapse offer, before later field and visibility tests.

The pickup's old source-skin fallback restores 6,948 / 10,898 triangles at the
two near levels. The auxiliary guard used the width of the containing triangle
as the width of a newly visible patch. A broad triangle can appear through a
subpixel slit. The replacement samples that actual patch at half-switch-pixel
spacing and retains the existing three-pixel width criterion. Narrow-slit and
broad-exposure fixtures pass; native switch renders must still approve its
actual use. No RGB, alpha or local image threshold changed.

The station's ten net new boundary edges are source junctions with three face
incidences, reduced to one when a small closed construction disappears. Their
measured coordinates are retained in `build/lod-v4/station-edges.json`. Pinning
source junction endpoints before pruning addresses that cause; a fresh whole-
assembly audit, rather than a constant or a rendered silhouette, must prove it.

An initial edge-constrained colonial LOD1 trial reached 29,514 triangles; its
middle build was canceled to incorporate per-side affine wedge transport and
source-normal sampling. It is diagnostic evidence only. The subsequent full
near trial and proxy material-field diagnoses are still pending at this entry.
Evidence and original-image archives: `build/lod-v4/`; baseline report/strips:
`build/lod-v4/baseline/`. The 443-file preservation check passes after the main
merge `6e1f96a`.

## Pass 32 — isolate projection causes and restore the delivered shading frame

Reviewed the three native-size pickup strips in
`build/lod-v4/frame-probe/` and all fifteen native proxy diagnostic strips in
`build/lod-v4/proxy-diagnosis/`. These are controlled experiments on the handoff
meshes, **not approval of the still-pending cheaper reductions**.

Color/value first: the source-density station atlas spreads pale fascia text
and loses contrast; its base-only local error is .0943, while plain gray
geometry is .0463 locally. Coverage, roughness and source AO do not explain the
broad label miss. The colonial remains visibly flat around windows and its
porch even with the same gray material: gray-geometry mean .0319 versus .0195
for unlit base color. The pickup mixes geometric recess loss with optical
response; its gray-geometry mean is .0276. A blanket color correction would
hide those different causes. These diagnostic projections deliberately disable
lighting for the individual field views; their remaining differences cannot
be attributed to the color bake containing studio illumination.

The installed Blender 5.2 importer reads NORMAL but ignores TANGENT. A supplied
normal map therefore receives a different basis after each retriangulation.
The comparison renderer now reconstructs the supplied frame, including tangent
handedness and independent coat normals. The GPU fixture independently evaluates
aligned, rotated, mirrored and placed tangent fields: maximum component error
1.4481e-5. Its twelve constant-field output images were reviewed together in
`build/lod-v4/shading-fixture-contact.png`. The aligned native/restored pair
agrees; rotated native/restored fields intentionally differ.

The native pickup probe now shows the same broad grille reflection in original
and restored near levels. LOD1/front mean .00161, p95 .00392; LOD2/rear mean
.00405, p95 .02137. Remaining changes concentrate on chrome contour pixels and
small rear edges. LOD3/front is still wrong (mean .03153, p95 .14294); it is not
approved. LOD0 itself was not modified: the renderer correction changes only
the temporary imported shader graph.

The near front's 8x8 raw patch maximum .1936 fails the old .08 limit despite
being a contour shift, not broad reflection movement. A separate same-image
sampling calibration (`build/lod-v4/pixel-calibration.json`) shifts LOD0 by
fractional native pixels without changing its colors: .5px horizontal yields
.1304, 1px vertical .1973. This demonstrates that .08 is incompatible with the
accepted subpixel structural policy on a bright chrome contour. Any revised
local limit must remain limited to the calibrated near pickup case, retain
mean/p95/coverage gates and be accompanied by its actual native strip. The
proxy's broad front error has no such exemption.

## Pass 33 — reject a misleading aggregate topology improvement

The first station trial reached 9,890/18,258 triangles (54.17%) at LOD1, but its
individual ten previously failing junctions still each had incidence **3 → 1**.
The aggregate canopy boundary count improved 442 → 334 and therefore concealed
them. This trial is rejected, not a passing checkpoint. Its LOD2 was stopped
once the upstream defect was identified; the partial log and memory receipt
remain `build/lod-v4/station-near-v2.*` (946 seconds, 583,496 KiB peak).

The fault occurs before pruning: independently transformed source corners share
a six-decimal world-space key, but straddle adjacent FLOAT values after the
static merge. For example the top of a 0.55 m fascia edge becomes
14.429400444 versus 14.429399490 m. The contact detector then sees different
edges and cannot protect the junction. `merge_static` now chooses a shared
double-precision representative for every original world-space coincidence
**before** FLOAT storage. It reports measured corner counts and maximum movement.
The regression uses two translated panels whose independent casts open their
shared edge; the corrected merge retains the original six boundary edges with
less than one micrometer of canonicalization. Full public shared-map fixture,
including this case, passes (`shared-float-contact-fixture.log`, 16.67 seconds,
466,896 KiB peak).

The collapse also checks local edge incidence classes, so removal at an existing
three-face junction cannot create a new one-face boundary while unrelated source
boundaries disappear. Source seam membership remains movable; this does not pin
all coincident corners. The rejected trial's lower totals are retained as an
explicit example of why totals do not prove closure. The corrected component
and complete station still require their own measured rebuilds.

## Pass 34 — a storage-dependent audit was retaining unnecessary geometry

The cheap station junction component was rejected as gaining boundaries.
An independent comparison of the identical stored POSITION values found:
FLOAT arithmetic measured 64 boundaries / 56 nonmanifold edges in the source;
double arithmetic measured 74 / 46. The 140-triangle candidate measured 74 / 16
with either storage dtype. It had no additional open edge under a consistent
measurement. The false source weld came from decimal rounding performed in
FLOAT at a large placement, not a visible hole in the candidate.

The topology audit, contact keys, pin lookups and source-skin boundary keys now
evaluate stored positions in double precision before applying the unchanged
six-decimal coordinate convention. A regression compares disjoint translated
panels under both array dtypes; both must report eight edges. The full public
shared-map fixture passes (16.87 seconds, 493,376 KiB peak). This corrects the
measurement, not the structural/pixel limit.

The actual corrected junction component now keeps 480 triangles near and
**140 middle**, versus 472 middle under the false veto. Both retain 74 true
boundaries and expose zero inherited multi-face junctions. The measured inputs,
raw cheap candidate and before/after dtype counts are retained in
`build/lod-v4/station-contact-rounding.json`, `station-contact-raw-candidate.npz`,
and `station-contact-component.json`. No source delivery was changed.

The complete new station LOD1 is 9,500/18,258 (52.03%), under its 10,041 ceiling.
Individually checking all ten original failures now gives **3 → 3 incidences**,
rather than the handoff's 3 → 1. Tracking overlapping boundary segments also
finds zero unmatched segments at those junctions. The canopy totals are
442 → 318 boundaries / 130 → 95 nonmanifold edges; dispenser 128 → 128,
both nozzles 0 → 0. Those totals describe inherited source constructions,
not a claim that all source graphics are watertight. Actual-junction proof:
`build/lod-v4/station-near-v4-junction-coverage.json`.
Full LOD2 and native visual checks are still pending at this entry.

The new physical shared-map-pool fixture also passes: two independently built
kinds backed by one embedded original map resolve to one external PNG, preserve
its bytes and original GLB, and add no texture allocation. This is additional
package sharing; canonical material binding is still required in the engine.

All three original fence sources were rebuilt from unchanged scripts as
adoption prerequisites: privacy 2,100, picket 2,936, chain-link 8,588 triangles;
each finalized UV audit passes with zero overlap. These are source preparations,
not LOD adoption proofs. Original exports/bakes/checks and the frozen-tool
adoptions remain pending. The 443-file pre-existing preservation receipt passes.

## Pass 35 — distinguish true field bounds from the ranking estimate

The saturated 1,740-triangle station fascia component had 188 UV-seam and 368
hard-normal vertices, but **zero persistent pins and zero initially unavailable
vertices**. Seam membership did not freeze it. Profiling the stalled 732-triangle
result found 25,771 UV-quadric rejections after correcting an endpoint error.
The accumulated affine UV-plane estimate extrapolates gradients beyond each
incident triangle; it is a useful ranking cost, but not a valid hard UV bound
on a curved/quantized chart.

Removed that attribute-estimate veto on the seam-sliding path. Its weighted
ranking, geometric quadric prefilter, source-side vertex/face samples, progressive
95% area ledger, independent final UV/frame/color/surface audit and topology
guards remain. The legacy cone path is unchanged. The real component now reaches
260 triangles; independent validation reports UV error .83684 of its unchanged
half-mip-texel allowance, color error .000673, maximum surface error .00800 m,
p95 .00795 m and no rejection reasons. Raw and validated accessors are retained
under `build/lod-v4/station-quadric-guard-*`. This is geometric/field evidence;
full-chain native switch images still have to approve the result.

Also corrected a stale closure endpoint in reverse/updated wedge offers. A
closed thin-box regression now reaches six faces rather than eight while
preserving its exact affine per-side UV fields and closed topology. A separate
closed, hard-capped cylinder with a mildly varying monotonic UV chart reaches
38 rather than 68 triangles through the complete component validator. Its
sampled UV error is .23256 of the limit, all field/surface checks pass, and it
remains closed. A smooth rounded-box control still reaches 194/972 triangles
with both policies. The expanded public shared-map fixture passes (about 67
seconds, under 0.5 GiB child RSS). No texture, material or image-acceptance limit
changed in these corrections.

## Pass 36 — measured pins, full station reduction and adoption start

The complete station near build now yields **9,186 / 5,488 triangles**
(50.31% / 30.06% of selected LOD0). LOD1 meets its cap; LOD2 still misses
4,564. Both levels retain all ten previously failing junctions at their original
three incidences, with **zero unmatched tracked segments**. This is a measured
surface-incidence result, not an image-based inference. Fresh switch previews
and a lower `.075` middle request remain pending; the first lower trial was
canceled because it needlessly repeated LOD1. Its replacement builds just the
middle candidate directly from LOD0 at the same `.12` switch.

The exact initialization comparison below uses each implementation's actual
corner deduplication and persistent-pin rule on the same original deliveries.
Labels are **overlapping memberships of pinned vertices**, not independent
causes to add together. UV/normal splits themselves do not imply a pin.

| Persistent-pin membership | Pickup before → after | Colonial before → after |
| --- | ---: | ---: |
| Unique pinned vertices | 4,086 → 4,022 | 1,674 → 552 |
| UV-seam members | 3,425 → 3,425 | 1,335 → 551 |
| Hard-normal members | 3,226 → 3,226 | 1,380 → 552 |
| Material-border members | 48 → 48 | 0 → 0 |
| Open part-border members | 64 → 0 | 1,122 → 0 |
| Moving-part members | 380 → 360 | 32 → 8 |
| Protected-surface members | 4,022 → 4,022 | 552 → 552 |

Geometric vertices after initialization are 30,975 → 30,971 for the pickup and
31,491 → 31,379 for the colonial. These actual wedge-initialization counts
supersede the earlier rough aggregate inventory where they differ. No original
delivery bytes changed. The larger pickup obstacle was rejection of otherwise
movable vertices by the attribute estimate and source-skin guard, not tens of
thousands of literally fixed seam vertices. Receipt and executable comparison:
`build/lod-v4/pin-comparison.json`, `compare-pins.py`.

All six original pilot `make check` commands pass, with accepted generated inputs
explicitly frozen. The colonial includes 1,000 generated plans and six negative
controls; commercial includes the station and strip families. Original street
light, privacy, picket and chain-link checks also pass. Full commands and exits:
`build/lod-v4/original-checks.json` and `adopter-original-checks.json`. The fresh
CPU suite passes all 26 files; six GPU files are in progress. The rebuilt cone
keeps the accepted **626 / 436** counts; its new image/check pass is pending.

Main was merged again as `29b5cc2` after the skateboard landed; there were no
additional kit changes. Five new original gallery images extend the preservation
receipt to **476 files**, all matching. The original fence inputs were absent
and rebuilt before adoption; their newly generated maps/exports were then added
to the receipt, without refreshing any existing hash.

The recipe/tool freeze is `29b5cc2`, recorded with complete tool, rule, report,
auditor and recipe hashes in `build/lod-v4/adoption-freeze.json`. Following the
written examples produced street-light and WoodPrivacy configs plus opt-in
Make hooks in `5f1bd0a`. Privacy covers Section_A, Section_B and Gate_Bay on
one original atlas; its three 20-triangle posts deliberately stay LOD0. Builds
and native review are pending, so this entry does not claim completed adoption.

## Pass 37 — native near review, channel isolation and a literal recipe failure

Opened all three 9,186-triangle station LOD1 strips at native size in
`build/lod-v4/previews/commercial/near-v5-1/`, then the original-size worst-patch
crops in `build/lod-v4/local-controls/`. Color/value first: the fascia retains
its plum hue, the lettering stays crisp and columns/soffit retain their values.
Mean RGB is .00124–.00141 and p95 .00392. Two local tests fail (.116/.160),
entirely on thin bright lamp contours; the front local value is .0755.
The native crops show about one pixel of contour displacement, rather than a
broad emission or albedo change. LOD0-only half-pixel translations produce
.097–.125 locally; a one-pixel vertical translation produces .195–.200.
The corrected station LOD1 local limit is **.21**, with every other gate
unchanged. The new per-level limit API keeps the far local limit at .08 and
never silently drops unspecified gates. Pure tests cover that separation.

All three new far station strips were opened in
`build/lod-v4/previews/commercial/proxy-v6/`. The switch-capped chart allocation
does fix the visibly blurred RILLWAY lettering. It does **not** close the chain:
full RGB means remain .0247/.0303/.0295, with pale/speckled columns. Opened all
five independent field strips in `proxy-diagnosis-v6/` plus metalness and the
full PBR render without normals in `proxy-diagnosis-v6b/`. Base-color mean/p95/
local are .0109/.0588/.0685; roughness and occlusion pass too. Metalness misses
thin trim coverage (mean .0405, p95 .293), and normal p95 is .157. Disabling
normal maps alone still gives mean .0249/p95 .122. This rules out a blanket
albedo/color-space correction and a normals-only explanation.

A controlled fourfold atlas bake, filtered from 2048 to the same 512 delivery,
retains the same 1,798-triangle geometry. Its three native strips are in
`previews/commercial/proxy-ss4/`, all opened at full size. Local RGB now passes
.08 in all views (.0766/.0781/.0797), but global means .0206/.0242/.0246 and
p95 .124/.125/.122 still fail. This is a measured improvement, not approval.
The next envelope control has 1,762 triangles and removes voxel rounding;
its preview is pending. Both bakes stay below 2.60 GiB child RSS and ship only
512 maps. Optional `bake_supersample` preserves the default accepted grill
policy; channel-space filtering reuses the kit's downsampler as a library.

The first literal street-light recipe run gives 1,656 / 1,212 triangles.
Opened all six native strips. LOD1 passes all views with 1.96–2.37% silhouette
loss; LOD2 visibly fades the shaft, losing 13.4–24.3% coverage. At the front far
view, integrated alpha falls from 132.655 to 100.388 pixels. The retained LOD1
at that same far camera has 129.776 pixels and passes all image gates at all
three azimuths (1.89–2.17% silhouette loss). Tightening the second level's
structural allowance to .02 pixels costs 2,048 triangles, above the retained
1,656. The adoption therefore keeps one useful additional level. The recipe
now explains subpixel shaft coverage, tighter optional bounds and omitting an
unhelpful level. Its standard-prop example matches that choice. No coverage
limit was relaxed. The source-only far control and failed strips are archived
under `build/lod-v4/` and `before-policy-fix/street-light/`.

An interruption sent SIGTERM to the unfinished lower station trial and several
background dispatchers. Completed artifacts/checks survived. Subsequent jobs
are directly monitored, with one Blender at a time. The old adoption freeze is
archived; general cache and metric fixes require a fresh recipe-step-3 proof.
Source-vs-bytecode cache versions now use an import-time source receipt, tested
across three fresh CPU Blender processes including a source-edit invalidation.
The complete 32-file suite passed before these later fixes; the expanded
34-file final regression and fresh canonical/adoption proofs remain required.

## Pass 38 — projection control rejected; final reductions underway

Opened all three native `previews/commercial/proxy-nearest/` strips. Forcing
nearest-visible reevaluation does not close the station: RGB means are
.0233/.0283/.0260 and p95 .123/.137/.125. It also changes layout probes, so it
is not a projection-only control. The runtime monkeypatch remains scratch;
no nearest-first policy was added to the tool. The non-voxel 1,762-triangle
control was also opened in all three views and still fails (.0234–.0254 mean,
.114–.122 p95). Retain both negative controls rather than claiming rounding
or nearest projection alone explains the difference. A source-only independent
seed/convergence control is queued before any further metric decision.

The fourfold field-aware bake is now an optional committed implementation;
the default remains unchanged for accepted proxy policies. Seven pure filter/
report tests pass. The supersampled GPU fixture and full fresh suite remain
required. The corrected pickup near rebuild is underway with one CPU Blender;
completed large components reach their requested .4 ratios. This is not yet
an assembled-count or rendered approval.

Merged main again as `e24f45e` (main `ae3dde6`, skatepark). No kit changes came
from that merge. Five new gallery images extend the original preservation
receipt to 481 files; no existing hash was refreshed. Repository check now
passes 1,962 source files. The prior adoption freeze remains obsolete until
all general changes settle and the recipe is followed afresh.
