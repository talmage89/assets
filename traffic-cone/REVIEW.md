# Cone review

Pass 1: opened source hero, grip and base close-ups and the product-photo pair.
Dimensions and collar heights read correctly, but the initial top lip was too
wide relative to the grip detail: changed it to the sheet's 1.5-inch top above
the 2-inch lower shoulder. The orange was too pale and the collar edges too clean.
Deepened the pigment, narrowed the specular response, added contact-located foil
edge nicks and fine moulded grip flutes. The base keeps its independently measured
14-inch size; soft photo corners are unsuitable camera anchors, so calibration
uses the body/grip landmarks. Photograph pixels remain comparison-only.

Pass 2 source: opened the revised hero, grip, base close-up and matched pair.
The smaller grip lip, mould flutes and deeper orange read better. The body-only
photo fit is 0.6 px RMS in the 182 px image (151.4 mm estimated lens); its base
remains an independent dimensional check rather than an unreliable soft-corner
camera constraint. The source is cleaner/brighter than aged roadside stock;
WEAR=.55 remains confined to handling and road/ground exposure.

Assembly review caught a genuine bore issue before final delivery: mapping the
base's rounded-square corner parameters onto the bore made a rounded-diamond
opening. Rebuilt both rings from equal-angle stations, using a rounded-square
ray intersection for the outside and a circular inside. The base revision had 792
triangles. The two-instance GLB stack test measures the first clear pitch from
actual mesh intersections, with a stated 0.1 mm safety margin.

The first exported close-up exposed a black neck ring absent from the source.
The sparse inner-wall profile crossed the outer neck. Added two inner transition
stations, preserving a positive wall throughout; added an independent radial-ray
check on the imported GLB so each sampled section must have exactly two wall
hits and at least 2 mm thickness. Rebaked the corrected shell.

Final corrected GLB: opened the hero, all four turnaround images, grip/base
close-ups, human scale, Eevee, contact sheet and calibrated photo pair. The
neck is orange with no projection ring. Collar heights and taper agree with
the photographed slim cone; base width follows the independent 14-inch spec.
The source mould flutes and foil nicks soften at 512, and top-view faceting is
visible close up. This is an acceptable repeated street prop compromise.

`make all match-final PASS=review2` and `make check` pass: 872 triangles, one
material, three 512 maps, 355,384-byte GLB; zero UV overlaps. Stack pitch is
83.446 mm with the 0.1 mm margin, and 336 radial sections remain at least
2.509 mm thick. Support-surface tests and the mesh collision/ray tests prove
physical construction separately from export/reimport serialization.


## Phase 2 regression and used-condition calibration

The clean baseline still exports 872 triangles / one 512 set / 355,384 bytes,
matching the README. A new bake diagnostic found 48,167 black/missed interior
samples among 8,212,941 covered 4096 samples. Independently rasterized each
object's UVs: every miss belongs to the weighted base's coarse outer corner
walls; the orange shell/grip has zero misses. This is not the previously fixed
neck geometry defect. The inset low corner chords lie behind the high base
surface beyond the old 2 mm cage. The wear build uses a 5 mm cage and 12 mm
ray limit, preserving geometry and UV policy. Review its bake report and the
actual exported base/neck before accepting; no missing pixels are filled.
Diagnostic: `../build/polish/cone-bake-diagnostic.json`; original report is
`../build/polish/cone-baseline-bake-report.json`.

First wear source comparisons opened against the moderate campus and severe
roadside photographs. Rejected the broad tan base dust and parallel marks
that read as decorative stripes. The severe roadside cone is a useful upper
limit, not the few-seasons target. Narrowed rubber transfer to one short
contact patch, reduced base dust and mid-body stacking grime, retained more
orange saturation, and dulled the plastic. Collar abrasion remains localized
to film rims and stacking directions. The next pass also tests the measured
base-corner projection correction without changing any mesh or UV.

Second wear checkpoint accepted after opening both source/exported campus
and roadside pairs plus the full hero, four orthos and both detail views.
The 512 atlas preserves visibly worn collar film, low splash and dull scuffed
PVC; short rubber transfers remain localized instead of wrapping like stripes.
The base retains its dark material rather than a tan dust coating. The campus
photo is the moderate-use target; the severe roadside image is only an upper
limit. Studio color is lighter than outdoor PVC and the small atlas blurs fine
scratches. Original 20-sided silhouette and foot faceting remain unchanged.

The actual base-corner bake correction passes: 5 mm cage and 12 mm ray reach,
zero misses in all five channels over an 8,212,941-texel interior mask, zero
black BaseColor interior samples. This is projection reach, not painted repair
or new geometry. `make export check` passes at 872 triangles, one material,
one mesh, 499,956 bytes. Maps stay 512: 224,662 / 83,999 / 143,583 bytes.
Full final studio/docs generation follows this accepted material checkpoint.

Final Phase 2 `make` exits 0 (`../build/polish/cone-final.log`). Opened all
eight final Cycles views, Eevee, contact sheet and all three final docs.
Collar abrasion and low scuffs read at full-frame hero distance; the base
corner projection holes are absent. Current-GLB hashes match all nine final
studio metadata records. Geometry/UV/normals/tangents and origin are bytewise
unchanged by the material/projection update, independently compared to the
clean baseline GLB. No construction, scale or budget regression remains.
