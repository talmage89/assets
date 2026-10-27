> **Current pin oak: final summer delivery, finish pass 5 below.** Earlier
> findings and checkpoint numbers are historical; final images are under
> `renders/oak-final/`, with matched source evidence in `renders/oak-final-source/`.

# Red maple / structure checkpoint review

This log covers **form development with placeholder shaders**, not final leaf or
bark approval. Every rendered view was opened, including the final six-view
set and both photographic pairs. No final documentation images are committed.
The photos stay ignored and are credited in refs/SOURCES.md.

## Pass 1 — reject the sparse pole-and-spray form

Evidence: `renders/pass1/{daylight,structure}.png`, both reference photographs,
and exploratory `match_{psu,osu}-pair.jpg`.

**Color/value first:** bark was much too pale, nearly white, against the medium
and dark photographic trunks. The leaves were dark but so sparse that sky
rather than shadow determined the interior. Darkening the wood placeholder
was necessary before evaluating the structure honestly.

The main bole looked like a utility pole. Branch sprays were disconnected from
one another, leaving long bare shafts. The roughly pyramidal outline read as
sparse sapling architecture at mature-tree scale. Ladder-like opposite leaf
pairs produced obvious repeated fern shapes. Measured width was 10.10 m,
outside the brief, despite the narrow impression in one projection.

Actions: replace the single-axis scaffold pattern with staggered leaders;
shorten/rebudget secondary geometry; increase actual foliage coverage; constrain
outer shoot positions. The first 24,778 triangles were being spent poorly.

**Invalid camera evidence:** unconstrained biological anchors invented a
below-ground Penn State camera and a high Oregon State viewpoint. The black
Penn State pair is a failed diagnostic, not a valid reference match or a passed
look check. It is retained locally so the failure is visible. It must not be
used as approval evidence.

## Pass 2 — connected crown, still recognizably procedural

Evidence: `renders/pass2/{daylight,structure,crown_up}.png` and both pairs.

**Color/value first:** the darker wood improved relative value, but remained
uniform gray. Outer leaf masses received light; the inner crown was now dark.
Opaque placeholder backs were already crushing some interior values. Final
leaf response will need to recover detail without washing out the canopy.

The 22,670-triangle tree had real subordinate leaders and a connected crown,
but the repeated ladder sprites were even more apparent looking upward. There
were too many similarly dense branch sprays. Coarse junctions still showed
capped tubes disappearing into their parent rather than grown collars.

Actions: replace ladder sprites with three-axis leafy shoots; vary density by
branch family, including noticeably thinner sectors. Add explicit eye-height
and lens constraints to the kit fitter. A known-camera numerical fixture
passes. Earlier pair crops still clipped part of the crown, so their framing
was not accepted; base/top anchors needed more weight than uncertain lateral
anatomy. The photographed trees are different individuals, not survey targets.

## Pass 3 — foliage breakup improves; reject tube intersections

Evidence: `renders/pass3/{daylight,crown_up,unions,silhouette}.png` and revised
full-framing `match_{psu,osu}-pair.jpg`.

**Color/value first:** large foliage masses were deep green with brighter outer
edges. The palette avoided the washed-out library tendency, but some backs
were nearly black. The broad source/reference color difference was reduced;
flat leaf color and missing pale undersides remained obvious in the up view.

The original mathematical placeholder sprites now read as lobed leaves rather
than fern ladders. Sky gaps survived between branch families. The crown no
longer made an even smooth shell, although some masses still looked like
repeated compact puffs. There were thin slashes from edge-on cards. Those are
not excused as photoreal leaves: their final shape/normal/underside treatment
must be addressed after this checkpoint.

The leaf-off close-up exposed the worst structural issue: a sharp intersection
seam and caps at the scaffold roots. Smooth uniform material made the fault
especially clear. Do not try to hide it with bark textures.

Actions: union coarse roots, bole, leaders and scaffolds; relax the unions and
restore an explicit geometry budget. Fine twigs remain economical separate
closed components. Leave shader look development for the requested next stage.

## Pass 4 — continuous coarse unions; lower crown still too high

Evidence: `renders/pass4/{daylight,structure,unions}.png`, compared with the
same summer photos and the pass-3 framed pairs; foliage placement was unchanged
in this pass.

**Color/value first:** gray coarse wood retained useful light/shadow separation
at the joins, which now read as a continuous surface. It still looked like
untextured plastic, as expected of a structural placeholder. Coarse surface
continuity improved the silhouette independently of color.

The union removed the visibly intersecting coarse caps. The whole-tree view
still had too much clear bole below the foliage compared with both photos.
The lowest sprays swept upward too aggressively, contributing to the impression
of a dense ball mounted too high. Some leaders remained overly straight; fine
branches were angular at close range because of their low radial/longitudinal
resolution. Both limitations need to stay visible in the report.

Actions: lower the three outer lower scaffold masses while preserving their
real parent attachments. Keep the 9 m crown target instead of widening the
entire tree to match the distinctly broader Penn State individual. A topology
audit then caught two submicron decimation slivers. Weld/dissolve cleanup removed
them; a follow-up audit caught a 16.6-micrometer wire remnant, which was removed.
The completed source audits now report no slivers or non-manifold edges.

## Pass 5 — completed requested checkpoint, still not final look approval

Evidence: all eight Cycles renders under `renders/round1-checkpoint/`, its `contact.jpg`,
`review-sheet.jpg`, `shots.json` and `tonal-check.json`. Six presentation views
plus two calibrated source renders; the latter are shown in both summer pairs.
All eight render metadata hashes match the current packed source. The scale
view uses the unchanged 1.8 m kit silhouette.

**Color/value first:** no pale all-over wash. The selected green-dominant crown
pixels have display luminance p5 **0.0084**, median **0.0645**, p95 **0.4018** and
p99 **0.5025**, with **0% channel clipping in that mask**. The mask excludes sky,
wood and some neutral highlights; this is a sanity check, not an albedo or
whole-object clipping measurement. Interior blacks are too severe in places.
Final two-sided leaf response must open them slightly while keeping deep shade.

Lower branch masses now reach down into a more plausible lower crown; the
asymmetric silhouette has visible sky windows and finer boundary breakup.
Root flare meets grade, large forks are continuous, and the main trunk tapers
through a hierarchy instead of carrying a spherical shell. Compared with the
photographs, the remaining central-axis impression is still stronger and the
masses are coarser, especially from the calibrated front. The reverse silhouette
has a somewhat conspicuous central window. The placeholder leaf silhouettes
are too regular and flat to pass a close inspection. The up view still exposes
edge-on slashes. These are explicit limits, not cleared failure modes.

Photo fits: Penn State **73.80 px RMS**, estimated **75.5 mm**; Oregon State
**34.55 px RMS**, estimated **80.0 mm**. Lateral anchors are downweighted because
the individuals have different crowns; base/top have stronger weights. These
are approximate anatomical composition fits, with residuals shown, not precise
matched surveys. Penn State is appreciably broader than the specified target;
Oregon State is closer in habit. Neither tree's age or dimensions is verified.
The actual model dimensions are measured independently from its vertices.

### Checkpoint proof and stop

- `make -C trees`: passed, rebuilding the sources/checks and all requested
  Cycles views, both pairs and contacts, at 1200 px / 40 GPU samples.
- `make -C trees check`: passed source budgets, actual dimensions, manifold
  solids, nonzero triangle area/normals, card UV bounds/density, unit custom
  normals, all Wind values, growth attachments, camera projection and repo rules.
- Wood **11,090**, cards **11,946**, total **23,036 / 25,000 triangles**;
  **2 materials / 2 static meshes**. Lowest vertex **0 m**.
- Actual envelope **8.96965 × 8.87478 × 12.43311 m**. Actual 1.35 m triangle-plane
  section circle-fit diameter **0.355919 m**. No configured constant is reported
  as this physical measurement.
- Separate source/game builds have equal independently audited geometry digests.
  Centerline attachments agree within float tolerance; that check proves growth
  placement, not fusion of every twig or final serialization.
- Source **1,015,191 bytes**; current **2048² RGBA placeholder 96,123 bytes**.
  No GLB or final textures. Planned shared three-map 2048 set **16 MiB** with mips.
- No moving parts. Source `Wind` RGBA and custom normals are checked; their final
  export/re-import is pending. Bark unique UVs and final bake are also pending.

Stop here, as requested. Lead review should assess the silhouette, crown height,
openings and branch architecture in the contact and two photo pairs before
leaf/bark look development. Do not interpret passing checkpoint measurements
as photorealism approval or completion of the library's final delivery gates.

# Structure round 2 — lead-directed rebuild

## Measured photo targets before rebuilding

Evidence: `renders/round2-measurements/{psu,osu}-measurements.jpg`, tracked
`src/reference_measurements.py` and `build/reference-measurements.json`.

The manually inspected continuous crowns measure **1.256** W/H (Penn State,
691 × 550 px) and **0.960** (Oregon State, 666 × 694 px). Their bases sit **12.3%**
and **15.1%** of total tree image height above grade. Estimated landmark
uncertainties are ±12 / ±15 px. These dimensionless measurements do not prove
real height or age. Normalizing both to 12.4 m would imply 1.52 / 1.87 m bases,
which are estimates rather than surveys. The 2–2.5 m base in the brief remains
the independent metric constraint.

## R2-A — reject the whole-network union; value still too low

Evidence: `renders/round2-a/{daylight,structure,crown_up,unions}.png`.

**Color and value first:** original mid-green albedo, pale backs and 38% diffuse
transmission improved on the round-1 black leaves, but green display-luminance
p5/median/p95 were **0.024 / 0.095 / 0.365**. This was still much too dark beside
the photos (Penn State **0.073 / 0.260 / 0.564**). No claim of a meaningful
finished value match was made here.

The continuous branchlet distribution removed the detached two-arm shape and
coarse isolated puffs. Orthogonal companion branchlets with true-normal
coverage fade removed the obvious long edge-on card slashes in the upward
view. But **the wood was catastrophically wrong**: remeshing the complete
fine twig network created tiny handle topology, and aggressive decimation
produced flattened facets, a spike at the base and 11k wood triangles. This
render is rejected evidence, not a valid checkpoint.

The diagnostic stages are retained under `build/round2/`. Coarse-only union
retained sensible volume; whole-network decimation doubled its volume and
could not meet the budget. The fix was to fuse only bole/roots/co-dominants/
scaffolds, remove disconnected sub-voxel crumbs explicitly, and retain compact
authored small branches. A new Blender fixture passes both component policies
and checks sealed surfaces and retained main volume.

## R2-B — divided structure works; overly long co-dominants remain

Evidence: `renders/round2-b/{daylight,structure,crown_up,unions}.png`.

**Color/value first:** stronger procedural sky fill improved the selected green
p5/median/p95 to **0.047 / 0.136 / 0.378**, but the median still missed the photo.
The next pass needed camera exposure and hue calibration with the new real
albedo/transmission response, not an emission floor or painted-in ambient term.

The structure now had four co-dominants, sixteen scaffolds and two additional
orders. The main union was sealed. Nevertheless the long co-dominants still
looked like a bundle of rods, and a four-way same-height fork looked artificial.
The first corrected mesh was also over budget at 25,576 triangles: shorten
fine branch station counts rather than reducing foliage into sparse puffs.

## R2-C — stagger the fork, calibrate values; reject bright lime tint

Evidence: `renders/round2-c/` four structure views and both photo pairs.

**Color/value first:** adjusting exposure with unchanged thin-leaf response
brought the green median near **0.22**, versus Penn State **0.26**. However, the
upper leaves now looked lime-green and too saturated; the photographed summer
canopy is more muted. The bright spots rolled off rather than clipping. Final
leaf albedo was moved toward a less saturated mid green, with pale but not
cyan backs. The wood placeholder was darkened to avoid the pale-library tell.

Co-dominants now emerge at staggered **2.10–2.65 m** locations, with a terminating
bole rather than a central axis to the apex. The main fork close-up no longer
shows the prior open notch. Continuous coarse topology checks support that
observation; small separate branch caps remain an explicit limit.

## R2-D/E — fuller hierarchy; dense version obscures too much structure

Evidence: `renders/round2-d/` and the full intermediate checkpoint archived as
`renders/round2-e/`, including its photo comparisons and contact.

**Color/value first:** the muted green removed the lime cast; thinning the
back-color multiplier reduced the cyan impression. Shadows stayed green, with
visible thin-leaf transmission under backlight. The bark is still uniform gray,
which is appropriate only for this form checkpoint.

Co-dominants were shortened to divide again around **6–7 m**, with more branching
responsibility passed to their scaffolds. The pipe model assigns nominal
cross-section from actual supported branchlet counts, instead of choosing
skinny radii independently of branch load. Four orders remain visible in the
leaf-off mesh.

At 24,040 triangles, 67.4% were foliage. Although technically within budget, the
8,100-card version was denser than needed and hid too much interior structure.
It also relied more on extra cards than the lead wanted. Keep the new 24–30-leaf
branchlets, return card count close to the old 5,973, and reduce coarse wood
triangles where they do not change the silhouette.

## R2-F — inspected second checkpoint and stop

Evidence: every current render in `renders/round2-checkpoint/`, including
`contact.jpg`, `review-sheet.jpg`, the two `*-measured-pair.jpg` comparisons,
`tonal-check.json` and `shots.json`. All eight Cycles renders were opened. The
original round-1 daylight/structure cameras are retained for direct comparison;
the upward and union cameras were adjusted to show the lowered divided crown.

**Color/value first:** green p5/median/p95 are **0.072 / 0.219 / 0.577** in the
Penn State camera, beside the photo's **0.073 / 0.260 / 0.564**. Oregon State
camera values are **0.069 / 0.216 / 0.582**, beside that brighter/scanned photo's
**0.122 / 0.394 / 0.641**. Less than **0.05%** of selected green pixels are below
0.02 display luminance; **0%** clip a channel. The crown retains dark recesses,
mid-green sunlit foliage and pale backs instead of the previous nearly black
leaf planes. There is no emission term. These are display-image comparisons,
not calibrated reflectance measurements or identical lighting claims.

