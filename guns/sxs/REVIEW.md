# Covey 26 — form and motion gate

This gate holds look-dev. The materials are inspection constants, not an
accepted blued finish, walnut finish or field wear. The exported GLB supplies
the inspection views and motion evidence. Dense furniture/thumb-control
sources get the same photo cameras independently. No photographic pixels enter
the asset. Final UVs, checkering, markings, baking and delivery are not claimed.

## Reference and framing discipline

The [register](refs/SOURCES.md) identifies every original, author and license.
The native left-side photograph is 4608 pixels wide. The right-side photograph
is 3840 pixels wide and shows an open gun with a different pistol grip, sling
and stock boot. The sharp trigger photograph and detached-barrel
photograph are 2136 × 4624 pixels; the measured regions exceed 600 native
pixels. The assembled, loaded-breech photograph is 3008 × 2000 pixels. The
small empty-action image and an exploratory over-under are not
acceptance references. Engraving, manufacturer contours and marks are not
copied.

Color/value comes first in each pass. The sheet in the sharp construction
photos supplies a white neutral, balanced in linear light before comparison;
`build/references/whitebalance.json` records patches and gains. The loaded
outdoor image uses a pale shirt stripe, with mixed lighting as a limitation.
The left photo's wooden floor has no reliable neutral, so it supports form
only. No quantitative color or wear acceptance is taken from it.

Cameras are solved from manually observed landmarks, then checked through
Blender's projection independently. `build/cameras.json` retains observations,
native-pixel residuals, focal length and camera. Approximate native RMS errors:
left 29.8 px, right 127.6 px, action 19.2 px, trigger 49.9 px, detached barrel
detail 10.5 px, assembled loaded breech 26.7 px. These are different original
guns. In particular, the right
stock is downweighted because its grip/boot differs. The loaded sidelock
comparison uses a different sidelock body: it checks assembled opening,
raised shells and viewing angle, not the shape of our boxlock side flats.

The sharp photo shows detached barrels, with its extractor pressed home.
It cannot establish an assembled opening angle. Its detail crop deliberately
compares the chambers and extractor only. Its matched
presentation uses the same physical home position as Close, with an open
empty action. `shots.json` identifies this override. It does not relabel the
canonical raised-extractor IdleOpenEmpty pose. All geometry remains visible.

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

## Form acceptance against images

All seven regions were opened at native render resolution and compared with
the listed photographs/sections. The checks mark completion of this form
review; the remaining differences are retained for the lead at this gate.

The following list is about the visible form. Geometry/state measurements
corroborate it; they do not replace the photographs. Each difference is stated
before the checkpoint disposition. Paths are generated locally by `make`.

- [x] **Action, fences, lever and safety.** Reference differences: the original
  action has plainer, longer side flats, broader central roof land and a more
  exposed safety guide opening. It omits the reference's engraving. Inspect
  `beauty/action.png`, `action_left.png`, `top_controls.png`, both raking views,
  `pairs/action-pair.jpg` and the standing-breech/tang-inlet sections. Require
  rounded fences flowing into the body, visible seated pin heads, a supported
  lever/spindle and safety in both detents. The smooth roof highlight is a
  required acceptance condition, not hidden by a rougher shader.
- [x] **Triggers and guard.** Reference differences: our oval guard is broader
  in the belly and its tail transition is plainer; the two blades have
  original lateral staggering. Inspect `beauty/triggers.png`,
  `trigger_quarter.png` and `pairs/trigger-pair.jpg`. Require flat blade
  thickness, front/right and rear/left order, concave faces forward, forward
  tips, a band-shaped guard and visible clearance throughout both firing clips.
- [x] **Barrels, rib, bead and muzzles.** Reference differences: original muzzle
  wall/rib proportions and a plain unbeaded action decoration; rib matting is
  deferred normal detail. Inspect side/top/front orthos, `beauty/muzzle.png`,
  `aimed.png`, `pairs/left-pair.jpg` and both barrel sections. Require two open
  tubes with walls, joined upper/lower ribs, a seated bead and a continuous
  visible rib from the exact Eye camera against gray.
