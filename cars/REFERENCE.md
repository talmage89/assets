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

# Alder H120: compact five-door hatchback, source form checkpoint

The H120 is an original 2018–2022-class front-drive hatch. Two different
manufacturers establish the package and provide independent shape comparisons;
neither silhouette is traced into a mesh. The Toyota's short rear package and
the Hyundai's relatively level roof are useful constraints. Alder's narrow
rising lamp blades and broad horizontal grille continue the sedan language.

## Published dimensions and chosen package

All values below are millimeters. Direct PDFs, author, rights and local fetch
names are recorded in [refs/SOURCES.md](refs/SOURCES.md).

| Dimension | Toyota Corolla hatch, MY2019 Europe | Hyundai i30 five-door, November 2018 UK | H120 design target |
| --- | ---: | ---: | ---: |
| Length | 4370 | 4340 | 4360 |
| Wheelbase | 2640 | 2650 | 2650 |
| Body width | 1790 | 1795 | 1795 |
| Height | 1435 | 1455 | 1450 |
| Front / rear track | 1531 / 1544 | 1565 / 1573, SE 16-inch package | 1550 / 1560 |
| Front / rear overhang | 935 / 795 | 1690 combined, calculated | 925 / 785 |
| Width with mirrors | Not used from this sheet | 2039 | About 2039 |
| Ground clearance | 135 | Not used from this sheet | 140, underbody deferred |

