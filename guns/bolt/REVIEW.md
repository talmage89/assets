# Vesper B24 — form round two

Quick materials only. The lead accepted the dimensions, rig, nine clips, 1.2.0
supplement, contacts/sweep and scope/Eye layout from round one. **Form acceptance
remains the lead's decision.** No paint, wear, final marking atlas, baked sculpt
normal, UV acceptance or finished optical response is claimed here.

The before geometry is our own checkpoint at `f622cc9`. The `baseline` target can
rebuild its authored scripts from Git into ignored scratch, then render it with
our current cameras and quick lights. This avoids comparing a better-lit after
image against an unfair before. No external model or other worktree is loaded.

Before/after sheet (`renders/checkpoint/changes.jpg`) ·
Current contact sheet (`renders/checkpoint/contact-sheet.jpg`) ·
Dimension rulers (`renders/checkpoint/dimensions.jpg`) ·
Nine tang-to-butt sections (`renders/checkpoint/sections/wrist-sections.jpg`) ·
Channel and barrel sections (`renders/checkpoint/sections/forend-sections.jpg`)

## References that can judge the form

The cluttered trade-show left and blurred painted open-action photos are
superseded. The clean true-left PEO Soldier photograph, clean Air Force right
profile and sharp original action photography are recorded with direct URLs,
authors, licenses, measurements and limitations in [SOURCES](refs/SOURCES.md).
The old right photograph is retained as requested. No reference was mirrored,
projected, traced or used as geometry or texture.

| Pair | Source | Native-pixel landmark RMS | Limitation |
| --- | --- | ---: | --- |
| Clean right (`renders/checkpoint/pairs/profile_right-pair.jpg`) | U.S. Air Force M24 profile, public domain | 10.7 | Lens estimated; our shorter forend and fixed butt are original |
| Clean left (`renders/checkpoint/pairs/left_photo-pair.jpg`) | PEO Soldier M24 profile, public domain | 26.1 | 105 mm equivalent from EXIF is fixed; original padding is uncertain |
| Open action and bolt (`renders/checkpoint/pairs/open_photo-pair.jpg`) | Sharp Gunsumer Reports original close-up | 24.5 | Reference is unscoped; our scope and base remain visible |
| Large wrist and grip (`renders/checkpoint/pairs/wrist_photo-pair.jpg`) | Sharp Gunsumer Reports original close-up | 19.8 | Fit uses action features; original stock differences remain visible |
| Old right (`renders/checkpoint/pairs/right_photo-pair.jpg`) | Original SPS right photograph | 30.4 | The reference has a shorter barrel and swept grip |

Errors are in the source crop's native pixels, not the resized pair's pixels.
These are camera-fit diagnostics, not form scores. The old left/open errors were
68/56 px. The new views reveal construction that those images could not judge.
The same cameras also produce dense-source pairs (`renders/checkpoint/sculpt-pairs/`).

## Critique and corrections

Round one is rejected as a form result. Its dimensions and serialization did not
excuse the ball-shaped rear, invisible port, lumpy inlet, thin guard, oversized
magazine or weak bipod. Its self-review was too lenient in those regions.

1. **First round-two assembly — `renders/round2-pass1/`.** Value: temporary tan
   still looks pale beside the black references; no finish approval. Rebuilt the
   rear into a collar, swept stem, cylindrical shroud and lower tail. The stock's
   flowing wrist and tapered butt improve its volume, and the box is shorter.
   Rejected 56,443 triangles and excessive wall geometry. Moved control ribs into
   the dense bake source, reduced flat stock surfaces and simplified machining
   subdivisions. The first topology reduction damaged the receiver's bore;
   rejected it rather than weakening the manifold or clearance checks.
2. **Rear/action close-ups — `renders/round2-pass2/`.** Value: the receiver still
   hides its internals in dark-on-dark light. A sharp reference exposes an overly
   long rear bridge. Shortened the receiver's rear and moved its collar/shroud
   geometry along the existing bolt axis; muzzle, barrel length, trigger, bone
   frames and schedules stay fixed. The first inlet still has a thin raised
   shoulder, and a magazine wall masks its round. Replaced the rectangular handle
   cut with a round open notch, restricted the large bedding cavity to the actual
   receiver, and trimmed the feed walls to their formed lips.
3. **Raking and underside views — `renders/round2-pass3/`.** Value: the soft port
   fill makes steel shapes legible without approving their polish as a field
   finish. The first underside camera sees the studio floor, and the leg detail
   cuts off a foot. Corrected those views. The mag is still too low in the port.
   Raised its feed geometry, then reduced that rise to 7 mm to clear the lifted
   lugs throughout cycling. The catch and accepted bone/socket frames stay put.
4. **Section-driven correction — `renders/round2-pass4/` and section sheets.**
   Value: plain tan makes the continuous highlight easy to inspect, but still
   lacks composite/web-paint response. The channel has enough land width, yet
   its inner corner is sharp: tiny Boolean edges clamp the nominal bevel. Rebuilt
   the upper section with a smooth transition into the cylindrical channel,
   before voxel sculpting. The actual cuts now show rounded lands. Lowered the
   wrist's top naturally and restored volume beneath it so the lower cocking tail
   clears without carving a long lumpy trough.
5. **Assembly and final close-ups — `renders/round2-pass5/` and current views.**
   Value: broad steel highlights and cavity shadow separate the parts; polished
   constants remain unapproved. Rebuilt cap ears with a real split, four screws
   per ring, clamp washers and hex nuts. Found that the rear foot lacked base
   support; extended the one-piece tail under the accepted ring location, gave
   its underside the receiver's curvature and placed base screws over bridges.
   Refined the forged stem sweep and shifted the safety's thumb geometry slightly
   outboard to clear each other and the rail at intermediate times. No motion
   tolerance or hold key was relaxed. An export-only normal failure identified a
   microscopic rear-bore Boolean sliver; welded it before generating normals.
6. **Last tang inspection — `renders/round2-pass6/` and current rear view.**
   Value: checked once more without finish variation. The close rear camera
   exposed a pointed saddle where the tang pocket met the round handle relief.
   Applied a localized relaxed sculpt blend across that junction, retaining the
   narrow tang reveal and the surrounding wrist volume. Regenerated the complete
   evidence and both source sweeps after this correction.
7. **Optical-path correction — `renders/round2-pass7/`.** Value: the black
   reticle still disappeared into a dark field. The turret section exposed a
   solid saddle across the tube. A structural ray confirmed the blockage in the
   round-one source. Opened its internal bore without changing the exterior or
   accepted optical layout. Nine parallel rays now check the central passage in
   game source, dense source and the joined fresh-import GLB. The aimed image
   shows a crisp black center through the open passage; its unmagnified tunnel
   and dark peripheral field still require the documented objective-camera
   magnification integration and final coating response.
8. **Fastener and sling-seat review.** Value: no finish change. The taller butt
   had buried its rear sling eye, and the rear action screw lay beyond the old
   plate end. Lowered the eye into an exposed seat, extended the matching plate
   and inlet, turned the underside/rear-facing socket recesses outward, and gave
   pad/base heads real recesses. Solid rail lands preserve the base screw seats.
   A surface ray now measures the rear stud's exposed depth. The final game surface measures 6.59 mm of exposed rear-stud depth. Overall
   dimensions, bone frames and schedules remain fixed. These corrections add
   540 triangles.
