# Guns interface 1.4.0 — swing-out revolver supplement

Additive to [1.0.0](../INTERFACE.md) and the shotgun's 1.1.0 supplement.
Versions 1.2 and 1.3 are the bolt rifle's and the SMG's supplements. This binding
is `src/interface.py`; no existing family module or meaning is changed.

The Meridian Six declares a six-chamber cylinder, double and single action,
manual swing-out reload and a speedloader. It has **no magazine** and no
last-round hold-open. Existing magazine socket names remain compatibility
references, are explicitly inactive, and never request a magazine spawn.
`Root` remains identity; move the complete scene instance for stance/recoil.

Each saved state includes six stable physical chamber IDs, `0..5`, each exactly
`loaded`, `fired`, or `empty`. A fired case remains in its chamber until extraction.
`index` is the number of 60-degree steps from the authored rest; orientation
repeats modulo six. Chamber 0 starts at the top. The firing sequence is
1, 2, 3, 4, 5, 0 because the cylinder indexes **before** the hammer falls.
`action` is `closed`, `moving` or `open`, and `hammer` is `rest` or `cocked`.
The manifest's `snapshot(clip,frame)` returns discrete occupancy and committed
index; the evaluated animation describes motion between those events.

| Clip | Duration | State / events, 60 Hz frames |
| --- | --- | --- |
| Idle | 1 frame | six loaded, index 0 |
| Fire, Fire2–Fire5, FireLast | .70 s each | starts with the preceding chamber state; index f21, stop seated f24, shot f27, reset f38 |
| IdleAfter1–IdleAfter6 | 1 frame | retains each corresponding fired set and index |
| CockHammer | .70 s | indexes f29, stop f32, cocked f36 |
| IdleCocked | 1 frame | six loaded, index 1, hammer held cocked |
| FireSingle | .40 s | starts cocked; shot f4, reset f20; ends like Fire |
| DryFire | .70 s | empty cylinder; indexes, hammer falls f27; no shot event |
| IdleEmpty / IdleDryIndexed | 1 frame | holds empty index 0 / 1 |
| Reload | 3.60 s | latch f12, open f40, rod full f58, cases release f60, clear f80, star home f88, loader enters f104, seated f142, release f144, clear f172, closed f200, latch f208 |
| ReloadSingle | 3.00 s | chamber 0 empty, others loaded; open f40, insertion f76, seated f116, commit f118, hand clear f140, closed f164, latch f172 |
| Inspect | 2.40 s | opens loaded cylinder f40, closes f128, latch f136 |

`FireLast` starts with five fired cases and the last live round, and ends with
six fired cases in the closed cylinder. `Reload` starts in that exact state.
There is no silent conversion of a fired case to an empty chamber on firing.
Reload resets the logical index from 6 to 0 without spinning the geometry
through a full turn; these are the same physical orientation.

The cylinder stop rocks about its transverse pin, retracting before indexing
and seating after alignment or crane closure. CockHammer leaves the trigger
partly rearward (−10°); FireSingle pulls it farther (−15° total), fires and
resets. The corresponding idle holds preserve those visible control poses.

Cartridges, cases and loader rounds have separate STEP visibility channels.
The six cases visibly travel with the star until release, then fall away.
The incoming loader rounds travel on their own guide; f144 hands occupancy to
the chamber objects at the same seated position and presses the loader release.
This is a visual handoff, without a functional lockwork or spring simulation.

Pause at any frame by retaining `{version, clip, frame, state}` from
`interrupt()`. Resume that same clip/time and hold the current pose while paused.
No early exit to a closed idle is promised while the cylinder or loader moves.
The sequential Fire / IdleAfter bindings provide exact pose continuity.
An engine using arbitrary mixed chamber states owns their six visibility
channels and chooses the appropriate live/dry event; it must not replay the
canonical six-live demonstration and overwrite its own ammunition bookkeeping.

| Added socket | Frame and use |
| --- | --- |
| Socket_Cylinder | rides Cylinder; rear axis frame; full affine transform |
| Socket_Speedloader | rides LoaderGuide; spawn the standalone loaded speedloader |
| Socket_Round | rides nonscaling RoundGuide; single-round presentation / spawn frame |

The three added socket frames remain nonsingular even when their display
meshes are hidden. Loader spawn is relevant between loader-enter and loader-clear;
single-round spawn is relevant during its insertion phase. These sockets retain
+Y forward, +Z up, +X right in Blender. Cylinder/crane
rotation changes their full orientation. `Socket_Ejection` remains the static
legacy reference and is inactive for simultaneous revolver extraction. At the
cases-release event, spawn each fired case using its corresponding Case bone
frame, then hide the internal demonstration case if external physics is used.
`Socket_MagWell` and `Socket_Magazine` are likewise inactive compatibility nodes.
The loader and ammunition GLBs use those documented complete local frames.

The source keeps named rigid parts for surface audits. Final delivery consolidates
those weights into one animated skin and one shared 2048 BaseColor / OpenGL
Normal / ORM atlas through the kit delivery path. The cartridge, fired case
and loaded speedloader reuse byte-identical canonical maps in their complete
posed guide frames. Consumers retain imported PBR materials and cache the
canonical atlas/content hashes across separately loaded GLBs.