The 6,000-card version keeps the complete oval, small sky holes and fine edge
scallops, with more visible inner branches. It has only **27 more cards than
round 1**, while increasing leaves per card from 18 to **24–30**. The structure
has no continuous trunk to the top. True-normal glancing fade plus orthogonal
companions prevents the prior edge-on slashes; thin lines visible in the
leaf-off image are actual modeled branch sections. Final sculpted leaf
curvature, fine serration and bark response remain outside this checkpoint.

### Ratios beside the photographs

The measured comparison JPGs put these values above their respective panels:

| Image | Projected crown W/H | Crown-base fraction of total tree image height |
| --- | ---: | ---: |
| Model / Penn State camera | 0.973 | 19.4% |
| Penn State photograph | 1.256 | 12.3% |
| Model / Oregon State camera | 0.972 | 19.2% |
| Oregon State photograph | 0.960 | 15.1% |

The model matches the **Oregon State oval**, not the broader Penn State
individual. It retains more clear bole than the normalized photo estimates.
That mismatch is not hidden by fitting or by the passing dimensional checks.
The specified 9–10 m width, 12.4 m total height and 2–2.5 m lawn clearance favor
this end of the photographic range. Photos are different individuals without
surveyed metric heights; camera fits remain approximate at 68.2 / 40.4 px RMS.

Projected green-crown bounds reject isolated green denoising pixels on the
neutral bole, using a minimum occupied row width. This fixed an initially
incorrect Oregon State crown measurement that accidentally included the foot.
The independent physical measure instead transforms retained alpha texel-center
support onto actual cards: **9.429 × 9.139 × 10.234 m**, base **2.120 m**, top
**12.354 m**, giving 3D X/Y W/H **0.921 / 0.893**. These physical ratios are not
misrepresented as projected photographic ratios.

### Proof and remaining weaknesses

- `make -C trees`: passed the complete checkpoint build, six presentation views,
  two calibrated Cycles renders, measured pairs and contacts at 1200 px / 40 samples.
- `make -C trees check`: passed source manifold/area/normals, dimensions/budget,
  actual chest-height section, all Wind values, custom normals, deliberate tile
  reuse/density, four low co-dominants, hierarchy/attachments, pipe profiles,
  camera projection and repository gates.
- `blender -b --factory-startup --python-exit-code 1 --python kit/test_botany.py`:
  both default and connected-only union fixtures pass.
- **18,340 triangles**: **6,340 wood / 12,000 foliage**, **65.4% foliage**, two
  materials and two static meshes. No moving parts. Lowest vertex **0 m**.
- Actual DBH **0.358661 m**; complete mesh including alpha corners
  **9.702851 × 9.392061 × 12.460386 m**. 348 growth paths, 85 checked area
  junctions. Maximum nominal-profile pipe area error is floating-point noise;
  this is not a measured exact area-conservation claim on the fused surface.
- Packed source **955,789 bytes**; original **2048² RGBA atlas 125,178 bytes**.
  Future shared three-map atlas remains approximately **16 MiB**. No final GLB.
- Separate source/game geometry digests agree. Every current render records
  the current source hash. Camera/lighting/material settings are reproducible.

The crown still has more regular large-scale symmetry than the photos. Fine
modeled branches remain angular when isolated, and the plain gray bark makes
some coarse facets obvious in close-up. Penn State is not an exact proportion
match. The new leaf response and glancing coverage will need equivalent engine
shader support alongside wind; stock GLB MASK alone is insufficient. These are
explicit limits of the second checkpoint. Stop here for the lead's next review;
do not begin final bark/leaf surface work, baking or export yet.

## Round 3 — lead rejection of the round-2 crown

Round 2 is archived at `renders/round2-checkpoint/`. Its positive self-review
of the oval was too lenient: both pairs show a stippled egg, and the close-up
still has a rectangular crotch. Passing topology and dimensions did not prove
those forms. The lead's third-round brief supersedes the round-2 acceptance
language. This round starts with the silhouette's branch masses, then checks
color/value, structure and construction. Final surface work/export remain held.

### R3-A — replace the filled envelope

The old sampler placed foliage in an oval and derived branches from it. That
makes symmetry and uniform leaf breakup the default outcome. Replaced it with
four curving co-dominants and 19 explicitly grown scaffolds, each carrying its
own limb-sized mass and six smaller subclumps on secondary/fourth-order forks.
The lower scaffolds spread almost level then turn down; upper destinations are
staggered. A dense leafy core in overlapping subclumps should screen central sky
holes, while recesses remain between the masses. This is the first candidate,
not an accepted visual result.

Color/value hypothesis: warmer source RGB, reduced backface pale multiplier,
and a below-view condition for pale backs address the emerald/mint speckle.
The lighting stays fixed. Bent normals now blend 28% crown and 72% branch mass,
then bend 90% away from the physical card normal. The original value statistics
must be checked after rendering rather than assumed to survive these changes.

Wood: all retained branches exceed 2 cm authored diameter. Geometry is gently
curved rather than single straight fourth-order rods. Smooth collar patches
are unioned with all retained wood; a weighted decimator protects the lower
forks. Five low rounded buttresses disappear below grade within 0.5 m. The
surface will be checked from both sides at eye height, including second-order
unions. This replaces the previous disconnected fine-branch assembly policy.

### R3-B — first rendered candidate rejected

Evidence: all ten `renders/round3-a/` images opened. **Silhouette masses first:**
the egg is gone, but its replacement has isolated pompons and over-deep holes,
including a bright opening around the lower fork. The upper mass stands alone.
This overshoots the reference notches; add an overlapping mass core and foliage
on the inner parts of the low limbs, without returning to an envelope fill.
Color/value: warmer green and reduced pale flecks help, but the crown is too
sparse to judge the final shaded recess values fairly.

The all-wood voxel surface decimated to budget, but flattened fine tubes into
pointed ribbons. Reject those meshes even though their graph diameter was >2 cm.
The initial weighted decimation attempt was also rejected (it retained >300k
vertices). Next: union coarse living forks separately; retain economical curved
secondary sweeps and Boolean-union their embedded collars without a final
whole-network decimation. Use three secondary limbs per mass, sharing the six
small subclumps, and put their fine daughters entirely in the alpha branchlets.

### R3-C/D — join failure caught, support continuity restored

Evidence: `round3-b` photo pairs and all ten `round3-c` views (opened individually
or on the contact). The B pairs are still a set of detached masses with a
narrow upper crown, though their widest band is in the lower half. Grew four
additional scaffold-supported intermediate masses and broadened the upright
upper branches. These overlap the terminal masses and screen the large central
openings; their positions still come from specific branches.

The C Boolean candidate lost the bole: flattening below-grade root vertices
had made a self-intersecting operand. This was a build failure, not an acceptable
checkpoint. Move the grade cut after the unions, use a real planar bisect/cap,
and guard every Boolean against losing solid volume. The corrected D source
has the bole and curved secondary limbs, but its 8.6k wood triangles need modest
consolidation. No surface from the failed candidate is accepted.

Color/value: B p5/median/p95 was 0.033 / 0.189 / 0.557, too dark inside compared
with the earlier checkpoint and Penn State. Increase procedural skylight fill
from .22 to .30, diffuse transmission .34 to .40 and path depth 8 to 12. Sun,
exposure, albedo and zero-emission policy stay fixed; remeasure after rendering.

### R3-E/F — measured masses; final corrections before delivery

All ten F views and both measured pairs were opened. **Silhouette first:** the
separate upper tufts and lower-half width now read at limb scale, but isolated
branchlets still float above the apex, and the OSU projection is slightly narrow
(0.974). Pull only sparse within-mass outliers toward a neighboring branchlet;
broaden branch destinations about 4%, and place a small share of each mass's
core population on its supporting scaffold's distal interior. This screens the
remaining bright central window with inner leaves, retaining outer notches.

Value check: F p5/median/p95 = 0.049 / 0.206 / 0.558 in Penn State, 0.045 /
0.204 / 0.563 in OSU. The sunlit value is right; deepest selected green is still
too dark. Increase sky fill .30 → .40, keeping sun/exposure and the warmer
albedo fixed. The underside has fewer mint flecks and the lower view retains
transmission. Remeasure the final views.

The main notch is gone, but F's front union has a faceted horizontal shading
band. Correct the decimator's collapse-permission weights (all positive; lower
permission near actual first/second-order forks). The initial R3-A mask had
incorrectly protected unassigned zero-weight upper vertices instead. Blender's
edge-cost implementation confirms zero forbids collapse; this is why that
attempt stalled above budget. Source: Blender `bmesh_decimate_collapse.cc`,
https://github.com/blender/blender/blob/main/source/blender/bmesh/tools/bmesh_decimate_collapse.cc.
No downloaded code is used. Rebuild and inspect the same four union views.

### R3-G through Q — judge the closest wood, not just topology

The J checkpoint and its pairs are archived at `renders/round3-j/`; all eleven
views and both pairs were opened. Its crown now has real mass-level value
modeling, but the close-ups still show reduced upper tubes and a lower shading
band. A passing manifold test did not make those shapes acceptable.

Replaced the voxel/reduction wood policy entirely with economical authored
curved, tapering sweeps. Their 23% basal swell forms the collar; manifold union
removes the overlapping inner walls. A 1-degree planar cleanup removes
redundant Boolean splits. No global twig/wood decimator survives. Rejected the
intermediate K–M simplification attempts: they opened small junction faces.

An independent connected-component check then caught four closed but loose
secondary limbs. Their centers were attached to the dense design curve, while
the retained parent sweep followed a slightly coarser curve. Each child now
starts on the actual retained parent centerline, with the adjustment blended
out along its curve. No loose components are discarded to conceal this.

The Q source passes as one connected, sealed woody surface. The four-order
growth graph is retained; the fourth-order continuation and thinner twigs live
in the branchlet cards. Co-dominants and scaffold sweeps retain curved round
sections. More authored cross-section geometry is spent on the visible wood,
while 7,800 cards are concentrated in the branch masses, not in a uniform oval.

The original OSU frame clipped the broadened model's right edge. Ratio and
widest-band values from that clipped image are invalid. New study canvases add
neutral side margins to the unchanged photo crops and widen the horizontal
render field equally. Camera pose, roll and vertical field remain calibrated;
independent projection agreement is below 0.001 px. Lens values in the framed
JSON are the equivalent focal lengths for that enlarged field. Both original
and framed calibrations remain available; no photograph is altered into an
asset texture or model.

## R3 final — inspected checkpoint and stop

Evidence: all eleven presentation views and both matched renders in
`renders/checkpoint/`, their measured pairs, `contact.jpg`, `review-sheet.jpg`,
`tonal-check.json` and `shots.json`. Final close-ups from both sides of both
orders and the root detail were opened separately; the remaining views were
also inspected individually or in the contact. These are source renders with
usable placeholder leaf response, not baked/exported-GLB proof.

**Silhouette's masses against the photographs first:** the crown now reads as
scaffold-sized foliage masses with smaller tufts, offset upper leaders, lower
horizontal/drooping limbs and a scalloped asymmetric edge. It no longer has the
round-2 smooth egg envelope. The photos still have more interlocking, less
individually rounded masses; the model's right upper recess is deeper and its
waist more pronounced. This is a visible remaining limitation, not something a
ratio check excuses. The lower crown is wider than the middle/upper crown in
both uncut photo views.

| View | Model W/H | Photo W/H | Widest band above crown base: model / photo | Widest-band height, 12.4 m image normalization: model / photo |
| --- | ---: | ---: | ---: | ---: |
| Penn State | 1.025 | 1.256 | 18.0% / 25.5% | 4.08 / 4.29 m |
| Oregon State | 1.022 | 0.960 | 35.7% / 36.5% | 5.88 / 5.71 m |

The target 1.0–1.15 projected ratio is met. Penn State remains the broader
individual. The model's base is 18.1 / 18.2% of whole-tree image height, versus
12.3 / 15.1% in the photographs. Photos have no surveyed height or age; normalized
meters are comparison aids. Photo widest bands have ±30 px uncertainty. The
physical retained foliage starts at **2.025 m**, reaches **12.240 m**, and spans
**10.727 × 10.206 m** horizontally. The full card-corner envelope is
**10.955 × 10.523 × 12.373 m**. The retained crown is deliberately broader than
the original 8–10 m range to meet the newer W/H/low-drip-line direction; do not
continue claiming the round-2 9 m width.

**Color/value next:** Penn State-camera selected-green p5/median/p95 is
**0.062 / 0.244 / 0.580**, compared with photo **0.073 / 0.260 / 0.564**. OSU-camera
values are **0.061 / 0.243 / 0.584**, versus its brighter photo **0.122 / 0.394 /
0.641**. Zero selected-green pixels clip a channel. Below-0.02 display luminance
accounts for **0.31% / 0.32%**, compared with **0.38% / 0.18%** in the photos.
This preserves useful sunlit mids and dark recesses without the old black
planes; it is not a calibrated-reflectance or identical-lighting claim. Warmer
outer greens and blue-sky-lit shaded foliage replace the emerald/mint speckle.
Pale backs appear mostly from below; transmission remains visible in crown-up.

Each mass now has a sunlit cap and shadowed lower/interior faces. Crown/mass
radial normals are blended 28/72 before 90% card bending. The glancing coverage
and orthogonal companions remain effective: I do not see the previous plane
slashes in crown-up or drip-line. The blades are still flat prototypes and the
sprite-scale pattern is visible close to the camera; final leaf curvature,
serration/veins and material detail are held for the next phase.

**Unions, thin limbs and roots:** inspected `unions`, `unions_reverse`,
`unions_upper` and `unions_upper_reverse`. The large rectangular notch is gone;
all modeled wood is now a single sealed union rather than caps passing through
one another. Basal daughter swelling provides collars. Crotches retain dark
ridges/shadows, and uniform gray material makes some faceting obvious. Several
thin limbs remain angular in the leaf-off close-ups; they are improved curved
sweeps, not perfect organic limbs. Do not describe them as final bark/form
polish. No separate loose fragment survives the component test. Minimum
retained authored diameter is **2.1 cm**, with thin continuation in the atlas.

