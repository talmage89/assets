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
at the same radius. Preserve the thin real cap and flange shadow reveals. Final construction inspection
also caught bolt heads buried too deeply in the flange crowns; reseat the
bonnet/base hardware above the actual casting surfaces. The material masks are
clamped before deriving metallic, so stronger wear cannot produce negative
metallicity. A fixed barrel hook now anchors the common chain ring;
the three caps stay tethered independently of each other.

Camera fit: 112.07 px RMS at the original 3508 × 4765 resolution (about 22 px
at a 950 px-wide comparison); older-casting differences and estimated silhouette
landmarks remain. Independent Blender projection disagreement is 0.00162 px.
Lens 109.5 mm is a fitted estimate, not a claim about the photograph's physical
lens. The calibration overlay displays residuals explicitly.

## Delivery review

The first eight exported-GLB Cycles images were opened individually. Geometry,
bolt seats, the grounded base, cap chains and scale read correctly. Close-ups
exposed weak letter relief: vertical extrusions have parallel front normals,
so a projection bake cannot capture a hard vertical letter edge reliably.
Added 1.2 mm source edge fillets and 0.9 mm extrusion/draft. This changes only
the high source (47,832 triangles); the game mesh stays 5,980. The first weak
casting close-up is retained in `build/delivery-review/casting-before.png`.

Opened all eight revised Cycles views individually: hero, front, side, back,
top, controls, casting and scale. Opened the Eevee hero and the complete contact
sheet as well. Beveled letter relief now survives the 1024 normal map and reads
as casting marks in the rear/detail views. Bonnet/base hardware is seated above
the flange crowns; ribs terminate below the shoulder; chains have a fixed hook.
The 1.8 m silhouette establishes the 812.8 mm asset height. Eevee is darker and
more contrasty than Cycles under the shared studio, with the same baked material.

`make` completed with exit 0 after the clean delivery rebuild and corrections;
`make check` also completed with exit 0 on the revised export. The game/high
audits report 5,980 / 47,832 triangles, valid closed topology and matching
415.544 × 395.000 × 812.800 mm bounds. The GLB is 4,127,488 bytes, one mesh and
one material, with exactly three 1024-square textures. Independent re-import
reports zero measured vertex displacement and zero UV overlap; coverage is
56.73%, density p5/median/p95 is 539/597/683 px/m. Vertex normal length error
is 1.19e-7; shipped texture normal vectors pass the independent normalization
check. All nine shot records identify the same exported GLB SHA-256.

`renders/final/contact.jpg` includes all eight Cycles views and Eevee last.
Final README images are `docs/hero.jpg` (79,605 bytes), `turnaround.jpg`
(136,113 bytes), and `details.jpg` (106,042 bytes), all no wider than 1600 px.

The weakest areas remain close cap-rim normal waviness, angular chain wire, and
soft small lettering/paint chips in one 1024 atlas. The studio red is less
saturated than the direct-sun reference; wear is more orderly than incidental
real damage. This is a street-scale prop, with those close-range compromises
reported rather than called an exact photographic replica. No more source
critique rounds are justified for this importance tier.