9. **Strip framing.** Value: unchanged gray inspection shading. The lowest
   chambered-reload handoff clipped the magazine at the bottom of the old strip
   camera. Widened its lens from 55 to 45 mm; the magazine's evaluated bounds
   retain at least 13.44 pixels of vertical margin in both reload strips. Viewed
   the corrected handoff and all nine strips. Timing and poses are unchanged.

## Regional inspection and photographic differences

Checks below mean the stated condition was inspected in these images and their
sections. They do not mean the owner has approved the form or final finish.

| Region | Before and after | Current condition and how the photograph still differs |
| --- | --- | --- |
| Bolt rear | Comparison (`renders/checkpoint/changes/bolt_rear.jpg`), cocked/fired against sharp photos (`renders/checkpoint/rear-states.jpg`) | Forged collar, swept stem, tapered cylindrical shroud and separate lower tail replace the ball/block. Both tail and striker move visibly. Our knob is larger and oval; the reference tail is darker and its forging has different flats. |
| Ejection port | Comparison (`renders/checkpoint/changes/port.jpg`), sharp open pair (`renders/checkpoint/pairs/open_photo-pair.jpg`) | A measured 72 mm opening with radiused ends shows the brass/copper top round and longitudinal raceway. Local fill exposes the surfaces. Our visual feed/raceway geometry is simpler; it does not claim a functioning internal mechanism. |
| Wrist, inlet and comb | Wrist comparison (`renders/checkpoint/changes/wrist.jpg`), butt comparison (`renders/checkpoint/changes/butt.jpg`), nine sections (`renders/checkpoint/sections/wrist-sections.jpg`), large pair (`renders/checkpoint/pairs/wrist_photo-pair.jpg`) | Continuous changing oval volumes replace the troughs, shelf, blade and diagonal grip crease. The handle notch is radiused and the tang pocket is narrow. The butt tapers to a 127 mm pad. Our low wrist is longer and grip more vertical; the M24 has an adjustable butt and lower comb. The fixed raised comb and original contours remain deliberate. |
| Channel lips | Section comparison (`renders/checkpoint/changes/channel.jpg`), barrel gap (`renders/checkpoint/sections/forend-sections.jpg`) | Rounded transitions run into broad lands rather than pointed lips. Actual surface sections measure about 1.05 mm minimum radial float clearance at three stations. The reference stock is less square underneath and its forend is longer. |
| Bottom metal and guard | Comparison (`renders/checkpoint/changes/bottom.jpg`) | Broad flat bow faces, a 14.5 × 7.6 mm rounded rectangular section, radiused inletted plate and front paddle replace the wire-like loop. The sharp reference has a hinged internal-magazine floorplate; ours intentionally uses detachable-magazine bottom metal. Tool marks and casting/finish variation are absent. |
| Magazine | Comparison (`renders/checkpoint/changes/magazine.jpg`), loaded (`renders/checkpoint/loaded/magazine.png`), empty (`renders/checkpoint/empty/magazine.png`) | The five-round reference supplies a 64.008 mm rear height and 77.597 mm body length. Pressed ribs have corresponding inner relief, the lips are formed, the floor has a retaining lip, and the catch uses a real notch/sill. The rib positions and floor outline are original; only two representative cartridges are modeled. |
| Bipod | Comparison (`renders/checkpoint/changes/bipod.jpg`), folded (`renders/checkpoint/folded.png`) | Measured 14.5 mm sleeves, 9.5 mm rods and 24.8 mm molded cup feet with flared flat soles replace wires and balls. The reference has tension springs; our permitted torsion return and simpler yoke remain. The spring is visual, not a deformation simulation. |
| Barrel | Comparison (`renders/checkpoint/changes/barrel.jpg`), crown (`renders/checkpoint/crown.png`) | The measured 30.734 mm shank and 23.55 mm near-muzzle diameter follow the cited heavy straight taper shortened to 24 inches. The original target crown is recessed. The reference has different sights/attachments and a duller finish; machining grain and carbon remain deferred. |
| Scope rings/base | Comparison (`renders/checkpoint/changes/rings.jpg`), both rings (`renders/checkpoint/optic.png`) | Separate split caps, two screws per side, base clamps, hex cross-bolt nuts and washers are visible. Both feet now seat on the extended base, whose saddle follows the receiver. Reference screw heads and clamp contours differ; fine tool radii are less rich until baking. |
| Aimed view | Comparison (`renders/checkpoint/changes/reticle.jpg`), true Eye view (`renders/checkpoint/aimed.png`) | The pattern is black and crisp over the newly open central passage. The direct unmagnified tube has a narrow bright field and dark periphery; full-aperture magnification and coating response remain explicitly logged for look-dev/engine integration under the brief's allowance. Eye position and optional objective-camera semantics are unchanged. |
| Scope body | Optic close-up (`renders/checkpoint/optic.png`), clean right pair (`renders/checkpoint/pairs/profile_right-pair.jpg`) | The accepted 30 mm tube, 44 mm objective and 357 mm envelope remain. The reference's objective transition, mounting height and original optic model differ. Our constant aluminum is too smooth to judge a final finish. |
| Turrets and eyepiece | Optic close-up (`renders/checkpoint/optic.png`), aimed rim (`renders/checkpoint/aimed.png`), turret cut (`renders/checkpoint/sections/sections.jpg`) | Axial shoulders, diopter and power rings remain separate. Small grip relief now belongs to the dense normal-bake source. The reference's turret profile and scale spacing differ; the game controls are visually plain before that bake. |
| Cartridges and fired case | Loaded magazine (`renders/checkpoint/loaded/magazine.png`), fired mouth (`renders/checkpoint/case/case_mouth.png`) | The CIP envelope and separate brass/copper forms remain. The reference's jacket/case finish is less uniform; headstamp/anneal detail is absent at this gate, and the 400-triangle case is visibly faceted at macro distance. |

The other cartridge/case forms are unchanged. The open fired mouth (`renders/checkpoint/case/case_mouth.png`)
remains visibly faceted in a macro view at its 400-triangle repeated-object budget.
No new detail is hidden by a promised wear layer.

Image acceptance list (self-review; final form approval belongs to the lead):

- [x] Rear collar, swept stem, tapered shroud and lower cocking tail read as
  separate construction in the rear states (`renders/checkpoint/rear-states.jpg`).
- [x] The radiused port exposes both a round and its raceway in the
  open action (`renders/checkpoint/port.png`).
- [x] Tang-to-comb volume changes smoothly in the
  nine sections (`renders/checkpoint/sections/wrist-sections.jpg`) and
  raking rear quarter (`renders/checkpoint/wrist.png`).
- [x] Rounded channel lands and a continuous barrel gap are visible in the
  forend cuts (`renders/checkpoint/sections/forend-sections.jpg`).
- [x] The bottom view (`renders/checkpoint/bottom.png`) shows a broad guard bow,
  inletted plate and forward paddle.
- [x] The detached magazine (`renders/checkpoint/loaded/magazine.png`) shows ribs,
  formed lips and a lipped floor; seated protrusion is checked in the bottom view.