The root detail shows **five modest low buttresses**, with reach at less than
8 cm height **0.401 m**, rather than the previous 0.65–1.15 m tripod fins. The
plain grade makes their cut at the lawn more conspicuous than it will be among
grass. Root tips sink into grade; lowest surface is at zero, origin at the bole.

### Current proof and limits

- `make -C trees`: **passed**, complete checkpoint at 1200 px / 40 GPU Cycles
  samples; eleven presentation renders, two matched renders, uncut pairs,
  annotated proportions and both contacts. All thirteen hashes match the source.
- `make -C trees check`: **passed** source topology/area/normals, measured scale
  and chest-height section, triangle/material limits, alpha tiling/density,
  Wind/custom normals, four low co-dominants, hierarchy, pipe profiles, actual
  connected woody surface, root reach, near-bole clearance, camera and repo gates.
- Shared-kit fixture: `blender -b --factory-startup --python-exit-code 1 --python
  kit/test_botany.py`: **passed**, including unchanged normal defaults, optional
  mass-normal blend and the existing union component policies.
- **23,754 triangles** = **8,154 wood + 15,600 foliage**, **65.7% foliage**;
  **7,800 cards**, two meshes, two materials. No armature or moving parts.
- Actual fitted DBH **0.360006 m**. Four co-dominants start at **2.193–2.726 m**,
  measured initial angles **39.0–39.3°** from vertical. 378 designed growth paths,
  four orders (the fine fourth order is in the branchlet representation).
- Actual woody mesh: **one connected component, zero nonmanifold edges**,
  positive volume **0.674355 m³**. Whole-card bounding spheres conservatively
  clear **3.33 m** within 1 m of the bole; the 2.2 m walking target is clear.
- **97** nominal pipe junctions checked, relative area discrepancy below
  **4e-16**. This is design-profile conservation, not exact fused-surface area.
- Independent source/game builds agree on geometry digest
  `82df60b3508bf348a52f30d1b6e581841b465b30448bfa38327fad76c4f706e7`.
- Packed source **1,149,767 bytes**; one original **2048² RGBA atlas 124,974 bytes**.
  Planned compressed shared BaseColor-alpha / Normal / ORM set remains about
  **16 MiB**. No final textures, GLB or GLB re-import certification exists yet.

Stop at this third structure checkpoint. The main weaknesses remain the more
discrete lobes/deeper windows relative to the photos, angular isolated thin
limbs, flat close leaves and unfinished bark. No tools or permission are needed
from the lead; the requested next step is their silhouette/structure review.


## Finish pass 1 — source, color/value first

Evidence: all eleven `renders/finish-1/` views and both measured pairs opened.
Penn State-camera green p5/median/p95 **.036 / .196 / .491**, photo **.073 / .260 / .564**.
The lower albedo removes lime, but too much foliage falls below .02 (1.99%);
the next pass should recover some shaded detail without returning to pale caps.
Oregon State is used for form only because the lead identified its color shift.

The top is fuller, but the waist still has deep notches and a central window;
the first overlap rule picked central masses rather than the outward masses
above/below the gap. Reject that distribution. Link the supported outer masses
across their intervening height, and reserve inner population for screening wood.
Do not add triangles.

The root flare now widens continuously over the lower .7 m and the pointed tips
are buried; the broad buttresses are materially better. The bark is still too
blue/pale in the unshaded diagnostic views, and the Voronoi ridges look like
reptile scales at collars/roots. Reduce their height and continuity, keep long
narrow plates on the older bole and fade them out before the limbs.

The lobed blades and red petioles read clearly from below. The current shoots
are too saturated and uniformly thick; reduce twig gauge/red and keep the
petioles red. Backs need a grayer response. Source and final GLB have not yet
been compared; this pass does not certify delivery.


## Finish pass 2 — source refinement, color/value first

Evidence: all views on `renders/finish-2/contact.jpg`, full-size daylight, root
flare and both measured pairs opened. Penn State green p5/median/p95 is
**.038 / .208 / .519** with **1.65%** below .02, zero clipped channels. The
median is lower than round 3 (.244) as requested; lit masses retain mid yellow
green, but shaded recesses are too uniformly dark. The OSU scan is judged for
form only. Full lit/shaded population statistics will accompany final pairs.

The upper sides overlap into a connected dome with shallow top notches, and
the waist is less empty. Deep recesses still separate some rounded caps, more
than in Penn State. Reduce the local-mass normal blend from .72 to .60, keeping
the physical asymmetry, to avoid overstating individual floret shading. No
triangle increase. Lowest skirt and clear-bole walking space remain.

The root flare is continuous, with broad rounded buttresses rather than pointed
roots stuck onto a cylinder. A measured grade-area equivalent diameter was
.673 m, 1.88× DBH including buttresses: too broad for the requested 1.5–1.8×.
Reduced bole flare and buried root reach modestly; remeasure the shipping mesh.
Bark relief is now shallower and fades out on limbs; the neutral diagnostic
grade and sky still give it a cool cast. Final bark detail must keep real leaf
shade enabled. Twig gauge/red has been reduced; gray-green backs, fine cup/rib
normals and varied blade tilts are added before delivery.

### Delivery defects found before accepting pass 3

The initial generic Smart UV pack failed overlaps/coverage. Authored branch-axis
seams plus angle unwrap now give zero overlaps. A faulty seam that cut across
rings was rejected; the accepted seam follows the shared edge between faces
on opposite sides of the angular wrap. Explicit area normalization prevents
tiny Boolean patches getting arbitrary density. Regional priority favors the
bole over fine limbs.

The initial tight cage missed 25,757 interior texels. A .003 m cage / .025 m ray
range gives **zero missed or black interior texels of 3,851,514**.

The first GLB did NOT pass: Blender dropped four duplicate triangles and changed
nearby wood normals. Triangulating the union exposed four microscopic pairs of
oppositely wound internal faces hidden inside valid-looking source n-gons.
Remove BOTH sides of those pairs and their wire edges before source acceptance;
never count the exporter's silent cleanup as a pass. This is a real correction
to the earlier source-only manifold claim. Wind data and leaf normals survived
that candidate, but it is not accepted final delivery.

## Finish pass 3 — exported GLB, color/value first

Evidence: all eleven `renders/finish-3/` GLB views opened individually, plus
both measured photo pairs. Source bark shaders were not loaded by the final
renderer; the foliage response used only the GLB's three embedded maps.

Penn State selected-green p5/median/p95 is **.043 / .220 / .531**, beside the
photo's **.073 / .260 / .564**. Brightest-fifth median is **.478 / .495**;
darkest-fifth median **.063 / .100**. The warm mids are improved, but the
shadow population's hue is still **109°**, versus the photo's **125°**. Increase
blue in the authored leaf albedo while keeping the median below the original
lime checkpoint; compare the final exported maps again. The population numbers
are display-image measurements across different lighting, not reflectance.
Oregon State remains form-only.

The .60 mass-normal blend helps the crown read as an undulating connected
surface. It still has more distinct rounded caps than the photographs, and the
Penn State individual is broader. The top is full rather than two narrow peaks;
the lower skirt and asymmetry survive the width reduction. Whole-card corners
span **10.074 × 9.111 × 12.535 m**, while actual retained leaves span **9.801 ×
8.857 m** horizontally. The latter is the visible crown width.

The corrected flare measures **.620 m area-equivalent diameter at .01 m**, or
**1.72×** the measured .361 m DBH; **.373 m at .70 m**, or **1.03×**. These are
closed triangle/plane intersection loops, not the authored flare parameter.
The buttresses reach **.378 m** below 8 cm height. No pointed claw extends from
a straight bole.

Bark is the remaining failed surface: the imported close-up blurs the fine grain
and emphasizes smooth vertical streaks. The first stronger Voronoi preview is
also rejected: continuous cell walls still suggest an artificial scale pattern.
Replace them with slowly warped longitudinal fissures and intermittent shallow
flake faces; keep smoother young limbs and north-side lichen sparse. The final
stage's grade will meet the foot within 1 mm, removing the old 15 mm staging gap.

The blade close-up shows three main lobes, sparse five-lobed variants, teeth,
raised palmate ribs, varied projection/cup and red petioles with browner red
shoots. Pale gray-green backs are confined mainly to below views. The limited
atlas resolution softens fine teeth and small leaf scars; do not call this a
botanical macro asset. Several isolated upper limbs are still angular in the
leaf-off diagnostics.

Delivery proof for this candidate: **23,680 triangles**, **8,080 wood / 15,600
foliage**, **two materials**, three shared **2048²** maps. Independent checks
find zero position or linear Wind errors, split-normal vector error below
**8.6e-5**, zero UV overlaps and zero missed/black interior bake texels. The
remaining acceptance is the corrected final GLB appearance and complete render
set, not another structural approval checkpoint.


## Finish pass 4 — full GLB set; bark rejected before docs commit

The complete 1600 px / 72-sample Cycles set, Eevee hero, two measured pairs and
checks completed. **Color/value first:** Penn State green p5/median/p95 is
**.040 / .219 / .543**; brightest-fifth median **.488** versus photo **.495**.
The corrected shaded-leaf hue is **123.3°**, beside photo **124.9°**, rather than
the previous too-yellow 109°. The crown median remains darker than the original
.244 checkpoint. Zero green channels clip. Deepest recesses are still darker
than the photo; that is retained as a limitation, not hidden with emission.

The full-tree/turnaround, top, branchlet and shade views were opened. They retain
the accepted asymmetric structure, low skirt, broad top and interlocked waist.
The crown still has some overly rounded caps. Small leaves remain recognizably
lobed at the edge, with red petioles and gray-green backs below.

**Reject the bark close-up:** periodic longitudinal ridges read as manufactured
fluting. No docs images from this state were committed. The replacement uses
irregular elongated plate cells with spatially interrupted fissures and relief.
Its first `renders/bark-plates/` pair was also opened and rejected: complete
cell walls on the flare still look reptilian. Mask both color cracks and relief
to broken growth patches; sparse lifting plate faces and fine bark grain should
interrupt the network. Re-export and inspect `renders/bark-final/` before the
last full build. No geometry, triangle or texture-size increase.

Both complete `make -C trees` and the independent delivery checks passed in this
intermediate state. Texture cost is **16 MiB**, measured geometry accessors
**2,667,648 bytes**, estimated combined GPU allocation **18.54 MiB** before
engine overhead. These checks do not override the failed surface review.


## Finish pass 5 — clean rebuilt GLB, accepted for delivery

Evidence: every current presentation/diagnostic PNG, the Eevee hero, both
measured photo pairs, contact and all three final docs JPGs opened. The bark
macro and root detail were checked separately after the last export.

**Color/value first:** final Penn State selected-green p5/median/p95 is
**.040 / .219 / .543**, photo **.073 / .260 / .564**. Brightest-fifth medians
are **.488 / .495**; shaded-fifth hues **123.3° / 124.9°**. Median green stays
below round 3's .244. The shade now reads blue-green rather than yellow-black.
Deepest recesses still skew dark: **1.59%** below .02 versus the photo's **.38%**;
zero selected-green channels clip. No emission or painted lighting compensates
for this. OSU values are retained in the JSON for transparency but its shifted
slide is used only for form. Population statistics are display measurements,
not calibrated albedo or equal-lighting claims.

The current crown is connected through fuller upper shoulders and overlapping
scaffold masses; the deepest previous windows are reduced without filling a
symmetric envelope. Its retained width is **9.801 m**. The front/side/back/top
views retain asymmetry and the low skirt. Some cap shapes remain too rounded,
and Penn State's specimen is still broader. Projected model W/H is **.961 /
.952**, photographs **1.256 / .960**. Widest bands lie **38.8% / 39.9%** above
crown base (photos **25.5% / 36.5%**), still in the lower half. The newer
about-10 m width instruction takes precedence over round 3's 1.0–1.15 ratio.

The flare is a smooth lower-bole widening with broad buried buttresses,
**1.72× DBH** at .01 m and **1.03×** by .70 m. The final grade is within 1 mm
of the foot. Root tops now carry interrupted shallow bark plates; the complete
reptile network and continuous fluting are gone. The 2K normal map softens
fine relief at this close camera, and the procedural sky gives gray bark a
cool cast. Those remain visible limits. Young limbs are deliberately smoother.
First/second-order unions were inspected from both sides: no open join or
rectangular notch; isolated fine limbs still show angular low-poly sections.

Leaf close-ups show broad three-lobed/occasional five-lobed blades, softened
serration, palmate ribs and shallow cups, red petioles and red-brown shoots.
Gray-green undersides show from below; the deepest inner leaves remain dark.
The branchlet macro exposes planar construction and repeating atlas logic.
There are no edge-on card slashes in crown-up/drip-line at the intended view
distances. Eevee is flatter and lighter than Cycles because its thin-leaf/GI
response differs; it is shown honestly alongside the Cycles shots.

### Final proof

- `make -C trees clean` followed by **`make -C trees`: passed**, rebuilding
  sources, UVs, 4096 GPU bake/composite, 2048 delivery set, GLB, all final views,
  photo pairs, contact, docs and checks from scripts.
- **23,680 triangles:** **8,080 wood / 15,600 foliage** (65.9% foliage), two
  materials, two static meshes, no moving parts/armature. Source/game geometry
  digests agree; wood is one sealed component with zero nonmanifold edges.
- Shared **2048² BaseColor-alpha / Normal / ORM**, lower half leaf variants,
  upper half unique bark. PNG bytes **1,535,382 / 1,545,254 / 1,077,311**.
- **GLB 6,829,972 bytes**. Block-compressed full-mip textures **16 MiB**;
  actual vertex/index accessor data **2,667,648 bytes**; estimated combined
  GPU allocation **18.54 MiB**, excluding engine overhead.
- UV overlap **zero**; unique coverage **22.95% of the whole atlas**, with the
  separate lower half reserved for leaves. Bark density p5/median/p95
  **101 / 310 / 437 px/m**; leaves **727–812 px/m**.
