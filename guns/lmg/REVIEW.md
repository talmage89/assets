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

## Look round 1 — pass 12, first baked export (rejected)

Color/value first: opened the native 1600-pixel `renders/look-pass1/hero.png`
and the handguard close-up beside `used_receiver.jpg`, `used_oblique.jpg`,
`stock.jpg` and `belt.jpg`. The receiver's black begins from the accepted
Rill/Relay paint (.0015 linear, roughness .42, specular factor .161), but gray
rivet heads made an artificial dotted pattern. The gray heat shield was too
light against the black handguard. Polymer had no legible molding response.
Rejected this bake as a finish. Paint the receiver rivets and pressed heat
shield; increase molding relief from 24 to 65 µm at a coarser 2.3-mm scale.
These are shader/normal changes, with no added game triangles.

The handguard detail exposed circular projection marks beside its molded
ribs. Isolate the main handguard, its six ribs and the shield in the kit baker.
The first box scuffs read at the two bottom corners, but the barrel/handle
and feet remain too uniform to accept before the per-site controls. Cartridge
cases have a broad bright reflection; check the histogram and actual belt
photo before accepting that brightness. The first transparent hero also
needs an opaque neutral background for unambiguous full-frame judgment.

White balance: the new used receiver photograph has an unclipped gray studio
backdrop at (80,40)–(280,210), with linear RGB gains .9140/.9960/1.1087.
The issued field photo uses pale gravel, and the belt close-up uses the gray
range background at its upper left. The earlier clipped catalog whites
cannot establish color; they remain form comparisons only.

UV preparation exposed submicron slivers in FeedCover_Shell. A 2-µm
degenerate-edge cleanup in the delivery stage removes 132 triangles there
(800 → 668); the accepted source stays at 47,640, and delivery is 47,508.
No other named part's triangle count changes. The round/link reuse, all
64 bones, twelve sockets and nineteen clips remain. This is the sole form
cleanup, to be bounded against actual source surfaces in final verification.

The initial all-edge cleanup above was rejected for simplifying 132 triangles
when only two failed the UV gate. Restricted cleanup to
the single common shortest edge of the two submicron triangles. The revised
cover is 798 triangles, not 668; delivery is 47,638 rather than 47,508.
The final surface comparison, rather than the requested operator tolerance,
will establish how much this changes the actual surface.

## Look round 1 — pass 13, corrected bake and framing

Color/value first: opened the next gray-background native hero and handguard
close-up. The black rivets no longer draw a dotted map of the receiver; the
heat shield now belongs with the painted stamped parts. Independent rib
projection removes the little circular ghost marks along the handguard.
The gray barrel and bipod are distinct from paint. The cover's exposed
underlayer still reads too pale under the studio softboxes; lower it from
.084 to .062 linear, keep its matte roughness, and retain bright steel only
on a very small high-point subset. Add spatially varying oil polish inside
the support-hand contact on the molded handguard, not a general noise wash.

The first deployed hero put a foot on the bottom frame boundary. Lower the
camera's target by 60 mm while retaining its location and 53-mm lens, so the
whole deployed silhouette has inspection margin. The right ejection ports
are physically hidden in the left hero: deliver both full-frame hero angles
for each independent wear control and state which view actually sees a site.
No assertion of visible right-port carbon will be based on the left hero.

Preservation audit correction: the first single-precision BVH test reported
0.125 mm even when querying identical unchanged faces. That was numerical
loss in the tiny-face BVH, not a measured form change. Replaced it with
double-precision point-to-triangle distances and re-ran both directions on
vertices, centroids and edge midpoints. The restricted cleanup's maximum
sampled surface difference is **0.000324 mm**. Every other part has identical
triangles and vertex coordinates.

## Look round 1 — pass 14, native studio and baked assembly

