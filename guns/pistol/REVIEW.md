# PD C9 — form and final finish reviews

The current delivery is the [final finish stage](#final-look-dev--form-accepted-by-the-lead).
The lead accepted the round-three form before look-dev. Round-two/three findings
below are historical; four exported finish critiques and the clean final audit
follow them. Final materials, bake and delivery supersede checkpoint-only claims.

## Historical round-two form and rig review

The cold review was correct. Round one's clearance and serialization checks did
not establish contact, intended animation state or convincing first-person form.
The earlier decision to defer silhouette defects to materials is withdrawn.
Look-dev remains closed. The neutral atlas is a delivery integration proof using
the checkpoint constants, not a finished gun.

## Form acceptance list

Acceptance is based on the rendered views below, with mesh measurements as
supporting evidence. A camera-fit residual is not a form score. Final rendered
pair/atlas review is recorded below after the clean build.

- [x] Slide shoulders carry a broad rounded highlight and the nose a carry bevel;
  serrations stop below the shoulder with rounded ends. Evidence: pass7/left and
  final/right, left, rear.
- [x] Grip reads as a rounded volume with a swell, approximately 22° rake and a
  beavertail. No panel-carrier borders or upper-grip seams. Evidence: pass7/left,
  grip_guard; final/left and grip_guard.
- [x] Guard is a rounded rectangular opening with a squared front, realistic wall
  gauge and an underside finger undercut. The former drilled-looking side hole
  is removed. Evidence: pass7/grip_guard; final/grip_guard.
- [x] Trigger is a curved 7 mm shoe with a separate safety blade. Evidence:
  final/grip_guard and both quarter views.
- [x] Frame has depth and changing sections, with short dust cover and nearly
  flush rear tang. Evidence: orthos/side, top; final/left, right.
- [x] Cover is flush in a shallow closed seat; low sights have visible dovetail
  feet. Front dot is centered in the rear notch from the actual Eye socket.
  Evidence: final/rear and aimed.
- [x] Hood fills the battery port coherently; open action exposes the breech and
  supported recoil guide/wound assembly. Evidence: final/right, open_right,
  partial, returning; open-action photo pair.
- [x] Stop meets its notch in the locked pose. Evidence: left/locked pose strips,
  plus independent opposing-face/contact measurements. Clearance alone is not
  counted as proof of engagement.
- [x] Magazine lips curve over and retain the top cartridge; loaded and empty
  variants show the correct follower/round state. Evidence: loaded and empty
  magazine renders, ReloadEmpty strip, rotated-spawn checks.
- [x] Timed strips show full holds, discrete occupancy and a deliberate reset.
  ReloadEmpty keeps its slide open while the magazine is exchanged. Inspect
  uses a small locked press check. Charge is explicitly an empty rack.

## Visual critique passes

1. **Primary volume, Workbench.** Color/value calibration is unavailable in clay;
   judged the highlight bands first. The 52,466-triangle rebuild had a much better
   molded grip and flush cover, but the hood left a large port gap. A finger-relief
   cut made a small through-opening. Both were construction failures, not texture
   omissions. Widened the hood appropriately and rebuilt clearance around it.
2. **Reduction, Workbench.** Value discontinuities revealed the failed reduction:
   decimating after beveling destroyed the slide/guard normal field. Budget passed
   near 33k but the image did not. Rejected. Reset the slide's normals and moved
   molded-volume reduction earlier.
3. **Guard/control close-up.** Clay value still showed pinched triangles around
   the guard and control recesses. Merely preserving the bevels was inadequate.
   Rejected. Rounded the actual finished cavities as one continuous mold, then
   reduced the surface while transferring its continuous high normal field.
4. **Construction and slow motion.** Black/gray massing was now coherent in clay.
   The physical checks exposed intersecting guide components, insufficient hood
   clearance during a slow rack, and an open upper guard ceiling. Rebuilt the
   telescoping guide bore, magazine upper cavity, guard rear slope/ceiling and
   slow unlock schedule. Added the lower notch lead-out. No skipped contact pair
   was used to make these errors disappear.
5. **Aimed and mechanism views.** Neutral values expose a solid flush rear rather
   than a hollow extrusion. The front dot now aligns through the notch from Eye;
   Eye was lowered 2.2 mm to the optical line. Root motion was removed from Inspect
   so static public references cannot detach. Port-side views confirmed the new
   hood fit. Clay guard/pocket highlights became continuous rather than faceted.
6. **Cycles close review.** Color/value first: the cool slide and warmer frame
   are distinguishable and stay black; the temporary hood is too bright and
   uniform for a used gun. That finish issue remains closed until look-dev. Form
   review caught a genuine error the clay overview concealed: the relief still
   read as a transverse drilled hole. Also saw brass through an exposed web gap
   beside the stop. Rejected both. Opened the relief into the underside and added
   a continuous internal mold web. These repairs were not deferred to normals.
7. **Undercut and final gauge, Workbench.** Value bands now follow an open underside
   scallop, with no side hole. The formerly exposed control gap is closed. Guard
   front thickness reduced into the requested 4–5 mm band. Added small rounding to
   the visible crown edges. Geometry remains below 35k. Pass7 images record this
   last source change; all final images and the neutral atlas are rebuilt from it.
8. **Final photo/atlas review.** Color/value first: the right-side slide patch is
   102.24/255 display luma versus 102.22 in the reference; frame 102.11 versus
   94.41; grip 43.51 versus 107.68. These are view values under different lighting,
   not measured albedos. The grip and uniform bright hood are not finish-accepted.
   The continuous grip/web, underside scallop, flush cover and sight alignment
   survive the neutral atlas. The two right/open pairs show the barrel projection
   and port opening in the correct class range. Our 27 mm slide section remains
   visually deeper than the photographed sample; this is the weakest form match
   and is recorded as a C9 design choice, not photographic identity. The smooth
   frontstrap and original control contours also deliberately differ. Timed
   strips show the slide holding throughout the empty magazine exchange, discrete
   occupancy changes, final lock and reset. Decoded animated WebP durations agree
   with the interface (200/250/2000/2400/1500/600 ms); static idle holds remain
   still images with their source durations in timing.json. The cheap case has
   analytic radial normals, avoiding warped cylinder highlights without extra
   triangles. A last construction review shortened the representative wound segment
   and added a cap shoulder so no coil overhangs its guide at full stroke.

## Response to the twelve review findings

1. **Holds / discrete states.** `kit.weapon.action` now keys the complete pose at
   every schedule entry. Explicit hold boundaries precede movement. Scale state
   uses CONSTANT/STEP. Source and imported pistol each pass intended half-frame
   states, including ReloadEmpty f28/f73, Fire f5, trigger pull/reset and stop
   hold. Compound fixtures also test fractional poses. A fractional slow-rack key
   originally exposed 60-Hz export sampling error; its boundary now lies on an
   integer frame. Do not assume arbitrary subframe bends survive fixed-rate
   animation sampling exactly.
2. **Contacts.** Added the notch and engaging lug, curved feed lips, follower
   support and seated shoulder. Separate surface-distance and opposing-face
   assertions test the actual meshes. The aperture is measured at 7.20 mm versus
   9.92 mm case diameter. Every intended overlap in the sweep is bounded and
   still measured; there are no wholesale prefix skips in the pistol policy.
3. **Visible construction.** Rebuilt continuous molded frame/grip/guard, broad
   slide shoulders/nose, flush rear seat, transverse trapezoid dovetails, lower
   sights, rounded serration ends and supported recoil assembly. The guard's
   underside scallop and internal web were fixed again after Cycles review.
4. **Sockets.** Internal Root stays identity; whole-instance placement is external.
   This retains the rifle's top-level reference paths and bone-riding magazine.
   Tests compare full orientation and position through every clip. Muzzle agrees
   at shot; Ejection lies in the moving port at eject. Eye renders the actual
   optical view. Static effect references are event references, not constraints
   on a silently moving crown during a press check.
5. **Family interface.** `INTERFACE.md` 1.0.0 plus `src/interface.py` declare required
   and optional clips, events, capabilities, start/end states and reload resume
   semantics. Tested Fire → Idle, FireLast → ReloadEmpty → Idle, Charge → IdleOpen,
   normal reload and press-check returns. Material binding preserves imported
   PBR slots; it does not key on Rifle/RifleLens names. A different gun must
   declare its own insertion phases/events rather than inherit pistol timings.
6. **Motion estimates.** The README labels slide stroke, lock, barrel motion,
   trigger/safety/stop angles and release travel individually as visual estimates.
   The right/open photograph pair supports the 34–36 mm displacement range.
   Small Inspect travel has no tilt. ChamberRound follows Barrel. Charge starts
   empty and ends locked open. Feeding and spring compression are not simulated;
   visible guide support and slow holds are modeled and checked.
7. **Kit integration/tests.** Added shared affine/socket/surface verification,
   fresh import, detachable rebasing and action-aware camera/strip helpers.
   Established atlas exporter now optionally ships actions and detachments with
   its PBR material. Static defaults remain unchanged. Compound and actual GPU
   baked-delivery fixtures cover nested rotation/translation, STEP states,
   orientation, loaded/empty extraction and common atlas hashes. All 21 kit test
   files were run from clean fixture directories. The negative bounded-contact
   fixture initially chose a bound equal to its measured penetration; correcting
   that test to a stricter bound made its intended rejection meaningful. Final
   suite: 21/21 pass, including its rerun.
8. **Allocation/atlas.** Fine tabs/marks, most hidden cartridge work and deep bore
   geometry were reduced. Main investments are the 9k continuous frame and 8.5k
   slide. The case is 384 triangles. An actual neutral 2048 atlas reserves separate
   pistol/magazine/case rectangles, uses first-person priorities and rigid-bone
   projection isolation, and ships one material in each of four GLBs. Embedded
   image hashes agree. Runtime texture sharing still needs a consumer cache.
9. **Empty magazine.** Loaded and empty GLBs share the same origin and atlas;
   empty omits rounds and raises the follower. Fresh imports reproduce the full
   rotated Reload/ReloadEmpty f40 spawn, not merely a translation. The magazine-out
   event precedes the offscreen replacement at f47.
10. **Review gate.** Explicit image-based acceptance list above; opposite-side and
    locked-action photos; actual Eye view; uniform timed strips and real-duration
    WebP loops. Seven source critique passes precede final comparison. No primary
    silhouette defect is designated future finish work.
11. **Dimensions.** Slide is now 174 mm; steel sight radius 152 mm. Actual sections
    measure about 30.19 × 50.57 mm and 21.97°. Guard aperture is about 32.89 × 27.01
    mm. The shorter 67.49 mm trigger reach and narrow compact envelope are explicit
    fictional-design choices, with the published 71.2 mm baseline cited.
12. **Build/verification.** Modeled blend, all four GLBs, count data, atlas maps and
    presentation groups are declared Make outputs. Fresh imports check both
    standalone magazines and the case; normal direction is tested against winding
    as well as unit length. Missing-output recovery is tested separately from the
    clean build; results are recorded below.

## Limits carried forward

This is a visual game mechanism. There is no hand rig, physical feeding,
ballistics, spring compression or manufacturing-tolerance model. The two photo
pairs are low-resolution references to a different compact design; residuals
remain visible and do not certify form accuracy. Short trigger reach, the deeper slide section and original
controls are intentional deviations. The deeper slide is the weakest remaining
form comparison. The single neutral atlas also uses one standard PBR specular
lobe; it does not preserve every temporary palette material's specular setting.
Final finish work must use an exportable common response and recheck it. Fine stipple, molding marks, markings,
carbon, polish, hand shine and carried wear remain absent because look-dev has
not begun. The bright, uniform hood and smooth grip are obvious temporary surface
limitations, not final realism claims. The next stage must calibrate used-black
values against daylight photos and review normal/detail loss at full frame.

## Final evidence

- Clean build: removed guns/pistol/build, then `make -C guns/pistol`; passed. A final rebuild
  after the case-normal and presentation changes also passed. All Cycles work
  used the shared GPU lock. No look-dev/wear shaders were introduced.
- `make -C guns/pistol check`: passed source and finalized-atlas geometry, contacts and
  all-clip clearance; intended source/import states; 1,110 affine/socket samples;
  standalone imports/spawns; shared atlas payloads; repository check.
- Every `kit/test_*.py`: 21/21 pass from clean fixture directories, including a
  second full run after tightening bounded-contact broad-phase tolerance. Pure
  tests used unittest; bpy fixtures used Blender; baking fixtures used the GPU
  wrapper. Logs: build/kit-regression/summary.json and individual test logs.
- Deleted build/magazine_empty.glb and ran `make model`: all four GLBs regenerated
  byte-identically. Repeated on the final revision in build/recovery, with all
  four hashes matching both the primary outputs and their rebuild. Deleted orthos/side.png and ran `make orthos`: the complete
  image group regenerated. Evidence: build/round2-recovery.json and recovery logs.
- Native inspection: pistol 33,862 triangles; loaded magazine 3,380; empty magazine
  2,540; case 384. Neutral atlas: pistol 33,846 (16 collapsed micro-triangles removed),
  magazines 3,380 / 2,540, case 384. All remain within their specific budgets.
- Neutral atlas GLBs: pistol 5,188,932 bytes; loaded 2,860,156; empty 2,828,012;
  case 2,761,940. Each has one material and the same three embedded 2048 images.
  Shared compressed GPU allocation estimate: 16 MiB with mipmaps, when the consumer
  caches the common atlas. Inspection GLBs retain the nine temporary palette slots.
- Source and atlas sweeps each sample 1,110 poses, with zero violations and no
  skipped cross-bone pairs. Largest measured overlap is 0.203 mm at a declared
  chamber contact (0.60 mm bound); ordinary pairs retain the 0.20 mm threshold.
  Required contacts are measured separately. Affine round-trip maximum position
  error is approximately 0.000080 mm; maximum linear-matrix error 1.79e-7.
- Image evidence: renders/round2/contact-sheet.jpg, dimensions.jpg, clips.jpg;
  final/aimed.png, right.png, left.png, open_right.png, grip_guard.png, rear.png,
  partial.png and returning.png; pairs/right_photo-pair.jpg and open_photo-pair.jpg;
  atlas/ and atlas-pairs/ repeat the important views with the baked neutral atlas.
  All ten clips have separate strips and real-duration WebP playback in strips/.
- Camera fits: 77.9 mm / 13.31 px RMS (right); 53.9 mm / 12.52 px RMS (open).
  Neither fit reaches a lens bound. Independent Blender projection checks pass.
  These residuals quantify framing disagreement; they do not certify shape.

The checkpoint is ready for the lead's form/rig review. No tools, downloads or
permissions are needed from the lead. Look-dev remains closed.

## Folder split checkpoint

`main` merged before the split. All tracked pistol files moved with `git mv`.
`common/` now owns the reusable renderer, timed-strip generation, versioned
interface/frame checks and photographic camera helpers. The pistol owns its
viewpoints, photographic landmarks, clip binding, contacts and shape. The
interface is still 1.0.0; only its implementation path changed.

From an absent `guns/pistol/build/`, `make -C guns/pistol` passed. Explicit
`make -C guns/pistol check` and `make -C guns check` both passed. The four
inspection GLBs are byte-identical to their pre-move builds (hash comparison in
`build/guns-restructure-reproducibility.json` at repository root). Inspection
pistol: 33,862 triangles; neutral atlas: 33,846, one material, three 2048 maps.
Both construction audits retain all required contacts and 1,110 sampled poses,
with no motion violations. Fresh imported states, sockets and detached spawns
pass. UV regions have no measured overlaps, degenerate UV triangles or escapes.
Repository check: zero errors. Logs are in root `build/guns-restructure-*.log`.

Regenerated round-two views, photo pairs, dimensions and timed strips were
opened and reviewed. They retain the earlier cutout flank, shallow dust cover,
strap guard and oversized-looking feed lips: this commit changes organization,
not form acceptance. `renders/round2/contact-sheet.jpg` remains the baseline.
No kit file or final docs image changed.

## Round three — sculpted form, before look-dev

### Pass 1 — rounded volumes, rejected

Color/value first: the neutral black polymer is still too dark relative to the
low-contrast photograph, while the bare hood is uniformly bright. No finish
acceptance is claimed. In `renders/round3/pass1-pairs/`, the molded volume carries
highlights across its flank and the guard is visibly thicker, but the upper
superellipse falls away from the slide and reveals the rail inserts. The release
surround is egg-shaped; the thumb web has two conspicuous lobes. Those are shape
failures, not material issues. `pass1/left.png` and `grip_guard.png` show them.
The dense/game sections agree closely, but the initial upper grip cut also
intersects the guard and cannot describe a grip section alone. Move it below
the undercut. The bar section is genuinely oval, about 13.74 × 6.68 mm.

The first source sweep caught release travel, takedown seats, blade clearance,
reserve-round fit and magazine withdrawal intersections. All contacts still
passed, but clearance did not. 35,182 triangles is over budget; rejected. The
next pass flattens only the upper seating land, retains a bowed flank, removes
the local release lump, moves the relief above the accepted rake measurement,
and gives each moving part a real recess. No collision threshold is increased.
The guard gauge was independently estimated from photo pixels: a 526 px slide
baseline / 174 mm gives 3.023 px/mm, with about 19 px bottom / 21 px front walls
(6.3 / 6.9 mm, approximately ±0.7 mm). This is photographic side gauge, not a
manufacturing measurement. The annotated picks are regenerated at checkpoint.

### Pass 2 — seating land and control seats, rejected

Color/value first: black massing is consistent, but the temporary metal hood
still clips perceptually against the frame and the smooth grip looks too clean.
The right/open pairs preserve the original cameras. `pass2-pairs/` shows that
the seating gap is repaired, but the frame still presents too broad a planar
highlight. The finite finger-relief tool creates a drilled-looking notch again.
Rejected both. A new continuous curved section replaces the flank's straight
segment, and the guard's round-bar union supplies the saddle without that cut.
The first left-quarter fit reaches its lens bound and is rejected as a camera
comparison. The existing left-side photo is instead leveled on a comparison-only
canvas: the new fit is 76.4 mm / 24.07 px RMS, with neither lens bound reached.
No landmark or camera of the original right/open pair is changed.

### Pass 3 — curved flank and open saddle

Color/value first: `pass3/rake_right.png` and `rake_left.png` now show a curved
highlight below the slide and deep cavity shadow, rather than a cutout's flat
side. The source sweep passes all 1,110 poses without increased tolerances.
The 34,692-triangle mesh is within budget. Guard and grip sections still need
final delivery measurement. The round shoe has thickness, and the safety face
is visible in `pass3/grip_guard.png`. The rectangular release and serrated stop
read as controls, but the large open stop recess remains more schematic than
the photo's compact installation. The rear web still has a two-lobe underside,
and the well flare reads as an added band. Rejected these transitions: replace
local ellipsoids with one broad swept palm-web volume and blend the flare into
the existing grip stations. The next magazine pass opens the rear spine's
U-shaped relief so the cartridge head is visible behind the curled lips.

### Passes 4–5 — web, well entry and magazine

Color/value first: raking-light surfaces remain black, with a broad shoulder
highlight and dark guard interior. The smooth grip and white hood are still
unaccepted finish placeholders. `pass4/` exposed a new cuff-like line where the
web's rounded-rectangle seed terminated outside the grip. Rejected it; the new
web uses the grip's own curved sections, starting inside its volume and ending
inside the upper mold. `pass5/` shows the cuff and stacked lobes removed. The
well flare is now part of the bottom grip sections rather than an added belt.
No grip midsection, rig, socket or clip was moved.

The shoe is measured on actual side surfaces: 4.92 mm at Z=24, 3.62 mm at Z=17,
2.76 mm at Z=7; its face is 7 mm wide. The release gets a rounded molded surround
and a thin body standing about 1.3–1.5 mm proud of its local surround. The magazine's steel lips
are thin curls rather than a cap. A rear U-relief exposes the cartridge head;
the rear still stands above the front. The floorplate is 3.3 mm thick with a
small front lip, rather than the former 5 mm pedestal. Five real witness holes
open through the rear spine. The additional Tony Webster rear-magazine photo
is inspected for this distinction, with source/license in `refs/SOURCES.md`.
The reserve round and cavity were corrected together; no new motion exception
was added. The full pass-five source sweep passes.

The first atlas unwrap rejected 31 tiny overlap pairs at a fraction 1.38e-5.
The narrower 40° projection reduces this below the unchanged kit 1e-5 limit.
This is a real unwrap change; no overlap tolerance was raised. Final bake and
post-import visual acceptance are recorded after the complete rebuild below.

### Final source and delivery critique

The broad seed stations initially retained changes of tangent in the palm web.
The final source uses bounded C1 flow before union/remeshing, preserving the
section extrema while removing the visible bands. The stop stem now runs inside
the molding and connects to its pad through a bent steel bridge. A first attempt
left a thin wall that broke into a slit: rejected after the baked close-up. The
stem/cavity were moved inward, leaving a continuous outer skin. Three actual
exterior ray hits now check that skin in addition to the full motion audit. The
release remains 1.30–1.45 mm proud at the sampled surround points.

The magazine floorplate was reduced again to 27.2 × 40.5 × 3.3 mm. Its seating
contact still passes. The former standalone studio floor clipped the bottom of
the plate; the corrected camera/studio presentation exposes the entire part.
Pistol and case studio ground heights were also corrected without changing the
accepted case geometry. No texture, weathering or finish detail was introduced.

The earlier atlas used the default dielectric specular level rather than the
source polymer's .22. The delivery now retains that existing neutral constant
through the kit's material override/`KHR_materials_specular` support. This is a
source/delivery response correction, not new look-dev. A common atlas response
still cannot reproduce every temporary metal palette's settings exactly.

The exported-normal audit also rejected nanometer-wide Boolean strips in the
bent stop stamping. Welding/dissolving those strips is restricted to that part;
a trial cleanup of every part opened a small magazine hole and was withdrawn.
After UV finalization, near-tangent/opposing corner normals are reseeded on the
actual delivery triangles **before** baking. The independent GLB winding check
is unchanged. No motion exception or clearance threshold was relaxed.

### Eight regions — current differences from the photographs

These are review findings, not a declaration that the asset is finished.
Both dense-source pairs (`renders/round3/sculpt-pairs/right_photo-pair.jpg`)
and baked GLB pairs (`renders/round3/atlas-pairs/right_photo-pair.jpg`) are required
evidence. The eight-region sheet (`renders/round3/regions.jpg`),
source/bake comparison (`renders/round3/source-vs-baked.jpg`) and
actual section cuts (`renders/round3/sections/sections.jpg`) accompany them.

1. **Frame flank and dust cover.** Region 1 (`renders/round3/regions/region-1.jpg`),
   right pair (`renders/round3/atlas-pairs/right_photo-pair.jpg`), and
   open pair (`renders/round3/atlas-pairs/open_photo-pair.jpg`). The shoulder now
   carries a curved highlight beneath the slide; the deeper cover rounds under
   and rises toward the muzzle, flowing into the guard. The source/game cuts
   show changing sections rather than a side-profile extrusion. **Still different:**
   our cover has a fuller belly and broader lower sweep. The retained 27 mm slide
   is deeper than the photographed class sample; this proportion remains visible.
2. **Beavertail and tang.** Region 2 (`renders/round3/regions/region-2.jpg`),
   left pair (`renders/round3/atlas-pairs/left_photo-pair.jpg`), and
   raking left (`renders/round3/atlas/rake_left.png`). The rearward hook and palm
   web are a continuous mold, with no stacked lobes or cuff seam. **Still different:**
   the photograph has a more concentrated hook and tighter inner saddle; ours
   retains a broader, softer web radius. It is no longer a short flat tang.
3. **Trigger guard.** Region 3 (`renders/round3/regions/region-3.jpg`) and
   sections (`renders/round3/sections/sections.jpg`). The bar has a rounded section,
   thicker walls and a generous frontstrap root; there is no drilled relief hole.
   Front/bottom center gauges are about 6.72/5.97 mm, versus the photo estimate
   6.9/6.3 ±0.7 mm. **Still different:** the front is more vertical than the
   photographed slight sweep/hook. The aperture stays within the requested class
   range, but is not claimed identical to the photographed opening.
4. **Trigger.** Region 4 (`renders/round3/regions/region-4.jpg`) and
   grip/guard close-up (`renders/round3/atlas/grip_guard.png`). The 7 mm shoe has a
   curved face, roughly 4.92 mm side thickness near its top, tapering to 2.76 mm
   near its toe, with the blade visibly within the central recess. **Still different:**
   the photo's lower shoe curls back more; ours has a straighter toe. Fine face
   ridges are absent at this gate.
5. **Controls.** Region 5 (`renders/round3/regions/region-5.jpg`) and
   left pair (`renders/round3/atlas-pairs/left_photo-pair.jpg`). The rectangular
   release, molded surround, narrow takedown tabs and thin stamped stop/pad now
   read as their material/construction class. The stem is enclosed, rather than
   displayed as a long flat external plate. **Still weaker:** small softness and
   waviness remain around the release surround's rounded corners. The stop pad's
   outline and original control spacing differ from the reference. This is the
   least polished small molded detail, and is not concealed by a finish claim.
6. **Slide serrations.** Region 6 (`renders/round3/regions/region-6.jpg`),
   raking right (`renders/round3/atlas/rake_right.png`), and the side pairs. The
   regular 3 mm-pitch, approximately 1 mm-deep field has radiused lower ends and
   continues into the top bevel. **Still different:** our narrower, more numerous
   grooves are the original C9 pattern; the photo's field is wider/coarser. Tiny
   bright transitions at the shoulder/dovetail intersections remain in close-up.
   They no longer read as separated groups of cooling vents.
7. **Grip.** Region 7 (`renders/round3/regions/region-7.jpg`) and the three
   dimensioned grip sections (`renders/round3/sections/sections.jpg`). The accepted
   rounded section/rake survive, with raised panel rims and the well flare formed
   in the mold. **Still different:** the photo has finger features and a more
   irregular textured panel boundary; ours keeps its smooth frontstrap and
   original panel outline. Fine stipple is deliberately absent. The bare smooth
   panel is conspicuously less realistic than the used photograph.
8. **Magazine.** Region 8 (`renders/round3/regions/region-8.jpg`),
   loaded (`renders/round3/atlas-loaded/mag_standalone.png`),
   empty (`renders/round3/atlas-empty/mag_standalone.png`), and
   rear spine (`renders/round3/atlas-loaded/mag_rear.png`). Thin curled steel lips
   attach to the shell, the rear U-relief exposes the cartridge head/follower,
   the rear stands higher than the front, the noses stay behind the body's front
   envelope, and the shallower plate has a modest lip. **Still different:** the
   reference rear view has a staggered witness pattern; ours uses one original
   row. The follower is a simplified smooth molded shape. Coating texture,
   labels and handling wear are absent. The source/atlas comparison is not a
   claim of finished magazine materials.

Look-dev remains closed. The surface constants, bright uniform hood, lack of
stipple and absence of carried wear still prevent photographic realism. The
remaining form differences above are recorded explicitly for the lead's review;
the numerical checks do not overrule the images.

### Final checkpoint proof

The form implementation and reproducible presentation scripts are committed as
**2fba268 — `pistol: sculpt compound frame and correct construction`**.

The restructuring commit is **4860305 — `guns: one folder per gun`**. Before
that commit, the pistol was rebuilt with its new `build/` absent. `make -C
guns/pistol`, `make -C guns/pistol check` and `make -C guns check` passed. All four
inspection GLBs were byte-identical across the move. The root worktree's
`build/guns-restructure-reproducibility.json` records those hashes; the associated
`guns-restructure-{make,pistol-check,family-check}.log` files record the commands.
`INTERFACE.md` remains 1.0.0. No `common/` module has changed since that commit,
and this round changes no `kit/` or shotgun files.

After the final geometry and studio-floor corrections, the following completed
successfully, without changing scripts during the build:

```sh
make -C guns/pistol
make -C guns/pistol check
make -C guns check
python3 kit/repo_check.py
python3 -m compileall -q guns/common guns/pistol/src
git diff --check
```

The first three logs are in the root worktree's
`build/pistol-final-{make,pistol-check,family-check}.log`. Repository check:
632 source files, zero errors. No generated artifact or checkpoint JPG is
committed. The GPU lock wrapped every Cycles bake/render.

| Output | Triangles | Materials | GLB bytes |
| --- | ---: | ---: | ---: |
| Inspection pistol | 34,308 | 9 temporary constants | 1,440,344 |
| Baked pistol | 34,276 | 1 | 6,151,696 |
| Baked loaded magazine | 5,256 | 1 | 3,493,300 |
| Baked empty magazine | 4,416 | 1 | 3,459,368 |
| Baked fired case | 384 | 1 | 3,301,624 |

The dense frame is 1,185,828 triangles, reduced to 9,600 on the game mesh.
The 4096/32-sample bake ships three 2048 maps: BaseColor 313,192 bytes, Normal
1,131,841 bytes, ORM 1,826,775 bytes. All four GLBs embed identical image payloads;
the canonical shared atlas costs about 16 MiB compressed with mipmaps when
cached once. The native fired-case GLB is byte-identical to the pre-move baseline.

`build/check.json`, `build/sculpt-check.json` and
`build/atlas-proof/construction.json` each pass all 11 contact/containment
measurements and 1,110 half-frame motion samples. These use actual surfaces and
solid intersections, not only source/export agreement. The largest recorded
penetration is 0.203 mm at the already declared chamber contact (0.6 mm bound);
no new contact exception, skipped pair or looser tolerance was introduced.
The source and imported semantics pass all ten clips, transitions and eight
interrupted-reload resumes. Affine re-import agreement across 1,110 samples has
maximum positional error 0.0000803 mm. That is serialization evidence; it does
not by itself establish correct construction. Independent GLB winding/normal
checks pass for all four delivery files.

The final pistol UVs have no outside or degenerate triangles, 12 microscopic
overlap pairs, fraction 6.00e-6, below the unchanged 1e-5 limit. Magazine and case
have zero overlap pairs. Pistol median density is 2,969 px/m at 2048; the
non-overlapping family rectangles remain intentionally reserved. This is not
a claim of zero pistol UV overlap or final packing efficiency.

The final visual review opened the three source pairs and three baked pairs,
both raking views, all six cuts, the individual close-ups, the magazine front
and rear quarters, the aimed view, orthos and every clip strip. All 192 final
shot metadata records match the SHA-256 of their current source; section JSON
also records both source hashes. Primary evidence:

- Contact sheet (`renders/round3/contact-sheet.jpg`),
  sections (`renders/round3/sections/sections.jpg`),
  source/bake (`renders/round3/source-vs-baked.jpg`),
  eight regions (`renders/round3/regions.jpg`).
- Right pair (`renders/round3/atlas-pairs/right_photo-pair.jpg`),
  open pair (`renders/round3/atlas-pairs/open_photo-pair.jpg`),
  left pair (`renders/round3/atlas-pairs/left_photo-pair.jpg`).
- Aimed (`renders/round3/atlas/aimed.png`),
  grip/guard (`renders/round3/atlas/grip_guard.png`),
  loaded magazine (`renders/round3/atlas-loaded/mag_standalone.png`),
  empty magazine (`renders/round3/atlas-empty/mag_standalone.png`).

Color/value remains the first limitation: sampled slide/frame/grip view luma is
82/105/44 versus the photo's 102/94/108. Different lighting and the missing
microtexture prevent interpreting these as albedo measurements. The right hero
has full-image luma range 0–239/255, and neither it nor the two raking views has
an all-channel-255 pixel. Cavities retain deep shadow, without a washed-out
overall image; the uniform bright hood and smooth grip remain visibly synthetic.
`build/value-review.json` records the patches and percentiles. No finish
acceptance is implied. Stop here for the requested form review.

Nothing additional is needed from the lead to reproduce this checkpoint. A
future kit improvement could expose separate AO and normal-bake sample counts;
the current shared bake path works and was left unchanged.

## Final look-dev — form accepted by the lead

The sculpted frame, serrations, guard, trigger, controls and magazines were
accepted before this stage. The rail presentation was the remaining construction
correction: attached accessory plates were removed; radiused longitudinal reliefs
and the transverse slot are now cut into the continuous frame mold. No rig,
socket, clip, interface meaning or contact exception changed.

### Finish pass 1 — rejected

**Color and value first.** The exported GLB's median slide/frame/textured-grip
view values in the daylight left comparison are 54/72/49, versus 76/67/70 in the
photo. Slide G-normalized RGB is 1.000:1:1.019; frame is 1.014:1:0.986. The
slide is too dark in the comparison, while the hood remains visually too bright
under the studio reflection. These are display-view values, not recovered
physical albedos. The scanned right/open photographs are much flatter and
brighter; they remain additional comparisons, not a reason to bleach both blacks.
Fixed, manually picked patches and all medians/channel ratios are in
`renders/lookdev/pass1/values.json`; the polygon overlays are in
`value-patches.jpg`. The photo, material and geometry paths remain separate.

Pass-one sheet (`renders/lookdev/pass1/contact-sheet.jpg`),
right pair (`renders/lookdev/pass1/pairs/right_photo-pair.jpg`),
open pair (`renders/lookdev/pass1/pairs/open_photo-pair.jpg`),
left pair (`renders/lookdev/pass1/pairs/left_photo-pair.jpg`).
The grip pattern survives the bake but reads too subdued; the molded lettering
is nearly lost. The magazine release has a false vertical wear stripe through
its face because it reused the stop's contact region. Reject that mask. The
next pass limits release wear to its perimeter, darkens the hood's unrubbed
nitride, strengthens the grip's molded relief, raises only the textured polymer's
diffuse response, and reduces the studio's broad upper reflection. Holster
exposure and barrel/slide rub remain the causes of the metal wear.

Every pass freezes its actual four shipped-format GLBs under `build/review/`;
its render metadata carries their SHA-256. Pass one was baked at 4096 with eight
samples and filtered to 2048; finals will use 32 samples. The delivery path reports
zero missed interior texels on all six bake channels, including material micro-AO.

### Finish pass 2 — rejected

**Color and value first.** Daylight-left slide/frame/grip medians improve to
61/72/54 against 76/67/70. Slide RGB is now neutral 1:1:1; the frame remains
warmer at 1.014:1:0.986. Right/open slide medians remain 56/59 against 106/107;
those references have a much higher black floor. The grip relief reads at full
frame and the release's false central stripe is gone. However, the hood still
looks like a bright plate in the port close-up (`renders/lookdev/pass2/port_hood.png`).
An independent UV/texture probe confirms a black top-center albedo (14/15/16
sRGB), but also finds the side rub mask covers the whole exposed right wall.
Reject that broad mask: only narrow contact tracks should polish it. The left
studio strip also sits almost exactly in the top's reflected viewing direction;
move and widen that light rather than hiding the black surface under a white
reflection. Increase the slide's dark conductor response and the grip's diffuse
response modestly; retain the two distinct blacks and deep cavity shadows.
The markings need a clearer cut edge, without light-colored printed lettering.

Pass-two sheet (`renders/lookdev/pass2/contact-sheet.jpg`),
right pair (`renders/lookdev/pass2/pairs/right_photo-pair.jpg`),
open pair (`renders/lookdev/pass2/pairs/open_photo-pair.jpg`),
left pair (`renders/lookdev/pass2/pairs/left_photo-pair.jpg`).
All nine images completed before the orchestration process was terminated;
composition resumed against their frozen GLB hash without replacing the render.

The final measurement method projects an unmarked slide station separately from
the manual photo patch: the fictional text occupies different screen positions.
Pass-one/two metrics were recomputed on their frozen images with this same
method, removing lettering/port bias. Photo polygons never drive the asset.

### Finish pass 3 — targeted correction

**Color and value first.** With the same unmarked slide-patch method, daylight
left is 84/70/58 (slide/frame/grip) against 76/67/70. Slide hue stays neutral,
1:1:1; warm frame is 1.014:1:0.986. The steel now overshoots slightly, while the
textured grip remains too dark. Reduce the nitride response modestly and raise
the textured polymer's diffuse response. Do not brighten the smooth frame.

The hood (`renders/lookdev/pass3/port_hood.png`) finally reads black with localized
rub tracks, rather than a bright uniform block. The changed strip position also
restores a dark rear slide top. The hero (`renders/lookdev/pass3/hero.png`) retains
visible muzzle/front-edge carry wear and deep cavities. The texture survives
normal-map downsampling, but the smooth frame still lacks the restrained hand
polish and fine roughness variation in the used photo. Add these only at the
thumb/web, grip crowns and bottom contact area. A small lint strand is confined
to the sheltered upper texture boundary. Molded/engraved text now reads through
cut edges instead of pale printed letters.

Pass-three sheet (`renders/lookdev/pass3/contact-sheet.jpg`),
right pair (`renders/lookdev/pass3/pairs/right_photo-pair.jpg`),
open pair (`renders/lookdev/pass3/pairs/open_photo-pair.jpg`),
left pair (`renders/lookdev/pass3/pairs/left_photo-pair.jpg`).
The separate Eevee presentation trial exposed a scale-shot setup error: its
small studio wall occluded the figure below the chest. Enlarge only that shot's
studio, keep a true 1.8 m silhouette, and hide Cycles-only reflection flags in
Eevee (which does not honor their camera-ray visibility). This is presentation,
not a change to the gun, scale, exported rig or textures. Check the magazine and
case finishes in the next complete exported pass as well.

### Finish pass 4 — final material gate

**Color and value first.** At 4096/32 samples, shipped at 2048, daylight-left
slide/frame/grip medians are **76.00/70.93/63.21** versus **75.85/66.79/69.57**.
G-normalized RGB is **1.000:1:1.000**, **1.000:1:0.986** and
**1.032:1:0.952**, respectively. The slide has no blue cast; textured polymer is
warmer and its grip crowns and valleys separate. The right/open scanned-photo
comparisons remain darker: slide 70/73 versus 106/107; frame 66/57 versus 89/88.
These unresolved view differences remain visible in the pairs. They are not
claimed to be recovered albedos or exact light matches. No level-remapping of
the reference or render is used to manufacture a match.

Pass-four sheet (`renders/lookdev/pass4/contact-sheet.jpg`),
right pair (`renders/lookdev/pass4/pairs/right_photo-pair.jpg`),
open pair (`renders/lookdev/pass4/pairs/open_photo-pair.jpg`),
left pair (`renders/lookdev/pass4/pairs/left_photo-pair.jpg`),
value/hue patch overlays (`renders/lookdev/pass4/value-patches.jpg`).
The hood's black center and rubbed perimeter now read correctly in the port
close-up. It still reflects a broad studio card from the rear angle, as does
the slide top; this view-dependent reflection is distinct from its black baked
albedo. Carbon stays at the breech/crown, bright rub at the hood's tracks and
contact edges, hand polish at the thumb/web and grip crowns, chafe at the lower
grip contact, and sparse lint in sheltered texture valleys. Carry wear is visible
at full-frame muzzle/front edges, hood and controls, without outlining every edge.
The rail is a continuous molded part with actual dark reliefs, not pale plates.
The small fictional text is engraved/molded; the long serial remains soft at this
atlas density. The grip's original cellular pattern remains more regular and
cleaner than the irregular used photo. These are the weakest finish details.

The loaded/empty magazines retain attached curled lips, contained cartridges,
spine holes and thin floorplates; bright steel is limited to their contact areas.
Brass/copper, follower and fired-case primer remain distinct. The extreme case
close-up exposes its accepted 12-sided silhouette; no case geometry was changed.
The magazine framing is too tight at the top/bottom in this pass: widen only
those final cameras, and add the case-mouth view to show its soot. The final
scale and Eevee setup trials now show the entire 1.8 m figure and gun. The 190 mm
hand-length guide is a size reference, not a grip-fit claim.

Proceed to the clean rebuild and final image audit. Material/geometry changes
are frozen at this gate; remaining changes are presentation and documentation.

### Clean final audit — fifth visual pass

**Color and value first.** The clean rebuild retains the pass-four medians and
hues: slide/frame/grip 76.00/70.93/63.21 versus daylight-photo 75.85/66.79/69.57.
The hero's full-image luma spans 0–219.65/255 with no all-channel-255 pixels;
the hood and grip close-ups also retain deep cavity shadow and highlight rolloff.
The scanned right/open references still have a brighter black floor. Their
mismatch is visible and measured, not removed by grading either image.

Opened the final contact sheet, all three final pairs, every final view, all ten
Eevee clip strips, both magazine quarters and spine details, both case ends, the
scale cues and all five docs JPGs. The main magazine views now include complete
feed lips, cartridge noses and floorplates with breathing room. Spine views are
close-ups of the witness holes. The three required detail subjects and additional
markings view survive the docs reduction. The aimed view still uses the actual
Socket_Eye frame. The size shot shows the entire neutral 1.8 m figure; the
separate 190 mm guide is a readable size cue. Remaining weaknesses are the
regularity/softness of the fine texture and long serial at this atlas density,
accepted broad molding radii, case end faceting at extreme magnification and
Eevee's darker reflections/shadows. No further form or material change followed
the fourth gate.

Implementation: **399df47 — `pistol: finish carry materials and animated atlas delivery`**.
The neutral `atlas_proof.py` stage was replaced by separate preparation,
look-dev, bake and export stages using the same kit APIs. One dense frame is
still the actual selected-to-active source; finish detail adds no game triangles.
The final family index points to this finished pistol. No shotgun file changed.

The generated `build/`, `textures/` and `export/` were moved out before the clean
build. This rebuilt native forms, UVs, procedural materials, 4096 bakes, 2048
maps, all four GLBs and the final renders from scripts. The first final audit
caught an actual playback defect: libwebp optimized static holds into stills and
lost their duration. The guns-only strip writer now preserves the same encoded
pixels in one timed WebP frame. A decoded-pixel check proved the 17 ms hold was
unchanged visually. All ten actual decoded durations now match the clip manifest:
17, 200, 200, 250, 2000, 2400, 1500, 600, 1000 and 1000 ms. This fix is
**903a5b1 — `guns: preserve real duration of static WebP holds`**.

Successful final commands and logs, relative to the worktree root:

```sh
make -C guns/pistol                 # build/pistol-finish-final-make.log
make -C guns check                  # build/pistol-finish-family-check.log
python3 guns/pistol/src/review.py --docs
python3 -m compileall -q guns/common guns/pistol/src
python3 kit/repo_check.py
git diff --check
```

The preceding fresh model/bake/check/render work is in
`build/pistol-finish-clean-make.log`; its initial hold-duration audit failure is
retained rather than hidden. The later complete make and family check both exit
zero. Repository check: 645 source files, zero errors. No kit file changed, so no
kit regression-suite change is claimed.

| Final GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| Loaded pistol | 33,588 | 1 | 8,090,968 |
| Loaded magazine | 5,256 | 1 | 5,453,836 |
| Empty magazine | 4,416 | 1 | 5,419,904 |
| Fired case | 384 | 1 | 5,262,284 |

Native pistol: 33,620 triangles. Final frame: 9,600; slide shell: 8,972.
All four GLBs embed identical three-map 2048 payloads. BaseColor/Normal/ORM PNG
sizes are 742,155 / 1,666,175 / 2,824,016 bytes. Bake: 4096, 32 samples, zero
missed interior texels on all six channels. Normal filtering retains the 16-bit
intermediate before 8-bit shipping. Runtime atlas allocation is about 16 MiB
compressed with mipmaps when cached once. Exact records are in
`build/delivery/verify.json` and `build/baked/4k/bake-report.json`.

Source, dense and finalized assemblies each pass all 11 actual-surface
contact/containment checks and 1,110 half-frame motion samples. The accepted
bounded chamber contact remains the maximum penetration, 0.203 mm within its
0.6 mm declaration. No threshold or exception changed. All ten imported clips,
transitions and eight interrupted-reload resumes pass. Bone/socket affine
round-trip maximum positional error is 8.025e-8 m; loaded/empty magazine rotated
spawn error is 3.332e-8 m. These prove serialization separately from construction.
Independent raw-GLB normal/winding checks pass on all four files.

Fresh UV measurement has zero outside/degenerate triangles and seven microscopic
overlap pairs, fraction 2.529e-6 across the atlas, below the unchanged 1e-5 limit.
Actual atlas coverage is 30.22%; median density 3,277 px/m, with 5th/95th
percentiles 2,648/7,572. Reserved family regions and small-island padding leave
unused area; this is not claimed optimal packing. The pistol-only median is
about 2,932 px/m. This density accounts for the softened smallest lettering.

The clean-rebuild native GLBs match byte-for-byte; dense source positions and
corner normals also hash identically. Repeated GPU bakes differ by at most one
8-bit channel level at 2 BaseColor, 11 Normal and 13 ORM texels. This tiny floating
rounding residual is a repeatability limitation; a bit-identical final-atlas
claim is not made. `build/pistol-finish-clean-repro.json` and
`build/pistol-geometry-repro.json` record the comparison outside the asset folder.

`build/final-provenance.json` passes **173** current-source view/strip records and
all decoded WebP durations. All final make-controlled GPU work honors the
inherited shared `ASSETS_GPU_LOCK`. An early manual trial incorrectly substituted
a worktree-local lock; subsequent make-controlled bakes/renders and the entire
clean final build use the inherited shared lock. No output is presented as proof
of concurrent GPU exclusion from that earlier manual trial.

Primary final evidence:

- Hero (`renders/final/beauty/hero.png`), contact sheet (`renders/final/contact-sheet.jpg`),
  turnaround (`renders/final/turnaround.jpg`), details (`renders/final/details.jpg`).
- Right (`renders/final/pairs/right_photo-pair.jpg`),
  open (`renders/final/pairs/open_photo-pair.jpg`),
  left (`renders/final/pairs/left_photo-pair.jpg`),
  value/hue patches (`renders/final/photos/value-patches.jpg`).
- Aimed (`renders/final/beauty/aimed.png`), locked (`renders/final/beauty/locked.png`),
  scale (`renders/final/beauty/scale.png`), 190 mm guide (`renders/final/beauty/hand_frame.png`),
  Eevee (`renders/final/eevee/hero.png`), clips (`renders/final/clips.jpg`).
- Loaded (`renders/final/loaded/mag_standalone.png`),
  empty (`renders/final/empty/mag_standalone.png`),
  case head (`renders/final/case/case.png`), case mouth (`renders/final/case/case_mouth.png`).

Five final docs JPGs only: hero 101,369 bytes; turnaround 85,193; details 179,055;
action 130,290; Eevee 106,791. Every file is at most 1600 px wide and 200 KB.
The README includes dimensions, construction, finishes, cost, files, complete
socket/pivot tables, clips, rebuild commands, credits and these limitations.

Shared guns-only changes are deliberate: final-GLB metadata/guard, Eevee flag
visibility, an optional mapped engine for real-time strips, and preservation of
static hold timing. The original checkpoint defaults and public entry points
remain. No shared module was renamed; no interface meaning changed.
Nothing additional is needed from the lead. A future atlas-packing improvement
for dense fields of bevel islands would improve tiny lettering without spending
more triangles or texture memory; no kit change was needed to finish this gun.

## Final carry correction — three surface issues only

### Correction pass 1 — exported 2048 textures, crest width rejected

**Color and value first.** Daylight-left slide/frame/grip medians remain
76.00/70.93/63.21 against 75.85/66.79/69.57; their G-normalized RGB ratios remain
1:1:1, 1:1:.986 and 1.032:1:.952. The accepted broad black finishes have not
been raised to make wear visible. The hood now shares the slide's nitride
response and reflects the same studio card, with a clean dark face in the
port view. Compared with the daylight photograph, the first new serration
mask brightens too much of each land and looks too uniformly machined.
Rejected that width: retain just the central crest of each raised land.

The frozen shipped-format GLB and its sources are in `build/review/carry-fix1/`;
sheet (`renders/lookdev/carry-fix1/contact-sheet.jpg`),
hood (`renders/lookdev/carry-fix1/port_hood.png`),
rear (`renders/lookdev/carry-fix1/rear_sights.png`),
daylight pair (`renders/lookdev/carry-fix1/pairs/left_photo-pair.jpg`).
Opened the six studio views, three photo pairs and the magazine/case sheet.
The release now has an edge/pad response rather than round pale stains. The
frame web retains its dark polymer color; polish follows its bearing normals
and changes roughness primarily. The accepted molding radii remain visible.

The hood defect originated in the shader mask, then was magnified by bake
sampling: the front band at Y=63.1 mm had 1.2 mm half-width plus 1.4 mm feather
on each side (5.2 mm total); its side bands were inset from the actual edges.
360/m isotropic noise broke these broad regions into millimeter blobs. With
only about 57 × 110 shipping texels across the top's atlas bounds, those blobs
became blocky gray islands. BaseColor and roughness already contain this
pattern; the tangent-normal top is nearly flat. This is not ray dropout or
legitimate wear. The old shader also made the unworn hood substantially darker
than the slide to compensate for the studio reflection, confusing the diagnosis.

The measured hood top density is 3,275–3,308 px/m (median 3,276) at 2048.
The UV island/layout is retained. Low and high hood share the same surface;
the 0.16 mm cage and 0.8 mm maximum ray distance are retained, and all six bake
channels report zero missed interior texels. New wear lies on the actual
front/side bearing rims, with a 0.5–0.6 mm transition and coherent directional
interruption; carbon stays at the rear breech. No rear picture-frame rub band
remains. No game triangles or atlas resolution were added.

### Measured surface values and immutable delivery

`src/surface_audit.py` casts rays onto the actual finalized surfaces, interpolates
their UVs and samples the shipped PNGs. These are independent measurements of
what ships, not shader constants. Each entry below is the median of its sampled
surface region; BaseColor is sRGB bytes, roughness is ORM G / 255.

| Surface | Before BaseColor | Final BaseColor | Before / final roughness |
| --- | --- | --- | --- |
| Unworn hood center | 14/15/16 | 45/45/45 | .592 / .522 |
| Hood front bearing | 39/40/40 | 81/82/81 | .557 / .408 |
| Unworn slide | 45/45/45 | 45/45/45 | .522 / .522 |
| Front serration crests | 45/45/45 | 74/75/74 | .522 / .439 |
| Palm web | 19/18/16 | 20/18/17 | .569 / .467 |

Final release-edge median is 84/86/84, roughness .392; front-sight top is
93/94/92, roughness .353. The broad release pad remains mostly dark with its
upper contact area lightly rubbed. The palette, markings, magazine/case finishes,
studio setup and camera fits are retained.

The unmodified accepted exports were saved under the root worktree's
`build/pistol-touchup-before/export/` before any edit. The normal Blender export
regenerated one of 143,124 pistol tangent components with a different last
rounded digit (.0686 → .0687, delta .000100002). All other non-image buffers
and the delivery JSON already matched. `surface_audit.py --keep-tangents`
restored that component's accepted bytes only after asserting every other
non-image buffer and delivery-JSON field matched; it rejects any other drift.
The magazines/case needed no preservation. This is an explicit texture-only
refresh step, not a change to the kit exporter or a claim that its tangent
rounding is bit-reproducible across a future clean build.

A second strict read-only audit, with preservation disabled, proves **every
non-image buffer byte is identical** in all four current GLBs: positions,
indices, split normals, tangents, UVs, joints, weights, inverse binds and all
clip data. Complete JSON also matches apart from buffer/image lengths and
offsets. Geometry, rig, sockets, clips, material binding and delivery layout are
unchanged. No kit, common gun module or shotgun file changed.

Reproducible commands, from the worktree root (the saved baseline is only needed
to prove/preserve identity with the preceding revision):

```sh
blender -b --factory-startup --python-exit-code 1 --python guns/pistol/src/surface_audit.py -- --before build/pistol-touchup-before/export --keep-tangents --out build/pistol-touchup-preserved.json
blender -b --factory-startup --python-exit-code 1 --python guns/pistol/src/surface_audit.py -- --before build/pistol-touchup-before/export --out build/pistol-touchup-identical.json
```

The first report records the single preserved tangent; the second is strict
identity proof. `make check` also runs the default read-only surface sampler
into `build/surface-audit.json` inside the pistol folder. The initial failed
identity probes and single-thread exporter experiment remain in root `build/`
logs; neither was used to conceal or relax a geometry change.

### Correction pass 2 — final exported GLB, accepted

**Color and value first.** The daylight-left medians are still
76.00/70.93/63.21 (slide/smooth frame/grip) against 75.85/66.79/69.57, with
the same neutral steel and warmer polymer channel ratios as pass one. New
wear increases local edge response without lifting the broad black surfaces.
The final hero's full-image luma spans 0–227/255, with zero all-channel-255
pixels; the hood and grip close-ups also have zero clipped pixels. The rear
view reflects a bright studio card across both steel tops, but its hood is
now clean and continuous rather than stippled with pale bake blocks. Its
view-dependent brightness is consistent with the adjacent slide.

The narrower serration crest survives 4096 → 2048 filtering and the docs
reduction. In the hero (`renders/final/beauty/hero.png`), muzzle corners, the
leading shoulder, sight top and crest lines now read as carried gray steel,
while groove floors and broad flats stay dark. The
daylight pair (`renders/final/pairs/left_photo-pair.jpg`) is the calibration:
its used pistol has the same localized bright shoulder and crest response.
Our original grooves are narrower/more numerous; their pattern is retained.
The port (`renders/final/beauty/port_hood.png`),
rear (`renders/final/beauty/rear_sights.png`) and
top (`renders/final/beauty/top.png`) show no broad noisy hood perimeter.
Release wear is concentrated at the steel edge and upper pad. The palm web
shows a flowing sheen and a one-byte-scale value increase, not round diffuse
blots. No more surface adjustment followed this pass.

Opened all final studio views, all three pairs and value-patch overlays, every
frame of all ten regenerated Eevee strips (in two-row inspection panels), both
magazine quarters/spines, both case ends, the full contact sheet and all five
docs JPGs. The same baked maps remain bound through the clips, and wear stays
attached to its owning parts. Eevee still has darker reflections/shadows than
Cycles; the fine serial and cellular relief remain soft at the accepted atlas
density. Those existing weaknesses, broad accepted mold radii and the cheap
case's end faceting were outside this correction and remain. Nothing is needed
from the lead. A future deterministic tangent-export improvement would avoid
the explicit preservation step; no kit change was required here.

Final GLBs and current source snapshots are frozen in `build/review/carry-fix2/`.
Pistol SHA-256: `5767252f388c1ad65c7329008e6ceb5ae2d33b3638f2be177f6dcd131ee90927`.

### Correction delivery proof

Successful commands, from the worktree root:

```sh
make -C guns/pistol                 # build/pistol-touchup-final-confirm.log
make -C guns check                  # build/pistol-touchup-family-check-fixed.log
python3 -m compileall -q guns/pistol/src
python3 kit/repo_check.py            # 646 source files, zero errors
git diff --check
```

Both Make commands exit zero. The preceding full render regeneration is in
`build/pistol-touchup-final-make.log`; the confirmation reruns the current Make
graph including the corrected default audit hook. The first family-check attempt failed in the new
audit hook because it assumed an optional Blender `--` separator was present.
The parser now accepts the no-argument Make invocation; its direct default run
and complete family rerun pass. The original failed log remains in
`build/pistol-touchup-family-check.log`. No asset/material check was bypassed.

| Final GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| Loaded pistol | 33,588 | 1 | 8,012,624 |
| Loaded magazine | 5,256 | 1 | 5,375,492 |
| Empty magazine | 4,416 | 1 | 5,341,560 |
| Fired case | 384 | 1 | 5,183,940 |

One identical embedded 2048 three-map set in every GLB. BaseColor/Normal/ORM
PNG bytes: 700,453 / 1,666,260 / 2,787,287. Compressed shared runtime allocation
remains about 16 MiB with mipmaps. GPU bake: 4096, 32 samples, six channels,
zero missed interior texels. Every GPU bake/render used the inherited shared
lock through `kit/with_gpu.sh`.

All 11 actual-surface contacts and 1,110 half-frame motion samples pass on
native, dense and finalized assemblies; maximum declared chamber penetration
remains .203 mm within its existing .6 mm bound. No tolerance or exception
changed. All ten imported clips, transitions and eight reload resumes pass.
UVs retain 30.22% atlas coverage, seven microscopic overlap pairs (fraction
2.529e-6), zero outside/degenerate triangles and 3,277 px/m atlas median density.
Serialization maximum positional difference remains 8.025e-8 m. Strict
baseline-byte identity is separate evidence in `build/pistol-touchup-identical.json`.

`build/final-provenance.json` passes all **173** current-source image records
and decoded playback durations. Final evidence:

- Hero (`renders/final/beauty/hero.png`),
  details (`renders/final/details.jpg`),
  turnaround (`renders/final/turnaround.jpg`),
  contact sheet (`renders/final/contact-sheet.jpg`).
- Right pair (`renders/final/pairs/right_photo-pair.jpg`),
  open pair (`renders/final/pairs/open_photo-pair.jpg`),
  daylight pair (`renders/final/pairs/left_photo-pair.jpg`),
  value patches (`renders/final/photos/value-patches.jpg`).
- Eevee (`renders/final/eevee/hero.png`), clips (`renders/final/clips.jpg`).

Docs JPGs are final only: hero 103,261 bytes; turnaround 86,239; details 181,191;
action 130,804; Eevee 108,058. Every image is at most 1600 px wide and 200 KB.
