# Parking garages — form and baked look-dev checkpoint

This is a review checkpoint, before README galleries or `docs/` images.
The accepted four-level municipal and three-level commercial programs,
stalls, ramps, floor surfaces, paths and public generator limits are retained.
The original 63 garage delivery files and 559 other-family delivery files
are protected by SHA-256 manifests; new deliveries use `export/lookdev/`.
No shared-kit implementation changed.

## What changed, and where to inspect it

All paths below are generated locally by `make`. Full views are 1280 pixels
wide; each before/after panel is at least 1200 pixels wide without enlargement.
The comparison script checks camera position, lens and aspect before assembly.

| Fix | Fixed-camera evidence | Final view |
| --- | --- | --- |
| Daylight, floor bounce, physical wraparound fixtures | [Municipal aisle](renders/fixes/101-retained_aisle.jpg), [commercial aisle](renders/fixes/202-retained_aisle.jpg) | [Municipal aisle](renders/lookdev-checkpoint/101/aisle.png), [tee underside](renders/lookdev-checkpoint/101/tee_detail.png) |
| Deep tee stems, tapered sections and dapped bearing ends | [Municipal aisle](renders/fixes/101-retained_aisle.jpg) | [Exported precast pair](renders/lookdev-checkpoint-matches/precast-pair.jpg) |
| Stair flights, landings, glazed lift shaft, doors, cab, panel joints, cap and machine hood | [Municipal tower](renders/fixes/101-tower.jpg), [commercial tower](renders/fixes/202-tower.jpg), [open municipal lift](renders/fixes/101-tower_open.jpg) | [Landing](renders/lookdev-checkpoint/101/tower_landing.png), [open commercial lift](renders/lookdev-checkpoint/202/tower_open.png) |
| Spandrel reveals, seals, rails, runoff, level colors, garage name/hours and backed turn warnings | [Municipal facade](renders/fixes/101-retained_hero.jpg), [commercial facade](renders/fixes/202-retained_hero.jpg) | [Municipal hero](renders/lookdev-checkpoint/101/hero.png), [commercial hero](renders/lookdev-checkpoint/202/hero.png) |
| Street foreground, meters, queue, closing town blocks and maintained turf | [Municipal entry](renders/fixes/101-entry.jpg), [commercial entry](renders/fixes/202-entry.jpg) | [Municipal above](renders/lookdev-checkpoint/101/above.png), [commercial above](renders/lookdev-checkpoint/202/above.png) |
| Seeded wear at its causes, coated traffic surface and worn top-deck sealer | [Municipal turn](renders/fixes/101-ramp_turn.jpg), [commercial turn](renders/fixes/202-ramp_turn.jpg), [municipal top](renders/fixes/101-top_deck.jpg), [commercial top](renders/fixes/202-top_deck.jpg) | [Top deck](renders/lookdev-checkpoint/101/top_deck.png) |

The [final contact sheet](renders/lookdev-checkpoint/contact.jpg) includes the
two garages and all source/baked photographic pairs. The [before/after sheet](renders/fixes/contact.jpg)
indexes sixteen comparisons. The drawn drive route appears only in the
dedicated [municipal plan](renders/lookdev-checkpoint/101/plan_path.png).
Heroes retain 35 mm lenses at 1.65 m eye height, with a clear procedural sky
and low raking sun; their wider crop reduces empty road without changing lens.

The PCI section is 12 ft wide, 30 in deep, with a 4 in flange and stems at
6 ft centers. Tapered webs and end daps preserve the original bearing seats.
Only central ramp stations rise; the level end platforms remain level.
The maintained turf reuses Ground Lawn maps, world-space density and School's
maintained tint, with a small geometric fringe at the mown edge.
The municipal service-history preset is stronger than commercial (relative
strength 1.0 versus 0.65); seed-owned positions and widths vary leaks, deposits,
patches and tire transfer. These are artistic upkeep controls, not measured years.

## Geometry and resources

| Garage | Structure, towers, graphics and age | Cars | Other context | Complete scene |
| --- | ---: | ---: | ---: | ---: |
| 101 municipal | 136,638 | 13,540,116 / 201 instances | 1,342,324 | 15,019,078 |
| 202 commercial | 54,466 | 6,026,168 / 91 instances | 1,319,376 | 7,400,010 |

