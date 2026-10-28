# Meridian Six — form and motion checkpoint review

Look development has not started. All renders in this review use temporary constant
materials. Photographs only enter comparison tools, never the model or shaders.
The report distinguishes assembly correctness, serialization and visual review.
The author's checklist is a submission for the lead's review, not lead acceptance.

## Critique history

1. **Primary volumes, rejected.** Color/value calibration is unavailable in
   Workbench clay; judged highlight bands and cavity values first. Opened all
   five images in `renders/pass1/`. The underlug was a tall flat slab, the lower
   grip ended in a sharp heel, finger saddles were nearly invisible, and the
   crane pivot appeared unsupported. The trigger's working face did curve
   toward the muzzle, but this did not redeem the rest. Replaced the lug with
   a rounded lower section, increased resolved finger-saddle stations and
   added a real frame bearing/support. The first 65,145-triangle assembly was
   rejected; duplicated ammunition and Boolean tessellation were major costs.
2. **Compound grip and swept construction, rejected.** Clay values revealed
   improved changing grip sections and a rounder lower barrel, in all five
   `renders/pass2/` images. The grip's upper rectangular seat exposed a gap;
   the lower lug still lacked a coherent longitudinal shroud. More seriously,
   topology inspection found microscopic Boolean seams, degenerate triangles
   and ineffective reduction. Cleaned in millimeter space and rebuilt the
   barrel as one analytic bored skin instead of overlapping tube unions.
   Recessed the grip against the actual forging and remeshed its dense cavity.
3. **Topology and independent contacts.** Began with clay value discontinuities:
   `renders/pass3/` showed broken barrel normals and a stepped rear grip seam.
   These were geometry/normal problems, not deferred material work. Replaced
   the barrel's remaining overlap construction with a continuous rib/lug/bore
   mesh and one open-left milling cut. Checked every part for closed manifold
   topology and positive volume. Actual rays measured the cone gap and bore
   center; required contacts passed before the motion sweep. The sweep then
   rejected case flight before mouths cleared, premature stop return, an
   obstructed latch stroke, and a yoke/barrel corner collision. Each repair
   changed the actual path or surface. No collision pair was skipped and no
   penetration threshold was increased.
4. **Cycles and exported mechanism.** Color/value first: the quick stainless
   reflects broad white cards too uniformly and the rubber lacks molded
   texture. Neither is finish accepted. Opened all five `renders/pass4/`
   exported-GLB images, including both raking views and exact Eye against gray.
   The rounded barrel, grip saddles, broad trigger and deep window read, but
   the initial raking cameras clipped the gun; widened them. The star originally
   missed the rims despite nearest-distance contacts. Rebuilt its recess and
   arms so its rear bearing plane reaches the rims' forward faces. Added six
   actual extraction-support checks and six loader retention checks. The loader
   release's zero-scale parent also failed round trip; it now rides a nonscaling
   guide with separate STEP visibility. Intermediate affine testing then passed.
5. **Photographic comparison and macros.** Color/value first: the declared
   ATF white patch was later found clipped; Stephen Z gray paper shows used steel and
   textured grips; ours remains a uniform inspection finish. Opened the three
   `renders/pair-trial/pairs/` images, both trigger pairs and all ammunition
   macros. Rejected an unconstrained camera below the right-side gun and the
   weak six-inch left-photo direction fit. Added height priors; the left fit
   now includes explicitly virtual six-inch class anchors, while our actual
   barrel remains four inches. The open phone photograph retains its measured
   EXIF 26 mm equivalent lens, and its larger residual stays visible. The
   frame's rear was too straight and triangular beside the curved class spine;
   rebuilt that upper contour with changing forging sections. The loader's
   cap/pockets had stale interpolated normals and the live case's automatic
   cap hid its primer. Reseeded machining normals and opened the primer seat.
   Increased case rims/mouths to 24 sides, paying with smaller hidden bullet
   sections and small hardware. None of these defects is called future wear.


