# Street signs: dimensional reference

The original assembly uses a [30-inch R1-1 STOP](https://highways.fhwa.dot.gov/sites/fhwa.dot.gov/files/2022-06/fhwasa1108.pdf)
(FHWA Intersection Safety, US government) and [MUTCD 11th edition](https://mutcd-dr.fhwa.dot.gov/pdfs/11th_Edition/mutcd11thedition.pdf)
Sections 2A/2B/2D. This is a residential ≤25 mph visual asset, not a certified
traffic-control product. Installed STOP bottom is 7 ft / 2133.6 mm, its regular
octagon is 762 × 762 mm and 2 mm thick. Plate center is 2514.6 mm above grade.
The white/red shape is authored mathematically, never traced from a sign image.
STOP capitals occupy 254 mm height; installed open DejaVu Sans Condensed Bold
substitutes for the highway alphabet, with original graphic rasterization.

Two original 762 × 228.6 × 2 mm green aluminum name blades have 101.6 mm-class
capitals, lower-case legends and fictional names. FHWA's street-name research
[appendix](https://www.fhwa.dot.gov/publications/research/safety/03082/app.cfm)
records 24/30-inch residential blanks and 9-inch-high blades; exact bracket,
blade length and cast profile are authored choices. The [municipal Waco T-6](https://www.waco-texas.com/files/sharedassets/public/v/2/departments/engineering/traffic/t-6-sign-post-installation.pdf)
detail identifies a 2-inch square perforated support; the file server refuses
local PDF retrieval. The asset uses 50.8 mm square, 2 mm wall, 3000 mm exposed
post; 7.94 mm nominal perforations at 25.4 mm pitch are normal/color detail.
A 57.15 mm square anchor sleeve projects 76.2 mm above grade with a through pin.
These wall gauges, sleeve dimensions and hardware are construction estimates.

Crossed upper blades terminate at 3448.2 mm. Slotted cast aluminum saddles grip
the blades with 0.10 mm authored side clearance, and the post/stop spacers and
anchor pin provide a supported load path. `assembly-check.json` measures the
actual evaluated surfaces; its distances are not nominal constants.

The photograph by Thermidor2 (CC BY-SA 4.0, exact URL in refs/SOURCES.md) is an
older New York installation. Only its stop plate, sheeting, wear and fastening
are compared; its historic black blades, real street names, round post and
site-specific hardware are not copied. Photo pixels never enter materials.
The fitted camera uses upright EXIF-corrected image coordinates and an estimated
lens; residuals remain visible in calibration overlays.

Reflective sheeting is approximated by a low-metallic satin dielectric PBR
surface. glTF cannot encode true headlight retroreflection; an engine requiring
that response must add a view/light-dependent shader. The delivered material is
not emissive. Fading follows upper exposure; fine grime follows the lower edge.
One 1024 atlas holds all four fictional name pairs and common STOP/post surfaces.
