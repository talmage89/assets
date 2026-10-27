# Alder C150 / cars family

An original full-size late-2010s American pickup: four-door crew cab, short
bed, 4x4 stance and 275/65R18 all-terrain tire volumes. **Third body-form checkpoint
only. Work stops here for the lead's review.**

[Contact sheet](renders/checkpoint/contact.jpg) ·
[50% side overlay](renders/checkpoint/side-overlay.jpg) ·
[Front clay](renders/checkpoint/front_three_quarter.jpg) ·
[Rear clay](renders/checkpoint/rear_three_quarter.jpg) ·
[Front clay + stripes pair](renders/checkpoint/match_front_stripes-pair.jpg) ·
[Rear clay + stripes pair](renders/checkpoint/match_rear_stripes-pair.jpg) ·
[Measured profile](renders/checkpoint/side-measurements.jpg)

All checkpoint renders load `build/game-audit.blend`, with the actual game
sampling. Clay uses Workbench; the striped diagnostics and two calibrated clay-with-stripes pairs use
Cycles GPU through the shared lock. None is a baked/exported delivery render.
The images remain ignored build outputs; no preliminary docs JPG is committed.

## Dimensions

[REFERENCE.md](REFERENCE.md) distinguishes published dimensions from authored
construction estimates. [refs/SOURCES.md](refs/SOURCES.md) records reference
licenses and direct image/PDF URLs. The primary envelope comes from Ford's
MY2018 short-bed crew-cab specification, cross-checked against GM and the
same-generation Ford body-builder data.

| Measurement | Reference/design target | Actual checkpoint |
| --- | --- | --- |
| Length | 5890.26 mm | 5889.46 mm (0.80 mm tessellation difference) |
| Width, mirrors excluded | 2029.46 mm | 2029.51 mm |
| Height | 1960.88 mm | 1960.88 mm |
| Wheelbase | 3683 mm | 3683.00 mm between actual wheel pivots |
| Front/rear track | 1716 mm | 1716.00 mm |
| Clear bed floor length | 1704.34 mm | 1704.34 mm |
| Tire section / top / ground | 275 mm nominal / lightly loaded | 275.00 / 802.70 / 0.00 mm |
| Front/rear door seam | 4–5 mm, chosen 4.5 | 4.500 mm surface distance, 32 edge samples per side |
| Cab/bed separation | 16 mm | 16.000 mm at the lower rear wall / outer bed envelope |
| Tire top to arch crown | Original ride-height design | 90.30 mm vertical difference |
| Ground clearance | 226 mm eventual target | Pending axle/frame; no ground-clearance proof claimed |

The orthographic [side](renders/checkpoint/side-dimensions.jpg),
[front](renders/checkpoint/front-dimensions.jpg) and
[top](renders/checkpoint/top-dimensions.jpg) sheets show cited target lines.
`build/form-check.json` supplies actual vertex/surface measurements, per-mesh
triangle counts and the source hash. The body width excludes coarse mirror envelopes. Full width with mirrors is
2458.72 mm; diagnostic bounds include those mirrors separately.

## Construction at this gate

The broad side is now a shared Hermite section with a measured **6.26 mm
vertical crown** over the 820–1200 mm chord. A straight lower die line and a
supported shoulder cross the panel reveals. Squared arch boundaries trim that
same surface; broad flares stand **35 mm** out from the adjacent door section
and draw into the side over **195–225 mm** above the opening. There are no
separate annular flare skins or height-faded flare ends. Opening width at the
rocker increased from 886 to 995 mm while its 893 mm crown height stayed fixed.
This remains an analytic quad surface method, with explicit tangents and
physical feature stations, rather than a subdivision modifier.

The hood leading center is 67 mm lower, with a raised center and lower fender
tops. The center slopes 7.50 degrees; the front face rakes 5.71 degrees, with
a 35 mm proud original grille surround and 337 mm of headlamp wrap. The bumper
uses formed sections around a blocked intake and a separate lower valance.
The windshield meets the beginning of a rolled header/roof surface, rather
than a raised bridging block; measured top-edge recess is 1.14 mm. Its outer
A-pillar is 34.90 degrees above horizontal versus the photograph's 34.4 +/-1.5.
The roof narrows 15 mm per side toward its rounded back, whose center sits
88 mm below the unchanged 1961 mm peak. Fixed rails sit behind the separate
door sashes; three actual surface-ray samples measure 1.64–2.49 mm separation.

[Measured side overlay](renders/checkpoint/side-measurements.jpg) retains the
original axle-only registration. Hood silhouette excess is now 6 / 11 / 20 mm
at the three inspected stations, versus 66 / 57 / 52 mm before. Rear roof
stations improved from 34 / 72 mm high to 0 / 26 mm. Front/middle roof excess
remains 54 / 37 mm with the specified peak height held. Photo picks have about
16 mm height uncertainty; the reference caption is 4x2, and this is a 4x4.

The fixed bumper envelope still extends 124 mm at the front and 46 mm at the
rear beyond that axle-scaled photograph. It was not shortened to hide this
remaining mismatch. A photograph is not perfectly orthographic, and the
specified envelope/axles remain the dimensional authority.

Camera RMS remains **5.69 px front / 5.11 px rear** on the same five chassis
anchors. [Front](renders/checkpoint/match_front_stripes-measurements.jpg) and
[rear](renders/checkpoint/match_rear_stripes-measurements.jpg) now show separate
body landmark residuals; those differences never enter the camera fit. They
are substantially larger than chassis RMS. The marked picks have +/-14 source
pixel uncertainty and approximate correspondence between different designs.
[Two-make comparison](renders/checkpoint/class-crosscheck.jpg) records the
Ford and Ram cross-check; it is explicitly not another registered pair.

