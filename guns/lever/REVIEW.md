# Bracken L20 — form, motion and finish review

The opening sections preserve the earlier form checkpoint. The current
finish critiques and delivery proof are at the end under **Look round 3**;
earlier finish acceptance is historical and was superseded by the lead's
second-round rejection.

This is the requested stop **before look-dev**. Inspection colors are constant;
the walnut has no grain or dings and the steel has no wear. This review does
not accept their final appearance. The source is an original visual game asset
with deliberately incomplete internals, rather than a mechanically functional
reproduction. Published dimensions and authored animation estimates are kept
separate in [README.md](README.md) and [refs/SOURCES.md](refs/SOURCES.md).

## Reference treatment

The lower carbine in Hmaag's CC0 right photo is the main straight-grip .30-30
proportion reference. The upper long rifle is excluded. Cjp24's sharp left
profile/close-up is a different .375 variant; it constrains construction and
viewing angle, not its checkering, finish or exact stock contour. Hmaag's
`receiver.jpg` really shows the action open. `open.jpg` and `open2.jpg` are
closed oblique action views despite their cache names. No photo is mirrored.

Every paired photo is adapted in linear RGB before composition. The right
photo uses unclipped white paper below the lower gun. The left profile uses
a bright bare screw-slot facet; the open-action photo uses a polished pivot
screw facet. The oblique left uses a polished cross-pin highlight, and the
right/top reference uses a broad bare bolt flat. Native rectangles, gains,
valid pixel counts and marked originals are in
`build/white-balanced/corrections.json` and `*-neutral.jpg`.

The small silver facets reflect their surroundings. They are estimated
neutrals, with remaining cast visible in the photographs, not measured gray
cards. No albedo is recovered from them at this gate. In particular the old
steel's residual blue is not copied into our steel. Later finish acceptance
needs additional neutrals and used-surface value measurements.

`kit/photo_match.py` fits comparison cameras from manually selected anatomical
landmarks, without supplying geometry to the model generator. A narrow prior
on estimated camera height prevents the planar side landmarks from inventing
a very low right camera or an overly elevated open-action view. These are
estimated views, not recovered EXIF. Lens, residuals, projection overlays and
height assumptions are retained in `build/cameras.json` and the calibration
JPGs beside the pairs. Different original contours prevent exact registration.

## Image critique history

The early previews remain ignored under `renders/pass1/` through `pass6/`.
They document rejected iterations, not final delivery. Each pass began by
looking at value/color before construction and silhouette.

1. **Initial form.** Against the native Commons references, the furniture
   looked pale and the steel too uniformly bright. Quick colors were darkened
   and the lighting kept neutral. The first assembly exceeded the triangle
   ceiling and had unsupported/overlapping linkage and feed parts. Those were
   rejected. Hidden tube rounds were simplified, screws budgeted, and cavities,
   real bearing bores, lock seats and supported linkage built before proceeding.
   Inspection sheet: `build/lever-pass1-sheet.jpg`.
2. **Machined planes and proportions.** Value remained provisional. The
   receiver's large flat faces showed triangular highlight fans; the body was
   too long and the forend too short beside the photos. Broad plane normals
   were corrected, the receiver rear moved to its current shorter envelope,
   and the compound forend lengthened. A box-like butt return was replaced by
   a genuinely curved steel plate seated against the wood. Inspection sheet:
   `build/lever-pass2-sheet.jpg`.
3. **Construction at first-person scale.** The dark cavity/readable edge
   balance was improved, but the stock head still read as an open wooden
   trough, and the upper tang was too broad behind the wrist. The tang was
   narrowed aft, the unnecessary deep mortise removed and clearance cut from
   an envelope of our own moving hammer. Bands were fitted to actual sections,
   rather than merely placed around nominal radii. Native images are in
   `renders/pass3/`.
4. **Rejected forward-hammer trial.** Quick values were stable. Moving the
   hammer forward reduced the opening but made its base clash with the carrier
   bearing and sear arm. The sweep rejected that trial even though the static
   contact assertions passed. The image still showed an oversized spur and
   exposed trough. It was not accepted. `renders/pass4/hammer.png` and
   `stock.png` show the trial.
5. **Shorter forged hammer.** The thumb pad remained too bright/plain for a
   finished gun, which is deferred. The shape was shortened and the internal
   pivot raised; the sear support was rerouted. The stock slot became smaller,
   but the tang lay below the head's surface. Its forward path was raised to
   follow that surface. A real bolt passage and broader front rails replaced
   the interpenetrating front. `build/lever-pass5-sheet.jpg` and
   `renders/pass6/hammer.png` expose the difference.
6. **Calibrated photographic review.** The paired right/left/open images
   exposed the trigger's overly hooked toe and heavy blade. Its curve was
   softened and width/thickness reduced while retaining the muzzle-facing
   concavity. The first camera solution showed too much top surface in the
   open view; camera-height priors now keep the comparisons closer to the
   photographs. The lower link, original lock relief and demonstration feed
   remain visibly simpler than the class's hidden mechanism; they are recorded
   as visual design limitations below. The hammer now has separately supported
   full-cock and half-cock lands. Its bolt-overtravel pose remains depressed
   until the returning bolt is clear, rather than intersecting the pin tail.
7. **Ammunition macros and inspection contrast.** The standalone white floor
   and exposure washed out brass, so the macros now use a transparent surround
   and lower exposure; the sheets composite them onto neutral gray. Large
   triangular case highlights revealed that registration discarded the
   analytic revolution normals. Those normals are now applied after
   registration. The head face also concealed the struck primer: a round
   shallow seat and a denser primer face expose its actual dent. Independent
   imported-surface rays measure a 0.22 mm dent with 0.07 mm axial thickness
   behind its center. The visible case-seat rings were increased without
   changing the eight-sided occluded tube variants. The finished checkpoint
   remains below 40k triangles. Workbench strips now have enough contrast to
   read the complete gun and flying case against their gray surround.

8. **Empty-cycle dependency.** Final clip inspection caught that the empty
   branch skipped the carrier lift. It now follows the same cam stroke as a
   loaded cycle, including the last-case and empty demonstration clips. An
   independent pose assertion checks the raised carrier even with no round.

9. **Tang seating from the final sections.** The earlier wide tongue was
   supported at its center but overhung the round wrist at its edges. The aft
   tongue is now narrower and nearly flush, broadening only into the head; a
   changing carved crown supplies its actual inlet land. Eight underside-land
   surface probes check both edges through the wrist/head instead of inferring
   support from one minimum distance. A buried fork connects the narrow rear
   tongue to both receiver cheeks below the race; a slotted retention screw
   seats on the tongue. Every disconnected tang component must independently
   meet the receiver, so a decorative floating rear plate cannot pass. The
   stock remains a compound cage.
10. **Closed cuts and normal-field polish.** The inlet now uses our unrelieved
    tang solid with a 0.03 mm outward normal offset, rather than scaling a
    hollow part and enlarging its voids. Distinct stock/steel race floors avoid
    coplanar cuts. Concave Boolean polygons are ear-clipped before reduction;
    only zero-volume triangle fins with two boundary edges and one overfull
    edge are pruned. Source and reduced stock/tang remain closed at each stage.
    The reduced wood receives the retained cage's smooth vertex-normal field,
    without adding triangles or textures. The tang's machined horizontal cap
    has a flat normal field. These remove the triangular highlight fans visible
    in `renders/pass10/`; `renders/pass11/` shows the correction.

Final checkpoint inspection, region acceptance and measured proof follow below.

## Form review — round two

The first checkpoint's self-acceptance was too lenient. The owner's second
brief accepted the dimensions, rig/37 clips, interface, contacts/clearance,
forend/bands, front sight, aimed alignment and trigger direction; the other
forms were rejected. This table replaces the earlier region judgments.
It records the revised forms and their remaining photographic differences;
final form acceptance belongs to the lead. Paths are under `renders/checkpoint/`.

