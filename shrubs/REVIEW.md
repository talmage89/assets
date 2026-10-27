# Foundation shrubs / boxwood look-dev checkpoint

These are source look-dev renders, using original 4096 analytic fields filtered
to the proposed shared 2048 set. No final GLB/bake or delivery acceptance is
claimed. Photographs are local ignored comparison evidence, credited in refs.

## Pass 1 — reject color, perched ball and lost basal stems

Evidence: all seven `renders/pass1/*.png` presentation/diagnostic images opened,
plus both `match_*-pair.jpg` comparisons and preview front/side.

**Color and value first:** the leaves are visibly blue/cyan and too dark beside
both photos. Selected green display luminance p5/median/p95 is
.045/.167/.381 in the Green Velvet camera, versus .100/.321/.539 in the
photo's interior patch. The clipped comparison reads .049/.170/.387 versus
.131/.260/.413. These are different populations/specimens/lighting, not albedo
calibrations. Zero selected-green clipping does not excuse the hue error.
The procedural sky also turns neutral grade/wood blue, so correct illumination
before pushing leaf albedo. Glossy reflections should be local, not a cyan wash.

The candidate reads as a small topiary tree: tapering lower sphere, one visible
pole, and a conspicuous gray polygonal soil plate. The rooted union discarded
six independent basal stems because they were not actually connected. Fine
branches from those discarded parents remain visibly unsupported in structure.
Reject this construction; make all basal stems share a real connected stock,
measure attachments, and preserve the seven leaders. Broaden the lower skirt
and compress its underside into a mound while retaining bare low forks.

Long ladder-like shoots are too obvious. The outer silhouette has sparse fern
spikes with overly regular leaf pairs. Keep opposite botany but vary projection,
axis length, internode spacing and shear-tip foliage. The 1 m camera is too
close for its focal length and clips the object; show a true 1 m near-surface
leaf detail with a deliberately documented field, not a whole shrub close view.
The clipped photo render clips the root patch at the bottom; its framing is
invalid evidence until padded/reframed. Initial 4,131 triangles are within budget;
counts do not compensate for these failures.

## Pass 2 — reject open shell; connected stock and hue improve

Evidence: all seven views on `renders/pass2/contact.jpg`, full-size leaf/base/
structure images and both padded pairs opened. The new neutral margins retain
fit projections and reveal the complete model; both references remain unchanged
inside their canvases.

**Color and value first:** desaturating the procedural sky removes the cyan
wash from leaves, wood and ground. The foliage is now plausible muted green,
but the main reference is warmer and has a brighter middle population. Do not
brighten the whole scene or add emission: increase the blade's green modestly,
keep brown shaded leaves local and preserve the darker underside. Gloss is
still overly broad/matte in the 1 m view; refine after coverage is correct.

The seven basal leaders now join through real stock and the structure diagnostic
has no missing parents. Measured visible foliage spans .993 × .941 m, top .898 m,
with its lowest retained leaf at .138 m. The complete mesh is 1.042 × .987 × .905 m.
However, the shell is visibly too open: large bright see-through holes near
its center and a round lower taper still suggest a decorative topiary. Reject.
Concentrate more of the existing shoot sites at the outer shell, use three
orthogonal planes per shoot instead of two, and make denser short lateral sprays.
A modest triangle increase is justified by coverage at street distance.

The basal soil still looks like a smooth stone plate. Give it original granular
soil/mulch response and an irregular feathered edge inside the same opaque
material. New shoots need their UV V axis aligned to growth instead of relying
on the global up projection. Leaf cards repeat at close range; their size is
within the brief, but projection and shorter varied branch axes need to break
the repeated ladders. At 4,079 triangles this source is a useful rejected stage,
not a look acceptance.

## Pass 3 — hue and mound improve; reject remaining bright windows

Evidence: all seven images on `renders/pass3/contact.jpg`, full-size leaf/base,
three-quarter and both padded pairs opened.

**Color and value first:** warmer blade green is much closer to the primary
photograph than the cyan first pass, and the underside is dark. The close-up
still reads too matte and too uniformly lit, with insufficient waxy roll-off
on individual blades. Restore a stronger dielectric highlight and modestly
lower roughness under the neutralized daylight, then judge highlights rather
than assuming the brighter green alone solved realism.

The denser sprays and three directions improve the clipped mass. Large bright
windows still cross the middle; the photos show dense, dark interior foliage
rather than background. Add a small inner population, plus short lateral sprays
in unused tile space, instead of adding more outer shell sites. No opaque
ball is allowed as an occluder. Preserve shallow pruning lobes and the low
shaded thinning. All added coverage must stay within 6k triangles.

