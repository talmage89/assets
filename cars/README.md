# Alder C150 / cars family

An original full-size late-2010s American pickup: four-door crew cab, short
bed, 4x4 stance and 275/65R18 all-terrain tire volumes. **Second body-form checkpoint
only. Work stops here for the lead's review.**

[Contact sheet](renders/checkpoint/contact.jpg) ·
[50% side overlay](renders/checkpoint/side-overlay.jpg) ·
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
| Length | 5890.26 mm | 5890.26 mm |
| Width, mirrors excluded | 2029.46 mm | 2029.46 mm |
| Height | 1960.88 mm | 1960.81 mm; crown sampling difference 0.07 mm |
| Wheelbase | 3683 mm | 3683.00 mm between actual wheel pivots |
| Front/rear track | 1716 mm | 1716.00 mm |
| Clear bed floor length | 1704.34 mm | 1704.34 mm |
| Tire section / top / ground | 275 mm nominal / lightly loaded | 275.00 / 802.70 / 0.00 mm |
| Front/rear door seam | 4–5 mm, chosen 4.5 | 4.500 mm surface distance, 8 edge samples per side |
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

The first form was rejected by the lead. The body now uses section stations,
near-planar ruled quad patches and small tangent fillets at authored character
lines. A shared cross-section is split at the door/cab/bed reveals. The hood
has a flat raised center stamping. Arch flares use separate annular quad grids
with radial support stations, rather than deforming the door/fender grids.
The gauge is evaluated before reapplying outer skin normals; the form check
independently compares broad panel normals against the actual surface slopes.

The straight outer A-pillar is 35.2 degrees above horizontal, compared with
34.4 +/-1.5 measured in the side photograph. Glass has tumblehome; the roof is
one crowned skin tied to the front and rear headers. Upper-only dark liners
stay inside the arches. Bumper upper returns meet the fascia and tailgate;
the bed has capped rails, a tailgate lip and vertical taillamp form envelopes.
Simple grille/headlamp envelopes establish the tall upright front face; no
optics, badges, trim textures or small detail have been added.

The new [side overlay](renders/checkpoint/side-overlay.jpg) uses only axle
centers to scale a 50% blue orthographic silhouette onto the known 145-inch
wheelbase photo. [Rake measurement](renders/checkpoint/side-rake.jpg) and
[REFERENCE.md](REFERENCE.md) disclose the photo's published 4x2 caption and
other configuration differences. Three-quarter RMS is **5.69 px front / 5.11 px
rear**, in original reference pixels, on five chassis anchors each. This is
not an all-body-landmark fit: roof/mirror/bumper accuracy remains weaker than
requested, and the pairs show the unresolved shape differences.
Tires have a radial carcass profile, bulged sidewalls, a crowned tread volume
and a small parked contact patch. Wheels establish the 18-inch barrel/offset
and spoke volume. Fine tread, lettering, brakes and suspension wait for the
next gate. Interior, underside, final transparent glass/frit, light optics,
paint, wear, UVs, bakes and GLB export are also pending.

## Budget at this gate

The game-density source has **59,740 triangles**; the final ceiling
remains 70k. 10,260 triangles remain below it. This is a form budget,
not a completed car budget: hidden sheet surfaces and wheel spoke bevels will
need further optimization as interior, brakes and underbody are added.

| Part category | Triangles |
| --- | ---: |
| Hood | 1,124 |
| Cab/floor/roof/headers | 4,448 |
| Glazing volumes | 532 |
| Front fenders/flares/arch returns | 9,568 |
| Four door skins/sashes | 4,208 |
| Coarse mirrors/supports | 976 |
| Bed/rails/tubs/rear corners/flares | 11,240 |
| Lamp envelopes | 784 |
| Wheel-well liners | 1,936 |
| Tailgate | 1,236 |
| Nose/grille form | 1,508 |
| Bumpers/upper returns | 2,180 |
| Four tires | 11,520 |
| Four wheel barrels/hubs/spokes | 8,480 |
| **Total** | **59,740** |

Each wheel group is 5,000 triangles including its tire. Each door group is
1,148 including its glass; the per-object table is in `build/form-check.json`.
The high source has 131,396 triangles. Ignored high/game blend files are
1,032,264 / 523,235 bytes in this build (serialization sizes may vary).
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
