## Cold-build investigation — subdivision parameter charts

**No production fix adopted.** The changing operation is Blender 5.2.3's
threaded subdivision UV interpolation. Script workarounds made the mesh repeat,
but did not preserve the accepted native cars within the existing guards.
The prototype model, Makefile and exporter changes were reverted. All four
accepted car GLBs, all 35 existing texture PNGs and every docs image retain
their original bytes. No kit or downstream-family file was changed.

Three factory-empty mesh builds per body, in separate folders, are exact at
one thread: X220 **62,880** triangles and H120 **46,737**. Four-thread builds
reproduce the fault: X220 **62,924 / 62,920 / 62,920**, H120
**46,749 / 46,749 / 46,764**. Evidence is in
`build/cars-determinism/{before,threaded}-{suv,hatch}-{0,1,2}/`.
The garage's native adapter uses four threads and bypasses the cars' one-thread
Makefile setting. These are form counts, before the adapter adds exterior parts.

Tracing BMesh inputs/outputs finds the first changed coordinates in the chart
resampling, before any bisect or aperture cut. In the changing H120 pair, all
1,870,529 parent positions, normals, 3,735,552 triangles and corner indices are
exact; **2,976 UV floats** differ, by at most **0.0000076293945 chart units**.
Three resamplings of one frozen parent are exact, including all 12,697 X220
query results. The spatial query is not the source of that variation.

A narrower reproduction evaluates just the final subdivision modifier on one
fixed input: positions and topology repeat, but native interpolated UVs have
three hashes across three fresh four-thread processes. The standalone
[subdivision probe](src/subdivision_probe.py) prepares that input from the
scripted control net and records independent receipts; its docstring gives
the commands. Scratch receipts and intermediate arrays are in
`build/cars-determinism/`.

The cars use those UVs as geometric parameters, so last-bit chart drift moves
sampled skin points and changes tolerance-sensitive clipping/gauge allocation.
Both authored charts are regular integer grids; their five subdivision levels
have an exact **1/32** parameter lattice. This is an internal construction
chart, separate from the delivery's later atlas unwrap.

In the changing X220 four-thread pair, the final mesh differences are in
`Liftgate outer`, `Rear molded fascia`, `Rear quarter_L` and the rear lower
bumper cladding;
the liftgate changes from 2,860 to 2,856 triangles. In H120 the changing
meshes include the rear fascia and right rear quarter, which change from
5,238 to 5,250 and 2,403 to 2,406 triangles. The first differing BMesh input
is already the resampled sheet; bisects, aperture cuts and gauge allocation
amplify the parameter difference rather than originating it.

### Rejected source-workaround trials

An experimental lattice restoration removes the varying subdivision values.
The isolated modifier probe produces one canonical UV hash from three different
native UV hashes. Restoring the exact lattice also exposes existing sensitivity
in subsequent construction; it is not yet an adopted delivery fix.

The first X220 trial has 63,690 form triangles: a rejected rear gauge patch
causes the entire panel's back reduction to be discarded. Preserving that
patch's boundary when retrying the reduction, using 180 mm rear gauge cells,
keeps the mesh closed and the complete exposed triangle soup unchanged. Three
fresh four-thread form builds then finish at **62,916** triangles. The depth
and manifold checks retain their original limits.

The H120 trial stops at the existing aperture-coverage gate: one rear fascia
fragment has a **0.0000229806634 m** gap against the unchanged **0.000020 m**
limit. Log: `build/cars-determinism/fixed2-hatch-0/build.log`. These trial results
do not establish a valid export, a surface-tolerance pass, or cold baked-map
identity. Accepted exports, maps and documentation images remain untouched.

### Prototype mesh-stage proof (not an adopted delivery)

`regular_chart.restore()` restores the authored lattice after each subdivision.
It rejects nonfinite coordinates and charts farther than 0.0001 units from the
expected lattice, rather than quantizing arbitrary UVs. It changes construction
parameters only; it never rounds positions, normals or the delivery atlas.
No environment variable or caller thread count is pinned.

