# Alder H120 — detail and look checkpoint

An original compact five-door hatchback in the 2018–2022 class. The accepted
round-four form now has its working closures, original exterior hardware,
five-seat cabin, cargo well, FWD underside and five daily-driver finishes.
This stops at the requested review checkpoint; no final hatch gallery JPGs
are committed.

![Five factory finishes](renders/hatch-checkpoint/five-colors.jpg)

[Contact sheet](renders/hatch-checkpoint/contact-sheet.jpg) ·
[Details](renders/hatch-checkpoint/details-contact.jpg) ·
[Opening poses](renders/hatch-checkpoint/motion-sweeps.jpg) ·
[White-balanced front pair](renders/hatch-checkpoint/used_front-measured.jpg) ·
[White-balanced rear pair](renders/hatch-checkpoint/used_rear-measured.jpg) ·
[Eevee](renders/hatch-eevee/front_three_quarter.png) ·
[Critique log](REVIEW.md#h120-detail-and-look-checkpoint)

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

No parent control-net refit was made. Local game reflection sampling adds 384
body triangles: 48 new interior edge samples per rear quarter and 32 per front
fender/hood, projected onto our own accepted dense source. Maximum new-sample
projection is 1.011 mm; retained samples and exterior cut boundaries stay held.
The hidden spoiler foot is seated above the roof, and steering liners/inner
returns move inside the accepted outer arch. A tiny fixed front glazing sail
is split from the moving window along a 2 mm bonded reveal. Original form
artifacts remain separate from these detailed construction changes.

## Parts and mechanisms

The grille has swept gloss-black cascade vanes, diamond relief behind them,
a dark-chrome surround and an original Alder badge. Projector bowls, optics,
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
| pillars | 1,374 |
| glass | 2,220 |
| doors | 4,428 |
| body | 13,101 |
| fascia | 8,722 |
| arches | 784 |
| liners | 1,168 |
| openings | 3,840 |
| lamps | 3,304 |
| mirrors | 1,016 |
| spoiler | 1,184 |
| tires | 4,224 |
| wheels | 3,544 |
| brakes | 1,120 |
| trim | 2,396 |
| interior | 3,600 |
| cargo | 260 |
| underbody | 1,792 |
| hinges | 1,912 |
| **Total** | **59,989 / 60,000** |

The accepted form was 46,737 triangles and its detail plan 59,237. The final
checkpoint spends 752 above that plan, inside the 60k cap: optics, real hinge
hardware and reflection sampling receive the extra room; hidden wheel and
cabin detail is reduced. `build/hatch-detail/game.counts.json` lists every
mesh and immediate moving parent. The high source has 156,266 triangles.

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

Paint uses a smooth clearcoat, faint peel, undercoat metallic flake where
appropriate, and wash marks in roughness. Glass is transmissive with frit and
lower-edge residue. Rubber, glossy grille, dark chrome, painted alloy and
black molded trim have distinct responses. Low road film follows wheel wakes
and height, chips follow door hems/hood leading edge, grime follows gaps and
lamp edges, brake dust follows the caliper region outward, and luggage abrasion
stays on the rear bumper shelf. `WEAR=.65` is the checkpoint daily driver.

The verified GLB is **8,256,940 bytes**, with 21 meshes / 36 material primitives.
It embeds exactly three 2048 images: Normal 1,555,580 B, ORM 1,842,218 B, BaseColor 853,521 B.
Maximum re-import rest-position error is 0.386 micrometers; pivot matrix error is
2.38e-07. UV coverage is 40.48%, with zero overlapping, outside or degenerate
triangles. Measured 5th / median / 95th density is 74.8 / 227.5 / 380.5 px/m.
Forty-seven logged UV repairs/splits retain the thin cut fragments through
float32 export. No geometric vertex was moved to make a UV check pass.

Prepared material channels bake directly on the finalized game surface:
**5,937,221 checked interior texels, zero misses** in every channel.
Partwise rays approve 223 higher-detail hardware/tread/cabin parts for
normal projection; smooth glass and panel normal fields stay with the direct
source. Reversed projection texels and chart edges keep the direct normal.
The final imported views are the visual check of that policy, rather than
coverage statistics alone. The raised original tire lettering also catches a
faint causal dust deposit, preserving its legibility after minification.

GLB SHA-256: `c0e0adb268eb3d5de7ac3fa71cf93834633d72c4699bd64a6b4911ea4e253c45`.

The final Cycles heroes have asset luma p1 / median / p99 of
**0.8 / 46.3 / 249.1** front and **0.0 / 45.7 / 248.9** rear. Their clipped
channel fractions are zero; the other factory-color heroes have at most
0.0013% of channel samples at 254 or above. This follows
a real re-render at −2.5 exposure, after rejecting the brighter clipped set.
The Eevee fallback has darker glass and 0.078% clipped channels. All 58 final
views and their per-view tone statistics are in `tonal-range.json`.



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
(±15°), and asphalt-gray ground; no studio lights or flags remain in those views.

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
| front / rear road film | 142.9 | 142.2 | -0.7 |
| front / front glass | 72.2 | 72.8 | +0.6 |
| front / windshield | 123.8 | 109.9 | -13.8 |
| front / tire sidewall | 22.8 | 33.9 | +11.0 |
| rear / upper front door | 172.8 | 177.8 | +5.0 |
| rear / front road film | 156.5 | 165.5 | +9.0 |
| rear / rear door | 177.2 | 178.6 | +1.4 |
| rear / rear road film | 160.9 | 168.8 | +7.9 |
| rear / front glass | 123.7 | 161.9 | +38.2 |
| rear / backlight | 121.2 | 73.4 | -47.7 |
| rear / tire sidewall | 27.0 | 31.9 | +5.0 |

Upper white paint is within 8 display levels in these particular patches, and
the lower-film gradient is within 9. Rear side-glass and backlight are still
**+38.2 / −47.7**, respectively; the front tire sidewall is **+11.1**. Those
are visible limits of the current glazing/environment and tire response, not
a successful radiometric match. Source and exported measurements remain
separate so bake loss is visible.


## Rebuild and evidence

```sh
make -C cars BODY=hatch
make -C cars BODY=hatch check
make -C cars BODY=hatch source-render
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

`make check` also passes in a source-only copy under
`build/hatch-detail-cleancheck/`, after rebuilding the original form, detail,
markings, atlas and export. Its 484 objects / 455 meshes match the working
source exactly, as do all 455 meshes' atlas UV arrays. Independent GPU bakes
differ by at most one 8-bit channel level: 1 BaseColor pixel, 115 Normal pixels
and 4 ORM pixels out of 4,194,304 per image. This is quantization-level
variation, not a claim of byte-identical GPU textures. Raw evidence is
`build/hatch-detail/clean-rebuild-comparison.json`. A missing shipped BaseColor
map was also removed in that scratch tree and successfully regenerated,
re-exported and re-verified from the declared atlas dependencies.

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
family implementation, sedan module or kit file changed in this detail round.

The cabin controls, headrests and cargo trim remain coarse; tire shoulders, inner-arch return glints
and wheel chamfers are softer than a product photograph at extreme close-up.
The secondary grille lattice loses contrast after baking, while the modeled
cascade vanes and surround survive. Fine hood/lamp-corner highlight jogs,
regular shut lines and the crowded rear shoulder/D-pillar still read as CG.
The suspension/steering links and upper gate-frame support are simplified
layout proxies, rather than a complete detailed mechanical assembly. Tires
retain the accepted circular rolling envelope, without loaded contact flattening.

The largest appearance limitation is the rear glazing: the procedural sky and
asphalt do not reconstruct the photographed buildings/vegetation reflected in
it, and its value residual remains large. Wear is visible low on the white
body; the finest clearcoat swirls and small relief soften at 2048. These are
checkpoint limitations, not a claim of photographic equivalence or final
portfolio delivery. No additional tool or lead action is needed to reproduce
this checkpoint. A configurable pixel padding in the generic kit baker would
avoid the small H120 normal-only wrapper; `kit/` is unchanged here.