- [x] Tubes and molded soles read at full detail scale in the
  bipod view (`renders/checkpoint/bipod_detail.png`).
- [x] The heavy taper reads in the dimension side view (`renders/checkpoint/dimensions.jpg`),
  and the crown (`renders/checkpoint/crown.png`) has a visible recess.
- [x] Both split caps, four screws per ring, clamps and nuts are visible in the
  rings view (`renders/checkpoint/rings.png`).
- [x] The aimed pattern (`renders/checkpoint/aimed.png`) uses black material.
- [x] The optic (`renders/checkpoint/optic.png`) retains the accepted stepped
  tube/eyepiece layout; ammunition (`renders/checkpoint/loaded/magazine.png`)
  retains separate case, jacket and formed-lip silhouettes.
- [x] The central etched pattern is crisp over the structurally open passage.
- [ ] Full-field magnification and peripheral optical contrast remain an
  integration/look-dev item, as permitted by the brief.

## Budget and allocation

The current complete rifle is **48,933 triangles**, down from 49,859. It includes
scope, bipod, seated loaded magazine and a chamber representation. The stock is
9,000 game triangles. Fine relief remains authored in `build/sculpt.blend` for
the later normal bake; no normal texture has been baked at this gate.

| Allocation | Before | After | Difference |
| --- | ---: | ---: | ---: |
| Stock | 13,000 | 9,000 | −4,000 |
| Turret grip ribs | 1,536 | 0 | −1,536; dense bake source retained |
| Power/diopter grip ribs | 960 | 0 | −960; dense bake source retained |
| Fine rail bevels | Game geometry | Dense source | Broad rail/slots remain in game geometry |
| Magazine shell and floor | 992 | 2,502 | +1,510 for formed construction |
| Bottom metal and guard | 1,660 | 2,812 | +1,152 for plate/bow section |
| Rear collar, shroud, handle, tail and tang | Simpler assembly | Rebuilt assembly | Main remaining expenditure is visible first-person construction |
| Hollow turret saddle | Solid block | Open structural passage | +284 triangles; center sight is no longer obstructed |
| Pad recesses and seated base heads | No exposed seats | Modeled recesses and solid bearing lands | +540 triangles in the final assembly pass |

Ten temporary constant materials and no texture images are intentional. The next
stage still targets one 2048 BaseColor/Normal/ORM set plus glass. This checkpoint
is not final atlas delivery and does not certify UV overlap or texel density.

## Verification

The following checks passed on the round-two geometry:

| Command / evidence | Result |
| --- | --- |
| `make check` (also included by `make`) | Game solids manifold, dimensions in range, 27 contacts pass; all nine clips swept at half-frame intervals, 2,195 poses, no violations |
| `blender -b --factory-startup --python-exit-code 1 --python src/check.py -- --source build/sculpt.blend --dense --motion --out build/sculpt-check.json` | Dense source: 1,433,619 triangles; same contacts and 2,195-pose sweep pass |
| `src/verify.py`, run by the check target | Fresh GLB: 2,195 affine/semantic poses; seven transitions and eight interrupted-reload resumes pass in source and import; all 48,933 triangles have agreeing winding/normals |
| Independent factory-startup build to `build/recovery-final/bolt.blend` | Rifle and all three standalone GLBs byte-identical; recorded in `build/round2-clean-rebuild.json` |
| `make baseline` | Own ancestor rebuild matches the exact original GLB SHA-256; current presentation regenerated from that geometry |
| Nine optical-path rays in `check.py` and `verify.py` | Game, dense and fresh-import passage clear; the same test rejects the solid round-one saddle (`build/round2-optical-regression.log`) |
| `python3 -m compileall -q guns/bolt/src` and `git diff --check` | Pass |

Logs: `build/round2-make-final.log`, `build/round2-sculpt-check.log`,
`build/round2-clean-rebuild.log` and `build/round2-baseline.log`.
The full `make` also regenerates nineteen principal views, five GLB/photo pairs,
five dense-source/photo pairs, fifteen section cuts, all nine 15-Hz strips and
their real-duration playback loops, four standalone views and the review sheets.
After the strip-only framing change, `make render strips baseline` and
`python3 src/review.py` regenerate the presentation and re-audit playback/source
provenance (`build/round2-presentation-final.log`). Geometry and all four GLB
hashes are unchanged by that camera correction.

`build/provenance.json` audits 317 current-source image records and decoded
playback durations. The exposure-only tonal check includes the studio and is
not an albedo measurement: all-channel white-pixel counts are 2 / 0 / 1 / 0 in
right / left / grip / optic, with no broad clipped highlight areas. Finish and
real albedo calibration remain outside this quick-material gate.

| Inspection export | Triangles | File bytes | Materials / textures |
| --- | ---: | ---: | --- |
| Rifle, scope, bipod and loaded magazine | 48,933 | 2,698,272 | 10 quick constants / none |
| Detached loaded magazine | 4,978 | 118,300 | 4 constants / none |
| Detached empty magazine | 3,718 | 85,792 | 2 constants / none |
| Fired case | 400 | 12,884 | 2 constants / none |

The maximum source/import socket-position difference is 0.000241 mm; the
maximum linear-frame coefficient difference is 0.000000660. The minimum
corner-normal/face-normal dot is 0.0886. Detached magazine spawns are compared
under an independently rotated and translated root, with maximum vertex error
0.000027 mm. These numerical checks prove serialization, not photographic form.

The rig definition, nine clip schedules, socket definitions and 1.2.0 supplement
are unchanged from the accepted checkpoint. The safety's visible stalk/pad,
bolt rear, magazine feed height and base geometry changed around those frames.

The original 24 contact checks retain their meanings and limits. Three added
checks measure both ring feet against the extended base and the base against the
receiver: **27 contacts** in total. The ordinary sweep tolerance remains 0.20 mm.
The existing finite allowances remain 1.9 mm for the 1.8 mm trigger bearing pin,
1.4 mm for the 1.3 mm safety pin, 0.75 mm for the spring-wire joint and 0.30 mm for
visual chamber contact. These pairs are still measured, not skipped. The roughly
1.800 mm aggregate peak is the intentional trigger bearing, not ordinary overlap.

Contact/clearance correctness is checked independently of export agreement.
The fresh-import audit additionally asserts intended ammunition STEP states,
holds, transitions and interrupted reload resumes, then compares affine frames,
posed surfaces, rigid weights, winding/normals and detached magazine spawns.
Matching an incorrect source would not pass the independent contact/sweep tests.

No kit, common module, other gun, rig schedule or interface meaning changed.
Asset-local additions support EXIF-aware captions, denser section evidence and
reproducible historical comparisons. No extra tool or access is needed.

## Final-delivery look development

The current brief accepts the form, mechanism, rig, nine clips, supplement and
27 contacts. The merge is `7784270`, retaining main outside this asset except
both family supplement links and index entries. A forced rebuild and the
original `make check` passed before the merge commit. The only form correction
is `a83e337`: a single shallow rounded receiver tongue replaces the exposed
fork. `detail_032.jpg` shows the class's continuous tang beneath the tail.
The correction retains all bone/socket frames, clips and contact limits;
48,765 inspection triangles, 27 contacts and 2,195 half-frame poses pass.

