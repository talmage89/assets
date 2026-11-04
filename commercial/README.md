# Commercial / seeded corner gas stations

**Form checkpoint, before look development.** Four original American corner
stations of the 1995–2010 type, intended to represent maintained fifteen-year-old
sites after the next surface stage. Current quick materials intentionally carry
no accepted manufacture or service wear. These are diagnostic GLBs, with actual
separate reusable modules, doors and nozzle sockets; they are not finished game
packages or baked portfolio assets.

The family starts with the station. The later strip mall can reuse the retail
wall/opening grammar, aluminum storefront bays, hinged leaves, parapet/coping,
membrane roof, rooftop units, drains and services. Fuel equipment and corner
planning are separate from that building code. Nothing is downloaded as a model,
material, texture, decal, lighting environment or executable.

[REFERENCE.md](REFERENCE.md) distinguishes published dimensions, original design
choices and camera-fit limits. [REVIEW.md](REVIEW.md) records rejected form passes.
[TEXTURES.md](TEXTURES.md) explains the shared texture/memory plan, and
[refs/SOURCES.md](refs/SOURCES.md) credits photographs and published drawings.
All review images are ignored rebuild outputs; no unfinished docs JPGs enter Git.

## Four original plans

| Seed | Lot, ft | Store, ft / area | Canopy / fueling positions | Corner / walls / brand / price sign |
| --- | --- | --- | --- | --- |
| 101 | 150 × 150 | 60 × 50 / 3,000 sq ft | 3 islands, parallel; 6 faces | SW / split CMU / Rillway / corner monument |
| 102 | 140 × 150 | 56 × 48 / 2,688 sq ft | 2 islands, perpendicular; 4 faces | SE / brick / Latchline / south-frontage pylon |
| 103 | 160 × 160 | 64 × 48 / 3,072 sq ft | 4 islands, parallel; 8 faces | NW / smooth CMU / Latchline / west-frontage monument |
| 104 | 160 × 160 | 66 × 50 / 3,300 sq ft | 3 islands, 30° to store; 6 faces | NE / EIFS / Rillway / corner pylon |

Both streets have a 24 ft commercial opening and 5 ft transition wings. The
source keeps the ground family's 6 in grid, 5 ft sidewalk, 6 ft planting strip,
15 ft corner radius and curb/gutter section. The extended commercial opening
uses that section at its real dimensions, rather than scaling a 10 ft house cut.
The outer sidewalk meets site grade with the native 1% crossfall; the curb
flowline is .16764 m below it. The lot is centered on grade, Blender +Z up and
canonical −Y store front; a
quarter turn places it on its geographic corner. Each module retains a local
footprint/ground origin. Above views use one geographic camera orientation and
fit every exported
station vertex inside a measured 4% image margin;
street cameras stand across each seed's own corner at 1.68 m.

The canopy has **4.4196 m / 14 ft 6 in nominal soffit clearance**, a .9906 m /
3 ft 3 in fascia and .3556 m / 14 in square outer columns. Island centers are
7.62 m / 25 ft apart. Each combined column/pump/service island is 1.2192 ×
5.4864 m / 4 × 18 ft, .1524 m above the concrete pad, leaving 6.4008 m / 21 ft
between curbs. Their round ends, base plates, anchors, pipe guards, supported
drains, hollow fascia and flush light openings are geometry. Small soffit joint
relief lies below the nominal plane; the posted height is not an engineering
clearance certification. Published dimensional comparators and limits are in
REFERENCE, including 12 in steel-column literature and the different broader
clad columns in the Pennsylvania photograph.

Store slabs sit .1524 m above the site; their 203.2 mm wall shell has actual
storefront/service openings. Window heads are 2.75 m, the membrane datum 3.9624 m,
and parapet 4.8768 m. Coping has folded returns and hems. The exterior includes
divided glass, dark shallow retail/entry backings, fictional posters, ice cabinet,
propane cage, two RTUs, scuppers/downspouts, electrical service, selected cooler
boxes, and a gated CMU dumpster yard. It is an exterior asset, not a playable
retail interior or engineered construction set.

Every fictional **Cairn M3** dispenser has two faces, a 1.10 m cabinet, .62 m
electronics depth, 1.19 m crown and 2.24 m crown height above its island. Three
gasoline products share one hose on each face, with individual unit-price windows
and grade buttons. Both faces carry the fuel brand and separate fictional maker.
Hoses are 30 mm outside diameter,
with breakaways, retractors, a tether attached to the actual curve, a slack loop,
swivel and original compound-section cast nozzles. Small controls/graphics share
one generated preview sheet; contour fonts do not consume pump triangles.

