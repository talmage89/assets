# Shared commercial maps

Manufacture fields are original 4096 images, Cycles flat-baked at 4096 and
filtered to the sizes below in linear color, vector-normal and roughness-RMS
space. Typography and marks are original raster art, coverage-filtered from
4096. No photograph supplies pixels. The final judgments import stock glTF
with these exact external maps.

| Set | Shipped maps / size | Use | BC7 / BC5, full mips |
| --- | --- | --- | ---: |
| CommercialCMU | Color / Normal / ORM, 1024² | 2.4384 m repeat; 8 × 16 in units. Smooth and split faces share images with distinct normal strengths. | 4 MiB |
| CommercialBrick | Color / Normal / ORM, 512² | 1.2192 m repeat; neutral mortar and per-unit kiln tones. | 1 MiB |
| CommercialEIFS | Color / Normal, 512² | Fine aggregate; scalar .88 roughness / zero metal. | ⅔ MiB |
| CommercialRoof | Color / Normal, 512² | Gray membrane, scalar .93 roughness / zero metal. | ⅔ MiB |
| CommercialConcrete | Color / Normal / ORM, 1024² | 1.524 m repeat; sand, pores, irregular broom bristles. Pour tone and absorbed standing bands use vertex color. | 4 MiB |
| CommercialEquipment | Color / Normal / ORM, 2048² | Shared equipment and trim: steel, stainless, soffit, coping, extrusions, hardware, guards, shredded bark and product fronts. | 16 MiB |
| CommercialGraphics | RGBA Color / RGB Emission, 1024² | Both original brands, prices, labels, wear and powered diffusers/panels. | 2⅔ MiB |
| **New commercial family** | **18 images** | All seeds and wall alternatives, shared once. | **29 MiB** |
| Ground Asphalt / Lawn | Existing 2048² triples | Canonical external URIs and byte-identical PNGs. Station traffic and repeated broad-field compensation use vertex color. | **32 MiB reused** |
| Shrubs Boxwood | Existing 2048² triple | Bark and leaf meshes joined locally under the existing mask material. Original stock vertices and pixels retained. | **16 MiB reused** |
| **All family alternatives, landscaped** | **27 unique images** | A default CMU station omits unused brick/EIFS. | **77 MiB** |

A default station's actual allocation is 75⅓ MiB. A neighborhood already
loading ground and shrubs adds only the commercial 29 MiB. Estimates assume
8-bpp block compression and full mip chains; PNG bytes and Blender decoded
images are different quantities. Geometry and map bytes are in README and
`build/delivery.json`. The original 39⅔ MiB plan is reduced by consolidating
trim into equipment, even after adding dedicated concrete and emission.

One canonical `export/textures/` directory serves all four external glTFs.
Ground and shrub images retain their family's relative URIs, so a scene can
cache each image once. Fresh import of all four stations plus a repeat proves
Blender image identity reuse. No stock house, ground or shrub source/export
is modified. Their original low-frequency asphalt repeat is reported to the
lead; station/presentation copy compensation leaves the library set intact.

## Materials and UVs

Each station has nine materials (ten for smooth/split CMU seed 103): equipment,
graphics, glass, the selected masonry, concrete, roof, asphalt, lawn and shrubs.
The additional smooth-CMU material shares every image but changes normal
strength. Dedicated tile scales and roughness responses justify the building
materials; repeated hardware, trim and equipment share the same guarded atlas.
Exact per-part materials and glTF primitive counts are in README and
`build/delivery-check.json`.

Equipment has 32 guarded finish cells. Geometry assigns its manufactured
finish before consolidation, with original six product fronts and fine
cast-metal grain. Shredded bark uses sparse raised pieces over overlapping tapered fibers with irregular
length, width, direction and raised ridges; it has no paver grid.

Graphics combines opaque ink, alpha wear and all emission. UV0 selects
color/coverage, UV1 selects powered pixels or a zero-emission swatch. This
avoids separate materials for each lamp color, transparent stain or brand.
The 16-bit emission map encodes normalized radiance with a shared scalar
strength; no vertex emission tint is required. Glass is one scalar material.
Native exported emission stays active in both day and blue-hour views.

Repeating tile UV overlap is intentional. Guarded equipment and graphics
charts avoid neighbor bleed. Raw glTF checks measure every actual triangle's
UV area/density and unit normal, and reject zero-area charts. No claim of
unique-island overlap is made for these deliberately shared materials.

