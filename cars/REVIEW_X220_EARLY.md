# X220 early UV and delivery review

These original delivery passes precede the final X220 audit in [REVIEW.md](REVIEW.md).

## Delivery pass 1 — inspect before UVs and bake

Color/value first: preserve the accepted factory factors and matched-light
exposures. The prior Aluminum rear has 534 clipped painted pixels, localized
to its intense softbox return (x226–359/y335–519 at 1600 pixels). This is display
exposure saturation, not a material mask, cut or normal defect. The pickup's
unchanged gallery recipe is now used at scale 3, with its original light powers,
positions, diffusion broadening, cove and AgX look. A first -.2 EV Aluminum rear
control still clips 74 paint pixels; the hero clips 221 at baseline exposure.
Use a photographic Aluminum exposure bracket, independently of the accepted
sun/sky comparisons. Do not lower its albedo to compensate for a studio return.

Opened the full-size source gallery hero, rear and rear-quarter close-up.
The fine numerical cut-border curvature noise does not produce the earlier
tears in these studio views. Preserve the accepted geometry/normal fields;
test their continuity again after UV work and GLB import. Arch and projector
silhouettes are still economical, but the unsupported arch tail is absent.
The grille's blades remain regular in these new reflections. The next risk is
thin-surface cross-projection: isolate manufactured parts and test the exact
reviewed game surface before accepting any normal projection.

## Delivery pass 2 — reject the first baked inspection set

Color/value first: factory factors still match the accepted source. The first
atlas allocates 49.3% of its area with no overlaps/degenerate UVs after nineteen
explicit seams on subpixel cut/gauge charts. Bake rays fill all 7,641,490 checked
interior texels. This proves fill, not appearance. Opened hero, rear, face,
lamp, quarter, wheel and cargo at 1600 pixels. The paint has no whole-body
noise wash, but the plate and badge are visibly blurred: their actual object
names missed the first priority prefixes. Increase those specific chart weights
and the tire's, rather than adding maps.

The glass has small ripples absent from the source control despite a shader
with no optical bump height. A quantized tangent normal texture is unnecessary
on that molded shell: retain its real vertex normals and set the standard
glTF glass normalTexture scale to zero. This affects the shipped material, not
only the renderer. An independent accessor audit also finds up to 1.036 degrees
of corner-field change at thin rear-door caps when the family exporter joins
and rebases them. Preserve FLOAT_VECTOR world corner directions through that
operation and reseed them in the final owner frame; keep the .10-degree audit
tolerance. The generic verifier's transformed wheel boxes overstate width by
80 mm; raw-accessor vertex bounds remain 2117.000 × 4598.830 × 1735.000 mm.
Gate those actual dimensions independently, without reporting the inflated box
as the vehicle's measured width.

## Delivery pass 3 — preserve relief and inspect the insert normals

Color/value first: the source paint/film and the three baked color/roughness/
metal channels remain unchanged. The normal-field export repair initially
reseeded against a stale object matrix and failed badly; an explicit dependency
update fixes the frame. The unchanged independent normal gate now passes at
0.0396 degrees maximum. Reject the stale-frame images in `suv-export-pass2`.

The direct-surface normal trial still loses tire lettering and tread, despite
visible source relief. Frozen coordinate attributes retain scalar values but
lose the shader differentials needed by the normal bake. Bake the explicit
meter-height output instead; differentiate it within connected UV charts using
the actual physical tangent Jacobians, then vector-filter at delivery size.
An affine sheared/mirrored-UV fixture checks that conversion independently.
This transfers the original procedural relief, not a photograph or new noise.

The rejected direct-normal trial also exposes 27 backward interior texels.
UV picks locate them in the two corner pockets, exhaust insert and reflector
inserts, rather than the painted shell or optical lenses. Their source custom
corner normals include near-tangent/opposed cap directions inherited from the
projected sheet. Recompute those five molded inserts' own smooth wall normals
with hard gauge turns: minimum face/corner dot becomes .976 or better. No
positions, pivots or triangles change. Do not neutralize the failed texels and
call that a correction. Source and exported cargo controls agree on the exposed
quarter/header joints; they are economical construction in the accepted source,
not an export displacement. The revised final set still needs its visual gate.

The first height-atlas trial also differentiated PIL raster-edge pixels that
Cycles had not covered. Those read as zero encoded height (−5 mm), creating
false border slopes. The derivative now uses the bake's actual alpha validity
and one-sided same-chart differences. Missing raster-border samples stay flat;
valid samples are never neutralized. Thin cut charts get representable UV
altitudes before packing, so GLB float conversion cannot collapse them.

Opened the height-normal and shared-tyre controls at full size. The original
four tyre charts left lettering too soft. One canonical torus tile raises
carcass density to 854–1099 px/m without new texture memory or geometry. Left
angular reflection preserves readable lettering but mirrors tread handedness;
four separate carcass primitives are the declared draw-call cost. The final
prototype's paint and optical returns remain smooth, and lettering survives.
The final clean build must reproduce this result before docs are committed.

## Delivery pass 4 — reject aggregate density as a sufficient gate

Color/value first: the first clean export's broad paint and molding values
retain the source, but the per-panel density report exposes another allocation
fault. Aggregate painted-chart p5/median/p95 (UV-area weighted) of 208/231/244
px/m hid roughly 46 px/m on both molded bumpers, mirrors, spoiler and painted
header/sash pieces. Their names did not match the initial priority prefixes.
Give those actual manufactured pieces explicit priorities and require at least
100 px/m median on every painted piece larger than .02 m². Rebuild the atlas,
bake, GLB and all finals; keep the rejected images in `suv-uv-audit`.

Opened its seven completed gallery views at 1600 pixels: hero, rear, front,
side, back, top and face. The frontal hood reflections deserve an identical
source control. `suv-gallery-source-diagnostic` confirms the broad bends follow
the accepted formed banks, while the glass edge is continuous. That snapshot
control has unresolved relative marking-image paths (magenta badges), so it
is only a paint-form diagnostic; the final bake-loss controls use the rebuilt
source in its proper location. Preserve the accepted body design. The grille
blades stay regular, lens returns follow their shells, and no arch-tail spike
returns. Economical wheel/optic silhouettes and exposed cargo/header joints
remain source limitations; source/export equality cannot excuse a new bake tear.

