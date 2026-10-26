# Painted cedar picket sublibrary

Part of [the modular fence family](../README.md). Build here with `make`; the
family root `make` includes this delivery. References, critique and final docs
are shared in the parent folder, and docs JPGs are composed once for the batch.

42 in / 1.0668 m French Gothic boards, actual 5/8 × 3.5 in / 15.875 × 88.9 mm,
start 2 in / 50.8 mm above grade. Thirteen boards span each 8 ft / 2.4384 m
post-center bay, with 85.2714 mm interior gaps and equal end gaps. Two actual
38.1 × 88.9 mm rails sit at Z 254 and 889 mm, carried in galvanized saddles.
Posts are actual 88.9 mm square, top 1.16 m; pyramid cap top is 1.205 m.
Paint wear follows edges/cut ends/nails; damp mildew fades upward from grade.

`Picket_A` and `Picket_B` contain panels and brackets; `Picket_End`, `Picket_Line`
and `Picket_Corner` contain one post and cap each. Every module origin is on
the post centerline at grade. Panel `__L`/`__R` sockets are X ±1.2192 m;
post connection sockets are at its origin, yaw 0° for end, 0°/180° for line,
180°/90° for corner. Front is Blender −Y, rail side +Y, up +Z. glTF coordinates
are `(x,z,-y)`. Replace the root's inspection transform on placement.

`Picket_GateBay` includes both posts: use its `__L`/`__R` (X ±.50165 m) as
neighboring panel endpoints and omit duplicate standalone posts. Clear opening
914.4 mm, leaf 889 mm, side gaps 12.7 mm. Five full-width boards, perimeter
frame and compression brace bear from lower hinge toward upper latch.
`Picket_Gate` pivots at local bay (−.45085,−.054,0), local Z −110°…0°.
`Picket_Gate_Latch` lifts about local Y −65°…0°; release before gate swing.
Both physical hinge pins are coaxial with the moving root. Hinges/latch are
separate from fixed post plates, pins and keeper.

One 1024² BaseColor / OpenGL +Y Normal / ORM set, shared by every piece;
4096² Cycles source bake. Approximately 4 MiB with BC7/BC5 plus mipmaps.
No separate set for black gate hardware or galvanized saddles. Module budgets,
actual export sizes and final image links are in the family README.

For slopes, step rigid level bays and regenerate taller posts plus high/low
rail-face sockets. Keep pickets vertical, caps level and the gate opening level;
a raked fence requires rebuilding rail/brace joinery and is not obtained by
rotating or shearing these ready-made panels. Underground posts/footings and
engine collision/LOD meshes are intentionally omitted.
