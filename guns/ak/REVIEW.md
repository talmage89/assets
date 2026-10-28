# Rill 39 — checkpoint review

Form gate only; no look-dev, baked finish, wear or final delivery acceptance.
The current images use an exported GLB with constant inspection materials.
Source photographic views are separately labeled. These checks do not make
the internal proxies functional firearm engineering.

## Critique passes

1. **Color/value first:** neutral Workbench gray isolates form; it does not
   match the museum wood or painted steel. Opened all ten first-pass views.
   Rejected misplaced box-built pieces caused by a missing scene update before
   applying object placement. The aimed view lacked its post and rear notch.
   Fixed placement at the generator, rebuilt and re-exported.
2. **Color/value first:** retained neutral gray. Opened the second ten-view
   sheet and native trigger/aimed images. Rejected severe longitudinal shading
   bands on both handguards, open cover rear, excessive transverse cover ribs,
   and a long, weakly curved magazine. The trigger faces forward, but its upper
   blade overlaps the grip. Fixed compound grip clearance, increased magazine
   curvature and shortened its visible depth against the museum photograph.
3. **Color/value first:** five GPU Cycles views expose the overly bright quick
   varnish and card reflections; these are not proposed material values. Opened
   right, wood, Eye, cover/rear and open action at native size. Rejected the
   handguard stripes again: clearing a transferred normal field alone did not
   solve them. Assigned analytic oval normals to the actual rounded sections.
   Reduced the cover's corrugation, added its rear closure and retained a true
   optical socket. The first clearance sweep exposed hidden proxy overlaps,
   a paddle/housing conflict and an obstructed rock path. Fixed geometry and
   path before accepting any sweep.
4. **Color/value first:** opened the source and exported photographic pairs
   against the museum's neutral gray backdrop. Black inspection steel still
   becomes silver under broad cards, and constant wood is pale peach rather
   than the reference's varied amber/reddish varnish. No material acceptance.
   The new sharp trigger pair exposed the misplaced blade and weak forward
   toe. Moved it clear of the grip and reshaped its concave muzzle-facing face
   and rounded forward tip. Added guard mounting flanges against the receiver.
   The blade remains broader than the sharp photograph. This is recorded as a
   form difference, not something future textures will correct.
5. **Color/value first:** retained the same inspection constants. Reviewed the
   Cycles macro set, section cuts, open action and magazine strips. The earlier
   handguard stripes are gone; compound sections agree with the retained dense
   sources. The carrier/hammer proxies required more clearance. The visual
   hammer now clears the moving carrier. Ejected-case visibility had lost
   rotation/translation through zero-scale TRS export: a motion parent with a
   visibility child fixed the source/import mismatch. Sweeps and independent
   imported surface comparisons now pass. These are visual-animation fixes,
   not working lock or sear validation.
6. **Color/value first:** all 20 final beauty views, five source pairs, five
   exported pairs, ten extra stills and all 290 strip samples were opened,
   including the numbered inspection pages. The reference neutral choices
   are explicit; sky/colored garment estimates were rejected and excluded
   from color measurements. Rejected clipped stock in both raking views and
   clipped standalone magazine presentation, then widened the cameras. Final
   form differences are listed below. The output is ready for a form review;
   this log does not grant overall form or final-asset acceptance.

## Form acceptance list

All paths below are relative to `renders/checkpoint/`. Checked items record
the specific visible criterion examined; unchecked items remain unresolved.
Every comparison was opened in both source and exported-GLB form. Material
matching is outside this gate, and none of these entries means lead approval.

### Receiver, rivets and top cover

Evidence: [receiver pair](renders/checkpoint/pairs/receiver_photo-pair.jpg),
[rear cover](renders/checkpoint/beauty/cover_rear.png),
[right raking](renders/checkpoint/beauty/raking_right.png),
[left raking](renders/checkpoint/beauty/raking_left.png),
[sections](renders/checkpoint/sections.jpg).

Photo differences: the photo's cover has finer shoulder beads and a more
subtle crown transition; ours shows slight pinching near its rear crown and
more regular ribs. Our dimples are softer, and the receiver's broad blank
panel is cleaner and less constructed-looking than the photographed surface.
Rivet head sizes/press layout are original; their unmarked finish is temporary.

- [x] The section is open folded sheet with two surfaces and bottom radii,
  including a magazine-well opening; it is not a solid receiver block.
- [x] Front/rear head groups, cover closure, retaining button and ejection
  opening read in the two oblique views.
- [ ] Rear-crown pinching and soft dimple transitions are not fully resolved.

### Selector and charging handle

Evidence: [controls](renders/checkpoint/beauty/controls.png),
[open action](renders/checkpoint/beauty/open.png),
[three positions](renders/checkpoint/selector.jpg).