Color/value first: opened all 23 exported studio views in the native hero and
three review sheets, including both sides, the four orthographic directions,
rear sight, opened cover, handguard, handle, ammunition, aimed and shooter
views. Paint is now visibly deeper than the polymer. The shield belongs to
the painted group; the barrel and bipod keep gray phosphate. The cover rubs
read as a few connected gray lands, with black lengths between sites. The
box corners show gray scuffing without a uniform pale bottom band. Deep
receiver and handguard cavities stay dark on the neutral gray background.
The cartridge highlights remain broad under these studio cards and require
the forthcoming whole-part histogram check.

The deployed still revealed two tiny black detent witnesses hanging below
the pads. The measured gap to each supporting extension was 14.8069 mm,
left over from the accepted leg shortening. Move each former 259-mm witness
to 363 mm, the next 26-mm station after 285/311/337. Keep its name, owner,
shape and triangles. Both actual support gaps become zero by triangle-surface
intersection. These are the only source-form corrections in this look round;
the delivery-only cover cleanup removes two submicron triangles. No leg
length, leg profile, hinge, clip or original contact is changed. Two new support
rows supplement the retained 27 contact rows. Rebuild the bake and every
exported render after this correction.

Added sharp used whole-gun views with unclipped gray studio backgrounds.
The earlier clipped white ribbed-handguard image remains useful for molding
texture and construction, but cannot calibrate a residual color cast. The
new gray-background images give a second neutral check for black paint,
molded polymer, barrel and bipod relationships. Their older furniture and
more exposed receiver finish are explicit photographic differences.


## Look round 1 — pass 15, whole-part color and bake loss (rejected texture scale)

Color/value first: opened the native final hero, the reversed hero, the used
receiver pair, ammunition pair and three-gun studio comparison. The family
paint blacks agree; the cover and receiver wear reads in a few connected gray
lands. The older reference receiver has much more exposed gray/green phosphate
than our black-painted receiver. Its value distribution is consequently
brighter; matching only that receiver's median would destroy the specified
black coating and the family's paint relationship. The reference bipod is
also more exposed and brighter. Record those differences explicitly.

The metallic ammunition highlights are gold/copper and the green tips follow
the photograph, but the macro is too perfect. Its drawn tooling variation and
the polymer grain nearly disappear at 2048. Rejected that manufacturing-texture
scale after opening the handguard and carrying-handle details. Increase the
mold height input from 65 to 240 µm (160 µm on rubber), retain the same 2.3-mm
molding scale, and increase the secondary fine relief from 3 to 18 µm. These
are peak input ranges, not an assertion of measured physical roughness. Hand
polish still reduces relief inside its original contact site. Add original
axial draw-roughness variation on the cases and jackets; break the annealed
neck transition slightly along the forming direction and retain the brass
beneath it. Do not add triangles or spread any of the nine wear masks.

Found a sharper used fixed-stock photograph on concrete and two used molded
box photographs. The concrete is the stock photo's estimated neutral. Both
box photos have clipped white backdrops; they are useful texture/value and
wear-shape evidence but cannot prove residual highlight cast. Compare the
stock and box over their own whole visible surfaces, replacing the earlier
shared-molding proxy crops. The unclipped gray-background handguard/grip
photographs remain the cross-check on that shared black molding finish.
Rebuild the canonical bake and every independent wear control after this
manufacturing change; no former render may count as final evidence.


The photographic-mask audit also rejected two earlier numerical comparisons:
the near-leg outline cut across the background, and the grip polygon included
a wedge beside its curved back. Inspecting native grid overlays exposed both.
Replace them with whole visible silhouettes of both legs and the grip, extend
the receiver and cover observations over their complete visible bodies, and
exclude the flash hider from the barrel-only sample. The earlier histogram
numbers are superseded. Save native outline overlays for every final
photographic observation so this can be judged in two dimensions too.


## Look round 1 — pass 16, revised exported texture checkpoint