The soil normal field looks quilted in the macro and the low stem UVs enter
its dark strip, creating a sharp brown band. Separate their UV ranges and use
fine low-amplitude granular normals on soil. The basal stock now has seven
visible leaders but needs an independent attachment/closed-wood audit; the
combined soil sheet's allow-boundary flag is too broad a check exemption.
Move the soil sheet to its own source mesh so the woody solids are audited.
Reframe the 1 m camera at an exact 1 m target distance, with a downward angle
that removes the staging horizon. The second photo is lower quality and a
different cultivar; use it for the clipped mass, not detailed blade identity.

## Pass 4 — corrected source checkpoint and stop

Evidence: every current PNG under `renders/checkpoint/` opened, both full photo
pairs, `contact.jpg` and `review-sheet.jpg`. Nine GPU Cycles renders at 1200 px /
40 samples. The 1 m view has an actual camera-to-target distance of 1.000 m.
The scale view uses the unchanged kit 1.8 m silhouette. No docs JPGs committed.

**Color and value first:** primary-camera selected green display luminance
p5/median/p95 is **.073/.310/.561**, versus **.100/.321/.539** in the photo's
interior patch. Median hue **103.28° / 103.53°**. No selected-green channel clips;
**.52%** lies below .02 display luminance. The original cyan wash is gone and
individual waxy highlights now roll off. Model shadows are deeper and highlights
slightly brighter than the primary photo. The second comparison is **.076/.319/
.564**, photo **.131/.260/.413**, with hue **103.02° / 94.74°**: that model view
is brighter and less yellow than this other cultivar's low-resolution photo.
Do not claim both lighting situations or cultivars are exact matches. Statistics
compare different display-image populations, not calibrated albedo.

The inner leafy population and denser short lateral sprays close the largest
bright central windows without adding an opaque ball. Shallow lobes and uneven
shoots interrupt the clipped mound, and low +Y leaves include brown/olive older
growth with less coverage. The lower skirt is broad rather than perched on one
stem. Some small gaps survive, particularly from the shaded side. The silhouette
is still more regular and the leaf sprays less upright/interlocked than the
Green Velvet photo; the 1 m view exposes repeated planar leaves. Those remain
limitations for lead review, not passed photorealism claims.

The first stricter wood audit rejected the core's **negative signed volume**.
Normal recalculation after the tiny grade cap had selected its inner orientation.
The source now measures volume after capping and flips inward faces before
saving. Both independent builds pass zero nonmanifold edges and positive
**0.00085624 m³** total wood volume. All **35 actual four-vertex daughter-base
centers** lie inside the actual primary surface by all three ray tests, with
nearest primary surface **1.47–6.23 mm** inward. This proves embedded bases,
not that all fine attachment caps are Boolean-unioned. The economical closed
fine sweeps still have hidden internal cap faces. No per-sprite twig-continuity
proof is claimed.

Soil has its own source mesh and no longer exempts the wood from manifold
checks. Its granular field is less quilted and the stem UVs no longer enter its
dark strip. The thin polygonal patch edge is still conspicuous in the base macro;
a softer bed transition is needed for final delivery. Basal wood remains angular
at this close distance. Shading and form, rather than pass counts or budgets,
remain the review decision.

### Proof of this checkpoint

- **`make -C shrubs`: passed**, complete source checkpoint, source/game audits,
  botanical checks, camera projection verification, nine Cycles views, pairs,
  contact and value/provenance reports. Every Cycles operation held the shared
  GPU lock. **`make -C shrubs check`: passed** explicitly afterward.
- **4,893 triangles**: **3,794 leaf / 1,082 wood / 17 soil**; **1,897 alpha cards**,
  **two materials**, **three source meshes**. Opaque wood/soil consolidation is
  final-delivery work. No moving parts or armature.
- Actual retained foliage **1.02109 × .98092 m**, bottom **.11181 m**, top
  **.88021 m**. Complete card-corner envelope **1.10102 × 1.03837 × .90659 m**.
  Origin on grade; numerical lowest Z is −3.4e−9 m. Bounds use actual alpha
  texel-center support on actual quads, not authored envelope constants.
- Original 4096 fields filtered to shared **2048² BaseColor-alpha / +Y Normal /
  ORM**. PNG bytes **654,733 / 1,290,223 / 134,896**; packed source
  **2,276,380 bytes**. Planned full-mip BC7/BC5/8-bpp ORM allocation **16 MiB**
  for both shrubs together, excluding geometry/engine overhead. Upper-right
  atlas space remains reserved for hydrangea.
