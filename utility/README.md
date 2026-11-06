# Rill / wood utility poles and overhead lines

Original scripted US residential distribution, maintained 1970–2010 equipment
with 15–30 years of service age. This checkpoint adds the measured cable
envelopes, seeded communication plant, causal surfaces, a shared Cycles-baked
atlas and external-image glTF delivery to the accepted construction.

After `make`, inspect [the hero](renders/final/101/hero.png),
[dusk](renders/final/101/dusk.png), [all views](renders/final/contact.jpg),
[four streets](renders/final/four-streets.jpg),
[construction](renders/final/construction.jpg),
[matched-light pairs](renders/final/matched-pairs.jpg), and
[exact wire ranges beside photos](renders/wires/photo-distance-pairs.jpg).
[Native before/after crops](renders/fixes/comparison.json) each retain at least
800 pixels per panel. These are rebuilt, ignored outputs; no docs images are
committed this round.

[REFERENCE.md](REFERENCE.md) distinguishes published dimensions from authored
choices; [REVIEW.md](REVIEW.md) records the critique rounds and remaining
limits; [refs/SOURCES.md](refs/SOURCES.md) records authors, rights and URLs.

## Construction and scale

Southern yellow pine, **ANSI class 4**, linear taper and bare cut top. WPS
P25/P30 and the published ANSI O5.1-2008 table supply the dimensions.

| Overall / set depth | Exposed height | Circumference 6 ft from butt | Top circumference |
| --- | ---: | ---: | ---: |
| 35 / 6 ft | 8.8392 m | .8001 m / 31½ in | .5334 m / 21 in |
| 40 / 6 ft | 10.3632 m | .8509 m / 33½ in | Same |
| 45 / 6½ ft | 11.7348 m | .8890 m / 35 in | Same |

The exported polygon perimeters are measured, including the below-grade
reference station on the 45-ft pole. Only a 120 mm insertion stub is geometry.
Pole origins sit at grade at the shaft center. No climbing steps are supplied.

A fictional **12.47/7.2 kV grounded-wye** system uses WPS-informed crossarm
and armless framing. Arms are 2.4384/3.048 m long, .09525 × .12065 m in
section, with steel braces, bearing washers and ⅝-in through-bolts. Gray
ANSI 55-3 porcelain has a 120.65 mm shed and 95.25 mm body height; seeded
armless poles use polymer posts. The MPS-informed 50 kVA can has a 508 mm
tank and 1,066.8 mm bottom-to-HV-terminal height, rolled lip, lifting eyes,
hangers, grounded cutout/arrester equipment and separate leads.

The three-can pole has three primary phases and three independent 120/240 V
secondary circuits. Center A supplies the sample houses; B/C retain distinct
service sockets. This is a mechanical bank, without a three-phase secondary
interconnection diagram. Each riser phase has its own sealed termination.
Dead ends and angles carry 9.525 mm guys, 15.875 mm anchor rods and 2.4384 m
hollow yellow guards. The street-light bracket uses a 60.3 mm tube and 2 m
reach; its separate library head is presentation only.

## Wires and the four streets

| Conductor | True envelope | Source / construction |
| --- | ---: | --- |
| Primary | 10.1092 mm | Southwire Raven 1/0 6/1 ACSR |
| Neutral | 8.0264 mm | Southwire Sparrow #2 6/1 ACSR |
| Triplex hots / messenger | 7.6962 / 6.35 mm | Classic Wire #4 Periwinkle, triangular constituent packing |
| Telephone | 37 mm | Published 200-pair .63 mm GR-421 envelope |
| CATV | 24.384 mm | QR860 jacket, separate 6.35 mm strand |
| Fiber bundle | 2 × 15.8 mm, 31.6 mm wide | Two touching jackets, separate 6.35 mm strand |
| Retained copper | 28 mm | Published 100-pair .63 mm GR-421 envelope |

