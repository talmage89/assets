# Open parking garages — form and construction checkpoint

Two original scripted American parking structures for a 1995–2015 town:
**Alder Quay**, a 1988 municipal precast garage, and **Bellwether Commons**, a
1996 cast-in-place commercial garage. This delivery deliberately stops before
look-dev. Concrete/steel use quick scalar materials; shared native paving,
cars, trees and street luminaires keep their own original library resources.
There is no committed docs imagery at this checkpoint.

[Municipal hero](renders/checkpoint/101/hero.png) ·
[Commercial hero](renders/checkpoint/202/hero.png) ·
[Complete contact sheet](renders/checkpoint/contact.jpg) ·
[Photographic comparisons](renders/matches/contact.jpg)

| Seed | Structure and plan | Structural footprint | Levels | Ramp |
| --- | --- | --- | ---: | --- |
| 101 | Long-span precast; flat 60ft bay beside a full-rise parking bay | 80.4672 × 36.576m | 4 | 5.7292%, 58.5216m run |
| 202 | Cast PT; flat 60ft bay beside a narrow external speed ramp | 58.5216 × 25.6032m | 3 | 10%, plus 5% end transitions within 36.576m |

Both use 8.5 × 18ft stalls, 24ft two-way aisles and 11ft levels. Towers,
entry gantry and roof poles extend beyond the structural envelope. Published
geometry, authored choices and the limits of the engineering interpretation
are in [REFERENCE](REFERENCE.md); credits and direct sources are in
[SOURCES](refs/SOURCES.md).

The generator in [plan.py](src/plan.py) accepts `seed`, `system`, `levels`,
`tee_count` and `occupancy`. The two proof seeds pin the plans above. Other
seeds vary length, level count and actor placement within the selected system.
An incompatible short parking ramp is rejected rather than silently made
steeper. Bounds are 3–5 levels and 12–24 tee stations, further restricted by
ramp grade. The Python manifest can be consumed without Blender. The Make
graph presents proof seeds 101/202; the core API/CLI accepts other seeds and
explicit bay counts. `python3 src/parameter_check.py` checks 45 valid programs,
33 rejected short ramps and invalid/empty/full occupancy inputs without Blender.

The kit contains double tees, inverted-T and L girders, corbel columns, PT
columns/slabs/beams, spandrels, cable barriers, fixtures, wheel stops, drains,
gates, ticket/pay machines and three tower heights. StructuralBay, EndBay,
RampBay and PTStructuralBay are independently exported mating assemblies.
Precast seats, joint strips, connectors and cast slab anchor patches are
modeled. Central ramp/flat interfaces use paired L girders on separate bearing
seats; the inverted-T module serves level adjoining bays. Major service wear
remains the next phase: connector runoff, leaking
joints, spalls, oil, turn rubber, repainted ghosts, roof fading and droppings
must be placement-owned and cause-specific, not repeated marks on each tee.

Current garage exports, excluding every car:

| Seed | Triangles | Stalls / occupied | Materials (quick) | glTF + BIN bytes |
| --- | ---: | --- | ---: | ---: |
| 101 | 95,672 | 291 / 196 | 16 | 7,864,593 |
| 202 | 44,386 | 76 / 56 | 17 | 3,310,355 |

| Construction module | Triangles |
| --- | ---: |
| DoubleTee | 192 |
| InvertedT | 28 |
| LBeam | 20 |
| ColumnCorbel | 88 |
| CorbelPair | 48 |
| ColumnPlain | 40 |
| PTColumn | 40 |
| PTSlab | 116 |
| PTBeam | 44 |
| Spandrel | 68 |
| CableBarrier | 260 |
| PTGuard | 192 |
| Fixture | 88 |
| WheelStop | 44 |
| Drain | 120 |
| Gate | 128 |
| Ticket | 72 |
| PayStation | 72 |
| Tower | 3,236 |
| Tower3 | 2,276 |
| Tower5 | 4,196 |
| StructuralBay | 968 |
| EndBay | 968 |
| RampBay | 968 |
| PTStructuralBay | 596 |