Toyota source: [MY2019 European Corolla launch press kit, p50](https://newsroom.toyota.eu/download/647310/2019-toyota-corolla-dpl-en-983710.pdf).
Hyundai source: [November 2018 UK i30 technical specifications](https://www.hyundai.news/newsroom/dam/uk/press-kits/20181001_i30/hyundai_i30_fivedoor_and_tourer_press_kit_november2018_technical_specifications.pdf).
The Hyundai sheet does not separately establish the two overhangs here; their
1690 mm sum is calculated from length minus wheelbase. Tracks depend on the
wheel package.

The chosen tire is **225/40R18**, a listed Toyota upper-trim size. The
[2021 Australian i30 same-generation specification](https://www.hyundai.com/content/dam/hyundai/au/en/models/i30/docs/Hyundai_i30_Hatch_Specifications.pdf)
independently lists 225/40R18 on an 18 × 7.5J +53 wheel for N Line, with
1549 / 1563 mm tracks and 135 mm kerb clearance. Its base trim lists 140 mm
clearance and 1559 / 1568 mm tracks. This is explicitly a later, same-generation
cross-check, not a MY2019 specification. H120 tracks are original rounded
upper-wheel-package values. Its 140 mm target is not reported as a measured
minimum: there is no drivetrain or suspension underneath at this checkpoint.

The tire designation gives a nominal 637.2 mm diameter. The form wheel uses
the family's simple circular tire at 314.6 mm hub height, 4 mm below nominal
unloaded radius; measured geometric diameter is 629.2 mm. This is an explicit
form approximation, not a loaded-tire or contact-patch simulation. All four
arch tops are 40 mm above those tires, with inward 18 mm arch returns.

## Photographic evidence and its limits

The eight CarsDirect/Autodata photographs are MY2019 Corolla Hatchback SE and
MY2019 Elantra GT Base (the North American i30 five-door). Front/rear
three-quarters, near-profile and rear photographs of each make were inspected.
Their wheel designs are not copied. Both sets have neutral white studio
backgrounds; that unobstructed white is the comparison neutral, with unit RGB
gains. It does not make silver metallic paint a clay albedo reference.

Four camera fits use five chassis landmarks each: near wheel centers, near
tire contacts and one far tire contact. Body silhouette points are held out.
At native 2100-pixel width the RMS residuals are 3.59 / 2.95 px for the Corolla
front/rear, and 5.02 / 7.81 px for the Hyundai front/rear. These prove camera
registration accuracy at those anchors, not body accuracy. The photographs'
wheel diameters differ slightly from the chosen H120 upper-trim package.

Both side overlays use only the wheel centers to determine scale and level.
The stock photographs retain perspective, and the illustrated elevations in
Toyota's MY2019 brochure and Hyundai Morocco's July 2018 sheet also differ from
their numerical package ratios. None is presented as an exact orthographic
engineering drawing. The raw overlay deviations are retained in the review
JSON and README; there is no silhouette warp or fitted body outline. Manual
side picks have approximately ±14 mm uncertainty at the wheel plane, in
addition to the unquantified perspective error.

Rear photo widths, normalized to each published body width, estimate:

| Projected feature | Corolla | Hyundai |
| --- | ---: | ---: |
| Backlight upper width | 1114 mm | 1149 mm |
| Backlight base width | 1232 mm | 1385 mm |
| Outer pillar band at lower-glass level | 123 mm | 88 mm |

These are ±30 mm photographic estimates: top/base glass and body-width
landmarks are at different depths. All pixel picks and marked photos remain
in `renders/hatch-checkpoint/rear-reference-measurements.json` and accompanying
JPGs. H120 actual mesh widths are measured separately; its pillar measurement
is explicitly a projected difference between the upper-quarter width and
lower-glass width, not a structural metal-section thickness.

H120 uses a small fixed rear quarter pane, like the Hyundai, flush side glass,
and a black B-pillar applique. The bumper carries the plate pocket, also as on
the Hyundai; the uninterrupted upper gate and split wraparound lamps are
original. Fine lamp optics, trim, weathering, cargo/interior construction,
hinges and struts remain beyond this form checkpoint.

### H120 round 2: perspective profiles and regional choices

The original axle-registered orthographic overlays are historical evidence,
not the current comparison method. Both profile photos now have kit pinhole
camera fits using near wheel hubs and tread contacts. Body silhouette picks
are held out. Four coplanar landmarks do not determine a unique focal length:
the fit uses a 65 mm prior, 45–100 mm bounds and converges near 70.8 mm.
Native-image RMS is 4.30 px Corolla / 4.31 px Hyundai. A separate Blender
projection check validates the solver-to-render camera conversion. It does
not validate the assumed depth or the body shape.

The new silhouette is rendered directly through each fitted camera. Regional
errors are equivalent millimeters using local center-plane projection scale;
manual edge-pick uncertainty is approximately ±16 mm. The Corolla governs the
rear roof, spoiler, glass rake and upper gate, while Hyundai governs the lower
bumper tuck and bumper-mounted plate. The photographs disagree substantially
at the upper tail; the report preserves both deviations. Accepted body length,
wheelbase, tracks, door sections and arch gaps are retained.

The measured mirror span is 2039.3 mm, following the **2039 mm** published
width with mirrors in the November 2018 Hyundai UK manufacturer sheet linked
above. The new wedge caps sit on the front door’s sail, with a flat rear pane.
Reference photos are used only for measurements and side-by-side review.


### H120 round 3: rear construction and surface references

The lower black bumper center and tall slim corner reflectors now follow the
Corolla rear photograph (`refs/hatch-corolla-back.jpg`), while retaining the
accepted plate pocket and gate cut. The Hyundai rear is retained as a second
comparison: its broader painted bumper and horizontal reflectors differ, so
this treatment does not claim to match both. On the 1824-pixel Corolla image,
the body spans approximately x = 356…1470 at its rear shoulders. A reflector
spans approximately 13 × 135 pixels, implying roughly 21 × 217 mm using the
1790 mm body width. These are projected class estimates, about ±20 mm in
height and ±5 mm in width, not a parts drawing. The original H120 guide is
24 × 200 mm before projection onto its own curved corner. The checkpoint
report measures the resulting mesh separately.

White studio backgrounds provide the neutral for both makes' comparisons;
unit RGB balance is retained. No photograph supplies model vertices or texels.
The side's shoulder, rising lower hollow, wheel crowns, gate pinching, lower
hem shadow, bumper corner roll and mirror crown are judged in the unchanged
calibrated pairs and procedural reflection bands.
