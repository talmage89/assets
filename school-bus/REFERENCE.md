# C75 measurement and construction basis

The vehicle is an original late-2000s Type C, presented as a district bus in
service around 2012. Morrow, C75, the three districts, fleet numbers and plates
are fictional. Neither a manufacturer's styling nor a reference contour is
copied. References remain in the ignored `refs/` folder; their original authors,
licenses and retrieval URLs are in [SOURCES](refs/SOURCES.md).

| Package datum | Published basis | Original design target |
| --- | --- | ---: |
| Exterior steel body width | Blue Bird AM-VIS-0710 brochure, dimensions table | 96 in / 2.4384 m |
| Conventional wheelbase | Same table, 72/77 student package | 273 in / 6.9342 m |
| Tire designation | Same brochure | 11R22.5; 1.046 m circular loaded envelope |
| Capacity class | Same table, 72–77 children | 25 three-place benches / 75 children |
| Total length | Within the brochure's 289–499 in range; brief asks about 40 ft | 480 in / 12.192 m bumper to bumper |
| Roof height | Brief's nominal 10 ft 6 in; optional equipment adds height | 126 in / 3.2004 m steel roof |

The 2018 Thomas C2 sheet cross-checks the available conventional-wheelbase
range only. It does not date or style this design. Exact cowl, hood, fender,
track, overhang, bay, door and seat positions are original construction
estimates. These must not be described as manufacturer measurements.

The [2010 NSTSP](https://www.msbo.org/sites/default/files/NationalSpecs.pdf)
and [2015 NSTSP](https://www.nasdpts.org/NSTSP-Documents) body/chassis sections
guide yellow/black livery, lettering, corrugated rails, step arrangement and
the crossing gate. They are recommendations unless locally adopted. The
modeled 104mm rail exceeds the 4-inch recommendation; first tread is about
354mm above ground including its wear layer, followed by 210mm rises. The
deployed crossing loop extends more than 70 inches. Glyph height is measured
from our generated bitmap's active bounds, not its transparent/substrate box.

Period federal source: the **2012 CFR**, rather than a current regulation
silently applied to an older vehicle. All six original PDFs are registered.

| Standard | Visible consequence in the model |
| --- | --- |
| [111 — mirrors](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-111.pdf) | Paired flat/convex side mirrors and separate curved crossview mirrors on supported brackets. Field-of-view compliance is not certified. |
| [131 — pedestrian devices](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-131.pdf) | 500mm-across-flats red octagon, white border and two red lamps, both readable faces, true side pivot. |
| [217 — emergency exits](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-217.pdf) | Rear exit, forward-hinged left side exit and two roof openings with separate lids; one bench omitted at side exit. |
| [220 — rollover](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-220.pdf) | Continuous roof section, header and post rhythm. No structural load test is simulated. |
| [221 — joints](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-221.pdf) | Sheet lap joints, returns and fastener patterns. No joint-strength result is claimed. |
| [222 — seating](https://www.govinfo.gov/content/pkg/CFR-2012-title49-vol6/pdf/CFR-2012-title49-vol6-sec571-222.pdf) | Forward padded benches and front barrier. 39-inch cushions support the period three-child occupancy calculation; no seat crash test is simulated. |

The 2011 service-side photograph is a different length/package; its camera
fit deliberately retains wheelbase/overhang mismatch. The front photograph's
Commons date and EXIF conflict. The rear shows a 2010 vehicle photographed in
2022, so its wear is older than this checkpoint's target. Three paired views
are class comparisons, not claims of a measured replica. Neutral assumptions,
RGB gains and residuals are recorded in `build/balanced/white-balance.json`
and `build/calibration.json`. Reference imagery is never used by the builder,
marking generator or baker.

The native school sockets reserve **11m** vehicles and sit **12m** apart. A
40ft bus fits one position along the straight curb but needs greater center
spacing for a second one. `build/school-fit.json` reports actual imported lane
ray hits and bumper spacing; the school is an unchanged presentation input.