Color/value first: opened the new native 1600-pixel hero and the handguard,
carrying-handle and belt details directly from the revised GLB. The molding
now has a visible fine relief under the raking card, without a pale color
wash. The cartridge's forming variation remains inside the brass hue rather
than reading as dirt laid over the belt. Paint and the phosphate underlayer
retain the family studio relationship established in pass 15. Freeze these
finishes for the final comparisons and nine complete control bakes.

The close view still has smoother ammunition than the photograph, especially
the green paint and drawn jacket; the repeated belt instances share the same
atlas chart. The handguard's tiny seam darks are more apparent under the
macro's rake than at player distance. Keep those limitations in the final
report. No extra geometry or additional texture set is added to disguise them.
The raw, unseparated GLB audit will check that the diagnostic part recovery
has not changed the final rendered normals or appearance.


The final full-gun photo sheets exposed two slightly clipped deployed feet.
Added a camera-only framing audit using actual fresh-import triangles in each
photographic pose. Preserve the fitted lens, orientation and roll; translate
the camera in its image plane and back just enough to retain a 3.5% margin.
Recompute and expose the landmark RMS after this adjustment. Right, left,
issued-field and used-right views need a change; the old box/belt view already
fits. No part, pose, authored key or sight station changes. The used-right
bounds change from Y 114–802 to 54–725 in its 779-pixel photographic frame.
Source and GLB comparisons are regenerated with these same final cameras.

The isolated ammunition comparison is also darker than its used photograph
over the complete case and link surfaces. Increase the procedural cards and
reflected environment by 2.4× for that diagnostic photo only, retaining its
camera/background exposure and all frozen material inputs. This is a lighting
fit; the hero and its three-gun studio lighting are unchanged. Re-render them
as well after the presentation-code revision so every final is current.


Resolved the independent-control footprint check on actual atlas surfaces.
Receiver wear also reaches the adjoining receiver cap/collar and a few rivet
heads through the selected-to-active bake; cover wear reaches the touching
sight base. Those are the same exposed edge neighborhoods, rather than a
new use mask or a different material pass. Include these physical parts in
the site's on/off mask and audit their complete guarded charts. The first
three current controls pass with no unrelated change over three quantized
levels in any embedded map. The other controls will use the same audit.

A closer neutral inspection found an unclipped strip of the first used-box
photo's white paper in its cast shadow, native (900,1300)–(1100,1304).
Its linear RGB gains are 1.08750/1.01133/.91603. Use that whole box for the
primary value/highlight chart, with the mixed key/fill limitation stated.
The second box photograph's clipped whites remain texture/wear-shape evidence
only. Rebalancing changes only this one color-reference image; every camera
comparison's white-balanced input is byte-identical to its previous version.


Opened all fourteen dense-source pairs beside the fourteen baked-export pairs,
the five standalone stills and four raw-import stills. The same photo cameras
show no missing mold or material region after the bake. The source has finer
molding and draw detail; the exported metal retains broader, smoother
highlights. The standalone loaded/empty box stills clipped the scuffed bottom
corners slightly. Pull only those two inspection cameras 20% farther from
their unchanged targets. Add a 3% frame-margin assertion on the actual imported
triangles of all five standalones. This is a presentation fix; spawn origins,
geometry, subsets and materials are unchanged.

The unseparated byte-identical GLB comparison records native-image mean
absolute RGB differences of .00615 (hero), .00354 (handguard), .00303
(handle/barrel) and .00233 (belt), on the 0–255 scale. The hero's maximum is
three levels; the handguard has one pixel over four levels (maximum six).
The other two have no pixel over four levels. These tiny render differences
do not explain the material character; the named-part reconstruction has not
substituted a prettier source scene for the shipped mesh.


The trial 20% pullback still left only 1.08% below the standalone boxes, so it
was not accepted as the final framing. Center each on its actual imported
three-dimensional bounds, retain its viewing direction/lens, and move back
until every vertex has at least 5% margin. Both boxes finish at 5.07%; the
cartridge, case and link retain their existing 20.97%, 10.63% and 20.32%
minimum margins. The final review independently checks the rendered cameras
against freshly imported triangles, with a 3% lower gate.


