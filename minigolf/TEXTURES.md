# Look-dev texture allocation

The course atlas is authored entirely by `src/textures.py` at **4096²**.
`kit/flat_bake.py` evaluates a physical tangent normal in GPU Cycles and
validates color/ORM projection with emission bakes. `src/finish_bake.py` checks
those bakes against the original fields, then retains exact authored color/ORM
pixels and float64 symmetric height derivatives for deterministic delivery.
GPU resampling showed occasional one-code rounding differences. The retained
GPU normal checks polarity and the eight-metre / .018 m physical footprint;
sampling kernels differ (mean angular difference 2.79°, 95th percentile 9.91°).
The kit's linear-color,
normalized-vector and roughness-RMS downsampler produces **2048²** maps.
The bake receipt retains GPU mean error/bias and authoritative-field hashes;
`channels` describes GPU validation, `delivery_maps` the actual source maps.
No photograph enters a shader, height field or bake; this is an original
field-material pipeline, not a claimed high-poly color-projection bake.

| Shared set | Maps / shipped size | Compressed GPU with full mips | Purpose |
| --- | --- | ---: | --- |
| Minigolf | 2048² BaseColor, +Y Normal, ORM | 16 MiB | Three carpet hues, loop nap, glue seam and patch; cast stone, painted masonry and fixture paint; cup metal, rubber, soil, canvas stripes, separate pond-ripple/falling-water and glazing regions |
| Original graphics | 1024² RGB BaseColor | 1⅓ MiB | Number/par, two whole fictional pylon faces, price/menu boards, 18-column scorecards |
| Ground Concrete | Existing 2048² triple | 16 MiB | Slabs, walks, concrete curb and clubhouse foundation |
| Ground Asphalt | Existing 2048² triple | 16 MiB | Parking court and adjoining street |
| Ground Lawn | Existing 2048² triple | 16 MiB | Maintained outer grade and planted subbases |
| WoodPrivacy | Existing fence 2048² triple | 16 MiB | Weathered structural lumber, perimeter fence and human bridge |
| Shrubs (presentation instances) | Existing 2048² triple | 16 MiB | Native boxwood and hydrangea share one atlas |

**New: 17⅓ MiB. Delivered course image sets: 81⅓ MiB. With shrubs:
97⅓ MiB. Full assembled review setting: 192 MiB / 39 unique images.**
That final figure adds Ground trim (16), both car sets (32), maple/oak (32),
street lights (4), and strip/station graphics (10⅔ MiB). Houses and utility
construction use source scalar finishes at background distance.
`export/Minigolf-*-context.json` records decoded-pixel image identities, actual
instance placements and this estimate. It assumes an engine shares identical
images, at 8 bpp block compression with full mip chains. The sets are shared external PNG identities in the two glTFs.
The embedded GLBs are self-contained review equivalents; loading both GLBs
without a content/atlas cache may duplicate allocations. Disk PNG and GLB
bytes are reported separately from block-compressed GPU estimates.

Ten material states: opaque course, graphics, lit pylon graphics, water, glazing, emissive lamp,
Ground Concrete/Asphalt/Lawn and lumber. Water, glazing and lamp reuse the
course's three images. Clear glazing uses a near-neutral scalar base color
with the existing normal and .025 roughness atlas region; its real 3/6 mm shell thickness controls
refraction rather than a dark absorbing color. Falling water has 1.5 mm
closed films for an actual exit interface and .035 roughness; pond roughness
is .17 with its separate colored-depth region. Wet stone occupies a separate
region of the same atlas, selected only near the actual flow and waterline. This is the justified large-site palette, rather than
a different texture set per hole. Pivots retain independent geometry.

`src/look.py` authors the UV rectangles and eight-texel delivery guards. The
carpet uses a full lane chart; trims and constructed parts reuse declared
rectangles; Ground keeps metre-based tiled UVs, while lumber uses protected
interior board/end-grain charts in its existing unique atlas. Mulch skins are
split at a two-metre repeat so bark chips retain their size across the bed.
Continuous coping and rock skins use that physical repeat as well; source
fields are periodic across the protected interiors. Twelve independent
BaseColor/ORM/Height boundary checks stay within one code value. Intentional
tile reuse is audited separately from escaped charts; this is not a unique
atlas with a claimed zero-overlap UV layout. The raw delivered UV density
percentiles and normal lengths are in `build/look-check.json`.

Traffic masks follow tee-to-cup centerlines and concentrate around the cup
and tee. They lighten/desaturate polypropylene; the original normal field
flattens its nap along the traffic line. Seams and repair edges are authored
into the roll. Paint failure is confined to panel boundaries with a previous
coat exposed; the original south-face exposure mask is stronger on the older
classic course. Wet rock darkening/algae follow the waterfall and waterline;
fallen leaves cluster in sheltered water, and lost balls sit on the liner.
All remain subject to full-frame imported-GLB critique in `REVIEW.md`.
Individual 5.2 mm carpet tufts are below this lane chart's delivered sampling
limit. Its effective micro-relief is reduced before baking so filtering does
not turn them into false centimetre-scale lumps; close-up fibers remain soft.

Town, cars, trees and street lights are presentation resources with their own
existing shared sets. Context construction is generated into this family's
ignored build directory when no canonical delivery is present. No existing
family delivery, texture or docs image is rewritten.

Normals derive from original procedural height fields. The 4096 source-field
comparisons use identical imported geometry and expose filtering loss; they do
not claim a high-poly-to-low-poly surface-projection bake.