Every finish pass below loads the **exported GLB and its embedded 2048 maps**.
Each review folder retains camera metadata, GLB/map hashes, finish source and
photo pairs. Geometry checks establish construction/serialization, while these
images judge appearance. Reference pixels never enter the materials.

1. **Pass 1 — `renders/review/pass1/`. Color and value:** the stock is too pale
   and yellow in the used daylight comparison: its selected display patch is
   148.69 versus 116.86/255, R:G:B .993:1:.811 versus .924:1:.950. It reads as
   a clean pale molding. Steel/scope medians differ from the sky-reflecting
   photo, and the scope view needs a patch unoccluded by the lifted handle.
   Rejected the grip/comb rubs: their long boxes terminate like applied labels.
   Rejected the multiple silver eyepiece rings: although narrow in meters, they
   read as decorative bands at full frame. Darkened/desaturated the original
   olive paint, increased resolved spatter contrast, changed contact fields to
   tapered patches, and limited worn eyepiece metal to one accessible rim.
   The continuous tang is visibly one tongue in the rear close-up. The bolt
   bands, retained brass round and dark reticle survive the bake. The exact eye
   view still shows the accepted unmagnified optical tunnel; the optional
   objective-camera integration remains necessary for full-field magnification.
2. **Pass 2 — `renders/review/pass2/`. Color and value:** the darker olive is
   closer to the used stock and keeps cavity depth; the two blacks remain
   distinct. The photo's blue sky reflections are still missing in the neutral
   studio daylight setup, so a separate procedural blue sky fill is required
   for those comparisons, rather than tinting every hero surface blue.
   The scope no longer carries four decorative rings. The grip rub still reads
   as a horizontal sticker: its ellipse extends beyond both visible sides of
   this small curved grip. Reoriented that contact into a narrow longitudinal
   palm-swell rub, with tapered ends inside the surface. The top turret shows
   duplicate numbers from the retained original geometry and the new procedural
   scale; keep its original scale and restrict the new circumferential numbers
   to windage/parallax. The spatter and orange peel now resolve, but the macro
   still has less irregular finish richness than the used photo. Added a faint
   colored reflection component to the glass proxy; no magnification is claimed.
3. **Pass 3 — `renders/review/pass3/`. Color and value:** the daylight stock
   patch is now 119.28 against 116.86/255, with .943:1:.853 versus .924:1:.950.
   The reference coat is grayer; reduce the yellow bias slightly. Its steel and
   scope reflect blue daylight: photo 83.27/65.75 versus render 57.52/35.51.
   Reassessed the material model instead of raising every black's albedo: intact
   matte resin/ceramic steel coating and dyed anodic oxide should have a
   dielectric surface lobe, with metallic response reserved for exposed metal.
   The previous high-metallic dark fields suppress that lobe. Correct this while
   retaining the bright metallic wear cores. The palm rub is now longitudinal
   and tapers inside the curved grip; no transverse rectangular label remains.
   The comb rub follows its top, and the original elevation numbers are no
   longer duplicated. A diagnostic found the leg's normal-based scuff also
   touched its inner bore: constrain it to the actual outer radius. Move the
   right receiver caliber/serial onto the solid rear bridge, clear of the port.
   The shipped bolt-band core is actually 196/202/206 sRGB, metallic 1,
   roughness .290; the turret's >.95 cores are 206/211/215, metallic 1,
   roughness .341. These are PNG readings, not shader-color declarations.
   The diagnostic's first alpha-based coverage denominator was invalid because
   Blender makes self-bake alpha opaque outside the islands; replace it with
   independent exact UV-center rasterization before reporting fractions.
4. **Pass 4 — `renders/review/pass4/`. Color and value:** the final exported
   review patches measure stock **119.94 vs 116.86**, coated steel **86.13 vs
   83.27**, and anodized scope **63.46 vs 65.75** (render/photo, display luma
   0–255). Ratios are stock **.919:1:.911 vs .924:1:.950**, steel
   **.864:1:1.102 vs .744:1:1.279**, scope **.815:1:1.200 vs .750:1:1.250**.
   The two blacks differ in value, hue and roughness. The reference's reflected
   sky is bluer, particularly on steel; the original olive is still less gray
   than its painted camouflage. These are honest view/light differences, not
   a recovered albedo claim. The coating change restores body to the dark
   highlights without raising the stock. Opened the complete nine-view sheet,
   individual hero/optic/bolt/grip/wrist views and the used-action comparison.
   The narrow palm rub follows the swell; the cheek contact stays on the comb.
   The black reticle stays crisp in its accepted central passage. Scope edges
   are silver at full frame, without the old multiple decorative rings.
   Bolt raceway bands remain bright while the intervening oxide stays dark.

   Final diagnostic masks use actual UV-center coverage. Stock: **359,521**
   interior texels, **9,119** above half strength, **7,837** above .95. Its
   worn-core shipping RGB is **33/40/32**, roughness **104/255**, metallic zero:
   dark undercoat with localized gray composite flecks, not a pale noise wash.
   Bolt: **27,715** texels, **5,717** above .95, actual RGB **196/202/206**,
   ORM **255/74/255**. Scope body: **165,485** texels, **277** above .5;
   the narrow rear-rim profile occupies **one shipping texel / about .60 mm**.
   At that profile the delivered RGB is **195/200/204**, ORM **253/87/224**;
   filtering mixes a small amount of intact oxide into this one-texel line.
   It is visibly silver, not a slightly lighter black. The turret's .95 cores
   are **206/211/215**, ORM **255/87/254**; its measured narrow profile is one
   texel / about **.35 mm**. These one-texel edges cannot carry finer chip detail.
   The exterior-only bipod scuff now measures RGB **196/202/206**, ORM
   **255/74/255**, instead of picking up the sheltered bore's dark AO.
   Full samples, thresholds and physical profiles are built by `make wear-audit`
   at `build/review/wear-final/mask-stats.json`. This diagnostic evaluates the
   same original masks on finalized surfaces; dense-source normal/projection
   differences are explicit, while RGB/ORM always come from shipping PNGs.
