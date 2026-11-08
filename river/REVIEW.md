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
was copied. The Type III section is independently derived from FDOT 20130.

Viewed the four period photographs in `build/reference-sheet.jpg` at size and
the actual FDOT section. The type differs from the wider steel Huron reference;
the bank photo hides a simpler bridge's ends. The comparisons must retain those
differences. Camera height priors reject an initial mathematically plausible
but below-ground fit. Final fits retain their residuals, not just a nominal lens.

Photo balance uses assumed neutrals: Raisin parapet concrete, Morrison trail
wall and Huron concrete cap. The original images are unchanged. Exact patch
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
