# Shared commercial maps — exported surface checkpoint

The strip center's form build uses quick scalar materials and one original
2048² RGBA sign sheet, **5⅓ MiB** with 8-bpp block compression/full mips.
It holds all tenant/center names, window notices, addresses and parking text;
tenants change through UV selection without geometry or per-seed maps. Stock
Boxwood reuses its existing **16 MiB** triple. No strip surface bake is done.

For the later look, the strip shares the sets below, adding only that sign
sheet: **45 MiB new commercial family allocation** including the gas brands,
or **109 MiB** with the existing ground/lawn/shrubs. Mansard variants also
reuse HouseShingles, the houses' unchanged **16 MiB** triple. That is an
existing allocation, not a new commercial texture. The simple visible room
furnishings need no interior sheet. These are plans, not final strip delivery
or draw-call acceptance; see [STRIP.md](STRIP.md).

Manufacture fields are generated at 4096, GPU Cycles flat-baked at 4096 and
filtered to the sizes below, following houses' shared external-image delivery.
Original typography/marks are rasterized at 4096 and filtered in premultiplied
linear color to 1024. Repeat UV overlap is deliberate on building tiles;
trim/equipment faces stay within guarded finish cells. The photo comparisons
load the actual exported glTF and its unchanged shipped maps.

| Set | Ship maps / size | Physical use and reason | BC7 / BC5 + full mips |
| --- | --- | --- | ---: |
| CommercialCMU | Color / Normal / ORM, 1024² | 2.4384 m repeat, 8 × 16 in construction; normal strength distinguishes smooth/split faces. Broad store and future tenant/end walls need repeat density. | 4 MiB |
| CommercialBrick | Color / Normal / ORM, 512² | 1.2192 m repeat; neutral mortar and per-unit kiln tones, shared by station and strip mall. | 1 MiB |
| CommercialEIFS | Color / Normal, 512² | Fine aggregate finish; scalar .88 roughness / 0 metal avoids a redundant ORM. | ⅔ MiB |
| CommercialRoof | Color / Normal, 512² | Large low-detail membrane behind parapets; scalar .93 roughness / 0 metal. | ⅔ MiB |
| CommercialTrim | Color / Normal / ORM, 2048² | Storefront extrusions, coping/hem, painted/bare metal, RTU louvers, soffit folds, door hardware and service gear. One sheet serves both building types and their fixtures. | 16 MiB |
| CommercialEquipment | Color / Normal / ORM, 2048² | One shared dispenser/prop atlas: close card reader, nozzles, cabinet seams, air machine, ice cabinet, cage, refuse and guards. Shared repeated pumps justify 2K; no per-pump sets. | 16 MiB |
| CommercialGraphics | RGBA BaseColor, 1024² | Both fictional brands, 0–9 digits, grade labels, posters and safety graphics. Guarded equal-size cells let brands and prices swap through UV selection. Glass/emission use scalar state and the same pixels. | 1⅓ MiB |
| **New commercial allocation** | **17 images** | Reused once across all seeds and the later strip mall. | **39⅔ MiB** |
| Ground asphalt + concrete | Existing two 2048² triples | Canonical ground-family original fields; 6.096 / 3.048 m repeats. No new commercial paving maps. | **32 MiB already allocated when ground is loaded** |
| **Whole commercial family with required paving** | **23 unique images** | Includes all wall variants; a CMU-only station need not load brick/EIFS. | **71⅔ MiB** |

These are allocation estimates, assuming 8-bpp BC7 color/ORM and BC5 normals,
with complete mip chains. A 2048 triple is 16 MiB, a 1024 triple 4 MiB, a 512
triple 1 MiB; a single 1024 RGBA image is 1⅓ MiB. PNG sizes are unrelated.
Canonical ground URIs or an importer texture-ID cache must be retained so the
road and station do not upload identical paving images twice. A standalone
commercial package still needs those two triples once. Loading the entire
64 MiB ground family plus commercial adds only 39⅔ MiB: 103⅔ MiB combined.

There is one canonical directory of **17 new images**, without per-seed maps.
Stock external glTFs reference these files and the ground/shrub families'
canonical image URIs. Their unchanged PNG bytes and same-scene image identities
are independently checked. PNG sizes and Blender's decoded image bytes are
not claimed to be actual compressed engine upload measurements.

The 2048 equipment sheet contains 32 guarded cells: painted steel, dark molded
plastic, stainless, rubber, bark chips, four accumulated oil footprints, linear
tire/joint contact, gum, runoff/salts, corrosion/scuffs and six original product
fronts. Alpha is coverage only in the wear material; opaque equipment keeps
ordinary PBR. Eight trim strips carry white enamel, aluminum, anodized finish,
soffit, galvanizing, painted brand fields and louvers. EIFS/roof use scalar
.88/.93 roughness and zero metal without redundant ORM maps.

Both brands' wordmarks and marks use equal geometry and select guarded ink
cells through UVs. Ink colors live in the image: standard glTF emission cannot
multiply vertex tint. Price LEDs use uniform amber emission; canopy, wall-pack,
lot and interior lamps reuse the equipment images. Scalar glass adds no image.
Day renders turn exterior luminaires off, retain interior/LED lighting and
reduce logo-panel emission to .10; dusk uses exported authored strengths.
These are documented operational states of the delivered materials.

Wear comes from parked/fueling engine drips, swept driveway tire paths, a
repaired service trench and sealed cracks, retained joint deposits, door/base
gum/grime, impact scuffs and exposed-steel rust, coping/fascia runoff, low
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