6. **Final controls and independent surface audit.** Constant inspection values
   remain unchanged; no finish acceptance is inferred. Single action initially
   returned the trigger fully forward after cocking. It now holds a partly
   rearward trigger and uses a shorter additional SA pull. Replaced the stop's
   sliding placeholder with an offset rocker, bored bearing and supported pin;
   relieved its whole swept path and lengthened the cylinder's notch. Rejected
   pin/lever interference and thin frame-pocket bevel collapse. A separate BVH
   test then found overlapping frame miters despite closed manifold topology.
   Restricted bevel weights to edges with sufficient surrounding clearance and
   left the hidden intersecting stop pockets out of the bevel operation. The
   frame's broad forging radii remain explicit loft sections. The final frame
   has zero disjoint triangle intersections, now checked in source and import.
   A pre-bevel closed molding solid also prevents bevel miters from corrupting
   the grip cavity. Added an immediate empty-part assertion after finalization.
   These fixes preserve the same 0.20 mm motion tolerance and no contact skips.


7. **Machining highlight correction.** Opened the regenerated hero, both side
   orthos and top view. Values again showed constant chrome rather than a used
   satin finish, but a separate defect could not be deferred: triangular
   highlight patches crossed nominally planar cheek lands, and the cylinder's
   rim response looked uneven. Rebuilt the frame's split normals from actual
   coplanar cheek faces, carrying those normals across their adjacent edge
   breaks. Used analytic radial normals on the cylinder's true outer skin and
   axial normals on genuine barrel/cylinder end faces. This changes shading,
   not the measured dimensions or motion. Regenerated the complete evidence
   and reran raw GLB normals, source/import surfaces and clearance checks.


8. **Recess depth, rejected contact-only proof.** In the open/star views the
   cartridge rims stood proud of the cylinder. Inspection confirmed the
   counterbore step had been placed at the rear face, leaving zero depth inside
   the solid. A nearest-distance seat test could pass that wrong construction.
   Cut six genuine 1.40 mm-deep rim recesses, moved the cartridge bases flush
   with the rear face, and moved the extractor bearing web into the matching
   deeper star recess. Extended the loader's retaining fingers without moving
   its body into the ratchet. Placed the flute axes between chamber axes so the
   mill relief acts in the thicker webs, and snapped mathematical zero-axis
   coordinates before Boolean operations to eliminate microscopic coplanar
   failures. Each chamber now has separate measured rim/floor
   coincidence, recess depth and rear-head flushness evidence, in both source
   and fresh import. This changes construction and visible loaded-cylinder form;
   previous photographs are superseded by the regenerated final set.


9. **Barrel / shroud proportion.** Returned to the neutral-balanced four-inch
   ATF photograph before accepting the final pairs. Value bands showed that
   the original lower rounded lug was nearly as wide as the barrel, reading as
   two stacked tubes. Reduced the lower outside radius from 8.9 to 5.7 mm while
   retaining the actual 3.8 mm round-root rod channel. Common tangent sides join
   the barrel and lower curve, replacing the pinched twin-circle waist and its
   folded cap. Its minimum lower wall is
   now 1.9 mm, the full underlug remains continuous to the muzzle, and the
   barrel/rib/lug envelope is 33.9 mm high instead of 37.1 mm. This is an authored
   photographic proportion correction, not a published product measurement.


10. **Bore roundness from the section sheet.** Opened all final stills, both
    sets of three photographic pairs, both trigger pairs and the section sheet.
    Started with the same uniform inspection values; final steel/rubber finish
    remains unaccepted. The barrel section exposed long inner-bore chords at
    the straight web/rib transitions. A centerline test proved alignment while
    missing this wrong shape. Resampled those polar transitions and added
    sixteen independent radial surface rays with an 0.08 mm radius tolerance.
    Regenerated the complete evidence set after the correction.


