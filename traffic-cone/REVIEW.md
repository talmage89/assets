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
