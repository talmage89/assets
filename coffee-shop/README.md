# Coffee shop / outdoor seating family

Three original neighborhood businesses for a 1995–2015 American town:
**Folio** in an old Main Street storefront, **Morrow** in a strip-center end
cap, and **Switchyard** in a small converted pad building with a walk-up
window. All geometry, graphics and quick texture pixels are scripted.

**Form and construction checkpoint.** This delivery intentionally stops
before look-dev, manufactured normal baking and age-specific wear. There is
no final docs gallery. The local evidence is the [three Cycles heroes](renders/checkpoint/heroes.jpg),
[drawn seating layouts](renders/checkpoint/layouts.jpg), [piece sheet](renders/checkpoint/piece-sheet.jpg),
[all views](renders/checkpoint/contact.jpg), and [period photo pairs](renders/matches/matched-contact.jpg).
[REVIEW.md](REVIEW.md) records the critiques and remaining weaknesses;
[REFERENCE.md](REFERENCE.md) separates published dimensions from original choices.

## Construction and dimensions

| Proof / business | Host footprint | Seating plan | Authored age |
| --- | --- | --- | --- |
| 117 / Folio | Downtown, **9.144 × 27.432 m**, two stories | 20 ft sidewalk, curbside fenced band, separate public path and west entrance | Old building, freshly fitted room |
| 228 / Morrow | Commercial, two combined 21 ft bays, **12.8016 × 19.5072 m** | Covered through walk with a railed patio outside its columns | Worn entrance and patio, 2004 fit-out |
| 339 / Switchyard | Original pad envelope using Commercial helpers, **10.9728 × 9.144 m** | Split front/side court, separate entry gap and side walk-up connection | Faded, patched 1997 conversion |

Downtown's masonry shell, cornice, sash, recessed iron storefront, stair
entry and rear construction are reused. Its generic shop room/sign/awning
are suppressed and replaced locally. Commercial's two stock bays, flat walk
canopy, wrapped end-cap glazing, coping and services are called directly,
with their stock tenant fit-outs suppressed and demising wall omitted. The
pad calls the same wall/aperture, storefront, leaf, coping and RTU helpers;
its small envelope, side sliding aperture and patch are new. Host-family
source files and every existing delivery remain unchanged.

Visible rooms have customer joinery and a separate back bar with a **.96 m**
working aisle, two-group espresso equipment, two doser grinders, a conventional
drip brewer, register, glass tip jar, cup stacks/pitchers, curved pastry case,
large menus, condiment cabinet, tables/chairs, soft seating, pendants, art and
community notices. Their **6.7 / 7.5 / 7.8 m** depth is a window-visible fit-out,
rather than a full playable restaurant.

The chair uses real **22 mm** bent round stock, a crowned steel seat, curved
expanded-steel back, perimeter/support members and glides. Fine diamond holes
use original coverage in the shared sheet; the frame remains geometry.
The **711.2 mm** round tables have actual open cast lattices, a **742 mm** top,
and either a three-foot pedestal or four splayed legs around an umbrella base.
The latter has a **52 mm** pole guide and **68 mm** top opening around Patio
Set's unchanged **38.1 mm** pole. Its stock open/tied umbrellas retain their
cloth sag, vent, ribs, crank and weighted bases.

Each shop has one **914.4 mm square**, **762 mm high** accessible exterior
table. Imported-surface measurements give **775 mm** between the side rails
at 700 mm height and **732 mm** center underside height; 195 forward rays
test the approach/knee box. The public through corridors are **1.870 / 1.880 /
1.900 m** wide. Separate **.940 / 1.000 / .920 m** connectors continue to the
cafe or side route. The downtown curb buffer is **.9144 m**. Actual furniture,
foliage, canopy edges, feet and rails are tested against the drawn boxes.
These are geometric lower bounds on the shown layouts, not permit or whole-site
accessibility certification. See the municipal/ADA sources and exact limits
in REFERENCE.

## Generator and placement

`src/plan.py` is Blender-independent. An integer `seed` and `kind` (`downtown`,
`strip`, `pad`) choose an identity/palette, two or three outdoor pairs, bounded
counter offsets, table settings, furniture positions and placement seeds.
The pad adds two front tables to its side court. Smaller seating seeds shorten
their fence; the proof seeds use three pairs / three pairs / five tables.
The three types have different circulation and counter orientations, rather
than a common plan with different colors. Names, lettering, menus, paper
masthead and artwork are fictional and generated from installed open fonts.

