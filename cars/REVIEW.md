# X220 SUV — delivery

## Close-up repair pass 3 — baked close-ups and complete final audit

Color/value first: the final molded cargo sides retain their dark-gray polymer
value and visible drawn form; the floor and recesses remain deeply shaded.
The first baked liner exposed an outward-facing source sheet: correct its
winding toward the cavity and independently gate that direction. Its top also
ended below the rising quarter-window belt. Follow that actual belt and lap
behind it instead of masking the resulting slit. Camera rays distinguish the
remaining thin painted-frame highlights from empty seams. The complete wrapped
shoulder now moves with the gate, eliminating the standing triangular remnant.

Open `cargo`, `face`, `wheel` and `lamps_lit` from the rebuilt exported GLB at
their native 1600 px. The cargo laps close the daylight paths, the side liner
reads molded, ALDER is sharp on the grille and wheel, the projector cores/rims
read round, and the lower grille seam follows one fair curve. Native-pixel
before/after crops are `renders/suv-final/before-after-{cargo-seams,cargo-corner,
grille-badge,wheel-badge,projectors,bumper}.jpg`. The measured delivered front
badge is 202 × 46 pixels, caps 146 × 51, rear badge 143 × 51, model 201 × 51
and plate 253 × 125. All eight pass the new 96 × 24 footprint gate without
raising the ordinary density/coverage limits.

Inspect all 24 gallery/color PNGs, Eevee, both photo-matched exports/source
controls, four source studio controls and every one of the 21 motion frames
at native size before replacing docs. The contact and detail sheets also pass.
The accepted paint softbox remains continuous; cameras, lights, exposure and
color presets match the delivered metadata exactly. The independent source
comparison preserves 443 unaffected meshes including their corner normals and
all 13 pivots exactly. Aluminum still has zero clipped painted pixels in both
gallery views. The other rear presets have at most ten isolated hot pixels.
The photo neutrals remain front asphalt and the rear unprinted white sign.
Matched-light paint shifts 0–3 display levels through the bake; cladding shifts
0–.72. Gallery paint mean absolute RGB loss is .51 / 1.03 / 1.33 / .76 for
hero / face / lamp / wheel. Rear glass shifts −8.57; uniform glass and the
estimated surrounding reflections remain approximations, not a photo match.

Rebuild from a clean SUV output tree: source/checks, 4096 GPU bake, 2048 maps,
export/re-import, gallery/pairs/source controls/motion, then default `make` and
`make check` pass. Source repeat passes. All six bake channels have zero missed
interior texels over 8,667,462 checked samples each. Final export: 64,933
triangles, four materials, three embedded 2048 maps, 9,061,968 bytes; 39 fewer
triangles than the previous delivery. Both 413-pose sweeps retain the original
0.5 mm penetration tolerance. UV overlap/degeneracy/out-of-range counts are
zero; source/export corner-normal disagreement is at most .040°. Repository
check passes. The pickup retains its accepted 11,530,740 bytes and SHA-256.
No kit, other body generator, gallery recipe or accepted paint/wear factor
changes. The five bounded JPGs and 440,601-byte liftgate GIF replace the prior
docs in the amended delivery commit, after native final/compressed-image review.

Remaining CG tells: economical tyre silhouette and repeated relief, sparse
cabin, regular procedural weathering, plus the Eevee thin-sheet approximation.
The protected space under the cargo cover is intentionally dark. No additional
work or tools are needed from the lead for this limited repair.

## Close-up repair pass 1 — reopen the delivered defects

Color/value first: retain the accepted paint factors, photo neutrals (front
asphalt / rear white sign), exposures and C150 gallery. The delivered cargo
quarter is largely unlined: its dark steel reverse and two small wheelhouse
boxes read black. Add an actual molded dark-gray quarter liner with drawn
wheelhouse, cover shelf and lapped opening return. The white lines are open
construction seams, not an exposure or denoising defect. A flat-Y first liner
trial protruded past the sloping opening; reject it. Its end must follow the
actual quarter at every height, then return onto the steel/seal.

The 46 mm spike is the tapered fixed remnant of the upper-aft quarter's second
X split at 782 mm. That complete wrapped shoulder belongs to the liftgate;
keep it moving as one stamping, then independently sweep its new ownership.
The print chart names already match their priorities, but a sixfold weight
still leaves only about 31–51 pixels across a diagonal badge chart, and its
artwork leaves nearly half the width blank. A subsequent physical-axis audit
finds the larger cause: Blender's averaging/packing inherits the 4:1 marking
image aspect, producing 17.7 × 46.8 pixels along the front print's U/V axes
for a 96 × 22 mm land. Scalar area normalization cannot correct that shape.
Reconstruct print aspect from actual world vertices and authored PrintUV,
keep allocated area, and repack against a square dummy image. Restore every
original image/node before baking. Enlarge the actual lettering and allocate
measured print-axis footprints, then judge the 2048 bake itself.

The projectors use 16 segments and their glowing cores 12: this is silhouette
faceting. Use 32 angular stations, continuous wall normals and the actual lens
exit surface. Spend no geometry on the buried reflector closing strip or the
back of the emitting substrate. The wheel-center outline also needs more
stations; hexagonal wheel nuts remain intentionally hexagonal.

The bumper seam's two independently centroid-directed edge setbacks create
unequal heights along the same nominal curve. Fair the existing seam vertices
to one shared curve and reveal. Preserve the cage, apertures and parent normal
fields. Any triangle reallocation must still pass the actual surface-error,
closed collision-gauge and motion checks; a trial rear molding failed its
reconstructed gauge and is rejected. No budget or tolerance is raised.

## Close-up repair pass 2 — construction, clearance and clean source gate

Color/value first: the quarter liner uses linear RGB .105/.112/.116, a dark
gray molded polymer. The floor and protected cavity retain their deep shadow;
no gallery light, exposure, paint factor or wear mask changes. The liner has a
drawn wheelhouse, a cover ledge fading into its rear end, a turned opening lap,
a curved sill and a continuous aperture seal. Inner upper jamb returns and
higher/tapered door carriers back the visible closure gaps. Shortening those
returns above the hinge pockets fixes a rejected hinge collision. The gate's
actual skin/cassette envelope sets the liner's setback; a first central-only
sample missed the wrapped cassette end and was rejected. Two collapsed top-lap
triangles were also removed by giving the knee a real fore-aft span.

All source topology and construction gates now pass, including the full 413
poses at each density (826 total), with the original 0.5 mm tolerance. The game
source is 64,933 triangles. More angular stations go to projector bowls/lenses/
cores, wheel barrels/centers and rotors. Buried tread bottoms, rotor backs and
cassette/liner reverse gauge faces fund them; collision queries reconstruct
those exact hidden closures or the declared manufacturing gauge. Ordinary
molding reduction still gates measured surface/border error and a closed
reconstructed collision gauge; no invalid candidate is accepted.

The independent before/after source audit finds 443 meshes with exact world
positions, topology and corner normals outside the enumerated repairs, and all
13 pivot contracts exact. Source repeat also passes. Printed charts receive a
separate measured footprint gate. Every original aggregate density limit is
retained; the ordinary-surface p95 is measured separately against the same
1200 px/m ceiling.
The fixed three-map 2048 budget is unchanged. A pinned-rotation trial wasted atlas space
(24.79% unique coverage / 34.46 px/m p5) and was rejected. Keep ordinary packing
free to rotate; afterward shrink only surplus cross-word extent inside each
packed print parallelogram, retaining all word-axis pixels. This corrects the
rectangular pack's .72-squared aspect distortion without disturbing neighbors
or relaxing the original .30 unique-coverage / 35 px/m p5 gates. The baked GLB still requires its visual gate.

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

## Delivery pass 5 — reject subpixel material contamination

Color/value first: a saturated red fleck at the lower intake is impossible on
its neutral molded cladding. The 9,725,396-byte trial passes all geometric UV
checks but fails its image review. Camera rays locate face 789 of the front
lower bumper cladding at UV (.99488,.33085); the shipped RGB sample is
203/18/10. That chart is valid yet smaller than one shipped texel, so it samples
nearby lamp padding. Several lower fins also pick up brighter material colors.
This is atlas sampling loss, not red light, a shape defect or grille warping.

Keep every vertex/normal/pivot. Before repacking, expand tiny unique charts to
hold their own sampled material, using principal chart axes and measured UV
area. The revised minimum is 4.03 shipped pixels of area; no unique chart is
below four. The atlas stays within one set. Independently bilinear-sample
cladding/gloss-black triangles for impossible substrate colors, and require
that check as well as another full-size face/front inspection. Generic
non-overlap and successful serialization did not prove this bake correct.

The Aluminum exposure bracket already has zero clipped painted pixels in
both gallery three-quarters (max channels 250/253); the final new atlas must
repeat that result. The quarter source control also retains faint paint
microtexture inside the soft return, with a smooth reflection edge across
the rear cuts. No geometry change is justified by that shader grain.

The first footprint rebake clears the face but the independent color check
still rejects nine samples on a thin rear-arch gauge strip. The color extension
was 12 bake pixels while the packed gap was only about six: reduce opposing
extensions to three pixels each. All 39,948 bilinear material-color samples now
pass. Also use the height codec's unset-zero sentinel: flat surfaces encode .5,
whereas Cycles can retain alpha 1 on uncovered raster-border pixels. Exclude
those data holes from physical derivatives instead of interpreting them as
−5 mm relief. The accepted corner fields remain geometry data throughout.

## Delivery pass 6 — reject the generic dielectric response

Color/value first: the first complete matched-light export adds +5.72 / +5.93
levels to front/rear cladding even though the source's albedo/roughness were
baked correctly. Source `Nodes.finish()` uses specular IOR level .33; the family
Opaque export defaulted to .5. Preserve .33 with standard glTF
`KHR_materials_specular` factor .66, without darkening the accepted albedo.
Re-export and regenerate every GLB view and pair. Rear molding now measures
27.65 source / 27.65 export / 27.43 balanced photograph; front is
32.86 / 33.57 / 37.43. This is the value-first correction the bake-loss controls
were needed to expose. No added material or texture is required.

The first GIF also exceeded its budget. A shared palette, no dithering and
native delta frames retain all 21 poses within 450 KB at 640 px. The initial
oversized file was rejected before staging docs.

## Delivery pass 7 — final exported asset, full-size visual gate

Color/value first: paint-patch source/export ΔY is 0–3 levels, cladding 0–.72.
Rear glass ΔY is −8.36, bringing it to 130.29 versus photo 127.49. Gallery paint
RGB mean absolute deltas are .50 hero / 1.02 face / 1.33 lamp / .76 wheel.
The accepted photo mismatches remain: front glass −21, rear quarter −11 and low
front door +9 levels. Full eight-patch source/export/photo values are in SUV.md
and `renders/suv-final/bake-loss.json`; asphalt/sign neutrals and the estimated
sun/sky are unchanged. Do not call this a zero-loss or exact-environment bake.

Opened every final gallery/color PNG at 1600 px (24), the Eevee render, both
matched-light exports, source controls, all 21 motion frames, contact/sheets,
and the five bounded docs JPGs before staging any images. Followed the softbox
edge across windshield, side/rear glass, hood, fenders, molded bumpers and
quarters: no tears, new lumps or arch-tail spikes. Grille blades/carriers keep
their regular chevrons and depth; lower fins have their own pattern, with no
red or white atlas contamination. Lamp covers are continuous molded shells.
Tyre tread/lettering survives the shared tile. Road film is a low soft gradient
with spray wakes; no whole-panel noise wash was added. Aluminum clips zero
paint pixels in either three-quarter. Other rear colors retain 1–12 isolated
point pixels at 255, not broad clipped reflection areas.

The remaining CG tells are economical optic/tyre silhouettes at macro range,
soft small print/grain, sparse cabin detail, and the pointed exposed cargo/header
joins already present in the accepted source. Eevee's screen-space thin-sheet
refraction differs visibly from Cycles, and the procedural outdoors lacks the
photographs' detailed reflected surroundings. The gallery recipe stayed fixed.

Clean source→atlas→bake→export→finals rebuild completed after the documented
rejections. `make BODY=suv check`, exact source repeat, the independent affine /
missing-height fixtures, 826 source poses, grille support, raw GLB verification
and repository rules pass. The actual GLB remains 64,972 triangles in 26 mesh
nodes, four family materials and three embedded 2048 images; 9,234,008 bytes.
Atlas: 32.26% unique + 24.75% shared tyre tile = 57.01%; painted-panel density
147/210/221 px/m (UV-area p5/median/p95). All 39,948 bilinear substrate-color
samples pass. All 267 protected geometries and thirteen pivot contracts remain
exact. The pickup's accepted SHA-256 remains byte-identical. No kit or other
body generator changed. No new tool is needed.

# X220 SUV — surface and matched-light checkpoint

## Surface pass 1 — diagnosis before repair

Color/value first: Graphite's inherited linear RGB .160/.153/.141 is warm;
its luminance will be retained while moving to a slightly cool neutral gray.
The front reference is shaded/diffuse (no measurable sharp sun shadow); the
rear has very soft daylight shadows. The former asphalt neutral and rear
unprinted sign neutral remain the available white-balance anchors. Direct
sun direction/elevation can only be an estimate from these photographs.

Opened the old face, lamp, all ten full-size factory views and both actual
used photographs. Before changing geometry, rendered the SAME source with
only roadside reflection proxies removed (`renders/suv-ablation-no-canopy/`).
The supposed studio softbox was an overcast world with twelve serrated opaque
canopy polygons and trunks; the area lights were disabled. Their silhouettes
produce the white/black lens shards, the hood's large wavy patches and much
of the rear gate/quarter mottling. These patterns disappear without moving a
vertex. A second normal/bump-disabled ablation is recorded separately. No SUV
bake exists: these source defects cannot be attributed to atlas projection.

There are additional actual faults, not explained by the environment. The
projected cut and later closed-shell splits transfer nearest corner normals
without a retained outside/back/rim field. The same exterior vertex can acquire
different normals from a cap or the other side. The first audit records up to
76.65 degrees at the front fascia, 10–11 degrees on lower rear quarters, and
24–31 degrees in the A-frame. Optical shell rims must be excluded from the
continuity statistic: their approximately 90 degree turns are intentional.
The lens itself has no authored smooth parent normal field. The arch endpoints
also continue below the sill as unsupported narrow molded tails, visible as
black slivers in the old front three-quarter; these are geometry, not dirt.

Repair plan: retain a manufacturing face role and one continuous parent normal
field through cuts, joint splits and allocation; pair both laminate faces;
terminate the molded arch ends into their real sill/bumper seat. Keep all
accepted body sample positions and features. Use the family's real broad
softbox studio and separate estimated sun/sky comparison lighting. The grille
is genuinely five ribs on an opaque bed, not merely a bad reflection; replace
it with an open, deep patterned face and a distinct lower intake.

## Surface pass 2 — reject the first softbox set

Color/value first: use the inherited neutral anchors, and retain Graphite's
linear luminance (old .1536218; revised .140/.1555/.175 gives .1536126).
The first actual softbox set is darker and more contrasty than the earlier
overcast comparison. It is a surface diagnostic, not a new paint-value target.
Opened every frame in `suv-surface-control`, `suv-surface-high-control`,
`suv-surface-pass2`, and the two no-canopy/no-bump ablations. Disabling paint
bump barely changes the broad shapes: peel does not cause those waves.

The retained POINT field removes face-to-face normal disagreement at the
front fascia and lower rear quarter: the first audit's 76.65 / 11.10 degree
maxima become zero at common outside vertices. This measures continuity only,
not positional fairness. The full softbox views remain necessary. The new
quarter highlight is coherent. Ray-picking the old visible arch spike hits
`Arch cladding_RR quarter` at (0.855,1.813,.295) m; its constant-width miss
fallback was the physical cause, rather than a wheelwell or shadow artifact.
The corrected continuation retains the original silhouette elsewhere.

Reject this first repaired set. The hood still has angular reflection steps,
and the denser original source has the same broad draw-bank turn. A diagnostic
implicit-field normal copy measures .20 / 1.51 / 2.61 degree median/p95/max
departure from the original hood field; compare its actual studio pixels
before choosing a repair. The small fuel flap also shades as flat triangles:
its non-planar cap had no continuous quarter normal field. Capture that field
for the formed cap. The new explicit optical roles must survive material-slot
collapse and must not make optical backs eligible for concealed-skin removal;
both implementation hazards were caught before checkpoint acceptance.

The new upper grille has sixteen mirrored chevron blades in dark chrome, two
support rails and the retained badge; eighteen straight black lower fins are
visually distinct. It replaces 560 old rib/web triangles with 560 real open
triangles, leaving the deep bed and surround. It is much more intentional than
the former radiator, but the first close-up is too angular at blade bends.
Check whether a softer manufactured edge can read within the same allocation.
Still CG here: hood reflection steps, triangular fuel flap, and very regular
optical jewelry/arch facets. These frames are rejected progress, not finals.

## Surface pass 3 — reject the clear-sky and uniform-cloud comparisons

Color/value first: front asphalt and the rear sign still supply the same
neutral balance. The clear scattering-sky trial (`suv-daylight-pass2`) gives
front mid-door 116.6 versus 88.1 and glass 52.9 versus 158.8. Its rear view was
occluded by an accidentally retained studio cove and is invalid; no rear
measurement from that frame is accepted. Removing the cove and adding diffuse
cloud cover (`suv-daylight-pass3`) raises front glass to 154.2, but also raises
the door to 135.7 and rear door/cladding to 197.5/78.7 versus 135.3/27.4.
Opened both whole frames and annotated pairs. Reject the uniform bright dome.

The photos' low horizon is wooded, while the inclined glass sees brighter sky
above it. Add original smooth closed canopy masses that cast shade and obstruct
the low horizon, separate from the clean softbox studio. They are schematic
lighting geometry, not copies of photographic foliage. Lower comparison
exposure and judge again; do not alter the four accepted paint values to
compensate for an over-bright environment. Direct solar direction/height remain
uncertain because both photos have very soft contact shadows, not crisp
shadow endpoints. The numerical sun settings are estimates with ±20° angular
uncertainty, not shadow-derived precision that the photographs cannot support.

The implicit-normal hood experiment changes little in the actual softbox
pixels and is rejected as a repair. Keep the accepted parent. Refine twenty
game hood cells ranked by their parent-normal interpolation error instead;
this adds actual samples where a broad reflected edge steps, without refitting
the sculpting. Full closed glazing can simplify legally where the old open
windshield could not; retain both optical surfaces and use those savings.
Validate the outside/reverse provenance against the parent hemisphere after
closed-volume winding correction, then keep one field through all later cuts.
Still CG in these rejected comparisons: overly uniform reflected surroundings,
regular wheel/optic jewelry, and the stepped hood highlight at game density.

## Surface pass 4 — optical geometry, then the sampled studio edge

Color/value first: the wooded-horizon trial (`suv-surface-pass5`) gives front
mid/low door 100.7/94.8 against 88.1/76.6, front glass 150.1 against 158.8,
rear door 135.2 against 135.3, rear quarter 138.2 against 152.6, rear cladding
31.0 against 27.4 and rear glass 167.4 against 127.5. Opened all seven actual
studio/comparison frames. Lower front exposure by .3 EV. Reduce the excessive
blue in the trial Graphite while retaining its exact .1536218 linear luminance:
final factor .150/.1540545/.160 is neutral to slightly cool. Calibrate the
front solar-control and rear privacy reflection amplitudes separately, keeping
IOR, transmission tint and glass roughness. Check those changes in both stages,
not solely at the selected patches. Road-film masks remain unchanged.

The optical trials exposed a geometry cause beneath the normal-transfer fault.
The steel-chart hull projects into crossed or almost-collinear pane triangles.
Backlight fans connect distant lower-border stations; rear-side top-edge fans
also have three almost-collinear border vertices. Their geometric normals turn
against the intended pane even when a continuous optical normal is supplied.
The retained bad-face report in `build/suv-surfaces/bad-optic.log` records the
actual world positions, areas, face normals and optical normals. This is a cut/
triangulation fault, not orange peel, opacity, a bake or a reason to relax the
normal check.

Use each pane's original generated ordered guide border, its own injective
YZ/XZ chart and smooth sag. An inward 26 mm collar connects each curved border
segment to a nearby interior sample, eliminating the three-border-vertex fans.
Both real 4.8 mm laminate surfaces share the optical parameter field. Keep the
authored collar through the game allocation instead of dissolving it back into
long fans. The windshield retains its parent shape and now has its real reverse
surface; its legal closed reduction funds the optical collar and twenty extra
hood sample cells. No implicit-normal-only hood substitution ships.

The collared game source passes the unchanged solid and optical checks at
**64,896 triangles**. Full game sweeps pass all 413 poses with no violation.
The detailed cabin, underbody, wheels and pivot contracts still require the
explicit old/new preservation comparison before reporting. Final renders are
the next gate: regular optics/wheel silhouettes and schematic distant foliage
remain possible CG tells even with these checks passing.

Before freezing the grille, an actual support probe finds no badge/grille
triangle contact and a 20.25 mm minimum badge-vertex distance. Its two straight
support rails also chord across the bowed blade field. Replace those rails
with six-section curved carriers and add the required badge stem. The planned
76 extra triangles are construction, funded by the remaining reserve; the
badge must sit on the grille rather than float in front of it.

The taller opaque rear-tree trial made the chosen glass patch 32.8/255, so it
is rejected too. The November photograph has a sparse/bare wooded horizon;
aggregate porous canopy coverage preserves bright gaps without the original
serrated polygon shapes. At -.6 EV it gives rear door/quarter/cladding/glass
151.1/156.1/39.7/153.2. Lower rear exposure another .35 EV and correct the rear
molding's excessive film: the old aft-wheel mask continued uniformly across
the protected center face. Attenuate that layer on the rear-facing center,
retaining the side wakes, sill gradient, loading wear and every paint mask.
The trial Specular IOR Level changes have little effect on fully transmissive
Cycles glass and will be removed; retain physical IOR 1.52 and the family glass
response rather than promising an unverified coating calibration.

## Surface pass 5 — frozen source, full studio crops and matched daylight

Color/value first: the final Graphite factor is .150/.1540545/.160, with
linear luminance .15362178 versus the inherited .1536218. The four other
paint factors and all metallic factors remain unchanged. Front photo balance
uses the foreground asphalt (linear gains .8834/.9907/1.1647); rear balance
uses the unprinted white sign (1.0173/1.0173/.9672). These are available scene
neutrals, not calibrated cards. Final median display-luma samples, out of 255:

| View / patch | Render | Balanced photo | Difference |
| --- | ---: | ---: | ---: |
| Front / mid-door | 87.4 | 88.1 | -0.7 |
| Front / low door | 82.4 | 76.6 | +5.8 |
| Front / cladding | 33.2 | 37.4 | -4.2 |
| Front / glass | 137.2 | 158.8 | -21.6 |
| Rear / mid-door | 135.9 | 135.3 | +0.6 |
| Rear / quarter | 141.2 | 152.6 | -11.4 |
| Rear / cladding | 27.6 | 27.4 | +0.2 |
| Rear / glass | 137.9 | 127.5 | +10.4 |

Actual boxes, RGB samples, balance gains and lighting are in
`renders/suv-surfaces/pair-measurements.json`; annotated picks accompany each
pair. The pairs use the calibrated cameras, procedural scattering sky, diffuse
cloud coverage, estimated broad sun lobe and asphalt-gray ground. Front solar
elevation/azimuth are 48/-40 degrees; rear 34/145 degrees, each with roughly
20 degrees of directional uncertainty. Smooth original canopy volumes supply
the wooded horizon; the rear canopy is porous. This matches diffuse light
structure, not either photograph's detailed reflected environment. The front
glass still reads too neutral and dim; the rear quarter is too dark and the
chosen rear glass patch too bright. A matching door sample does not make the
whole render photographically matched. Paint wear remains unchanged; only the
protected rear-facing cladding film is attenuated, as the previous pass found.

Opened the final 1600-pixel face, lamp and rear-quarter views, all ten full-size
color views, both used pairs, all eight curvature/both-stripe pages and every
before/after region. The lens now carries one coherent softbox reflection
rather than the earlier serrated shards. Fender and lower grille reflections
continue across their surface instead of choosing unrelated cap normals. The
hood's accepted broad draw-bank turn remains; local sampling reduces its
piecewise steps without changing the parent. Rear gate/quarter highlights are
coherent, the fuel flap no longer shades as a triangle fan, and the trailing
arch spike is gone in the actual front three-quarter crop. Historical lighting,
old mesh under the same softboxes, and repaired mesh are shown separately:
most of the dramatic old lens/hood mottling was the reflected environment.

The diagnostics now include all 492 tagged meshes: glass, lamps, grille,
arches, wheels and visible interior/underbody, not only painted panels. Mean
curvature uses actual triangle positions, with boundaries/gauge exclusions
gray; stripes replace every measured material with the same reflective shader
and preserve its mesh and normals. Their limitations remain visible: fine
cut-border curvature noise near the rear quarter and small polygonal steps
at some stamped transitions. Continuous authored normals are not evidence that
the geometric curvature is everywhere smooth. Arch molding, projector rings,
mirror/roof details and wheels still show economical facets close up; the
accepted detail was not expanded to disguise these limits. Schematic horizon
reflections and a sparse cabin are further CG tells in the used pairs.

Tonal masks retain deep zero-level cavity shadows. Paint p99 luma spans
223.6–247.9 across the ten studio color views. Nine have zero clipped sampled
paint channels; Aluminum rear has 0.133% at the brightest specular return.
That small residual is recorded rather than calling the whole set unclipped.
The face, lamp, rear-quarter and both daylight views have no clipped sampled
channels. Numeric tone masks are in `tonal-ranges.json`.

The open chevrons, distinct lower fins, bowed carriers and badge stem now
measure actual contact: 16 badge/stem crossings, 16 stem/carrier crossings,
and positive intersections at all sixteen blade/carrier joints. The rebuildable
`suv_grille_check.py` fails if those supports disappear. This proves engagement,
not structural load capacity. Final allocation is **64,972 triangles / 492
meshes / 35 source materials**, 24 triangles below the accepted source; high
is 167,002 / 500. There is still no SUV bake or GLB. The one-2048-set / 16 MiB
delivery plan remains reserved, not delivered.

`make BODY=suv detail`, `make BODY=suv check`,
`make BODY=suv check-detail-repeat` and
`make BODY=suv surfaces WIDTH=1600 SAMPLES=48` pass. The last command produced
41 inspection frames plus sheets/crops/pairs under `renders/suv-surfaces/`.
The final source hash is
`01b2a4699150989d1b84ad8ff09e36d78c553561211d2ca869af1c1623c0a1ef`.
Independent preservation compares 267 accepted mesh geometries and all thirteen
pivot contracts exactly. Both unchanged 413-pose sweeps pass (826 total), at
0.4315 mm game / 0.2069 mm high maximum measured penetration and 0.5 mm tolerance.
Side-laminate entrance/exit normal mismatch is at most 0.060 degrees at both
densities. Repeated generation agrees exactly on positions, polygons, corner
normals, matrices, parents and material names. Pickup bytes/hash are unchanged.
These prove geometry, sampled clearance, source repeat and preservation; they
do not prove final UVs, bake quality or exported appearance. Stop at this gate.

# X220 SUV — detail and look development

## Detail pass 1 — form fixes and inherited-work audit