5. **Pass 5 — `renders/review/pass5/`, then full-resolution finals. Color and
   value:** the original coating values are retained; the final, independently
   ray-hit surface patches measure stock **113.94 / 116.86**, steel
   **89.10 / 83.27**, scope **62.17 / 65.75** (export/photo). Export/photo
   ratios are stock **.906:1:.914 / .924:1:.950**, steel
   **.868:1:1.099 / .744:1:1.279**, scope
   **.797:1:1.203 / .750:1:1.250**. These supersede the earlier approximate
   patch-coordinate measurements: each corner now comes from a real finalized
   triangle hit at declared Y/Z stations. The geometry, rays, measurement-source
   hashes and GLB identity are included in the value report. The stock remains
   slightly greener and the steel's reflected sky less blue than the photo.

   The first full-resolution underside view exposed overly regular bag-contact
   boundaries, despite their causal placement. Rejected that regularity. Added
   only submillimeter lateral fray at 5–12 mm intervals along the existing
   contact paths, and suppressed orange peel where paint has been polished off.
   No broad noise field determines the worn region. Opened the new hero, wrist,
   palm, bolt, optic, engraving and underside views and the eleven-view sheet.
   The tapered paint loss now has resolved small boundary variation and smooth
   exposed contact cores. It retains visible dark undercoat and sparse gray
   composite. The final stock mask has **9,150** texels above .5 and **7,668**
   above .95, over the same **359,521** interior texels; actual core RGB stays
   **33/40/32**, ORM **255/104/0**. The other finishes and their wear values are
   unchanged from pass 4. No rig, UV, contact or clip schedule changes occur.

   The native-scale pair keeps the hero's actual stock and cap pixels. The used
   stock crop is resized to an estimated receiver-diameter scale; its different
   coating and contour are labeled. A second row compares the cap's apparent
   edge scale against a used field-painted cap. It is explicitly not identical
   anodizing or submillimeter photographic metrology. The single-texel silver
   rim remains visible at the actual hero size. Full-frame hero luma p1/p50/p99
   is **3.00 / 76.36 / 188.43**, with **11.93%** below 24/255 and **zero clipped
   pixels**: the stock is not pale, cavities stay deep and highlights roll off.
   Tiny white specular pixels remain in the optic/bolt macros (fractions
   4.56e-6 / 2.46e-5), without a broad clipped area.

## Final delivery proof
Commands completed with exit 0:
```sh
make -C guns/bolt
make -C guns/bolt critique PASS=pass5
make -C guns/bolt export
make -C guns/bolt check
make -C guns/bolt render match strips extra source-match review docs
make -C guns/bolt wear-audit
python3 -m compileall -q guns/bolt/src
python3 kit/repo_check.py
git diff --check
```
The full default build passed before the last localized paint refinement. The
final export/check/presentation sequence above then regenerated and checked
the actual shipping textures. No kit, existing common, pistol or shotgun file
was changed. Main outside this asset is retained, apart from the requested
family index and additive interface links. All GPU stages used the inherited
shared kit lock; scratch remained inside this worktree.
| Audited assembly | Triangles | Contacts | Swept poses | Result |
| --- | ---: | ---: | ---: | --- |
| Inspection | 48,765 | 27 | 2,195 | Pass |
| UV-prepared | 48,763 | 27 | 2,195 | Pass |
| Actual imported GLB triangles | 48,763 | 27 | 2,221 | Pass |
| Dense finish source | 1,433,451 | 27 | 2,195 | Pass |

Imported animation key times include tiny float-offset samples in addition to
the 2,195 half-frame contract poses; they add clearance samples, not duration.
Raw GLB sampler times independently match all nine declared durations. Ordinary
clearance remains .20 mm. The approximately 1.800 mm aggregate maximum is the
intentional trigger bearing, still measured under its unchanged 1.9 mm bound.
The original safety/spring/chamber finite allowances also remain unchanged.

All **2,195** affine/state comparisons pass. Maximum socket/bone
position delta is **0.000241 mm**, and maximum linear-frame
coefficient delta **0.000000659**. Imported triangle attribution
is one-to-one across all **48,763** triangles / **181** named
parts, maximum vertex difference **0.000065 mm**. These prove
serialization; the independent contacts/sweeps above prove construction under
the declared sampling and finite joint allowances.

The clean factory-startup repeat produces four byte-identical inspection GLBs.
The final 4096/32 bake checks **4,443,384 interior texels per channel**, with
zero missed samples in BaseColor, roughness, metallic, AO, micro-AO and normal.
Every delivered PNG is 2048; all four GLBs embed byte-identical canonical maps.
Fresh gun UV coverage is **30.4045%**, clipped overlap **0**, outside/degenerate
triangles **0**, density **1,612 px/m median**, 5th/95th **1,064 / 2,680**.
The complete atlas covers **32.2257%** including the denser reserved case.

| Final GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| bolt | 48,763 | 2 | 11,102,844 |
| magazine_loaded | 4,976 | 1 | 7,016,076 |
| magazine_empty | 3,716 | 1 | 6,947,144 |
| case | 400 | 1 | 6,756,048 |

The magazines retain their accepted held-gun geometry rather than a separate
dropped-prop reduction; their geometry is counted inside the rifle ceiling.
The explicit fired-case ceiling remains 400. Canonical PNG sizes: 1,402,055 / 2,174,142 / 3,149,718 bytes
(BaseColor / Normal / ORM). Runtime allocation is approximately **16 MiB**
compressed with mipmaps, with consumer atlas/content-hash caching.

Final provenance passes **315 current-GLB PNG records** and decoded
real durations for all **9** WebPs. Opened the final docs, the full still
contact sheet, six exported photo pairs and six dense-source pairs, the native
stock/cap wear pair, and the twelve clip inspection panels covering every
rendered time sample. The clips retain clear magazine handoff margins and the
bipod camera retains the feet through fold/extension. The refreshed paint stays
attached to its rest surfaces; no projection tear or texture swimming appeared.

Final stills: `renders/final/beauty/`; extra engraving/bag-contact views:
`renders/final/details/`; detachables: `renders/final/loaded/`, `empty/`,
`case/`; contact sheet: `renders/final/contact-sheet.jpg`; exported/source
pairs: `renders/final/pairs/` and `renders/final/source-pairs/`; real-speed
strips: `renders/final/strips/`. The final rifle SHA-256 is
`7cc808a4ef23c7c43f4b82371dafd0b28e6752881de6f9231d739f864c609cd3`.

Docs JPGs (all 1600 px wide, below 200,000 bytes): action **133,923**, details **177,795**, eevee **52,184**, hero **49,145**, turnaround **58,008**.

Remaining weaknesses: the direct scope view is an unmagnified dark peripheral
tunnel, with the accepted objective-camera integration still required for
full-field game magnification. Fine engraving/spatter/knurl detail softens in
the 2048 bake; the source/display pairs show that loss. The one-texel silver
cap/rim cannot carry smaller nicks. The 400-triangle case is faceted in extreme
macros. The used photograph has bluer steel reflections and different paint,
stock and scope construction; these differences are explicit, not hidden by a
low landmark residual or a dimensional pass.

No new tool or lead input is needed. A future kit improvement would be shared
rigid-part triangle attribution and exact UV-center wear rasterization, which
currently remain asset-local wrappers following the finished family bar.

## Lead correction pass 1 — white balance, scope integration, round case

**Color and value.** The previous blue calibration was wrong. Its shade cast
was carried into the coating rather than separated from the finish. All
comparison photographs now pass through an explicit reference-only linear RGB
neutral adaptation before measurement and pair composition. Multiply linear
RGB by the following gains, normalized to preserve the neutral patch's Rec.709
luminance; this is a chromatic correction, not an exposure match. Native pixel
rectangles, selected-neutral overlays and every material patch are reproducible
with `src/white_balance.py` and `src/reference_measurements.py` in
`build/white-balanced/`. No reference pixels enter a shader or atlas.

