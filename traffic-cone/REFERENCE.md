# Traffic cone: measured references

The controlling [OrangeGear technical sheet](https://orangegearsafety.com/images/products/cones/specs/DataSheet-OG2810SO64B.pdf)
is a 28-inch, 14-inch-square-base slim PVC cone. Geometry is authored from the
published dimensions; drawings and photos are not traced, imported or sampled
into the asset. This is an original unbranded variant, not a manufacturer replica.

| Feature | Published reference | Authored |
| --- | --- | --- |
| Overall height | 28 in | 711.2 mm |
| Base width/depth | 14 × 14 in | 355.6 × 355.6 mm |
| Lower tapered body diameter | 7.5 in | 190.5 mm near the bottom, above the flared foot |
| Upper reflective collar | 6 in, 4 in below top | Z 457.2–609.6 mm |
| Gap between collars | 2 in | 50.8 mm |
| Lower collar | 4 in | Z 304.8–406.4 mm |
| Wall gauge | 0.1 in | 2.54 mm-class tapered shell |
| Grip | 1.5 in top, 2 in lower shoulder, .75 in opening | 38.1 / 50.8 / 19.05 mm |

The 25.4 mm black base thickness, 16 mm rounded corners, bore, flared foot and
waist profile are authored construction estimates. The base and body have real
open passages, so cones can stack without a solid internal cap. This is fixed
geometry, not a deformable crush simulation. Its origin is at the base footprint
center on the ground, Blender +Z up / −Y front, glTF +Y up / +Z forward.

The sheet's embedded 182 × 435 product photograph is used for both source and
exported-GLB profile comparisons. Its small, soft base corners do not provide
precise camera constraints, so the camera fits the measured body/grip landmarks
and leaves the independent 14-inch base dimension intact. The illustrated base
looks narrower than that nominal envelope; the asset retains the dimensioned
specification. Lens and residuals are estimates, not recovered EXIF.

The source uses original PVC mould grain, eight fine grip flutes, two cut-edge
foil/collar layers and their rear overlap seam. Wear follows road splash at the
lower skirt, ground-drag on base edges, handling at the grip, and nicks at exposed
collar edges. `WEAR` changes these layers; noise only breaks causal masks.
Orange fluorescence and true retroreflection are approximated by standard glTF
PBR response; no emissive cheat or photographed texture is used.

All extracted `refs/sheet-*.jpg` images remain reference material under the
manufacturer's copyright, credited in [refs/SOURCES.md](refs/SOURCES.md).
The site's small cone icon was examined and rejected as a photograph.
