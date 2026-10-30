# Harrow 56 — form checkpoint review

This is a reviewable **unbaked visual checkpoint**, not form approval or final
asset acceptance. No look-dev, production texture delivery or docs JPG is
claimed. The acceptance marks below mean that the named trait was observed in
an image; the residual column remains part of each finding.

Passes 1–7 and their measurements are the original checkpoint history.
**Round 2 is recorded in passes 8–11 below; pass 11 and the current README
supersede the older budgets, material counts and provisional eye station.**

## References and color/value discipline

The sharp right and oblique-left exterior photographs are 2,126 pixels across.
The early attached-box photograph is 2,507 pixels across. The open-cover field
photograph is 4,235 pixels across; its tray region remains over 600 source
pixels across. They show different furniture generations, not one exact
product to copy. Authors, licenses, direct image URLs and use are in
[refs/SOURCES.md](refs/SOURCES.md). No photograph is a texture input.

`src/white_balance.py` balances the comparison copies before measurement. The
right/left white backdrops clip, giving identity gains; those neutrals cannot
constrain a remaining cast. They are form evidence, not albedo calibration.
The early box view uses the pale backdrop rectangle (20,20)–(220,90): linear
gains .991262/.979209/1.030978, preserving neutral luminance. The open field
view lacks a trustworthy neutral and remains form-only. Its sandy ground is
not assumed gray. Correction records are in
`build/white-balanced/corrections.json`. No material values are accepted here.

The attempted aiming candidates are also logged rather than misused:
`cheek.jpg` looks toward the photographer; `aim1.jpg`/`aim2.jpg` use optics
and hide the stock contact; `iron_aim.jpg` does not show a settled cheek weld.
Two later sharp candidates also fail that specific test: `aim_kneeling.jpg`
shows a chin against a telescoping stock tube, with the pupil hidden behind
the helmet/glasses; `aim_prone.jpg` rests the head on the support hand. Both
are useful exterior evidence, without supplying a measured fixed-stock weld.
None justifies a measured iron-sight eye relief. The present 75 mm relief is
provisional. The ray and comb distance are actual mesh measurements, separate
from that ergonomic gap in the evidence.

Camera fits use manually observed landmarks through the kit's photo-match
solver, with an independent projection check. Native residuals remain visible
in `build/cameras.json`. A low residual is not contour approval. The right and
open comparisons do not fully align the original stock/sight spacing and
cover opening; the region list below does not conceal that mismatch.

## Critique passes

1. **Color/value first — first assembly.** The constants are clean and much
   more uniform than either the used box view or the field photograph. No
   finish judgment. `renders/pass1/all-images.jpg` exposed an entirely occluded
   hero camera behind the small studio wall, an empty-looking belt/tray, an
   overlong box pedestal, a sharp trigger toe and a plain handguard. Rejected
   that result. Hid the wall for held-asset views and used an opaque procedural
   gray camera background. Every still explicitly requests the complete Idle
   pose rather than the common rest template pose.
2. **Color/value first — export ownership.** The gray constants made the missing
   belt especially obvious. `pass2`/`pass3` showed only one cartridge at the
   box, despite correctly spaced bone heads. Inspection of actual evaluated
   meshes exposed shared deform-group ownership: every linked copy followed
   the final owner. Replaced those skins with rigid bone-parented shared mesh
   instances. Source/import checks now inspect the meshes, not just the bones.
   Shortened the suspension so the box actually clips immediately below the
   receiver. Rejected the crossing, disconnected-looking bipod deployment.
3. **Color/value first — visible assembly.** In `pass4`, the gold/gray belt was
   finally visible and contrasted too strongly with the clean receiver; these
   are still inspection constants. The front/side views exposed an excessive
   curl at the box mouth, a clipped muzzle and clipped bipod feet. Rebuilt the
   guide with a continuous downward entry, widened the hero framing, separated
   fold/splay owners and changed the splay direction. Moved channel ends onto
   their mounting seats. The near aperture and centered post read against gray;
   its oversized-looking base remains a form weakness.
