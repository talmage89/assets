# River form review

All judgments below concern the form checkpoint. Quick PBR and placed coarse
maintenance are not a final look-dev delivery. Photographs are type references,
never projected textures. Every inspection render is imported from external
glTF. No docs JPGs are committed at this checkpoint.

## Reference and construction audit

Read the complete repository contract, shared kit, common brief, owner log,
rifle README/tools, native town/site/ground/vehicle/botanical families and all
four skatepark briefs. Read the unmerged freeway README and girder/support
source read-only. Main was merged at the start; no freeway branch code or map
was copied. Freeway subsequently landed on main and was merged at `dcc2132`;
pass 6 uses its native factories and shared maps. The Type III section remains
independently derived from FDOT 20130.

Viewed the four period photographs in `build/reference-sheet.jpg` at size and
the actual FDOT section. The type differs from the wider steel Huron reference;
the bank photo hides a simpler bridge's ends. The comparisons must retain those
differences. Camera height priors reject an initial mathematically plausible
but below-ground fit. Final fits retain their residuals, not just a nominal lens.

Photo balance uses assumed neutrals: Raisin parapet concrete, Huron concrete
cap and, in the final bank study, the weathered gray wooden dock. Earlier
rejected studies used Morrison's trail wall. The originals are unchanged. Exact patch
coordinates, medians and neutral gains live in `build/photo-calibration.json`.
Neither the photographs' exposures nor these patches establish absolute albedo.

## Pass 1 — exported Cycles, 900px / 16 samples

Color/value first: water is uniformly blue and mirror-like, missing the depth
and bank-edge variation in the Raisin photograph. The selected foreground
photo patch is itself blue from sky reflection; it is not an albedo target.
The repeated normal makes a rigid comb in the rural hero.
Concrete is flat gray and provisional. Under-deck shadows are deep, but the
sky is desaturated. Exposure remains fixed; the water/sky fixes change the
material and illumination spectrum, not exposure to whiten the concrete.
The selected displayed RGB/luma patches are in `build/pass1-values.json`.

Opened and critiqued **all four frames**, `renders/pass1/{101,202}/{hero,above}.png`:

- Both aerials expose a rectangular world ending in black. The downstream
  trees even float beyond that end. Add explicitly costed distant valley/water
  continuation, native trees and homes, keeping the 300m core separate.
- Downtown is an office-park array of freestanding brick buildings. Build
  party-wall blocks by each native building's actual lot width, align their
  street fronts and put their rear additions/fire escapes toward the river.
  Give the blocks their real streets, walks and service alleys.
- The rural banks read as a regular steep trench. A blanket 2.1m fill floor
  was overriding the low bank and riverwalk; remove that override except on
  the actual approach fills. Preserve the pool, inner bar and riffle section.
- The bridge's overall girder/slab proportions read at eye height; its cap,
  bearing and approach construction still need the close inspections.
- The downtown walk's nominal .34m girder clearance fails physically. Lower
  the floodable path to .65m above water, giving 2.337m nominal clearance,
  and retain the raised city behind a separate floodwall. Cut soil below the
  span and seat it behind the abutment backwall, away from pads/girders.
- Native tree alpha is intact, but grass is too sparse against the reference's
  continuous low bank cover. Sample the actual triangulated terrain under all
  rock and card placements; retain dense colonies rather than isolated tufts.

Implemented for pass 2: a welded, consistently outward closed water shell for
depth-dependent absorption; warmer green-brown attenuation, more roughness and
less normal amplitude; richer sky; actual terrain ray sampling; critical
water-edge/walk/abutment stations in the mesh; corrected street blocks and low
walk; distant world continuation. Fine weathering is deferred to look-dev.

## Pass 2 — exported Cycles, 1000px / 24 samples

Color/value first: the water remains too blue/dark, and the boosted sky is
too cyan. Absorption alone does not communicate suspended sediment. Introduce
modest green-brown scattering from exported uniform coefficients, keep the
surface nearly neutral/transmissive, and soften the dominant ripple comb.
Increase sky fill to read the underside without changing exposure or the
low-sun direction. Concrete remains a provisional shared Ground finish.

Opened all **19 scene/module frames** at native size and all three composed
photo pairs. This pass is **rejected**, not a delivery gallery:

- Both aerials show black stripes across terrain and alternating far water.
  Unit-length normals passed, but that test missed orientation. Recalculating
  each disconnected open quad had reversed many faces. Preserve authored
  winding on open faces, force heightfield faces upward, and check signed
  triangle orientation independently in the glTF. Distant water now uses a
  surface-only material; an open plane cannot define a finite volume.
- The downtown hero is blocked by a soil levee. A vectorized ray against the
  actual export hit RiverBank only **6.13m** ahead, at Z **2.296m**. The old
  bank-height floor applied at u=1.05 while the walkway cut began at u=1.10,
  leaving a 2.5m strip. Replace those overlapping conditions with an explicit
  shore / low walk / raised city profile.
- The downtown bar and abutment views are black or blocked. Place the bar
  camera at the actual exposed water edge, and move the abutment camera onto
  the city bank. The driver camera is too close to a hatchback; move it into
  the preceding traffic gap.
- Camera projection agrees within .025px but does not establish visibility.
  All three photo pairs fail as evidence: a tree/ground blocks the urban
  bridge, the bank camera is inside a native house, and the under-bridge camera
  is below the dirt bench. Move country houses back into the high floodplain,
  keep maintained access sightlines clear, and lower the under-bridge service
  bench. Do not accept the small fit residual as proof of a visible feature.
- The module sheet needs a receiving floor and names; black space conceals
  section thickness. The scale views do show a real 1.8m person and native car.
- Reopened FDOT 20130 at high resolution. The flange widths/web and overall
  depth were correct, but the vertical zones were not. Correct them to
  **7 / 7.5 / 19 / 4.5 / 7in**, with the ¾in foot chamfer. A new end-section
  accessor check measures all seven stations rather than only the envelope.
- Scuppers must penetrate the slab, not merely have pipes nearby. Cut the
  curb and slab, add open troughs and hollow outlets. Carry slab crossfall
  under the asphalt so its 60mm overlay remains present at the gutter.
- Flare the wingwalls 30° on real strip footings. Excavate the 12% boat-launch
  plane so its pavement is not hidden by uncut bank soil.

The new construction gate passes: actual exported section dimensions agree
within 2e-5m; sampled bearing gaps are zero; minimum sampled riverwalk clearance
is **2.34795m** (the prestress camber adds to the nominal 2.337m).
The next images must show the changes before they can be accepted.

## Pass 3 — exported Cycles, 1000px / 24 samples

Opened all twelve frames in `renders/pass3/`. Color/value first: the water
still reflects as broad blue smears; its low-amplitude normal and .24 roughness
lose the broken reflections in the photographs. The bank-edge view does show
submerged cobbles, but it is not enough. Increase normal strength and reduce
microfacet roughness so the surface breaks reflections instead of blurring them.
Concrete reads in sun, while underside cavities retain deep shade. No exposure
increase is used to turn the gray concrete white.