| Region | Revised form, images and remaining difference |
| --- | --- |
| Receiver and loading gate | `views/receiver.png`, `receiver_left.png`, `receiver_raking_right.png`, `receiver_raking_left.png`, `raking.jpg`, right/left/open pairs. Flat cheeks now have longitudinal corner rolls, a raised rear lower heel, an action belly and a rounded front barrel/tube ring. The top opening surrounds the separate bolt, flush with its rails. The 0.9 mm spring cover is 0.05 mm inside the side plane, with its rounded front and rear screw. Our screw pattern remains original, the front ring taller and the gate longer than the small right/top reference. The gate opening retains the clearance needed by the accepted insertion path. |
| Lever | `views/lever_open.png`, `lever-stroke.jpg`, `pairs/open_photo-pair.jpg`, `lever_rest_photo-pair.jpg`. One continuous forging replaces the intersecting ellipse/spine/hook bars. Actual opening 104 × 29 mm, bar 2.2 × 8.2 mm, 0.28 mm perimeter roll. Orthographic rest/40°/80° views retain its full length and mid-plane. The calibrated open photograph estimates 105 × 32 mm and 2.1 mm side depth; ours is slightly narrower. The closed oblique reference recovers a substantially smaller loop, approximately 72 × 18 mm. It does not establish the same lever/camera calibration as the open photo. We used the open view for length and retain that closed-view mismatch explicitly. Our S web is cleaner and its throat sits higher than the photographed dropping-link assembly. |
| Tangs and wrist | `sections.jpg`, `views/hammer.png`, `wrist_under.png`, both raking views. Both tongues follow actual walnut surfaces and are inletted through the original outer envelope; the section plot includes measured pre-inlet wood in gray. Their edges no longer stand on the wood. A real shank and bored path pass through both tangs and the wrist. Measured radial shaft/wood clearance is 0.05 mm. The head mortise is larger than the reference because it clears the already accepted 90° visual hammer overtravel; its buried fork remains an original visual construction. |
| Bolt, locking block and carrier | `views/open.png`, `open_left.png`, open pair and Cycle strips. Accepted geometry and motion are retained. Our forked lock, carrier web and exposed link remain simplified visual internals, with the previously documented occluded feeding handoffs. The photograph cannot establish their hidden cam paths. |
| Hammer | `views/hammer.png`, `pairs/hammer_photo-pair.jpg`, `hammer-trigger-pairs.jpg`, HammerSafe/Cock strips. Curved volumetric body and returning spur replace the block/hook. The crowned 20 × 12 mm thumb table has 1.0 mm checkering and lies at a measured 13° when cocked, against approximately 12.9° recovered from the sharp photo. Pivot, 44° cocking pose and all clip keys are retained. Our table is more rectangular and its modeled diamonds more pronounced than the worn reference; pitch is an authored class estimate. The source remains a remeshed compound forging. |
| Trigger | `views/trigger.png`, `trigger_quarter_view.png`, both trigger pairs. A 6 mm wide, 3.7 mm deep blade replaces the wire-like section. Its existing muzzle-facing concavity and forward toe remain. The oblique view exposes flat sides and blade depth. Our toe and upper bearing neck retain original contours; the blade is slightly fuller than the photographed one. |
| Sights | `views/sights.png`, `front_sight.png`, `aimed.png`, `aimed-pixels.png`. Rear ears now belong to a 1.1 mm flat blade, with thin swept tips. Dovetail, leaf and stepped elevator contacts are retained. The front sight and exact Eye frame are preserved. The 8× enlargement uses native pixels with nearest-neighbor filtering, never a changed camera. Ear tip contours remain original and slightly more open than the photograph. |
| Barrel, magazine and bands | Orthographic side/top/front, `views/forend.png`, `front_sight.png` and side pairs. Accepted meshes are preserved, including their normals, sleeve fits, gauge and support contacts. Their original clamp details and band spacing still differ from the older photograph as recorded at the first gate. |
| Butt stock and butt plate | `sections.jpg` at Y −240/−200/−150 mm, `views/stock.png`, `butt_plate.png`, `butt_plate_profile.png`, both side pairs. Broad flanks, rounded comb and narrower toe replace pointed ellipses. The steel plate follows the same outline with an approximately 9 mm shallow crescent and two screw seats oriented to its curve. The entire wooden end cap is deformed, rather than only its perimeter. Fifteen actual surface rays place the wood 2.83–3.31 mm behind the steel. Our comb remains fuller and the crescent less deep than the older reference; the later checkered stock is a different variant. |
| Forend | `views/forend.png`, side pairs and three section stations. Accepted geometry is preserved. Its fuller nose and plain uncheckered surface still differ from the later .375 reference. Grain, dings and hand oil remain deferred. |
| Ammunition | `case/case.png`, `case/mouth.png`, cartridge macros and published C.I.P. exterior stations. The body/shoulder/neck are clean straight tapers; the apparent dent was interpolation of shoulder normals over the long body. Independent imported rays check eleven exterior points on each standalone. Counts remain 1,598 live / 1,326 fired. The required flat nose differs from the reference soft point; our shoulder transition is sharper and the brass cleaner than the used photo. |

All photographs retain the documented linear neutral adaptation. Constant
inspection colors remain provisional: this gate makes no wood-grain, wear,
albedo or baked-material acceptance claim. The fresh exported GLB is the form
judgment; dense-source pairs are supplementary.

## Round-trip correction

The first complete source sweep passed while fresh imported Cycle/Chamber
failed at f49.5. glTF sampled a zero-scale CarrierRound at f50 as an identity
rotation, so interpolation prematurely tipped the still-visible cartridge into
the barrel and forend. FiredCase similarly lost rotation just before f34.
STEP visibility itself was correct. Motion now belongs to nonscaling
CarrierGuide/FiredGuide bones, while their children control display alone.
Targeted half-frame source/import comparisons and the imported Chamber sweep
confirmed the correction before repeating the complete checks.

The initial Makefile also expanded BP/PYTHON before the kit defined them.
Recursive expansion fixes both commands. That initial failed run is not counted
as a passing build. The final reported make run uses the corrected graph.

## Planned hunting wear, after this gate

| Named site | Finished appearance and cause |
| --- | --- |
| Receiver corner rubs | Narrow broken bright-gray steel along handled/projecting corners; dark bluing retained in recesses |
| Receiver bottom rubs | Directional gray contact streaks below the action, confined to exposed bearing/handling areas |
| Receiver plum flats | Uneven thin bluing with a restrained plum/brown cast on exposed flats, not a uniform noise wash |
| Lever hand arcs | Smooth polished-gray bands on the lower and inner finger loop where fingers ride |
| Gate lips | Thin bright steel at the spring cover's mouth and handled edge |
| Band shoulders | Small edge rubs on projecting steel, no dirty halo on adjoining wood |
| Muzzle rim | Fine radial and axial scuffs at the accessible crown rim, bore kept dark |
| Toe/heel crush marks | Small directional compressed/darkened walnut dings at exposed corners |
| Forend edge dings | Sparse broken dents on grasped and bumped wood shoulders |
| Wrist hand oil | Darker, smoother walnut around the palm contact, following carved fiber |

No finish effect is accepted from a close-up alone. The later baked hero must
show the localized use at full frame without washing out steel or walnut.


## First-checkpoint verification (historical)

The checkpoint `make` graph runs the source construction/state sweep, fresh
GLB verification, repository check, imported geometric topology check and all
presentation stages. `make repeat` performs a second independent build.
The final inspection uses the exported game GLB, including its provisional
materials; high-source pairs are supplementary and explicitly labeled.

Recorded successful commands:

```text
make -C guns/lever                 exit 0, including check and fresh-import sweep
make -C guns/lever repeat          exit 0, independent rebuild comparison passed
python3 kit/repo_check.py          exit 0, 781 source files, 0 errors
python3 -m compileall -q guns/lever/src guns/common/ammo_3030.py guns/common/interface_v1_5.py
                                  exit 0
git diff --check HEAD              exit 0
```

- **39,768 gun triangles**, including all ammunition representations; 118 named
  inspection meshes, seven constant material classes, zero texture images.
  Gun GLB **2,649,528 bytes**. The standalone live round is **1,598 triangles /
  58,656 bytes / five materials**; the fired case **1,326 / 47,052 / three**.
- **67 required contacts/support probes** pass in the source and fresh import.
  The worst measured gap is **0.11815 mm**, inside its stated limit. All eight
  tang bearing-land gaps are at most **0.05892 mm**. Each tang component has
  an actual triangle intersection with the receiver. This establishes stated
  construction, separately from serialization agreement.
- **232 intended event/state checks**, the complete count chain, insertion
  interruptions, standalone origins/scale, visible fired-primer dent and its
  remaining thickness pass. Carrier travel is checked on empty cycles too.
- All **37 clips** pass the kit's half-frame clearance sweep: **5,271 source /
  5,304 imported samples**. There are no violations of the declared policy.
  Explicit chamber/bearing contacts and connected hand-envelope overlap retain
  finite bounds in `src/check.py`; this is not a continuous collision proof or
  an anatomical hand simulation.
- **5,271 full affine samples** compare every bone and all ten socket frames.
  Maximum position difference **1.975 micrometers**, maximum linear-component
  difference **0.00000781**. **185 event/end-frame surface comparisons** have
  maximum distance **0.121 micrometers**. These establish serialization.
- Raw exported normals are finite/unit and face outward relative to winding;
  skin weights are rigid and sum to one. All **118 imported geometric solids**
  are closed after check-only welding of duplicated normal/attribute seams at
  **0.01 micrometers**. Unwelded raw seam edges are retained in the geometry
  record for transparency; delivered meshes/normals are not welded by the test.
- The repeat build has identical vertex/normal/skin/animation accessors,
  metadata and oriented triangle sets. Only identical bead triangles can be
  serialized in a different order. Both ammunition GLBs reproduce byte-for-byte.

The dimensional sheet records **965.20 mm overall, 508.00 mm barrel, 340.18 mm
pull, 42.54 mm width and 183.92 mm height**. The section labels describe the
combined section envelope where barrel/tube/bands are included; the flat at
Y=330 mm is the actual rear-sight dovetail seat. The high/low outlines coincide
closely while retaining the varying stock and forend sections.

Camera RMS residuals are **14.10 / 23.08 / 10.46 pixels** for right/left/open,
**3.97 / 3.40 pixels** for trigger side/oblique. These estimated photographic
fits are distinct from the kit's subpixel camera-projection implementation
check. They are not claims of exact contour identity.

`build/check.json`, `serialization.json`, `topology.json`, `determinism.json`
and `provenance.json` retain the complete measurements. `renders/checkpoint/`
contains the contact sheet, regions, dimensions, sections, both photo-pair
sheets, whole-gun strips and eleven action-detail strips. The 37 whole-gun
and eleven detail WebPs retain their encoded real durations; static holds
retain their duration as well.

The final visual audit opened the regenerated contact sheet, region views,
dimension sheet, actual section cuts and both sets of photographic pairs.
All 1,025 whole-gun/detail clip samples were accounted for by decoded-pixel
hashes; their 132 distinct images were opened in six inspection sheets. Exact
duplicate holds share that inspection, rather than being mistaken for missing
poses. Together with the 38 still/pair renders, provenance records **1,063
current-source images**. The audit confirms the smoother stock highlights and
seated tang visible in the last correction, while retaining the region-by-region
photographic differences above. It does not accept the inspection materials as
finished surfaces.

