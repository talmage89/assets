# Alder C150 / cars family

An original late-2010s full-size crew-cab 4x4 pickup, on 275/65R18 tires.
**Look-dev round 2 checkpoint. Stopped before UV, bake and export.**

[Contact sheet](renders/lookdev/contact.jpg) ·
[Front](renders/lookdev/front_three_quarter.jpg) ·
[Rear](renders/lookdev/rear_three_quarter.jpg) ·
[Side](renders/lookdev/side.jpg) ·
[Front detail](renders/lookdev/front_detail.jpg) ·
[Wheel](renders/lookdev/wheel_detail.jpg) ·
[Used-truck front pair](renders/lookdev/aged_front-pair.jpg) ·
[Used-truck rear pair](renders/lookdev/aged_rear-pair.jpg) ·
[Five paints](renders/lookdev/five-colors.jpg)

These are Cycles OptiX renders of the high source, with original procedural
finishes and generated markings. The separate game-density source supplies the
budget and construction measurements. Images remain ignored build outputs;
there are no committed preliminary docs images or delivery assets.
[REVIEW.md](REVIEW.md) records the rejected passes and remaining weaknesses.

## Dimensions and form

[REFERENCE.md](REFERENCE.md) separates published dimensions from authored
construction estimates. [refs/SOURCES.md](refs/SOURCES.md) credits the photographs
and manufacturer documents. The envelope/wheelbase follow the Ford MY2018
short-bed crew-cab specification, cross-checked against GM and Ford body-builder
data; the sculpting, lamps, grille and badges are original.

| Measurement | Measured game source |
| --- | ---: |
| Length | 5889.46 mm; target 5890.26, 0.80 mm tessellation difference |
| Body width, excluding mirrors | 2029.57 mm; target 2029.46 |
| Height | 1960.88 mm |
| Wheelbase / track | 3683.00 / 1716.00 mm |
| Clear bed floor length | 1704.34 mm |
| Door seams | 4.500 mm, 14 sampled edge positions per side |
| Cab / bed separation | 16.000 mm |
| Lower door-to-sill reveal | 4.924 mm, eight samples per side |
| Tire width / top / ground | 275.00 / 802.70 / 0.00 mm |
| Arch crown / tire-top clearance | 893.00 / 90.30 mm |
| Lowest underbody surface | 226.00 mm above ground, measured on differential |
| Full width including mirrors | 2458.72 mm |

The three form corrections preserve those dimensions. Round 2 raises only the
hood nose by 35 mm over its first 420 mm to meet the taller surround; the body
envelope, stance and side fields stay fixed. The flare's maximum is
at the arch boundary and falls into the side, rather than making a closed
panel-centered bump. Actual surface rays 10 mm above the arch crown measure
33.28 / 33.24 mm front/rear draw, with more than 2 mm of draw persisting to
165 / 180 mm above the opening. The broad lower tuck is monotone; cab and bed
share the 578 mm lower skin boundary. Protective headlamp lenses follow the
same corner seat and end 2.00 mm inside the fender.

Earlier form evidence: [corrected stripes](renders/lookdev-form/stripes_side.jpg),
[clay/stripe pairs](renders/lookdev-form/match_front_stripes-pair.jpg),
[side overlay](renders/lookdev-form/side-overlay.jpg) and
[form contact](renders/lookdev-form/contact.jpg) remain separate diagnostics.
The earlier axle-scaled overlay registration is retained. Its known fixed-envelope
overhang mismatch and roof-height differences remain documented in REVIEW;
this detail stage does not refit the dimensions to another photograph.

The body still uses authored Hermite sections, shared surface derivatives and
explicit curvature stations. Flat regions have fewer rows; arch edges,
shoulders and roof rolls retain them. Closed sheet thickness now uses normal
offsets: even-offset miters produced spikes at sharp, narrow returns. A new
measurement checks every paired sheet vertex against its specified gauge.

## Construction

- Single projector optics and reflector cups sit behind clear, wrapping
  polycarbonate lenses and sealed black housings. An original angular running
  signature (16 mm light guide), amber markers, vertical red rear optics, reverse
  windows and upper brake lamp have an independently rendered [lit state](renders/lookdev/lamps_lit.jpg).