- The urban riverwalk is now clear in the hero; both underside inspections
  reveal the girder rhythm and support frames. The rural hero now stands on
  the actual trail, rather than in the shallows. Final planting clears its
  narrow maintained sightline while retaining native trees around it.
- The urban abutment inspection is mostly foreground soil. Relocate it into
  the dry under-bridge maintenance bay, looking toward the seat and wingwall.
- Roads end abruptly in both aerials. Extend them into the distant town/fields,
  grade them to the floodplain, and carry actual soil under their approaches.
  Bring Main Street's backs closer to their service alleys. The distant terrain
  remains explicit removable context, not part of the 300m reach budget.
- Independent edge incidence finds **1,000 open edges in each water shell**.
  Side closures sampled the analytic bed while the floor sampled triangles.
  Use identical sampled bottom points and require two faces per welded edge
  plus positive signed volume. The old visual claim of a closed shell was
  incorrect; this supersedes it.
- The former bearing check sampled the minimum girder end height, not its
  actual underside at the pad. Replace it with a ray onto each real bearing
  seat, then a ray onto the sole plate. Add short flat end seats and put the
  sockets at their centers. Also reduce the excessive deck overhang to .95m
  from the exterior girder centerline and align the wall cutwater with flow.
- House and tree placements in the final model use actual terrain seating;
  rural houses move beyond the bank camera. Lower the urban maintenance bay
  and its retaining cap to clear the measured under-bridge photo camera.

The twelve frames are retained as rejected controls. The final pass must prove
the volume, views and comparisons after a clean rebuild. Fine bank materials,
wear, turf response and maintenance texture work remain outside this form gate.

## Pass 4 — clean build, exported Cycles, 1280px / 32 samples

Opened all 21 scene/module images and the three photo pairs. Color/value first:
the water now breaks reflections and shows a darker brown/olive body from above,
but remains blue at grazing angles. The river's far surface approximation is
too light; lower its diffuse contribution. The hero exposure stays at −.4EV.
The underside inspections need normal photographic exposure adaptation, so
their final exposures are explicit in each frame's receipt, not a hidden grade.

This batch is **rejected**. The image gate independently rejected the urban
abutment frame as nearly black; no threshold was relaxed.

- The urban photo is blocked by a building. Moving aligned fronts inward was
  wrong: native depths are **27.432–33.528m**, not guessed shallow shops. Derive
  a safe street line from those actual lot depths, bend and bank width. Check
  all forty exported building bounds against the full walk corridor. Also
  exclude tree trunks from lots and paving rather than letting trees grow
  through brick walls. The urban riffle frame revealed the same overlap as an
  overhead slab; it is placement failure, not an exposure failure.
- The urban abutment camera hits the retaining wall only **1.647m** ahead.
  Choosing the wall bay's height from its start station left the −8..−6m bay
  high. Choose its midpoint. Keep the dry maintenance path unobstructed.
- The bearing close-ups reveal unsupported abutment plinths. Girder-to-pad
  contact was correct but insufficient: the stem ended behind the pads.
  Add the real projecting seat and test plinth-to-seat contact at centers and
  four near-corner points as well. Do not describe the old partial check as
  proof of a supported assembly.
- The rural bank camera sees a field, whereas Morrison's photograph sees a
  path; its small bridge-anchor fit did not validate terrain correspondence.
  Retire that final comparison and add a 2008 Huron bank-and-water study.
  Its EXIF reports 99mm equivalent. Shore shapes and scale are unsurveyed;
  retain the larger fit residual and disclose the different wooden landing
  and autumn vegetation. These are comparisons, not scene reconstructions.
- Grass cards remain narrow toothpicks over a smooth base. Widen the low
  clumps, cross their cards and increase colony density, keeping the trail
  and launch clear. Add the riverwalk's actual square-bar infill. All new
  geometry remains separately costed and the new construction stays within
  the reach/bridge budgets.
- A Cycles **76 > 64** closure warning comes from its conservative allocation
  for the two volume nodes plus Principled surface, not proof of a bad mesh.
  Use one Volume Coefficients node with the same RGB absorption/scattering
  coefficients and HG anisotropy. No native shader or delivery is rewritten.

After these changes, raw/import checks pass: closed positive water shells,
30/20 girder-seat contacts, 150/100 plinth-support contacts, fifteen walk
clearance samples (minimum **2.34770m**) and forty building/walk bounds checks.
The exact rebuild repeats **41** generated mesh/image/manifest files byte for
byte. Final images must still show the corrected construction and placement.

## Pass 5 — corrected exported checkpoint, 1280px / 32 samples

Opened all 21 scene/module frames, the three composed photo pairs and both
contact sheets. Color/value first: the bridge has readable sunlit gray faces
and deep underside cavities, and the aerials show an olive/brown water body.
The low-angle water is still too blue and smooth beside the balanced Huron
bank photograph. This is a recorded appearance miss for the next look-dev
round; it is not a claim that a closed volume proves water realism.

- The downtown hero now shows the low walk, backs of connected brick blocks,
  actual traffic and a town continuing beyond the crossing. The rural hero
  has its own bend, wooded banks, gravel edge and fields/houses beyond. These
  are distinct plans. Both aerials still expose regular analytic bank slopes
  and an abrupt change to the distant water approximation.
- Girder/bearing close-ups now show pads seated on the projected abutment
  shelves. Raking under-bridge views expose the section, diaphragms, drains
  and conduit rather than hiding them behind soil. The rural abutment view
  communicates wingwall and riprap better than the urban view.
- One urban abutment camera remained blocked by foreground retaining work.
  Move that inspection above the water toward the downstream wingwall. The
  strict camera gate correctly rejected the old image; rerender that view
  and require its new camera and unchanged bundle hashes to agree. The new
  frame shows the assembly, but the wall still takes too much foreground.
- Broader crossed grass cards provide continuous bank cover, but the clumps
  and substrate still look procedural at water-edge distance. The riffle's
  foam strokes are provisional and too evenly distributed; final causally
  driven broken water is a look-dev task.
- Raisin's bridge is now visible in the matched frame. The Huron underside
  comparison is darker than its reference and compares our concrete girder
  to a much wider steel bridge. The 2008 bank comparison replaces the failed
  Morrison fit; it shows water/bank, but its 56.11px residual, elevated fitted
  camera and unmodeled wooden landing prevent an exact-match claim. The
  autumn trees differ. The neutral patch was inspected on gray dock decking,
  not sampled from blue water.

`make`, `make check` and `make repeat` passed after the camera correction.
All 24 required frame receipts agree with the current export bundles and
camera definitions; the gate checks visibility histograms but does not judge
appearance. Photo projection verification agrees with the kit within .004px;
that proves projection implementation only. This pass preceded freeway's
main landing; its image archive is under `build/river-review-archive/pass5/`.
No final docs images were committed.

## Pass 6 — shared construction and distant-world controls