## First-checkpoint remaining limits (historical)

The original loop, stock/crescent, gate and horn contours still differ from the
photos as itemized above. Lock/carrier/fire-control internals are incomplete
visual constructions; feeding contains declared occluded representation
handoffs. The eye's 368 mm placement is an authored ergonomic estimate with a
qualitative cheek-weld reference, not a published dimension. The 3.1 kg mass is
only a class target. Inspect supplies an internal hammer-touch presentation;
the consumer supplies whole-instance turns and hand IK.

Finish, wear, grain, UV/density checks, the 4096-to-2048 bake, final atlas
consolidation and textured delivery remain after lead form review, as requested.
No docs JPGs or generated binaries are committed at this gate. No kit or
existing common/gun file changed. A future kit guide/display helper and a
hide-boundary fixture would make the zero-scale export pitfall harder to repeat.


## Round-two critique passes

The original checkpoint is preserved under `renders/round1/`. The round-two
trials are ignored in `renders/form2-pass*/` and `build/form-round2/`; only the
current `renders/checkpoint/` evidence is presented for this gate.

1. **Forged forms and sections.** Color/value first: keep the provisional dark
   steel and brown walnut, and compare silhouettes against the neutral-adapted
   photographs described above. They still lack photographed finish variation;
   this is deferred deliberately. Replace the separate hooked lever bars with
   one forging, sculpt flat stock flanks and a rounded comb, and build a stepped
   receiver with a front ring and open bolt race. Keep the accepted action keys
   and forend. Early gate and hammer trials failed the unchanged motion policy;
   those versions were rejected rather than enlarging collision allowances.
2. **Inlets and camera anatomy.** Value first: dark wood/steel seams must remain
   narrow, without pale highlight fans. Wrist sections showed the old tangs
   outside the wood envelope. Rebuild them against measured walnut surfaces and
   cut their actual inlets. A cutter ending inside the surface left a thin wood
   skin; extend it through the crown. Correct the oblique camera's mislabeled
   wood landmarks to actual receiver corners. Its honest RMS residual increases
   to 10.26 px; the previous 3.40 px fit was anatomically invalid. The open-view
   weak-perspective camera reduces its residual from 10.46 to 4.17 px, while
   retaining the estimated-camera limitation.
3. **Exported grazing highlights.** Value first: the steel showed a wavy bright
   front ring despite a clean silhouette. Give the receiver its analytic loft
   normal field and genuine flat cheek normals. Give the long lever an actual
   0.28 mm rolled perimeter after Boolean cleanup; an earlier nominal bevel had
   clamped almost to zero. The fired case's false shoulder wave came from
   interpolating shoulder normals along the long body. Separate the analytic
   cone normals at those stations; keep the exterior geometry and round budget.
4. **Plate and wood cap.** Value first: a brown patch in the black plate macro
   revealed exposed wood through the crescent. Deforming the cage perimeter
   alone left the subdivided end-cap center behind. Deform the complete finished
   cap, add more radial plate rings and orient both screw seats to the curve.
   Fifteen imported surface rays now place wood behind steel. The native macro
   and profile expose the full curve and both screws; they do not conceal the
   remaining shallower crescent relative to the older photo.
5. **Hammer at the photographic angle.** Value first: the bright table silhouette
   was too upright and block-like beside the sharp photograph. Recover its
   roughly 12.9° cocked slope from native endpoints and rebuild the returning
   spur/table at a measured 13°, retaining the accepted 44° cocking key. Model
   crowned 1 mm diamonds, a curved compound body and a deeper trigger blade.
   Preserve the 90° overtravel and cut its actual swept envelope from the
   wood/tang. Clean two tiny detached Boolean chips and sub-micrometer collinear
   tang slivers; keep closed topology and the original normal-direction limits.
   The larger mortise and more rectangular thumb table remain visible limits.

Final inspection begins with value again. On alpha-covered hero pixels
(alpha > 0.5), display luma p1/median/p99 is **4.35 / 47.31 / 194.13** on the
right and **5.00 / 62.00 / 225.21** on the left, on a 0–255 scale. No foreground
pixel clips all three channels at 254 or higher. Cavities remain dark and the
broad highlights roll off, but these measurements do not establish real albedo
or accept final materials. `build/form2-values.json` retains both measurements.

## Round-two verification

Successful commands, each exit 0:

```text
make -C guns/lever
make -C guns/lever check
make -C guns/lever repeat
blender -b --factory-startup --python-exit-code 1 --python src/preserved.py -- --before build/round1/lever.blend
  (run inside guns/lever; optional saved-checkpoint audit)
python3 -m compileall -q guns/lever/src guns/common/ammo_3030.py
python3 kit/repo_check.py
  784 source files, 0 errors
git diff --check
```

At the repository root, the complete final build log is
`build/form-round2/checkpoint-final5.log`;
explicit check and repeat logs are `check-final.log` and `repeat-latest.log`
in the same directory. The saved baseline is optional evidence and is never
required to rebuild the asset.

| Output | Triangles | Inspection materials | Texture images | GLB bytes |
| --- | ---: | ---: | ---: | ---: |
| Gun, including all ammunition representations | **39,926** | 7 | 0 | 2,856,292 |
| Live cartridge | **1,598** | 5 | 0 | 61,728 |
| Fired case | **1,326** | 3 | 0 | 50,124 |

The net increase is **158 gun triangles**, inside the requested 30–40k budget.
Reduction is concentrated on the receiver, stock, swept relief and hidden
surfaces to pay for the lever edge roll, plate curvature and hammer table.
There are **116 named inspection meshes**, all closed after the kit's
check-only 0.01-micrometer attribute-seam weld. Finite/unit/outward normal and
rigid-skin checks pass; the normal-direction record excludes one triangle below
its existing tiny-area threshold rather than claiming that it measured a face
normal there. No tolerance or clearance allowance was relaxed.

- **Construction:** all **67** source/import contacts pass, worst measured gap
  **0.11814 mm**. Both tangs lie inside the measured pre-inlet wood at all six
  inspected section/part combinations. The actual screw-shank/wood-bore radial
  gap is **0.05000 mm**. Fifteen plate/wood rays measure **2.826–3.313 mm** from
  the exterior steel to the covered wood. Each tang component reaches the
  receiver. These establish stated construction, separately from serialization.
- **Lever:** actual opening **104 × 29 mm**, bar **2.2 × 8.2 mm**, unchanged to
  numerical precision in the three evaluated **0° / 40° / 80°** poses. An added
  callback checks its center and transformed X normal at every half-frame sweep
  evaluation: **5,272 source / 5,305 imported callbacks**, including pose restore,
  no mid-plane failures. No rig change was necessary.
- **Motion and states:** **37 clips**, **5,271 source / 5,304 imported** clearance
  samples, no declared-policy violations; **232** intended event/state checks
  pass. The existing finite bearing/chamber and connected-hand allowances remain
  explicit. This is sampled clearance of the stated volumes, not a continuous
  physical or anatomical simulation.
- **Serialization:** **5,271** full affine samples, maximum position difference
  **1.974 micrometers**, maximum linear-component difference **0.000007808**;
  **185** event/end-frame surface comparisons pass. The two standalone imports
  also pass eleven actual exterior rays apiece against the published straight
  body/shoulder/neck segments. The fired primer retains its measured 0.22 mm
  dent and 0.07 mm center thickness.
- **Preservation:** the saved first-checkpoint audit compares **30 accepted
  meshes**, all **26 rest bones** and all **37 complete clip F-curve sets**.
  Ordered vertices, owners and topology are unchanged. The bead retains its
  exact oriented triangle set with maximum normal rounding **0.0000001192**;
  Blender may reorder those identical triangles. All socket orientations are
  unchanged. `Socket_Butt` alone moves **4.2936 mm forward** to the revised steel
  surface, documented in `INTERFACE.md`. Eye and LeverHand remain exact.
- **Repeat:** every vertex/normal/skin/animation accessor, metadata and oriented
  triangle set matches the independent build. The gun file hash differs only
  through the documented bead index ordering; both standalone GLBs reproduce
  byte-for-byte. `build/determinism.json` records this distinction explicitly.

Current measured dimensions are **965.20 mm overall / 508.00 mm barrel /
340.74 mm pull / 42.55 mm width / 183.76 mm height**. The original overall and
barrel dimensions remain exact to float precision; pull changes slightly with
the revised curved butt surface and deeper trigger, rather than being reported
as an unchanged constant.

Photographic RMS residuals, in order right/left/open/trigger-side/trigger-oblique/
hammer/closed-lever, are **14.10 / 23.08 / 4.17 / 3.97 / 10.26 / 10.49 / 10.25 px**.
They establish the estimated fit's limits, not an exact photographic match.
`build/photo-measurements.json` records native endpoints, both loop estimates,
S-curve offsets and the hammer slope. The open estimate is about 105 × 32 mm;
the closed estimate is about 71.5 × 17.8 mm. Their disagreement remains visible
in the two lever pairs. The transverse bar and checkering pitch remain authored
class estimates.

The final visual audit opened all **35 gun/ammunition stills** and **14 exported/
dense-source pairs**, the final contact sheet, photographic sheet, sections,
raking sheet, hammer/trigger pairs, lever stroke and native sight enlargement.
All **1,025** clip samples were accounted for by decoded-pixel hashes; their
**134** distinct images were opened in nine inspection pages. Together these
are **1,074 current-source renders**. `build/provenance.json` confirms their
current GLB/sculpt hashes and all 37 whole-clip / eleven closer-strip durations.
The actual aimed camera remains unchanged; `aimed-pixels.png` enlarges a
110 × 84 native-pixel crop by exactly 8× with nearest-neighbor filtering.

