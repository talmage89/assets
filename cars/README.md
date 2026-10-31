# Cars family — Alder C150 and S240

The C150 pickup is delivered. The [S240 sedan](#alder-s240--sedan-form-checkpoint) is a source form checkpoint; `BODY=sedan` stops before detail and delivery.

An original late-2010s crew-cab 4×4 pickup on 275/65R18 all-terrain tires.
Five factory paints share one baked atlas and four delivery surfaces. The
body, fictional lamps, grille, badges and markings are generated entirely
from scripts; reference pixels never enter the asset.

![Alder C150](docs/hero.jpg)

GLB (`export/AlderC150.glb`) · Contact sheet (`renders/final/contact.jpg`) ·
Turnaround (`renders/final/turnaround.jpg`) · Scale (`renders/final/scale.jpg`) ·
Eevee (`renders/final-eevee/hero.jpg`) · Lit lamps (`renders/final/lamps_lit.jpg`) ·
Used-truck pairs (`renders/final-pairs/used-pairs-contact.jpg`) ·
[Critique log](REVIEW.md)

Every final view starts with a fresh import of the exported GLB and its three
embedded baked maps. The factory paint/lamp uniforms are decoded by
[src/delivery_materials.py](src/delivery_materials.py); the high source and its
procedural manufacturing shaders are never loaded for finals. View metadata,
GLB hashes, paint/geometry masks and measured tonal ranges accompany the renders.

## Dimensions and construction

[REFERENCE.md](REFERENCE.md) distinguishes published dimensions from original
construction estimates. [refs/SOURCES.md](refs/SOURCES.md) records the authors,
URLs and reference licenses. The envelope follows Ford's MY2018 short-bed
SuperCrew specification, cross-checked against GM and Ford body-builder data;
the design is fictional.

| Measurement | Actual game surfaces / pivot centers |
| --- | ---: |
| Length | 5889.26 mm; 5890.26 mm published target |
| Body width / full mirror width | 2029.57 / 2458.72 mm |
| Height | 1960.88 mm |
| Wheelbase / front and rear track | 3683.00 / 1716.00 mm |
| Clear bed floor length | 1704.34 mm |
| Door seams / cab-to-bed gap | 4.500 / 16.000 mm |
| Lower door-to-sill reveal | 4.924 mm |
| Tire width / top / ground | 275.00 / 802.70 / 0.00 mm |
| Arch crown / tire-top clearance | 893.00 / 90.30 mm |
| Lowest underbody surface | 226.00 mm, differential |
| Face sweep at x = 950 mm / rearward rake | about 121 mm / 8.00° |
| Headlamp front projection | 387 × 154 mm, tapering to 58 mm |
| Lamp corner return / developed centerline | 178 / 553 mm |

Analytic side sections share position and normal derivatives across the 4.5 mm
reveals. Stamped outer panels have 0.9 mm gauge, inward returns and arch lips;
the separate bed has inner wheelhouses, tie-downs and a lined cargo floor.
The broad grille occupies about 61% of the face width. Its 70 mm lands have a
rounded face and a real return; dark blades and original diamond relief sit
82–84 mm behind it. The surround is **satin dark chrome**, with a dim sky
reflection along the top. Mirror caps are textured black. The separate 250 mm
painted bumper has a crisp upper highlight and lower return, a plate pocket,
and a black valance with recovery hooks and intake below.

Curved lamp covers enclose a projector, broad reflector and original 16 mm
running guide. Vertical rear optics, reverse windows and a third brake lamp
have separate lit controls. Six Y spokes, deep barrels, six lugs, rotor hats,
friction rings and actual U-section calipers sit inside the wheels. Five seats,
a formed dash, gauges/display, console, door cards and headliner fill the cab.
Boxed rails, suspension, drivetrain, tank, exhaust and a supported spare fill
low views. Driver controls are at +X, behind `Door_FR`; side suffixes follow
the authored coordinate labels.

The moving meshes needed several functional corrections: a real caliper slot,
inner wheelhouse steering clearance, rear hood/cowl clearance, tailgate corner
and rail clearance, true mirror fold bearings and upward wiper sweeps. These
retain the accepted body fields, factory colors and causal wear. Static support,
gauge, brake and optical-seat measurements are in `build/detail-check.json`.

## Delivery budget

The delivery mesh is **59,838 triangles**, below the 60,000 limit. Detailed
counts are rebuilt in `build/form-check.json` and `build/export-report.json`.
Static manufacturing pieces consolidate by their moving parent; doors,
mirrors, glass, wheels and their fittings stay attached to the proper pivots.

| Source construction group | Triangles |
| --- | ---: |
| Body panels, bumpers and liners | 25,466 |
| Four wheels, tires and brakes | 15,112 |
| Lamps, grille, mirrors, trim and bed hardware | 8,412 |
| Interior | 4,856 |
| Glazing, including protective headlamp covers | 1,444 |
| Underbody, including spare | 4,548 |
| **Total** | **59,838** |

The 195,738-triangle high source is used only for baking. The shipped rigid
mesh allocation is:

| Exported part | Triangles |
| --- | ---: |
| Static body/interior/underbody assembly | 34,608 |
| Hood / tailgate | 792 / 1,098 |
| Each front / rear door | 1,792 / 1,584 |
| Each mirror | 516 |
| Each spinning wheel/tire/rotor assembly | 3,678 |
| Each front steering knuckle/caliper assembly | 176 |
| Fuel door / each wiper | 108 / 192 |

| Delivery resource | Budget / actual |
| --- | --- |
| Materials | 4: Paint, Opaque, Glass, Lamps |
| Textures | One shared 2048² sRGB BaseColor RGBA, linear OpenGL +Y Normal RGB, linear ORM RGB |
| Bake | 4096², GPU Cycles, 24 samples; linear-light downsample to 2048² |
| GLB | 11,530,736 bytes, embedded PNGs and moving hierarchy |
| Raw mesh buffers | 5,389,908 bytes; 30 mesh primitives |
| Texture GPU estimate | **16 MiB** with three 8-bpp compressed maps and full mip chains |
| Texture GPU estimate, RGBA8 | 64 MiB with full mip chains |

The GPU figures describe texture allocation after engine upload, not PNG file
size or measured renderer residency. The five paints add only uniform values. Raw mesh buffers add about 5.14 MiB
before engine packing/overhead, for roughly 21.14 MiB with the compressed maps.
The normal bake carries tread, sipes, lettering, grille relief and manufacturing
microstructure; no extra geometry is added for these details. UVs have zero
overlap or outside/degenerate triangles; density is weighted toward exposed
body panels, optics, wheels and markings, with structural undersides lower.

## Paint, wear and factory colors

![Five shared-atlas colors](docs/five-colors.jpg)

The fifth color costs no additional texture set. This delivery uses a **factory
factor over neutral coverage**, rather than `KHR_materials_variants` or five
material copies. The shared RGB is a correct Atlantic fallback. Paint-island
alpha stores remaining neutral paint coverage, so changing a factory tint in
linear light is:

```glsl
paint_rgb = max(vec3(0), base.rgb + base.a * (factory_tint - atlantic_tint));
```

This is equivalent to `factory_tint * coverage + contamination`: brown road
film and gray chips keep their colors. The five linear tints and metallic
factors live in the Paint material's GLB extras. [src/paint.glsl](src/paint.glsl)
contains the engine decode, including coverage-dependent clear coat and lamp
power. [src/delivery_materials.py](src/delivery_materials.py) implements the
same delivery operation in Blender for validation and finals.

| Preset | Linear tint | Factory metallic factor |
| --- | --- | ---: |
| Porcelain | .780 / .790 / .760 | 0 |
| Carbon | .009 / .011 / .013 | 0 |
| Aluminum | .460 / .480 / .490 | .55 |
| Graphite | .160 / .153 / .141 | .42 |
| Atlantic | .012 / .037 / .071 | .12 |

The four surfaces share the same three images. Paint has clear coat; Glass
has transmission/IOR; Lamps has an emission sampler and scalar control.
Lamp-island alpha stores each emitter's power divided by 80, independently of
paint coverage. The helper selects unlit or calibrated lit states from those
embedded values. A stock glTF viewer shows Atlantic with uniform coat and the
emission fallback; the supplied decoder enables the five paints, localized
coat contamination and individual lamp powers. No source shader is reconstructed. The Eevee preview uses an explicit thin-sheet
Fresnel/colored-transparency fallback for the stacked cover and projector panes,
reading the same embedded tint, roughness and normal maps. Cycles follows their
nested refraction; the screen-space preview approximates it. The adapter is
included in the delivery helper, and this difference is recorded in view metadata.

Default wear `.65` represents a four- or five-year daily driver: dilute road
film fans behind wheels and stays low, brake dust sits toward wheel interiors,
stone chips occur at the leading edge, cargo scrapes follow the bed floor,
dust collects in bed corners and on the tailgate rail, and water-spot rims
vary chrome roughness. These are separate physically located masks. Baked
coverage reduces the paint coat where contamination sits. Fine flake response
is filtered into the undercoat roughness/normal at the shared atlas density.

## Articulation and clearance

Meters, Blender +Z up, front −Y; glTF +Y up, front +Z. Origin is the bumper
footprint center on the ground. Ranges below are local-axis rotations from the
closed/rest transform, expressed in Blender authoring axes. In the GLB,
local X stays X and local Z becomes Y. Door and wheel assemblies are rigid children of named
pivots; front calipers steer but never spin.

| Pivot nodes | Local axis | Full range | Clearance sample spacing |
| --- | --- | --- | --- |
| `Door_FL`, `Door_RL` | Z | 0…72° | 2° |
| `Door_FR`, `Door_RR` | Z | −72…0° | 2° |
| `Hood` | X | −62…0° | 2° |
| `Tailgate` | X | −90…0° | 2° |
| `Wheel_FL/FR/RL/RR` | X | full revolution, 0…360° checked | 15° |
| `Steer_FL/FR` | tilted Z | −35…35° | 1° |
| `Mirror_L` / `Mirror_R` | Z | −50…0° / 0…50° | 2° |
| `Fuel_Door` | Z | 0…95° | 2° nominal |
| `Wiper_0/1` | tilted Z | −80…0° | 2° |

Front door hinge lines pass through `(±.944, −1.40275, 1.040)` m; rear door
hinges through `(±.944, −.05275, 1.040)` m. Hood hinge is
`(0, −1.4495, 1.408)` m; tailgate hinge is `(0, 2.824, .905)` m.
Each front wheel is nested under its kingpin pivot: actual exported axes
measure 12.00° inward inclination, 6.50° caster, 40.00 mm scrub and 45.00 mm trail.
Wipers sweep about their own axes normal to the windshield, rather than world Z.

`make check` runs **17 full-range BVH clearance sweeps on both game and high
assemblies**, with a 0.5 mm tolerance. Only named bearing, CV/ball-joint and
mirror-hinge interfaces permit intentional contact. Tires/liners and
rotors/calipers have no collision exemption. These tests establish mechanical
clearance at the stated angular samples; they are not continuous-time physics.

`build/car-delivery-check.json` independently checks the GLB's parenting,
kingpin geometry, preserved panel normals, actual atlas contents and every
sampled rigid articulation against the source transforms. The kit's delivery
check also compares re-imported vertices/pivot matrices and validates UVs,
normal vectors, materials, texture sizes and bounds. Serialization agreement
and mechanical clearance are reported separately.

The circular tire is a **mean loaded-envelope approximation**: 401.35 mm rolling
radius, without a rotating parked flat spot. A separate fixture checks ground
support through a full revolution. It does not simulate tire carcass squirm,
suspension travel or road contact physics.

## Rebuild and evidence

```sh
make -C cars                    # references, source, UV/bake, GLB, all finals,
                                # photo pairs, three docs JPGs, and checks
make -C cars check              # source construction, both motion sweeps,
                                # re-import and independent car delivery checks
make -C cars final-render       # GLB Cycles views and Eevee
make -C cars final-colors final-pairs
make -C cars docs               # provenance/tone/contact sheets and docs
make -C cars face PASS=face-checkpoint WIDTH=1500 SAMPLES=64
                                # archived source face checkpoint
```

All Cycles work holds the kit's shared GPU lock. The asset builds from clean
scripts with the repository tools, Blender, NumPy, Pillow and installed Noto
Sans fonts resolved by `kit/fonts.py`. No downloaded code, models, materials,
textures or HDRIs are used. Generated blends, GLBs, maps and renders remain
ignored; only the three final bounded docs JPGs are committed.

The four final photo pairs use the original used-truck camera solver and
procedural daylight conditions. Ford supplemental RMS is 44.88 / 26.60 native
pixels; the five-year Ram RMS is 19.57 / 19.83 pixels. These measure class
camera registration, not design identity. Cropped framing, trim, tire and
wheelbase differences remain disclosed uncertainties.

![Baked front, wheel and open-driver interior](docs/details.jpg)

The shipping critiques are at the top of [REVIEW.md](REVIEW.md). Reflections
remain simpler than the photographed street and parking lots; the low-detail
interior and tiny filtered markings are the weakest close-range areas.
The shared atlas averages microscopic flakes and limits sidewall-type detail.
The script source and shader behavior are available for engine integration.


## Alder S240 — sedan form checkpoint

An original 2018–2022 FWD midsize sedan, compared against the Camry and Accord.
**Round 2, source form only:** sculpted body, six-light glazing, shared-family
wheels and 235/45R18 tires, real panel reveals and arch returns, and dark blanks
for lamps, grille, intakes, handles and diffuser. Optical construction, interior,
underbody, paint/wear, UVs, bake and sedan GLB remain later stages. No sedan docs
images are committed at this gate.

`src/build.py --body pickup|sedan` selects the family body. The default pickup
path is unchanged. The sedan uses one connected Catmull-Clark section cage;
a rounded elliptical fascia volume fairs both ends before panel separation.
Radial projection preserves the ordering of the cap rows. Top crown, upper rake,
bumper tangent and lower tuck belong to that same surface. Evaluated normals
transfer across the panel reveals after closing the sheet gauge. This is a
sculpted three-dimensional surface, not an extruded side outline with bevels.

The cabin, door cuts and axles translate together 90 mm forward to correct the
old overhang allocation. The accepted windshield rake, side-window profile,
tracks, tire dimensions and 40 mm arch gaps remain. The requested header change
follows the windshield direction. The central backlight extends rearward to
leave a short deck; the quarter-window side profile remains. The B-pillar has
its black applique, and the tucked lower doors sit over a recessed rocker.
Rear lamp blanks now split between the decklid and quarter panels.

### Dimensions and measured end specifications

[REFERENCE.md](REFERENCE.md) gives the manufacturer table, sources and uncertainty.
The [MY2019 Toyota eBrochure](https://cdn.dealereprocess.org/cdn/brochures/toyota/2019-camry.pdf)
and [MY2019 Honda specification](https://hondanews.ca/en-CA/releases/release-4f32a27ba2ad7509bfa642e1160157a6-2019-honda-accord-specifications)
provide the class basis. The [Toyota UK metric brochure](https://www.toyota.co.uk/content/dam/toyota/nmsc/united-kingdom/brochure-archive/camry/camry-jun-21.pdf)
explicitly gives 975 / 1085 mm overhangs on its 4885 / 2825 mm envelope.
Our extra 10 mm in length minus wheelbase goes behind the rear axle, giving
975 / 1095 mm targets. The front number is 25 mm beyond the rough 860–950 mm
photo range, but follows the coherent manufacturer dimensions.

| Quantity | Actual evaluated game source |
| --- | ---: |
| Length × width × height | 4900.0 × 1850.0 × 1449.2 mm |
| Wheelbase; front / rear track | 2830.0; 1590.0 / 1600.0 mm |
| Front / rear overhang, full mesh bounds | 974.7 / 1095.3 mm |
| Tire width / loaded diameter; arch gap | 235.0 / 660.7 mm; 40.0 mm on all four |
| Windshield rake / B-section tumblehome | 61.48° / 24.14° from vertical |
| Door reveals, 40 sampled points | 4.497–4.502 mm |
| Ground clearance | 145 mm target; underbody measurement deferred |

End measurements below come from actual mesh rays, cuts and retained aperture
vertices. The checker verifies that aperture samples still lie on their actual
mesh after adaptive refinement; it does not report design controls as measurements.
Plan sweep is measured at x=850 mm, at each bumper's measured leading height.
The section proof is `renders/sedan-round2/section-centerline.jpg`.

| Front specification | Actual | Requested |
| --- | ---: | ---: |
| Plan sweep | 314.3 mm | 250–350 mm |
| Bumper leading height | 484.0 mm | 450–550 mm |
| Upper face rake from vertical | 35.22° | 30–45° |
| Hood edge setback / height | 185.2 / 746.4 mm | 150–250 / 720–800 mm |
| Chin tuck / height | 119.0 / 189.2 mm | 100–150 / 150–200 mm |
| Hood rise / cowl height | 10.47° / 964.6 mm | 8–12° / 950–1000 mm |
| Hood transverse crown, x=±800 mm at y=−1650 mm | 30.3 mm | 20–40 mm |
| Headlamp developed length | 696.3–696.4 mm | 600–700 mm |
| Headlamp maximum height / corner return | 146.6–146.6 / 224.9–225.0 mm | 120–180 / 200–300 mm |

The hood has two soft longitudinal draws that move outward into the A-pillar
feet, and a curved leading reveal following the lamps' upper outline. The wide
trapezoidal grille, black lower intake and corner pockets are conformed locators
in the molded fascia. Their wells and optics are intentionally deferred.

| Rear specification | Actual | Requested |
| --- | ---: | ---: |
| Plan sweep | 237.9 mm | 150–250 mm |
| Deck trailing lip height | 1042.7 mm | 1000–1050 mm |
| Upper panel lean from vertical | 11.47° | 5–15° |
| Bumper rearmost height | 602.0 mm | 550–650 mm |
| Lower tuck / diffuser height | 175.8 / 300.0 mm | 150–200 / 250–350 mm |
| Deck length / rise / transverse crown | 372.7 mm / 5.00° / 22.1 mm | 350–450 mm / rising / crowned |

The tail's upper edge lies forward of the bumper tangent; below it the diffuser
recedes farther forward. This is the conventional outward bumper relationship
visible in both makes. The brief's phrase “tucks forward … to the rearmost point”
is directionally ambiguous; the cut and coordinates make the chosen relationship
explicit. The lip is the highest crisp edge of the tail beyond the backlight.

### Allocation and later delivery

The game source is **46,972 triangles**, close to the accepted 46.9k
plan; the separate high source is **373,984**. Denser aperture cells are used
only where their chords would otherwise enter the painted body. The game body's
interior reduction retains seam vertices and transfers the original smooth field.

| Form parent / assembly | Triangles |
| --- | ---: |
| Static body, glass, fascia, liners and locators | 30,308 |
| Hood / trunk, including lid lamp blanks | 876 / 1,144 |
| Front door L / R | 1,312 / 1,312 |
| Rear door L / R | 1,200 / 1,204 |
| Wheel and tire, each | 2,404 |
| **Total** | **46,972** |

Every mesh and construction category is listed in `build/sedan/form-check.json`.
There are four clay materials and **zero image textures**. The planned shared
2048² BaseColor / OpenGL Normal / ORM set remains **16 MiB** at three 8-bpp
compressed maps with full mips (64 MiB at RGBA8). No new paint sets are created.
Common-family texel sharing, five neutral-atlas paint factors, frit, lamps/lit
state, interior method and causal wear remain the later-stage family methods.
Source game/high files are about 1.0 / 6.8 MB, ignored and rebuildable.

Four door pivots, hood/trunk pivots and the family's wheel spin/steer hierarchy
are provisional form roots. Their eventual hinges, ownership and full-range
clearance remain later work. The 45–55k final aim and 70k ceiling still apply;
replace temporary locators and remove redundant hidden sheet faces as detail is
introduced, rather than treating this checkpoint as free extra geometry.

### Rebuild and evidence

```sh
make -C cars BODY=sedan WIDTH=1600 SAMPLES=40
make -C cars BODY=sedan check
make -C cars BODY=sedan review
make -C cars                         # accepted pickup delivery path
```

`sedan.mk` defaults to `renders/sedan-round2/`. The **27-view contact sheet** is
`contact.jpg`: clay front/rear three-quarter views; dimensioned side/front/top;
wheelbase-registered side overlay; both stripe directions on both ends; front
axle, B-pillar, rear axle and centerline cuts; photographic tumblehome estimate;
and front/rear comparisons against both makes, in neutral clay and striped clay.
The four residual overlays expose the camera fits rather than hiding their error.

| Camera | Chassis-fit RMS, native pixels |
| --- | ---: |
| Accord front / Camry rear | 5.76 / 5.30 |
| Camry front / Accord rear | 11.07 / 8.76 |

Blender's independent projection agrees within 0.003 px. These are registrations
from wheel hubs/contact points, not fits of the body silhouette. White studio
backgrounds provide the neutral balance. Photo tumblehome is an estimate with
±4.5° uncertainty. The side overlay holds out all body landmarks: the roof-front
station is about **+14 mm**, the hood lead **+33 mm**, and the worst sampled
station is the deck at **−96 mm**, with ±16.5 mm picking uncertainty and residual
perspective. The 1043 mm lip follows the brief; it does not match the Camry SE's
higher spoiler silhouette. The full coordinate/pixel record is beside the overlay.

`make check` passes game/high topology, normals, slivers, 3 mm envelope tolerance,
budget, all 23 numeric end requirements, physical sections, camera projection and
repository policy. It does not certify sedan UVs, motion, baking or export.
All Cycles views use the kit GPU lock. **No kit changes.**

The pickup preservation check was rerun: **454 source meshes and all 150 GLB
accessors are identical**, as are the embedded maps and delivery graph. The
entire independently re-exported pickup GLB is byte-identical, 11,530,736 bytes,
SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
This reuses the accepted finalized source/maps and makes no new GPU rebake claim.
Evidence: `build/sedan/pickup-preserved.json`. The sedan also has an independent
exact-array regeneration check in `build/sedan/repeat-check.json`.

[REVIEW.md](REVIEW.md) records the rejected rounds and two current regional
critiques. Remaining weaknesses are the unusually regular window corners, the
simpler fascia/pocket sculpting beside production photos, and tightly gathering
reflections at the lamp/shoulder and lower corner transitions. The deck remains
lower than the photographed Camry. This checkpoint stops before detail.
