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
