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

## Round-two region evidence (historical; superseded below)

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


## Round-three review

The lead now accepts the grip form, trigger, band guard, continuous rear frame
curve and extractor plate. The lead also corrects the prior enclosure request:
the left shroud opening is necessary and accepted in principle, provided it
stays narrow and the right wall hides the rod. The unresolved-enclosure text
above is the historical round-two finding, not the current requirement.

20. **Initial machined-form pass (`renders/round3/pass1/`).** Color/value first:
    the inspection steel remains cleaner and its white-card reflections brighter
    than the used photographs; neither is final albedo. The rib root and recessed
    crown improved, and moving the grip cavity cut after relaxation removed the
    torn voxel lip. Rejected the plate's rippled normals and the invisible fine
    teeth: smooth vertex normals averaged their pyramids into a blank roof.
    The first sweep also caught 0.269 mm of new spur-root/frame overlap.
21. **Surface correction (`renders/round3/pass2/`).** Recalculated plate normals
    and retained its actual planar cheek field; the plate now has a fine seam
    rather than a beveled step. Narrowed the spur's hidden root to clear the
    unchanged slot. Fine tooth facet normals reveal the original sub-millimeter
    field. Joined body and spur into one closed mesh; the triangular internal
    overlap no longer masquerades as an assembled hammer. The new local crown,
    passage, right-wall and solid-cheek gauges pass independently of serialization.
22. **Macro and photographic correction (`renders/round3/pass3/`, hammer pairs).**
    Color/value still limits the comparison; gray foam balances the rest photo,
    and the cocked photo's locally neutralized cheek retains mixed blue lighting.
    Rejected the first cameras' excessive roof visibility and cropped body.
    Lowered their angles and reframed. The pairs also exposed a shoulder step:
    raised the thumb roof's root into the rounded body and thinned its tip.
    The rear sight's thick U block needed a real thin blade/backing distinction,
    its elevation button needed a slot, and the front pin needed seated ends.
23. **Final construction correction (`renders/round3/pass4/` and final checkpoint).**
    Added the tapered shallow topstrap mortise under the sight tongue, rounded
    the hammer tip's transverse outline, and derived the spur cheek normals
    from its changing width rather than its tooth tips. The crown has a true
    recessed annular floor and protective lip. The crane's lower web, which made
    the dark hanging rectangle, now has a round boss and a tapered web behind
    the right forging bolster. No pivot, clip or clearance exception changes.

24. **Final hammer/blade cleanup.** The last macro still showed the old raised
    hammer forehead as a separate block above the spur. Lowered and rounded
    that upper contour into the continuous roof, retaining the nose and rest
    contact. Reallocated 100 triangles to the thin notch blade/backing and
    reseeded its normals after reduction to remove folded-looking highlights.

25. **Continuous hammer cage (`renders/round3/pass7/`).** The joined profile
    still made a visible shoulder in the cocked photo pair. Replaced it with
    one closed three-dimensional cage through body, rounded cheek rails, neck,
    curved thumb roof and thinning tip. The fine roof cells share the cage's
    perimeter vertices. Their face attribute confines flat tooth normals to the
    teeth, so the blank neck no longer inherits triangulated tooth shading.
    The trial passes Idle/CockHammer clearance and source/import gauges, and
    saves 188 triangles compared with the joined-profile revision. Final full
    sweeps and all images are regenerated from this cage.

## Current round-three region evidence and remaining photographic differences

All paths below are relative to `renders/checkpoint/`. These images show the
exported inspection GLB; separately labeled source pairs show the dense grip.
The temporary materials remain unbaked. The form is submitted for lead review.

1. **Hammer.** `hammer-pairs.jpg`, the two individual `hammer-pairs/` comparisons,
   `beauty/hammer_rest.png`, `hammer_cocked.png` and `hammer_top.png` show the
   rounded body, continuous back/up sweep, thinning tip and fine curved-top
   pyramids. Body and spur are one closed mesh on the original Hammer bone.
   Our roof is more regular, the visible neck fuller and its tip narrower than the used comparator;
   its machined cheeks are cleaner and more reflective. The pair cameras are
   explicitly estimated, with different source viewpoints; no pixel-perfect
   camera calibration or manufacturer checkering pitch is claimed.