4. **Color/value first — construction under raking light.** `pass5` and the
   first photographic pairs showed a cleaner, simpler cover/handguard than the
   references. Kept finish behind the gate. Rebuilt the trigger as a curved
   broad blade with a blunt, rounded section rather than accepting its angular
   toe. Added proper visual openings for the tray, cover hinge/release tabs,
   safety display and box lid. The first clearance sweep was rejected: it
   measured tray/receiver crossings, lid and belt intersections, and legs
   passing through each other. Serialization agreement did not excuse them.
5. **Color/value first — belt and contact corrections.** The reference's links
   remain darker/more varied than our constants. No wear acceptance. Removed
   the guide's abrupt reversal at the box mouth; it caused a multi-millimeter
   spacing excursion between frames. The current solver has a continuous guide
   and measured interpolation error. Consumed owners now disappear before the
   incoming belt advances, while the last-three demonstration reveals the real
   tail. The reload lifts outboard before lifting higher, keeping the train
   clear of the closed side flap. The box's mouth continues through its upper
   side wall, and the lid clears its suspension. Further sweeps rejected small
   tray-edge intersections: narrowed the actual pan/seat rather than granting
   a belt-wide exception. Only the two small bipod splay shoes retain explicit
   finite seating allowances; no wildcard or unbounded collision waiver exists.
6. **Color/value first — final checkpoint evidence.** The main hero has deep
   black cavities, medium gray body highlights and bright ammunition; its
   constants remain much cleaner than the photographs. The approximate
   foreground display-luma 1st/50th/99th percentiles are 0/61/224; 0.42% of
   foreground pixels reach 255 in a channel. That small bright-metal clipping
   is not finish acceptance. Opened all main/detail/standalone renders, all
   five photographic pairs, the sections and all nineteen strip sheets.
   Widened the right rake to retain the muzzle. Added a separate full-cover
   view because the photo-fitted open view crops the cover crown. Rejected the
   remaining cropped muzzle in the motion camera and replaced that camera
   with a wider orthographic view. The comparison bipods now use the shorter
   extension pose at frame 54; the fully extended frame 84 stays in the bipod
   detail. The right pair still puts a foot at the lower frame edge. The
   right/left pairs also show the reference handle raised against ours folded;
   that pose mismatch limits handle comparison. The body proportions read as
   the class, but the oversimple sight base, capsule handguard, small feet and
   broad unbroken receiver/cover flats remain visibly CG form weaknesses.
7. **Color/value first — isolated link support.** The clean gray standalone
   link made two floating bridge strips obvious. They sat above the open
   cuff arcs. Rejected that construction and rebuilt each as a finite diagonal
   formed web whose ends enter the actual cuff bands. Opened the new
   Workbench close-up and the regenerated exported-link studio view; the webs
   now visibly meet both cuffs. The triangle allocation stays unchanged. This
   repairs support in the visual mesh, without claiming a real interlock or
   engineering-standard pitch. The complete source/import checks and
   presentation were rerun for this revised shared mesh.

## Image acceptance list and remaining differences

All paths below are under `renders/checkpoint/`. Primary stills and pairs load
the exported GLB with its quick constants. Sections intersect actual imported
triangles. These are visual traits checked at this checkpoint, not a claim that
all regions already meet the final photographic bar.