## Round-two remaining limits and handoff

The region table above is the current critique. The largest remaining form
uncertainties are the smaller closed-reference loop, the higher S-web throat,
the broader hammer mortise required by accepted overtravel, and the more
rectangular/checkered thumb table. Our comb remains fuller, the crescent shallower,
and the front ring/gate larger than their comparison photos. The internals and
occluded feeding handoffs retain the accepted visual simplifications. These
are disclosed differences, not self-accepted exact matches.

This stops again at the requested form checkpoint. Grain, wear, UV/density,
bake transfer, final atlas consolidation and textured delivery remain deferred.
No generated binary or docs image is committed. No kit file or other gun changes;
only the existing common .30-30 generator receives the analytic-normal fix.
Nothing is needed to reproduce or inspect this gate. A future kit fixture that
checks a moving part's invariant plane would make this new lever regression
check reusable; no kit API was changed during this round.

## Last form corrections and finish authorization

The lead accepted round two's dimensions, mechanism, interfaces, contacts,
lever opening/S, receiver, tangs, butt sections/plate, hammer/trigger, forend,
bands, front sight, aimed alignment and ammunition. This continuation changes
the three requested visible issues, then completes the authorized finish.
Earlier statements that finish is deferred describe the historical checkpoints.

**Color and value first — last form pass.** The constant dark steel and brown
wood remain inspection colors. In the old `views/sights.png`, the empty U and
long ears read as bent wire. A ruler photograph of a real semi-buckhorn sheet
(`refs/rear-blade.jpg`, Homestead Parts) supplies independent height/ear/notch
observations. Its gray backdrop is the white-balance neutral. The seller's
9.017 mm height is distinguished from the ruler's perspective-dependent
estimate; the blade and ruler are not coplanar. Our actual mesh measures about
8.98 mm high, 1.10 mm gauge, 2.18 mm ear rise, 1.60 mm notch width and 1.25 mm
notch depth. The smaller notch is part of this expressly requested sight fix;
its shoulders and the exact Eye frame retain the accepted bead alignment.
The blade has one filled, flat face. Assigning true flat face normals removes
the triangular highlight fan exposed by the first front-on render.
The ruler-plane estimates are 10.12 mm overall, 1.62 mm ear rise,
2.02 mm notch width and 1.21 mm notch depth. Our blade therefore has taller
ears and a narrower notch than that photographed insert, in addition to its
more angular tips and different mounting. The independent 9.017 mm published
height controls the overall envelope; estimated perspective prevents treating
the ruler as a coplanar manufacturing drawing. These remaining differences
are visible in the pair, rather than being hidden by the measurement table.

The rest photograph's loop is smaller than our accepted opening. Consequently,
use bar-to-opening ratios as well as the underdetermined camera-plane lengths.
The 5-pixel loop bar recovers 2.09 mm on that smaller loop; normalized to the
accepted 29 mm opening it is 3.40 mm. The bow's 19-pixel normal section recovers
8.00 mm, about 13.0 mm at the same opening normalization. Our lower loop rail is
3.30 mm deep, transverse width 8.20 mm; actual bow depth is recorded in
`build/form3-idle.json`. The aperture remains 104 x 29 mm. The deeper upper rail
initially touched the unchanged lower tang/wood by about .8 mm. Reject that
trial. Relieve the concealed upper run back to its original 2.2 mm section;
the hand-ridden lower rail keeps its new depth. No opening, pivot, clip, socket
or collision allowance is moved to accommodate it.

The wrist's creases came from normal transfer against an already inletted dense
mesh: cut-wall normals contaminated the outer carving. Preserve the smooth
**uncut** cage as a separate normal reference and use nearest-surface transfer
for the stock. Apply that same uncut field to its dense bake source, so baking
cannot reintroduce the fault. Every stock vertex and triangle stays identical.
The broad outer flank is now smooth into the seam; the internal mortise retains
its actual cut walls and the previously accepted hammer clearance.

Rebuilt evidence: `renders/form3/form-fixes.jpg`, `lever-stroke.jpg`,
`wrist_raking.png`, `sights.png`, `sight_blade.png`, `aimed.png` and the three
pairs in `renders/form3/pairs/`. Native sight/ruler endpoints and their limits
are in `build/final-form-measurements.json`; lever endpoints and normalized
ratios are in `build/photo-measurements.json`.

Remaining differences, judged from those pairs: our sight has short angular
outer tips, while the photographed insert has rounder outer shoulders and two
mounting holes. Its mounting window is not ours. Our loop retains the accepted
longer opening; the rest photo's smaller loop cannot match its crop exactly.
The S throat is cleaner and higher than that gun's linkage. The wrist seam is
smooth, but our accepted larger hammer mortise and broader thumb table still
differ from the used photograph. Those accepted forms are preserved.

## Finish critiques

1. **Source pass 1 — value and hue first.** `renders/lookdev/pass1/` uses the
   initial procedural source. White-balanced `open2.jpg` uses its broad bare
   bolt flat, native (470,166)-(570,177), as an estimated silver neutral.
   `open.jpg` uses its polished cross-pin facet; `receiver.jpg` its silver pivot
   screw. The right full-gun photo uses unclipped white paper. Neutral names,
   gains and marked patches are rebuilt under `build/white-balanced/`.
   None is a calibrated gray card; the reflective neutrals retain environmental
   uncertainty. The first source receiver flat is **9.34/255** versus **58.73**
   in the used photo; wrist **70.24** versus **26.75**; forend **94.00** versus
   **57.29**. Reject the orange, glossy furniture, black receiver flat, broad
   white top reflections and uniform silver outline. The standalone atlas
   staging rounds also appeared in the source hero: hide them in source-only
   presentation, retaining them in the bake atlas.
2. **Source pass 2 — value and hue first.** `renders/lookdev/pass2/` gives
   receiver/wrist/forend **37.11 / 40.27 / 50.25**, with the same photographic
   values **58.73 / 26.75 / 57.29**. Darker walnut and taller neutral reflection
   cards correct the biggest value errors. The wrist still reads gray because
   a broad dielectric reflection overwhelms its dark hand staining; the wood
   needs a lower gloss response. The receiver's lower edge and gate rubs are
   visible, but the upper rim is too uniformly bright. Break its contact
   continuity and narrow the gate's exposed core. Keep gray bare steel separate
   from the brown/plum thinned oxide on the flats.
3. **Source pass 3 — value and hue first.** `renders/lookdev/pass3/` measures
   wrist **29.12** versus **26.75**, forend **47.01** versus **57.29**; receiver
   remains **37.11** versus **58.73**. The lower wood gloss restores a brown
   wrist. Reject the broad, evenly spaced growth bands: they read as a laminate
   despite the correct longitudinal direction and separate vessel pores.
   Reduce annual-layer spacing, reduce its broad tonal swing and retain narrow
   latewood/vessel structures. Brighten the original walnut diffuse field
   modestly, preserve hand-darkened wrist placement, and raise only the thinned
   plum/brown oxide toward the observed receiver value. No reference image or
   measured photo mask enters those procedural fields.
4. **Source pass 4 — value and hue first.** `renders/lookdev/pass4/` measures
   receiver **57.65**, wrist **29.19**, forend **55.86**, beside photographic
   **58.73 / 26.75 / 57.29**. RGB medians are receiver **83/53/32** versus
   **81/54/39**, wrist **39/27/22** versus **44/23/11**, forend **84/50/31**
   versus **86/51/32**. The wrist remains less red/yellow than the estimated
   photographic neutral permits. This is observed display agreement under
   estimated lighting, not albedo recovery. The finer growth structure avoids
   the broad laminate bands; natural walnut's irregular figure remains richer.
   The named dings are local crushed-fiber bowls with broken pale finish lips;
   the receiver flat stays thinned brown oxide, distinct from exposed gray
   steel along its contact edges. Original rollmarks and serial are baked
   relief, using installed Noto Sans. Proceed to judge the shipped bake.

An independent serialization test caught a pipeline error before delivery:
applying the dense stock's normal-transfer modifier also cleared its armature
modifier, so the temporary checkpoint GLB lacked stock skin weights. Preserve
and restore the rigid armature binding around that operation. This does not
change geometry, bones, clip keys or socket frames. The failed GLB is not used
for final delivery; the rebuilt export must pass the raw weight/import checks.

5. **Exported pass 1 — value and hue first.** The first 4096-to-2048 GLB
   comparison (`renders/lookdev/export1/`) retains receiver/wrist/forend
   **57.86 / 29.12 / 55.86**, against **58.73 / 26.75 / 57.29**. Pores and
   fine rollmarks soften, while broad color, grain direction and hand darkening
   survive. The front bead mistakenly inherited the non-ammunition dark-steel
   branch: give its existing brass assignment the actual brass shader. Do not
   alter its accepted mesh or sightline. A raw-normal check also catches one
   meter-scaled stock sliver and seven UV-preparation corner normals; compare
   them with the actual meter-space triangle winding and correct only opposed
   vectors. The low's microscopic cleanup removes 18 triangles, leaving 39,950.

