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
