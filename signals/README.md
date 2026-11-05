# Waycroft traffic signals

Original, maintained 1995–2015 American signal equipment, with four road-derived
installations and shared baked surfaces. This is the requested look checkpoint;
no docs images are committed this round. All inspection renders come from
the exported game parts, with separate source comparisons to expose bake loss.

[REFERENCE.md](REFERENCE.md) records measured standards and authored choices.
[TEXTURES.md](TEXTURES.md) explains the atlas, material references and age.
[REVIEW.md](REVIEW.md) records rejected views and remaining weaknesses.
[refs/SOURCES.md](refs/SOURCES.md) credits photographs and engineering drawings.

## Four towns

| Seed | Road plan and support |
| --- | --- |
| 201 / Aldervale | Five-lane 55 ft arterial crossing a 22 ft street; center turn lane, 35 ft corner returns and a channelizing island; four galvanized mast supports, yellow cases and FYA on the arterial; commercial corner with the library gas station |
| 202 / Cinderbrook | Two 22 ft streets, 15 ft corner returns; two diagonal dark-green poles with paired arms reaching the lanes each serves; black cases, doghouse left treatment and supplemental near-side faces |
| 203 / Wrenfield | 66 ft divided boulevard: four 11 ft through lanes and a 22 ft median, with an 11 ft left-turn bay cut into each end; 22 ft cross street, rounded noses, tapers and 25 ft returns; four bronze masts, yellow cases, protected arrows and Rill luminaires |
| 204 / Morrow Glen | Two-lane T with 20 ft returns and a continuous walk on its closed side; two black strain poles, catenary/messenger, lashed cable, lower tether and six faces serving the three actual approaches |

The cabinet corner, pedestrian arrangement, pole corners and arm reaches follow
the road grammar. Native ground deliveries remain untouched. The additive
`ground/export/ArterialSites.glb` contains four separate junction modules built
by `ground/src/junction.py`; it is independent of Ground.glb and the earlier
ArterialCheckpoint.glb. Houses, trees, street lights, the gas station and the
pickup/crossover/hatchback are presentation only and never enter signal exports.

## Construction and dimensions

| Feature | Dimension / construction |
| --- | --- |
| Vehicle indication | 304.8 mm / 12 in nominal clear circle; 370 mm section pitch |
| Cases / visors | Original compound Waycroft shoulders, separate retaining rim, hinge and latch; 1.6 mm sheet visors, 205 / 245 mm reach |
| Pole | 25 ft from plate bottom; 16 → 12.53 in across flats, twelve-sided taper |
| Base | 30 × 2½ in plate, six 1¾ in anchors on 23 in circle, hollow nut covers, 4 ft round foundation |
| Arm | Brake-formed taper, 2° camber, flange/box connection; reach derived from controlled lanes, within the brief's 20–45 ft range |
| Pedestrian case / post | 444.5 × 419.1 × 180 mm, 150 mm hood; 4 in pedestal |
| Accessible button | Axis 1.0668 m / 42 in above the actual landing; raised tactile arrow and separate instruction sign |
| Cabinet | Original Morrow Controls 910 × 720 × 1660 mm shell, 3 mm aluminum over 200 mm plinth |
| Cabinet interior | Rack controller, conflict monitor, detector inputs, load-switch bay, breakers, harness and door document pocket; simple forms with generated fronts |

MUTCD 2009 and FDOT 2014 establish the period convention and chosen support
construction. The installation is a game asset, without structural, electrical,
traffic-study or accessibility certification. Lane widths, tapers, plans and
fictional makes are authored choices, distinguished from published dimensions.

Mast wiring enters the head's top boss through its bracket into the hollow arm.
The detector lead is clipped to its riser. Span clamps follow the messenger;
overlapping extension bars and balance adjusters support the heads, with short
gravity-hanging entry loops and one drip loop at each pole. FDOT 17727 sheets
1–2 inform that construction. There are no large rings or airborne mast handles.

## Game parts and state control

`export/Signals-201…204.gltf` are complete equipment-only installations.
`export/parts/` supplies MastArm, Pedestal, PushButtonPost, Cabinet, PushButton,
PedHead, Head_three, Head_fya, Head_five, Head_protected and SpanSet. Their .bin
files carry geometry; every referenced image resolves to `export/textures/`.

Meters, Blender +Z up / −Y front, glTF +Y up / +Z forward. Ground sockets retain
placement frames. Main support origins sit at the pole foundation; the span
set's origin is its installation center. Each head's origin is its indexed
hanger. The door uses local Z, −110…0°. Heads retain local Z ±15° aiming and
X ±4° limited movement. A game moving a head must update its flexible cable
and tether ends; a static service loop is not a cable simulation.

Every indication retains its stable `signal_lens` / `signal_kind` / `powered`
extras and name, such as `Mast_0__Head0__S00_red`. Swap that mesh's reference
between SharedLens_Off and SharedLens_Lit. Never modify a shared material to
change only one head. FYA S02 carries `flashing_yellow_arrow`; S01 is the steady
yellow arrow. No timing controller or animation is imposed.