Three primary phases and one neutral, or one phase and neutral, remain as
accepted. Communication counts are independent supported routes: telephone,
CATV, optional paired fiber, optional older copper. The 680 × 144 mm splice
case has clamps and returning slack loops. The triplex mass correction to
.227692 kg/m preserves the accepted sag by scaling horizontal tension.
All tension examples are authored self-weight states, not stringing tables.
Telecom forces scale with load to retain the accepted .24 kg/m / 900 N
catenary shape: 6,641.25 / 1,612.5 / 1,350 / 4,256.25 N for phone / CATV /
paired fiber / retained copper. Different sag ratios had brought neighboring
routes into contact. An independent section audit now measures at least
.226 m free vertical space between actual exported route envelopes across
84 sampled planes per communication street.

| Seed | Town / framing | Nominal span | Communication routes | Utility triangles |
| --- | --- | ---: | ---: | ---: |
| 101 | Older grid, 40 ft, three-phase crossarm | 140 ft | 3 | 46,108 |
| 102 | Postwar feeder, 35 ft, one-phase armless | 110 ft | 2 | 37,780 |
| 103 | Commercial edge, 45 ft, three-phase crossarm/bank | 185 ft | 0 | 41,734 |
| 104 | Later suburb, 40 ft, three-phase armless, shallow jog | 160 ft | 4 | 48,420 |

Each street has five poles and twelve optional service-mast attachments.
Geometry budgets exclude presentation context. The library houses face both
sides; native roads, walks and curbs continue beyond frame. Mature red maple
and pin oak occupy yards and strips, with crowns near the line corridor.
Original library pickups have three source paint variants; original light
heads and house windows receive a dusk presentation state. All context is
staged under `utility/build/context/`, using the neighboring families' own
source shaders; only utilities are delivered here as baked external glTF.

The hero uses a measured 1.68 m eye above the sidewalk and 35 mm lens, with
raking sun. Dusk uses a procedural blue-hour sky, powered heads and windows.
No downloaded lighting or assets enter any output.

Displayed line contrast is `(sky Y′ − line Y′) / sky Y′`, median of
61 transverse profiles in undenoised 1600 × 800 Cycles controls, 50 mm lens.
These are actual exported tubes or the evaluated far recipe, with a separate
empty-sky control for each exact horizontal range. Full profiles, linear-light
contrast and integrated deficits are in `renders/wires/contrast.json`.

| Range | Primary tube / ribbon | Telephone tube / ribbon | CATV tube / ribbon |
| --- | ---: | ---: | ---: |
| 30 m | 33.2 / 37.7% | 87.8 / 99.4% | 79.6 / 90.3% |
| 60 m | 10.5 / 15.5% | 51.1 / 53.8% | 34.1 / 34.7% |
| 120 m | 3.8 / 7.6% | 21.3 / 23.9% | 14.9 / 20.5% |

The photographs have **no surveyed line depths**. Their native near / middle /
far bare-line samples measure NC **11.0 / 9.7 / 6.8%**, Maryland
**23.1 / 23.6 / 24.7%**; separate jacket samples measure Maryland **60.1%**
and the hardware photo **83.7%**. The latter's profile follows the cable centre,
clear of the splice case; the earlier off-centre selection was rejected.
These bracket photographic visibility; they do not establish a literal
30/60/120 m photographic survey. Sky, lens, resolution and wire orientation
also differ. The 120 m primary still needs the documented engine policy:
physical tubes alone are insufficient for that view. The far policy restores
approximately the NC far sample's displayed contrast while retaining true
socket diameters and physical near geometry.

## Surfaces and delivery cost

