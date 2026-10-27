# Alder C150 detail / look-dev gate

Scope: the three accepted-form corrections, optimized detailed source, original
procedural finishes and source Cycles photo critique. Stop before UV/bake/export.

## Budget committed before detail

| Group | Working allocation |
| --- | ---: |
| Body panels, bumpers, bed | 25,000 |
| Four wheels / tires / brakes | 12,000 |
| Lamps / grille / mirrors / trim / markings | 6,500 |
| Interior | 5,000 |
| Underbody including spare | 3,000 |
| Glazing | 1,000 |
| Construction and silhouette reserve | 7,500 |
| Working finished target | 60,000 |
| Absolute cap | 70,000 |

Reduce redundant flat sheet grids first; keep station rows at the shoulder,
arch lip, roof rolls and panel silhouettes. Tire tread, sidewall type, grille
perforations, brake drill/vent detail and small hardware use scripted height
fields / original font sheets for later normal baking. No bake at this gate.

## Delivery material plan

One 2048 BaseColor / Normal / ORM set shared by paint presets
Porcelain, Carbon, Aluminum, Graphite and Atlantic. A paint color factor changes
without allocating images. Paint islands encode absolute contamination in
BaseColor RGB and remaining paint coverage in alpha. The paint shader computes
`factory_tint * coverage + contamination`, preserving the same brown dust and
gray chips across all five colors. A plain glTF base-color multiply cannot do
this: the delivery gate must implement and verify the engine paint decode and
its GLB fallback. Source shaders already expose both bake channels. No extra
map is required for this packing. Four delivery surfaces: tintable coated paint,
opaque trim/interior, glass, and lamps. Source manufacturing materials and
script-generated marking/relief sheets are baking inputs, not extra delivery
sets. Compressed three-map memory with mipmaps: about 16 MiB shared by all five
colors. The factor/coat/export policy still needs delivery-stage implementation
and verification; no GLB is claimed here.

## Form corrections

- A ridge with its maximum at the arch boundary and an outward slope that
  decreases continuously into the side over 150–250 mm; no flat flare plateau.
- Lamp lens and opening share the fender's corner boundary and tangent, inset
  into a housing rather than an outboard block.
- A broad monotone lower tuck; aligned cab/bed lower edges, no tight reversing
  lower-section fold.

## Review

Retain the clay/stripe form diagnostics. Source Cycles: front/rear 3/4, side,
front-end detail, wheel detail, lit state and all five paint factors. Use outdoor
used-truck photographs for calibrated color/value-first critique. Report
geometry measurements separately from serialization or camera projection checks.
