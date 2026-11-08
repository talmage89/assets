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