2. **Frame side / slot / sideplate.** `beauty/star.png`, both rakes, `side.png`,
   `rear.png` and the frame sections show the continuous accepted back curve,
   solid side cheeks and internal top/rear hammer opening. The shield's release
   pocket starts ahead of a solid rear wall. The plate is cut from the forging's
   own skin, so its lower curved edge follows the frame instead of sitting on
   a proud slab. The remaining original plate outline is fuller than the photo.
   The deep ratchet-release well still reflects less evenly than the real steel.
3. **Barrel / rib / crown / lug / shroud.** `beauty/muzzle.png`, `lug_front.png`,
   `shank.png`, both side pairs and the shroud section show the blended rib root,
   deliberate flats, recessed crown and rounded integral lower nose. The narrow
   swing-side release remains open; the right side hides the rod. The former
   black rectangular projection was the crane's lower web and pivot. The web is
   tapered and its boss round, with a blended stationary right bolster; its real
   small bearing projection remains visible. The reference's lug has a slightly
   different rolled lower silhouette and the source photograph's reflections
   reveal machining absent from this checkpoint.
4. **Sights.** `beauty/rear_sight.png`, `sights.png`, `muzzle.png` and the aimed
   view show a thin notch blade, radiused backing, tapered forward body seated
   in a shallow topstrap mortise, slotted elevation/windage heads, and a curved
   front ramp with flared seated base and flush pin ends. The exact Eye and
   sight tops are retained. Our blade corners and plain black sight face remain
   original; the photo's colored insert, witness lines and fine serrations are
   omitted at this form gate.
5. **Thumb latch.** `beauty/latch.png`, `open.png` and the open photo pair show
   the contoured dish and fine thumb teeth, a clear screw land and a radiused
   backing. It stands proud of the steel side. The original pad outline
   is rounder than the photo and the teeth are more regular; no stamped logo or
   trademark is reproduced. Its accepted translation and pin engagement remain.
6. **Grip seam.** `beauty/grip_seam.png`, `star.png`, both grip macros and the
   three height sections retain the accepted silhouette, finger saddles and egg
   sections. The cavity is now cut with an unbroken outer forging envelope after
   the rubber's voxel relaxation, leaving a clean continuous molded lip instead
   of a torn edge. Some polygon economy is visible in this enlarged macro;
   the fine molded texture and parting-line finish are reserved for look-dev.
7. **Accepted trigger / guard / cylinder / star / ammunition / loader.** Both
   trigger pairs, `beauty/open.png`, `star.png`, `ammunition.jpg` and all 22 strips
   retain the accepted forms and motions. The round-three native comparison
   requires the entire cylinder, extractor plate, trigger and guard to match the
   round-two checkpoint exactly, as well as the rig, clips, sockets and ammo.
   Grip topology changes only to repair its cavity seam; the sculpt cage is the
   same. Fine chamber-face wear, headstamps and material response stay held.

## Round-three proof

- `make -C guns/revolver` completes successfully, including the full rebuild,
  source/import checks, independent rebuild, comparisons, sections and clips.
  `make -C guns/revolver check` also passes explicitly on this final generator.
  Logs are `build/round3-delivery-checkpoint.log` and
  `build/round3-explicit-check.log` at repository root.
- **39,734 staged / 31,080 active / 27,960 unloaded triangles**. Every hidden
  ammunition alternative and reload representation remains counted. This is
  916 more than the second checkpoint and within the unchanged 40,000 cap.
  The forging saves 200 triangles and the flush plate saves 80; the final
  continuous hammer saves 188 versus the joined-profile experiment.
- Primary regions: forging 3,500; sideplate 320; barrel/lug 2,200; hammer body
  and integrated spur 1,760 plus nose 108; grip 4,200; latch thumbpiece 674;
  rear leaf/blade/backing 196/400. Cylinder 6,068, extractor plate 750, trigger
  550 and guard 700 retain their round-two geometry exactly.
- Inspection GLB **2,472,184 bytes**, 123 named meshes, nine temporary materials
  and zero textures. The merged hammer removes one old mesh name. Ammunition
  and loader GLBs remain 18,788 / 15,516 / 163,880 bytes. No UV/bake acceptance
  or final material/draw-call claim is made at this checkpoint.
- The round-three baseline comparison preserves **170 native entries** and
  reports zero unexpected changes: all bones, sockets, clip keys, ammunition,
  loader, complete cylinder, extractor plate, trigger and guard. The separate
  forward-cylinder comparison also retains all 3,672 oriented triangles.