- Independent source/game geometry SHA-256 agrees:
  `7d5127eb3d2dd31104c5947175ec89e1e459e094283c978a509957dc073ec55c`.
  Wind values finite/normalized and zero-sway at grade; actual normals unit;
  alpha UVs remain in their declared lower-half tiles. Card density
  **3,701–3,910 px/m** at the proposed delivery size. Unique final stem UVs,
  final bake and GLB checks are deliberately pending.
- Both anatomical fits retain their estimated-lens RMS **16.11 / 18.78 px**;
  independent Blender projections agree to **.00011 / .00029 px** after framing.
  Different living specimens and uncertain anatomical anchors limit the fit.
- All nine image metadata hashes match current source SHA-256
  `b7ac0d897901d097cc2430d5af3aac3227d227e62e879d0b90925e3d79413e65`.
  `renders/checkpoint/render-check.json` certifies source provenance only.
- Current images: `renders/checkpoint/{three_quarter,side,close_1m,scale,base,
  shaded_side,structure}.png`, `match_{green_velvet,clipped}-pair.jpg`,
  `contact.jpg`, `review-sheet.jpg`, `tonal-check.json`, `shots.json`.

### Shared kit changes and compatibility

- `7458a56`: move the maple thin-leaf material into `kit/foliage.py`, with
  optional species gloss/transmission/back-color controls. The original maple
  default graph's nodes, links, values and properties have an identical golden
  byte snapshot; `kit/test_foliage.py` passes.
- `2aded7e`: move the maple comparison framer to `kit/photo_frame.py`. Its
  original default JSON and generated PNGs compare byte-identical; optional
  vertical margins preserve camera projection. The maple's wrappers retain
  existing entry points. **No change to `kit/rules.mk`.**
- Full maple source rebuilt twice, with pre-extraction and current material.
  Exact positions, triangle indices, corner normals, UVs and Wind share digest
  `01a3f2577af1c5635cf2796aa3916ca2fc8ae9dc5819fa7fdc3aeee0490a2967`;
  all three analytic atlas PNG SHA-256 values also agree. Evidence:
  `../build/maple-extraction-regression.json`. This is full source/content
  compatibility; GPU rebake/export was not repeated and is not claimed byte-identical.
- `kit/test_botany.py`: passed both union component policies and optional normal
  defaults. `python3 -m unittest kit.test_delivery`: **six tests pass**.
  Repository rules and `git diff --check` pass.

Stop here as requested. Hydrangea botany/reference photos are researched but no
hydrangea geometry is built. Final unique UVs, GPU stem bake, GLB/re-import,
wind serialization and exported-GLB renders remain held. No tool or permission
is needed; the lead's review of this boxwood checkpoint is the next decision.

# Lead-directed boxwood correction, then hydrangea

The lead rejected pass 4's appearance. Its whole-crown selected-green median
was not an adequate test of the pale gray film across the lit front. Prior
claims that the shell read as boxwood are superseded by this review.

## Boxwood fix 1 — reject sparse shell and over-dark diffuse response

**Color/value first:** spatially matched lit/front patches now include gray-green
highlights (G/R >1.015, G/B >1.025), rather than excluding low-saturation sheen.
The rejected checkpoint's front-patch median is .384 versus photo .361;
brighter-half median .493 versus .440, saturation .435 versus .571. This
quantifies the lead's visible gray film. The photo is overcast; brightness
populations are not an illumination/reflectance calibration.

Lowering specular .40→.12 and changing leaf projection removes the film, but
fix 1 overshoots: patch median .239, brighter-half .323 and saturation .776.
Do not accept it as "deep green" merely because it is darker. Raise diffuse
blade values and reduce excess chroma while retaining small sharp highlights.

All seven views, the contact and both pairs in `renders/boxwood-fix1/` were
opened. Twenty-four 7–11 mm basal stems replace the seven thick leaders; daughters
branch within the low stem region. The outline is now a dome widest at the
skirt. Dropping the soil patch makes the stems meet grade cleanly. But shrinking
the card sprays exposes severe bright windows and visible upright wood.
Reject the sparse shell. Fill more of each existing tile with short individual
6–10-leaf sprigs, retaining varied normal/projection angles. This adds density
without geometry or a solid-ball occluder. Check the next pair before moving on.

## Boxwood fixes 2–4 — restore dense sprig grain; calibrate lit patches

**Color/value first:** fix 2 loses the gray film but is still too dark/chromatic:
front-patch median .292 versus .361, brighter-half .397 versus .440, saturation
.787 versus .571. Fix 3's brighter diffuse palette overshoots: .385/.504 and
saturation .528. Reject that pale candidate rather than accepting the convenient
whole-crown statistic again. Fix 4 interpolates diffuse color with unchanged
small-highlight specular: **.351/.468**, saturation **.628**, versus photo
**.361/.440**, **.571**. Highlight population remains about 6% brighter under the
procedural directional daylight than this overcast photo, but the broad gray
film is removed. Display-image populations are not calibrated reflectance.