11. **Rear hammer housing.** The rear macro showed an unnecessarily long open
    trough behind the hammer. Shortened the machining slot to the actual
    hammer-body envelope; the rear forging now closes that unused void. Kept
    the hammer's complete cocking arc, grip fit, Eye ray and all contacts under
    the same source/import clearance checks. The spur is still our broader,
    flatter original contour rather than the reference's serrated sweep.


12. **Flute-end and loader cap highlights.** The full-frame review still showed
    angular flute-end highlights. Replaced the short conical end approximation
    with hemispherical cutter ends, and derived their split normals from the
    actual swept cutter axis. This spends the reserved cylinder allocation on
    changing curvature rather than decorative microgeometry. Flattened the
    loader's actual cap normals and traded 100 body triangles for a smoother
    push-button silhouette. Total staged budget remains below 40,000.

## Photographs, white balance and fit limits

`src/prepare_refs.py` writes comparison-only neutral balances, with the exact
patches, original medians and gains in `build/references/whitebalance.json`.
ATF's white photographic backdrop is clipped at RGB 255/255/255. Its unity
gains cannot recover chromatic balance, so that pair and its trigger crop are
used for form only. No material hue/value acceptance comes from that photo.
Both Stephen Z photos use unclipped gray paper;
Dmoore5556's open photo uses the gray foam above the gun. The blue-lit Spencer
Dutch macro backdrop can remove a global cast, but directional blue reflection
remains. The dark target-macro photograph has no reliable neutral and is used
only for construction, never quantitative color matching.

Camera residuals measure estimated correspondence, not form quality. The left
reference has a six-inch barrel and wood target grip; two virtual class anchors
set its barrel direction without extending our four-inch geometry. The open
reference has seven chambers and different grips; our empty six-chamber pose
exposes the star. Its camera is constrained by the original iPhone 11 EXIF:
4.25 mm focal length / 26 mm equivalent, f/1.8. The mismatches are retained,
not removed by changing model dimensions to a photograph's projection.

## Image-based form acceptance list

Every item below was checked in the regenerated images. These are author
form/motion checkpoint checks, submitted for lead review; they do not accept
the temporary finish or replace the differences recorded below.

- [x] Frame and seated sideplate: radiused forging, continuous rear curve,
  narrow reveal, screws and window thickness.
- [x] Barrel, rounded full underlug and open-left ejector shroud: complete
  material gauge, bored crown and visible forcing cone.
- [x] Cylinder: six real openings, rounded flutes, rear stop notches and lead-ins.
- [x] Crane, latch and star: supported bearings, thumbpiece, ratchet and actual
  rim-bearing extractor arms, open with the star extended.
- [x] Hammer: separate pivoted body and widened swept spur; slot clears the
  full cocking arc.
- [x] Trigger and cylinder stop: broad muzzle-facing concavity, forward toe,
  rest land, stop seated only after indexing/closing.
- [x] Sights: pinned ramp, adjustable leaf/notch and exact gray-backed Eye view.
- [x] Grips: compound palm/backstrap sections and three finger saddles,
  rounded butt and fitted upper saddle.
- [x] Ammunition and speedloader: open fired mouth, visible primer, separate
  retained loader rounds and push-release handoff.

## Checkpoint scope and deliberate omissions

Fine grip stipple, hammer checkering, headstamp and maker/model engraving,
brush/turn direction, used-service carbon, stop track, holster polish and hand
shine belong to the subsequent authorized normal/material bake. They are not
presented as finished here. The planned sites are named in `REFERENCE.md`.
There is no UV, baked atlas, wear or final delivery acceptance at this gate.

The rig is a visual game assembly: no functional lockwork, internal springs,
physical hand rig, ballistics or simulated cartridge dynamics. Ejected cases
have an authored collision-cleared flight; a game can replace them with physics
at the release event. Arbitrary chamber bookkeeping belongs to the consumer;
the canonical sequential clips and their endpoint holds demonstrate six shots.


## Final region evidence and remaining differences

