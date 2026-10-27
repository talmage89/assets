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
| Ground clearance | GM MY2018 4WD crew short-box guide p19, 226 mm at base curb weight | 226 mm eventual underbody target; **not measured or built at this gate** |
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

The tire is lightly flattened 12 mm at the ground. Ford's p16 tire table lists
a 14.33-inch minimum static loaded radius for this size; this checkpoint's
395.35 mm hub height represents a deliberately lighter parked load, **not**
a reproduction of that minimum-load condition. Tire section and contact are
measured independently in `build/form-check.json`. The static contact patch is
not yet a rolling deformation solution.

## Photographs

Sources, authors and licenses are in [refs/SOURCES.md](refs/SOURCES.md).
The final comparison pair uses Kevauto's April 2019 front/rear photographs of
a 2018 crew-cab 4x4. Earlier black Ford and gray Ram photos informed proportions,
body construction and the critique passes. The Ram is a cross-design check,
not a specification source for the primary envelope. Final photo matching
fits a lens/pose using inspected wheel, roof and bed landmarks. Shape differences,
landmark uncertainty and photographic distortion remain in the published
residuals; calibration is not a photogrammetric reconstruction.
