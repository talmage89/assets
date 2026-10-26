# Residential galvanized chain-link sublibrary

Part of [the fence family](../README.md). `make` rebuilds the original model,
frame bake, reused analytic mesh tile, GLB, imported studio/corner runs and
physical checks. Shared references and critique are in the parent folder.

48 in / 1.2192 m fabric starts 2 in / 50.8 mm above grade. Bays use 10 ft /
3.048 m post-center pitch. Actual tube ODs: 1-5/8 in / 41.275 mm line posts,
2-3/8 in / 60.325 mm terminals, 1-3/8 in / 34.925 mm top rail and gate frame.
Rail axis Z 1.25 m; line tube top 1.20 m, terminal tube top 1.27 m, cap top
1.303 m. Tube/cast-fitting gauges are authored construction estimates.

11 gauge / 3.048 mm nominal wire and 2 in clear mesh. The tile locks four
repeat widths into 304.8 mm, giving **50.8335 mm perpendicular clear opening**,
only 0.0335 mm above nominal. This avoids a phase jump when repeating 10 ft
bays. Diamond width is not the clear mesh dimension. Rounded knuckled top and
bottom strips replace cut/twisted tips on this residential fence. The small
weave displacement and tangent normals are generated analytically; no photo
pixels are used. Source precision is retained by tiling, not unique section UVs.

One 1024² BaseColor RGBA / OpenGL +Y Normal / ORM set, approximately **4 MiB**
BC7/BC5 with mipmaps. Unique galvanized frame islands occupy the upper atlas;
all mesh cards reuse a 256² field plus a 256×32 selvage region, about 840 px/m.
Cards are cut into repeat-sized quads so UVs stay inside those regions without
an engine-specific shader. One opaque material and one double-sided glTF MASK
material share the same three images; alpha cutoff 0.5. Expect alpha aliasing
on distant subpixel wire; engines should preserve alpha coverage in mipmaps.

| Module | Role | Post-center sockets |
| --- | --- | --- |
| `Chain_Start` | Terminal on left, line on right | `__L` X −1.524, `__R` X +1.524 m |
| `Chain_EndSection` | Line on left, terminal on right | Same |
| `Chain_Section` | Line at both ends; continuous intermediate run | Same |
| `Chain_BetweenTerminals` | Terminal at both ends; short runs, corner to gate | Same |
| `Chain_Terminal` | End post with fittings facing +X, fabric −Y | `__connect_0` at grade origin |
| `Chain_Terminal_End` | End post facing −X, fabric still −Y | `__connect_180` at grade origin |
| `Chain_Line` | Eye cap and four tie wires | `__connect_0` / `__connect_180` at origin |
| `Chain_Corner` | Two separate rail ends, bars and band sets | `__connect_180` / `__connect_90` at origin |

Each bay origin is the midpoint between post centers at grade; each post origin
is its center at grade. Use the appropriate termination variant: fabric ends at
terminal bars 45 mm inward of terminal centers; intermediate fabric ends at line
centers. Rail socket empties also mark the centerline at Z 1.25 m. Replace the
root inspection transform when placing a module. Front Blender −Y, up +Z;
glTF coordinates `(x,z,-y)`. Post fittings remain on the correct fabric side.

The `Chain_GateBay` prefab includes three independently reusable pieces:
`Chain_GatePost_Hinge`, `Chain_GatePost_Latch` and `Chain_Gate` with its fork
latch child. Their combined prefab cost is explicitly greater than 2k, but each
post and gate is below the 2k modular-piece budget. Bay L/R sockets are X
±.5349875 m; the two post origins sit there. Use them as adjacent panel endpoints
and omit duplicate standalone posts. Gate leaf outer width 914.4 mm, clear
opening 1009.65 mm (3-3/4 in total allowance), 47.625 mm gaps each side.

`Chain_Gate` pivots at bay-local (−.479425,−.043,0), local Z −110°…0°.
Hollow sleeves clear fixed pins; bent necks join the gate clamps. `Chain_ForkLatch`
pivots about local Y −95°…0°, at closed bay-local (.4672,0,.72); its two open
jaws straddle the latch post and lift before the gate swings. Both axes are
measured against actual pins. The gate has a closed rounded welded tube frame,
tension bars and ties; it needs no wooden-style compression brace.

The assembly proof imports the baked library, makes a 90° corner, joins a short
terminal-to-terminal transverse run, and places a gate at the long run's end.
All socket coincidences are measured. Unique UV overlap tests exclude only the
explicitly declared repeated card regions; card bounds/density, normals and MASK
policy are independently checked. Frame support checks use actual evaluated
triangles. Fabric tie checks use the card's support envelope, not a claim of
continuous 3D wire contact or a collision mesh for every diamond.

On slopes, keep posts plumb and regenerate rail endpoints, eye/cup angles,
fabric cuts/phase and tension-wire heights from grade. Do not rotate an entire
10 ft section or stretch diamonds. At sharp grade changes use terminal posts;
keep the gate bay level. Footings, full below-grade posts, engine LODs and
collision meshes are intentionally omitted.