| Reference | Neutral, native rectangle | Linear RGB gains |
| --- | --- | --- |
| right_photo / left.jpg | Bare silver bipod screw, 809,184–816,191 | 1.253420 / 0.970818 / 0.770660 |
| profile_right | Bare silver mounting ring, 760,70–774,83 | 1.017628 / 0.988191 / 1.072228; backdrop clipped |
| left_photo | White backdrop, 150,100–500,220 | 1 / 1 / 1; clipped, residual cast unconstrained |
| open_photo | Silver feed/raceway highlight, 1530,184–1640,197 | 0.906192 / 1.009801 / 1.263708 |
| wrist_photo | Silver cocking pin, 855,154–863,176 | 0.984356 / 0.993911 / 1.120427 |
| used_open / Rackandchamber | Pale gray uniform panel, 20,20–65,55 | 1.214051 / 0.977881 / 0.772139 |
| independent daylight | Snow near boot, 145,650–200,685, brightest 15% | 1.008604 / 1.008604 / 0.901206 |

The screw and bare-metal highlights are estimated neutrals rather than a color
chart. The field fabric is also an estimate. Clipped white cannot measure a
cast: the profile therefore uses its independent gray ring, and the left image
remains an auxiliary construction/finish comparison with that limitation stated.
The primary steel target is the corrected right photograph, never the shaded
camouflage photograph. Corrected right barrel median is **66.72/255**,
**0.955:1:1.045**; receiver **48.88**, **0.840:1:1.140**. Their different shadow
and reflection angles explain the remaining local hue range. The scope shows
both a satin highlight (**112.32**, **0.895:1:1.061**) and a dark lower strip
(**17.73**); neither is treated as recovered albedo. Used olive-gray paint is
**117.42**, **1.017:1:0.847** on the original polygon, versus **113.64**,
**0.948:1:0.871** in the first neutral-lit export. Keep the accepted original
olive paint and its wear unchanged.

Opened `renders/review/correction1/views/{hero,aimed,right_photo,profile_right,
used_open}.png` at native size. The first neutral steel export measured **81.00**,
**1:1:1**, at the right-camera receiver patch: hue fixed, but its broad reflected
highlight still lifted the matte action too far above the black reference.
Increase only the intact steel's central roughness from .47 to **.60**; keep
its neutral linear base **.0035/.0035/.0035**. Scope base is a deeper neutral
**.0018/.0018/.0018**, with its existing .33 fine satin and accepted opaque
silver edges. All wear masks, exposed bolt bands and markings stay unchanged.

The first integrated aimed view now fills the ocular with the actual objective
render of the procedural range: **8×, 10.0042° square FOV, 100 m, 1.8 m target**.
It retains the exact Eye frame and 70° player-camera FOV, a thin black rim and
centered original pattern. Raise the primary aimed render to at least 128
samples without denoising so the thin black shader reticle survives cleanly.
The source GLB keeps its original geometry reticle; the opaque render target
occludes it in the demonstration. Slot assignment and all power fields are
now explicit in INTERFACE.md.

The fired case retains all 14 axial stations and dimensions. Radial counts vary
with visibility: 40 at both mouth loops, 32 at neck/shoulder, fewer at the hidden
base. Angular zipper joins have no T junctions. Total **768 triangles**, within
the lead's revised approximately 800 ceiling. The loaded and chambered rounds
retain their accepted geometry. Native magazine/port inspection confirms their
24/18/20-sided representations stay round at the sizes shown. The first case
macro exposed uneven triangle-weighted shoulder normals at the variable ring
joins. The next pass replaces only those case normals with analytic revolution
normals, retaining true hard rim and extractor-groove boundaries. The initial
case evidence is archived in `renders/review/correction1/case/`.


## Lead correction pass 2 — final exported delivery

**Color and value.** Measure the complete exposed face, keeping its dark
regions as well as the reflection strip. The corrected right photograph's
combined receiver/barrel median is **41.40/255**, **0.881:1:1.071**; the
export is **38.00**, **1:1:1**. This is the near-black value target. The
earlier 66.72 measurement was only the barrel's brighter stripe, not the
complete black face. Both masks and the narrow diagnostic stripes remain in
`values.json`; no measurements were discarded. Full photo barrel/receiver
medians are **42.43 / 37.03**, versus **37 / 55** in the exported patches.
Their local reflection angles differ, but their combined value and neutral
coating agree. The separate flash-light tests did not improve agreement and
are not used by the final neutral comparison setup.

Scope: corrected photo visible-bell median **32.59**, **0.853:1:1.235**;
rendered diffuse tube **31.72**, **0.984:1:0.969**. These sample different
surface normals. Photo dark/highlight patches span **17.73–112.32**, while
exported diffuse/highlight patches are **31.72–68.89**. The painted/dyed
coating is a deeper black with a .33 satin response; the steel's .60 matte
reflection is broader. Neither black carries the earlier blue base color.
The remaining photographic hue is not copied into either neutral material.
Steel highlight pixels also remain neutral under the neutral studio lights.

Stock: corrected used coat **117.42**, **1.017:1:0.847**, versus original
olive export **113.57**, **0.940:1:0.871**. Keep the accepted greener olive
paint and its narrow contact wear. The source stock function is unchanged.
The reference is gray/olive field camouflage rather than the same web paint.
Hero luma p1/p50/p99 is **2.00 / 68.86 / 173.50**, with **0%** fully clipped
pixels and deep cavities. This is not a pale blue-gray action.

All reference material medians below were remeasured after their individual
corrections. Full RGB/G ratios, pixel counts and native polygons are in
`build/white-balanced/measurements.json`; selected patches are marked in
the adjacent `*-measurements.jpg` files. A missing scope is explicitly absent.

| Corrected reference | Steel median(s), 0–255 | Scope median, 0–255 | Stock median, 0–255 |
| --- | ---: | ---: | ---: |
| left.jpg | 42.43 / 37.03 | 32.59 | 81.53 |
| m24_profile.jpg | 45.08 / 81.58 | 26.86 | 77.87 |
| PEO_M24_SWS-01.jpg | 91.78 | 78.15 | 96.15 |
| detail_030.jpg | 88.99 | absent | 164.95 |
| detail_029.jpg | 95.47 | absent | 181.08 |
| open.jpg | 83.39 | 65.30 | 117.12 |
| daylight.jpg | 25.58 | 21.86 | 19.65 |

The left reference's receiver is field painted, not exposed black steel; its
backdrop is clipped. Its identity correction and auxiliary status are explicit.
The daylight stock is black, not the foreground camouflage rifle. The
profile's corrected gray ring uses gains **1.017628 / .988191 / 1.072228**.
No estimate here is presented as a calibrated material reflectance.

The final case macro was reopened after the second 4096 bake and GLB import.
Its 40-sided mouth is circular at 1100 px; the 32-sided shoulder no longer
reads as an octagon. Analytic radial/profile normals remove the uneven face
weighting at the ring transitions, while real rim and groove boundaries stay
sharp. The case remains **768 triangles**, **12.01 × 51.18 mm**. Loaded-magazine
and open-port finals were checked at native resolution: their existing round
silhouettes do not need extra triangles. The accepted rifle, magazine geometry
and rig therefore remain unchanged.

