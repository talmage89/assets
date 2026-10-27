# Alder C150 / cars family

An original full-size late-2010s American pickup: four-door crew cab, short
bed, 4x4 stance and 275/65R18 all-terrain tire volumes. **Body-form checkpoint
only. Work stops here for the lead's review.**

[Contact sheet](renders/checkpoint/contact.jpg) ·
[Front clay](renders/checkpoint/front_three_quarter.jpg) ·
[Rear clay](renders/checkpoint/rear_three_quarter.jpg) ·
[Front photo pair](renders/checkpoint/match_front-pair.jpg) ·
[Rear photo pair](renders/checkpoint/match_rear-pair.jpg)

All checkpoint renders load `build/game-audit.blend`, with the actual game
sampling. Clay uses Workbench; the two striped reflection diagnostics use
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
| Length | 5890.26 mm | 5888.90 mm; finite grid misses exact bumper apex by 1.36 mm |
| Width, mirrors excluded | 2029.46 mm | 2031.83 mm; +2.37 mm at the authored arch stamping |
| Height | 1960.88 mm | 1960.88 mm |
| Wheelbase | 3683 mm | 3683.00 mm between actual wheel pivots |
| Front/rear track | 1716 mm | 1716.00 mm |
| Clear bed floor length | 1704.34 mm | 1704.34 mm |
| Tire section / top / ground | 275 mm nominal / lightly loaded | 275.00 / 802.70 / 0.00 mm |
| Front/rear door seam | 4–5 mm, chosen 4.5 | 4.500 mm surface distance, 12 edge samples per side |
| Cab/bed separation | 16 mm | 16.000 mm at the lower rear wall / outer bed envelope |
| Tire top to arch crown | Original ride-height design | 119.81 mm vertical difference |
| Ground clearance | 226 mm eventual target | Pending axle/frame; no ground-clearance proof claimed |

The orthographic [side](renders/checkpoint/side-dimensions.jpg),
[front](renders/checkpoint/front-dimensions.jpg) and
[top](renders/checkpoint/top-dimensions.jpg) sheets show cited target lines.
`build/form-check.json` supplies actual vertex/surface measurements, per-mesh
triangle counts and the source hash. The bounding widths above exclude mirrors,
which are deferred with other details.

## Construction at this gate

A crowned hood and roof; tapered cab glazing; four separate curved lower door
skins and rounded stamped sashes; front fenders and narrow turned arch lips;
an open double-wall pickup box with wheel tubs, floor and front wall; a separate
tailgate; swept bumper envelopes; dark wheel-well volumes. Outer sheets have
closed gauge and inward returns. The broad nose is unpierced until the form is
reviewed; grille, lamps, badges and handles have not been modeled.

Tires have a radial carcass profile, bulged sidewalls, a crowned tread volume
and a small parked contact patch. Wheels establish the 18-inch barrel/offset
and spoke volume. Fine tread, lettering, brakes and suspension wait for the
next gate. Interior, underside, final transparent glass/frit, light optics,
paint, wear, UVs, bakes and GLB export are also pending.

## Budget at this gate

The source has **52,540 triangles**, including all four wheels and separate
sheet gauges. The final budget remains 40k–70k; 17,460 triangles remain below
the ceiling. The aim is to recover redundant inner sheet sampling as detail
is added and keep the finished vehicle near the middle of the range.

| Part category | Triangles |
| --- | ---: |
| Hood | 1,108 |
| Cab/floor/roof/rails | 5,356 |
| Glazing volumes | 664 |
| Front fenders/arch returns | 5,016 |
| Four door skins/sashes | 4,736 |
| Bed/rails/tubs/rear corners | 8,944 |
| Wheel-well liners | 2,016 |
| Tailgate | 1,464 |
| Nose envelope | 1,108 |
| Bumpers/upper returns | 2,128 |
| Four tires | 11,520 |
| Four wheel barrels/hubs/spokes | 8,480 |
| **Total** | **52,540** |

Each wheel group is 5,000 triangles including its tire. Each door group is
1,280 triangles including its glass. The complete per-object table is in the
form report. The high source contains 182,636 triangles. Ignored high/game blend files are
1,802,753 / 505,264 bytes at this checkpoint (serialization sizes may vary).
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
`matched-cameras.json`, and `renders/checkpoint/tonal-check.json`.
Read [REVIEW.md](REVIEW.md) for the critiques, verified commands and remaining
weaknesses. The lead's next action is the body-form review.
