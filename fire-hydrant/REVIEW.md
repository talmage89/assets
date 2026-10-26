# Photo-directed review

Reference images are only viewed beside the original model, never sampled into
geometry, UVs or textures. The manufacturer drawing controls the absolute
height, nozzle axes and wrench nut; the older installed rear photograph checks
construction and weather. Original casting differences remain visible.

## Pass 1 — source, 850 px / 24 Cycles GPU samples

Opened every render: `renders/pass1/hero_closed.png`, `casting.png`, `front.png`,
`installed_rear.png`, the `installed_rear-pair.jpg` comparison and calibration
overlay. Compare to `refs/weathered.jpg` and `refs/product.jpg`.

The asset read as a hydrant but the pale, matte red looked like a plastic toy.
The barrel lacked the lower cast shoulder; the foundry text was too small and
appeared to float slightly over the surface. The edge-wear mask hardly touched
the nozzle cap rims, so there was no visual history of wrench handling. The
close-up camera caught the dark end of the studio background. Chain endpoints
coincided at the center without a distinct joining ring.

Corrections: deeper red enamel with a more coherent satin highlight; stronger
cast microstructure; physically located cap-rim chip masks; dust/splash at the
lower flange; lower cast shoulder and stronger reinforcing ribs; larger original
foundry type; real joining ring and offset chain endpoints; elevated rear-detail
camera. The low mesh retains only silhouettes and wrench flats; washers, fine
cap beads and letter relief remain source-only for baking.

## Pass 2 — source, 950 px / 32 Cycles GPU samples

Opened `renders/pass2/hero_closed.png`, `casting.png`, `installed_rear.png` and
`installed_rear-pair.jpg`. The metal cap highlights, edge abrasion, lower shoulder
and foundry lettering now read more clearly at street distance. The photograph
has stronger direct sunlight and more accidental surface variation; the studio
is intentionally softer. The original casting is taller above the nozzles and
has a different bonnet/shoulder profile from the older photographed casting.
Do not force those estimates into a false exact replica.

Remaining errors corrected before bake: reinforcing ribs were extending above
the cast shoulder as little fins; terminate them below the shoulder. Embed the
raised text root into the calculated barrel radius instead of holding all words
at the same radius. Preserve the thin real cap and flange shadow reveals.

Camera fit: 112.07 px RMS at the original 3508 × 4765 resolution (about 22 px
at a 950 px-wide comparison); older-casting differences and estimated silhouette
landmarks remain. Independent Blender projection disagreement is 0.00162 px.
Lens 109.5 mm is a fitted estimate, not a claim about the photograph's physical
lens. The calibration overlay displays residuals explicitly.

## Delivery review

Pending exported-GLB inspection and the final delivery checks.
