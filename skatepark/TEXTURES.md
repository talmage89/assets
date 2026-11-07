# Shared manufactured finishes

The final external-image delivery uses placement-owned contact wear and gray
municipal bowls. Fixed-camera corrections are in `renders/gate-fixes/`;
native exported-scene critiques and the repeat proof are recorded in
`REVIEW.md` and `build/repeat-check.json`.

All pixels are original scripted fields, Cycles flat-baked at 4096 and filtered
in linear color, coverage alpha, vector normal and RMS roughness space.
Photographs supply measurements and criticism only. No source image enters
a shader. The existing Ground, tree and fence maps remain byte-identical.

| Shared set | Shipped maps | Full-mip block-compressed memory | Use |
| --- | --- | ---: | --- |
| Ground Concrete | 2048² BaseColor / OpenGL +Y Normal / ORM | 16 MiB reused | Poured slab edges and mow strips. |
| Ground Asphalt | 2048² triple | 16 MiB reused | Prefab pad and parking; local darker wearing-course tint. |
| Ground Lawn | 2048² triple | 16 MiB reused | Site turf. |
| SkateTrim | 2048² RGBA BaseColor / Normal / ORM | 16 MiB new | Three steel ages, pool coping, tile, vertical formed-wall stains, phenolic composite, plates, wax, contact marks, cracks, grit, fictional tags and signs. |
| Prefab, historical filename | 1024² triple | 4 MiB new | Now the shared concrete manufacture tile. Troweled rides suppress its bristle normal and reduce roughness; broom walks retain more relief and roughness. |
| Red Maple / Pin Oak | Two 2048² triples | 32 MiB reused | Canonical alpha-cut foliage, bark and `_WIND`. |
| Chain-link | 1024² triple | 4 MiB reused | Canonical woven-wire atlas; six-foot geometry retains native wire pitch. |

**20 MiB new + 48 MiB Ground + 36 MiB trees/fence = 104 MiB per complete
park.** These estimates assume three 8bpp maps and full mip chains, not PNG
or geometry-buffer bytes. The two new triples are shared across all seeds
and modules. Relative external image URIs point directly at the canonical
`skatepark/`, `ground/`, `trees/` and `fences/` files. Embedded GLBs are build
artifacts under `build/embedded/`; the glTF/BIN packages contain geometry.

Concrete uses a 1.524m manufacture repeat, independent pour-batch tints and
local use history. The flat source bake's 3.048m coverage and .004m height
range become a .002m physical range at that repeat; riding/walk normal factors
reduce it further. Vertical retaining faces use their own trim chart, so a
square noise field does not stretch into horizontal waves. Their metric second
UV set reuses Ground's concrete normal at 1.524m independently of that color
chart. A bowl shares one pour batch across its reusable sectors. Both shipped
bowls are municipal concrete, using the deck's gray manufacture set. `pool` selects block coping
and a tile band; it does not imply warm backyard-pool plaster. No shipped
seed has plaster. Memorial is a coping/tile comparator only.

Sawn joints have real recessed backing and dark dirt/sealant tint. Urethane
contacts have nominal 45–70mm soft envelopes with approximately 20–30mm dark
cores at transition lips/toes. Four soft-edged smears share the existing atlas.
Paths vary by seed and placed piece, project onto actual game triangles,
and merge into that piece before export. Reusable sectors and vertical
retaining charts contain no wheel marks. Ledge-face contact is confined to
22mm-high truck scrapes just below its armored edge. Long pocket routes carry
faint polish, with sparse rubber slides below actual placed Approach sockets.
Riding routes are smoother, ledge wax darker/glossier, and steel crowns ground
bare. Grit follows the floor's fall toward its drain, with leaves on the low
flat and toe; no warm wall-to-floor fade supplies the dirt. Toe plates retain
steel reflectance with bright scuffs and oxidation at their edges. Paint chips belong at corners. Composite
lanes fade lighter, with separate black wheel contacts. Fresh joint repairs
contrast with the older park. Rasterized hand strokes have variable pressure,
overspray, drips and a buff patch; no font makes the tags.

Terrain/trim UV reuse is intentional. Audits report actual density, reject
collapsed charts and escaped atlas sampling, measure unit normal/tangent
frames, and independently clip bowl triangles to reject unintended overlaps.
They do not call repeated UVs a successful unique-atlas overlap test. Physical
fixture-base, support and section probes are separate from serialization.
`make repeat` checks deterministic procedural fields and external geometry
byte for byte, including rebuilt context GLBs and source measurements; its
independent GPU rebake uses the kit's maximum 2/255 channel delta and 0.02
byte-domain RMSE per map. Coverage alpha remains exact.

Opaque trim, transparent contact/tag layers and wax share three image payloads.
Wax changes roughness and metallic factors without another ORM. Native fixture
context retains some constant-color materials. Neighborhood houses/roads are
presentation context and do not ship in the park packages. See `REVIEW.md`
for full-size critiques and the appearance gate; a passing numerical check
alone does not certify the finish.