Fill covers use API color/symbols: white/black cross regular, blue/white cross
plus, red/white cross premium, orange vapor; the alcohol-extender borders and
monitoring-well triangles are explicit. Three 12 ft vent risers stand at the
outer lot edge. Concealed tanks and plumbing are omitted. Air/water, accessible
parking/sign/approach with a 6 ft ramp run and a 6 ft level landing in the 12 ft
walk, wheel stops, continuous landscape strips, low shrubs and lot lights
complete the form program.

## Generator and reuse

`src/plan.py` is Blender-independent. `generate(seed, overrides)` emits the
lot, `BuildingSpec`, canopy axes/spacing/count, islands, sign, driveway sockets
and parking. The four fixed proof seeds preserve the table above. Other seeds
vary bounded store dimensions, corner, brand and sign within four supported
planning topologies; a 1,000-plan sweep checks them. Unsupported controls and
islands intruding on reserved circulation space fail.

`src/build.py --plan` accepts a JSON override, for example,
`{"brand":"latchline","sign":"pylon","cooler":false}`.
`store` is `(width_ft, depth_ft, front_y_ft)`; `lot` is `(width_ft, depth_ft)`;
`count`, `angle`, `canopy_y` in feet, `yaw`, `wall`, `brand` and `sign` are bounded
controls. `sign_placement` selects `corner`, `south` or `west`; frontage
placements orient the cabinet toward their street. Angles are 0/30/90° within the canopy frame; corner yaw is a quarter
turn. These are validated plans rather than independent random object placements.

From `commercial/`, an override saved to `build/variant.json` builds separately:

```sh
blender -b --factory-startup --python src/build.py -- --seeds 101 --plan build/variant.json --out build/custom/station-101.blend
```

`building.py` exposes `wall_with_openings`, `storefront`, `glazed_leaf`,
`retail_shell` and `rooftop_unit`. `equipment.py` builds reusable pumps/signs/
props; `siteworks.py` handles paving and interfaces. Shared low-level boxes,
lofts, tubes, pivots and fonts come from `kit/`. No kit file changed.

Two original brands are applied consistently to canopy, pumps, sign and store:
**Rillway**, aubergine/copper/ivory with three unequal piers; **Latchline**,
graphite/periwinkle/off-white with offset square brackets. Neither uses familiar
red/yellow, green/yellow or red/blue/white fuel trade dress, stars, shells,
flowers, dinosaurs, arrows or maple leaves. REFERENCE records the US/Canadian
comparison and its scope. The future equal-cell decal sheet makes brand swaps
geometry-independent; raised form marks are current placeholders.

## Measured checkpoint budgets

Counts include moving leaves, hoses, original cylinders and service equipment.
Paving is separate; presentation roads, house and pickup are excluded.
Each diagnostic station has 24 used source material states and one 2048²
lettering image, not a final material/atlas budget. Raw-accessor/fresh-import checks are
separate from construction measurements.

| Seed | Store | Canopy + islands | Each dispenser | Price sign | Whole station | Diagnostic GLB bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 101 | 18,980 | 5,670 | 5,716 | 908 | **63,826** | 4,835,120 |
| 102 | 17,592 | 4,390 | 5,980 | 1,216 | **55,042** | 4,278,400 |
| 103 | 19,112 | 7,478 | 5,980 | 1,172 | **74,200** | 5,524,148 |
| 104 | 19,732 | 5,670 | 5,716 | 952 | **64,818** | 4,961,760 |

Default seed 101, including all parts placed on its site:

| Part | Copies | Triangles each |
| --- | ---: | ---: |
| Store, entries/service door/RTUs/drains | 1 | 18,980 |
| Canopy/islands/column guards | 1 | 5,670 |
| Dispenser, two hoses and detachable nozzles | 3 | 5,716 |
| Price monument | 1 | 908 |
| Paving, walks, street edges and continuous planting beds | 1 | 3,848 |
| Tank pad and covers | 1 | 1,164 |
| Tank vent assembly | 1 | 376 |
| Trash/washer/towels/squeegee | 3 | 1,116 |
| Ice merchandiser | 1 | 1,808 |
| Propane cage, doors and eight original cylinders | 1 | 4,474 |
| Dumpster enclosure, gates, container/lids | 1 | 2,316 |
| Air/water machine and hose | 1 | 1,634 |
| Store bollard | 4 | 252 |
| Accessible sign | 1 | 448 |
| Light pole | 2 | 348 |

