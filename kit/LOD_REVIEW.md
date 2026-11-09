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

## Pass 39 — converged station proxy passes; a second reduction blocker closes

Opened all four native strips in `build/lod-v4/convergence/`. Two unchanged
LOD0 renders at 128 samples differ by .0152 mean / .0784 p95; at 2048 samples
the independent-seed difference is .00330 / .0182. The original final station
policy already used 2048; the low-sample diagnostics had exaggerated the
remaining error. The new atlas still needs comparison at that final policy.

Opened all three `previews/commercial/proxy-converged/` strips at full size.
They hold source and candidate at the same 2048 samples, supplied frames and
camera. The old proxy still gives mean .0296/.0225/.0236, p95 .169/.129/.114
and local .137/.108/.148. The new 1798-triangle atlas gives mean
**.0105/.0122/.0138**, p95 **.0481/.0519/.0627**, local **.0348/.0397/.0568**,
alpha MAE .0064–.0098 and silhouette loss .0075–.0124: every original far gate
passes against LOD0. Lettering remains crisp and column values now agree at
native size. `controlled-improvement.json` measures both from the same source
render. The cause-specific fix is switch-capped chart allocation plus a
fourfold antialiased field bake downfiltered to the same 512 maps; no palette,
lighting, AO or acceptance-limit adjustment was made. The full chain still
needs a canonical rebuild and comparison with its actual preceding level.

The pickup's 1616-triangle source component exposes a second avoidable stall.
Its 646-triangle collapse passes all source-field samples; unconstrained normal
transport then breaks two edge-midpoint samples and forces a 1034-triangle
fallback. Saved source and pre-transport arrays are in `car-frame-control/`.
The bounded transport defers only **2 of 471** independently projected frames,
retains 469 and keeps **646** triangles with zero failed samples (worst UV
fraction .91450, unchanged). These deferred corners retain their interpolated
LOD0 frames, never normals recomputed from the reduced geometry. Neighboring
face checks repeat after each local reversion, with unchanged UV/frame/data
limits; final independent auditing still runs. The new analytic curved-normal
regression and the entire shared-map fixture pass. The full fresh kit suite
and all rebuilt pilot images remain required. One interrupted control received
SIGTERM; the directly monitored retry completed successfully. The long pickup
build was stopped deliberately at a cache boundary to run these controls.

## Pass 40 — frozen-tool adoptions complete, cost-driven recipe correction

Fresh adoption freeze is `3b43bcd`, with complete tool/rule/report/auditor and
recipe hashes in `build/lod-v4/adoption-freeze.json`. No kit source changed
through these builds. The street light is 3180→1656 (52.08%), one .25 level;
all three native strips, differences and both close views were opened. Color/
value and pole coverage match; worst mean RGB .00375 and silhouette loss
.02370. `make check-lod` passes. Resident chain **4.348 MiB**, including only
.1233 MiB extra mesh allocation and no extra images. The family review records
the rejected old shaft-fading level and this fresh proof as two critique passes.

The first WoodPrivacy recipe run passes every check at 664→416→248 for A/B,
712→414→230 for Gate_Bay. Opened all 18 strips and nine construction images.
Values and grain match; far close views show squared tops/board cuts that do
not read as a pop at the 97px switch. The near rows retain 58–63%, so they add
little useful reduction. The recipe now explicitly permits omitting such a
row, uses one useful .09 level in its modular example, and includes the
`shared_textures` pool field in both complete shared-family examples.

Rebuilt the three single-level configs without changing the tool. Opened all
nine final native strips/differences and six close views. A/B each keep
**37.35%**, Gate_Bay **32.30%**. All original image gates, topology, imported
geometry/pivots and normal checks pass. Gate/latch moving nodes remain, so the
bay still has three draws with one material. Twenty-triangle posts stay LOD0.
Whole family resident estimate **16.2639 MiB** = original maps once + original
container once + .0766 MiB extra meshes; no intermediate images. Both adoption
reports/contact sheets are under `build/lod-adoptions/`. Original street-light,
privacy, picket and chain-link checks were rerun and all pass. Preservation
481/481; repository 1962 sources, zero errors. Family reviews each contain two
concrete critique passes. These are rest/data and rendered proofs, not engine
performance or new swept-motion claims.

A scratch pickup diagnostic had stubbed component reduction while using the
production group-cache wrapper. Those derived group entries were purged,
along with the other group entries, before the fresh adoptions. Genuine
component cache arrays were not written by that stub and remain valid. Scratch
controls now bypass the group wrapper. No final pickup build uses those
entries; cache provenance is not silently assumed from an output hash.

The first new grill assembly is **11050 / 7544 / 1796**. Both near caps still
miss. Its 2468-triangle HoseAssembly retains accepted skin weights/vertices.
At LOD2, source-skin ordering restores 1204 triangles: measured exposed back
patches are 7.5px on the grease tray, 3.5px on the lid and 4.5px on one static
construction. This is not a visual exception yet: the lower .35/.05 request
and native fault controls remain required. The accepted 1796 proxy stands.

## Pass 41 — a converged control rejects the grill's guard as proof of a fault

The .35/.05 grill build is 10620 / 7504 / 1796. Opened all nine native closed
strips and all four construction views at 128 samples. One near local patch
is .08128 versus .08. A 512-sample preview passes all three near views, with
worst local .07959. Opened independent-seed LOD0 controls at both counts:
mean noise .00252→.00113, local .02555→.01107. The final closed 512-sample
chain passes every image gate and `make check-lod`; resident estimate 20.081
MiB. Every final image still needs to be opened after its regenerated evidence.
No image limit was changed; the 128-sample failure remains archived.

The more important negative control bypasses only source-skin restoration,
leaving genuine QEM/field cache outputs intact: **6300** triangles. At -75°
lid opening, cameras use the actual posed height at the same .12 switch,
11.48 m. Opened every 128- and 512-sample native strip. The initial rear local
.0850 drops to .07756 at 512; every image gate now passes, including the open
pose. There is a small reflection-band difference, not a sufficient visible
failure to justify retaining all 1204 restored triangles. The exported grill
material is explicitly `doubleSided: true`. The auxiliary back-face ordering
rays were therefore over-conservative here; they are not proof of a hole.
Do not report 7504 as the lowest visually passing count or claim the cheaper
control fails at final sampling.

Added a scoped `backface_guard: false` policy for a reviewed all-double-sided
source. Other sources retain the conservative default; one-sided materials
cannot disable it. Only the auxiliary ordering rays are scoped; assembled
contacts/topology and all other checks remain active. The shared-map fixture
passes new validation, nested/exception reset and still-active topology cases.
No geometric reduction code/cache fingerprint changed. The interrupted clean
CPU suite stopped after six passing files; its saved genuine reduction cache
was restored. A fresh full suite and fresh frozen-tool adopter proof are now
required after this general fix. The grill's canonical 6300 build, stronger
budget attempt and native review remain pending.

## Pass 42 — clean full suite and repeated frozen-tool adoptions

At `ab9d354`, all 34 kit test files pass from clean fixtures: 28 CPU files
(298.13 s, peak 2.74 GiB) followed by six GPU files (1731.15 s including fair
shared-GPU queues, peak .941 GiB). Source hashes and every exit code are in
`build/lod-v4/regressions/`. The actual supersampled proxy fixture and supplied
shading-frame import/bake/repair/re-import fixture pass; the latter's maximum
vector error is .00001453. Interrupted earlier attempts are superseded by this
complete run.

Repeated both adoptions against the frozen `ab9d354` tool, without tool changes:
street light and all three WoodPrivacy configs rebuilt, rendered, and passed
plain `make check-lod`. All four delivered glTF payload hashes match their
previously reviewed builds. Raw PNG hashes differ because Blender includes
render metadata; decoded reference/level pixels for all 18 fence far-view
images are exactly identical (zero changed pixels), recorded separately in
`adoption-refresh-pixels.json`. Opened all eight refreshed construction views:
unchanged light shaft/fixture; unchanged wood value/grain, with the previously
recorded squared tops and simplified hinge bevels only apparent close up.
The native switch evidence and costs remain those of pass 40. All four original
adopter checks pass again after this refresh (41.21 s, peak .789 GiB).

The new canonical grill mesh is 10620 / 6300 / 1796; its prior renders still
belong to the 7504-triangle middle level. Fresh canonical render/check and the
stronger budget/fault control are required before treating it as a final chain.
Pickup and colonial proxy/near work is still in progress. No incomplete pilot
is approved by the completed suite or adopter results.

## Pass 43 — exact lock inventory and rejected pickup controls

Merged the later playground main, `4714b3a`, as `a882a31`; no kit code changed
in that merge. The original 481-file preservation receipt still passes, then
appended the five newly merged playground gallery files: 486 protected files.
The complete pass-42 suite and frozen adopter code remain current.

Completed the handoff/current inventories using identical source components.
The persistent-pin comparison stops immediately after pin initialization; the
offer comparison builds the exact initial heap with ratio 1, without reducing.
It now includes every small unskinned component and the correct geometric
remap for retained skins. Receipts: `build/lod-v4/pin-comparison.json` and
`lock-comparison.json`. Counts below overlap across causes; they cannot be
summed. A UV seam or hard normal is a field constraint, not automatically a pin.

| Cause | Pickup persistent before → after | Colonial persistent before → after | Pickup L1 unavailable initial offers | Pickup L2 unavailable initial offers | Colonial L1 unavailable initial offers | Colonial L2 unavailable initial offers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| UV seams | 3425 → 3425 | 1335 → 551 | 7220 → 3622 | 4979 → 3465 | 3767 → 973 | 2733 → 555 |
| Hard normals | 3226 → 3226 | 1380 → 552 | 6719 → 3327 | 4591 → 3266 | 3816 → 974 | 2781 → 556 |
| Material borders | 48 → 48 | 0 → 0 | 48 → 48 | 48 → 48 | 8 → 4 | 8 → 0 |
| Part borders | 64 → 0 | 1122 → 0 | 64 → 0 | 64 → 0 | 1122 → 144 | 1122 → 0 |
| Moving parts | 380 → 360 | 32 → 8 | 2143 → 360 | 1028 → 360 | 80 → 24 | 32 → 8 |
| Protected shader surfaces | 4022 → 4022 | 552 → 552 | 4022 → 4022 | 4022 → 4022 | 552 → 552 | 552 → 552 |
| Unique total | 4086 → 4022 | 1674 → 552 | 8584 → 4232 | 6164 → 4062 | 4871 → 974 | 3812 → 556 |