Color/value first: retain the stock photos' neutral white backdrops (unit white
balance gains). Gloss clay is a neutral linear .18 clearcoated gray; it is not
a match to the white paint. Its procedural sky and actual dark ground plane
supply the upper/lower reflected values. Opened all five actual-triangle
curvature maps and their matching stripes, all four old-photo-camera gloss
views, the side and the front/rear gloss views. Evidence: `renders/suv-detail-form/`
and `renders/suv-detail-gloss/`, with the four original cameras in
`renders/suv-detail-gloss-pairs/`.

The interrupted work correctly identified two different faults. The cowl used
a hard hood/canopy height switch with different lateral values and derivatives;
it now blends the two fields before fitting the control cage. Aperture cuts
mixed existing coarse chord vertices with newly projected limit vertices,
creating ridges in skinny cut triangles. The local cutter now intersects the
same physical source triangles, and the exposed front fascia is resampled on
its parent using a constrained chart with real hole membership. The denser
parent and local A-foot sampling retain that shape. These change actual
positions/topology; the raw mean-curvature diagnostic is not filtered.

The corner comparison's negative-curvature tail improves: in the disclosed
X640–890 / Y<-1700 / Z400–940 mm region, five valid vertices below -5 /m become
zero. This is a changing sample set (587 versus 347 vertices), not a pointwise
improvement score. The A-foot becomes a coherent narrow concave transition,
not a perfectly convex panel: its local minimum remains about -6.5 /m and the
hood-cowl draw is still visible. Small cut-border speckles remain at the thin
upper fascia strip. Do not report them as eliminated. Broad corner stripes
are smoother; the remaining raw sampling noise deserves another look at bake.

In the side gloss, the shoulder reads continuously as a bright-to-dark reflected
break, the rising lower crease changes value above the rocker, and both fenders
carry broad crown highlights. Keep their accepted amplitudes. Against Honda
and Toyota the original's cowl is still less relaxed, its lower line subtler,
and the untrimmed glass and optical blanks still look cheap. No change to the
accepted package or photo cameras is justified by this lighting test.

The inherited detail scene was also opened and rejected: 65,980 triangles,
coarse sweeps with intersecting cards/tires, supports passing through the dash,
a roof/spoiler overlap, and trim clips on exterior surfaces. Its source modules
are useful scaffolding, not verified work. The next passes correct construction,
measure actual surfaces, and judge new renders against the used photographs.

## Detail pass 2 — reject ornamental hardware and unsupported cabin surfaces

Color/value first: factory Graphite is the family's linear .160/.153/.141,
with a continuous clear coat. The inherited gray source is not a silver/white
match. Compare it against both used-car photos before adding fine wear. Opened
`renders/suv-lookdev-pass2/` front/rear, opened and cargo views beside the two
used photographs. The body still looked too dark below its shoulder and the
optics were too plain. The front and rear needed separate camera/value checks.

Reject the first assembly: it was 70,624 triangles after real sash/header
separation, and actual rest/swept contacts occurred in cards, tires, the floor,
hood supports and dropped spoiler ends. The first hinge blocks neither sat on
real bearings nor concealed themselves behind the skin. Do not accept parenting
as construction. Rebuilt pin/sleeve bearings, inboard goosenecks and documented
hinge axes; split the steel and plastic at the closure joints. Sashes and arch
segments follow their door. The gate carries its upper header and spoiler while
the fixed D-pillar stays below the joint. The struts now articulate from measured
attachment frames, rather than staying as fixed cylinders in the open views.

The cabin uses shaped five-seat upholstery, actual cards, a cluster/display,
console, headliner and cargo trim. A later emission-only material probe exposed
the dark lower-door band: the constant-X inner carrier protruded through the
inward-curving outer skin. It was not dirt. The carriers/cards are now fitted
behind actual door rays; the floor is narrowed to clear them. The cargo cover
has a tapered rear edge and the inner gate lining stays behind the pocket.
No outer body vertex is moved to accommodate these interior corrections.

Still cheap/CG in this pass: angular sparse cabin trim, over-plain lamp backs,
small uniformly silver wheel faces and exterior-looking hinge bits. Fix those
before treating a counts/audit pass as a look approval.

## Detail pass 3 — reject the first used-pair calibration and glass transfer

Color/value first: the eventual comparison balances the front photo on the
foreground asphalt and the rear on unprinted white sign stock. These are
available scene neutrals, not calibrated gray cards. The former gains are
.8834/.9907/1.1647 in linear light; rear gains 1.0258/1.0129/.9635.
Opened the two `renders/suv-lookdev-pass3/` pairs and rejected both as evidence.
The rear inherited picks missed the wheel centers by over a hundred preview
pixels and used the wrong near-side sign. A low coplanar landmark RMS did not
make that camera physically correct; the body was cropped and the hidden wheels
fit instead. Re-inspected the full 1400-pixel previews and added the visible far
rear contact with lower weight. The shared solver now gives 12.66/6.39 native-pixel
RMS, estimated 72.17/106.18 mm lenses, and the correct camera quadrants. All
projection-implementation residuals remain independently checked in Blender.

The reduced glass also showed black triangular facets. Its vertex query chose
entrance, exit or rim normals interchangeably at shared border coordinates.
Re-seed each corner from the same geometric hemisphere, preserving smooth
entrance/exit fields and flat gauge rims. Reject open or >1.3 mm chord-error
reductions; keep the original windshield and backlight where proposals fail.
The typed source audit additionally rejects opposed transmission normals.
These are optical/shading corrections, not a frost tint or roughness increase.

Opened `suv-lookdev-pass4`, `pass5` and `pass6` pairs. The corrected framing,
separate optical internals and actual interior are substantially clearer.
An emission-only BaseColor/road-film/gap-grime probe confirmed that the broad
black band was carrier geometry, not a weather texture. Once it was moved
inboard, the lower painted door returned. The blank plate was also seated on
its true sloping pocket plane, rather than intersecting the bed, and the
washers are supported on actual hood rays. Both corrections matter at full frame.

Still CG: uniform sky/ground reflection fields, dull gray door values, sparse
red lamp jewelry and very regular window trim. Use original camera-hidden
roadside reflection silhouettes with the procedural sky/ground, not a downloaded
HDRI or a texture reconstructed from the photographs.

## Detail pass 4 — color/value calibration before final presentation

Color/value first: `renders/suv-lookdev-pass6/measurements.json` records the
unretouched display RGB samples after the photographic balance above. At the
front, mid/low door luma was 52.6/48.6 against 88.1/76.6; rear mid-door was
97.5 against 135.6. This was an exposure/reflection problem, not permission to
make the paint chalky. Keep the factory tints, neutralize the overly blue cloud
source and raise the comparison exposure by .9 EV, from -.3 to +.6.

Opened `renders/suv-lookdev-pass7/` and both annotated measurement pages.
The same front mid/low patches now read 82.1/76.9 against 88.1/76.6; rear
mid-door 139.2 against 135.6, and rear-quarter 146.4 against 152.7.
Cladding is 32.7 versus 37.4 front, and 39.9 versus 27.4 rear. The rear molding
is still too light in that sample. Front glass is 116.2 versus 158.8; rear glass
141.6 versus 127.7. Environment/reflection correspondence is weaker than paint
value correspondence. The silver remains cooler than Toyota's warm reflected
mid-door, and the original warm Graphite is less violet than the balanced Honda.
No pixel samples are reported as measured albedo. The camera/trim/lighting and
regional correspondence limitations stay visible in the pairs.

The extra road load follows axle wakes and stays low; upward cladding fade,
loading/sill scuffs, hood/door-edge chips, gap deposits, glass-bottom sediment,
brake dust and wash swirls each have a physical mask. Inner arch fastener heads
are original height relief, rather than the inherited floating exterior blocks.
Clearcoat, peel and flake remain the family method, with solid colors turning
flake off in the review. The five paints use factors, not five texture sets.

Still CG in this pass: the reflection environment is simpler and less varied
than the real wooded parking places; very regular side trim and low-detail
cabin shapes remain visible. The lamps and wheel need their final close-ups,
and wear visibility must survive the later 4096/2048 bake. This is source look
development, not a shipping or baked-GLB approval.

---

## Detail pass 5 — optics, wheel finish and inspection views

Color/value first: the 1600 px source close-ups retained the matched +.6 EV
setup. Paint has reflected sky/ground separation and dark cavities, but the
unlit projector substrate was almost white and the entire alloy wheel shared
one bright value. The lower side-glass sediment scattered into a coarse white
strip. Those are material failures visible before any bake, not excuses to
increase exposure or make glass opaque.

Keep the lit emitter's warm-white emission and darken its unlit physical
substrate. Separate machined axial wheel faces from darker cast pockets using
rest normals, add wheel-centered radial brake dust and fine machining response,
and retain the family alloy/paint method. Reduce sediment to the bottom few
centimeters, with finer deposit density, a much smaller roughness change and
nearly intact transmission. These remain manufacturing masks for the later
neutral bake, not extra per-color textures.

The original eye-height cabin image was dominated by the sky reflection and
large mirror, so it did not prove the interior. Shift the camera toward the
front window center; add a camera-hidden photographer's black flag and a small
physical cabin bounce. The glass material is the same as in the hero. Taper and
round the upholstered headrest sections instead of retaining box-like caps.
The cargo floor/cover, rear bench and actual gate supports are present; the
cargo trim remains deliberately sparse. The first low view mostly showed the
rockers and wheels. Lower its camera to 80 mm above the ground and add a separate
below-floor inspection view with the ground removed, so the AWD layout can be
judged independently of the low-angle vehicle view.

The extra fuel-flap sweep exposed an uncut quarter-panel behind its outer cap.
Cut the actual skin, form a filler cup and cap, and align the hinge with the
flap's forward-edge chord. Both source densities now clear to 85°. All twelve
required mechanisms also pass their individual sweeps. The game plate's tiny
bevel moves to the high source to fund that pocket; game total is 64,980.
Two sub-micron C-divider cap slivers were cured by welding coincident cut points
within 5 micrometers before capping. The high source passes the unmodified kit
solid/sliver audit. The solid, budget and 0.5 mm motion tolerances are unchanged.

Remaining CG tells to review in the final set: the regular low-segment projector
bezel and wheel-barrel silhouettes in extreme close-up, idealized roadside
reflection shapes, simplified cargo and engine compartments, and the thin
upper-fascia cut-border curvature noise. The final source is frozen before the
last render batch; its renderer now rejects source or recipe edits during a
batch so provenance cannot drift while images are being written.

## Detail pass 6 — physical supports and parallel glass

Color/value first: keep the prior photographic neutrals and +.6 EV; the front
and rear paint value corrections remain. The revised side-window view removed
the broad sky veil, but exposed two separate defects. A visible white oval was
the inspection area light itself, so hide that fixture from camera, glossy and
transmission rays while retaining its diffuse bounce. Large triangular cabin
displacements persisted, proving they were not just lighting or dirt.

Compare the game and unreduced high cabin, plus an explicitly diagnostic IOR=1
copy. The high and IOR=1 images have coherent seats/controls; the old game has
broken refraction. Entrance/exit shading-normal rays find up to 47.7° mismatch
through a 4.8 mm laminate. A hemisphere test alone missed this: independently
transferred normals selected an old rim on one layer and the pane on the other.
Use one actual exterior-sheet field for both layers, with flat physical rims.
The 116-ray diagnostic grid falls below 1.85°. The broader 13×13-per-pane audit
also samples the tightly curved lower A-corner: its maximum is 3.65° on both
source densities, with all rear/quarter panes below .56°. Record that residual
and a disclosed 5° audit bound; do not claim perfect optical parallelism. Final
images retain physical IOR 1.52 and the real laminate; the IOR=1 copy never enters
the checkpoint. Evidence: `renders/suv-interior-pass8/`, `suv-interior-high8/`,
`suv-interior-ior1/`, `suv-interior-pass9/` and `suv-interior-pass10/`.

The second eye-height camera sees the steering wheel, shifter/cup holders,
cluster and center screen. Replace the oversized shared placeholder text with
separate original instrument and abstract navigation graphics. The seat/cargo
camera and this controls camera complement each other; one cannot prove all
five seats and all controls in the same frame.

A direct contact audit found a fault that stroke/sweep tests cannot find: hood
strut body seats were 149 mm from surrounding structure, and hinge plates were
8.64 mm below the hood. Add two formed triangular fender returns (16 game
triangles total), then fit the hinge tops in vehicle space, not their pivot's
local Z. Measured final hinge-to-skin distance is .40 mm. Actual seat/return and
return/fender surface intersections prove support on both source densities.
The small exhaust hanger ends now reach the actual floor or rear longitudinal;
they have 12/12/10 measured game triangle crossings at those attachments.

The final game source is **64,996 triangles**, four below the hard limit; high is
167,598. The source has 35 manufacturing materials and six generated marking/UI
images. These are not a shipping draw-call or texture-memory claim. The later
neutral 2048 atlas remains budgeted at 16 MiB with compression/full mipmaps.
The source is frozen before the final full render set. Remaining CG tells are
the regular close-up wheel/projector silhouettes, broad procedural reflection
shapes, sparse cargo/engine detail and unmodeled full hood reinforcement. The
lower front glass corner and thin upper fascia cut-border noise remain honest
limits for the checkpoint, not hidden by a normal-map claim.

## Detail pass 7 — final full set and used-photo comparison

Color/value first: the final front photo uses the lower-left asphalt neutral,
linear gains .8834/.9907/1.1647. The final rear uses the unprinted white sign
patch, gains 1.0173/1.0173/.9672. The full pairs and measurement crops use the
same neutral balance. These are display-RGB comparisons under different
reflection environments, not measured albedos. The small rear gain change from
the earlier preview comes from the final Lanczos-resampled neutral patch.

| Patch | Render luma / 255 | Balanced photograph / 255 |
| --- | ---: | ---: |
| Front mid-door | 82.1 | 88.1 |
| Front low door | 77.1 | 76.6 |
| Front cladding | 32.7 | 37.4 |
| Front glass | 116.4 | 158.8 |
| Rear mid-door | 139.2 | 135.3 |
| Rear quarter | 146.4 | 152.6 |
| Rear cladding | 39.9 | 27.4 |
| Rear glass | 141.4 | 127.5 |

The main paint values are close; the front factory Graphite is warmer than the
Honda's violet-gray, and Aluminum is cooler than Toyota's reflected silver.
The rear cladding remains too light and the front glass reflection too dark in
these selected patches. Do not hide those misses by changing the neutral
factory palette or treating the photographs as albedo maps. The roadside
reflection environment is deliberately original and remains less detailed than
the actual leafy/urban surroundings.

Opened all 34 final form frames as four inspection pages, all 28 look frames,
the direct lamp/wheel/controls/cargo/underbody/opened close-ups, and the three
gloss-clay views. The gloss clay shows a narrow shoulder value break, the lower
die's broader shadow change and curved fender highlights. The maps and matching
bands retain the thin cut-border noise instead of concealing it. Color variants
retain body identity, dark cavities and distinct plastic/gloss trim; the white
and silver remain different, and black retains sky reflections. Across all ten
factory-color views, geometry's first-percentile luma is 1.1–2.1/255 and paint's
99th percentile is 227–233/255, with **zero clipped paint channels**. The lit
lamp close-up intentionally clips its luminous cores; its paint 99th percentile
is 216/255. Masks and complete per-frame ranges accompany the sheet.

The new controls view reads through actual glass without the old triangular
prisms or visible inspection fixture. Instruments and navigation graphics are
separate, original assets. The opened gate shows the cargo cover, floor and
three rear headrests; the low shot and below-floor inspection complement each
other. Orange trajectories show sampled actual vertices; the numerical proof
remains 413 individually sampled poses per source density, at the documented
0.5 mm penetration tolerance. No continuous swept-volume or arbitrary combined
pose clearance claim is made.

Remaining CG: regular macro wheel/barrel and projector silhouettes; stylized
low-frequency reflections; sparse cargo/engine/hood underside detail; the small
A-corner optical mismatch and upper-fascia cut-border curvature noise. Tire dust
and small wear remain more regular than the photographs. Fine peel/flake,
lettering, UI and grain may lose definition in the future 2048 bake; no baked
or exported appearance is being claimed. The checkpoint keeps these limits
visible for review rather than declaring the asset finished.

# X220 SUV — form round 3

The accepted round-two source is `53f57a8`. `main` was merged at the start
(already up to date). Its images and source snapshot were preserved before
editing. Work stays in SUV modules and evidence; no kit/shared generator,
sedan, hatchback or pickup source changed. Current evidence is
`renders/suv-round3/`, with 34 source renders and a 52-view contact.

## Round 3.1 — diagnose the damage before editing

Color/value first: both makes' white studio backgrounds remain the neutral,
with unit RGB gains. Clay linear value stays 0.36. Do not mistake a dark optical
blank or different exposure for a panel dent. Opened round two's rear/front and
raking images, the two makes' front/rear photographs, and five baseline
mean-curvature views of both the actual game body and the independently rebuilt
uncut parent. The broad dents were present before the projected cuts.

The plate surround came from the explicit 22 mm `plate_sculpt` displacement.
The hood's narrow 26 mm crown collided with the leading roll. The rear chart
bunched and reversed quads where two projection centers blended, compounded by
abrupt height-dependent plan exponents. The side's narrow die hollow continued
around the bumper and produced repeated reflection teeth. Mirrors used an
irregular polygon loft with QEM collapse, leaving visible planar fans.
These are distinct causes; a normal reset is not a repair for any of them.

Retained raw rays, normals, exclusions and geometric curvature. The new mean
map uses actual game triangles, cotangent weights and mixed Voronoi area, with
no smoothing or custom-normal substitution. Analytic plane, sphere and cylinder
checks pass. Boundary vertices are gray, unmeasured parts dark, and all views
use the same signed scale. The large number of skinny cut triangles produces
local numerical noise; that is shown rather than filtered away. Both makes'
photos have clean uninterrupted panel highlights, so a merely passing section
test is insufficient evidence of fairness.

## Round 3.2 — clean gate and plate recess

Color/value first: compare the body highlight in both calibrated rear clay
pairs against the white-background neutrals. Keep the pocket dark, but inspect
its silhouette and lit return. Opened straight rear, rear three-quarter, both
rear photo pairs in clay and stripes, the rear curvature/stripe pages, and the
round-two/new rear comparisons.

Removed the displaced plate surround. The gate is convex across; actual
center-to-X600 setbacks are 24.4 / 28.5 / 45.6 mm at three heights. The cut pocket
has a planar bed (49 ray hits, less than 0.001 mm departure from its fitted
plane), sharp edges and its own return. The 320 × 170 mm nominal pocket has a
323 × 176 mm actual cut including clearance. Actual lip depths vary 20.8–24.9 mm
under the sloping convex mouth; the old guide-to-bed rays were 4 mm proud and
are no longer described as physical depth. The panel turns in below the lamps,
with a broad 1201 × 44 mm garnish and badge land above the pocket.

The former broad soft dents around the pocket no longer appear in the clay.
The rear map shows a broad coherent field around it, and vertical reflection
bands sweep through the gate rather than breaking around the old displacement.
Compared with Honda, the garnish and lower gate still read more generic and
less decisively stamped. Toyota has stronger angular side shoulders around its
plate; the X220 follows Honda's softer convex panel without copying the lamp
signature. The garnish remains a little bar-like and the empty pocket increases
the prototype impression. Small cut-border disturbances remain in the raw map.

## Round 3.3 — rear corner and D-pillar

Color/value first: neutral backdrop balance as above; inspect gradients, not
photo paint brightness. Opened both makes' rear clay/stripe pairs, raking side,
rear and side stripes in both directions, and the matching whole-mesh maps.
The reference highlights sweep through each corner without a dent or repeated
zigzag.

Replaced the abrupt plan-power changes with broad smooth transitions; relaxed
four-valent control spacing before subdivision and used one radial projection
center. That alone was insufficient: the first trials still showed teeth below
the rear arch. Ending the lower-door die field in the arch and fading the bumper
crease before the corner removed the repeating ripple. Independent 95th-percentile
game/parent normal mismatch at the rear bumper and D-pillar is now 0.36 / 0.54°,
versus 2.67 / 2.86° before. The high source audit subsequently caught a tiny
concealed lower-return fold; the control-spacing correction was extended there
instead of exempting that object from topology checks.

The broad quarter and bumper no longer read as pushed-in panels in either rear
pair. Vertical bands are substantially more regular. Residual high-frequency
noise remains around cut/stitch triangles in the unsmoothed game curvature map;
it is not evidence of a perfect class-A surface. The broad rear pillar is still
heavier than Honda's, and the regular window corners and bare lamp cavities look
cheaper than either reference. The existing Honda D-pillar outline miss remains
about 106 mm nearest-silhouette distance; this round did not refit the accepted
package to that photograph.

## Round 3.4 — shoulder, lower line and swells

Color/value first: body albedo is unchanged. The low sun direction runs along
the side, with neutral sky fill, to reveal normal turns rather than bleach the
paint. Both makes' front and rear calibrated pairs show highlights continuing
across the doors. Opened the side clay, relit raking view, both side band
directions, actual ray profiles and whole-body curvature side view.

The supported shoulder now turns **16.1–16.3° across 30 mm**, with a measured
10–90% transition width of 30.5–31 mm. It runs continuously between the lamp
ends and is a narrow red/orange strip in the geometric map. The lower crease
turns **9.0–9.5° across 80 mm**, with a 37–43.5 mm 10–90% transition width; it
rises from 561 to 587 mm. The fender swells remain **32.3 / 29.6 mm** beyond the
door at Z900 mm. Both show as broad curvature changes around the wheel openings.

The shoulder is now a visible continuous break in the raking image. The rising
lower line and rear arch swell read clearly; the front swell is weaker in that
single lighting direction and clearer in the three-quarter pairs. Toyota's
lower stamping is more assertive and Honda's shoulder has a more confident,
continuous highlight. The X220 door centers remain very plain without handles,
and horizontal stripes still expose minor sampled waviness over the front arch.
Do not call those remaining issues solved by the angle measurements.

## Round 3.5 — hood and mirrors

Color/value first: white-background neutral in both front reference pairs;
compare highlight shape independently of the dark production mirror trim and
headlamp reflectors. Opened the front, top, front three-quarter, both front
pairs in clay/stripes, both hood reflection directions, and the mean maps.

The narrow corner crown is broadened and reduced; the two raised draw banks
fade before reaching the nose. The raised center drops **34 / 30 / 18 mm** to
X600 at the three measured hood stations. The new bands show two continuous
raised banks rather than folded corners. The front still has the accepted long
lamps meeting the original grille surround. Compared with both makes, the
remaining optical blanks and three broad grille blades look unfinished; the
hood's A-foot transition also concentrates bands more than a production panel.
The hood corner remains the weakest sampled region, with 95th-percentile
normal mismatch to the fair parent of 3.48°.

The mirror shells now have evenly distributed rounded sections and **1246
triangles each**. Size, sail placement, 1135 mm bottom and 2117 mm overall width
are unchanged. Their front silhouette and highlights are smooth, with crowned
tops, rounded ends and planar rear glass. Honda's cap is softer than Toyota's;
the X220 is now closer to that soft cap, but a little oval/bulbous, especially in
front three-quarter. Its border and tiny sail still lack the assembled precision
of either production mirror. The old large polygon facets are gone.

## Round 3.6 — molded spoiler

Color/value first: compare against both rear pairs after neutral background
balance; Honda's black spoiler is judged by section and silhouette, not copied
as a material treatment. Opened the rear, raking side, rear three-quarter, top,
both rear pairs, stripes and geometric maps, plus round-two/new rear comparisons.

Replaced the thin board with a closed molded section continuing the roof. Its
main aft chord is **65–76 mm** thick, with **159–191 mm** downturned end returns.
Twenty-nine root rays show 5.4–8.0 mm overlap into the roof seat. The underside
turns forward into the gate and the third-lamp blank is integrated in its aft
face. The spoiler group costs **1710 triangles** including the lamp.

The side and rear pair now show depth and downturned ends instead of a plate
standing on the roof. Honda is the closer construction reference; Toyota's
trailing surface is flatter and its black end treatment more angular. The X220
end caps remain somewhat abrupt where they meet the D-pillar, and the broad
white bridge looks bulkier than Honda's dark assembly. The lower surface is a
closed root plus an overhang, not a claim that the underside touches glass all
along its length.

## Round 3.7 — whole car, white clay

Color/value first: unchanged linear clay value 0.36, deep black cavities and
rolling highlights; hero foreground p99 remains about 231 / 219 with no clipped
channels. The raking view is intentionally darker (median about 39, p99 199).
These are source lighting measurements, not a claim about finished albedo.
Opened both makes' four calibrated clay pairs, the corresponding stripe pairs,
all original view modes, the old/new comparison sheets, overlays and five
whole-mesh curvature/stripe pages.

The accepted wrapped face, taller lamps, door mirrors, low rails and rear lip
are retained. The gate no longer looks dented, the hood has visible draw banks,
the shoulder is continuous, and the spoiler has a molded section. The remaining
cheap/CG tells are the uneven untrimmed window boundaries, plain optical blanks,
regular wheel proxies, sparse garnish construction and a few small cut-edge
highlight disturbances. The raw curvature maps still show sampling noise at the
end-corner triangulation; they do not justify a claim of perfectly fair surfaces.
The side package still differs from Honda at the D-pillar and cowl. Keep this a
form checkpoint and stop before interior/detail/bake work.

---

# X220 SUV — form round 2

This round retains the accepted package and cameras from `74b40c4`. `main`
was merged first (already up to date). The hatchback's `577ca2c` modules and
briefs were read as method references; no hatchback code was copied or edited.
The new evidence is `renders/suv-round2/`, with 24 source renders and a 45-view
contact. The first round remains below and in `renders/suv-form/`.

## Round 2.1 — face, hood and front plan

Color/value first: both makes' white photographic backgrounds are the neutral,
with unit RGB gains. Their pearl paint is not a clay-albedo target. The new
white clay retains black cavities; body linear value is 0.36 at the recorded
exposure. Opened both calibrated clay front pairs, both striped pairs, the
straight-front reference measurements, top view and both hood band directions.

Reject the original vertical wall, shallow slivers and broad lamp/grille lands.
The front now turns back **255 mm at X800 mm**, against approximately **271 mm
Toyota / 258 mm Honda** from the two independently scaled rescue plans. The
long lamps grow to **158 mm** vertically, wrap **542 mm** in Y, and approach
the grille mouth to **18.8 mm**. The grille has an original hexagonal folded
lip and **66–67 mm** depth; blades follow its curved bed. Tapered corner wells
are **60–62 mm** deep under a raised ridge. The front black center is **329 mm,
34%** of hood-to-ground height; at X700 mm it is **155 mm** high. Painted
corners now descend around it, matching the construction visible in both makes.

The raised hood center and two draw banks now show in both pairs. Actual
center-to-X600 drops are **37 / 29 / 18 mm** at three fore-aft stations; crowns
are **7–10 mm** above their adjacent hood edge. Early trials crumpled at the
lamp/hood turn because a Cartesian nearest-point projection climbed onto the
hood. Polar guides and local constrained cuts remove that failure. A whole-panel
triangulation trial filled previous recesses; it was rejected. The local cutter
excludes upward-facing hood triangles that share its angular/height chart.

Still weaker than both makes: the three broad blades and dark optical blanks
remain visually plain, and the hood's transition into the A-foot concentrates
reflection bands. The face now has the right large-scale planes, but the clay
is not a finished modern grille/lighting assembly.

## Round 2.2 — mirrors

Color/value first: neutral white background in both front/rear reference pairs;
compare the painted cap's highlights and silhouette separately from the black
production mirror trim. The side, top, front and all four three-quarter pairs
were inspected. A bright irregular highlight is a fairness issue, not wear.

