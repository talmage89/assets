# Guns interface 1.7.0 — break-action side-by-side supplement

Additive to [1.0.0](../INTERFACE.md), retaining the per-chamber vocabulary of
the revolver's [1.4.0](../revolver/INTERFACE.md) and the shotgun's shell-guide
frames in [1.1.0](../shotgun/INTERFACE.md). The 1.5.0 lever-action and 1.6.0 stamped-receiver supplements retain their
meanings. No existing meaning changes.

This member declares `break_action`, `barrel_count=2`, `double_triggers`,
`automatic_safety`, `extractors` and `magazine=false`. It has no ejectors,
detachable magazine or automatic hold-open. Chamber IDs are stable: **0 right,
1 left**. Each is exactly `loaded`, `fired` or `empty`. Each internal hammer is
`cocked` or `rest` in the manifest only; there is no hidden lockwork geometry.
`action` is `closed`, `moving` or `open`; `safety` is `safe` or `fire`.

The front Trigger fires right, TriggerRear fires left. `Fire` fires right;
`FireLeft` continues from that state. Fired hulls remain in their own chambers.
The consumer owns arbitrary mixed states and dry-fire decisions; the canonical
two-shot demonstration must never overwrite its ammunition bookkeeping.

| Clip | Seconds | Start → end; events at 60 Hz frames |
| --- | ---: | --- |
| Idle | 1/60 | both loaded, cocked, closed, safety off |
| Fire | .50 | right loaded → fired at f5; trigger reset f22 |
| FireLeft | .50 | left loaded → fired at f5; trigger reset f22 |
| Open / OpenLoaded | 1.20 | spent / live pair → open; lever/right and unlocked f12, automatic safe f20, cocked f48, full opening f56, extractor raised f64 |
| Unload | 1.60 | open spent → open empty; grasp f12, hulls axially clear f50, released f68, hand clear f88 |
| Reload | 2.40 | open empty → both loaded; right enters f12, seated f44, committed f46, hand clear f64; left f76/108/110/132 |
| ReloadSingle | 1.40 | right empty, left loaded → both loaded; right f12/44/46/72 |
| Close | 1.20 | open loaded → closed loaded/safe; extractor home f20, barrels closed f56, lever home/locked f64 |
| Safety / SafetyOn | .50 | fire / safe detent reached f20 |
| Inspect | 3.00 | loaded/fire → open → loaded/safe; opening events as above; extractor home f132, closed f164, lever home/locked f172 |

`IdleAfterRight`, `IdleSpent`, `IdleSafe`, `IdleOpenSpent`, `IdleOpenEmpty`,
`IdleOpenOne` and `IdleOpenLoaded` retain those exact control/ammunition poses.
Every clip has complete boundary keys. Root stays identity. Apply stance,
recoil and whole-gun inspect motion to the complete scene instance externally.
Meters, palm origin; Blender +Y forward, +Z up, +X right; glTF −Z forward/+Y up.
The Eye optical frame points down approximately 0.374 degrees from +Y to
the bead. The accepted cheek station remains 35 mm behind the comb nose.
The vertical location now follows the CPSA sporting coin-rule sight picture:
eye Z≈60.500 mm, 42.811 mm above the actual comb, derived from the actual rib
and the bead (see README and refs/SOURCES.md). This is a fitted visual view,
not an anthropometric measurement or a personal ergonomic fit test.
All other socket frames retain the gun basis. This is the same optical-frame
meaning as 1.0.0, with the pitch required by this member's stock and rib.

Extraction lifts both rims without throwing them. `Unload` first draws the
hulls along the chamber axes until their mouths clear, then moves them out
with the external hand. No hand mesh ships: sockets and the visible held
hulls are targets for the consumer's hand IK. There is no instantaneous
conversion from a fired chamber to empty on firing.

The incoming shell is handed from InsertR/L to LiveR/L at the same seated
transform using STEP visibility, with no growing shell. `snapshot(clip,frame)`
returns committed chamber/control states. `interrupt()` retains
`{version,clip,frame,state}`; pause the pose and resume that exact clip/frame.
There is no promised early jump to closed Idle while the gun or hand is moving.

All seven legacy nodes remain. Magazine and mag-well nodes are inactive
compatibility references; no magazine spawn is requested. The static Muzzle
and Ejection are rest/effect references, not animated constraints.

| Added / reused socket | Complete frame |
| --- | --- |
| Socket_SupportHand | rides Forend, following the barrels |
| Socket_Shell | existing 1.1.0 meaning, right hand-insertion guide |
| Socket_ShellL | matching left guide |
| Socket_ChamberR / Socket_ChamberL | head-center frames riding Extractor; also hull grasp/spawn frames |
| Socket_MuzzleR / Socket_MuzzleL | each actual muzzle, riding Barrels |

Guide/socket bones never change scale. Only display children use STEP hiding.
Standalone shell/hull origins are head centered, +Y toward the mouth. Spawn
the hull at its actual HullR/L bone frame when handing it to external physics;
the chamber sockets represent extraction, before the manual pull separates it.
Keep the corresponding internal display hidden after external handoff.

The round-four form gun is `export/sxs.glb`, through the kit's atlas and
animated exporter: one 2048 BaseColor/OpenGL Normal/ORM set with the inspection
constants and baked source normals. Named rigid parts remain at this review
gate for independent contact tests. The native `build/sxs.glb` and standalone
shell/hull GLBs remain diagnostic, unbaked outputs. Final finishes and standalone
small texture sets remain held; this changes no rig, socket, clip or state meaning.