Fresh pickup near meshes with the current reducer are 38020 / 31388. Opened
every `build/lod-v4/previews/cars/guarded{1,2}/` native strip. Body coverage is
intact, but the grille reflection moves; L1 local errors .1854/.1862/.1122
and L2 rear .0827 remain failures. This is not final acceptance.

The whole-source skin fallback is another substantial restriction beyond pins:
it adds 6438 / 8312 triangles to raw 31582 / 23076 candidates. Opened all six
`unguarded-near{1,2}` strips: disabling the auxiliary guard creates black body
triangles, visible even at the .10 switch. All source materials being double
sided is insufficient to approve that control. Removing shader protection from
a scratch source, then restoring the exact source shaders/maps before rendering,
reaches 26576 / 16712. Opened all six `protection-near{1,2}` strips: it also
damages body coverage and the powered lamps. Rejected both controls.

CPU pixel-ray probes identify a front-fender coverage miss of 2.554 pixels,
beyond the nominal two-pixel maximum. The existing reverse surface audit samples
source vertices; source face interiors can escape it. A control adding face
centers/edge samples increases one fender from 532 to 612 or 784 triangles,
but isolated skin ordering still fails. The full-vehicle fender-only control
looks correct at all three native angles because other original parts occlude
it. That closed rest pose does not prove an isolated moving assembly safe.
Restoring the reference occluder before the exposed component gives exactly the
same 38020 / 31388 totals; it is not an improvement. A local-anchor experiment
also failed to converge in its four completed iterations and was stopped.

Opened all nine proxy channel-control strips. Removing emission worsens the
front mean from .0350 to .0403; removing transmission gives .0955, and removing
both .0910. The latter two visibly whiten the windshield. These controls reject
a blind emission scale or transmission removal as the color fix. The unmodified
SS2 proxy remains a failure, with the front worst patch too bright and a rear
patch too dark. Material/coverage probes are pending.

The 4950-triangle forced grill control retains the original maps, pivots and
skin, but forcing its rigid geometry down with ordinary collapse makes missing
panels and diagonal shards visible at the .12 switch. Opened all three native
strips in `build/lod-v4/previews/gas-grill/forced4950/`; mean errors are
.0764/.0657/.0501 and silhouette losses .1602/.2200/.2180. This is a rejected
target-count control, not proof that no valid reduction can reach 4978.

One duplicate reverse-coverage control was inadvertently launched after its
first successful run; it ran for 169 seconds before being stopped. The first
successful receipt is preserved separately. It did not change source files or
production caches. Every controlled cache entry used here has genuine reducer
inputs and outputs; no stub result is stored under an original key.

## Pass 44 — finer skin retries and projection-field diagnosis

The exact reducer can keep useful reductions of failed skins. Isolated controls
pass at door 194/432, hood 436/792, front fender 836/1520 and bumper 974/1500;
the immediately cheaper tested densities fail the same three-pixel ordering
guard. An assembled control starts from the conservatively restored mesh,
retries only implicated components at finer densities, and tests the entire
assembled mesh after each replacement. Every retry retains the original UV,
normal/tangent, color, topology and surface bounds. Genuine component caches
use the actual changed ratio. No modified geometry is stored under a raw key.

The resulting scratch pickup is **33816 / 25166** triangles, **56.51% / 42.06%**
of LOD0. Source-skin overhead falls from 6438/8312 to 2234/2090 triangles over
the raw candidates. Build exit 0, 2963.44 s including queue, peak .633 GiB.
This is a method control under `cars/build/lod-v6-skin-backoff/`, not a change
to the production tool or an approved chain. Native three-angle proofs are
queued. Both goals are still missed.

Traced the actual near worst patches with independent double-precision native
pixel rays and decoded the supplied material fields. The glass normals match
to about .0000015 degrees. The front/three-quarter patches are mostly metallic
opaque surround, with roughness about .16–.23. At the three-quarter patch,
unfiltered decoded normal directions differ by 5.02 degrees median and 41.05
degrees p95. These point samples describe the delivered fields, not a filtered
pixel normal AOV. Moving a bevel changes which part of that field the camera
sees, even when individual transported vertices meet their source bounds.
A tighter-geometry metallic-surface control is queued, with a .25 base ratio
to leave room for those bevels. The source-UV frame control also awaits review.

Superseded the early Blender pixel probes with F64 analytic camera rays.
Transforming a 1 mm near-clip point into a scene tens of meters away loses
precision in float storage; rotate the ray direction before adding translation,
or form the pinhole ray directly. New receipts are
`build/lod-v4/car-near-material-probe-exact.json` and
`car-proxy-material-probe-exact.json`. The older probes remain useful geometric
counterexamples, but are not the exact pixel correspondence evidence.

At the canonical pickup's front worst patch, source paint has mean base
(.0123,.0372,.0713), zero emission and zero transmission. Proxy point samples
on those source-paint pixels have base (.1084,.1313,.1571), emission roughly
(5.08,5.68,6.11) and transmission .282. Rear paint samples keep their original
color closely. That rules out a global color-space or palette correction.
Surface-field association/coverage and the source-consistency of emission
repair need testing: the existing position repair changes other channels while
excluding emission. A same-geometry SS4 baseline and consistent-emission control
are queued; no speculative emission tint/scale has been adopted.

Rejected the new .25-pixel proxy deflation before baking it further. Independent
first-hit orientation at every native pixel finds pickup reversed first hits
120/260/261 versus canonical 0/16/9, and colonial 11/9/54 versus canonical
0/0/1. One windshield ray exits before entering its thin layer, separated by
only .675 mm. This is a measured ordering defect, despite clean edge counts
and positive total volume. It is not a fix for color. Pending bake jobs on
those trial geometries were cancelled before Blender launch. New SS4 controls
reuse the existing non-deflated 2800/1798-triangle geometries. The sparse
canonical reversed hits remain a limitation to inspect, not an intersection-free
claim. An installed Cycles/glTF sidedness control is also queued.

Clarified the adoption recipe's street-light paragraph: `.02` belonged to the
rejected far-level control, which cost 2048 triangles. The delivered one-level
1656-triangle config uses the default allowance. No production kit code changed
in this pass. Preservation remains **486 files, zero changes**. Fresh frozen
adoption proof will follow any eventual general tool fix.

## Pass 45 — integrate bounded skin retries

Integrated the finer-skin path in `lod_shells.py`, scoped from the shared-map
builder. Failed construction skins try genuine denser component reductions
before whole-source restoration. The UV, normal/tangent, color, distance and
topology bounds remain unchanged; every trial checks assembled visibility.
An optional `reflective_surface_pixels` cap selects source components using
their original linear ORM fields and factors. The raw reducer is unchanged,
so its exact content caches remain reusable. No near image or material is added.

The integrated `test_lod_shared.py` run passes, including the actual bounded
reducer fixture: source 192 triangles, invalid coarse candidate 12, valid refined
candidate 38, rather than restoring all 192. ORM wrap/filter/transform and policy
reset cases pass, as does topology repair with the backface guard disabled for
explicitly double-sided materials. This is correctness evidence, not approval
of the queued native appearance controls. The complete clean suite must still
be repeated after the final tool changes.

The old-module colonial baseline finished LOD1 at 24949/58232 (42.84%), then
continued through LOD2's construction pieces. Stopped that process with SIGTERM
so pending GPU controls could run; its completed exact component caches were
preserved. A fresh-module build reused LOD1 immediately and resumed LOD2.
Its runner yields this cache-backed CPU work when the shared GPU becomes
available. Direct nonblocking lock checks show the GPU is occupied outside our
process namespace; the local process listing alone does not prove it is free.
No cancelled build is reported as a complete proof.

Current preservation check: 486 original delivery/docs files, zero changes.
Repository check: 1996 source files, zero errors. Proxy color, grille reflection,
final budget selection, final chain rebuilds and frozen-tool adoption refresh
remain pending; the earlier adoption and full-suite receipts are stale after
this general tool change.

The fresh colonial near build now completes: **24949 / 13218** triangles,
**42.84% / 22.70%** of LOD0, meeting both caps. Six inherited materials and ten
draw calls per near level; zero new intermediate image hashes. Peak child RSS
656236 KiB. This scratch near-only manifest excludes the final proxy and is
not the final whole-chain cost or render proof.

All ten original `make check` commands pass with their accepted generated
inputs frozen. The clean **28-file CPU kit phase passes**, peak child RSS
2848364 KiB; source hashes remained unchanged and the production cache was
restored. Its shared-map fixture includes the new clean refinement directory.
The six GPU files and final frozen-tool adoptions still need fresh runs.
Station LOD1 has reached 9130/18258 (50.01%), below its cap; LOD2 is pending.

## Pass 46 — native UV-frame control and measured canopy closure

Color and value: the pickup UV-frame control keeps the original dark paint and
lamp values at the .25 switch. The visible residual is a localized bright
reflection around the grille, rather than a general color shift. Opened all
three native `build/lod-v4/previews/cars/uv-exact/1-{0,55,145}-strip.jpg` files.
The corrected source-UV frame control still has local errors
.18538/.18619/.11219, with means .00189/.00202/.00173. It does not close the
reflection failure and is not adopted. The tighter reflective-geometry control
still needs its native review; no image limit is changed here.