One **2048² BaseColor / OpenGL +Y Normal / ORM** set, baked at 4096.
Sixteen guarded stock charts intentionally reuse UVs across parts. Two pine
charts carry silvered gray-brown grain, longitudinal checks, uneven wet/green
ground-line absorption, darker cut ends, bolt runoff and sign-removal scars.
Fir grain follows the arm; coherent waviness and knots avoid ruled grooves.
Paint chalks on exposure, with runoff starting at lift-eye welds/lid seam and
staining retained at the bottom. Zinc ages at cut edges and seats; dielectric
sheds retain lower-lip dust. Guard yellow fades on exposure and scuffs near
grade. Fictional RILL/RV marks share the atlas and conform to the real facets.
`WEAR=1` is the service-age default; it is a causal-mask strength, not a
uniform overlay. Selected seeds retain sparse rooted vines and old staples.

| Material / parts | Maps | Why retained / draw calls |
| --- | --- | --- |
| `Utility`: pole, arm, transformer, mounting hardware, guy/guard/anchor, case, labels, optional mast | Shared trio | One PBR material and one primitive per fixed assembly; material variation is in the atlas |
| `Utility_Aluminum`: primary, neutral, messengers | None | Oxidized bare conductor response differs from jacket; one primitive per merged conductor group |
| `Utility_Cable`: telecom, service hots, drops | None | Near-black PE/XLPE needs its own rough dielectric response; one primitive per merged group |

The parts library has one material and nine primitives. Blocks have three
materials and **27 / 27 / 24 / 27 primitives**, including twelve optional
masts; the mixed service and telecom groups each have two primitives. There
is no armature or moving mechanism. Fixed parts can be instanced or batched
by an engine; these counts describe ordinary imported glTF draws.

| Reusable module | Triangles | BIN payload bytes | Materials / primitives |
| --- | ---: | ---: | ---: |
| Tangent / angle | 3,632 each | 274,704 / 274,896 | 1 / 1 |
| Dead end | 3,056 | 223,104 | 1 / 1 |
| Transformer pole | 6,668 | 496,056 | 1 / 1 |
| Three-phase riser | 4,356 | 319,704 | 1 / 1 |
| Street-light bracket pole, excluding head | 4,024 | 302,064 | 1 / 1 |
| Crossarm module | 1,248 | 103,872 | 1 / 1 |
| Standalone transformer module | 3,036 | 221,160 | 1 / 1 |
| Guy / guard / anchor | 280 | 20,592 | 1 / 1 |
| Optional service mast | 1,088 | 70,656 | 1 / 1 |
| Placed three-can pole, seed 103 | 8,438 | 690,228 | 1 / 1 |

Per-part BIN bytes sum the actual buffer views referenced by each mesh,
including indices and vertex attributes. Shared maps, socket metadata and
scene JSON are counted separately below. The optional mast is a named part
of each street package; the bank is seed 103's `P3` assembly.

Optional light/communication/vine combinations differ: seed 101's fullest
single-can pole is 7,212; the four-route armless seed 104 reaches 7,468.
The latter spends 256 more triangles on the requested extra communication
plant. The fullest riser is 4,508, below its accepted 4,528. All blocks remain
below 49k, funded by tighter catenary stations and repeated mast sampling,
with the same 8 mm/4 m curve screens. Individual tubes use 24–120 triangles
in these layouts; `build/checks.json` records every span.

External delivery is `export/UtilityParts.gltf` plus four
`export/UtilityStreet-<seed>.gltf`, their `.bin` geometry and `.json` sockets.
Every file points to the same `export/textures/` trio; images are losslessly
retained from the bake. Loading all five actually creates three image
datablocks, not five independent sets. Internal `build/*.glb` checkpoints
remain available for exact serialization checks.

| Package | glTF + BIN bytes | Optional socket/curve JSON bytes |
| --- | ---: | ---: |
| `UtilityParts.gltf` | 2,269,663 | 19,214 |
| `UtilityStreet-101.gltf` | 2,926,088 | 211,643 |
| `UtilityStreet-102.gltf` | 2,422,331 | 153,086 |
| `UtilityStreet-103.gltf` | 2,780,085 | 145,517 |
| `UtilityStreet-104.gltf` | 3,023,912 | 240,916 |

