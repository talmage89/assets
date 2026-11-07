# Roadside miniature golf — form checkpoint

Two original, seeded 18-hole courses for an American town of 1995–2015:
**Bramble Putt**, a compact classic course with concrete and treated-timber
borders and painted Americana; **Cairn Creek**, a larger harbor/quarry adventure
course with shaped greens, rising ground, faux rock, pond, stream and waterfall.

**This delivery stops at the requested form/construction checkpoint.** All
views re-import the external-image glTFs. Materials are quick swatches and
original diagnostic typography. Final carpet/rock/paint normals, finished
weathering and final documentation JPGs await the look gate. No final-game
UV/bake certification or photoreal finish is claimed.

[Construction references](REFERENCE.md), [source credits](refs/SOURCES.md),
[critique log](REVIEW.md), [texture plan](TEXTURES.md).
No downloaded mesh, texture, material, lighting or reference pixel contributes
to the asset. Original graphics use installed open-license DejaVu Sans.

## Dimensions and construction

| Element | Chosen construction |
| --- | --- |
| Parcels including clubhouse/parking | Classic 49 × 56 m; adventure 64 × 65 m |
| Holes | 5.2–8.6 m centerline; 2.0–3.6576 m nominal width, with seeded necks/heads and bends |
| Concrete / carpet | Actual .1016 m slab edge; .0048 m nominal outdoor carpet top offset; compacted planted base below |
| Cup | .10795 m clear opening, .1016 m liner depth, 2 mm wall, open 20 mm drain; circular hole in carpet mesh |
| Tee | .9144 × .6096 × .003175 m rubber pad with real drilled start pocket; number/par, scorecard shelf and pencil |
| Borders | .1524 m concrete curb; brick units; .0889/.1397 m treated timber stock; irregular set rock |
| Playing ground | Classic almost level; adventure .025 rising grade, seeded banks, .26 m bump and .48 m ramp/steep drop features |
| Pond / stream | Adventure nominal 7.2 × 14 m water envelope, .40 m depth to liner floor; protected sloped EPDM bank; separate water surface |
| Waterfall | 1.30 m stainless lip, 1.05 m fall, framed exterior rock envelope, screened intake, service vault, routed 63 mm return |
| Human footbridge | 3.6 m span; 1.524 m nominal clear path; 2×6 joists, .0381 m boards, 1.067 m guard above deck |
| Themed fixtures | 3.20 m windmill; 4.73 m lighthouse; 2.80 m castle; 2.30 m covered ball bridge; 2.40 m wreck |
| Clubhouse | 6.8 × 4.6 m, framed open counter, pitched roof, actual entry hinges, sorting trays and 16-putter rack |
| Parking | Measured 7.3152 m / 24 ft aisle, 5.4864 m / 18 ft stalls, nominal 2.7432 m / 9 ft pitch; two 6.096 m driveways |
| Walks / fence / lights | 1.524 m connected walks with tee/cup approaches, three-rail face-fastened fence, four benches, five twin-head course lights |

Wittek's published stock sizes establish the mat and cup class; Harris's
published sections establish the four-inch slab, carpet, borders and drainage
practice. Henderson and Winnipeg establish shotcrete/framing and protected
45 mil EPDM practice. Lane routing, grading, fixtures, dimensions outside those
stock anchors and all business identities are authored choices, not a copied
plan or an engineering/accessibility certification. Hidden rebar and inner
rock-shell faces are omitted from the game exterior envelope.

## Generator and reusable parts

`src/plan.py` runs without Blender. `generate(seed, kind=None)` selects classic
or adventure; explicit kind overrides the seed's default. Seed controls
feature order, par, dimensions, bend, axis, carpet swatch and fixture placement.
All courses have 18 numbered holes; 250 seeds are checked deterministically.

The routing is six serpentine columns, ascending/descending alternating rows,
with side paths and connected headlands. Adventure separates its lobes around
a water spine and gives the greens organic shoulders and a rising site.
The grammar guarantees four theme types; adventure includes a wreck and some
classic seeds add one. This is a bounded roadside-course grammar, not arbitrary
parcel packing or a ball-physics simulation.

Reusable roots: each `Hole_nn`, each themed `Fixture_nn_*`, `Clubhouse`,
`RoadSign`, each bench/light, `WaterSystem`, `StreamFootbridge`, and `Site`.
Each hole includes separate Tee/Cup sockets and its reserved footprint in
extras. Fixed parts consolidate by module; true moving members stay separate.
Blender meters, +Z up / −Y front; glTF coordinates are `(x,z,-y)`. Course roots
are at the parcel center/low-grade datum, so the pond extends below Z=0.
Replace the course root transform; preserve descendants. Hole footprint extra
coordinates and documented axes use Blender's frame, while actual glTF node
transforms are converted to glTF's frame.

| Moving part | Blender local axis and range |
| --- | --- |
| Windmill rotor | Y, 0–360°, shaft at (0, −.79, 1.63) in fixture; actual bored hub |
| Castle portcullis | Z translation, 0–.40 m from its raised rest position |
| Clubhouse door | Z, −90–0°, left jamb at (2.29, 2.26, .13) in clubhouse |
| Cup-marker flags | Z, −30–30°, pole base beside cup; authored sagging fabric |