The fresh station near build is 9130/5388 triangles, 50.01%/29.51% of selected
LOD0. The first cap passes; the second misses by 824. A .075-density control at
the same .12 switch is in progress. The exact junction audit tracks all ten
previously unmatched canopy junctions by both incidence and spatial overlap.
Each has three incident faces again at both near levels; **zero of ten remain
unmatched**. This closes the reported ten-edge failure without claiming that
all of the source's construction boundaries are watertight. Receipts:
`build/lod-v4/station-near-v5-junctions.json` and
`station-near-v5-junction-coverage.json`.

The colonial's independent serialized normal/UV audit passes on both new near
meshes. Maximum normal difference is .019783 degrees at both levels, p95 zero;
maximum UV error is .99593/.99798 of each applicable half-texel allowance. These
are source-field measurements, not native appearance approval.

The grill's wider-surface control completes at 6144 triangles (30.86%), still
above 4978, versus the current 6300. It has no new maps. Its native review and
the separate feature-pruning control remain pending. The accepted 1796-triangle
proxy is unchanged.

Several queued control drivers received SIGTERM while the first GPU control
completed. Completed native images and exact component caches are intact.
Restarted only unfinished work after checking processes and receipts; an
interrupted partial build is not reported as a successful control. The shared
GPU queue still governs all bake/render work and own Blender work stays serial.

## Pass 47 — one-sided render correction and SS4 proxy comparison

Color and value: the canonical-geometry pickup SS4 proxy still makes the front
lamp area too bright and loses dark rear trim contrast at its .04 switch.
Opened all three native `build/lod-v4/previews/cars/proxy-canonical-ss4/`
strips. Mean errors .03547/.02013/.02342, p95 .13725/.08627/.10980,
local .21553/.23459/.15999; coverage metrics pass. Higher sampling alone does
not close this color failure. No palette, gamma or image-limit adjustment is
adopted. A source-consistent emission repair is baked and awaiting native review.