All fix-2 views and pairs were opened on the contact, with 1 m and primary pair
also inspected full size. Fix 3/4 use two targeted source views and both pairs;
all were opened. Each normal tile now contains short distinct 6–10-leaf sprigs
with mixed projection/cup directions, rather than large blades laid flat across
one spray. Reusing more tile area strengthens grain without new silhouettes.
A deeper inner leaf population screens lower windows; move it lower/wider in
the final source so the source's understory becomes pockets of shade, not grade
showing through. This modestly raises total triangles from 4,893 to 5,588, still
inside 6k; no texture/material allocation increases.

The rooted fan now has 24 slender stems plus 32 low daughters; the broadest
clipped section is at the skirt. The polygonal soil patch is removed. Some
sprig repetition and a few overly even new shoots remain, to be reassessed in
the final combined source renders after hydrangea development. No bake is run.

## Hydrangea pass 1 — reject bouquet form and dotted flower caps

**Color/value first:** individual source leaves read lime and too evenly bright;
flower caps are pale blue. The house reference has substantial medium/dark
foliage and deep interior pockets. The first sampled house-head patch is .678
versus .400 photo, but that comparison includes different head exposures; this
is a diagnostic miss, not a final reflectance target. Initial narrow leaf patch
coordinates accidentally select deep photo shade despite a "lit" label. Replace
that invalid label with explicit broad plant-region populations and a separately
marked shaded patch; do not use it as a sunlit albedo calibration.

Every view, contact and both full pairs in `renders/hydrangea-pass1/` were
opened. Reject: the plant is a bouquet of long stalks with all heads above its
sparse body. The clusters are open, overly regular dotted caps. Leaf grids show
curvature and veins, but the tall straight stem run destroys shrub scale.

The correction spreads the main stems early, lowers outer heads, adds low
leaf-bearing daughters and opposite nodes, and spends fewer triangles per
cupped blade so more leaves can fill real stem masses. Smaller, denser florets
have radial-depth and angle variation. No opaque floral sphere is used. Target
about 5.5k triangles, two materials, the accepted shared 2048 allocation.

## Hydrangea passes 2–3 — source form, coverage and color corrections

**Color/value first:** the house-camera broad foliage median improves .449→.412
between passes 2/3, but the photo population is .101; source remains far too
bright/open relative to that sunlit house specimen's deep mass. Janke's brighter
bed is a different target: .443→.344 model versus .376 photo. Flower medians
.627→.599 versus .372 house; .602→.583 versus .526 bed. Different specimens,
exposures, mass depth and selected regions matter: neither global number proves
a calibrated albedo match. Reject the evenly bright source response and sparse
mass against the house photo; do not claim the bed median alone proves realism.

Every view in both contacts, the close-ups and both full pairs were opened.
The early-fanning stems and low branches remove the bouquet's long bare foot,
but pass 2 remains skeletal above the middle. Pass 3 adds more opposite leaves
on physical cupped grids, with varied orientation, and replaces coarse single
florets with smaller three-floret clusters on the same atlas space. Head grain
improves, while some heads still have visible gaps and the upper foliage needs
more interlocking. Two source materials and one family atlas are retained.

Final correction: use the remaining triangle allowance for upper foliage,
expand/interlock the floret patches around complete heads, add the short leaf
petiole to the original alpha field, and start that field at the actual shifted
parent station. This removes the apparent blade/stem gap. Slightly deepen the
mid-green blade palette. Retain open dark cavities rather than sealing a single
envelope. Physical stem/leaf organization and final appearance are checked
separately. Final source renders and values follow below.

## Hydrangea passes 4–5 — reject exposed core cards; measure construction

**Color/value first:** pass 4 has darker leaf pockets but remains too evenly
lit against the house photo. The corrected stem masses and shaded foliage are
closer to the brighter foundation-row photo. Never claim both references'
shadow values are interchangeable; retain both measurements in the final report.

Pass 4's targeted views and pairs were opened. Its new dimension check rejected
several heads at only 13.7–14.0 cm maximum retained extent. Restore their authored
radius and enlarge floret patches so actual retained heads fall in the specified
15–20 cm range. Two comparison renders also clip the plant skirt/left edge;
those old frames are invalid. Wider symmetric neutral study margins keep the
same calibrated camera/pixel projection while displaying the whole asset.

