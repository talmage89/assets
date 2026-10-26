# C48 review

## Source pass — outdoor photograph and construction

Inspected all manufacturer references, including an outdoor photograph of the
actual cooler being carried through water; catalog views may be visualizations.
Camera fit uses six lid/body landmarks at 480 px crop width; 9.5 px RMS, lens
hits the 180 mm bound. Its held/tilted pose and small image constrain calibration
poorly. This is an estimated framing comparison, not a recovered physical lens
or an exact replica. Original C48 has teal/flax molding, integral recessed grips
and a different crown; the reference has tan molding, rope handles and a broad
recessed front panel. No photograph becomes a shader or model.

First source hero/controls showed an unacceptable faceted lid and too much
mottled mud on the bottom. Smoothed the actual molding normals and narrowed the
height-driven dirt/scuff zone, halving the deposit strength. The revised source
pair reads as molded polyethylene and rubber with restrained outdoor use.
Further inspection caught the front emboss appearing on the inner back wall:
restricted it to the exterior front position as well as its facing normal.
Corrected the source-only mold parting witness to follow the actual rounded
corner surface; it no longer floats off the wall. The side drain streak follows
the side-face horizontal coordinate and gravity from its measured outlet.

The first scripted open image had released latches but a closed lid: the studio
Lid channel resets the named pivot after generic parts poses. Changed the shot
to the existing lid channel, then widened the open hero to include latch tips.
No kit duplicate was added. The actual motion checks had independently caught
and fixed an eye/crown collision and moving hinge bridge without an axle bore.
Both bridges now have real clearance bores. Source/game latches, drain rotation
and lid sweep after releasing both latches pass. Gasket seats on the mouth;
no broad hard-part collision exemptions were added. Flexible latch/lug cam
contact and the captive eye/pin are the only intentional latch allowances.

Measured game cavity 47.350 US qt from actual vertex section areas (small drain
volume omitted), 29.61 mm remaining behind the grip, four ground pads, and an
unobstructed drain centerline. The C48 name is nominal. UVs: 64.19% coverage,
no overlaps/outside/degenerate triangles, p5/median/p95 433/497/509 px/m at 1024.

## Exported pass

Opened the exported outdoor pair. Overall molding, actual T-latch silhouette,
restrained lower-edge wear and original embossed brand survive the 1024 atlas.
The large lettering is softer than the source and the small subline is close to
its resolution limit. The photo is wet, sunlit tan plastic; ours is dry teal/flax
under procedural studio lights. A specular/color match would misrepresent that
original material choice. No broad projection holes, stripes or unintended
normal flips are visible. The standard three-map PBR delivery necessarily loses
sub-millimeter molding grain and some tiny edge polish. Those are the weakest
close-view details; 1024 remains appropriate for a normal patio prop.

`make` completes the 4096 GPU bake, three 1024 maps, GLB, ten imported-GLB
Cycles views, Eevee, three final JPGs, shipped photo pair and all checks.
Opened every final render and the contact sheet. The open view includes both
released latches and the gasket; the 1.8 m silhouette confirms the ordinary
portable-cooler scale. Small latch-ear/reaction-lug and pad fillets show local
normal-bake distortion in the close-ups, more visible than in the source. This
is a reported weakness of the 1024 delivery, not an intentionally distressed
molding. Broad body, lid and grip shading are clean at patio viewing distance.

Final: 3,396 triangles, one material, shared three-map 1024 set (~4 MB compressed),
GLB 1,536,272 bytes. Refined prismoidal integration of actual polygon sections
measures 47.350 US qt game / 47.372 source, not a capacity constant. All four
pads have measured body-runner support and Z=0, footprint-origin error is zero,
grip wall 29.61 mm, drain bore unobstructed, and released-lid sweep has no
measured hard-part penetration. `make check` independently repeats these and
UV/budget/normal/re-import/repository checks. No cooler-specific kit changes
or installations are needed.

## Used-object recalibration after the contract clarification

Added actual used full-cooler and owner close-up photos, credited in SOURCES.
The earlier manufacturer outdoor photograph establishes construction only; its
age is unknown. The used seller photo calibrates six corners at 11.10 px RMS
on a 635 px crop, estimated 62.3 mm lens. Original/reference body proportions
differ; this is approximate framing, not an exact-product or age measurement.

The first stronger source weather pass made too many horizontal white lines
round every corner. Opened its four source views and both photographic pairs;
rejected that regular banding. Broke corner impacts into sparse, coarse-gated
abrasion patches. Retained narrow floor-contact grime, actual drain deposits,
upward exposure fading and two broken drink-base mineral rings on the lid.
Small latch mounts/lugs/base runners now use matching two-segment source/game
bevels; the added silhouette geometry is justified by the previous distorted
normal bake. Game count is 4,036, within the 5,000 limit.

Opened the refined four source views and both new pairs. Sparse scratches now
read as damage on exposed corners rather than a repeating band. Bottom dirt
and lid rings are visible in the full hero; the broad middle faces stay less
damaged than the heavily used white reference. The default is intentionally
ordinary patio use, not the reference's worst gouges. Next is the exported
bake comparison and final studio inspection.

Opened both refined exported pairs. Corner scratches and narrow floor grime
survive the 1024 bake; the former repeated white striping is gone. The original
molded branding softens substantially, especially the small subline. Small
foot/runner fillets retain local shading imperfections; broad body and lid
remain clean. The used reference is much more gouged than the intended few
seasons of patio handling, and its white palette differs. No claim of a precise
service age or color match is made. New delivery: 4,036 triangles, one material,
1,642,980-byte GLB; UV coverage 64.21%, density 439/497/509 px/m, zero overlap.
Physical checks still pass with the new mount bevels. Final studio inspection
and explicit repeated delivery check follow.

Opened all ten final Cycles views, Eevee, final contact and both rebuilt GLB
photo pairs. The used-object cues remain visible in the full hero, and the
open view includes both released latches, gasket and real cavity. Matching
mount bevels reduce geometric differences but do not completely remove tiny
latch-ear/lug/runner shading artifacts. Do not mistake them for authored wear.
Rubber feet and small fillets are still more angular than their source view.
These limits are disclosed rather than hidden by a distant documentation camera.

Final `make` and explicit `make check` complete with exit 0. Delivery remains
4,036 triangles / one material / one three-map 1024 set (~4 MB compressed),
GLB 1,642,980 bytes. Capacity, grip wall, supported feet, drain bore and staged
released-lid sweep are independent actual-surface measurements. Fresh import,
UV/density, normals, budgets, camera agreement and repository checks all pass.