Freeway landed on main and was merged. Replaced the duplicate bridge module
construction with calls to its native factories, retaining our cited Type III
profile and smaller crossing dimensions. Reused its Concrete and Zinc images.
The adapter preserves circular 1.2m columns and adapts the cap/seat geometry;
the native fixed overpass delivery is unchanged.

Opened five refreshed controls: urban hero, aerial, under, bearings and pier.
Color/value first: shared concrete reads gray in sun, while the bearing close
view is too dark for inspection. Increase that camera's explicit exposure
from +.8 to +2EV; do not lighten the material. The quick runoff strokes and
algae bands remain geometric placeholders, visibly too regular for final art.

- Lamp plates were wider than the parapet crown. Add local cast pedestals,
  put all four bases on their actual top surfaces and face arms over the road.
- Some native guardrail feet stood several millimeters above uneven approach
  soil. Lower their mounting datum and sample actual exported bottom vertices.
  This checks seating, not the buried length/strength of a highway post.
- The underside photo anchors still used the old .8m cap. Use the actual
  shared 1.10m cap and its 50mm chamfer endpoints. The residual grows to
  **20.97px**, honestly showing the mismatch with the wide steel reference.
- The aerial exposes side streets ending at ±150m and a straight change to
  the opaque distant water. Reject this context. Continue the Main Street
  roads/sidewalks toward ±650m, carry their elevations with the actual valley,
  extend native neighborhood houses and riparian maples, and replace painted
  distant water with finite closed bodies using the same medium and normal.
  Add the submerged bed beneath them; check their welded edge incidence and
  signed volumes independently. Cost all continuation as removable context.

The pre-continuation construction gate passed: 196 light-base samples have
zero measured gap; 672 rail-foot samples per crossing sit 3.6–18.7mm into the
soil. Girder/pad gaps are zero and the largest plinth/support residual is
.00000024m. Original 519 delivery files remain byte-identical, as do all 628
current dependency files. These controls are archived at
`build/river-review-archive/pass6-controls/`; the full refreshed set follows.

The next eight city frames were also opened (hero, above, under, bearings,
pier, abutment, driver, riffle). The aerial rejects the first continuation:
separately closed adjoining volumes produce a dark refracting line. Remove
their internal end faces, weld top and bottom vertices and use one closed
water body; retain core/presentation limits as extras for streaming. Also
continue horizontal surface normals through that boundary. The water budget
now includes its presentation extension rather than hiding it in context.

The riffle view also exposes an unsupported service alley on the natural
right bank: its street elevation preceded the full raised terrace. Move it
inland to the terrace, follow the local valley grade, insert the actual
terrace/alley stations in the terrain and sample the exported paving against
soil. The new gate rejected a stale pre-station mesh with a **.2194m** gap;
do not loosen its .04–.10m paving/base interval to accept that geometry.
These eight controls are under `build/river-review-archive/pass6-water-interface/`.

## Pass 7 — connected-water form controls

Opened the five connected-water controls (urban hero, above, under, bearings,
pier) at native size. Color/value first: water is dark olive beneath the bridge
and blue where it reflects the clear sky; the repeated ripple field still
looks too uniform. The aerial now has a continuous reflection/depth response
through the former boundary, with no black closing-plane line. Streets
continue beyond the site. The bank still reads as a regular constructed
profile rather than accumulated slumps; final material work will not, by
itself, solve every such silhouette. Retain that weakness for the form review.

The water is now one closed, outward mesh through ±800m, including the
300m core. Exported signed volumes are **39,105.8 / 46,992.7m³** for the two
whole presentation bodies, not measurements of only the core. The full water
allocation is **31,480 triangles per crossing**, including foam/continuation.
The 540 actual urban alley samples now measure **.0749996–.0750003m** above
soil, matching their paving/base allocation. The five controls are archived
under `build/river-review-archive/pass7-connected-control/`.

Before the last full batch, audit also found the drift too far ahead of the
supports and insufficiently immersed. Place it across local flow against the
upstream column/cutwater and sample its actual exported vertices against the
pier and water surfaces. Closest vertex-to-pier distances are **4.29mm** at
both bents and **6.72mm** at the wall nose; wood extends about **108mm below**
and **178mm above** the water. This is a geometric contact/immersion check,
not a buoyancy simulation. The former log placement is rejected.

Opened all fourteen pre-skirt frames: the full city set plus rural hero,
above, under and bearings. The city abutment angle exposes the unclosed
75mm paving gap: top-to-soil spacing alone did not prove a solid base. Add
the exposed edge faces, omit buried undersides/internal bay walls, and measure
the bottom vertices against soil as well. **1,057** actual alley-base samples
now sit **4.9996–5.0004mm into soil**. The corrected body retains its 75mm top
allocation. Break up the evenly spaced drift branches; their former comb is
visibly artificial. These controls are at
`build/river-review-archive/pass7-pre-skirts/`.

## Pass 8 — current exported checkpoint, 1280px / 32 samples

Opened **all 24 current frame receipts**: twenty crossing inspections, the
module sheet and three calibrated reference views. Also opened all three
composed photo pairs and both contact sheets. All rendering was serial Cycles
GPU through the shared lock, from the external-image glTF imports.

Color/value first: sunlit bridge concrete reads gray, with deep cavities and
unclipped highlights. Hero display-luma percentiles (1 / 50 / 99) are
**0 / .362 / .849** downtown and **0 / .429 / .873** rural. These describe the
rendered tonal range, not measured surface albedo. Compared with the balanced
photographs, water remains too blue/smooth at grazing angles and the repeated
ripple pattern is conspicuous. Shade and the bar edge show a darker body and
submerged pebbles, but the riffle does not yet sell broken moving water.

- The two places have distinct channel/spans/pier/land-use plans, actual
  traffic, native trees and town/field continuation. The aerial water join is
  continuous, without the former internal-face dam. Periphery is still a
  sparse, repeated presentation neighborhood, not a finished town layout.
- Under views show the Type III rhythm, diaphragms, bearing shelves, open
  outlets and conduit. The rural abutment view shows its seat, wingwall and
  riprap. The city abutment view remains over-dominated by the foreground
  floodwall; it is a weak inspection composition, not a hidden success.
- Bank silhouettes remain too regular. Local slump lobes, overhangs and sod
  breaks need more specificity; changing roughness cannot fix that form.
  Grass/card colonies and the pebble/riprap texture are visibly provisional.
  Runoff triangles, algae bands and repeated patch shapes are coarse causal
  placement markers, not acceptable final weathering.
- The balanced Raisin pair exposes the different setback/shore arrangement
  as well as the simpler parapet/bridge silhouette. Huron's steel underside
  differs in class and width, and our paired roof is too dark to judge its
  surface response. The separate raking underside inspection is clearer.
  The 2008 bank pair has a different landing, season and channel shape, plus
  an unsurveyed **56.11px** fit residual. None is a replica or a completed
  appearance match. Final fitted RMS is **12.69 / 20.97 / 56.11px** for
  urban / under / bank. Assumed neutrals and gains are retained in the receipt.