The windmill's lowest swept points cross a 42.7 mm ball's envelope and clear
the actual carpet. Rotor, gate and entry leaf are measured with `kit.motion`
at explicit angular/translation samples; these are sampled clearance checks,
not continuous collision guarantees. Bridge deck/joist/abutment contacts are
measured before consolidation. Source dimensions and fresh exported cup rays
prove construction; raw counts, socket comparison and import prove serialization.

## Checkpoint budgets

Hole totals include pad, number/par, cup, flag, border and playing feature;
the themed fixture on the hole is counted separately. Both 2k–8k hole and
15k fixture ceilings pass.

| Seed / kind | Course triangles | Per hole | glTF + BIN bytes | Material primitives |
| --- | ---: | ---: | ---: | ---: |
| 71 / classic | 123,712 | 4,144–5,512 | 7,712,267 | 77 |
| 92 / adventure | 174,304 | 5,640–7,108 | 9,671,837 | 79 |

Per-hole construction, excluding the separately budgeted themed fixture:

| Hole | Classic 71 | Adventure 92 |
| --- | ---: | ---: |
| 1 | 4,144 | 5,992 |
| 2 | 4,232 | 6,964 |
| 3 | 4,320 | 6,384 |
| 4 | 5,012 | 6,080 |
| 5 | 4,232 | 6,964 |
| 6 | 4,320 | 6,964 |
| 7 | 5,512 | 5,992 |
| 8 | 5,512 | 6,964 |
| 9 | 5,512 | 6,968 |
| 10 | 4,320 | 6,080 |
| 11 | 4,340 | 6,964 |
| 12 | 4,232 | 6,964 |
| 13 | 4,464 | 5,904 |
| 14 | 4,320 | 7,072 |
| 15 | 4,320 | 7,108 |
| 16 | 4,320 | 5,640 |
| 17 | 4,924 | 6,276 |
| 18 | 4,232 | 7,052 |

| Fixture | Triangles |
| --- | ---: |
| windmill | 3,420 |
| castle | 2,184 |
| covered bridge | 988 |
| lighthouse | 2,848 |
| shipwreck | 6,428 |

Three material states per course: opaque swatches, graphics, and water.
Both courses resolve the **same three external PNG identities**: 256² color,
256² ORM, 1024² graphics. About **1.5 MiB** compressed with mips at this gate.
No normal map is present at this gate. [TEXTURES.md](TEXTURES.md) plans the final
16 MiB course triple and 1⅓ MiB graphics sheet: **17⅓ MiB new**;
**97⅓ MiB** including Ground concrete/asphalt/lawn, fence lumber and shrubs
if none is already loaded. These future allocations are not claimed shipped.

The road uses Ground's native construction with a quick palette; presentation
houses/shops are original massing, and the existing RedMaple/Boxwood exports
supply linked landscape instances. These do not ship in the course glTF.
Each view places 39 maples (923,520 triangles) and 17 boxwoods (94,996),
sharing only 23,680 + 5,588 unique botanical triangles and their existing maps.
Town/road construction adds its own presentation geometry. A fully textured
course site will adopt the shared sets during the look gate.

## Rebuild and inspect

Needs installed Blender 5.2, Python/NumPy/Pillow, open fonts and flock. No
software or executable content is downloaded. All Cycles work holds the shared
kit GPU lock; scratch stays inside the clone.

```sh
make -C minigolf WIDTH=1440 SAMPLES=32  # refs, model, check, Cycles, pairs, sheets
make -C minigolf check                # 36 cups, scale, raw normals, budgets, motion, parking, repo
make -C minigolf repeat               # rebuild and compare glTF/BIN/PNG bytes
make -C minigolf check-renders        # all 15 Cycles frames, source/image byte receipt
make -C minigolf match                # three neutral-balanced period-photo pairs
```

For alternate proof seeds, run `src/build.py` from the family folder with
`--classic-seed` and `--adventure-seed`; defaults are 71 and 92. The supplied
make/check/presentation recipes intentionally use those two documented seeds.

| Generated local output | Contents |
| --- | --- |
| `export/Minigolf-{71,92}.gltf` + `.bin` | Separate courses, shared external quick images |
| `build/course.blend` | Generated construction checkpoint, both courses |
| `build/source-construction.json`, `check.json` | Actual gauges, cups, bridge contacts, parking, sockets, sampled motion, 250 seeds |
| `build/repeat.json`, `preservation.json`, `render-check.json` | Byte repeat; every pre-existing delivery/doc remains unchanged |
| `renders/checkpoint/hero.png` | Eye 1.65 m above local grade, 40 mm, raking sun, pond/fixture/hut/road/town |
| `renders/checkpoint/{classic,adventure}-{ground,above}.png` | Distinct places, full layouts and player viewpoints |
| `renders/checkpoint/{tee,cup,border,waterfall,fixture,bridge,clubhouse}.png` | Construction close-ups; measured 1.8 m silhouette in fixture view |
| `renders/checkpoint/contact.jpg`, `matched-pairs.jpg` | Complete image inventory and three period photographs |
| `renders/pass1/`, `renders/pass2/` | Rejected first/second-pass images, kept locally |
| `build/photo-calibration.json`, `reference-balance.json` | Estimated cameras, visible residuals, neutral ROI/gains |

No docs image is committed at the form gate. Full-size review and remaining
CG tells are recorded in REVIEW. No kit code or other delivery is changed.