Replaced the old transverse rounded box and tube stalk with a compound loft,
flat rear glass and a broad tapered sail on the upper front door. Actual size
is **260 × 160 × 130 mm**, centers **X ±928.5 / Y −649 / Z1215 mm**, bottom
**1135 mm**, total span **2117 mm**. The sail begins at Y−890 mm behind the
A-foot. The side silhouette no longer puts a cap on the hood/cowl. The top view
proves its depth and tapered front; the rear pair proves the flat glass face.

Compared with Toyota's compact wedge and Honda's softly rounded cap, this is
closer in placement and section. Its cap highlights are still uneven and its
rear border is more polygonal than a production molded part. That remains a
localized CG tell even though the bounding dimensions and door parent pass.

## Round 2.3 — shoulder, lower line and fenders

Color/value first: the same white-backdrop neutral is retained in both makes'
pairs. The previous raking view was too dark and put a long mirror shadow
across the doors. Reverse the low sun along the side and provide neutral sky
fill; do not increase the material's albedo to fake a crease. The final raking
foreground median rises to **53**, with p99 **185** and no clipped channel.

Sharpened the shoulder's supported transition while retaining **1037 / 1051 /
1062 mm** measured heights and **16.2–16.5°** upper lean. Lower lean grows from
**4.7–4.8°** to **15.6–16.0°**; the low crease turns **9.0–9.5°** over 80 mm,
rising from **562 to 587 mm** across the measured door stations. Fender swells
are **32.4 / 29.3 mm** beyond the central door at Z900 mm. Both striped side
views, actual sections and the low-sun view were opened.

The raking image now shows a continuous narrow shoulder highlight and a rising
lower light/dark break. The rear swell is obvious; the front is subtler at this
sun direction and clearer in three-quarter. Toyota's lower side stamping is
more angular and Honda's transition more fluid. The X220 still has very regular
window borders and an overly uninterrupted door field without the later handles;
those missing details must not be used to excuse a weak highlight.

## Round 2.4 — rear plan and taillamps

Color/value first: white photographic background neutral in both rear pairs;
keep the lamp blank dark so its border, rather than optical jewelry, proves
its form. Opened both rear clay/striped pairs, straight rear, top and the two
rear reflection directions alongside both photographs.

The rear envelope now sets back **211 mm at X800 mm**, following Honda's
approximately **197 mm** more closely than Toyota's **252 mm**. Its actual
local XY circle at X650/700/750 is **308 mm**, not a prescribed constant radius.
The gate is convex across and the bumper has a broad central crown. The two
lamp pieces follow one polar guide with a clean split at the gate shut line;
maximum corner height is **183 mm**, against **178 / 197 mm** photo estimates.
The cases have measured **42 mm** walls to their recessed beds. Cutting guides
retain their exact boundary vertices instead of snapping to a coarse lens disk.

This removes the old torn blobs and their large painted notches. The lamp's
pointed side tip is still more stylized than either make, and fine waviness
survives in the gate seam through the quarter. Clear-aperture rays prove the
holes, not optical quality or highlight fairness.

## Round 2.5 — gate stamping, bumper and lower rear

Color/value first: white studio neutral in both rear photos. The dark central
pocket is deliberate; bright, lumpy patches around it are not accepted as a
material effect. Inspect the rear clay and both band directions before calling
the sheet sculpted. The initial broad rounded recess was too pillow-like; a
harder trapezoid trial then showed coarse facets. Broadened its banks, reduced
its depth and let the bottom blend toward the gate cut. Removed a separate
narrow garnish that read as a tube, keeping the stamped cross-gate crease and
small unmarked badge seat.

The pocket remains **320 × 171 × approximately 25 mm**, with its overhead lamp.
The painted upper bumper wraps into the corners above a **220–248 mm** main
black lip. Toyota/Honda main lips estimate **229 / 233 mm**; their additional
upper black areas are recorded separately rather than counted as part of that
short lip. Reflectors and exhaust finisher are real recessed locations, with
central skid finish. The actual **20.64°** departure follows Toyota's cited
**21°**, not Honda's 25.3° FWD trim.

A first corrected corner setback still left the bumper **95 mm** short in the
side overlays. Broadening its center plan brought the final held-out bumper
miss to **34 / 40 mm nearest silhouette**. This is independent proof: setback
alone did not establish the profile. Still wrong: the plate surround remains
softer and less crisply stamped than both references, especially Honda. The
lower finish/reflector relief is subdued in the dark clay; finishing must keep
its real depth rather than substitute bright decals.

## Round 2.6 — spoiler and rails

Color/value first: compare silhouettes against the white background in both
rear pairs; a dark underside is an overhang shadow, not proof of an air gap.
Inspect the root in geometry as well as the side/top/rear images.

The spoiler is now a closed molded section seated into the roof, with ends
dropping over the D-pillars and an integrated third-light blank. All **23**
measured root samples overlap the roof by **1.5–4.1 mm**. The side overlay follows
Honda's spoiler (**8 mm** nearest miss); Toyota differs by **44 mm**. That
choice is explicit. Rails are **39–47 mm** above the local roof on two molded
feet each, keeping the **1700 mm** overall height. The old tall stalks are gone.

Both photographs have more resolved spoiler end-cap/roof junctions. The X220's
extreme end still concentrates stripes and can read a little folded. The rail
feet also remain simpler than production molded trim, though the near-flush
height now reads correctly in the side view.

## Round 2.7 — fairness and overlay audit

Color/value first: neutral white reference backgrounds; procedural white/black
reflection bands test slope flow, not paint color. Opened seven final band
views, four striped pairs, all four curvature plots and all profile overlays.
The continuous hood center, doors and main roof show much cleaner flow. Lamp
corners no longer contain holes from chart aliasing. Local refinement around
the rear turn reduces the earlier zigzags without refining the whole car.

The curvature report retains every raw sign reversal. Its new named regions
cover the actual raised hood banks, corner-pocket ridge, plate shoulder and
broadened bumper crown/waist. At Y2100 the parent has additional reversals near
Z400/472 mm in the lower bumper return; the game has reversals near Z838/956 mm
where the broad bumper joins the quarter. These are visible designed section
changes, not silently removed samples. Both finite checks pass their documented
feature zones. **They do not certify Class A fairness.** Rear horizontal bands
still expose local ripples around the bumper corner and D-pillar/gate junction;
the mirror cap is also less fair than the references.

In the perspective overlays, lower front chin nearest miss is **9 / 5 mm**,
rear bumper **34 / 40 mm**, lower rear **22 / 31 mm**, spoiler **44 / 8 mm**
(Toyota / Honda). Front bumper remains **42 / 4 mm**, upper rear **24 / 44 mm**.
The accepted upper side package is unchanged in its important dimensions:
Honda's D-pillar holdout remains about **101 mm nearest**, **211 mm fixed-column
vertical**, and its cowl **57 mm nearest**. Do not call the whole silhouette a
40 mm match. The raw orthographic overlays remain available too; they are not
substituted for the specified perspective views.

## Round 2.8 — whole car in white clay and checkpoint decision

Color/value first: both white stock-photo backdrops are the neutral (unit gains).
Final hero foreground p99 is **230 front / 218 rear**; neither has a clipped
255 channel. Deep intake, wheelwell and under-car shadows remain. These numbers
are diagnostic-clay exposure evidence, not final paint/albedo validation.
All 24 final source renders were opened in four review pages, both full-size
heroes and four full-size clay pairs. The technical evidence, reference
annotations, old/new comparisons and final contact were also inspected.

The car now reads as a contemporary compact crossover more readily: swept
full-height lamps, a shaped grille opening, descending painted corners, hood
draws, a shoulder highlight and lower side crease, wrapped rear units and low
rails. It remains a prototype beside both production photographs. The biggest
remaining form weakness is the soft rear plate surround; local rear and mirror
highlight unevenness and regular greenhouse borders still read CG. Fine optics,
handles, trim, seats, underbody and materials are deliberately absent. Stop at
this form gate rather than disguise those weaknesses with finishing.

Actual allocation is **59,642 triangles**, **141 meshes**, **5 clay materials**,
**0 image maps**, no SUV GLB. Tires save 1,408, openings/cases 2,188, cladding
1,356 and doors 408 versus round 1; those savings fund the sculpted fascias and
compound caps. The plan in SUV.md removes another 5,500 from hidden backs,
flat/inboard surfaces and wheel proxies while reserving 10,000 for cabin,
underbody and remaining detail: **64,142 planned**, not already built.

`make -C cars BODY=suv model check`, `render`, `review` at 1600/40, and
`check-repeat` pass. Source audits have zero errors/warnings; all 141 meshes
repeat exactly including corner normals, transforms, materials and parents.
All 24 renders use one source hash. `pickup-round2-preservation.json` proves
454 pickup source meshes and 150 GLB accessors unchanged; the fresh GLB is
byte-identical, **11,530,740 bytes**, SHA-256
`ec70cde87fbe50fb814cc14c900ee324e254711b5bfa5d3735aef166b146de5b`.
No kit files changed. The only shared code edit is an optional tire-segment
setting with unchanged defaults, committed separately. No tools or installs
are needed. A future reusable local surface-chart cutter would help the kit,
but its domain and winding tests should precede generalization.

---

# Round 1 history

# X220 SUV — source form checkpoint

## Pass 1 — reject folded quarters and cosmetic cut faults

Color and value first: the four 2020 RAV4 LE / CR-V LX stock photographs have
white studio backgrounds (white-balance neutral, unit RGB gains). Their pearl
paint and transparent windows are not clay albedo targets. Opened the eight
native front/rear/profile/rear photos, the first four full clay pairs and the
complete pass-1 through pass-4 Workbench sheets. Early clay had a broad pale
window reflection; suppress specular on the opaque diagnostic glazing rather
than treating that reflection as body form or raising the exposure.

- Profile: the package reads as a lifted long-roof car, but the window rectangles
  and nearly vertical quarter-window ends read as a cheaper older wagon. Replace
  them with projected six-light apertures, round their corners, and raise the
  quarter-window's lower aft edge. Keep two makes visible in the comparisons.
- Side: the progressive section is present but a false panel cut at the low die
  line interrupts it. The inherited rocker label created that cut. Remove it;
  the door is a continuous stamping behind the separate lower molding.
- Front: real grille/intake/corner wells replace dark slabs. The lamp blank is
  too thin at the outer tip and the lands are too plain beside both production
  fronts. The apron and lower molding have small cutting spikes, not acceptable
  wear or intentional detail. Trim every affected skin at each opening and
  close the lower fascia independently. A wider crown is needed toward the A-foot.
- Rear: reject the first folded D-pillars and flaps. The high rear-glass rows
  wrongly used a sedan's low-deck section topology: the shoulder climbed half a
  meter between adjacent control rows. Continue the actual shoulder/belt/roof
  section through these rows before fitting. Widen the rear glass on its own
  projected aperture, keep substantial sails, and keep the plate pocket crisp.
- Construction: the first black band was separated from an already closed
  gauge, leaving open cut edges. Split the outer sheet at the molding line and
  close both physical pieces. The longitudinal low cladding must also be cut
  away at the wheel openings; it cannot cross an empty arch.
- Fairness: the hood center's driver-eye bands are continuous, but the A-foot
  has concentrated grazing bands and the original rear quarter bunches them.
  The stripes do not yet prove a fair whole body. The unclassified sign changes
  remain in the raw curvature report, with no acceptance claim.
- Allocation: reject 68,920 triangles. The earlier source wasted samples at end
  backs and glazing; retain feature-aligned exterior samples, reduce redundant
  glass grids/rail spans and keep the 60k cap. The later 55,894 candidate is a
  better allocation, subject to the pending topology and form checks.

The chassis fits are 7.19 / 8.91 / 8.40 / 9.99 native pixels RMS. These are five
chassis anchors with uncertainty, not all-body accuracy. Mirror, pillar, bumper
and roof correspondence is independently judged; no photographic outline enters
geometry. No UV, paint, bake, interior, underbody or motion approval is implied.

## Pass 2 — judge the unadorned body and the reflected bands

Color/value first against both makes' white stock photographs: compare form,
not neutral clay to pearl paint. The white backdrop remains the neutral; no
photo-derived tint enters Blender. Opened every pass-1 through pass-7 render
in `build/suv/intermediates-0.jpg` through `intermediates-6.jpg`, plus the
full-size driver-eye hood, front horizontal bands, rear vertical bands and
raking side. The raw front/rear photos remain beside the clay pairs.

The roof is long and nearly level, the hood is short/high, and the squared arch
moldings establish the crossover class. The first independent arch band crossed
the low door moldings, making teeth at the openings. Cut those moldings too,
shorten their toes to the sill, and remove hidden game steel hems covered by
the molded inner returns. Tire/arch crown gaps stay near 55 mm. The two makes'
body sides show more construction variation than the unadorned clay; adding
handles or lamp jewelry is not a substitute for the crown and low die line.

The old rear chart lifted its shoulder toward the backlight. Keeping the actual
shoulder/belt section through the rear rows removes the large flap, but the
first rear lamp outline still made a high black triangular tip beside the
backlight. Lower its corner guide while retaining the measured 120–200 mm
corner height. Broaden the rear glass on its own aperture and move the gate's
side cuts outside it. The lower bumper needs its convex plan and turned-under
bottom; a plate beneath it would be a different construction failure.

The hood's center reflection lines are continuous, with concentration at the
two intended draws. The doors show broad flowing bands. Do not approve the
A-foot simply because most of the door is smooth: a coarse chart chord crossed
the compound parent there. Regular quarter-step chart samples around that foot
are needed; local inserted n-gons made the cut topology worse and were rejected.
The final chart retains its feature flow without a new evaluated-surface fit.
Fine grazing variation at the header and quarter still needs the final views.

## Pass 3 — construction and actual measurements, before final presentation

Color/value first against the same four neutral-background photo pairs and
both raw rear-width photos. Keep dark cavities, charcoal moldings and opaque
glazing as diagnostic materials. Reject the earlier glossy plate-bed blob and
window glare as presentation; the actual recess still needs a crisp outline.
The rear plate mouth was only about 160 mm high after projection. Enlarge its
control height to reach approximately 170 mm, retain the 25 mm depth and seat
its small overhead lamp from the actual mouth samples. Use 4.8 mm main glass,
not the optical blank's default 1.5 mm gauge.

The physical fascia split must precede closing the sheet. Extracting an exterior
from a closed, repeatedly perforated fascia could include one return strip;
that produced a three-face edge at the grille. Form both upper paint and lower
plastic regions on the fair open sheet, then close and cut each. Fixed welded
upper-frame regions do not need artificial reveals between themselves. Exact
world-space door cuts keep their real reveals. No topology exception is added.
The final tiny collinear-face cleanup dissolves degeneracy at 0.1 micrometre;
it does not weld the two layers of a closed shell. A broad closed-shell weld
was tried, made the fan topology worse, and was rejected.

The source's upper door lean is about 16 degrees; lower lean grows from about
4.6 to 15 degrees, with a measurable inward hollow and a roughly 9-degree die
turn. The grille/low intake/corner wells have approximately 62/55/48 mm depth,
with paint-clearance rays measured along the actual bed normals. An axial ray
at a tapered corner can leave the aperture and is not proof of a blocked hole.
Mirrors are door-mounted 260 × 125 × 164 mm wedges, 2117 mm across the pair,
with a flat rear pane. They no longer form oval caps on the cowl.

The front chin is lowered toward the profile, and the angle test now uses a
supporting plane tangent to the mean loaded tire circle. A line from the patch
center alone understated the real approach/departure angle. Both values are
retained in the report; suspension compression and underbody clearance remain
outside this form build. No input dimension is returned as a measurement.

The original allocation spent too much on temporary glazing/rails and hidden
backs. Keep the game source inside 60k without exempting any part. It still
sits near that cap, above the desired 50k: later detail must replace/reduce this
allocation, not be added on top. No kit or sedan module changes were needed.

## Pass 4 — reject full-size aperture artifacts

Color/value first: the first 1600-pixel Cycles candidate was too pale, even
though its channels did not hard-clip. Keep the white photographic backdrops
as the neutral and judge neutral clay separately from the manufacturers' paint.
Lower the diagnostic exposure; do not brighten the cavities or moldings.
Opened the complete later Workbench sheets, the uncut parent from the side and
front three-quarter, and the rejected full-size Cycles front/rear candidate.

- Rear: a large notch at the D-pillar was a cutting fault, not an acceptable
  styling feature. The convex hull of a wrapped optical border in parameter
  space crossed a region above the actual guide. Preserve this concavity,
  partition it into convex cutters and use a constrained lens triangulation.
  An independent ray traced the missing paint to the quarter-lamp cut. The
  uncut parent was continuous there. Reject the attempt to use concave borders
  for the simple windows/pockets: it left little irregular edges.
- Openings: retain explicit outside/back/rim provenance through Solidify;
  classifying coarse skin chords by a 25-degree normal threshold can discard
  legitimate compound-corner skin. Closed cassettes have curved beds and walls;
  their geometry follows the corner instead of a straight n-gon across it.
  A very dense cassette trial exceeded the cap and was rejected. Spend on the
  border; use a coarser internal bed grid. Never exempt hidden backs from the
  budget. Disjoint cutters now leave untouched triangles intact instead of
  unnecessarily fragmenting them along extended cutter planes.
- Lamps: the coarse guide's straight segments in chart space still made an
  irregular outline around the tight corner. More guide stations follow the
  physical bend. Project their construction onto the evaluated fair parent,
  rather than the coarser game chords; the latter introduced a little facet
  jitter into a densely sampled border. Optical guides go directly to the
  chart triangulator instead of refining/closing a disposable Cartesian lens.
- Cladding/wells: replace the circular liner behind the squared arch with the
  same squared section. This closes the daylight above the tire. Reduce the
  arch crest's authored proud offset by 2.5 mm: the actual rear measurement was
  27 mm, beyond the brief's 25 mm maximum. Preserve the 22 mm inward flange.
- Cowl/quarter: keep the shoulder control rows below the belt as the canopy
  folds down, and maintain distinct monotone end-row tangents. The source
  parent is much better than the first folded rows. The A-foot and header's
  concentrated grazing reflections still deserve scrutiny in the final pairs;
  a successful door section cannot certify these separate regions.

The later previews are retained in `build/suv/late-previews-*.jpg`; rejected
Cycles candidates remain under `renders/suv-candidate/` and
`renders/suv-candidate2/`. They are review history, not accepted final images.

## Pass 5 — reject the premature profile handoff

Color/value first: use the white photographic backdrop as the neutral, with
unit RGB gains. The clay is a diagnostic gray, not either make's pearl paint.
The earlier pale Cycles candidate hid too much of the crown; use 18-percent
linear gray for the final body and a darker wheel proxy. Opened all 24 views
on the four `build/suv/candidate3-page-*.jpg` sheets, the four striped photo
pairs, the original side photos and both registered overlay methods. Also
opened all eighteen subsequent low-resolution profile/rear trial renders.

- Profile: reject the apparently tidy upper tail. Its nearest silhouette miss
  against the CR-V's D-pillar was 148 mm; its fixed-column vertical miss was
  280 mm. The end draw pulled the upper gate too far forward. Extend the upper
  mass/hinge by 120 mm, keep the spoiler's aft extent, and maintain the glass's
  approximately 30-degree rake. Use an upright upper gate and a stronger lower
  bumper tuck. A single end-depth coefficient made the lower plastic project
  too far after the upper gate correction. The separate, smooth lower return
  restores the departure angle, measured from actual outer surfaces.
- Front roof/cowl: the old header was roughly 100 mm high at the RAV4 holdout.
  Lower the cowl and header and let the roof rise toward its nearly level main
  span. Retain the measured windshield rake inside 55–60 degrees. Lower the
  mirror housing 20 mm and move it aft 50 mm to keep its rounded cap within the
  corrected profile, with its foot still at the door's front upper corner.
  The front chin also needs its lower draw, rather than a nominal approach
  constant printed beside the picture.
- Glass measurement: the old fixed 1.25/1.51 m ray chord did not always touch a
  side pane. The high front sample hit a frame, and after lowering the header
  it hit the windshield. It was not a glass-tumblehome measurement. Find the
  actual side-pane ray span and measure its central 60 percent; retain the old
  chord, its hit-object names and explicit invalid-for-glass scope in the JSON.
  The three central panes remain around 19 degrees. Do not report the fixed
  chord as a successful glass check or silently delete that debugging evidence.
- Rear construction: retain the projected glass widths and real gate cut,
  narrow the pocket's authored height to recover its actual 170 mm mouth after
  changing the gate's slope, and keep the overhead lamp attached to that mouth.
  Recheck the actual optical paths and clear-paint rays after the end changes.
- Method: retain both fixed-axis residuals and nearest silhouette distances.
  A steep backlight amplifies the former. Neither metric is a full photo
  outline fit. Keep the raw orthographic overlay and supplemental fixed-lens
  perspective overlay, even where either one misses the 40 mm request. Hide
  the studio floor in quantitative profile renders so shadow-catcher pixels
  cannot become part of the measured silhouette.

The body is closer to the modern crossover class, with a long roof and a real
lower door turn. The regular side-window corners, plain front lands and broad
unadorned rear bumper still read older/cheaper beside both photos. Fine grazing
concentrations at the A-foot/header and small arch-to-lower-molding junctions
remain CG tells for the final scrutiny. Handles, optics and badges cannot
substitute for fixing those surfaces. No detail or finishing stage is opened.

## Pass 6 — rear glass proportions and final evidence integrity

Color/value first: the photographic white studio remains the neutral. The
18-percent gray body keeps deep cavities and un-clipped highlights; it is not
matched to pearl paint. Opened all 42 candidate-4 review views, including both
rear photographs, both rear construction comparisons and every clay/striped
pair. The completed contact exposed a miss that the width calipers alone had
not caught: the backlight was 413 mm high and touched the lamp band. It read as
an older tall-window wagon beside both makes.

Measure height too: the same rear-photo ratios give about 314 mm Toyota and
275 mm Honda vertical span, with perspective/body-width/pick uncertainty. Raise
the glass base on the unchanged fair parent. The next measured centerline span
is 301 mm, with a 30.7-degree rake and approximately 1393 / 1159 mm base/top
widths. The painted land between the backlight and lamps now exists. Opened
the new rear and rear-three-quarter Workbench renders before proceeding.
The same-height projected D-pillar is only about 162 mm: it remains slimmer
than the photo-ratio estimates, which also use a different body-width height.
That ratio is a remaining weakness, not an approval claim.

Crown calipers now find the actual Hood object's plane-cut boundary and sample
1 mm inboard of its gauge rim, then search the adjacent fender. They measure
12.7 / 14.1 / 14.1 mm rise. The old x=735 mm probe was a surface sample, not a
measurement of the actual shut-line edge. The result remains inside 10–30 mm,
with the corrected method recorded explicitly.

After lowering the front header, move the driver's-eye reflection camera aft
inside the greenhouse (+X 340, Y −100, Z 1470 mm). Its old Y −520 mm position
could sit above the lowered windshield. This is an authored seated eye estimate,
not an interior/ergonomic certification.

The image check also rejected two empty rear clay pairs. Their low matched
cameras were behind the studio cove's rising back. Rotate the cove for rear
views, regenerate, and reject any review image with empty opaque foreground.
The geometry and fitted cameras are unchanged by that lighting correction.
Keep quantitative profile renders free of the shadow-catcher floor.

The broad rear plastic and regular window/upper-frame transitions still read
cheaper than the production photos. Small grazing-band concentrations at the
A-foot, D-pillar and lower rear remain visible in stripes. This finite source
gate is not a global Class A surface or a finished vehicle.

## Pass 7 — final source review; do not approve form from numeric checks

Color/value first: the white studio backdrops remain the neutral, with unit
RGB gains. Final clay is 18-percent linear gray. Opened every final view on
`build/suv/final-review-0.jpg` through `final-review-6.jpg`, the complete raw
front/rear photographic comparisons, full-size CR-V front and RAV4 rear clay
pairs, the driver's-eye hood and front reflection bands. The front/rear hero
p99 display luminance is 219 / 206; clipped-255 fraction is zero. Cavities
retain deep shadow. The low-sun view is too dark to be the main side proof
(median 19); use it alongside the studio and both stripe directions.

- Profile/package: the high short hood, long roof, raised wheels and squared
  moldings establish the class. The overlay still fails the brief's 40 mm
  target. Raw wheelbase-registered nearest misses are 83 mm Toyota lower tail
  and 81 mm Honda front bumper; upper-profile maxima are 49 / 46 mm. The
  fixed-axis maxima are 128 / 110 mm. Supplemental fixed-lens fits still have
  101 / 103 mm nearest misses and 128 / 244 mm axis maxima. Retain all four
  overlays; neither method is permission to call the silhouette accepted.
- Side/greenhouse: actual shoulder heights 1037 / 1050 / 1062 mm, upper lean
  about 16 degrees, progressive lower lean 4.6 to 14–16 degrees and a 9–9.5
  degree low die turn give the doors a visible gradient. Glass lean is around
  19 degrees. Reflections still concentrate/pinch at the A-foot/header and
  upper quarter/D-pillar. The regular pane corners and uneven applique ends
  read procedural. The finite eleven-section check misses these transitions;
  it is not a global fairness certificate.
- Face: the 654–657 mm wrapped lamps, 13–14 mm fender crown and real grille,
  intake and corner wells are measured on actual surfaces. The lamps' tiny
  cut-edge tips/margins and the parallel grille blades still read as a proxy,
  and the broad unarticulated fascia lands look cheaper/older than both
  references. Fine optics and badges would not resolve the parent transition.
- Rear: the corrected 301 mm glass height and 30.7-degree rake remove the old
  tall-window wagon proportion. Widths are 1159 / 1393 mm top/base; the
  same-height D-pillar estimate is only 162 mm against uncertain photo ratios
  of 196 / 235 mm. The gate has a real 319.5 by 170.4 mm plate mouth and
  25–26 mm recess, but the broad convex lower plastic, unshaped plate land and
  regular lamp borders remain the most obviously older/cheaper rear cues.
  Small grazing concentrations remain at the lower rear/quarter transition.
- Arches/assembly/allocation: actual crown clearance is about 55 mm; moldings
  have 60 mm bands, 19–23 mm sampled proud offsets and visible inner flanges.
  Small toes where they meet the low molding remain CG tells. Actual outer
  approach/departure are 19.45 / 20.97 degrees. There is no measured underbody
  clearance or completed hinge/suspension sweep. All parts count toward
  58,422 triangles, near the 60k cap; later detail must replace geometry.

The complete source make/check and independent 139-mesh repeat comparison
pass. Both parent/game curvature reports retain raw crossings with no crossing
outside their declared construction zones. All 24 renders share the measured
source hash; all 42 review views were inspected. The pickup comparison remains
454 unchanged source meshes and 150 unchanged GLB accessors, embedded maps and
graph, with byte-identical fresh exports. No kit or sedan modules changed.

Stop at this requested source checkpoint. The remaining visual faults and
failed overlay tolerance mean this is a review candidate, not accepted form.
Do not open interior, underbody, optics, paint, UV/bake/export or LOD work.

# Sedan form round 4 — character and construction

This is the requested source form checkpoint. No sedan delivery, optics,
interior, paint, wear, UV, bake or motion approval is implied. The accepted
pickup generator and delivery branch remain independent.

## Pass 1 — reject a dressed-up flat tail and thin lamps