```sh
python3 src/plan.py --kind strip --seed 812 --out build/custom-plan.json
blender -b --factory-startup --python src/build.py -- --kind strip --seed 812 --out build/custom.blend
```

Build the default once before a custom shop, to create its host cache. A custom
build also writes the reusable stock library and its own `CoffeeShop-812.gltf`;
the default `make` restores the three proof exports. The footprint/depth and
style are fixed within a host type at this checkpoint. This generator does not
claim arbitrary parcel sizes or unbounded procedural architecture.

Coordinates are meters, Blender +Z up and −Y front, glTF +Y up / +Z front.
Each delivered shop root is at its host footprint center on ground grade.
`FrontFrame` is the front-center datum at local Y = −depth/2. Plan coordinates
are relative to that frame. Furniture standalones have footprint/grade origins.
`CoffeeShopPieces.gltf` spreads them for inspection; individual files under
`export/pieces/` retain zero placement.

Chairs remain individually placeable. `*__Seat` sockets mark seated people,
`*__Placement` marks furniture, `*__Top` supports settings, `*__Wheelchair`
marks forward approach, and pendant/sign sockets locate engine lights.
Door leaves retain the host's physical hinge frames: Downtown **local Z
0–100°**, Commercial entry/service leaves **local Z −100–0°**. The pad's
`Walkup_SlidingPane` has local X **−.86–0 m** travel in its rotated wall frame.
Umbrellas are separate open/tied static alternatives; stock cranks turn around
local Y **0–360°**. No armature or folding-cloth animation is provided.
Full pivot/socket positions are in `build/shops/<seed>.json`. Closed-position
closer links are form detail; opening-link kinematics and full swept-door
clearance are not certified by the checkpoint check.

## Budgets and shared images

<!-- METRICS_START -->
| Seed | Shop triangles | Visible room | Materials / mesh primitives | glTF + BIN bytes |
| --- | ---: | ---: | ---: | ---: |
| 117 | 63,572 | 19,286 | 12 / 67 | 4,493,411 |
| 228 | 70,522 | 25,646 | 17 / 95 | 3,976,313 |
| 339 | 71,720 | 20,150 | 15 / 53 | 3,137,177 |

| Reusable piece | Triangles | Measured W × D × H, m |
| --- | ---: | --- |
| BistroChair | 2,156 | 0.538 × 0.588 × 0.836 |
| BistroTable | 1,220 | 0.711 × 0.711 × 0.742 |
| UmbrellaTable | 1,384 | 0.711 × 0.711 × 0.742 |
| AccessibleTable | 244 | 0.914 × 0.914 × 0.762 |
| Counter | 232 | 3.730 × 0.780 × 1.053 |
| EspressoMachine | 1,612 | 0.720 × 0.630 × 0.538 |
| Grinder | 572 | 0.235 × 0.345 × 0.598 |
| Brewer | 480 | 0.216 × 0.477 × 0.445 |
| PastryCase | 1,820 | 1.120 × 0.712 × 1.408 |
| SoftChair | 828 | 0.810 × 0.780 × 0.930 |
| AFrame | 220 | 0.625 × 0.634 × 1.021 |
| Planter | 636 | 0.580 × 0.581 × 0.892 |
| Umbrella_Open | 3,920 | 2.764 × 2.764 × 2.565 |
| Umbrella_Closed | 3,908 | 0.500 × 0.500 × 2.565 |
| BikeRack | 1,020 | 0.868 × 0.152 × 0.914 |
| Litter | 2,966 | 0.700 × 0.702 × 0.960 |
| Recycling | 2,966 | 0.700 × 0.702 × 0.960 |

The three packages reference **14** unique image files / **25,355,801 bytes** across the family. The same-scene import/reimport retains **14 / 14** decoded image datablocks. Construction primitives are counted before optional engine instancing/batching.
<!-- METRICS_END -->

One new shared **2048² BaseColor / +Y Normal / ORM** set is allocated for
furniture, fit-out, original signage and alpha steel/vinyl coverage: **16 MiB**
at 8 bpp per map with complete mip chains. It is a quick form sheet with a
neutral normal map, not a claimed 4096 bake. Opaque, glass and cutout are the
new construction's three material states. Repeated swatch/tile charts overlap
intentionally; final unique baking and texel-density quality remain later work.

