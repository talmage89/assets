# Cars family — Alder C150 and S240

The C150 pickup and [S240 sedan](#alder-s240--midsize-sedan) are independently rebuildable game assets with baked GLBs, working mechanisms and studio galleries.

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


## Alder S240 — midsize sedan

An original 2018–2022 FWD midsize sedan on 235/45R18 touring tires. Its six-light
greenhouse, continuous stamped surfaces, swept lamps and cascade grille are
Alder's own design. Five factory colors share one sedan atlas. The C150's GLB
and atlas remain independent and unchanged.

![Alder S240](docs/sedan-hero.jpg)

| Rear | Factory colors |
| --- | --- |
| ![Rear](docs/sedan-rear.jpg) | ![Five colors](docs/sedan-five-colors.jpg) |

[Details](docs/sedan-details.jpg) · [Turnaround](docs/sedan-turnaround.jpg) ·
GLB (`export/AlderS240.glb`) · Studio contact (`renders/sedan-detail/contact.jpg`) ·
Scale (`renders/sedan-detail/scale.jpg`) · Eevee (`renders/sedan-eevee/`) ·
[Critique and limitations](REVIEW.md)

Every gallery view imports the exported GLB and its embedded baked textures.
No high scene, source material or reference photograph supplies the finals.
The runtime factory/coat/lamp decoder is the same method as the pickup's.

### Dimensions and construction

The class envelope is measured against Toyota's MY2019 Camry US eBrochure and
Honda's MY2019 Accord metric specifications, cross-checked with Toyota UK's
2021 Camry brochure. [REFERENCE.md](REFERENCE.md#alder-s240--original-20182022-midsize-sedan--form-gate)
and [refs/SOURCES.md](refs/SOURCES.md) distinguish published figures from original
construction estimates and record the reference URLs, authors and licenses.
The table below measures our actual surfaces and pivot centers.

| Measurement | Delivered asset |
| --- | ---: |
| Length × body width × body height | 4884.9 × 1849.4 × 1449.6 mm |
| Including mirrors / antenna | 2104.6 mm wide / 1481.8 mm high |
| Wheelbase / front and rear tracks | 2830 / 1590, 1600 mm |
| Tires / mean rolling diameter / crown gap | 235/45R18 / 660.7 / 44 mm |
| Rim bead width / overall metal width | 190.5 / 196.0 mm |
| Studs / pitch circle / hub-cap recess | five / 114.3 / 12.0 mm |
| Lowest underbody point | 146.5 mm, engine sump |
| Nominal door reveals | 4.5 mm, including the physical sill cut |
| Hood front / nose's leading height / chin | about 770 / 500 / 174.9 mm |
| Front lower tuck / rear lower tuck | 133.9 / 189.5 mm |
| Rear departure ground tangent | 18.04°, against the cited 17.5° class cross-check |

The hood, fenders, doors, roof, sails, deck and fascias derive from one supported
Catmull–Clark sheet, subdivided before its panels/openings are cut. Outer skins
have 0.9 mm steel gauge; molded fascias 3 mm; glazing 4.8 mm. The control
section stays monotone before its surface fit, removing collapsed shoulder
ribbons. Glazing recesses normally beneath its separate seals; it is
not distorted by a tangential panel inset. Openings clip the actual game facets
without lifting only their new vertices onto a different surface. The hood's
lamp cuts use its XY manufacturing plane and final laminate footprint.

Inner backs are triangulated and checked against the actual outer triangles,
including exact crossings. Their reduction preserves the hinge and gas-support
spaces. Mean-curvature maps, reflection stripes and independent surface checks
cover all 420 parts in seventeen categories on both the source and freshly
imported GLB, including glass, grille, lamps, arches and tires. Source names select parts; delivery geometry and corner normals supply the
geometric proof. Native before/after crops separately judge the baked materials.

The 1211 / 1268 mm backlight, broad sails, integrated deck lip, convex bumper,
153 mm class taillamps and 320 × 170 × 26 mm plate pocket retain the accepted
construction. Seventeen bowed gloss-black grille vanes sit over original
diamond relief, within a dark-chrome surround carrying an ALDER badge. The
plate carries an original ALDER / WILLOW MOTOR CO. dealer insert with dark
frame, without a registration format or serial. Its molded return contacts the
insert within 0.25 µm numerical error and has 2.22 mm sampled pocket clearance.

The clear headlamp covers seat on molded bucket lips across their reveals.
Projectors, reflector bowls, swept light guides, side markers, reverse windows,
pull handles, seals/brightwork, wipers, nozzles, antenna and fuel flap complete
the exterior. The five-place cabin has separate seats/headrests, dash/cluster,
screen, console/shifter, wheel, cards, headliner and rear shelf. The low-detail
underbody carries the FWD powertrain approximation, stepped floor, subframes,
suspension, CV shafts, tank/straps and supported exhaust. Fine tread, lettering,
flake, coating and machining detail are scripted/baked. No downloaded model,
material, texture, decal or HDRI enters the asset.

### Delivery budget

| Manufactured group | Triangles |
| --- | ---: |
| Body skins / molded fascias | 13,574 / 11,230 |
| Pillars / door skins | 1,404 / 2,836 |
| Glass / mirrors | 2,248 / 660 |
| Arch flanges / liners | 384 / 1,168 |
| Recesses and grille / optical assemblies | 2,864 / 5,688 |
| Tires / wheels / brakes | 3,136 / 4,072 / 1,120 |
| Exterior trim / hinge hardware | 2,724 / 1,176 |
| Interior / underbody | 3,886 / 1,760 |
| **Delivered total** | **59,930** |

| Moving parent, including attached detail | Triangles |
| --- | ---: |
| Front doors L / R | 1,680 / 1,680 |
| Rear doors L / R | 1,612 / 1,628 |
| Hood / trunk | 1,148 / 3,384 |
| Each spinning wheel assembly | 1,982 |
| Each front steering carrier | 148 |
| Hood support sleeves / rods, both sides | 128 / 64 |
| Static assembly | 40,382 |

The high source is 174,212 triangles. Every mesh is itemized in
`build/sedan/detail-game.counts.json`; independent source checks and GLB
re-import reports separate construction from serialization. The repaired car is two triangles below the earlier delivery. Hidden gauge,
redundant guide chords and the grille backs fund the fair skins, supported
optical seats and rounder tires. Guide reduction measures every authored station
against its final chord; maximum error stays below 0.30 mm.
The embedded-texture GLB is **9,152,252 bytes**.

Four delivery surfaces match the pickup: **Paint, Opaque, Glass and Lamps**.
Separate recoloring/coat, transmission and switchable emission responses need
four materials; this is the brief-authorized exception to the three-material
preference. All four reference one three-map **2048²** set, baked at **4096²**:

- `T_AlderS240_BaseColor.png`: sRGB, with independent paint-coverage/lamp data in alpha.
- `T_AlderS240_Normal.png`: OpenGL +Y tangent normal.
- `T_AlderS240_ORM.png`: linear occlusion, roughness, metallic in R/G/B.

The set costs **16 MiB** with full mips at 8 bpp per map (for example BC7/BC5/BC7),
or 64 MiB expanded to three RGBA8 mip chains. Loading both cars costs about
32 MiB compressed. These bodies share methods, rather than atlas pixels.
A common family repack would require a coordinated change to the accepted pickup.

Porcelain, Carbon, near-neutral Graphite, Aluminum and Atlantic use the family's
coverage-delta decoder in [delivery_materials.py](src/delivery_materials.py):
linear `RGB + coverage * (factory tint - reference tint)`. It preserves colored
deposits without five texture copies. The standard GLB fallback is Atlantic;
other colors need that documented decoder, not a simple whole-material tint.
Spawn weights are 31/19/21/8/10 out of 89 from Axalta's 2025 North American new-car
color shares for these five choices; they are not used-fleet measurements.

The clearcoat's unresolved peel, flakes and hairline swirls are integrated into
the mean finish instead of point-sampled into a noisy normal atlas. Road film
rises softly from the rocker and follows elongated rearward tire wakes; it keeps
the paint's hue. Chips and residue stay at leading edges and actual shut lines.
Wear defaults to `--wear .65` on the detail generator.
ORM blue stores clean coverage before the factory metallic factor, so road
deposits retain a dielectric response in every color. The pickup preparation
and shader remain unchanged. Glazing is dark/transmissive with edge frit and
lower residue. Continuous carcass normals and 56 circumferential stations keep
the touring tires smooth; native-size molded type gets extra atlas space. Wheels
have a charcoal alloy response, caliper-centered brake dust and darker radial
tire dust.

BaseColor/ORM and shader normals bake directly on the prepared finalized skin.
Original coordinates survive UV packing. High-source normals replace direct
normals only where independent partwise rays pass; the bake report records the
coverage and neutral tangent fallbacks: 256 parts, or 7.77% of the atlas,
receive high-source normals. Grille vanes and arch returns use their direct
normals. Paint and glass use their continuous exported corner normals, without
an unresolved tangent-normal texture binding.

The final UV pass logs 31 repairs for overlapping or subtexel fragments. Its
direct bake has zero missing interior texels among 6,080,665 checked samples;
six backward tangent samples are neutralized by the documented hemisphere
fallback. UV coverage is **40.82%**, with zero overlap/outside/degenerate
triangles; measured p5/median/p95 density is **59.6 / 264.3 / 506.0 px/m**.
Hidden gauge receives less space; painted panels, tire sidewalls, plates and
markings receive extra density. A square UV context prevents source-image
aspect from stretching charts. The six planar marking charts have measured
UV Jacobian condition numbers below 1.00003; area-only density would miss that
failure.

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
stays **66.8–283.7 mm** through the range. Trunk goosenecks clear the backlight,
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
Across the measured grille mouth, 8,069 rays find zero painted obstructions
through its recessed well. This independently detects the old uncut triangles.
Front-cover chart orientation and rays along the real cover normals check the wrapped
optical seats. The open game arch returns have an additional 290-pose check of
exact tire intersections and solid containment; the solid-only sweep cannot
certify an open sheet. Sampled vertex distances are labeled as samples.

After changing the hood pose, re-aim each support frame toward its exported
`support_target` endpoint, as `supports()` in `src/sedan_lookdev.py` demonstrates.
The rigid members telescope; glTF does not serialize Blender tracking constraints.

### Rebuild and inspect

```sh
make -C cars BODY=sedan WIDTH=1600 SAMPLES=256
make -C cars BODY=sedan check
make -C cars BODY=sedan panel-diagnostics
make -C cars BODY=sedan form       # archived clay/stripes/overlay presentation
make -C cars                      # independent pickup delivery path
```

The default sedan graph fetches the recorded image/PDF references, builds both
source densities and markings, checks scale/topology/construction and motion,
packs/bakes/downsamples the atlas, exports/re-imports the GLB, renders the studio,
five colors, scale, Eevee, motion and used-car pairs, and creates five bounded
`sedan-` docs JPGs. Cycles work uses the shared GPU lock. No downloaded code or
additional packages are needed. This round changes no kit or pickup source file.

| Generated image location | Contents |
| --- | --- |
| `renders/sedan-detail/contact.jpg` | Cycles gallery and Eevee, all from the delivered GLB |
| `renders/sedan-detail/turnaround.jpg` | Front, side, rear, top |
| `renders/sedan-detail/details.jpg` | Grille/lamps, wheel, cabin through glass |
| `renders/sedan-detail/factory-colors.jpg` | Five colors, front and rear three-quarters |
| `renders/sedan-detail/scale.jpg` | Real-scale car and 1.8 m human silhouette |
| `renders/sedan-motion/*-sweep.jpg` | Five poses each for doors, hood, trunk, steering, wheel spin |
| `renders/sedan-used-pairs/` | Sun/sky-matched, white-balanced used-class pairs and measured patches |
| `renders/sedan-panels/*-comparison.jpg` | Actual GLB curvature and both reflection directions, seven views including face and wheel |
| `renders/sedan-panels/source/` | The same expanded measurements and views on the source |
| `renders/sedan-surface-repair/` | Captured native-size earlier/revised delivery crops and their camera/provenance record |
| `renders/sedan-eevee/` | Eevee export view |
| `renders/sedan-detail/checkpoint.jpg` | Combined gallery, pairs and motion review |

The used-photo lighting uses a procedural scattering sky and an estimated 27°
front / 30° rear sun, with approximately ±6° elevation uncertainty. Asphalt and
original facade reflectors supply the observed ground/building reflections.
No studio softbox is present in the matched pairs. Their assumed-neutral white
balance uses front plaster and a background white-car trunk; neither is a gray
card. Patch values measure displayed appearance, including lighting, shape and
class differences, rather than material albedo. Final figures are in
`renders/sedan-used-pairs/appearance-patches.json` and [REVIEW.md](REVIEW.md).
The front upper-door median is RGB **150/148/148** against **153/147/151**;
rear upper door **125/126/128** against **121/119/131**. Across ten paint/wear
patches, median absolute displayed-luma difference is **12.8/255**, worst
**29.4/255** on the rear quarter's sky reflection. Source/export pairs and
their separate bake-loss measurements regenerate with the default build; the
maximum measured patch-channel bake difference is 1/255.

### Limits and credits

The accepted wheelbase-scaled side overlay retains its reported class mismatch:
118.8 mm front / 71.8 mm rear raw holdout extremes. Those are not hidden by
fitting the body outline. Construction is original; the reference cars have
different optical graphics and panel shapes. Broad door/quarter reflections do
not match every photographic patch. The estimated procedural surroundings are
simpler than the photographed building. Raw curvature/stripes expose remaining
cut-cell and tire-section discretization under extreme inspection lighting.
Hard mirror/wheel bevels, simple cabin/underbody forms and rear optics remain
the main CG tells. Molded tire type stays faint and some small text is soft at
macro distance. Eevee transmits less nested glass depth than Cycles.

Reference photographs and manufacturer specifications: authors, URLs, licenses
and exact uses in [refs/SOURCES.md](refs/SOURCES.md). Markings use installed Noto
Sans under the SIL Open Font License. All geometry, shaders and graphics are
original scripts; photographs remain comparison material in ignored folders.
