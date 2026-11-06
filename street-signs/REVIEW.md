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