Pedestrian hand, walk and `Countdown_{Tens,Ones}_{A…G}` remain independent parts.
Use the ordinary seven-segment table, suppress countdown during walk as needed,
and control legal phases in the game. The demonstration keeps protected arrows
red while opposing through traffic runs; the T has no face aimed at its missing
branch. The optical fixture shows lit/dark copies at measured 30 m and 100 m.

## Budget and verification

One 2048 BaseColor / +Y Normal / ORM set, a 1024 indication sheet and 512 × 256
name sheet cost about **17.5 MiB** with 8-bpp compression and complete mips.
They are allocated once for the whole family. A mast uses atlas, two state
references and names; a cabinet uses only the atlas. See TEXTURES.md for details.

The actual per-part triangles, primitive/material references, per-intersection
bytes, map hashes and UV density are generated in `build/budget-report.json`
and `build/budget-report.md`. Every vehicle-head variant stays at or below
1,500 triangles; complete mast assemblies stay under 14,000, cabinets under
3,000 and pedestals under 4,000. The two halves sharing a Cinderbrook pole are
also reported together as one complete dual-arm support.

Measured equipment totals (ground and presentation excluded):

| Delivery | Triangles | Materials | glTF + geometry bytes |
| --- | ---: | ---: | ---: |
| Aldervale 201 | 47,036 | 4 | 2,507,052 |
| Cinderbrook 202 | 42,244 | 4 | 2,274,444 |
| Wrenfield 203 | 51,356 | 4 | 2,729,061 |
| Morrow Glen 204 | 31,340 | 3 | 1,608,485 |

Reusable three / FYA / five / protected heads are 1,060 / 1,340 / 1,500 / 964
triangles. PedHead is 464; PushButton 408; PushButtonPost 1,044; Pedestal 1,564;
Cabinet 2,800; MastArm 8,174; SpanSet 17,456. The complete dual-arm Cinderbrook
support is 13,380 triangles. Variants' actual per-head and support counts are
also retained in the generated report. Shared PNGs total 3,657,737 bytes;
all fifteen glTF/bin deliveries plus that single map copy total 14,607,229 bytes.

`make` rebuilds fields, locked Cycles bakes, game parts, external glTFs, checks,
checkpoint views, source/game photo pairs and review sheets. Defaults are
1600 px / 32 samples. Render seeds run sequentially in fresh Blender processes;
presentation images are capped at 512–1024 in memory while the signals retain
their full delivered maps. Source files are never resaved by this cap. Kernel
peak RSS for the render processes is recorded in build/memory/. `WEAR=.8` controls service age. No kit code is changed.

```sh
make
make check
make repeat
make arterial
make WIDTH=1200 SAMPLES=24 render
```

Checks distinguish source-surface contacts and sampled motion from raw glTF
accessors, UV trim domains and fresh-import serialization. An additional layout
check measures actual pole counts, face aiming toward existing roads, primary
face separation and a conservative 20° horizontal view cone at the stop bar.
They prove construction and serialization, not photographic realism.
`make repeat` replays the model recipe in a separate factory-startup build;
it checks exact GLB bytes, without claiming bit-identical GPU rebakes.

## Inspection artifacts

| Path | Evidence |
| --- | --- |
| renders/checkpoint/201/hero.png | 40 mm sidewalk view, eye 1.6 m above its actual standing surface |
| renders/checkpoint/201/dusk.png | Lit indications, street lights and town windows; sky brighter than ground |
| renders/checkpoint/<seed>/{above,driver}.png | Four distinct plans and driver's approaches |
| renders/checkpoint/201/{head_lit,head_dark,connection,base,pedestrian,button,cabinet,cabinet_open}.png | Equipment close-ups, including the operating cabinet |
| renders/checkpoint/204/span_hanger.png | Clamp, extension, entry loop and lashing |
| renders/checkpoint/optics/{30m,100m}.png | Equal-distance lit/dark imported heads, with distances and pixel bounds in sidecars |
| renders/matches/ | Seven game-part photo pairs across four seeds, with balanced neutrals and fitted camera overlays |
| renders/source-matches/ | The same comparisons before delivery filtering |
| renders/form-fixes/ | Native-pixel before/after panels, at least 800 px across each crop |
| renders/checkpoint/contact.jpg | Complete checkpoint sheet; four-towns.jpg, construction.jpg and photo-pairs.jpg separate the views |

The Oregon mast pairs fit the complete three-face FYA assembly from actual
lens vertices, with constrained sidewalk and driver eyes. The other pairs
check black cases, yellow cases and span construction. Omitted presentation
equipment/context is recorded in sidecars. Finishes and original street
geography differ, which limits direct surface conclusions. Head and hanger
details remain simpler than the photographs; tall-pole texel density and the
repeated neighborhood are the weakest close views. This checkpoint does not
claim that those differences have disappeared.
