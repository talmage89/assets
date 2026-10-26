# Privacy fence image and construction review

Only the privacy system is in this stop point. Reference images remain local;
see refs/SOURCES.md. Observations below distinguish photographed construction,
authored aging, physical measurements and serialization checks.

## Pass 1 — source, Eevee, 1000 px / 16 samples

Opened all six images in `renders/pass1/contact.jpg`: good side, rail side,
grain, post saddle, gate front and gate back. Compared directly with both
Denver construction photos and Classic Fence Co PDF p36 (weathered dog-ear).

- Picket dog-ears, three rails and the gate's lower-hinge-to-upper-latch brace
  direction read correctly. Two source sections need different board rhythms.
- Growth bands are too regular; identical fiber phase makes the boards look
  machined. Knots are too soft and wide in comparison with the sharp dark cores
  and disturbed surrounding fibers visible in the photographs.
- Very pale source light washes away the gray/tan wood. Back views are unusable:
  the seamless backdrop sits between the reverse camera and the product.
- Source audit also caught a latch pivot/frame update error. The corrected game
  assembly measures 2068 triangles before the small latch stand-off addition.
- Solid motion checks caught the latch bar entering the post and strike backing
  during release. Moved the bar in front of the post plane, with a real pivot
  stand-off; no collision exception is used to excuse that interference.

Changes: independently phase each board's fine fibers, reduce broad stripe
contrast, tighten knot cores, introduce more tan/gray variation; rotate the
studio for rear views. Keep silhouette geometry lean and leave the boards'
end checks and fasteners in the bake. The 4096 bake is downsampled to one 2048
atlas; measured initial packing has zero overlaps, 50.2% coverage and 233 px/m
median, with extra density on hardware and the gate.

The daylight cedar photo calibrates joinery/camera, not pine hue. Its inferred
8 ft bay and rail positions have photographic uncertainty: the initial fit RMS
is 5.60 px over a 475×420 crop. Classic Fence p36 supplies a separate direct
weathering comparison; the watermarked PDF is not used as a texture or docs.

## Pass 2 — source and exported GLB

Reviewed the four source Cycles views in `renders/pass2-final/contact.jpg`
and its calibrated rail-side photographic pair, then every exported studio
view in groups covering heroes, turnaround, grain, joinery, hinge hardware,
gate front/back, exploded modules, posts and human scale. Also opened the
assembled corner pair, Eevee view and exported photo-match pair.

- Increasing irregular earlywood erosion and drying checks made the gray/tan
  boards read as aged timber at gameplay distance. The source remains finer
  than the delivered atlas: at 233 px/m, the closest grain and bracket views
  show filtering softness. That is a real delivery limit, not source quality
  presented as a game result. Macro grain is still more regular than the photos.
- Source/end-grain review separated timber axes from height above grade: splash
  now stays near the ground on horizontal rails, and cut faces expose growth
  rings. The two section seeds retain coherent gray/tan hues instead of green
  or pink random board colors.
- Export review exposed a modular projection error: neighboring rail brackets
  had baked metallic marks onto bare post faces. Changed the bake to eight
  isolated module/moving groups and preserved 65 explicit wood coordinate
  frames. The imported ORM now measures **0.0 metallic** at 96 post-body sample
  points. The isolated post render visibly confirms the correction.
- Corrected the cropped post inventory camera. The reverse corner view needed
  a lower aim and a wider seamless: independent vertex projection now frames
  all complete post/assembly geometry; corner rays hit the backdrop in all
  four image corners. View settings are separated from delivery policy.
- The gate's bent straps initially crossed the pin bore; trimmed their necks
  around it. Both high/game released-gate sweeps now pass at 111 poses over
  −110°…0°, and both latch sweeps pass at 34 poses over −65°…0°. No collision
  exceptions are used. Physical hinge-axis error measures zero at stored float
  precision.
- Twenty-eight evaluated triangle-surface support checks per quality pass.
  Maximum sampled contact bound: 0.00013 mm game, 0.00005 mm high. The measured
  clear opening is 914.4001 mm, leaf 888.9999 mm, with 12.7001 mm side gaps;
  brace bearing-plane errors are below 0.00012 mm.
- Actual imported post-center sockets coincide for the straight run and the
  assembly proof. The imported 90° corner check measures zero penetration at
  its 0.3 mm acceptance tolerance. These are construction tests, distinct from
  the kit's independent GLB serialization/texture/UV verification.

The final calibrated rail-side camera is approximately 71.4 mm, with a
5.64 px photographic RMS on the 475×420 crop. Blender's independent projection
agrees within 0.00028 px. The reference is unsurveyed new cedar, so remaining
rail/camera residuals and its warmer hue are not hidden or called an exact
pine material match. Classic Fence p36 remains the direct aging reference.

Final acceptance: preserve the lean geometry and shared texture memory; accept
close-up filtering and some procedural grain regularity at this repeatable
fence's intended viewing distance. No white picket or chain-link work is started.


## Accepted privacy follow-up — knot population only

The lead accepted construction, sockets and lean geometry, and rejected the
repeated soft dark ovals. Changed only the shared pine material: approximately
half of timber draws are clear, remaining branches occur in one or two whorls,
with strongly skewed sizes, tilted axes, a narrow resin ring and occasional axial
check. Continuous grain diversion replaces blending a broad oval into the grain.
UV aging desaturates knots along with their board. All geometry, pivots and
installation choices are unchanged.

Opened `renders/knots-glb/match_rails-pair.jpg`, rendered from the freshly baked
export at the existing calibrated camera, beside the Denver construction photo.
The dots no longer march across every board: Section A has 12 clear pickets and
8 branch cuts on the other five, with radii 2.0–21.0 mm, some clipped by board
edges. The wide variation, quiet branches and local grain deflection read as
wood rather than a spotted decoration. The cedar photo remains warmer and more
knotty than this aged pine; that material/age distinction was already accepted.
Fine resin lines and pin knots soften at the unchanged 233 px/m atlas density.
Source and GLB checks pass with the original 664-triangle section meshes.
Final studio images are regenerated from the revised exported textures; family
docs JPGs are deferred until picket and chain-link are also complete.