Two reused native roof poles add 3,180 triangles each; they are included in
each garage total.

These are measured exported counts. Simple beams remain below the indicative
300-triangle modular range because additional tessellation would not change
their form; each module is below 2,000, and each tower below 8,000.

The complete measured inventory is generated as `build/metrics.md` and
`build/modules.json`. `build/garage-<seed>.json` records every placed piece,
stall, route and occupied actor reservation. Native cars are reported apart.
No parked-car mesh is embedded in the garage's geometry budget.

Cars are linked native instances, accounted separately from garage geometry:

| Seed | Garage cars / expanded triangles | Surface cars / triangles | Street cars / triangles | Unique site mesh triangles | Site glTF + BIN bytes |
| --- | --- | --- | --- | ---: | ---: |
| 101 | 196 / 13,222,936 | 0 / 0 | 4 / 259,148 | 659,126 | 36,758,954 |
| 202 | 56 / 3,685,880 | 30 / 2,007,714 | 4 / 274,542 | 680,778 | 37,799,527 |

Expanded actor counts charge every parked placement. The much smaller unique
mesh count reflects shared geometry; it includes the garage, buildings,
landscape and all native vehicle types. These counts describe the actual
checkpoint sites, not an additional garage triangle allowance.

| Output | Use |
| --- | --- |
| `export/ParkingGarage-<seed>.gltf` + `.bin` | Placeable garage, meters, external shared images |
| `export/sites/ParkingGarageSite-<seed>.gltf` + `.bin` | Complete seeded town setting and instanced parked cars; same canonical external images |
| `export/modules/<name>.gltf` + `.bin` | Independent construction and mating modules |
| `export/ParkingGaragePieces.gltf` | Module-sheet arrangement; reset roots before mating |
| `build/garage-<seed>.blend` | Scripted authoring state, including actual drive/pedestrian curves |
| `build/garage-<seed>.json` | Same paths as point lists, stall sockets and piece manifest |
| `renders/checkpoint/<seed>/` | Exported-glTF Cycles hero, above/path, aisle, ramp turn, roof, entry, tower and scale |
| `renders/checkpoint/modules.png`, `contact.jpg` | Module sheet and complete checkpoint contact sheet |
| `renders/matches/*-pair.jpg`, `contact.jpg` | Three white-balanced fitted photographic type comparisons |
| `build/check.json`, `render-values.json`, `preservation.json` | Fresh-import geometry, construction surfaces, exposure diagnostics and protected resource hashes |
| `build/site-check.json`, `resources.json` | Complete-site instancing, actor counts, external image hashes and memory estimates |

The footprint origin is the structural rectangle's ground center; front is
Blender −Y, up +Z. glTF maps these to +Z front, +Y up. Preserve the relative
image URIs and cache resolved canonical images. The same images are reused by
both seeds; no source image is copied per garage. Diagnostic embedded GLBs
remain under build/embedded/, not the public delivery path.

The per-seed authoring blends retain local module templates as well as the
placed `Garage_<seed>` hierarchy. Public exports select only the intended
hierarchy; presentation imports those exports.

Curve point lists in JSON/extras use Blender meters. Convert `(x,y,z)` to
glTF `(x,z,-y)` before applying the garage root transform in a game. The
native Blender curves and serialized point lists describe the same routes.

| Interaction | Blender local axis / range |
| --- | --- |
| Gate arm | Y, −90…0°; gearbox axle |
| Stair landing doors | Z, 0…95°; garage-facing jambs |
| Ground stair exit | Z, 0…95° relative to its authored +90° side-wall rest pose |
| Elevator leaves | X, 0…±.72m; center-opening pair |
| `Stall_<id>` | Parking-space center, width/depth/level/occupied extras |
| `Drive_Up_*`, `Drive_Down_*` | Two-way aisle/ramp point lists in extras and JSON; native curves in the blend |
| Threshold / module sockets | Ground exit, garage stair/lift interfaces, bearing/stack/bay ends |