Color/value first: the four manufacturer-class stock photos use the white
studio background as the neutral (unit RGB gains). Silver and black paint
are not clay-albedo targets. Opened the four raw photos, the previous round's
handoff images, every new clay/stripe preview and all four calibrated neutral
pairs in `renders/sedan-r4-pass2/`. Earlier lighting/allocation experiments
are in `sedan-r4-pass1/` and `sedan-r4-pass1c/`. Cycles lighting initially
washed out the clay and reflected a white card over the whole windshield;
reject that presentation, lower the exposure and suppress the diagnostic
opaque window's specular response. No paint-match claim.

- **Side:** the broad wall is now a crown, and there is a clear shoulder-to-
  sill gradient. The low die hollow/crease is still too broad: a 36 mm normal
  interval turns only about 3.5–5.5 degrees. The actual front lower door is
  about 87 mm inside its shoulder, beyond the requested 50–80 mm. The three
  section rays are stricter evidence than the brighter door highlight.
- **Front:** the blank painted wall has gone; the upper grille, lower intake
  and corner pockets are real skin cuts with inward returns. Reject the
  headlamp's doubled-back guide near x=840 mm: its inflated 803 mm path is
  not a long, fair lamp. Correct that guide and keep the outer tip rising.
  The fender ridge is too low in two sections (5–10 mm), and the hood's
  corners still look too busy. The narrow central opening/bar treatment is
  more resolved than round 3 but remains generic beside both production cars.
- **Rear:** the raised deck helps the profile but the lip still reads too
  shelf-like at its ends. Lamp outlines are rectangular in rear projection;
  the dark form blank cannot stand in for the eventual original optic graphic.
  The plate pocket adds depth, but the lower painted expanse is too plain.
  Move the bumper top to 620 mm and keep the diffuser inside the molding.
- **Stripes:** broad doors are smoother and carry a real gradient. Reject the
  remaining lower-rear tooth. Extra samples from round 3 were concentrated at
  the side tangent, rather than the tighter front/rear plan turn. Fit a finer
  regular control net before subdivision, and place game samples at the turn.
  Keep the same procedural reflection-band diagnostic; do not hide the tooth
  with material roughness or a different light pattern.
- **Mirrors/package:** both mirrors are now visible and supported by stalks.
  Their oval housings still look like form proxies. The accepted tires,
  tracks, arch gaps, roof peak, rake and tumblehome remain the package basis.

Actions: support the lower die line before the long sill return; shorten its
broad transition; retain a slight concave run; reduce hidden well/liner
allocation to fund the silhouette. Raise the fender crown, remove the lamp
backtracking, and check the same actual end numbers again. The first 61k
allocation and the 55,418-triangle support experiment are rejected. No budget
limit has been raised.

## Pass 2 — final character, with the remaining misses explicit

Color/value first against all four final Camry/Accord clay and striped pairs:
the photographic white studio backdrops remain the neutral, with unit RGB
gains. Neutral clay is not a paint-albedo match to the silver Accord or black
Camry. Cycles hero foreground p1/p99 luma is
0/238 front and
0/225 rear; no opaque foreground channel reaches 255.
Cavities remain deep, and the raking side retains a shoulder-to-sill gradient.
Opened every final view in the 37-view contact, all eight paired comparisons,
the sections and curvature plots; front/rear clay and key pairs were also
opened at full size. Rejected intermediate views are retained in the six
`build/sedan-round4/all-intermediates-*.jpg` review pages.

- **Side:** actual mid-front-door / B / mid-rear-door shoulders are 910 / 921 /
  932 mm high. Upper inward lean is 20.2–21.2 degrees; lower lean progresses
  from 4.6 just below the shoulder to 16.3 / 15.3 / 13.1 degrees low on the door.
  Lower-edge insets are 80.4 / 75.0 / 70.1 mm, then 40.9 / 45.4 / 49.7 mm
  more sill tuck. The soft crease turns 11.2 / 10.7 / 9.7 degrees over the
  recorded 80 mm interval; 50 mm chords find 1.7–1.8 mm inward hollows. These
  sections replace the broad chord that incorrectly called the old wall fair.
  The low line and shoulder now carry separate value bands. A small abrupt
  grazing-band change at the front lower-door/sill junction still reads CG.
- **Fenders:** same-height wheel/door rays measure 33.3 / 28.2 mm swells.
  Crown rises are 19.0 and 14.8 mm behind the lamp, but only 3.9 mm close to
  the A-pillar (y=−1.10 m). That last crown blend still misses 10–30 mm and
  weakens the hood's recess there. It is printed in the report, not gated away
  by selecting only the successful stations.
- **Face:** the grille, lower intake and corner pockets are actual openings,
  with inward returns and broad original blades. Mouth-to-bed rays measure
  64–67 / 60–62 / 50–52 mm; eighteen separate axial rays find no painted skin
  across their centers (including the rear pockets). The rising headlamp
  paths are monotone at 746 mm, about 110 mm tall, with 268–292 mm returns.
  The top follows the shut-line arc, and the fender ridge separates from the
  hood. The simple parallel bars and small regular corner pockets still look
  generic and cheaper than both photographed production faces. Optical
  internals and their lit response remain later work.
- **Rear:** the tapered wings now extend across the lid cut and corner rather
  than two rectangles. The deck is 366 mm long; its crest is 1111 mm, with a
  measured 21.3 mm kick over the extrapolated adjacent deck. All fixed tail
  and quarter areas retain the same parent; there is no separate tail patch.
  The 303.4 mm local plan circle retains the approximately 305 mm draw. The
  lower fascia seam is at 620 mm, and the molded diffuser is 11–14 mm behind
  its mouth, within the fascia outline. The broad painted bumper remains too
  plain beside both photos. The last rear clay revealed that the old temporary
  cavity closure, not the recessed diffuser bed, still projected as a flat
  plate underneath. Its box is now inboard of the wheel wells and forward of
  the tucked tail, with 127.5 mm actual axial tire clearance.
- **Profile/overlay:** the first final candidate still missed the C-pillar by
  111 mm even though its deck had risen. Reject that partial correction and
  raise the C-pillar control stations themselves. Final held-out deviations
  are −32.9 mm C-pillar and −35.3 mm deck; every recorded upper silhouette
  holdout is within 35.3 mm, with ±16.5 mm pick uncertainty. The lower-end
  request is not met: bumper tangents are +132.9 mm nose / +78.2 mm tail in
  the unchanged wheel-center-only orthographic overlay. Lower nose/chin are
  +41.2 / +25.9 mm; lower tail/under-tail +41.2 / +2.9 mm. The accepted 4900 mm
  envelope and 975 / 1095 mm overhangs remain held. Near-profile perspective
  is an uncertainty; it is not used as a pass flag, nor is the outline fitted
  or warped to hide the miss.
- **Stripes/fairness:** refining only the plan tangent did not remove the
  lower-rear tooth. Screen rays identified it on actual fascia around y=1.9 m,
  forward of that region. Local game-chart refinement in both directions
  removes the large zigzag while coarser central-canopy chords fund it. The
  front's painted corner bands are more coherent after the real cut openings.
  Fine grazing waviness remains at the lower rear; this is not a global
  Class A claim. Both parent and game checks retain every raw sign crossing.
  Documented zones cover the die hollow, rocker/shoulder, fender-crown/hood
  transition and lower fascia roll, including the parent's z=371 mm roll.
  None of those plots is substituted for the photographic/stripe critique.
- **Mirrors/greenhouse:** 250 × 204 × 157 mm housings span 2110 mm and are now
  visible in front and rear three-quarters. Stalks seat on the front doors.
  The oval caps/panes and regular window corners remain obvious form proxies.
  The six-light layout, roof peak, windshield rake, tumblehome, tires, tracks
  and 40 mm arch gaps remain the held package.

The original grid projection at the tapered rear-lamp tips produced tiny folded
cells and non-manifold six-face edges. A 0.1 mm weld was insufficient. Replace
the optical blank topology with a constrained triangulation in the continuous
parent chart before gauge closing. Both source densities then pass closed,
positive-volume audits. This is a construction fix, not a loosened audit.
Recess normals also exclude flat gauge rims: their tangent normals initially
gave an invalid negative diffuser-depth result. Independent outward smooth
skin normals give the 11–14 mm bed recess; separate rays still prove the holes.

Final proof: `make -C cars BODY=sedan WIDTH=1600 SAMPLES=40`, `make -C cars
BODY=sedan check` and `make -C cars BODY=sedan fairness` pass. Actual game source
is **52,628 triangles**, with five diagnostic clay materials and zero
image textures. Both densities, real openings/depths, end ranges, sections,
source scale/normals, calibrated camera projection and repository checks pass.
There are 22 rendered views with one source hash and a 37-view contact at
`renders/sedan-round4/contact.jpg`. The final two source blends and all generated
images remain ignored; no checkpoint docs JPGs are committed.

Independent one-thread regeneration matches all 112 meshes' positions,
polygons, corner normals, transforms, materials and parents exactly. Fresh
pickup generation matches all 454 meshes; all 150 re-exported accessors,
embedded maps and graph match, and the complete 11,530,736-byte GLB retains
SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
This last check proves serialization/byte preservation; the sedan rays and
closed-surface tests prove its source construction. Full mechanical clearance,
UV/bake, finish/wear and sedan GLB validation remain deferred. No kit changes.

The most important remaining issue for the next form decision is the raw
lower-bumper overlay miss while keeping the accepted envelope/tangents. The
near-A-pillar crown, plain fascia lands, mirror proxies and fine grazing bands
also remain weaker than desired. This checkpoint stops here.


# Sedan form round 3 — one fair parent

This source checkpoint supersedes round 2's surface judgement. The earlier
claim that its broad stripes were fair was too lenient: the hood pooled,
fascia corners zigzagged, and the rear still read as a box. Its measured end
numbers and accepted package remain targets, not evidence of fairness.
No sedan delivery, material, wear or motion approval is implied here.

## Pass 1 — reject the first pole-free sheet

Color/value first against the silver Accord front, black Camry rear and Camry
profile: neutral gray clay must retain dark glass, wells and intake locators.
The stock photographs' white backgrounds are the balance neutral, with unit
RGB gains. Their silver/black paint is not treated as the clay's albedo.
Opened the three rejected round-2 stripe images and rear clay at full size,
the raw photographs, and the complete first replacement views.

Evidence: `renders/sedan-r3-pass1/`, `sedan-r3-pass2/`, `sedan-r3-pass4/`
and `build/sedan-round3/all-previews-0.jpg` through `all-previews-3.jpg`.
The sheets include every rendered intermediate, not selected successes.

- **Package/stance:** the envelope, wheelbase, tracks, 235/45R18 rolling
  envelope and 40 mm arch gaps remain fixed. Early mesh bounds show that
  subdivision rounding can still lose millimeters; recipe constants are not
  reported as measured geometry.
- **Hood:** removing post-subdivision end projection immediately improves the
  broad crown. The first edge/corner distribution still produces a false
  ridge and a knot where the fascia rows enter the fender. Reject it.
- **Front:** a single rectangular sheet can fold over the nose without cap
  poles, but nearly parallel longitudinal and cross rows create an unstable
  chart near the corner. Its bands still change direction abruptly.
- **Doors:** the requested concave run below the widest shoulder is present,
  but game reduction and changing row spacing leave waves. A few broad bright
  bands do not excuse those waves.
- **Rear/deck:** the first corner tangent lies too far aft; measured rear plan
  sweep is only about 70 mm. The deck still meets an almost flat tail face.
  There is a visible pinched transition at the quarter's top.
- **Canopy/wheels:** the accepted side profile/rake and wheel package should
  not be altered to rescue the ends. Their plain glazing and wheels are form
  proxies; they cannot conceal a wrong stamping.

Action: fit one continuous waterline/cover section family to the **control
net**, before final Catmull-Clark evaluation. Spread the end-to-side chart
through the quarters and retain a regular quad sheet. No evaluated vertex
projection, separate end volume, cap grid or analytic replacement normal is
used. The exported game-stage normals come from the evaluated parent itself.

## Pass 2 — reject collapsed reflections and damaged boundaries

Color/value first: striped diagnostics use a neutral substrate and procedural
black/white latitude or azimuth bands. Keep the deep values and highlight
rolloff; do not brighten the clay to imitate the silver photograph. Viewed
all pass-5 through pass-13 renders in their sheets, with the significant hood,
front/rear stripe and plan views also opened individually against both makes.

- **Hood/front:** a fair shallow crown and supported paired draw lines remove
  the leading dent. Piecewise fascia controls still concentrate curvature at
  their joins. Replace them with smooth positive-curvature center sections;
  the accepted height, rake, tuck and plan measurements still have to pass.
- **Side/arches:** the broad swells now read over each wheel. QEM reduction
  treats a shallow door as almost planar and removes the vertices that carry
  the changing reflected normal. Its large polygon-shaped highlights are
  unacceptable even while position error and the triangle budget pass.
- **Panel cuts:** a planar boundary dissolve cuts chords across curved hood
  and deck corners. The resulting triangular holes are visible in plan. The
  first replacement reduction is rejected rather than hidden with dark glass.
- **Rear/canopy:** a height-only rule mistakes low backlight corners for the
  body side and moves them outward. Protect the complete accepted canopy
  chart, not merely points above a height. Refit its transverse crown without
  changing its center/side silhouette. This removes the false corner humps.
- **Construction:** trim wheel openings on the open fair sheet, then close
  the gauge. Split point-touching sheet fans before Solidify; a four-face edge
  along a gauge rim is a real topology error, not a tolerable audit exception.

Action: resample the evaluated parent on a feature-aligned quad grid, retain
its extrema and normals, then make physical panel cuts. Exact 4.5 mm door cuts
replace station-dependent setbacks. Trunk side/bottom reveals align with its
split lamp pieces. The final reduction does not collapse a whole door into
large triangles. Source evaluation uses one CPU thread: an independent threaded
run exposed last-bit vertex/normal differences and one changed locator triangle.

## Pass 3 — both makes, curvature and the driver's hood view

Color/value first against the four calibrated neutral/striped pairs in
`renders/sedan-round3/`: the original clay's doors were too dark to judge well.
The balanced Workbench studio makes their gradient readable without changing
the body albedo or lifting the cavities. White photographic studio backgrounds
remain the neutral reference, with unit gains. No paint or used-car wear match
is claimed. Opened the complete contact and both makes' front/rear pairs.

- **Hood:** all three transverse sections remain convex, with localized
  curvature concentration at the two intended draw lines rather than pools
  or alternating dents. The driver's-eye reflection strip is continuous.
  It isolates the actual hood at a plausible eye because this form gate has
  no interior or transparent glazing. No smoothing shader replaces the mesh.
- **Front:** its measured plan sweep remains about 317 mm at x=850 mm. The
  turn under each lamp flows into the fender, with a roughly 386 mm local plan
  radius. The fascia is still plain beside both production photographs: the
  grille/intake/DRL locators lack the later molded seats and optical detail.
- **Doors:** the shoulder is the widest part of the section. A shallow concave
  run leads to the rising lower character line and recessed rocker. Horizontal
  and vertical bands now run across the four doors without the old repeated
  waves. The 7.8 mm mid-door chord deficit is a section
  measurement, not an artistic fairness certificate.
- **Fenders/wheels:** same-height mesh rays measure
  33.9 / 29.9 mm front/rear swell over the door.
  The swells blend into the body; they are not attached annular flare strips.
  The unchanged tires retain 40 mm crown clearance and actual inward arch hems.
- **Rear:** the local three-point radius is 305.1 mm, within 250–400 mm.
  The tail is convex across its width, with a shallow upper lean and a lower
  tuck. The crowned deck rolls into the quarter without the old corner humps.
  Its trailing edge is sharper, and the lower reveal gives the lid a coherent
  cut through the upper tail panel. Its broad plain lands remain less resolved
  than the Accord and Camry, even though their section is no longer a box.
- **Canopy:** the original six-light profile, fast windshield and tumblehome
  stay. The roof/pillar/window corners remain unusually regular compared with
  the photographic trim. This is still the least natural part of the upper form.

The plots sample five body stations plus three across each cover, on both the
unseparated parent and actual game skin. Cuts/part boundaries split derivative
runs; inward gauge faces and flat rims are excluded from an outer-skin curvature
measurement. Shaded zones explicitly mark the rocker, lower draw, shoulder,
bumper roll and deck edge. There is no unclassified sign reversal in those
sampled runs, and no hood/deck reversal away from cuts. This finite sampling
and the stripe views support one another; neither proves global Class A fairness.

## Pass 4 — actual apertures and the reproducible checkpoint

Color/value first: the inherited lamp locators sat on painted skin, so they
could hide an uncut face. The final cut gives them a real dark edge and recess,
without painting fake gaps into the material. The first projected polygon had
jagged rims and too many fragments; reject it. Fair the authored locator outline
in the parent's chart, offset it in the tangent plane, clip the already fair
skin, and close its gauge afterwards. The final local cuts preserve the parent
curvature and stay within the unchanged triangle budget. The complete new clay
views are in `renders/sedan-apertures3/`; finals are rebuilt in `sedan-round3/`.

All six lamp pieces now sit behind actual apertures. Eighteen center rays pass
through the lamp footprint without finding painted skin in the tested interval.
The black grille/intake/plate/handle locators remain form proxies; there are no
optical internals, grille wells or finished fittings at this gate.

## Pass 5 — inspect the lowest corner at both densities

Color/value first: retain the same reflection contrast while comparing the
1200 px dense-source and game views in `renders/sedan-density-check/`,
`sedan-density-game/`, `sedan-density-game3/` and `sedan-density-game4/`.
The dense source is cleaner at the lowest rear corner; the game grid still
shows small grazing-angle ripples. Additional longitudinal samples alone do
not fix them. Concentrate transverse samples in the corner as well, funded
by simpler temporary dark locator grids. The extra columns stop at the rear
chart, using a stitched transition instead of wasting them across all doors.

A hidden-gauge dissolve across the thin doors is rejected: its inner chords
cross the 0.9 mm outer sheet and give negative volumes despite closed topology.
Keep the steel backs unchanged. Restrict the reduction to the molded fascias,
with a construction-appropriate 3 mm nominal wall. Centroid and edge-midpoint
probes reject any reduced back that comes within 0.4 mm of the outer skin.
Earlier rear-back reductions fail that probe and are rejected. The final
front/rear back probes retain at least 2.20 / 1.77 mm inward depth at the tested
points, and both reductions pass. The source audits remain positive and closed.
The dense/game corner comparison is stricter evidence than the eleven sampled section checks.

The final hood and door runs are substantially cleaner than round 2. Fine
ripple remains at the fascia corners under grazing bands, most visibly at
the lowest rear corner. The plain fascia and regular upper window corners remain weaker than the photos.
The underside's band convergence appears at both densities; the small adjacent
game-mesh ripple is not dismissed as the same effect. This checkpoint is not
a claim that every reflection has reached production Class A surfacing.

Opened every final JPG in `build/sedan-round3/review-verified-0.jpg` through
`review-verified-4.jpg`, with the clay three-quarter views, rear stripes and
curvature plots also inspected at full size. All twenty render metadata entries
match the final source hash. Front/rear clay foreground 1st/99th-percentile
luma is about 8/151 and 6/128; no foreground channel clips at 255. Cavities stay
dark, and the body gradients remain visible. These are clay tonal checks,
not final paint albedo validation.

Proof from the final scripted build:

- `make -C cars BODY=sedan WIDTH=1600 SAMPLES=40` and `make ... check` pass:
  both density audits, positive closed source gauges, normals, no zero-area
  triangles, budget, accepted envelope, all 23 end ranges, swells/corner radius,
  real lamp openings, independent camera projection and repository rules.
- `make ... fairness` passes both parent and game sections. Raw positions,
  normals and signed curvature remain in `build/sedan/curvature.json` and
  `parent-curvature.json`; the paired plots are in the render folder.
- The control sheet is one connected component with 29,376 quads and
  valence four at every interior vertex. The final subdivision is evaluated
  after fitting; no post-evaluation end projection remains.
- Independent one-thread regeneration matches all 94 meshes' positions,
  polygons, normals, transforms, material names and parents exactly.
- Fresh pickup generation matches all 454 source meshes. A single-thread
  re-export matches all 150 accessors, maps and graph, and the complete
  11,530,736-byte GLB retains SHA-256
  `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.

The overlay still has a roughly −94 mm deck/spoiler difference, +33 mm hood
lead, −21 mm hood middle and −9 mm cowl; front/peak roof are +14 mm and aft roof
−12 mm. Pick uncertainty is ±16.5 mm, with residual near-profile perspective.
The roughly 1040 mm original lip follows the held spec rather than the higher Camry SE
spoiler. The four chassis camera RMS values stay 5.76 / 5.30 / 11.07 / 8.76 native
pixels. They do not certify the body silhouette or identical styling.

Remaining weaknesses are the plain fascia/pocket treatment, regular window and
C-pillar corners, grazing ripple at the fascia corners (worst at the lower
rear), and the deck/spoiler mismatch. Fine trim, optics, interior, underbody, real paint/wear and moving-part clearance remain later work; none is
claimed done. No kit changes, no sedan GLB and no committed checkpoint images.
The later detail pass must replace the temporary locator allocation to stay
inside 55k. The source checkpoint stops here.

# Sedan form round 2 — the ends

This gate supersedes the sedan form judgement at `402318a`. It is source clay,
not a finished car or a sedan GLB. The original critique and pickup history are
retained below. The accepted cabin/chassis package moves forward together by
90 mm to correct the overhang allocation; its doors, tracks and tire clearances
retain their dimensions. Only the requested front roof transition changes.

## Pass 1 — reject the first rebuilt ends

Evidence: `renders/sedan-r2-pass1/` through `sedan-r2-pass4/`, compared directly
with the Accord front and Camry rear stock photographs and the Camry profile.
White balance reference: white photographic studio background, unit RGB gains.
These are neutral clay tests; no factory-paint color claim is made.

- **Color/value first:** the dark glass and intake blanks give useful cavity
  contrast, but the body still has a chalky, simple reflection beside the silver
  Accord. Clay is appropriate here; a material change cannot repair the form.
- **Proportions and stance:** shifting the axles and cabin together corrects the
  wrong front-longer allocation. Tires still fill the arches with the accepted
  40 mm crown gap. The first nose loses too much length to subdivision rounding;
  measuring only the recipe would miss roughly 60 mm of lost overall length.
- **Hood and front panels:** the broader plan arc is better, but an inverted
  shoulder row and tightly clustered end support loops make a knot at the lamp
  corner. The upper face is still too soft in one pass; the lamp is 742 mm long,
  only 118 mm tall and returns just 89 mm. Reject against the requested envelope.
- **Front highlight flow:** the stripe fans remain conspicuous. Relaxing the
  cage alone does not solve them. The cap/side chart must be made fair, rather
  than approving the good center section and ignoring the corners.
- **Rear panels:** the reverse taper is gone, but the actual sweep is 442 mm at
  x=850 mm, almost twice the requested rear sweep. The deck measures only 318 mm;
  the upper panel leans 18 degrees. The center section alone flatters the result.
- **Side panels/wheels:** the lower draw rises correctly and the wheel package
  is retained. The rear quarter still lacks a broad, continuous haunch; its tight
  corner turns interrupt the reflection instead of blending into the quarter.
- **Roof:** the front overlay holdout remains above the Camry. Correct it along
  the accepted windshield direction so the rake does not drift.

Action: a rounded elliptical fascia volume constrains the unified subdivided
cage. A radial projection from inside that volume replaces nearest projection,
which folded adjacent rows over the hood/fascia junction. The profile, top crown
and underside tuck become one smooth surface before panel separation. Restore
normals from this same continuous sculpt, and split rear lamps at the lid cut.

## Pass 2 — final source checkpoint, both makes and both ends

Evidence: every view in `renders/sedan-round2/contact.jpg`, with the full-sized
clay/striped pairs, orthographic plan, side overlay and four actual section cuts
opened for review. Front and rear are each compared with both the Accord and
Camry, in the same calibrated framing. Backdrops are the white-balance neutral
(unit gains); the photographs' silver and black paint are not treated as clay.

- **Color/value first:** neutral clay has deep glass/intake/wheelwell shadows,
  rather than the first checkpoint's pale blocks. Opaque foreground luminance
  p1/p50/p99 is 4/43/158 front and 3/29/102 rear (8-bit display values); no channel
  clips. The rear clay is still quite dark beside the silver Accord. Its side
  curvature is easier to judge in the complementary striped view. This gate
  supplies no paint/albedo or used-car wear claim.
- **Proportions/stance:** actual full bounds are 4900 × 1850 × 1449 mm, with
  2830 mm wheelbase and 975 / 1095 mm overhangs. The previous front-longer mistake
  is removed. Both references still look more detailed and visually lighter
  around the sills; that is partly their narrower trim and real cavity openings.
  The regular greenhouse corners remain a visible procedural tell.
- **Front plan and fascia:** the 314 mm sweep now runs across the face and turns
  continuously into the fenders. It no longer presents a straight plank with
  corner radii. The centerline tangent is at 484 mm; the upper face rakes 35.2°
  to a 746 mm hood edge set back 185 mm. The 189 mm chin tucks 119 mm. Compared
  with both photos, the fictional fascia still has too much uninterrupted plain
  land between its lamp and grille locators. It needs richer molded pocket
  construction at the later detail stage; the optics will not fix a wrong contour.
- **Hood/fenders:** the hood rises 10.5° to a 965 mm cowl, with 31 mm cross crown.
  The soft paired draws move outward toward the A-pillar feet. The leading reveal
  now follows the end arc. Broad bands are fair across the hood and fascia;
  highlights still gather tightly at the lamp/shoulder junction compared with
  the Accord's gentler draw. The form locators originally let paint poke through
  their chords. Local conforming subdivision removes those white tears without
  changing the body's sculpt or floating the whole lamp farther off the body.
- **Lamps/grille:** each headlamp measures about 696 mm along the actual sampled
  surface, 147 mm maximum aperture height and 225 mm return into the side. Their
  upper outline follows the hood reveal. The grille is a broad trapezoid above
  the black lower intake, with separate corner pockets. These remain dark
  locators, visibly simpler than real lenses and deep grille seats in the photos.
- **Cabin/roof:** the requested header adjustment follows the accepted rake,
  measured at 61.48° from vertical. B-pillar tumblehome measures 24.14°, within
  the requested class band and the photo estimate's uncertainty. The roof-front
  overlay holdout is now +14 mm, down from about +49 mm; peak +14 mm, rear roof
  −12 mm. The fixed quarter pane and accepted side-glass outline remain.
- **Side panels/highlight flow:** the shoulder is legible through the handles
  in both three-quarter views; the lower draw rises rearward. Door panels keep
  a broad outward crown and tuck into the rocker. The rear haunch has a broad
  reflection over the wheel instead of a separate swollen corner. The small
  lower corner transitions still gather the bands more tightly than production
  surfacing. The gross cap crumples are removed; this is not a claim that every
  highlight now matches an OEM stamping.
- **Rear plan/panel:** 238 mm sweep, 11.5° upper lean and a 602 mm bumper tangent
  replace the square vertical tail. The lower fascia recedes 176 mm to the
  diffuser at 300 mm. The wrap blends into the quarter without the old reverse
  taper. Its broad plain tail land still looks less resolved than both makes'
  sculpted plate recesses; that weakness remains visible in clay.
- **Deck/lamps:** actual center deck length is 373 mm, rising 5° to a 1043 mm lip,
  with 22 mm transverse crown. Lamps wrap from quarter to lid, with a real
  separated cut and correct parent ownership for the lid blanks. The lip is
  crisp in section but subtler in the clay rear view than the Camry SE spoiler.
- **Wheels/arches:** all four retain 40 mm crown clearance and the 235 mm tire
  width; tires sit close to the shoulders with actual inward arch flanges. Wheel
  and tire geometry is the accepted family method, 2404 triangles per corner.
  The sportier Camry wheels and Accord's smaller package should not be used to
  rescale this accepted tire choice.
- **Overlay limits:** worst sampled vertical difference is −96 mm at the Camry
  deck/spoiler; hood lead +33 mm, hood middle −21 mm, cowl −9 mm. Picks carry
  ±16.5 mm uncertainty and the near-profile photo retains perspective. The
  1043 mm original lip follows this brief's 1000–1050 mm spec, so the higher
  photographed spoiler is not silently adopted. The nose still differs in
  silhouette despite the corrected package; the 975 mm published front reference
  is 25 mm outside the brief's rough 860–950 mm photo estimate.

Proof: full `make BODY=sedan WIDTH=1600 SAMPLES=40` passes from scripts through
both-density audits, all 23 numeric end checks, independent Blender camera
projection, all renders/pairs and repository policy. Camera RMS, native pixels:
Accord front 5.76, Camry rear 5.30, Camry front 11.07, Accord rear 8.76. These fit
chassis anchors, not body shape; the extra two fits have visibly larger residuals.
All retained lamp samples are measured on the actual mesh (zero distance).
Game: 46,972 triangles; high: 373,984; four diagnostic materials, zero maps.
The planned 2048 set remains 16 MiB compressed with full mips. Independent sedan
regeneration matches all 94 meshes exactly. Fresh pickup generation and re-export
retain all 454 source meshes, 150 GLB accessors, maps and graph; the complete
11,530,736-byte GLB retains SHA-256
`f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
No kit changes and no sedan detail/delivery work beyond this checkpoint.