Current proof, all passing:

```sh
make model check BLENDER='blender -t 1'
make repeat BLENDER='blender -t 1'
make BLENDER='blender -t 1' WIDTH=1280 SAMPLES=32
blender -t 1 -b --factory-startup --python-exit-code 1 --python ../kit/photo_match.py -- verify --calibration build/photo-calibration.json
```

The complete make exited zero. The independent projection check agrees within
.00368px; it proves optics implementation only. All 24 export bundle hashes,
camera receipts and visibility histograms pass. The deterministic geometry/
manifest/image comparison repeats **41 files**; all **five CPU images** were
also independently regenerated and compared by SHA-256. Fresh import counts,
finite tiling UV/density, unit normals, closed positive water shell and actual
construction contacts pass. Atlas overlap/bake fidelity are not certified at
this quick-material checkpoint. **519 original / 628 current** pre-existing
delivery files remain unchanged. Repository rules pass; no kit/index changes.

The README contains measured modules, category totals, material/draw counts,
bytes and shared-image memory. Presentation vegetation/context are expensive
and unbatched; no final engine performance claim is made. Stop here before
look-dev, as briefed. Nothing is needed from the lead to reproduce the checkpoint.
A future shared bridge-factory API with section, cap and bearing parameters
would replace the local compatibility adapter without duplicating factories.

## Pass 9 — rejected handoff, form before appearance

Color/value first: opened the handoff contact, both 1280px heroes/aerials,
bearing, pier, abutment and riffle, and the photo contact at native size.
Compared directly with Raisin and Riverside Park photographs, using the
recorded parapet and gray dock neutrals. The concrete shadows are cyan;
the water shares that sky color across nearly its whole surface. Riverside
has olive/brown body color between interrupted blue reflections. Its sunlit
bank grass is much lighter than the black-green card masses in our hero.
These are appearance failures despite the passing construction receipts.

The city aerial is a repeated six-building block beside a straight lawn
channel. The rural reach has isolated crowns over an unworked field.
Neither reads as its requested place. Preserve the accepted Type III section,
generators, exports' paths and shared canonical images; move unique native
rear elevations toward working river alleys, and add a continuous rural
maple/shrub strip, agriculture and occupied road frontage.

The cap's pointed runoff polygons and the bearings' blank stack fail close
inspection. Replace the former with alpha texture masks in the existing
512 sheet, and articulate the latter without changing the seat datum.
The abutment inspection needs a bank view showing the complete wingwall and
stone slope. HEC-23 DG14.8–11 informs its wrap/toe coverage; no hydraulic
stone-sizing calculation is claimed. Cutbank retreat, sod breaks, root
exposure and a steeper riffle must alter form before material tuning.

The full-size handoff is preserved under `build/round2-before/`. The bank's
hard 99mm lens constraint is rejected for this unsurveyed authored channel.
The old steel underside is replaced by FHWA's 2008 concrete I-beam photo.
Four measured support landmarks fit framing, not the whole beam system.
Subsequent export controls must decide whether the new light, water and age
actually work; these changes are not accepted merely because they build.

## Pass 10 — 960px exported controls, rejected details

Color/value first: opened all sixteen new crossing frames and all three
composed photo pairs at native size. Concrete is now neutral/warm gray and
the sky has depth. Grass is visible and yellow-green rather than black.
Compared with the neutral-balanced dock and concrete photos, water is still
far too silver: the desaturated lighting sky dominates its reflections.
The cap's salt patch is too pale/opaque and its grime reads stamped. Reduce
salt opacity, restore the blue visible sky to glossy rays, and drive the
normal/roughness continuously from the exported flow vectors.

The city now has different native rear walls, escapes, doors and dumpsters
beside the river. Its aerial still opens onto empty lawns outside the first
rows. Add independently seeded opposite block faces across Main Street.
The farm has a convincing denser bank strip, but the hay swaths look like
painted warning stripes, and old random trees stand in the fields. Fill the
stubble field with close-value harvest rows and move those trees to fencerows.
Correct the houses' orientation toward their road/driveways.

The section and girder lower flanges read under raking light. The downtown
bearing and abutment controls fail: their low cameras lie in the newly added
stone/soil. Raise them from the actual bank profile and gate camera/rock
clearance. The rural bearing is legible but too low to inspect the anchors.
The rural abutment shows the stem and armored slope; keep that bank context.

The riffle has obvious broad triangular slabs and opaque floating white
sticks. Reject both. Use a denser still-budgeted water grid, modest physical
relief, continuous analytic surface normals and alpha foam at the actual
surface. The raw flow remains game data; its continuous shading coefficients
will be documented alongside the existing volume reconstruction.

The four-point underside fit of .61px is rejected despite its number: its
camera looks into the cap. The photographed visible column is the near end
column, not the center column. Correcting that correspondence gives 10.93px
with a camera on the low bank outside the structure. The urban 12.69px and
bank 11.57px framing remain. The new fit still needs an exposed render to
prove visibility. No low RMS is accepted as appearance or camera-clearance
proof. Controls are retained at `renders/pass10/`; their photograph frames
are archived before the next render batch.

## Pass 11 — full exported revision, rejected surface and inspection faults

Color/value first: opened all 21 new 1280px crossing/module frames and the
three freshly composed pairs at native size. The bridge is neutral warm gray,
the sky has depth, and the reeds catch yellow-green sunlight. Those changes
hold. Water is still much too dark blue in the bank pair compared with the
dock-balanced Riverside photograph. Broad smooth reflections suppress its
own color. The bar's high-contrast circular clasts look printed; applying the
same bed map to quarry rocks makes polka dots. Reject both surface responses.

The urban hero now has native rear doors, escapes and service equipment at
the river, and the rural hero has layered vegetation and occupied frontage.
The aerial still shows similar-height Midwest roofs and empty ends of rows.
Use varied native regional parameter draws, extend the rows, and use their
remaining unique buildings along the crossing street. Native per-building
budgets remain enforced; the river does not alter downtown's factory.

The bearing images fail despite the new geometry: the outside keeper leg
conceals its own anchor nuts. Put that leg beside the pad and the nuts on
the outboard horizontal foot. The city camera sees soil, while the rural
seat macro makes the missing nut visibility especially clear. The additional
camera controls show the city pier seat clearly; retain that view after the
construction correction. The abutment bench also buries most of the stem.
Lower its under-deck bench and blend to the outer bank, exposing the actual
retaining construction rather than moving a camera through ground.

Quarry stones crossing the clipped approach soil have stretched lower
corners and become tall posts. Reject placements with excessive soil-height
variation; grade the toe outside the retaining wings. The farm's large hay
quads intersect their undulating support, producing triangular green gaps.
Assign the harvest rows on actual terrain faces, and subdivide the drives
against the measured soil. These are construction faults, not shadows.