A final optical calculation caught the initial presentation-FOV convention:
using the player's 70° field divided by power would understate magnification
inside this smaller physical aperture. The shipped integration instead uses
`2 atan(0.0188 / (0.0919 * M))`. The aperture subtends **23.12298°** at Eye;
**8× uses 2.92961°** horizontally/vertically, at **100 m**, on the existing
ocular. This implements angular magnification at the actual eye relief. The
70° primary camera stays exact Socket_Eye. All integer powers 4–16 have their
fields in `scope-integration.json` and INTERFACE.md. This supersedes the
initial 10.0042° pass-1 experiment.

The final delivery identity audit compares all **229 rifle accessors**, plus
all four accessors in each magazine, byte-for-byte with the accepted delivery.
Positions, indices, normals, tangents, UVs, weights, joints, bind matrices,
clip samples, nodes, mesh/material/texture layout all agree. Only image
payloads and the intentionally revised standalone case are excluded.
`src/stable_delivery.py` preserves one accepted pad tangent component at a
four-decimal MikkTSpace rounding boundary; its exact vertex and UV are asserted
before restoring the accepted value. This avoids a numerically equivalent
0.0001 tangent variation from violating the requested byte identity. It adds
no geometry, rig or layout change. Proof: `build/correction-identity.json`.

`make -C guns/bolt check` passes after the final case rebuild: all **27
actual-surface contacts**, source/finalized/imported/dense motion and intended
states, independent rebuild, budgets, UVs, normal directions and canonical
embedded atlas hashes. Bake remains **4096 / 32 samples → 2048**, zero missed
interior texels on every channel. No kit/common/pistol/shotgun changes.

Final static budget: rifle **48,763 triangles / 2 materials / 11,066,664 bytes**;
loaded magazine **4,976 / 1 / 6,979,896**; empty **3,716 / 1 / 6,910,964**;
fired case **768 / 1 / 6,735,228**. Canonical PNGs are **1,395,234 / 2,172,295 /
3,122,206 bytes** (BaseColor / Normal / ORM), embedded identically in all four
GLBs. Gun UVs stay unchanged: **30.4045%**, zero overlap/outside/degenerate
triangles, median **1,612 px/m**, p5/p95 **1,064 / 2,680**. The complete atlas
now covers **31.8515%** after re-unwrapping only the case's reserved rectangle;
case median is **4,086 px/m**. Maximum affine errors remain **0.000241 mm**
position and **0.000000659** linear coefficient. All **2,195** intended pose
comparisons and the additional imported float-key samples pass.

Final provenance passes **315 current-GLB image records** and exact decoded
playback durations for all **9** WebPs. Opened the final contact sheet and all
five docs JPGs, all six exported and all six source photo pairs, the native
wear pair, the case macro and aimed view at native size, plus all twelve clip
inspection panels (also composed into four review overviews). No material
swimming, missing round, changed pose or clipped bipod appeared. The final
rendered evidence and current source snapshot are frozen under
`renders/review/correction2/`; pass 1 remains separate.

Final paths: `renders/final/beauty/` (including integrated `aimed.png`, objective
`aimed-range.exr` / preview PNG and `scope-integration.json`),
`renders/final/pairs/`, `renders/final/source-pairs/`,
`renders/final/{loaded,empty,case,details,eevee,strips}/`, and
`renders/final/contact-sheet.jpg`. Rifle SHA-256:
`63b8c20c86f8983f15e6ba298827b5fc032f91068bb619364db645197b137a1e`.
Docs JPGs, all 1600 px wide and below 200,000 bytes: hero **48,032**,
turnaround **57,420**, details **170,231**, action **136,344**, Eevee **51,029**.

Remaining limits: white balance from small silver/fabric patches is an estimate;
clipped backdrop whites cannot prove a residual cast. Local reflection angles
and reference coatings differ, so the published display medians are not albedo
measurements. The 2048 atlas still softens fine engraving/spatter/knurl detail.
The engine must implement the documented camera/RT composite; the Blender
integration now demonstrates it completely. No lead input or new kit feature
is needed for this delivery.

## Trigger correction — blade direction and exported close-ups

The accepted rifle's trigger was wrong: a 4.4 mm round rod bowed toward the
muzzle, with its toe returning toward the grip. This correction changes only
`Trigger_Shoe`. The existing pivot `(0, 26.69, 23)` mm, rigid Trigger bone,
−12° X pull, all nine clips, and all other manufactured parts stay fixed.

References: Arthurrh's isolated right-side 700 action, CC BY-SA 3.0, and Zachi
Evenor's sharp 5076 × 1600 M24 photograph, CC BY-SA 4.0, both on Wikimedia
Commons. Direct URLs, authors, licenses, native crops and limitations are in
[refs/SOURCES.md](refs/SOURCES.md). Neither is mirrored or used to generate
vertices or texels. The latter has different chassis/guard construction; only
its trigger is a form comparison. The former's silhouette is clear, but its
small native trigger cannot resolve fine machining.

1. **Profile and volume — `renders/review/trigger1/`. Color/value:** neutral
   Workbench shading is a form aid, not a proposed finish. Compared the actual
   photographs with right, oblique and pulled views. The first blade has the
   correct concave +Y finger face, convex rear and forward toe, and the oblique
   view shows parallel flat sides instead of a round rod. Its toe ends too
   abruptly as a rectangular cut. Add a 0.32 mm machined perimeter radius.
2. **Toe and clearance — `renders/review/trigger2/`. Color/value:** the same
   gray inspection shading keeps the comparison fair. Reopened all five views,
   including both photo cameras. The toe's small roll catches a continuous edge
   highlight, and the blade reads as broad and flat in the oblique view. The
   full pull visibly moves toward the grip, with daylight under the toe. Keep
   the already accepted guard; do not reshape it to the different chassis.
3. **First exported bake — `renders/review/trigger-bake1/`. Color/value:**
   accepted near-black control finish, deep surrounding cavities and a narrow
   silver reflection edge. At native macro resolution the toe's baked shading
   ripples, although the game geometry is clean. Reject that projection loss.
   The independently resampled dense toe bevel has a slightly different corner
   fan. Use the resolved game blade's manufactured surface as its bake source,
   retaining the original procedural control-finish microdetail. No game vertex,
   normal, UV, pivot or animation changes in this bake correction. Also refine
   the short-baseline oblique camera fit; its native landmark RMS falls from
   7.13 to 4.53 px. These residuals describe camera fitting, not shape accuracy.
4. **Corrected exported bake — `renders/final/trigger/` and
   `renders/final/trigger-pairs/`. Color/value:** retained the accepted neutral
   black control coating, with a broad dim reflection and a narrow edge roll;
   no new blue albedo or raised finish value. Opened the right, three-quarter,
   pulled and both paired exported views at native resolution. The toe ripples
   are gone. The oblique view exposes the blade's transverse width and gently
   crowned finger face; both photographs and the export curl toward the muzzle.
   Also opened the two dense-source comparisons: the shipping atlas softens the
   finest edge response, but preserves the curve and rounded toe. Hero opaque
   asset-pixel luma p1/p50/p99 is **2.00 / 69.00 / 171.07**, with **zero**
   all-channel clipping (`build/trigger-hero-values.json`). Surrounding cavities
   stay deep. The oblique lens estimate reaches its 150 mm fit bound; these
   short-baseline, cropped photographic fits are orientation/form evidence,
   not calibrated physical dimensions or recovered albedo.