The municipal cars comprise 196 in the garage, four on the street and one
in the entry queue. Commercial has 56 inside, 30 in the surface court, four
on the street and one queued. Existing car meshes and weekday occupancy
are retained. These are placed triangle totals, including instances, not
unique mesh storage. Town/car resources are outside the garage budget.

The prior garages were about 95.7k and 44.4k triangles. The additions above
pay for actual tower interiors, 30 in tee construction, facade/opening details,
and sparse causal age films; accepted circulation geometry remains unchanged.
Both stay below the brief's 300k whole-garage limit. Every ordinary module is
below 2k; the tallest tower stays below 8k. Individual exported module counts:

| Piece | Triangles | Piece | Triangles |
| --- | ---: | --- | ---: |
| DoubleTee | 384 | InvertedT | 28 |
| LBeam | 20 | ColumnCorbel | 76 |
| CorbelPair | 48 | ColumnPlain | 28 |
| PTColumn | 28 | PTSlab | 148 |
| PTBeam | 44 | Spandrel | 100 |
| CableBarrier | 260 | PTGuard | 192 |
| Fixture | 88 | WheelStop | 44 |
| Drain | 128 | Gate | 136 |
| Ticket | 80 | PayStation | 80 |
| Tower3 | 4,580 | Tower (four levels) | 6,168 |
| Tower5 | 7,756 | StructuralBay | 1,496 |
| EndBay | 1,496 | RampBay | 1,496 |
| PTStructuralBay | 644 | | |

The one new shared sheet carries bare precast/cast concrete, coated traffic
concrete, steel, small hardware colors and causal wear masks. It is actually
baked in Cycles at 4096, then shipped at 2048 as BaseColor, OpenGL Normal
and ORM. Coverage is retained independently from baked RGB; normals filter
as vectors and roughness as RMS. Periodic guards reconcile duplicate bake
samples in linear color/vector space. There is no downloaded texture input.

| Resident images, shared across both garages | Compressed+mipped estimate |
| --- | ---: |
| New ParkingGarage three-map 2048 set | 16 MiB |
| Extended GroundParkingTrim 2048 RGBA page | 5.33 MiB |
| Existing GroundTrim three-map 2048 set | 16 MiB |
| Existing Concrete three-map 2048 set | 16 MiB |
| Existing StreetLight three-map 1024 set | 4 MiB |
| **Garage family total, 13 images** | **57.33 MiB** |

This is an estimated block-compressed GPU allocation including mipmaps, not
PNG size. Towns, trees and cars have their existing separate sets. The private
eight-level photo specimen has an additional diagnostic graphics page; it is
outside the game-family residency. Each public garage has eleven material
slots, including reused ground/light/glass/graphics and the atlas's coverage
and emissive variants. Those atlas variants share the same three images.
Including the town and cars, unique scene images total 142.67 MiB municipal
(29 images, 50 material slots) and 148 MiB commercial (30 images, 64 slots).
The extra residency is reused Lawn/Asphalt, two tree sets, the shared car set
and town sign pages; it is not another newly manufactured garage set.

The three shipped PNGs occupy 2,164,043 / 5,309,779 / 844,571 bytes
(BaseColor / Normal / ORM). Municipal glTF JSON/BIN are 1,805,734 / 23,421,960
bytes; commercial are 651,391 / 8,742,796 bytes. The garage-only review GLBs
are 47,940,560 and 32,106,600 bytes respectively. Images remain external and
shared in the glTF delivery. Complete site GLBs also exist as rebuildable review conveniences;
they duplicate shared images and are not committed delivery sources.
Per-placement triangle ledgers are in [101](build/lookdev/look-101.json) and
[202](build/lookdev/look-202.json); [site resources](build/lookdev/sites.json)
separate every actor category from the static surroundings.

## Photographic comparisons