The shared PNGs total **9,375,154 bytes** (BaseColor 3,452,511, Normal 4,930,357, ORM 992,286). Count this trio once when combining packages. All five glTF/BIN geometry
payloads total **13,422,079 bytes**; optional JSON sidecars add 770,376 bytes.

The three maps cost **16 MiB** with three 8-bpp block-compressed maps and
full mip chains, shared across all instances/seeds. This is an engine memory
estimate, not PNG disk size; uncompressed RGBA8 with mips is about 64 MiB.
The tall shaft and readable near-ground marks justify 2048; the chart audit
reports an area-weighted shaft density near 346 px/m, with greater allocation
for small markings and hardware. Reused UVs are intentional and tested as
guarded stock charts, not falsely reported as a unique nonoverlapping unwrap.

## Sockets, parts and game use

Meters, Blender +Z up, street run +Y, asset front −Y; glTF maps `(x,y,z)` to
`(x,z,-y)`. The parts library is `export/UtilityParts.gltf`; replace a part root's
inspection-layout transform. Pole grade remains local zero. Crossarm origins
are their central mounting-bolt datum; transformer origins are the pole-line
mount frame at tank-bottom height; guy origins use the pole grade datum.
Those mounted modules intentionally use installation frames rather than
standalone ground-prop centers.

Every pole carries `<root>__Socket_<name>` empties with `socket_kind`:

| Socket | Role |
| --- | --- |
| `Primary_A`, optional `Primary_B/C` | Actual tangent saddles or deadend clamps |
| `Neutral` | Neutral spool's outside bearing line |
| `Service` | Central triplex strain clamp; optional bank `Service_A/B/C` are distinct circuits |
| `CommStrand`, `LashedFiber_0/1`, `Telephone`, `CATV`, optional `LegacyCopper`, `<route>Strand`, `CommDrop` | Each long conductor and the house drop |
| `GuyUpper` | Upper guy eye |
| `CrossarmMount`, `TransformerMount` | Installation frames for reusable equipment |
| `Riser_Primary_A/B/C`, `RiserUnderground` | Sealed phase terminations and underground entry |
| `LightBracket`, optional `LightHead` | Bracket pad and head slipfitter; local −Y points toward the street after a +90° Z rotation |

`export/UtilityStreet-<seed>.json` records complete Blender world coordinates and
construction parameters. House mast roots carry `ServiceDrop` and
`CommunicationDrop`. `build/house-attachments-<seed>.json` is the optional
sidecar: local coordinates, instance transform, house type/seed and ray-measured
roof-guy anchor points. The mast's lower elbow enters the wall; an internal
route to the original meter is reserved, not modeled in the exterior shell.
No second meter, altered house mesh, house export or changed house script.
The render-context check also ray-tests the anchors against the actual posed
library house meshes, catching presentation rotations as well as modeling
errors. It does not substitute an intended transform for the visible geometry.

The pure-Python API works without Blender; add `utility/src` to the import path.
It uses +Z up. Convert imported engine coordinates `(x,y,z)` to `(x,-z,y)`
before calling it, then convert the result back with `(x,z,-y)`:

```python
from span import sample, sag_from_tension

# Transform imported socket positions into one common world frame first.
points, report = sample(start_socket, end_socket, sag=0.8)
# Or calculate a self-weight case from horizontal tension:
sag = sag_from_tension(start_socket, end_socket,
                       mass_kg_m=0.2158, horizontal_tension_n=550)
```

`sample` handles unequal supports, solves the actual catenary, and adaptively
subdivides to 8 mm chord error / 4 m maximum steps. Its arc length and minimum
height are included in the report. `construction.conductor` creates the Blender
tube. For an engine, sweep a four/six-sided section along the points, or use
`ribbon.data(points, diameter)` for the far mesh. Sag is below the chord at
horizontal midspan; it is not the absolute elevation of the lowest point.