- All 123 source/import parts are closed/manifold, have positive volume and
  contain no zero-area triangles. Forging, barrel and cylinder have zero
  disjoint triangle crossings. All 48 independent actual-surface records pass.
- Full source sweep: **1,842 samples**; fresh-import sweep: **1,854 samples**.
  Maximum measured penetration is **0.095825 mm**, below the unchanged
  **0.20 mm** tolerance, with no allowed-pair exceptions. These establish
  sampled clearance; the separate affine comparison establishes serialization.
- Independent current rebuild: **187 entries**, zero differences. Full affine
  comparison: 1,842 poses, maximum position error **0.0000672 mm**, maximum
  linear-frame error **0.00000054**. All 32 bones, 22 clips, ten sockets,
  per-chamber semantics, interrupted resumes and endpoint holds pass.
- Actual source/import rays measure the crown recess at **1.450 mm**, swing-side
  passage at **3.500 mm**, plate-to-adjacent-cheek step at **0.026 mm**, hammer
  body at **7.435 mm** in an **8.009 mm** slot (about **0.287 mm** per cheek),
  and central cylinder-window lights of **0.441/0.454 mm**. Twelve side-cheek
  rays hit solid steel; the right shroud ray reaches its outer wall before the
  rod. These are measured triangle surfaces, not repeated design constants.

- `audit.json` passes **295 current-GLB PNG records**, all **22 decoded,
  correctly timed WebP clips**, three separately labeled dense-source pairs,
  five standalone views and the section provenance. Current GLB SHA-256:
  `3f298877e6be350976fb0b3dc604fa15bfabe0944c58be4fe6101d697d58168f`.
- Reviewed all 27 current beauty views, both hammer pairs, imported/source
  photo comparisons, both trigger pairs, all 15 sections, ammunition and aimed
  sheets, plus all 22 clip frame sheets. The longer reload/inspect sheets show
  the case rise/release, loader handoff, single insertion and full closing arc;
  short endpoint sheets retain the corresponding hammer/trigger holds.
- Hero object luminance p1/p50/p99: **9.93 / 52.00 / 246.93** of 255 across
  282,199 object pixels. **0.0450%** clips all channels; **1.857%** lies in deep
  shadow. This checks usable tonal range with dark cavities and controlled
  highlights; it does not accept final steel/rubber albedo or material response.

The review entry points are `contact-sheet.jpg`, `photo-pairs.jpg`,
`hammer-pairs.jpg`, `sections/sections.jpg`, `aimed-detail.jpg` and the named
macros above. Per-clip JPG/WebP files remain under `strips/`.

No kit, common module or other gun changes; no tools or installations are needed.
All generated images and binary assets remain ignored, and no docs JPGs are
committed before final acceptance. Look development remains held. The remaining
visual weaknesses are the fuller original hammer neck, rounder latch outline,
some low-poly economy at the enlarged rubber lip, and the less even reflection
inside the deep ratchet-release well. A future general kit fixture for rounded
profile normals and fine relief masks would help catch this class of shading
loss; no shared-tool change is required for the checkpoint.

## Last form revision and look development

The new brief accepts the prior dimensions, rig/22 clips/1.4.0 state contract,
48 construction records, cylinder and extractor, ammunition, rubber form/seam,
trigger and guard, sideplate seam, sights/latch and recessed crown. Their
acceptance is retained. The new native audit limits geometry changes to
`Frame_Forging`, `Frame_Sideplate`, `Barrel` and `Hammer_Body`; the sideplate is a
patch of the changed forging skin. Every other native entry remains identical.

26. **Form, first revised cage. Color/value first:** temporary steel remains
    more reflective and cleaner than the used photos. The new broad tongue and
    subdivision cheeks remove the wire spur and faceted wedge, but the first
    belly made a pointed dip above the guard, and the lower crane seat crossed
    the newly fuller forging. Rejected both (`renders/round4/form1/`). Replaced
    repeated eased stations with monotone tangent flow; relieved the crane's
    actual lower envelope. Kept the original yoke, pivot, contacts and tolerance.
