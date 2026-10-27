# Foundation shrubs

Original scripted summer foundation shrubs, built on the shared botanical
kit. **Current stage: boxwood source look-dev checkpoint.** Hydrangea has been
researched but is held until the checkpoint review. No final GLB, baked stem
atlas, delivery verification or final docs JPGs are claimed yet.

The sheared hybrid boxwood has a soft mound about 0.9 m tall × 1.0 m across,
15–25 mm opposite entire leaves, a dense pruning shell, uneven new shoots and
thinner old foliage on its low +Y shaded side. Seven basal leaders share a
rooted woody core. Blender −Y is the front; the origin is at grade.

[Reference evidence](REFERENCE.md) · [Sources and rights](refs/SOURCES.md) ·
[Critique history](REVIEW.md).

The family reserves one 2048² BaseColor-alpha / OpenGL +Y Normal / ORM set for
both species, generated at 4096 and filtered with the kit. Its eight boxwood
tiles occupy the lower half, stems/soil an upper-left strip and future hydrangea
leaves/flower tiles the remaining upper region. Two materials at most. Full-mip
BC7 BaseColor-alpha, BC5 normals and 8-bpp ORM cost **16 MiB total**, shared
across all instances/species; geometry and engine overhead are additional.

Every source vertex carries normalized `Wind` RGBA: R height sway, G hierarchy,
B stable phase, A leaf flutter. Zero sway/flutter at grade. Wind is data, never
an albedo multiplier; final export is planned as `_WIND`, as on the maple.
No armature or moving parts.

```sh
make -C shrubs                    # current look-dev checkpoint only
make -C shrubs check              # source, camera, botanical and repo checks
make -C shrubs preview            # quick Eevee source views
make -C shrubs render match contact PASS=study WIDTH=1100 SAMPLES=32
```

Installed Blender 5.2, Python/NumPy/Pillow, fontconfig and flock are required.
Every Cycles render uses the shared GPU lock. Downloaded photos/PDFs are ignored
and used only for measuring and local comparisons. All geometry and atlas
pixels are original equations/seeded procedural output. No documentation image
is committed before the asset is final.