The same canonical Patio Set umbrella maps cost **16 MiB**, Street Furniture
rack/litter/recycling **17⅓ MiB**, and Ground concrete **16 MiB**. Downtown's
existing sign sheet adds **5⅓ MiB** for retained upper-building marks. Quick
host walls otherwise use their form palette. Thus current shop texture loads
are approximately **70⅔ / 65⅓ / 65⅓ MiB**, shared across instances and seeds.
These exclude presentation context and geometry. PNG disk bytes are reported
separately by the generated table. Adding another chair or table allocates no
new texture. The low-cost accessible table, counter, brewer and A-frame are
below the preferred 500-triangle lower end because their construction needs
fewer faces; they are not padded with hidden detail.

For look-dev, the plan is to bind Downtown's existing masonry/mineral/finish
sets or Commercial's existing wall/roof/equipment sets, retaining this single
new cafe set and the existing furniture/ground resources. No extra per-seed
wear texture is planned: causal large wear belongs to each placed instance,
while small manufacturing detail belongs to the shared maps. Downtown gets
fresh fixtures in an older shell; the strip gets door/drag wear; the pad gets
sun fading, repairs and valance deposits. That work is intentionally pending.

External-image glTFs and geometry bins sit in `export/`. Reused images resolve
to their canonical family paths; only the new form set and retained Downtown
sign sheet live under `coffee-shop/export/textures/`. Keep relative directory
layout and cache resolved image URIs in the engine. Embedded GLBs under
`build/` are inspection intermediates. Fresh import of all three seeds and a
repeat checks decoded image reuse, rather than assuming equal filenames mean
equal GPU resources.

## Rebuild and evidence

```sh
make WIDTH=1600 SAMPLES=48       # refs, hosts, stock, shops, checks, Cycles, pairs, sheets
make check                      # checkpoint geometry/resources/clearance checks
make repeat                     # isolated deterministic stock/host/shop rebuild
make check-repo
```

Missing original family dependencies build through their own public targets;
present deliveries are read-only inputs and are never refreshed by the coffee
build. Blender jobs are serial and all Cycles rendering uses the kit's shared
GPU lock. Work and temporary files stay in ignored build folders. No kit file
or top-level README is changed. Requires Blender 5.2, Python/Pillow/NumPy,
fontconfig/open DejaVu fonts, GNU make, curl and flock; no installation occurs.

| Local path | Evidence |
| --- | --- |
| `export/CoffeeShop-<seed>.gltf` + `.bin` | The three shop packages, external shared images |
| `export/pieces/*.gltf`, `CoffeeShopPieces.gltf` | Independently placeable new/reused stock and inspection library |
| `build/check.json` | Fresh-import counts/bounds/normals/UV presence, actual route surfaces, knee-space rays, image resources |
| `build/preservation.json` | Hashes of all preexisting family delivery/map inputs |
| `build/repeat.json` | Deterministic byte comparison with normalized canonical URIs; no GPU bake at this gate |
| `build/photo-calibration.json` | Named landmarks, estimated cameras, residuals and assumed-neutral balance |
| `renders/checkpoint/<seed>/` | Eye-height 40/45/42 mm hero, overhead, drawn clearances, table/counter/awning/chair details, 1.8 m scale; pad walk-up |
| `renders/checkpoint/piece-sheet.jpg` | Every furniture/fit-out module with labels |
| `renders/checkpoint/contact.jpg` | All current views and three photo pairs |
| `renders/matches/*-pair.jpg` | The actual export against three neutral-balanced 2008 photographs |
| `build/presentation-check.json` | Current package/image hashes and hero display-range diagnostics |

The checkpoint is not a final game-readiness certificate. The strongest
remaining tells are the quick flat host surfaces, overly orderly pastry and
smallware arrangements, simplified joinery/hardware, sparse setting and the
absence of each age's causal wear. Some fine glass reflections obscure the
menus; the photographic umbrella and pad fits reach their 70 mm lens bound.
These limitations remain explicit in REVIEW. Reference credits, primary
specifications, newspaper archives and font licenses are in SOURCES.
