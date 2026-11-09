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

## Archived rejected LOD reports — round 1

These reports are rejected evidence, not delivered chains.

## LOD rollout status: blocked

The largest multi-plate kind was tested first. Its school-speed trial below
passes the switch images but fails the independent UV/tangent audit. The
printed primitive gains three/two zero-area UV triangles at LOD1/2; LOD2
also gains a zero-length tangent. No sign chain is adopted. The other
assemblies and legacy name variants retain their original LOD0 deliveries;
their measured costs remain in the tables above. This failure does not approve
or reject an untested kind's appearance.

`make lod` and `make check-lod` currently reproduce this blocked trial only.
The two original checks, `make check set-check`, pass before and afterwards
with accepted generated inputs explicitly frozen. The literal tool/recipe and
all original delivery/map/docs bytes remain unchanged.
[Two LOD critiques and raw per-material evidence](REVIEW.md#lod-rollout-2026-11-09).

<!-- LOD checkpoint school-speed: begin -->
## School speed assembly LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/school-speed/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 1,400 / — | 2 / 2 | 113,009 | 674,885 | 787,894 | 5.333 + 0.1035 | near |
| LOD1 | 722 / 560 | 2 / 2 | 69,397 | 674,885 | 744,282 | 5.333 + 0.0631 | 25.0% / 11.97 m |
| LOD2 | 512 / 210 | 2 / 2 | 49,461 | 674,885 | 724,346 | 5.333 + 0.0441 | 9.0% / 33.24 m |

Chain check: True; image check: True; normal check: False.


Whole-chain resident GPU estimate: **5.544 MiB**, versus LOD0 alone **5.437 MiB**. Unique textures 5.333 MiB = 5.333 MiB original + 0.000 MiB proxy/impostor; all meshes 0.2108 MiB. Increase over LOD0 0.107 MiB = 0.000 MiB far maps + 0.1073 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/school-speed/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/school-speed/check.json` and `export/lod/school-speed/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 1 × 2048×2048; LOD1: 1 × 2048×2048; LOD2: 1 × 2048×2048.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 2,634 | 2 | 6 | 906,752 | 5.5441 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 2 to 2 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint school-speed: end -->
