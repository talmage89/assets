# Covey 26 — form round 2

Look-dev remains held. All current views are constant-material inspection
renders. No normal-map edge transfer, checkering, finish, wear or final atlas
is being passed off as complete. The previous checked region list was too
lenient and is superseded below. This document requests review; it does not
approve its own remaining form and measurement limitations.

## References and photographic framing

Commons was searched first. Its plain American whole-side photograph is sharp
as a whole gun but does not resolve the action at 600 pixels. The new primary
plain 12-gauge dealer set supplies native 1876–4767 px originals: both action
sides, top, underside, splinter underside and assembled open action. The
registered smaller-gauge dealer set supplies complete left/right views with
the entire gun over 800 native pixels. The primary wide 12-gauge sides clip
the muzzle and are never labeled whole-gun references. The old decorated
sideplate action and loaded sidelock are excluded from current acceptance.

See [SOURCES.md](refs/SOURCES.md) for every original, dimensions, attribution,
license and use. The tile-pyramid fetcher assembles the dealer's original
pixels without tracing or changing a contour. It downloads images only.
No photo or measured outline is consumed by the geometry generator.

The white backdrop in the whole-gun pair is balanced in linear light. The
black-background macros contain no reliable neutral; they are form-only
comparisons, with unity gains explicitly recorded. No bluing or case-color
patch is assumed gray. Each critique begins with value; these materials are
inspection constants and cannot establish photographic finish or wear.

`build/cameras.json` retains native observations, fitted cameras, residuals
and view constraints. Blender independently verifies the projections. Eleven
pairs cover right, left, both action sides, top, bottom, open action, detached
barrel flats, bottom and side of the forend, and triggers. RMS is not form
acceptance. The whole-gun fits are about 4–6 native pixels. Eight macro view directions
are locked after visual inspection; translation, focal estimate and roll
fit the framing. They retain up to 132 px native residuals because original
contours and landmarks differ. This limitation is visible in every pair.

An early open pair fitted circles while viewing the wrong side of the breech.
It was rejected despite its smaller RMS. The corrected comparison fixes a shallow view from above and forward of
the breech, with an empty 30-degree photographic presentation and its
extractor pressed home. The 42-degree canonical clips and extractor travel
are unchanged. The open reference also has a raised top extension with a rectangular cut,
which our original under-lug construction does not share. It must not be
misidentified as our barrel flats. The detached flats reference has no action or forend: only the
visible barrel region can be compared; it cannot establish an assembled fit.
The matched flats shot omits the action and forend to match the detached
photograph; the full exported gun and canonical clips are unchanged.

## Round 2 critique passes

7. **Photographs and sections.** Color/value: black backgrounds have no
   defensible neutral, so no quantitative finish match is claimed. The old
   action reference was the wrong construction class. The old breech outer
   walls overlapped, the rib was a post, and the forend was too round/full.
   Replaced the acceptance set, cut joined breech flats, filled the top valley
   with a seated tapered rib, and built a slim, flat-sided splinter with its
   channels, iron pocket and bottom latch. Added separate wood dimensions to
   the section labels so barrel width cannot be mistaken for wood width.
8. **Forging and furniture.** Color/value: checked the roll-off on dark steel
   and the head's shaded seam before detail. The first union left a slab-like
   bar/receiver transition, long rear body and an oval wood head that made
   wings beside the metal. Rebuilt the forging's changing sections, rounded
   belly, bowed rear seam, tapered bar and concentric knuckle; matched the
   wood head to its inlet section. Replaced the proud slotted hinge heads
   with the ends of a small flush cross pin. The source forging is retained.
9. **Lever, guard and actual assembly.** Color/value: underside views were
   unreadably black, so added a procedural inspection softbox below them.
   The lever was a thin plate; the first thicker sweep collided at the crown
   and stock. Lowered the central rear crown, seated the thick shank and
   swept thumbpiece, and opened the stock inlet. Refitted the guard bow and
   wrist tang, and moved the rear blade's root back 12 mm while retaining
   direction, angle and assignment. Corrected actual collisions instead of
   adding clearance exceptions. A tiny folded Boolean flap at the guard-tang
   inlet was removed by its topology, not filled into a nonmanifold patch.