| Region | Observed form / evidence | How the photograph still differs |
| --- | --- | --- |
| [x] Receiver and rivets | `raking_right.png`, `left.png`, `sections.jpg`, `pairs/right_photo-pair.jpg`: broad sheet lands, open finite-wall receiver, exterior rivets and rails. | Our rivet pattern is more regular and the pressed rails simpler. Reference seams, stamped relief and local fastener seating are richer. The ribs are separate visual skins over the folded shell; the inner wall does not repeat their full emboss. No wear breaks up those broad flats yet. |
| [x] Cover, tray and rear sight | `cover_open.png`, `cover_open_full.png`, `rear_sight.png`, `pairs/open_photo-pair.jpg`: low shell, rear release tabs, pivot sleeves, tray opening/stop, underside display pawls and a genuinely open aperture. | The reference's cover has more reinforcement and smaller layered sight fittings. Ours has a long plain crown and a heavy-looking sight base. The field comparison's original cover/optic differs in length/angle, leaving the top incompletely framed; use `cover_open_full.png` as well. This mismatch is not accepted by a camera RMS. |
| [x] Charging handle | `charging_handle.png`, `pairs/right_photo-pair.jpg`: broad paddle, finger opening and separate shoe in an exterior guide. It remains stationary during firing. | The reference paddle has a stronger curved finger cup and subtler radii. Ours is a simpler angular stamping, with a conspicuous open slot. |
| [x] Trigger, guard, grip and safety | `trigger.png`, `lower_raking.png`, `pairs/trigger_photo-pair.jpg`, grip cuts in `sections.jpg`: muzzle-facing concavity, forward toe, broad guard band, changing grip sections and push-button display. | The source trigger face is broader and its lower curvature fuller; ours remains an original slimmer blade. The reference has a more developed molded housing, grip texture and flank panels. The new toe removes the old knife-like bend, without claiming identical contour. The current blade crop is below the requested 600-pixel regional reference size; it proves direction only, and finer acceptance remains open. |
| [x] Barrel, handle, gas group and front sight | `barrel_handle.png`, `front_sight.png`, both rakes, `aimed.png`: stepped exterior, slotted muzzle envelope, collar/web construction, windowed tower/hood/post and outboard folded carry handle. | Original longitudinal sight/collar spacing differs from the references. The reference has fuller collar transitions, finer regulator relief and more contour in its handle grip. These differences limit the whole-gun camera fit. The simplified display gas group has no operative port. |
| [x] Handguard and stock | `furniture.png`, `handguard.png`, both rakes and six furniture cuts: compound retained subdivision molds, hollow U handguard, changing stock neck/comb and rounded straps. | The handguard reads smoother and more capsule-like than the reference's broad flank/scalloped front. The stock's wrist/comb is an original smoother curve, with fewer molded recesses. Dense-source pebbling, seam relief and finish are still pending a bake. |
| [x] Bipod | `bipod.png`, front view and `strips/BipodDeploy.jpg` / `BipodFold.jpg`: open channel legs, separate extensions, witnesses, detents and finite feet; fold and splay no longer cross the legs. | The reference feet are broader and more dished, with more developed hinge/stop fittings. Ours is a simplified original assembly. The two visual splay shoes seat by a bounded small overlap; that is reported, not called zero penetration. |
| [x] Box and belt | `belt.png`, `box.png`, `pairs/belt_photo-pair.jpg`, `strips/Reload.jpg` / `ReloadEmpty.jpg` / `BeltEnd.jpg`: close suspension, separate lid and mouth, curved individual train, count-aware real tail and outboard reload lift. | The photographed early box is narrower and its belt hangs more vertically; ours bows farther outboard. It is an authored planar guide, not a gravity/stiffness solution. The cyclic helper is not an engine integration or an occlusion proof. Baked clip interpolation retains a small measured spacing error. |
| [x] Ammunition and links | `detachables/cartridge/cartridge.png`, `detachables/case/case.png`, `detachables/link/link.png`, plus the belt macro: round silhouettes, open fired mouth and individual finite cuffs/webs, with mesh reuse. | The photo's shoulder/jacket transitions and link bends are finer. The links are decorative visual approximations and no real mechanical interlock/pitch standard is certified. The fictional headstamp masks are prepared, but remain unbaked and therefore absent from these GLBs. |

## Evidence boundaries and outstanding form issues

The source/import affine/surface comparisons establish serialization. The
separate triangle-surface contact tests establish visible seating; the full
sampled clip sweeps establish the stated penetration bounds at their sampled
times. None is a continuous collision guarantee or a functional firearm test.
There is no sear render geometry, so no bolt/sear physical-contact claim.
Bipod detent proximity is a visual surface fit, not a working detent model.

The exact sight ray reaches the post and clears the cover/handle. The eye is
75 mm behind the actual aperture rim and approximately 57 mm above the stock
at its station. The latter is high enough that a proper measured cheek-weld
reference remains necessary before eye placement can be accepted.

## Rebuild and measured proof

`make -C guns/lmg WIDTH=1440 SAMPLES=32` completed successfully. After the
camera, dimension-overlay and presentation-audit refinements, the individual
`check`, `render`, `strips`, `pairs`, `extra`, `sections`, `dimensions` and
`markings` targets also completed successfully. `src/evidence.py` verifies
current-GLB hashes for every presentation image and exact encoded durations
for all nineteen real-speed WebPs. It records twenty primary stills, five
photo comparisons, five standalone stills, seven belt-advance frames and
nineteen uniformly timed clip strips. Full commands and logs remain ignored
under the worktree's `build/`.

