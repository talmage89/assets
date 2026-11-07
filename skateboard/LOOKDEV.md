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

## Form review

Before/after panels retain 1440 native pixels per view. Both sides use the same
camera, sun and quick palette. The finished hardware panels substitute the
baked GLB on the right, so they also expose normal-map transfer and materials.

| Correction | Local review image |
| --- | --- |
| 80 mm continuous kick transition; minimum authored radius about 164 mm | [Side](renders/form-fixes/side-before-after.jpg) |
| Progressive concave and 5.25 mm rail roundover | [Stance](renders/form-fixes/section_stance-before-after.jpg), [mount station](renders/form-fixes/section_truck-before-after.jpg), [kick](renders/form-fixes/section_kick-before-after.jpg), [rail](renders/form-fixes/tail_plies-before-after.jpg) |
| Smooth end outline and 64-sided wheel silhouette | [Hero](renders/form-fixes/hero-before-after.jpg), [wheel](renders/form-fixes/wheel_bearing-before-after.jpg), [steered](renders/form-fixes/lean_right-before-after.jpg) |
| Drafted triangular web, open annular seat, pocketed plate and machined nut lands | [Baked truck](renders/lookdev/truck-finished-before-after.jpg), [inner side](renders/lookdev/truck_inner-finished-before-after.jpg) |
| Visible bushings, cup washers, shield, race and 24-TPI axle relief | [Bushing stack](renders/lookdev/truck_inner-finished-before-after.jpg), [bearing](renders/lookdev/wheel_bearing-finished-before-after.jpg) |
| Full-size photographic comparison replacing miniature | [Loose truck](renders/lookdev/pairs/period_truck-pair.jpg), [used truck/wheel crop](renders/lookdev/pairs/fullsize-wheel-pair.jpg) |

The deck's actual mesh envelope is 203.092 × 815.867 mm after rounding; the
press nominal is 203.2 × 815.975 mm. Its center gauge including grip measures
11.050 mm, near-rail concave 7.431 mm, and the sampled outer kick slopes
18.569° nose / 18.568° tail. The source construction check measures these from
triangle surfaces; GLB verification separately proves export preservation.
New/season total 13,888 triangles; beat 13,928. The full allocation is in the
[asset README](README.md#counts-and-materials).

## Look review

[Contact sheet](renders/lookdev/contact.jpg), [photographic pairs](renders/lookdev/matched-pairs.jpg)
and [graphics sheet](renders/lookdev/graphics-sheet.jpg) are ignored checkpoint
outputs. Each state has eight 1440 px views under `renders/lookdev/<state>/`.
The 3072 px matched renders and the three dense-source comparisons retain their
camera/light metadata beside the images. The two used-board fits have RMS
15.34 px on a 1285 px crop and 22.60 px on a 3072 px crop; the full-size loose
truck has 13.65 px RMS on a 600 px photograph. Upsampling that last photograph
does not add detail or improve its measured fit. The 1140 px wheel/truck crop
comes from the constrained 3072 px full-board fit, not an invented close-up fit.

The numerical evidence is `build/<state>/{construction,high-check,verify}.json`,
`build/repeat-delivery.json`, `build/repeat-form.json`, `build/photo-balance.json`
and `renders/lookdev/{budgets,values}.json`. `make check`, `make repeat`,
`make repeat-form` and `make check-variants` rebuild those respective audits.