10. **Stock drop and exact eye.** Color/value: judged the bead and rib against
    the neutral gray card. A bead hit alone did not prove visibility. The
    source/import checks now test every occupied skin along that ray and rays
    to three forward rib stations. Lowered the comb to the published drop
    and located the cheek station 35 mm behind its nose. The exact socket
    view shows a short rib length and the bead, with the action below. The
    vertical human cheek-to-eye citation remains missing: see measurement
    limits below. A 45 mm inspection lens makes the actual sight picture
    readable; it does not alter the socket or imply a physiological FOV.
11. **Exported shading and final evidence.** Color/value: checked deep
    cavities, unclipped bright regions and the crown's moving highlights.
    The roof's inherited Boolean face labels were unsafe after reduction;
    use actual surface location to identify the analytic roof field. A dense
    normal-transfer experiment was rejected. The bar now shares continuous
    surface strips with the body; its former overlapping table union was
    removed, and the fence shoulders were made more proud of the tubes. Keep
    the raking views and dense-source comparisons visible: smoothness and
    photographic form still require the lead's judgment, not a passing mesh
    check. The final sheet review also rejected a low-RMS forend side camera that
    had drifted below the wood. Locked that view and isolated the barrel
    assembly for the detached flats reference, where the action had occluded
    the part under review. Rebuilt all current evidence against the final
    output hash.

## Region review and remaining differences

- **Action, fences, top lever and safety.** The forging now has bowed rear
  inletting, rounded top/bottom shoulders, a tapering bar and circular knuckle
  bearing. The primary photo's fences have a more cylindrical rear roll;
  its rear head has deeper scalloped fingers around the tang. Ours remains
  fuller through the central crown, with a plainer rear seam and a more
  exposed spindle. The bar/receiver transition and crown highlights are the
  weakest form cues and must not be called fixed by future texturing.
  Inspect `beauty/action.png`, `action_left.png`, `top_controls.png`,
  `rake_right.png`, `rake_left.png`; `pairs/action-pair.jpg`,
  `action_left-pair.jpg`, `action_top-pair.jpg`, `action_bottom-pair.jpg`;
  and the standing-breech, bar and knuckle side sections.
- **Triggers and guard.** Both faces retain their forward concavity, forward
  tips and barrel assignment. The guard is a swept flat band with a rear tang
  following the wrist. The photo has a longer, more delicate front blade and
  a flatter lower bow. Ours is thicker through the lower corners and has
  more front clearance. Inspect `beauty/triggers.png`, `trigger_quarter.png`,
  `pairs/trigger-pair.jpg`, `strips/Fire.jpg` and `FireLeft.jpg`.
- **Barrels, rib, bead and muzzles.** Joined outer flats replace overlapping
  skins at the breech. The rib fills the valley, follows the barrel seats and
  tapers to the muzzle. The photo has a narrower, more visibly raised rib at
  the rear; ours has a broad shallow-concave face there. Matting is held for
  the normal map. Inspect side/top/front orthos, `beauty/muzzle.png`,
  `aimed.png`, both whole-side pairs and both barrel sections. The exact eye
  sees the bead and a short forward rib; most rear rib remains foreshortened.
- **Breech, extractor and lumps.** Our joined-tube construction has a narrower
  web and stepped central lumps. The reference has broader continuous flats
  and a different single lug profile. No detached photograph proves hinge
  engagement. Actual hook/pin, breech, rim/extractor and bite/shoe probes do.
  Inspect `beauty/breech.png` (loaded from above/behind), `open.png`,
  `lumps.png`, `pairs/open-pair.jpg`, `barrel_flats-pair.jpg`, floor/lump
  section, `opening.jpg` and the Open strips. Shell dimensions are unchanged.