The first dense core-card trial (pass 5) hides the blooms and exposes giant
flat sprays on the outside. Reject it. Restrict those economical branchlets to
the interior (.32 m centerline reach, .25–.74 m height); keep individually curved
blades on the visible outside. Replace the trial's broad generic normal waves
with the actual original blade rib/cup normals rotated with each reused blade.
The leaf-tile composite only reads our own analytic pixels; no photo is read.

The completed construction audit independently finds all **664** pass-4 curved
blade petiole starts inside their actual parent stems, with all three ray
parities agreeing. This is stronger than checking two stored anchor constants.
The final mixed representation will repeat this check for its retained curved
leaves and report core sprites separately. All solids, Wind data, actual head
sizes and source/game agreement remain independent acceptance gates.

## Hydrangea pass 6 — retain interior depth; consolidate family materials

**Color/value first:** confining six-blade branchlet cards to the interior
changes the house-camera foliage median from the pale early passes to .249
versus .101 photo. Its brighter-half population is .353 versus .334; the marked
low shaded patch is .069 versus .075. The whole-plant median mismatch therefore
also records too little shaded area, not simply a diffuse-color error. Flowers
are still .569 versus .372 in this darker house photo. In the brighter bed,
foliage is .234 versus .376 and flowers .544 versus .526. These conflicting
exposure/shadow populations are retained, not averaged into an invented albedo
calibration. There is no channel clipping in the measured model patches.

The three-quarter, 1 m view, both complete pairs and then all seven views on
the full contact were opened. Deep interlocking leaf masses now replace the
exposed giant sprays of pass 5; individually curved outer blades keep physical
leaf shading. Heads read as complete individual masses with nodding variation.
The actual alpha-supported head extents are 16.7–19.5 cm. The final representation
uses 5,222 triangles, including 1,116 in wood and 4,106 in foliage/sepals. All
372 outer petiole starts lie inside their actual parents (three parity rays);
102 two-plane interior branchlets are explicitly a sprite approximation.

Remaining tells: outer blades repeat one silhouette/vein field too visibly;
sepal contours are too similar and some heads too evenly spherical. Card
intersections and a few straight-looking stalk runs remain visible at 1 m.
The house photograph has more flowering mass and a broader continuous low
skirt. This is a source look-dev review, not a finished asset claim.

The final family assembly exposed a material-budget issue: the two plants had
slightly different leaf response graphs. They now use one family foliage
factory with the boxwood's calibrated response, plus one shared wood factory.
The cross-species check compares actual node/default/link/image signatures;
two definitions cover the entire family. Species roughness, normal detail and
color remain in their shared atlas tiles. Rerender both plants after that
consolidation. A silhouette-edge check also caught the second boxwood pair's
clipped bottom skirt; increase neutral framing margins while keeping the
calibrated camera projection. No bake or export is run.

## Boxwood final correction check — complete source views and pairs

**Color/value first:** with complete comparison framing, the Green Velvet lit
patch measures **.351 model / .361 photo** median display Y, brighter-half
**.469 / .440**, saturation **.629 / .571**, hue **108.9° / 102.4°**. The broad
sage film is removed; highlights remain about 6% too bright, with a slightly
cooler/more saturated green than the photo. Its low shaded patch is **.296 /
.245**. The different clipped cultivar is darker/yellower still: lit **.361 /
.291**, shaded **.318 / .200**. Do not describe those residuals as a perfect
photo match or a calibrated reflectance measurement. The spatial mask includes
low-saturation green glints, unlike the rejected whole-crown selection.

All seven daylight views on the final boxwood contact and both pairs were
opened; the 1 m, base and pairs were also inspected at larger size. Fine sprig
grain and dark inter-tuft pockets now read at full-shrub distance. The low dome
is widest in the .158–.238 m height band (1.035 m alpha-supported X width), not
at mid-height. Retained foliage reaches .060 m above grade, with its top at
.867 m. Twenty-four slender grade-cut basal stems replace the old seven leaders;
32 daughter centers lie inside actual parent surfaces. There is no soil polygon.

Remaining tells: the outside is still more regular than the photographed hand
shearing; its low skirt has a few small see-through windows, and the 1 m view
reveals repeated fine sprays and planar leaves. The source correction uses
5,588 triangles (936 wood, 4,652 foliage), within the cap but above the accepted
old 4,893-triangle candidate. The extra 695 triangles fill low/interior pockets
and support finer grain without adding material or texture allocation.

## Family checkpoint — final shared-material render audit

**Color/value first:** the common material slightly changes hydrangea's broad
house foliage/head medians to **.254/.574**, against **.101/.372** photo; its
marked shaded pocket is **.083/.075** (model/photo). The bed comparison is
**.237/.376** foliage, **.549/.526** heads and **.181/.126** shade. Its house
brighter-half foliage is .361 versus .334. Keep the dark-house mass discrepancy
and repeated blade/sepal forms as unresolved look-dev weaknesses. Boxwood's
final measurements above use the complete, wider pair canvases.