The final complete rebuild, including the supported link webs, is logged as
`build/lmg-final-make-link-supported.log`. Earlier interrupted attempts are
retained as diagnostics; they are not reported as successful builds.

- `build/check.json`: 47,760 staged scene triangles, no nonmanifold meshes,
  1,040.000 × 169.242 × 283.000 mm loaded/stowed envelope. Source clearance:
  802 samples, zero violations. Belt half-frame spacing error at most
  0.087264 mm; cartridge-axis error zero.
- `build/serialization.json`: 3,529,940-byte GLB, seven temporary materials,
  zero textures, 34,728 unique raw mesh triangles. 64 bones, twelve sockets,
  nineteen clips. 155 affine samples, maximum position error 0.0001661 mm;
  five actual evaluated surface poses agree within 0.000152 mm. Minimum raw
  normal/corner dot is +0.06064. Fresh-import clearance: 1,538 samples, zero
  violations. Ordinary penetration at most 0.1666 mm. The two named bipod
  shoes reach 0.3549 mm under their explicit 0.4 mm seating bounds.
- Eight fresh-import surface gaps, in mm: cover latch 0; box latch 0;
  suspension seat 0.000004; left/right bipod detent 0.200/0.200; first round
  to stop 0.00356; next round to pawls 0.1076/0.2392. The contact negative
  fixture correctly rejects a 1 mm lifted land. Three pure belt continuity,
  count and owner-recycling tests pass.
- The inspection GLBs for loaded box, empty box, cartridge, case and link
  contain 5,564 / 2,668 / 896 / 704 / 276 triangles and occupy 146,136 /
  65,116 / 23,204 / 18,776 / 11,196 bytes. No texture subset exists yet.

The image index is `renders/checkpoint/contact-sheet.jpg`, with three
`review-page-*.jpg` pages. Dimension overlays are in
`orthographic-dimensions.jpg`; twelve actual imported cuts in `sections.jpg`;
the focused seven-frame feed sequence is `belt-advance.jpg`. All region
evidence paths are listed in the table above. The material stage remains
intentionally unstarted. This evidence supports a reviewable checkpoint;
the form weaknesses and missing cheek/trigger evidence prevent full form
acceptance.

Process correction: early manual preview calls used a worktree-local GPU lock
instead of the inherited shared lock. The canonical make/render path uses the
inherited shared `ASSETS_GPU_LOCK`. Early previews are diagnostics, not final
proof. No kit or existing common code was changed to hide this correction.

Possible kit follow-up: promote the touching-versus-lifted parallel-land
regression and triangle-centroid contact fallback into `kit/assembly.py` after
running the full kit suite. This branch keeps that fallback local. The kit is
unchanged; the only new shared modules are the inert 5.56 display meshes and
the additive 1.8 schema helper. No other gun folder or existing common module
was edited.

## Form round 2 — pass 8, first revised surfaces

Color/value first: `renders/round2-pass1/` uses Workbench gray to expose form;
its dark background and constant clay are not albedo evidence. Opened all six
native previews beside the right/left crops and the sharp underside/sight
photographs. The stock is visibly deeper through the toe, the comb has the
photograph's dip, and the handguard has broad flat sides and a flat lower
edge. Rejected the initial 58,499-triangle allocation. The handguard ribs spend
too many triangles on tiny radii; the sight ears also overspend on bevels.
The rear aperture is now small, but the old camera sits implausibly close.
The underside arm reads in the cover; the tray is a plate rather than rods.
The handguard detail and furniture camera clip their subjects and need wider
framing. The receiver's new embossing produced a nonmanifold Boolean edge;
this is a failed build, not acceptable topology. Reduced covered/subpixel
surfaces and removed three box-end display meshes while retaining all 64
owners and all 19 clips. Every visible cartridge uses the accepted shared mesh;
its standalone is unchanged. Further pairs and motion checks follow below.

## Form round 2 — pass 9, photographic pairs and sections

