> **Current checkpoint: structure round 3, appended below.** Earlier findings
> are historical. Round-1/2 images remain under `renders/round1-checkpoint/`
> and `renders/round2-checkpoint/`; current views live in `renders/checkpoint/`.

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