6. **Two-dimensional receiver wear — color/value first.** A brightness-only
   mask on the brown right/top photo is invalid: it counts bright patina and
   a little background as exposed steel. Reject that comparison as acceptance.
   Keep the right/top photograph for brown oxide/wood values. The sharper
   white-balanced open-left action shows the rubbed gray lower fillet clearly;
   its pivot-screw facet is the estimated neutral. Compare the actual shipped
   bare-steel mask with an independent native annotation of that apparent gray
   fillet, on an approximately 115 x 8 mm grid at 0.5 mm. Native coordinates,
   uncertain approximately one pixel, remain in the JSON. Neither photo pixels
   nor annotation enters the asset generator or a shipped texture. Photographic
   gray response does not prove the finish's chemistry.

   The first proper 2D comparison is frozen under `build/review/wear-before/`:
   actual bare area **26.90%**, photographed annotation **27.07%**, both one
   connected region. Similar areas are insufficient: our band sits too low
   across the fillet and its four repeated width lobes look procedural. Reject
   that morphology. Move only the contact center 0.85 mm up the lower corner,
   replace the repeated large sine lobes with a broad carry-pressure field and
   small boundary variation, and compare both axes again after baking. The
   intact brown oxide and its calibrated values remain unchanged.

Initial hypothesis, rejected in pass 7: the white point in an early stock
macro has ordinary wood texels at the initially probed surface:
BaseColor **63/38/23**, Normal **128/125/255**, ORM **255/122/0** at the actual
surface hit. Try clamping indirect samples at 2 while retaining direct
highlights; the fuller seam-neighborhood investigation below supersedes this
first firefly hypothesis.

7. **Exported 2D wear pass 2 — color/value first.** Brown oxide still retains
   the calibrated value. The shifted strip covers **29.21%** of the comparison
   grid against **27.07%** in the annotated photo, but its shape still fails:
   constant contact height creates a straight ruler stripe. Its first/second
   height quarters cover **43.80/73.04%**, versus **35.54/72.50%**; agreement
   in those coarse totals conceals the photo's curving center. Reject it. Give
   the carrying-hand field a broad downward reach around the pivot and a
   return onto the side, and slightly reduce its width. This remains an
   original analytic contact field, never a projected or traced photo mask.
   Rebuild the complete bake/export and comparisons after this change.

   The first stock-glint diagnosis was incomplete: clamping indirect samples
   at 2 did not remove it. A new full-scene surface probe finds only Stock at
   the three tested pixels, excluding a protruding screw or tang. Its 9 x 9
   texel neighborhood has nonmetallic ORM and ordinary brown walnut, but this
   samples only one side of the UV seam. Test a fully sampled macro and the
   neighboring triangles before accepting the diagnosis or image.

   Root cause, established on the actual imported GLB: the neighboring stock
   triangle at pixel **839,259** samples BaseColor **162/164/167** and metallic
   **155/255**, although it is walnut. The initially tested brightest pixel
   lies on the other side of the UV seam and samples valid brown. The affected
   stock UV triangle is long and subpixel-thin near its tip; polished lever UVs
   lie only **5.63 shipping pixels** away, inside the six-pixel downsampled bake
   padding. This is atlas contamination, not a firefly. A 256-sample render
   confirms that the streak is stable. Reserve separate stock/forend regions
   within the same one-set atlas. Broader 45- and 18-degree Smart UV attempts
   fail the unchanged clipped-overlap limit, so retain conservative projection
   angles; never waive the check to improve packing.

8. **Bake-isolation correction — color/value first.** The reserved regions
   reveal additional gray contamination from rays encountering neighboring
   stationary steel. Isolate the two carvings through the kit's existing
   named-root projection policy, retaining rest-position shader attributes and
   stationary AO shadow copies. The resulting complete stock and forend
   regions both have **maximum metallic byte 0**, including all padding and
   subpixel tips. The new audit makes this a delivery assertion, rather than
   eroding away the narrow triangles that exposed the defect. No kit code,
   geometry, rig or triangle budget changes. Regional packing raises stock
   density to approximately **2,441 px/m**; forend remains **1,934 px/m**.
   All six 4096/32-sample bake channels hit all **4,143,388** checked interior
   texels. Render the exported atlas again before accepting this correction.

9. **Exported finish recheck — color/value first.** The corrected stock macro
   (`../../build/lever-final/glint-corrected/stock.png`) has no white streak at the
   standard 64 samples. Brown figure and the dark grip survive; toe/heel dings
   remain local. The revised contact field's actual 2D bare-steel share is
   **25.11%**, beside **27.07%** in the photo annotation. It now curves around
   the lower corner instead of following a constant-height ruler line. Across
   height it rises and falls over nine 0.5 mm rows, versus the photo's nine;
   the photographic area is slightly fuller near the rear. The native-pixel
   annotation uncertainty and different original fillet remain explicit. This
   morphology is substantially closer, and broad material values are retained.

   The stricter delivery audit initially conflated raw delivered normals with
   Blender's imported custom-normal encoding. Measure both independently:
   raw FLOAT corner normals differ by at most **8.53e−5** in vector length
   (about **0.0049 degrees**); positions are exact and UV difference is at most
   **2.98e−8**, about **0.000061 shipping pixels**. Blender's custom fan
   re-encoding reaches **0.584 degrees** at a narrow stock inletting cut.
   Retain the strict raw-normal check; separately bound imported fan error
   below one degree. This does not waive raw direction/unit-normal tests or
   the exact one-to-one oriented triangle/UV correspondence. Raking exported
   views establish that the accepted outer walnut remains visually smooth.

The final calibrated forend patch is **55.79** luma (photo **57.29**); receiver
and wrist remain **57.86 / 29.12**. The whole-stock flash photograph is not a
successful display-value match: **140.38** luma versus **64.79** in the neutral
studio. Its broad glossy reflection and the oil-finish lighting setup differ.
Keep this discrepancy in the complete patch report rather than presenting the
three closer primary-used-photo patches as proof of universal photographic
agreement. Real walnut also retains more irregular figure than our source.

10. **Final studio pass — color and value first.** The final right hero's
    object-only luma percentiles (1/50/99) are **1.79 / 59.77 / 219.35**;
    **13.62%** of object pixels are below luma 24. The left hero is
    **0.93 / 59.14 / 211.07**, with **22.13%** below 24. Neither hero has any
    channel reaching 254: maximum RGB is **239/241/241** on the right and
    **238/239/240** on the left. Cavities, the race and underside remain deep;
    steel highlights roll off. The receiver macro has **0.62%** white-clipped
    direct specular pixels; that is retained in the tonal report, not hidden.
    Both source and exported photo pairs have been opened and compared.

    The brass display patch is **206.07** versus photographic **207.04** luma.
    Copper is **96.92 / 68.57**, and lead **72.16 / 104.14** (export/photo).
    Different reflection angles and the photographed rounded soft point versus
    the accepted flat nose limit those comparisons. Its estimated neutral is
    the exposed lead cap, with native coordinates in the ammunition JSON.
    The remaining regular wood figure, softened small lettering/pores, taller
    angular sight tips, narrower notch and bright flash-stock mismatch remain
    explicit limitations. No claim of identical photographic illumination or
    recovered albedo is made.

    Final framing now shows the complete toe in the front turnaround, the
    complete curved butt plate and both screws in its macro, and clear space
    between the carbine and the 1.8 m scale figure. The aimed camera remains
    the accepted opaque 70-degree Socket_Eye view. All 37 real-duration WebPs
    decode to their declared times. All **71 unique** final clip images were
    inspected: 67 match the previously reviewed set, and four new raster
    variants were opened separately. There are no visible new motion artifacts.

## First finish delivery proof (historical)

- `make -C guns/lever`: **exit 0**. Complete log:
  `../../build/lever-final/make-final.log`.
- `make -C guns/lever check`: **exit 0**. Complete log:
  `../../build/lever-final/check-final.log`.
- Independent `make -C guns/lever repeat`: **passed**; the report hashes still
  match all three current inspection GLBs. Vertex, normal, skin and animation
  accessors match; oriented triangle sets match. Bead index ordering may differ.
- `src/preserve_final.py`: **passed** against the saved handoff. The 113 other
  mesh geometries, all **26 bones**, **37 clips** and **10 complete socket
  frames** compare unchanged; stock vertices and triangles are identical.
  Bead corner-normal ordering/encoding is excluded from this optional exact
  historical comparison. Raw delivered normals are checked independently.
- Source: **39,968 triangles**. Shipped carbine: **39,950 triangles**, one
  material, **11,804,068 bytes**. Standalone cartridge: **1,598 triangles /
  6,786,108 bytes**; fired case: **1,326 / 6,767,264 bytes**. No budget increase.
- One canonical **2048 BaseColor / OpenGL Normal / ORM** set, identically
  embedded in all three GLBs. PNG bytes: **1,659,560 / 2,286,588 / 2,718,359**.
  The 4096/32-sample bake hits all **4,143,388** checked interior texels in
  every channel. Stock/forend regions contain no metallic texels, including
  narrow UV tips and padding.
- Gun atlas coverage **27.73%**; complete gun/ammunition family **32.44%**.
  Zero escaped or degenerate UV triangles. Three microscopic upper-tang overlap
  pairs total **8.63e−8 UV area**, family fraction **2.66e−7**, below the
  unchanged **1e−5** limit. Regional densities and full distributions are in
  `build/delivery/*-uv.json` and `verify.json`.
- The current GLB's **39,950 actual imported triangles** match the finalized
  named surfaces one-to-one across **116 closed solids**. Its **67 actual
  surface contacts** pass, all **37 clips / 5,304 imported clearance samples**
  pass under the accepted bounded-contact policy, and the mid-plane checks
  pass. These establish sampled construction/clearance, rather than only
  serialization. They do not claim continuous-time mechanism physics.
- Separately, **5,271 complete affine bone/socket samples** and **185 posed
  event/end surface comparisons** establish serialization. Maximum affine-frame
  position difference is **1.974 micrometers**; maximum posed-surface difference
  is **0.121 micrometers**. Raw positions, UVs, unit normals, rigid weights,
  texture hashes and standalone origins also pass.