- **Forend and iron.** The splinter is narrower than the barrels, with nearly
  flat tapering sides, rounded bottom and two top channels. The photo's nose
  is squarer and rises more sharply; ours is rounder and more pointed. Its
  iron wraps farther up the rear wood; ours uses two separate bearing cups
  and a simpler inset latch. The bottom photo alone cannot validate that
  latch design. Inspect `beauty/forend.png`, `pairs/forend-pair.jpg`,
  `forend_side-pair.jpg`, two dimensioned wood sections and the reload strips.
  No hand mesh is present, so hand contact is not proven; socket and shell
  paths clear the revised furniture through all clips.
- **Stock, wrist and butt.** Kept the straight hand, length and front-trigger
  pull. Widened the wrist and fitted the head to the bowed forging seam.
  Actual rib/wood rays now measure published-class comb/heel drops. The
  whole-gun reference has a different grip and butt treatment; its geometry
  cannot establish our exact straight-hand contours. Our head is plainer and
  its tang inlet seam broader. Inspect `beauty/stock.png`, both whole-side
  pairs, both butt sections, wrist and tang-inlet sections.
- **Ammunition.** Accepted dimensions and shared module are unchanged. Our
  unmarked red hull and primer are simplified original exterior forms.
  Inspect `ammunition.jpg`, `beauty/breech.png` and reload/unload strips.
  Markings, head finish and hull wear remain held.

## Measured dimensions and evidence limits

The imported GLB measures 1079.95 mm overall, 660.40 mm barrels and 369.63 mm
front-trigger pull. Stock drop, measured against a straightedge reconstructed from actual points on
the rib centerline, is 38.05 mm at the authored comb nose and 63.05 mm at the heel,
against published 38/63 mm. This centerline datum approximates a
straightedge: the concave rib edges rise about 0.22 mm above it. The cheek station is 35.00 mm behind that nose,
within the primary fitting source's 31.75–38.10 mm range.

**The human vertical fit is not sourced.** The socket is (0,−123,67) mm,
49.31 mm above the actual comb at its station. That is a measured model offset
and an authored vertical fit, not a measured human cheek weld. The original
45 mm justification is withdrawn. A reproducible mounted-person measurement
with scale is still needed to satisfy that part of the brief.

Wood-only wrist at Y = −15 mm is 32.23 × 37.74 mm. The forend's overall wood
bounds are 34.40 × 24.19 × 173.01 mm; its sections at Y = 211 / 320 mm are
34.39 × 22.53 / 25.90 × 18.68 mm. These are actual triangle intersections.
The photos constrain proportions, but their absolute wrist/forend dimensions
were not independently calibrated in millimeters. Do not label these numbers
as published specifications or precise photo measurements. This reference
measurement requirement remains weaker than requested.

## Verification scope

`make check` runs separate source and fresh-import topology/contact sweeps
through all 19 clips at half-frame intervals, with a 0.20 mm visual tolerance
and no contact allow-list. Actual-surface probes cover hinge, knuckle, breech,
chambers, rim support, locking bites, lever seat, safety and sight visibility.
A separate global-X surface-extrema check proves that the two joined tube
skins do not overlap; their shared bone would exclude them from the normal
cross-bone sweep. A second independent build checks deterministic geometry, normals, bones,
sockets and animation. Source/import affine samples and event surfaces prove
serialization separately from assembly correctness. Timed WebPs are decoded
and summed at their real durations. `audit.json` checks current source hashes.

Current proof: `make -C guns/sxs` and `make -C guns/sxs check` pass.
The staged gun is 34,638 triangles, 54 rigid meshes, nine inspection materials,
zero images and 1,630,020 GLB bytes. Source/import sweeps cover 1,715 / 1,728
samples across 19 clips, with 246 measured contact records each and 0.17201 mm
maximum penetration. Rebuild comparison passes all 104 entries at 1 nm position
rounding and five decimal normal components. The presentation audit confirms
301 current render records and all 19 real-duration WebPs. Hero luma p1/p50/p99
is 1.07 / 46.21 / 204.27, with zero all-channel clipping; this is a tonal-range
check on inspection materials, not finish acceptance.