- Bake: **zero missed/black interior texels of 3,683,718 checked**.
- Raw GLB and fresh import: position and linear Wind error **zero**; maximum
  split-normal vector error **8.51e-5**. `_WIND` survives without COLOR_0 tint.
- All **20 Cycles / 1 Eevee** metadata hashes match final GLB SHA-256
  `2731af03fcf606c583edd6403a9e55a538bd40318bd4ead659a88ce034de7834`.
- Final evidence: `renders/final/{hero,front,side,back,top,bark,branchlet,
  crown_up,scale,root_flare,unions,unions_reverse,unions_upper,
  unions_upper_reverse,dripline,silhouette,structure,daylight}.png`;
  `renders/final/match_{psu,osu}-measured-pair.jpg`;
  `renders/final/contact.jpg`, `review-sheet.jpg`, `tonal-check.json`,
  `color-value-populations.json`, `render-check.json`;
  `renders/final-eevee/hero.png`.
- Final docs: `hero.jpg` **180,106 bytes**, `turnaround.jpg` **151,838 bytes**,
  `details.jpg` **196,641 bytes**; all at most 1600 px wide and 200 KB.

### Shared kit changes and remaining integration

Commit `26d0df3` adds opt-in custom wind-color export, split-normal-preserving
card triangulation, authored-seam unwrap and measured island/regional density
normalization, an analytic-tile bake-composite hook, RGBA coverage-aware color
filtering and a configurable final renderer. Defaults stay compatible.
`kit/test_botanical_delivery.py`, the default atlas/composed export/studio
fixtures, botanical fixtures, policy fixture and five delivery unit tests pass.
The pilot asset itself was not rebuilt; these fixtures exercise the unchanged
default paths.

Engines still add distance LODs/impostors, wind and the documented two-sided
thin-leaf response. Stock MASK PBR cannot reproduce that response alone. The
final renderer uses only imported embedded maps when restoring it. No request
for tools or approval is outstanding. Bark macro fidelity, some rounded masses,
angular isolated fine wood and visible cards at botanical close range are the
honest remaining weaknesses. Stop after this first tree as the brief requires.

## Finish pass 6 — lead bark correction (supersedes pass 5's bark acceptance)

The lead accepted the crown, leaves, petioles/twigs, flare shape and budget,
but rejected the bark. The previous report's admitted softness/cool cast was
an unresolved appearance failure, not a completed surface.

**Color/value first:** inspected the original summer photos and enlarged bole
crops. Penn State's upper-trunk shade patch has median display luminance
**.077**, lower bole **.124**. The delivered model measured **.244 / .427**
in comparable clear-bole regions. Its median RGBs were **(.200,.255,.286) /
(.404,.431,.447)**: conspicuously too pale and blue. Penn State's corresponding
RGBs are **(.055,.082,.067) / (.108,.131,.114)**. Both photo regions lie beneath
the crown; the lower one is not claimed to be a directly sunlit calibration.
The OSU slide is measured separately but remains unsuitable for color matching.
These are explicitly labeled display-image comparisons across different
specimens/illumination, not albedo measurements.

Candidate `renders/bark-correction-1/` was opened in bark, 2 m, root and union
views, and both photo cameras. Reject: stronger closed cell walls look like
scales. Values improved to Penn State **.163 / .329** but remain far too light.
Candidate 2's same four details and both cameras were opened. Reject: open
ridges still look like ruled fluting, with **.126 / .274** display values and
blue specular fill. Blender's exporter was omitting IOR alone: a nondefault
specular override now carries both KHR_materials_specular and IOR into the GLB.
The matte constants are uniform parameters, without another texture.

Replace the procedural cell network with an original seeded physical field:
unequal 2–4 cm ridges, individually wandering edges, staggered 10–30 cm plates,
ragged short lips, granular faces and shallow millimeter relief. Reject an
unrendered overly regular field before baking; add independent edge motion and
seeded multi-scale granularity. The intermediate field stores height, face
variation and microcavity visibility. It is generated from equations/random
seeds, never photographs. Bake normals at 4096 and filter to the same shared
2048 atlas; multiply the original microcavity visibility with geometric AO.
Radius/height maturity keeps sub-10 cm limbs smooth and lighter. Rain masks
follow protected vertical tracks below the crotch; lichen stays sparse.

The measured eye-height density was already about **408 px/m**, but repacking
more of the existing bark half for the bole raises it to **480 px/m median**
(**470–503** range). This is area-based density; the full report also discloses
directional anisotropy. Foliage UVs, geometry, all crown/leaf settings and the
three map dimensions are unchanged. No triangle or texture-memory increase.

Final imported-GLB review and delivery measurements follow below.

Candidate 4 fixes the value: Penn State model lower bole **.126** beside
photo **.124**, upper shade **.048 / .077**. The lower bark is warm gray-brown;
shade goes nearly black without blue-gray specular fill. All four imported
close-ups and both photo cameras were reviewed, including the labeled
`bark-value-pair.jpg`. Reject its remaining weak plate lips at 2 m.

The new diagnostic caught a hidden problem: its **481 px/m area average**
concealed **234 px/m** in the poorest direction. The tall source-field image
was influencing Blender's UV aspect, before the atlas's wide reserved region
scaled the UVs again. Test the actual delivery-region aspect instead, restore
all procedural input images afterward, and split the existing bole UV island
around the .8 m and 2 m stations. These are seams on existing edges, with no
new geometric faces. The compact eye-height island measures **457–464 px/m
in every tangent direction**, rather than relying on the area average alone.
The source UV-aspect fixture now measures near-isotropic Jacobians and proves
the tall source image is restored. The default botanical fixture still passes.
Broaden the short lip relief and face granularity just enough to survive 2K
filtering; retain shallow millimeter relief, without changing the silhouette.

### Final bark delivery review and proof

Every final PNG was opened, including the four union views, the 2 m view,
Eevee, both measured pairs, the bark-value crop pair, contact and docs JPGs.
Candidate 5's plate lips and rough faces survive the final imported-GLB 2 m
view. Ridges are dark, shallow and uneven, with short staggered plate breaks;
young upper wood stays smoother. The source mesh, crown layout, leaf settings,
root shape and lighting are retained. No painted light or emission is added.

Final Penn State median display luminance: **lower bole .119 / photo .124**;
**upper shade .041 / .077**. Lower-bole median RGB is **(.122,.118,.114)**,
photo **(.108,.131,.114)**; the former pale blue cylinder is now gray-brown.
The model's upper shade remains darker and cooler than the photo (model RGB
**.031/.043/.047**, photo **.055/.082/.067**). These residuals are not hidden.
The OSU slide reads model/photo **.053/.167** in upper shade, **.143/.222**
lower down; it remains form-only because of the scan's shifted colors.
`bark-evidence.json` records the exact rectangles and scope.

Actual shipped eye-height density: **458.1–461.8 px/m by area**, median
**460.7**. Crucially, the directional minimum/maximum is **456.8 / 464.0
px/m**, after the aspect correction; no blurred direction is concealed by
an average. Twenty-four thousand uniform surface-area samples of the embedded
2048 maps find normal-angle p10/median/p90 **1.59° / 4.27° / 14.75°**, with
ORM occlusion p10 **.608**, median **1**. The cracks carry both normal relief
and cavity visibility at delivery resolution. Unique UV overlap is zero;
coverage **22.65%** of the whole atlas, with the lower half separately reserved
for the unchanged leaf cards. Source wood has 205 UV islands.

- `make -C trees export`, then full **`make -C trees`: passed**. The current
  source scenes, authored UVs, 4096 GPU bake, 2048 filtering, GLB and full final
  render set were rebuilt. Every final Cycles operation used the shared lock.
- Budget: **23,680 triangles** (8,080 wood, 15,600 foliage), **two materials**,
  three shared **2048²** maps. PNG bytes **1,398,132 / 2,411,144 / 1,388,810**
  for BaseColor-alpha / Normal / ORM. **GLB 7,876,080 bytes**.
- Compressed full-mip textures remain **16 MiB**. Geometry accessors total
  **2,673,408 bytes**, estimated combined **18.5496 MiB** before engine overhead.
  The additional seam splits cost **5,760 bytes** (0.0055 MiB); no new triangles
  or texture allocation. No BarkMaturity data is exported: it is baked away.
- Bake: **zero missed/black interior texels of 3,511,566**. Position and linear
  Wind errors remain zero; maximum split-normal vector error **8.51e-5**.
- **21 Cycles / 1 Eevee** final metadata hashes all match GLB SHA-256
  `0bca0a4c94061101848e439bd9d2be9a21cf9a87eb458f93db85e14d0f14910f`.
- Final images: `renders/final/{bark,bark_2m,root_flare,unions,unions_reverse,
  unions_upper,unions_upper_reverse,hero,scale}.png`, the full turnaround,
  branchlet/underside/diagnostics, both `match_*-measured-pair.jpg`,
  `bark-value-pair.jpg`, `contact.jpg`; `renders/final-eevee/hero.png`.
- Refreshed docs: hero **180,690 bytes**, turnaround **152,174 bytes**, details
  **183,734 bytes**. Three JPGs, each at most 1600 px wide and 200 KB.
- Kit fixtures passed: `test_export_policy.py` (actual specular/IOR extensions),
  `test_material_ao.py` (real GPU emission/ORM bake, including unchanged default
  AO), `test_uv_target_aspect.py` (isotropic non-square target and restored
  source image), `test_botanical_delivery.py` (defaults, normals, wind, alpha),
  and the five `kit.test_delivery` unit tests. Other assets were not rebuilt.

Shared-kit commits `4557e4c` and `4ceef72` add opt-in material cavity AO,
uniform matte specular export and target-region aspect for authored UVs.
Existing defaults remain unchanged; engine imports must honor the documented
specular/IOR constants. Final limits: some columnar regularity in macro bark,
flat plate silhouettes at grazing angles, and deeper/cooler trunk shade than
Penn State. Existing card/mass/isolated-limb limitations remain as previously
reported. No further asset or tool approval is needed.

Final explicit **`make -C trees check`: passed**, including budgets, source form,
bake coverage, GLB/UV/PBR verification, wind/normals and eye-height directional
density/normal/occlusion checks. `git diff --check` also passes.

# Pin oak / structure checkpoint (new species, leaf look-dev held)

The maple review above is preserved. Its repeated puff/egg/fluting failures
inform this second species. No oak final delivery or leaf-surface acceptance is
claimed in this checkpoint.

## Oak pass 1 — reject the sparse conifer impression

Evidence: all three `renders/oak-pass1/{daylight,crown_up,structure}.png`
opened against OSU's summer pin oak, Stony Brook's summer street planting,
and the WWU leaf/bark photographs. **Color/value first:** leaves are too dark
and cool under the prototype response, the bole is plain gray, and the
blue-sky-lit backs are too pale. The OSU slide's yellow highlights are not a
color calibration target. Keep the placeholder status explicit.

The form is a pine-like spindle of detached pads surrounding a pole. The
straight leader is right for this species, but the equal-sized isolated
foliage pillows are wrong. At 21,142 triangles the retained width was 9.75 m;
passing width did not justify this appearance. The upward view exposes flat
prototype blades and fine triangular card-edge artifacts. The lower dead pins
were accidentally excluded by the shared nominal-radius filter; the rendered
bare bole revealed the omission. Correct that rather than claiming designed
stems were delivered geometry.

Actions: distribute branchlets along the actual supporting limb, add near-bole
foliage, broaden upper lateral reach, increase prototype shoot coverage and
spend up to 7,800 cards within the same 25k cap. Shade the shallow tier using
its elliptical dimensions, not a round clump normal field. Keep the shared
maple algorithm and random sequence unchanged. Retain actual dead pins.

## Oak pass 2 — improved continuity, reject oversized top

Evidence: `renders/oak-pass2/{daylight,crown_up,structure}.png` opened; same
photographs, plus the same-calibration comparisons recorded below.
**Color/value first:** crown mids remain dark/cool, with gray-green backs and
useful deep shadows under the boughs. The wood still needs the oak's subtler
sheen and shallower fissures rather than the inherited maple roughness.

Foliage now extends down the boughs and tier tops carry separate lighting.
There are still overly pillowy outer ends and large repeated notches. The
upward view is more connected and the lower pins are present, but card edges
and simplified tubes remain visible. The upper lateral formula overshoots the
leader: actual full-card height is 18.05 m and retained foliage reaches 17.79 m.
Reject that despite the near-target 10.00 m crown width. Cap upper limb ends
below the leader and maintain an ascending final tangent. The actual DBH is
43.1 cm (triangle-plane section/circle fit), not the 45 cm input constant.

The wood has 9,122 triangles, foliage 15,600: 24,722 total, two materials.
This oak spends 63.1% on foliage; the maple-specific 64% test is not a brief
requirement. Keep a 60% oak floor while retaining the real 25k cap. All 23 dead
pins must remain measured in the retained geometry. Final surface/bake work
remains held.

Pass-2 photo pairs were opened after the three view renders. In both, the model
has clearer but much more isolated, sausage-shaped bough ends than the
photographed trees. The crown is still too conifer-like. OSU is the closer
pyramidal individual; Stony Brook has a broader upper half and irregular twig
windows. It is also partly occluded by a neighbor and probably older, so its
full left outline is not treated as a measured silhouette target. Fits retain
17.2 / 175.3 px RMS residuals at the original photo resolutions; the 80 mm
upper lens limit is reached in both, showing the underdetermined fit.

## Oak pass 3 — corrected axes; reject residual apex scatter

Evidence: both `renders/oak-pass3/{daylight,crown_up}.png` opened against the
same photos. **Color/value first:** the old prototype green remains cool/dark,
with conspicuous pale backs; these views do not clear leaf look development.
The apex's supporting limb ends were corrected below the leader. A diagnostic
normal-preserving triangulation does not remove the fine angular lines in the
up view; it is rejected as a cure and does not enter the asset's build.