Checkpoint checks distinguish measured construction from export fidelity:

- Four outside masonry rays verify each authored shell width/depth. Two
  rear scupper passages are open through the actual wall and sleeve.
- Nine roof rays per seed read 3.9849 m at the membrane surface; the coping top
  reads 4.9128 m. Canopy nominal clearance reads 4.4196 m; its cap reads 5.4482 m.
  Island widths/lengths and hose surface radii are independently probed.
  Ramp rays read .01524 / .07620 / .13716 m through the 1:12 run; three
  independent top-landing samples read .15240 m.
- Eleven solid moving assemblies per seed pass 237 sampled poses at 5° intervals
  (948 poses total), with 1 mm penetration tolerance and no allowed-contact exceptions.
- Native straight/cut curb profiles from the delivered ground GLB match 48 actual
  station surface samples per seed within 0.000004 m across all four corners.
  This checks the section, not a complete road-crown or whole-street tiling assembly.
- Full-body 5.70 × 2.14 m pickup envelopes pass forward-only routes with occupied
  store stalls, through a fueling lane and the other street opening. The four
  minimum separating-axis gaps are .225 / .310 / .225 / .286 m. These deliberately
  tight demonstrated paths are not tanker sweeps or opposing-traffic simulations.
  The extended pure-plan regression also passes all 1,000 seeded pickup routes;
  physical source/export checks remain on the four displayed proof seeds.
- Raw GLB triangles agree with source totals; unit-normal error is below 1.2e−7.
  Fresh-import positions agree within 7.7 µm and pivot/socket matrices within 5.8e−6.
  Those checks prove serialization, separately from the surface and motion checks.
- A second factory-startup seed-101 build produces a byte-identical diagnostic GLB.

The store, canopy and price sign are below the brief's preferred ranges at this
form stage. Their silhouettes and operating assemblies are retained; there is
no reason to add invisible framing or pad triangles to reach a lower bound.
The later material charts, causal weather samples and optimized detail transfer
still have room within the stated ceilings. Pumps are below their 6k ceiling;
small props are at or below their relevant tiers. Low-sided bollards and poles
are lean repeated modules whose finer fasteners belong in the trim normal.

The shared delivery plan is **39⅔ MiB of new commercial maps**, plus the two
existing ground paving triples (**32 MiB**), for **71⅔ MiB** across the complete
commercial family. A neighborhood already using ground adds only 39⅔ MiB.
The strip mall reuses these sets. These are BC7/BC5 estimates with full mipmaps,
not PNG bytes or measured engine uploads; see TEXTURES for every allocation.
No final PBR texture bake or UV-density certification has run.

## Parts, motion and sockets

Fixed construction is consolidated per reusable module. The station's GLB
retains `Store`, `Canopy`, `Dispenser_<n>`, `PriceSign`, `SitePaving`, `TankPad`,
`TankVents`, `TrashWasher_<n>`, `AirWater`, `IceMerchandiser`, `PropaneCage`,
`DumpsterEnclosure`, store/island bollards, accessible sign and light poles.
Nozzle meshes and hinged leaves remain separate. Helpers carry local frames;
no armature is used.

| Moving node | Local axis / range | Origin and use |
| --- | --- | --- |
| `Entry_Left` / `Entry_Right` | Z, −100…0° / 0…100° | Outer jamb hinge barrels; paired outward leaves |
| `ServiceDoor` | Z, −100…0° | Rear steel leaf's physical exterior hinge |
| `IceDoor_-1`, `IceDoor_1` | Z, −100…0° | Independent left-hinged insulated utility doors |
| `PropaneDoor_-1`, `PropaneDoor_1` | Z, −100…0° | Independent front cage gate hinges |
| `DumpsterGate_-1` / `DumpsterGate_1` | Z, −110…0° / 0…110° | Yard's outer front jambs |
| `DumpsterLid_-1`, `DumpsterLid_1` | X, −105…0° | Rear edges, above an actual open steel container |
| `Dispenser_<n>_NozzleA/B` | Detachable rigid rest frame | Nozzle body, hand socket and holstered pose; hose deformation/controller is future runtime work |