# Alder S240 sedan — source form checkpoint

The C150 pickup below remains accepted. This section is the second body type's
source form gate only. No sedan look-dev, wear, interior, underbody, atlas,
bake, GLB, final docs or motion-clearance certification is claimed.

## Sedan pass 1 — reject the end closures and artificial seam highlights

Color/value first against the silver Accord and black Camry stock photographs:
neutral gray clay is deliberately neither reference paint. Use their neutral
white studio backdrop for white balance (unit RGB gains), retain charcoal tire
and glazing proxies, and compare geometry and bands rather than brightening the
clay to match silver. All five `sedan-pass1` and `sedan-pass2` views were opened
in complete contacts; neither pass is an acceptable review candidate.

The roof peak, low hood and fast rear slope identify the class in profile, but
the independent end moldings leave square discontinuous walls. Top view exposes
the open corners. The first side has broad bright vertical bands at the door
boundaries: the sheet closing changed the smoothing fans despite the correct
pre-split normals. The black grille is a small rectangle in an otherwise flat
face. The first count is 46,504, spending 13,316 on the two inefficient caps.
Reject those caps and the apparent seam dents; dimensions alone do not rescue
this. The A/C-pillar transitions and lamp seats also need a continuous source.

## Sedan pass 2 — continuous corners, then reject the normal encoding

Color/value first against both makes: keep the neutral diagnostic clay and
unclipped stripe world. The two-color world is lighting equipment, generated by
nodes; it contains no reference image. Opened all seven `sedan-pass4` views,
including top, side and both full-size stripe directions.

The replacement cap grids now share the actual body-cage boundary vertices.
Catmull-Clark evaluates hood, sides, greenhouse, deck and both end caps together
before panels separate. This removes the disconnected bumper plate. Smooth
master normals transfer across the 4.5 mm shut lines after closing the gauge.
But the first stripe pass still bends sharply in broad strips beside seams:
edge-return faces remained in the outer skin's smoothing fans. Mark those
edges sharp and keep their normals geometric before restoring the outer field.
The rerender (`sedan-pass5`) removes these false vertical dents without changing
the dimensional targets. Both doors carry continuous broad bands.

Region critique: the stance and low arch gap read better than the pickup's
clearance. The hood is still too featureless beside both photos; the fascia and
rear are tall, square and too regular. Roof/glass boundaries are less rounded
than production glazing. Do not conceal those weaknesses with lamp details or
paint. The initial 220 mm C-divider is excessive; replace it with a short thin
post and a fixed quarter pane. Split the recessed rocker from the lower doors.

## Sedan pass 3 — calibrated photographs, construction and measured section

Color/value first: the silver Accord is brighter than clay, and the black Camry
carries a more complex studio reflection. Neither difference justifies changing
the neutral body or hiding lower-panel curvature. Opened all four raw stripe /
matched views in `sedan-pass5`, and both full-size composed photo pairs.

The kit fits five chassis anchors per view. Front Accord RMS is 5.76 native
pixels; rear Camry is 5.30 at 2100 px width. Two near hubs and contacts constrain
scale/stance. The Accord's obscured far-front contact is low-weight and has
larger uncertainty. These are chassis registrations, not all-body accuracy;
roof/deck/lamp and original overhang differences remain plainly visible.

Measured Accord B-pillar glass picks are back-projected through its calibrated
camera into a local y=0.20 m section plane. The class estimate is 23.97 degrees
from vertical, with about +/-4.5 degrees uncertainty for picking, camera/class
registration and unmeasured pillar rake. The neutral white backdrop is the
white-balance reference. This is an explicitly approximate photographic section,
not a manufacturer cross-section drawing. No picked outline becomes geometry.

The evaluated B-pillar cut measures 23.75 degrees. The front/rear axle cuts
intersect hood and descending deck/greenhouse respectively, so a full-height
side-glass angle is not invented there. Actual door rays show a 13.8 mm crown
above their lower/upper chord. All four tire/arch crowns have 40.0 mm clearance;
flanges run inward 18 mm, and dark inboard liners block daylight through the
wells. The side's lower die line now rises aft instead of remaining horizontal.
Front DRL and lower intake pockets are blocked only, with real recessed depth.
Wrapped lamp volumes follow the corner's local plan normal; optics are deferred.

The 44,454-triangle pass still facets the broad rear cap, so increase the master
sampling to two subdivision levels and reduce its interiors while preserving
all evaluated seam vertices. A subsequent restoration of the pre-cut master
normal field removes the aperture-induced cap bands. Do not relax the topology
or normal checks to accept them. All `sedan-pass6` and `sedan-pass7` clay views
were opened in complete contacts. The cap's planar character and unusually even
window edges remain artistic weaknesses to judge in the final set.

## Sedan pass 4 — reject invalid cuts and a misleading reflection dome

Color/value first: retain neutral clay, charcoal tires and deep cavities. The
white studio reference backgrounds remain the neutral balance. Full-size pairs
and the complete 16-view contact exposed radial bands over the end caps; they
were not acceptable as a fairness claim. `renders/sedan-cap-rejected/` preserves
the earlier comparison set. A rectangular cap grid removes the old converging
U strips and reduces redundant geometry, while shared evaluated boundaries keep
the corner attached to the body. Separate plan sweep and vertical face sections
avoid forcing all height variation to zero at the side corner.

Both-density builds also exposed an unstable exact swept lamp cut: it could
discard an entire high-source fender or quarter. The model now rejects that
condition explicitly during development; it is not allowed to pass as an empty
part. At this form gate, the final opening locators are conformed dark blanks,
including the grille/DRL/diffuser and lamps. Finished wells and optical internals
remain deferred. Their front faces need actual interior sampling: a single
non-planar n-gon chords through the body crown and disappears behind it. The
sampled blanks retain their outline without pretending to be detailed optics.
One-micron welding at the exact arch intersections removes four high-source
slivers; the unchanged audit tolerances still reject zero-area triangles.

The remaining radial fan was partly a diagnostic error: atan2(Z,X) put a stripe
pole along the front/rear axis. That environment can make a fair face look like
a pinched fan. Replace horizontal bands with arcsin(Z) latitude bands, leaving
the mesh fixed, and rerender both studio stripes and both calibrated pairs.
Vertical bands retain an independent azimuth mapping. The final horizontal
render no longer has those radial cap fans. Do not report the old dome's pole
as a measured surface defect or claim that cage changes alone fixed it.

## Sedan pass 5 — final form candidate, with remaining weaknesses explicit

Color/value first against the final Accord/Camry pairs in `renders/sedan-form/`:
neutral clay retains black tires, dark glazing and darker lower/cavity regions.
It is not silver or black paint look-dev. The white backdrops supply neutral
balance. The hero's foreground display luma p1/p50/p99 is 4.79/43.38/145.37;
rear is 3.79/30.07/117.22 on 0–255. Neither clips a channel to 255. About
15.9% / 26.4% of those foregrounds is below 25, excluding background and floor.
These are diagnostic image statistics, not measured albedos.

Opened every final view through the complete 16-image contact, then inspected
the two full-size photo pairs, both stripe directions, clay heroes, section
plot and overlay separately. These are all one current game source. The kit
independently verifies the fitted camera projections; the 5.76 / 5.30 px native
chassis RMS does not make the body a few-pixel match.

Region-by-region judgment:

- Proportion/profile: 4900.01 x 1850.06 x 1449.87 mm, 2830 mm wheelbase and
  1590/1600 mm tracks are measured. The 757.78 mm leading hood, 61.20-degree
  A-pillar and roof peak behind the B-pillar meet the requested language. The
  axle-scaled Camry overlay still shows a roughly 50 mm earlier/higher front
  roof transition and an 87 mm lower selected deck station (+/-16.5 mm picks,
  residual perspective and original styling). The 1043.79 mm deck crest meets
  the brief but is not a Camry replica. Keep these differences visible.
- Stance/arches: four 40.00 mm crown clearances and 235 mm tires read low and
  closely filled. Wheels sit about 12–13 mm inside the body's maximum shoulder,
  not deep under a pickup flare. Arch returns and inboard closures are present.
  Tread and brake construction remain the later shared-family detail stage.
- Section/side: actual B-pillar tumblehome is 23.75 degrees against the uncertain
  23.97 +/-4.5 photo estimate. The lower door tucks into a recessed rocker and
  carries a 13.76 mm vertical crown. The die line rises aft. Door bands now
  continue across the measured 4.497–4.502 mm gaps without the former broad
  artificial seam dents. Small compression remains at the sill/arch junction.
- Hood/roof/greenhouse: broad hood and roof bands are continuous. The A/roof rail
  and glazing corners are still unusually regular, with tighter stripe turns
  than the class photographs. The front roof transition is more upright/early
  than the Camry, and the C-pillar/quarter-pane termination is less fluid. The
  six-light choice is practical but does not by itself make these corners Class A.
- Front: plan crown and low wrapped lamp blanks are now clear; the low grille,
  lower intake and DRL pockets belong to one molded fascia. It remains plainer
  and squarer than either reference. The lower corner has localized stripe
  compression; the current broad smooth body should not be mistaken for a
  finished bumper tooling design. Opening blanks are intentionally temporary.
- Rear: lamps turn from the cap into the quarter, the deck has an integrated
  trailing crest, and the lower diffuser is located. The rear cap and bumper
  need more distinct production-like sculpting; the central plate/trunk field
  remains especially plain. Horizontal bands flow across the cap after fixing
  the dome, while corner/rail reflections still deserve the lead's scrutiny.

`make -C cars BODY=sedan WIDTH=1600 SAMPLES=40` passes the full source checkpoint,
including both-density kit audits, measured form checks, camera verification,
GPU-locked Cycles stripes/pairs, Workbench clay, all annotations and repository
policy. Game/high counts are **46,892 / 360,452** with four clay materials and
zero image textures. Game/high blends are about **1.1 / 6.1 MB**, ignored.
`build/sedan/form-check.json` contains every per-mesh/parent/category count.
The future three-map 2048 plan is about 16 MiB compressed with mips, not a
shipped allocation. UVs, underbody clearance, interior, finishes, moving-part
ownership/sweeps, baking, GLB and final delivery remain explicitly open.

Independent sedan regeneration matches all captured geometry, corner normals,
transforms, materials and hierarchy exactly. The pickup comparison matches all
454 source meshes, 150 GLB accessors, all three embedded images and the full
GLB bytes: SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
It re-exports accepted finalized geometry/maps; no GPU rebake is claimed. The
pickup README's previous byte count was 12 bytes stale and is corrected to the
measured 11,530,736; the GLB itself has not changed. No kit code or docs images
change. Nothing is needed beyond the lead's requested form review. Stop here.

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

Current evidence: source contact (`renders/lookdev/contact.jpg`),
used front pair (`renders/lookdev/aged_front-pair.jpg`),
used rear pair (`renders/lookdev/aged_rear-pair.jpg`),
front close-up (`renders/lookdev/front_detail.jpg`),
wheel close-up (`renders/lookdev/wheel_detail.jpg`),
five colors (`renders/lookdev/five-colors.jpg`) and
corrected stripes (`renders/lookdev-form/stripes_side.jpg`).
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
The primary evidence is the contact sheet (`renders/checkpoint/contact.jpg`),
front pair (`renders/checkpoint/match_front-pair.jpg`),
rear pair (`renders/checkpoint/match_rear-pair.jpg`), and the
striped side (`renders/checkpoint/stripes_side.jpg`).

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

Latest evidence: all views (`renders/checkpoint/contact.jpg`),
side overlay (`renders/checkpoint/side-overlay.jpg`),
rake measurement (`renders/checkpoint/side-rake.jpg`),
front pair (`renders/checkpoint/match_front-pair.jpg`),
rear pair (`renders/checkpoint/match_rear-pair.jpg`),
front stripes (`renders/checkpoint/stripes_front.jpg`),
side stripes (`renders/checkpoint/stripes_side.jpg`).

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

## Alder H120 — compact hatchback form checkpoint (in progress)

### Hatch pass 1 — package and four calibrated pairs

Evidence: `renders/hatch-pass3/`, including Corolla and Hyundai front/rear
three-quarter clay and striped pairs. Earlier `hatch-pass1` and `hatch-pass2`
clay turnarounds were rejected during construction: their high rear control
rows folded into fins at the glass/quarter junction. They are not candidates.

Color/value first: both stock-photo sets use a neutral white studio background;
the unobstructed white background is the neutral reference (unit RGB gains).
Silver metallic paint is lighter than the diagnostic gray clay. Judge the
position/width of gradients and the shadows, not absolute silver brightness.
Opaque dark glass is a deliberate form proxy; it does not excuse bad pillars.

- Profile/greenhouse: the roof is appropriately level and the rear overhang
  short, but rectangular quarter glazing and a broad rear glass make it read
  like an older small wagon. The rear glass is 1.62 m wide near its base,
  plainly wider than either photograph. Narrow the aperture on the fair sheet,
  taper the quarter-window termination and raise the rear belt slightly.
- Side: the shoulder and lower die line are visible at full-frame scale. The
  three door sections have progressive crown and a local hollow. Front lower
  edge inset is 81.4 mm, and sill return only 33.9 mm; correct those small but
  real section misses. The door cut arrangement is still too rectilinear.
- Front: the long rising lamps and recessed grille follow the family, but the
  painted band and tiny corner pockets read cheap/older. Increase the pockets
  and grille height. Hood highlights are clean across the broad center;
  compressed stripes at the fender/cowl corner need further scrutiny.
- Rear: the gate is upright, but the huge backlight and short lamps give the
  rear a featureless appearance. Split lamps and bumper plate pocket are real
  apertures. The quarter-to-glass strip is pinched; lower bumper corner bands
  also curl. Remove the projected lower tails and inspect the corrected parent.
- Mirrors: correct small door-mounted envelope, but the front cap's highlights
  form a conspicuous cross. It needs a fuller rounded wedge and smoother fans.
- Wheels/arches: 40 mm tire-top clearance, with inward hems. End fascia pieces
  still intrude into the lower arch silhouette; trim all adjacent skins with
  the same opening, not just the metal fenders.

Camera residuals are 3.59/2.95 px (Corolla front/rear) and 5.02/7.81 px
(Hyundai front/rear), in 2100-pixel-wide reference images. These are five
chassis-anchor residuals, not body-fit errors. Every anchor and residual remains
in `build/hatch/cameras.json`. Stripe and clay pairs were inspected together.
Source curvature has no unexplained reversal at the eleven sampled sections;
that does not establish fairness between those stations, particularly at the
D-pillar and bumper corner where the reflection test is stricter.

### Hatch pass 2 — sections, aperture construction and rear glazing

Evidence: `renders/hatch-pass4/` through `hatch-pass6/`, compared with the same
Corolla and Hyundai photographs and the four pass-3 calibrated pairs. White
studio backgrounds remain the neutral reference; no colored shade is sampled
as a paint albedo. The broad side now has a shoulder highlight and a descending
value gradient. The diagnostic glass remains intentionally opaque.

- Profile: hood lead, windshield rake and overhangs meet their dimensional
  targets. The level roof reads closer to the Hyundai than the Corolla. The
  rear spoiler still has an overly square end in the side silhouette.
- Side: the rocker correction brings the front-door lower inset below 80 mm
  and the further sill tuck above 40 mm. The soft die crease rises rearward,
  with a measurable shallow hollow above it. The door shut lines remain too
  vertical and regular compared with both photographs; this is a form weakness,
  not a missing handle that later detail will cure.
- Face: taller grille and corner wells now have depth. Their beds are behind
  actual holes; axial rays confirm that painted faces do not cover them.
  The upper grille still looks conventional and the narrow lamp tips need
  careful reflection inspection. Hood center bands stay calm.
- Rear: narrowing the glass fixes the excessive broad backlight, but the first
  taper leaves too much painted D-pillar. The lower bumper corners have tight
  stripe curls. A cut routine was accidentally retaining diagonal gauge rims
  as outer paint; tracking the actual outer face count fixes that construction
  error. This is a topology repair, not evidence of visual fairness.
- Wheels: arch trims now include adjacent fascia sheets. Tire/arch top gap is
  40 mm. Wheel detail is deliberately limited to the existing family form wheel.
- Mirrors: subdivision rounds the housing silhouette, but the nose still has
  an over-regular four-way highlight. It remains weaker than the reference's
  smooth, asymmetric molded cap.

### Hatch pass 3 — complete evidence set and failures retained

Evidence: all 22 renders and 41 review images in `renders/hatch-pass10/`.
All four Corolla/Hyundai front/rear clay and striped pairs were inspected.
The clay studio renders are too light relative to the dark Workbench pairs;
the next pair set therefore uses the same Cycles clay response as the studio
views. The white photographic backdrop remains the neutral; silver paint is
not treated as a target gray value. Deep openings are visible, not filled with
ambient gray, and the upper highlights retain shape.

- Profile: the raw wheelbase-registered orthographic overlays miss the requested
  40 mm envelope. Worst sampled deviations are 160 mm at the Corolla backlight
  and 113 mm at the Hyundai chin. Hood-middle differences are −81/−72 mm.
  Both photos show finite perspective; the manufacturer brochure illustrations
  are also not exact engineering outlines. Keep these errors visible. Do not
  shorten the numerically sourced package to force a photographic fit.
- Greenhouse: roof/glass proportions are less wagon-like, but the severely
  clipped quarter pane leaves a conspicuous painted patch. Retain a small rear
  quarter pane, as on the Hyundai, and widen the bottom of the rear glass while
  keeping its top narrow. This is the last glazing revision before review.
- Side: the actual three sections pass the requested lean, inset, sill and
  crease ranges. The simple shut-line layout still looks older/cheaper than
  either reference. Low sun reveals the broad lower-door crown rather than a
  flat plate, though the rocker termination is too abrupt.
- Front: the upper lamp sweep and fender crowns read correctly at distance;
  close views still reveal fender/cowl compression. The front-corner pockets
  have depth but could have more coherent transitions into the arch.
- Rear: high-frequency D-pillar wrinkles remain visible even in neutral clay.
  Denser rear sampling improves the stripe contour but does not eliminate the
  underlying problem. An uncut parent comparison isolates the extra sampling
  error. Inspection also finds a discontinuous fitting-ray origin at the
  side/end transition; replace that switch with a smooth blend in the control
  fit. Recheck sections and reflections after this structural change.
- Assembly/topology: two tiny, disconnected lower-door scraps fail the solid
  audit. They are outside the door stamping, below the rocker, not functional
  geometry. Remove disconnected door islands before closing the gauge; retain
  and report the removed area. The resulting pass-11 game solid audit passes.
- Mirrors and spoiler: both are dimensionally plausible, but their cap/end
  highlights still read more regular than molded automotive plastic. No badges,
  trim or paint are being added to distract from those weaknesses.

The parent and sampled game curvature checks pass at the eleven nominated
sections. Those finite tests did not catch the D-pillar between stations.
The reflection views and photograph pairs remain the deciding evidence.

### Hatch pass 4 — checkpoint handoff, form limitations explicit

Evidence: `renders/hatch-checkpoint/contact.jpg`, all 22 final renders and
all four calibrated Corolla/Hyundai front/rear clay and striped pairs, plus
the two unregistered rear comparisons and both raw side overlays. Every final
render and both parent/game curvature reports identify the same game source.
All rendered views were opened, including the seven reflection views and the
independent uncut-parent plots. The final geometry is in source commit
`2479d35`; this documentation records its review, not a later detail pass.

Color/value first: neutral remains the unobstructed white photographic studio
backdrop, with unit RGB gains. Neutral clay now uses the same Cycles response
for the four calibrated pairs and studio three-quarters. The opaque-foreground
display-luma median/p99 is 157.2/239.1 front and 164.2/228.9 rear; no foreground
channel reaches 255. Deep-shadow fractions below luma 25 are 10.2% and 8.6%.
Cavities stay dark and bright panels retain gradients. This is a clay tonal
check, not certification of real paint albedo or glass transmission.

- Profile: the level roof, short tail and steep glass now read as a compact
  hatch rather than a sedan deck or fastback. It still has a more rectangular,
  older greenhouse than either photo. The raw overlay **does not meet 40 mm
  everywhere**: worst 157.5 mm at the Corolla backlight, 113.3 mm at the Hyundai
  chin. Front bumper deviations are +107.8/+105.1 mm; rear bumper +62.2/+80.3 mm.
  Hood-middle differences are −80.8/−72.1 mm, roof peak +2.1/−6.2 mm. The two
  rear profiles genuinely differ, and finite camera perspective is also
  present; neither is claimed to explain away every discrepancy. Numerical
  length, wheelbase and overhangs remain held.
- Body side: three sections meet the requested shoulder, inward lean,
  progressive lower crown, hollow, crease turn and sill tuck. The raking view
  carries a readable shoulder-to-lower-door gradient. Vertical door cuts and
  the abrupt lower front-door termination remain conspicuously procedural;
  both photographs have more carefully resolved frame and sill transitions.
  Fender swell is 29.6/29.0 mm at the measured above-arch peaks. Its blending
  and highlight continuity still deserve examination between the sampled cuts.
- Face: actual crown rises are 14.95/21.61/10.12 mm at the three stations.
  A stronger local crown experiment was rejected when the **parent** curvature
  test found extra hood reversals; it was not excused by expanding the allowed
  crease zones. The final control fit restores the broad hood's calm curvature.
  The 691 mm lamps rise at their outer ends, and grille/intake/pockets have real
  depth. The grille's simple trapezoid and the pocket-to-arch junction still
  look older/cheaper than the references. Lamp corners remain too angular.
- Rear: the glass is now 1173/1411 mm top/base, closer to the Hyundai's broad
  base; the projected pillar band is 145 mm. Removing the invented painted
  patch shut line and smoothing the fitting transition removes the most
  obvious D-pillar creases in clay. The remaining broad pillar bulge still
  compresses stripes more than the reference's calm quarter turn. Fine lower
  bumper-corner zigzags and the exhaust-cutout transition remain visible in
  grazing reflections. The gate's large unarticulated painted area is still
  too plain; adding a badge is not a substitute for resolving its form.
- Mirrors/greenhouse: the rounded superelliptic caps remove the four-way
  diamond highlight. The measured 234 × 141 × 126 mm housings and 2039 mm total
  span are plausible. Their rear faces and the spoiler's square end still
  look regular. The small quarter pane avoids the earlier painted rectangle,
  but the side-window corners need more automotive shaping in a later form
  revision. Opaque glass is a stage proxy and must not conceal future interior
  or window-attachment work.
- Wheels/assembly: all four top gaps are 40 mm; tire/arch outboard extrema
  differ by only ±2.5 mm. The source solid audits pass at both densities after
  removing hidden disconnected door scraps. No moving-part clearance claim
  is made: these are closed form assemblies with provisional pivot groups.
- Budget: 53,384 triangles is within the 55k limit but too near it for the
  future interior/detail allowance. Rear sampling costs real triangles.
  Reduce hidden gauge backs and fixed-body overhead before adding those stages;
  do not silently raise the final budget.

`make -C cars BODY=hatch` completes the source build, checks, rendering and
41-image review. `make -C cars BODY=hatch check` covers both closed-solid audits,
measured proportions/sections/depths, all eleven game and parent curvature
stations, Blender camera projection agreement (under 0.0011 px), and repository
rules. Independent one-thread regeneration matches **all 131 objects and 118
meshes exactly**, including corner normals and transforms. The default pickup
comparison matches 472 objects / 454 meshes, all 150 GLB accessors, embedded
maps and graph, and the whole 11,530,720-byte GLB. Details and reproducible scope
are in [HATCH.md](HATCH.md).

The source checks pass; the pictures still show the limitations above.
This is the requested stop before detail, not final surface or delivery
approval. No kit change or additional installed tool is needed. A useful future
kit improvement would be a portable adaptive surface-sampling error report
that compares both positions and normals; the tight rear turn showed why
triangle count or sampled curvature alone is insufficient.

## Alder H120 — form round 2

### Round 2 pass 1 — perspective diagnosis and first end revisions

Evidence: `renders/hatch-r2-camera/`, `hatch-r2-shape1/`, `hatch-r2-shape2/`.
The first folder renders the original checkpoint through fitted profile
cameras before changing geometry. White studio backgrounds remain the neutral;
unit RGB gains, with no silver-paint albedo inferred from neutral clay.

- Cameras/profile: add the two near wheel centers and tread contacts to the
  kit's pinhole solver. Chassis-anchor RMS is 4.30 px Corolla / 4.31 px Hyundai
  at native 2100 px width. No outline landmark enters the fit. Four coplanar
  anchors leave lens/depth weakly constrained, so the approximately 70.8 mm
  estimates retain their stated prior; the millimeter comparisons are screen
  deviations at the body center plane, not recovered 3D surface errors.
  Perspective changes the diagnosis: the original gate is close to Corolla,
  while Hyundai carries its roof and upper tail farther aft. Follow Corolla
  at the rear greenhouse and Hyundai at the lower bumper where they disagree.
- Hood/header: both remain below the photographed outlines after matching.
  Move the straight windscreen forward 105 mm with its rake unchanged, and
  raise the intervening hood crown. The first revised overlays reduce hood/
  header misses to 39 mm Corolla / 27 mm Hyundai. No wheelbase or side-section
  scaling is used. A broad fit transition near the relocated cowl introduces
  extra curvature reversals; reject it and retest the parent surface.
- Front end: shifting the tangent to upper-fascia height while retaining too
  much of the old lower curvature over-tucks the chin. The first attempt misses
  by 239/201 mm, worse than the starting shape. Reduce that tuck before keeping
  the revision. The second attempt follows Hyundai's lower front within 7 mm;
  Corolla's deeper chin still differs by 50 mm. Lamp-top facets remain visible.
- Rear: a first narrow blend from the broader bumper into the gate produces a
  conspicuous reflection bullseye at the quarter. Spread that plan transition
  vertically; a checked silhouette alone does not justify the narrow blend.
  The gate needs a deliberate transverse feature and a central badge location,
  not just a dark plate opening. Plate location stays in the bumper, following
  Hyundai. The spoiler free edge also needs its own fair crown; sampling every
  root chord directly carries roof-corner facets into that edge.
