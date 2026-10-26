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

Pending final rendered review and independently measured construction results.
