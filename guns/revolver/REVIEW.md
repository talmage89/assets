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

## Handoff checklist (superseded by the lead’s round-two rejection)

These were the previous author’s claims. The round-two brief rejects the frame,
barrel/shroud, hammer, blade thickness, guard, grip and extractor-plate form.
The accepted dimensions, cylinder machining, trigger direction, ammunition,
loader, rig, 22 clips, chamber supplement, Eye and construction checks remain
the baseline. The new image-based region list below replaces these checkboxes.

- [ ] Frame and seated sideplate: radiused forging, continuous rear curve,
  narrow reveal, screws and window thickness.
- [ ] Barrel, rounded full underlug and open-left ejector shroud: complete
  material gauge, bored crown and visible forcing cone.
- [x] Cylinder: six real openings, rounded flutes, rear stop notches and lead-ins.
- [ ] Crane, latch and star: supported bearings, thumbpiece, ratchet and actual
  rim-bearing extractor arms, open with the star extended.
- [ ] Hammer: separate pivoted body and widened swept spur; slot clears the
  full cocking arc.
- [ ] Trigger and cylinder stop: broad muzzle-facing concavity, forward toe,
  rest land, stop seated only after indexing/closing.
- [x] Sights: pinned ramp, adjustable leaf/notch and exact gray-backed Eye view.
- [ ] Grips: compound palm/backstrap sections and three finger saddles,
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


## Round-two visual review

Color/value first in every pass: the quick constant steel still has clean white-card
reflections and the rubber lacks grain. The ATF white backdrop is clipped and
constrains form only. Stephen Z’s gray paper and Dmoore5556’s gray foam supply
the recorded neutral balances. No finish/albedo acceptance is inferred here.

13. **Handoff rejected against its photographs.** Opened the requested side,
    left rake, sights, star, photographic sheet, section sheet and oblique trigger
    pair. The topstrap/backstrap had faceted stations, an unused hammer trough,
    generous rectangular window light and a separate front support step. The
    lower barrel was an open hook, the trigger blade and oval guard were thin,
    the grip had a straight rear/flat heel, and the star did not fill the webs.
14. **First volume pass (`renders/round2/pass1/`).** The backstrap curve, closer
    window, flat band and broad star improved the silhouettes, but the grip screw
    was buried, the shield’s normals rippled and the hammer trough remained too
    long. Measured the screw seat on the actual molded surface, replaced the
    rectangular hammer pocket with its swept body envelope, and corrected the
    shield field. The motion sweep rejected a latch overlap, the raised shield
    over the ratchet, early cylinder/topstrap interference and the longer rod tip.
    Local release pockets and the left topstrap chamfer repair those surfaces;
    no clip, contact exception or penetration tolerance changes.
15. **Second pass (`renders/round2/pass2/`).** Opened the changing egg sections,
    flat guard section, doubled blade depth, star plate and narrow hammer slot.
    The sweep passed idle/cocking/reload, but Boolean slivers and one crossed
    frame bevel failed topology. Manifold operations on the revised forging,
    barrel and spur avoid coincident cut seams. The crane heel is now part of
    the forging. Separate shallow checker passes avoid coplanar cutter floors.
16. **Third pass (`renders/round2/pass3/`).** Both grip rakes show the curved
    back, palm swell, deep finger saddles and upper wrap; the butt still looked
    cut off, so its source now has a longitudinal dome. The front lug macro
    exposed an angular cap and a triangular highlight fan. Rebuilt the barrel
    as a closed exterior plus independently bored cone/crown, with a rolled
    quarter-ellipse at the nose. A diagnostic red-rod render proved that the
    remaining left release exposes the rod; it cannot be called fully enclosed.
17. **Fourth pass (`renders/round2/pass4/`), rejected barrel shading.** Opened
    all seven views. The new cap and heel improved, but long faceted bands ran
    down the barrel. These are a shape/normal defect, not future machining.
    Replaced the upper polygon shoulder with a sampled circular sweep and
    derived side normals from its rounded outline, preserving actual side flats.
    The grip and hammer changes remain inside their original motion frames.

18. **Fifth pass (`renders/round2/pass5/`).** Color/value remains the same
    unbaked stainless/rubber limitation. Opened the regenerated left rake, nose
    and shield macro: the upper barrel now has continuous curved highlights
    alongside genuine machined flats, and the lower nose no longer has its
    former folded triangular cap. The deep ratchet-release well still has a
    less even reflected response than the photograph. Kept this limitation
    explicit. The left rod passage remains a form exception requiring review.