## Look round 1 — pass 17, final baked delivery

Color/value first: opened the native hero, all 23 studio views, the Eevee
hero, the fourteen baked and fourteen dense-source photo pairs, the raw-import
checks, all five standalones and the nine independent full-frame wear pairs.
The neutral family studio keeps the Harrow's paint black alongside the Rill
and Relay. Its barrel and bipod are gray, its molding is a separate black,
and its copper/brass remains warm. The native hero's luminance p1/p10/p50/
p90/p99 is **1 / 10.93 / 46.43 / 96.57 / 201.16**, with zero clipped foreground
channels. The finish table in README records every whole-part distribution
and highlight RGB, including misses rather than only favorable patches.

The nine on/off differences stay where their causes act. Receiver and cover
show a few gray lands with black lengths between them. The handle changes
mostly by polish, the three carbon sites darken their discharge neighborhoods,
the feet have separated pressure/lip scraping, the box has two lower corner
scuffs, and the butt has a rubbed return. The left hero's one changed port
pixel is indirect/minor and cannot establish visible port carbon; use the
reverse hero's 1,619-pixel change. README lists each site's area and ΔY and
links the complete on/off proof. The worn receiver/cover's base-color and
roughness samples establish gray phosphate against glossy black enamel.

All nine 4096/32-sample control bakes have zero missed interior texels. Their
GLB geometry, UVs, normals, skinning, nodes, sockets, 19 clips, material
settings and samplers are identical; the maximum texture change outside
the physical site charts plus guards is two quantized levels. The raw import
image check and six posed triangle comparisons separately bound diagnostic
part-recovery error. Contact and motion checks separately establish fit.

`make -C guns/lmg` passed in `build/make-final-refined.log` (exit 0), and the
explicit `make -C guns/lmg check` passed in `build/check-final-refined.log`
(exit 0). The accepted source has 47,640 triangles; the final GLB has 47,638,
64 bones, twelve sockets, nineteen clips and one three-map 2048 material.
It is 12,496,192 bytes; canonical PNGs total 7,932,869 bytes. All five lossless
subsets, their bytes and their source/spawn comparisons are in README and
`build/delivery/verify.json`. The 1,529-source / 1,556-import pose sweeps have
zero violations. All original 27 contacts and both added mark-support
contacts pass. No clearance waiver was added.

The brighter stripped receiver and polished bipod reference, smoother
ammunition macro and the small raking-light seam darks on the handguard
remain the weakest comparisons. The stock's used photograph has broader
field scuffs than this brief's focused butt rubbing. Do not call these images
an exact photometric reproduction of one factory variant. This original
combination keeps the accepted form and the requested coating states.

No docs JPGs, kit changes, common-module edits or other-gun source changes.
No tool or approval is needed from the lead. A future kit helper that retains
rigid part attribution through joined weapon export would remove local
recovery code; the actual-triangle and raw-render checks here show the
current method's practical error bounds.


The final index contains 67 hash-verified native GLB renders and 128 total
sheet entries, including both sets of fourteen photo pairs, twelve finish
charts, eighteen on/off sheets, the photographic outlines and the three-gun
studio composite. Opened all eleven final review pages and both reframed
native standalone boxes. The final contact sheet is
`renders/final/contact-sheet.jpg`; the measured tables and direct pair links
are in README. Final presentation audit passes after including the studio
composite in the index. No docs images are generated.

## Look round 2 — pass 18, baseline and physically plausible inputs (rejected)