All paths below are relative to `renders/checkpoint/`. Opened every still and
all 261 strip frames, including all endpoint holds, after the final rebuild.
The photographic sheets include both the imported GLB and the dense-grip source.
Color/value first: gray-paper and gray-foam balances are recorded; our constant
metal has broader, cleaner white-card reflections and our rubber lacks the
photographs' grain and hand shine. These values are inspection lighting, not
accepted satin steel or rubber albedo. The clipped ATF background establishes
no chromatic calibration; that image is used only for form.

1. **Frame and sideplate.** `beauty/side.png`, `beauty/left.png`, both raking
   views and `pairs/right_photo-pair.jpg` show the continuous rear curve,
   substantial window rails, seated plate/reveal and three screws. The rear
   macro also shows the closed unused part of the hammer housing. Our lower
   belly and sideplate are broader and more angular than the photographs;
   these are retained original contours. The reference's smaller radiused
   transitions and used machining response remain the softer-looking finish.
2. **Barrel, underlug and shroud.** `beauty/rake_left.png`, `beauty/front.png`
   and the shroud panel in `sections/sections.jpg` show a single continuous
   rounded/tangent body, complete open-left rod channel and circular bore.
   Its measured envelope is 20.00 by 33.90 mm; the 1.9 mm lower wall is an
   authored nominal gauge. The reference has a rounder lower-side transition;
   our straighter web is an intentional full-lug contour. The nose still needs
   the planned directional machining and narrow holster polish.
3. **Cylinder and flutes.** `beauty/rear.png`, `beauty/open.png` and the cylinder
   section show six chambers, flutes between their axes, rounded cutter ends,
   stop notches and approach cuts. The former triangular flute highlights are
   gone in the final raking/rear views. Actual rim floors are 1.400 mm deep,
   with flush cartridge heads. Our scallops are more uniform than the worn
   reference and the bare rear-face response is too clean; stop track and
   carbon are absent at this gate.
4. **Crane, latch and star.** `beauty/open.png`, `beauty/star.png`,
   `beauty/reload.png` and the Reload strip show the supported pivot/yoke,
   wide thumbpiece, star, hub, ratchet and rod. Extended star arms bear on all
   six rims; the loader retains all six incoming heads. The open photo has
   seven chambers, a differently shaped latch and a different crane opening.
   Our cylinder hangs farther left/down. Its 84.9 px camera residual and
   narrower apparent rear face limit that pair's authority; the independent
   open/star views and surface checks carry the assembly evidence.
5. **Hammer.** `beauty/rear.png`, `beauty/sights.png` and the CockHammer/
   FireSingle strips show a broad forged body, changing spur section and full
   cocking travel, with the unused rear trough filled. Our spur is wider and
   flatter than the reference's upward serrated sweep. Coarse ridges exist;
   fine checkering remains for the normal bake. The rest seat is independently
   measured rather than inferred from animation preservation.
6. **Trigger and cylinder stop.** Both `trigger-pairs/` images and
   `beauty/trigger_quarter.png` show muzzle-facing concavity, a forward toe and
   a substantial blade. Our stem is slimmer and guard squarer than the photos.
   The sharper oblique photo is the better blade-width reference; the ATF
   side crop has limited pixels and supplies no finish calibration. The strips
   show stop retraction before indexing and seating before firing/after closing,
   plus the cocked trigger hold and shorter SA pull. Actual notch-roof/stop-top
   rays and the bearing/pin checks establish seating.
7. **Sights.** `beauty/sights.png` and `aimed-detail.jpg` show the pinned ramp,
   adjustable rear leaf/notch, adjustment heads and exact gray-backed Eye view.
   The blade is centered and level; topstrap and cylinder remain below it. No
   camera rise, geometry hiding or pose shift is used. Our plain black front
   blade omits the real reference's colored insert, and our rear body is more
   square. Eye is 649.40 mm behind the near edge of the notch; its 650 mm center
   distance follows the cited 800 mm eye-to-front-sight baseline.