27. **Form, machining cleanup. Color/value first:** white card bands made a
    small broad edge look worse than its silhouette. The small even rear radius
    reads correctly; the source's lower nose still had a squared reflection and
    microscopic split Boolean seams. Rolled it across the width, widened only
    the mouth's cutter break, welded its sub-4-micron seams and excluded the
    narrow crane-bearing pocket from the bevel miter. The crown gauge and rod
    release remain unchanged. Actual closed topology and disjoint-crossing
    checks pass; no collision exception was added.
28. **Form, photographic proportions. Color/value first:** neither the blue-lit
    cocked photo nor the clipped ATF backdrop supplies albedo. Rest/cocked
    comparisons showed that the first fuller tongue extended too far and had
    a bulbous tip. Shortened and tapered the same continuous cage. The actual
    source/import gauges are approximately 6.02/3.58 mm in side thickness,
    9.95 mm across and 16.02 mm beyond the defined frame gauge. The photographic
    estimates and their perspective uncertainty are recorded in REFERENCE.md.
    `renders/round4/final-hammer-pairs/` shows both poses; fine roof cuts are
    reserved for the normal bake rather than consuming silhouette triangles.

Current form differences, before judging finish:

- **Hammer:** rounded crescent cheeks, thicker rounded tongue and continuous
  roof replace the horn/wedge. Our underside is more concave and the thumb end
  more regular than the worn specimen; these are still visible in the pairs.
  There is no stepped separate spur or faceted cheek cap. Final baked pairs
  must also retain the curved roof checkering.
- **Rear frame:** a small continuous round follows the accepted rear curve.
  Our machined side land is flatter and cleaner than the photographed forging;
  the former wide planar chamfer is gone.
- **Bottom/front:** the guard joins the continuous belly into a rounded crane
  corner, and the stationary forging covers the accepted moving yoke. The lug
  nose is one compound rolled surface around the rod passage. The real open
  milling has a small visible mouth face; it no longer has a separately
  projecting lower block. The original corner remains fuller than the photo.
- **Window:** the recoil edge is narrower and the upper shoulders wrap the
  cylinder instead of showing a rectangular dark border. Central upper/lower
  actual running light remains about .443/.457 mm; the forcing-cone gap remains
  .200 mm. The left roof keeps its required swing relief, so the oblique left
  light is slightly broader than the right. No accepted motion is changed.

## Finish critiques

29. **Source pass 1 — `renders/look/pass1/`. Color/value first:** against the
    gray-paper-balanced used photograph, rubber texture/hand medians were
    about 20/32 versus 75/98. Rejected the nearly black blank grip and spotless
    steel. Added original molded cells with distinct smooth hand-contact fields,
    directional brushed/turned manufacture, fictional engravings and the named
    stop/holster/carbon sites. Reference pixels never enter the shaders.
30. **Source pass 2 — `renders/look/pass2/`. Color/value first:** rubber texture
    was still about 27 versus 75. The raised cells read in the macro but not
    sufficiently at full frame. Increased their resolved relief and kept the
    smooth web/finger crests dark. A direct emission-mask inspection in
    `renders/look/debug/` showed the causal fields were located correctly, but
    low carbon coverage averaged into gray steel. Raised deposit-core opacity
    while retaining broken localized haloes. The earlier barrel patch sampled
    the lower lug; corrected the anatomical patch rather than tuning to it.
31. **Source pass 3 — `renders/look/pass3/`. Color/value first:** barrel view
    value was about 163 versus 151, and hand polish about 90 versus 98. Rubber
    texture remained low; a new near fill also reflected directly in the steel
    cheek and washed it out. Rejected that lighting. Increased the rubber's
    actual textured reflectance, left hand contact darker, and moved/reduced
    the fill. Used-reference comparisons use a neutral room field; hero views
    retain negative fill and deep cavities. The gray-paper neutral is native
    (100,45)–(300,110), linear gains .98535/1.00245/1.01997.
32. **Source pass 4 — `renders/look/pass4/`. Color/value first:** lower fill
    still made the underside too white and the grip too gray. Reduced it again
    before delivery rendering; retained the material values and the small
    dark cavity range. The front-open view now exposes six localized carbon
    rings; the closed hero shows the stop line and muzzle contact. The hammer's
    dense source has continuous cheeks and fine crossed cuts over its roof.
    The next acceptance is the exported atlas, including projection loss,
    actual wear texels and tonal measurements, not this source scene.
