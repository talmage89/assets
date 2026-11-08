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