Color/value first: opened the two native player/hero images, three-gun panel,
all twelve finish charts, all eighteen on/off sheets, wear-sites sheet and the
native used whole/receiver photographs. The reported misses are real visible
failures. The coating crushes while phosphate and furniture look like primer.
The receiver target is unpainted olive phosphate and cannot accept black paint.
Preserved the complete round-1 GLB, maps, renders, geometry observations and
source shader under `build/look-round2/before/` before changing anything.

Opened the native first source trial beside those photographs. A 2.2% diffuse
paint input removes the implausible .15% input, but its broad response is too
bright under the old diffuse comparison lighting. The reference has a narrower
reflected card, dark flats and brighter high points. Merely increasing albedo
is rejected. Phosphate now starts dark, with bath/crystal variation and local
brown heat; the first trial is too dark in the photo setup. None of these
source previews counts as shipped appearance or acceptance.

## Look round 2 — pass 19, lighting and comparison camera audit (rejected)

Color/value first: opened native `renders/round2-pass2/` hero, receiver and
whole-gun comparisons. Lower fill improves darks, but cover median remains
81 against 37; grip 60 against 79; barrel 30 against 53. Reject all three.
The previous whole-gun camera was below the receiver and the close receiver
fit used a rear-sight landmark on the wrong part. It changes which surfaces
are sampled and which reflection family is visible. Re-observe local body
landmarks and constrain the visible elevation, keeping fit residuals explicit.

Opened the sharp replacement black-coated receiver photograph. White paper
under the grip's cast shadow is an unclipped neutral estimate. The two gray-
carpet dealer photographs were inspected and rejected as close surface targets:
one is olive phosphate, and both have too little regional resolution. The
old stock and box comparisons used unrelated inspection angles. Fit their
actual photographed flank/end views before deciding their finish values.

## Look round 2 — pass 20, located wear and revised photo views (rejected)

Color/value first: opened all seven native `renders/round2-pass4/` views. The
revised hero has narrower satin reflections and darker phosphate; its coat
still reads too gray. The stock's diffuse photo fit overexposes its edge; the
box and stock camera optimizations hit a roll/pose limit and are rejected.
Do not excuse a distribution error with those bad views.

Extended receiver/cover abrasion along exposed lengths, with phosphate first
and rare bright steel at sharp high points. Added independently switchable
rivet-head rubs and original finite gear-drag scratches on the handled cover
top. Their procedural construction reads no reference pixels. The source
close-up shows the scratches, but full-frame wear still needs measurement and
baked confirmation. The new grain is too coarse on furniture in these source
macros; reduce its scale and height before final baking. All accepted forms,
64 bones, twelve sockets and nineteen clips remain unchanged.

## Look round 2 — pass 21, actual 2048 bake and lighting response (rejected)

Color/value first: inspected all ten native `renders/round2-baked1/` images
against the white-balanced studio references. The barrel and stock are now
dark in the hero, with deep internal shadow, but the cover's highlight is
still too sharp and the box and grip need separate response corrections.
The preliminary baked table has cover 24/47/80 against 28/37/115; the polymer
box 62/78/91 against 25/47/72. Reject them. The source appearance is not an
acceptance proxy: baked phosphate and polymer grain lose substantial contrast.

Rendered and inspected six complete twenty-card linear-light diagnostics of
the actual import. A single physical rig per photograph can recover barrel,
bipod, stock, box and ribbed-handguard distributions without implausible base
colors. The overbright whole-gun diagnostic was a misplaced reflecting card,
not permission to darken the whole gun. Retain fitted area lights, then rerender
and measure final PNGs rather than accepting the linear predictor.

The cover-top cuts in the shooter view are too long, broad and alike. Shorten
and vary their finite gear-drag paths; narrow the edge contact lands and break
the bead exposure. Keep the visible rivet crowns independently switchable.
The box impact damage occupies too much of its lower corners; constrain it
to the corner returns instead of a broad rubbed end. Increase the resolvable
dry-grain relief, preserving the same geometry, maps and draw-call budget.

## Look round 2 — pass 22, reject a numerically favorable partial light fit

