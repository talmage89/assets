# Bracken L20 — form and motion review

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

## Final acceptance proof

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
