# Skateboard look-dev checkpoint

This round stops before final docs and a README gallery. `make` rebuilds the
three states, UVs, 4096 bakes, 2048 delivery maps, embedded GLBs, construction
and delivery checks, same-camera form comparisons and Cycles look-dev views.
`make check` repeats the construction, imported-GLB/UV/texture and repository
gates. Blender calls run serially in this worktree; every Cycles bake and render uses
the kit's shared GPU lock.

The comparison baseline is reconstructed locally from the tracked form scripts
at `8cc0710`; that commit must be available in the local Git history. No other
worktree is read or modified. Downloaded references remain measurement and
review inputs only. `src/graphics.py` and `src/lookdev.py` generate every texel.

- `export/{new,season,beat}.glb`: game assemblies, retained wheel/hanger pivots
  and the five accepted sockets.
- `textures/<state>/T_Skateboard_{BaseColor,Normal,ORM}.png`: one 2048 set per
  state. ORM is occlusion/roughness/metallic; normal is OpenGL +Y.
- `build/<state>/{model,high,finalized}.blend`: measured game form, dense finish
  source and packed game assembly. The finalizer uses a cleaned low scene;
  retained dense sculpts cannot enter the export.
- `renders/form-fixes/`: full-size before/after panels and three rail sections.
- `renders/lookdev/`: each state's hero, underside hero, tail, truck, bearing
  and grip views; contact sheet, matched photographs, values and budgets.
- `renders/lookdev/graphics-sheet.jpg`: Ditchlight orbital contour, Kilnline
  fired-brick/lightning and Static Orchard interrupted growth/radio motifs.

The sheet contains three distinct original graphics selected by seed. Wheel
and truck marks are fictional Kilnline and Crossway. This checkpoint exports
the default Ditchlight board in all three ages. Other seeded deck sizes remain
parametric construction variants, not three additional look-dev approvals.

One resident state costs about 16 MiB for three 2048 8-bpp block-compressed maps
with mip chains. Loading all three age atlases costs about 48 MiB. The three
response classes (common, clear-coated wood/ink, mildly transmitting urethane)
share that atlas; they allocate no additional images. Fine grit, drive recesses,
cast grain, grind scores, wood fibers, markings and axle threads live in the
normal/albedo/ORM bake rather than additional game triangles.

Season wear is concentrated in belly slides, rear-kick abrasion, planted-foot
zones, exposed hanger grind faces and rolling wheel shoulders. Beat adds a
thinned tail, localized rail loss, two lifted maple splinters, a torn nose-grip
patch, heavier wheel staining/coning and a ribbed shoe-goo repair. Bushing flex
remains a visual approximation; the accepted steering axis/range are preserved.

`make repeat` repeats serialization of the accepted finalized scenes/maps and
requires byte-identical GLBs. It does not claim an independent repeated GPU bake.
Numerical checks distinguish source construction from export preservation;
photographic pairs and the critique log judge appearance.