`...__Hand` nozzle sockets lie in the grip; door handles have their own hand
socket. `Socket_StoreEntry` and `Socket_StoreWalk` expose the retail approach; the walk helper is the frontage grade datum beneath the store
face, not the outer edge of the paved approach.
`Socket_Drive_south/west` expose the private paving interface.
`Socket_GroundCurb_*`, `Socket_GroundApron_*` and `Socket_GroundWalk_*`
expose the native ground flowline frames, including its actual vertical offset.
Their local +X points inward across each 24 ft opening before the station's
global corner rotation. Source JSON and glTF extras retain actual per-seed frames.
Blender Z becomes glTF Y; local X lid hinges remain X. The motion audit samples
the actual solid surfaces at 5° increments and distinguishes this construction
proof from simply preserving node transforms during serialization.

Original scripted 20 lb cylinders fill the exchange cage. The owner's external
tank is used only by the optional read-only fit audit, never joined, baked,
modified, saved or exported. Its imported .3122 m diameter × .4680 m height
fits the cage; horizontal bay choices and ray-measured shelf height are reported
separately in `build/tank-fit.json`.

## Rebuild and review evidence

From the clone root:

```sh
make -C commercial WIDTH=1440 SAMPLES=40  # all four forms, checks and Cycles evidence
make -C commercial check                 # grammar, surfaces, motions, raw GLBs/import, repo
make -C commercial model                 # no bake or rendering
make -C commercial match                 # two dated photo comparisons
make -C commercial scale                 # same-scale split-level and pickup
make -C commercial repeat                # independent factory-startup byte repeat
make -C commercial fit TANK_REFERENCE=../../.foundry/shared/propane-tank.glb
```

The last command needs the expressly authorized local owner reference, not
provided by this repository. On another clone, pass its own authorized path.
The scale shot imports this worktree's existing `houses/export/HearthfieldSplit-51.gltf`
and `cars/export/AlderC150.glb`, for presentation only. Existing
exports are reused when present; `src/context.py` builds missing same-worktree
exports with those families' own Makefiles. Hashes include the house's external
buffer and maps. The station never changes or re-exports loaded context.
All Cycles renders hold the shared GPU lock and enable OptiX/CUDA through kit.
Scratch and generated data stay in ignored worktree `build/` directories.

| Local output | Evidence |
| --- | --- |
| `build/station-<seed>.blend/.glb/.json` | Four independent source forms, stock diagnostic exports, counts/frames |
| `build/plan-check.json` | 1,000 bounded plans and pickup routes, eight invalid controls; four named proof routes |
| `build/checks.json`, `build/motion-<seed>.json` | Actual roof, island and hose probes; fixed entry opening; motion; independent raw attributes/import/pivots |
| `build/tank-fit.json` | Optional owner reference bounds and actual cage shelf clearance |
| `build/repeat-check.json` | Independent factory-startup seed-101 geometry/embedded-image repeat |
| `renders/checkpoint/hero.png` | Cycles from exported GLB, eye at 1.68 m across the corner |
| `renders/checkpoint/seeds/<seed>/{above,street}.png` | Each whole property and each actual street approach |
| `renders/checkpoint/{dispenser,canopy,entry,sign}.png` | Required construction close-ups |
| `renders/checkpoint/{rear,motion,scale}.png` | Services, paired open entry, split-level/pickup at common meter scale |
| `renders/matches/*-pair.jpg` | Two kit-calibrated comparisons, with original dated photos and disclosed neutral balance |
| `renders/checkpoint/{family,details,circulation,contact}.jpg` | Review sheets; never committed portfolio images |
| `build/view-check.json` | Current source/image/recipe hashes for the checkpoint |

Weakest at this gate: broad surfaces are deliberately smooth and unaged; brick,
split-face CMU and EIFS differ by quick color, not accepted manufactured relief.
The light/shadow and glazing are controlled outdoor previews with simple retail
backings and a spare landscape. Prop cylinders, pipe bends and tiny fittings
remain coarse at extreme close-up. The small cooler condenser still uses the
large RTU helper's fan/grille proportions and needs a size-specific refinement.
Original plan and column/cabinet differences
remain visible in the photos; a small camera-fit residual does not erase them.
Brand/decal geometry independence, final draw calls, shared map reuse, UV/density,
baked wear and exported-PBR photo fidelity await the requested next stage.

Stop here for form review. There is no strip-mall asset, completed look-dev,
texture bake or final portfolio delivery hidden behind this checkpoint.