- A tall hood-following surround and three recessed chrome lamellae sit over
  an original diamond relief pattern. Actual bar-front recess is 79.00 mm;
  sampled hood-to-surround surface gaps are 4.75–7.78 mm.
  Formed bumpers carry recovery loops, a recessed fictional plate, rear step
  pads, a hollow 2-inch hitch receiver and chain eyes. Cowl wipers, tapered
  painted mirror caps, black glass cases and inset bezels on substantial
  door-sail arms, bowed handles, a hinged fuel flap, fictional Alder badges and B-pillar blackout complete the trim.
- The lined bed has inner wheelhouses, four supported tie-down loops, a separate
  tailgate and pull handle. Cargo scuffs follow the floor, rather than covering
  the whole truck with noise.
- Each 18 × 7.5-inch wheel has a deep barrel, six continuous cast Y spokes,
  six hex lugs, center cap, stepped rotor hat, concentric friction ring and
  stationary caliper. Carcass geometry establishes the real tire size, bulge
  and parked contact. Tapered shoulder lugs break the silhouette; central tread,
  sipes and fictional sidewall type are shader height inputs for the later normal bake.
- Five seats, a formed dash, original gauges/display, steering wheel, console,
  door cards, headliner and stowed visors form the [interior](renders/lookdev/interior.jpg).
  Boxed rails, spring packs, shocks, wishbones, knuckles/spindles, axle,
  drivetrain, tank, exhaust and a suspended spare fill low views. The skid is a formed 4 mm sheet on
  measured frame supports, and driver controls sit at +X.

Static measurements give **21.20 mm** axial separation between caliper and
spoke envelopes. Caliper-vertex to barrel-surface samples are at least
**9.66 mm** apart. Actual bearing/hub and spare-hanger/crossmember surface
intersections establish those supports; they are intended assembly contacts.
`build/detail-check.json` and `detail-high-check.json` preserve the measurements,
source hashes and limitations. They do not certify full steering or hinge sweeps.

## Triangle budget

The allocation was written in [LOOKDEV_PLAN.md](LOOKDEV_PLAN.md) before detail.
The current game-density source is **59,266 triangles**, with 734 below the
60k round-2 limit (now enforced by both source budget checks). Each
tire/wheel/brake corner is **3,722 triangles**. The extra underbody allocation carries the spare,
suspension and actual hub supports. Source objects remain separate for building;
static batches will be joined during delivery preparation.

| Group | Triangles |
| --- | ---: |
| Body panels, bumpers and liners | 26,420 |
| Four wheels, tires and brakes | 14,888 |
| Lamps, grille, mirrors, trim and bed hardware | 7,322 |
| Interior | 4,792 |
| Underbody, including spare | 4,548 |
| Glass, including protective headlamp covers | 1,296 |
| **Total** | **59,266** |

The high source is 203,650 triangles. The current high/game blend files are
approximately 2.35 / 1.03 MB, ignored and rebuildable; serialization sizes can
vary. There is no GLB or shipped texture set. Per-mesh/category counts are in
`build/form-check.json`; the general kit audits check both source densities.

## Materials and five colors

The source uses **33 manufacturing materials** and six original marking/relief
sheets, generated with Pillow and installed open-license Noto Sans. No reference
image enters any shader. Meter-scale rest positions keep splash attached to
moving panels. Dilute road film fans aft of the wheels and stays low on the
rockers; tailgate-top and bed-corner dust, leading-edge chips, highlight-only
wash swirls, localized brake dust, chrome water-spot rims and bed scrapes have
separate masks. The mid-tailgate streaks and all-over chrome film are removed.
Film reduces clear-coat response where it sits. Default wear is `.65`, calibrated
as a four- or five-year daily driver, rather than a mud-covered truck.

Porcelain, Carbon, Aluminum, Graphite and Atlantic change one factory tint node
and the paint's metal response. Clear coat, textured plastic, rubber, chrome,
clear/privacy glass, frit and unlit/lit optics are procedural source shaders.