The H120 coverage failure above is a float32 BVH false positive: the complete
old skinny triangle is present, with exactly the same three coordinates, in the
new triangulation. Recognizing that exact footprint proves coverage everywhere
on that triangle. Changed triangles still pass the original sampled physical
gate. The captured regression has zero misses with the triangle present, and
one miss at 0.0000229806634 m when that triangle is removed. Reducing CDT's
epsilon from 1e-7 to 1e-10 does not repair the false spatial-query result.

X220 first attempts its established gauge reduction. Only a rejected, unclosed
rear-fascia candidate retries with 180 mm cells and the rejected boundaries
pinned. The original gauge-depth, closed-mesh and exact exterior-soup tests
remain mandatory. Other panels retain their established allocation.

Three fresh four-thread builds per body now give exact vertices, polygons,
corner normals, transforms, parents and material assignments:

| Body | Form triangles, all three builds | Mesh-array receipt, not a GLB hash |
| --- | ---: | --- |
| X220 | 62,916 | `87a5e6979799efe795ca8728aaedadf114e23556ad1bc1fafb0aa334f588ac87` |
| H120 | 46,698 | `cc39975696ef957f54c3e8a6b350806dcdac4a166b239f650914f78ab87d3303` |

The independent kit source audits pass for both bodies, including scale,
normals, topology and their source budgets. Receipts are
`build/cars-determinism/fixed3-{suv,hatch}-audit.json`; complete cold source
folders are `fixed3-{suv,hatch}-{0,1,2}`. Export/map byte identity and accepted
surface comparisons remain separate delivery gates.

### Preservation stop

The unmodified garage guard rejected the complete native X220 prototype:
**73,416** triangles against **73,426** (0.01362%, inside 0.1%), but a sampled
rear-fascia return was **1.02705 mm** away (outside 1 mm). All other named
meshes were below 0.323 mm. A subsequent cached rear-return-only 170 mm cell
trial retained 3,068 triangles and reduced that part's sampled error to
0.584883 mm; it did not complete a new whole-car cold proof.

The native H120 prototype was rejected at **58,145** against **58,032**
triangles (0.19472%), with **36.9832 mm** sampled optical-housing displacement.
Its housing/guide geometry is rebuilt from a fitted, retessellated lens; tiny
parameter changes can therefore change much more than the original cut skin.
Restricting lattice restoration to the final subdivision, leaving the already
repeatable first-stage UVs intact, still failed at **58,142** triangles and
the same 36.9832 mm maximum. No tolerance was widened and no candidate adopted.

Receipts: `build/cars-determinism/native/crossover-guard.json`,
`native-final/hatchback-0/guard.json`, `native-narrow/hatchback/guard.json`.
Per-object distances are in `native/details-{crossover,hatchback}.json`.
Rejected source files and the patch are archived only under the ignored
`build/cars-determinism/prototype-source/` folder; the model scripts are restored.

This stops short of a preservation-safe source fix. Three cold shipped
GLB/map builds, `make check` and `make repeat` are **not** claimed. No bake or
render was run. Changing Blender's operation, or introducing a separately
validated serialized native-car build, needs further work; changing an
environment in a person's shell would not repair the native imported callers.

### Reproduce the native operation

From the cars directory, prepare one original control net, stopping immediately
before its final subdivision, then evaluate that same frozen input in fresh
processes. Only ignored build artifacts and JSON receipts are written:

```sh
blender -t 4 -b --factory-startup --python-exit-code 1 \
  --python src/subdivision_probe.py -- --prepare suv --out build/chart-probe/input.blend
for i in 1 2 3; do
  blender -t 4 -b --factory-startup --python-exit-code 1 \
    --python src/subdivision_probe.py -- --source build/chart-probe/input.blend \
    --out build/chart-probe/run-$i.json --canonical
done
```

`positions_sha256` and `topology_sha256` stay exact while
`native_uv_sha256` can differ. `--canonical` only hashes the mathematical
1/32 lattice as a diagnostic; it does not patch or adopt a mesh. The smaller
17×17 flat-sheet test was exact in three runs, so the frozen car control net
is the narrowest reproduction established here.

