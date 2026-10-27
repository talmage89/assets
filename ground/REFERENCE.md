# Dimensional decisions

This is an original low-speed local street system, assembled from municipal
construction conventions rather than a copy of one town's complete civil plan.
Source URLs, authors and usage rights are in [refs/SOURCES.md](refs/SOURCES.md).

| Feature | Authority | Choice |
| --- | --- | --- |
| Local residential section | Auburn 2024 sheet 5.00, street-width table | 28 ft back to back of curb; 24 ft asphalt. **27 ft face to face**, after the 6 in curb backs; do not mislabel 28 ft as clear curb-to-curb width |
| Crown | Auburn sheet 5.00, 1/4 in per foot | 1:48 each side, 6.35 mm tie-in at asphalt/gutter edge; center 82.55 mm above gutter flow line |
| Curb and gutter | Auburn sheet 5.04 for envelope/pan; lead's visual-revision brief for barrier profile | 24 in total width, 18 in exposed pan, 6 in rise, 6 in back. Revised to 13 mm tool radii and a 1:12 battered face instead of Auburn's large rounded nose; only exposed skin is exported |
| Sidewalk | Auburn sheet 5.00, sidewalk notes | 5 ft clear width; 5 ft control-joint pitch, nominal 1/8 in saw width; 1% toward street |
| Parkway | Windsor CO Division I, revised 2019, 1.12.B.3 | 6 ft reserved planting strip; no lawn/soil textures delivered in this run |
| Curb return | Windsor Table 1.13.1 lists a 15 ft local-residential return | 15 ft face radius, chosen for a quiet intersection; raised Auburn curb is combined with that plan radius rather than claiming a whole Windsor standard assembly |
| Curb ramp | Access Board PROWAG R304/R305 | Perpendicular run through 6 ft strip, 5 ft width plus flares; full 5 ft sidewalk landing; no single diagonal ramp dumping into the center of the intersection |
| Warning | PROWAG R305 | 60 x 24 in; 1.1 in base domes, 60% top diameter, .2 in height, 2 in square pitch. Domes transfer to a tangent normal field rather than thousands of small triangles |
| Depressed drive curb | Auburn driveway 5.08 | 10 ft clear depressed span, 5 ft transition each side, 1.02 in remaining nose; apron and driveway surface follow in next run |
| Centerline | FHWA 2023 MUTCD 3B.02 | Omitted for this low-volume local street. A centerline is optional here; the warrant for a 20 ft urban arterial/collector at 6000 ADT does not require painting all residential locals |
| Crossing | MUTCD 3B.19 and 3C | 6 ft crosswalk band, 18 in white longitudinal bars with 18 in gaps; 12 in stop line at least 4 ft before nearest stripe, on incoming right-hand lane only |

The 6 in snap subgrid is our modular design choice. The road module is 20 ft
long, curb module 10 ft, and sidewalk module 5 ft. The intersection radius
centers are 28.5 ft from its center along both axes. Surface normals at its
ports analytically continue the straight road's crown.

The family is authored at zero longitudinal grade. A real civil layout needs
longitudinal fall, inlets and sag points; neither the level sample assembly nor
its checks certify drainage. Skin meshes intentionally omit buried pavement,
footings, backs concealed by future terrain, bottom faces and internal end caps.
They are ground surfaces, not watertight standalone solids.

Photographs set the material/wear target: oxidized mineral asphalt, sparse
repairs, broom concrete, toe sediment and tactile-panel wear. Photo calibration
uses assumed nominal dimensions, clearly separate from the cited measurements.
It compares finish and framing, and does not independently survey the real sites.

## Street completion

- **Drive concrete:** Portland Bureau of Transportation's March 2018 Sidewalk
  Repair Manual, contraction/expansion-joint section and Appendix VII, informs
  joints between pours, thickness changes and continued sidewalk scoring. The
  existing Auburn curb cut controls the apron toe: 25.908 mm at the 10 ft low
  span, transitioning over 5 ft wings. Our apron tapers from 20 ft to 10 ft
  through the existing 6 ft planting allowance. Private slabs are original
  10 × 10 ft panels on a mild 0.4% outward grade. Hidden concrete thickness is
  omitted from these surface skins; a vehicle crossing would use the drive's
  concrete section rather than a thinner pedestrian-only section.
- **Lawn:** the used Ohio street photo and Lawton's Illinois inlet photo set
  color, thin-patch and edging targets. A 10 × 10 ft tile is an authored
  coverage choice, with millimetric original blade strokes, clover and soil.
  Perimeter grass is original alpha geometry on the trim atlas; no reference
  pixels are sampled into any map.
- **Inlet:** Lawton's photograph shows the common US combination of a slotted
  grate and an open cast curb hood. Plymouth MN's STM-2 plate specifies a
  nominal 1 in local depression at the curb. Our 890 × 375 mm grate and
  800 mm-wide throat adapt that construction to this family's narrow 18 in
  gutter pan and 6 in curb. The pan is lowered 25.4 mm; the grate top sits
  25.4 mm below the flow-line datum, flush with the depressed pan/frame. Its 95.4 mm
  clear throat is a measured authored fit, not a claimed dimension of the
  casting named in the municipal drawing. It is not a hydraulic capacity
  certification. The curb casting follows the existing 1:12 battered face and
  rounded top exactly; its lower face-plate edge is 70 mm above flow-line
  datum. Original 25 mm transverse cast bars have 9.6 mm slot necks and
  12 mm chamfered mouths (US Access Board §302.3 supplies the half-inch
  limiting-opening convention). The shallow modeled basin has no buried outlet/pipe network.
- **Manhole:** the manufacturer's Construction Castings catalog, printed p.52,
  lists the 24 in lid / 25 in upper frame / 1.5 in lid-thickness convention.
  We retain those nominal sizes with an original grip pattern and fictional
  ALDERVALE / SANITARY lettering. The visible top flange/bevel extends to
  641 mm; buried frame foundations are omitted. The irregular nominal
  1.12 m resurfacing cut is an authored maintenance event, and is shared by
  the separate patch ring and the actual hole in the replacement road module.
  Daderot's CC0 cover photos inform cast grain, polished lands and dirt/rust
  around a frame, rather than a copied surface pattern.

All new source URLs, authors, licensing and retrieval limits are in
`refs/SOURCES.md`. There is still no claim of full compliance with a single
municipality's complete street standard.
