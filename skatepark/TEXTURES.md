# Baked look-dev allocation

The look-dev GLBs use original 4096-pixel Cycles bakes, filtered with the kit's
linear-color, coverage-alpha, vector-normal and roughness-aware filters.
Photographs are comparison evidence only. The accepted Ground image files are
reused unchanged; local vertex color and normal/roughness factors distinguish
riding concrete, walks and asphalt.

| Shared set | Shipped maps | Compressed GPU memory including full mips | Use |
| --- | --- | ---: | --- |
| Ground Concrete, reused | 2048² BaseColor / OpenGL +Y Normal / ORM | 16 MiB | Troweled riding surfaces and original broom response on walks. Saw cuts have recessed, dirty backing. |
| Ground Asphalt, reused | 2048² triple | 16 MiB | Prefab pad and parking, with darker wearing-course vertex color. |
| Ground Lawn, reused | 2048² triple | 16 MiB | Tiled turf; its planar edge silhouette remains a presentation weakness. |
| SkateTrim, new | 2048² RGBA BaseColor / Normal / ORM | 16 MiB | Three steel-age lanes, radial pool blocks, tile/grout, armor, gauge steel, absorbed wax, riding marks, scrapes, cracks, grit, fictional tags and rules. |
| Prefab, new | 1024² triple | 4 MiB | Original composite riding sheets, panel seams and lighter worn lines. Frame/plate surfaces use the trim set. |

**20 MiB new + 48 MiB reused Ground = 68 MiB across the complete family.**
These are 8bpp block-compression estimates with full mip chains, not PNG or
GLB file sizes. Every piece/seed references the same sets. Opaque, cutout and
wax states share the same trim pixels; wax uses a roughness factor and does
not generate another ORM. The raw GLB audit checks the embedded images.

The two delivered tree species add two existing 2048² triples (32 MiB), and
native chain-link adds its existing 1024² triple (4 MiB). A complete poured
site therefore uses about 100 MiB; the prefab site adds 4 MiB, for 104 MiB.
Existing fixture context still has constant-color material states. Town
houses and roads beyond the site are presentation context and do not ship in
the park GLBs. No new tree geometry or tree texture is authored here.

Terrain is intentionally tiled, and trim regions intentionally overlap across
parts. They are not unique whole-object bake charts. The audit measures actual
exported UV area/density, rejects collapsed charts, checks trim bounds and
normal/tangent frames, and independently checks the bowl's plan projection
for folded/overlapping riding triangles. It does not describe intentional
tile/trim reuse as a successful unique-atlas overlap test.

Use history is local: paint is lost at steel contact crowns and oxidized at
its sides; pool noses darken where boards grind; pumping wear follows bowl
chainage, approach wear follows the quarter/bank sections; cracks start at
saw cuts; clipped sediment triangles and leaf litter gather at the drain.
1999 is the hard-worn prefab installation, 2004 the middle-aged concrete park,
and 2011 the newer pool-coping park. See `REVIEW.md` for rejected passes and
`LOOKDEV.md` for the final measurements and remaining weaknesses.
