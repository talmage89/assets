# Open parking garages — form and construction checkpoint

Two original scripted American parking structures for a 1995–2015 town:
**Alder Quay**, a 1988 municipal precast garage, and **Bellwether Commons**, a
1996 cast-in-place commercial garage. This delivery deliberately stops before
look-dev. Concrete/steel use quick scalar materials; shared native paving,
cars, trees and street luminaires keep their own original library resources.
There is no final gallery or committed docs imagery at this checkpoint.

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
steeper. The Python manifest can be consumed without Blender.

The kit contains double tees, inverted-T and L girders, corbel columns, PT
columns/slabs/beams, spandrels, cable barriers, fixtures, wheel stops, drains,
gates, ticket/pay machines and three tower heights. StructuralBay, EndBay,
RampBay and PTStructuralBay are independently exported mating assemblies.
Precast seats, joint strips, connectors and cast slab anchor patches are
modeled. Major service wear remains the next phase: connector runoff, leaking
joints, spalls, oil, turn rubber, repainted ghosts, roof fading and droppings
must be placement-owned and cause-specific, not repeated marks on each tee.

The complete measured inventory is generated as `build/metrics.md` and
`build/modules.json`. `build/garage-<seed>.json` records every placed piece,
stall, route and occupied actor reservation. Native cars are reported apart.
No parked-car mesh is embedded in the garage's geometry budget.

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
| `build/check.json`, `render-values.json`, `preservation.json` | Fresh-import geometry, construction rays, exposure diagnostics and protected resource hashes |
| `build/site-check.json`, `resources.json` | Complete-site instancing, actor counts, external image hashes and memory estimates |

The footprint origin is the structural rectangle's ground center; front is
Blender −Y, up +Z. glTF maps these to +Z front, +Y up. Preserve the relative
image URIs and cache resolved canonical images. The same images are reused by
both seeds; no source image is copied per garage. Diagnostic embedded GLBs
remain under build/embedded/, not the public delivery path.

| Interaction | Blender local axis / range |
| --- | --- |
| Gate arm | Y, −90…0°; gearbox axle |
| Stair landing doors | Z, 0…95°; garage-facing jambs |
| Ground stair exit | Z, −95…0° relative to its authored side-wall rest pose |
| Elevator leaves | X, 0…±.72m; center-opening pair |
| `Stall_<id>` | Parking-space center, width/depth/level/occupied extras |
| `Drive_Up_*`, `Drive_Down_*` | Two-way aisle/ramp point lists in extras and JSON; native curves in the blend |
| Threshold / module sockets | Ground exit, garage stair/lift interfaces, bearing/stack/bay ends |

There is no armature or authored animation. Elevators have sliding doors and
shallow openings, not a moving car, shaft machinery or a full elevator system.
Garage-facing stair/elevator landings share one face; ground stair exits have
separate openings to the public walk. Openings are real apertures in the walls.

The planned look-dev allocation is **one new 2048² concrete/steel PBR triple**,
about **16 MiB** at 8bpp/map with full mips, shared across every placement and
seed. An additive Ground parking graphics page supplies stall numbers, arrows
and level signs without changing Ground's existing atlas bytes. Its current
quick sheet is 2048² RGBA color, **5⅓ MiB** at the same estimate; normal/ORM
manufacture and final page sizing are deferred. GroundTrim's existing three
2048 maps cost 16 MiB, Ground Concrete's existing triple another 16 MiB;
the native roof luminaire's 1024 triple costs 4 MiB. The garage checkpoint
therefore references 41⅓ MiB of shared mipped images at this uniform estimate,
with no second copy for seed 202. The planned new concrete/steel triple is
additional to these reused resources and has not been manufactured yet.
Presentation additionally reuses Ground asphalt/lawn, native trees and car
resources. Final UV density, bake loss, weathering and material/draw-call
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

[REVIEW](REVIEW.md) records the image critiques and remaining weaknesses.
Measurements distinguish actual surface tests from serialization checks; this
checkpoint does not claim final game readiness. Existing library delivery
bytes are hash-protected and the top-level repository index is left untouched.