The broad upper reach is more plausible, but overall bough ends still look
rounder and more separate than the reference tiers. Reduce mass-normal emphasis
from .80 to .60 and widen vertical aprons with bounded scatter. Keep dark
under-tier recesses. The later source audit correctly rejected a 17.94 m
full-card envelope against its narrower authored-size tolerance: Gaussian card
scatter still extended 1.08 m above the 16.7 m leader. Bound that scatter and
keep upper card centers below the leader; do not relax the tolerance to pass.
No additional geometry or leaf surface detail is added.

The prototype backs are made neutral green rather than retaining the maple's
blue-biased multiplier. Flat normals/roughness and quick flat lobes remain.
Bark controls now give the oak shallower fissures, smooth small limbs and a
subdued gray sheen. These are source controls, not a finished baked surface.

## Oak pass 4 — complete set inspected; bark rejected

Evidence: **all ten Cycles PNGs** and both photo pairs under
`renders/oak-pass4/`, plus its contact/review sheet. Every presentation image
was opened separately, including the eye-height full view, crown-up, silhouette,
scale, leaf-off structure, lower pins, bark and maple/oak family view.

**Color/value first:** the neutral green prototype no longer has the old cyan
backface bias; broad foliage retains lit mids and dark tier undersides. It is
still a flat prototype, without the pin oak's final glossy cuticle, fine veins
or bristle detail. The paired OSU slide remains form-only. The bark is still
too cool and its continuous dark fissures resemble ruled planks. **Reject the
bark**, even at this structure checkpoint: the brief explicitly warned against
carrying that tell forward. Narrow the gray-brown ridges, lower relief to
submillimeter scale, reduce contrast and interrupt fissures across smooth
patches of younger bark. Keep a subdued sheen. The maple branch of that shared
field code must retain its exact old arithmetic/RNG when breakup is absent.

The family view clearly separates a lower divided, broad maple from the taller,
central-led oak. The final oak's 16.95 m card-corner height no longer overshoots
the brief; retained crown top is 16.79 m. The reverse silhouette still has
large angular tier windows and too much visible central axis. Branch ends
remain more compact and sausage-like than either photo, especially Stony
Brook's broader upper crown. These remain structure weaknesses for the lead to
assess, not an approval claim. The upward view reveals flat repeated sprites,
angular thin shoot lines and simplified four-sided fine wood; this cannot pass
as a close botanical view. The low dead pins are visibly present and attached,
but their ends are faceted. Do not hide that behind the manifold test.

Proof at this pass: 24,722 triangles = 9,122 wood + 15,600 foliage; source/game
geometry hashes agree. Wood is one sealed connected component, zero nonmanifold
edges. Measured DBH 0.4311 m, retained crown 9.9938 × 10.0160 m, base 2.5566 m.
Walking clearance near the bole is conservatively 2.767 m using whole-card
bounds. Lower/middle/upper authored limb chord angles are −13.1…−11.2° /
+0.25…+0.30° / +9.3…+47.0° from horizontal. Those are centerline angle
measurements; they do not certify final fused cross-section mechanics.


## Oak pass 5 — checkpoint delivered; stop before leaf look-dev

Evidence: `renders/oak-bark-study/bark.png` and **every final image** under
`renders/oak-checkpoint/`, including both full photo pairs, contact and review
sheet, opened. The source build, independent game build and all ten GPU Cycles
views are current. No final docs image is committed.

**Color/value first:** the narrower, interrupted, lower-contrast bark ridges
are subtler than pass 4's ruled panels, and the base is gray-brown with a mild
sheen. The surface is still too axially ordered in a macro view; it is not a
finished photoreal bark approval. Smooth young limbs remain visually distinct
from the shallow lower-bole furrows. Foliage keeps dark tier undersides, green
mids and neutral pale backs. In the two transparent comparison renders, selected
green display-luminance p5/median/p95 is **.043/.187/.501** (OSU camera) and
**.048/.189/.491** (Stony Brook camera), zero selected-channel clipping. About
**1.17% / .89%** falls below .02. These are render sanity checks, not calibrated
albedos or a claim to match the differently lit/scanned photographs.

The single leader, drooping low limbs, level middle limbs, ascending top and
retained lower pins clearly distinguish the oak from the maple in the family
view. Tier tops light separately and the undersides keep deep recesses. The
remaining shape failures are real: overly compact/sausage-like outer bough
ends, deep angular windows, too much visible axis and a more conifer-like,
ordered upper crown than the references. Stony Brook has broader shoulders.
The widest projected band is too close to the lower skirt. The pins are too
evenly distributed and their ends too faceted. Up close, repeated flat sprites,
angular thin shoot lines and simplified fine wood remain obvious. These are
recorded for the lead's structure review, not excused by the passing tests.
No further structure acceptance or leaf/bark finish acceptance is asserted.

### Checkpoint proof

- `make -C trees SPECIES=oak`: **passed**, references, independent source/game
  rebuilds, construction checks, camera checks, eight presentation/diagnostic
  Cycles views, two photo-camera Cycles views, both pairs and both sheets.
  1200 px width / 40 samples; every Cycles invocation held the shared GPU lock.
- Source/game geometry digest: `a78aa7146e4ec0f6d60db971951c9fec23a8444260de54182d8cf43684b35060`.
  One sealed connected wood surface, zero nonmanifold edges, positive measured
  wood volume 1.6555 m³. Bounds, actual trunk section, alpha support, card
  normals, all Wind values, UV tile bounds/density, graph attachments, retained
  dead pins and limb-zone slopes pass. This is source construction proof.
- **24,722 / 25,000 triangles**, **9,122 wood / 15,600 foliage**; **two materials,
  two static meshes**, 7,800 cards, 38 live laterals and 23 lower dead pins.
  No armature or moving parts. Origin at bole center on grade.
- Measured full card-corner envelope **10.414 × 10.354 × 16.948 m**; retained
  foliage width **9.994 / 10.016 m**, base/top **2.557 / 16.790 m**. Actual
  chest-height fitted diameter **0.4311 m**, conservative near-bole whole-card
  walking clearance **2.767 m**, root reach below 8 cm **0.478 m**.
- Camera projection agreement **.00020 / .00113 px**. Biological fit residuals
  remain **17.2 / 175.3 px** at original photo sizes. Both fits reach the 80 mm
  lens bound, so those lenses are estimates; frame margins give equivalent
  64.5 mm lenses. OSU has clipped apex tips; Stony Brook has left-side neighbor
  occlusion. Neither supplies a surveyed age/height/DBH.
- `renders/oak-checkpoint/shots.json` and `render-check.json`: **all ten current
  source hashes agree**, SHA-256
  `6602c4e26fb86d3003056a1e5ec0947cdc57083b442b591a7e6a1398c4ea9062`.
  The family view also records the actual maple-source hash.
- Packed oak source **43,736,974 bytes**; original prototype BaseColor-alpha
  **589,156 bytes**, **2048²**. Flat prototype Normal/ORM and the intermediate
  analytic bark field are source inputs, not a shipped texture allocation.
  Planned shared 2048² BC7/BC5/ORM set is **16 MiB with mips**, plus geometry,
  aimed below about 20 MiB. **No oak GLB, finished atlas, final unique UV pack,
  re-import or bake-loss certification yet**, as the checkpoint brief requires.
- Renders: `renders/oak-checkpoint/{daylight,crown_up,silhouette,scale,family,
  structure,lower_pins,bark,oak_match_osu,oak_match_stony}.png`;
  `oak_match_{osu,stony}-pair.jpg`, `contact.jpg`, `review-sheet.jpg`.
- `make -C trees check`: **passed** the maple's source, bake, GLB/UV/PBR,
  botanical Wind/normal, bark and camera checks after the refactor. Current
  maple comparison pairs were opened; they retain the accepted appearance.
- `python3 -m py_compile trees/src/*.py`, `git diff --check`, repository rules:
  **passed**. No `kit/` file changed; no kit suite was required. Existing
  `botany` sweeps/cards/Wind, `foliage`, photo matching/framing and shared
  finalize/bake/export/verify code are reused.

### Maple byte comparison — exact data, disclosed GPU rounding

The pre-edit baseline is preserved locally under `build/maple-baseline/`.
`compare_maple_source.py` checks **exact source position, triangle, UV, split
normal and Wind byte arrays and all four packed procedural PNG inputs**:
identical. The original growth JSON is byte-identical. The final comparison
also checks all **12 delivered accessor buffers** byte for byte: identical,
including positions, indices, UVs, normals, tangents and `_WIND`.

Re-exporting the rebuilt finalized mesh with the preserved maps produces the
**entire original GLB byte for byte**, SHA-256
`ad060a9aac22b94d5eb021b2fcf60791044daecb04c14fbe03d590037ff8c945`.
There is no intentional maple geometry, material or source-texel change.

The fresh GPU rebake is not byte-exact. Every changed pixel/channel coordinate
is recorded in `build/maple-byte-comparison.json`; all differ by exactly one
8-bit step. Final repeat results:

| Delivered maple map | Changed channels | Max byte delta | Byte-domain RMSE | PNG bytes |
| --- | ---: | ---: | ---: | ---: |
| T_RedMaple_BaseColor.png | 3 | 1 | 0.0004229 | 1,398,130 |
| T_RedMaple_Normal.png | 9 | 1 | 0.0008457 | 2,411,154 |
| T_RedMaple_ORM.png | 6 | 1 | 0.0006905 | 1,388,798 |

The unchanged **pre-refactor source** GPU control also differs from its own
baseline: 3 / 10 / 5 channels in BaseColor / Normal / ORM, one byte maximum.
This demonstrates the same sparse GPU bake rounding without the refactor.
The new GLB is **7,876,080 bytes**, baseline **7,876,088**;
PNG compression, embedded image payloads and following buffer offsets account
for the difference. Current SHA-256:
`75df16f76446e073ca2b2765169ff7818f595474a7207ee97587506b508e3251`.
Both delivery texture dimensions and allocation stay unchanged: three 2048²
maps, 16 MiB compressed textures, about 18.55 MiB including actual geometry.
The maple remains 23,680 triangles, two materials and two meshes.

Stop here, before oak leaf look-dev, as requested. The lead has the complete
structure evidence and explicit weaknesses to review. No tools, permission,
shared-kit feature or contract change is needed to reach this checkpoint.

# Pin oak / structure round 2 — lead rejection of the fir form

The lead accepted species parameterization, maple preservation, dimensions,
limbed-up trunk and budget, but **rejected the form**. That rejection supersedes
round 1's qualified checkpoint language. The targets now include 35–45 irregular
primaries, real secondary forks, long lower/middle reach, a broad continuous
upper crown and one rounded point. The original checkpoint is archived under
`renders/oak-round1-checkpoint/`.

## R2-A — new ramifications; reject the hollow crown and excess geometry

Evidence: every `renders/oak-r2-a/{daylight,structure,crown_up}.png` opened
against the original OSU summer/leaf-off photographs. **Color/value first:**
the warmer gray-brown wood is closer to the photographs than the old blue-gray
pole; leafy caps still have dark undersides, but bright sky dominates the
empty center. A correct palette cannot repair that form.

Forty irregularly spaced primaries now fork into 124 secondaries, with 744
short live laterals represented by cards. The retained branch reaches approach
5 m and shorten to 1.5 m near 80% tree height. However, the leaf placement is
still too distal and the secondary masses too small: a hollow pole is ringed
by isolated caps, with a separated upper group. Reject this appearance. The
28,114 triangles are also over budget (14,314 wood / 13,800 foliage).

Actions: lengthen the secondary forks, extend foliage along them, broaden
supported branch masses and upper overlap, and rebudget economical small-branch
sweeps instead of dropping anatomical branches. Keep fine live laterals in the
cards. The numerical union audit identified an isolated 20-micron zero-volume
triangle at a dead-twig intersection, **not an anatomical hole**. The family wood
cleanup now removes only a closed sub-0.1 mm membrane or repairs a tiny closed
triangle boundary, rejecting larger defects. No authored limb is discarded.
The maple's exact source-array/image comparison passes with that cleanup.

## R2-B — budget and broad-band profile pass; reject the axial sky window

Evidence: every `renders/oak-r2-b/{daylight,structure,crown_up,bark}.png`
opened. **Color/value first:** lower bark is now neutral gray-brown and young
limbs are smoother/lighter. Dead pins carry a separate gray attribute through
the same wood material; they curve downward and carry fine forks, instead of
being evenly spaced dark rods. Macro bark remains more regular than the photo.

The mesh is 24,310 triangles (12,310 wood / 12,000 foliage). The source envelope
is 10.750 × 10.768 × 16.881 m. Alpha-supported crown width is 10.352 / 10.433 m;
its X/Y mean section profile peaks at **34.3%** of crown height and has **.715**
maximum mean-width/height ratio. These measurements meet the numeric profile
but do not clear the look: the image still has an enormous axial sky window.

A measured cause was the supposedly irregular angular sequence. Its 7–12 m
branches clustered around two opposing sectors; only 66 of 1,184 cards in the
7–9 m band projected within 0.9 m of the daylight camera's centerline. Replace
that correlated rotation with a random candidate distribution that avoids
recently occupied angular sectors. Keep irregular internodes and avoid whorls.
The upper foliage also needs more overlap. One tiny apical limb missed the
30-degree exit-angle floor because its sideways bow was as large as its reach;
scale the bow/side offset with short-limb length, rather than relaxing the test.

## R2-C/D/E — reject numeric success without upper continuity

All C/D diagnostic images, D's two photo pairs, and E's complete ten-view set
were opened. **Color/value first:** the leafy tops and deep undersides have
useful separation, with no clipped green pixels. However, the direct bark
close-up still reads cool in open-sky shade, despite warmer albedos. The OSU
bark photo is medium gray-brown, with small shallow scaly interruptions rather
than long parallel grooves. This remains a correction, not a passed material.

