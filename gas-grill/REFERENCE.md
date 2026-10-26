# Cinder Works — Field 3 / modeling specification

An original three-burner American LP grill, with a porcelain-enamel hood, cast
end cheeks and firebox, brushed stainless control fascia and side shelves, an
open powder-coated steel cart, two 180 mm wheels and two fixed feet. A separate owner-supplied
tank fits outside the right cart rail beneath the shelf. The grill supplies the
hanger, cradle, regulator, coupling and hose; it does not supply a cylinder. No side
burner, cabinet, electronics or brand-specific accessories. This configuration
keeps the construction and tank visible and uses the triangle budget on the
parts that define an everyday backyard grill.

The dimensional reference is the **2018–2024 Weber Spirit II E-310 US layout**,
not its differently sized 2025 successor. The asset's hood profile, handle,
frame details, badges, control graphics and markings are our own design.
Reference files, authors, license status and direct URLs: [SOURCES](refs/SOURCES.md).

| Feature | Reference | Asset target | Basis / uncertainty |
| --- | --- | --- | --- |
| Closed width | 52 in | 1320.8 mm | US catalog p12, extended shelves |
| Closed depth | 27 in | 685.8 mm | US catalog p12, extremities |
| Closed height | 44.5 in | 1130.3 mm | US catalog p12, hood crown |
| Open height | 57 in | about 1448 mm | US catalog; hinge stop adjusted to original hood profile |
| Primary area | 424 in² | 0.27355 m² | US catalog; 610 × 448.45 mm grate envelope |
| Warming rack | 105 in² | 557 × 121.62 mm | US area, manufacturer metric width; nominal bounding area |
| Burner count | 3 | 3 longitudinal tubes + crossover | Catalog + owner/exploded manual |
| Grate height | about 880 mm | 887 mm | Estimated from front photograph, ±15 mm |
| Shelf top | about 865 mm | 865 mm | Estimated from front photograph, ±15 mm |
| Knob centers | about 205 mm pitch | 205 mm | Ratio to calibrated 1320.8 mm front width; ±8 mm |
| Main frame | about 650 mm wide | 664 mm | Photo proportion; ±15 mm |
| Wheels | about 180 mm diameter | 180 mm | Photo proportion; ±10 mm |

Construction: hollow sheet hood, actual inner wall and rim; cast cheeks with
hinge bosses and rear vent gap. Two removable cast grates above five folded heat
tents (three cover burners), three stainless tubes and a rear crossover. Sloped
firebox floor drains into a sliding grease tray and small catch pan. Frame rails
have folded edges, bolted joints and plastic end feet. A spring hanger engages the separate canonical tank collar; a lower cradle
retains its foot ring, and the grill-owned regulator and hose connect its
valve outlet to the manifold.

Wear is controlled by one `WEAR` scalar (default 0.35): slight enamel waviness,
fine stainless brushing, localized cooked-on grease on grates/tents, soot inside
the hood/firebox, settled dust on the bottom shelf, scuffed wheel shoulders.
The upper exterior stays cared-for. No uniform rust or decorative edge outlines.

Coordinates: meters, +Z up, front −Y; origin at the center of the cart footprint
on the ground. Lid pivots about X at the rear rim. Knobs about local Y; wheels about Y.
The external tank origin is the bottom center of its foot ring. `tank_socket`
places that origin at world (451.5, 13, 198) mm, yaw +50° about Blender Z.
The canonical tank measures 312.2 mm diameter × 468.0 mm high; collar 175 mm,
foot ring 210 mm. Its outlet face is (0, −41.9, 423.5) mm, axis −Y. The coupling
meets the transformed face on axis. The hanger lifts the underside of the
canonical collar handle lip at (−94, 0, 436) mm; the cradle and rubber pads touch
the actual foot-ring radius. This supersedes the earlier Worthington dimensions.

One 2048 BaseColor / Normal / ORM set, baked at 4096, and at most 20,000 grill
triangles include all hose/regulator/hanger geometry. Six connected hose bones
are an owner-approved exception to the default rigid-prop convention. No tank
texture set or tank/valve geometry is generated. The optional canonical GLB is
loaded only by the dedicated checker and fit-check render, never the build,
UV, bake or export. Absence skips those optional checks clearly.


Current photographic comparisons use `grill-three-quarter.jpeg` and
`open-photo.png`. `src/photo_matches.py` lists measured world/pixel anchors.
The kit fits camera position, angle, roll and estimated lens, retaining residuals
in JSON and review sheets. No source EXIF is available. Fit errors are about
6.5 / 18.1 pixels at the original crops. The historical third comparison with
`tank-connected.jpg` is retained in REVIEW.md; the photograph now supplies only
regulator/hose/hanger construction reference, since the canonical tank supersedes
our former cylinder. These are comparisons, not identical-geometry claims.

The open reference has regional GBS grates; the US specification retains two
straight sections. The historical connection photograph shows the scale on the other image side;
our outside-right spring scale follows this cart's mounting arrangement. The
extended-table envelope is 1320.0 × 685.8 × 1130.3 mm. Grill-owned hardware
stays within it. Small deviations in nominal cooking area
reflect the cast perimeter frames and assembly clearance.


Construction gauges are authored manufacturing estimates, not published service
measurements: 2 mm formed cart steel, 1.8 mm hood steel, 1.4 mm shelf/fascia
sheet, and a 4–7 mm cast vessel wall. They provide credible hems, joints and
inside clearances without claiming a manufacturer CAD reconstruction.