Photo differences: our lever is a broad smooth plate with a folded thumb land;
the photo has more developed edge folds, hub nesting and stamped transitions.
Our handle has finite thickness and a seated root, but its cheek/neck is
simpler than the photo's rounded forged transition. Finish does not explain
those form differences.

- [x] Three distinct poses, an unobstructed ejection opening and the handle
  attached to the carrier are visible; the handle reciprocates in the strips.
- [ ] Selector edge construction and hub contour are simplified.
- [ ] Safe-position mechanical handle blocking/detent function is not certified.

### Trigger, guard and magazine release

Evidence: [sharp trigger pair](renders/checkpoint/pairs/trigger_sharp-pair.jpg),
[museum trigger pair](renders/checkpoint/pairs/trigger_photo-pair.jpg),
[side](renders/checkpoint/beauty/trigger_side.png),
[oblique](renders/checkpoint/beauty/trigger.png).

Photo differences: the sharp photograph's blade is narrower with a straighter
upper shank and a longer shallow forward sweep. Ours has a broader middle and
rounder toe. The original guard has rounded corners and seated flanges; its
rear turn is more regular than the photo. The release paddle/housing is
visibly simpler, especially the box-like catch cover.

- [x] Concave face opens toward the muzzle; the rounded toe curls forward.
- [x] Side and oblique views show a blade, finite guard ribbon, clearance from
  grip and guard, and actual guard flange contact with the receiver.
- [ ] Exact blade proportion and stamped release construction need refinement.
- [ ] The sharp pair's 11.66 px residual/lens bound and the museum pair's
  out-of-crop anchors prevent claiming exact photo-overlay acceptance.

### Barrel, gas block, tube and muzzle brake

Evidence: [gas/muzzle](renders/checkpoint/beauty/gas_muzzle.png),
[right pair](renders/checkpoint/pairs/right_photo-pair.jpg),
[left pair](renders/checkpoint/pairs/left_photo-pair.jpg).

Photo differences: the photographed gas-block neck has more rounded forged
shoulders and less planar transition into its bands. Our tube vent details
and retainer edges are simplified. The brake has its slanted sleeve outline,
but its fine lip/retention detail is absent. The cleaning rod is supported and
has measured visual thickness; no operational gas path is represented.

- [x] The two side views show the barrel/tube relationship, inclined neck,
  supported rod, bayonet-lug silhouette and slanted brake.
- [ ] Forged shoulder transitions and fine retainer/brake detail remain weaker.

### Front and rear sights

Evidence: [rear](renders/checkpoint/beauty/rear_sight.png),
[front](renders/checkpoint/beauty/front_sight.png),
[exact Eye](renders/checkpoint/beauty/aimed.png),
[cheek-weld estimate](renders/checkpoint/cheek-weld.jpg).

Photo differences: the museum rifle has protective ears rather than our
requested original closed hood. Our rear block/slider is cleaner and has less
compound rounding than the photo. Graduations exist; final fictional numerals
are absent. The leaf/slider is static at this checkpoint.

- [x] The aimed render shows the rear notch and centered post level with its
  shoulders, inside the hood, with cover and handguard below.
- [x] Eye is behind the notch on the actual optical line. Its 295.00 mm distance
  is within the coarse 268 ±35 mm cheek-weld estimate, not an ergonomic proof.
- [ ] Sight adjustment and slider motion are not rigged.

### Handguards, pistol grip and stock

Evidence: [handguards](renders/checkpoint/beauty/wood.png),
[grip/stock](renders/checkpoint/beauty/grip_stock.png),
[sections](renders/checkpoint/sections.jpg), both raking views above.

Photo differences: the photograph's lower handguard has a more obvious palm
swell, stepped end relief and varied scallop; ours has smoother, more uniform
lengthwise transitions. Our grip has less developed rear palm contour. Stock
cheek/wrist transitions are original and smoother than the museum example.
No grain, molded surface, dings or varnish wear exists. The buttplate trap is
present but static.

- [x] Two stock stations and two stations in each handguard change section;
  the grip is compound, not a beveled side-profile extrusion.
- [x] The U handguard channels and finite walls are visible in actual cuts.
- [ ] Palm-swell/end-relief fidelity and grip contour remain weaker than photo.
- [ ] Buttplate trap motion, normal bake and finish remain pending.

### Magazine

Evidence: [installed](renders/checkpoint/beauty/magazine.png),
[loaded lips](renders/checkpoint/loaded/mag_lips.png),
[empty lips](renders/checkpoint/empty/mag_lips.png),
[rock-in](renders/checkpoint/rock-in.jpg), sections above.

Photo differences: our press layout and floorplate outline are original. Ribs
are deeper/rounder than the museum's finer pressing; small triangulation glints
remain near their terminations. The top catches/lips are simplified exterior
proxies. The display wire crossing the photographed magazine is excluded.