19. **Final side/open comparison.** Color/value first: the steel remains
    cleaner and brighter than the neutral-balanced used photograph. The full
    side pair exposed a spur-height error: its edge was nearly level with the
    topstrap, while the photograph puts it roughly 11 mm lower. Lowered and
    reshaped the spur/body and its swept slot, retaining the pivot and +35°
    cocking angle. The open-cylinder macro also showed wavy star-face normals;
    reseeded them and preserved its true axial planes. The plate’s geometry
    and extraction stroke remain unchanged. The final inspection pass is
    `renders/round2/pass6/`, followed by all current checkpoint images.

## Current region evidence and photographic differences

The final regenerated evidence is under `renders/checkpoint/`. These are form
submissions for the lead, not blanket acceptance. All stills use the imported
GLB; source comparisons are labeled separately. No docs JPGs are committed.

1. **Frame / sideplate.** `beauty/side.png`, `rake_right.png`, `rake_left.png`,
   `sights.png`, `recoil_shield.png` and the three frame sections show the swept
   rear radius, the filled unused trough, a narrow body-sized slot, closer window,
   integrated rounded crane heel and radiused boss around the firing bushing.
   The original sideplate and its screws retain their geometry. Our lower frame
   and plate outline remain fuller than the four-inch photograph; the left
   topstrap underside rises slightly to clear the real cylinder swing. The
   photographic shield has a less visibly regular machining response.
2. **Barrel / lug / shroud.** `beauty/lug_front.png`, `rake_left.png`, `front.png`
   and the underlug section show the rib, machined flats, narrow barrel-to-lug
   transition, round bore and rolled lower nose. **Still unresolved:** the
   3.5 mm left departure passage exposes part of the rod, rather than only its
   tip. A completely closed fixed tube intersects the accepted sideways rod
   path. The requested enclosure is not marked done; the current revision keeps
   the accepted swing and all-clear sweep, pending the lead’s decision.
3. **Cylinder / flutes / stop notches.** `beauty/open.png`, `rear.png` and the
   cylinder section retain the accepted chamber/flute/notch form. The only
   generator change is the larger extractor seat at the rear. The baseline
   comparison independently matches every one of the 3,672 triangles forward
   of that seat (Y > 41.05 mm). The six actual rim-floor/flush checks remain.
   Our bare face is cleaner and its flute spacing more regular than the used photo.
4. **Crane / latch / extractor star.** `beauty/star.png`, `open.png`, `reload.png`
   and the extractor section show a broad scalloped plate across the chamber
   webs, with a lip under each rim. All six cases rise on it. The accepted crane,
   latch, hub, ratchet and extraction timing are unchanged; the frame alone gains
   their local clearance relief. The plate outline remains original and more
   regular than the worn reference. The open comparator has seven chambers and a shorter rod; our longer
   forward rod leaves that fitted crop at its left edge. The independent open
   and star views show the complete assembly.
5. **Hammer.** `beauty/hammer_cocked.png`, `sights.png`, `rear.png` and the slot
   section show a 7.6 mm body in an approximately 8.0 mm slot, a wider curved spur,
   original diagonal checkering and a separate visible nose. The source/import
   gauges measure the cheek clearance; the full cocking arc passes. The spur’s
   contour is broader/flatter and its checkpoint checkering coarser than the
   photograph. Absolute photographic width is an estimate with foreshortening.
6. **Trigger / guard / stop.** Both `trigger-pairs/` images and the blade/guard
   sections show the deeper working blade, retained muzzle-facing concavity,
   forward toe, original pivot/pull, and flat 8.4 × 2.8 mm guard section with
   rounded edges. The source/import middle blade is about 6.11 mm deep instead
   of about 3 mm. The guard’s bow remains squarer than the photo and the blade
   tapers differently near the toe; its oblique working width now reads much
   closer. The accepted cylinder stop and its contact records are unchanged.
7. **Grip.** `beauty/grip.png`, `grip_left.png`, both full-gun rakes and the three
   height cuts show changing egg shapes, palm swell, deep finger saddles, a domed
   butt and a high rounded wrap over the steel backstrap. The upper saddle no
   longer ends in a diagonal metal step. Our palm and heel are fuller than the
   ATF service grip and the high web is more pronounced. Grain, mold seam and
   hand polish remain held for look development; those omissions do not excuse
   the former shape defects.
8. **Sights / ammunition / speedloader.** `beauty/sights.png`, `aimed.png`,
   `aimed-detail.jpg`, `ammunition.jpg` and the real-time strips retain the accepted
   sightline, original ammunition and loader. Eye remains approximately 650 mm
   behind the notch with no camera shift. Small ammunition macros still show
   the accepted radial economy; no fine headstamp or bake is claimed.

## Round-two proof