All eighteen final views were opened on the combined sheet, plus the final
hydrangea 1 m view and the full photo pairs. No source geometry or texture was
changed after these renders. The edge check still found five opaque pixels at
the second boxwood pair's bottom edge with .20 vertical margins. Reject that
frame, increase vertical margins to .36 and rerender both boxwood pairs. The
complete-pair check then passes for all four comparisons. The reference pixels
and fitted camera pose remain unchanged; only neutral study margins expand.

Proof: `make -C shrubs check` passes all checkpoint audits, including actual
stem solids/attachments, 372 hydrangea petiole starts, normals, Wind, camera
projections and repository rules. `make -C shrubs match check-framed-cameras
contact family-contact` passes after the framing correction. Both scenes have
exactly the same two material node/default/link/image signatures. Each of the
nine render metadata entries per species agrees with its current packed source
SHA-256. The combined sheet and `family-check.json` live in
`renders/family-checkpoint/`; PNGs and sources remain ignored rebuild outputs.

Final counts: boxwood **5,588**, hydrangea **5,222** triangles. Both share the
same three original 2048 maps, **16 MiB** with full mip chains at BC7/BC5/8-bpp
ORM. The curved-grid botanical fixture passed default, connected and curved
card cases; existing maple entry points are unchanged. Bake, unique wood UVs,
GLB export/re-import and final docs JPGs are deliberately not run at this stop.

## Finishing source correction — 36 heads and layered, curved leaves

**Color/value first:** the first revised source pair (`renders/fix1/`) measures
bed heads .395 versus .526 photo, house heads .449 versus .372. The former
bright blue has become dusty lavender/blue with scattered mauve. Bed leaves
.188 versus .376 are too dark; house .185 versus .101 remains brighter in its
middle population. These exposure differences are retained. All seven source
views were opened on `inspection.jpg`, the 1 m view full size, and both full
photo pairs. This source review does not count as an exported-asset critique.

There are 36 heads over the top and sides, 15 nodding. The first revision is
still too perched at its top, with coarse smooth sepal ellipses and an exposed
basal fan. Add leaf pairs close below terminal heads and one more interior low
tier; keep the outer small leaves physically cupped. Increase only hydrangea
leaf albedo, reduce sepal albedo further so individual lit heads can be checked
against .53, and add uneven sepal rims/fine rib relief. Broad blades now vary
about 8–15 cm; three green tiles and a low yellow tile break the repeated paddle
surface. Four-triangle blades keep their real normals. True broad-leaf backs
receive a paler, matte response selected by UV; accepted boxwood tiles remain
unaffected. No extra triangles or maps are used for veins/teeth/sepal crinkles.

### Delivery setup rejection — stem UV fragmentation

The first finalizer run rejected tiny isolated stem UV faces: unique coverage
.0097, median 220 px/m. Add longitudinal and cap seams to the existing stems,
unwrap against the reserved region's actual aspect, and use .0005 packing
margin. The revised actual pack measures .03525 whole-atlas coverage, median
419 px/m (p5/p95 395/437), with zero overlaps. Most pixels are deliberately
reserved for reused cards; a whole-atlas .20 coverage floor was inappropriate.
The kit now honors the already-existing family `UV_MIN_COVERAGE` setting in
finalization as well as verification, retaining its .20 default. The real atlas
fixture passes its previous export and a new small-region packing case.

## Export critique 1 — color holds; reject grade and card-fringe defects

Evidence: `renders/export-pass1/{hero,side,close_1m}.png`, its contact, both
photo pairs and head-value windows. All were opened; the macro and bed pair
were inspected full size. This is the actual embedded-map GLB, not the source.

**Color/value first:** house foliage/heads .268/.393 against .101/.372 photo;
bed .263/.377 against .376/.526. Head-window medians span .205–.516 in hero,
.215–.508 in the house camera and .240–.464 in the bed. Each is below the .53
reference median; individual glints are not a .53 pixel clamp. Display values
remain lighting/specimen comparisons. The matte paler leaf backs are visible
and the green highlights are now brighter than the shaded flower surfaces.

The new ribs/serration survive export at 1 m and head grain reads at the hero's
roughly 3 m camera distance. The heads still sit in too obvious an outer ring;
the top remains a little comb-like. Move six existing daughter terminals inward,
vary upper stem heights and make heads slightly oblate/uneven. This redistributes
the same 36 heads/triangles rather than increasing the silhouette budget.
The white vein network still looks drawn: use a recessed analytic vein field
with dark secondary grooves instead of bright secondary lines.

