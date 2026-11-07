# Shared image allocation

Native-size artistic judgment is recorded separately in [REVIEW.md](REVIEW.md).

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
to 2048². Current GPU-normal agreement is mean **2.921°**, p95 **10.751°**;
these different sampling kernels are compared, not claimed identical.
Photographs never enter shaders or bakes.

Ten classic / eleven adventure core material states reuse those images: opaque
course, graphics, lit graphics, water, glazing, lamps, three Ground states,
lumber, and adventure foam. Rock shares the ordinary opaque atlas state.
Falling water and pools share the same transmission state with different UVs.
Foam uses soft per-vertex coverage in its own consolidated RGBA mesh; opaque
pigment retains float RGB values. This adds no image or duplicate texture set.
The raw-export check requires BLEND, a coverage channel, transparent edges and
partly covered interiors. Buff/tan minerals are baked; exposure, damp crevices
and localized moss add continuous vertex modulation.

Carpet uses lane charts and tee-to-cup traffic, sun fade, cup wear, seams and
patches; 5.2 mm individual tufts remain below delivered chart sampling. Rubber
has molded ribs and central abrasion. Classic white borders expose an older
coat at their edges; adventure white surfaces sample the less damaged interior.
The painted blue basin sits under neutral transmissive water, and the two-metre
ripple mapping is stable across the surface strips. Moss/stain follow flow,
waterline and shaded damp feet. Static aeration and impact foam remain an approximation of moving water.

Coping abrasion follows its outer nose and inner splash face. The painted
blue bowl uses a separate world-height tide-film mask tied to the actual
shallow-water datum and stream drops. The packed-color check measures the
strongest surviving tint against the nearest delivered water vertex, without
calling either source mask or water-height function, and verifies that the
deepest floor paint remains clear. The inspected exports place the strongest
sample 17.5 mm above the water and retain floor tint above .99998.

Ground keeps its metre-based repeat. Lumber reuses protected board/end-grain
charts in the unchanged native atlas. Rock, mulch and water are split at their
authored repeats; atlas guards protect sampling. Tile overlap is intentional;
`check_look.py` rejects escaped charts and reports actual density percentiles,
normal/tangent lengths and color ranges. It does not claim a unique atlas with
zero overlap. Twelve source-field boundary checks pass within one code value.

Embedded GLBs are verification products under `build/embedded/`. The external
checker compares indexed corners, transforms and PNG payloads against them;
`export/` contains glTF/BIN and receipts, with no copied image directory.

The native oak has one Mikk tangent component that straddles Blender's
four-decimal rounding boundary. The landscape exporter stabilizes that one
asset-owned corner in both containers. Exact position/normal/UV guards and a
.00011 maximum component difference reject changed geometry or larger errors;
the embedded path uses the kit's existing guard. Native library files remain
untouched. Replay compares the resulting tangent bytes exactly.
