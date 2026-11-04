# Cars family — Alder C150 and S240

The C150 pickup is delivered. The [S240 sedan](#alder-s240--sedan-detail-and-look-checkpoint) has a baked GLB and checked mechanisms; its form and look checkpoint remains under review.

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


## Alder S240 — sedan detail and look checkpoint

An original 2018–2022 FWD midsize sedan. Round 6 adds the exterior, five-place
cabin, low underbody, factory coatings and working mechanisms to the accepted
continuous-sheet body. The delivered GLB is **59,992 triangles**. This is a
review checkpoint: the side-overlay 40 mm target and photographic polish remain
open, as described below. Checkpoint images stay in ignored `renders/`; final
`docs/` images have not been committed.

### Form and real construction

The hood, fenders, doors, greenhouse, deck and fascias retain their common
Catmull–Clark parent and its measured sections, shoulder, lower character line,
fender swells, recessed face and painted rear sails. Local sampling and fairing
at the lamp crests, A-pillar feet and C-header corners improve reflection flow.
The lower nose/arch chart boundary no longer makes a false panel seam. Steel
skins have 0.9 mm gauge, molded fascias 3 mm, glazing 4.8 mm.

The nose now leads at **500 mm** and tucks **133.9 mm** to its **174.9 mm** chin.
The rear leads at **602 mm**, tucks **189.5 mm** to the diffuser's 300 mm station,
and its painted bottom rises to **270 mm**. The actual rear tire/overhang ground
tangent is **18.04°**, above Honda's published **17.5°** later-generation Accord
class cross-check. This is not a MY2019 Camry departure-angle claim; see
[REFERENCE.md](REFERENCE.md) and [refs/SOURCES.md](refs/SOURCES.md).

The 1211 / 1268 mm backlight and sails, integrated deck lip, convex bumper,
153 mm class taillamps, 320 × 170 × 26 mm plate pocket, reflectors and rolled
exhaust finisher remain. The registration plate is blank. The door-mounted
mirrors keep their full span; the compound caps now measure 167 × 120 × 96 mm,
with supported arms, body clearance and real reflective panes.

The detail uses an original recessed barred/relief grille, 52 mm projector
optics in formed reflector bowls, swept twin running guides, amber side
markers, red rear optics and reverse guides. Fictional ALDER/S240 markings,
pull handles and cups, window seals/brightwork, B appliques, parked wipers,
washer nozzles, shark fin and fuel flap complete the exterior. Fine lettering,
tread, machining and coating detail are procedural or generated with Noto Sans;
no downloaded texture, model, HDRI or photograph enters the asset.

The frameless doors carry their glass, cards and controls. Inside are two front
seats and a three-place rear bench with five headrests, dash, cluster and center
screen, console/shifter, steering wheel, headliner and rear shelf. Underneath
are a FWD engine/transaxle approximation, subframes, independent suspension,
CV shafts, tank/straps and supported exhaust. Hidden geometry is deliberately
simple; the engine bay and upholstery remain visibly approximate at close range.

### Dimensions and budget

Dimensions come from actual mesh rays/vertices and the cited class references,
not copied CAD or a fitted photographic outline.

| Measurement | Actual source / delivery |
| --- | ---: |
| Length × body width × body height | 4884.9 × 1849.4 × 1449.6 mm |
| Including mirrors / antenna | 2104.6 mm wide / 1481.8 mm high |
| Wheelbase / front and rear tracks | 2830 / 1590, 1600 mm |
| Tires / rolling diameter / crown gap | 235/45R18 / 660.7 / 44 mm |
| Rim bead width / overall metal width | 190.5 / 196.0 mm |
| Studs / pitch circle / cap recess | five / 114.3 mm / 12.0 mm |
| Lowest underbody point | 146.5 mm, engine sump |
| Nominal door reveals | 4.5 mm, including the physical sill cut |
| Game / high source | 59,992 / 170,032 triangles |
| GLB | 12,845,344 bytes |

| Manufactured group | Triangles |
| --- | ---: |
| Body skins | 12,916 |
| Molded fascias | 10,772 |
| Pillars / door skins | 1,316 / 2,808 |
| Glass / mirrors | 2,272 / 660 |
| Arch flanges / liners | 784 / 1,168 |
| Recesses / optical assemblies | 2,796 / 6,144 |
| Tires / wheels / brakes | 3,520 / 4,072 / 1,120 |
| Exterior trim / hinge hardware | 2,812 / 1,176 |
| Interior / underbody | 3,896 / 1,760 |
| **Total** | **59,992** |

| Moving parent, including its attached detail | Triangles |
| --- | ---: |
| Front doors L / R | 1,664 / 1,666 |
| Rear doors L / R | 1,624 / 1,626 |
| Hood / trunk | 892 / 3,474 |
| Each spinning wheel assembly | 2,078 |
| Each front steering carrier | 148 |
| Hood support sleeves / rods, both sides | 128 / 64 |
| Static assembly, including cabin and underbody | 40,246 |

Every individual mesh count is in `build/sedan/detail-game.counts.json` and
`build/sedan/detail-check.json`. Hidden gauge-back reductions preserve all
exposed vertices and dense-parent corner normals. Fine shoulder blocks and
chamfers stay in the high source; the game tire retains procedural tread relief.

### Coatings, atlas and runtime controls

Five factory factors use the pickup's coverage-delta method over one neutral
atlas: Porcelain, Carbon, cool Graphite, Aluminum and Atlantic. Graphite is an
original cooler sedan option; the pickup's factors and export remain intact.
The normalized spawn weights are 31 / 19 / 21 / 8 / 10 out of 89, using Axalta's
2025 North American new-car color shares for these five choices. They are not a
measurement of the used-car fleet.

Paint has a continuous clearcoat, faint procedural peel/flake and wash swirls.
Road film comes from low splash and fans aft of the wheels, broken by gravity
streaks; chips follow hood-front and door edges, with residue in the shut lines.
Metal, black plastic, rubber, cloth and chrome have separate source responses.
Glass has dark transmission, printed edge frit and visible cabin depth. The
wheels use caliper-centered brake dust and fictional ALDER TOURING tire relief.
Wear is `--wear` on the detail generator, default 0.65.

The three maps are `T_AlderS240_BaseColor.png` (sRGB),
`T_AlderS240_Normal.png` (OpenGL +Y) and `T_AlderS240_ORM.png` (linear R/G/B =
occlusion/roughness/metallic), baked at 4096² and delivered at **2048²**.
BaseColor alpha retains paint coverage or lamp strength according to surface;
`src/delivery_materials.py` and the documented family decoder apply factory
factors and lit/unlit state without five texture copies.

There are **four delivery surfaces**, matching the pickup: Paint, Opaque,
Glass and Lamps. Paint recoloring/coat, transmission and switchable emission
need separate responses; this exceeds the standing three-material preference.
All four reference the same three embedded images.

The set costs **16 MiB with full mip chains at 8 bpp per map** (for example
BC7/BC5/BC7), or 64 MiB if all three are expanded to RGBA8 with mips. This
checkpoint shares the pickup's material/decoder methods, **not its atlas pixels**:
loading both current cars costs about 32 MiB compressed. A common family atlas
would require a coordinated repack/rebake of the accepted pickup and parallel
bodies; that remains a family integration limitation.

The bake is explicit about correspondence. Direct finalized-surface procedural
BaseColor/ORM and shader normals avoid neighboring-skin, reverse-gauge and optical
projection contamination. Original coordinates are stored before UV packing. High-source
normals replace exact-surface shader normals only on parts passing independent
partwise projection rays. The body already carries the dense parent's normal
field. `bake-report.json` lists accepted parts and fallback coverage; this is
not a claim that every high-detail feature survived projection. A tiny set of
backward direct-normal samples falls back to the neutral tangent normal; the
report exposes both interior counts and padding counts. The source geometric
normal field remains intact. The final direct normal interior fallback is
172 / 4,744,395 samples (0.0036%); verified high normals cover 256 parts and
8.64% of the atlas.

UV coverage is 37.06%, with 83.7 / 234.5 / 268.0 px/m at the 5th / median /
95th percentiles. No UV triangle is degenerate or out of bounds. Four residual
subpixel overlaps total less than one shipped texel and pass the kit threshold.
Visible skins take priority over hidden gauge backs; small markings retain
extra density.

### Pivots and measured motion

Coordinates are meters in Blender: +Z up, front −Y, origin at the authored
footprint center. Doors rotate about **custom unit vectors**, stored in each
node's `hinge_axis_vehicle`; use an axis-angle quaternion, not a local-Z Euler
rotation. Their mesh frames stay aligned with the vehicle at rest.

| Node | Pivot (x, y, z) | Axis / tested range |
| --- | --- | --- |
| Door_FL / FR | (±0.880, −1.060, 0.740) | normalized (±0.14, 0, 1); L 0…60°, R −60…0° |
| Door_RL / RR | (±0.865, 0.125, 0.740) | normalized (±0.14, 0, 1); L 0…68°, R −68…0° |
| Hood | (0, −1.080, 0.977) | local X, −62…0° |
| Trunk | (0, 1.720, 1.010) | local X, 0…72° |
| Wheel_FL / FR | (±0.795, −1.475, 0.33035) | local X, full revolution |
| Wheel_RL / RR | (±0.800, 1.355, 0.33035) | local X, full revolution |
| Steer_FL / FR | (±0.68478, −1.48236, 0.33035) | inclined local Z, −35…35° |

In this table negative x is L; the door-axis x sign follows its side. The
steering unit vectors are L (+0.20663, +0.11076, +0.97213) and R
(−0.20663, +0.11076, +0.97213), an original 12° SAI / 6.5° caster package.
Four wheels spin independently; calipers stay on their steering/rear carriers.
The hollow hubs have minimum 70.4 mm bores around 70.0 mm journals, measured
0.20 mm radial clearance and 31.0 mm axial engagement through a full revolution.

Eight concealed hinges have measured 8.0 mm pins, minimum 8.4 mm bores and
approximately 0.20 mm radial clearance. Moving leaves contact their barrels
and lie within 0.94 mm of the supporting sheet; fixed leaves meet their pins.
Front jamb channels, inner B posts and sill reinforcements carry the loads.
The hood uses two telescoping hollow gas supports. Measured member overlap
stays **67.9–280.2 mm** through the range. Trunk goosenecks clear the backlight,
rear shelf and tub. Their lid ends are measured within 0.30 mm of the actual
inner sheet, and their fixed supports meet both bearing and tub. Tank straps,
exhaust hangers and upper dampers are seated on measured supporting surfaces.
The 1.2 mm stepped floor rises over the tank and joins the trunk; front rails
and engine-mount gussets carry the front structure.

The kit tests all 12 mechanisms on both game and high sources: door/hood/trunk
steps 2°, steering 1°, wheel spin 10°, **491 sampled poses per source** at
0.5 mm penetration tolerance. Independently evaluated hood-support sweeps cover
all 32 hood poses, including the real hollow rod/sleeve pair. These are sampled
surface-collision tests; GLB re-import separately proves geometry and pivot
serialization, not mechanical correctness between samples. Intended CV, lower
ball-joint and coaxial strut/knuckle contacts use explicitly named composite
joint proxies; they are not unrelated-panel collision exceptions.

After changing the hood pose, re-aim each support frame toward its exported
`support_target` endpoint, as `supports()` in `src/sedan_lookdev.py` demonstrates.
The rigid members telescope; glTF does not serialize Blender tracking constraints.

### Rebuild and inspect

```sh
make -C cars BODY=sedan WIDTH=1400 SAMPLES=36
make -C cars BODY=sedan check
make -C cars BODY=sedan form       # accepted-sheet clay/stripes/overlays
make -C cars BODY=sedan check-motion
make -C cars                     # pickup delivery path
```

Studio heroes use exposure −2.8: all ten factory-color views have zero clipped
paint pixels. Used-car patches have median absolute display-luma difference
14.0/255 and worst 49.7/255 at the rear quarter; Graphite remains too cool.

The default sedan graph fetches only recorded reference images/PDFs, builds
both sources and markings, checks physical construction/motion, packs UVs,
bakes via the shared GPU lock, downsamples, exports/re-imports, and renders the
GLB. No installed packages or downloaded code are needed. An independent
regeneration matches all **405 meshes / 426 objects**, including topology,
vertices, corner normals, transforms, parents and material assignments exactly.
The pickup preservation report matches all 454 source meshes and the accepted
GLB's 150 accessors, embedded maps, graph and binary payload; only the current
exporter-version label differs on re-export. Its accepted export is untouched.
No kit files changed. The only shared family edit adds optional wheel sampling
and centers narrow-caliper scaling on the hub; pickup defaults are identical.

| Generated image location | Contents |
| --- | --- |
| `renders/sedan-round6/` | Clay, stripes, sections, three perspective variants and raw side overlay, form/photo pairs and contact sheet |
| `renders/sedan-detail/contact.jpg` | Exported-GLB studio views, orthographic turnaround, face, lamps, wheel/mirror, cabin through glass, low and underside views, open mechanisms, human scale |
| `renders/sedan-detail/factory-colors.jpg` | Five colors, front and rear three-quarters |
| `renders/sedan-motion/*-sweep.jpg` | Five visible poses each for doors, hood, trunk, steering and wheel spin |
| `renders/sedan-used-pairs/` | Calibrated, white-balanced five-year class pairs, annotated surface patches and display-value measurements |
| `renders/sedan-eevee/` | Eevee export check |
| `renders/sedan-detail/checkpoint.jpg` | Combined review contact sheet |

### Limits of this checkpoint

The physical lower-end targets pass, but the **40 mm side-overlay target does
not**. Raw wheelbase-scaled worst deviations remain **118.8 mm front / 71.8 mm
rear**. The perspective camera alternatives reach **110–131 mm** below the ends.
The raw photo wheelbase scale implies a roughly 4702 mm envelope versus the
accepted 4885 mm body. The length is retained; this discrepancy is exposed in
all overlays and is not excused as lens error or hidden by fitting the outline.

[REVIEW.md](REVIEW.md) records the color-first critique passes, rejected bakes
and final measurements. Remaining CG tells include simple seat/dash forms,
coarse grazing reflections at the C-sail and lamp crest, simplified rear optics,
and less convincing surrounding reflections/road-film variation than the used
photographs. This is not final photographic or family-atlas approval.