The wet-band atlas is upside down for algae: its dense origin is at the top,
leaving squared high edges. Reverse that chart for water-grown stains and
connect the column band's heights smoothly. The cap runoff direction stays
unchanged. The riffle's foam is too fine and faint; increase its broken
coverage and actual surface relief. Native boxwood was stretched vertically
into topiary-like cones; use lower, wider, leaning clumps.

The replacement concrete underside is exposed and readable at **10.93px**;
its wider fascia view still differs substantially from the photograph's
interior beam arrangement. Four support anchors prove only that framing.
The urban fit remains **12.69px**, the bank **11.57px**. Pass 11 exports,
pairs and receipts are retained at `renders/pass11/` and
`build/pass11-matches/`. Its full make, construction/preservation gates,
41-file repeat and 20 identical-camera panels passed. Passing them did not
make these appearance faults acceptable.

## Pass 12 — targeted camera and scattering controls

Color/value first: opened all ten 960px controls. Increasing volume scatter
alone barely changes the grazing hero reflections (A/B mean pixel difference
is .154/255). The water needs stronger, less repetitive local surface slopes
so the turbid body contributes between reflections. Keep transmission and
the closed volume; test the stronger flow-driven normal against a fresh
export rather than calling the scattering-only controls a solution.

The city pier-seat control clears the terrain and frames the laminated
stack. The rural abutment seat control frames the pad clearly. Both still
show the keeper blocking the nuts, confirming the construction correction.
The two city abutment controls from across the river show the enclosing
riverwalk but hide the stem behind its bank. Prefer the bank inspection
after correcting the bench itself. Controls remain in
`renders/pass12-controls/`. None is final checkpoint evidence.

## Pass 13 — corrected construction and stronger exported flow

Color/value first: opened all twelve 960px crossing controls, the three
fresh pairs and their contact at native size. Concrete stays neutral/warm;
the wet body now contributes olive/brown between blue sky reflections.
The riffle has visible broken white coverage and the bar's edge transmits
bed detail. Pools still look smoother and darker than Riverside's wind-
roughened autumn reference. The quarry stones are too chalky, particularly
beside wet silt. Reduce their dry value and darken them continuously with
height above water; keep the new bed's restrained angular clasts.

The keeper correction works: nuts and washers are visible outside the
upright, with the laminated pad and sole plate behind. The urban pier-seat
and rural abutment-seat cameras resolve them. Lowering the under-deck bank
exposes the retaining stem; the rural view shows its wingwall and armored
toe in context. Large quarry facets and broad cap repairs remain obvious
checkpoint simplifications. The abutments are no longer floating boxes.

The new native town is fuller and its one-, two- and three-storey rear
elevations vary. Its long frontage is assembled through downtown's validated
JSON-plan API and unchanged factory. Native checks rejected overly ornate
three-storey end corners; the retained end corners have two storeys while
interior three-storey elevations remain. All 160 new buildings passed their
native per-building caps. Rear parking clears the additions. Remaining lots
continue the crossing street; canonical distinct buildings continue the reach.

The bank shrubs are lower, wider clumps rather than tall topiary cones.
The farm rows follow the actual terrain now, but green slices persist at the
far side. Their second cause is the coarse lateral background skin overlapping
the core heightfield. Move its start to the actual sampled outer boundary,
with matching edge stations, rather than covering the crop with more planes.

The regraded soil exposed a real contact failure: imported rail feet were
up to 23.7mm above soil. Only their buried tips now follow the actual terrain,
with a `_GROUND_TIP` semantic. Fresh import measures all **672** tagged tips
per crossing: **−5.018 to −4.987mm**, inside soil, with the native profile and
404-triangle module unchanged. Bearing/plinth, walkway, camera and preservation
checks also passed. This proves sampled construction contacts; it does not
certify every contextual house or vehicle contact.

One render process received SIGTERM without a Blender diagnostic after four
valid controls. The remaining eleven were resumed serially under one GPU lock
and completed. No partial or stale frame is treated as final. Frames and pairs
are retained at `renders/pass13/` and `build/pass13-matches/`. The final full-size
set must show the last ground-overlap and stone-value corrections before this
checkpoint is reported.

## Pass 14 — full-size controls expose the last field cutoff

Color/value first: the 1280px heroes retain neutral warm concrete and deep
under-deck shadow. The olive/brown water body now shows between sky reflections;
the sunny reeds have yellow-green variation and seed heads. Wet quarry value
is closer to the silt than in Pass 13. Its large facets, broad repair masks,
regular town footprints and static whitewater still read as CG.

The full-size rural overhead reveals green teeth at one outer crop edge.
The lateral terrain no longer overlaps the core, but the crop assignment's
170m face-centroid cutoff divides its last triangulated strip. Continue that
material to the actual mesh edge. This adds no triangles or images. Keep
the cameras, lighting and all construction unchanged for the next control.
The complete preceding set is archived at `renders/pass14/` after its batch
finishes; its match set is retained at `build/pass14-matches/`.

The twenty-panel audit also rejects the urban riffle's black before frame.
Its revised bank camera clears the new channel but lies inside the accepted
town terrace. Raise that one camera above both surfaces and regenerate both
sides. Baseline rendering now measures each eye against the imported accepted
terrain; evidence composition also rejects nearly black images on either side.
The other nine urban comparisons were opened at their full 1280px-per-side size.

The independent Blender projection check agrees within .005px with all three
fits: urban 12.69px, bank 11.57px and underside 10.93px. The concrete underside
reference is readable, but its interior beam arrangement differs from this
exterior fascia view. Four cap landmarks do not establish full beam alignment.
The bank water remains smoother/darker than the wind-roughened autumn photo.
One subsequent model process ended with SIGTERM during export, without a
Blender diagnostic; no process survived it. Restart the build serially and
require complete fresh receipts before accepting the corrected evidence.

## Pass 15 — valid comparisons, measured crop-cell failure

Color/value first: all ten rural views and the three fresh photo PNGs were
opened at native size. Concrete remains warm gray, the water olive/brown
between sky reflections, and the reed heads sunlit. The overhead still shows
green teeth inside the hay field. Removing the outer 170m cutoff did not
resolve this inner edge; reject that attempted correction.

Ray tests on the exported triangles locate two adjacent pixels on opposite
halves of one quad: one uses hay and one lawn. Its corners are approximately
(46.629,−62), (66.039,−62), (66.486,−60), (47.052,−60)m. The whole exported
bed contains **37** crop quads divided this way. Classify each whole quad
and its row tint together, then check imported triangle neighbors for the
same failure. The correction needs no extra triangles or images.

The raised town riffle camera works on both exports. Its measured clearance
above the accepted terrain is **1.14503m**. Both PNGs and their full-size
comparison were opened; the other nine town comparisons were reviewed in
Pass 14. Baseline clearance and two-sided near-black gates now pass all twenty
views. Their receipts are `build/baseline-clearance-*.json` and
`build/fix-evidence.json`.

