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

The 1065 mm front and 1005 mm rear overhangs follow the requested original
front-longer stance. They are not Camry dimensions: the UK sheet has 975 / 1085 mm,
so the independent Camry side overlay must retain the resulting axle-registered
nose/tail discrepancy. A photograph is not stretched to hide it.

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
traced or fitted into the cage. The two 3/4 camera fits use chassis landmarks;
body correspondence remains an independent visual judgment and held-out report.
The stock backgrounds are neutral white: comparison white balance uses that
backdrop, not the warm/cool reflected paint. Clay is neutral gray by design.