- `build/final-provenance.json` associates **731 GLB-derived images**, including
  all clip samples, with the current exports. Hero on gray:
  `renders/final/hero-gray.jpg`; contact sheet: `renders/final/contact-sheet.jpg`.
  Final photos and pairs: `renders/final/photos/` and `pairs/`; source comparisons:
  `source-photos/` and `source-pairs/`. Native studio/scale/aimed views:
  `renders/final/beauty/`; Eevee: `renders/final/eevee/hero.png`.
- Five final docs JPGs are **1600 px wide**, **38,280–187,668 bytes** each.
  They were opened and remain **uncommitted**, as requested, for lead acceptance.
  Scripts compile and repository checks pass; no generated binaries, textures
  or references are staged. No kit or shared gun module was changed.

No additional tool is needed from the lead. Suggested kit follow-up: validate
thin UV tips/padding as well as eroded interiors, expose stationary projection
isolation more clearly, and distinguish raw GLB normals from Blender's imported
custom-normal fan encoding. The existing helpers already support this delivery;
no shared-code change was necessary.

## Look round 2 — lead rejection and new critiques

The preceding final-look acceptance was too lenient. The lead retained the
form, all mechanism/interface evidence, lower-fillet contact shape and delivery
budgets, but rejected copper-like oxide, chrome-like rubs, uniform receiver
thinning and the straight wrist cuff. This section supersedes the old finish
acceptance. The handoff is frozen under `../../build/look-round2/before/`.

1. **Color and value first — whole-plate baseline.** Opened the native hero,
   receiver, used pair, value patches and the finished Hearth 12 docs. The
   original hero's entire oxide-flat median is **120/79/50**, versus the
   white-balanced used photograph's **79/53/36**; the bright deciles are
   **166/121/88** and **104/73/57**. The old favorable rectangle does not
   establish whole-plate agreement. Copper-colored reflections, a continuous
   receiver outline, pale lever/trigger/bands and a square-ended wrist stain
   remain obvious at full frame. The neutral is the same broad exposed bolt
   flat, native (470,166)-(570,177), adapted in linear RGB. This is an estimated
   reflective neutral, with uncertain illumination, not an albedo measurement.
   Build the main-branch shotgun in an ignored local snapshot and compare its
   exported hero/receiver under the same cards before setting the final steel.

   ![First critique: rejected Bracken hero beside the approved main-branch Hearth hero](../../build/look-round2/before/hero-shotgun.jpg)

2. **Color and value first — source trials, rejected.** The first effective
   oxide/steel blend removes orange conductor reflections but is too pale;
   5 mm protected halos look like black spray-painted circles around screws.
   `renders/look-round2/source1/` records that rejected version. Narrow and
   reduce those halos. The second source has a too-neutral flat: hero
   **89/80/76**, used-view **74/66/61**. It loses the photograph's brown diffuse
   body. The third restores brown diffuse under a dielectric oxide surface
   with gray substrate, but overshoots value: hero **108/84/69**, used-view
   **103/80/65**. Darken that diffuse endpoint, retain neutral reflection and
   desaturate high carry scratches. The whole-plate mask is inset from the
   exposed fillet and excludes separate hardware. A first photo polygon
   included a few background pixels along the lower edge; correct its actual
   native contour before using distributions, rather than thresholding pixels
   until a statistic agrees. All masks, RGB, HSV and bright-decile distributions
   are in `src/plate_review.py` and its generated JSON/plots.

   The new sight source has rounded lobe shoulders and a measured 2.02 mm
   notch, retaining the 1.1 mm sheet and shoulder/floor heights. It reads as
   one filled sheet in front and oblique views. One 0.1 mm gauge bevel replaces
   extra subtexel bevel segments to pay for the lobes, reducing the source to
   **39,744 triangles**. The existing actual-surface form/contact check passes.
   The finished raking source shows a smooth outer wrist. The sharp interior
   hammer-mortise lip remains a real cut edge; recheck it after the normal bake.
   No stock geometry or accepted normal-transfer method is changed.

3. **Color and value first — exported steel and controlled studio.** Opened
   `renders/look-round2/export1/` beside the independently rebuilt main shotgun,
   both rendered with identical Bracken cards/cameras. The former copper
   highlights are now nearly neutral: whole-plate hero bright decile
   **93/82/78**, versus the handoff's **166/121/88**. However the inner lever
   rail and grazing upper tang still read too white. The same frontal cards
   make the accepted Hearth receiver/port and action bars pale too. This is
   evidence that the two original guns did not actually share their complete
   light setup. Stop calibrating against those frontal cards. Match the
   Hearth's five cards, world strength, exposure and black reflection flags
   exactly, retaining all Bracken cameras and the exact Eye frame. Keep the
   satin material response and compare again. Baseline hero pairs are in
   `../../build/look-round2/before/hero-shotgun.jpg`; original Hearth studio
   renders are in `../../build/look-round2/shotgun-studio/`, and the controlled
   former-Bracken-light comparison is `shotgun-shared/` beside it.

   The exported `export2/` in the actual Hearth studio fixes the white tang
   and lever: they now read as satin gray under the same light as its worn
   port. It also exposes the old diffuse calibration's reliance on frontal
   light: whole-plate hero **51/37/32**, used-view **48/34/28**, versus the
   photo's **79/53/36**. The small receiver/wrist/forend rectangles are now
   **51/31/20**, **24/11/5**, **52/27/11**, below photographic
   **81/54/39**, **44/23/11**, **86/51/32**. Reject this dark candidate too.
   Recalibrate oxide diffuse and walnut under the common studio, without
   increasing conductor saturation, reducing roughness or whitening the rubs.
   The exported wrist rake retains the smooth outside crown; no pinched fold
   runs into the wood beside the hammer. Its actual mortise edge remains sharp.

4. **Color and value first — final 2048 candidate.** The final export under
   the Hearth studio has whole-flat hero median **73/52/37**, against the
   photo's **79/53/36**. Display-luma p10/median/p90 is
   **24.71/55.88/62.36**, versus **46.10/56.95/72.65**. The darker low tail
   comes from the protected ends, screw seats and loading recess; the photo's
   different plate, reflections and lighting retain a narrower lower tail.
   Median HSV is **22.59 degrees / .443 / .286**, versus photograph
   **22.59 / .533 / .310**. The handoff hero was **24.00 / .569 / .471**.
   The corrected hero has a muted brown body, dark surviving bluing and gray
   reflections, rather than one smooth copper conductor.

   Distinguish diffuse brightness from reflection: the brightest flat decile
   is still brown (**91/58/33**); it is not an isolated specular lobe. The
   independently selected rolled shoulder measures approximately **38/36/35**
   in the hero and **73/73/74** in the matched used view. The photographed
   shoulder is **242/229/220** under its different light. This tests reflection
   color, not highlight width or recovered roughness. Native polygons, HSV
   distributions and both kinds of highlight samples remain in the JSON.
   The small receiver/wrist/forend rectangles now measure
   **86/53/30**, **41/22/12**, **86/51/34**, against photographed
   **81/54/39**, **44/23/11**, **86/51/32**. Luma is
   **58.50/25.18/57.21**, versus **58.73/26.75/57.29**.

   Opened the final native hero, receiver, wrist rake, common-studio hero
   comparison, full macro/photo pair and whole-plate histogram sheet. The
   tang is satin dark gray; lever contact is on the interior/rear rather than
   coating the exterior bow; trigger sides remain blue. Gray steel no longer
   forms a full bright outline around all receiver edges. The accepted lower
   fillet remains continuous where the carrying hand follows it; its shape
   is not changed to make the new roughness look quieter. Wrist darkening
   has a broad form-following fade, with no straight cuff. The outer carving
   beside the hammer stays smooth in the finished raking view; the mortise
   lip is an actual machined edge, not a pinched normal fold.

   Hero object luma p1/median/p99 is **0/54.42/158.65** with **29.52%** below
   24 and zero fully clipped pixels. Fine rollmarks and carry scratches soften
   at the one 2048 atlas; original walnut figure remains more regular than a
   real blank. These remain limits, not reasons to increase triangles or maps.
   Proceed to complete all final sheets, clip provenance and required checks
   against this exact export; the command results below are recorded only
   after those stages finish.

5. **Color and value first — native sight silhouette, further correction.**
   The final material candidate retains the preceding gray steel reflections
   and brown diffuse body; no color or value change is needed. Native front
   review nevertheless shows a small peak where the hand-placed ear segments
   meet. The source/photo sheet makes this visible even though the oblique
   view seemed rounder. Reject that remaining faceting. Replace only those
   ear segments with sampled elliptical arcs whose crest chord error is below
   0.005 mm, keeping the 2.02 mm notch, shoulders, floor, 1.1 mm sheet and
   optical frame. Spend the triangles saved from subtexel bevels on the actual
   silhouette. Interrupt the incomplete presentation/check run and regenerate
   the model, atlas, exports and all required proof from these final arcs.

   Opened the new native exported `export-rounded/sight_blade.png` and
   `sights.png`: the visible pointed crest is gone. Actual surface rays measure
   **9.000 mm height, 1.100 mm gauge, 2.200 mm ear rise, 2.020 mm notch width
   and 1.250 mm notch depth**. Source **39,832**, delivered **39,814** triangles,
   still 136 below the handoff. The new independent repeat passes, and the
   optional handoff audit again preserves all 115 other meshes, 26 bones,
   37 clips, ten sockets and the five accepted lower-fillet expressions.
   Full-plate hero RGB is **72.5/52/37**, unchanged within atlas filtering.