This serial restart completed `make`, `make check`, the 41-output exact repeat
and independent photo projection verification. All 628 existing delivery files
remain unchanged. The set is retained at `renders/pass15/` and
`build/pass15-matches/`. It is still rejected for the visible field defect;
the remaining visual limitations recorded in Pass 14 also remain.

The replacement classifies both halves from their original cell's four
corners. The regression check first reproduced all **37** failures on a fresh
import of the preceding export. A fresh corrected import then measured
**8,273** paired cells, **20** collapsed single triangles and **zero** divided
crop cells. Construction and 628-file preservation checks pass, with the same
triangle counts and image allocations. Its full-size appearance check remains
pending; these measurements establish material continuity alone.

## Pass 16 — completed export checkpoint

Color/value first: reviewed the final 24 export frames, three photo pairs,
both contacts and all twenty 1280px-per-side comparisons at native size.
The photo neutrals remain the urban concrete parapet, weathered gray dock
and underside cap; their measured gains are retained in the calibration.
Concrete is now neutral/warm with deep cavities, the sky is clear and deeper,
and the river has an olive/brown body between sky reflections. Reed blades
and seed heads have sunny yellow-green variation. Neither hero carries the
previous overall cyan cast. Bank water remains darker and smoother than
the wind-roughened autumn photograph.

The full-size overhead confirms the crop teeth are gone. All 8,273 paired
terrain cells pass the imported material-continuity check, with 20 valid
collapsed singles and zero divided crop cells. Rows now stay continuous.
The dense linked bank strip, occupied yards, drives, field boundaries and
sagging utility conductors give the rural reach its requested setting.
The town has distinct native rear elevations and working service courts
against the riverwalk, with streets and additional buildings continuing it.
The overhead still exposes a regular rhythm of footprints and roof systems.

Girder flanges, cap ends and seats read below the overhang. Bearing macros
resolve laminated pads, plates, keepers and outboard anchors. The bank views
expose abutment stems and wingwalls against seated riprap. Drips are texture
masks rather than spikes, but broad cap repairs and blank wall expanses still
lack the fine stain hierarchy of the photographs. Quarry stones remain too
faceted in macros; bank cards retain visible pixel edges and simple clump shapes.
Riffle foam and pier wakes remain static analytic approximations. The stock
glTF water fallback needs the documented engine shader for depth/flow response.

Final RMS is urban **12.69px**, bank **11.57px**, concrete underside **10.93px**.
Independent Blender projection disagrees by at most .00428px. These are selected
landmark fits. The underside's four cap anchors do not match its full interior
beam arrangement; the exported view is an exterior fascia comparison.

`make`, `make check`, the exact **41-output** repeat and the independent photo
projection check completed successfully. The five-image CPU regeneration
receipt remains exact, and all **628** existing delivery inputs are unchanged.
The final render process ended with SIGTERM after four valid frames, without
a Blender diagnostic. The remaining six views and bank pair were resumed
serially under the shared lock and completed. Bundle/camera/image gates verify
the complete set; no partial or stale frame is accepted and no job survives.
Per-piece and per-category costs are regenerated in `build/checkpoint-report.md`.
This is the requested checkpoint, with the appearance limits above retained.
No kit change, docs images, README gallery or top-level index edit is included.

## Pass 17 — light and storage controls

Color/value first: opened the seven specified handoff frames at native size,
then two 1280px light studies and four 1000px directional controls. Compared
Raisin's concrete parapet and FHWA's cap as assumed photographic neutrals;
the retained bank pair uses gray dock decking (no concrete in that frame).
The original glossy-ray sky was 8.6 times darker than the diffuse sky. It
made reflected water nearly black independently of its physical depth.
The first correction restores the real sky to reflected rays. Stronger
16-degree downstream-side sunlight separates the deck lip, web and flange,
and casts rail shadows on the walk. Foreground shade remains too dominant,
and the water's fine even ripple still reads as an analytic pattern. Reject
these as finals; revise the wave trains, depth response and surface hierarchy.

The storage control preserves all triangle indices and structural positions.
Exact sharing alone is insufficient because the distinct native buildings
dominate the downtown package. Bounded context position storage, normalized
normal/color attributes, decoded native UVs and omitted regenerable tangents
reduce the trial packages to 118.1 / 22.9 MB without reducing geometry. The
maximum position half-step is .362mm. The first fresh-import images expose
rectangular native leaves: the thin-leaf adapter ignores decoded UV transforms.
Reject that control and retain exact UVs for all vegetation materials. This
is a serialization/shader compatibility finding, not a visual acceptance.

The first complete geometry revision serialized at 111,687,574 / 22,839,068
bytes. Correspondence tested 5,500,602 / 930,971 original attribute vertices:
maximum context position errors .363 / .099mm, normal angles .382 / .387
degrees, color errors below .002 and UV errors below .000418. Every original
triangle index and structural position is exact. These prove storage only.
The civil audit rejects downtown at 161,307 triangles: capped tubes for tiny
form ties consume about 10k. Replace them with recess charts in the existing
sheet, and concentrate water tessellation at the shoal. Do not relax 150k.
The subsequent model process ended in SIGTERM without a Blender diagnostic;
no process remained. Restart serially with one worker and require fresh checks.

## Pass 18 — complete correction control, water rejected

Color/value first: opened all thirteen 1280px revision-three frames. Balanced
Raisin's parapet and Morrison's bank-bridge face on concrete; retained the
accepted Huron pair's dock neutral. Concrete samples are about .61/.58/.53
and .62/.60/.55 display RGB, with zero near-clipped hero pixels. Deep underside
shade is retained. The western sun still leaves the near walk and wall in
flat shade, so test the eastern side of the frame with slightly more sky fill.

The lower rural bank eye exposes the web, flange and overhang more clearly.
Retain the original high-trail camera as an extra comparison. Downtown depths,
heights, gaps and setbacks now break the former roof grid; native rear details
remain. Wall joints, tie recesses, weeps, ladder, stairs and lamps are visible.
The wall still lacks runoff from its coping joints. Narrow cap runs replace
the broad repair masks, but the white mineral edges need to sit in front of
the dark decal, not behind it.

Reject the water and quarry stones. Water reads as pebbled silver metal;
the bed barely shows at the bar, and ribbon foam sinks through the sampled
wave surface. The riffle is a zipper rather than broken standing water.
The new dark triangular stones replace cubes with pointed polyhedra. Rebuild
them from independent fracture planes, lighten their mineral albedo and drive
wetness/algae from each actual corner's height. Lengthen the wind ripples,
seat foam against the actual exported surface and test direct sunlight through
the water interface. This pass is not accepted for documentation. No gallery
has been created.

## Pass 19 — side-light control, excessive water chroma

Color/value first: inspected hero, overhead, underside and bearings at 1280px.
The eastern 16-degree sun finally lights the walk and wall, throws parapet
shadows down the exposed webs and retains deep cavities. Concrete stays gray
with warm highlights. The illuminated water, however, is excessively yellow
green beneath the bridge, and the overhead lacks convincing shallow-bed
transmission. Reject this water for final documentation. Reduce the medium's
scattering and chroma while retaining the new direct-light interface treatment.