## Weather from service

Station asphalt compensates the ground map's broad periodic field while
retaining its aggregate. Drive lanes darken/polish at actual tire paths;
weathered edges, engine centers, a service trench and sealed cracks explain
large changes. Concrete has independent pours, joint sealant and narrow joint
dirt. Absorbed gray-brown oil combines many overlapping drips and a standing
band, with swept tire contacts through it. At the doors/pump bases are gum,
working grime and scuffs. Curved paint loss at bumper height and the wet base
ring controls bollard rust. Yellow remains yellow. Coping/fascia runoff begins
at real joints and excludes scupper openings; low masonry retains salts and
dirt. Sun-facing paint fades. Broad effects use stock glTF vertex colors,
small deposits use guarded alpha swatches; there is no whole-surface noise
wash, random wall peeling or arbitrary dark blotch.

The hero revision generates oil, tire and runoff coverage directly into the
existing graphics sheet, without rebaking manufactured finishes or changing
powered pixels. Round absorbed drops account for the physical 3.0 × 9.0 m
fueling footprint; wheel contacts continue through the operating lanes and
traffic around the pad. Fixed sunlit-floor masks compare coverage and contrast
against both used-paving photographs (`src/hero_review.py`). These are
projected appearance measurements, with annotated exclusions and disclosed
thresholds, rather than surveyed stain areas or recovered albedos.
mpact scuffs and exposed-steel rust, coping/fascia runoff, low
masonry salts, and south-facing paint fading. Broad low-frequency age uses
stock COLOR_0; manufacture stays in the maps. No whole-station unique atlas,
uniform noise wash or scattered wall peeling is introduced.

Maintained beds instance **Boxwood** from `shrubs/export/Shrubs.glb`: two shared
meshes, three existing 2048 maps (**16 MiB**, reused once). Public planting and
neighboring presentation lawns also reuse Ground's existing lawn triple
(**16 MiB**). These are existing stock families, not new commercial sets.
A standalone fully landscaped station references 39⅔ + 48 ground + 16 shrubs
= **103⅔ MiB** across all wall alternatives. A neighborhood already loading
ground and shrubs still adds only **39⅔ MiB** for commercial. Neighboring
houses/trees used only for presentation are excluded from the station export.


## Strip-center look checkpoint

Strip manufacture uses the gas delivery's unchanged CMU, brick, EIFS, roof,
concrete and equipment maps. It also reuses Ground asphalt/lawn, Boxwood
and (for seed 202) HouseShingles without changing their pixels. Furniture
uses equipment cells; no interior sheet is added.

The only new strip allocation is **StripSigns: 2048² RGBA color + 1024² RGB
emission, 6⅔ MiB** at 8 bpp with full mips. It replaces the station's
1024² graphics pair rather than loading alongside it. Original tenant
art, window notices, tower faces, address numbers, south-facing faded
variants, removed-letter ghost, lamps and causal deposit charts share it.
UV0 selects ink/coverage and UV1 selects radiance or a zero swatch.
The 16-bit normalized emission file retains low sign output alongside
brighter fixtures under one glTF emissive-strength scalar.

| Allocation | GPU memory, full mips |
| --- | ---: |
| All strip commercial wall alternatives, including StripSigns | 33 MiB |
| Existing Ground asphalt + lawn | 32 MiB |
| Existing Boxwood triple | 16 MiB |
| Family with all wall alternatives, no mansard | 81 MiB |
| Existing HouseShingles triple, only mansard | +16 MiB |
| Actual seed 201 / 202 / 203 / 204 referenced maps | 79⅓ / 92⅓ / 76 / 79⅓ MiB |

These are compressed GPU estimates, not PNG or GLB sizes. A neighborhood
already loading commercial manufacture, ground and shrubs adds only
6⅔ MiB for strip art; shared external URIs allow one image cache.
`build/strip-look/delivery.json` records every map and actual part primitive.
The strip has **nine material states**, except the mansard's **ten**: its
existing shingle material is needed alongside the flat roof membrane.
Nine states do not mean nine draw calls: the default hierarchy has 246
material primitives, including 36 placed shrubs and separate moving leaves.
Per-part materials and their construction roles are listed in STRIP.md.
