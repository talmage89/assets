## Cold-build investigation — subdivision parameter charts

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

### Source-workaround trials

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