At distance use the original `src/wire.gdshader` and `ribbon.data`: a camera-facing
.85-pixel floor, opacity `(true_width / widened_width)^.55`. Exponent 1.0
is strict integrated coverage; the calibrated .55 default retains more optical
contrast. Neither changes a socket's true diameter. Transition from physical
tubes below about .8 px projected width, retain tube shadows, apply object
scale, convert positions/tangents, and expand the runtime AABB. Cross-fade
without drawing both at full opacity. Use two shared far-material instances:
linear bare RGB (.012,.013,.012), jacket (.0015,.0017,.0015). The example
uniform deliberately takes linear vectors without `source_color`; the
[Godot color-uniform documentation](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#using-source-color)
explains the sRGB conversion applied by that hint. The numeric inputs match
the Cycles inspection; an engine tone mapper will still alter displayed
contrast. This requires no texture. Godot
compilation, moving-camera AA and performance remain untested; the Cycles
inspection is evidence of the policy, not proof of an engine integration.

## Rebuild and evidence

```sh
make -C utility clean
make -C utility
make -C utility check
make -C utility repeat
python3 kit/repo_check.py
```

Installed Blender 5.2, Python/NumPy/Pillow and open fonts; one Blender process
at a time, four CPU threads, and the shared GPU lock for Cycles. Nothing is
installed or downloaded as code. Reference cache remains through `clean`.
`make` rebuilds original fields, the Cycles bake, parts/blocks, external
delivery, physical/serialization checks, 22 Cycles views, three matched-light
pairs, exact wire-range controls, Eevee hero and native before/after crops.

`build/checks.json` measures actual shaft sections, planting-strip footprints,
wire surfaces, clipped road minima, interspace gaps, actual inter-route
triangle sections and roof overflight rays.
`build/delivery-check.json` separately proves external payload equality, UV
chart allocation/density, normal/tangent validity, conforming label contact,
socket re-import and three-image cache reuse. `build/repeat-check.json` records
a fresh geometry export, all original fields, and independent GPU rebake.
All five GLBs and 48 source fields reproduce byte for byte. In the final
independent bake, BaseColor and ORM match exactly; Normal differs in one
channel sample by one 8-bit level (RMSE .000282/255), within the stated GPU
bake tolerance. The shipped maps remain the canonical original bake.
The Eevee checkpoint losslessly packs six house-context scalar masks into
two RGBA attributes and prunes unreachable shader branches to avoid its
vertex-attribute limit. Measured packing roundtrip error is zero; no utility
material or neighboring source is changed. Seven independent span controls pass. These checks establish construction
and serialization; only the full-size
images and photographic comparisons assess appearance.

Minimum supply/communication gap is about 1.228 m. The lowest private service
surface is 5.193 m; comm drop is 4.397 m. Actual road-clipped minima exceed
the selected 18-ft service / 15½-ft comm screens. Current layouts avoid roof
overflights. These are level-terrain authored tension cases, without
structural, ice/wind or all-weather certification.

No kit or neighboring family source/delivery is changed. Existing neighboring
generated deliveries were absent on takeover, so the recorded preservation
snapshot has zero files; no neighboring output path is written. The top-level
README stays with the lead. Photo dates after 2010 describe older maintained
plant and are not asserted as installation-period evidence.

The three photographic camera fits have RMS residuals of **6.51 / 6.19 /
9.74 px** (NC street / Maryland top / full communications portrait). The
held-out telephone-height shaft centre is **2.17 px** from the observed
point. The portrait is native 749 × 1640; both review crops are 570 × 370.
Upper-arm and shaft controls do not assert an exact can/case/span-layout fit.

Remaining limitations: photographic can height, case placement and span
azimuth differ from the selected construction. The close wood fibres are
soft at the shared atlas density; fine rust and scars remain subtle in the
full street hero. The sparse vine silhouette is angular. Four-sided tubes have a directional width compromise and need
the far policy at distance. Helical triplex and long-span lashing are below
this mesh budget. Repeated house/tree/pickup context, simplified lawns and
cloudless procedural skies still read as CG. The runtime shader needs an
engine compilation/motion-AA check. No docs images are committed this round.
