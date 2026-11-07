# Shared image allocation — correction checkpoint

The visual delivery gate remains rejected; see [REVIEW.md](REVIEW.md).
This document describes current technical bindings, not photographic approval.

| Canonical set | Shipped images | Full-mip memory at 8 bpp |
| --- | --- | ---: |
| Minigolf | 2048² BaseColor, OpenGL +Y Normal, ORM | 16 MiB new |
| Graphics | 1024² BaseColor | 1⅓ MiB new |
| Ground Concrete / Asphalt / Lawn | Three unchanged 2048² triples | 48 MiB reused |
| Fence WoodPrivacy | Unchanged 2048² triple | 16 MiB reused |
| Optional maple / oak / shrubs | Three unchanged 2048² triples | 48 MiB reused |

Construction: **81⅓ MiB / 16 images**. Construction plus native landscape:
**129⅓ MiB / 25 images**, shared across both seeds and the piece library by
canonical relative URI. New allocation remains **17⅓ MiB**. These are
compression/mipmap estimates, not PNG disk size or measured engine residency.
`build/costs.json` enumerates each file and the separate geometry costs.

`src/textures.py` generates original 4096² color, ORM and physical height
fields. GPU Cycles emission/normal bakes validate their channels and polarity;
`finish_bake.py` preserves deterministic authored color/ORM and float64
height-derived tangent normals, retaining the actual GPU maps separately.
The kit filters color in linear light, normals as vectors and roughness by RMS
to 2048². Current GPU-normal agreement is mean **2.972°**, p95 **10.782°**;
these different sampling kernels are compared, not claimed identical.
Photographs never enter shaders or bakes.

Eleven core material states reuse those images: opaque course, rock, graphics,
lit graphics, water, glazing, lamps, three Ground states and lumber. Falling
water and pools share the same transmission state with different atlas UVs.
The rock coat uses continuous vertex-authored mineral pigment, with the
existing baked aggregate/roughness fields; no additional image. Its current
color variation is too weak and its form still reads as smooth clay.

Carpet uses lane charts and tee-to-cup traffic, sun fade, cup wear, seams and
patches; 5.2 mm individual tufts remain below delivered chart sampling. Rubber
has molded ribs and central abrasion. Classic white borders expose an older
coat at their edges; adventure white surfaces sample the less damaged interior.
The painted blue basin sits under neutral transmissive water, and the two-metre
ripple mapping is stable across the surface strips. Moss/stain follow flow,
waterline and shaded damp feet. Foam is still too regular and graphic.

Ground keeps its metre-based repeat. Lumber reuses protected board/end-grain
charts in the unchanged native atlas. Rock, mulch and water are split at their
authored repeats; atlas guards protect sampling. Tile overlap is intentional;
`check_look.py` rejects escaped charts and reports actual density percentiles,
normal/tangent lengths and color ranges. It does not claim a unique atlas with
zero overlap. Twelve source-field boundary checks pass within one code value.

Embedded GLBs are verification products under `build/embedded/`. The external
checker compares indexed corners, transforms and PNG payloads against them;
`export/` contains glTF/BIN and receipts, with no copied image directory.