Exported pairs (original asset left, unmirrored photograph right):

- `renders/final/trigger-pairs/trigger_photo_right-pair.jpg` — Arthurrh,
  [right-side 700 action](https://commons.wikimedia.org/wiki/File:Rem700_action_lefthand_standard_right.jpg),
  **2.70 native px** camera-fit RMS.
- `renders/final/trigger-pairs/trigger_photo_quarter-pair.jpg` — Zachi Evenor,
  [sharp right/oblique M24](https://commons.wikimedia.org/wiki/File:IDF-modernized-M24-SWS-0001.jpg),
  **4.53 native px** camera-fit RMS.
- Dense-source equivalents: `renders/final/trigger-source-pairs/`.
  Blender independently verifies the fitted projections within **0.00020 px**.

The blade is **6.35 mm wide**, with a **3.2 mm nominal section depth**, gently
radiused front and **0.32 mm toe edge radius**. Width is an authored class
estimate from the photographs, not a manufacturer dimension. Actual centerline
front-face rays at Z = 14 / 10 / 4 / −3 mm hit Y = **34.560 / 32.018 / 29.957 /
32.949 mm**. Their normals face +Y. Back-face rays hit **30.619 / 28.388 /
26.687 / 28.416 mm**, with −Y normals. These measured surfaces establish the
concavity, convex back and forward return independently of the authoring knots.

The trigger still pulls **−12° about X**, about its unchanged **(0, 26.69, 23)
mm** pivot. Additional construction checks use actual triangle vertex/face and
edge/edge minima, after rejecting surface intersections. Thirteen quarter-frame
pull poses retain measured shoe/pin engagement (intersecting solid visual
bearing surfaces) without any guard crossing. These are sampled poses, not a
continuous-time collision proof; the existing full clip sweep remains intact.

| Actual triangle surfaces | Rest gap | Pulled gap | Minimum over 13 pull poses |
| --- | ---: | ---: | ---: |
| Source / finalized | 1.549 mm | 1.473 mm | 1.431 mm |
| Fresh imported GLB | 1.549 mm | 1.473 mm | 1.431 mm |

No tolerance or finite joint allowance was relaxed. These measurements prove
construction; the serialization comparisons prove agreement with that source.
`build/trigger-identity.json` passes against the saved accepted exports for all
four deliveries. Every non-trigger ordered triangle-corner byte (positions,
normals, tangents, UVs, joints and weights) agrees; all rig/clip accessors,
nodes, skins, animations, mesh/material/texture layout agree exactly. Joined
indices necessarily shift after changing the trigger vertex count, so the
comparison expands ordered triangle corners before excluding only the Trigger
bone. Images are the intentionally rebaked exception. Separate source audits
prove all **180** other inspection meshes, **181** finalized meshes including
the staged case, and **181** dense-source meshes byte-identical in positions,
topology, normals and UVs (`build/trigger-mesh-identity.log`,
`build/trigger-dense-identity.json`). No accepted source snapshot is a new
build dependency: the old authored tube is regenerated solely as an atlas
packing reservation, then replaced by the blade in a previously empty strip.

Trigger: **452 → 620 triangles (+168)**. Complete rifle: **48,763 → 48,931**
delivery triangles (**48,933** inspection). Two materials; one 2048 three-map
atlas, rebaked at **4096 / 32 samples**. All **4,404,558** checked interior
texels per channel hit their source, with zero missed samples. Full UV coverage
is **31.9759%** including the staged case; rifle **30.5289%**, no overlap,
outside or degenerate triangles. Rifle density is **1,613 px/m median**,
p5/p95 **1,064 / 2,680**. All four GLBs embed the same canonical maps.

| Final GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| bolt | 48,931 | 2 | 11,090,352 |
| magazine_loaded | 4,976 | 1 | 6,997,748 |
| magazine_empty | 3,716 | 1 | 6,928,816 |
| case | 768 | 1 | 6,753,080 |

Canonical BaseColor / Normal / ORM PNGs: **1,397,751 / 2,178,855 / 3,130,984
bytes**. The accepted scope integration, case, wear functions, cameras and
presentation layout are retained. No kit/common/pistol/shotgun changes.

Final commands, all exit 0:

```sh
make -C guns/bolt export
make -C guns/bolt trigger-match
make -C guns/bolt check
make -C guns/bolt render match strips extra source-match review docs
# From guns/bolt, compare against the saved accepted exports:
blender -b --factory-startup --python-exit-code 1 --python src/trigger_identity.py -- --before build/trigger-before/export
python3 -m compileall -q guns/bolt/src
python3 kit/repo_check.py
git diff --check
```

| Independent construction audit | Triangles | Original contacts | Swept poses | Result |
| --- | ---: | ---: | ---: | --- |
| Source inspection | 48,933 | 27 | 2,195 | Pass |
| UV-finalized | 48,931 | 27 | 2,195 | Pass |
| Actual fresh-imported triangles | 48,931 | 27 | 2,221 | Pass |
| Dense source | 1,433,619 | 27 | 2,195 | Pass |

The additional thirteen-pose trigger checks pass in all four audits. The
factory-startup repeat reproduces all four inspection GLBs byte-for-byte.
All **2,195** affine/state comparisons pass, maximum positional error
**0.000241 mm**, maximum linear coefficient error **0.000000659**. Fresh-import
triangle attribution is one-to-one across **48,931 triangles / 181 parts**,
maximum vertex error **0.000065 mm**. No semantic schedule, socket or clip changed.

Logs: `build/trigger-export2.log`, `build/trigger-check2.log`,
`build/trigger-pairs2.log`, `build/trigger-finals2.log`. Final provenance passes
**320 current-GLB image records** and exact decoded durations for all **nine**
WebPs. Reopened the still contact sheet, all five docs JPGs, exported/source
photo-pair overviews and all twelve clip inspection panels in three overviews.
Magazine handoff, round visibility, bipod framing and exact integrated scope
view remain intact. These broader views retain the accepted delivery; native
trigger images judge this correction.

Final stills: `renders/final/beauty/`, including `bottom.png`; full sheet:
`renders/final/contact-sheet.jpg`; trigger rest/pulled macros:
`renders/final/trigger/`; trigger pair sheet: `renders/final/trigger-pairs.jpg`;
exported/dense pairs: `renders/final/trigger-pairs/` and
`renders/final/trigger-source-pairs/`. Existing exported/source pairs,
detachables, extras and nine playback strips are regenerated in their original
locations. Rifle SHA-256:
`05e9bd69971aca05c4ca9040b519d805c52ad918661c26863de33a2696488d5b`.

Final docs: hero **48,015**, turnaround **57,408**, details **170,152**, action
**136,309**, Eevee **51,023 bytes**; all 1600 px wide and under 200 KB.

Remaining limits: width is a class estimate, and the photographic fits cannot
establish manufacturing dimensions or submillimeter machining. The older
isolated-action photo has limited native resolution; the sharper M24 photo has
a different chassis and guard. The shipped normal atlas softens fine edge
response in an extreme macro. No unresolved trigger clearance or construction
failure remains. No kit change, new tool or lead input is needed.
