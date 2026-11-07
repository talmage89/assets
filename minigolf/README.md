# Roadside miniature golf — look-dev checkpoint

Two original, seeded 18-hole courses for an American town of 1995–2015:
**Bramble Putt**, a compact classic course with concrete and treated-timber
borders and painted Americana; **Cairn Creek**, a larger harbor/quarry adventure
course with shaped greens, rising ground, faux rock, pond, stream and waterfall.

**This round stops before final documentation images.** The source generates
procedural course PBR surfaces and imports the delivered GLBs for Cycles judgment.
Full-resolution local views, comparison pairs and critique receipts are under
`renders/`; there is deliberately no README gallery or `docs/` image this round.
The remaining limitations are recorded in REVIEW; passing a geometry check is
not visual acceptance.

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
| Borders | .1524 m concrete curb; brick units; .0889/.1397 m treated timber stock; continuous carved shotcrete / mortared stone |
| Playing ground | Classic almost level; adventure .065 rising grade with level fixture landings, seeded banks, .26 m bump and .48 m ramp/steep drop features |
| Pond / stream | Adventure nominal 7.2 × 14 m free-form envelope, .40 m main-pool depth; two downstream 35/45 mm drops; protected shelves/EPDM and continuous water skin |
| Waterfall | three 1.15/1.55/1.90 m stainless weirs, receiving ledges and splash pool, carved exterior rock envelope, screened intake, service vault, routed 63 mm return |
| Human footbridge | 3.6 m span; 1.524 m nominal clear path; 2×6 joists, .0381 m boards, 1.067 m guard above deck |
| Themed fixtures | 3.20 m windmill; 4.73 m lighthouse; 6.00 m castle keep / 4.20 m front turrets; 2.30 m covered ball bridge; 2.40 m wreck |
| Clubhouse | 6.8 × 4.6 m, sided walls, framed windows, sliding service sash, supported awning, boards, fluorescent emitter socket, sorting trays and 16-putter rack |
| Parking | Measured 7.3152 m / 24 ft aisle, 5.4864 m / 18 ft stalls, nominal 2.7432 m / 9 ft pitch; two 6.096 m driveways |
| Walks / fence / lights | 1.524 m connected walks with tee/cup approaches, three-rail face-fastened fence, four benches, nine twin-head course lights |

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

The classic fans opposed pairs into a shared mulched bed, with curved walk
connections chosen around the actual border and fixture footprints. Adventure uses an
outer circuit and inner sequence around the quarry water spine; holes 15 and
18 cross the water, with graded tees, fixture landings, a quarry stair and an
upper ledge. Actual fence-post mesh centroids enclose **1,948.55 m² classic /
2,033.50 m² adventure**, excluding the hut and parking: **9.24 / 8.85 holes
per 1,000 m²**. The published Middletown and Oak Island play enclosures give
8.81 / 10.42 respectively. All actual carpet vertices lie inside our fences.
These are density comparators, not copied site plans. `build/routing.json`
separates these measured enclosures from the 1,220.92 m² classic common bed,
the 1,840 m² adventure routing window and the full property. Actual carpet
elevations span .129–.610 m classic and .130–2.590 m adventure.

The grammar always has 18 holes and its signature fixture types. This remains
a bounded original grammar, not arbitrary parcel packing or ball physics.

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
| Service sash | X translation, −2.04–0 m from closed; views show it opened 1.40 m |
| Cup-marker flags | Z, −30–30°, pole base beside cup; authored sagging fabric |

The windmill's lowest swept points cross a 42.7 mm ball's envelope and clear
the actual carpet. Rotor, gate and entry leaf are measured with `kit.motion`
at explicit angular/translation samples; these are sampled clearance checks,
not continuous collision guarantees. Bridge deck/joist/abutment contacts and both crossing-walk bearings are
measured before consolidation. The stream steps are measured on imported water surfaces. Source dimensions and fresh exported cup rays
prove construction; raw counts, socket comparison and import prove serialization.

## Look-dev budgets

Hole totals include the tee, sign, cup, flag, border and playing feature;
fixtures are counted separately. The accepted 2k–8k hole and 15k fixture
ceilings remain unchanged. Botanical and town context are reported separately.

| Seed / kind | Course triangles | Per hole | glTF + BIN bytes | Primitives |
| --- | ---: | ---: | ---: | ---: |
| 71 / classic | 123,982 | 4,144–5,512 | 14,326,195 | 183 |
| 92 / adventure | 172,789 | 4,816–7,166 | 20,399,940 | 199 |

| Hole | Classic 71 | Adventure 92 |
| --- | ---: | ---: |
| 1 | 4,144 | 5,992 |
| 2 | 4,232 | 4,888 |
| 3 | 4,320 | 4,996 |
| 4 | 4,924 | 5,728 |
| 5 | 4,320 | 4,816 |
| 6 | 4,232 | 4,888 |
| 7 | 5,512 | 5,552 |
| 8 | 5,512 | 4,888 |
| 9 | 5,512 | 5,580 |
| 10 | 4,232 | 5,552 |
| 11 | 4,340 | 4,816 |
| 12 | 4,320 | 4,888 |
| 13 | 4,376 | 6,080 |
| 14 | 4,232 | 4,924 |
| 15 | 4,320 | 7,094 |
| 16 | 4,232 | 5,904 |
| 17 | 4,924 | 4,852 |
| 18 | 4,232 | 7,166 |