The bridge's lip, web and bottom flange now separate; the overhead town's
varied depths and gaps survive. The four frames are archived in the worktree's
`build/river-review-history/pass19/`; earlier controls are in its `revision3/`.
The render process again ended with SIGTERM without a Blender diagnostic.
No worker remains. Use bounded serial workers with verified image receipts
under one GPU-lock acquisition, then rejudge every frame. No docs are approved.

## Pass 20 — exported shape control, stones and foam rejected

Color/value first: opened all eleven downtown candidate frames at native
1280px, including the concrete-balanced hero, underside, pier and bar. The
new medium is muted green brown in shade, with blue sky and warm bank
reflections; submerged bed and stones show at the bar. Raking sun lights the
fascia, web and flange, the walk and the panelled wall; cavities remain dark.
The stair, ties, weeps and access detail survive export. Preserve this tone.

Reject the riprap: changing cubes into eight-plane hulls did not remove their
common horizontal bedding and cuboid proportions. Give every fracture a full
three-axis orientation and less orthogonal cleavage. Reject the riffle foam:
flow-aligned geometry still carries isolated spot charts, so it remains
confetti. Replace that chart with a connected porous streak and lower the
urban riffle eye now that both comparisons use the same accepted bend.
The wind normal is too isotropic and cellular; use weaker, directional waves.
Cap runoff is narrow but its cropped heads form a printed comb. Follow the
actual chamfer with continuous soft gravity runs and adjacent mineral edges.

Stopped the render dispatcher deliberately after these failures; its managed
children terminated and the GPU lease released. All eleven produced images
were opened. They are archived in `build/river-review-history/pass20/` in the
worktree. This clean build's model/check passed, but its render/delivery did
not complete. No final docs are authorized by this visual pass.

## Pass 21 — focused export previews, geometric causes isolated

Color/value first: opened eight 1280px partial-export controls, two abutments,
piers, riffles and bars. These omit native town and trees, so their blue sky
reflection is not a final water-color control. The white cap lines are too
bright compared with the concrete-balanced FHWA cap; reduce their width and
reflectance. Preserve the full-scene medium from pass 20.

The new continuous foam reads as flow streaks over the standing waves, and
the weaker directional normals remove the cellular silver surface. The low
urban bank eye resolves the wave profile. Quarry orientation removes common
flat tops, but the trial's oblique halfspaces produce unbounded long shards.
Reject them. Bound fragments by actual radius, use four balanced corner cuts
and keep fewer, better graded blocks within the same civil budget.

The shallow-water bands are a separate geometry defect: a bottom offset at
sparse samples can interpolate above the actual triangulated bed. Put the
invisible closing interface below the whole bed, retaining physical depth
from the actual bed hit. Require an independent imported surface-clearance
check. The first corrected core counts predict 148,770 / 85,646 civil
triangles including the existing site and water continuation. All eight
previews were opened; archived in `build/river-review-history/probe21/`.
No final appearance claim is made from this partial scene.

## Pass 22 — bounded fragments and the real export tint path

Color/value first: inspected all eight revised partial-export controls and
both final cap controls at 1280px. Quarry stones are gray with varied brown
mineral tint, dark where wet; their axes and clipped corners now vary, with
no tall shards. Less exposure keeps sunlit abutment concrete from whitening.
The shallow bed is visible and the false underwater bright strips are gone.
Continuous foam follows the shoal's wave trains instead of scattering spots.

The cap control exposed a separate serialization failure: legacy MixRGB did
not export the authored maintenance vertex tints. Its COLOR_0 was entirely
white. Replace it with the kit's supported ShaderNodeMix pattern. Independent
raw accessors now range down to .102/.094/.075; both reimported cap controls
show narrow dark runs and thin, subdued mineral edges instead of toothpaste.
Require nonwhite maintenance values in the storage audit. Preserve all native
images; the accepted plant and legacy weather chart regions remain pixel exact.

Remaining CG cues in these controls are hard low-poly stone edges, very regular
analytic wave spacing and simple snagged wood. The previews prove the local
corrections, not the complete places: final approval still requires freshly
imported complete crossings, both heroes and photographic comparisons.

## Pass 23 — complete clean build, elevated foam rejected

Color/value first: opened all 25 complete export frames at 1280px, the
concrete-balanced bank/urban controls and the photographic pairs. The side
sun separates parapet, lip, web and flange, lights the walk and backs, and
retains deep underside cavities. Calm water reflects sky and banks with a
muted green-brown transmitted bed. The bar's false bright strips are gone.
Both Eevee controls remain paler around the waterline than Cycles.

Reject the elevated bank comparison: despite acceptable low riffle views,
the foam and transverse crests form a ladder across the shoal. A completed
clean make and an independent five-image texture repeat with zero byte error
do not establish appearance. Archive this set in the worktree's
`build/river-review-history/pass23/`; create no docs from it.

Four additional wall macro controls expose ties, panel seams, flood residue,
weep holes, the open outfall and ladder hardware. The accepted bench blocks
the new west ladder. Move the ladder four meters upstream, preserving the
bench, and check nearest actual imported bench/ladder surfaces. Smooth the
outfall barrel's radial shading without adding triangles. Remaining CG cues
include hard stone edges, pixel-stepped macro bank cards, repeated block
rhythms, analytic water and Eevee's weaker transmission/occlusion.

## Pass 24 — localized crests, solid ribbons still rejected

Color/value first: the partial export controls preserve the muted surface
and blue sky reflection; native trees/context are absent, so this is only a
shape control. Opened both low riffles and both elevated controls at 1280px.
Independent bowed crest trains improve the wave silhouette, but solid narrow
foam ribbons still look like wires. Reject this probe. Broaden the streaks,
introduce multiscale porous necks and holes, taper their opacity, reduce their
count and vary their start stations. Keep them confined to the shoal chutes.
Final full-scene comparisons remain required.

## Pass 25 — curved porous streaks, ready for the complete scene

Color/value first: opened all four revised 1280px partial-export controls.
The muted water and sky reflection remain; do not assess bank color without
the complete trees and town. The low views now show small standing trains
with curved downstream foam tails. Elevated inspection separates two broken
chutes instead of a regular wire ladder spanning the reach. Keep this shape
for the full exported comparison. The short analytic crests remain visibly
more orderly than turbulent water in the concrete-balanced Huron photograph.

The atlas preview initially appeared solid because the image display ignored
its alpha. Independent pixel inspection confirms transparent pores and
0–174 alpha values, so there was no image serialization failure. The actual
fixes are wider variable strips, curved paths, discontinuities, a continuous
UV chart per strip and multiscale porous coverage. No docs have been made;
judge both complete crossings and the matched-light bank view next.

## Pass 26 — complete clean exports and the elevated water gate