An original emissive-quad control measures imported one-sided front/back alpha
as 1/1 in the installed Cycles renderer, despite its viewport culling flag.
That violates [glTF one-sided visibility](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#double-sided).
The temporary shading adapter now wraps one-sided material outputs with a
transparent back-face branch; double-sided materials keep their response.
The new actual Cycles fixture passes front/back/double-back alpha **1/0/1** and
idempotent restoration. Opened all three original and all three fixed 64px
renders. The first fixed-test attempt stopped on a PNG fixture-reader error,
then passed after using PIL for Blender's filtered PNGs. Source/export bytes
are untouched. This is a render-correctness fix, not the proxy color fix.
Render receipts now include the shading-adapter hash. Full regression/adoption
receipts must be refreshed after this general change.

Station density .075 reaches 4750 (26.02%); .04 reaches **4614 (25.27%)**,
50 above its 4564 cap. Both keep the .12 switch and original maps/bounds; neither
has native appearance approval yet. The grill SP1 control remains 6144 pending
its review, and the feature3 control is still processing. The accepted grill,
cone and maple far constructions remain unchanged.

The canonical-geometry pickup SS4 bake completed at 2800 triangles and 512 maps,
peak child RSS 2554308 KiB, about 150 s of work after its GPU queue. Another
queued parent driver received SIGTERM while its completed bake receipt remained
intact. Switched remaining GPU work to direct, individually polled jobs and
stopped the idle follow-up driver to avoid duplicates. Reused only completed,
verified outputs, not interrupted partial builds. Latest preservation remains
486 files/zero changes; repository check 1996 source files/zero errors.

## Pass 48 — station quarter cap and pickup grazing-layer diagnosis

Color and value: opened all three station `build/lod-v4/previews/commercial/mid002/`
native strips. At the unchanged .12 switch, the 4542-triangle candidate retains
the fascia value, lettering, roof, posts and dispenser coverage. Mean errors
.008567/.007105/.005077, p95 .070588/.043137/.035294, local
.056924/.053554/.036301; alpha and silhouette gates pass unchanged. This is
24.88% of selected LOD0. Adopted the .02 request in the canonical config; the
previous 5388-triangle middle level is superseded. LOD1 remains 9130 (50.01%).
The ten-junction audit must also be repeated on this selected middle mesh.

The pickup's reflective-cap control fixes the frontal grille reflection:
local .058068, down from .185. Opened all three native `reflective-geometry`
strips; az55 and az145 still fail at .124959/.112173. Exact double-precision
pixel rays identify a grazing hood layer change at az55: the candidate's
underside faces the camera where LOD0 exposes the top. Both faces are front
facing, so the auxiliary back-face sampler cannot certify this case. Restoring
only the original 792-triangle HoodMesh in place of 376 reduced triangles gives
34398 total. All three `hood-source` strips were opened: local errors
.058068/.050073/.112173. The first two pass; the remaining patch hits the
opposite front rim, whose .30196 median roughness just misses the .30 optical
classification. A .35 classification control is pending. No blanket wheel
retention or normal-map gamma change was made.

Added explicit `source_geometry_nodes` for measured exceptions of this kind.
It retains selected construction geometry and its frame/materials/maps while
letting other instances reduce. The real serialized fixture passes: one of
two shared-mesh moving instances keeps all original arrays and topology;
its twin remains reduced, with its own canonical frame. Unmatched patterns
fail. This does not claim that a visibility sampler proves all thin-shell
ordering, nor does it hide the added triangles in a seam-lock inventory.

The unchanged grill hose measures 2468 triangles. Wider-surface and feature3
controls are 6144/6214 versus standing 6300; native review is pending. The
1796-triangle accepted proxy is retained. The colonial near chain measures
24949/13218 (42.84%/22.70%); independent original UV/normal audits pass.

## Pass 49 — native pixel-phase calibration and proxy field controls

Opened all eighteen native strips under `build/lod-v4/source-pixel-controls/`.
They compare immutable LOD0 with itself at the same switch, lights, maps and
seed, moving the film horizontally by a measured half pixel only. At the house
.045 switch, frontal mean/p95/local are .01713/.09020/.06549. Thus the generic
.08 p95 rejects an unchanged house solely from subpixel trim alignment. Rear
controls are .00630/.03529/.02731. The SS4 house proxy, also opened at all three
native views, is .02593/.10980/.07079 front; coverage and local gates pass.
A .75-pixel source-only control is queued before choosing a scoped correction.

The pickup far source-only controls reach only .01059 mean and .05839 p95,
with worst local .05580 across its views. Its SS4 proxy remains visibly brighter
at the headlamps and differs around rear trim/windows: .03547/.02013/.02342
mean and .21553/.23459/.15999 local. Pixel alignment does not explain this
failure. Neither consistent primary emission repair nor a surface-density2
atlas control improves it; both are rejected. One-field-at-a-time normal,
coat, emission, transmission and occlusion controls are queued to isolate the
transfer failure. No proxy color gate is waived.

At the pickup near switch, a half-pixel unchanged-source shift reaches local
.15051 front and .08789 rear, despite matching material response. Native
appearance still distinguishes a harmless edge shift from the hood's wrong
surface layer. No near limit has been changed on this evidence alone.

## Pass 50 — selected canopy junctions and complete resident storage counts

The selected station chain now has measured closure at both near levels:
9130/4542 triangles. The same ten old valence-three junctions that became open
at handoff have three incident faces again in each selected mesh. Spatial
tracking finds **zero of ten still unmatched** at both levels. Whole-canopy
boundaries are 442 in source versus 298/274; nonmanifold edges 130 versus
97/42. This closes the ten reported failures without claiming that the whole
construction is watertight. Receipts: `build/lod-v4/station-near-v6-junctions.json`
and `station-near-v6-junction-coverage.json`.

Added a measured whole-chain storage table to the report and README output:
all default stored mesh triangles, canonical material resources, stored
primitive placements, distinct payload bytes and resident GPU estimate.
Full immutable source containers count once across modular kinds. Active draw
calls are stated separately; resident alternatives are not drawn simultaneously.
The actual-file fixture passes with two source meshes, one additional source
instance and two independently selected module chains: four stored mesh
triangles, two canonical materials, five stored placements, and the measured
filesystem bytes. All five report unit tests pass. The final clean suite still
needs its complete refresh.

Merged school/minigolf main `380a67f` as `27e55e1`; no kit code changed there.
The original 486 protected files remained unchanged; the receipt now also
covers ten newly merged gallery images, 496 total. Repository check: 2095
source files, zero errors. The recipe now explains that requested ratios must
remain nonincreasing even for an absolute-budget proxy. The station's .02
middle request requires a proxy request no greater than .02; its corrected
.01 request retains the same 1800 absolute budget. All ten canonical configs
pass configuration validation.

The pickup density control finishes LOD1 at 35212 (58.85%), only 756 below
the 35968 control including the original hood. Its middle level is pending.
This remains a scratch .35 optical-classification control, not an adopted
production chain. A source receipt shows a 1992-triangle construction retained
without a collapse attempt by whole-component powered-source protection.
A triangle-local protection control is queued, keeping existing glass and
emissive masks and all UV/frame/topology/visibility checks.

Source optical-receiver UV measurements also expose a far-atlas sampling gap:
all 1772 glass faces exceed the ordinary 22.03 texels/m switch cap; the frontmost
784 glass faces have p05/median/p95 densities 194.75/219.25/221.87 texels/m.
The existing high-frequency class excludes transmission receivers. A control
adds them to its four-texel/pixel cap (about 88 texels/m), within the same 512
atlas. No production layout change is adopted before native review.

The shared GPU lease remained unavailable outside this process namespace for
almost three hours. A read-only descriptor audit found no leftover own holder.
The CPU runner yielded with genuine completed caches intact when a lease
became available; queued native reviews have begun. No interrupted build is
reported as a successful chain and no image gate is waived by the wait.

## Pass 51 — native reductions, individual proxy fields, and house phase limit

Opened the 512-sample native pickup LOD1 strips at all three azimuths under
`build/lod-v4/previews/cars/density012/`. The 35212-triangle result passes the
unchanged image limits: mean .00142/.00185/.00193, local
.05805/.04310/.06271. Grille highlights and the original hood skin remain
consistent. Production now uses the tested .35 roughness classification,
.125-pixel reflective cap and explicit original `HoodMesh`. The 25648-triangle
middle control still awaits its own native review; its count alone is no pass.

Opened all six colonial near strips in `previews/houses/near-v5/`: garage
panels, roof, siding and window construction remain readable at their true
switch sizes. Both counts meet the requested caps (24949/13218). The middle
rear local metric is .08589 versus .08; near source-only controls are queued
before any scoped correction. Opened both grill middle controls at all three
azimuths: 6144 and 6214 triangles. The lower count retains the hose, frame,
lid and wheels; its front local .08805 narrowly fails. The 6214 control has
worse side/rear local errors, so it is not preferred merely for its count.
The 6144 setting is selected provisionally, pending source phase and open-lid
checks. The accepted 1796-triangle grill proxy remains unchanged.

Opened all six .75-pixel unchanged-house controls under
`source-pixel-controls075/houses-3/`. Front mean/p95/local reach
.02472/.12549/.09585 with identical maps, geometry and lighting. At 49 pixels
high, aligned bright trim alone makes the previous generic mean/p95 limits
reject immutable LOD0. The SS4 proxy's native front .02593/.10980/.07079 is
comparable and its silhouette/alpha pass. Set only the house far level to
mean .03, p95 .13 and local .10; all other metrics and levels keep their own
limits. This is a switch-size phase correction, not a global color tolerance.
The atlas uses the tested 1/4 density caps and 4x bake, with no new near maps.

Opened all 21 single-field-removal proxy strips in `proxy-field-controls/`.
Removing base normals, coat normals, both, emission, transmission, coat or AO
does not produce an acceptable pickup. AO removal is numerically identical
to baseline. Transmission removal makes broad pale window/lens patches;
emission removal turns the lamps off. No such omission is adopted. A
transmission-receiver density control improves front mean from .03547 to
.02954, but local .17559/.21062/.15803 still fails. It is not a color fix.
Its alpha errors are **identical** to baseline (.02232/.02200/.02340): an
earlier scratch interpretation misread the decimal, and is withdrawn.
Geometry, normals and material settings are also unchanged. Additional
light-free shader-input comparisons are queued to distinguish field transfer
from lighting response. No pickup proxy color exception is granted.

## Pass 52 — powered-neighbor scope control and refreshed original checks

The triangle-local powered-neighbor control completes at 23502 triangles
(39.28% of pickup LOD0), versus the 25648 whole-component control. Peak child
RSS is 648720 KiB. It retains the original alpha/glass/emissive masks and all
UV/frame/topology and visibility checks. A formerly fixed 1992-triangle
construction first reduces to 624, but the visibility guard rejects those
densities through 918 and accepts a finer 1210. The result is not simply an
unprotected lamp assembly. Receipts and exact control code are under
`build/lod-v4/car-local-power-control*`; native review is queued before any
production policy change. A corresponding near control and separate pin
inventory are also queued. No target exception is justified by this count.

The original cone, grill, pickup, colonial and maple `make check` runs pass
with accepted generated inputs explicitly frozen. The station check is still
running. Full exact commands and exits are persisted in
`build/lod-v4/original-checks.json`. All 496 protected delivery/docs files still
match, and the repository check reports 2095 source files, zero errors.
The shared GPU is queued again; no pending native comparison is reported as
passing. An additional optical-density control follows the measured partial
improvement at cap4: cap8 for optical/graphic receivers and .5 for ordinary
surfaces, retaining the same 512 atlas. Its result is still pending.

## Pass 53 — measured pin savings and independent candidate audits

The local powered-neighbor near control finishes at 33260 (55.58% of LOD0),
350 triangles above the requested cap. Changing only its reflective allowance
from .125 to .15 switch pixel gives 33100 (55.32%), 190 above. A .20 control
is running to test a cheaper candidate against the actual reflection fault.
None is adopted before native review. Geometry/re-import and independent
source UV/normal audits pass for the .125 near and 23502 middle controls:
maximum normal errors 2.716/2.381 degrees, p95 zero; maximum UV errors
.99179/.99488 of the unchanged half-mip-texel bound. These prove source-field
and serialization bounds, not visible acceptance.

The candidate pin inventory now separates the powered-scope savings from the
paired-seam changes. Counts below are overlapping fixed geometric vertices;
they are not exclusive cause totals. Original hood geometry restored after
reduction is a separate measured cost.

| Pickup cause | Handoff | Candidate near | Candidate middle |
| --- | ---: | ---: | ---: |
| UV seam | 3425 | 1950 | 2044 |
| Hard normal | 3226 | 1688 | 1776 |
| Material border | 48 | 4 | 4 |
| Part border | 64 | 0 | 0 |
| Moving part | 380 | 360 | 360 |
| Protected source surface | 4022 | 2196 | 2302 |
| Unique fixed vertices | 4086 | 2196 | 2302 |

Colonial fixed counts remain UV 1335→551, normal 1380→552, material 0→0,
part 1122→0, moving 32→8, unique 1674→552, at both near switches. Receipts:
`build/lod-v4/pin-comparison-local.json` and its measured Markdown table.

All six pilot and four adopter-family original checks complete successfully.
The fresh clean CPU kit suite also completes with all 28 files passing and
peak child RSS 2858132 KiB. Its completion receipt is newer than the recorded
run start, and every captured kit source hash matches. An earlier progress
message mistakenly read an older completion receipt while the new suite was
running; that claim was corrected before this verified completion. Helpers
now record run starts and the monitor gives live wrappers precedence. The
six GPU test files and final frozen adoption proof are still pending.

## Pass 54 — source phase, real lens contact, and unchanged proxy failure

Opened all eighteen native strips under `source-pixel-controls-near/`: both
.75-pixel film shifts at all three views for grill LOD2 and house LOD1/2.
The unmodified surfaces retain color and construction while their bright
contours alone exceed generic local limits. Source local maxima are
.08409/.10650/.09038 respectively. Selected candidates are .08805/.10721/
.08589. Scoped local bounds are .09/.11/.095; other near metrics remain.
The grill source control reaches alpha .05041, but the candidate is .022–.024,
so no alpha relaxation is needed or made. The new grill open-lid proof is
queued at the original rest-bound switch distance, not a farther posed bound.

Opened all native pickup .125/.15/.20 local-protection near strips and both
whole-component 25648 and local 23502 middle sets. Near counts are 33260,
33100 and 32508; the last meets 55%. Grille, hood and rim reflections remain
close, but all three local near controls lose a small red rear reflector
region, local .08713. The diagnostic native crop and fourfold explanatory
crop are `previews/cars/local-power-near/worst-patch.jpg`; acceptance still
uses the full native strips. This is a material loss, not a phase exception.

Double-precision geometric layer rays locate the source's 92-triangle opaque
insert at the same z=-2.875 plane as the glass back. Its 42-triangle reduction
moves that face approximately 80–90 micrometers deeper, past the interface.
The glass itself is unchanged. This is a straight geometric layer diagnostic,
not a refraction simulation; the native render independently shows the loss.
Added sampled opposed transmission contacts to local protection. It pins source
opaque triangles where their vertices/centers meet the lens surface within
the established micrometer convention, and reports measured distances and pins.
The meaningful fixture keeps a real contact while rejecting a separated panel
and a same-facing sheet. The complete shared-map fixture passes. Default
whole-component behavior remains unchanged. The public builder's repaired
near level measures 32612: 104 triangles above the faulty 32508 control and
still below 55%. Middle build and repaired native review are pending.

Opened all six light-free shader-input strips and all three optical-cap8
native strips. BaseColor/transmission inputs retain the broad source fields;
the emission-input comparison intentionally differs because the proxy carries
transmitted emission while the diagnostic source glass is opaque. It cannot
be read as a radiance error measurement. Cap8 plus ordinary .5 yields means
.02987/.01914/.02451 and local .16969/.19454/.15792: still a clear failure.
Cap4 is the better all-view allocation control, but also fails. No car far
color limit is changed. A same-layout 1024 filtering control is queued solely
to test texture capacity; it is outside the delivery budget and cannot ship.

Merged coffee-shop main `941c8c0` without kit changes. The previous 496 protected
files remain identical; append-only protection now also covers its five gallery
images, 501 total. Repository check: 2134 source files, zero errors. The full
kit suite must refresh after the new local/contact features; only their complete
shared-map fixture has been rerun so far. Fresh recipe adoption is still pending.

## Pass 55 — contact repair verified and native phase calibration

Opened all six LOD0-only pickup middle-switch strips under
`build/lod-v4/source-pixel-controls-car-mid/cars-2/` and all three contact
candidate middle strips under `previews/cars/contact-2/`, at native size.
Value and hue remain close. The unmodified .75-pixel shifts reach local
.11632; 23530 triangles reach .08324. Scope the middle local bound to .12;
mean, p95, alpha and silhouette gates remain. The near 32612 level restores
the rear red insert, passes all unchanged gates, and meets 55%.
The middle remains above 25%; source-static geometry accounts for most of its
cost. A real cheaper contact-only control is queued, retaining original glass,
alpha/emission surfaces, source hood, contacts and all independent field gates.
Saturation alone is not claimed as an exception.

Opened all three grill 6144-triangle lid-open strips at the original rest-bound
12% switch (8.16 m), not the farther posed-bound distance. They pass the scoped
.09 local and unchanged other gates: worst local .07590, alpha .03734,
silhouette loss .04241. The previously reviewed forced 4950 control remains
rejected for its rest-view missing panels/shards; a lower count is not accepted
merely because its open-lid pose happens to look similar.

Opened all three same-layout 1024 pickup proxy strips. It is a diagnostic only,
outside the 512 budget. Means .02750/.01823/.02139 and local
.15677/.18688/.13971 still fail, ruling out capacity alone as a sufficient fix.
Opened the two linked-normal shader-input strips: paint-interior median direction
errors are 3.16 and .45 degrees, with p95 17.50 and 12.04 degrees. These are
pixel-averaged direction comparisons including correspondence and remaining
edges, not proof of a unique baker defect. A tighter .25/.15 voxel/inflation
proxy measures 2794 triangles and is queued for native review, alongside a
source-point material-field control. No far color limit has been changed.

## Pass 56 — fresh fixed-vertex inventory and accepted cone retained

Recomputed the same-source pin inventory with the public local/contact policy
and the actual separately retained hood. Counts below overlap: a fixed vertex
can be on a UV seam and a hard-normal edge. Moving means fixed vertices in a
moving mesh, not a rule that freezes every moving vertex. The full JSON also
keeps source constraint membership distinct from persistent pins and initially
unavailable collapse offers.

| Cause | Pickup handoff | Pickup L1 | Pickup L2 | Colonial handoff | Colonial L1/L2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| UV seam | 3425 | 2005 | 2099 | 1335 | 551 |
| Hard normal | 3226 | 1743 | 1831 | 1380 | 552 |
| Material border | 48 | 30 | 30 | 0 | 0 |
| Part border | 64 | 0 | 0 | 1122 | 0 |
| Moving part | 380 | 394 | 394 | 32 | 8 |
| Unique fixed vertices | 4086 | 2257 | 2363 | 1674 | 552 |

Receipt: `build/lod-v4/pin-comparison-final.json` and `.md`. This inventory is
before pruning/reduction, not a sum of repeated trial records. Source-hood
restoration is a separate measured cost: 792 source triangles replace 408/482
reduced triangles (384/310 additional triangles). Later source-skin refinements
are also separate: for example, pickup middle static geometry goes from
13540 to 16086 under the sampled visibility guard. These costs are not hidden
inside the seam-pin counts.

The frozen-source clean CPU suite completes: 28/28 test files pass, all source
hashes match, fresh completion follows the recorded start, peak child RSS
2883864 KiB. Six GPU files remain pending. The recipe freeze covers all 102
kit source files and the literal recipe; fresh adopter outputs are separate
from their archived previous runs.

Opened all six fresh canonical cone native strips, its three construction
views and contact sheet. Color/value, broad stripe placement and ground contact
remain consistent with LOD0. LOD2's faceting is visible in the deliberately
closer construction view but does not pop at its unchanged 9% switch. Counts
remain the accepted 626/436; all native image gates pass. Its independent final
check is queued, not inferred from its renderer result.

The source-point/512 control is now reviewed at all three native views. Means
.03205/.01920/.02071 and local .20989/.18634/.11385 do not fix the front;
the lamps are brighter. Reject this control. Canonical far settings now use
the previously reviewed better all-view optical-cap4 SS4 allocation (1/4 caps,
including mapped transmission). Its known color failure remains explicit; the
tighter-geometry comparison is pending. No far metric is relaxed. This is a
configuration change under the frozen tool, not a new adoption tool revision.

## Pass 57 — native grill chain and pickup far controls

Opened all nine fresh canonical grill strips, four construction views and the
contact sheet. The chain is 10620/6144/1796, and its complete `check-lod` passes
both geometry/re-import and the independent UV/frame audit. Values remain dark,
metal highlights roll across the same surfaces, and the hose loop, wheels and
support frame read consistently at their switches. The middle construction
close-up exposes faceted fittings and a lid-trim discontinuity; those are real
limitations at that deliberately closer camera, not hidden by a metric. The
native 12% strips retain the silhouette and construction. Its local maximum is
.08805 under the source-phase-calibrated .09 bound. The already reviewed forced
4950 rest-view control remains the cheaper visible-fault witness. The accepted
1796 proxy remains; its close-up is visibly coarse and blurred, while all three
3% switch strips pass. No proxy budget exception is reopened.

Opened all three 2794-triangle tight pickup proxy strips at their native 4%
switch. Alpha errors improve to .01538/.01829/.01838, but color does not:
means .03350/.02021/.02240, local .19191/.21734/.18446. Front lamps and rear
trim still differ; reject it in favor of the previously measured optical-cap4
baseline. Geometry coverage alone is not a sufficient fix.

Opened all six measured .75-pixel LOD0-only pickup far controls. Their maxima
are mean .01515, p95 .07548 and local .07863: all stay inside the existing color
limits. Thus the far proxy's color failure is not explained by pixel phase,
and no far color limit is changed. A source control's silhouette loss reaches
.05136, but the proxy's coverage already passes, so that does not justify or
require changing a silhouette limit either.

The public double-sided middle control measures 20608 and passes independent
geometry/re-import and source UV/frame correspondence: max normal 2.381 degrees,
p95 zero, max UV error .99489 of its own half-mip-texel bound. Its native review
is pending. The tight proxy's audit passes its new cage and normal-map validity;
that audit does not approve baked appearance or require its new geometric
normals to match LOD0. A nearest-compatible point-field control is queued to
isolate source association from the earlier ray-first point-field control,
using identical geometry, UV allocation, shipping size and controlled baker.
No production source or frozen recipe changed for that diagnostic.

## Pass 58 — first frozen-tool adopter reviewed

The fresh street-light build retains 1656/3180 triangles (52.08%), three materials
and three draws per level, with no new image content. Whole-chain resident
memory is 4.348 MiB under the documented block/mip estimate. Its three native 25% strips,
two construction views and contact sheet are opened at full size. Values remain
consistent: the shaft does not fade, its bend and lamp head keep their outline,
and the small ground flange stays legible. Worst mean .00375, p95 .01545,
local .01276, alpha .01597 and silhouette loss .02370 pass unchanged limits.
The complete `make check-lod` also passes geometry/re-import and original-field
audits. Frozen source/recipe checks remain intact; the second family, family
joint proof and post-build original checks are still pending.

The first GPU regression attempt did not run a fixture: a scratch-runner change
nested `with_gpu.sh` under an already held GPU lock. The wrapper does not skip
that lock; it waited on itself. The deadlocked attempt is terminated and saved
separately. The replacement batch uses one outer `kit/with_gpu.sh`, and its
children skip a second wrapper when the held marker is present. No kit source
changed and no test pass is inferred from the interrupted attempt.

The replacement GPU batch completes with all six files passing. Together with
the fresh CPU phase this is 34/34 files, with every test-file digest and both
full kit-source snapshots matching. Fresh completion follows the corrected
GPU start; peak child RSS for that GPU phase is 989036 KiB. The interrupted
double-lock attempt is excluded from this pass claim.

## Pass 59 — visible pickup skin failure despite passing metrics

Opened all three public 20608-triangle middle strips at the original 10% switch.
The front surround reflection changes and black triangular tears appear above
the front wheel at 55 degrees and along the rear bed at 145 degrees. They are
visible at the native 118-pixel height. Reject this candidate despite its mean
.01171/.00847/.00768, p95 .07844/.05883/.05099 and local
.08271/.07309/.08258, which pass the calibrated numeric limits. Its source
UV/frame and geometry audits also passed. Those checks prove neither source-skin
visibility nor appearance. The default visibility guard's additional geometry
is necessary here. Retain 23530 (39.32% of LOD0), with the cheaper fault shown in
`build/lod-v4/previews/cars/double-sided/2-55-strip.jpg` and `2-145-strip.jpg`.
The 25% target remains explicitly unmet; this is the measured exception evidence,
not a claim that saturation proves a mathematical minimum.

Opened all three nearest-compatible point-field far strips. It does not fix
color: means .03244/.02004/.02231, local .22689/.19254/.10621. Front lamp spill
persists and the rear develops false bright red emission. Reject it. No
production transfer policy or frozen recipe changed. Keep the better reviewed
optical-cap4 SS4 allocation in the canonical build and retain the known far
color failure. Geometry tightening, higher filtering resolution, coherent
point fields and nearest-compatible association have not supplied a passing
512 atlas; no palette, lighting or color-space correction is invented to hide it.

The unused cold diagnostic variants remain archived; they are not adopted or
reported as completed tests. The canonical pickup rebuild is queued, followed
by its full check and a separately scoped geometry/field audit if the far image
check fails. The full failed image result is preserved.

## Pass 60 — second frozen-tool adopter at its intended size

Opened all nine fresh WoodPrivacy native strips, six module construction views
and three contact sheets. Section A/B retain 248/664 triangles each (37.35%);
the gate retains 230/712 (32.30%). The complete three-config `make check-lod`
passes. Native values and grain stay consistent; plank seams sharpen slightly,
with worst mean .00593, p95 .02985, local .02708, alpha .03222 and silhouette
loss .03357 across all kinds/views, inside unchanged limits. Source dog-ear
profiles and bevels become square/coarse in the deliberately closer construction
views; that limitation is visible and is not described as close-view equivalence.
At the 9% switches the boards, rails and gate still read correctly. Existing
20-triangle posts remain LOD0-only.

Both family rebuild/render/check sequences return zero, and every literal
`sha256sum -c build/lod-freeze.sha256` entry matches, including the recipe.
The tool was not edited during adoption. The assembled-joint proof and all
post-build original checks remain pending; passing isolated modules is not
reported as proof of their assembled support contacts.

The four adopter original checks have now completed after the frozen builds:
street-light, privacy fences, picket and chain-link all return zero. The privacy
command freezes its recursive family target and the two subfamilies are checked
explicitly; their construction and motion checks are included. Complete commands
and results are in `build/lod-v4/adopter-original-checks.json`. The four current
adopter manifests, checks and all 60 recorded render-file hashes match. The
reduced assembled-joint proof remains queued and is still a separate obligation.

## Pass 61 — canonical colonial review catches a native visual failure

Opened all nine fresh colonial strips, four construction views and the contact
sheet. The chain measures 24949/13218/1798; both near caps are met and all nine
configured image comparisons pass. Broad siding values, garage panel response
and roof color agree. The 512 proxy loses detail at the construction camera;
at its 4.5% switch it retains the broad values and passes the previously justified
house-only phase limits (.03 mean, .13 p95, .10 local). This does not approve
new faults in its near levels.

The near front and side strips expose thin dark vertical seams below several
windows. They are visible at native size in `houses/renders/lod/LOD1-0-strip.jpg`
and `LOD1-55-strip.jpg`, and remain in the middle views. They are **a visual
failure despite passing metrics**, not a close-view-only limitation. Native
two-panel crops are in `build/lod-v4/previews/houses/canonical-inspection/`.
Straight double-precision geometry rays at four measured dark streaks find a
different first-hit siding layer in three of them (for example, source facing
cosine .939 versus candidate .304, with a 26 mm depth change); the fourth has
a 3 mm shift on a similar-facing surface. This diagnoses geometric layer
exposure at those samples, not a radiance simulation or a universal explanation
for every dark pixel. Receipt: `build/lod-v4/house-seam-rays.json`.

A separate public-config control tightens `surface_pixels` to .125 for both
near levels. Its native review is pending. No production tool, frozen recipe,
near material or original delivery has changed. Until a control passes, the
canonical house's seams remain explicitly open; neither its target counts nor
its numeric image result is reported as visual acceptance.

The native failure is archived under `build/lod-v4/house-seam-baseline/`, with
render hashes, configuration, original manifest and exact index/attribute
arrays in relocated meshes. The .125-pixel near control completes at 28698
triangles (49.28%). Its unfinished middle attempt was stopped deliberately;
the standalone near rebuild returns zero and its native review remains pending.
The interrupted canonical check has also been recaptured: `make check-lod`
returns zero, including the independent original-field audit. That result
does not approve the observed seams.

## Pass 62 — frozen adoptions and actual assembled fence joins

The final adoption freeze is `5b75c09`. All 103 literal hash entries still match,
including every kit source and the recipe. Fresh street-light and all three
WoodPrivacy builds, renders and `check-lod` commands return zero. Every native
strip and construction image is opened, and all 60 recorded evidence hashes
match the current manifests. Original street-light, privacy, picket and
chain-link checks return zero after those builds. No tool or recipe edit
occurred during this proof. The current combined adoption report and contact
sheet are `build/lod-adoptions/report.md` and `contact.jpg`.

Opened all three exported fence assembly strips and all six construction/joint
views under `build/lod-v4/fence-joints/`. Color/value and the line-post/gate
joins remain consistent at the native switch. The common 17.6166 m camera is
derived from the smallest original module height, 1.83077 m. Worst mean RGB
.00631, p95 .03253, local .02968, alpha .01864 and silhouette loss .01915
remain within the unchanged limits. The close views expose squared dog-ear
tops, stronger plank seams and simpler hinge bevels; these remain closer-camera
limitations. Gate and line-post placement show no new visible join gap.

The actual six source/reduced socket errors are identical, with maximum
1.13297e-7 m. These are measured socket origins, not a claimed bearing-surface
or swept-clearance measurement. This proof combines those frames with the
rendered joins; the original construction/motion checks are separately retained.
The joint command returns zero, peak child RSS 1361920 KiB. Its official source,
donor, script and tool receipts are in `fence-joints/receipt.json`. The paused
post-adoption supervisor has been removed after both joint proof and four
original checks completed; no duplicate validation was scheduled.

## Pass 63 — close the colonial near seams and review the canonical pickup/maple

Opened all three .125-pixel colonial near control strips at native size. The
long window-to-wall dark seams are gone; siding, trim, garage panels and roof
retain the source values. Counts are 28698/58232 (49.28%), inside 55%.
Mean RGB is .00139/.00139/.00107; local .05850/.04853/.01430 and coverage
pass the existing limits. Public geometry/re-import and independent UV/normal
audits return zero. Adopted `surface_pixels: .125` for LOD1. A same-setting
middle control is building before the full canonical house is rebuilt. The
cheaper 24949/13218 seam baseline remains reproducible in
`build/lod-v4/house-seam-baseline/`; no original bytes or tool source changed.

Opened all nine fresh canonical pickup strips, four construction views and
contact. LOD1's grille surround and rear red insert agree closely with LOD0;
all six near numeric comparisons pass. The middle front view still changes
the grille-band reflection, and the close view exposes front-joint/A-pillar
gaps and coarse wheels. This is not described as an exact shading match.
An existing-policy control applies LOD1's .2-pixel reflective bound to the
middle level too: 25448 triangles, native review pending. Count alone does
not approve it. The current 23530 mesh and all its images are archived in
`build/lod-v4/car-middle-baseline/` before any replacement.

The canonical far pickup still visibly fails all three views: mean
.02956/.01901/.02258, p95 .13227/.08311/.10980, local
.17560/.21085/.15801. Coverage passes. The complete `make check-lod` returns
2 solely for image differences; the separately captured geometry check returns
zero and the current independent UV/frame audit passes. The full failed check
is preserved. No far color gate changes. Current resident estimate is
28.527 MiB versus 21.140 MiB for LOD0: only 2.334 MiB proxy maps and 5.053 MiB
extra meshes are added. Near maps remain the exact original image content.

Opened all twelve fresh maple strips (including its camera-facing alternative),
five construction images and contact. Native crown values and mass remain
consistent at 8%, 3.2% and 1.5%; larger leaf cards are obvious closer, while
the fixed impostor exposes its four planes in the elevated construction view.
The accepted chain remains 11840/4736/8, with the separate two-triangle
alternative. All image comparisons and the captured `make check-lod` pass.
Default-chain residency is 21.204 MiB versus LOD0's 18.550 MiB. No maple
policy, count or switch changed.

## Pass 64 — validated middle fixes restore the original near color gates

Opened every native middle control at full size. The pickup's .2-pixel
reflective control removes the changed grille band at 25448 triangles (42.53%
of LOD0). Mean RGB is .00449/.00382/.00382 and local
.05500/.05454/.03424. Geometry/re-import and original UV/frame audits pass.
Adopted the bound for LOD2 as well as LOD1. The former .12 local allowance
was too lenient for that visible reflection defect: its source-phase control
did not prove the reduced surface looked right. The allowance is removed;
all original near color limits now pass. The 23530-triangle wrong-band witness
remains in `build/lod-v4/car-middle-baseline/`; the 20608-triangle skin-tear
witness remains separately retained. The 25% target is still unmet.

The colonial .125-pixel middle control removes the native window/wall seams
at 18427 triangles (31.64%). Mean RGB is .00285/.00254/.00172, local
.02043/.02157/.01075, with alpha and silhouette errors below .00037.
Geometry/re-import and original UV/normal audits pass. Adopted the bound at
both near levels and removed their old .11/.095 local allowances. The original
.08 local gate passes. LOD1 remains 28698 (49.28%); LOD2 still misses 25%.
The cheaper 13218 native seam failure is retained in
`build/lod-v4/house-seam-baseline/`. These are the lowest reviewed passing
controls, not a mathematical minimum over all possible meshes.

The recipe now explicitly requires checking thin seams, glossy response and
coverage at native size before accepting a phase-based limit, and archiving
a failed config, payload hashes and images before replacement. Its earlier
claims that those faulty near trials looked correct are withdrawn. Because
the literal document changed, the prior frozen adoption proof is archived;
both families must repeat the updated text under a new freeze. The 102 kit
source files are unchanged, as are all test inputs: no kit test reads this
document or these pilot configs. The 34-file source-verified suite remains
valid. Full canonical pickup/colonial rebuilds and the new literal recipe
proof are pending, with the pickup far color failure still explicit.

## Pass 65 — canonical station color and junction failures closed

Opened all nine fresh station native strips, all eight whole/detail construction
views and the contact sheet. Also opened the full 1920px near-side reference
and reduced frames to inspect the dispenser at its actual size. Fascia value,
lettering, columns and coverage remain consistent. Close dispenser trim and
hoses expose coarse/jagged geometry; that loss does not read as a fault in
the native switch views. No close-view equivalence is claimed.

The chain is 9130/4542/1798 (50.01%/24.88%/9.85% of selected LOD0), with
4/4/1 materials and 10/10/1 active draws. Both near triangle caps are met.
All nine rendered comparisons and the captured `make check-lod` pass, including
the independent UV/frame audit. The far reference means are
.01049/.01221/.01386, p95 .04856/.05225/.06275 and local maxima remain below
.057. Lettering and broad column/fascia values agree at the 4.5% switch.
The corrected cause is switch-capped chart allocation and a 4x antialiased
field bake filtered into the same 512 atlas, with delivered shading frames;
lighting, palette and AO are not adjusted to conceal the miss. The prior
controlled old/new comparison at converged samples remains the cause evidence.
Whole-chain residency is 90.963 MiB versus LOD0's 87.678 MiB, including the
complete immutable source container. No near image is added.

The fresh actual-world junction audit tracks all ten reported seams: source
valence 3, handoff valence 1, selected valence 3, at both near levels. Spatial
segment tracking finds zero of ten still unmatched. Whole-canopy boundary
counts are 442 to 298/274; nonmanifold counts 130 to 97/42. This closes the
reported junctions without calling the inherited construction watertight.
Current source/level/script receipts are `build/lod-v4/station-final-*.json`.

Recomputed the identical-source persistent-pin inventory using the selected
final car and house presets. Counts are unchanged from pass 56: pickup unique
4086 to 2257/2363, colonial 1674 to 552/552. The JSON now records final config
hashes and actual bounds. The cause columns are overlapping memberships of
true pins; UV/normal/material membership alone does not freeze a vertex on the
sliding path. Remaining persistent pins belong to protected optical/alpha/contact
sets. Initial offer eligibility and later geometry/frame/visibility rejections
remain separate, as do retained source geometry and refinement triangle costs.

## Pass 66 — final pickup rebuild, with the proxy failure retained

Opened all nine newly rebuilt native strips, four construction views and the
contact sheet. LOD1 and LOD2 now preserve the grille surround's value and
reflection band at their switches. All six comparisons pass the original
color limits, including the .08 local bound; no near phase allowance remains.
The transported original normal/tangent fields and .2-pixel reflective surface
bound are both retained. Close LOD2 inspection still exposes hood/front-joint
and A-pillar gaps and coarse wheels. That is a closer-camera limitation, not
a claim of close-view equivalence.

Final counts are 32612/25448/2800 against 59838 original triangles:
54.50%/42.53%/4.68%. LOD1 meets 55%; LOD2 misses 25%. The lower reviewed
23530-triangle trial changes the native grille reflection, archived at
`build/lod-v4/car-middle-baseline/renders/LOD2-0-strip.jpg`. The separate
20608-triangle backface control exposes skin tears at the native side views,
`build/lod-v4/previews/cars/double-sided/2-55-strip.jpg`. These witnesses
explain the chosen tested bound; they do not prove a global minimum.

The 2800-triangle proxy still fails color at all three native views:
`cars/renders/lod/LOD3-{0,55,145}-strip.jpg`. Mean RGB is
.02956/.01901/.02258, p95 .13227/.08310/.10980 and local
.17559/.21085/.15800. Lamps, hood and window highlights remain wrong;
coverage passes. There is no color-limit waiver. The full captured
`make check-lod` returns 2. Its independently captured geometry check returns
zero and the original UV/frame audit passes; the failed full report is kept.

The final manifest is
`f932af0ba5239677a1a6ce78ca78df44e3278c8418499c05b50aee1579dfa4e9`.
Default-chain residency is 28.662 MiB versus 21.140 MiB for LOD0, including
2.334 MiB additional proxy maps and 5.188 MiB additional mesh buffers.
Near levels add no image and retain all four canonical source materials;
active draws are 30/30/30/1. Mesh, render and independent audit commands
return zero; the render command's zero exit means images were produced,
not that its failed image gates were accepted.

## Pass 67 — final colonial strips and all six original checks

Opened every newly rebuilt colonial native strip, all four construction views
and the contact sheet. Color/value comes first: the near garage panels, siding,
roof and window trim retain the original response. The long dark vertical
window seams from the cheaper baseline are absent at both switches. The near
levels pass every original color/coverage limit, including .08 local; no near
phase allowance remains. LOD1 mean RGB is .00139/.00139/.00107 and local
.05850/.04853/.01430. LOD2 mean is .00285/.00254/.00172 and local
.02043/.02157/.01074; alpha/IoU errors stay below .00037.

The 512 proxy visibly blurs shingles and trim at the construction camera. At
its actual 4.5% switch it retains the broad wall/roof values and openings;
brighter trim pixels are within the measured unchanged-source phase floor.
Reference mean is .02593/.01926/.01015, p95 .10980/.08245/.04706 and local
.07079/.06348/.04444. It passes the already documented far-only .03/.13/.10
limits, with unchanged alpha/IoU gates. This is a native-size phase correction,
not a global lighting, palette, color-space or occlusion adjustment. The
original .75-pixel source controls remain its justification.

The final chain is 28698/18427/1798 against 58232 original triangles:
49.28%/31.64%/3.09%. LOD1 meets 55%; LOD2 misses 25%. The cheaper
13218-triangle seam failure remains at
`build/lod-v4/house-seam-baseline/renders/LOD2-55-strip.jpg`. This is the
lowest reviewed passing middle setting, not a global minimum. Six canonical
materials and ten active draws remain near; the proxy has one of each.
Residency is 48.795 MiB versus LOD0's 42.837 MiB, including every mesh and
only the proxy's 1.333 MiB of new images. The final manifest is
`e1312a1dce7c354a8d250f85d1b1c423eeeeb9d5809decd955aa045af93fb235`.
Captured mesh, render and full `make check-lod` commands return zero; the
independent original UV/frame audit passes. Render peak child RSS is
1677908 KiB; the full check peaks at 604192 KiB.

All six pilots' original `make check` commands also return zero after their
final mesh manifests. Exact frozen-input commands and results are in
`build/lod-v4/original-checks.json`; batch peak child RSS is 1358048 KiB.
A subsequent preservation audit finds all 501 original delivery/docs files
byte-identical. No source or tool edit occurred during this validation.

## Pass 68 — final literal recipe proof and checkpoint audit

Repeated both adoptions under the final literal recipe freeze `30228e8`.
All 102 kit sources and `kit/LOD.md` match their 103 recorded hashes before
and after the proof. Every fresh street-light and three-kind fence mesh,
render and `make check-lod` stage returns zero. Opened all twelve new native
strips, eight construction views and four contacts, then the rebuilt combined
adoption contact sheet. Color/value, lamp/shaft coverage, wood grain, gate
hardware and module silhouettes remain consistent at their actual switches.
Close views still expose squared fence tops, stronger seams and simpler hinge
bevels; these are not described as close-view equivalence.

Street-light keeps one 1656/3180 (52.08%) level at 25% / 27.56 m, three
materials/draws and 4.348 MiB resident versus 4.225 MiB for LOD0. Fence A/B
each keep 248/664 (37.35%) at 9% / 17.62 m; the gate keeps 230/712
(32.30%) at 18.09 m. Their active draws are 1/1/3, with one canonical
material. The 20-triangle posts remain LOD0-only. The whole privacy family is
2826 stored triangles, one material resource, thirteen stored primitive
placements, 19649439 physical payload bytes and 16.2639 MiB resident versus
16.1873 MiB for its original container. Its original three 2048 maps allocate
16.0001 MiB once; every additional module mesh adds .0766 MiB and no image.

All four post-build original street-light/privacy/picket/chain-link checks
return zero. The exact original and three fence donor dependencies, tool and
joint-script bytes are also unchanged: `fence-joints-current-proof.json`
revalidates the already opened nine assembly/joint images against this final
export. No obsolete donor is substituted. The measured six socket-origin
errors remain identical, maximum 1.13297e-7 m; this is not an exhaustive
bearing-contact or swept-clearance certificate.

Following the recipe literally required documenting one useful standard-prop
level instead of an extra shaft-fading level; omitting marginal modular levels
and already minimal posts; shared image pools, distinct module output/README
keys and serial `LOD_CONFIGS` hooks; complete source-container/family costs;
nonincreasing ratio requests even for proxies; and exact frozen-input original
checks. The final correction explicitly requires native seam/gloss/coverage
review and preserves failed config/payload/image witnesses before overwrite.
A metric or unchanged-source phase control cannot approve a visible fault.
The two final adoptions use that corrected text without changing the tool or
recipe. Generated README diagnostic placeholders are resolved to their actual
module paths; no source change is made for that formatting.

Final commands/evidence:

- All 34 `kit/test_*.py` files pass in fresh fixture folders, with Blender for
  `bpy` fixtures and the GPU wrapper for six baking/shading fixtures. Both
  source snapshots still match the final tool. Full results are in
  `build/lod-v4/regressions/results.json`.
- All six pilots and four adopted kinds have fresh mesh/render/check receipts,
  current manifests and independently audited original UV/frames. Five pilot
  `make check-lod` commands and both adopter commands pass; the pickup returns
  2 for its three proxy color views. Its separate geometry check passes and
  the full failed check is preserved. No image failure is waived.
- All six pilot and four adopter original `make check` commands return zero,
  after final mesh manifests. Exact accepted-input arguments are captured in
  `original-checks.json` and `adopter-original-checks.json`.
- `python3 build/lod-v4/final-proof.py` verifies all test/source/config/recipe/
  original/render hashes and whole-chain accounting. It reports
  `all_chain_checks_passed: false` and `all_near_caps_met: false` honestly.
  `python3 kit/repo_check.py` reports 2134 source files, zero errors;
  preservation reports 501 original files, zero changed; `git diff --check`
  passes. LOD/test/check peak child RSS is 2978852 KiB. The earlier required
  original fence-source bakes peaked separately at 7030268 KiB. Work is serial.

The rebuilt six-pilot tables/contact are `build/lod-pilots/report.md` and
`contact.jpg`; the four adopted-kind tables/contact are under
`build/lod-adoptions/`. Both reports include per-level and whole-chain costs,
with stored placements separated from active draws. All individual native
strips, differences and construction views are in each family's `renders/lod/`.
The six-pilot report intentionally uses `--allow-failed`; the adoption report
does not. Both combined sheets are opened after final generation.

Still open: pickup proxy color at every native azimuth, and the 25% LOD2 caps
for pickup (42.53%), colonial (31.64%) and grill (30.86%). Their cheaper
grille/skin-tear, wall-seam and missing-panel witnesses remain preserved.
All four requested LOD1 caps pass; the station LOD2 cap passes. The accepted
cone 436, grill proxy 1796 and maple chain remain. Close-view geometry loss,
rest-pose proxies and frozen foliage lighting/wind retain their documented
limits; no engine benchmark or continuous motion proof is claimed. Nothing
needs installing or input from the lead. Future kit work should focus on
powered proxy optical transfer and source-layer ordering before attempting
further reductions of those failed controls. The checkpoint stops here.

## Fixed UV domains — reduction regression, 2026-11-09

`preserve_uv_regions` is a per-level opt-in for shared-map reductions. It pins
source chart/material boundaries, UV folds and inherited flat-UV triangles,
vetoes unmatched-wedge extrapolation and checks orientation/area after FLOAT
storage. Normal-only splits do not create regions. Component and exported-file
audits compare boundary records; a deliberate changed exported UV is rejected.
No proxy baker, renderer, transfer code, original material or image changes.

The concave, holed, two-layer atlas-seam fixture reduces 62 to 34 triangles;
the old reducer reaches 11 but changes its domain boundary. The 23-triangle
increment is the measured cost of this conservative fixture policy, not a claim
of optimality. Fold, FLOAT-flattening, tangent, cache isolation, public-option
validation and exception-reset cases are covered by `test_lod_regions.py`.

All 35 kit test files pass serially from fresh fixtures, including six GPU
files under the shared lock. The final fold refinement is additionally rerun
in the region fixture. Logs: `build/lod-uv/tests/{cpu-passed,gpu}.json` and
`build/lod-uv/regions-final.log`. The default cone (626/436), hydrant (3524)
and bench (2360) rebuild byte-identical glTF/BIN/PNG payloads. Their complete
manifest measurements match too; only tool provenance hashes necessarily
change. Comparison receipt: `build/lod-uv/compatibility.json`. Existing source
deliveries, maps and docs are protected by `build/lod-uv/originals.json`.

Family adoptions require their own frozen-tool images and checks. This fixture
does not approve a pole, signal or sign, or predict its retained triangle cost.

## Factory paint adapter control, 2026-11-09

`490b6e8` adds an explicit `factory_paint: true` path for the delivered
`reference_plus_coverage_delta` convention. The new transfer is disabled by
default; the ordinary proxy path is unchanged. The source paint/coat/lamp decode is evaluated
before transfer. One additional linear atlas stores AO / tint coverage / clean
metallic coverage; a one-material proxy retains the original tint and metallic
tables. Its runtime metallic decode preserves the nonpaint reference response.
Family helpers opt into that graph only for the new coverage tag.

The independent GPU fixture builds its own paint, metallic trim, glass and lamp
boxes, bakes a proxy and evaluates installed color/metal fields through Cycles
after five fresh imports. Maximum measured linear component error is .001557;
all three nonpaint probes have zero tint/metallic coverage. Both lamp states
route. The fixture preserves source dependencies and measures one material/draw.
One 512 map adds 349,552 compressed-mip bytes (.333 MiB); the car proxy uses
eight 512 maps / 2.667 MiB altogether. No intermediate image is introduced.

This is a contract proof, **not a passing car adoption**. The H120 source was
rebuilt with its original family `make` before the control. All five presets
execute on LOD0 and the proxy in ten fresh imports of the actual delivered
decoder. The old control still raises `StopIteration` for every proxy preset.
The unchanged old control also reproduces its recorded native RGB errors.

Opened all six new native strips (three old-control and three adapter views),
their differences, four construction views and both contacts. Color/value first:
the reference-preset blue body remains recognizable, but the proxy loses the
windshield's broad pale cabin band and changes front lamps and rear window/trim
response. The adapter control uses 512 render samples, a fourfold bake filtered
to 512, and no image-limit override. At .04 / 43.2px / 32.5845m its 2,498/2,500
triangles meet the count, while means .060548/.033157/.031670 and p95
.270588/.168627/.207843 fail .02/.08. Local patches also fail; coverage passes.
Even the reference preset, with zero tint delta, fails. Tint coverage alone
cannot repair those existing optical differences.

Full `check-lod` returns 2 with only the rendered-difference error; the independent
normal audit, topology, fresh-import and immutable-source checks pass. No new
car chain is adopted. The brief's adapter gate stops the S240, X220 and full
H120 adoptions and pickup re-adoption. Detailed two-pass critique and measured
costs are in `cars/REVIEW.md` and `cars/README.md`. Native evidence is
`cars/renders/lod/hatch-adapter/` and `hatch-proxy-control/`; generated reports
are under `build/car-lod/adapter-report/` and `control-report/`.

The literal pre-change kit archive matches `1d9d429`. The opt-in implementation's
source/recipe freeze is `build/car-lod/freeze.sha256`; all recorded entries still
match. All **35 kit test files pass** in one serial clean-fixture run, including
the new factory fixture and existing GPU proxy/frame/transfer fixtures. The run
took 1366 seconds; commands, exits and tested source hashes are in
`build/car-lod/tests/results.json`. No runtime source changed afterwards.

Opt-out byte proof is **incomplete**, not a blanket compatibility approval:

- Cone: both full builds complete; every glTF/BIN/PNG matches byte for byte.
  The manifest differs only in its honest tool hashes.
- Maple: all ten payload files in the default 11,840/4,736/8-triangle chain match
  byte for byte. Its default manifest matches after removing tool receipts and
  optional alternatives. The optional camera-facing billboard fails strict byte
  equality: one channel of one pixel differs by 1/255, inherited from sector 0
  of the fresh capture. The fixed crossed atlas is byte-identical. The origin of
  that single-pixel variation is not isolated, and it is not waived as a pass.
- Pickup: the frozen cold build exceeded about one hour without completing
  LOD1. It was stopped with SIGTERM under the car time budget, preserving genuine
  completed reduction caches. No complete baseline/current pickup comparison is
  claimed. The full baseline phase, including cone/maple, took 3785 seconds.

Exact comparison receipts are `build/car-lod/optout-proof.json`,
`tree-default-proof.json`, `tree-pixel-differences.json` and
`pickup-regression-incomplete.json`. Every pre-existing delivery/map/image file
in the 2,996-file ledger remains byte-identical. The original H120 `make check`
passes after both controls, with explicit frozen inputs. Repository and diff
checks pass. `build/car-lod/final-audit.json` deliberately reports
`car_image_checks_passed: false`, `compatibility_proof_complete: false` and no
car adoptions. These remaining failures prevent calling the adapter/adoptions
complete; no new car delivery or documentation image is committed.

## Maple repeat proof, 2026-11-09

Four fresh 32-view camera-facing atlas builds isolate the optional maple
variation: two with every archived Python source verified literally against
`1d9d429`, then two with the accepted factory adapter. All four commands finish
successfully, serially through the GPU lock, with four Blender threads. The
source GLB SHA-256 is unchanged. Each output directory starts empty, so no
capture cache can approve this comparison.

The frozen pair differs in three pixels/channels, each by one 8-bit code;
the current pair differs in two, also by one code. Frozen run 1 and current
run 2 are byte-identical (atlas SHA-256 beginning `6f419578596f30c4`). Thus the
frozen tool alone varies, and the previously reported one-code optional-atlas
difference is a pre-existing bake variation, not evidence of an opt-out change.
The fixed crossed maple payload and cone regression remain byte-identical,
including manifest semantics except the required tool-source receipt. Literal
optional atlas byte determinism is not claimed. The pickup's hour-long full
baseline remains explicitly skipped at the lead's request.

Commands, all four full atlas hashes, pairwise pixel counts and source hash:
`build/car-lod/maple-proof/proof.json`; capture images and logs are alongside.
No runtime or accepted delivery bytes changed for this proof.

## Optional proxy glass partition — independent proof, 2026-11-09

`50856ff` adds `separate_transmission: true`; `31fc324` retains a source glass
coating when one exists. Both are opt-in. The second proxy material shares
the atlas, carries source glass culling/IOR and switchable spatial emission,
and receives only facets whose padded UV rectangle has zero paint tint and
metallic derivatives. Mixed facets stay on the factory decoder material.
Geometry, oriented corner fields and UVs remain exact across the partition.
This adds one material/color-pass draw, no map or triangle; boundary vertex
records and index/accessor packaging can add measured mesh bytes.

The new test independently checks a mixed paint/glass facet, exact position,
normal, UV and color data, source culling/IOR, and retained native coating.
A real supersampled 128-square bake then measures 48 triangles, two materials,
two draws and the same eight maps. Five fresh imports execute all paints and
both lamp states; glass has no factory-delta graph. This is interface/field
proof, not approval of a car's optical appearance or missing cabin geometry.
Native car image gates remain unchanged and independently required.

All **36** `kit/test_*.py` files pass serially from fresh fixture folders,
including the new GPU test and the existing immutable-source proxy, source
frame, factory paint, UV and material tests: 1,414.2 seconds in total.
`build/car-lod/round2/tests/results.json` records every command, exit, timing
and complete tested source hashes. Genuine pre-existing reduction caches were
archived for the clean run and restored afterward; no cache bypasses a field,
geometry or appearance check.

Fresh current-tool opt-out builds match the saved literal `1d9d429` baseline:
all seven cone game payloads and all ten fixed-maple game payloads are byte
identical. Both default manifests match except the required tool receipts.
The optional maple sector-0/camera-facing atlas retains the already isolated
pre-existing one-code variation; it is not called byte deterministic. Full
receipts: `build/car-lod/round2/optout/proof.json`. The full pickup baseline
remains skipped as requested. No result here approves an unfinished car chain.

## Fixed UV integration closeout, 2026-11-09

The fixed-domain work adopts six utility pole kinds, three signal assemblies
and eight sign kinds. Each has its own two-pass native review, immutable-source
receipt and public config; uneconomic controls remain unwired. Measured kind
tables and remaining holds are in the three family READMEs/reviews.

During closeout, main advanced to `39a466d`. Its factory/optics implementation
is retained literally; only the conflicting tool-digest list is combined with
the UV-domain module. The original `cc6cfee` adoption freeze is retained as
historical evidence. The integration freeze records 109 literal source/recipe
hashes in `build/lod-uv/integration/freeze.sha256`; every entry matches after
the complete proof. No runtime file changes after that freeze.

All 37 kit test files pass serially from fresh fixture folders, including eight
GPU test files through the shared lock: 1413.3 seconds. Per-command exits and
timings are in `build/lod-uv/integration/all-tests.json`, with raw CPU/GPU logs
alongside. Genuine production reduction caches are restored after testing.

All 17 adopted chains plus cone, hydrant and bench rebuild under the combined
tool. Every one of their 54 glTF/BIN/shipped-map payload files is byte-identical;
all 20 complete manifests match except honest tool-source receipts. The earlier
pre-fix/default comparison remains in `build/lod-uv/compatibility.json`.
Integration receipt: `build/lod-uv/integration/comparison.json`.

The 303 native proof files are accounted separately: 179 file hashes change,
143 of those decode identically, and 23 raw renders change only one or two
channels by one 8-bit code. Derived amplified differences/JPEGs also change.
Affected native/close views are reopened and all unchanged image gates pass;
literal render-file byte determinism is not claimed. All 20 full `check-lod`
runs pass after generating the three legacy chains' locally missing renders.

The three original frozen-input family checks pass again after integration
(`build/lod-uv/integrated-originals.json`). Their source receipts match, as does
the 1251-file original export/map/docs ledger. Repository check and the branch
diff against main pass. The root README and incoming car/proxy files are left
unchanged relative to main. Current reports/contacts are under
`build/lod-uv/{utility,signals,street-signs}-final-report/`. Counts remain above
their goals; this conservative lock is not a minimum-triangle or engine timing
claim. Cabinet interaction still holds LOD0, and no phase-timing or flexible-wire
simulation approval is inferred from rest images and state-field checks.