Beam end sockets denote their column/grid stations. The default EndBay is
36ft long, matching the proof garages. The double-tee bearing sockets sit at
the midpoint between the two pad
undersides at each end. They describe a bearing plane, rather than a solid
contact at the midpoint between the stems.

There is no armature or authored animation. Elevators have sliding doors and
shallow openings, not a moving car, shaft machinery or a full elevator system.
Garage-facing stair/elevator landings share one face; ground stair exits have
separate openings to the public walk. Openings are real apertures in the walls.

The planned look-dev allocation is **one new 2048² concrete/steel PBR triple**,
about **16 MiB** at 8bpp/map with full mips, shared across every placement and
seed. An additive Ground parking graphics page supplies stall numbers, the
accessibility glyph and level/entry signs. Directional arrows reuse GroundTrim's
paint region; Ground's existing atlas bytes are unchanged. Its current
quick sheet is 2048² RGBA color, **5⅓ MiB** at the same estimate; normal/ORM
manufacture and final page sizing are deferred. GroundTrim's existing three
2048 maps cost 16 MiB, Ground Concrete's existing triple another 16 MiB;
the native roof luminaire's 1024 triple costs 4 MiB. The garage checkpoint
therefore references 41⅓ MiB of shared mipped images at this uniform estimate,
with no second copy for seed 202. The planned new concrete/steel triple is
additional to these reused resources and has not been manufactured yet.
Presentation additionally reuses Ground asphalt/lawn, native trees and car
resources. The context hatchback/crossover use scalar form finishes; the
sedan retains its native baked maps. The complete sites reference 126⅔ /
132 MiB of shared images, 132 MiB for their combined cached union: 27 images,
72,601,461 PNG bytes. These include paving, vehicles, trees and context signs.
Downtown and Commercial surface deliveries are absent in this checkout, so their original source generators supply quick context finishes
and original sign pages. Their existing DowntownMasonry / MineralRoof /
Finish and Commercial masonry / Equipment allocations remain the binding
choice for finished context; no replacement building surface set is authored
here. Final UV density, bake loss, weathering and material/draw-call
consolidation are explicitly not certified at this form gate.

Run with installed Blender 5.2, Python/Pillow/NumPy, open DejaVu fonts, Poppler
and flock. Native Ground, street-light, tree and sedan exports are read-only
inputs. Missing downtown/commercial and hatch/crossover context is generated
inside this asset's ignored build/ from their original scripts. No other family
is rebuilt or edited. Every Blender invocation is serialized on the shared
lock; render sets acquire it once. No downloaded code, assets or HDRI is used.

```sh
make -C parking-garage                  # form exports, checks, Cycles views and sheets
make -C parking-garage matches          # three fitted export comparisons
make -C parking-garage check
make -C parking-garage repeat           # deterministic geometry/image/manifest bytes
make -C parking-garage WIDTH=1000 SAMPLES=24 render
```

The site exporter uses the kit's exact-signature tangent guard for one native
PinOak four-decimal rounding boundary. Its accepted value comes from the
immutable native tree input; positions, normals and UVs are unchanged. The
repeat comparison still requires identical bytes, with no comparison tolerance.
Render receipts hash both external glTF and BIN payloads.

[REVIEW](REVIEW.md) records the image critiques and remaining weaknesses.
Measurements distinguish actual surface tests from serialization checks; this
checkpoint does not claim final game readiness. Existing library delivery
bytes are hash-protected and the top-level repository index is left untouched.


The measured checkpoint run was
`make -k WIDTH=1200 SAMPLES=24 all repeat`: exit 0, all form checks passed,
and 70 files / 91,258,230 bytes rebuilt identically. The three precast mating
assemblies pass 48 girder-cap samples and 18 bearing-plane socket checks;
all 60 motion sweeps pass. Sampled aisle minima are 2.6932 / 2.5898m,
and measured van-route minima 2.4892m. The check is discrete surface sampling,
not a continuous swept-car or engineering compliance certificate.