| Photo | Native landmark RMS | Exported baked pair | Original-field pair |
| --- | ---: | --- | --- |
| Precast underside | 15.806 px | [Baked](renders/lookdev-checkpoint-matches/precast-pair.jpg) | [Source](renders/lookdev-checkpoint-source-matches/precast-pair.jpg) |
| Pleasant Hill facade | 14.923 px | [Baked](renders/lookdev-checkpoint-matches/pleasant-pair.jpg) | [Source](renders/lookdev-checkpoint-source-matches/pleasant-pair.jpg) |
| Harmon cast deck | 5.674 px | [Baked](renders/lookdev-checkpoint-matches/harmon-pair.jpg) | [Source](renders/lookdev-checkpoint-source-matches/harmon-pair.jpg) |

The preserved previous pairs are [precast, 45.7px](renders/before/matches/precast-pair.jpg),
[cast deck, 62.7px](renders/before/matches/harmon-pair.jpg), and the already
accepted [facade, 14.9px](renders/before/matches/pleasant-pair.jpg).

The precast diagnostic uses flat spans, actual inverted-T seats, 30 in tees
and four native cars. Its surrounding roof continues across eighteen tees
and three transverse spans. The visible central members retain their measured
coordinates; the continuation outside the photo crop supplies surrounding
shade, not a claim to have measured the photographed garage's full footprint.
The cast diagnostic uses eight levels, round cast
columns and the photographed edge downstand. Those variants match the photos'
construction rather than forcing the accepted town programs into those views.
The public generator still has its accepted three-to-five-level limits.
Harmon's close crop has an estimated 113.4 mm effective lens; it is a
photo diagnostic, separate from the 35 mm public heroes.

The concrete neutral is a bare column patch, not the taped white notice.
`build/lookdev/matches/calibration.json` records the fitted points, crop,
camera and native-pixel residuals. These residuals prove landmark projection;
they do not certify an entire silhouette or material match. The pairs remain
the evidence for appearance. Source pairs retain the same exported geometry,
with the analytic manufacture fields substituted for the filtered bake.
References and permitted uses are recorded in [SOURCES](refs/SOURCES.md).

Light-isolation tests found the earlier short specimen admitted too much sky
onto its camera-facing column. Roof continuation corrects that construction
error. The comparison uses broad wraparound practicals at 1.5 times the public
view preset, with the sun behind the visible column face; the public scenes
keep their existing lighting. Narrower downward distributions created harsh
floor pools and were rejected. Temporary wet-floor material probes darkened
the floor without correcting the column; they were also rejected and are not
part of the exported family. The remaining floor-state difference is explicit
in the critique rather than hidden by a local color adjustment.

Final displayed-image measurements against the concrete-balanced photo:

| Precast surface | Photo median linear Y | Export median linear Y |
| --- | ---: | ---: |
| Bare column | 0.10930 | 0.13066 |
| Shaded soffit | 0.00794 | 0.00720 |
| Foreground floor | 0.06963 | 0.05117 |

The column is about 20% brighter; the floor remains about 27% darker and warmer.
Those readings compare illumination and finish together, not intrinsic albedo.
Both public heroes have zero clipped RGB pixels. Their linear-Y p1/p99 values
are 0.00030/0.70944 municipal and 0.00126/0.72468 commercial, including context
and sky. Deep shade remains inside the levels while sunlit concrete rolls off.

## Mechanical and serialization proof

Fresh imports test actual bounds, triangle counts, unit normals, UV chart
membership, noncollapsed UV triangles, accepted route coordinates and floor
surface contacts. Repeating tiling charts intentionally overlap UV space;
this is not a unique lightmap atlas. Area-weighted 2048 texel density p5/median/p95
is 314/333/333 px/m municipal and 250/333/333 px/m commercial.

Measured minimum aisle headroom is 2.54080 m municipal and 2.58980 m commercial;
the accessible route minimum is 2.48920 m for both, including fixture housings
and diffusers. These are sampled rays against imported surfaces, not continuous
clearance certification. Imported path/floor discrepancies are below 0.001 mm.
The queue's four native tire contact patches now follow the actual apron:
maximum signed-surface discrepancy is 0.0682 mm municipal and below 0.0001 mm
commercial. The former municipal rear-wheel gap was 33.85 mm.