6. **Color and value first — carry variation after native review.** The
   preceding export is close in whole-flat median and retains neutral gray
   reflections, but the native macro still presents the brown thinning as a
   smooth vignette. A matching median cannot excuse that remaining tell.
   Replace the weak broad modulation with overlapping axial cloth/holster
   pressure inside the existing hand-contact envelope. Increase the resolved
   longitudinal striae and add six short, tapered grit tracks, 8–22 mm long
   and 0.08–0.14 mm wide. These are shader relief/color/roughness fields in
   the forging frame, not geometry or photographed textures. Keep screw,
   gate and tang protection; keep the five accepted lower-fillet expressions
   exactly. The native source trial in `renders/look-round2/source-carry/`
   shows the direction of travel and small surviving-blue variations across
   the flat. Check filtering on the exported single 2048 set before accepting
   this refinement. No wood, ammunition, geometry, rig or camera is changed.

   The exported native macro in `renders/look-round2/export-carry/` retains
   the tracks and overlapping thinning after filtering. Whole-flat hero
   median is **74/53/39**, luma p10/median/p90 **27.02/56.74/64.28**, and
   median HSV **22.59 degrees / .439 / .290**. The photo remains
   **79/53/36**, **46.10/56.95/72.65**, **22.59 / .533 / .310**. This
   retains the previous gray reflections while resolving its smooth flat.
   Opened the exported hero/macro and the regenerated native turnarounds.
   Keep this refinement, then rebuild the remaining comparisons and complete
   the full command/provenance audit. The exact handoff audit still passes.

   The final matched used view now gives receiver **86/54/34**, luma
   **59.43**, against **81/54/39**, **58.73**. Whole used-view flat is
   **72/51/35**, not that single rectangle. Its rolled-shoulder reflection
   is **73/73/74**; the hero's is **38/36/35.5** and the macro's
   **26/25/26**. Brightest flat deciles remain brown and are explicitly
   separated from those gray reflections. The full-profile, flash-lit stock
   remains a large display mismatch (**188/128/119**, luma **140.38**, versus
   **96/55/35**, **62.20**). Retain it in the sheet and README; do not claim
   whole-stock photographic agreement from the much closer used wrist and
   forend patches. Different incident illumination and finish remain limits.

## Round 2 delivery proof

- `make -C guns/lever` and `make -C guns/lever check` both exit **0**.
  Complete logs are `../../build/look-round2/make-carry.log` and
  `check-rounded.log` beside it. The latter completed against the current
  rebaked maps and exports. The independent `make -C guns/lever repeat`
  also exits **0**, recorded in `repeat-rounded.log`.
- The handoff preservation audit passes: **115 other meshes, 26 bones,
  37 clips, ten complete socket frames**, and the five lower-fillet
  expressions remain exact. The bead's corner-normal roundoff is
  5.96e-8. No accepted wood, lever, trigger, ammunition or rig geometry changes.
- Final source **39,832 triangles**; delivered gun **39,814**, one material,
  three embedded 2048 maps, **12,298,660 bytes**. Cartridge **1,598** /
  **7,302,732 bytes**; case **1,326** / **7,283,888 bytes**. Canonical PNGs
  are **1,890,081 / 2,269,287 / 3,021,758 bytes** for BaseColor/Normal/ORM.
- The 4096/32-sample GPU bake misses **zero** of **4,110,236** checked
  interior texels in all six channels. Full stock/forend reserved regions
  contain zero metallic texels. Escaped/degenerate UV triangles are zero;
  combined family overlap fraction **2.64e-7**, below **1e-5**.
- Construction passes on the finalized asset and the independently
  reconstructed imported GLB: **67 contacts**, **37 clips**, **5,304**
  imported half-frame sweep samples, with the unchanged bounded contact
  policy. Serialization separately compares **5,271** complete affine
  frames and **185** event/end surfaces; maximum posed surface delta
  **1.21e-7 m**. Raw delivered position error is zero, normal-vector error
  **8.53e-5**, UV error **2.98e-8**. Imported custom-normal fan encoding
  remains a separately measured **0.584-degree** limit at a narrow cut.
- The rebuilt 2D scalar contact mask measures **24.67%**, versus photo
  annotation **27.07%**, with one connected region each and both area-share
  axes reported. This is the projected factor **>0.42** metric, independent
  of the corrected darker steel. The historical **25.1% / 27.1%** RGB-mask
  comparison and unchanged contour are not redefined as that new metric.
- Final provenance passes for **735** current exported-GLB image records,
  all **37** decoded real-duration WebPs, **696** strip frames and **87**
  distinct strip images. Opened all distinct poses in four native inspection
  pages, all source/export photo pairs, native details/turnarounds, band and
  ammunition macros, the wear pair, final sheets and all five docs JPGs.
- Final hero object luma p1/median/p99 is **0 / 54.63 / 158.51**;
  **29.40%** falls below 24, with **zero** fully clipped pixels. The main-
  branch Hearth comparison uses the current Bracken cards and cameras from
  `../../build/look-round2/shotgun-calibration/`. Final hero/steel comparisons,
  whole-plate histograms, macro/photo and named wear panels are in
  `renders/final/look-review/`; the final contact sheet is
  `renders/final/contact-sheet.jpg`.
- Docs are **1600 px wide**, **37,663–182,703 bytes**, five JPGs, all kept
  **uncommitted**. Repository check reports **873 source files, zero errors**;
  Python compilation and `git diff --check` pass. No kit or common/gun module
  is changed. Remaining visual limits are the regular walnut figure,
  softened fine relief/lettering at 2048, the flash-stock display mismatch
  and different reference illumination; no additional maps or triangles
  are used to conceal them.

## Look round 3 — receiver continuity, sheen and local carry marks

The third look brief accepts the other finishes and all geometry, motion and
budgets. It rejects the receiver's dark perimeter, orange bright decile and
uniform brushed field. This section supersedes round 2's receiver acceptance.

1. **Color and value first — baseline beside Hearth.** The whole plate's
   middle value is close, but the receiver macro's brightest decile is
   **92/59/37**, saturation **.60**, versus **104/73/57**, **.45**, in the
   used photograph. Its rolled shoulder is **26/25/26**: the black forging
   perimeter visibly encloses a brown, wood-like inset. The baseline and
   accepted main-branch shotgun share exactly the five cards, gray world,
   exposure and reflection flags. The shotgun has a continuous steel response
   and locally exposed gray port edges; the Bracken has a diffuse brown field
   and black shoulders. Preserve the accepted controls, wood and geometry.
   Extend oxide across the external forging, restrict blue to millimeter-wide
   seats, and replace the all-over scratch field with individual carry marks.
   The photo neutral remains the broad exposed bolt flat, native
   (470,166)–(570,177), adapted in linear RGB. It is a reflected estimate,
   not a gray card; highlight widths are not used to infer roughness.

   ![First round-three critique: current hero beside accepted Hearth](../../build/look-round3/before/hero-shotgun.jpg)

2. **Color and value first — source response trials.** The first continuous
   oxide trial removes the black frame, but its hero bright-decile saturation
   is **.512**, still above the photograph's **.444**. Reject that diffuse
   response. Three controlled metallic/roughness variants use the same studio:
   v2 gives hero **74/51/42**, bright decile **75/52/44 / .413**; v3 is too
   dark (**65/42/34**) and too saturated (**.478**); v4 still exceeds the
   target (**.463**). V2's gray-brown body is closer, but its shoulder is still
   paint-like. Thin and burnish the oxide on the exposed rolls, keeping it
   continuous and distinct from actual bare corner patches. Source5's actual
   key-reflection shoulder is **133.5/112/101**, with brightest reflection
   **143/126/117**. Its ring has an arbitrary axial color boundary: reject
   that boundary and derive ring burnishing from the outward front normal.
   Restore more of the accepted warm body hue, and vary thickness/roughness
   with palm pressure, leaving the unhandled field free of brushed striae.
   Eight separate tapered marks now occupy only the central palm and lower
   scabbard sites; at hero scale they almost disappear. The macro resolves
   individual strokes without an all-over parallel texture. Source trials
   are under `renders/look-round3/`; no trial is a delivery acceptance.

   Source6's wider thinning variation made the body too dark (**68/47/36**)
   and increased its bright-decile saturation to **.493**. Reject it.
   Source7 restores hero **72/51/40**, bright decile **79/56/45 / .425**;
   macro **67/47/37**, bright decile **74/52/42 / .440**. The narrow blue
   seats no longer form a broad outline, and ring burnishing follows the
   outward surface rather than an axial painted boundary. Desaturate only
   the exposed shoulder substrate a final small amount before baking, toward
   linear **.145/.135/.130**, so its key reflection is gray with a warm cast.
   The effective oxide flat retains metallic **.45**, roughness **.40**;
   the thinner exposed rolls reach **.72 / .34**. Bare receiver patches are
   linear **.38/.41/.43**, metallic **1**, roughness centered on **.48**, set
   against the Hearth's actual worn edges under identical lighting. Other
   parts retain every node/default/link. The saved-handoff audit passes for
   **116 meshes, 26 bones, 37 clips, ten sockets and 117 nonreceiver finishes**.
   Recheck these source decisions after the 4096-to-2048 bake and GLB export.

