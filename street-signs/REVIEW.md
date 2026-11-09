# Review log

Pass 1: opened source hero, bracket and rear close-ups, and photo pair. Found
clipped street suffixes in the authored rasterization, undersized STOP capitals,
and unslotted saddle blocks. Fixed the text canvas to its measured font bounds,
set 254 mm STOP capitals, cut actual blade slots, and seated screw heads on the
clamp surfaces. Corrected post-hole spacing to 25.4 mm. Added the pinned sleeve
at grade. The comparison exposed an EXIF-orientation composition bug; the kit
now uses upright reference coordinates consistently. These images are local
research comparisons only, never source textures.

Pass 2: opened the revised source hero, two details, upright photo pair, all
eight exported-GLB Cycles views, Eevee and the nine-view contact sheet. Ran
`make match-final PASS=review2 WIDTH=900 SAMPLES=24` and opened its GLB/photo
pair. The plate outline, readable full legends and stiff sheet construction now
read correctly. Rectangular source print aspect was distorting shared UVs;
disabled source-image aspect correction, retained all overlap/outside checks,
and obtained a valid family atlas. All four GLBs independently pass and embed
identical texture bytes. The installed assembly is 568 triangles, not the 928
triangle bake workspace (which includes parked name templates).

The exported text and perforations soften as expected at 1024; tiny fasteners
become darker than the procedural source. Rear plate and slotted saddles stay
supported. Surface-based checks independently prove the post/spacer/plate,
saddles/blades and pin/sleeve load path; GLB checks prove unchanged geometry and
UVs. These are distinct checks. True retroreflection and regulated alphabet
forms remain material/font approximations, not claims of certification.

Photo-fit RMS is 86.34 pixels in the 2150-pixel crop; lens hit its 180 mm fitted
bound and is poorly constrained by this nearly coplanar plate. This is an
estimated same-view comparison, not recovered EXIF or exact photographic pose.
The older scanned reference has a warm cast and perspective not copied into the
new green residential blades. Two source critique passes plus the shipped-GLB
comparison are sufficient for this repeated street prop.

## Added set finish pass 1

Color and value first: the form palette did not separate plain metal from
sheeting. The independent added set now uses metallic aluminum/zinc and two
daylight sheeting grades on its one shared image. Read SHS Appendix 6-10/6-58
and opened the generated figures beside the book: replaced the generic figures
with original grid primitives and curved torso contours. School has child left,
adult right and distinct satchels. Exact federal lettering and headlamp return
remain approximations. The earlier STOP/blade delivery is unchanged.

## Added set finish pass 2

Color and value first: opened the exported 1440 px R2-1 close-up and full
warning lineup. Neutral white, dark black and separate yellow/FYG survive the
shared sheet. Corrected pedestrian/school silhouettes read at lineup distance.
The speed face still reveals substituted letter outlines and slightly faceted
corners under macro inspection. Rejected the green-road presentation error;
its ground-plane/tree-density corrections await the next exported street image.
Full details and image paths are in [SET_REVIEW.md](SET_REVIEW.md).


## Added set finish pass 3 — final audit

Color and value first: reviewed the exported street hero, complete lineups,
face/back/base/band details, Eevee and balanced shaded R2-1 pair at full size.
The final white ROI is 0.434 versus the photograph's 0.436 display luminance;
black print stays dark under raking sun. Concrete controls the photo balance.
The detailed third pass and remaining limits are in SET_REVIEW.md: open-font
outlines, softened minute sheeting detail, flat support-hole indications and
no true headlamp retroreflection. The SHS appendix comparisons and all current
exports are linked there. The accepted STOP/blade delivery and its three docs
images remain byte-identical. Two new JPGs extend this family's docs to five.

## LOD rollout, 2026-11-09

Frozen kit/recipe revision `c339679`; the 103 literal hashes are in
`build/lod-rollout/street-signs/freeze.sha256`. The original legacy and added-set
`make check set-check` passes before the trial, with accepted generated inputs
frozen by explicit `-o` arguments. Exact command, exit and memory receipt:
`build/lod-rollout/street-signs/original-before.json`.

### LOD critique 1: exported school-speed assembly

Started with the largest multi-plate kind, at 1400 triangles, on the original
shared external 2048 sign sheet. Opened all six native strips, each including
original/preceding/new/amplified difference, three construction views and the
contact. Color/value first: white and yellow-green sheeting, dark letters,
metal backs and zinc pole agree at both switches. The pole keeps coverage;
the 20 and SCHOOL remain readable, while the small time legend becomes
subpixel at 9%. The 722/512 levels pass all six native image gates at
25%/9%, 11.97/33.24m, but miss their 560/210 goals. The close LOD2 view exposes
cut-away edges of the SCHOOL plate and coarse backing/fasteners; no close-view
equivalence is claimed. No image, palette or material is changed.

### LOD critique 2: independent audit rejects the chain

`make check-lod LOD_THREADS=4` returns 2. Geometry/re-import and source-byte
checks pass, but `normals-vs-lod0.json` rejects both levels for new zero-area
UV triangles and LOD2 for an invalid tangent basis. Inspected the actual
accessors independently with NumPy, recorded in
`build/lod-rollout/street-signs/raw-field-counts.json`. Source primitive 1
has 114 triangles and zero degenerate UVs; LOD1 has 88 with three degenerate
UVs; LOD2 has 62 with two. Source has zero zero-length tangents; LOD2's
metal primitive gains one. Its maximum new tangent-length error is 1.0.
These are separate from the source's inherited flat UVs on unprinted metal.
The source normal directions still agree, illustrating why that check alone
cannot approve the result. Passing native RGB/coverage cannot waive the audit.

Stopped this family under the brief's frozen-tool-defect rule, without tuning
other kinds or bypassing the failed gate. A general correction needs an
isolated regression and fresh frozen proof; none is made during rollout.
All other delivered kinds remain LOD0 pending that work, including already
compact 446–712-triangle pieces and 568-triangle legacy name variants. No
untested kind is described as having a passing chain. The original per-kind
triangles, materials, bytes and shared map costs remain in the existing README.

Preserved config, every payload hash and native image under
`build/lod-rollout/street-signs/school-speed-pass1/`, as well as the canonical
failed output and `school-speed-pass1-check.{json,log}`. Measured tables/contact
are `build/lod-rollout/street-signs/report/`, generated with reporting-only
`--allow-failed` and opened afterwards. The original `make check set-check`
passes again (`original-after.json`). Only the original 5.333 MiB sign image
is referenced; no new image is added. Full tested-chain residency and stored
costs are in the measured README block. All other original exports and docs
remain untouched; final literal and preservation checks accompany closeout.