No kit or shared/common file changed in this round. There are no final UVs,
textures or bake-loss claims. No hand mesh or ergonomic fit test is supplied.

## Prior checkpoint history, not current acceptance

The following log records the first session's investigations. The owner's
round-2 rejection supersedes its favorable judgments and reference choices.

## Critique log

1. **Blockout, both sides and sections.** Color/value: constant dark steel and
   brown wood make no finish claim; pale Workbench illumination is unsuitable
   for color acceptance. The first allocation was too expensive, the tang
   floated over the wrist, and the safety lacked a convincing seat. Rebuilt
   tang inlets and fitted the controls; reduced hidden bevel and cage costs.
   Preserved the stock's changing comb/cheeks and the splinter's barrel
   channels instead of flattening either into an extruded profile.
2. **Raking form and trigger photograph.** Color/value: retained dark material
   values and inspected the light roll-off, without matching the colored
   floor's hue. The action looked like a rounded cap on a separate plank.
   Rebuilt a changing-section body with continuous fences and a unioned water
   table. Broad guard band, blade thickness and forward-concave trigger faces
   were checked in side and underside views. Narrow wires and backwards
   hooks were rejected. Hero framing was enlarged to retain the whole butt.
3. **Open assembly and actual contacts.** Color/value: dark cavities must stay
   legible under the breech. The extractor bridge/stem, rim seats, lock shoes
   and lever spindle exposed real interpenetrations during motion. Cut their
   actual passages and reset the movement sequence; no clearance allow-list
   hides them. The lower tang/safety support and forend iron were fitted to
   their actual surfaces. Shell skins were made closed without overlapping
   disconnected head/hull components.
4. **Cycles exported close-ups.** Color/value: no all-channel white clipping
   is accepted in the hero; black metal must retain deep cavities and rolling
   highlights. The shell heads had a false concave reflection after export;
   restored planar head normals. The exact aimed view hid too much rib;
   raised the eye and remeasured the comb offset. The roof showed triangular
   highlight boundaries, and some cross-pin heads were buried or reversed.
   Rebuilt longitudinal curvature and normal fields, seated both pin pairs,
   and added a recessed steel floor/rails under the safety.
5. **Sharp breech photo and section recheck.** Color/value: white-balanced the
   new sheet-backed macro; no sampled finish is accepted yet. Replaced the
   undersized open-action target. A section exposed a floating bottom rib;
   rebuilt it to join both lower barrel skins. Coincident extractor-relief
   cuts left hatch-like sliver faces; moved the cutter into empty bore space.
   The remaining roof sawtooth came from a hard minimum in the fence/land
   surface, not lighting. A continuous radius removed it under the same
   raking camera (`renders/crown-review/action.png`). Final reduction also
   exposed a microscopic folded corner at the lever bore. Welding within
   0.0001 mm after reduction repairs it; both topology checks must pass.
6. **Whole photographic framing.** Color/value: retained the declared neutral
   patches; finishes remain held. Chamber-only fitting concealed an incorrect
   whole-assembly comparison. Inspecting the full sharp original and the
   neighboring photographs showed its barrels were detached. Reclassified
   that pair as barrel detail, rather than forcing a false hinge fit. Corrected
   the left/right shell identification and removed an arbitrary camera-height
   prior in the assembled loaded photograph; its fit improved from 120.3 to
   26.7 native pixels. Both action and shells now share the photographed
   framing. Fixed a presentation-only extractor press that an active animation
   had overwritten. The pose is frozen before applying it, then asserted.
   Restored smooth sculpt shading on the dense controls in their comparison
   scene; inherited flat cage faces had produced bands absent from the game
   normals. Enlarged the stock/lump framing and gave trigger/safety clips
   their own close cameras so their real travel can be judged.
