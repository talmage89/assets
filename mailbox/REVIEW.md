# Mailbox review

Pass 1: opened the closed/open source, mechanism and timber details and the
manufacturer pair. The traditional silhouette and hollow/open door read, but
flat roof strips, an accidentally rotated print, very pale wood and a matte
charcoal finish made it look synthetic. Smoothed curved sheet normals, repaired
print-corner UV ownership in the kit, added lengthwise fibers and end grain,
and changed the powder coat to a darker, glossier black. Eagle, branded handle
and approval stamps are deliberately not copied. The camera initially had the
crop origin subtracted twice in the asset landmarks; corrected that error.

Construction sweeps found a crown/catch collision, lower door/pin interference,
and an inboard bracket crossing the swinging face. Bent the catch above the
crown, lowered the hinge axis 0.5 mm, moved the fixed cheeks outboard and joined
them to the shell with anchored tabs. Hinge ears now have real bores. Source
sweeps at one-degree steps pass with a 0.05 mm tolerance, not a relaxed visual
exception. The kit's documented spring and pin contacts stay narrowly named.

Pass 2: opened revised source views and the correctly framed photograph pair.
The address reads, roof reflection is continuous and flag/door poses work.
End grain exposed a shader-vector output error (noise blobs rather than rings);
replaced it with explicit radial arithmetic and softened the ring contrast.
Darkened/glossed the finish to approach the photographed powder coat. Camera
fit is a construction comparison against a slightly larger modern box, not a
claim of reproducing the manufacturer's envelope or hardware.

First GLB review: motion passed, but the address was a black rectangle. The
separate source print sheet shadowed the underlying door during AO baking.
Moved the original print shader/UVs onto the actual stamped front face, removing
the extra print plane entirely. Rebake required. End-grain ring contrast was
softened and its phase varied spatially to avoid perfect target rings.

Final corrected GLB: opened every Cycles view (hero, front/side/back/top,
mechanism/timber details, human scale and open pose), Eevee, contact sheet and
`renders/review4-glb/shell-pair.jpg`. Address 1847 now reads with no black AO
rectangle. Roof curvature, returned door and independent flag survive the bake.
Tiny hardware has stronger/darker contrast and fine fibers soften at 1024; the
wood is deliberately lightly weathered, not deeply split. The larger modern
photograph still has a glossier finish and different latch/flag details. The
final pair includes the real exported support below the reference-only box.

`make all match-final PASS=review4` passes, including all normal `make check`
prerequisites: 1,264 triangles, one material, three 1024 maps, 1,300,792-byte
GLB, 71.15% UV coverage and no overlaps. Reimport position error is zero.
The imported Door/Flag sweeps test 106/91 positions, with zero measured
penetration at 0.05 mm tolerance and no allowed-contact exclusions. Thirteen
support tests pass on actual game surfaces. The isolation report records three
projection groups and eight stationary AO shadows. This uses the merged kit
features, not a manual bake fallback. No continuous-sweep guarantee is claimed.


## Phase 2 combined-kit regression and wear calibration

Clean baseline `make` / `make check` passed: 1,264 triangles, one material,
1,300,792 bytes. Opened committed/new hero and full Cycles/Eevee contact:
construction, framing, open Door/raised Flag and hardware agree. The new-looking
finish is inherited, not an integration regression.

First wear checkpoint: opened `renders/wear-pass1-{source,glb}/used_black_post-pair.jpg`.
Rejected the exaggerated white roof stripe and the yellow-green curtain across
the lower shell. The reference has sparse chips and rubbed folds, not wholesale
crown paint failure or a moss-covered wall. Removed the non-edge crown band,
narrowed lower fold chips and reduced their coverage. Confined seam dirt to a
small lower zone in darker neutral dirt. The kit's weathered pine replaces the
fresh wood, but appeared too pale in the pair: added an age-dependent cooler,
darker tone through OUT_base while preserving grain, checks, knots and causal
ground splash from `materials.weathered_wood()`. Correct grain and grade frames
are separate for the horizontal arm. No geometry or texture-set change.
First export/check passed (2,591,284 bytes); acceptance waits on the correction.

Opened the first full-frame hero and six-side/detail contact as well: the roof
stripe is unmistakably wrong from above, and the post foot is still too clean.
The pine replacement needs more caused dirt near grade, even after darkening
the wood palette. A further local adjustment amplifies the kit
`OUT_splash` mask only on the vertical post and mixes a dark damp-earth tone.
It retains the kit's irregular grade-driven shape; no uniform whole-post grime
or circular stain is introduced. Review the lower post in the final hero.

Second source pair: the crown stripe and moss curtain are gone, and the pine
now reads silver-gray. Noticed vertical dirt streaks on the red flag: the lower
shell-height mask had been evaluated in the flag's hinge-local coordinates.
Removed that deposit layer from the red signal finish and gave the Door paint
its actual rest-height offset, so lower-fold deposits remain attached to the
correct manufactured region. The third bake includes this coordinate correction
and the already identified stronger road-splashed post foot.

Third checkpoint: opened both refreshed source/exported used-photo pairs and
all eight hero/orthographic/detail/open-pose probes in `renders/wear-pass3-*`.
Accepted the sparse fold wear, clear crown, unstriped red flag, silver-gray
pine and irregular dark splash at the grade contact. The foot now reads at
full hero size; broad post faces retain gray wood instead of a uniform dirt
wash. Fine checks/fibers soften in the atlas, and the photographed post has
more knots; these are explicit close-view limits. `make export check` passed:
1,264 triangles / one material / 2,082,780 bytes, with three 1024 maps
BaseColor / Normal / ORM 645,381 / 638,621 / 703,649 bytes. Source/imported motion
and actual-surface support checks pass. Final docs follow this acceptance.