- Mirrors: the supported trapezoidal cap reads as a wedge rather than an oval.
  Its flat rear pane and broad door sail are visible. Move the sail down into
  the door stamping and verify actual surface intersection; proximity alone is
  not a contact proof. The initial depth is 130.6 mm, so shorten the cap slightly.
- Diffuser/budget: axial projection holds its lower edge within about 1 mm in
  height; retaining its bed sampling removes the earlier decimation wrinkles.
  Fixed skins can omit their buried reverse faces without altering the painted
  sheet or the visible edge returns. The first allocation drops to 42,559
  triangles. Audit each new boundary's face role explicitly; do not treat an
  open fixed stamping as a closed solid or excuse a missing outer face.

### Round 2 pass 2 — surface repair, rear articulation and allocation

Evidence: `renders/hatch-r2-shape3/`, `hatch-r2-shape4/`, and the complete
intermediate set `hatch-r2-pass5/`. Inspect both stripe directions, white clay,
the four calibrated three-quarter pairs and both profile comparisons. Neutral
white photo backgrounds still use unit RGB gains. Clay is deliberately lighter
than the reference silver; judge highlight roll, cavity separation and form,
not metallic albedo. No new texture or paint approval is implied.

- Nose/hood: broad lower fascia and narrow lamps now read as a compact from
  the late 2010s. The original lower tangent was still just ahead of the upper
  one by less than a millimeter. Move that lower run back 1.5 mm, preserving
  package length, then measure the leading tangent independently. Denser local
  chart columns and reprojecting new cut vertices onto the fair parent remove
  the folded hood/lamp junction. Parent-normal gauge extrusion avoids collapsed
  corners introduced by averaged normals on narrow clipped triangle fans.
  The tip remains a very sharp styling event; do not hide it behind black optics.
- Roof/spoiler: lower the last 390 mm, increase rear glass rake, and give the
  spoiler free edge a continuous crown independent of the irregular root
  chords. The broad top highlight is cleaner. The accepted wide D-pillar still
  compresses stripes around its corner more abruptly than either reference;
  neither a sampled curvature pass nor smooth shading proves it perfect.
- Gate/bumper: a transverse stamped band and inset garnish establish the badge
  location between the lamps. The lower gate cut remains above the separate
  soft bumper crease. The wider lower plan improves the rear three-quarter
  compared with the early pinched corner. The narrow blend experiment made
  a conspicuous bullseye reflection and was rejected. Keep the broader blend.
  The intermediate garnish looked proud: its newly attached parent's matrix
  had not been evaluated before carving. Correct that transform dependency and
  add an independent world-guide/bounds check before accepting the recess.
- Plate/diffuser: retain Hyundai's bumper plate location, sharp pocket rim and
  overhead lamp. Diffuser projection is axial so the lower row stays near level;
  retain that bed's samples instead of decimating them. The lower edge no longer
  has the repeated wrinkles of round 1. The black plate pocket is still empty,
  so it cannot stand in for the later plate/optics construction.
- Mirrors: the trapezoid with rounded front sections now reads as a wedge and
  has a flat rear pane. A broad sail and shoe replace the stalk. Verify actual
  edge/surface intersections with the door and cap; five and twelve per side
  support the contact claim. The 228 × 136 × 128 mm cap does not break the
  hood/cowl silhouette. Its simple rear glass and thick dark shoe still look
  unfinished beside the photographs; finer trim belongs to the next stage.
- Budget: remove only buried backs from fixed stampings and keep all paint
  faces and visible gauge returns. Mark and audit the resulting inner boundary
  edges, rather than calling those skins closed solids. The intermediate local corner
  sampling and supported spoiler bring this intermediate form to 45,893 triangles, leaving
  14,107 beneath the finished-car ceiling. This is enough only with the explicit
  interior/underbody allocations in HATCH.md; it is not permission for unplanned
  detail growth.
- Measurement correction: locator guides sit above paint by 2.5–4 mm. Recess
  depths must start on the evaluated parent skin. Project mouth measurements
  there, retaining actual bed-ray hits, rather than reporting the locator offset
  as additional pocket depth. Recheck every opening with this corrected origin.

### Round 2 pass 3 — close front view rejects residual sampling pinches

Evidence: full set `renders/hatch-r2-pass8/` (formerly the candidate round-two
final), plus `hatch-r2-corner-diagnostic/front_clay.png` and the dense-source
comparison `hatch-r2-corner-high/front_clay.png`. Neutral studio light and white
background gains remain unchanged. The extra front render uses Cycles to
separate real shading faults from Workbench's cavity emphasis.

The front still has small darts at the inner lamp/hood intersections. They
are reduced in the dense source, so a general parent reshaping would attack
the wrong cause. Refine those local game cells in both chart directions;
transverse columns alone left long longitudinal chords. The broad grille bed
also shows diagonal dents absent from the high source. Its aggressive hidden-
bed decimation is inappropriate because the bed remains visible between bars.
Retain the crown grids for the grille, intake, plate pocket and garnish. Use
some of the saved back-face budget here, then repeat the full checks and views.

The whole intermediate car already reads as a contemporary compact hatch in
white clay, but calling the corner repair complete from its three-quarter view
would be lenient. The rear garnish now has a real recess and a separate lower
gate panel; its straight transverse treatment still looks more generic than
the sculpted Corolla. The D-pillar reflection compression and the very regular
side-window corners remain visible limitations. The smooth free spoiler edge
and level diffuser bottom are improvements in both stripe directions.

### Round 2 pass 4 — final regions and whole car in white clay

Final evidence: `renders/hatch-round2/contact.jpg`, all 26 native renders,
four front/rear three-quarter pairs in clay and stripes, two perspective profile
pairs, both original/current overlay comparisons, and game/parent section plots.
The four white-clay three-quarter pairs were also opened individually at full
size. The reference neutral remains unobstructed white background, unit RGB
gains. Front/rear clay heroes have display-luma P99 of **240.1 / 227.9**, zero
clipped channels, and **11.7% / 9.8%** of opaque foreground below 25/255. Cavities
have depth and the white highlights roll off; these are form materials, not
silver-paint or aging approval.

- Profile/ends: chassis fits remain **4.298 / 4.312 px RMS**. The regional table
  in HATCH.md reports both makes without silhouette fitting. Corolla governs
  roof/spoiler/backlight/gate: maxima **34.2 / 9.1 / 20.5 / 41.0 mm**. Hyundai
  governs lower front/rear bumpers: **4.5 / 31.6 mm**. Hood/header are within
  **38.7 mm** of both. The worst disagreement remains Hyundai's spoiler,
  **180.7 mm**; that make has a different upper-tail shape. Four coplanar anchors
  and the lens prior limit reconstruction accuracy. Do not treat a 4.3 px
  anchor fit as 4.3 px body accuracy or the projected millimeters as 3D errors.
- Hood/face: targeted two-direction sampling costs 220 triangles and removes
  the prominent inner-corner darts seen in pass 3. Restoring the four visible
  recess beds costs 768 and removes their false diagonal dents. Broad hood
  reflections flow continuously, including the driver's-eye lines. Very thin
  cut rims and the outer lamp tips still expose small angular marks in the
  severe front Workbench view; the A-pillar/cowl junction is less polished
  than the reference stampings. The broad face layout remains accepted.
- Roof/spoiler: the last roof section now falls toward the spoiler; measured
  backlight rake is **46.58°**, spoiler overhang **106.9 mm**. The supported
  free edge is smooth in both stripe directions. The broad accepted D-pillar
  remains too abrupt in reflection compression compared with both photos.
  Its white-clay highlight is cleaner but is not a claim of perfect fairness.
- Mirrors: supported door sails, wedge caps, flat rear panes; **228 × 136 ×
  128 mm**, housing bottom **994.7 mm**, span **2039.3 mm**. The housings remain
  below the side profile and actual surface intersections prove support.
  The dark shoe is visually heavy and the pane perimeter is still simple;
  these make the mirror look cheaper than either photographed assembly.
- Rear: the transverse garnish now follows the surface without the decimated
  pill-shaped bulge. Its bed is **6.0–7.1 mm** recessed. The lamps are **125.5 mm**
  at the quarter and taper to **51.7 mm** at their inner gate tips. Gate cut,
  upper bumper crease and lower turn-under read as separate construction.
  The bumper plate mouth is **319 × 166 mm**, actual depth **21.0–21.6 mm**, with
  its overhead lamp. The diffuser bottom varies **0.965 mm** across its sampled
  row; the old repeated wrinkle is gone. The lower bumper turns under over
  **144.1 mm**. The straight garnish and wide plain lower gate still read more
  generic and slightly older than the Corolla's shaped gate; fine angular cut
  marks below the lamps and around the reflector mouths remain CG tells.
- Whole white clay: it reads as a modern compact five-door, retaining the small
  package, filled arches and side gradients. It remains less convincing than
  the photographs: nearly rectangular side-window corners, very regular door
  cuts, opaque glass, empty optics and bare wheels simplify its appearance.
  The first two are form weaknesses; the last three are deliberate stage
  omissions. Do not use those omissions to excuse the remaining rim and pillar
  issues. No interior, underbody, hinges/struts, paint or baked export is added.
- Allocation/proof: **46,881 triangles**, down **6,503** from round 1; the current
  code removes **14,327** buried reverse-skin triangles and spends some savings
  on the visible repairs. The finished plan is **59,381 + 500 contingency**,
  under 60,000. Both density audits, measured shape/depth/contact checks, eleven
  game and parent curvature stations, all camera projection checks and repository
  rules pass. Independent regeneration matches **133 objects / 120 meshes**
  exactly. Pickup remains **472 objects / 454 meshes**, **150 GLB accessors**,
  embedded maps and full file hash identical. No sedan module or kit changed.

Commands completed for the final revision: the scripted game/high builds,
`make -C cars BODY=hatch check`, `make -C cars BODY=hatch render`,
`make -C cars BODY=hatch review`, Python compilation and independent deterministic
regeneration. Every final shot and game measurement report refers to source SHA-256
`a0e2e383288e48e09664ea760db2296e55449aaa4329940ac2c217a5e2194c55`.
This is the requested stop at the form checkpoint. The remaining visual misses
above are reported for the lead; no tool, kit change or permission is needed.

## H120 form round 3 — sculpture and reflection flow

### Pass 1 — stronger lines, rejected end treatment

Evidence: `renders/hatch-r3-pass1/`, `hatch-r3-pass2/` and
`hatch-r3-pass4/`; round-two views remain in `hatch-round2/`. The four
front/rear calibrated neutral pairs in pass 4 were opened beside both
photographs. Neutral is the unobstructed white studio background in each
reference, with unit RGB gains. This is neutral source clay, not a paint
albedo match; judge value gradients and geometry before optical detail.

The side's sharper shoulder and deeper rising lower hollow produce distinct
light/dark runs in the pairs. The first wheel-crown increase widened the body
beyond its accepted package, so reduce that increase and spend effort on the
normal transition and its game sampling. The raking side is still less sharply
articulated than either photograph. Do not accept the angle measurements as
proof that the side looks right.

The original flat garnish was removed and the gate itself drawn inward between
convex lamp corners. The first game tessellation flattened the proposed lip:
it did not achieve its requested overhang despite the parent controls. Add
samples across the hem and inset the bumper immediately below it. A black
lower center and slim vertical reflectors follow the Corolla rear photograph;
the Hyundai retains a broader painted bumper and horizontal reflectors. The
H120 keeps the accepted bumper plate location. The larger black area helps the
rear proportions, but conceals neither its painted-corner lumps nor the torn
marks below the lamps. Add an unpainted rear stripe diagnostic so black
plastic cannot conceal an unfair surface.

The crowned mirror outline and tapered nose are much closer to the Elantra
than the old flat-topped block. The sail is thinner and triangular. The new
cap is still rather egg-shaped beside the photograph, and the simple pane
perimeter lacks a production molding's crispness. Preserve the mounting and
2039.3 mm span while judging that tradeoff in the front view.

### Pass 2 — close views reject sampling and cut artifacts

Evidence: `renders/hatch-r3-pass7/` and `hatch-r3-pass9/`: front/rear,
rear three-quarter, raking side, front stripes in both directions and rear
stripes with the entire bumper reflective. These were opened individually.
The same neutral and lighting settings are retained. Highlights roll into
dark cavities; increasing exposure would only conceal the weak forms.

The gate now has a clearly visible concave run and a shadowed lower hem.
Measured lip projection is about 32–33 mm. The lower center follows the
Corolla's black construction while the corners remain painted. Nevertheless,
the taillamp surrounds have fine torn marks, the lower bumper corners ripple,
and the hood ends still have darts. The Corolla has a much cleaner single
lamp outline; both photographs have calmer bumper reflections. Reject these
candidates despite acceptable dimensions and triangle counts.

Tracing the generated triangles found several separate causes: a reversed
longitudinal control ordering at the front fender transition; narrow clipped
polygons triangulated after bending into space; and a lens disk using all its
projected guide points while its cut used only the original guide perimeter.
A first triangulation-order correction alone did not remove the visible marks.
A more complete chart-cut revision is therefore required, with coverage checks
rather than accepting a lower triangle count as proof of optimization.

Candidate 10's attempted chart retessellation lost large painted patches; the
side-ray check rejected it. The failed clay and stripe views in
`hatch-r3-pass10/` were inspected and are retained only as diagnostic evidence.
Subsequent candidates are checked for old-to-new chart coverage and topology.
No failed candidate is the checkpoint source, and no diagnostic image is
committed to `docs/`.


### Pass 3 — final pairs expose a second optical boundary

Evidence: the first complete `hatch-round3/` candidate (20), then
`hatch-r3-pass21/` and `hatch-r3-pass22/`. Front, rear and both three-quarter
clay views were opened individually. White balance remains the photographs'
white studio backdrop, unit RGB gains. The neutral clay has deep lower-body
and aperture shadows; there is no evidence that raising exposure would solve
the form problems.

- Side, against both makes: shoulder and lower line are visible in the neutral
  front/rear pairs and horizontal stripes. The lower hollow is clearer than in
  round two. However, the unchanged low-sun side is only modestly stronger;
  the broad door still changes value less convincingly than the Corolla or
  Hyundai. The roughly 24-degree shoulder number cannot be used to call that
  visual issue solved. Wheel crowns catch a narrow highlight but are quieter
  than the photographs' flared arches.
- Gate and rear construction, against both rear pairs: the inward central run
  and shadow under the hem replace the old flat rectangle. The Corolla's black
  center and tall corner reflectors are the chosen construction; the Hyundai's
  broader painted bumper is deliberately not followed there. The H120's gate
  scoop is more symmetrical and regular than either stamping. The straight
  gate cuts still make it look cheaper. The lower corner now joins the arch
  with a continuous broad surface, but stripes retain fine crowding at its
  bottom roll; do not describe the entire bumper as perfectly fair.
- Mirrors, against both front pairs: the crowned cap and rounded outboard end
  remove the rectangular silhouette. The thin sail meets the window corner,
  and the measured span remains 2039.3 mm. The cap is too egg-shaped beside the
  Hyundai's crisper teardrop; its simple pane edge still looks cheaper than
  both production mirror moldings.
- Face, against both front pairs: the curved recessed grille and surrounding
  lip now join the lamp ends closely. Its regular horizontal slats still read
  older than either reference's mesh. Broad hood bands are calmer, but the
  outer cowl/lamp transition retains small pinches in the front and both stripe
  directions. This is a form weakness, separate from the deliberately absent
  optical internals.

The nominal final candidate still showed a second dark edge above the rear
corner lenses and below the headlamps. Plotting the actual lens triangles and
cut boundaries identified a further error: a straight edge in the parent
chart curves in space. The body cut sampled that curve, while the lens used a
long endpoint chord. Its edge therefore sank through the painted surface.
Candidate 21 refined all lens triangles and cleaned the boundary but cost
49,572 triangles, so it was rejected. Candidate 22 refines only those boundary
chords whose midpoint error exceeds 3 mm. It spends 220 additional triangles,
keeping the total at 46,788. The rear now has a single outline in the straight
rear view; the large false wedges below the front lamps are gone. Small
angular tip marks and a dark sliver at the outer headlamp/hood junction remain.
Do not relabel those remaining artifacts as production detailing.


### Pass 4 — preserve the profile, retain the diagnostic limits

The full candidate-22 profile overlays revealed a regression that the package
bounds alone did not detect: the Hyundai rear-bumper maximum grew from 31.6 to
47.4 projected millimeters. Candidate 23's fuller plan recovered most of that
loss but also moved the upper gate. The final lower-plan adjustment blends out
before the backlight. Its native-size Workbench silhouette preview restores
31.6 mm at the Hyundai bumper while retaining the Corolla roof, spoiler and
backlight deviations. The final Cycles overlay is the authoritative comparison.
Both makes' profile images were opened; the cameras and held-out picks were
unchanged. This is a shape correction, not a calibration adjustment.

The final form is 46,843 triangles, leaving 38 within the accepted 46,881 form
allocation. Actual lower-gate lip projections remain 32.31 / 31.76 / 32.51 mm
at x = 0 / 250 / 500 mm. The center section is 24.18 mm concave over its 120 mm
chord; the transverse center run is 16.63 mm inside its 900 mm chord. Black
bumper widths are 1454 / 1384 / 1270 mm at z = 350 / 450 / 550 mm, with the
painted center band still 570–644 mm. The final tall reflectors measure about
19 × 198 mm in rear projection, within the photograph's measurement uncertainty.

The revised rear game section has a curvature reversal at z = 695.1 mm, above the
669.2 mm arch crown (HUB_HEIGHT + ARCH_RADIUS). The former Gaussian-support
estimate began at 707.7 mm and excluded the lower blend. The check now uses the
actual arch crown as the construction region's lower bound. Raw crossings,
points and normals remain visible, including this reversal. That revision does
not certify the reflection as fair and must not conceal the visible corner
weaknesses from pass 3.


The solid audit then rejected both gate-lens shells for negative signed volume.
The earlier per-triangle orientation correction was wrong: isolated flips in
curved chart chords made adjacent faces disagree. The final implementation
retains one coherent chart winding and creates the 1.5 mm inner gauge along the
parent normals instead of averaging the defective local fans. All six lens
blanks now measure zero inconsistent-winding edges and positive volume. This
changes the inner shell and winding, preserving the authored outer outline and
46,843-triangle total. The independent round-three report now retains those
actual topology and volume measurements.

### Pass 5 — final white clay and same-camera comparison

Evidence: all 27 native views in `renders/hatch-round3/`, the twelve calibrated
stripe/neutral pairs, `contact.jpg`, and the 23 comparisons collected in
`round2-round3-contact.jpg`. Every native view was opened, as were all six
neutral pairs and the individual before/after front, rear, raking side and
horizontal rear stripes. Cameras are unchanged. The final source is
`d6901bfc3cb9f97bf78a90580bec2972df16ec06f5356df1b7f2dc3d7fffc3da`.

Color/value first: reference neutral remains the unobstructed white studio
background, unit RGB gains. No factory-paint match is claimed for white clay.
The front/rear heroes have display-luma 99th percentiles of 240.9 / 227.9,
zero clipped channels, and 12.0% / 14.3% of opaque foreground below luma 25.
The grille, plate, underbody and gate lip retain deep shadow. The pale roof
does not need darker exposure to reveal the remaining geometric defects.

- Side: the front and rear pairs against both makes now show a shoulder edge,
  rising lower crease and concave run above it. Horizontal stripes change
  direction decisively at both lines. Measured normal turns are 23.79–23.89°
  at the shoulder and 12.78–16.20° at the lower line over 30 mm vertical spans.
  Wheel-crown turns are 13.62° front / 9.60° rear over 70 mm. These gains are
  visible, but the round-two/three raking comparison is only modestly better:
  the door remains broad and quiet, and the crowns lack both photographs'
  stronger rolling highlight. This remains the largest unmet visual ambition.
- Rear: both neutral rear pairs now show an inward gate run and a real lip
  shadow. The actual lip is 31.76–32.51 mm proud; the center section is 24.18 mm
  concave over 120 mm, and the plan run 16.63 mm over 900 mm. The Corolla-style
  black center reduces the broad painted mass; the central painted band is
  only 74 mm high. The center bumper reflections are calmer. In the unpainted
  diagnostic, however, the lower painted corners still crowd and kink near
  the arch/hem junction. The gate bowl is too symmetric and its corner stripe
  transitions too busy beside either real stamping. The single taillamp
  outlines are much cleaner in the straight rear view, with small extreme-tip
  angular marks remaining. These are not final-quality surfacing claims.
- Mirrors: the straight front comparison clearly replaces the old rectangular
  caps with crowned tops and rounded outboard ends, measured at 57.9 mm radius.
  The 2039.3 mm span and door-sail location remain. Both front photo pairs still
  expose an overly egg-shaped cap, a simple pane perimeter and a visible small
  mounting shoe. The Hyundai's tapered molding is more precise and looks less
  cheap. The sail is thinner, but the whole assembly has room for refinement.
- Face: the grille's 66.0–67.5 mm bed depth and proud curved frame read in the
  front pairs, with only 15.0 mm to each lamp. The large false wedges under the
  headlamps are removed. Broad hood bands are fairer in both stripe directions,
  but cowl/lamp-end pinches and dark slivers remain visible in the straight
  front and raking views. The regular slats and angular lamp ends still make
  the face look older and cheaper than either photographed car.
- Whole white clay: the package, short roof and rear opening still read as a
  compact five-door, and the rear now has distinct construction rather than a
  flat wall. It remains recognizably CG: regular window corners and door cuts,
  crowded D-pillar reflections, the symmetric gate scoop and the face/corner
  weaknesses above. Empty optics, opaque glazing, bare wheels and the absent
  interior are separate stage omissions; they do not excuse those form issues.

The final 2100 px Cycles overlays confirm unchanged selected Corolla
roof/spoiler/backlight maxima (34.2 / 9.1 / 20.5 mm) and Hyundai front/rear
bumper maxima (4.5 / 31.6 mm). The Corolla gate maximum moves 41.0 → 45.6 mm,
hood 36.5 → 38.7 mm and nose 6.8 → 22.8 mm. HATCH.md lists every region for
both makes, including the intentionally larger Hyundai upper-rear errors and
the approximately ±16 mm manual-pick uncertainty. The cameras were not refit.

`make -C cars BODY=hatch` completed successfully, including both source builds,
both density audits, package/character/round-two/round-three checks, eleven
game and parent curvature stations, camera verification, repository rules,
27 renders and the full review/comparison set. Log:
`build/hatch-r3-final4-make.log`. Independent factory-empty regeneration matches
all 132 objects / 119 meshes exactly (`build/hatch/determinism.json` under
`cars/`). The 783-ray normal-query equivalence check has zero position error
and maximum normal-vector difference 1.23e−7. These checks establish the
stated construction and repeatability, not visual approval.

Final form: 46,843 triangles; high source: 114,174; five temporary materials;
zero image textures; game/high files 1,059,996 / 2,427,423 bytes. The unchanged
12,500 future allowance makes 59,343 against the accepted 59,381 plan. The
fresh pickup source matches 472 objects / 454 meshes. Its re-export matches
150 accessors, embedded maps, delivery graph and all 11,530,720 bytes, SHA-256
`58661d0c2e11c2050e10677e12fabdf61570a3d25dc53837b485fee5c55a85ea`.
That check uses the accepted finalized source/maps and does not claim a fresh
GPU rebake. No shared family implementation, sedan module or kit file changed.

Stop here for the requested form review. No hatch interior, underbody detail,
UV/bake/export work or final docs images were added. No new tool or permission
is needed from the lead; the remaining visual misses above are the review items.

## Alder H120 — form round 4

### Pass 1 — diagnose the folds on the parent and game mesh

Starting point: `da466e3`, retained under `build/hatch-round3-baseline/`.
`main` was already merged. The round-three cameras, matte clay and reflection
stripe rigs are unchanged. New diagnostics live only in `hatch_*` modules.
The reference neutral is still each photograph's white studio background,
with unit RGB gains. Gray gloss is a form diagnostic, not a factory-paint
color match. The first gloss exposure was too pale; the final diagnostic
uses the same darker exposure for both revisions, without altering geometry
or the existing matte/stripe look.

The front pairs against both Corolla and Hyundai show the same failure:
creases near the outer hood/lamp junction break into short angular marks,
where both real stampings carry a continuous crown. The Hyundai's broader
hood roll is particularly unforgiving. The rear pairs expose a soft central
hollow with busy ends, unlike the Corolla's bounded gate recess or the
Hyundai's smoother convex gate. Those are geometric weaknesses, not missing
paint or optical detail.

Cause isolation used the uncut parent, the game skins, dense-parent stripe
renders, stored-normal inspection and actual face orientation. Three faults
were distinct:

- At the cowl/front-fender transition, the side controls swept longitudinally
  while their crown height dropped. Rows became almost parallel in YZ and
  folded back across each other. A separate 20 mm fitting-weight handoff
  displaced controls over too short a distance. The old parent had 1,049
  suspect faces in the tested cowl region, including almost reversed normals.
  Locally unswept rows and a 160 mm fitting handoff remove those parent folds;
  the corresponding diagnostic then found none. The windshield controls and
  its accepted rake are retained.
- At the lamp tips, the parent was fair but chart-space Delaunay triangles
  became nearly collinear, reversed chords in world space. The old hood had
  three inverted triangles, totaling about 6 square millimeters. Physical-XY
  triangulation preserves the parent samples and aperture boundary while
  removing that inversion. Simply beautifying the old triangles was insufficient.
- The remaining narrow crown corrugation followed coarse game diagonals.
  Dense-parent stripes were substantially smoother. Position error alone is
  insufficient on such a tight turn: interpolated normals must resolve the
  changing reflection as well. This motivated local physical sampling and
  explicit reflection-error checks, instead of another change to hood shape.

The lamp shell does not deform the parent. There is no QEM reduction of the
outer sheet. A suspected normal-transfer fault was disproved: independently
retransferred normals agree to approximately 0.03 degrees on the exposed hood.
Blender's zero-vector reset had retained the custom normals; removing the
attribute produced the expected different result. That failed diagnostic is
not evidence of a broken transfer.

The whole-body curvature colors use the actual game triangle positions:
signed cotangent mean curvature with mixed Voronoi areas, no spatial smoothing
or outlier removal. Open cut boundaries are gray because their one-ring
neighborhood is incomplete. Raw values are retained; the display has an asinh
scale clamped at +/-40 inverse meters. Analytic plane, cylinder and sphere
checks validate sign and magnitude independently of the car. This map also
shows irregular sampling at rear-quarter and bumper turns; those regions
must be checked beside reflections rather than dismissed as harmless color.

Scratch evidence is under `build/hatch-r4/`: `fold-causes.json`,
`inverted-regions.json`, `pass2-parent-regions.json`,
`pass2-inverted-regions.json`, `normal-transfer.log`, and
`curvature-calibration.log`. Final reproducible maps and same-camera
comparisons are listed in the concluding pass below.


### Pass 2 — retain the crown and repair physical sampling

Value remains neutral gray against each photograph's white studio neutral.
The procedural sky has a brighter upper hemisphere and dark ground reflection;
it exposes the crown's value turn without changing the accepted matte rig.
A first broad fitting handoff removed the fold but reduced the aft front-fender
rise to 6.4 mm. The existing character check rejected it. A 120 mm handoff,
with the local unswept rows retained, restores the aft rise above 10 mm without
bringing back the parent fold. The check was retained without loosening its
10–30 mm range.