Reject two measured delivery defects. The low core-card trial has a corner at
−.071 m: restore the .25 m interior-center floor while retaining the extra tier.
The verifier also catches six zero-length normal texels in near-transparent
core-card fringes. RGBA resizing amplified their color components. Reconstruct
those card normals in the positive tangent hemisphere and give discarded fringe
texels flat normals before the ordinary vector downsample. Never waive the
normal or grade checks. This rejected GLB is retained only in ignored build.

## Export critique 2 — redistribute the blooms; preserve measured relief

Evidence: all five PNGs in `renders/export-pass2/`, its contact, both full pairs,
hero and 1 m close-up. **Color/value first:** house leaf/head medians .220/.396,
bed .213/.374. The brightest head-window median is .527 in the 1 m shot; all
hero/pair window medians remain below .53. Flower saturation in the house pair
is .313, versus .268 photo: dusty but still somewhat more saturated. None of
the measured model channels clips. Keep these residuals explicit.

Moving six existing heads inward and lowering some upper terminals replaces
the empty central rosette with overlapping flowers among foliage. Slightly
oblate, uneven heads have visible sepal grain at the 3 m hero camera. Opposite
outer pairs now alternate 90 degrees around the stem instead of both aiming
outward. The normal-derived recessed veins read at 1 m; the former drawn
white network is gone. Dark small pockets remain among overlapping tiers;
paler matte backs and a few low yellow leaves read without a pale overall wash.

The independent GLB verifier now passes normal texture vectors, overlap,
density and all PBR/alpha checks. The source grade audit still rejects one
**transparent core-card corner at −4.55 mm**, measured on vertex 2452/face 817,
not a wood root or a petiole. A square can reach its half-diagonal below its
center after roll. Set the core-center floor to .265 m (above the .255 m
half-diagonal), retaining its .36 m size and the same triangle count. Do not
relax the grade assertion. Final full views and the third export pass follow.

Remaining visual tells: the blades are still tidier and the heads more
spherical/regular than the photos; the 1 m close-up reveals repeated sepal
patches and occasional intersections. Keep those as budget limitations, and
check the complete turnaround/Eevee before final docs.

## Export critique 3 — complete Cycles views; reject washed-out Eevee

**Color/value first:** the final 1600 px Cycles pair retains the boxwood's deep
green: .348 lit versus .361 photograph (accepted lower-resolution source .351).
The accepted geometry/normals/Wind hash remains
`13e52dab7f2043a29e22c190fd068125017a6d78385f9ac1f589fc35acaccc8d`;
all three lower foliage atlas regions compare byte-identical. The modest
measurement difference is not an intentional recolor. Hydrangea house leaves /
heads are .220/.396 versus .101/.372; bed .213/.375 versus .376/.526. Its shaded
patches are .112/.075 house and .103/.126 bed (model/photo). The darker house
still has more shaded area than the model; the brighter bed's whole population
is much brighter. Do not claim a universal photo match.

Every final Cycles view was opened on both inspection sheets, plus both heroes,
all four full exported photo pairs and the 1 m details. The low skirt, dense
opposite leaf tiers, visible ribs/serration and uneven sepal clusters survive.
The .265 m core floor passes the real grade assertion. All 408 outer petiole
starts are inside their actual parent wood with three agreeing parity rays.
Thirty-six actual heads measure 16.7–20.9 cm maximum retained extents; the
largest tips exceed the nominal 20 cm by 9 mm, explicitly retained in README.

Reject the first Eevee boxwood: its selected-green median is .522 versus .312
Cycles, with pale interior foliage and inadequate occlusion. Keep materials and
geometry fixed; enable Eevee ray tracing and screen-space ambient occlusion at
shrub scale. The 1000 px study drops to .339, p5/p95 .193/.562 versus Cycles
.107/.567. It retains the waxy glints while restoring dark pockets, though its
shadows are still shallower. Re-render both final Eevee heroes using that setup.

The Wind audit's apparent mismatch is independently diagnosed as a nearest-
vertex ambiguity: opposite blades meet at a shared petiole position but carry
different flutter and split normals. The shared audit now matches both data
fields on one coincident candidate. Its real export/import regression accepts
that case and rejects a deliberately corrupted mask; tolerances are unchanged.
Actual family position/Wind errors are zero, maximum normal vector difference
8.42e-5. This proves serialization, not botanical correctness or appearance.

## Export critique 4 — final presentation and limits