Color/value first: inspected all five native `renders/round2-fit1/` images.
The isolated stock and box are close to their distributions. The whole-gun
light fit is rejected: it fits the barrel and bipod by putting a large card
in the receiver's reflection, turning unmeasured paint pale. A favorable
barrel table cannot accept that whole photograph. The small linear response
images also bias narrow-barrel and leg tails after mask erosion and separate
denoising. Refit at delivery resolution without per-card denoising, include
whole-view coating/polymer guard observations, and verify the rerender.
No mask, contrast adjustment or reference image may enter the asset.

## Look round 2 — pass 23, measured wear density and grain retention (rejected)

Color/value first: opened all second-bake hero, shooter and surface macros.
The broad black family is much closer, but surface relief is still too smooth
in the close views. Delivered handguard tangent-normal samples cluster near
127.6/127.6/255, with only about 1–2 encoded levels of interior variation.
Raw noise has far less contrast than its nominal height implies. Normalize
its original molding/conversion-grain signal before baking; put phosphate
relief at a wavelength that survives 2048 rather than adding unresolved noise.

Opened the native coverage pairs and independently classified photo overlays.
The revised cover-top footprint is 1.139% against 1.207% in the photo, and
rivet crowns 75.742% against 67.702% (photo threshold sensitivity 59–76%).
Cover edges are still 13.688% against 2.157%; a broad gray rub is not a match
for intermittent thin chips. Narrow the contact lands and interrupt their
exposure along the full edge. Exposed phosphate remains the primary substrate;
reserve realistic high-reflectance steel for the sharp crests. Retain every
measurement rule and photograph outline while changing the authored masks.

## Look round 2 — pass 24, reject excessive grain contrast

Color/value first: inspected every native third-bake hero, shooter, macro and
ammunition comparison. The larger grain survives 2048, but phosphate has
become a coarse gray camouflage and the polymer relief is too deep under
raking light. This is a visible regression, not an acceptable dry finish.
Retain normalized fine roughness, reduce phosphate relief to 12 µm and bath
albedo variation to ±20%, and reduce normalized molding relief to 80 µm.
The sharp oblique reference shows a fine skin with localized handling marks,
not large height lumps across every steel part. Exposed phosphate at chips
needs a predominantly diffuse crystalline response; reduce its metallic mix
instead of whitening every edge. Keep rare steel at high crests.

## Look round 2 — pass 25, controlled native finish and area audit (rejected)

Color/value first: opened native `round2-final-fit/used_photo.png` and the
replacement paint-receiver view. The receiver now measures 1/35/66 against
0/35/68, H 79/82/88 against 81/83/85. The cover's 24/40/128 is within the
value corridor, but its blue highlight is 171 against 196: still a miss.
Use a slightly smoother satin cover film (.35), while retaining .42 receiver
paint and the same real 2.2% base reflectance. The handle's P90 is 155 against
186; restore an ordinary dielectric F0 through specular factor 1.0. The grip
73 median against 79 and its three highlight channels are already in range.

The barrel assembly mask included chamber/collar and protected surfaces under
the shield, while the photo outline included only the complete exposed front
bay. Retain the assembly numbers as a deliberately non-comparable diagnostic,
and compare the full bay beyond the authored front-bay split station Y=.545 m.
This is a geometry/observation correction, not a favorable color patch. Its
source triangles remain unchanged and its native coverage pair is retained.
The bipod's first-round median was close to its photo; the global phosphate
change unnecessarily darkened that separate finish. Restore its original
.044/.045/.042 bath color instead of forcing a brighter whole-gun light fit.

Opened the new cover coverage pair: 2.144% against 2.157% in the photograph.
Cover-top damage is 1.320% against 1.207%; rivets 73.822% against 67.702%,
inside the photo's 59–76% classification sensitivity. Receiver edges remain
10.502% against 5.222%; narrow those strips before the next canonical bake.
These are physical on/off-map footprints on the hero's actual visible parts;
final reports also retain the stricter actual rendered visibility fraction.