Color/value first: opened all 25 complete exported inspection frames at their
native 1280px width. Both 40mm bank heroes have sunlit gray concrete, deep
underside cavities, warm bank/building reflections and blue reflected sky.
The concrete-balanced Raisin and Morrison controls remain the value references.
The river is green brown in depth; bed and submerged stones remain visible at
both bars. The hidden-floor light bands do not return. Neither hero clips its
highlights in the display-value audit.

The low riffle views and the complete elevated bank comparison now show two
broken, curved foam chutes with short standing trains. The rejected channel-wide
wire ladder is gone. Source-field and shipped bank controls retain the same
flow shapes and muted tone, without projection holes or lost shallow detail.
The analytic crests remain more orderly than the Huron photograph's turbulence.
Accept this specific correction; do not describe it as a fluid simulation.

The overhead town has different neighboring depths, widths, heights, rooflines
and setbacks, rear additions, service gaps and parking. The underlying block
rhythm still reads regular. Both undersides resolve the I-section, overhang,
drip line, joints and scuppers; cap runs stay narrow with subdued mineral edges.
Quarry stones are graded gray/brown fracture hulls with partly buried toes,
soil/vegetation gaps and water-height tint. Their hard silhouettes, macro card
pixels, simple snagged wood and native quick context materials remain CG cues.
Eevee has paler waterline transmission and weaker underside occlusion than
Cycles. Preserve those controls and disclose the difference. The new ladder
and outfall macros still need their final inspection before gallery creation.

## Pass 27 — wall access passes; comparison exposure correction

Color/value first: opened all three assembled matched-light pairs at full size.
The urban and bank renders are darker than their corresponding illuminated
photo surfaces. Raise only those comparison exposures to +.35 / +.65EV;
retain the underside's +1.6EV, all optical fits and the heroes' separate light.
Do not create gallery docs until the four affected export/source controls
have been rerendered and inspected.

Opened both wall macros and both accepted-version controls at 1280px. The
barrel is hollow with a recessed interior; the poured bays have actual ties,
weeps, high-water residue and paint-over. The west ladder is accessible,
3.789m from the nearest bench surface. No accepted bench moved. The low sun
casts hardware and railing shadows on the walk and wall. The barrel rim's
limited segments and the flood-line mask remain simplified CG detail.
Clean `make` completed, and all 24 comparisons retain identical optical
cameras at 1280px per side. Appearance and numerical checks remain separate.

## Pass 28 — corrected pairs and encoded gallery

Color/value first: opened the four revised export/source comparison frames,
both revised pairs, and all five gallery JPGs at native size. Raising only
the urban/bank pair exposures opens their concrete, banks and water toward
the balanced photographs. No hero or material value changed. The pair fits
remain 12.69 / 11.57 / 10.93px; autumn foliage, structures and clear-sky
conditions still differ, so these remain estimated light/type comparisons.

All 30 delivered export frames have current bundle, camera, recipe and image
receipts. The gallery preserves the hero shadows and shallow-water detail
after encoding, at 1280–1600px wide and 176,899–198,538 bytes per JPG. Approve
the five images for delivery after repeat and independent texture checks.
The explicit remaining CG cues are analytic crest/foam placement, hard quarry
facets, coarse macro card edges, regular urban block rhythm, simple snagged
wood and native presentation materials. Eevee's pale waterline/weak occlusion
remains visible in its labelled controls. No simulation or renderer-parity
claim is made.

Final verification: clean build and final `make check` passed. `make repeat`
matched all 486 files byte for byte, including the five gallery JPGs and
delivery manifest. The independent 4096 rebake/1024 filter matched all five
shipped images with zero maximum/RMS byte error. All 633 existing delivery
files remain unchanged. The repository check reports zero errors, and the
final render/bundle/image receipts are current. No Blender worker or GPU
lease remains from this build. Kit and the top-level index were not edited.

## Pass 29 — last-round concrete rejection and revised surface sampling

Color/value first: opened the seven requested 56cce73 close views at their
native 1280px width before modeling. The concrete reads warm cream, despite
referencing the freeway maps. Checked the concrete-balanced urban and FHWA
underside pairs: the map's narrow 133–139 sRGB red range supplies mineral
grain, but the river bypasses the freeway's placed age. Keep the accepted
16-degree lighting, exposure, green-brown water and photo cameras.

Opened four fresh 1280px exported probes: 101 pier, bearings and floodwall,
and 202 abutment. The neutral gray tint, form seams and ties improve the
construction read. Reject their broad surfaces as still too smooth. Strengthen
meter-scale paste/pour variation and add an air-pore/paste layer in the existing
repair chart. Preserve narrow cap leakage, and add height-driven basal dampness.
The bright bearing exposure still makes its sunlit faces pale; this is a
remaining appearance risk, not proof that the first gray correction landed.

The first surface grid also adds too many wall triangles. Reduce wall sampling
to vertical color stations, retain its existing joints/ties, and spend geometry
on supports that need it. Packed riprap replaces isolated placements; sparse
rounded cobbles and the rounded gravel normal field replace most bar chips.
The first cellular texture probe looked like polygonal mosaic and was rejected;
the revised crowns use rounded radial relief and fines between them. Neither
probe is a final appearance approval. All five last-round fixes still require
complete exported views, budget checks and a second critique before docs.

## Pass 30 — six exported controls; freeze the remaining misses

Color/value first: opened all six 1280px last-surfaces exports (101 pier,
bearings, floodwall; 202 abutment, bar, riffle), against the previously opened
concrete-balanced urban/underside and bank photographs. Gray concrete is an
improvement over cream, but the first pore layer is oversized and graphic.
Reduce its size/opacity. The bearing exposure remains bright and its girder
faces too uniform. The first snag is light tan: darken bark and broken ends.
Abutment algae incorrectly follows elevated soil height; confine green growth
to water height and sample actual triangulated soil for splash darkening.

The abutment has a much denser stone blanket, but its exposed facets remain
too clean/light and ordered. Darken the gray/brown range, loosen the row jitter
and retain fewer fracture corners to pay for coverage. The first combined
export exceeds both the civil budget and 120 MB downtown package. The reduced
core probe measures 52,095 reach and 64,548 site triangles; adding the previous
measured complete water projects 148,441 civil triangles. That is a projection,
not the final independent export measurement. The full clean check must gate it.

The bar is visibly lighter, rounded and continuous rather than chips on mud.
Its texture still resembles flat discs and repeats; its sand/silt lee and
specific willow seedlings are incomplete. The first shared gravel field also
turns ordinary exposed banks gray: retain brown silt there, using the same
normal/ORM resources. No new image allocation. The wider riffle shows more
standing trains and long foam, but its center/right is still too calm to call
fully convincing fast water. The new log has taper, roots and twig packing;
its bark/root anatomy remains simplified. Stop look changes after these bounded
tone/classification and budget corrections. The optional town/paving work is
not attempted. Deliver all five as partial fixes and name their CG cues.

The six previews, earlier concrete controls and their receipts are retained
under `../build/river-last-round/probes/` through the clean build. Finals must
come from fresh complete exports and be judged separately before docs commit.
