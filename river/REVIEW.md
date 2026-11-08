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