| Fixture | Triangles |
| --- | ---: |
| castle | 3,524 |
| covered_bridge | 988 |
| lighthouse | 3,084 |
| windmill | 5,536 |
| shipwreck | 6,428 |

Both courses share external 2048² BaseColor, OpenGL +Y Normal and ORM
images for the course atlas, plus a 1024² original graphics sheet. Ground
concrete/asphalt/lawn and fence lumber retain their canonical existing maps.
Ten material states share these images: course, graphics, lit pylon graphics, water, glazing,
lamp, the three Ground states and lumber. The new allocation remains
**17⅓ MiB** compressed with mips; the delivered sets total **81⅓ MiB**, or
**97⅓ MiB** with the shared shrub atlas loaded. [TEXTURES.md](TEXTURES.md)
separates shipping and presentation costs. PNG disk size is not GPU memory. Embedded review GLBs are 78,694,548 /
84,761,468 bytes; their identical embedded images account for most of that
size. The external glTFs share those image files.

The surrounding road uses Ground construction and maps. Actual library
house, strip-mall, station, cars, utility poles, street lights, maple/oak and
boxwood/hydrangea construction supply the setting. Two additional native
boxwood geometry seeds (811/829) bind the canonical shared shrub maps.
Planted-bed footprints are shared by source construction and placement;
foliage envelopes avoid the lanes, fixtures and walks. Context is instanced for
presentation and is not included in the course triangle budget. The companion
`export/Minigolf-{71,92}-context.json` files record placements and source roots,
placed/unique triangles and the complete **192 MiB / 39-image** memory estimate.
Each setting has eight houses across three variants, the strip mall and gas
station, five cars, four street lights and 80 maple/oak instances. Classic has
44 boxwood and 14 hydrangea; adventure has 68 and 22. These native instances
sum to 3,164,068 / 3,346,276 placed triangles from 562,636 unique source
triangles, excluding procedural road and poles. They are presentation context,
not an additional flattened course mesh; the companion recipes preserve
shared source geometry and maps.
Seven native utility poles carry 24 catenary spans between their transformed
primary/neutral hardware sockets. The companion receipt checks actual cable
end-ring centroids against those anchors; it does not claim a surveyed utility
installation.

## Rebuild and inspect

Needs installed Blender 5.2, Python/NumPy/Pillow, open fonts and flock. No
software or executable content is downloaded. All Cycles work holds the shared
kit GPU lock; scratch stays inside the clone. Missing native Ground, lumber,
car, tree, shrub and street-light dependencies invoke their own exporters;
existing deliveries are retained byte-for-byte. The before/after target needs
Git history containing the accepted `0aedb91` revision.

```sh
make -C minigolf WIDTH=1440 SAMPLES=32  # refs, model, check, Cycles, pairs, sheets
make -C minigolf check                # 36 cups, scale, raw normals, budgets, motion, parking, repo
make -C minigolf repeat               # rebuild and compare glTF/BIN/GLB/PNG bytes
make -C minigolf review               # local sheets and GLB tonal receipts
make -C minigolf match                # three neutral-balanced period-photo pairs
```

For alternate proof seeds, run `src/build.py` from the family folder with
`--classic-seed` and `--adventure-seed`; defaults are 71 and 92. The supplied
make/check/presentation recipes intentionally use those two documented seeds.

| Generated local output | Contents |
| --- | --- |
| `export/Minigolf-{71,92}.gltf` + `.bin` | Separate courses, shared external baked PBR images; GLBs are embedded review equivalents |
| `build/course.blend` | Generated look-dev checkpoint, both courses |
| `build/source-construction.json`, `check.json` | Actual gauges, cups, bridge contacts, parking, sockets, sampled motion, 250 seeds |
| `build/repeat.json`, `preservation.json`, `render-check.json` | Byte repeat; every pre-existing delivery/doc remains unchanged |
| `renders/lookdev/{classic,adventure}-hero.png` | Eye measured 1.65 m above imported support, 40 / 35 mm, raking sun, water/fixture/hut/road |
| `renders/lookdev/{classic,adventure}-{ground,above}.png` | Distinct places, full layouts and player viewpoints |
| `renders/lookdev/{tee,cup,border,pond,waterfall,fixture,bridge,clubhouse,sign}.png` | Construction close-ups; measured 1.8 m silhouette in fixture view |
| `renders/lookdev/contact.jpg`, `renders/look-matches/contact.jpg` | 22 GLB views and three period photographs |
| `renders/source-matches/contact.jpg` | Three 4096-field comparisons on identical imported geometry; filtering comparison, not high-poly projection |
| `renders/comparison/contact.jpg` | 13 same-camera pairs, including a separate shoreline and pylon inspection; each original frame is 1440 px wide |
| `renders/look-pass1/`, `renders/look-pass2/`, `renders/look-pass3/` | Rejected first/second-pass images, kept locally |
| `build/photo-calibration.json`, `reference-balance.json` | Estimated cameras, visible residuals, neutral ROI/gains |

The course adds construction beyond the accepted form checkpoint, principally
bridge undersides/girders/bearings, real fixture/clubhouse construction and
planted-bed edges. Hole and fixture ceilings remain unchanged. Source
construction checks are independent of exported serialization checks.
Long-bevel float32 zero tangents are repaired from valid geometry/UV
derivatives in float64; the regression cases reject invalid UVs and preserve
valid tangents. `build/tangent-repair-{71,92}.json` records each repair.

No docs image is committed at this look-dev gate. Full-size review and remaining
CG tells are recorded in REVIEW. No kit code or other delivery is changed.