8. **Grips.** `beauty/grip.png`, both raking views and the three horizontal plus
   longitudinal sections show changing palm/backstrap volume and three finger
   saddles, rather than a beveled side extrusion. Actual section widths/depths
   are 33.19/51.95, 33.33/49.28 and 28.89/41.10 mm. Our butt is flatter and the
   lower grip longer-looking than the service photograph. The molded grain,
   parting seam and polished hand-contact crests are still absent.
9. **Ammunition and speedloader.** All five `ammo/` images and `ammunition.jpg`
   show the separate primer, soft-point jacket/nose, open fired mouth, struck
   cup, six-pocket loader and broad push release. Final cap highlights are
   planar and the button silhouette is smoother. The rims/mouths still reveal
   their 24-sided economy in these deliberately enlarged macros. Fine fictional
   headstamp, case-mouth/primer detail and used surface response await baking.
   Free cases follow one authored clearance path; no hand rig or independent
   case physics is supplied. The release event exposes individual spawn frames.

## Final checkpoint proof

- `make -C guns/revolver`: complete checkpoint passed, including the independent
  rebuild, source/import checks, all presentation stages and image provenance.
- `make -C guns/revolver check`: passed again on the final generator. All 129
  named mesh parts are closed/manifold with positive volume and no zero-area
  faces. Frame, barrel and cylinder each have zero disjoint triangle crossings
  in source and fresh import. No kit file or existing common/gun file changed.
- 39,212 staged triangles, including every hidden ammunition alternative,
  loader and single-round display; 30,558 active loaded-gun triangles and 27,438
  unloaded-gun triangles. Cylinder 6,974; grip 3,998; frame 2,600; barrel 2,800.
  Nine temporary materials, zero textures. Planned final delivery remains one
  shared 2048 BaseColor/Normal/ORM set, approximately 16 MB compressed with mips.
- Inspection GLBs: revolver 2,275,972 bytes; cartridge 520 triangles / 18,788
  bytes; fired case 456 / 15,516; loaded speedloader 5,398 / 163,880.
- 32 bones, 22 clips, ten sockets. Independent semantics cover 1,842 half-frame
  poses, six physical chamber IDs and five interrupted/resumed reload poses.
  Every visible control endpoint joins its documented idle hold. Full affine
  comparison covers those same 1,842 poses; maximum position error is below
  0.0001 mm. Standalone and single-round spawn frames also pass.
- Source clearance: 1,842 sampled poses; imported clearance: 1,854 including
  imported key boundaries. Maximum measured penetration is 0.18811 mm against
  0.20 mm tolerance, with no allowed-contact exceptions. This proves sampled
  cross-bone clearance; serialization is checked separately.
- Forty-eight independent surface-evidence records include actual cone gaps
  of 0.2004–0.2010 mm, six rim floors and flush heads, extractor/loader supports,
  crane/latch closure, rest stops and the unobstructed Eye ray. Sixteen bore
  rays measure 4.5178–4.5198 mm radius. These are evaluated mesh measurements.
- The independent repeat build matches 193 entries: native positions,
  connectivity, ownership/material IDs, rest rig, socket frames and exact
  animation keys. The repeat digest does not claim to compare corner normals.
- `audit.json`: 282 current-GLB PNG records, all 22 correctly timed WebP loops,
  plus independent source/ammunition/section hashes. Hero object luminance
  p1/p50/p99 is 11.65/47.58/247.93 of 255; 1.56% deep shadow and 0.0275% fully
  clipped pixels. This checks tonal range, not photographic finish.

The main sheets are `contact-sheet.jpg`, `dimensions.jpg`, `sections/sections.jpg`,
`photo-pairs.jpg`, `source-photo-pairs.jpg`, `aimed-detail.jpg`, `ammunition.jpg`
and `clips.jpg`. Each clip has its own readable JPG and real-duration WebP under
`strips/`. No documentation JPG is committed at this checkpoint.

Only form review is needed from the lead. Look development, UV/bake acceptance,
causal service wear and final consolidated delivery remain deliberately held.
A useful future kit addition would be reusable recess-depth, bore-roundness and
self-intersection audits; this asset currently keeps those checks local.