- `make -C guns/revolver`: full current checkpoint rebuild, including the
  independent factory-startup build, source/fresh-import checks, stills, pairs,
  sections, trigger comparisons, all 22 real-duration clips and provenance.
- `make -C guns/revolver check`: the explicit final command repeats repository,
  topology, source/import, independent rebuild, surface gauges and motion checks.
- **38,818 staged / 30,164 active / 27,044 unloaded triangles**, 394 fewer than
  the handoff in each comparison. All hidden ammunition, loader and single-round
  representations remain counted. Frame 3,700; grip 4,200; cylinder 6,068;
  barrel 2,200; star 750; guard 700; trigger 550; hammer body/nose/spur
  500/108/650. The broader extractor seat removes rear-face tessellation;
  the unchanged forward cylinder comparison guards its accepted machining.
- Main inspection GLB **2,314,420 bytes**; 124 named meshes, nine temporary
  materials, zero textures. Cartridge 520 triangles / 18,788 bytes; fired case
  456 / 15,516; loaded speedloader 5,398 / 163,880. The future atlas remains one
  2048 BaseColor/OpenGL Normal/ORM set; no UV, bake or finish acceptance here.
- All 124 source/import parts are closed/manifold, with positive volume and no
  zero-area triangles. Frame, barrel and cylinder have zero disjoint crossings.
  No clearance exception is added and the tolerance stays **0.20 mm**.
- Source clearance: **1,842** poses; imported clearance:
  **1,854** including import key boundaries. Maximum measured penetration is
  **0.08873 mm**, inside the unchanged 0.20 mm tolerance.
- All **48 actual-surface records** pass in both source and import: cone gap,
  chamber/bore alignment and sixteen bore rays, stop/notch and rocker support,
  six recessed rim seats and flush heads, crane/latch closure, trigger/hammer
  rests, optical tops/ray, all six extracting rims and loader supports.
- New independent source/import gauges measure hammer **7.600 mm** in a
  **7.995 mm** slot (about **0.198 mm** per cheek), guard
  **8.400 × 2.728 mm** at Y=40 mm and trigger
  **6.992 × 6.109 mm** at Z=10 mm. The window’s central top/bottom
  lights are **0.447/0.461 mm**. These are rays on triangles, not repeated constants.
- The handoff comparison passes **169 unchanged native entries**, including
  every bone, socket, clip, ammunition and loader part. All **3,672 cylinder
  triangles forward of Y=41.05 mm** match exactly; only the rear extractor
  seat changes. The independent current rebuild matches all **188 entries**.
  Native repeat digests compare geometry/ownership, not corner normals.
- Serialization tests retain 32 bones, 22 clips, ten sockets, 1.4.0 chamber
  semantics, five interrupted resumes and every visible-control endpoint hold.
  Full affine comparison covers **1,842 poses**; maximum position error is
  **0.0000672 mm**, maximum linear-frame error **0.00000054**.
  Standalone and single-round spawn frames pass independently.

The main evidence is `contact-sheet.jpg`, `photo-pairs.jpg`,
`source-photo-pairs.jpg`, `dimensions.jpg`, `sections/sections.jpg`,
`trigger-pairs/`, `aimed-detail.jpg`, `ammunition.jpg` and `clips.jpg`.
Individual dimensioned section panels accompany the combined sheet.
The still and playback audit passes **286 current-GLB PNG records** and all
**22 decoded, correctly timed clips** against GLB SHA-256
`fb1ce19f84884f6f2a0a789580c1518394b3bdd665ab3fd5da6fc1a007ecd666`.
It separately validates the three dense-source comparisons and five standalone
ammunition/loader renders. Visual review covers the 20 current beauty views,
both sets of photo pairs, both trigger pairs, all 15 section panels, aimed and
ammunition sheets, and all 22 playback strips (viewed as frame sheets).

On the hero object's 281,357 measured pixels, luminance p1/p50/p99 is
**10.65 / 51.29 / 247.93** on a 0–255 scale; **0.0384%** clips all channels
and **1.752%** lies in deep shadow. Cavities remain dark and the broad upper
highlights roll off. These are unbaked inspection constants: neither photographic
albedo nor final material response is accepted at this form checkpoint.

No kit or existing common/gun module changes in this revision. No revolver docs
JPGs are committed. No tool installation is needed. The lead needs to resolve
full shroud closure versus the accepted sideways rod exit; the current model
retains the narrow release and its remaining rod exposure. The deep ratchet-well
reflection, fuller original grip and coarse checkpoint hammer checkering remain
weaker than the photos. Look development stays held. A useful future kit feature
would preserve analytic normals on rounded machined outlines without flattening
curved shoulders, with an exported macro fixture to catch the lost highlights.