3. **Color and value first — first exported candidate, reject the flatness.**
   The full 4096/32 bake and 2048 export retain the source response. Hero
   median **71/51/40** is close to the accepted body value; its brightest
   decile is **79/56/45**, saturation **.425**, below the photograph's
   native-pixel median saturation **.444** (rounded in the brief to .45).
   Macro bright decile **75/52/42 / .440** and matched used view **.444**
   also meet that comparison. The physical key-reflection site gives hero
   **139/130/125** in its brightest decile, macro **136/127/124**: near-gray
   sheen, distinct from diffuse brown. The old rolled-shoulder rectangle
   rises from **26/25/26** to **124/112/106** in the macro. The black frame
   is gone; no blue survives across the front ring. Gray rub brightness sits
   below the Hearth's brighter port rim under identical studio lighting.

   Opened the exported hero beside the main-source Hearth, the full macro
   beside the neutral-adapted used photograph, distributions, reflection
   polygons and both steel macros (`renders/look-round3/export-review/`).
   The new plate distribution is too narrow: the native macro still looks
   evenly coated. Do not accept a passing bright-decile number as proof of
   the whole look. Vary oxide thickness inside the existing carrying-palm
   envelope with elongated cloth pressure, retaining oxide outside it.
   Stronger oxide can be warmer in shadow; thinner contact areas should be
   lighter and less saturated. Keep the sparse individual scratch sites,
   narrow blue seats, gray shoulder reflections and accepted bare contour.

   Source8 restores hero **76/53/38**, with luma p10/median/p90
   **49.23/56.81/69.67**, beside photo **46.10/56.95/72.65**. Its bright
   decile is **92/69/55 / .411**. Native macro review rejects the strongest
   cloth smears: their contrast suggests a mottled overlay. Reduce the
   pressure modulation range without spreading it outside the carrying hand.
   Source9 retains hero **76/52.5/38**, luma **49.23/56.30/68.81**, bright
   decile **91/67/53 / .418**. Macro bright decile is **86/64/49 / .430**.
   The quieter variation remains visible but does not replace the individual
   scratches with a brushed field. Bake this candidate, preserving all other
   finishes and the exact lower-fillet contact field.

   The receiver-mask audit catches a remaining structural issue before the
   second bake is accepted: testing only side/top exposure can miss the
   middle of the front ring's larger R8 roll. Replace that heuristic with
   the signed distance to the original changing R2.2–R8 rounded section.
   The oxide now follows the actual external forging through the whole arc;
   interior machined walls retain protected blue. Stop the partial second
   bake and regenerate it from the corrected mask. No geometry, UV, bare
   lower-fillet field or other material is changed by this correction.

4. **Color and value first — corrected exported candidate.** The final
   exported GLB retains hero whole-flat **76/53/38**, versus used photo
   **79/53/36**. Hero luma p10/median/p90 is **49.23/56.59/68.88**, beside
   **46.10/56.95/72.65**. The brighter decile is **91/68/53**, saturation
   **.418**, versus photo **104/73/57 / .444**. Macro **86/64/49 / .427**
   and matched used-view **84/62/48 / .429** also stay below the photograph.
   Saturation is the median of individual pixel saturations; the saturation
   of the channel-wise median photograph RGB is .452, explaining the brief's
   rounded .45. Neither statistic is substituted for the other.

   The fixed oxide shoulder site reflects the key at bright-decile hero
   **138/128/123**, macro **135/126/123**, and matched used view
   **201/197/195**. These are gray with a modest warm cast. The original
   shoulder rectangle is now **124.5/110/102**, rather than **26/25/26**.
   These two physical polygons are independently recorded: one spans the
   shoulder roll, the other is centered on the actual key reflection and
   excludes both bare upper-corner patches. The front ring is oxide-covered
   across its complete larger radius. Barrel and magazine remain blue-black.
   The primary used-photo flat patch is **79/57/43**, against **81/54/39**;
   wrist/forend remain **41/22/12** and **86/51/34**, unchanged from handoff.

   Opened the native exported hero/macro, hero beside Hearth, both steel
   macros, full used-photograph comparison, HSV plots, reflection polygons
   and named-site overlay in `renders/look-round3/export2-review/`.
   The top and front no longer surround the flat in black. Their oxide sheen
   joins the flat through the rolled surface; gray exposed rubs stay on the
   cupped bottom and isolated corners. They read as satin beside the Hearth's
   brighter port edge under the same five cards. The middle palm marks and
   lower scabbard marks are sparse and individually separated; the other
   field carries no brushed scratch texture. Quiet variation follows the
   hand's envelope instead of fading to blue around every edge.

   Remaining look differences: the used photograph has richer fine oxide
   breakup and incidental damage, while our eight original tracks soften at
   2048. Its direct shoulder reflection is broader/brighter under different
   illumination; the studio is held fixed rather than tuning a highlight
   width to that photo. The accepted wood's regular figure and flash-lit
   full-stock mismatch remain unchanged. Complete the final views, pairs,
   wear evidence, strip provenance and required checks for this exact export.

5. **Color and value first — final studio and motion review.** The final
   hero's object-only luma p1/median/p99 is **0 / 54.85 / 161.78**; **26.98%**
   lies below 24. Maximum RGB is **238/221/224**, with no channel at 254.
   The left hero is **0 / 66.62 / 170.93**, **21.77%** below 24, maximum
   **232/228/227**, again with no clipped channel. The receiver macro also
   has zero fully clipped pixels. The dark race, bore, loading recess and
   underside stay deep; the exposed rolls retain gray reflection without
   washing the body or walnut out.

   Opened the final native studio views, all exported photographic pairs and
   all nine dense-source pairs. The accepted round ears/notch, finished wrist
   beside the mortise, graded hand oil, local dings, crown/bore, blued controls
   and band faces remain intact. Viewed both individual band macros and all
   five ammunition macros. The still/contact/wear sheets and all five final
   compressed docs JPGs were also opened. Every **89 distinct** clip image
   was reviewed across the four `build/final-inspection/clips-*.jpg` pages;
   final provenance accounts for **696** strip frames and decodes the real
   durations of all **37** WebPs. No visible texture sliding, unsupported
   new part or new motion artifact appears. The accepted source/2048 loss in
   tiny lettering, pores and fine oxide detail remains visible in the pairs.

### Look round 3 — delivery proof

- `make -C guns/lever` and the separate `make -C guns/lever check` both
  completed with exit **0**. The full build used the kit's GPU lock for
  baking/rendering, a **4096 / 32-sample** bake and **2048** shipping maps.
  All six bake channels have **zero** missed interior texels out of
  **4,110,236** checked. The stock and forend regions remain dielectric,
  with maximum metallic byte **0** across their complete reserved regions.
- Final exports: gun **39,814 triangles / 12,212,120 bytes**; live round
  **1,598 / 7,216,192**; fired case **1,326 / 7,197,348**. Each has one
  material and embeds the same three-map 2048 atlas. Canonical PNG sizes
  are BaseColor **1,891,947**, Normal **2,269,287**, ORM **2,933,355 bytes**.
  The delivered gun SHA-256 is
  `f6e0357c4bd67db9fd6972514ec34975b1092654c25f9d40c1f46cf5e2173fee`.
- `build/delivery/verify.json` passes for that exact export: family atlas
  coverage **32.21%**, no escaped or degenerate UV triangles, three
  microscopic overlap pairs totaling **2.638e-7** of occupied area, below
  the **1e-5** policy. Median family density is **2,376 px/m**. Raw delivered
  corner positions are exact; normal-vector error is **8.53e-5**, UV error
  **2.98e-8**. Imported topology is **116 closed geometric solids**.
- Construction checks evaluate **67** actual contact probes and all **37**
  clips at **5,304** imported half-frame samples, with zero motion-policy
  violations. The largest measured gap among distance probes is **0.1182 mm**.
  The existing bounded-contact policy and ownership events are unchanged.
  Separate serialization checks cover **5,271** affine frames (maximum
  position error **1.975e-6 m**) and **185** posed surfaces (maximum vertex
  delta **1.206e-7 m**). Those last comparisons prove delivery fidelity,
  rather than physical construction or the photographic finish.
- The optional preservation command,
  `blender -b --factory-startup --python-exit-code 1 --python guns/lever/src/preserve_receiver.py -- --before build/look-round3/before`,
  passes against the saved handoff: **116** identical meshes, **26** bones,
  **37** clips, **10** socket frames, **117** unchanged nonreceiver material
  graphs and all **five** accepted lower-fillet expressions exact.
  The baseline is not a dependency of a clean rebuild.
- `build/final-provenance.json` passes: **735** GLB-derived image records,
  including **696** strip frames and all **37** decoded real-duration WebPs.
  Final images are under `renders/final/`; the overview is
  `contact-sheet.jpg`, gray hero is `hero-gray.jpg`, and the Hearth hero
  comparison is `look-review/hero-shotgun.jpg`. Receiver evidence is
  `look-review/receiver-used-closeup.jpg`, `receiver-histograms.jpg`,
  `reflection-samples.jpg`, `receiver-sites.jpg` and `wear-sites.jpg`;
  `photos/value-patches.jpg` and `pairs/wear-2d-pair.jpg` retain the native
  patch and accepted-contour evidence. Source-photo pairs stay separately
  labeled in `source-pairs/`.
- All five regenerated docs JPGs remain **uncommitted**, as requested.
  Each is 1600 pixels wide: hero **37,936 bytes**, turnaround **52,858**,
  details **183,636**, action **95,210**, Eevee **39,540**. No file exceeds
  the 200 KB docs limit. No kit, shared gun code or other asset was changed.
- Final `python3 -m compileall -q guns/lever/src`,
  `python3 kit/repo_check.py` and `git diff --check` exit **0**; the repository
  check reports **928 source files, zero errors**.

The remaining weaknesses are the fine oxide breakup, incidental damage and
2048 detail loss described in passes 4–5. No new tool or permission is
needed from the lead. The receiver preservation audit is asset-local;
there is no shared-kit or contract change in this revision.