C's balanced azimuths reduced the enormous center window. Initial retained
centerline angles now meet all three zones: lower −18.57 to −14.07 degrees,
middle −4.46 to 11.90, upper 35.04 to 44.64. Yet its 23,992-triangle crown still
had a separated upper cap. D increased the prototype atlas's coverage and
allocated 6,375 cards without adding anatomical branches; its 24,738 triangles
fit. Six fine shoots on the actual leader replaced the old isolated terminal
mass and three peaks. Its alpha-supported mean section profile peaked at
29.34% of crown height, with W/H .723. The mean envelope is the right shape;
the envelope does not measure continuous occupancy.

E lowered upper secondary shoots to overlap the shoulder and shortened dead
pin exposure. Its 24,536 triangles, 40 primary / 119 secondary limbs and .723
mean section ratio passed the numbers. But the daylight and silhouette views
still exposed a distinct upper hat, and the OSU pair showed too much open bole
through the middle. **Reject E as the final checkpoint.** The cause is the
abrupt endpoint change from level middle branches to rising upper branches:
nearby branch roots do not imply nearby leafy growth. Make the outer middle
shoots rise progressively through the shoulder, preserving the middle limbs'
level exit angles. Do not close the gap with an unsupported filler volume.

## R2-F/G/H — supported upper overlap; correct the cool bark

F's daylight and bark images and G's daylight/bark images were opened against
the same photos. **Color/value first:** F's bark was still too dark and cool;
G raises the diffuse gray-brown and lowers specular response. The ridges now
read warm neutral at the light-facing edge, with cool ambient shade retained,
rather than the whole bole looking blue. The flat shallow ridges are closer
to the OSU bark's scale, but the long parallel organization is still more
regular than that photograph. No claim of a finished bark bake is made.

Progressively rising middle endpoints joined the upper masses to the shoulder.
F exposed a middle limb whose *retained first segment* rose 21.83 degrees,
even though its design tangent was level. This is why the test measures the
retained sweep. Lower the design tangent slightly through the shoulder; G's
actual middle maximum is 19.16 degrees. Do not relax the +/-20-degree test.
G uses broader secondary fans and taller middle masses, retaining the low
windows. It is 24,490 triangles. The crown still has a sparse collar under its
upper mass; H extends middle secondaries upward and weights upper leaves
slightly toward their proximal laterals to make continuous supported growth.

A separate reconstruction of the retained bole sweep measures the exposed main
pin centerlines after they leave that surface. One retained pin was only
13.3 cm long, despite a 15 cm minimum *configured horizontal extension*.
Increase that input to 18 cm; final exposed lengths must be measured again.
The audit explicitly distinguishes this from a fused-wood surface measurement.

## R2-I — complete ten-view checkpoint resubmission; stop before leaf look-dev

Evidence: H's daylight preview, every final Cycles view and both final photo
pairs were opened. Final outputs are under `renders/oak-round2-checkpoint/`:
`daylight`, `crown_up`, `silhouette`, `scale`, `structure`, `lower_pins`, `bark`,
`family`, `oak_match_osu` and `oak_match_stony`. The two `*-pair.jpg` files,
`contact.jpg`, `review-sheet.jpg`, `crown-profile.jpg` and
`osu-profile-measurements.jpg` accompany them. No checkpoint image is committed.
The source hash recorded in all ten shots and the render check is
`b3483ec2448d3eb2e89c99135776dad3ad45875435981f467253955f2dfb6184`.

**Color/value first:** the final bole has a medium gray-brown lit surface and
cool ambient shade; the whole trunk is no longer the uniform blue pole of the
rejected candidates. The prototype foliage remains flatter and less glossy
than real summer pin oak. In the OSU source render, selected green display
luminance p5 / median / p95 is **.054 / .198 / .519**, with **.59%** below .02
and **zero** clipped green pixels. Stony is .058 / .196 / .507. These are image
values under the review lighting, not albedo measurements or photo color
calibration. OSU's aged slide remains a form reference only.

**Form:** the longer curved primaries now fork into visibly spread secondary
fans, with irregular heights and azimuths rather than whorls. The top is one
point carried by the leader and is connected to the ascending upper crown;
the earlier detached cap and three competing peaks are gone. The lower crown
is broad, with real downward sweeps and windows between its masses. In the
matched OSU camera, the upper crown now merges into a continuous pyramidal
oval instead of separate terminal puffs.

**Remaining tells, not hidden by passing measurements:** daylight still shows
more middle/lower bole and larger sky windows than OSU. Some lower foliage
masses still finish in compact rounded tufts; card repetition and flat leaves
are obvious in `crown_up`. The highest outline is narrower/more regular than
Stony's broad mature crown. Bark's fissures remain too parallel at macro scale,
and small wood forks show their economical angular sampling. The source-only
leaf-off diagnostic hides the twig-bearing cards, so it is not a claim that a
winter pin oak would have only these retained wood paths. The checkpoint is
submitted for review, not declared a finished/shippable oak.

### Measured crown profile against Oregon State

The source profile clips **actual retained-alpha support hulls on the card
surfaces** by 141 horizontal planes. Holes within one card's alpha hull are not
counted as density; this measures an envelope. A five-plane (~0.5 m) mean
locates the broadest band without selecting a single protruding leaf. No photo
coordinates enter growth, geometry or textures. Independently marked photo
margins are used only by the review/chart code.

- Retained crown base/top: **2.560 / 16.766 m**, height **14.206 m**.
- Global retained X/Y widths: **10.617 / 10.380 m**; global X W/H **.747**.
- Maximum mean X/Y section width: **10.246 m**, W/H **.721**.
- Broadest smoothed band: **6.628 m above grade**, **28.63%** of crown height
  above its base; target 25–35%.
- OSU photo: widest marked band near **30%**, projected W/H **.723**.
  Estimated uncertainty is ±20 px on lateral tips/base; the apex is clipped
  and the lower-left margin partly obscured by a neighbor. This is not a survey.
- The matched render's robust projected section peak is **27.5%**. Its full
  projected crown W/H is **.830**, wider than the photo's .723. The perspective
  camera, different specimens and physical X/Y mean are distinct measurements;
  the close normalized section curves do not establish an exact photo match.

| Crown height fraction | Source X width (m) | Source Y width (m) | Mean width / maximum | Photo width / maximum |
| --- | ---: | ---: | ---: | ---: |
| 10% | 7.958 | 7.668 | .763 | .745 |
| 20% | 9.174 | 9.422 | .907 | .928 |
| 30% | 10.407 | 9.599 | .976 | 1.000 |
| 40% | 9.069 | 9.428 | .903 | .932 |
| 50% | 8.740 | 9.338 | .882 | .857 |
| 60% | 8.528 | 8.281 | .820 | .789 |
| 70% | 6.490 | 7.057 | .661 | .650 |
| 80% | 5.589 | 5.492 | .541 | .549 |
| 90% | 3.178 | 3.100 | .306 | .430 |

The profile substantially fixes the narrow fir envelope: widest low and smoothly
narrowing through the middle/upper crown. The most visible residual envelope
miss is the uppermost 10%, too narrow relative to the clipped OSU slide.
Compare the chart and annotated original photograph with the pair; do not
substitute the numeric pass for the images.

### Measured architecture and budget

All limb reaches, lengths and exit angles below use the **retained sweep
centerlines**, not config constants or only the denser design curves.

| Measurement | Result |
| --- | ---: |
| Complete source envelope, including clear card corners | 10.966 × 10.655 × 16.926 m |
| Trunk diameter, actual section circle fit at 1.35 m | .4331 m |
| Lowest whole-card corner within 1 m of bole | 3.118 m |
| Primary / live secondary limbs | **40 / 119**; **2–4** secondaries each |
| Fine live laterals in cards | 714 secondary laterals + 6 leader shoots |
| Irregular primary internodes | .132–.485 m |
| Primary base profile diameter, including collars | **6.72–11.82 cm** |
| Primary horizontal reach range | .346–**5.102 m** |
| Primary retained arclength range | .474–**5.396 m** |
| Limb at 13.411 m attachment (80.3% of leader height) | **1.509 m** horizontal reach; 1.904 m arclength |
| Lowest primary endpoint | **2.988 m** above grade |
| Lower / middle / upper retained exit-angle ranges | **−18.57..−14.07 / −4.62..19.16 / 35.04..44.64 degrees** |
| Curved main dead pins, with thin side forks | **22** |
| Exposed retained main-pin centerlines | **15.68–37.07 cm** |
| Wood / foliage / total triangles | **11,720 / 12,750 / 24,470** |
| Leaf cards / materials / meshes | **6,375 / 2 / 2** |
| Connected wood components / nonmanifold edges | **1 / 0** |

Dead-pin exposure is measured beyond a separate reconstruction of the authored
bole sweep, not as an exposed fused-surface distance. Branch diameters describe
retained circular profiles including collars, not exact fused cross sections.
The manifold/positive-volume check independently examines the actual wood.

The source file is **44,056,967 bytes**; its three **2048² prototype leaf PNGs**
are **743,807 / 16,914 / 16,914 bytes** (BaseColor-alpha / flat Normal / flat
ORM), plus the original intermediate **2048 × 4096 bark field**. These are
source-development maps, not the final packed atlas or GPU allocation. There
is **no oak GLB yet**. The planned compressed three-map 2048² delivery remains
16 MiB textures plus geometry, targeting about 20 MiB total.

### Proof and scope

- `make -C trees SPECIES=oak`: **passed**, from rebuilt source/game scenes
  through architecture/topology/alpha/Wind/normal checks, source/game audits,
  camera verification, repository rules, all ten GPU Cycles views, both pairs,
  contact/review sheets and the crown profile comparison.
- The source and game geometry digests are identical:
  `e86fecfed548bc31037cbb6f28b38da4434aa77832c58eaa485cf30133def328`.
  This proves the checkpoint does not hide an over-budget high-detail scene;
  it does not certify future GLB serialization or bake loss.
- `python3 -m py_compile trees/src/*.py` and `git diff --check`: **passed**.
- The maple repeat compares all source position/triangle/UV/split-normal/Wind
  byte arrays and four packed PNG inputs with the accepted source; the exact
  comparison passes. Its growth JSON is byte-identical. No maple delivery map
  or GLB was regenerated in this round. The previously disclosed GPU bake
  rounding and exact preserved-map GLB proof remain as recorded above.
- No `kit/` file was changed relative to `main`; the main merge was done before
  this round. Existing kit sweeps/cards/Wind, photo tools and audit helpers are
  reused. No shared-kit feature, tool installation or contract change is needed.

Stop here, before finished oak leaf look-dev, delivery UVs, baking and GLB.

# Pin oak / leaf, bark and delivery finish

The lead accepted the round-2 architecture. This finish preserves the 40
primaries, 119 secondaries, one leader and 22 pins. The three requested form
corrections concern supported inner foliage, drooping lower sprays and the
root flare. Maple's exact-source baseline is retained throughout.

## Preflight — source candidates, not shipping critique passes

Color/value first: the first new leaf atlas changed the blue-green prototype
toward olive. Its source OSU-view bright/dark fifth medians were .515/.115
(photo .649/.119); Stony .506/.120 (photo .494/.080). These are selected-green
display populations, not equal-light reflectance. Later source candidates
exposed too much inner wood and silvery reflection. Reduce the mass-normal
bend .90 to .82, give the backs a matte surface, and move existing cards onto
inner supported shoots. A four-shoot atlas adds distal alternate blades without
more cards. Deep U sinuses, five/seven lobes, bristles, pinnate veins, cups and
cuticle roughness are original equations; no photo pixels enter the generator.
Source evidence: `oak-finish-source1`, `oak-finish-source2` and
`oak-finish-source-final` under `renders/`; every generated view was opened.

The first UV attempt failed: the 15 m leader island consumed the atlas and
left median bark density at 64 px/m, with folded junctions. Shorter leader
sections recovered coverage; isolating triangulated union patches removes
internal folds. The finalizer still independently checks the complete pack.
A stale UV-layer handle in the first preparation script crashed Blender;
refreshing RNA handles after edit-mode changes fixed it. No failed candidate
is accepted. No shared-kit code changed.

## Finish pass 1 — exported GLB rejected for weak bark and remaining bare wood

**Color/value first:** `renders/oak-finish-1/` contains five opened GLB detail/
hero views and both opened full photo pairs. OSU bright/dark fifth medians are
**.576/.089**, photo **.649/.119**; Stony **.454/.076**, photo **.494/.080**.
Lit/shaded hues are **80.6/93.2 degrees** in OSU, against **90.6/109.7**.
The albedo is too yellow, while the photo-camera lighting is short of the
sunlit target. Correct the authored RGB from (83,102,38) to (77,105,48), then
match direct light separately in each photographic view. Same albedo in both;
no emission, painted light or exposure adjustment to the saved images.

The middle is improved but the 5–7 m bole still shows as a shaft. Bring the
inner shoot population closer to its real primary axis. Lower sprays remain
compact: distribute those existing cards along descending secondary curves,
with extension/drop correlated, rather than scattering them around a tuft.
The flare meets the numeric 1.486× DBH target but **still looks bell-like**:
its five roots are buried inside the widening bole. Reduce the core flare and
let shallow buttresses project beyond it, then measure again.

The bark pair fails visibly. Its model/photo patch medians are **.234/.422**
under different illumination. The source albedo is brown; the shaded camera
and blue sky also affect the display value. Inspect a key-facing surface next.
The embedded 2048 map has normal-angle p90 only **3.37 degrees**, cavity AO p10
**.937**, despite genuinely isotropic **432.6–433.6 px/m**. This is bake loss/
insufficient authored relief, not a density excuse. Broaden short fissures and
increase shallow granular/flake relief. Avoid restoring closed cellular walls.

At the overly close .95 m leaf camera, the flat cards and softened veins are
obvious. Increase blade cup/twist in the normal field and inspect a whole
cluster at approximately 1.8 m. The 3 m game-distance question is distinct
from a botanical macro claim. The backlight view has yellow-green transmission
but remains too flat locally; the limbs stay dark. Root, bark, crown-up, leaf
cluster, hero, and both pairs were all inspected, including the marked bark pair.

