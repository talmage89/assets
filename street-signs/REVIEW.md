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