Color/value first: the exported one-material inspection palette has deliberately
uniform response and pale brass. It is visibly unlike the used photographic
finishes, which remain outside this round. Opened all nine native pass-2 pairs,
the imported section sheet and the two-link section. The new stock's lower
edge is substantially closer, but the molded recess needs more depth to read
under the rake. Rejected the tiny carry-handle rise: its folded arm radius was
too short to produce the raised silhouette in the photograph. Lengthened the
outboard arm while retaining its owner, axis and clips. The handguard's broad
flank and 14-mm rib spacing now read; its front must remain square.

Rejected the rear-sight close-up: the aperture is smaller, but the reference's
two knobs are on one flank at different longitudinal stations, and its ears
rise toward their front. Ours put one knob on each flank and used level ears.
The 234-pixel fit residual was warning of wrong correspondence, not permission
to accept it. Corrected those external relationships and refitted the camera.
The close tray pair hid the plate under ammunition although the photo is empty;
use ReloadEmpty at the same cover angle. The new box pair looks from the wrong
end and clips its catch; refit against the actual near-end landmarks. The feet
still read as end blocks: their broad planes rotated vertical on deployment.
Reoriented the pads at their existing owners, compensating splay, so their
planes are nearly horizontal in the deployed view. No new rig bones or clips.

The source's full-frame sweep reduced the construction failures to a single
left rivet touching the tray by 0.50 mm. Moved that rivet down within its pressed
land, rather than exempting it. The imported sections now show both walls of
the receiver emboss and a hollow stock at both requested stations. The two
links' mesh section shows the middle cuff between its neighbor's two cuffs.

## Form round 2 — pass 10, player views and assembly corrections

Color/value first: opened the native Cycles hero, eye view, shooter's oblique,
stock, handguard, open cover and bipod from `renders/round2-pass3/`, and all
three new region renders. The one-material quick palette is too uniform and
its brass too pale for finish acceptance. The stock recess now reads under
raking light; the toe and butt height still need the final local photo check.
The sight's smaller aperture no longer fills the receiver width, and the post
is centered. The 20-mm presentation lens wastes most of the frame at the longer
eye station; use 40 mm from the same socket without moving the camera.

The deployed pads now show flat upper surfaces and a pressed lip. Their legs
are still longer than the near leg in the right photograph; shorten the inner
end by 45 mm and use the fully extended pose for the oblique left photograph.
The closed cover's lower edge left a 4-mm visual gap over the rear receiver;
extend its side walls to the receiver top. The region render exposes the old
box lid's large center cut and unsupported suspension: remove that cut and
make the suspension a lid-owned component, retaining the Magazine parent and
spawn frame. The taller, shallower shell better matches the manufacturer's
box. Two belt/lid contacts remain in the full sweep. Diagnostics locate them
at the pre-scaled opening edge; explicitly update the edited mesh before the
Boolean and re-run the complete sweep. No blanket collision exception added.

## Form round 2 — pass 11, final exported evidence

Color/value first: opened the final exported-GLB contact sheet and native
hero/player/region stills beside the balanced photographic pairs. Inspection
steel remains dark through its cavities and the highlights roll off without
clipping: approximate foreground display luma P01/P50/P99 is 0/65.06/226.86,
with no foreground channel at 255. Uniform roughness and pale brass still
look synthetic. They are inspection constants, not accepted albedos or wear.
The clipped white side backdrops cannot calibrate material color; the red
sight backdrop and field photograph are form-only evidence.

Opened the four new close pairs (cover underside, empty tray, rear sight,
right receiver) and the molded-box pair, all with landmark arrows. The sharp
2538 × 3384 cover photo retains more than 600 source pixels across the tray.
The cover now reads as pressed walls, arm, pawls, latch and sight housing;
the tray reads as a finite plate with formed lips rather than a rod frame.
The wider `cover_open_full.png` retains the entire raised assembly. The loose
sight pair retains the full rim; its 217.4-pixel native RMS and its different
base/ear contour remain the weakest comparison. This is not an exact replica
or a finished-form approval. Tiny manufacturing relief awaits the retained
high-source normal bake; reduced ear surfaces show coarse shading up close.

