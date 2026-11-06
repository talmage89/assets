# Main Street shared textures

The 28 buildings use stock glTF with shared external images. There is no
per-building atlas, custom runtime shader, or embedded copy of each map.
Six material states cover the family. The mineral and roof faces share one
state; storefront glass uses uniform IOR/transmission and allocates no image.

| Allocation | Ship maps | Purpose | GPU MiB |
| --- | --- | --- | ---: |
| DowntownMasonry | 2048² BaseColor / Normal / ORM | Common-bond red, running-bond red, painted brick and buff common-bond guarded regions | 16 |
| DowntownMineralRoof | 1024² BaseColor / Normal / ORM | Tooled limestone, terra cotta, mineral roof and poured mineral regions | 4 |
| DowntownFinish | 2048² BaseColor / Normal / ORM | Painted wood, painted iron, aluminum, bronze, woven canvas, cornice paint, pressed relief/acanthus, blind slats | 16 |
| DowntownSigns | 2048² RGBA BaseColor | Original tenant signs, date/name stones, weathered ghost paint | 5.333 |
| DowntownInterior | 1024² RGBA BaseColor | Drawn room/shelf backing plus black and warm fixture regions | 1.333 |
| Glass | No new image | 4 mm panes, transmission 1, IOR 1.50, roughness .014 | 0 |
| **All four towns** | **11 canonical images** | **Six states** | **42.667** |

These are allocations assuming BC7 color/ORM, BC5 normal, 8 bpp per image
and complete mip chains. PNG bytes do not establish GPU allocation. RGBA8
uploads with complete mip chains would cost 170.667 MiB. Importers must cache
canonical image URIs; the stock Blender re-import check measures actual shared
image datablocks across all 28 buildings and a repeated import.

## Reuse decision

Before authoring masonry, inspected `houses/src/textures.py`'s HouseVeneer,
`ranch_fields.py`'s brick fields, and the Cape/split brick replacements. They
supply running bond only. None supplies the header course every sixth course
needed for common bond, or a neutral painted-brick region in that same shared
set. Tinting their red tile would also tint mortar and could not make the
painted variant. Downtown therefore authors one new masonry allocation;
it does not duplicate a house tile under another filename. House, Ground and
other accepted delivery images are unchanged. Downtown presentation uses
existing original family generators for its cars, trees, houses and lights.

## Physical fields and charts

`src/textures.py` authors 4096² BaseColor/ORM and signed meter height fields.
The kit's GPU Cycles flat baker evaluates tangent normals and lighting-independent
BaseColor/ORM. One sample per source texel avoids nondeterministic GPU
accumulation in these lighting-independent data bakes. Two independent 4096 bakes and delivery filters
are compared byte for byte, including every shared PNG; the check does not reuse
cached maps or accept a pixel tolerance. The kit's channel-correct filter produces
the ship sizes:
linear-light color, renormalized OpenGL +Y normals, RMS roughness and linear
AO/metallic. No photo is read by the generator or baker.

Masonry's physical repeat is 4.8768 m wide. Each guarded region holds eighteen
67.733 mm courses of 203.2 mm modules. Common bond includes a header course
every six courses. The painted region retains joints/relief under paint;
the red/buff regions retain neutral mortar and their own kiln colors. Faces
are split at V repeat boundaries, so triangles cannot interpolate through an
unrelated region. Repeated U and reused trim charts are intentional.

The charts reserve 8 delivered pixels above/below each masonry/finish region
and 4 on the smaller mineral map. Roof and mineral share four regions;
finish has eight. Geometry carries sill washes/drips, hood keys/ears/consoles,
scroll-bracket silhouettes, sheet profiles, corbel courses and raised frieze
borders. Tooling, grain, canvas weave/stitching, paint microstructure and fine
pressed relief stay in normals. Independent raw-accessor checks measure chart
areas, positive UV area, region guards and masonry course scaling. These are
repeated tile/trim charts, not a unique per-building nonoverlapping unwrap.

`COLOR_0` carries rest-position weather and finish colors through ordinary
glTF. Unpainted brick is not globally recolored with a vertex palette: its
mortar stays neutral. Splash, sill runoff, scupper damp, repointing repairs,
threshold contact and folded-paint loss use their physical causes. Fine paint
loss follows folded edges in finish strips. `--wear 0` disables the broad
rest-position weather for controls; default is the maintained century-old
building. Ghost-paint alpha loses its field along bed/head joints and through
irregular erosion, exposing the masonry rather than an opaque sign panel.

## Rooms and night

The same interior image drives day color through UV0 and emission through
`LightUV`. The second chart chooses black for unlit cells and a warm fixture
region for selected rooms. Actual shop fixture geometry uses the light region
for its diffuser. All images are shared; there is no second night atlas.
Presentation adjusts emission and adds room lights and lights at the imported
street lamps' actual emitter sockets. Those presentation lights and the town
context never enter a delivered building.

Disk bytes, image-normal checks, actual URI reuse and measured chart-density
percentiles are recorded in `build/texture-check.json`, `build/resource-check.json`
and `build/chart-check.json` after `make check`.

The final form pass keeps these eleven allocations. Modillion acanthus occupies
the right half of the existing pressed-relief strip; frieze rosettes retain
the left portion. Original maker plates reuse a narrow vacant sign-sheet band.
The ghost's field paint is mostly transparent, with surviving letters losing
more paint at coursing and downward water runs. Flush parging/tar remnants
use eroded alpha in another vacant sign-sheet band; filled joist pockets
and protected brick tint record the former neighbor's construction.
Dry concrete uses slab variation and edge deposits, gum and local stains;
asphalt has differently aged repair patches and routed joint sealant. These
use the existing mineral/roof state and vertex colors, adding no allocation.