This candidate's checks pass but its appearance does not: **24,238 triangles**,
**2 materials**, **2048² three-map set**, GLB **8,451,652 bytes**, compressed full
mip textures **16 MiB**, geometry **2,742,996 bytes**, estimated total
**18.616 MiB**. Zero UV overlaps, zero degenerate UVs, zero missed/black bake
interiors of 4,559,883 checked. Raw GLB/fresh-import position and Wind comparisons
pass. The preserved candidate is local `build/oak-pass1.glb`; passing technical
checks do not override the rejected surface and crown observations.

## Finish pass 2 — exported color/value passes, root construction still rejected

**Color/value first:** opened all seven views/pairs in `renders/oak-finish-2/`.
OSU bright/dark fifth medians are **.666/.108**, photo **.649/.119**: deltas
**+.017/−.011**. Stony **.496/.083**, photo **.494/.080**: **+.002/+.003**.
Both populations in both pairs meet .03. OSU lit/shaded hues are **91.6/107.6°**,
photo **90.6/109.7°**. Stony remains greener than its photograph (98.3/111.2°
versus 82.0/91.6°); do not claim both photographs have identical color balance.
The explicit photo daylight controls are OSU sun 19 / sky .25 / exposure .80,
Stony sun 8.3 / sky .25 / exposure .5. These are display-light composition fits,
not a surveyed common illumination or a calibrated photographic albedo.

The brighter OSU image still has overly broad pale caps despite passing green
population values. Reduce normal bending .82→.68 to give individual blades
more independent lighting; keep mass shading and the same card/triangle count.
The close leaf camera now covers an actual outer cluster from 1.8 m. Its blade
cups are stronger, but veins still soften excessively; broaden the midrib at
source resolution. Backlight is visible but too neutral: use a separate thin-leaf
transmission spectrum, with no emission, to favor yellow-green transmitted light.

The bole is screened above most middle branches; the lowest open tiers remain
more exposed than OSU. The lower outer sprays are looser, with finer holes and
a descending edge. The source crown profile peaks at **27.9%**, W/H **.706**;
40 primaries / 119 secondaries / one leader / 22 pins remain unchanged.

Bark now retains **10.23°** normal-angle p90 and AO p10 **.804**, compared with
3.37°/.937 in pass 1. It is shallow, irregular and interrupted rather than
planks or a complete cell mesh. The key-facing comparison is still dark and
short of photographic fine roughness. Delivered chest-height albedo has median
sRGB **(.282,.251,.200)**, linear **(.0648,.0513,.0331)**: brown, not blue.
Raise the gray-brown ridge faces moderately; keep fissures shallow and smooth
limbs lighter. The sky's cool effect is distinct from those raw map values.

**Reject the root shape again:** numeric grade flare **1.428× DBH** and
**1.032× at .50 m** are right, but tube roots emerge through abrupt angular
shelves. Replace the visible tube-root union with five shallow lobes grown into
the bole sweep, fading over its lower half meter. This is a construction/shape
correction, not a numeric-budget exception. Reconstruct the same lobed bole
in the independent pin-exposure probe. The full root view was inspected.

`make -C trees SPECIES=oak check`: passed this candidate's source/game audits,
architecture, camera, UV/PBR, actual GLB positions/normals/Wind, bake coverage
and repository gates. **24,560 triangles** (11,810 wood / 12,750 foliage),
GLB **9,620,444 bytes**, **2 materials**, **18.647 MiB** estimated GPU memory.
All 4,403,078 checked interior bake texels are covered; UV overlap zero.
The pass-2 GLB remains local at `build/oak-pass2.glb`.

## Finish pass 3 — exported blade response and continuous buttresses; fix tile borders

**Color/value first:** inspected all five GLB hero/details and both photo pairs
under `renders/oak-finish-3/`, including the marked bark comparison. OSU
bright/dark fifth deltas remain **+.017/+.010**; Stony **+.028/+.022**. Both
still meet .03, although Stony has little headroom. Its final direct/sky light
will be reduced slightly (7.6/.22) without changing the common authored albedo.
More independent blade lighting (.68 normal bend), stronger midribs and the
separate yellow-green transmission spectrum reduce the broad cap/flat backlight
impression. Deep crown recesses remain. Some mass-level roundness is still
more orderly than in the photographs.

The bark is now medium gray-brown in the key-facing view rather than the old
blue pole. Patch median is **.355**, photograph **.422**; this remains a darker,
cooler display under the model's crown, not an equal-light calibration. Normal
p90 **10.19°** and AO p10 **.812** survive filtering. Fine photographic grain is
still richer. Young limb albedo must remain lighter than the revised bole, so
that specific final setting is raised while retaining its smoother response.

The root shelves are gone. Five shallow lobes are part of the continuous bole
surface, rather than protruding tubes. Measured grade equivalent diameter
**.6149 m / 1.418× DBH**; by .50 m it is **1.043×**. Root reach below 8 cm is
**.3465 m**. The foot remains polygonal in a macro image; its modest extent and
continuous transition are correct. The mesh is **24,234 triangles** after
removing the redundant buried-root sweep geometry; accepted live architecture
and pins are retained. Original root design paths remain in growth metadata to
preserve the accepted branch random sequence; they are not counted as surfaces.

**A further real defect, caught in atlas inspection:** the first four variants
have 57/58/4/107 retained border texels. Some complete blades cross the tile
edge. This can create hard straight edges in the upward view and invalidates a
claim that every delivered blade retains its whole authored length. Move the
few affected blade bases inward, reconnect their petioles and assert empty
borders in every generated tile. Do not enlarge or shrink leaves to hide it.
Add an actual 3 m cluster inspection alongside the 1.8 m view.

The preparation seam probe and finalizer also used different image aspects.
The resulting eight residual overlaps cover only **.287 delivered pixels**
in total and pass the kit tolerance, but they are disclosed, not called zero.
Use the final target aspect in the probe too before the final clean rebuild.
The candidate remains local at `build/oak-pass3.glb`. Next is the complete
clean-built GLB set, with both photographs repeated on source and export.

## Finish pass 4 — full-resolution export: reject the repeated twig fork at 3 m

**Color/value first:** the 1600 px / 72-sample hero and all four turnaround
views retain olive summer greens, deep recesses and unclipped-looking rolled
highlights. Bark remains cooler/darker in shade than the photographic patch;
raw embedded albedo stays gray-brown. The scale, lower pins, roots, backlight,
family and both 1.8/3 m cluster views were also opened. These thirteen GLB views
are archived as `renders/oak-finish-4/`, with `build/oak-pass4.glb`.

The continuous shallow buttresses, finer outline and screened upper bole are
retained. The real 3 m inspection found a failure that the distant hero hid:
**the same bare four-prong convergence appears repeatedly below leaf clusters**.
The eight variants varied blades but not enough of the twig topology. Reject
this result for the explicitly requested 3 m view. The old four-shoot atlas
will not ship. Replace it with one curved continuation plus two or three side
shoots attached at staggered nodes, vary their lengths/attachments, and put
leaves nearer the start of the short laterals. Keep the same physical blades,
card count, tree geometry and texture allocation. This directly addresses the
repeating sprig, without disguising it with a different camera.

The technical checks passed this candidate (24,234 triangles; two materials;
16 MiB textures / 18.615 MiB total estimate; 9,787,644-byte GLB). The source
comparison and bake-loss sequence was stopped after that visual rejection;
incomplete pair output from this candidate is not final evidence. No docs JPGs
were committed. The final photo pairs and complete presentation must be rebuilt
from the corrected export.

## Finish pass 5 — final exported GLB, source/export pairs and complete delivery

**Color/value first:** all final views were opened individually or on the CG
contact, with the leaf macro, actual 3 m view, upward backlight, bark pair and
both source/export photo pairs inspected separately. Source/export both use
1600 px / 72 samples and the same fitted daylight/camera settings.

| Display population | Export | Source | Photo | Export − photo |
| --- | ---: | ---: | ---: | ---: |
| OSU bright fifth | .67027 | .67002 | .64866 | +.02162 |
| OSU shaded fifth | .12861 | .12944 | .11934 | +.00927 |
| Stony bright fifth | .50507 | .50312 | .49368 | +.01139 |
| Stony shaded fifth | .09080 | .09135 | .08012 | +.01068 |

All four values meet .03; maximum source/export difference is **.00195**.
OSU lit/shaded hues are **86.28/98.14°**, photo **90.62/109.67°**. Stony is
**89.89/102.36°**, photo **82.04/91.55°**. Hue is closer in the lit crown;
shade still differs across the different photographs. Same authored albedo in
both views; OSU sun/sky/exposure **19/.25/.80**, Stony **7.6/.22/.5**.
This is an explicit display-light fit, not identical illumination or calibrated
reflectance. Green hero p5/median/p95/p99 is **.0973/.2774/.5710/.6491**,
with **zero clipped green channels**, **.366%** below .02. Neutral highlights,
wood and background are outside that selected-green mask.

The staggered 3/4-shoot variants remove the rejected bare pitchfork in the
actual 3 m export image. No complete blade reaches a tile border. Alternate
five/seven-lobed leaves retain deep rounded cuts, bristles, brighter pinnate
ribs and varied cup/twist response; whole blades measure **8.14–12.88 cm**
including card scaling. The 1.8 m macro still exposes planar construction and
filter-softened bristles. Backlit blades now glow yellow-green while the limbs
stay dark. No emission is used. Upper/middle foliage is continuous, with deep
recesses and small sky holes; low sprays have a ragged descending edge. The
lowest tiers remain more open/ordered than OSU, with some isolated rounded
clumps. That visible residual is not cleared by numeric form checks.

Bark export/source patch medians are both **.362**, photograph **.422**.
Gray-brown albedo is independently read from the embedded map: median linear
RGB **(.0865,.0742,.0513)**. The cooler shaded display is therefore distinguished
from a blue albedo. Directional chest-height density **438.68–440.00 px/m**;
normal angle p10/median/p90 **1.31/4.71/10.19°**, AO p10 **.812**. The scaly
split/rejoin field survives baking; fine photo grain is still richer and the
model's bark patch remains darker/cooler under different illumination. Source
and export bark pairs were opened separately. Five shallow buttresses are now
continuous with the bole, with grade flare **1.418× DBH**, **1.043× by .50 m**.
The foot and isolated thin limbs remain visibly economical at macro distances.

### Final build proof

- The oak was rebuilt after `make -C trees SPECIES=oak clean`; a failed seam
  diagnostic was repaired, then `make -C trees SPECIES=oak` completed. The later
  sprig correction rebuilt both sources, UVs, 4096 GPU bake/composite, 2048 maps,
  GLB and the entire final set. **Final `make -C trees SPECIES=oak`: passed.**
- Explicit **`make -C trees SPECIES=oak check`: passed**; **`make -C trees check`:
  passed** for maple. Camera, source/game audits, actual architecture/topology,
  atlas/GLB/PBR, linear Wind, normals, bake and repository checks pass. Same
  source/game geometry digest is checked independently. All Cycles operations
  used the shared GPU lock. No shared-kit file changed.
- **24,234 triangles** = **11,484 wood + 12,750 foliage**, **6,375 cards**, two
  materials / two static meshes. **40 primaries / 119 secondaries / one leader /
  22 pins**. Longest reach **5.102 m**, reach near 80% tree height **1.509 m**.
- Full card envelope **10.771 × 10.610 × 16.931 m**; alpha-supported crown
  **10.471 × 10.255 m**, base/top **2.504/16.826 m**; actual fitted DBH **.43353 m**.
  Broadest smoothed mean section at **27.92%**, W/H **.70154**. This preserves
  the accepted branch architecture; the finer atlas/sprays change the visible
  alpha envelope slightly from the prototype's .721 section ratio.
- Shared **2048² BaseColor-alpha / OpenGL +Y Normal / ORM**. PNG bytes
  **1,747,351 / 3,216,779 / 1,726,833**. **GLB 9,437,096 bytes**.
  Full-mip compressed textures **16 MiB**, actual geometry **2,741,564 bytes**,
  estimated combined **18.6146 MiB** before engine overhead.
- Bake: **zero missed/black interior texels of 4,665,705** checked. Unique UV
  coverage **29.1067% of the full atlas**, with the lower half reserved for
  leaf reuse. Zero degenerate/outside UV triangles. **Eight subpixel overlaps**
  total **.287 delivered pixels** (fraction 2.354e-7), within the independent
  kit tolerance; not misreported as zero. These persist after aspect matching.
- GLB/raw accessor/fresh import: position and linear Wind errors **zero**;
  maximum split-normal vector difference **8.30e-5**. `_WIND` retained without
  `COLOR_0` albedo multiplication. Origin at trunk base on grade; no rig/moving parts.
- **15 Cycles + 1 Eevee** hashes match final oak SHA-256
  `82b2a27bd291f9aae703b66debaf932e839942bba612261f9da39ed062fbab3b`.
  The family checks the actual imported maple GLB hash as well. Eevee is
  visibly cooler, paler and flatter than Cycles; it is included honestly.
- Final images: `renders/oak-final/{hero,front,side,back,top,branchlet,cluster_3m,
  bark,lower_pins,crown_up,scale,root_flare,family,oak_match_osu,oak_match_stony}.png`;
  both `oak_match_*-pair.jpg`, `bark-pair.jpg`, `turnaround.jpg`, `details.jpg`,
  `contact.jpg`, `review-sheet.jpg`; `renders/oak-final-eevee/hero.png`.
  Source pairs/bark: `renders/oak-final-source/`. All were opened.
- Final docs only: `docs/oak-hero.jpg` **193,874 bytes**, `oak-details.jpg`
  **199,786 bytes**, both at most 1600 px wide. Five family docs JPGs total.
  No photo, private-person/home identifier, generated binary or texture is committed.
- `python3 -m py_compile trees/src/*.py`, `git diff --check`, repository rules:
  passed. Kit regressions are not required: no `kit/` file changed.

### Maple preservation repeated on the final shared code

