# Alder C150 / dimensional basis

This is an original late-2010s American crew-cab 4x4 with a nominal 5.5-foot
bed. The envelope uses one coherent short-bed configuration. Manufacturer
names identify references, never the generated vehicle's brand or design.

| Quantity | Reference | Selected design |
| --- | --- | --- |
| Overall length | Ford MY2018 SuperCrew 5.5-foot box, 231.9 in | 5890.26 mm target |
| Wheelbase | Same configuration, 145.0 in | 3683 mm |
| Body width, mirrors excluded | Same, 79.9 in | 2029.46 mm target |
| Roof height, 4x4 | Same, 77.2 in | 1960.88 mm |
| Bed length at floor | Same, 67.1 in | 1704.34 mm |
| Front/rear track | Ford MY2017 body-builder book p15, 1716 mm each | 1716 mm each |
| Front overhang | Same book p11, 959 mm / rounded 37.8 in | 960.12 mm from inch conversion |
| Ground clearance | GM MY2018 4WD crew short-box guide p19, 226 mm at base curb weight | 226 mm target and measured differential clearance |
| Tire | Ford MY2017 book p16, 275/65R18 A/T on 18 x 7.5 wheel | ISO nominal 814.7 mm diameter, 275 mm nominal section |
| Wheel inset | Same book p16, six-spoke 18 x 7.5 wheel, +44 mm | +44 mm mounting-face plane |