## Look round 2 — pass 26, native area and light audit

Color/value first: opened all ten native pass-12 GLB hero, shooter, macro and
finish views. Receiver, box, handguard and stock values and highlight RGB now
meet the requested limits under their respective physical light rigs. A floor
card beneath the forward bipod lights its exposed steel without washing the
painted receiver gray; the former whole-gun lighting solution is rejected.
The cover's bright tail still spreads too broadly: reduce only the cover film
roughness from .35 to .33, retaining its real 2.2% paint reflectance.

Opened every pass-12 wear-coverage pair. Cover-edge footprint is 2.172% versus
2.157%; top scratches 1.320% versus 1.207%; rivet crowns 71.728% versus
67.702%. Widen receiver strips about 19% from 4.364% toward 5.222%, reduce
scratch widths 5%, and slightly tighten the fractured rivet crown field.
The handle's 78.798%, regulator's 100% and butt's 13.407% cover too much
surface. Confine polish to the handle's upper contact band, carbon to the
regulator's forward discharge lip, and stock rub to heel/toe returns. Do not
spread soot to match the dark empty port in a photograph. Its threshold is an
appearance upper bound, not a carbon label. Narrow muzzle deposit and bottom
box scuffs. These comparisons use physical atlas changes; final rendered
visibility remains a separate, stricter measurement.

A newly cited manufacturer's studio photograph supplies the links' primary
finish target, with an unclipped paper neutral. Retain the old field-belt
comparison as an explicit secondary diagnostic. The link skin needs dry fine
roughness rather than a smooth silver reflection: restore .61 plus fine grain
while retaining the revised real steel reflectance. Cartridge brass and
copper/green-tip materials stay as accepted.


## Look round 2 — pass 27, reject coarse molding relief

Color/value first: opened both native pass-13 heroes and the shooter view.
Paint and front phosphate stay within a coherent dark material band under
this shared light. Cover scratches and sharp edge damage are readable in the
shooter view. However, narrowing handle polish exposes excessive molding
relief: the highlight becomes a white furry strip. The stock's raking-light
grain also reads too coarse beside the photographed fine molded skin.
Reject this regression before final controls. Reduce molding relief to 35 µm,
handle relief to 20 µm, fine relief to 5 µm and rubbed lands to 8 µm. Retain
roughness variation and original finite contact fields, rather than using
height exaggeration to make a grain statistic visible. Rerender the new bake;
no photograph supplies any texture.


## Look round 2 — pass 28, native final-bake checkpoint

Color/value first: opened the pass-14 hero, reverse hero and shooter view at
native resolution beside `used_whole.jpg` and `used_receiver.jpg`. The black
receiver retains body and broad satin reflection, the front conversion finish
is dark, and the polymer remains dark rather than mid-gray. Cover scratches
and worn return lines read in the shooter view. The 35-µm molding / 20-µm
handle relief reduces the furry reflection; coarse variation is now primarily
roughness, not deep height. Its final close pairs still need inspection after
the light fits. The accepted original cover geometry reflects a different
highlight shape from the reference's cylindrical pressing; this must remain
an explicit limitation of the reflection-profile comparison.

The intermediate pass-13 `make check` overlapped replacement of its atlas by
pass 14 and correctly rejected mismatched embedded-image hashes. This was an
invalid concurrent check, not a reason to relax verification. The complete
checks are rerun only after the canonical pass-14 export has exited normally.


## Look round 2 — pass 29, reject contaminated link observation

Color/value first: the new link photo's initial whole-part highlight statistic
was 169–172 despite the visibly matte black steel. Opened a native overlay:
the coarse polygon included white paper outside the curved cuff and lower
web. That is an invalid observation, not a bright steel target. Refined the
whole silhouette, including the actual dark necks and excluding background;
retain the same one-pixel erosion as every other photograph. No image values
or surface regions are selected by brightness. Both round-one and round-two
renders will be measured against this same corrected whole-part outline.
The physical-light fit for links must be rerun with that correction. The
old field-belt comparison remains separate and unchanged in scope.


