# Alder H120 — surface checkpoint

An original compact five-door hatchback in the 2018–2022 class. The accepted
round-four form now has its working closures, original exterior hardware,
five-seat cabin, cargo well, FWD underside and five daily-driver finishes.
The surface round replaces the folded optical molds, resolves paint-normal
aliasing, rebuilds the grille and tire carcasses, and seats the arch liners.
This stops at the requested review checkpoint; no final hatch gallery JPGs
are committed.

![Five factory finishes](renders/hatch-checkpoint/five-colors.jpg)

[Contact sheet](renders/hatch-checkpoint/contact-sheet.jpg) ·
[Details](renders/hatch-checkpoint/details-contact.jpg) ·
[Opening poses](renders/hatch-checkpoint/motion-sweeps.jpg) ·
[White-balanced front pair](renders/hatch-checkpoint/used_front-measured.jpg) ·
[White-balanced rear pair](renders/hatch-checkpoint/used_rear-measured.jpg) ·
[Surface comparisons](renders/hatch-checkpoint/compare-five-colors.jpg) ·
[All-surface curvature](renders/hatch-checkpoint/surface-proofs/curvature-contact.jpg) ·
[Horizontal stripes](renders/hatch-checkpoint/surface-proofs/horizontal-contact.jpg) ·
[Vertical stripes](renders/hatch-checkpoint/surface-proofs/vertical-contact.jpg) ·
[Eevee](renders/hatch-eevee/front_three_quarter.png) ·
[Critique log](REVIEW.md#h120-detail-and-look-checkpoint)

Each same-framing region retains the earlier exported checkpoint beside the
new one. The original source hash and exact crop rectangles are recorded in
`surface-comparisons.json`.

| Region | Before / corrected |
| --- | --- |
| Headlamp molded lens | [Pair](renders/hatch-checkpoint/compare-lens.jpg) |
| Hood reflection | [Pair](renders/hatch-checkpoint/compare-hood.jpg) |
| Quarter and compound fuel flap | [Pair](renders/hatch-checkpoint/compare-rear-quarter.jpg) |
| Front arch / liner | [Pair](renders/hatch-checkpoint/compare-front-arch.jpg) |
| Tire carcass and molded lettering | [Pair](renders/hatch-checkpoint/compare-tire.jpg) |
| Open grille lattice and badge | [Pair](renders/hatch-checkpoint/compare-grille.jpg) |
| Lower face / pocket blank | [Pair](renders/hatch-checkpoint/compare-fog-pocket.jpg) |
| Complete face | [Pair](renders/hatch-checkpoint/compare-face.jpg) |
| Rear glazing in studio | [Pair](renders/hatch-checkpoint/compare-rear-glass.jpg) |

Curvature and both stripe directions cover nine views each, including glass,
lenses, grille, lamps, arches and rubber. The GLB maps weld only coincident
diagnostic vertices at UV seams; exported geometry is never modified. Joined
GLB meshes discard stale inherited per-part face counts and measure all faces,
including gauge. Source maps retain authored outer-skin roles. Gray marks
true incomplete boundary neighborhoods, not filtered curvature outliers. The
[source curvature](renders/hatch-source-surface-proofs/curvature-contact.jpg),
[horizontal source stripes](renders/hatch-source-surface-proofs/horizontal-contact.jpg)
and [vertical source stripes](renders/hatch-source-surface-proofs/vertical-contact.jpg)
remain separate from the 27 exported diagnostics. Raw signed curvature and
cut-boundary outliers are retained, without smoothing or outlier removal.

## Accepted form and package

[HATCH_FORM.md](HATCH_FORM.md) preserves the complete accepted report: profile
overlays and residuals, measured sections and lines, gloss clay, raw curvature
maps and both makes' comparison views. `STAGE=form` rebuilds that graph. None
of the new appearance cameras replaces its accepted profile calibration.

| Measurement | H120 | Basis |
| --- | ---: | --- |
| Length × body width × body height | 4363.0 × 1796.5 × 1450.6 mm | Accepted original package; manufacturer class sources in REFERENCE.md |
| Mirror span | 2039.3 mm | Accepted measured span; Hyundai UK sheet 2039 mm |
| Overall height with antenna | 1505.0 mm | Detailed mesh bounds |
| Wheelbase | 2650 mm | Accepted axle package |
| Front / rear track | 1550 / 1560 mm | Actual wheel pivot positions |
| Tire / alloy | 225/40R18 / 18 × 7.5 | 629.2 mm rolling envelope; 190.5 mm bead seat |
| Tire-to-arch gap | 40 mm | Accepted outer arch and rolling radius held |
| Lowest underbody surface | 146.5 mm above ground | Actual authored underside vertices, independent of serialization |

No parent control-net refit was made. Local game reflection samples and
continuous shading normals follow our accepted evaluated parent. The surface
round additionally samples the hood, rear quarters and front arch fascia where
reflected-normal interpolation changes fastest; retained exterior cut boundaries
stay held. Independent parent residuals and rejected repair attempts are logged
in REVIEW.md. The fuel flap now has a compound disk aligned to the shoulder.
The hidden spoiler foot is seated above the roof, and steering liners/inner
returns move inside the accepted outer arch. A tiny fixed front glazing sail
is split from the moving window along a 2 mm bonded reveal. Original form
artifacts remain separate from these detailed construction changes.

## Parts and mechanisms

The grille has an open gloss-black diamond lattice, a deep matte cavity,
a dark-chrome surround and an original Alder badge on a seated carrier. The
lower intake has a finer lattice of its own; formed corner pockets carry
seated molded blank inserts with recessed slots. Projector bowls, optics,
white guides and amber elements sit inside the swept headlamps; rear guides
and red covers follow the accepted lamp cuts. The source and imported renderer
switch the lamp emitters without replacing textures. Wipers front/rear,
washer nozzles, handles, window trims, black B pillars, fuel flap, antenna and
fictional rear badges complete the exterior. The framed promotional insert
reads **ALDER / WILLOW MOTOR CO. / ALDER AUTHORIZED RETAILER**, with no state or
registration format.

Five compound-section seats, dash/cluster/screen, console/shifter, steering
wheel, door cards and headliner are visible through the glass. The rear has
a carpeted cargo well, wheelhouse trim, load sill and parcel cover. Underneath
are stamped rails/floor, subframes, front halfshafts, suspension, fuel tank,
catalyst, exhaust and a hollow rolled outlet at the accepted left cutout.
The underside and cabin are deliberately less detailed than the exterior.

Coordinates below are meters in Blender: +Z up, front −Y, origin at the center
of the footprint on the ground. Positive rotations follow the listed axis.

| Node | Pivot / axis | Range |
| --- | --- | --- |
| Door_FL / Door_FR | (∓0.838, −0.902, 0.740), normalized (∓0.10, 0, 1) | left 0…62°, right −62…0° |
| Door_RL / Door_RR | (∓0.820, +0.225, 0.740), normalized (∓0.10, 0, 1) | left 0…66°, right −66…0° |
| Hood | (0, −1.080, 0.977), X | −62…0° |
| Liftgate | (0, +1.455, 1.385), X | 0…82° |
| Wheel_FL / Wheel_FR | (∓0.775, −1.255, 0.3146), local X | full revolution, tested 0…360° |
| Wheel_RL / Wheel_RR | (∓0.780, +1.395, 0.3146), local X | full revolution, tested 0…360° |
| Steer_FL / Steer_FR | (∓0.710703, −1.264156, 0.3146), local Z | −35…+35° |

Front kingpin axes in vehicle space are (±0.257266, 0.109393, 0.960129): 15°
SAI, 6.5° caster and −20 mm scrub, original design choices rather than recovered
manufacturer geometry. Formed hinge leaves, bored sleeves, welded backing
pads and jambs give the doors real support. Roof pins/ears carry the liftgate.
Two gas supports carry each of the hood and gate, with actual ball brackets
on the relevant skins/frame. Their cylinders aim at exported endpoint nodes;
`hatch_lookdev.supports()` re-aims them after a runtime pose. No armature is used.

The kit sweeps all twelve motions on game and high sources at 0.5 mm tolerance:
2° closures, 10° wheel spin and 1° steering. Independent one-degree coupled
spring sweeps supplement the kit's cached fixed geometry. Forty-two measured
support pairs pass. Minimum rod engagement is 35.9 mm hood / 78.0 mm gate on
the game mesh; minimum bottom clearance is 114.1 / 12.6 mm. The largest within-tolerance sampled intrusion is 0.451 mm; all
four wheel-spin and both steering sweeps measure zero. These prove sampled
construction and travel, separately from GLB serialization. They are not a
continuous collision proof. Fuel flap and parked wipers are static accessories
at this checkpoint; the explicitly requested closures and wheels articulate.

## Budget and finishes

| Part category | Game triangles |
| --- | ---: |
| pillars | 1,356 |
| glass | 2,508 |
| doors | 3,653 |
| body | 12,634 |
| fascia | 9,152 |
| arches | 752 |
| liners | 1,168 |
| openings | 3,036 |
| lamps | 3,376 |
| mirrors | 1,016 |
| spoiler | 1,184 |
| tires | 3,584 |
| wheels | 3,544 |
| brakes | 1,120 |
| trim | 3,531 |
| interior | 3,600 |
| cargo | 260 |
| underbody | 1,792 |
| hinges | 1,912 |
| **Total** | **59,178 / 60,000** |

The accepted detail checkpoint was 59,989 triangles. The surface round spends
on optical molds, compound paint sampling and a geometric grille by simplifying
only measured hidden gauge and covered door backs, and the tires' inboard
section. Visible cabin, cargo, underbody and hinge categories are held.
`build/hatch-detail/game.counts.json` lists every mesh and immediate moving parent.

One H120 set, separate from the pickup: `T_AlderH120_BaseColor.png` (sRGB RGBA),
`T_AlderH120_Normal.png` (OpenGL +Y), and `T_AlderH120_ORM.png` (AO/roughness/metal).
Baked at 4096 and shipped at 2048. BC7/BC5-class 8-bpp compression with full
mipmaps costs approximately **16 MiB** for all three maps; three RGBA8 runtime
allocations with mips would cost 64 MiB. PNG/GLB file bytes are not GPU memory.

The family uses four delivery surfaces: Paint, Opaque, Glass and Lamps. This
retains the family's documented material exception for independent clearcoat,
transmission and lamp emission over one atlas. Original source materials
consolidate into those four; source shader count is not the runtime draw cost.
Five factory factors (Porcelain, Carbon, Graphite, Aluminum, Atlantic) decode
coverage alpha over the shared Atlantic fallback, preserving dirt's own hue.
The weights follow the selected five North American production colors,
normalized to 31:19:21:8:10, not a used-fleet census.

Paint uses a smooth clearcoat, undercoat metallic response where appropriate,
and wash marks in roughness. The source's micron peel/flake height is unresolved
at the shipped density, so the delivered normal atlas excludes that aliased
detail. Paint and Glass export normal strength zero, retaining the authored
continuous normal fields without 8-bit neutral-map deflection. Glass has frit and
lower-edge residue. Rubber, glossy grille, dark chrome, painted alloy and
black molded trim have distinct responses. Low road film follows wheel wakes
and height, chips follow door hems/hood leading edge, grime follows gaps and
lamp edges, brake dust follows the caliper region outward, and luggage abrasion
stays on the rear bumper shelf. `WEAR=.65` is the checkpoint daily driver.

The verified GLB is **7,945,496 bytes**, with 21 meshes / 36 material primitives.
It embeds exactly three 2048 images: Normal 1,180,948 B, ORM 1,864,053 B,
BaseColor 844,383 B. Maximum re-import rest-position error is 0.342 micrometers;
pivot matrix error is 2.38e-07. UV coverage is 38.99%, with zero overlapping,
outside or degenerate triangles. Measured 5th / median / 95th density is
74.5 / 226.4 / 380.6 px/m. Forty-six logged UV repairs retain the thin cut
fragments through float32 export; no geometric vertex moves for a UV check.

Prepared material channels bake directly on the finalized game surface:
**5,714,185 checked interior texels, zero misses** in every channel.
Partwise rays approve 219 higher-detail hardware/tread/cabin parts for normal
projection. Smooth glazing and paint use authored surface normals; micron
paint height is excluded from the shipped field. glTF normal scale is **0**
on Paint and Glass, **1** on Opaque and Lamps. This prevents a quantized
neutral map from perturbing smooth refractive/reflective surfaces. Reversed
hardware projection texels and chart edges keep the direct normal. The raised
original tire lettering retains a faint causal dust deposit after minification.
The high source has 157,002 triangles.

GLB SHA-256: `9f4a4c6c13bb47b5e1af51840a54aa07db1c6e78491c4621095f8243f5f9fca0`.

The final Cycles heroes have asset luma p1 / median / p99 of
**0.0 / 46.3 / 248.9** front and **0.3 / 45.8 / 248.9** rear. Both have zero
clipped channel samples. Factory-color heroes have at most 0.0013% of channel
samples at 254 or above. The accepted −2.5 studio exposure is unchanged.
Eevee has darker glass and 0.0261% clipped channels. All 61 native views and
per-view tone statistics are in `tonal-range.json`.

## Matched-light appearance

The references are Elise240SX's MY2018 white compact hatchback photographed
2022-08-06, registered with original URLs and CC BY-SA 4.0 in
[refs/SOURCES.md](refs/SOURCES.md). Manufacturer dimensions, neutral patches,
lighting assumptions and color-report attribution are in [REFERENCE.md](REFERENCE.md).
No photo contributes a model vertex, material texel or environment map.

Four wheel anchors per image constrain the cameras with a stated 1.50 ± 0.15 m
height prior: native RMS is 9.24 px front / 9.76 px rear, estimated focal lengths
88.7 / 71.2 mm. Blender projection agrees with the solver within 0.004 px.
Diffuse photo shadows do not recover a unique sun. The pair setup uses a
procedural multiple-scattering sky, a broad weak sun estimated at 24° elevation
(±15°), and asphalt-gray ground. The rear pair additionally has a narrow bright
procedural facade in the glazing rays, estimated from the surrounding building
sector. Its dimensions, linear albedo and pose are recorded in shot metadata;
it never enters the exported car. No studio lights remain in either pair.

White balance uses the front white siding and rear gray garage mullion in
linear light. Patch values below are displayed luma on a 0–255 scale, not
recovered paint albedo or roughness. The panels and environments differ;
annotated patches, raw RGB, p10/p90 ranges and all gains remain in
`renders/hatch-checkpoint/pair-values.json`.

Front linear RGB gains: **1.0453 / 0.9788 / 0.9788**; rear:
**1.0416 / 0.9689 / 0.9923**. The earlier front patch contaminated by vegetation
is rejected in REVIEW.md.

| View / patch | Balanced photo | Exported GLB | GLB − photo |
| --- | ---: | ---: | ---: |
| front / upper front door | 162.6 | 156.2 | -6.4 |
| front / front road film | 144.5 | 140.4 | -4.1 |
| front / rear door | 163.0 | 155.2 | -7.8 |
| front / rear road film | 142.9 | 142.3 | -0.6 |
| front / front glass | 72.2 | 74.8 | +2.6 |
| front / windshield | 123.8 | 114.1 | -9.7 |
| front / tire sidewall | 22.8 | 32.8 | +10.0 |
| rear / upper front door | 172.8 | 171.6 | -1.2 |
| rear / front road film | 156.5 | 157.4 | +0.9 |
| rear / rear door | 177.2 | 175.6 | -1.6 |
| rear / rear road film | 160.9 | 164.8 | +3.9 |
| rear / front glass | 123.7 | 121.6 | -2.1 |
| rear / backlight | 121.2 | 122.0 | +0.9 |
| rear / tire sidewall | 27.0 | 48.9 | +22.0 |

Rear side-glass improves from **+38.2 to −2.1** levels; backlight from
**−47.7 to +0.9**. The photo's p10–p90 intervals are 121.7–133.2 side and
118.4–124.1 backlight. Delivered values are **121.6 / 122.0**: the side is
0.1 below the lower decile, and the backlight is inside its interval. The rear
sky strength's final 2.2% increase (.225 to .230) centers the backlight while
retaining the accepted studio and paint factors; sun energy remains 3.25.
The narrow facade and clearer transmission explain the large correction, while
zero normal scale and matching 1.52 IOR remove the export-side deflection.
These are displayed patch values under estimated context, not recovered glass
albedo. Front windshield (−9.7) and tire patches (+10.0 front / +21.0 rear)
remain weaker matches; the rear tire patch also has a broad photo range that
includes part of the bright rim. Source measurements remain separate in
`renders/hatch-source-pairs/pair-values.json`.

## Rebuild and evidence

```sh
make -C cars BODY=hatch
make -C cars BODY=hatch check
make -C cars BODY=hatch surface-compare
make -C cars BODY=hatch source-surface-proofs
make -C cars BODY=hatch STAGE=form
python3 -m py_compile cars/src/hatch_*.py
python3 kit/repo_check.py
```

The default detail graph fetches the three additional references, generates
both source densities and markings, checks construction and motion, prepares
coordinate attributes, unwraps/validates UVs, bakes material and verified
geometric-normal detail, downsamples, exports/re-imports and renders the
checkpoint. GPU work always uses `kit/with_gpu.sh` and the shared environment
lock. The default cars build and pickup gallery remain unchanged.

Raw proofs are under `build/hatch-detail/`: `detail-check.json` and
`detail-high-check.json` measure supports/clearance/travel; `motion-*.json`
measure solid sweeps; `audit-*.json` measure counts/bounds; `determinism.json`
compares independent generation; `uv-report.json` measures atlas geometry;
`projection-check.json` tests high/low correspondence; `delivery-check.json`
checks the actual re-imported GLB. Those checks certify different things.

Independent regeneration of the current detail source compares all 471 objects
and 442 meshes: transforms, hierarchy, vertices, faces, split normals and
material names agree exactly (`determinism.json`). The earlier detail round's
source-only clean-copy bake comparison remains historical evidence for the
accepted graph; its old counts and maps are not the surface round's result.

The normal-strength kit change has a separate commit. All 24 `kit/test_*.py`
modules pass sequentially in a scratch copy with an initially clean `build/`;
pure-Python tests use unittest, Blender fixtures run in fresh processes, and
the three real bake fixtures use the shared GPU lock. The actual glTF test
checks scale zero and a neighboring unchanged default over three shared images.
Logs are in `build/hatch-surfaces/kit-test-logs/`.

All checkpoint views use the imported GLB and baked images, with family paint
and lamp uniforms only. Metadata records its hash, framing, light recipe and
engine; the review script rejects mixed or stale source hashes. The color
sheet has ten views, motions five poses per mechanism group, and the details
include the face, grille, lamp states, wheel, glass/cabin, cargo, underside,
opened parts, scale and a four-view turnaround. Current source pairs are under `renders/hatch-source-pairs/`; earlier source
comparisons and the rejected first-bake images remain separate.

## Preservation and remaining limits

A fresh pickup generation matches all 472 objects / 454 meshes. Re-exporting
its accepted finalized scene and maps matches 150 GLB accessors, graph, images
and every byte: 11,530,720 bytes, SHA-256
`58661d0c2e11c2050e10677e12fabdf61570a3d25dc53837b485fee5c55a85ea`.
See `build/hatch-detail/pickup-preservation.json`. This proves generation and
re-export compatibility; no second identical GPU bake is claimed. No shared
family implementation or sedan module changes in this round. The
only kit change is the backward-compatible per-surface normal-strength option.

The cabin controls, headrests and cargo trim remain coarse. Alloy rim/spoke
chamfers, the projector module and very small cut fragments are still visible
as game geometry in extreme close-ups. Some reflection-direction changes remain
at cut/trim transitions. The suspension/steering links and upper gate-frame
support remain simplified layout proxies. Tires retain the accepted circular
rolling envelope without loaded contact flattening. Finest swirls, tread,
small badges and molded type soften at 2048.

The pair lighting is an estimated surrounding scene, not a unique radiometric
reconstruction. Windshield and tire patch residuals remain separate from the
two corrected rear glazing patches. No additional tool or lead action is needed
for this checkpoint. This stops at the requested surface review; no new final
portfolio gallery is committed.