Ford's [MY2018 specification sheet](https://media.ford.com/content/dam/fordmedia/North%20America/US/product/2018/f-150/18_F150.pdf),
p2, supplies the primary envelope. It was readable through the web tool;
its direct download returned HTTP 403. It is cited but is not a build dependency.
The locally downloaded [MY2017 body-builder book](https://madocumentupload.marketingassociates.com/api/Document/GetFile?v1=4311674&v2=060118100149&v3=60&v4=3f2137473068fd5fc81405c4d6ffa529d55a0aa9f7e934d690b5cef0&v5=False)
is explicitly the previous model year of the same generation, used for chassis,
wheel and construction context rather than relabeled as MY2018 data.

The [GM MY2018 guide](https://www.gmupfitter.com/wp-content/uploads/2021/05/2018-gmf-silverado-special-service-police-spec-guide.pdf),
p19 (printed p16), is a class cross-check: 5842 mm length, 3645 mm wheelbase,
2032 mm width and 1761 mm bed floor for the 4WD short box. It describes a
special-service variant, so its lower height is not substituted into the Ford
crew-cab envelope. Its ground-clearance figure supplies the original design's
provisional underbody target.

## Authored construction and uncertainty

The 4.5 mm door reveals, 0.9 mm outer sheet gauge, 12–13 mm inward edge returns,
4.8 mm glazing thickness, 16 mm cab/bed gap and panel styling are original
construction estimates. They are not claimed manufacturer measurements.
The roof, hood and side surfaces are analytic equations authored in meters;
no image outline was traced, projected or converted to mesh.

The shipped tire uses a circular mean loaded envelope: 401.35 mm rolling
radius, 275 mm section width, and 802.70 mm overall height. A parked 12 mm
flat spot would rotate through the ground during wheel animation, so the
radial sidewall compresses toward the bead instead. This represents a light
load; it does not simulate carcass squirm. Ford's p16 minimum static loaded
radius of 14.33 inches describes a different load condition. Ground contact,
width and full-revolution support are independently checked; the accepted
arch/tire-top clearance remains 90.30 mm.

## Photographs and the second form gate

Sources, authors and licenses are in [refs/SOURCES.md](refs/SOURCES.md).
The previous Kevauto comparisons are superseded by the CarsDirect/Autodata
2018 XLT SuperCrew 5.5-foot / 145-inch-wheelbase stock front, rear and true
profile photographs. The source page labels them **4x2**; do not assume the
photographic ride height is the 4x4 design's specified height. The pictured
alloy wheels also differ from the authored 18-inch wheels. These are class
proportion and construction references, not a claim of an identical trim.

The side overlay uses only the two inspected wheel centers and the published
3683 mm wheelbase to determine scale, translation and a 0.125-degree image
level correction. No body silhouette participates in that fit. The straight
A-pillar segment measures approximately **34.4 degrees above horizontal**
(55.6 from vertical), with roughly +/-1.5 degrees of photographic picking
uncertainty. The authored outer A-pillar is 35.2 degrees above horizontal.
`side-rake.jpg` shows the picked segment; `side-overlay.json` records pixels,
scale, opacity, source hashes and the height/configuration caveat.

Three-quarter calibration fits two visible wheel hub centers, two tread-ground
contact centroids and one opposite-side tire contact. The opposite-side point
is necessary: four near-side points alone poorly constrain camera height.
The ground anchors represent visible contact centroids, not an invisible
point directly below an outer hub. Their lateral position has approximately
20 mm uncertainty; the soft contact shadows have several pixels of picking
uncertainty. The early form calibration held hub height at 395.35 mm; final used-truck
calibrations use the shipped 401.35 mm rolling radius.

The reported few-pixel RMS is for those **five chassis anchors only**. Roof,
mirror and bumper correspondence is not established to that accuracy; these
original body shapes are compared visually and in the independently scaled
side overlay. Thus this improves the former 74 px registration, but does not
fully satisfy the requested all-body-landmark calibration. Do not treat the
low chassis residual as proof of a correct body. No roof fitting or body
warping conceals the visible differences. The symmetric extra image margins
keep the original truck's full front and rear corners in view; the photograph
has transparent padding there, not generated photographic content.

## Third form gate: authored surfacing and independent measurements

The envelope, chassis, floor and reveal targets above remain authoritative.
The requested 30–40 mm flare is a design requirement from the form brief,
not a published manufacturer stamping dimension. Crown, die lines, arch power,
roof roll and front-face rake are authored original controls, informed by
looking at both Ford and Ram photographs, without image tracing.

`form_evidence.py` measures the evaluated mesh by surface rays and outer-skin
vertex rows. `side_overlay.py` registers only the original two axle picks and
then measures the rendered alpha at separately inspected photographic silhouette
stations. Photo station uncertainty is +/-5.6 original pixels (about 16 mm).
Bumper outline picks are +/-7 px (about 20 mm). These estimates do not remove
perspective or the 4x2/4x4 configuration difference.

`compare_form.py` marks semantic body points on the same calibrated 3/4 pairs,
with +/-14 source pixel picking uncertainty. Body residuals are reported
separately and never improve the five-chassis-anchor RMS. Their larger errors
remain evidence of styling, correspondence and calibration limitations; they
are not hidden by a new camera fit. `class-crosscheck.jpg` additionally places
the Ford and Ram photographs beside the original clay and explicitly makes
no registration claim.


# Alder S240 — original 2018–2022 midsize sedan / form gate

The sedan combines the class envelope below with its own six-light greenhouse,
swept narrow lamp openings and low grille. It is not a reproduction of either
reference. All values in the design column are original targets; actual surface
measurements are rebuilt in `build/sedan/form-check.json`.

| Quantity | Toyota MY2019 Camry SE, US manufacturer eBrochure | Honda MY2019 Accord LX, manufacturer metric sheet | S240 target |
| --- | ---: | ---: | ---: |
| Length | 192.7 in = 4894.58 mm | 4882 mm | 4900 mm |
| Wheelbase | 111.2 in = 2824.48 mm | 2830 mm | 2830 mm |
| Body width | 72.4 in = 1838.96 mm | 1862 mm | 1850 mm |
| Height, unloaded | 56.9 in = 1445.26 mm | 1450 mm | 1450 mm |
| Front track | 62.2 in = 1579.88 mm | 1600 mm | 1590 mm |
| Rear track | 62.6 in = 1590.04 mm | 1610 mm | 1600 mm |
| Clearance | 5.7 in = 144.78 mm | 149 mm no load / 125 mm full load | 145 mm underbody target; underbody deferred |
| Tire | P235/45R18 | 225/50R17 LX | 235/45R18 |

[Toyota's manufacturer-authored eBrochure, archived PDF](https://cdn.dealereprocess.org/cdn/brochures/toyota/2019-camry.pdf),
EXTERIOR DIMENSIONS table and SE wheel/tire specifications, supplies the US
comparison. Decimal-inch conversion has rounding uncertainty; it does not claim
submillimeter manufacturer precision. [Honda Canada specification](https://hondanews.ca/en-CA/releases/release-4f32a27ba2ad7509bfa642e1160157a6-2019-honda-accord-specifications)
supplies the metric cross-check; the [US sheet](https://hondanews.com/en-US/releases/release-a8bcd9c102224d06ba836e803e27878d-2019-honda-accord-specifications-features)
agrees within published rounding. UK 2021 Camry brochure gives 4885 / 2825 /
1840 / 1445 mm and 145 mm clearance; it is an explicitly different-market check.

Round 2 corrects the original front-longer allocation: **975 mm front and
1095 mm rear** on the original 4900 mm length / 2830 mm wheelbase. The
[Toyota UK June 2021 brochure](https://www.toyota.co.uk/content/dam/toyota/nmsc/united-kingdom/brochure-archive/camry/camry-jun-21.pdf)
provides explicit 975 / 1085 mm overhangs on its 4885 / 2825 mm envelope. Our
10 mm extra length minus wheelbase goes at the rear. The 975 mm front is 25 mm
outside the brief's rough photographic 860–950 mm range; the coherent published
metric basis takes precedence over that approximate range. Cabin, door stations
and axles translate together 90 mm forward. This is a coordinate relocation of
the accepted package, not a wheelbase or track change.

Six lights leave a fixed triangular quarter pane in the C-pillar, reducing the
rear door's upper sash length under the fast roof. 22.5-degree section tumblehome,
4.5 mm nominal shut lines, 0.9 mm sheet gauge, 4.8 mm glazing and 18 mm arch
returns are authored construction estimates, not manufacturer stamping drawings.
The nominal tire diameter is 668.7 mm; the circular mean loaded envelope has
330.35 mm radius and 660.70 mm height, with a planned 40 mm arch crown gap.
This is the pickup's rolling-envelope method, not a carcass simulation.

The sculpted supported cage is authored in three dimensions; subdivision occurs
before any panel or glazing separation. The profile photo is used only in an
external, wheel-center-only similarity transform after rendering. No outline is
traced or fitted into the cage. The four 3/4 camera fits use chassis landmarks;
body correspondence remains an independent visual judgment and held-out report.
The stock backgrounds are neutral white: comparison white balance uses that
backdrop, not the warm/cool reflected paint. Clay is neutral gray by design.


Round 2's end-volume controls are original construction estimates constrained by
the requested dimensional ranges, checked against both makes. A continuous
elliptical plan loft, a rounded crowned top and a tucked lower face fair the
unified supported subdivision cage before separation. No photo is read by the
model generator. Mesh cuts/rays and actual aperture vertices independently
measure the resulting dimensions, including the centerline profile. The side
overlay's +14 mm roof-front holdout meets the requested approximate 20 mm target;
its −96 mm deck mismatch remains visible because the Camry SE spoiler sits above
the brief's 1000–1050 mm tail-lip height. It is not suppressed by warping the photo.




## Round 3 surface construction and measurement

The round-2 end-volume projection is historical. The current body is a single
regular quad control sheet spanning both ends and the accepted canopy. Original
waterline, centerline and cover sections fit the control vertices before final
Catmull-Clark evaluation. The evaluated surface is never projected onto separate
end volumes. No photograph is loaded by the model generator.

The rear 250–400 mm corner-radius target and 20–35 mm wheel swells come from
the round-3 brief. `sedan_shaping.py` measures a local circle through actual
x=800/850/880 mm bumper-height rays, and compares actual fender/door rays at
z=760 mm. A local circle is not a constant-radius claim for the whole quarter.
The concave door run and crisp support lines are authored original styling.
The 3 mm molded fascia wall is an authored construction estimate; the steel
skin and glazing retain their earlier gauge estimates.

The regular game chart retains parent extrema, positions and normals before
panel separation. World-space door cuts, trunk reveals and projected lamp
apertures are made afterwards; holes are independently ray-checked. Cover
curvature is sampled on both parent and game at three transverse stations each,
with five body sections as a separate check. Cut gaps split derivative runs.
Rocker, lower draw, shoulder and bumper/deck transition zones are explicit in
the JSON/plots. No smoothing curve is fitted to the resulting measurements.

The four cited stock photographs and Camry profile remain the two-make visual
basis, with the same chassis-only camera registrations. Their neutral white
backdrops supply unit-gain white balance. The held-out silhouette differences,
including the lower original deck versus the photographed spoiler, remain
visible. These comparisons and finite curvature samples are not a global
Class A or final material/delivery certification.

## Round 4 character, construction and measurement

The source remains one fitted regular quad sheet, subdivided before any cuts.
Round 4 adds progressive door sections and a supported lower die line, raised
fender crowns, original rising headlamp blades and tapered rear wings, actual
molding wells, a 21.3 mm integrated deck kick and door-mounted mirrors. The
C-pillar controls are raised independently of the held windshield/header.
The deck crest is now 1110.8 mm rather than round 2's 1000–1050 mm range:
this intentionally follows the later round-4 instruction to raise it onto the
overlay. Other round-2 end range checks remain active.

The original mirror housing is 250 mm outboard × 204 mm fore/aft × 157 mm
high, with 2110 mm across the assembled pair. Ford's manufacturer-authored
[MY2020 Mondeo brochure](https://www.ford.ie/content/dam/guxeu/uk/documents/feature-pdfs/FT-Mondeo.pdf)
provides the class cross-check: 2121 mm including mirrors, 1852 mm body.
These dimensions do not imply the mirror styling was copied. Housing and
molding construction dimensions are original estimates; see the source register.

`sedan_character_check.py` measures actual game cuts and rays, parent-derived
corner-normal angles, the shallow hollow's 50 mm chords and the crease's 80 mm
normal interval. Recess rays use only outward smooth skin normals; flat gauge
rims cannot define a recess normal. Separate paint-clearance rays establish
that each well is a real hole. The integrated lip is measured above a linear
extrapolation of two adjacent actual deck samples. Chart triangulation gives
each optical blank one disk topology before gauge closing, avoiding folds at
thin projected tips. Static construction and serialization are separate:
the sedan tests are source construction checks; the preserved pickup GLB
comparison proves serialization/byte identity.

The final local rear circle is 303.4 mm at x=800/850/880 mm, about the held
305 mm draw. Front circle probes move to z=570 mm, above the newly cut corner
pocket; its old z=502 mm probes are now holes. Wheel swells retain the earlier
same-height z=760 mm door-reference method. Curvature reports retain all raw
sign crossings and mark the actual construction-line zones, including the
fender-crown/hood draw transition and lower fascia roll.

The original wheel-center-only orthographic overlay is kept. Added lower-end
holdouts are independently inspected silhouette picks; their points and
±4-preview-pixel uncertainty are in `side-overlay.json`. The C-pillar/deck
now meet the approximate 40 mm request. The lower bumper tangents still miss
it (+132.9 / +78.2 mm); near-profile perspective is unresolved, and accepted
envelope/overhangs are not changed to fit that photograph. This limitation is
reported, not hidden in the camera calibration or softened by a pass flag.

## Round 5 rear construction and photographic limits

The backlight is cut narrower on the same canopy; the remaining painted sail
panels belong to that parent sheet. Widths are measured from the actual outer
glass corners. The source's roughly 1211 / 1268 mm top/base and 252 mm sails
interpolate the two photographed makes, rather than reproduce one of them.
The sail measurement is transverse to the vehicle at the glass base's Y station,
80 mm below that glass corner, approximately z=972 mm at the beltline.

The annotated rear photographs use the existing chassis calibrations. Rays
intersect the estimated glass plane `z + 0.30 y = 1.67 m`; the hip pick intersects
the mean glass-base Y plane. These yield Camry top/base 1316 / 1347 mm and near
sail 243 mm, and Accord 1202 / 1061 mm and 258 mm. Glass width uncertainty is
approximately ±80 mm, sail ±60 mm, including the picks, assumed plane and
camera/class mismatch. These are transverse class estimates, not manufacturer
glass dimensions or widths measured along curved surfaces. The white studio
backgrounds remain the balance neutral; no reference pixels become geometry.

Round 5 supersedes the earlier lower-end tucks and permits overall length within
the class. The actual molding envelope is about 4885 mm; the 4900 mm coordinate
package still defines the unchanged axle/cabin stations. The earlier 100–150 mm
front and 150–200 mm rear tuck ranges remain visible as superseded measurements
in `form-check.json`. The new lower tail turns under over its last 150 mm and
has lifted corners, flush reflector blanks and a rolled finisher. Plate mouth,
plate edge lengths and depth are independent mesh measurements. Their original
construction estimates follow the brief's 320 × 170 mm pocket / 12 × 6 inch
plate; they are not manufacturer stamping specifications.

The original wheel-center-only orthographic overlay is retained. An additional
six-wheel-anchor perspective registration uses an explicit 80 mm lens prior
and 1.25 ±0.10 m camera-height prior. Its estimated 82.3 mm lens has 2.02 native
pixel RMS; 60 / 100 mm priors fit 63.9 / 101.6 mm. A near-parallel wheel plane
does not determine a unique photographic focal length. All three perspective
overlays and the raw orthographic residuals are reported separately. None fits
the body outline or warps a photograph. The nominal perspective result alone
does not establish the original 40 mm overlay requirement; the raw comparison
and lens sensitivity remain limitations.

The quad control net is fitted before subdivision, including smooth fitting
frames at the low rear corners. Final skin normals are sampled directly from
that dense parent, rather than re-interpolated through the game chart. Clip
duplicates and bounded submillimeter crumbs are removed before gauge closing;
optical guides are triangulated in the injective chart before their gauge is
made. These construction changes preserve the existing independent topology,
surface-ray, curvature and chassis checks. They do not certify final optics,
materials, UVs, motion or delivery.

## Round 6: lower profiles, constructed mechanisms and used-car comparison

Round 6 restores the brief's physical lower-end requirements. The actual front
centerline leads at z=500 mm and turns back 133.9 mm to a 174.9 mm chin. The rear
leads at 602 mm and turns forward 189.5 mm to the 300 mm diffuser station; the
painted bottom is 270 mm. These are source rays/vertices, not values read back
from generator constants. A ground tangent to the actual rear tire and rear
overhang gives 18.04°. Honda's current FF Accord FAQ publishes 17.5° departure:
https://www.honda.co.jp/customer/auto/accord/faq/qa015/ . It is an independent,
later-generation class cross-check, not an asserted 2019 Camry specification.
The MY2019 Camry brochure remains the main envelope/tire/clearance reference.

The fixed wheelbase, accepted 4885 mm length and raw side photograph still do
not agree at both ends within 40 mm. Raw wheel-center scaling implies about
4702 mm overall; the final raw residual reaches 118.8 mm at the front bumper
and 71.8 mm at the upper tail. The three prior-constrained perspective cameras
remain separate evidence, with lower-end worst residuals 110–131 mm. No outline
anchor enters their fit. The physical tuck correction is real, and the remaining
overlay miss is real; a passed dimensions check does not establish a photo match.

The continuous sheet remains the form source. Local lamp/A-foot/C-header chart
samples and smooth fitting transitions improve the specified stripe breaks;
the nose/fender chart edge is no longer treated as a physical shut line. The
riggable version additionally cuts a real horizontal sill at 300 mm, keeping the
lower reinforcement fixed while the doors and their glass move. This changes
panel ownership on the accepted sheet, not its envelope. The source form is
52,452 triangles; the completed detail allocation is 59,992.

Five-year comparison photographs are the CC0 MY2020 Camry front/rear images in
`refs/SOURCES.md`, photographed 25 October 2025. Their visible dirt and wear
supply a condition comparison; model-year age is not a verified service history.
Four visible near-wheel hub/contact picks constrain each camera. The purported
far-wheel contacts were occluded and were rejected. Native-pixel RMS is 12.25
front / 13.49 rear, approximately 3 px at 1100 px comparison width. That proves
wheel registration, not body or coating agreement.

Before color comparison, front balance assumes the off-white plaster in the
upper-right background is neutral. Rear balance assumes white paint on the
background car's upper trunk is neutral; the stained curb was rejected. Linear
channel gains and exact source rectangles are in the balanced calibration JSON.
Neither contains a photographed gray card. Colored surroundings and class
material/shape differences remain uncertainty, so the reported RGB/luma values
are **display appearance**, never inferred paint albedos.

Each exported-car patch is ray-cast onto the actual paint skin at its Y/Z
station. Its camera pixel comes from Blender projection. The corresponding
photo patch uses the calibrated camera; cross-class surface correspondence is
approximate. Small annotated rectangles show whether a patch includes a trim,
reflection boundary or shadow. Previous constant x=−0.90 m proxy patches were
rejected: they could sample a different portion of the sloping lower door.
No photograph pixels enter any material, geometry, bake or lighting graph.

The reflection stage uses a procedural sky, area lights/sun and original facade
boxes with window openings represented by dark surfaces. Paint color factors,
metallic response, coating and dirt remain independently authored. A plausible
lighting fit is not proof of BRDF or albedo equivalence. Factory spawn weights
come from Axalta's 2025 North America new-car shares, normalized across the five
options only; they are not estimates of the surviving used fleet.

Door hinge axes are original 7.97° transverse inclinations, explicitly exported
as unit vectors. Pin/bore sizes, leaf attachment, rim/bead widths and stud circles
are measured from the final source meshes. Sampled game/high collision sweeps
and independently evaluated hood supports establish sampled mechanical behavior;
GLB verification establishes serialization. The two claims remain distinct.


The final mechanical allocation is 59,992 triangles. The stepped 1.2 mm floor,
returned tank straps, engine gussets and trunk bearing supports replace the
first underbody proxies without exceeding 60k. Measured lid tips and damper
mounts are within 0.30 mm of their actual supporting sheets; tank-strap/floor
contacts are within 0.20 mm. Wheel hubs have minimum 70.4 mm bores around 70.0 mm
journals, with 31.0 mm measured engagement and 0.20 mm radial running clearance.
The lower control-arm joint centers follow the front kingpin axes. Composite
CV/knuckle/strut contacts are explicitly documented in the motion policy.