## Look round 2 — pass 30, reject bright tail and coarse stock skin

Color/value first: opened all eight native final-bake photo renders and the
160 linear-light basis images on four diagnostic sheets. Eleven of twelve
finish roles pass their complete native value/highlight tests. The cover's
26/38/138 against 28/37/115 still fails P90. Its highlight RGB 174/179/183
against 175/184/196 now passes. The fitter's 2,200-pixel guide sample predicted
a lower P90; refit the actual full visible cover distribution rather than
accepting a favorable sample. Leave the real paint reflectance intact.

The stock close-up is still too pebbled beside the native `used_stock.jpg`.
Its roughness variation, not merely height, causes the coarse orange peel.
Reduce stock roughness variation from .22 to .07 and source relief from
35 µm to 5 µm, retaining its fine manufacturing skin. Its central raking-light
response must be reviewed on the new source and bake. Other moldings retain
their own accepted texture; no global grain wash is introduced. The field
ammunition fit now meets the value and highlight tolerances without changing
brass, copper or green tips. The studio link also passes with the corrected
whole silhouette; its old field-light diagnostic remains explicit.


## Look round 2 — pass 31, fine source-skin and sampling diagnosis

Color/value first: the complete linear-light prediction for the pass-14 cover
is 26.6/39.3/138.0, agreeing with the native Cycles 26/38/138. The sparse guide
sample, not denoising or image correction, caused the incorrect P90 forecast.
Use a denser fit and keep the final complete-part native histogram as the
acceptance test. Highlight RGB also agrees within two encoded levels.

The native box and handguard close-ups also expose the same overlarge orange
peel seen on the stock. Replace the shared exaggerated skin with separate
manufacturing inputs: 1800–2400 cycles/m, 2–6 µm source relief, roughness spans
.05–.14 (stock .07); rubber 12 µm. Grain becomes a fine microfinish rather
than large height/roughness lumps. Preview the source before the next full
bake and eleven controls. This is fine original shader noise, never a photo
projection or a texture imported from the reference.


## Look round 2 — pass 32, source preview and shipped molding skin

Color/value first: opened all four Eevee source previews and all three native
Cycles GLB molding comparisons. New baked handguard is 40/103/133 versus
38/102/135, stock 46/105/129 versus 48/111/129, box 25/47/68 versus 25/47/72;
each highlight RGB passes. Their broad hue is the photographed lighting cast,
not blue material input. The large orange peel is gone. Fine source grain
filters at the 2048 atlas density; the source does not justify claiming every
micrometer of relief survives. The matched GLB images, not source settings,
judge the remaining skin. The accepted molding contours remain unchanged.

The denser cover fit predicts 27/38/128 versus 28/37/115 and highlight RGB
173/178/181 versus 175/184/196. Rerender these physical fixtures on the new
export and measure every visible pixel before freezing the final comparisons.


## Look round 2 — pass 33, native cover rig frozen

Color/value first: opened native pass-15 `used_photo.png` and its three complete
part histogram pairs. Cover is 26/38/128 versus 28/37/115; highlight RGB is
173/178/181 versus 175/184/196. Grip is 46/75/103 versus 47/79/91, H
114/120/125 versus 116/122/130. Handle is 16/35/163 versus 16/35/188, H
193/197/199 versus 181/194/211. Each median, tail and highlight channel now
passes the requested limits on every visible part pixel. The real 2.2% paint
input is unchanged. The denser light fit fixes the tail without darkening its
base color or adjusting the rendered image. Freeze these parameters for the
canonical before/after run; keep the hem/cylinder highlight-width limitation
explicit in its profile pair.