Delivery is planned as **four surfaces**: coated paint, opaque trim/interior,
glass and lamps. The original brief explicitly permits the fourth surface for
independent paint tinting. All five colors share one **2048 BaseColor / Normal /
ORM set**, about **16 MiB compressed with full mipmaps** (three 8-bpp maps),
about 64 MiB as uncompressed RGBA8 with mips. Five colors do not multiply this
allocation.

Paint islands reserve BaseColor RGB for absolute contamination and alpha for
remaining paint coverage: `tint * coverage + contamination`. Both source bake
channels exist. This preserves brown dust and gray chips across the presets;
a plain glTF base-color multiply cannot. The delivery gate still needs the
engine paint decode, coat/glass/emission handling, a GLB fallback and re-import
verification. This is a material plan, not a shipped shader or memory measurement.

## Coordinates and pivots

Meters, Blender +Z up, front −Y. `AlderC150` sits at the bumper-footprint center
on the ground. Source pivots retain their names and measured world locations in
`build/detail-check.json` and the kit audit.

| Nodes | Local axis and authored range |
| --- | --- |
| `Door_FL`, `Door_RL` | Z, 0…72° |
| `Door_FR`, `Door_RR` | Z, −72…0° |
| `Hood` | X, −62…0° |
| `Tailgate` | X, −90…0° |
| `Wheel_FL/FR/RL/RR` | X, spin; parked loaded carcass needs rolling deformation |
| `Steer_FL/FR` | Z, ±35° source proxy; caster/SAI remains a delivery task |
| `Mirror_L/R` | Z, −65…0° / 0…65°; children of their doors |
| `Fuel_Door` | Z, 0…95° |
| `Wiper_0/1` | Tilted local Z, 0…80° |

Calipers follow the front steering node or fixed rear axle; they do not spin.
Full assembly sweeps, rolling tire behavior and kingpin geometry remain
uncertified at this source checkpoint.

## Rebuild

```sh
make -C cars                         # refs, source models/checks, Cycles views,
                                    # used-photo pairs, five paints, review sheets
make -C cars check                   # source geometry, dimensions and static fits
make -C cars preview                 # shorter source render pass
make -C cars form-diagnostics PASS=lookdev-form WIDTH=1200
```

All Cycles work uses the shared kit GPU lock; the kit selects the available
compute backend. The default pipeline
explicitly excludes finalize, bake and export. The full source checkpoint was
built with `make -C cars WIDTH=1500 SAMPLES=80`; its repo-root log is
`build/cars-lookdev/round2-final.log`. Tonal data, geometry/paint masks,
calibration diagnostics, source hashes, PNG originals and JPG/contact derivatives
sit beside the renders. The five-year Ram camera RMS is 18.90 / 21.20 native photo pixels; Ford
supplemental RMS is 43.84 / 24.73 px. The independent Blender projection check
agrees within 0.003 px. Cropped EXIF framing and class wheel/tire differences
remain disclosed calibration uncertainties. Those numbers
measure camera registration, not design agreement or material realism.

Shared additions are documented in [kit/README.md](../kit/README.md): optional
reduced tire profiles and vehicle source finishes on the existing Nodes API,
including opt-in refined daily-driver finishes and a turned-rotor shader.
Existing callers keep their defaults. Nothing is baked, exported or published
by this checkpoint.

## Round 2 evidence and limits

Four new photo critique passes are logged at the start of [REVIEW.md](REVIEW.md).
The final source checkpoint repeats every view and all five paints. Each photo
pair has its own documented daylight condition: clear sun for the dated Ram,
diffuse overcast for the supplemental Ford. Lighting geometry and irregular
foliage are original generated reflection equipment, excluded from the asset.
Glass retains smooth reflection over tinted transmission; the interior remains
visible. Paired inner/outer normals prevent faceted exit refraction, with a
measured maximum paired-normal deviation below 0.07 degrees at both densities.
The matching cameras and their disclosed registration uncertainties are unchanged. Fonts resolve by exact Noto Sans family/style using `kit/fonts.py`;
there are no machine-specific font paths in this family.

The synthetic surroundings remain less complex than the photographed parking
lots and street, and unlit lamp internals remain simpler than production optics.
The Ram match remains darker/more neutral than its photograph. Fine tread,
type and sparse wear still need a baked 2048 review. This gate
certifies source geometry and look-dev only. No UV/bake/GLB claim is made.