- [x] **Breech, extractor and lumps.** Reference differences: our extractor has
  two rounded rim pads on one bridge, a narrower central breech web and
  original lump outlines. The photograph has a fuller continuous breech-face
  surround; this remains a weaker construction cue in our original assembly.
  The photo's extractor is flush; normal open clips raise ours.
  Inspect `beauty/open.png`, `breech.png`, `lumps.png`, the assembled
  `pairs/open_loaded-pair.jpg`, sharp detached-barrel `pairs/open-pair.jpg`,
  floor/lump section and `opening.jpg`. Require real
  chamber recesses, visible empty space through the action floor, supported
  shells, concentric hinge contact and no floating metal strip.
- [x] **Forend and iron.** Reference differences: our splinter has a longer
  rounded nose and a simpler inset latch; checkering is held. Inspect
  `beauty/forend.png`, both rake views, right-side pair and two forend sections.
  Require compound palm/edge curvature, two barrel channels, central rib
  relief, an actual iron pocket, and cups on the knuckle during opening.
- [x] **Stock, wrist and butt.** Reference differences: our comb rises farther
  into the straight hand, heel/toe contours differ and the measured pull is
  4.63 mm longer than the published baseline. Inspect `beauty/stock.png`, both
  sides, `pairs/left-pair.jpg`, both butt sections and the wrist section.
  Require cheeks narrowing toward a rounded comb, changing wrist section,
  fitted tang seats and a pitched separate butt plate. Grain, checkering and
  toe damage remain look-dev work.
- [x] **Ammunition.** Reference differences: the shell is our family's fictional
  red hull with an unmarked head; primer and six-fold mouth are simplified
  exterior forms. Inspect `ammunition.jpg`, `beauty/breech.png` and the reload
  strips. Require the pump-compatible dimensions, a flat live head, an open
  fired mouth, separate portable GLBs and seated handoffs without growing
  geometry. Markings and finish are held.

## Motion and evidence limits

All 19 clips get half-frame clearance sweeps in source and fresh GLB imports,
including the floor/lumps, hand-held hull paths and incoming shells. There
are no allowed-contact exceptions. Actual surface rays measure the hook/pin,
iron/knuckle, closed breech, shell/chamber, rim/extractor, locking bites, comb,
lever seat and safety support. The 0.20 mm penetration tolerance is a visual
sampling threshold, not a mechanical fit specification. The measured contact
gaps are not manufacturing clearances.

Independent state checks use per-chamber loaded/fired/empty and per-hammer
cocked/rest. Complete affine/socket samples and event surface poses compare
the source with the GLB. These prove serialization separately from the intended
states and actual-surface checks. A second independent build compares geometry,
normals, rig, socket and animation entries. Timed WebP durations are decoded
and summed, rather than assumed from frame counts.

No hand mesh is supplied: the complete hand targets and visible shell/hull
paths show the intended reload. Field wear, whole-part finish histograms,
bake loss, atlas budget and final delivery validation remain after this gate.

## Gate results

`make -C guns/sxs`, `make -C guns/sxs check`, and the corrected
`make -C guns/sxs render review` completed successfully. The source and import
each pass topology, intended states, 242 actual-surface contact records and
all 19 half-frame clip sweeps, with no allowed-contact exceptions. Maximum
sampled penetration is 0.114 mm against 0.20 mm tolerance. The GLB matches
1,715 full affine/socket samples; maximum position error is 0.000191 mm.
The independent rebuild matches 107 geometry/rig/socket/clip entries.

There are 33,736 triangles including every hidden ammunition alternative,
57 named meshes, 17 bones, 19 clips and 14 sockets. The gun GLB is 1,602,672
bytes; separate shell/hull outputs are 752/480 triangles and 26,476/18,160
bytes. Nine constant inspection materials and zero texture images are
intentional at this gate. No final atlas, UV/bake or textured delivery is
accepted. The hero's 1st/50th/99th luma percentiles are 1.1/44.6/205.6 with
zero all-channel clipping; these establish inspection tonal range only.

The form package contains 19 Cycles stills, 11 actual triangle-plane sections,
six exported photo pairs, the same six dense-source pairs, 19 timed clip
strips/WebPs, a wide opening strip and both portable ammunition views.
`renders/checkpoint/audit.json` checks 291 render records against current
source hashes, photo cameras and decoded clip duration.

The weakest remaining form cues are the broad plain action flats, the exposed
safety inlet and the narrower breech web compared with the photographs. The
right-side reference also has a different stock and a less exact overall
fit. These are disclosed differences, not finish problems to cover with wear.
Mass is still an unmeasured 3.2 kg target. No hand mesh ships; reload targets
require consumer hand IK. Look-dev remains held for the requested checkpoint.