The side pair's raised carrying handle and deployed bipod now correspond to
the photographed pose. The right photograph uses the retracted deployed
legs, the oblique left uses the extended legs. The five stock landmarks are
within the stated ±8-mm local photographic uncertainty: rear/front comb
103.51/111.06 mm, butt height 134.00, toe drop 131.00 and lower edge at grip
42.33. The hollow stock sections and recess read in `sections.jpg` and the
furniture rake. No shoulder rest is modeled on the selected fixed-polymer
version. The flat handguard sections measure 65.83 × 62.48 and 63.30 × 60.81
mm, with approximately 4.5-mm outside corners and 14-mm rib spacing.

Both bipod legs measure 253.36/318.22 mm hinge-to-pad-centroid retracted/
extended. Their 12 × 9-mm channel sections and 36 × 22-mm pads read in the
close-up; deployed pad planes are 5° from horizontal. These are actual mesh
measurements. No individual leg-length specification was found in primary
class manuals; the retracted near-leg photo estimate is 235–260 mm. The
rounded box has its rim, end ribs, lid, catch and supported suspension clip;
the pair residual is 30.6 pixels. Its underside and broad flank are still
clean and feature-sparse until the later authorized finish stage.

Re-examining the cheek photograph corrected which spectacle lens covers the
aiming eye. The supported cheek/hand station implies approximately 88.5 mm
behind the aperture by an affine sight-radius transfer. Adopted **85 ±25 mm**,
replacing 75 mm. The pupil is hidden; this is an inferred plane, not a direct
anatomical measurement. `eye-weld.jpg` identifies that limitation. The main
eye view uses a 20-mm presentation lens from `Socket_Eye`; the separate
40-mm macro inspects the centered post without changing camera position.
The shooter's oblique shows the corrected cover, sight, handle and belt.

Opened all nineteen final strip sheets as well as the seven-frame belt
sequence. The long reloads retain their lift/remove/replace/close order; the
new box mouth and finite cover clear through the sampled motion. The strips
are dark Workbench motion evidence, not material judgments. WebP durations
are verified by metadata; viewing strip sheets does not claim continuous
collision proof or real-time playback assessment.

Final rebuild: `make -C guns/lmg` passes, logged in the worktree-local
`build/lmg-round2/make-final14.log`. The subsequent explicit
`make -C guns/lmg check` passes in
`build/lmg-round2/check-after-final.log`: 1,529 source and 1,556 fresh-import
poses, every 60-Hz clip frame plus authored keys/endpoints, zero violations.
Import includes extra nearly duplicate float key times; there are no skipped
integer frames. Maximum ordinary penetration is 0.1666 mm under the 0.2-mm
limit; named splay shoes reach 0.2804 mm under their existing 0.4-mm limit.
Pair-relative caching only removes duplicate solid tests.

The ready bolt's inert witness seats on a supported fixed witness at all
ready endpoints with measured zero gap, and separates 79.99998 mm at the
forward-empty endpoint. This is a visual seat, not an engineered sear.
Twenty-seven fresh-import contact rows pass, including the negative seat
check; the lifted-land regression and three belt tests pass. All sixteen
single cuffs fit their next round at the measured Idle pose within 0.000032
mm. The fifteen neighboring interleavings and recovered 3/3-mm axial gaps
are shown by actual imported triangles in `link-interleaving-section.jpg`.
The accepted belt guide and its 0.087264-mm half-frame spacing bound remain.

Final allocation: **47,640 / 48,000** evaluated scene triangles; **one**
untextured inspection material; **3,958,128-byte** GLB; 64 bones, twelve
sockets, nineteen clips. The current README lists triangles by part group
and all five standalone sizes. Two round owners and three link owners at
the hidden box end have no mesh; seventeen rounds and sixteen links retain
one shared mesh each. Fine detail is retained in source geometry for the
later bake. No cartridge, case or link source shape changed this round.

`build/presentation.json` verifies current GLB hashes for 22 main stills,
ten pairs, five standalone stills, seven feed frames and nineteen strips.
The final image index is `renders/checkpoint/contact-sheet.jpg` with four
`review-page-*.jpg` pages. Stock rulers, eye evidence, twelve imported
sections, and the two-link section are included. No look-dev or docs JPGs
were created. Only `guns/lmg/` changed; kit/common code is unchanged. No
additional tool or approval is needed. The local contact regression remains
a possible separately tested kit contribution.
