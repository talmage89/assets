# Cars family — Alder C150, S240 and X220

The C150 pickup and [X220 SUV](#alder-x220--compact-crossover) are delivered. The [S240 sedan](#alder-s240--sedan-form-checkpoint) record below is its source form checkpoint. `BODY=sedan` and `BODY=suv` select isolated pipelines. The X220 has articulated closures, a five-seat cabin, AWD underbody and an open chevron grille at 64,933 triangles.

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

An original 2018–2022 FWD midsize sedan, compared with the Camry and Accord.
**Round 4 is a source form checkpoint.** Interior, underbody, optical internals,
paint/wear, UVs, baking, motion certification and sedan GLB remain later work.
The pickup's default generation and complete exported GLB stay byte-identical.

### Construction and character

One connected, all-quad control sheet spans the hood, fenders, doors,
greenhouse, deck and both fascias. Its **124,032 control quads**
retain valence four at every interior vertex. Section fitting happens before
Catmull-Clark evaluation. Panels and apertures are cut afterwards; their
normals and curvature come from that parent. The game chart concentrates
samples at the lower rear corner and uses fewer chords across the broad
canopy. Steel gauge is 0.9 mm, molded fascia 3 mm and glass 4.8 mm.

The shoulder is the widest point of each door. Its upper door leans inward;
the lower door turns inward progressively through a shallow die hollow and
soft rising crease, then a recessed sill. Same-height rays measure **33.3 /
28.2 mm front/rear fender swell**. The rear's finite-span bumper-height plan
radius is **303.4 mm**, retaining the approximately 305 mm draw.

The original rising headlamp blades are **746 × 110 mm**, with 268–292 mm
returns. Their chart-triangulated blanks sit behind real skin apertures;
the triangulation prevents folded tiny cells at tapered tips. Upper grille,
lower intake and corner pockets have physical inward returns and blocked
horizontal blades. Measured mouth-to-bed depths are 64–67, 60–62 and 50–52 mm.
Fender crown rise over the hood side is 19.0 / 14.8 mm at y=−1.60 / −1.30 m,
falling to 3.9 mm by y=−1.10 m; that last blend remains weaker than requested.

The deck and C-pillar are raised per the round-4 overlay correction. The
integrated lip kicks up **21.3 mm** over the adjacent deck's
extrapolated slope. Tapered rear wings split at the lid's real cut and wrap
approximately 300 mm forward into the quarters. The plate pocket is 26–27 mm
deep; the diffuser is recessed 11–14 mm inside the fascia. These are source
mesh measurements, not design constants or delivery serialization checks.

Door-mounted mirror caps measure **250 × 204 × 157 mm** (outboard × fore/aft ×
height); full span is **2110.0 mm**. This original size is cross-checked
against Ford's manufacturer-published [2121 mm Mondeo mirror span](https://www.ford.ie/content/dam/guxeu/uk/documents/feature-pdfs/FT-Mondeo.pdf).
The housings remain form blanks; their stems are supported by the doors.

### Actual dimensions and sections

[REFERENCE.md](REFERENCE.md) and [refs/SOURCES.md](refs/SOURCES.md) distinguish
manufacturer dimensions, original styling and photographic uncertainty.

| Measurement | Actual game source |
| --- | ---: |
| Length × body width × height | 4900.8 × 1850.1 × 1449.6 mm |
| Wheelbase / tracks front, rear | 2830 / 1590, 1600 mm |
| Front / rear overhang | 975.4 / 1095.4 mm |
| Tire / loaded diameter / crown gap | 235/45R18 / 660.7 / 40.0 mm |
| Windshield rake / B-section tumblehome | 61.72° / 23.66° from vertical |
| Door reveals | 4.5 mm, measured across the actual cuts |
| Front sweep at x=850 mm / upper rake | 321.2 mm / 36.14° |
| Hood edge height / setback | 757.1 / 187.8 mm |
| Chin height / tuck | 176.7 / 123.9 mm |
| Hood rise / cowl height / crown | 10.03° / 966.1 / 22.9 mm |
| Rear sweep / upper tail lean | 247.9 mm / 12.55° |
| Deck crest height / deck length | 1110.8 / 366.4 mm |
| Rear lower tuck / diffuser test height | 195.6 / 300.0 mm |

| Section | Shoulder height | Upper inward lean | Lean just below / low door | Lower edge inset | Sill tuck | Crease turn over 80 mm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| mid front door | 910.0 mm | 20.2–21.2° | 4.6 / 16.3° | 80.4 mm | 40.9 mm | 11.2° |
| b pillar | 921.0 mm | 20.2–20.6° | 4.6 / 15.3° | 75.0 mm | 45.4 mm | 10.7° |
| mid rear door | 932.0 mm | 20.3–20.6° | 4.6 / 13.1° | 70.1 mm | 49.7 mm | 9.7° |

The three 50 mm chord tests find a 1.7–1.8 mm inward hollow. Section positions
come from actual triangle-plane cuts and rays; rendered normal angles use the
parent's interpolated corner normals. Raw sample points, derivative windows
and every curvature sign reversal remain in the JSON reports. Character zones
include the rising die line, rocker return, shoulder, fender-crown transition
and lower fascia roll. These finite tests do not certify global Class A fairness.

### Budget and reproducibility

The game source is **52,628 triangles** and the high source
**116,600**. Five diagnostic clay materials use **zero image
textures**. Generated game/high blends are 1,189,936 /
2,475,377 bytes. No sedan GLB is produced at this gate. The temporary cavity closure sits
inboard of the wheel wells and forward of the tucked tail; actual mesh extrema
measure 127.5 mm lateral clearance to the tire envelopes. Other motion remains
unverified.
The later shared 2048² BaseColor / OpenGL Normal / ORM plan remains 16 MiB
with three 8-bpp compressed maps and full mip chains. Temporary optical/well
allocation must be replaced during detail, not simply added to.

| Parent / assembly | Triangles |
| --- | ---: |
| Static body, fascia, glazing, mirrors and locators | 34,788 |
| Hood / trunk including its lamp blanks | 1,028 / 2,304 |
| Front doors L / R | 1,348 / 1,344 |
| Rear doors L / R | 1,100 / 1,100 |
| Each wheel and tire | 2,404 |
| **Total** | **52,628** |

```sh
make -C cars BODY=sedan WIDTH=1600 SAMPLES=40
make -C cars BODY=sedan check
make -C cars BODY=sedan fairness
make -C cars                         # unchanged pickup delivery path
```

The first three commands pass the source gate: both density audits, closed
positive gauges, normals, budget, scale, real cut openings and bed depths,
sections, end ranges, parent/game curvature, camera projection and repository
rules. UV, bake, motion and GLB checks remain explicitly pending. Independent
one-thread regeneration matches all 112 meshes' geometry, normals, transforms,
materials and parents exactly. A fresh default pickup build matches all 454
meshes; re-export matches all 150 accessors and the complete 11,530,736-byte GLB,
SHA-256 `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.

### Review images and remaining misses

`renders/sedan-round4/contact.jpg` contains 37 views: clay front/rear,
dimensioned side/front/rear/top and paired front/rear, raking side, both
stripe directions from front/rear/side, driver's hood reflections, five body
and six cover curvature plots, five transverse cuts plus centerline,
photographic tumblehome estimate, all four calibrated neutral and striped
pairs, and their calibration overlays. All 22 rendered views carry the same
source hash. [REVIEW.md](REVIEW.md) records the two critique passes and rejected
intermediate experiments. No checkpoint images are committed.

The wheel-center-only side overlay now measures **−32.9 mm at the C-pillar
and −35.3 mm at the deck**, with ±16.5 mm photographic pick uncertainty.
The lower-end 40 mm target is **not met**: the held bumper tangents remain
+132.9 mm nose / +78.2 mm tail in that raw overlay. Lower nose/chin are
+41.2 / +25.9 mm, and lower tail/under-tail +41.2 / +2.9 mm. Near-profile
perspective and original end styling remain uncertainties; no outline fit or
image warp is used to erase them. The accepted 4900 mm envelope and
975 / 1095 mm overhangs remain held.

The lower rear's large stripe zigzag is removed; fine grazing waviness and
the lower front-door/sill transition remain weaker. Plain bumper lands, simple
bars, regular glazing corners and oval mirror housings still read as form
proxies beside the photos. The fender crown fades too early near the A-pillar.
These are recorded limitations, not final paint or delivery approval. No kit
changes were needed.


## Alder X220 — compact crossover

An original late-2010s two-row crossover, generated entirely by scripts. The
stamped body, molded cladding, laminate glazing, chevron grille, projector lamps,
five-seat cabin, covered cargo floor and AWD underbody share one baked atlas.
The delivery preserves the accepted body lines, detail, colors and articulation.

![Alder X220 in the family gallery](docs/suv-hero.jpg)
![Rear three-quarter](docs/suv-rear.jpg)
![Optics, wheels, cargo and lit lamps](docs/suv-details.jpg)
![Turnaround, scale and Eevee](docs/suv-views.jpg)
![Five factory colors](docs/suv-five-colors.jpg)
![Liftgate through its 75-degree range](docs/suv-liftgate.gif)

Every final starts with a fresh import of `export/AlderX220.glb` and its three
embedded maps in the unchanged C150 gallery. Source shaders are used only for
separately labeled bake-loss controls. Full-size [contact sheet](renders/suv-final/contact.jpg),
[matched front](renders/suv-final-pairs/used_front-pair.jpg),
[matched rear](renders/suv-final-pairs/used_rear-pair.jpg),
[bake-loss measurements](renders/suv-final/bake-loss.json), and
[critique passes](REVIEW.md) accompany the delivery.

| Actual game measurement | Value |
| --- | ---: |
| Length / wheelbase | 4598.8 / 2690.0 mm |
| Body / full mirror width | 1842.0 / 2117.0 mm |
| Roof / rails / antenna height | 1679.0 / 1700.0 / 1735.0 mm |
| Front / rear track | 1600.0 / 1610.0 mm |
| Tires / lowest underbody surface | 225/65R17 / 205 mm |

The package is measured against Toyota's MY2020 US RAV4 brochure and Honda's
MY2020 CR-V specifications; the UK CR-V brochure cross-checks mirror width.
These are reference classes, not reproduced designs. [REFERENCE.md](REFERENCE.md)
and [SOURCES.md](refs/SOURCES.md) distinguish published dimensions, original
construction estimates and photographic authors/licenses.

| Delivery resource | Actual |
| --- | ---: |
| Triangles | **64,933 / 65,000** |
| Materials / embedded maps | **4 / 3**, family Paint, Opaque, Glass, Lamps |
| Shipped maps | **2048²** BaseColor / OpenGL Normal / ORM, baked at 4096² |
| Compressed texture allocation with mip chain | **about 16 MiB** |
| GLB | 9,061,968 bytes |
| Unique atlas / shared tyre tile / total occupied area | 30.39% / 24.75% / **55.14%** |
| Exterior painted-panel density | 137 / 195 / 206 px/m (p5 / median / p95, UV-area weighted) |

The four family surfaces share the same images: paint needs clearcoat and
factory factors, glazing transmission/IOR, lamps controlled emission, and
opaque fittings their own response (source dielectric specular level .33). This retains the family's four-material
exception to the general three-material target. The four identical tyre
carcasses reuse one tile at 854–1099 px/m; all other charts are unique. The
trade is four separate carcass primitives, parented to their spinning wheels.

Five factory presets cost no extra maps. The family coverage decoder keeps
colored dirt/chips while changing paint. SUV Graphite is linear RGB
`.150 / .1540545 / .160`, metallic `.42`; the other four family factors are
unchanged. [suv_delivery_materials.py](src/suv_delivery_materials.py) reads only
embedded images and material extras. Smooth glass has normal-texture scale
zero. The lamp extras specify the warm white projector/guide emission color
independently of its dark unlit substrate. Cycles follows nested refraction;
Eevee uses the family's documented thin-sheet fallback. A stock glTF viewer
shows the Atlantic fallback; runtime factors enable the other colors and lamps.

Doors open 60°, hood 65°, liftgate 75°, front steering ±35°, fuel flap 85°;
wheels spin continuously. Each is a separate rigid node with its actual pivot,
axis and range in extras. Eight endpoint-driven telescoping strut meshes stay
separate. [SUV.md](SUV.md) lists all local-axis conventions, per-part triangles,
UV measurements, measured bake loss and remaining limits.

```sh
make -C cars BODY=suv clean
make -C cars BODY=suv WIDTH=1600 FINAL_SAMPLES=64
make -C cars BODY=suv check
make -C cars BODY=suv check-detail-repeat
python3 kit/repo_check.py
```

`export`, `verify`, `final-render`, `final-pairs` and `docs` are separately
rebuildable targets. The default makes the complete SUV delivery. All GPU
bakes/renders use the shared kit lock. No kit or other body generator changed;
the existing C150 GLB remains byte-identical.