- [x] Curvature, hollow sheet, ribs, folded spines and tilted floor read from
  both sides; the loaded/empty exports show distinct round/follower occupancy.
- [x] The strip shows rotation around the front pivot before the rear seats.
- [ ] The front hook/slot is not a certified retention mechanism.
- [ ] Rib termination shading remains weaker than the reference pressing.

### Ammunition

Evidence: [cartridge](renders/checkpoint/cartridge/cartridge.png),
[case mouth](renders/checkpoint/case/case_mouth.png), loaded lips above.

Photo differences: constant olive lacquer and jacket metal are much more
uniform than the photograph. The exterior silhouette is approximate; the base
lacks its fictional headstamp and fine primer/extractor relief. The fired mouth
is open, without internal cartridge construction or a physical firing model.

- [x] Separate inert cartridge/case exports and three visibly staggered display
  rounds are present. Both upper cases lie beneath the overhanging lips.
- [ ] Fictional headstamp, base relief and final finish are not supplied yet.

## Proof and delivery state

`make -C guns/ak` passed from the scripted model through checks and media.
`make -C guns/ak check` passed after the final check enhancements. Camera-only
corrections were regenerated with `make -C guns/ak render extra` and sheets
rebuilt with `python3 guns/ak/src/review.py`.

- Gun: 39,524 triangles, eight constant materials, zero textures,
  1,943,468 bytes, 17 rigid bones, eight sockets, 20 clips, interface 1.6.0.
- Loaded/empty magazines: 6,400/4,240 triangles, 143,360/93,932 bytes.
  Cartridge/case: 960/704 triangles, 23,452/18,752 bytes.
- Actual overall envelope: 881.38 ×56.61 ×257.79 mm. Barrel exterior span:
  415.00 mm. Receiver sheet ray gauge: 1.00000017 mm. About 3.1 kg remains a
  class reference mass, not a measured property of the mesh.
- Eleven visual-contact/optical assertions pass in source and fresh import.
  Surface intersections prove visible seating, not functional engagement.
- All 20 clips swept at half-frame steps: 1,556 source and 1,568 import samples;
  zero violations under the declared rules. Ordinary tolerance is 0.2 mm.
  Five pin/handle/inert-catch joints have finite bounds of 1.0–2.1 mm; maximum
  measured overlap is 1.97104 mm at the catch joint during reload. These are
  explicit visual joint allowances, not a global 2.1 mm clearance tolerance.
- 1,556 source/import affine samples: maximum position difference
  0.0000913 mm; maximum linear-matrix difference 3.28e-7. Maximum evaluated
  posed-surface difference 0.0000894 mm. Raw normals are finite and unit length;
  minimum triangle/corner normal dot is 0.10214. No nonmanifold source parts.
- All four detached files fresh-imported. Loaded/empty full-rotated socket
  spawn error is below 0.000045 mm. A second factory-startup model build gives
  five byte-identical GLBs (`build/repeat.json`).
- 20 Cycles beauties, ten source/export photo stills, ten extra stills and
  290 Workbench strip samples: 330 render records verified against source
  hashes. All were opened, via native critical views and complete inspection
  sheets. Real-duration WebPs accompany every clip, including 60 Hz short
  cycles. Ten actual triangle section cuts compare game/dense-source outlines.
- `python3 -m compileall`, `git diff --check` and `python3 kit/repo_check.py`
  pass. No kit changes, so no kit test suite was required.

The final one-set 2048 UV/bake/material delivery, wear comparison, final studio
set and committed docs JPGs have not begun. The inspection GLBs are not the
final canonical atlas delivery and do not satisfy final material/draw-call
acceptance. No other gun or existing common module changed. New common modules
are `ammo762_visual.py` and `interface_v1_6.py`; family index/interface links are
additive. No downloaded asset/code was used, and nothing was pushed.

No new tool is needed. A useful kit documentation addition would be a minimal
motion-parent/STEP-visibility-child example for rigid glTF objects, because
animating compound TRS directly through zero scale obscured this round trip.
The next decision is the lead's form review of the unresolved entries above.

## Scope of contact evidence

Visual lip support, rear catch seating, handle-to-carrier union, stock seating
and an actual Eye ray are independent surface checks. Clip clearance measures
all cross-owner solids with finite visual-pin/handle joint bounds, rather than
ignoring contact prefixes. Source/import affine agreement is reported separately.

The brief's working bolt-lock, hammer/sear engagement and selector-blocking
engineering are deliberately not supplied. Those mechanisms remain inert
visual proxies; neither a serialization match nor a clear sweep can certify
their function. The front hook pivot/path is an animation convention; it is
not a manufactured retention assembly. This is a material limitation of the
checkpoint relative to those requested functional checks, not a passing claim.