All sixty gate, stair, street-door and elevator-door pivots pass their sampled
full-motion sweeps against neighboring actual meshes. The lift has a fixed
ground-floor cab with floor, walls, ceiling, guide hardware and inner sliding
panels; no elevator travel controller or vertically animated cab is claimed.
New interior door panels follow the existing door pivots and travel ranges.
Open-door views make the usable threshold and cab visible.
Formed 2 mm metal pockets now conceal the complete door travel. A first
zero-thickness version failed solid-containment tests despite zero triangle
crossings; closed skins pass without collision exemptions. Six-sided sections
on the small 30/38 mm stair tubes recover the triangles needed for those skins,
preserving actual diameters and paths. The original delivery retains its
original tube tessellation. The tallest revised tower is smaller than the
earlier pocketless version.

Geometry checks establish construction/serialization facts; they do not
establish photorealism. See the color-first critique history in [REVIEW](REVIEW.md).

## Remaining visual weaknesses

The checkpoint is materially improved but still reads as CG in several places.
Runoff sometimes resolves into comb-like groups; distant lawn plots are still
smoother than photographed grass. Repeated native car families, identical
fixture spacing and simplified neighboring buildings reinforce the procedural
rhythm. The elevator cab is intentionally a static ground-floor enclosure.
The commercial hero's surface-parked cars obscure much of its entry queue;
the entry close-up shows that actor clearly. Some foreground meters are
hidden by the crossing tree. The street framing is improved, but it does not
make every small foreground component independently legible in one image.

The hero carries cap runoff, failed joints, patching and larger traffic history.
The smallest oil, rust, salt and roost deposits resolve in details rather than
each being independently recognizable in the full-frame hero. That part of the
requested visibility bar is weaker than intended. The photographed precast
floor is wet and highly reflective, with broad cleaning/tire swirls; the dry
coated specimen does not reproduce that water state. Upper-deck sealer wear is
still subtle. The Harmon facade remains
cleaner and more uniform than its photograph despite the improved section and
camera. Tight landmark residuals must not be read as acceptance of those looks.

## Rebuild and verification

From `parking-garage/`, `make` builds the separate form and look-dev exports,
manufactures and bakes the shared atlas, runs construction/resource checks,
renders the review set under the shared GPU lock, and assembles the comparisons.
`make check` runs the accepted checkpoint checks plus the new import/atlas,
headroom, contact, preservation, dependency and sixty-pivot motion checks.
No rendering/baking lock is held during CPU model construction or checking.

Both plain `make` and the explicit `make check` exited successfully. Check output is retained in
`build/lookdev/final-check.log`. All sixty revised motion sweeps have zero
violations. The repository rules check reports 2,148 source files and zero
errors. The plain `make` run's output is in `build/lookdev/final-make.log`.

`make lookdev-repeat` passed: three source PNG fields, their chart layout,
and 82 generated form/look-dev/graphics delivery files, totaling 368,198,254
bytes, rebuilt exactly. This repeats tower/tee construction, town instancing,
private reference variants, UV binding, seeded age and export. The receipt is
[repeat.json](build/lookdev/repeat.json), with subprocess output in
`build/lookdev/repeat-build.log`. Canonical baked maps remain immutable during
that test; an independent GPU repeat is a separate check.

The independent GPU repeat also passed its predeclared maximum one-code and
mean 1e-5 tolerances. BaseColor and ORM are byte-identical. Normal differs in
three of 4,194,304 pixels, each by one 8-bit channel code (mean normalized
channel error 9.35e-10). This is a tolerance-based GPU result, not a claim of
universal GPU bit identity. Canonical maps were not overwritten. See
[bake-repeat.json](build/lookdev/bake-repeat.json). The executed combined batch
is `../kit/with_gpu.sh blender -b -t 2 --factory-startup --python-exit-code 1
--python build/lookdev/repeat-and-camera.py`: it runs the repeat, then the
standard 1280px/32-sample review batch with source pairs and baselines. The
reusable bake-only target is `make lookdev-bake-repeat`.

`python3 src/preserve.py` passed for all 63 original garage files and 559
other-family deliveries. The full [import/geometry receipt](build/lookdev/check.json)
records module budgets, map hashes, headroom, route surfaces, tire contact,
texel density and exact periodic chart edge agreement.

Nothing is needed from the lead to rebuild or inspect this checkpoint. A future
general kit helper for coverage-independent RGB baking and periodic tile guard
reconciliation would remove a subtle repeated failure mode; this round keeps
that implementation local rather than changing other families' bake behavior.
