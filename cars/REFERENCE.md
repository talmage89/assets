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

# Alder X220 — compact crossover form basis

An original two-row late-2010s compact crossover, compared with two makes.
The selected FWD-capable package uses 225/65R17 tires. All sculpting, aperture
outlines and construction controls are authored in metres; no photograph is
traced, imported into Blender or projected into a texture.

| Quantity | Toyota 2020 RAV4 LE US brochure | Honda 2020 CR-V LX US specification | X220 design target |
| --- | ---: | ---: | ---: |
| Length | 180.9 in / 4595 mm rounded metric | 182.1 in / 4625 mm rounded | 4600 mm |
| Wheelbase | 105.9 in / 2690 mm | 104.8 in FWD / 2662 mm | 2690 mm |
| Body width | 73.0 in / 1855 mm | 73.0 in / 1855 mm | 1855 mm including cladding |
| Published height | 67.0 in / 1701 mm, with antenna | 66.1 / 66.5 in FWD/AWD / 1679 / 1689 mm | 1679 mm roof / 1700 mm low rails |
| Front / rear track | 63.0 / 63.7 in / 1600 / 1618 mm | Same for FWD; AWD 62.9 / 63.5 in | 1600 / 1610 mm |
| Running ground clearance | 8.4 in / 213 mm | 7.8 / 8.2 in FWD/AWD / 198 / 208 mm | 205 mm underbody target, underbody deferred |
| Tire | 225/65R17 on LE | 235/65R17 on LX | 225/65R17 |
| Approach / departure | 19 / 21 degrees | 18.1 / 25.3 degrees FWD LX | Measured on actual form, not claimed OEM-equivalent suspension loading |

The [Toyota manufacturer-authored US brochure](https://cdn.dealereprocess.org/cdn/brochures/toyota/2020-rav4.pdf)
is archived by Dealer eProcess; see the exterior dimensions and capability
tables. The [Honda manufacturer sheet](https://hondanews.com/en-US/honda-automobiles/releases/release-47ef5ef525f391ae783334075a01030f-2020-cr-v-specifications-features)
explicitly distinguishes FWD/AWD. Inch publications are rounded; converted
values do not imply submillimetre physical precision.

Toyota's [2019 launch specification](https://global.toyota/en/newsroom/toyota/21906523.html)
explicitly gives **66.9 / 67.1 inches without/with roof rails**, but labels these
preliminary. The 2020 brochure's height includes its antenna. Those height
definitions and trim changes are retained rather than silently combined.
The [manufacturer-authored 2019 UK Honda brochure](https://www.kingswood-honda.com/wp-content/uploads/2019/01/CR-V_Brochure.pdf)
gives **2117 mm including mirrors**, used as a same-generation class cross-check
for the original housings. It is not asserted to be a US trim specification.

The downloaded June-2021 Toyota UK document is a **plug-in** cross-check:
4600 / 2690 / 1855 / 1690 mm, with 910 / 1000 mm overhangs and different
1600 / 1630 mm tracks. Its 190 mm clearance and 17.5 / 20 degree angles are
not substituted for the US LE. The X220's **960 / 950 mm** overhang allocation
is an original brief requirement (front longer), not a claim that both makes
publish that relationship. The full wheelbase-registered silhouette residuals
against each stock profile remain in the review images and JSON.

The 0.9 mm steel skin, 3 mm fascia/molding gauge, nominal 4.5 mm reveals,
4.8 mm main glazing, low rail feet, arch flanges and mirror housings are
construction estimates. Body panels, glazing and apertures are cut after the
single regular all-quad parent has been fitted and subdivided. The game mesh
retains parent normals; the master itself is never projected after subdivision.
Six lights provide a fixed rising quarter window; the rear glass and liftgate
share the roof-hinged parent. Hinge clearance, struts and interior remain later
work, so the pivot metadata is not a clearance certification.

The source check measures actual evaluated triangles, rays and plane sections,
including separate molding heights/proud offsets, optical lengths, well depths,
backlight widths and finite-span corner radii. The three-point circle is a local
plan measurement, not a constant-radius claim for an entire bumper. Angles from
normal interpolation are distinguished from position measurements. Curvature
reports keep every raw sign crossing, along with the specific die/shoulder,
molding and bumper-transition zones; these finite sections do not certify global
automotive Class A fairness.

Four chassis-only three-quarter fits use inspected hubs and ground-contact
centroids, with pixel-pick and tire/trim uncertainty. Two supplemental side fits
hold an estimated 85 mm lens and use four chassis anchors, not body outlines.
They disclose perspective effects alongside the unchanged orthographic overlays;
their fixed focal length is not EXIF. Rear photographs supply glass/body ratios
with approximately +/-5 preview-pixel uncertainty. No low chassis residual is
reported as all-body accuracy. White studio backdrops are the white-balance
neutral (unit gains); neutral clay is not a paint-albedo match.

For the SUV, glass lean is a chord across the central 60 percent of each actual
side pane's ray-hit height span, excluding rounded borders. The previous fixed
1.25/1.51 m chord can cross onto a frame or the windshield and is retained only
as debugging evidence with the hit-object names; it is not a glass angle.
Approach/departure use a mean circle fitted from actual tire extents and hub
height, and supporting-plane tests of the actual outer-form vertices. They do
not certify suspension loading, underbody clearance or later moving assemblies.

The two near-rear photographs estimate 314 mm (Toyota) and 275 mm (Honda)
vertical backlight span under the same width normalization. These are projected
photo ratios with uncertain camera pitch and body-width correspondence, not
manufacturer glass dimensions. The original's 250–360 mm construction range
allows for those uncertainties; the actual centerline height is measured in
`build/suv/form-check.json` along with its widths and rake.


### X220 round-two plan and fascia measurements

The Toyota RAV4 XA50 rescue sheet (2019-04) and Honda CR-V RW rescue sheet
(2019 model, release 08/2018) supply sparse top-view envelope measurements at
approximately 800 mm half-width. The images and four straight front/rear
photographs are annotated by `suv_references.py` in the ignored review folder.
That tool never supplies geometry to the model generator. Source links,
authorship and copyright are recorded in `refs/SOURCES.md`.

| Measurement | Toyota | Honda |
| --- | ---: | ---: |
| Front setback from center | 271 mm | 258 mm |
| Rear setback from center | 252 mm | 197 mm |
| Front lamp outer height | 161 mm | 167 mm |
| Front black center height / hood-to-ground share | 391 mm / 43.4% | 303 mm / 37.2% |
| Rear lamp corner height | 178 mm | 197 mm |
| Main lower rear lip | 229 mm | 233 mm |
| Entire rear black region including upper band | 407 mm | 276 mm |

Plan estimates allow approximately ±20 mm, photo heights ±30 mm, with additional
trim/perspective differences. The Honda rescue sheet predates the facelift and
is normalized to the cited US length; it is not precision 2020 bumper CAD.
The white background is the photographic neutral, with unit RGB gains.

The source front follows both makes' front setbacks. Its 211 mm rear setback
follows Honda rather than Toyota. The main rear lip is 220–248 mm, distinct from
the manufacturers' entire black upper-and-lower regions. The revised source
front approach is 17.88° (Honda's 18.1° comparison); rear departure is 20.64°
(Toyota's 21° comparison). Actual physical rays, sections and supporting planes,
not those targets, produce the source measurements. Source plan circle samples
are flattened into XY before reporting the local radius; their envelope hits
can occur at different heights.