The final fresh-input verification is in
`build/cars-determinism/final-probe/summary.json`. Three four-thread evaluations
of one frozen X220 input gave the following native UV hashes:

| Run | Native UV SHA-256 |
| --- | --- |
| 1 | `5d2ac605d50999b4930a4ca50cb775b12424f75c81a0fe7446a0f4a6acbd2315` |
| 2 | `fb1ab22459cd90a421ad618aabed399bb540ffdad9cfce1645ceaf5e24b7b055` |
| 3 | `bed4cfbffe29f06f40747d075756a892e528f47d85185561e9b2c90554e271c0` |

All three have 1,948,417 positions and 7,782,400 corners, with position hash
`5554aa284f5436d6f2ba2c2648bb836c3a405d4680aa44b449f0090afb110bde`
and topology hash
`011e9f089c125fb83fd79e89e5d06362ee644e8c1251acc900e517d345c6739a`.
Three one-thread controls retain those same arrays and all have the second
UV hash, `fb1ab224…`. This is an operator/channel reproduction, not a claim
of cold GLB or texture identity.

The hatch preparation mode was also rebuilt and exercised with three
four-thread and three one-thread evaluations. That frozen H120 input was
exact in all six, UV hash
`a9f60e2715d9be8a47cac4593a0d46749687121182f8ae639a9e67ff90d6542b`.
It does not independently reproduce the H120 variation seen in the full hot
builds; the captured full-build parent arrays above establish that divergence.
Receipt: `build/cars-determinism/final-probe-hatch/summary.json`.

### Preserved deliveries and consumer guards

Independent final file hashing confirms **four GLBs, 35 texture PNGs and
19 docs images** unchanged. Each GLB still has four materials and three
embedded 2048² PNGs. Receipt: `build/cars-determinism/preservation-final.json`.

| Car | Triangles | GLB bytes | Unchanged GLB SHA-256 |
| --- | ---: | ---: | --- |
| C150 | 59,838 | 11,530,736 | `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65` |
| S240 | 69,658 | 10,140,724 | `3b907074594759b4247e379b1535a4700f3ecdbcfcd67cd1b967390c2fe1ebfa` |
| X220 | 64,933 | 9,061,700 | `75fc9507347fbc96ae0af8204a59168f63098eeee8a9dd43362ad350a75c1e82` |
| H120 | 59,852 | 7,892,248 | `86104add5c3aaa7bf909af12fc666f9a0ef87f635df2b0e7ce7639c247f1136e` |

No downstream guard can become exact on the evidence in this branch alone.
After a preservation-safe fix, the native cache policy in
`parking-garage/src/dependencies.py` and `context_guard.py` needs three exact
cold native GLBs per recipe, new accepted hashes, and exact cache validation
before removing retries. `context_repeat.py` can then assert its existing
`identical` result instead of accepting only the geometric comparison.

The mixed-site exception in `context_embedded.py` / `embedded_repeat.py`, used
by the garage's repeat paths, additionally needs accepted sites rebuilt once
from those fixed car inputs and exact repeats of their car payloads. Non-car
nodes must continue passing their existing exact checks. Families with private
native-car/host caches or immutable library-car receipts need those inputs and
receipts refreshed after the fix, followed by their own repeat check. None of
those guards, caches, receipts or family deliveries was changed here.

### Additional H120 byte-identity obstacle

`hatch_detail.py` stores the input **blend-container** SHA-256 in scene
`form_source_sha256`; the original finalization/export retains it in the GLB's
scene extras. The three original one-thread H120 form builds have identical
mesh arrays but three different blend-file hashes, recorded in
`build/cars-determinism/hatch-container-hashes.json`. The accepted GLB currently
contains `6443725b18cc77d01825c713c075ef3f1cf8d2d14314040064c2ce020fc5ec81`.
Fixing mesh repeat alone therefore does not establish complete GLB byte repeat:
the delivery must omit this serialization receipt or replace it with a stable
scene-content receipt, while preserving binary provenance separately for audits.
The trial removed it from the finalized scene only; that production change
was also reverted when the geometry workaround failed preservation.