Physical-XY hood triangulation and locally radial fender triangulation remove
the reversed lamp-tip chords. An initially higher radial origin grazed the
concave crown and introduced eight tiny reversals; lowering that origin below
the crown resolves the projection ambiguity. This is a sampling repair on
the same evaluated sheet, not a new independently fitted panel.

The curvature maps also directed attention to the front arch/grille edge and
the rear shoulder termination. Two small reversed fragments at the front arch
and grille edge were resolved with parent-sampled midpoint refinement.
Feature-aligned shoulder edges are now retained across the rear quarter;
additional samples follow its tight reflection turn. The broad rear quarter,
gate and bumper parent were also inspected for fold orientation. Their tested
regions contained no reversed patches. Remaining raw map variation at
irregular cut triangles is disclosed with the final stripe comparisons.

Budget is reallocated by retiring redundant samples only after centroid and
edge-midpoint probes meet 0.3 mm positional and 1.5 degree normal-interpolation
limits. Rim vertices and the gate's tight lines are protected. Increasing the
candidate neighborhood does not relax either error bound. The ordinary clean
build and the independently prepared parent build match all 132 objects /
119 meshes exactly. No shared modeling or kit implementation changed.


The direct accepted-part comparison catches one local preservation departure
that the rake check alone cannot reveal: lowest windshield tips move up to
29.49 mm and adjacent lower pillar corners 26.52 mm as the folded cowl is
repaired. Above z = 980 mm, both surfaces agree within 0.00015 mm. Roof,
backlight, side glass and mirror sail differ only by tiny resampling roundoff;
mirror housings, spoiler and wheels match exactly. The accepted main glass
and its rake remain, but the entire windshield boundary is not byte-identical.
This exception is visible and measured, not hidden behind the package check.

The denser source also rejected a 1.9 mm rear-fascia chart coverage gap after
boundary cleanup. Its shorter 30 mm cleanup chord was restored; the final game
retains its verified 45 mm maximum with the same 0.3 mm positional bound. Both
ordinary source builds now pass their coverage checks. The full game orientation
audit retains three microscopic door-cut fragments totaling 0.00151 square
millimeters; no additional visible reversed region was found. The requested
hood/fender region contains none.


### Pass 3 — calibrated gloss pairs expose the remaining value hierarchy

Neutral remains the white studio backdrop in each reference, with unit RGB
gains. The new material is a darker mid-gray diagnostic rather than a silver
paint match. Its bright sky and dark ground show value changes that the
unchanged low-sun matte view cannot show. Both makes' photographs remain beside
their calibrated renders; their lighting is not reproduced or projected.

**Hood and front fenders, against both front pairs.** The previous short folds
along the narrow hood crowns are substantially calmer. Corolla's broad hood
highlight and Hyundai's continuous lamp-to-cowl roll now have a corresponding
continuous reflection on the H120. The crown is still narrower and more
pointed at the lamp end than either real stamping. The plain horizontal grille
bars and empty lamp shells look older and cheaper than both references. Small
aperture-end and cowl junction marks remain in the tight stripes; no assertion
of perfect surface continuity is warranted by the orientation checks alone.

**Gate and rear corners, against both rear pairs.** The top crease gives the
central run a definite upper edge, while the retained lower lip supplies its
second boundary and shadow. Interior bands are coherent in the rear view;
the old wrinkled smear is reduced. Compared with Corolla, the center still
reads more like a narrow scoop and the quarter's reflected transition is less
resolved. Compared with Hyundai's largely convex gate, the H120 recess is more
assertive and less restrained. The Corolla remains the chosen construction
reference for the black lower center and tall corner reflectors. Raw curvature
colors at the bumper cuts remain irregular and the rear shoulder termination
still has a fine reflection jog. The maps are not presented as blotch-free.

**Side, against both side pairs.** The shoulder gives a strong bright-to-dark
step and the wheel crowns turn reflected value. The lower crease is visible,
but its reflection remains substantially quieter than both Corolla's bright
lower sill shoulder and Hyundai's rising lower highlight. A trial increases
the hollow above that crease by 3 mm, so the lower surface can turn farther
toward the bright hemisphere. The accepted shoulder and wheel-crown parameters
are retained; this trial is judged visually before its measurements are used.


The local door trial is retained after opening both calibrated side pairs and
the front three-quarter. Its lower reflection is now a distinct bright edge
above the sill instead of only a darker blur. It remains less broad and bright
than the silver reference highlights, which also reflect studio light. The
measured turn is 18.35 / 22.82 / 24.73 degrees across 30 mm, versus the previous
12.77 / 15.67 / 16.20 degrees. Shoulder turn stays 23.79 / 23.89 / 23.87 degrees.
The extra 3 mm of draw fades at the wheel openings and is absent from the
molded ends. Form allocation becomes 46,745, including 4,428 door and 12,725
body triangles. `build/hatch-r4/lower-crease-side.jpg` records the same-camera
trial; the canonical checkpoint is regenerated from the ordinary build path.


The uniform 3 mm trial subsequently failed two existing character limits:
front low-door lean was 20.22 degrees (limit 20), and the B-pillar's older
80 mm window was 25.44 degrees (limit 25). Neither check was relaxed. Tapering
the additional draw from 2 mm at the front toward 3 mm at the rear retains
the clearer lower reflection in both side pairs while restoring front lean
to 19.49 degrees. Final 30 mm turns are **16.52 / 21.84 / 24.72 degrees**;
the 80 mm windows read **20.78 / 24.30 / 24.58 degrees**. Actual 50 mm hollow
chords measure **4.67 / 5.20 / 5.49 mm**. This version passes the character
check and uses **46,737 triangles**. The accepted shoulder remains unchanged.


### Pass 4 — final whole-car gloss and limits of the map

The white studio backgrounds remain the photographic neutrals, with unit RGB
gains. The gloss diagnostic uses scene-linear gray 0.18, roughness 0.22 and
clearcoat, with a procedural sky above a dark diffuse ground. Both revisions
use the same environment and exposure. This is a value/reflection comparison;
it does not match the silver paints or reproduce the manufacturers' studio rigs.

At whole-car scale the continuous bright shoulder above the darker door gives
the side a clearer section. The rising lower edge now catches a distinct
reflection in both calibrated side views, and both wheel crowns turn the value
around their arches. Corolla's lower highlight and Hyundai's longer rising
highlight remain broader and brighter. The H120 still looks more regular and
less subtly crowned across its large door fields. Its narrow hood crowns are
calmer but more pointed than either make. The grille's broad horizontal bars
look older, and the bare optical cavities, opaque glass, missing cabin and
uniform wheels remain obvious CG placeholders.

The gate's new top crease and retained lower lip bracket its hollow. Actual
normal turns are 34.51 / 32.99 / 16.42 degrees over 30 mm at x = 0 / 250 /
450 mm. The central run retains 24.00 mm section depth and 15.61 mm plan depth;
the lip stands 32.55–33.37 mm proud. Its interior curvature colors form broad
continuous bands and the rear reflections pass coherently through them. The
center remains more scoop-like than Corolla's stamping and less restrained
than Hyundai's largely convex gate. The rear shoulder's ending still makes a
small reflection jog, and the D-pillar transition remains crowded.

The maps are deliberately raw. They still have conspicuous triangular patches
at irregular cut-adjacent samples, especially the lamp crowns, rear quarter and
bumper corners. These are not all proven harmless merely because the parent
has no reversed faces. The corresponding stripes and gloss show much smaller
irregularities, but the evidence does not support a claim of universally clean
curvature. The repaired front-arch and grille fragments, the parent cowl folds
and the lamp-tip inversions are separately documented above. The full audit's
three microscopic door-cut fragments total 0.00151 square millimeters and are
retained in the raw report, not counted as visible panel damage.

The lowest windshield tips' 29.49 mm movement and adjoining pillar corners'
26.52 mm movement remain the local preservation exception. The main glass,
header and rake are preserved; the complete old glazing boundary is not.

The opaque car pixels in the final front/rear gloss three-quarters have
display-luma p1 / median / p99 of **3.0 / 94.7 / 220.7** and
**1.1 / 79.4 / 230.8** on a 0–255 scale. Pixels below 25 occupy 7.9% / 13.7%,
with zero clipped color channels in all ten gloss views. Cavities retain deep
values and the bright roof rolls off without clipping. These whole-car values
include dark inserts and tires; they are not measurements of body albedo.

Final ordinary `make -C cars BODY=hatch` completes successfully. Its check
target passes game/high source audits, the package/character and round-two
through round-four checks, parent orientation, curvature calibration, camera
verification and repository rules. `python3 -m py_compile cars/src/hatch_*.py`,
`git diff --check` and `python3 kit/repo_check.py` also pass. No source-audit
warning is outstanding. These checks certify the source checkpoint, not the
deferred UVs, baking, articulation or export. Independent factory-empty builds
match 132 objects / 119 meshes exactly, including authored normals.

The reviewed final set contains 47 native views: the original 27 matte/stripe
views and pairs, five actual-game curvature maps, five matching stripe views,
and ten gloss views including all six calibrated photo cameras. All 47
round-three comparisons retain their cameras. Every current view and game
measurement carries source SHA-256
`62deb6c290f859e3fb930965bcc32a23b5dd1b0d344bcbd87f2de0e9a4c4d4d5`.
The final side overlays retain 4.298 / 4.312 px camera RMS at 2100 px. The
accepted upper rear and lower bumper deviations remain as reported in HATCH.md.

Evidence is under `renders/hatch-round4/`: `round4-contact.jpg` contains
62 views; `contact.jpg` retains the earlier review layout. The five
`curvature-stripes-*.jpg` plates, six `gloss_*-pair.jpg` comparisons,
`round3-round4-*.jpg` comparisons, `gloss-tonal-range.json`,
`mean-curvature.json` and `round3-round4.json` carry the visual and numerical
record. All native renders, both profile overlays, game/parent curvature plots
and both makes' final gloss pairs were opened for review.

The final form is **46,737 triangles**, with the per-part allocation in HATCH.md.
The unchanged 12,500 reserve gives **59,237 against the 59,343 plan**, leaving
106. There are five temporary materials and zero textures. Game/high sources
are 1,084,081 / 2,303,895 bytes; the high source has 110,922 triangles.
Pickup regeneration matches 472 objects / 454 meshes; its re-export matches
all 150 GLB accessors, embedded maps and all **11,530,720 bytes**. No shared
family implementation, sedan module or kit file changed. Stop at this source
form checkpoint: no hatch detail, interior, UV, bake or GLB phase was started.


## H120 detail and look checkpoint

### Detail pass 1 — reject underexposure and the inherited inner package

Color and value first: the four-year white hatchback photographs (Elise240SX,
2022-08-06, `refs/hatch-used-*.jpg`) show white paint around mid/high display
values, dark but legible cabins, and dark used tires. The initial studio in
`renders/hatch-detail-pass1/` is too dark to judge any of those. Its metallic
coat reflects the lamps, but this does not establish a daylight match. The
white siding in the front reference and gray garage door mullion in the rear
are the proposed neutrals; their explicit patch gains are measured later.

The first optical housing used a nearest-normal field that admitted the inner
laminate at the boundary; the resulting reversed offsets stuck black geometry
above the hood. Use only the authored outer lens triangles for that field.
The first cargo opening proves the five-seat package, load well and parcel
cover, but also exposes floating tether ends and the backlight seal left in
the body hierarchy. Remove the unneeded tethers and carry the seal with the
gate. Cabin, firewall and floor corners copied from the longer sedan intrude
into the front wheel envelopes. The solid sweeps correctly reject those;
reshape those hidden corners instead of suppressing collision pairs.

### Detail pass 2 — reject streaked road film and concealed hardware outside

Color and value first: `renders/hatch-detail-pass2/` has a readable blue coat
but still excessively black glass and dark wheel pockets. The procedural
studio is an appearance diagnostic, not the reference daylight. The first
matched cameras were also rejected: four coplanar wheel anchors admitted a
camera below ground and a reflected pose. Correct the near-side sign and add
a stated 1.50 m height prior; keep the resulting 9–10 px native residual visible.
`hatch-detail-pass4/` accidentally selected Graphite through a renderer default;
that is diagnostic failure evidence, not a white-paint comparison.

`renders/hatch-detail-pass5/` finally compares white with white. It rejects the
illumination: the car and asphalt remain far too dim. Increase sky/sun together
before tuning paint albedo. It also rejects the inherited broad film fan: the
rockers look streaked and much dirtier than the photographed daily driver.
Shorten the tire wakes, lower their ceiling and use fine variation only in
deposit density. Preserve the clean paint's own hue.

The close face identifies an exposed straight crash beam through the curved
nose, not a new styling problem. Give its ends the fascia's plan curvature.
The hinge leaves also break through the lower door skins: the accepted form's
provisional pivots are too far outboard for real hardware. Move the hinge axis
inward, use 2 mm fixed leaves and preserve the world skin position. An actual
bored roof sleeve replaces the gate leaf drawn through its pin. Inner
wheelhouse returns clear the steering tire while their outer lips remain held.
The resulting twelve game sweeps pass at 0.5 mm tolerance, 2 degree closure,
10 degree wheel and 1 degree steering increments. These are sampled solid
clearance tests; they do not by themselves prove every fixed support contact.


### Detail pass 3 — matched daylight, fair reflections and supported hardware

Color and value first: `renders/hatch-detail-pass6/` replaces the rejected dim
white comparison with diffuse procedural sky/sun and asphalt. White paint now
sits in the photograph's value range; the sky is desaturated before any paint
hue adjustment. The front reference's white siding and the rear reference's
gray garage mullion are the stated white-balance assumptions, rather than an
unqualified claim that the photograph records true albedo. Glass stays dark,
with seats visible, and tire sidewalls remain darker than the paint. The new
short road-film fans stay below the door field and behind their originating
wheels. The former tall streaked overlay is rejected.

The game/high comparison exposes a small shoulder scallop near the rear cut.
Add 48 interior edge samples on each rear quarter, projecting only those new
samples onto our own dense accepted surface. Give the hood and front fenders
32 each for their narrow crown reflections. This adds 384 body triangles;
retained samples and exterior cut outlines are held. The largest new-sample
projection is 1.011 mm on the front left fender. Tight lamp-corner reflection
jogs remain a weakness, not a reason to refit the accepted package.

The full source close-ups show legible original tire relief, projector/guide
layers and a fictional dealer insert. Game spokes still need their high-source
chamfers in the normal map. The through-glass camera exposes a white softbox
reflection over the dash; move the studio around that inspection view before
judging cabin visibility. Do not brighten or frost the glass to reveal it.
Cargo trim and the shelf are deliberately simple, with no floating tethers.

Solid sweeps found a small fixed front pane needed ahead of the moving window,
a buried spoiler mounting foot, and a gas-spring casing clipping the closed
backlight. Split the tiny forward glazing sail without changing its outer
surface; seat the spoiler's hidden foot; place the gate ball brackets against
the actual perimeter segments with cabin-side stand-off. Formed door leaves
and welded pads replace unsupported hinge tubes. Check 42 actual support
contacts independently of the motion sweeps, and evaluate both moving spring
ends every degree. All source motions now pass on game and high meshes,
including the supplemental coupled high spring sweeps.


### Detail pass 4 — reject the first exported bake

Color and value first: `renders/hatch-bake-review/` is the first actual imported
H120 GLB, not the procedural source. Its blue paint and dark glass retain the
broad source values, but a thin red line above the grille and stray colored
strokes on trim are impossible material contamination. The first 5° UV pack
has 16,012 charts and only 37.1% useful area. Its narrow island gaps cannot
support the baker's broad padding. The original source close-ups stay clean;
this is bake loss rather than a new form defect. Reject these images as final
evidence and repack with broader charts, wider gutters and marking priorities.

The same first export makes the door-glass softbox reflection wavy and the
wheel chamfer highlights ragged. Do not accept partwise ray coverage as a
visual proof of a smooth reflection. Smooth glazing needs no high-source
geometric normal, and the game skins already carry the accepted parent normal
field. Restrict projected geometric detail to hardware, wheels, tread, cabin
and underbody where it has a cause. Keep the exact procedural tire sidewall
normal for the original raised lettering. Neutralize tangent normals on the
smooth glazing, and leave chart-edge normals with the direct bake.

The cabin remains legible through the dark pane, but the inspection light
reflects across the cluster. Rotate the inspection studio so the opening
reveals the dash; keep the photograph pairs free of every studio light. The
coarse headrests, simple cargo trim and low-detail underside remain visible
limitations. The lamp lit/unlit state and promotional insert do survive the
first bake, although text and the tire's small relief lose resolution.


### Detail pass 5 — correct the neutral, preserve the measured limits

Color and value first: the annotated front comparison exposes a reference
measurement mistake. The first purported siding neutral at x50–180/y80–100
on the 1200-wide image reaches vegetation (median RGB121/128/100). Reject
its magenta white balance and all front residuals derived from it. A clean
siding patch between the two windows, x120–220/y12–42, measures RGB166/171/171
and gives linear gains 1.0453/0.9788/0.9788. The rear neutral remains the gray
garage mullion with gains 1.0416/0.9689/0.9923. This correction changes the
front comparison without changing the rendered lighting or factory tint.

`renders/hatch-source-tuned/` uses the longer but strictly low wheel wakes,
with a slightly broken upper edge. The current direct source front paint
patches are 6.4/7.8 display levels darker than the corrected reference; its
low-film patches are 4.2/0.6 darker. Rear paint is 5.0/1.4 brighter, with lower
film 9.0/7.9 brighter. This is a materially closer low-body gradient than the
previous nearly clean rear rockers; the film remains caused by tire spray,
not a whole-car color overlay. The rear side-glass and backlight residuals
remain +38.2/−41.9: different reflected surroundings, viewing angles and the
privacy package are unresolved. Report those rather than tuning white paint
to conceal a glass/environment mismatch.

The revised atlas uses broader 35° charts, higher marking/tire priorities and
three-pixel bake padding. The first broad-chart repair has eighteen chart splits and 39.9%
coverage; float32 re-import then catches one collapsed subpixel altitude.
The revised guard logs 47 UV repairs/splits and yields zero overlaps with
40.5% coverage. Three submicron cut slivers retain their geometry with representable
UV altitudes. Smooth glazing keeps a neutral tangent map over its authored
vertex normals, and projected tread detail is confined to the crown. Final
imported images, not this source comparison or the rejected first bake, are
the next visual decision.


### Detail pass 6 — final bake survives; correct the studio's clipped highlights

Color and value first: the imported 2048 bake now preserves the deep black
optical cavities, clear dark glass, original dealer insert and restrained
dirt. The source/GLB daylight pairs use the corrected neutral patches and
the same procedural sky/sun. The first final studio heroes nevertheless clip
1.68% / 2.20% of asset color channels at 254 or above, with p99 luma255.
Reject that exposure as a tonal proof. `renders/hatch-tonal-study/` re-renders
the actual GLB one stop lower: p99 is 248.9 on both heroes and no checked
channel clips. Adopt −2.5 exposure for the whole-car heroes, five factory
colors, scale and the inherited whole-car mechanism poses. Keep the daylight
photograph recipe unchanged, and keep separate exposure for close inspection.
This is a physical re-render, not a remap of clipped PNGs.

The wheel close-up at `renders/hatch-checkpoint/wheel.png` retains ALDER
TOURING and the original size lettering after a faint dust deposit on the
raised type. The normal relief alone had faded below legibility in the first
bake. Broader charts and smaller padding remove the red line above the grille
and colored trim strokes. Neutral glass normals restore smooth reflections.
Spoke chamfers remain soft at 2048 and the tire's shoulder facets still show
in this extreme close-up; neither the vertex-normal check nor ray coverage
is used to claim otherwise.

The eye-height view now exposes the dash and steering wheel through the dark
pane by moving the studio reflection, without making the glass milky. Cluster
and screen detail remains small and dark, and the cabin's regular headrests
and cargo trim remain simplified. The lower gate stamping, fine hood-corner
reflections and regular door/window cuts still read more deliberately modeled
than the reference car. The static low-detail suspension is not a complete
kinematic steering linkage. These remain limitations for the checkpoint.


### Detail pass 7 — checkpoint review and explicit remaining limits

Color and value first: all 58 current native views were opened via the seven
review pages, with the wheel, glass/cabin and annotated pairs also inspected
at native size. The two 1400-pixel Cycles heroes have asset luma p1/median/p99
0.8/46.3/249.1 front and 0.0/45.7/248.9 rear, with zero channels at 254 or
above. Other factory-color Cycles heroes have at most 0.0013% of channel samples
at 254 or above; these are isolated near-white samples rather than broad
clipped reflection patches. White,
black, gray, silver and blue now occupy distinct plausible value ranges,
rather than five pale versions. The Eevee fallback has a tiny 0.078% clipped
channel fraction and darker glass; it remains a less faithful secondary view.

Correctly balanced exported white paint differs from the selected reference
patches by −6.4/−7.8 front and +5.0/+1.4 rear. Low-film patches differ by
−4.1/−0.7 front and +9.0/+7.9 rear. The rear side-glass/backlight remain
+38.2/−47.7, and the front tire sidewall +11.1. Those are substantial remaining
appearance differences; the gray procedural horizon does not reproduce the
photographed surroundings or the reference's glazing package. RGB medians,
patch ranges and neutral gains remain in `pair-values.json`, rather than
claiming that display luma measures intrinsic albedo. The current source
pairs are separately rebuilt under `renders/hatch-source-pairs/`.

The original cascade vanes, surround, badge and dealer insert read clearly;
the fine secondary lattice loses contrast in the atlas. Projector/guide layers
and lamp on/off state survive. Tire lettering survives the final bake, but
shoulder facets, thin inner-arch return glints and soft spoke chamfers remain
visible at the extreme wheel close-up. Small hood/lamp-corner highlight jogs,
regular door/window cuts and the crowded rear shoulder still betray the model.
The cabin's small graphics and regular headrests/cargo trim are weaker than the
exterior. Upper gate-frame and suspension/steering supports are simplified
proxies, not a fully detailed or fully coupled mechanical assembly.

`make -C cars BODY=hatch` and `make -C cars BODY=hatch check` pass. The clean
source-only copy also passes its rebuild/check; all 484 objects / 455 meshes
and every atlas UV match exactly. Independent GPU bakes differ by at most
one 8-bit level at 1/115/4 BaseColor/Normal/ORM pixels. Both source densities'
twelve kit motion sweeps pass, as do 42 support pairs and the one-degree
coupled gas-support checks. UV overlap/outside/degenerate counts are zero,
including re-import. The actual GLB is 8,256,940 bytes, 59,989 triangles,
21 meshes / 36 material primitives, four family surfaces and three 2048 maps
(about 16 MiB compressed with mips). Re-import position error is 0.386 μm.

Every indexed checkpoint view has GLB hash
`c0e0adb268eb3d5de7ac3fa71cf93834633d72c4699bd64a6b4911ea4e253c45`
and one current render-recipe hash. Sixteen legacy form views formerly in the
same folder were preserved under `renders/hatch-checkpoint-form-archive/`,
so they cannot masquerade as current detail views. Pickup source and full
GLB bytes remain identical. No kit/shared family implementation changed, and
no hatch docs images are committed. Stop at this requested checkpoint.

## H120 surface correction checkpoint

### Surface pass 1 — causes isolated before correction

Color and value first: keep the five accepted factory factors and the accepted
white-balance neutrals (front siding; rear garage mullion). The earlier rear
pair measures front side glass 161.9 versus 123.7 (+38.2), and backlight 73.4
versus 121.2 (−47.7). These are displayed values under the stated diffuse sky,
not recovered albedo. The rear photo has a dark building reflected in its side
pane and bright surroundings transmitted/reflected through its backlight;
the procedural open sky over asphalt does not supply that environment.
Tint, cabin occlusion and reflected-environment contributions need separate
experiments before any adjustment to paint or overall exposure.

Earlier images and the GLB are retained in `renders/hatch-surfaces-before/`
and `build/hatch-surfaces/before/`. Same-camera procedural-source renders are
in `renders/hatch-surfaces-source-before/`. Disconnecting every paint/material
bump input (`renders/hatch-diagnosis-no-bump-game/`) leaves the torn lenses,
hood reflection ripples and arch spikes. These defects therefore precede UV,
bake and normal-map filtering. The prior neutral glazing tangent map cannot
repair their source geometry.

Before fixes, `build/hatch-surfaces/normal-audit-before.json` measures outer
lens triangles with normal/face disagreement up to 177.6 degrees. A coherent
parameter-chart disk can still have reversed physical chords over this steeply
wrapped surface. Authored normals do not make those refracting triangles a
smooth molded shell. The game and high source both inherit this lens topology.
The hood and rear quarter have continuous normals at shared vertices, but
coarse diagonal interpolation across changing curvature remains visible with
bump disconnected. They need a denser or smoother physical derivative field,
not stronger orange peel or another coat.

Arch returns are separately sampled from side rays, with a hard `.89` fallback
when the ray misses near the lower/forward tip. Their outer contour is also
sampled independently of the actual clipped skin. The visible slivers already
exist in the source. Replace that unsupported return sampling, retaining the
accepted exterior opening. Tire sidewall rings expose another construction
fault: the generic tall-tire profile's fixed 75 mm station exceeds this low
profile tire's shoulder radius, doubling back before the tread. Sharp ring
edges and 48 circumferential samples amplify the polygonal result. Rebuild a
monotone passenger carcass and continuous toroidal normals; preserve its width,
rolling radius and wheel pivots.

The grille's vanes follow an uneven triangulated backing, deliberately kink at
their middle station, and stand in front of a procedural bumped diamond image.
This is the radiator appearance in both source and GLB. Replace the vanes and
bumped backing with an actual open regular cell lattice, a smooth dark recessed
bed, and the retained surround/badge. Give the lower opening a distinct lattice
and the corner pockets formed inserts with supported lamp/blank faces.

### Surface pass 2 — reject the first repairs, refine the causes

Color and value first: source tint trials leave rear side glass +14.4 and
backlight −9.3, versus the original +38.2/−47.7; the front pane is now too dark
(−17.8), so this is not an accepted glazing solution. A reflection-only ablation
places rear side glass at +1.0 but the front at −22.6. Removing the cabin changes
backlight by only about five levels. A traced refracted ray through the actual
backlight exits the far rear door pane: four tinted interfaces compound the
attenuation before the ray reaches low sky/ground. The photo has clearer rear
glazing. These tests explain why backlight tint alone did not recover its value.

Reject the first replacement lens. It used the analytic section target directly,
but the accepted subdivided crown blends away from that target near the lamp tip
by as much as 136 mm. A global polynomial fit was consequently both inaccurate
and ill-conditioned; its molded surface did not stay seated. The replacement
also initially used an outward offset instead of retaining the accepted 7.8 mm
recess. Neither is a valid correction. Sample the actual original evaluated
parent in a physical cylindrical chart, retaining the recess, with continuous
outer/inner normals. No source photograph enters this construction.

Hiding every arch flange leaves the principal spike visible. A camera ray at
its pixels identifies **Front molded fascia**, not the hem: a sparse curved
triangle fan and its interpolated normal field make a triangular reflected dark
flag near the arch's forward end. Resolve normal-interpolation error with local
physical samples on the accepted parent. The return's unsupported fallback was
also wrong, but it was not the whole cause; the first diagnosis overstated it.
A later all-skin reclip is rejected: it reconstructs thousands of already omitted
buried back faces, wastes the budget and does not address that fascia reflection.
The original physical arch cut is held for the next comparison.