`compare_maple_source.py` passes exact source position/triangle/UV/split-normal/
Wind byte arrays and all four packed procedural PNG inputs. The growth JSON
and all 12 final accessors are byte-identical to the preserved original.
Re-exporting the **latest finalized mesh with the preserved maps** reproduces
the complete original GLB, SHA-256
`ad060a9aac22b94d5eb021b2fcf60791044daecb04c14fbe03d590037ff8c945`.
The fresh GPU bake changes **4 / 8 / 5 channels**, each by one byte, in
BaseColor / Normal / ORM, with the unchanged-source control's same sparse
rounding class disclosed. Fresh GLB **7,876,076 bytes**. Reports:
`build/maple-source-comparison-finish.json`, `build/maple-byte-comparison-finish.json`.
There is no intentional maple geometry, material or source-image difference.

No tool, permission or kit/contract change is needed. Engine work remains the
usual foliage shader, Wind, LOD and impostor integration. Remaining visual
weaknesses are recorded above; no claim of botanical-macro photorealism is made.

# Pin oak / lead-directed bark, lower crown and display-value correction

## Revision pass 6 — exported GLB, reject residual bark regularity and dark Eevee

**Color/value first:** inspected the two photo pairs, Cycles/Eevee heroes,
chest-height bark and the new raking view from 1 m in `renders/oak-revision-6/`
and `renders/oak-revision-6-eevee/`. These are the exported, rebaked candidate,
1100 px / 32 samples, preserved as `build/oak-pass6.glb`.
OSU median foliage is **.32696 / photo .33543**, pixels above .5 **28.81% /
25.81%**; bright/shaded fifth deltas **+.02531 / +.00056**. Stony median
**.22332 / .20975**, above .5 **8.53% / 9.61%**, fifth deltas **−.01100 /
+.00425**. Median and fifths meet .03. The exact original green selector is
retained for comparability; a second, less selective population includes
near-neutral green highlights and is separately recorded, never silently
substituted. Remaining pale caps are concentrated spatially rather than proved
away by whole-image percentiles. Lower specular (.18), a .48 front roughness
floor, .32 transmission and reduced shared normal bending (.42) keep more
individual blade lighting and saturation. Same authored leaf atlas and variants.

Bark patch **.43417 / photo .42210**, median RGB **(.41569,.44314,.39608)** /
**(.42353,.42745,.37255)**. Red now exceeds blue, but the model still leans
more green than the photo. The continuous procedural 2–5 cm / 10–40 cm net
replaces disconnected ticks; raking light reveals physical normal relief at
1 m. Reject the remaining regular cross seams and soft ridge faces. Next:
shallow cross-break color contrast, stronger longitudinal hierarchy, warmer
ridge tops and more chest-height UV density using the same atlas allocation.

The lower 789-card allocation is now **2,127**; inner growth screens the old
3–5 m pole. Remaining large windows and exposed spokes around 6–8 m still need
short lateral sprays farther sideways and upward/downward into neighboring
tiers. Lower primaries now bend in continuous descending arcs; four sides and
ten stations spend their geometry on curvature. Counts stay **40 / 119 / 22**.
**24,744 triangles**, two materials; full source, UV, GLB, Wind and bake checks
pass, including zero UV overlap and zero missing/black bake interior texels.

Eevee's world-only teal fallback is replaced with a captured canopy irradiance
volume using the actual exported cards. Hue difference is now **.02592 turns**,
but median Y is **.12950 vs Cycles .27264**: reject the dark result. Its captured
indirect light needs engine calibration. No image recoloring or albedo swap is
used. No docs JPGs are updated for this candidate.

## Revision pass 7 — exported value/hue pass; retain breadth and improve ridge grain

**Color/value first:** inspected both exported photo pairs and the Cycles/Eevee
heroes, bark pair and 1 m raking view in `renders/oak-revision-7/` and its
`-eevee` folder. The warm-gray bark now measures **.415 / photo .422**, with
red above blue; the channels and foliage populations are preserved in its
`color-value-evidence.json`. The calibrated Eevee ambient hemisphere passes
both hue and value against Cycles, without changing the maps, sun or foliage
shader. The captured-volume trial remains rejected: it lost thin-leaf indirect
transport. Eevee uses a documented .18 ambient strength and (1.22,1,.70)
indirect spectral multiplier to approximate the missing warm canopy/grade
bounce. The camera still sees the same procedural sky. This is explicit
presentation-light calibration, not an albedo or image-color correction.

The bark no longer has the conspicuous black transverse symbols. Long fissures
split/rejoin and the raking image proves relief, but ridge faces remain too
soft and uniform against OSU's finer roughness. Give the delivered grain more
relief and variation, and widen the narrow longitudinal fissures modestly.
The same 2048 atlas now assigns about **649 px/m** to the chest band. A
micron-wide Boolean triangle initially collapsed under float UV precision;
its isolated island now has increased UV priority, preserving the unchanged
mesh. Final packing has zero degenerate or overlapping triangles. The old
maple median-density ceiling (500) does not describe this deliberate oak
allocation: declare the oak chest-band ceiling of 750 rather than scaling the
new detail back out. No kit threshold is changed.

The inner low foliage improves the pole, but some outer lower secondaries
became too sparsely covered and their breadth fell to **.682** mean W/H.
Reject this regression even though full width still fits the envelope. Restore
leaf-bearing secondary extensions, distribute the low allocation equally along
primary laterals and the inner secondaries, and preserve supported outer sprays.
Keep the accepted wood architecture and **24,984** triangle total. The candidate
is retained as `build/oak-pass7.glb`; it is not final and no docs are updated.

## Revision pass 8 — exported measurements pass; spend hidden wood on remaining low windows

**Color/value first:** inspected all six GLB preview views/pairs in
`renders/oak-revision-8/` and its Eevee hero. Bark **.41368 / photo .42210**,
RGB **(.41569,.41961,.35294)** / **(.42353,.42745,.37255)**; red minus blue
**+.06275 / +.05098**. Longitudinal relief is visible in the actual 1 m raking
view. The source field has more granular faces and narrow, darker longitudinal
fissures, with cross breaks kept shallower. No blue albedo or isolated symbol
mask remains. The tree-view bole is dark and warm under the crown.

OSU foliage median **.31430 / .33543**, above .5 **27.90% / 25.81%**;
bright/shaded fifth deltas **+.02251 / +.00169**. Stony median **.21703 /
.20975**, above .5 **8.22% / 9.61%**; fifth deltas **−.01440 / +.00815**.
All median/fifth value limits and the Eevee hue/value limits pass. The explicit
mask/sampling limits remain recorded; the near-neutral highlight population
is additional evidence, not substituted for the original mask.

Breadth is restored: measured mean W/H **.72032**, broadest band **30.77%** of
crown height. **24,984 triangles**, both `make check` species gates pass. The
primary lower arcs and central screening are improved. Still reject the large
low side windows compared with the photograph. Recover triangles from axial
rings in small secondary wood hidden by foliage (four stations to three,
retaining cross sections), and place the recovered allocation specifically on
low sprays. Keep all primary curves, upper card allocation, branch counts and
pin geometry. This addresses the brief's request to take triangles where they
do not change silhouette, rather than accepting residual windows at the cap.
The candidate is local `build/oak-pass8.glb`; final docs remain untouched.


## Revision pass 9 — final export, measured bark distance and complete replacement finals

**Color/value first:** opened all sixteen Cycles GLB views and the Eevee hero,
the full contact/turnaround, both final/source photo pairs, bark pairs and the
actual 3 m leaf inspection. All shipping views are 1600 px / 72 samples. The
near-final OSU bright fifth missed .03 by .00004 at full resolution; it was not
rounded into a pass. Further direct/exposure trials were inspected. The final
OSU light is **sun 11 / sky .25 / exposure 1.05**; Stony remains **7.6 / .22 /
.5**. Both source and export use those same per-view fits and the same authored
albedo. The full final comparison now passes with useful headroom.

| Display population | Export | Source | Photograph |
| --- | ---: | ---: | ---: |
| OSU median Y | 0.32220 | 0.32308 | 0.33543 |
| OSU above .5 | 26.29% | 26.40% | 25.81% |
| OSU bright fifth Y | 0.65935 | 0.65886 | 0.64866 |
| OSU shaded fifth Y | 0.12382 | 0.12441 | 0.11934 |
| Stony Brook median Y | 0.21104 | 0.21181 | 0.20975 |
| Stony Brook above .5 | 9.10% | 9.03% | 9.61% |
| Stony Brook bright fifth Y | 0.48874 | 0.48791 | 0.49368 |
| Stony Brook shaded fifth Y | 0.07902 | 0.07904 | 0.08012 |

The original strict green selector is explicit in every result. The looser
neutral-highlight diagnostic can admit tinted sky/grade and is not called
segmented foliage. The projected upper half is also recorded: OSU median
**.38504 / photo .36654**. Its above-.5 share **34.44% / 28.48%** remains more
concentrated than the photograph even though the whole-crown share is close.
This is a remaining CG tell, not concealed by the passing whole-crown median.
The hero's green p5/median/p95/p99 is **.09277/.25781/.53967/.63349**,
with zero clipped channels and **.152%** below .02. Sheen stays local to blades;
backlight stays saturated yellow-green, without emission.

Bark patch Y is **.40779 export / .40667 source / .42210 photo**. Median RGB
is **(.41176,.41176,.34510)** versus **(.42353,.42745,.37255)**. Model red/blue
**.41176/.34510**, photo **.42353/.37255**: both have red above blue. The
export/photo Y delta is **−.01432**, within .03. The tree-view trunk is warm and
dark under the crown, with foliage screening the previous low pole. Continuous
interlacing ridges replace isolated dark symbols. Brown fissures and irregular
flat faces survive the bake, with directional density **648.35–650.32 px/m**,
tangent-normal p10/median/p90 **1.71/6.13/19.94°** and AO p10 **.871**.
Fine photographic grain is still richer. Source and export bark were inspected.

The raking camera was moved back after checking that the earlier nominal meter
was measured to the axis. A ray against the delivered wood now measures
**1.00351 m camera-to-bark surface**. Only that affected view and the revised OSU
fit were regenerated; the complete set was reverified afterward. The default
rebuild uses the corrected camera. This is an actual exported-surface distance,
not a camera-placement constant. The final review enforces .95–1.05 m.

Eevee/Cycles hue difference is **.00578 turns (2.08°)**, median Y difference
**+.00112**, mean HSV value difference **−.00106**: all meet .05. The documented
Eevee ambient approximation uses the same maps, sun and leaf shader; no image
recoloring or leaf albedo swap is used. Its shading remains flatter than Cycles.

The low allocation is now **2,844 cards**, versus 789 before this correction.
Primaries keep ten-station continuous drooping arcs; hidden secondary axial
rings recover **1,008 triangles**, of which 840 fund 420 extra low cards.
All **40 primaries / 119 secondaries / one leader / 22 dead pins** remain.
Longest reach **5.102 m**, near-80%-height reach **1.509 m**. The alpha-supported
crown is **10.667 × 10.155 m**, base/top **2.570/16.752 m**; broadest mean
section at **30.77%**, W/H **.72683**. Near-bole conservative walking clearance
is **2.581 m**. Lower foliage now forms a connected dark skirt with glimpses
of wood. Some outer tier gaps remain too orderly; exposed small secondary
segments are angular in the foliage-hidden diagnostic. Planar cards and softened
bristles still show in macro views. Bark silhouettes remain smooth because its
fine relief is normal mapped. These limitations remain visible and disclosed.

### Final revision proof

- **`make -C trees SPECIES=oak`: passed**, including docs and every check.
  Explicit `make -C trees SPECIES=oak check` and **`make -C trees check`** passed.
  The source/game digest, actual construction, camera projection, UV, PBR,
  raw-accessor/fresh-import normals/Wind and repository rules are separate gates.
- **24,816 triangles = 10,536 wood + 14,280 foliage**, **7,140 cards**, two
  materials / two static meshes. Source and exported counts agree. Origin is
  the trunk base on grade; Wind is retained as linear `_WIND`.
- One **2048² BaseColor-alpha / OpenGL +Y Normal / ORM** set, from 4096 baking.
  PNG bytes **2,278,961 / 3,890,487 / 1,746,972**. GLB **10,822,788 bytes**.
  Compressed full-mip texture estimate **16 MiB**, geometry **2,901,792 bytes**,
  combined **18.7674 MiB** before engine overhead.
- Unique wood UVs cover **30.2812%** of the full atlas; zero overlap,
  degenerate or outside triangles. Leaf reuse stays inside its declared region.
  Bake interior has zero missed/black texels. The JSON records the checked count.
- The complete final set is **16 Cycles + 1 Eevee**, matching GLB SHA-256
  `0a554a3dfb3eff604712c794c43d3feeb4353ff6642e2da9ff6a0a12504b23d1`.
  The family also verifies the actual imported maple hash. Finals and contacts:
  `renders/oak-final/`; Eevee: `renders/oak-final-eevee/hero.png`;
  source bake-loss evidence: `renders/oak-final-source/`.
- Source/export median foliage differences stay below **.0009**; maximum
  bright/shaded-fifth loss is **.00083**. Bark patch loss is **.00112**.
- Final docs replace `docs/oak-hero.jpg` (**190,040 bytes**, 1600²) and
  `docs/oak-details.jpg` (**171,264 bytes**, 719 × 1600) in place. Five family
  JPGs total. No downloaded photo, texture, binary or private identifier is added.
- Maple exact source arrays/four source PNGs, growth JSON and all twelve final
  accessors pass again. Re-export with preserved maps reproduces the original
  GLB byte for byte (`ad060a9aac22b94d5eb021b2fcf60791044daecb04c14fbe03d590037ff8c945`).
  Fresh GPU maps differ in **5 / 6 / 5 channels**, each one byte, consistent
  with the unchanged-source control. Fresh maple GLB **7,876,072 bytes**.
  Reports: `build/maple-source-comparison-revision.json` and
  `build/maple-byte-comparison-revision.json`.
- No kit changes. Early manual previews mistakenly overrode the inherited GPU
  lock with a worktree-local lock; corrected before the shipping bake/finals.
  The final bake and every shipping render inherited the shared `ASSETS_GPU_LOCK`.
  No tools or approval are needed from the lead.
