# Skateboard delivered surfaces

One three-map set per age: 4096 Cycles source bake, 2048 delivery. BaseColor is
sRGB; tangent Normal is OpenGL +Y; ORM is occlusion/roughness/metallic. At three
8-bpp compressed maps with full mip chains, each state costs **16 MiB**. Loading
new, season and beat together costs **48 MiB**. Three material response classes
share the same three images: opaque manufactured surfaces, clear-coated wood
and ink, and mildly transmitting urethane. No separate hardware texture set.

Packing uses measured priority/density bands. Deck faces retain the most total
area; head drives, bearing faces and wheel lettering receive higher local
priority than concealed mounting surfaces. Narrow UV projections avoid folds
at annular casting seats. The independent delivery audit gates overlap, outside
and degenerate triangles, density, image sizes and normal-vector lengths.

`src/graphics.py` draws every source image with installed DejaVu fonts found
through `kit/fonts.py`. The sheet contains three distinct original fictional
designs: **Ditchlight** orbital contours, **Kilnline** fired-brick/lightning, and
**Static Orchard** interrupted growth/radio forms. No real logo, artwork or
reference pixel is used. Seed selects a panel; the default Ditchlight design
ships here in three ages. Wheel lettering is Kilnline; truck marking Crossway;
the grip carries no center label.

`src/lookdev.py` uses stable rest-position attributes, so material masks remain
attached to moving parts and survive projection isolation. The source retains
rounder drive machining, casting bores and 64-sided axles. Temporary per-part
owners isolate thin washers/bushings and other close neighbors during baking;
those owners disappear in export. The same packed images serve all rigid nodes.

Manufacturing detail includes silicon-carbide aggregates and fine facets at real submillimeter scale,
a filed score line measured from the actual grip/wood border, seven maple
bands with two cross-grain veneers, thin printed ink/clear coat, cast grain and
parting witness, steel machining, and 24-TPI axle-end threads. Shipped texel
size limits the smallest grit and lettering in extreme macro views; geometric
drive mouths preserve their own hard shadows.

- **New:** dark fresh grip, clean original ink and lacquer, maple rails, cast
  aluminum, amber bushings and ivory satin wheels.
- **Season:** parallel transverse boardslide passes abrade clear coat, expose the white ink base and then maple in the belly;
  rear-kick dragging abrades the tip; localized rail impacts chip upper veneers.
  Front-bolt/rear-pocket planted-foot zones collect irregular shoe dirt and polish
  the grit. Toe dragging frays the filed trim. Downward-facing hanger/axle-housing
  surfaces brighten and score; the deck-facing alloy stays cast gray, with dirt
  in its recesses. The kingpin nut also grinds. Urethane sidewalls yellow while
  the axial riding band becomes brown with grime; the sidewall print abrades.
  Biased turns cone the tread while one edge remains grounded.
- **Beat:** stronger belly loss, a thinner razor tail, two attached lifted maple
  splinters, a ribbed shoe-goo patch, a torn nose-grip area and deeper wheel
  staining/coning, plus a 1.4 mm planar skid flat on the front-left wheel using
  existing vertices. These stay at the corresponding contact/repair locations.

Reference colors are compared after balancing concrete, or the loose truck's
zinc washer, toward neutral. Mixed light and unknown photographic exposure
remain uncertainties. `REVIEW.md` logs color/value before finer critique.
Source and exported-GLB photo pairs distinguish material/form issues from bake
loss. Photographs never enter the source shader or texture generator.