The first tire carcass and lattice are materially clearer in their studio views.
Reject the first fog blanks, whose estimated stand-off leaves them outside the
pocket; seat them from rays against the actual pocket bed. Interior gauge
reduction must also be admitted by measured inward clearance, rather than an
angle threshold alone: keep at least 0.35 mm below the actual exterior, and
retain the old gauge if that bound fails. This allocation funds visible rubber
and optical sampling without increasing the 60k cap.

Further cause isolation in pass 2: the signed maps now include the lenses and
show physical chord failures even where every shared corner normal agrees.
A perspective chart aimed from inside the convex front resolves the grazing
chart direction, but still needs explicit chord-error refinement at thin tips.
The final candidate uses a symmetric, regularized physical contour and a smooth
cubic radial optical mold, fitted to samples of our evaluated parent. The mold
bridges the stamping's draw line, stays recessed behind it, and derives its own
continuous normals. Global section-target fits were rejected; the actual
subdivision surface is the fitting reference. Its extra seating recess and
maximum fit error are recorded on each lens, alongside every chord refinement.
This is a different optical mold behind the accepted painted aperture, rather
than a claim that the old crumpled shell was fair.

Both original and corrected skins are typically within hundredths of a
millimeter of the accepted parent (`build/hatch-surfaces/position-errors.json`).
The hood's largest tested residual is 0.451 mm, the right rear quarter's
0.258 mm. This rules out a broad form refit as the cause of the paint correction.
Local reflected-normal sampling is the appropriate correction; irregular-cut
curvature outliers are retained in the raw maps rather than filtered away.

The first all-surface audit also rejected zero-area return triangles caused by
repeated nearest hits on an already cut arch and repeated guide points. Arch
returns now ray-sample the original **uncut** parent, retaining their open arc
construction and inward steering clearance. Optical guides follow consistent
fractions of the fitted mold's physical chart, with duplicate chords removed.

The broad gray comparison facade was rejected: it lowered rear paint by more
than 20 levels while darkening the pane too much. A narrow, bright, procedural
facade changes that low-angle reflected sector while retaining the original
sun/sky and asphalt. It is estimated surrounding scene context, with dimensions,
albedo and placement recorded in the shot metadata; it is never exported or
baked into the car. A narrow-facade source trial leaves rear paint within four
levels, side glass −6.3 and backlight −3.1. Small final transmission adjustments
are checked in the actual exported pairs next. Front-side glass in that trial
is +1.7; the source windshield's −15.5 remains an independent residual.

The enlarged wheel crop and exact pixel rays refine the arch diagnosis again:
the thin spike's tip hits **Wheelwell_FR**, with the adjacent reflected region
on the fascia. The liner's constant 795 mm outboard coordinate exceeds the
fascia's actual tucked width near its bottom/front (about 790 mm there).
Its edge therefore protrudes through the paint and continues as a thin exposed
sliver below it. Extra fascia samples improve its reflection but cannot remove
that exposed liner. Clamp the lining inside the measured parent skin, sampling
the body hem above an open lower edge when necessary; retain the liner's radial
rolling/steering clearance. This is a construction interference, not a normal
map effect. The exact crop is `build/hatch-surfaces/arch-pick-grid.png`; pixel
rays are in `build/hatch-surfaces/pick-spike.log`.

### Surface pass 3 — source close-ups reject the flat fuel flap

Color and value first: the candidate preserves Graphite's accepted neutral
factor, darkens the grille's recessed bed without bleaching its webs, and
retains visible dark tire rubber and molded lettering. The rear-quarter close
view exposes another cause of the lumpy highlight: the fuel flap's nonplanar
ngon cap is triangulated as broad flat faces across the shoulder. Its reflection
therefore steps independently of the curved quarter beneath it. Replace that
cap with a sampled compound disk on the same accepted parent normal field;
retain the circular reveal and original 140 mm size. This spends visible
surface triangles by omitting the disk's buried game-side back, with the high
source keeping its full gauge. The studio close-up, not that allocation, decides
whether the reflection is improved.

A second exported-asset ablation separates the paint's bake defect from its
sampling defect. Disabling only the **Paint** normal input on the unchanged
old GLB (`renders/hatch-paint-no-normal/`) removes the coarse mottling around
both hood softboxes and the rear-quarter highlight. The broad curve/cut jogs
and flat fuel flap remain. The procedural source has much finer, weaker peel:
the 2800 cycles/meter paint micro-height is unresolved at the delivered body
density (about 228 pixels/meter). Baking point samples and then quantizing that
field leaves false millimeter-scale normal noise. The paint's only authored
height channels are micron peel/flake; wear and chips already live in color and
roughness. Keep those roughness responses and use a neutral delivered tangent
field on painted faces, as on smooth glazing. Geometric normal detail on tires,
alloys, hardware and the cabin retains its independent projection checks.
This removes an alias, not a designed stamp or normal-map scratch.

### Surface pass 4 — distinguish the remaining interpolation and delivery errors

Color and value first: the first new export preserves the five paint factors
and the original studio light/exposure, with deep grille cavities and visible
used rubber. It still fails the rear glazing test: side glass 118.8 against
123.7, backlight 101.8 against 121.2. Source values near 121.5 / 119.0 are not
proof of the delivered result. Reject that exported glazing result.

An actual-GLB ablation removes only the Glass normal input. With the same
1.50 delivery IOR the backlight rises to 120.2. An 8-bit neutral map has
128/255 in X/Y, not 0.5; the small tangent deflection changes the background
sector sampled through several refracting interfaces. This error is amplified
by the narrow bright facade, not evidence of darker exported tint. Retaining
the source glazing's 1.52 IOR as well gives **121.5 side / 121.0 backlight**
against **123.7 / 121.2**. Preserve the authored smooth Glass normal field with
glTF normal scale zero; the same policy avoids neutral-map deflection on Paint.
The independent material ablation is `renders/hatch-glass-delivery-150/` and
`-152/`. A small front-pane tint adjustment is checked in the final export.

Reject an additional bounded parent-normal projection. It fills its checked
outer-skin texels, but does not remove the remaining shoulder teeth and adds
unnecessary low-density map corrections. Both a normal-input ablation and a
constant-paint ablation retain those teeth. Their cause is the game skin's
irregular interpolation across a very narrow roll, independently of the
earlier micron-height alias. A direct comparison of game/finalized/imported
normal fields finds the latter two equivalent: this is not GLB serialization.

Simply bisecting three aligned rows improves the line but adds 1,954 triangles;
one row is insufficient. Instead, retain every existing patch boundary and
replace only the shoulder's interior chords in physical (longitudinal position,
height above shoulder) coordinates. Regular 21 mm stations and 7–8 mm rows
near the roll sample our actual evaluated parent. The two patches replace
868 / 862 triangles with 484 / 494, saving **752**. The source studio close-up
now carries an uninterrupted strip through the quarter and the compound fuel
flap. The first scratch patch had uninitialized rest-coordinate attributes and
therefore a rectangular shader artifact; reject it. Regenerating those
attributes resolves the artifact, as the actual model pipeline does for every
new vertex. A radial fuel-cap grid was also rejected for its central pimple;
the accepted disk's rows follow the shoulder instead.

The resulting game source is **59,178 triangles**. The new kit option is only
`DELIVERY_SURFACES[...]['normal_strength']`; default behavior is unchanged.
Real glTF regression checks zero scale, the neighboring default scale, and
three shared images. All **24** kit test modules pass sequentially from a clean
scratch build, including the three GPU-baking fixtures under the shared lock.
The final studio, all-surface diagnostics and measured pairs must now approve
the new export; earlier candidate sheets do not approve it.

### Surface pass 5 — exported checkpoint and the remaining CG tells

Color and value first: white balance remains on the front white siding and
rear gray garage mullion, with the recorded original linear gains. The final
rear side pane is **121.6 against 123.7 (−2.1)** and backlight **122.0 against
121.2 (+0.9)**. The side is 0.1 below the photo's p10 (121.7); the backlight
is inside its 118.4–124.1 p10–p90 interval. Do not round this into an exact
radiometric match. A final 2.2% increase in the rear diffuse sky (.225 to .230)
centers the backlight; the facade, sun, accepted studio and five paint factors
stay held. Front white paint patches remain within 7.8 levels, rear within 3.7.
Both Cycles heroes have zero clipped channel samples; luma p1/median/p99 is
0.0/46.3/248.9 front and 0.3/45.8/248.9 rear. Cavities and undersides stay dark.

The actual GLB studio pairs show the corrections: no crumpled white lens shards,
no coarse paint-normal mottling, an uninterrupted quarter/fuel-flap reflection,
no protruding liner spike, and a bulged, smoothly shaded passenger sidewall.
All nine before/after regions use identical camera, framing, studio rotation,
paint factor, exposure and native resolution; these fields were compared
directly in both shot manifests. The upper 14×2 diamond lattice has real open
cells and depth over a dark bowed cavity. A finer 20×1 lattice serves the lower
intake, the surround remains dark chrome, the badge carrier touches the webs,
and the corner wells now have seated molded blanks and recessed slots.

The full curvature review caught a diagnostic bug: joined GLB objects retain
the active component's old outer-face count. That stale count masked most of
the assembly, leaving false gray areas. Discard it for the imported diagnostic
and measure every exported face, including gauge; weld only coincident UV-seam
positions in the disposable diagnostic scene. The corrected map measures
**28,352 vertices across 21 meshes**. Source maps keep their explicit outer
roles and measure **23,440 vertices across 442 parts**. Their different gauge
selection is stated in the JSON; raw signs and cut outliers are never filtered.
True open-boundary neighborhoods remain gray in source maps. Both stripe
directions cover the glass, lenses, grille, lamps, arches, rubber and hardware.
The studio crops, rather than those diagnostic colors, approve the appearance.

Evidence is under `renders/hatch-checkpoint/`: the ten-view five-color sheet,
nine `compare-*.jpg` regions, 61 native views/contact/review pages, measured used
pairs and 27 exported diagnostics. The 27 source diagnostics and two measured
source pairs remain in their own folders. All exported views name GLB SHA-256
`9f4a4c6c13bb47b5e1af51840a54aa07db1c6e78491c4621095f8243f5f9fca0`.
The delivery has **59,178 triangles**, four existing delivery materials, three
2048 maps, **16 MiB** BC-class mipmapped memory, and **7,945,496 GLB bytes**.
UV overlap/outside/degenerate counts are zero; bake interior misses are zero
over 5,714,185 checked texels per channel. Source construction/motion checks
and exact independent regeneration pass separately from re-import checks.
The pickup re-export still compares byte-identical at its accepted SHA-256.

What still reads as CG: alloy rim/spoke facets and the small projector bowl,
very small cut/trim reflection jogs, the fuel reveal's segmented outline,
coarse cabin/cargo controls, and softened small badges/type in the atlas. Tire
patch medians remain +10.0 front / +21.0 rear and windshield −9.7; source and
export tire values differ, so roundness is not a claim of a perfect rubber
response. The rear photo tire patch includes bright rim pixels and has a broad
range, but that does not erase the median mismatch. Lighting context remains
an estimate. No lead action is required; stop at this requested surface gate.

## H120 delivery

### Delivery pass 1 — isolate the remaining causes before accepting a bake

Color/value first: retain the accepted paint factors, Porcelain white balance,
rear daylight/facade and glazing IOR/normal policy. Front white siding and the
rear gray mullion remain the comparison neutrals; no lighting recalibration
is used to conceal a surface repair.

The softened type is already lost in the material bake, independently of the
Opaque normal input. `build/hatch-delivery/badges-before.json` and reconstructed
4K/2K badge texels show the cause: native UV island averaging inherited the
rectangular source image's aspect despite Smart UV `correct_aspect=False`.
The grille badge's chart has fourteen samples along the 94 mm word and 57
along its 24 mm height. Its area-equivalent 596 px/m therefore concealed a
roughly sixteenfold density anisotropy. Wheel-cap type has the same fault.
Rebuild only original print charts in their physical metric before priority
and packing. Keep artwork addressing in the separate `BakeSourceUV` attribute.
Increase marking priority, including dealer fine print and cabin displays;
measure both printed axes, rather than declaring legibility from atlas area.
Paint and Glass keep normal scale zero; Opaque and Lamps keep scale one.

The gate's wavering run occurs in both the game and high procedural source,
before baking. Dense parent versus its original continuous die field measures
up to 3.58 mm of draw error around the 47 mm hollow; the control-net radial fit
and subdivision underresolve that narrow feature. The repair is confined to
the lower gate: restore the continuous die field, blending to the accepted
parent at the lamp/perimeter/hem, and add local samples where interpolated
reflection normals disagree. The actual game vertices move at most 2.170 mm.
Retain the aperture, crease, lower lip, package and all moving pivots. A scratch
trial initially left the disposable uncut parent visible; reject that render
and remove it before evaluating the actual repaired panel.

Tail covers inherited angle-limited geometric smoothing, leaving hard fans
at their narrow ends. Give both sides of their laminate the continuous mold
normal field; leave the gauge rim separate. The projector reflector and optic
increase from sixteen to twenty-four circumferential samples. Restore the
spokes' real 1.8 mm chamfer loop instead of hoping a subtexel normal bake can
carry it, and increase the fuel reveal from twenty to forty-eight stations.
The compound flap's perimeter also gains samples. Offset that visible detail
with sixteen-segment inboard barrel rings and eight-segment phosphor disks
behind the projector optics. Held exterior wheel/tire envelopes are unchanged.
The game source is 59,968 triangles, with 32 left under the existing ceiling.

### Delivery pass 2 — reject partially buried rear lettering

Color/value first: the current source daylight pairs retain their accepted
neutral gains and glass context. Front paint differences remain about −6.4,
−4.3, −7.8 and −0.7 display levels; rear paint −0.5, +0.9, −1.6 and +3.7.
These are source values, not approval of the new export. The gate's broad
reflection is quieter through the corrected run, but its ends and small cut
boundaries still need the final gallery audit.

Full-size rear source inspection rejects the name/model badges independently
of the atlas repair: the four-corner plaques chord through the compound paint
surface. Only the end fragments of their black substrates and lettering are
visible. This is a physical occlusion; more pixels cannot fix it. Replace each
with a 4 × 2 conforming grid, sampled on the actual gate, 1.5 mm proud along
its smooth normal. Original artwork and dimensions are held. This adds 28
triangles for a 59,996-triangle candidate. A dedicated gallery gate view must
approve the complete words after export.

The first new UV validation also rejected a rear print's anisotropic repack.
The kit's existing target-aspect control now supports Smart UV as well as
seam unwrap, and the hatch's later cut-sliver repacks explicitly use square
aspect too. The real 4:1 print regression passes with axis anisotropy below
1.000001. The current packed charts measure grille 166.8 × 42.6 pixels,
wheel caps 137.3 × 47.3, and dealer insert 360.7 × 180.3, each with equal
physical density on both axes. Forty-one explicit cut-fragment UV repairs
leave 41.0% coverage, zero overlap, outside and degenerate triangles.

### Delivery pass 3 — the family gallery rejects the header and nose roll

Color/value first: the candidate uses the exact C150 gallery constructor,
diffusion adjustments, shared studio implementation and AgX settings. The
setup's AST matches the pickup recipe. Atlantic remains dark blue, cavities
are deep, and the broad hood is clean. Do not change the accepted lighting to
hide the defects below. The initial exported candidate passes its checks at
59,968 triangles, but these images reject its presentation.

`renders/hatch-gallery-audit1/hero.png` has a triangular white reflection at
an upper windshield corner. An actual-GLB reflection-only ablation retains it,
so this is neither a darker cabin nor refracted headliner light. Source corner
normals there turn toward the neighboring roof/A-pillar; their swing differs
by up to about 18° from a smooth height fit to the pane's own positions.
Use that pane-local mold derivative only at the header corners, blended into
the held field. No glass vertex, cut, tint, IOR or rear pane changes. The fit
has a 4.56 mm maximum diagnostic height residual on the game pane; it supplies
a normal approximation, not a claim of an exact positional reconstruction.
The actual-GLB normal trial removes the shard. High-source corrections are
bounded to avoid extrapolated corner fields; game corrections remain below 20°.

The apparent hood ripple is on **Front molded fascia**, measured by camera
rays, in the narrow strip above the grille. An implicit-normal-only trial
leaves its broad waves: the dominant fault is interpolation along irregular
radial diagonals across a narrow roll. Keep all 87 boundary vertices and
replace only interior chords in a physical chart parallel to the nose
contour. The candidate replaces 163 triangles with 295. New points sample
our own held parent; its small normal error is resolved against the original
continuous die field. The broad softbox edge now crosses the strip as one
curve. A remaining thin stepped feature in a source-only procedural preview
disappears under constant paint: its rest coordinates agree exactly and
shared-vertex normals have zero measured discontinuity. Do not mistake that
source microresponse/denoising artifact for another broad form defect. The
filtered exported material must decide whether it remains visible.

A buried 12 mm inboard wheel-barrel return is simplified in the game mesh to
fund the new visible chords. The bearing lip, tire/wheel envelope and all
outboard contours remain held, with the complete return in the high source.
The candidate source is exactly 60,000 triangles, within the existing cap.
Each final gallery view now starts a fresh GLB import, with the shared GPU
lock acquired per view; no studio recipe changes.

The clean build also caught a reference endpoint omitting `Content-Type` for
a valid manufacturer PDF. The fetcher now accepts that narrow case only after
checking `%PDF-`; explicit HTML and missing-header HTML still fail without a
file write. Its positive/negative fixtures pass. All 24 kit modules pass again
sequentially from a clean scratch build, with all bake fixtures under the lock.
No downloaded code is executed and the pickup still re-exports byte-identical.

### Delivery pass 4 — reject the first finals; resolve the remaining interpolation

Color/value first: inspect all fourteen gallery views, all five paints and the
Eevee hero at native size. Upper paint stays dark enough, the broad hood is
clean, and the road film retains its wheel-wake cause. The badges, plate type,
tail shell, fuel reveal, cast chamfers and header correction survive export.
The scale figure measures 1.8 m. Cabin contours are visibly economical in the
cargo view, and Eevee's screen-space optics remain weaker than Cycles.

The first finals still fail at the narrow front roll and around the gate draw.
Correct the previous pass's material diagnosis: the thin step also remains in
the constant-paint ablation. Separate actual-GLB coat-roughness, base-roughness,
coat-weight, metallic and normal ablations retain it. No new paint decoder or
studio change is justified. The front's reflection rays do not hit the car
again. Nearest-point normal projection across the roll changes the sampled
normal phase between its irregular chords. A smooth height fit to our own
parent in the nose-aligned chart supplies a coherent derivative instead.
Its diagnostic anchor residual is 1.12 mm at p95 and 8.42 mm at the extreme;
it approximates normals, and does not move the accepted surface to that fit.
The source gallery trial removes the thin step.

The gate needs both aligned rows and smooth derivatives. Differentiating the
parent's triangle **positions** through the fairing blend introduces its
faceted slope into an otherwise smooth die field. Blend the parent's smooth
normal derivative with the implicit die derivative, including the derivative
of the blend weight. Replace the central radial chords with 40 mm transverse
and 10 mm crease-aligned rows; retain all 81 boundary vertices. A sparse trial
still tears the highlight and is rejected. The finer trial makes the central
recess coherent; the letter plaques are constructed against the final skin.

Fund the visible rows by dissolving one-degree, nearly coplanar lower fascia
chords below 0.60 m. Every retained vertex stays fixed. Original-surface probes
at the resulting triangle centers and edge midpoints measure at most 0.272 mm
front and 0.648 mm rear, and retire 328 + 1,277 triangles. This is a sampled
chord-deviation check, not a continuous bound. The resulting source is 59,871
triangles, under the unchanged 60,000 cap. Rebuild, bake and re-audit the actual
GLB before accepting documentation images.

The native 2000 px source audit warrants one last transverse refinement inside
that hollow: 20 mm central columns, leaving the 40 mm outer columns and all
cuts held. The chart now replaces 293 triangles with 2,409. The front lower
allocation permits two degrees and measures 0.683 mm at worst; rear stays at
one degree / 0.648 mm. It retires 747 + 1,277 triangles, producing **59,964**
in total. The topology audit passes after explicitly removing nine retired
wire diagonals; independent regenerated transforms, faces, vertices, split
normals and material assignments match across 471 objects / 442 meshes.
Both source solid sweeps and coupled supports pass. The source close-ups are
`build/hatch-delivery/source-fine/{face,gate}.png`; the exported candidate must
still pass the final image audit.

### Delivery pass 5 — isolate the rear glass and retain its accepted values

Color/value first: the actual-GLB rear daylight trial retains side glass at
122.52 against the white-balanced photograph's 123.68 and backlight at 122.01
against 121.16. Paint, dirt and optical material factors remain held.

The native rear gallery view has a split hook-shaped reflection in the lower
backlight. Hiding negative-fill flags from glossy rays does not remove it.
Opaque reflection-only glazing retains it, ruling out light seen through the
cabin. Reflected-ray probes do not hit the car again. The lower field inherits
a saddle/normal inflection from the adjacent die; an unconstrained whole-pane
fit also incorporates the nearly horizontal header return. Both that fit and
a local unconstrained fit retain the hook and are rejected.

Fit the pane's own lower positions with its transverse crown and rake, using
a gently convex longitudinal mold derivative. The 25 m longitudinal radius is
an original design constraint, not a measured reference dimension. Blend it
into the held header. The resulting game normal correction is at most 8.05°;
no pane vertex, gauge, cut, tint, IOR or roughness changes. Its positional fit
residual is 11.52 mm at p95 / 15.55 mm maximum: this is explicitly a **normal
approximation**, not an exact positional reconstruction. The actual-GLB trial
replaces the split hook with a coherent broad reflection and preserves the
accepted measured value exactly. The source gallery confirms the same result.

The source topology, dimensions, closure/steering/wheel solid sweeps, coupled
supports and independent regeneration pass again. Re-bake and render the
actual exported asset before generating the final docs. The accepted gallery
studio recipe remains unchanged throughout; every ablation stays diagnostic.


### Delivery pass 6 — reject intersecting gate backs at native size

Color/value first: the native gallery retains the accepted five finishes,
deep cavities and bounded highlights. Badges, optics, fuel reveal and casting
chamfers survive the 2048 bake. Both the main and an entirely empty-output
rebuild pass `make` and `make check`, but those checks do not excuse the
remaining gate image defect. No docs are accepted from this candidate.

The 2000 px gate close-up exposes a dark slit and torn reflection below the
draw. Disconnecting the already disabled paint normal does not change it.
Ray intersections identify the coarse **reverse sheet** in front of the
refined outer surface, and the molded **inner card** protruding through the
hollow. The apparent large black handle is that card, not a designed aperture.
A reflected ray can also see these surfaces. An adaptive redistribution of
the same outer triangle budget does not fix the occlusion and is rejected.

Retain the outer hollow and regular chart. Round only its narrow die ridge
with a 6.5 mm / 25 mm Gaussian crown in the local detail field; the diagnostic
change from the preceding fairing is at most 2.828 mm. The original parent,
accepted raw form and other panels use their unchanged field. Retreat only
buried reverse vertices until six-millimeter barycentric probes keep their
chords behind the actual outer triangles; held outer/cut vertices never move
for this clearance operation. Seat the molded card from its whole face rather
than its locator rows. The game reverse is an economical occlusion surface,
not an exact reconstruction of uniform sheet gauge. The visible hems retain
their original gauge. No triangles are added.

The combined source trial removes the false black slit and crossed facets;
the softbox follows the recess as a continuous band. An independent seven-
millimeter offset ray grid is added to construction verification, comparing
actual triangle intersections for the outer sheet, reverse and card. This
checks the previously missed self-occlusion, separately from serialization
and assembly motion. Rebuild, bake and re-audit the resulting GLB and cargo
pose before accepting final docs.

The regenerated source keeps the raw accepted form byte-exact across all
132 objects / 119 meshes. Outer fairing now measures 2.333 mm maximum on the
game mesh. Buried reverse vertices retreat at most 11.067 mm and the card
35.089 mm; high-source values are 4.108 / 31.985 mm. The existing hidden-back
optimizer can now safely retire another 112 triangles, yielding **59,852**.
After that optimizer, the independent grid finds minimum reverse/card Y gaps
of 0.662 / 18.629 mm on the game mesh and 1.002 / 19.062 mm on the high source,
with zero piercing samples. The rejected candidate fails the same check:
1,328 reverse and 596 card rays pierce by up to 7.215 / 15.195 mm. These are
sampled triangle measurements, not constants or continuous guarantees.


### Delivery pass 7 — exported gallery accepted for documentation

Color/value first: open all fourteen 2000 px Cycles views, all five paint
variants and the native Eevee hero from GLB `fcbbc20b6a172beec6b16694985044afe6e93a78dbace6e112a0dbeb0107656e`.
The exact pickup gallery constructor, light diffusion and AgX setup remain
held. No hero RGB channel clips. With floor excluded, 25.89% of its vehicle
mask is below 0.10 display luminance; upper blue paint remains blue, cavity
shadows are deep and highlights roll off. Porcelain does not wash out.

Follow each card edge across hood, fascia, greenhouse and gate. The front
roll is continuous, the header shard and backlight split hook are gone, and
the gate has no exposed reverse sheet or trim slit. Its retained concave draw
now reads as painted sheet. The open cargo view retains seated trim and
working supports. Inspect grille webs, all badge/plate words, optical shells,
fuel reveal, spoke chamfers, tire carcasses/lettering and road film too.
Lettering is legible in its close-ups; wear stays localized to its causes.
A small amount of grazing interpolation remains near held patch margins;
the 32-station wheel lip and economical headrests/trim still reveal the game
budget at extreme range. Eevee's thin-sheet reflection/transmission fallback
is weaker than Cycles. Do not describe the result as indistinguishable from
a photograph in every close-up.

Re-run and inspect both source and exported matched-light pairs. On the
export, sampled upper paint medians are unchanged by the bake; road film
changes 0.00–0.93 display levels. Rear side glass is 122.52 versus the balanced
photo's 123.68; backlight 122.01 versus 121.16. Source-to-export loss is +0.72
for backlight, +3.79 for windshield and +5 / +7 for the tire patches. Tires
remain the largest measured bake change. No accepted material is recolored
to hide it. White-balance neutrals remain the front siding and rear mullion;
these lit patch values are not claimed as albedos.

The requested six same-camera before/after crops live in
`renders/hatch-delivery-comparisons/compare-*.jpg`, with camera/exposure/paint
and source hashes in `comparisons.json`. Four additional gallery crops show
the header, nose roll, gate and backlight changes, with their own manifest.
The header's earlier candidate is the actual rejected audit-one GLB, not the
later candidate in which it was already fixed. Normalize resolution before
identical crops; do not enlarge the after image to exaggerate its recovery.

The empty-output archive build and `make check` pass. Its source arrays match
471 objects / 442 meshes exactly; UV reports and all 174 GLB accessors match.
A fresh GPU bake changes one 8-bit level in 30 Normal pixels, three ORM pixels
and two BaseColor pixels. The independently saved source-blend provenance
hash differs too, so the hatch GLBs are not byte-identical across those two
full builds. The pickup's complete GLB remains byte-identical. All 24 kit
modules still match the tested kit snapshot and passed sequentially from
clean scratch. Native finals, contact/mask sheets and comparisons are now
accepted for generating the five bounded docs JPGs; inspect those separately
before committing them.


The five generated documentation JPGs are also opened at native size and
accepted: hero 156,259 bytes, details 185,066, turnaround 124,379, five colors
195,758 and scale/Eevee 195,856. Each is 1600 px wide and below 200 KB; no GIF
is needed. Captions use presentation names, and no photograph or diagnostic
ablation enters the committed gallery. Documentation is committed only after
this inspection. The pickup hash is checked again unchanged before delivery.