Tires have a radial carcass profile, bulged sidewalls, a crowned tread volume
and a small parked contact patch. Wheels establish the 18-inch barrel/offset
and spoke volume. Fine tread, lettering, brakes and suspension wait for the
next gate. Interior, underside, final transparent glass/frit, light optics,
paint, wear, UVs, bakes and GLB export are also pending.

## Budget at this gate

The game-density source has **66,904 triangles**; the final ceiling
remains 70k. 3,096 triangles remain below it. This is a form budget,
not a completed car budget: hidden sheet surfaces, wheel spoke bevels and broad panel sampling will
need further optimization as interior, brakes and underbody are added.

| Part category | Triangles |
| --- | ---: |
| Hood | 1,700 |
| Cab/floor/roof/headers | 8,180 |
| Glazing volumes | 952 |
| Front fenders/flares/arch returns | 8,712 |
| Four door skins/sashes | 7,216 |
| Coarse mirrors/supports | 976 |
| Bed/rails/tubs/rear corners/flares | 10,408 |
| Lamp envelopes | 1,968 |
| Wheel-well liners | 1,872 |
| Tailgate | 1,576 |
| Nose/grille form | 3,300 |
| Bumpers/upper returns | 3,244 |
| Four tires | 9,600 |
| Four wheel barrels/hubs/spokes | 7,200 |
| **Total** | 66,904 |

Each wheel group is 4,200 triangles including its tire. Tire/rim circumference
sampling is 80/48 at game density; dimensions are unchanged. Door and per-object
counts are in `build/form-check.json`.
The high source has 163,572 triangles. Ignored high/game blend files are
1,515,798 / 732,474 bytes in this build (serialization sizes may vary).
Six temporary diagnostic clay materials, **zero texture images**,
and **no GLB** exist at this checkpoint. These are not final material budgets.

## Family and paint plan

`src/pickup_spec.py` contains this vehicle's dimensions; `src/forms.py` and
`src/body.py` contain its original body. `src/wheels.py` accepts the vehicle's
dimension module rather than importing this pickup's dimensions. Generic
returned panels and loaded ISO tires live in `kit/vehicle.py`; later vehicles
can use the same primitives. Glass, lights, paint and interior modules will be
added when this form is accepted, rather than building speculative detail here.

The selected delivery approach is **one shared neutral 2048 texture set with
an independent paint material's base-color factor**, using the five linear RGB
presets already in `pickup_spec.COLORS`: white, black, silver, gray, dark blue.
A fourth active material is justified for tintable clear-coated paint alongside
opaque trim/interior, transmissive glass, and lights. Preset changes allocate
no additional images. A proposed driveway mix is 35% white, 25% black, 15%
silver, 18% gray and 7% blue; this is an art-direction distribution, not a
claimed measured sales statistic. **Delivery tinting is planned, not shipped.**

Expected texture memory: three 2048 BC7/BC5-equivalent 8-bpp maps with full
mips are about **16 MiB total**, shared by every color; uncompressed RGBA8 with
mips is about 64 MiB. Actual GLB texture references and GPU allocation still
need delivery verification. The fourth material costs a material batch on paint,
not five texture sets.

## Coordinate frame and provisional pivots

Meters, Blender +Z up, front −Y, root `AlderC150` at the center of the bumper
footprint on the ground. Four doors rotate about Z at their forward edges;
the hood and tailgate about X at their rear/front edges respectively. Wheels
spin about local X. Front wheel spin roots are nested under Z steering roots.
No armature is present.

| Node | Local axis / proposed range | Checkpoint status |
| --- | --- | --- |
| `Door_FL`, `Door_RL` | Z, 0…72° | Preliminary hinges; swept clearance pending |
| `Door_FR`, `Door_RR` | Z, −72…0° | Preliminary hinges; swept clearance pending |
| `Hood` | X, −62…0° | Preliminary rear-edge hinge |
| `Tailgate` | X, −90…0° | Preliminary lower hinge |
| `Wheel_FL/FR/RL/RR` | X, continuous | Static flattened tires; rolling solution pending |
| `Steer_FL`, `Steer_FR` | Z, −35…35° | Provisional vertical axes; caster/SAI and clearance pending |

These nodes establish assembly ownership. They do not certify working movement;
`MOTIONS=[]` intentionally declares no sweep at this form gate.

## Rebuild and evidence

Needs installed Blender 5.2, Python/Pillow/NumPy and flock. No downloaded code,
packages, textures, models or lighting are used.

```sh
make -C cars                         # full form gate, 1400 px by default
make -C cars WIDTH=1600              # delivered review image size
make -C cars check                   # source topology/bounds/budget + form + cameras + repo
make -C cars PASS=another-form render match stripes dimensions
blender -b --factory-startup --python-exit-code 1 --python kit/test_vehicle.py
```

`make` includes the kit rules with `CUSTOM_CHECKPOINT=1`, leaves
`FINAL_PIPELINE=0`, and never bakes, exports, writes final docs or proceeds to
detail. Reports: `build/game-audit.json`, `lookdev-audit.json`, `form-check.json`,
`matched-cameras.json`, `renders/checkpoint/form-comparisons.json`, `side-overlay.json`,
and `renders/checkpoint/tonal-check.json`.
Read [REVIEW.md](REVIEW.md) for the critiques, verified commands and remaining
weaknesses. The lead's next action is the body-form review.