**Color/value first:** all nine hydrangea views have projected head-window
medians below .53; the maximum is **.527** in the 1 m detail, hero **.425**, house
**.493**, bed **.463**. These are sampled visible color populations in projected
windows, which may include neighbors, not isolated object IDs or a pixel clamp.
No measured model channel clips. The final heads are muted blue/lavender/mauve,
with paler floret centers, and shade falls below bright green leaf surfaces.

Opened the final family contact (14 presentation Cycles and both Eevee views), all four
exported pairs, the final Eevee images, both 1 m images and all five docs JPGs.
The Eevee shadows remain shallower than Cycles but no longer wash out the crown.
The full turnaround exposes the remaining form limits honestly: hydrangea has
fewer exposed flowers on its back, some upper heads still show straight necks,
and its basal fan is visible from low front/back views. These are weaker than
the best photographed dense beds. Individual blades and florets remain tidier
than real growth; repeated sprites and card crossings show at 1 m. Boxwood's
accepted clipped dome remains more regular than the reference's hand shearing.
No geometry or atlas recolor is applied to that accepted shrub.

The delivery is one ordinary family GLB with two rooted nodes, two materials
and exactly three shared embedded image identities. Loading the library once
and instancing the selected root keeps one image allocation in the engine.
`_WIND` survives raw accessors and fresh import without albedo vertex colors.
The README distinguishes that portable PBR delivery from the documented engine
thin-leaf response used by the final renderer; wind deformation/LOD integration
remain engine responsibilities, not animation supplied by the GLB.

### Final proof

- **`make -C shrubs`: passed; `make -C shrubs check`: passed**, explicit final
  runs. Source construction/camera checks, actual GLB/UV/PBR verification,
  botanical serialization, bake-loss and repository checks all pass.
- **Boxwood 5,588**, **hydrangea 5,908** triangles; **two shared materials**,
  **three 2048² embedded images**. Family GLB **6,066,148 bytes**. Shipped PNG
  bytes BaseColor/Normal/ORM **1,052,212 / 3,297,050 / 271,948**.
- **16 MiB** estimated compressed full-mip texture allocation shared across
  both species; **1,437,872 bytes** actual geometry accessors, about **17.37 MiB**
  combined before engine overhead. The shared audit now reads embedded PNG
  dimensions; its 512 fixture correctly reports 1 MiB instead of assuming 2K.
- Final unique stem UV coverage **.02946**, density p5/median/p95 **363/386/402
  px/m**, zero overlaps. Reserved analytic card UV reuse is checked separately.
- GPU Cycles 4096 bake: **zero missed/black interior texels of 381,594**.
  Source/export pair display-RGB RMSE **.02179/.02230** boxwood and
  **.00656/.00634** hydrangea. Global selected-leaf medians differ by at most
  **.0015**. Every one of **3,670,016 analytic-region pixels per map** is
  byte-identical in the GLB; wood has real projection and coverage checks.
- Final GLB SHA-256:
  `09aa4f0497750215545d657cfa8fd2f4606f6bdc92a5685d76848964ea5fc929`.
  All **18 Cycles** views (including four photo cameras) and **two Eevee**
  heroes match that GLB. Four matching source photo-camera renders were also
  rebuilt, inspected and checked against their actual source hashes.
- Actual retained foliage spans boxwood **1.035 × 1.004 m**, bottom/top
  **.060/.867 m**; hydrangea **1.492 × 1.430 m**, bottom/top **.030/1.135 m**.
  These include actual alpha support; mesh serialization and form checks have
  separate scopes. Wind/position errors are zero through raw and fresh import.
- Images: `renders/final/` and `renders/hydrangea-final/` contain hero, full
  turnaround, `close_1m`, scale, contact and measured photo pairs.
  `renders/final-eevee/hero.png`, `renders/hydrangea-eevee/hero.png` and
  **`renders/family-final/contact.jpg`** complete the delivery presentation.
  Only five final docs JPGs enter Git; all are at most 1600 px wide / 200 KB.
- `kit/test_atlas.py` passes original stock PBR/re-import checks and the small
  unique-region case. `kit/test_botanical_delivery.py` passes legacy defaults,
  authored normal/Wind export, premultiplied alpha, coincident-data matching,
  deliberate Wind corruption rejection and image-derived memory estimates.
  No other asset's geometry/material/bake was rebuilt or changed.
- Privacy scan and manual reference-register review find no private subject
  identity, home address, listing link, machine path or host name in shrub
  source/docs. Public author credits remain for reference rights. No reference
  photographs enter committed docs. `git diff --check` passes.

No further tool or lead approval is needed. The known visual limits are above;
engine thin-leaf/wind/LOD integration is documented rather than claimed shipped
as stock glTF animation. Shared kit changes are isolated in their own commits.
